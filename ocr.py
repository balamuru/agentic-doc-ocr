import json
import os
import requests
import tempfile
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from dotenv import load_dotenv
import PyPDF2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
VA_API_KEY = os.getenv('VISION_AGENT_API_KEY')
if not VA_API_KEY:
    raise ValueError("VISION_AGENT_API_KEY not found in environment variables. Please set it in your .env file.")

# Define the schema globally
SCHEMA = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "API Response for Products",
  "description": "A schema for a list of products returned from an API, representing ALL floral arrangements (S, M, L sizes) extracted from the markdown document.",
  "type": "object",
  "properties": {
    "products": {
      "title": "Product List",
      "description": "An array of product objects, each representing a specific floral arrangement in ALL available sizes (S, M, L). Extract each size as a separate product with the appropriate size suffix in the ID.",
      "type": "array",
      "items": {
        "type": "object",
        "title": "Product",
        "description": "A single product (floral arrangement) with its details for a specific size.",
        "properties": {
          "id": {
            "type": "string",
            "title": "Product ID",
            "description": "Unique identifier for the product with size suffix, such as '197766S', '197766M', '197766L', '197756S', '197756M', '197756L'."
          },
          "name": {
            "type": "string",
            "title": "Product Name",
            "description": "Name of the product, such as 'Petal Palooza' or 'Field Study'."
          },
          "size": {
            "type": "string",
            "title": "Product Size",
            "description": "Size of the product (S, M, or L)."
          },
          "price": {
            "type": "number",
            "title": "Product Price",
            "description": "Suggested retail price of the product in USD for this specific size."
          },
          "flower-data": {
            "type": "string",
            "title": "Flower Data",
            "description": "Type and number of flowers in the arrangement for this specific size, e.g., '2 stems Hydrangea - Blue, 4 stems Carnation - Orange'."
          },
          "foliage-data": {
            "type": "string",
            "title": "Foliage Data",
            "description": "Type and number of foliage in the arrangement for this specific size, e.g., '3 stems Tree Fern - Painted, 1 stem Eucalyptus - Gunni'."
          },
          "dimensions": {
            "type": "string",
            "title": "Dimensions",
            "description": "Dimensions of the arrangement for this specific size, e.g., 'Arrangement Height 11\", Length 10\"'."
          },
          "construction-material": {
            "type": "string",
            "description": "description of the construction material eg 6\" gathering vase - clear"
          }
        },
        "required": [
          "id",
          "name",
          "size",
          "price",
          "flower-data",
          "foliage-data",
          "dimensions",
          "construction-material"
        ]
      }
    }
  },
  "required": [
    "products"
  ]
}

