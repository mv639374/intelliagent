import pytest

from app.rag.ocr.tesseract_engine import TesseractEngine


# Note: This test requires a PDF file at the specified path
# and for tesseract & poppler-utils to be installed locally or in the test environment.
@pytest.mark.skip(reason="Requires local tesseract/poppler and a sample file")
def test_tesseract_ocr_pdf():
    """
    Tests basic OCR functionality on a sample PDF.
    """
    engine = TesseractEngine()
    # Create a simple, text-based PDF named 'test.pdf' in the tests directory for this to work
    file_path = "tests/rag/ocr/test.pdf"

    results = engine.ocr_pdf(file_path)

    assert len(results) > 0  # Should have at least one page
    page_num, text = results[0]
    assert page_num == 1
    assert "expected_keyword_from_your_pdf" in text.lower()
