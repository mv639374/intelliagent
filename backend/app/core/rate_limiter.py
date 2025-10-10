import time
from fastapi import Request, HTTPException, status
from redis import Redis
from app.settings import settings

redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware for rate limiting based on client IP address.
    """
    # Allow health checks to bypass rate limiting
    if request.url.path == "/api/health":
        return await call_next(request)

    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    # Use a pipeline for atomic operations
    pipeline = redis_client.pipeline()
    pipeline.incr(key)
    pipeline.expire(key, 60) # 60 seconds window
    request_count, _ = pipeline.execute()

    if request_count > 100: # 10 requests per minute
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
        )
        
    response = await call_next(request)
    return response