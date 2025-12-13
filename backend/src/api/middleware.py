from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from typing import Optional

from src.core.config import get_settings

settings = get_settings()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware based on IP address."""

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


class TransformationRateLimiter:
    """
    User-based rate limiter for personalization and translation requests.
    Limits requests per user per time window.
    """

    def __init__(
        self,
        limit: Optional[int] = None,
        window: Optional[int] = None
    ):
        self.limit = limit or settings.TRANSFORM_RATE_LIMIT
        self.window = window or settings.TRANSFORM_RATE_WINDOW
        # user_id -> list of timestamps
        self.user_requests: dict[str, list[float]] = defaultdict(list)

    def check_rate_limit(self, user_id: str) -> tuple[bool, int]:
        """
        Check if a user has exceeded the rate limit.

        Args:
            user_id: The user's UUID as string

        Returns:
            tuple: (is_allowed, remaining_requests)
        """
        now = time.time()

        # Clean old requests for this user
        self.user_requests[user_id] = [
            t for t in self.user_requests[user_id]
            if now - t < self.window
        ]

        current_count = len(self.user_requests[user_id])
        remaining = self.limit - current_count

        if current_count >= self.limit:
            return False, 0

        return True, remaining

    def record_request(self, user_id: str) -> None:
        """Record a request for a user."""
        self.user_requests[user_id].append(time.time())

    def get_remaining(self, user_id: str) -> int:
        """Get remaining requests for a user."""
        now = time.time()
        self.user_requests[user_id] = [
            t for t in self.user_requests[user_id]
            if now - t < self.window
        ]
        return max(0, self.limit - len(self.user_requests[user_id]))

    def get_reset_time(self, user_id: str) -> Optional[float]:
        """Get seconds until rate limit resets for a user."""
        if not self.user_requests[user_id]:
            return None
        oldest = min(self.user_requests[user_id])
        return max(0, self.window - (time.time() - oldest))


# Global transformation rate limiter instance
transformation_rate_limiter = TransformationRateLimiter()
