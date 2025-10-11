import re
from app.agents.state import AgentState

class VerifierNode:
    """
    A node that verifies the quality of the generated answer.
    """
    async def __call__(self, state: AgentState) -> AgentState:
        print("--- ✅ Verifier Node ---")
        
        answer = state.get('answer', '')
        
        # Check for citations in the format [1], [2], etc.
        if not re.search(r'\[\d+\]', answer):
            error_message = "Answer verification failed: No citations found. The answer is not grounded in the provided context."
            print(error_message)
            state['errors'].append(error_message)
        else:
            print("Answer verification passed: Citations are present.")
            
        return state

verifier_node = VerifierNode()