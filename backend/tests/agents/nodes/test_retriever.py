import pytest
from unittest.mock import patch, AsyncMock
from app.agents.nodes.retriever import RetrieverNode
from app.agents.state import AgentState

@pytest.mark.asyncio
@patch('app.agents.nodes.retriever.hybrid_retriever', new_callable=AsyncMock)
async def test_retriever_node(mock_hybrid_retriever):
    """Tests that the RetrieverNode calls the hybrid retriever and updates state."""
    # 1. Setup
    mock_retrieved_chunks = [{"text": "chunk 1"}, {"text": "chunk 2"}]
    mock_hybrid_retriever.retrieve.return_value = mock_retrieved_chunks

    retriever = RetrieverNode()
    initial_state = AgentState(query="What is RAG?", errors=[], context=[])

    # 2. Action
    updated_state = await retriever(initial_state)

    # 3. Assertions
    mock_hybrid_retriever.retrieve.assert_called_once_with("What is RAG?", top_k=10, rerank=False, apply_pii_mask=False)
    assert "context" in updated_state
    assert updated_state["context"] == mock_retrieved_chunks
    assert len(updated_state["context"]) == 2