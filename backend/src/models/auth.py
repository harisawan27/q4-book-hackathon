"""
Authentication models for User Authentication, Personalization, and Translation feature.
"""
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .db import Base


class User(Base):
    """User table for authentication"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(DateTime(timezone=True), nullable=True)
    name = Column(String(255), nullable=True)
    image = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    background = relationship("UserBackground", back_populates="user", uselist=False)
    transformation_logs = relationship("TransformationLog", back_populates="user")


class UserBackground(Base):
    """User expertise profile for personalization"""
    __tablename__ = "user_backgrounds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    software_skills = Column(
        String(20),
        nullable=False,
        default="none"
    )
    hardware_skills = Column(
        String(20),
        nullable=False,
        default="none"
    )
    experience_level = Column(
        String(20),
        nullable=False,
        default="student"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="background")

    __table_args__ = (
        CheckConstraint("software_skills IN ('none', 'beginner', 'intermediate', 'advanced')"),
        CheckConstraint("hardware_skills IN ('none', 'beginner', 'intermediate', 'advanced')"),
        CheckConstraint("experience_level IN ('student', 'professional', 'hobbyist', 'researcher')"),
    )


class TransformationLog(Base):
    """Audit log for personalization and translation requests"""
    __tablename__ = "transformation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False)

    chapter_slug = Column(String(255), nullable=False, index=True)
    transformation_type = Column(String(20), nullable=False)

    input_length = Column(Integer, nullable=False)
    output_length = Column(Integer, nullable=False)
    duration_ms = Column(Integer, nullable=False)

    success = Column(Boolean, nullable=False, default=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="transformation_logs")

    __table_args__ = (
        CheckConstraint("transformation_type IN ('personalization', 'translation')"),
    )


class AuthSession(Base):
    """Session table for Better-Auth compatibility"""
    __tablename__ = "auth_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires = Column(DateTime(timezone=True), nullable=False)
