from typing import List, Set

def precision_at_k(retrieved_docs: List[str], expected_docs: Set[str], k: int) -> float:
    """Calculates Precision@k."""
    if k == 0:
        return 0.0
    retrieved_k = set(retrieved_docs[:k])
    relevant_retrieved = len(retrieved_k.intersection(expected_docs))
    return relevant_retrieved / k

def recall_at_k(retrieved_docs: List[str], expected_docs: Set[str], k: int) -> float:
    """Calculates Recall@k."""
    if not expected_docs:
        return 0.0
    retrieved_k = set(retrieved_docs[:k])
    relevant_retrieved = len(retrieved_k.intersection(expected_docs))
    return relevant_retrieved / len(expected_docs)

# MRR and nDCG can be added here later for more advanced evaluation.