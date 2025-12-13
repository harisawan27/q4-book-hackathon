# Quickstart Guide: Authentication, Personalization & Translation

**Feature**: 005-auth-personalization-translation
**Date**: 2025-12-13

## Prerequisites

- Python 3.11+
- Node.js 18+
- pnpm (or npm/yarn)
- PostgreSQL (Neon Serverless)
- Qdrant Cloud account (existing)
- Gemini API key

## Environment Setup

### 1. Backend Environment

Create `backend/.env`:

```env
# Database
NEON_DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname

# Vector Store (existing)
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
QDRANT_COLLECTION_NAME=giaic-q4-hackathon

# LLM (existing)
GEMINI_API_KEY=your-gemini-key

# Authentication
BETTER_AUTH_SECRET=your-random-secret-key-min-32-chars

# Optional
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7
TRANSFORM_RATE_LIMIT=10
TRANSFORM_RATE_WINDOW=3600
```

Generate a secure secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Frontend Environment

Create `website/.env`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Installation

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations (if not already applied)
# Connect to Neon console and run:
# backend/migrations/005_user_personalization.sql
```

### Frontend

```bash
cd website

# Install dependencies
pnpm install
```

## Running the Application

### Start Backend

```bash
cd backend
source venv/bin/activate

# Development mode
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000

### Start Frontend

```bash
cd website

# Development mode
pnpm start
```

Website will be available at: http://localhost:3000

## Testing the Features

### 1. User Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepass123",
    "name": "Test User",
    "background": {
      "software_skills": "intermediate",
      "hardware_skills": "beginner",
      "experience_level": "student"
    }
  }'
```

### 2. User Sign In

```bash
curl -X POST http://localhost:8000/api/v1/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepass123"
  }'
```

Save the returned `token` for authenticated requests.

### 3. Get Session

```bash
curl http://localhost:8000/api/v1/auth/session \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Personalize Content

```bash
curl -X POST http://localhost:8000/api/v1/content/personalize \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "chapter_slug": "intro",
    "content": "# Introduction\n\nROS 2 is a framework for robotics..."
  }'
```

### 5. Translate Content

```bash
curl -X POST http://localhost:8000/api/v1/content/translate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "chapter_slug": "intro",
    "content": "# Introduction\n\nROS 2 is a framework for robotics..."
  }'
```

## Frontend UI Flow

1. **Sign Up**: Navigate to `/signup`
   - Enter email, password, name
   - Complete background questionnaire
   - Automatically signed in after registration

2. **Sign In**: Navigate to `/signin`
   - Enter email and password
   - Redirected to homepage on success

3. **View Profile**: Navigate to `/profile`
   - See user info and background
   - Update background preferences

4. **Personalize/Translate**: Visit any doc page
   - Click "Personalize Content" for adapted content
   - Click "Translate to Urdu" for Urdu version
   - Click "Reset to Original" to restore

## Database Schema

Run the migration in Neon console:

```sql
-- See backend/migrations/005_user_personalization.sql
```

Tables created:
- `users` - User accounts
- `user_backgrounds` - Expertise profiles
- `auth_sessions` - Session tokens
- `transformation_logs` - Audit trail

## Troubleshooting

### CORS Errors

Ensure backend CORS settings allow frontend origin:

```python
# backend/src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### JWT Token Errors

- Check `BETTER_AUTH_SECRET` is set and at least 32 characters
- Ensure token is passed in `Authorization: Bearer <token>` header
- Check token expiration (default 7 days)

### Rate Limit Errors

- Default: 10 transformations per user per hour
- Wait for rate limit window to reset
- Check `TRANSFORM_RATE_LIMIT` and `TRANSFORM_RATE_WINDOW` env vars

### Translation Quality

- Ensure Gemini API key is valid and has quota
- Check content_service.py prompts for glossary terms
- Test with shorter content first

## API Endpoints Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/signup | No | Register new user |
| POST | /auth/signin | No | Sign in |
| POST | /auth/signout | Yes | Sign out |
| GET | /auth/session | Yes | Get session info |
| GET | /profile | Yes | Get user profile |
| GET | /profile/background | Yes | Get background |
| PUT | /profile/background | Yes | Update background |
| POST | /content/personalize | Yes* | Personalize content |
| POST | /content/translate | Yes | Translate content |
| GET | /content/logs | Yes | Get transformation logs |

*Requires completed background questionnaire

## Next Steps

1. Verify migrations are applied
2. Test all API endpoints with curl
3. Test frontend signup/signin flow
4. Test personalization with a real chapter
5. Test translation and RTL display
6. Verify RAG chatbot still works

---

**Status**: Ready for development
**See**: [plan.md](./plan.md) for full implementation plan
