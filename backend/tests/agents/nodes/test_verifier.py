import pytest
from app.agents.nodes.verifier import VerifierNode
from app.agents.state import AgentState

@pytest.mark.asyncio
async def test_verifier_node_detects_missing_citations():
    """Tests that the VerifierNode adds an error if citations are missing."""
    # 1. Setup
    verifier = VerifierNode()
    state_no_citations = AgentState(answer="This answer has no citations.", errors=[])

    # 2. Action
    updated_state = await verifier(state_no_citations)

    # 3. Assertions
    assert len(updated_state["errors"]) == 1
    assert "No citations found" in updated_state["errors"][0]

@pytest.mark.asyncio
async def test_verifier_node_passes_with_citations():
    """Tests that the VerifierNode does not add an error if citations are present."""
    # 1. Setup
    verifier = VerifierNode()
    state_with_citations = AgentState(answer="This answer is correct [1].", errors=[])

    # 2. Action
    updated_state = await verifier(state_with_citations)

    # 3. Assertions
    assert len(updated_state.get("errors", [])) == 0