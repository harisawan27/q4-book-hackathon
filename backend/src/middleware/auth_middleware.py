"""
Authentication middleware for FastAPI.
"""
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.services.auth_service import verify_token, get_user_by_id
from src.models.auth import User

# Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get the current user from JWT token if provided.
    Returns None if no token or invalid token.
    """
    if credentials is None:
        return None

    token = credentials.credentials
    user_id = verify_token(token)

    if user_id is None:
        return None

    user = await get_user_by_id(db, user_id)
    return user


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current user from JWT token.
    Raises 401 if not authenticated.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    user_id = verify_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_auth(user: User = Depends(get_current_user)) -> User:
    """
    Dependency injector that requires authentication.
    Use this in route handlers to ensure the user is authenticated.

    Example:
        @router.get("/protected")
        async def protected_route(user: User = Depends(require_auth)):
            return {"user_id": str(user.id)}
    """
    return user


def require_background(user: User = Depends(get_current_user)) -> User:
    """
    Dependency injector that requires authentication AND completed background.
    Use this for personalization endpoints.

    Example:
        @router.post("/personalize")
        async def personalize(user: User = Depends(require_background)):
            return {"background": user.background}
    """
    if user.background is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete your background profile first",
        )
    return user
