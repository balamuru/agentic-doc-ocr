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

base_pdf_path = os.getenv('BASE_PDF_PATH')
if not base_pdf_path:
    raise ValueError("BASE_PDF_PATH not found in environment variables. Please set it in your .env file.")

pdf_name = os.getenv('PDF_NAME')
if not pdf_name:
    raise ValueError("PDF_NAME not found in environment variables. Please set it in your .env file.")

headers = {"Authorization": f"Basic {VA_API_KEY}"}
url = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"

pdf_path = f"{base_pdf_path}/{pdf_name}"

# Define your schema
schema = {
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

files = [
    ("pdf", (pdf_name, open(pdf_path, "rb"), "application/pdf")),
]

payload = {"fields_schema": json.dumps(schema)}

response = requests.request("POST", url, headers=headers, files=files, data=payload)

output_data = response.json()["data"]
extracted_info = output_data["extracted_schema"]

# This is your desired output - clean, structured product data
print("=== YOUR DESIRED OUTPUT ===")
print(json.dumps(extracted_info, indent=2))

# Print detailed information about the extracted products
print("\n=== EXTRACTED PRODUCTS ===")
print(f"Number of products found: {len(extracted_info['products'])}")

# Print formatted JSON
print("\n=== FORMATTED JSON OUTPUT ===")
print(json.dumps(extracted_info, indent=2))

# Print each product separately for better readability
print("\n=== INDIVIDUAL PRODUCTS ===")
for i, product in enumerate(extracted_info['products'], 1):
    print(f"\nProduct {i}:")
    print(f"  ID: {product['id']}")
    print(f"  Name: {product['name']}")
    print(f"  Size: {product['size']}")
    print(f"  Price: ${product['price']}")
    print(f"  Flower Data: {product['flower-data']}")
    print(f"  Foliage Data: {product['foliage-data']}")
    print(f"  Dimensions: {product['dimensions']}")
    print(f"  Construction Material: {product['construction-material']}")

# Uncomment the line below to see the full API response
# print("\n=== FULL API RESPONSE ===")
# print(json.dumps(response.json(), indent=2))
