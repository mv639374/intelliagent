# from langgraph.graph import StateGraph, END
# from app.agents.state import AgentState
# from app.agents.checkpointer import PostgresCheckpointer
# from app.agents.memory.memory_manager import memory_manager

# # Import all the nodes
# from app.agents.nodes.planner import planner_node
# from app.agents.nodes.retriever import retriever_node
# from app.agents.nodes.solver import solver_node
# from app.agents.nodes.verifier import verifier_node
# from app.agents.nodes.tool_node import tool_node

# # Import the routing and conditional edge logic from their separate files
# from app.agents.edges.routing_logic import route_after_planner, route_after_tools
# from app.agents.edges.conditional_edge import should_retry_solver

# # --- NEW FOR STEP 2.5 ---
# async def load_memory_node(state: AgentState) -> AgentState:
#     """
#     Loads conversation history into the state at the beginning of a run.
#     This makes the agent aware of the conversation's context before planning.
#     """
#     # The 'thread_id' is the unique identifier for a conversation
#     # and is passed into the graph's config.
#     conversation_id = state.get("configurable", {}).get("thread_id")
    
#     if conversation_id:
#         history = await memory_manager.load_history(conversation_id)
#         state['conversation_history'] = history
#         print(f"--- 🧠 Loaded {len(history)} messages into memory ---")
#     else:
#         state['conversation_history'] = []
        
#     return state
# # --- END NEW FOR STEP 2.5 ---


# def create_agent_graph():
#     """
#     Builds and compiles the main agent graph with memory, conditional routing,
#     and all agentic nodes.
#     """
#     checkpointer = PostgresCheckpointer()
    
#     graph_builder = StateGraph(AgentState)
    
#     # 1. Add all nodes to the graph
#     graph_builder.add_node("load_memory", load_memory_node) # New memory node
#     graph_builder.add_node("planner", planner_node)
#     graph_builder.add_node("retriever", retriever_node)
#     graph_builder.add_node("solver", solver_node)
#     graph_builder.add_node("verifier", verifier_node)
#     graph_builder.add_node("tool_node", tool_node)
    
#     # 2. Define the graph's entry point
#     graph_builder.set_entry_point("load_memory") # <-- UPDATED entry point
    
#     # 3. Add all edges
    
#     # Standard Edges
#     graph_builder.add_edge("load_memory", "planner") # <-- NEW edge from memory to planner
#     graph_builder.add_edge("retriever", "solver")
#     graph_builder.add_edge("solver", "verifier")

#     # Conditional Edges
#     graph_builder.add_conditional_edges(
#         "planner",
#         route_after_planner,
#         {"tool_node": "tool_node", "retriever": "retriever"}
#     )
#     graph_builder.add_conditional_edges(
#         "verifier",
#         should_retry_solver,
#         {"solver": "solver", "__end__": END}
#     )
#     graph_builder.add_conditional_edges(
#         "tool_node",
#         route_after_tools,
#         {"retriever": "retriever", "__end__": END}
#     )

#     # Compile the final graph with the checkpointer
#     agent_graph = graph_builder.compile(checkpointer=checkpointer)
    
#     return agent_graph

# # A global instance of the compiled, final graph
# main_agent_graph = create_agent_graph()


from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.checkpointer import PostgresCheckpointer
from app.agents.memory.memory_manager import memory_manager

# Import all the nodes
from app.agents.nodes.planner import planner_node
from app.agents.nodes.retriever import retriever_node
from app.agents.nodes.solver import solver_node
from app.agents.nodes.verifier import verifier_node
from app.agents.nodes.tool_node import tool_node

# Import the routing and conditional edge logic from their separate files
from app.agents.edges.routing_logic import route_after_planner, route_after_tools
from app.agents.edges.conditional_edge import should_retry_solver

# --- NEW FOR STEP 2.5 ---
async def load_memory_node(state: AgentState) -> AgentState:
    """
    Loads conversation history into the state at the beginning of a run.
    This makes the agent aware of the conversation's context before planning.
    """
    # The 'thread_id' is the unique identifier for a conversation
    # and is passed into the graph's config.
    conversation_id = state.get("configurable", {}).get("thread_id")
    
    if conversation_id:
        history = await memory_manager.load_history(conversation_id)
        state['conversation_history'] = history
        print(f"--- 🧠 Loaded {len(history)} messages into memory ---")
    else:
        state['conversation_history'] = []
        
    return state
# --- END NEW FOR STEP 2.5 ---


def create_agent_graph():
    """
    Builds and compiles the main agent graph with memory, conditional routing,
    and all agentic nodes.
    """
    checkpointer = PostgresCheckpointer()
    
    graph_builder = StateGraph(AgentState)
    
    # 1. Add all nodes to the graph
    graph_builder.add_node("load_memory", load_memory_node) # New memory node
    graph_builder.add_node("planner", planner_node)
    graph_builder.add_node("retriever", retriever_node)
    graph_builder.add_node("solver", solver_node)
    graph_builder.add_node("verifier", verifier_node)
    graph_builder.add_node("tool_node", tool_node)
    
    # 2. Define the graph's entry point
    graph_builder.set_entry_point("load_memory") # <-- UPDATED entry point
    
    # 3. Add all edges
    
    # Standard Edges
    graph_builder.add_edge("load_memory", "planner") # <-- NEW edge from memory to planner
    graph_builder.add_edge("retriever", "solver")
    graph_builder.add_edge("solver", "verifier")

    # Conditional Edges
    graph_builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {"tool_node": "tool_node", "retriever": "retriever"}
    )
    graph_builder.add_conditional_edges(
        "verifier",
        should_retry_solver,
        {"solver": "solver", "__end__": END}
    )
    graph_builder.add_conditional_edges(
        "tool_node",
        route_after_tools,
        {"retriever": "retriever", "__end__": END}
    )

    # Compile the final graph with the checkpointer
    agent_graph = graph_builder.compile(checkpointer=checkpointer)
    
    return agent_graph

# A global instance of the compiled, final graph
main_agent_graph = create_agent_graph()
