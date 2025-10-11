# import json
# import uuid
# import time
# from typing import AsyncGenerator
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.responses import StreamingResponse
# from app.schemas.chat import AskRequest, AskResponse
# from app.rag.retrieval.hybrid_retriever import hybrid_retriever
# from app.api.deps import get_current_user
# from app.models.user import User
# from app.agents.graph_factory import main_agent_graph
# from app.agents.state import AgentState
# from app.agents.memory.memory_manager import memory_manager

# router = APIRouter()

# @router.post("/ask", response_model=AskResponse)
# async def ask_question(
#     request: AskRequest,
#     current_user: User = Depends(get_current_user)
# ):
#     """
#     Receives a user query, retrieves relevant documents using the hybrid retriever,
#     and returns formatted citations.
#     """
#     try:
#         start_time = time.time()
        
#         # Determine if PII should be masked based on user role (example logic)
#         apply_pii_mask = current_user.role != "admin"

#         results = await hybrid_retriever.retrieve(
#             query=request.query,
#             top_k=request.top_k,
#             rerank=request.rerank,
#             apply_pii_mask=apply_pii_mask
#         )
        
#         end_time = time.time()
        
#         return AskResponse(
#             query=request.query,
#             citations=results,
#             metadata={
#                 "user_id": str(current_user.id),
#                 "project_id": str(request.project_id),
#                 "retrieval_time_ms": (end_time - start_time) * 1000
#             }
#         )
#     except Exception as e:
#         print(f"Error during retrieval: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An error occurred while processing your request."
#         )



# @router.post("/stream")
# async def stream_agent_response(
#     request: AskRequest,
#     current_user: User = Depends(get_current_user)
# ):
#     """
#     Streams the agent's execution events in real-time.
#     This includes node transitions, tool calls, and final answer tokens.
#     """
#     conversation_id = str(uuid.uuid4()) # For a real app, you'd get this from the request or DB

#     async def event_generator() -> AsyncGenerator[str, None]:
#         # Initial state for the graph
#         initial_state = AgentState(
#             query=request.query,
#             conversation_history=[],
#             context=[], plan="", answer="", citations=[], tool_calls=[],
#             errors=[], retry_count=0, interrupt_required=False
#         )
        
#         config = {"configurable": {"thread_id": conversation_id}}
#         final_answer = ""

#         try:
#             # astream_events provides a real-time feed of graph events
#             async for event in main_agent_graph.astream_events(initial_state, config, version="v1"):
#                 event_data = {"event": event["event"]}
                
#                 # Stream tokens from the solver node as they are generated
#                 if event["event"] == "on_chat_model_stream":
#                     chunk = event["data"].get("chunk")
#                     if chunk and hasattr(chunk, 'content'):
#                         token = chunk.content
#                         final_answer += token
#                         event_data["data"] = {"token": token}
                
#                 # Stream information about which node is currently running
#                 elif event["event"] == "on_chain_start" and event["name"] != "LangGraph":
#                      event_data["data"] = {"node": event["name"]}

#                 # Send the formatted event to the client
#                 yield f"data: {json.dumps(event_data)}\n\n"
            
#             # After the stream is complete, save the conversation history
#             await memory_manager.save_message(conversation_id, "user", request.query)
#             await memory_manager.save_message(conversation_id, "ai", final_answer)

#         except Exception as e:
#             print(f"Error during agent stream: {e}")
#             error_event = {"event": "error", "data": {"message": "An error occurred."}}
#             yield f"data: {json.dumps(error_event)}\n\n"

#     return StreamingResponse(event_generator(), media_type="text/event-stream")


import json
import uuid
import time
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from app.schemas.chat import AskRequest, AskResponse
from app.rag.retrieval.hybrid_retriever import hybrid_retriever
from app.api.deps import get_current_user
from app.models.user import User
from app.agents.graph_factory import main_agent_graph
from app.agents.state import AgentState
from app.agents.memory.memory_manager import memory_manager

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Receives a user query, retrieves relevant documents using the hybrid retriever,
    and returns formatted citations.
    """
    try:
        start_time = time.time()
        apply_pii_mask = current_user.role != "admin"
        
        results = await hybrid_retriever.retrieve(
            query=request.query,
            top_k=request.top_k,
            rerank=request.rerank,
            apply_pii_mask=apply_pii_mask
        )
        
        end_time = time.time()
        return AskResponse(
            query=request.query,
            citations=results,
            metadata={
                "user_id": str(current_user.id),
                "project_id": str(request.project_id),
                "retrieval_time_ms": (end_time - start_time) * 1000
            }
        )
    except Exception as e:
        print(f"Error during retrieval: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )

@router.post("/stream")
async def stream_agent_response(
    request: AskRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Streams the agent's execution events in real-time.
    This includes node transitions, tool calls, and final answer tokens.
    """
    conversation_id = str(uuid.uuid4())
    
    # Print user query prominently
    print("\n" + "="*80)
    print(f"🔍 USER QUERY: {request.query}")
    print("="*80 + "\n")
    
    async def event_generator() -> AsyncGenerator[str, None]:
        initial_state = AgentState(
            query=request.query,
            conversation_history=[],
            context=[], plan="", answer="", citations=[], tool_calls=[],
            errors=[], retry_count=0, interrupt_required=False
        )
        
        config = {"configurable": {"thread_id": conversation_id}}
        final_answer = ""
        
        try:
            async for event in main_agent_graph.astream_events(initial_state, config, version="v1"):
                event_data = {"event": event["event"]}
                
                if event["event"] == "on_chat_model_stream":
                    chunk = event["data"].get("chunk")
                    if chunk and hasattr(chunk, 'content'):
                        token = chunk.content
                        final_answer += token
                        event_data["data"] = {"token": token}
                
                elif event["event"] == "on_chain_start" and event["name"] != "LangGraph":
                    event_data["data"] = {"node": event["name"]}
                
                yield f"data: {json.dumps(event_data)}\n\n"
            
            # Print final answer after stream completes successfully
            print("\n" + "="*80)
            print(f"✅ FINAL ANSWER FROM LLM:")
            print("="*80)
            print(final_answer)
            print("="*80 + "\n")
            
            # Save conversation history
            await memory_manager.save_message(conversation_id, "user", request.query)
            await memory_manager.save_message(conversation_id, "assistant", final_answer)
            
        except Exception as e:
            # Only print error if it's NOT a LangChain tracer exception
            if "TracerException" not in str(e) and "No indexed run ID" not in str(e):
                print(f"❌ Error during agent stream: {e}")
                error_event = {"event": "error", "data": {"message": "An error occurred."}}
                yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
