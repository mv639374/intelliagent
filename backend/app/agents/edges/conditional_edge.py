from app.agents.state import AgentState

def should_retry_solver(state: AgentState) -> str:
    """
    Determines if the solver should be retried after a verification failure.
    If errors are present and the retry limit has not been reached, it routes back to the solver.
    Otherwise, the graph execution ends.
    
    Ref: implementation_plan_2.pdf, Step 2.3, Sub-step 2 & 4
    """
    errors = state.get("errors", [])
    retry_count = state.get("retry_count", 0)

    if errors:
        if retry_count < 2:
            print(f"--- Routing: Verification Failed. Retrying solver (Attempt {retry_count + 1}) ---")
            # The retry count is incremented in the state by the graph factory just before this is called
            return "solver"

    print("--- Routing: Verification Passed or Max Retries Reached. Ending. ---")
    return "__end__"