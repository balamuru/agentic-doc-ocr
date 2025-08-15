# Agentic Document OCR

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
   git clone <repository-url>
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

The script will extract structured data from your PDF and output:

```json
{
  "products": [
    {
      "id": "197766S",
      "name": "Petal Palooza",
      "size": "S",
      "price": 39.99,
      "flower-data": "1 stem Hydrangea - Blue, 2 stems Carnation - Orange...",
      "foliage-data": "2 stems Tree Fern - Painted, 0 stems Eucalyptus - Gunni",
      "dimensions": "Arrangement Height 9\", Length 7\"",
      "construction-material": "6\" Gathering Vase - Clear"
    }
  ]
}
```

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

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:

1. Check the [Issues](https://github.com/your-repo/agentic-doc-ocr/issues) page
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
