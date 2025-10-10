from typing import List, Dict, Any
from collections import defaultdict

def reciprocal_rank_fusion(
    results_list: List[List[Dict[str, Any]]], 
    k: int = 60
) -> List[Dict[str, Any]]:
    """
    Performs Reciprocal Rank Fusion on a list of search results from multiple retrievers.

    Args:
        results_list: A list where each element is a ranked list of chunks from a retriever.
        k: A constant used in the RRF formula to control the influence of lower ranks.

    Returns:
        A single, fused, and re-ranked list of chunks.
    """
    ranked_scores = defaultdict(float)

    # Aggregate scores for each unique chunk
    for results in results_list:
        for rank, chunk in enumerate(results):
            chunk_id = chunk["chunk_id"]
            rrf_score = 1.0 / (k + rank + 1)
            ranked_scores[chunk_id] += rrf_score

    if not ranked_scores:
        return []

    # Create a unified map of chunk_id to chunk data
    all_chunks_map = {
        chunk["chunk_id"]: chunk
        for results in results_list
        for chunk in results
    }

    # Sort chunks based on their fused RRF score
    sorted_chunk_ids = sorted(ranked_scores.keys(), key=lambda id: ranked_scores[id], reverse=True)

    # Reconstruct the final ranked list
    fused_results = []
    for chunk_id in sorted_chunk_ids:
        chunk = all_chunks_map[chunk_id]
        chunk["score"] = ranked_scores[chunk_id] # Update score to RRF score
        fused_results.append(chunk)

    return fused_results