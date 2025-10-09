from typing import List, Tuple

import pytesseract
from pdf2image import convert_from_path


class TesseractEngine:
    """
    An OCR engine using Tesseract to extract text from PDF files.
    """

    def ocr_pdf(self, file_path: str) -> List[Tuple[int, str]]:
        """
        Converts each page of a PDF to an image and performs OCR.

        Args:
        ----
            file_path: The local path to the PDF file.

        Returns:
        -------
            A list of tuples, where each tuple contains the page number
            and the extracted text for that page.

        """
        try:
            images = convert_from_path(file_path)
            results = []
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                results.append((i + 1, text))  # page_num is 1-indexed
            return results
        except Exception as e:
            print(f"Error during Tesseract OCR: {e}")
            return []
