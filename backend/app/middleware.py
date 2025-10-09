# This file will hold custom FastAPI middleware.
# For example, you can add a middleware to log every incoming request.

# import time
# from fastapi import Request

# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
