import pytest
import uuid
from unittest.mock import MagicMock, AsyncMock

from app.agents.graph_factory import create_agent_graph
from app.agents.state import AgentState

# Mock the nodes to control their behavior for testing routing
@pytest.fixture
def mock_nodes():
    planner = AsyncMock(return_value={"plan": ""})
    retriever = AsyncMock(return_value={"context": [{"text": "mock context"}]})
    solver = AsyncMock(return_value={"answer": "mock answer [1]"})
    verifier = AsyncMock(return_value={"errors": []})
    tool_node = AsyncMock(return_value={"context": [{"text": "mock tool result"}]})
    return {
        "planner": planner, "retriever": retriever, "solver": solver,
        "verifier": verifier, "tool_node": tool_node
    }

def build_test_graph(mock_nodes):
    """Helper to build a graph with mocked nodes for testing."""
    graph = create_agent_graph()
    for name, mock_func in mock_nodes.items():
        graph.nodes[name]['func'] = mock_func
    return graph

# Test 1: Graph with Retry
@pytest.mark.asyncio
async def test_graph_with_retry_logic(mock_nodes):
    # Verifier fails once, then succeeds
    mock_nodes["verifier"].side_effect = [{"errors": ["No citations"]}, {"errors": []}]
    graph = build_test_graph(mock_nodes)
    
    initial_state = AgentState(query="test", retry_count=0, errors=[])
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    final_state = await graph.ainvoke(initial_state, config)

    assert mock_nodes["solver"].call_count == 2 # Called once initially, then retried
    assert mock_nodes["verifier"].call_count == 2
    assert final_state["retry_count"] == 1 # Incremented once

# Test 2: Graph with Tool Routing
@pytest.mark.asyncio
async def test_graph_with_tool_routing(mock_nodes):
    mock_nodes["planner"].return_value = {"plan": "I need to use a tool."}
    graph = build_test_graph(mock_nodes)

    initial_state = AgentState(query="test", retry_count=0, errors=[])
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    await graph.ainvoke(initial_state, config)
    
    mock_nodes["tool_node"].assert_called_once()
    mock_nodes["retriever"].assert_called_once() # Called after tool node
    assert mock_nodes["solver"].call_count == 1

# Test 3: Max Retries
@pytest.mark.asyncio
async def test_graph_with_max_retries(mock_nodes):
    mock_nodes["verifier"].return_value = {"errors": [" постійна помилка"]} # Always fails
    graph = build_test_graph(mock_nodes)

    initial_state = AgentState(query="test", retry_count=0, errors=[])
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    final_state = await graph.ainvoke(initial_state, config)

    assert mock_nodes["solver"].call_count == 3 # Initial + 2 retries
    assert final_state["retry_count"] == 2

# Test 4: Interrupt Logic
@pytest.mark.asyncio
async def test_graph_with_interrupt(mock_nodes):
    mock_nodes["planner"].return_value = {"plan": "Use the execute_code tool."}
    # Tool node returns a tool call that requires consent
    mock_nodes["tool_node"].return_value = {"tool_calls": [{"type": "execute_code"}]}
    graph = build_test_graph(mock_nodes)

    initial_state = AgentState(query="test", retry_count=0, errors=[])
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    final_state = await graph.ainvoke(initial_state, config)

    # The graph should end after the tool node due to the interrupt
    mock_nodes["tool_node"].assert_called_once()
    mock_nodes["retriever"].assert_not_called() # Does not proceed to retriever
    assert final_state["interrupt_required"] is True