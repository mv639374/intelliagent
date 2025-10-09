import os
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams


class VectorDBClient:
    def __init__(self):
        self.client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
        self.collection_name = "intelliagent_vectors"
        # Using SentenceTransformer 'all-MiniLM-L6-v2' which has a dimension of 384
        self.vector_size = 384
        self.distance_metric = Distance.COSINE

    def initialize_collection(self):
        """
        Creates the Qdrant collection if it doesn't already exist.
        """
        try:
            self.client.get_collection(collection_name=self.collection_name)
            print(f"Collection '{self.collection_name}' already exists.")
        except Exception:
            print(f"Collection '{self.collection_name}' not found. Creating collection...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=self.distance_metric),
            )
            print("Collection created successfully.")

    def upsert_embeddings(self, points: List[PointStruct]):
        """
        Upserts a list of points (embedding + payload) into the collection.
        """
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )


# Initialize a singleton instance
vector_db_client = VectorDBClient()
vector_db_client.initialize_collection()
