from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid

class AskRequest(BaseModel):
    query: str
    project_id: uuid.UUID
    top_k: int = 10
    rerank: bool = True

class Citation(BaseModel):
    source: str
    text_snippet: str
    score: float
    document_id: str
    chunk_id: str

class AskResponse(BaseModel):
    query: str
    citations: List[Citation]
    metadata: Dict[str, Any] = {}