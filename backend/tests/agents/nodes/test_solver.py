import pytest
from unittest.mock import MagicMock, AsyncMock
from app.agents.nodes.solver import SolverNode
from app.agents.state import AgentState

@pytest.mark.asyncio
async def test_solver_node():
    """Tests that the SolverNode formats context and generates a cited answer."""
    # 1. Setup
    mock_llm = MagicMock()
    mock_llm.ainvoke = AsyncMock(return_value=MagicMock(content="This is the answer [1]."))
    
    solver = SolverNode()
    solver.llm = mock_llm

    initial_state = AgentState(
        query="What is RAG?",
        context=[{"text": "RAG is Retrieval-Augmented Generation."}],
        errors=[]
    )

    # 2. Action
    updated_state = await solver(initial_state)

    # 3. Assertions
    mock_llm.ainvoke.assert_called_once()
    prompt_arg = mock_llm.ainvoke.call_args[0][0]
    assert "[1] RAG is Retrieval-Augmented Generation." in prompt_arg  # Check context formatting
    assert "answer" in updated_state
    assert updated_state["answer"] == "This is the answer [1]."