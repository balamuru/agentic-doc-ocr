# Agentic Document OCR

[![GitHub](https://img.shields.io/badge/GitHub-View%20on%20GitHub-blue?logo=github)](https://github.com/balamuru/agentic-doc-ocr)

A Python-based document OCR system that uses Landing AI's Vision Agent API to extract structured data from PDF documents. This project is specifically designed to extract product information from floral arrangement catalogs, but can be adapted for other document types.

## Features

- 🔍 **Intelligent Document Parsing**: Uses Landing AI's Vision Agent API for advanced document understanding
- 📊 **Structured Data Extraction**: Extracts product information in JSON format
- 🎯 **Multi-size Product Support**: Automatically extracts all product sizes (S, M, L) from catalog documents
- 🔧 **Environment-based Configuration**: Secure configuration management using `.env` files
- 📋 **Comprehensive Product Data**: Extracts ID, name, size, price, flower data, foliage data, dimensions, and construction materials
- 🛡️ **Schema-based Validation**: Uses JSON schema for reliable data extraction
- 📄 **Page-by-Page Processing**: Splits multi-page PDFs and processes each page individually
- ⚡ **Parallel Processing**: Processes multiple pages simultaneously for improved performance
- 📁 **Organized Output**: Saves results in timestamped directories with page-specific folders
- 🔄 **Backward Compatibility**: Maintains support for single-page processing mode

## Prerequisites

- Python 3.13.3 or higher
- Landing AI Vision Agent API key
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
   
   # Processing Configuration (optional)
   MAX_WORKERS=4  # Number of parallel workers (default: 4)
   ```

## Usage

### Basic Usage (Multi-Page Processing)

1. **Place your PDF file** in the directory specified by `BASE_PDF_PATH`
2. **Update the PDF name** in your `.env` file
3. **Run the OCR script**:
   ```bash
   python ocr.py
   ```

The script will automatically:
- Split the PDF into individual pages
- Process each page in parallel using the Vision Agent API
- Save results in organized directories
- Generate comprehensive summaries

### Output Structure

Results are saved in the following structure:

```
output/
└── 20241201-143022/          # Timestamp when processing started
    ├── 001/                  # Page 1 results
    │   ├── result.json       # Raw API response
    │   └── summary.txt       # Human-readable summary
    ├── 002/                  # Page 2 results
    │   ├── result.json
    │   └── summary.txt
    ├── 003/                  # Page 3 results
    │   ├── result.json
    │   └── summary.txt
    ├── processing_summary.txt # Overall processing summary
    └── combined_results.json # All results combined
```

### Advanced Usage

#### Custom Parallel Processing

```python
from ocr import process_pdf_by_pages

# Process with 2 workers (useful for slower connections)
result = process_pdf_by_pages("sampledata/sample-multi.pdf", max_workers=2)

# Process with 8 workers (for high-performance systems)
result = process_pdf_by_pages("sampledata/sample-multi.pdf", max_workers=8)
```

#### Single Page Processing (Legacy Mode)

```python
from ocr import process_document

# Process a single page or single-page PDF
result = process_document("sampledata/sample-good.pdf")
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

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `VISION_AGENT_API_KEY` | Your Landing AI Vision Agent API key | Yes | - |
| `BASE_PDF_PATH` | Directory containing PDF files | Yes | - |
| `PDF_NAME` | Name of the PDF file to process | Yes | - |
| `MAX_WORKERS` | Number of parallel workers for processing | No | 4 |

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

## Testing and Development

### Running Tests
```bash
python test_ocr.py
```

The test suite covers:
- PDF splitting functionality
- Output directory creation
- Page result saving
- Error handling
- Parallel processing structure

### Development Tools
- **`example_usage.py`**: Usage examples and demonstrations
- **`IMPROVEMENTS.md`**: Detailed documentation of recent improvements
- **`sampledata/`**: Sample PDF files for testing different scenarios
  - `sampledata/sample-good.pdf`: Standard single-page document
  - `sampledata/sample-multi.pdf`: Multi-page document for testing parallel processing
  - `sampledata/sample-bad.pdf`: Document for testing error handling

## Project Structure

```
agentic-doc-ocr/
├── ocr.py              # Main OCR processing script
├── example_usage.py    # Example usage demonstrations
├── test_ocr.py         # Test suite for functionality
├── IMPROVEMENTS.md     # Detailed improvement summary
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project configuration
├── sampledata/         # Sample PDF files for testing
│   ├── sample-good.pdf # Single-page example PDF
│   ├── sample-multi.pdf # Multi-page example PDF
│   └── sample-bad.pdf  # Test PDF for error handling
├── .env               # Environment configuration (not in git)
├── .env.example       # Environment configuration template
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
└── README.md          # This file
```

## Dependencies

- `agentic-doc` - Landing AI's document processing library
- `pydantic>=2.0.0` - Data validation and settings management
- `python-dotenv>=1.0.0` - Environment variable management
- `PyPDF2>=3.0.0` - PDF manipulation and page splitting
- `requests>=2.28.0` - HTTP client for API calls

## Performance Considerations

### Parallel Processing

- **Default**: 4 parallel workers
- **Recommended**: 2-8 workers depending on your system and API rate limits
- **High-performance systems**: Can use 8+ workers
- **Slower connections**: Use 2-3 workers to avoid overwhelming the API

### Memory Usage

- Each page is processed independently
- Temporary files are automatically cleaned up
- Memory usage scales with the number of parallel workers

### API Rate Limits

- The Vision Agent API has rate limits
- Parallel processing may hit these limits with too many workers
- Monitor API responses and adjust `MAX_WORKERS` accordingly

## API Integration

This project integrates with Landing AI's Vision Agent API for document analysis. The API provides:

- **Advanced OCR**: Superior text recognition and extraction
- **Document Understanding**: Intelligent parsing of complex layouts
- **Structured Output**: JSON-formatted results with confidence scores
- **Multi-page Support**: Handles multi-page documents automatically
- **Schema-based Extraction**: Customizable data extraction based on JSON schema

## Error Handling

The script includes comprehensive error handling for:

- Missing environment variables
- Invalid API keys
- File not found errors
- API request failures
- JSON parsing errors
- PDF processing errors
- Parallel processing failures

### Error Recovery

- Failed pages are logged with detailed error messages
- Successful pages continue processing even if some pages fail
- Temporary files are cleaned up even on errors
- Processing summary includes success/failure counts

## Security

- API keys are stored in `.env` files (not committed to version control)
- Environment variables are validated before use
- Sensitive configuration is excluded from git history
- Temporary files are securely created and cleaned up

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
4. Check the processing logs for detailed error information

## Roadmap

- [x] Multi-page PDF processing
- [x] Parallel processing capabilities
- [x] Organized output structure
- [ ] Support for additional document types
- [ ] Batch processing of multiple PDFs
- [ ] Web interface for document upload
- [ ] Database integration for storing extracted data
- [ ] Export to various formats (CSV, Excel, etc.)
- [ ] Real-time processing capabilities
- [ ] Progress tracking and resumable processing

## Acknowledgments

- [Landing AI](https://landing.ai/) for providing the Vision Agent API
- The open source community for various tools and libraries used in this project
