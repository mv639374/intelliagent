# import uuid
# from app.agents.graph_factory import main_agent_graph
# from app.agents.state import AgentState
# from app.agents.checkpointer import PostgresCheckpointer
# from sqlalchemy import select
# from app.db.sync_session import get_sync_db
# from app.models.graph_checkpoint import GraphCheckpoint
# import asyncio

# async def run_tests():
#     thread_id = str(uuid.uuid4())
#     config = {"configurable": {"thread_id": thread_id}}
    
#     print("--- 1. Testing Simple Graph Invocation ---")
#     initial_state = AgentState(query="Test query", errors=[], interrupt_required=False)
#     final_state = await main_agent_graph.ainvoke(initial_state, config=config)
#     assert final_state['query'] == "Test query"
#     print("✅ Checkpoint 1 Passed: Simple graph invoked successfully.\n")

#     print("--- 2. Testing State Persistence and Resumption ---")
#     checkpointer = PostgresCheckpointer()
#     saved_tuple = await checkpointer.aget_tuple(config)
#     assert saved_tuple is not None
#     assert saved_tuple.checkpoint['channel_values']['query'] == "Test query"
#     print("✅ Checkpoint 2 Passed: State was persisted and retrieved from Postgres.\n")

#     print("--- 3. Testing Interrupts ---")
#     # Simulate a state that should cause an interrupt
#     interrupt_state = AgentState(
#         query="Test interrupt", 
#         tool_calls=[{"type": "execute_code"}], 
#         errors=[], 
#         interrupt_required=False
#     )
#     # Note: Our simple graph doesn't have the interrupt logic wired yet.
#     # We are just setting the flag to demonstrate the principle.
#     from app.agents.interrupts import should_interrupt
#     assert should_interrupt(interrupt_state) is True
#     print("✅ Checkpoint 3 Passed: Interrupt logic correctly identifies tool call requiring consent.\n")

#     print("--- 4. Testing Graph Structure (Unit Test) ---")
#     assert "start" in main_agent_graph.nodes
#     assert "end" in main_agent_graph.nodes
#     print("✅ Checkpoint 4 Passed: Graph factory test asserts nodes are present.")

# if __name__ == "__main__":
#     asyncio.run(run_tests()) 


import uuid
from app.agents.graph_factory import main_agent_graph
from app.agents.state import AgentState
from app.agents.checkpointer import PostgresCheckpointer
from sqlalchemy import select
from app.db.sync_session import get_sync_db
from app.models.graph_checkpoint import GraphCheckpoint

def run_tests():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("--- 1. Testing Simple Graph Invocation ---")
    initial_state = AgentState(query="Test query", errors=[], interrupt_required=False)
    final_state = main_agent_graph.invoke(initial_state, config=config)
    assert final_state['query'] == "Test query"
    print("✅ Checkpoint 1 Passed: Simple graph invoked successfully.\n")

    print("--- 2. Testing State Persistence and Resumption ---")
    checkpointer = PostgresCheckpointer()
    saved_tuple = checkpointer.get_tuple(config)
    assert saved_tuple is not None
    assert saved_tuple.checkpoint['channel_values']['query'] == "Test query"
    print("✅ Checkpoint 2 Passed: State was persisted and retrieved from Postgres.\n")

    print("--- 3. Testing Interrupts ---")
    # Simulate a state that should cause an interrupt
    interrupt_state = AgentState(
        query="Test interrupt", 
        tool_calls=[{"type": "execute_code"}], 
        errors=[], 
        interrupt_required=False
    )
    # Note: Our simple graph doesn't have the interrupt logic wired yet.
    # We are just setting the flag to demonstrate the principle.
    from app.agents.interrupts import should_interrupt
    assert should_interrupt(interrupt_state) is True
    print("✅ Checkpoint 3 Passed: Interrupt logic correctly identifies tool call requiring consent.\n")

    print("--- 4. Testing Graph Structure (Unit Test) ---")
    assert "start" in main_agent_graph.nodes
    assert "end" in main_agent_graph.nodes
    print("✅ Checkpoint 4 Passed: Graph factory test asserts nodes are present.")

if __name__ == "__main__":
    run_tests()