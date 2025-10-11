from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.rate_limiter import rate_limit_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.v1.router import api_router

app = FastAPI(
    title="IntelliAgent API",
    version="0.1.0",
    description="Backend services for the IntelliAgent platform."
)

# CORS Configuration for frontend at localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers including Authorization
)

app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

# Include the main API router
app.include_router(api_router, prefix="/api")

@app.get("/api/health", tags=["Health Check"])
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}

@app.get("/")
async def home():
    return {"status": "chal raha hai"}
