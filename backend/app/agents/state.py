from typing import TypedDict, List, Dict, Any, Annotated
import operator

class AgentState(TypedDict):
    """
    Represents the state of our agent graph.
    """
    query: str
    context: List[Dict[str, Any]]
    plan: str
    answer: str
    citations: List[Dict[str, Any]]
    tool_calls: List[Dict[str, Any]]
    
    # operator.add appends to the list instead of overwriting it.
    errors: Annotated[List[str], operator.add]

    # Tracks the number of times the solver has been retried
    retry_count: int
    
    # A flag to signal the need for a human-in-the-loop interrupt
    interrupt_required: bool
    conversation_history: List[Dict[str, Any]]