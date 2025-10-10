from fastapi import APIRouter

from app.api.v1 import documents, chat, users

api_router = APIRouter(prefix="/v1")

# Include the documents router
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(users.router, prefix="/users", tags=["users"]) 