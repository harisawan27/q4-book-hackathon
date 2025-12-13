"""
Authentication service for JWT token management and user operations.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID
import uuid

from jose import JWTError, jwt
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core.config import get_settings
from src.models.auth import User, UserBackground, AuthSession

settings = get_settings()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(user_id: UUID, expires_delta: Optional[timedelta] = None) -> tuple[str, datetime]:
    """
    Create a JWT access token for a user.

    Returns:
        tuple: (token, expires_at)
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_EXPIRY_DAYS)

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt, expire


def verify_token(token: str) -> Optional[UUID]:
    """
    Verify a JWT token and extract the user ID.

    Returns:
        UUID: User ID if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return UUID(user_id)
    except JWTError:
        return None


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get a user by email address."""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
    """Get a user by ID with background loaded."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.background))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    email: str,
    password: str,
    name: Optional[str] = None
) -> User:
    """
    Create a new user with hashed password.

    Returns:
        User: The created user object
    """
    user = User(
        id=uuid.uuid4(),
        email=email,
        password_hash=hash_password(password),
        name=name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_user_background(
    db: AsyncSession,
    user_id: UUID,
    software_skills: str = "none",
    hardware_skills: str = "none",
    experience_level: str = "student"
) -> UserBackground:
    """
    Create background profile for a user.

    Returns:
        UserBackground: The created background object
    """
    background = UserBackground(
        id=uuid.uuid4(),
        user_id=user_id,
        software_skills=software_skills,
        hardware_skills=hardware_skills,
        experience_level=experience_level
    )
    db.add(background)
    await db.commit()
    await db.refresh(background)
    return background


async def update_user_background(
    db: AsyncSession,
    user_id: UUID,
    software_skills: Optional[str] = None,
    hardware_skills: Optional[str] = None,
    experience_level: Optional[str] = None
) -> Optional[UserBackground]:
    """
    Update or create user background.

    Returns:
        UserBackground: The updated/created background object
    """
    # Check if background exists
    result = await db.execute(
        select(UserBackground).where(UserBackground.user_id == user_id)
    )
    background = result.scalar_one_or_none()

    if background:
        # Update existing
        if software_skills is not None:
            background.software_skills = software_skills
        if hardware_skills is not None:
            background.hardware_skills = hardware_skills
        if experience_level is not None:
            background.experience_level = experience_level
        await db.commit()
        await db.refresh(background)
        return background
    else:
        # Create new
        return await create_user_background(
            db,
            user_id,
            software_skills or "none",
            hardware_skills or "none",
            experience_level or "student"
        )


async def get_user_background(db: AsyncSession, user_id: UUID) -> Optional[UserBackground]:
    """Get user background by user ID."""
    result = await db.execute(
        select(UserBackground).where(UserBackground.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Returns:
        User: The authenticated user if credentials are valid, None otherwise
    """
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def create_session(db: AsyncSession, user_id: UUID, token: str, expires: datetime) -> AuthSession:
    """Create a new auth session record."""
    session = AuthSession(
        id=uuid.uuid4(),
        session_token=token,
        user_id=user_id,
        expires=expires
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def invalidate_session(db: AsyncSession, token: str) -> bool:
    """Invalidate a session by deleting it."""
    result = await db.execute(
        select(AuthSession).where(AuthSession.session_token == token)
    )
    session = result.scalar_one_or_none()
    if session:
        await db.delete(session)
        await db.commit()
        return True
    return False
