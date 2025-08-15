# Sample Data Directory

This directory contains sample PDF files for testing and demonstrating the OCR functionality.

## Sample Files

### `sample-good.pdf`
- **Purpose**: Standard single-page document for basic testing
- **Use Case**: Testing single-page processing functionality
- **Size**: ~186 KB
- **Content**: Typical floral arrangement catalog page

### `sample-multi.pdf`
- **Purpose**: Multi-page document for testing parallel processing
- **Use Case**: Testing page-by-page splitting and parallel processing
- **Size**: ~152 KB
- **Content**: Multi-page floral arrangement catalog

### `sample-bad.pdf`
- **Purpose**: Problematic document for testing error handling
- **Use Case**: Testing error recovery and fault tolerance
- **Size**: ~44 KB
- **Content**: Document that may cause processing errors

## Usage

These files are referenced in the example code and documentation:

```python
# Single page processing
from ocr import process_document
result = process_document("sampledata/sample-good.pdf")

# Multi-page processing
from ocr import process_pdf_by_pages
result = process_pdf_by_pages("sampledata/sample-multi.pdf", max_workers=4)
```

## Note

These files are included in `.gitignore` and are not tracked in version control. 
Replace them with your own PDF files for actual testing and processing.
