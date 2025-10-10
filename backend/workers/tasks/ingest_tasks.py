# workers/tasks/ingest_tasks.py

"""
Document ingestion task - routes documents to appropriate processing based on file type.
Uses synchronous SQLAlchemy to avoid event loop conflicts in Celery.
"""

import docx
from sqlalchemy import select  # ← Added for sync queries

from app.db.sync_session import get_sync_db  # ← Changed from AsyncSessionLocal
from app.models.document import Document, DocumentStatus
from app.rag.ingest.metadata_extractor import MetadataExtractor  # ← NEW: Import metadata extractor
from workers.celery_app import celery_app
from workers.tasks.ocr_tasks import ocr_document_task
from workers.tasks.process_text_tasks import process_text_document_task


@celery_app.task(name="tasks.ingest_document")
def ingest_document_task(document_id: str, sha256_hash: str):
    """
    Main ingestion task that routes to appropriate processing based on file type.

    Args:
    ----
        document_id: UUID of the document in the database
        sha256_hash: SHA256 hash used as the filename on disk

    Workflow:
        1. Updates document status to PROCESSING
        2. Extracts and saves metadata from the file
        3. Routes based on mime type:
           - PDF → ocr_document_task
           - DOCX → Extract text → process_text_document_task
           - TXT → Read text → process_text_document_task

    """
    print(f"Starting ingestion for document_id: {document_id}")

    with get_sync_db() as db:  # ← Changed from asyncio.run(process_document())
        try:
            # 1. Fetch the document record from the DB
            result = db.execute(select(Document).where(Document.id == document_id))
            doc = result.scalar_one_or_none()

            if not doc:
                print(f"Error: Document with ID {document_id} not found.")
                return

            # 2. Update status to PROCESSING
            doc.status = DocumentStatus.PROCESSING
            db.commit()  # ← Sync commit
            print(f"Document {doc.filename} status set to PROCESSING.")

            # 3. Construct the file path
            file_path = f"/app/uploads/{sha256_hash}"
            print(f"Processing file at: {file_path}")

            # 4. Extract metadata from the original file
            try:
                with open(file_path, "rb") as f:
                    file_content = f.read()

                meta_extractor = MetadataExtractor()
                metadata = meta_extractor.extract(file_content, doc.mime_type)
                if metadata:
                    doc.doc_metadata = metadata
                    db.commit()
                    print(f"Extracted and saved metadata for document {document_id}: {metadata}")
            except Exception as e:
                print(f"Could not extract metadata for {document_id}: {e}")

            # 5. Route based on mime type
            if doc.mime_type == "application/pdf":
                print("Document is a PDF. Enqueuing OCR task.")
                ocr_document_task.delay(document_id=document_id, file_path=file_path)

            elif "openxmlformats-officedocument.wordprocessingml" in doc.mime_type:
                print("Document is DOCX. Extracting text directly.")
                try:
                    document = docx.Document(file_path)
                    full_text = "\n".join([para.text for para in document.paragraphs])

                    # Create page_texts structure (DOCX treated as single page)
                    page_texts = [{"page_number": 1, "text": full_text}]

                    # Enqueue text processing task
                    process_text_document_task.delay(document_id=document_id, page_texts=page_texts, tables=[])
                    print("DOCX text extracted. Enqueued text processing task.")

                except Exception as e:
                    print(f"Failed to extract text from DOCX {document_id}: {e}")
                    doc.status = DocumentStatus.FAILED
                    db.commit()

            else:
                # Assume plain text file
                print("Document is plain text. Reading directly.")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()

                    page_texts = [{"page_number": 1, "text": text}]

                    # Enqueue text processing task
                    process_text_document_task.delay(document_id=document_id, page_texts=page_texts, tables=[])
                    print("Plain text extracted. Enqueued text processing task.")

                except Exception as e:
                    print(f"Failed to read plain text file {document_id}: {e}")
                    doc.status = DocumentStatus.FAILED
                    db.commit()

        except Exception as e:
            db.rollback()
            print(f"Error processing document {document_id}: {str(e)}")

            # Update status to FAILED
            try:
                result = db.execute(select(Document).where(Document.id == document_id))
                doc = result.scalar_one_or_none()
                if doc:
                    doc.status = DocumentStatus.FAILED
                    db.commit()
                    print(f"Document {document_id} status set to FAILED.")
            except Exception as rollback_error:
                print(f"Failed to update document status to FAILED: {str(rollback_error)}")
