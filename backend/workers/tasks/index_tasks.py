# workers/tasks/index_tasks.py
from qdrant_client.http.models import PointStruct  # ← ADD THIS IMPORT
from sqlalchemy import select

from app.db.sync_session import get_sync_db
from app.db.vector_db import VectorDBClient
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.rag.embedder import Embedder
from app.rag.index.keyword_indexer import keyword_indexer
from workers.celery_app import celery_app


@celery_app.task(name="tasks.index_document")
def index_document_task(document_id: str):
    """
    Generate embeddings and index chunks in the vector database.
    """
    print(f"Starting indexing for document: {document_id}")

    with get_sync_db() as db:
        try:
            # Fetch all chunks for this document
            result = db.execute(select(Chunk).where(Chunk.document_id == document_id))
            chunks = result.scalars().all()

            if not chunks:
                print(f"No chunks found for document {document_id}")
                return

            # 1. Index chunks in Elasticsearch for keyword search
            chunk_data_for_es = [
                {
                    "chunk_id": str(chunk.id),
                    "text": chunk.text,
                    "metadata": {
                        "document_id": str(chunk.document_id),
                        "chunk_index": chunk.chunk_index,
                        # Add any other relevant metadata from chunk.chunk_metadata
                    },
                }
                for chunk in chunks
            ]
            keyword_indexer.index_chunks(chunk_data_for_es)
            print(f"✓ Indexed {len(chunks)} chunks to Elasticsearch for document {document_id}")

            # Generate embeddings (batch mode)
            embedder = Embedder()
            texts = [chunk.text for chunk in chunks]
            embeddings = embedder.embed_texts(texts)  # ← FIXED: use embed_texts()

            # Create PointStruct objects for Qdrant
            points = []
            for chunk, embedding in zip(chunks, embeddings):
                point = PointStruct(
                    id=str(chunk.id),  # Use chunk ID as point ID
                    vector=embedding,
                    payload={
                        "document_id": str(document_id),
                        "text": chunk.text,
                        "chunk_index": chunk.chunk_index,
                        "metadata": chunk.chunk_metadata,
                    },
                )
                points.append(point)

            # Upsert to Qdrant (batch)
            vector_db = VectorDBClient()
            vector_db.upsert_embeddings(points)  # ← FIXED: use upsert_embeddings()

            print(f"✓ Indexed {len(points)} chunks to Qdrant for document {document_id}")

            # Update document status to INDEXED
            result = db.execute(select(Document).where(Document.id == document_id))
            doc = result.scalar_one_or_none()
            if doc:
                doc.status = DocumentStatus.INDEXED
                db.commit()
                print(f"✓ Document {document_id} status set to INDEXED")

        except Exception as e:
            db.rollback()
            print(f"✗ Error indexing document {document_id}: {str(e)}")

            # Update document status to FAILED
            try:
                result = db.execute(select(Document).where(Document.id == document_id))
                doc = result.scalar_one_or_none()
                if doc:
                    doc.status = DocumentStatus.FAILED
                    db.commit()
            except Exception as update_error:
                print(f"Failed to update status: {str(update_error)}")
