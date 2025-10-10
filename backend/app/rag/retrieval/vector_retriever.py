from typing import List, Dict, Any
from app.rag.embedder import embedder
from app.db.vector_db import vector_db_client

class VectorRetriever:
    async def retrieve(self, query: str, top_k: int = 50) -> List[Dict[str, Any]]:
        """
        Embeds a query and retrieves the top_k most semantically similar chunks.
        """
        query_embedding = embedder.embed_texts([query])[0]

        search_results = vector_db_client.client.search(
            collection_name=vector_db_client.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True,
        )

        formatted_results = [
            {
                "chunk_id": result.id,
                "text": result.payload.get("text_snippet", ""),
                "score": result.score,
                "metadata": {
                    "document_id": result.payload.get("document_id"),
                    "chunk_id": result.payload.get("chunk_id"),
                }
            }
            for result in search_results
        ]
        return formatted_results

# Singleton instance
vector_retriever = VectorRetriever()