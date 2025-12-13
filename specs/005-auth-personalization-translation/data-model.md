# Data Model: Authentication, Personalization & Translation

**Feature**: 005-auth-personalization-translation
**Date**: 2025-12-13
**Database**: Neon Serverless Postgres

## Entity Relationship Diagram

```
┌─────────────────────┐       1:1       ┌─────────────────────────┐
│       users         │────────────────▶│    user_backgrounds     │
│  (Better-Auth)      │                 │   (expertise profile)   │
├─────────────────────┤                 ├─────────────────────────┤
│ id (PK, UUID)       │                 │ id (PK, UUID)           │
│ email (unique)      │                 │ user_id (FK, unique)    │
│ password_hash       │                 │ software_skills         │
│ email_verified      │                 │ hardware_skills         │
│ name                │                 │ experience_level        │
│ image               │                 │ created_at              │
│ created_at          │                 │ updated_at              │
│ updated_at          │                 └─────────────────────────┘
└─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────┐       ┌─────────────────────────┐
│    auth_sessions    │       │   transformation_logs   │
│  (session tokens)   │       │    (audit trail)        │
├─────────────────────┤       ├─────────────────────────┤
│ id (PK, UUID)       │       │ id (PK, UUID)           │
│ session_token       │       │ user_id (FK)            │
│ user_id (FK)        │       │ chapter_slug            │
│ expires             │       │ transformation_type     │
└─────────────────────┘       │ input_length            │
                              │ output_length           │
                              │ duration_ms             │
                              │ success                 │
                              │ error_message           │
                              │ created_at              │
                              └─────────────────────────┘
```

## Table Definitions

### 1. users (Better-Auth Compatible)

Primary user account table following Better-Auth schema conventions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique user identifier |
| email | VARCHAR(255) | NOT NULL, UNIQUE, INDEX | User email address |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hashed password |
| email_verified | TIMESTAMPTZ | NULL | Verification timestamp |
| name | VARCHAR(255) | NULL | Display name |
| image | TEXT | NULL | Profile image URL |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Last update time |

**Indexes**:
- `users_email_idx` on `email`
- `users_pkey` on `id`

**SQLAlchemy Model**: `backend/src/models/auth.py:User`

### 2. user_backgrounds

User expertise profile for content personalization.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Unique background ID |
| user_id | UUID | FK users(id) ON DELETE CASCADE, UNIQUE | Associated user |
| software_skills | VARCHAR(20) | NOT NULL, CHECK | none/beginner/intermediate/advanced |
| hardware_skills | VARCHAR(20) | NOT NULL, CHECK | none/beginner/intermediate/advanced |
| experience_level | VARCHAR(20) | NOT NULL, CHECK | student/professional/hobbyist/researcher |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Last update time |

**Check Constraints**:
```sql
CHECK (software_skills IN ('none', 'beginner', 'intermediate', 'advanced'))
CHECK (hardware_skills IN ('none', 'beginner', 'intermediate', 'advanced'))
CHECK (experience_level IN ('student', 'professional', 'hobbyist', 'researcher'))
```

**Relationships**:
- One-to-One with `users` (user_id is unique)

**SQLAlchemy Model**: `backend/src/models/auth.py:UserBackground`

### 3. auth_sessions

Session token storage for stateful authentication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Session ID |
| session_token | VARCHAR(255) | NOT NULL, UNIQUE, INDEX | JWT or session token |
| user_id | UUID | FK users(id) ON DELETE CASCADE | Session owner |
| expires | TIMESTAMPTZ | NOT NULL | Token expiration time |

**Indexes**:
- `auth_sessions_token_idx` on `session_token`

**Relationships**:
- Many-to-One with `users`

**SQLAlchemy Model**: `backend/src/models/auth.py:AuthSession`

### 4. transformation_logs

Audit trail for content personalization and translation requests.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT uuid_generate_v4() | Log entry ID |
| user_id | UUID | FK users(id) ON DELETE SET NULL | Requesting user |
| chapter_slug | VARCHAR(255) | NOT NULL, INDEX | Chapter identifier |
| transformation_type | VARCHAR(20) | NOT NULL, CHECK | personalization/translation |
| input_length | INTEGER | NOT NULL | Original content length |
| output_length | INTEGER | NOT NULL | Transformed content length |
| duration_ms | INTEGER | NOT NULL | Processing time |
| success | BOOLEAN | NOT NULL, DEFAULT TRUE | Success status |
| error_message | TEXT | NULL | Error details if failed |
| created_at | TIMESTAMPTZ | DEFAULT NOW(), INDEX | Request timestamp |

**Check Constraints**:
```sql
CHECK (transformation_type IN ('personalization', 'translation'))
```

**Indexes**:
- `transformation_logs_chapter_idx` on `chapter_slug`
- `transformation_logs_created_idx` on `created_at`

**SQLAlchemy Model**: `backend/src/models/auth.py:TransformationLog`

## Enum Values

### software_skills / hardware_skills

| Value | Description |
|-------|-------------|
| none | No prior experience |
| beginner | Basic understanding |
| intermediate | Working knowledge |
| advanced | Expert-level understanding |

### experience_level

