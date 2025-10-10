import os
from typing import Any, Dict, List

from elasticsearch import Elasticsearch, helpers


class ElasticsearchClient:
    def __init__(self):
        # FIXED: Use singular form to match where data is actually indexed
        self.index_name = "intelliagent_chunk"
        self.client = Elasticsearch(os.getenv("ELASTICSEARCH_URL", "http://localhost:9200"))

    def create_index_if_not_exists(self):
        """
        Creates the Elasticsearch index with specific mappings and settings
        for English language analysis and BM25 tuning if it does not exist.
        """
        try:
            if not self.client.indices.exists(index=self.index_name):
                print(f"Creating Elasticsearch index: '{self.index_name}'")
                settings = {
                    "analysis": {
                        "analyzer": {"default": {"type": "standard"}, "english_analyzer": {"type": "english"}}
                    },
                    "similarity": {"bm25_tuned": {"type": "BM25", "k1": 1.2, "b": 0.75}},
                }
                mappings = {
                    "properties": {
                        "text": {"type": "text", "analyzer": "english", "similarity": "bm25_tuned"},
                        "metadata": {"type": "object", "enabled": False},
                    }
                }
                body = {"settings": settings, "mappings": mappings}
                self.client.indices.create(index=self.index_name, body=body)
                print(f"Index '{self.index_name}' created successfully.")
            else:
                print(f"Index '{self.index_name}' already exists.")
        except Exception as e:
            print(f"Elasticsearch error while creating index '{self.index_name}': {e}")

    def bulk_index_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Performs a bulk indexing operation for a list of chunks.
        """
        try:
            actions = [
                {
                    "_index": self.index_name,
                    "_id": chunk["chunk_id"],
                    "_source": {"text": chunk["text"], "metadata": chunk["metadata"]},
                }
                for chunk in chunks
            ]
            helpers.bulk(self.client, actions)
            print(f"Bulk indexed {len(chunks)} chunks into index '{self.index_name}'.")
        except Exception as e:
            print(f"Elasticsearch bulk indexing error: {e}")

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Performs a keyword search against the 'text' field.
        """
        try:
            # Modern Elasticsearch Python client syntax
            response = self.client.search(index=self.index_name, query={"match": {"text": query}}, size=top_k)
            return response["hits"]["hits"]
        except Exception as e:
            print(f"Elasticsearch search error: {e}")
            return []


# Singleton instance
es_client = ElasticsearchClient()
es_client.create_index_if_not_exists()
