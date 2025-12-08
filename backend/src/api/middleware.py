from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 50, window: int = 3600):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [t for t in self.requests[client_ip] if now - t < self.window]
        
        if len(self.requests[client_ip]) >= self.limit:
            return Response("Rate limit exceeded", status_code=429)
        
        self.requests[client_ip].append(now)
        response = await call_next(request)
        return response
