import pytest
from langgraph.graph.graph import CompiledGraph

from app.agents.graph_factory import create_agent_graph

def test_create_agent_graph_builds_correctly():
    """
    Unit test to verify that the graph factory function
    builds and compiles a graph with the expected nodes.
    """
    # 1. Action: Create the graph
    agent_graph = create_agent_graph()

    # 2. Assertions
    
    # Assert that the returned object is a compiled LangGraph
    assert isinstance(agent_graph, CompiledGraph)

    # Assert that the placeholder nodes from Step 2.1 exist
    assert "start" in agent_graph.nodes
    assert "end" in agent_graph.nodes
    
    # Assert the entry point is set correctly
    # assert agent_graph.entry_point == "start"