| Value | Description |
|-------|-------------|
| student | Learning these concepts |
| professional | Working professional |
| hobbyist | Exploring as hobby |
| researcher | Academic researcher |

### transformation_type

| Value | Description |
|-------|-------------|
| personalization | Content adapted to user background |
| translation | Content translated to target language |

## Migration SQL

```sql
-- Migration: 005_user_personalization.sql

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (Better-Auth compatible)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email_verified TIMESTAMPTZ,
    name VARCHAR(255),
    image TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS users_email_idx ON users(email);

-- User backgrounds for personalization
CREATE TABLE IF NOT EXISTS user_backgrounds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    software_skills VARCHAR(20) NOT NULL DEFAULT 'none'
        CHECK (software_skills IN ('none', 'beginner', 'intermediate', 'advanced')),
    hardware_skills VARCHAR(20) NOT NULL DEFAULT 'none'
        CHECK (hardware_skills IN ('none', 'beginner', 'intermediate', 'advanced')),
    experience_level VARCHAR(20) NOT NULL DEFAULT 'student'
        CHECK (experience_level IN ('student', 'professional', 'hobbyist', 'researcher')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Auth sessions for token management
CREATE TABLE IF NOT EXISTS auth_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_token VARCHAR(255) NOT NULL UNIQUE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS auth_sessions_token_idx ON auth_sessions(session_token);

-- Transformation logs for auditing
CREATE TABLE IF NOT EXISTS transformation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    chapter_slug VARCHAR(255) NOT NULL,
    transformation_type VARCHAR(20) NOT NULL
        CHECK (transformation_type IN ('personalization', 'translation')),
    input_length INTEGER NOT NULL,
    output_length INTEGER NOT NULL,
    duration_ms INTEGER NOT NULL,
    success BOOLEAN NOT NULL DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS transformation_logs_chapter_idx ON transformation_logs(chapter_slug);
CREATE INDEX IF NOT EXISTS transformation_logs_created_idx ON transformation_logs(created_at);

-- Update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_backgrounds_updated_at
    BEFORE UPDATE ON user_backgrounds
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## Pydantic Schemas

```python
# backend/src/models/auth_schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID

# Enums as Literals
SkillLevel = Literal['none', 'beginner', 'intermediate', 'advanced']
ExperienceLevel = Literal['student', 'professional', 'hobbyist', 'researcher']
TransformationType = Literal['personalization', 'translation']

# Request schemas
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str  # min 8 chars validated in route
    name: Optional[str] = None
    background: Optional['BackgroundCreate'] = None

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class BackgroundCreate(BaseModel):
    software_skills: SkillLevel = 'none'
    hardware_skills: SkillLevel = 'none'
    experience_level: ExperienceLevel = 'student'

class BackgroundUpdate(BaseModel):
    software_skills: Optional[SkillLevel] = None
    hardware_skills: Optional[SkillLevel] = None
    experience_level: Optional[ExperienceLevel] = None

class PersonalizeRequest(BaseModel):
    chapter_slug: str
    content: str

class TranslateRequest(BaseModel):
    chapter_slug: str
    content: str
    target_language: str = 'Urdu'

# Response schemas
class UserResponse(BaseModel):
    id: UUID
    email: str
    name: Optional[str]
    email_verified: Optional[datetime]
    created_at: datetime

class AuthResponse(BaseModel):
    user: UserResponse
    token: str
    expires_at: datetime

class SessionResponse(BaseModel):
    user: UserResponse
    expires_at: datetime
    has_background: bool

class BackgroundResponse(BaseModel):
    id: UUID
    user_id: UUID
    software_skills: SkillLevel
    hardware_skills: SkillLevel
    experience_level: ExperienceLevel
    created_at: datetime
    updated_at: datetime

class TransformationResponse(BaseModel):
    content: str
    original_length: int
    transformed_length: int
    duration_ms: int
    transformation_type: TransformationType

class TransformationLogResponse(BaseModel):
    id: UUID
    chapter_slug: str
    transformation_type: TransformationType
    input_length: int
    output_length: int
    duration_ms: int
    success: bool
    error_message: Optional[str]
    created_at: datetime

class TransformationLogsResponse(BaseModel):
    logs: list[TransformationLogResponse]
    total: int
    limit: int
    offset: int
```

## Data Flow

### User Registration Flow

```
1. Client sends POST /auth/signup
2. Backend validates email uniqueness
3. Password hashed with bcrypt
4. User record created in users table
5. If background provided, record created in user_backgrounds
6. JWT token generated and stored in auth_sessions
7. Response includes token and user info
```

### Content Transformation Flow

```
1. Client sends POST /content/personalize or /content/translate
2. Backend validates JWT token
3. Rate limit checked (10/hour/user)
4. User background fetched for personalization
5. Content sent to Gemini API with appropriate prompt
6. Transformed content returned
7. Log entry created in transformation_logs
```

## Existing Tables (RAG Chatbot)

The following tables exist from the RAG chatbot feature and are unchanged:

- `sessions` - Chat session tracking
- `messages` - Conversation history
- `feedback` - User feedback on responses

These tables use the same UUID and timestamp patterns for consistency.

---

**Model Status**: COMPLETE
**Next Step**: Create API contracts
