#!/usr/bin/env python3
"""
Example usage of the improved OCR functionality.

This script demonstrates how to use the new page-by-page PDF processing
with parallel execution and organized output structure.
"""

import os
from ocr import process_pdf_by_pages, process_document

def example_single_page():
    """Example of processing a single page (legacy mode)."""
    print("=== Single Page Processing Example ===")
    
    # You would need to set these environment variables or modify the path
    pdf_path = "sampledata/sample-good.pdf"  # Adjust path as needed
    
    if os.path.exists(pdf_path):
        try:
            result = process_document(pdf_path)
            print(f"Successfully processed single page: {len(result.get('products', []))} products found")
        except Exception as e:
            print(f"Error processing single page: {e}")
    else:
        print(f"PDF file not found: {pdf_path}")

def example_multi_page():
    """Example of processing a multi-page PDF with parallel processing."""
    print("\n=== Multi-Page Processing Example ===")
    
    # You would need to set these environment variables or modify the path
    pdf_path = "sampledata/sample-multi.pdf"  # Adjust path as needed
    
    if os.path.exists(pdf_path):
        try:
            # Process with 4 parallel workers
            result = process_pdf_by_pages(pdf_path, max_workers=4)
            
            print(f"Processing completed!")
            print(f"Output directory: {result['output_directory']}")
            print(f"Total pages: {result['total_pages']}")
            print(f"Successful pages: {result['successful_pages']}")
            print(f"Failed pages: {result['failed_pages']}")
            
            # Show results for each page
            print("\nPage Results:")
            for page_num in sorted(result['results'].keys()):
                page_result = result['results'][page_num]
                if 'error' in page_result:
                    print(f"  Page {page_num}: ERROR - {page_result['error']}")
                else:
                    product_count = len(page_result.get('products', []))
                    print(f"  Page {page_num}: SUCCESS - {product_count} products")
                    
        except Exception as e:
            print(f"Error processing multi-page PDF: {e}")
    else:
        print(f"PDF file not found: {pdf_path}")

def example_with_custom_workers():
    """Example with custom number of workers."""
    print("\n=== Custom Workers Example ===")
    
    pdf_path = "sampledata/sample-good.pdf"  # Adjust path as needed
    
    if os.path.exists(pdf_path):
        try:
            # Process with 2 parallel workers (useful for slower connections)
            result = process_pdf_by_pages(pdf_path, max_workers=2)
            
            print(f"Processing with 2 workers completed!")
            print(f"Output directory: {result['output_directory']}")
            
        except Exception as e:
            print(f"Error processing with custom workers: {e}")
    else:
        print(f"PDF file not found: {pdf_path}")

if __name__ == "__main__":
    print("OCR Processing Examples")
    print("=" * 50)
    
    # Check if environment variables are set
    if not os.getenv('VISION_AGENT_API_KEY'):
        print("WARNING: VISION_AGENT_API_KEY not set in environment variables.")
        print("Please set it in your .env file or environment.")
        print()
    
    # Run examples
    example_single_page()
    example_multi_page()
    example_with_custom_workers()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nOutput Structure:")
    print("output/")
    print("└── YYYYMMDD-HHMMSS/")
    print("    ├── 001/")
    print("    │   ├── result.json")
    print("    │   └── summary.txt")
    print("    ├── 002/")
    print("    │   ├── result.json")
    print("    │   └── summary.txt")
    print("    ├── processing_summary.txt")
    print("    └── combined_results.json")
