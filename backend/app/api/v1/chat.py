from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.chat import AskRequest, AskResponse
from app.rag.retrieval.hybrid_retriever import hybrid_retriever
from app.api.deps import get_current_user # Will update this dependency next
from app.models.user import User
import time

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
        
        # Determine if PII should be masked based on user role (example logic)
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