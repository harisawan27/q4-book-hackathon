"""
Pydantic schemas for authentication, personalization, and translation API.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID


# === Authentication Schemas ===

class SignupRequest(BaseModel):
    """Schema for user signup request"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: Optional[str] = None
    background: Optional["UserBackgroundCreate"] = None


class SigninRequest(BaseModel):
    """Schema for user signin request"""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    user: "UserResponse"
    token: str
    expires_at: datetime


class SessionResponse(BaseModel):
    """Schema for session info response"""
    user: "UserResponse"
    expires_at: datetime
    has_background: bool


# === User Schemas ===

class UserResponse(BaseModel):
    """Schema for returning user info"""
    id: UUID
    email: EmailStr
    name: Optional[str] = None
    email_verified: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    """Schema for full user profile including background"""
    id: UUID
    email: EmailStr
    name: Optional[str] = None
    email_verified: Optional[datetime] = None
    created_at: datetime
    background: Optional["UserBackgroundResponse"] = None

    class Config:
        from_attributes = True


# === Background Schemas ===

class UserBackgroundCreate(BaseModel):
    """Schema for creating/updating user background"""
    software_skills: Literal["none", "beginner", "intermediate", "advanced"] = "none"
    hardware_skills: Literal["none", "beginner", "intermediate", "advanced"] = "none"
    experience_level: Literal["student", "professional", "hobbyist", "researcher"] = "student"


class UserBackgroundResponse(BaseModel):
    """Schema for returning user background"""
    id: UUID
    user_id: UUID
    software_skills: str
    hardware_skills: str
    experience_level: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# === Transformation Schemas ===

class PersonalizeRequest(BaseModel):
    """Schema for content personalization request"""
    chapter_slug: str = Field(..., description="URL slug of the chapter")
    content: str = Field(..., max_length=100000, description="Chapter content to personalize")


class TranslateRequest(BaseModel):
    """Schema for content translation request"""
    chapter_slug: str = Field(..., description="URL slug of the chapter")
    content: str = Field(..., max_length=100000, description="Chapter content to translate")


class TransformationResponse(BaseModel):
    """Schema for transformation result"""
    content: str
    original_length: int
    transformed_length: int
    duration_ms: int
    transformation_type: Literal["personalization", "translation"]


class TransformationLogResponse(BaseModel):
    """Schema for transformation log entry"""
    id: UUID
    chapter_slug: str
    transformation_type: str
    input_length: int
    output_length: int
    duration_ms: int
    success: bool
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TransformationLogsResponse(BaseModel):
    """Schema for paginated transformation logs"""
    logs: list[TransformationLogResponse]
    total: int
    limit: int
    offset: int


# === Error Schemas ===

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    message: str
    details: Optional[dict] = None


# Update forward references
SignupRequest.model_rebuild()
AuthResponse.model_rebuild()
SessionResponse.model_rebuild()
UserProfileResponse.model_rebuild()
