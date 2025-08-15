import json
import os
import requests
from dotenv import load_dotenv

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

def process_document(pdf_path):
    """
    Process a PDF document using Landing AI's Vision Agent API.
    
    Args:
        pdf_path (str): Path to the PDF file to process
        
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
        
        return extracted_info
        
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {e}")
    except KeyError as e:
        raise ValueError(f"Unexpected API response format: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from API: {e}")

def main():
    """Main function to demonstrate usage of the process_document function."""
    
    # Get configuration from environment variables
    base_pdf_path = os.getenv('BASE_PDF_PATH')
    if not base_pdf_path:
        raise ValueError("BASE_PDF_PATH not found in environment variables. Please set it in your .env file.")

    pdf_name = os.getenv('PDF_NAME')
    if not pdf_name:
        raise ValueError("PDF_NAME not found in environment variables. Please set it in your .env file.")

    pdf_path = f"{base_pdf_path}/{pdf_name}"
    
    handle_document(pdf_path)

def handle_document(pdf_path):
    try:
        # Process the document
        result = process_document(pdf_path)
        
        # Print the results
        handle_result(result)
            
    except Exception as e:
        print(f"Error processing document: {e}")

def handle_result(result):
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
