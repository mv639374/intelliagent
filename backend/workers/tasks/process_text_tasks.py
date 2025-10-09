# workers/tasks/process_text_tasks.py
from sqlalchemy import select  # ← Added for sync queries

from app.db.sync_session import get_sync_db  # ← Changed from AsyncSessionLocal
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.rag.chunker import Chunker
from app.rag.ingest.pii_redactor import PIIRedactor
from workers.celery_app import celery_app
from workers.tasks.index_tasks import index_document_task


@celery_app.task(name="tasks.process_text")
def process_text_document_task(document_id: str, page_texts: list, tables: list):
    """
    Process extracted text: redact PII, chunk, and save to database.
    """
    print(f"Starting text processing for document: {document_id}")

    with get_sync_db() as db:  # ← Changed from asyncio.run()
        try:
            # 1. Fetch document
            result = db.execute(select(Document).where(Document.id == document_id))
            doc = result.scalar_one_or_none()

            if not doc:
                print(f"Error: Document {document_id} not found.")
                return

            # 2. Initialize PII redactor and chunker
            pii_redactor = PIIRedactor()
            chunker = Chunker(chunk_size=500, chunk_overlap=50)

            # 3. Process and redact text from all pages
            for page in page_texts:
                page["text"] = pii_redactor.redact(page["text"])

            # 4. Chunk the text using the correct method
            chunks_data = chunker.chunk_pages_and_tables(page_texts, tables)

            # 5. Save chunks to database
            for idx, chunk_data in enumerate(chunks_data):
                chunk = Chunk(
                    document_id=doc.id,
                    text=chunk_data["text"],
                    chunk_index=idx,
                    chunk_metadata=chunk_data["metadata"],  # ← Now includes page and source
                )
                db.add(chunk)

            db.commit()  # ← Sync commit!
            print(f"Created {len(chunks_data)} chunks for document {document_id}")

            # 6. Trigger indexing task
            index_document_task.delay(document_id=document_id)
            print(f"Enqueued indexing task for document {document_id}")

        except Exception as e:
            db.rollback()
            print(f"Error processing text for document {document_id}: {str(e)}")

            # Update document status to FAILED
            try:
                result = db.execute(select(Document).where(Document.id == document_id))
                doc = result.scalar_one_or_none()
                if doc:
                    doc.status = DocumentStatus.FAILED
                    db.commit()
            except Exception as rollback_error:
                print(f"Failed to update status: {str(rollback_error)}")
