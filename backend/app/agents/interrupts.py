from .state import AgentState

# In a real app, this would be a more complex list, perhaps from a config file.
TOOLS_REQUIRING_CONSENT = ["execute_code", "delete_file"]

def should_interrupt(state: AgentState) -> bool:
    """
    Determines if the graph should be interrupted for human-in-the-loop approval.
    """
    if state.get("interrupt_required"):
        return True
        
    if state.get("tool_calls"):
        for tool_call in state["tool_calls"]:
            if tool_call["type"] in TOOLS_REQUIRING_CONSENT:
                # Set a flag in the state so we know why we interrupted
                state["interrupt_required"] = True
                return True
    return False