def split_pdf_by_pages(pdf_path):
    """
    Split a PDF file into individual pages.
    
    Args:
        pdf_path (str): Path to the PDF file to split
        
    Returns:
        list: List of temporary file paths for each page
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: If PDF processing fails
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    page_files = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            logger.info(f"Splitting PDF with {total_pages} pages")
            
            for page_num in range(total_pages):
                # Create a temporary file for this page
                temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
                temp_path = temp_file.name
                temp_file.close()
                
                # Create a PDF writer for this page
                pdf_writer = PyPDF2.PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_num])
                
                # Write the page to the temporary file
                with open(temp_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                page_files.append((page_num + 1, temp_path))  # page_num + 1 for 1-based indexing
                logger.info(f"Created page {page_num + 1} at {temp_path}")
                
    except Exception as e:
        # Clean up any temporary files created so far
        for _, temp_path in page_files:
            try:
                os.unlink(temp_path)
            except:
                pass
        raise Exception(f"Failed to split PDF: {e}")
    
    return page_files

def process_document(pdf_path, page_num=None):
    """
    Process a PDF document using Landing AI's Vision Agent API.
    
    Args:
        pdf_path (str): Path to the PDF file to process
        page_num (int, optional): Page number being processed (for logging)
        
    Returns:
        dict: Extracted product information in JSON format
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        ValueError: If API key is missing or invalid
        requests.RequestException: If API request fails
    """
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Get file name from path
    pdf_name = os.path.basename(pdf_path)
    
    page_info = f" (Page {page_num})" if page_num else ""
    logger.info(f"Processing document: {pdf_name}{page_info}")
    
    headers = {"Authorization": f"Basic {VA_API_KEY}"}
    url = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"

    files = [
        ("pdf", (pdf_name, open(pdf_path, "rb"), "application/pdf")),
    ]

    payload = {"fields_schema": json.dumps(SCHEMA)}

    try:
        response = requests.request("POST", url, headers=headers, files=files, data=payload)
        response.raise_for_status()  # Raise exception for bad status codes
        
        output_data = response.json()["data"]
        extracted_info = output_data["extracted_schema"]
        
        logger.info(f"Successfully processed {pdf_name}{page_info}")
        return extracted_info
        
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed for {pdf_name}{page_info}: {e}")
    except KeyError as e:
        raise ValueError(f"Unexpected API response format for {pdf_name}{page_info}: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from API for {pdf_name}{page_info}: {e}")

def process_page_parallel(page_info):
    """
    Process a single page in parallel.
    
    Args:
        page_info (tuple): Tuple of (page_num, temp_file_path)
        
    Returns:
        tuple: (page_num, result_dict) or (page_num, error_message)
    """
    page_num, temp_path = page_info
    
    try:
        result = process_document(temp_path, page_num)
        return (page_num, result)
    except Exception as e:
        logger.error(f"Error processing page {page_num}: {e}")
        return (page_num, {"error": str(e)})
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except:
            pass

def create_output_directory(pdf_filename=None):
    """
    Create the output directory structure with timestamp and optional filename.
    
    Args:
        pdf_filename (str, optional): Name of the PDF file being processed
        
    Returns:
        str: Path to the created output directory
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    if pdf_filename:
        # Remove extension and sanitize filename for directory name
        filename_without_ext = Path(pdf_filename).stem
        # Replace any problematic characters with underscores
        safe_filename = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename_without_ext)
        output_dir = Path(f"output/{timestamp}-{safe_filename}")
    else:
        output_dir = Path(f"output/{timestamp}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Created output directory: {output_dir}")
    return output_dir

def save_page_result(output_dir, page_num, result):
    """
    Save the result for a specific page to a numbered directory.
    
    Args:
        output_dir (Path): Base output directory
        page_num (int): Page number
        result (dict): Result data to save
    """
    page_dir = output_dir / f"{page_num:03d}"  # Zero-padded 3-digit page number
    page_dir.mkdir(exist_ok=True)
    
    # Save the result as JSON
    result_file = page_dir / "result.json"
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Save a summary text file
    summary_file = page_dir / "summary.txt"
    with open(summary_file, 'w') as f:
        f.write(f"Page {page_num} Processing Results\n")
        f.write("=" * 40 + "\n\n")
        
        if "error" in result:
            f.write(f"ERROR: {result['error']}\n")
        else:
            f.write(f"Number of products found: {len(result.get('products', []))}\n\n")
            
            for i, product in enumerate(result.get('products', []), 1):
                f.write(f"Product {i}:\n")
                f.write(f"  ID: {product.get('id', 'N/A')}\n")
                f.write(f"  Name: {product.get('name', 'N/A')}\n")
                f.write(f"  Size: {product.get('size', 'N/A')}\n")
                f.write(f"  Price: ${product.get('price', 'N/A')}\n")
                f.write(f"  Flower Data: {product.get('flower-data', 'N/A')}\n")
                f.write(f"  Foliage Data: {product.get('foliage-data', 'N/A')}\n")
                f.write(f"  Dimensions: {product.get('dimensions', 'N/A')}\n")
                f.write(f"  Construction Material: {product.get('construction-material', 'N/A')}\n\n")
    
    logger.info(f"Saved results for page {page_num} to {page_dir}")

