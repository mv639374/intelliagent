from fastapi import APIRouter

from app.api.v1 import documents

api_router = APIRouter(prefix="/v1")

# Include the documents router
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
