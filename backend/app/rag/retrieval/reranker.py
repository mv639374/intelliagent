from sentence_transformers.cross_encoder import CrossEncoder
from typing import List, Dict, Any

class Reranker:
    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2'):
        # This will download the model on first run
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, chunks: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Re-ranks a list of chunks based on their relevance to the query using a cross-encoder.
        """
        if not chunks:
            return []
        
        # The model expects a list of [query, text] pairs
        pairs = [(query, chunk["text"]) for chunk in chunks]
        
        # Predict scores for all pairs
        scores = self.model.predict(pairs)
        
        # Add scores to the chunks and sort
        for i, chunk in enumerate(chunks):
            chunk["score"] = scores[i]
            
        sorted_chunks = sorted(chunks, key=lambda x: x["score"], reverse=True)
        
        return sorted_chunks[:top_k]

# Singleton instance
reranker = Reranker()