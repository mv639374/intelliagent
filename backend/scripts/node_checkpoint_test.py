import asyncio
from app.agents.state import AgentState
from app.agents.nodes.planner import planner_node
from app.agents.nodes.retriever import retriever_node
from app.agents.nodes.solver import solver_node
from app.agents.nodes.verifier import verifier_node
from app.agents.nodes.tool_node import tool_node

async def run_node_tests():
    """Runs integration checks for each agent node."""
    
    print("--- Running Node Checkpoint Tests ---\n")
    
    # Checkpoint 1: Planner
    try:
        state1 = AgentState(query="Explain RAG in simple terms.", errors=[])
        state1 = await planner_node(state1)
        assert "plan" in state1 and len(state1["plan"].split('\n')) >= 2
        print("✅ 1. Planner node: PASSED")
    except Exception as e:
        print(f"❌ 1. Planner node: FAILED - {e}")

    # Checkpoint 2: Retriever
    try:
        # Assumes you have indexed project_details.pdf
        state2 = AgentState(query="What is LangGraph?", context=[], errors=[])
        state2 = await retriever_node(state2)
        assert "context" in state2 and len(state2["context"]) > 0
        print("✅ 2. Retriever node: PASSED")
    except Exception as e:
        print(f"❌ 2. Retriever node: FAILED - {e}")

    # Checkpoint 3: Solver
    try:
        state3 = AgentState(query="What is RAG?", context=[{"text": "RAG is a technique."}], errors=[])
        state3 = await solver_node(state3)
        assert "answer" in state3 and "[1]" in state3["answer"]
        print("✅ 3. Solver node: PASSED")
    except Exception as e:
        print(f"❌ 3. Solver node: FAILED - {e}")

    # Checkpoint 4: Verifier
    try:
        state4 = AgentState(answer="This is an answer without citations.", errors=[])
        state4 = await verifier_node(state4)
        assert len(state4["errors"]) == 1
        print("✅ 4. Verifier node: PASSED")
    except Exception as e:
        print(f"❌ 4. Verifier node: FAILED - {e}")

    # Checkpoint 5: Tool Node
    try:
        state5 = AgentState(tool_calls=[{"type": "mock_tool"}], context=[], errors=[])
        state5 = await tool_node(state5)
        assert len(state5["context"]) == 1 and "Mock result" in state5["context"][0]["text"]
        print("✅ 5. Tool node: PASSED")
    except Exception as e:
        print(f"❌ 5. Tool node: FAILED - {e}")

if __name__ == "__main__":
    # Ensure you have uploaded and indexed a document before running
    print("NOTE: Ensure 'project_details.pdf' is indexed for the retriever test to pass.")
    asyncio.run(run_node_tests())