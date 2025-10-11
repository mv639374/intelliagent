from app.agents.state import AgentState
from app.agents.interrupts import should_interrupt

# Keywords that trigger the tool-use branch
TOOL_KEYWORDS = ["tool", "search", "api", "execute", "browse"]

def route_after_planner(state: AgentState) -> str:
    """
    Determines the next step after the planner has run.
    If the plan mentions tool use, it routes to the tool node.
    Otherwise, it proceeds to the retriever.
    
    Ref: implementation_plan_2.pdf, Step 2.3, Sub-step 3
    """
    plan = state.get("plan", "").lower()
    if any(keyword in plan for keyword in TOOL_KEYWORDS):
        print("--- Routing: Planner -> Tool Node ---")
        return "tool_node"
    else:
        print("--- Routing: Planner -> Retriever ---")
        return "retriever"

def route_after_tools(state: AgentState) -> str:
    """
    Determines the route after the tool node has executed.
    If an interrupt is required for human consent, the graph pauses.
    Otherwise, it proceeds to the retriever to process tool results.

    Ref: implementation_plan_2.pdf, Step 2.3, Sub-step 5
    """
    if should_interrupt(state):
        print("--- Routing: Interrupt Required. Pausing for human-in-the-loop. ---")
        return "__end__"  # End the graph to wait for human input
    else:
        print("--- Routing: Tools -> Retriever ---")
        return "retriever"