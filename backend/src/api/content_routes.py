"""
Content transformation API routes for personalization and translation.
"""
import time
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.core.database import get_db
from src.core.config import get_settings
from src.core.logging import logger
from src.models.auth_schemas import (
    PersonalizeRequest,
    TranslateRequest,
    TransformationResponse,
    TransformationLogResponse,
    TransformationLogsResponse,
    ErrorResponse,
)
from src.models.auth import User, UserBackground, TransformationLog
from src.middleware.auth_middleware import get_current_user
from src.services.auth_service import get_user_background
from src.services.content_service import personalize_content, translate_content

settings = get_settings()

router = APIRouter(prefix="/content", tags=["Content Transformation"])


async def check_rate_limit(db: AsyncSession, user_id: uuid.UUID) -> tuple[bool, int]:
    """
    Check if user has exceeded transformation rate limit.

    Returns:
        tuple: (is_allowed, remaining_requests)
    """
    window_start = datetime.now(timezone.utc) - timedelta(seconds=settings.TRANSFORM_RATE_WINDOW)

    result = await db.execute(
        select(func.count(TransformationLog.id))
        .where(TransformationLog.user_id == user_id)
        .where(TransformationLog.created_at >= window_start)
    )
    count = result.scalar() or 0

    remaining = max(0, settings.TRANSFORM_RATE_LIMIT - count)
    is_allowed = count < settings.TRANSFORM_RATE_LIMIT

    return is_allowed, remaining


async def log_transformation(
    db: AsyncSession,
    user_id: uuid.UUID,
    chapter_slug: str,
    transformation_type: str,
    input_length: int,
    output_length: int,
    duration_ms: int,
    success: bool = True,
    error_message: Optional[str] = None
) -> TransformationLog:
    """Log a transformation request for auditing and rate limiting."""
    log = TransformationLog(
        id=uuid.uuid4(),
        user_id=user_id,
        chapter_slug=chapter_slug,
        transformation_type=transformation_type,
        input_length=input_length,
        output_length=output_length,
        duration_ms=duration_ms,
        success=success,
        error_message=error_message
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.post(
    "/personalize",
    response_model=TransformationResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        400: {"model": ErrorResponse, "description": "Background not configured"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
    }
)
async def personalize_chapter(
    request: PersonalizeRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Personalize chapter content based on user's background.

    - Requires user to have completed background questionnaire
    - Subject to rate limiting (10 requests/hour)
    - Preserves all technical accuracy and formatting
    """
    # Check rate limit
    is_allowed, remaining = await check_rate_limit(db, user.id)
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {settings.TRANSFORM_RATE_WINDOW // 60} minutes.",
            headers={"X-RateLimit-Remaining": "0"}
        )

    # Get user background
    background = await get_user_background(db, user.id)
    if not background:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete your background questionnaire before personalizing content."
        )

    start_time = time.time()

    try:
        # Personalize content
        personalized_content = await personalize_content(
            content=request.content,
            chapter_title=request.chapter_slug.replace("-", " ").title(),
            background=background
        )

        duration_ms = int((time.time() - start_time) * 1000)

        # Log transformation
        await log_transformation(
            db=db,
            user_id=user.id,
            chapter_slug=request.chapter_slug,
            transformation_type="personalization",
            input_length=len(request.content),
            output_length=len(personalized_content),
            duration_ms=duration_ms,
            success=True
        )

        return TransformationResponse(
            content=personalized_content,
            original_length=len(request.content),
            transformed_length=len(personalized_content),
            duration_ms=duration_ms,
            transformation_type="personalization"
        )

    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)

        # Log failed transformation
        await log_transformation(
            db=db,
            user_id=user.id,
            chapter_slug=request.chapter_slug,
            transformation_type="personalization",
            input_length=len(request.content),
            output_length=0,
            duration_ms=duration_ms,
            success=False,
            error_message=str(e)
        )

        logger.error(f"Personalization failed for user {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to personalize content: {str(e)}"
        )


@router.post(
    "/translate",
    response_model=TransformationResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
    }
)
async def translate_chapter(
    request: TranslateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Translate chapter content to Urdu.

    - Subject to rate limiting (10 requests/hour)
    - Preserves technical terms in English
    - Preserves code blocks and equations
    """
    # Check rate limit
    is_allowed, remaining = await check_rate_limit(db, user.id)
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {settings.TRANSFORM_RATE_WINDOW // 60} minutes.",
            headers={"X-RateLimit-Remaining": "0"}
        )

    start_time = time.time()

    try:
        # Translate content
        translated_content = await translate_content(
            content=request.content,
            chapter_title=request.chapter_slug.replace("-", " ").title()
        )

        duration_ms = int((time.time() - start_time) * 1000)

        # Log transformation
        await log_transformation(
            db=db,
            user_id=user.id,
            chapter_slug=request.chapter_slug,
            transformation_type="translation",
            input_length=len(request.content),
            output_length=len(translated_content),
            duration_ms=duration_ms,
            success=True
        )

        return TransformationResponse(
            content=translated_content,
            original_length=len(request.content),
            transformed_length=len(translated_content),
            duration_ms=duration_ms,
            transformation_type="translation"
        )

    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)

        # Log failed transformation
        await log_transformation(
            db=db,
            user_id=user.id,
            chapter_slug=request.chapter_slug,
            transformation_type="translation",
            input_length=len(request.content),
            output_length=0,
            duration_ms=duration_ms,
            success=False,
            error_message=str(e)
        )

        logger.error(f"Translation failed for user {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to translate content: {str(e)}"
        )


@router.get(
    "/logs",
    response_model=TransformationLogsResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def get_transformation_logs(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    type: Optional[str] = Query(default=None, description="Filter by transformation type: personalization or translation")
):
    """
    Get user's transformation history.

    - Paginated results
    - Optionally filter by transformation type
    """
    # Build query
    query = select(TransformationLog).where(TransformationLog.user_id == user.id)
    count_query = select(func.count(TransformationLog.id)).where(TransformationLog.user_id == user.id)

    if type and type in ["personalization", "translation"]:
        query = query.where(TransformationLog.transformation_type == type)
        count_query = count_query.where(TransformationLog.transformation_type == type)

    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Get paginated results
    query = query.order_by(TransformationLog.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    logs = result.scalars().all()

    return TransformationLogsResponse(
        logs=[
            TransformationLogResponse(
                id=log.id,
                chapter_slug=log.chapter_slug,
                transformation_type=log.transformation_type,
                input_length=log.input_length,
                output_length=log.output_length,
                duration_ms=log.duration_ms,
                success=log.success,
                error_message=log.error_message,
                created_at=log.created_at
            )
            for log in logs
        ],
        total=total,
        limit=limit,
        offset=offset
    )


@router.get(
    "/rate-limit",
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    }
)
async def get_rate_limit_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current rate limit status for the user.
    """
    is_allowed, remaining = await check_rate_limit(db, user.id)

    return {
        "limit": settings.TRANSFORM_RATE_LIMIT,
        "remaining": remaining,
        "window_seconds": settings.TRANSFORM_RATE_WINDOW,
        "is_allowed": is_allowed
    }
