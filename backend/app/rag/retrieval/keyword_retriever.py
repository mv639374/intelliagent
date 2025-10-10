from typing import Any, Dict, List

from app.db.elasticsearch_client import es_client


class KeywordRetriever:
    async def retrieve(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves relevant chunks based on a keyword query.
        """
        print(f"Performing keyword search for: '{query}'")
        search_results = es_client.search(query, top_k)

        # Format results to be consistent with other retrievers
        formatted_results = []
        for hit in search_results:
            formatted_results.append(
                {
                    "chunk_id": hit["_id"],
                    "text": hit["_source"]["text"],
                    "score": hit["_score"],
                    "metadata": hit["_source"]["metadata"],
                }
            )
        return formatted_results


# Singleton instance
keyword_retriever = KeywordRetriever()
