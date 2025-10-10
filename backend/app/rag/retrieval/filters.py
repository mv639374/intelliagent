from typing import List, Dict, Any

# Define confidence thresholds. These can be tuned based on evaluation.
VECTOR_SCORE_THRESHOLD = 0.4
BM25_SCORE_THRESHOLD = 1.0

def filter_low_confidence(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filters a list of chunks, removing those with scores below defined thresholds.
    This filter is applied after fusion but before reranking.

    Args:
        chunks: A list of chunks, each with a fused 'score'.

    Returns:
        A filtered list of chunks that meet the confidence criteria.
    """
    # The RRF score is a good general indicator. We can set a baseline for it.
    # A more advanced filter could check the original scores if they were preserved.
    RRF_SCORE_THRESHOLD = 0.01 # RRF scores are small, so the threshold is low
    
    filtered_chunks = []
    for chunk in chunks:
        if chunk.get("score", 0) >= RRF_SCORE_THRESHOLD:
            filtered_chunks.append(chunk)
            
    print(f"Filtered chunks: {len(chunks)} -> {len(filtered_chunks)}")
    return filtered_chunks