from app.rag.retrieval.filters import filter_low_confidence

def test_filter_low_confidence():
    """
    Tests that the filter correctly removes chunks with scores below the threshold.
    """
    mock_chunks = [
        {"chunk_id": "A", "score": 0.9},
        {"chunk_id": "B", "score": 0.5},
        {"chunk_id": "C", "score": 0.005}, # Below threshold
        {"chunk_id": "D", "score": 0.0},    # Below threshold
        {"chunk_id": "E", "score": 0.02},  # Above threshold
    ]

    filtered = filter_low_confidence(mock_chunks)

    assert len(filtered) == 3
    
    filtered_ids = {chunk["chunk_id"] for chunk in filtered}
    assert filtered_ids == {"A", "B", "E"}