def process_pdf_by_pages(pdf_path, max_workers=4):
    """
    Process a PDF by splitting it into pages and processing each page in parallel.
    
    Args:
        pdf_path (str): Path to the PDF file to process
        max_workers (int): Maximum number of parallel workers
        
    Returns:
        dict: Summary of processing results
    """
    logger.info(f"Starting PDF processing: {pdf_path}")
    
    # Get filename for output directory
    pdf_filename = os.path.basename(pdf_path)
    
    # Create output directory
    output_dir = create_output_directory(pdf_filename)
    
    # Split PDF into pages
    page_files = split_pdf_by_pages(pdf_path)
    
    if not page_files:
        logger.warning("No pages found in PDF")
        return {"error": "No pages found in PDF"}
    
    logger.info(f"Processing {len(page_files)} pages with {max_workers} workers")
    
    # Process pages in parallel
    results = {}
    successful_pages = 0
    failed_pages = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all pages for processing
        future_to_page = {executor.submit(process_page_parallel, page_info): page_info[0] 
                         for page_info in page_files}
        
        # Collect results as they complete
        for future in as_completed(future_to_page):
            page_num, result = future.result()
            results[page_num] = result
            
            # Save result to file
            save_page_result(output_dir, page_num, result)
            
            # Update counters
            if "error" in result:
                failed_pages += 1
            else:
                successful_pages += 1
    
    # Create summary file
    summary_file = output_dir / "processing_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(f"PDF Processing Summary\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Input PDF: {pdf_path}\n")
        f.write(f"Total pages: {len(page_files)}\n")
        f.write(f"Successful pages: {successful_pages}\n")
        f.write(f"Failed pages: {failed_pages}\n")
        f.write(f"Processing completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for page_num in sorted(results.keys()):
            result = results[page_num]
            if "error" in result:
                f.write(f"Page {page_num}: ERROR - {result['error']}\n")
            else:
                f.write(f"Page {page_num}: SUCCESS - {len(result.get('products', []))} products found\n")
    
    # Create combined results file
    combined_file = output_dir / "combined_results.json"
    with open(combined_file, 'w') as f:
        json.dump({
            "summary": {
                "total_pages": len(page_files),
                "successful_pages": successful_pages,
                "failed_pages": failed_pages,
                "processing_timestamp": datetime.now().isoformat()
            },
            "page_results": results
        }, f, indent=2)
    
    logger.info(f"Processing complete. Results saved to: {output_dir}")
    logger.info(f"Summary: {successful_pages} successful, {failed_pages} failed")
    
    return {
        "output_directory": str(output_dir),
        "total_pages": len(page_files),
        "successful_pages": successful_pages,
        "failed_pages": failed_pages,
        "results": results
    }

def main():
    """Main function to demonstrate usage of the improved PDF processing."""
    
    # Get configuration from environment variables
    base_pdf_path = os.getenv('BASE_PDF_PATH')
    if not base_pdf_path:
        raise ValueError("BASE_PDF_PATH not found in environment variables. Please set it in your .env file.")

    pdf_name = os.getenv('PDF_NAME')
    if not pdf_name:
        raise ValueError("PDF_NAME not found in environment variables. Please set it in your .env file.")

    pdf_path = f"{base_pdf_path}/{pdf_name}"
    
    # Get max workers from environment (default to 4)
    max_workers = int(os.getenv('MAX_WORKERS', '4'))
    
    try:
        result = process_pdf_by_pages(pdf_path, max_workers)
        print(f"\nProcessing Summary:")
        print(f"Output directory: {result['output_directory']}")
        print(f"Total pages: {result['total_pages']}")
        print(f"Successful: {result['successful_pages']}")
        print(f"Failed: {result['failed_pages']}")
        
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        print(f"Error: {e}")

def handle_document(pdf_path):
    """Legacy function for backward compatibility."""
    try:
        # Process the document (single page mode)
        result = process_document(pdf_path)
        
        # Print the results
        handle_result(result)
            
    except Exception as e:
        print(f"Error processing document: {e}")

def handle_result(result):
    """Legacy function for backward compatibility."""
    print("=== YOUR DESIRED OUTPUT ===")
    print(json.dumps(result, indent=2))

    # Print detailed information about the extracted products
    print("\n=== EXTRACTED PRODUCTS ===")
    print(f"Number of products found: {len(result['products'])}")

    # Print formatted JSON
    print("\n=== FORMATTED JSON OUTPUT ===")
    print(json.dumps(result, indent=2))

    # Print each product separately for better readability
    print("\n=== INDIVIDUAL PRODUCTS ===")
    for i, product in enumerate(result['products'], 1):
        print(f"\nProduct {i}:")
        print(f"  ID: {product['id']}")
        print(f"  Name: {product['name']}")
        print(f"  Size: {product['size']}")
        print(f"  Price: ${product['price']}")
        print(f"  Flower Data: {product['flower-data']}")
        print(f"  Foliage Data: {product['foliage-data']}")
        print(f"  Dimensions: {product['dimensions']}")
        print(f"  Construction Material: {product['construction-material']}")

if __name__ == "__main__":
    main()
