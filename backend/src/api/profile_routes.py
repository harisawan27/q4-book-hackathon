"""
Profile API routes for background management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.models.auth_schemas import (
    UserBackgroundCreate,
    UserBackgroundResponse,
    UserProfileResponse,
    ErrorResponse,
)
from src.services.auth_service import (
    get_user_background,
    update_user_background,
)
from src.middleware.auth_middleware import get_current_user
from src.models.auth import User

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get(
    "/background",
    response_model=UserBackgroundResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        404: {"model": ErrorResponse, "description": "Background not found"},
    }
)
async def get_background(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's background questionnaire data.
    """
    background = await get_user_background(db, user.id)

    if not background:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Background questionnaire not completed. Please update your profile."
        )

    return UserBackgroundResponse(
        id=background.id,
        user_id=background.user_id,
        software_skills=background.software_skills,
        hardware_skills=background.hardware_skills,
        experience_level=background.experience_level,
        created_at=background.created_at,
        updated_at=background.updated_at
    )


@router.put(
    "/background",
    response_model=UserBackgroundResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
    }
)
async def update_background_endpoint(
    request: UserBackgroundCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create or update the user's background questionnaire data.

    This data is used for content personalization.
    """
    background = await update_user_background(
        db,
        user_id=user.id,
        software_skills=request.software_skills,
        hardware_skills=request.hardware_skills,
        experience_level=request.experience_level
    )

    return UserBackgroundResponse(
        id=background.id,
        user_id=background.user_id,
        software_skills=background.software_skills,
        hardware_skills=background.hardware_skills,
        experience_level=background.experience_level,
        created_at=background.created_at,
        updated_at=background.updated_at
    )


@router.get(
    "",
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
