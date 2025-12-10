# middleware/custom_middleware.py

from fastapi import Request
from fastapi.responses import Response

async def process_time_middleware(request: Request, call_next):
    print("Request URL:", request.url)
    
    response: Response = await call_next(request)
    response.headers["X-Process-Time"] = "10 sec"
    
    return response
