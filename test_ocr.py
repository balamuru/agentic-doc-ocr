#!/usr/bin/env python3
"""
Test script for the improved OCR functionality.

This script tests the new page-by-page processing features without
requiring actual API calls or PDF files.
"""

import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

def test_pdf_splitting():
    """Test PDF splitting functionality."""
    print("Testing PDF splitting...")
    
    # Mock PDF file
    mock_pdf_content = b"%PDF-1.4\n%Test PDF content"
    
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
        temp_pdf.write(mock_pdf_content)
        temp_pdf_path = temp_pdf.name
    
    try:
        # Mock PyPDF2
        mock_page = Mock()
        mock_reader = Mock()
        mock_reader.pages = [mock_page, mock_page]  # 2 pages
        
        with patch('ocr.PyPDF2.PdfReader', return_value=mock_reader):
            with patch('ocr.PyPDF2.PdfWriter') as mock_writer_class:
                mock_writer = Mock()
                mock_writer_class.return_value = mock_writer
                
                # Import and test the function
                from ocr import split_pdf_by_pages
                
                result = split_pdf_by_pages(temp_pdf_path)
                
                # Verify results
                assert len(result) == 2, f"Expected 2 pages, got {len(result)}"
                assert result[0][0] == 1, "First page should be numbered 1"
                assert result[1][0] == 2, "Second page should be numbered 2"
                
                print("✓ PDF splitting test passed")
                
                # Clean up temporary files
                for _, temp_path in result:
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                        
    except Exception as e:
        print(f"✗ PDF splitting test failed: {e}")
    finally:
        try:
            os.unlink(temp_pdf_path)
        except:
            pass

def test_output_directory_creation():
    """Test output directory creation."""
    print("Testing output directory creation...")
    
    try:
        from ocr import create_output_directory
        
        output_dir = create_output_directory()
        
        # Verify directory exists
        assert output_dir.exists(), "Output directory should exist"
        assert output_dir.is_dir(), "Output should be a directory"
        
        # Verify timestamp format in name
        dir_name = output_dir.name
        assert len(dir_name) == 15, f"Directory name should be 15 chars, got {len(dir_name)}"
        assert dir_name.count('-') == 1, "Directory name should contain one hyphen"
        
        print("✓ Output directory creation test passed")
        
    except Exception as e:
        print(f"✗ Output directory creation test failed: {e}")

def test_page_result_saving():
    """Test saving page results."""
    print("Testing page result saving...")
    
    try:
        from ocr import save_page_result
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            
            # Test data
            test_result = {
                "products": [
                    {
                        "id": "test123S",
                        "name": "Test Product",
                        "size": "S",
                        "price": 29.99,
                        "flower-data": "1 stem Test Flower",
                        "foliage-data": "1 stem Test Foliage",
                        "dimensions": "Height 10\", Length 8\"",
                        "construction-material": "Test Vase"
                    }
                ]
            }
            
            # Save result
            save_page_result(output_dir, 1, test_result)
            
            # Verify files were created
            page_dir = output_dir / "001"
            assert page_dir.exists(), "Page directory should exist"
            
            result_file = page_dir / "result.json"
            assert result_file.exists(), "result.json should exist"
            
            summary_file = page_dir / "summary.txt"
            assert summary_file.exists(), "summary.txt should exist"
            
            # Verify content
            with open(result_file, 'r') as f:
                saved_result = json.load(f)
                assert saved_result == test_result, "Saved result should match input"
            
            with open(summary_file, 'r') as f:
                summary_content = f.read()
                assert "Page 1 Processing Results" in summary_content
                assert "Test Product" in summary_content
                assert "1 products found" in summary_content
            
            print("✓ Page result saving test passed")
            
    except Exception as e:
        print(f"✗ Page result saving test failed: {e}")

def test_error_handling():
    """Test error handling in page result saving."""
    print("Testing error handling...")
    
    try:
        from ocr import save_page_result
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            
            # Test error result
            error_result = {"error": "Test error message"}
            
            # Save error result
            save_page_result(output_dir, 1, error_result)
            
            # Verify error was handled correctly
            page_dir = output_dir / "001"
            summary_file = page_dir / "summary.txt"
            
            with open(summary_file, 'r') as f:
                summary_content = f.read()
                assert "ERROR: Test error message" in summary_content
            
            print("✓ Error handling test passed")
            
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")

def test_parallel_processing_structure():
    """Test the structure of parallel processing function."""
    print("Testing parallel processing structure...")
    
    try:
        from ocr import process_pdf_by_pages
        
        # Mock the dependencies
        with patch('ocr.split_pdf_by_pages') as mock_split:
            with patch('ocr.create_output_directory') as mock_create_dir:
                with patch('ocr.save_page_result') as mock_save:
                    with patch('ocr.process_page_parallel') as mock_process:
                        
                        # Mock return values
                        mock_split.return_value = [(1, '/tmp/page1.pdf'), (2, '/tmp/page2.pdf')]
                        mock_create_dir.return_value = Path('/tmp/output')
                        mock_process.return_value = (1, {"products": []})
                        
                        # Mock ThreadPoolExecutor and its context manager
                        mock_executor = Mock()
                        mock_executor_instance = Mock()
                        
                        # Set up the context manager behavior
                        mock_executor.return_value = mock_executor_instance
                        mock_executor_instance.__enter__ = Mock(return_value=mock_executor_instance)
                        mock_executor_instance.__exit__ = Mock(return_value=None)
                        
                        # Mock futures
                        mock_future1 = Mock()
                        mock_future1.result.return_value = (1, {"products": []})
                        mock_future2 = Mock()
                        mock_future2.result.return_value = (2, {"products": []})
                        
                        # Set up as_completed to return our futures
                        mock_executor_instance.submit.return_value = mock_future1
                        
                        with patch('ocr.ThreadPoolExecutor', mock_executor):
                            with patch('ocr.as_completed', return_value=[mock_future1, mock_future2]):
                                # Test the function
                                result = process_pdf_by_pages("/tmp/test.pdf", max_workers=2)
                                
                                # Verify structure
                                assert "output_directory" in result
                                assert "total_pages" in result
                                assert "successful_pages" in result
                                assert "failed_pages" in result
                                assert "results" in result
                                
                                print("✓ Parallel processing structure test passed")
                            
    except Exception as e:
        print(f"✗ Parallel processing structure test failed: {e}")

def main():
    """Run all tests."""
    print("Running OCR functionality tests...")
    print("=" * 50)
    
    test_pdf_splitting()
    test_output_directory_creation()
    test_page_result_saving()
    test_error_handling()
    test_parallel_processing_structure()
    
    print("=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    main()
