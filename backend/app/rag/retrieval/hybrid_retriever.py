import asyncio
from typing import List, Dict, Any

from .vector_retriever import vector_retriever
from .keyword_retriever import keyword_retriever
from .fusion import reciprocal_rank_fusion
from .reranker import reranker
from .filters import filter_low_confidence
from .citation_formatter import format_citations
from app.core.security import mask_pii_in_results

class HybridRetriever:
    async def retrieve(
        self,
        query: str,
        top_k: int = 10,
        rerank: bool = True,
        apply_pii_mask: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Performs a full hybrid retrieval pipeline with enhanced features:
        
        1. Fetches results from vector and keyword retrievers in parallel.
        2. Fuses the results using Reciprocal Rank Fusion.
        3. Filters low-confidence results (initial filter).
        4. Optionally re-ranks the top results using a cross-encoder.
        5. Applies post-reranking confidence filter (rejects irrelevant results).
        6. Applies PII masking to protect sensitive information.
        7. Formats results with citation metadata.
        
        Args:
            query: The search query string
            top_k: Number of final results to return
            rerank: Whether to apply cross-encoder reranking
            apply_pii_mask: Whether to mask personally identifiable information
            
        Returns:
            List of formatted citation results with scores and metadata
        """
        
        # 1. Run retrievers in parallel
        vector_results_task = vector_retriever.retrieve(query, top_k=50)
        keyword_results_task = keyword_retriever.retrieve(query, top_k=50)
        results_list = await asyncio.gather(vector_results_task, keyword_results_task)
        
        # 2. Fuse results using Reciprocal Rank Fusion
        fused_results = reciprocal_rank_fusion(results_list, k=60)
        
        # 3. Filter low-confidence results (initial filter)
        confident_results = filter_low_confidence(fused_results)
        
        if not confident_results:
            return []
        
        # 4. Optionally rerank using cross-encoder
        if rerank:
            # Rerank the top 20 fused results to get the final top_k
            results_to_rerank = confident_results[:20]
            reranked_results = reranker.rerank(query, results_to_rerank, top_k=top_k)
            
            # --- FIX: Add a post-reranking confidence check ---
            # Cross-encoder scores for irrelevant docs are often large negative numbers.
            # This is a powerful final filter that rejects gibberish queries.
            final_results = [
                chunk for chunk in reranked_results if chunk["score"] > -5.0
            ]
            
        else:
            final_results = confident_results[:top_k]
        
        # 5. Apply PII Masking (if required)
        if apply_pii_mask:
            results_to_format = mask_pii_in_results(final_results)
        else:
            results_to_format = final_results
            
        # 6. Format for final citation output
        citations = format_citations(results_to_format)
            
        return citations

# Singleton instance
hybrid_retriever = HybridRetriever()
