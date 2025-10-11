import pytest
from app.agents.nodes.tool_node import ToolNode
from app.agents.state import AgentState

@pytest.mark.asyncio
async def test_tool_node_appends_results():
    """Tests that the ToolNode executes a mock tool call and appends the result to the context."""
    # 1. Setup
    tool_node = ToolNode()
    initial_state = AgentState(
        tool_calls=[{"type": "search_web", "args": {"query": "LangGraph"}}],
        context=[{"text": "initial context"}],
        errors=[]
    )

    # 2. Action
    updated_state = await tool_node(initial_state)

    # 3. Assertions
    assert len(updated_state["context"]) == 2  # Initial context + tool result
    tool_result = updated_state["context"][1]
    assert "Mock result for tool 'search_web'" in tool_result["text"]
    assert tool_result["metadata"]["source"] == "tool"