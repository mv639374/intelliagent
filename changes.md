You've done an excellent job debugging, and you're very close. The index settings are now correct, but the final step—getting data _into_ the index—is failing. Your logs show the core problem perfectly.

The search is empty for a simple reason: **the indexing task is failing silently before it can add any data to Elasticsearch.**

### The Problem

There are two subtle bugs causing the failure:

1.  **Missing Task Logic:** The `index_tasks.py` file you're using successfully indexes to the vector database (Qdrant), but it **never calls the `keyword_indexer`** to add data to Elasticsearch. You can see this in your logs: the pipeline finishes at the "status set to INDEXED" step without ever mentioning Elasticsearch.
2.  **Outdated Search Syntax:** The `search` function in your `elasticsearch_client.py` uses the `body={...}` parameter, which is outdated. The modern client expects the query directly, like `query={...}`. This is why your manual search script runs but finds nothing.

### The Solution

We will fix this by providing the final, correct versions of `index_tasks.py` and `elasticsearch_client.py`, and adding a required helper file for synchronous database sessions in Celery.

#### **Step 1: Create a Synchronous DB Session for Celery**

Celery tasks run in separate processes and cannot use the `asyncio` event loop from FastAPI. They need a standard, synchronous database connection.

**File:** `backend/app/db/sync_session.py` (New File)

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Use a standard postgresql driver for the synchronous engine
SYNC_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:password@localhost:5432/intelliagent_db").replace("asyncpg", "psycopg")

engine = create_engine(SYNC_DATABASE_URL)
SessionLocalSync = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_sync_db():
    """Provides a synchronous database session for Celery tasks."""
    db = SessionLocalSync()
    try:
        yield db
    finally:
        db.close()
```

#### **Step 2: Update the Elasticsearch Client**

This version corrects the `search` method syntax.

**File:** `backend/app/db/elasticsearch_client.py` (Update)

```python
import os
from elasticsearch import Elasticsearch, helpers
from typing import List, Dict, Any

class ElasticsearchClient:
    def __init__(self):
        # Correct index name
        self.index_name = "intelliagent_chunks"
        self.client = Elasticsearch(os.getenv("ELASTICSEARCH_URL", "http://localhost:9200"))

    def create_index_if_not_exists(self):
        # ... (no changes here)
        pass # Keep existing implementation

    def bulk_index_chunks(self, chunks: List[Dict[str, Any]]):
        # ... (no changes here)
        pass # Keep existing implementation

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Performs a keyword search against the 'text' field.
        """
        try:
            # CORRECTED: The 'query' parameter should be used directly, not inside 'body'.
            response = self.client.search(
                index=self.index_name,
                query={"match": {"text": query}},
                size=top_k
            )
            return response['hits']['hits']
        except Exception as e:
            print(f"Elasticsearch search error: {e}")
            return []

# Singleton instance
es_client = ElasticsearchClient()
es_client.create_index_if_not_exists()
```

#### **Step 3: Update the Indexing Task**

This is the most important fix. This version uses the new synchronous session and correctly calls both the keyword indexer and the vector indexer.

**File:** `workers/tasks/index_tasks.py` (Update)

```python
from sqlalchemy import select
from qdrant_client.http.models import PointStruct

from workers.celery_app import celery_app
from app.db.sync_session import get_sync_db # Use the new sync session
from app.db.vector_db import vector_db_client
from app.models.chunk import Chunk
from app.models.document import Document, DocumentStatus
from app.rag.embedder import embedder
from app.rag.index.keyword_indexer import keyword_indexer # Import keyword indexer

@celery_app.task(name="tasks.index_document")
def index_document_task(document_id: str):
    print(f"Starting indexing for document: {document_id}")

    with get_sync_db() as db:
        try:
            # Fetch all chunks
            chunks = db.execute(select(Chunk).where(Chunk.document_id == document_id)).scalars().all()

            if not chunks:
                print(f"No chunks found for document {document_id}")
                return

            # --- KEYWORD INDEXING (THE MISSING STEP) ---
            chunk_data_for_es = [{"chunk_id": str(c.id), "text": c.text, "metadata": c.metadata} for c in chunks]
            keyword_indexer.index_chunks(chunk_data_for_es)
            print(f"✓ Indexed {len(chunks)} chunks to Elasticsearch.")

            # --- VECTOR INDEXING (EXISTING LOGIC) ---
            texts = [chunk.text for chunk in chunks]
            embeddings = embedder.embed_texts(texts)
            points = [PointStruct(id=str(chunk.id), vector=embedding, payload={"doc_id": str(chunk.document_id)}) for chunk, embedding in zip(chunks, embeddings)]
            vector_db_client.upsert_embeddings(points)
            print(f"✓ Indexed {len(points)} vectors to Qdrant.")

            # Update document status to INDEXED
            doc = db.get(Document, document_id)
            if doc:
                doc.status = DocumentStatus.INDEXED
                db.commit()
                print(f"✓ Document {document_id} status set to INDEXED")

        except Exception as e:
            db.rollback()
            print(f"✗ Error during indexing for doc {document_id}: {e}")
            # Handle status update to FAILED...
```

---

### Verifying the Fix

1.  **Restart your services** (`make stop`, `make run-dev`).
2.  **Start your Celery worker** (`make celery`).
3.  **Delete the old empty index** to ensure a clean slate:
    ```bash
    curl -X DELETE "http://localhost:9200/intelliagent_chunks"
    ```
4.  **Upload `pii_sample.pdf` again.**
5.  **Watch the worker logs.** You will now see logs for both "Indexed... chunks to Elasticsearch" and "Indexed... vectors to Qdrant".
6.  **Run the search test again.** It will now find and return the correct results.
    ```bash
    docker exec -it intelliagent-backend sh -c "cd /app && PYTHONPATH=/app python scripts/keyword_search_test.py"
    ```
