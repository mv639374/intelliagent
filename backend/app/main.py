from fastapi import FastAPI
from app.core.rate_limiter import rate_limit_middleware # <-- IMPORT
from starlette.middleware.base import BaseHTTPMiddleware # <-- IMPORT
from app.api.v1.router import api_router

app = FastAPI(title="IntelliAgent API", version="0.1.0", description="Backend services for the IntelliAgent platform.")

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
