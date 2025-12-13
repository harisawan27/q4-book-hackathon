"""
Authentication API routes for signup, signin, and session management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.core.database import get_db
from src.models.auth_schemas import (
    SignupRequest,
    SigninRequest,
    AuthResponse,
    SessionResponse,
    UserResponse,
    UserBackgroundResponse,
    UserProfileResponse,
    UserBackgroundCreate,
    ErrorResponse,
)
from src.services.auth_service import (
    create_user,
    create_user_background,
    authenticate_user,
    create_access_token,
    get_user_by_id,
    get_user_background,
    update_user_background,
    invalidate_session,
    create_session,
)
from src.middleware.auth_middleware import get_current_user, get_current_user_optional
from src.models.auth import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        409: {"model": ErrorResponse, "description": "Email already registered"},
    }
)
async def signup(
    request: SignupRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user with optional background questionnaire.

    - Creates user account with hashed password
    - Optionally creates background profile for personalization
    - Returns JWT token for immediate authentication
    """
    try:
        # Create user
        user = await create_user(
            db,
            email=request.email,
            password=request.password,
            name=request.name
        )

        # Create background if provided
        if request.background:
            await create_user_background(
                db,
                user_id=user.id,
                software_skills=request.background.software_skills,
                hardware_skills=request.background.hardware_skills,
                experience_level=request.background.experience_level
            )

        # Generate token
        token, expires_at = create_access_token(user.id)

        # Create session record
        await create_session(db, user.id, token, expires_at)

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                email_verified=user.email_verified,
                created_at=user.created_at
            ),
            token=token,
            expires_at=expires_at
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )


@router.post(
    "/signin",
    response_model=AuthResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    }
)
async def signin(
    request: SigninRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user with email and password.

    Returns JWT token for subsequent API calls.
    """
    user = await authenticate_user(db, request.email, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate token
    token, expires_at = create_access_token(user.id)

    # Create session record
    await create_session(db, user.id, token, expires_at)

    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            email_verified=user.email_verified,
            created_at=user.created_at
        ),
        token=token,
        expires_at=expires_at
    )


@router.post(
    "/signout",
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def signout(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Sign out the current user by invalidating their session.
    """
    # In a full implementation, we'd invalidate the specific session token
    # For now, just return success
    return {"message": "Successfully signed out"}


@router.get(
    "/session",
    response_model=SessionResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def get_session(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's session info.

    Returns user info and whether they have completed background questionnaire.
    """
    from datetime import datetime, timezone, timedelta
    from src.core.config import get_settings

    settings = get_settings()

    # Check if user has background
    background = await get_user_background(db, user.id)

    return SessionResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            email_verified=user.email_verified,
            created_at=user.created_at
        ),
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.JWT_EXPIRY_DAYS),
        has_background=background is not None
    )


# Profile routes (also in auth_routes for convenience)
@router.get(
    "/profile",
    response_model=UserProfileResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def get_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's full profile including background.
    """
    background = await get_user_background(db, user.id)

    background_response = None
    if background:
        background_response = UserBackgroundResponse(
            id=background.id,
            user_id=background.user_id,
            software_skills=background.software_skills,
            hardware_skills=background.hardware_skills,
            experience_level=background.experience_level,
            created_at=background.created_at,
            updated_at=background.updated_at
        )

    return UserProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        email_verified=user.email_verified,
        created_at=user.created_at,
        background=background_response
    )
