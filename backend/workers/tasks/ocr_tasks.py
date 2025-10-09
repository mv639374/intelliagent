# workers/tasks/ocr_tasks.py
import asyncio

from app.rag.ocr.layout_analyzer import LayoutAnalyzer
from app.rag.ocr.tesseract_engine import TesseractEngine
from workers.celery_app import celery_app
from workers.tasks.process_text_tasks import process_text_document_task


@celery_app.task(name="tasks.ocr_document")
def ocr_document_task(document_id: str, file_path: str):
    """
    Celery task to perform OCR on a PDF document.

    Args:
    ----
        document_id: UUID of the document in the database
        file_path: Full path to the PDF file on disk

    """
    asyncio.run(run_ocr(document_id, file_path))


async def run_ocr(document_id: str, file_path: str):
    """
    Orchestrates the OCR and layout analysis process for a PDF document.
    After OCR is complete, hands off to the text processing task.

    Args:
    ----
        document_id: UUID of the document in the database
        file_path: Full path to the PDF file on disk

    """
    print(f"Starting OCR for document: {document_id}")

    try:
        # Initialize OCR engine and layout analyzer
        ocr_engine = TesseractEngine()
        layout_analyzer = LayoutAnalyzer()

        # Perform OCR on all pages
        ocr_results = ocr_engine.ocr_pdf(file_path)
        print(f"OCR completed. Extracted text from {len(ocr_results)} pages.")

        # Extract tables from PDF
        tables = layout_analyzer.extract_tables(file_path)
        print(f"Layout analysis completed. Extracted {len(tables)} tables.")

        # Format OCR results for downstream processing
        page_texts = [{"page_number": page_num, "text": text} for page_num, text in ocr_results]

        # Hand off to the text processing task
        process_text_document_task.delay(document_id=document_id, page_texts=page_texts, tables=tables)

        print(f"OCR finished for document {document_id}. Handed off to text processor.")

    except Exception as e:
        print(f"Error during OCR for document {document_id}: {str(e)}")
        # Note: The text processing task won't be triggered if OCR fails
        # The document status will remain in PROCESSING until manually updated
        raise
