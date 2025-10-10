from unittest.mock import MagicMock, patch

from app.rag.index.keyword_indexer import KeywordIndexer


@patch("app.rag.index.keyword_indexer.es_client", new_callable=MagicMock)
def test_keyword_indexer(mock_es_client):
    """
    Tests that the indexer correctly calls the bulk index method.
    """
    # 1. Setup
    indexer = KeywordIndexer()
    sample_chunks = [
        {"chunk_id": "1", "text": "Chunk one.", "metadata": {}},
        {"chunk_id": "2", "text": "Chunk two.", "metadata": {}},
    ]

    # 2. Action
    indexer.index_chunks(sample_chunks)

    # 3. Assertion
    # Verify that the underlying bulk_index_chunks method was called once
    mock_es_client.bulk_index_chunks.assert_called_once()

    # Check the content of the call
    call_args = mock_es_client.bulk_index_chunks.call_args[0][0]
    assert len(call_args) == len(sample_chunks)
    assert call_args[0]["chunk_id"] == "1"
