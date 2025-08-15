# Agentic Document OCR

[![GitHub](https://img.shields.io/badge/GitHub-View%20on%20GitHub-blue?logo=github)](https://github.com/balamuru/agentic-doc-ocr)

A Python-based document OCR system that uses Landing AI's Vision Agent API to extract structured data from PDF documents. This project is specifically designed to extract product information from floral arrangement catalogs, but can be adapted for other document types.

## Features

- 🔍 **Intelligent Document Parsing**: Uses Landing AI's Vision Agent API for advanced document understanding
- 📊 **Structured Data Extraction**: Extracts product information in JSON format
- 🎯 **Multi-size Product Support**: Automatically extracts all product sizes (S, M, L) from catalog documents
- 🔧 **Environment-based Configuration**: Secure configuration management using `.env` files
- 📋 **Comprehensive Product Data**: Extracts ID, name, size, price, flower data, foliage data, dimensions, and construction materials

## Prerequisites

- Python 3.13.3 or higher
- Landing AI API key
- PDF documents to process

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/balamuru/agentic-doc-ocr.git
   cd agentic-doc-ocr
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` with your actual values:
   ```bash
   # Landing AI API Configuration
   VISION_AGENT_API_KEY=your_landing_ai_api_key_here
   
   # File Path Configuration
   BASE_PDF_PATH=/path/to/your/pdf/directory
   PDF_NAME=your_document.pdf
   ```

## Usage

### Basic Usage

1. **Place your PDF file** in the directory specified by `BASE_PDF_PATH`
2. **Update the PDF name** in your `.env` file
3. **Run the OCR script**:
   ```bash
   python ocr.py
   ```

### Example Output

The script will extract structured data from your PDF and output multiple products with all size variations:

```json
{
  "products": [
    {
      "id": "197766S",
      "name": "Petal Palooza",
      "size": "S",
      "price": 39.99,
      "flower-data": "1 stem Hydrangea - Blue, 2 stems Carnation - Orange, 1 stem Spray Roses - Hot Pink, 1 stem Daisy - Purple, 1 stem Alstroemeria - Orange",
      "foliage-data": "2 stems Tree Fern - Painted, 0 stems Eucalyptus - Gunni",
      "dimensions": "Arrangement Height 9\", Length 7\"",
      "construction-material": "6\" Gathering Vase - Clear"
    },
    {
      "id": "197766M",
      "name": "Petal Palooza",
      "size": "M",
      "price": 49.99,
      "flower-data": "2 stems Hydrangea - Blue, 4 stems Carnation - Orange, 2 stems Spray Roses - Hot Pink, 2 stems Daisy - Purple, 2 stems Alstroemeria - Orange",
      "foliage-data": "3 stems Tree Fern - Painted, 1 stem Eucalyptus - Gunni",
      "dimensions": "Arrangement Height 11\", Length 10\"",
      "construction-material": "6\" Gathering Vase - Clear"
    },
    {
      "id": "197766L",
      "name": "Petal Palooza",
      "size": "L",
      "price": 59.99,
      "flower-data": "3 stems Hydrangea - Blue, 6 stems Carnation - Orange, 3 stems Spray Roses - Hot Pink, 3 stems Daisy - Purple, 3 stems Alstroemeria - Orange",
      "foliage-data": "3 stems Tree Fern - Painted, 2 stems Eucalyptus - Gunni",
      "dimensions": "Arrangement Height 12\", Length 11\"",
      "construction-material": "6\" Gathering Vase - Clear"
    },
    {
      "id": "197756S",
      "name": "Field Study",
      "size": "S",
      "price": 39.99,
      "flower-data": "2 stems Alstroemeria - White, 2 stems Roses - Peach, 1 stem Button Pom - Purple, 1 stem Wax - Blush, 1 stem Mini Carnation - Peach",
      "foliage-data": "1 stem Huckleberry",
      "dimensions": "Arrangement Height 13\", Length 10\"",
      "construction-material": "6\" Gathering Vase - Clear"
    },
    {
      "id": "197756M",
      "name": "Field Study",
      "size": "M",
      "price": 49.99,
      "flower-data": "4 stems Alstroemeria - White, 4 stems Roses - Peach, 2 stems Button Pom - Purple, 2 stems Wax - Blush, 2 stems Mini Carnation - Peach",
      "foliage-data": "2 stems Huckleberry",
      "dimensions": "Arrangement Height 15\", Length 11\"",
      "construction-material": "6\" Gathering Vase - Clear"
    },
    {
      "id": "197756L",
      "name": "Field Study",
      "size": "L",
      "price": 59.99,
      "flower-data": "6 stems Alstroemeria - White, 6 stems Roses - Peach, 3 stems Button Pom - Purple, 3 stems Wax - Blush, 3 stems Mini Carnation - Peach",
      "foliage-data": "3 stems Huckleberry",
      "dimensions": "Arrangement Height 17\", Length 12\"",
      "construction-material": "6\" Gathering Vase - Clear"
    }
  ]
}
```

**Key Features Demonstrated:**
- **Multiple Products**: 2 different floral arrangements (Petal Palooza & Field Study)
- **Size Variations**: Each product available in S, M, L sizes (6 total products)
- **Detailed Specifications**: Complete flower and foliage breakdowns
- **Pricing Structure**: Different prices for each size ($39.99, $49.99, $59.99)
- **Dimensions**: Specific measurements for each arrangement size

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VISION_AGENT_API_KEY` | Your Landing AI Vision Agent API key | Yes |
| `BASE_PDF_PATH` | Directory containing PDF files | Yes |
| `PDF_NAME` | Name of the PDF file to process | Yes |
| `DEBUG` | Enable debug mode (True/False) | No |

### Schema Configuration

The extraction schema is defined in `ocr.py` and can be customized for different document types. The current schema is optimized for floral arrangement catalogs and extracts:

- Product ID with size suffix (e.g., "197766S", "197766M", "197766L")
- Product name
- Size (S, M, L)
- Price
- Flower composition and quantities
- Foliage composition and quantities
- Dimensions
- Construction materials

## Project Structure

```
agentic-doc-ocr/
├── ocr.py              # Main OCR processing script
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration (not in git)
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
├── README.md          # This file
└── sample.pdf         # Example PDF file (not in git)
```

## Dependencies

- `requests` - HTTP client for API calls
- `python-dotenv` - Environment variable management
- `json` - JSON data handling

## API Integration

This project integrates with Landing AI's Vision Agent API for document analysis. The API provides:

- **Advanced OCR**: Superior text recognition and extraction
- **Document Understanding**: Intelligent parsing of complex layouts
- **Structured Output**: JSON-formatted results with confidence scores
- **Multi-page Support**: Handles multi-page documents automatically

## Error Handling

The script includes comprehensive error handling for:

- Missing environment variables
- Invalid API keys
- File not found errors
- API request failures
- JSON parsing errors

## Security

- API keys are stored in `.env` files (not committed to version control)
- Environment variables are validated before use
- Sensitive configuration is excluded from git history

## Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:

1. Check the [Issues](https://github.com/balamuru/agentic-doc-ocr/issues) page
2. Review the Landing AI [API Documentation](https://docs.landing.ai/)
3. Ensure your environment variables are correctly configured

## Roadmap

- [ ] Support for additional document types
- [ ] Batch processing of multiple PDFs
- [ ] Web interface for document upload
- [ ] Database integration for storing extracted data
- [ ] Export to various formats (CSV, Excel, etc.)
- [ ] Real-time processing capabilities

## Acknowledgments

- [Landing AI](https://landing.ai/) for providing the Vision Agent API
- The open source community for various tools and libraries used in this project
