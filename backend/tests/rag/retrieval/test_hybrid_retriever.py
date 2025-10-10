import pytest
from app.rag.retrieval.fusion import reciprocal_rank_fusion

def test_reciprocal_rank_fusion():
    """
    Tests the RRF algorithm with mock retriever results.
    """
    # Results from Retriever 1
    results1 = [
        {"chunk_id": "A", "text": "..."},
        {"chunk_id": "B", "text": "..."},
        {"chunk_id": "C", "text": "..."},
    ]
    # Results from Retriever 2
    results2 = [
        {"chunk_id": "B", "text": "..."},
        {"chunk_id": "A", "text": "..."},
        {"chunk_id": "D", "text": "..."},
    ]

    # k=1 for simple calculation
    fused = reciprocal_rank_fusion([results1, results2], k=1)

    # Expected scores (1/(k+rank)):
    # A: (1/(1+1)) + (1/(1+2)) = 0.5 + 0.333 = 0.833
    # B: (1/(1+2)) + (1/(1+1)) = 0.333 + 0.5 = 0.833
    # C: (1/(1+3)) = 0.25
    # D: (1/(1+3)) = 0.25
    # Since A and B have the same score, their order might vary but they should be first.
    # C and D have the same score, they should be last.
    
    assert len(fused) == 4
    
    # Check that A and B are the top 2 results
    top_2_ids = {fused[0]["chunk_id"], fused[1]["chunk_id"]}
    assert top_2_ids == {"A", "B"}
    
    # Check that C and D are the last 2 results
    last_2_ids = {fused[2]["chunk_id"], fused[3]["chunk_id"]}
    assert last_2_ids == {"C", "D"}

    # Check scores (approximately)
    assert fused[0]["score"] == pytest.approx(0.833, abs=1e-3)
    assert fused[1]["score"] == pytest.approx(0.833, abs=1e-3)