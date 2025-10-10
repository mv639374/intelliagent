from typing import Any, Dict, List

from app.db.elasticsearch_client import es_client


class KeywordIndexer:
    def index_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Takes a list of chunk dictionaries and indexes them in Elasticsearch.

        Args:
        ----
            chunks: A list of dicts, each with 'chunk_id', 'text', and 'metadata'.

        """
        if not chunks:
            return

        print(f"Indexing {len(chunks)} chunks into Elasticsearch.")
        es_client.bulk_index_chunks(chunks)
        print("Bulk indexing to Elasticsearch complete.")


# Singleton instance
keyword_indexer = KeywordIndexer()
