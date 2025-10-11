import pytest
from unittest.mock import MagicMock, AsyncMock
from app.agents.nodes.planner import PlannerNode
from app.agents.state import AgentState

@pytest.mark.asyncio
async def test_planner_node():
    """Tests that the PlannerNode correctly invokes the LLM and updates the state."""
    # 1. Setup
    mock_llm = MagicMock()
    mock_llm.ainvoke = AsyncMock(return_value=MagicMock(content="1. Step one.\n2. Step two."))
    
    planner = PlannerNode()
    planner.llm = mock_llm  # Inject the mock LLM

    initial_state = AgentState(query="Explain RAG", errors=[], context=[])

    # 2. Action
    updated_state = await planner(initial_state)

    # 3. Assertions
    mock_llm.ainvoke.assert_called_once()  # Verify LLM was called
    assert "plan" in updated_state
    assert updated_state["plan"] == "1. Step one.\n2. Step two."