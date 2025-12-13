# Implementation Plan: User Authentication, Personalization & Urdu Translation

**Branch**: `005-auth-personalization-translation` | **Date**: 2025-12-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-auth-personalization-translation/spec.md`

## Summary

Implement user authentication with Better-Auth patterns, background questionnaire during signup, personalized chapter content based on user expertise, and Urdu translation for logged-in users. The system extends the existing Docusaurus + FastAPI + Neon Postgres architecture with new auth routes, content transformation endpoints, and React components for chapter-level controls.

**Key Insight**: Much of the infrastructure already exists in the codebase. This plan focuses on completing, testing, and integrating the existing partial implementation.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLAlchemy (async), python-jose, passlib, React 18, Docusaurus 3.x
**Storage**: Neon Serverless Postgres (via SQLAlchemy asyncpg), Qdrant Cloud (existing RAG vectors)
**Testing**: pytest (backend), manual E2E testing (frontend)
**Target Platform**: Linux server (backend), Web browsers (frontend via GitHub Pages/Vercel)
**Project Type**: Web application (backend API + frontend SPA)
**Performance Goals**: <2s auth operations, <15s content transformations, 50 concurrent users
**Constraints**: Rate limit 10 transformations/user/hour, no client-side LLM calls
**Scale/Scope**: ~100 users initially, 20+ book chapters, single backend instance

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | PASS | spec.md complete with 34 FRs, 21 NFRs |
| II. Privacy-First Data Handling | PASS | PII stored in secure DB, not exposed in logs |
| III. Accuracy | PASS | LLM prompts enforce factual integrity, no hallucinations |
| IV. Transparency | PASS | Button states indicate transformation status |
| V. Reproducibility | PASS | Deterministic rules documented, reversible |
| VI. Security | PASS | bcrypt hashing, JWT tokens, rate limiting |
| VII. Consistency | PASS | Docusaurus styling, MDX structure preserved |
| VIII. Authentication & Authorization | PASS | Better-Auth patterns implemented via JWT |
| IX. Knowledge Capture (PHR) | PASS | PHRs created for planning sessions |

**Gate Status**: PASS - No violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/005-auth-personalization-translation/
├── plan.md              # This file
├── spec.md              # Feature specification (complete)
├── research.md          # Phase 0 research findings
├── data-model.md        # Phase 1 data model
├── quickstart.md        # Phase 1 setup guide
├── contracts/           # Phase 1 API contracts
│   ├── auth.yaml        # OpenAPI for auth endpoints
│   ├── profile.yaml     # OpenAPI for profile endpoints
│   └── content.yaml     # OpenAPI for content endpoints
├── checklists/
│   └── requirements.md  # Spec quality checklist (complete)
└── tasks.md             # Phase 2 task list (via /sp.tasks)
```

### Source Code (existing repository structure)

```text
backend/
├── src/
│   ├── main.py                      # FastAPI app with all routers
│   ├── core/
│   │   ├── config.py                # Settings with auth config
│   │   ├── database.py              # Async SQLAlchemy engine
│   │   └── logging.py               # Logging setup
│   ├── models/
│   │   ├── db.py                    # Base model + RAG tables
│   │   ├── auth.py                  # User, UserBackground, TransformationLog, AuthSession
│   │   └── auth_schemas.py          # Pydantic request/response schemas
│   ├── api/
│   │   ├── routes.py                # RAG chatbot endpoints
│   │   ├── auth_routes.py           # /auth/* endpoints
│   │   ├── profile_routes.py        # /profile/* endpoints
│   │   ├── content_routes.py        # /content/* endpoints
│   │   └── middleware.py            # Rate limiting
│   ├── middleware/
│   │   └── auth_middleware.py       # JWT verification, get_current_user
│   └── services/
│       ├── auth_service.py          # JWT, password, user CRUD
│       ├── content_service.py       # Personalization & translation LLM
│       ├── chat.py                  # RAG chatbot
│       └── ...                      # Other existing services
├── migrations/
│   └── 005_user_personalization.sql # Schema migration
├── requirements.txt                 # Python dependencies
└── tests/                           # Test files (to be added)

website/
├── docusaurus.config.ts             # Docusaurus config
├── src/
│   ├── lib/
│   │   └── auth.ts                  # Auth API client
│   ├── pages/
│   │   ├── signin.tsx               # Sign-in page
│   │   ├── signup.tsx               # Sign-up page
│   │   └── profile.tsx              # Profile page
│   ├── theme/
│   │   ├── Root.tsx                 # AuthProvider wrapper
│   │   └── DocItem/index.tsx        # Custom doc layout
│   └── components/
│       ├── AuthProvider/            # React auth context
│       ├── SignIn/                  # Sign-in form
│       ├── SignUp/                  # Sign-up form
│       ├── BackgroundForm/          # Background questionnaire
│       ├── NavbarAuth/              # Navbar auth controls
│       ├── ChapterControls/         # Personalize/Translate buttons
│       └── ChatWidget/              # Existing RAG chatbot
└── docs/                            # Book chapters (MDX)
```

**Structure Decision**: Web application structure with separate backend/ and website/ directories. This matches the existing repository layout.

## Architecture Sketch

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DOCUSAURUS WEBSITE                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────────────┐ │
│  │  AuthProvider│  │ NavbarAuth  │  │         Chapter Page (MDX)          │ │
│  │   (Context)  │  │ (Sign In/Out)│  │  ┌─────────────────────────────┐   │ │
│  └──────┬───────┘  └──────┬──────┘  │  │      ChapterControls        │   │ │
│         │                 │         │  │  [Personalize] [Translate]  │   │ │
│         └────────┬────────┘         │  └─────────────┬───────────────┘   │ │
│                  │                  │                │                    │ │
│                  ▼                  │                ▼                    │ │
│         ┌────────────────┐          │  ┌──────────────────────────────┐  │ │
│         │   lib/auth.ts  │◄─────────┼──│  Content Display (RTL aware) │  │ │
│         │  (API Client)  │          │  │  - Original / Personalized   │  │ │
│         └───────┬────────┘          │  │  - English / Urdu            │  │ │
│                 │                   │  └──────────────────────────────┘  │ │
└─────────────────┼───────────────────┴────────────────────────────────────┘
                  │ HTTP (Bearer Token)
                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI BACKEND                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        Middleware Stack                                 │ │
│  │  CORS → RateLimitMiddleware → Auth Middleware (JWT verification)       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐│
│  │ /auth/*      │  │ /profile/*   │  │ /content/*   │  │ /chat (existing) ││
│  │ - signup     │  │ - background │  │ - personalize│  │ - RAG chatbot    ││
│  │ - signin     │  │ - get/update │  │ - translate  │  │                  ││
│  │ - signout    │  │              │  │ - logs       │  │                  ││
│  │ - session    │  │              │  │              │  │                  ││
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────────────────┘│
│         │                 │                 │                               │
│         ▼                 ▼                 ▼                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         Service Layer                                   │ │
│  │  auth_service.py  │  content_service.py                                │ │
│  │  - hash_password  │  - personalize_content (Gemini LLM)                │ │
│  │  - create_token   │  - translate_content (Gemini LLM)                  │ │
│  │  - verify_token   │                                                    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
└────────────────────────────────────┼─────────────────────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
┌──────────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│   NEON POSTGRES      │  │   QDRANT CLOUD   │  │   GEMINI API         │
│                      │  │   (existing)      │  │                      │
│ Tables:              │  │                  │  │ Models:              │
│ - users              │  │ Collection:      │  │ - gemini-2.5-flash   │
│ - user_backgrounds   │  │ - giaic-q4-      │  │   (personalization)  │
│ - auth_sessions      │  │   hackathon      │  │ - gemini-2.5-flash   │
│ - transformation_logs│  │                  │  │   (translation)      │
│ - (existing RAG)     │  │                  │  │                      │
└──────────────────────┘  └──────────────────┘  └──────────────────────┘
```

### Interaction Flow

```
1. USER AUTHENTICATION FLOW:
   User → /signup page → BackgroundForm → POST /auth/signup
   → auth_service.create_user() → JWT token → localStorage
   → AuthProvider.setUser() → NavbarAuth shows user name

2. CONTENT PERSONALIZATION FLOW:
   User clicks "Personalize Content" on chapter
   → ChapterControls extracts chapter content
   → POST /content/personalize (with Bearer token)
   → auth_middleware validates JWT
   → content_routes fetches user background
   → content_service.personalize_content() → Gemini LLM
   → Return personalized markdown
   → ChapterControls replaces content display
   → TransformationLog saved to DB

3. URDU TRANSLATION FLOW:
   User clicks "Translate to Urdu" on chapter
   → ChapterControls extracts chapter content
   → POST /content/translate (with Bearer token)
   → auth_middleware validates JWT
   → content_service.translate_content() → Gemini LLM
   → Return Urdu markdown with RTL
   → ChapterControls replaces content with dir="rtl"
   → TransformationLog saved to DB

4. RESET FLOW:
   User clicks "Reset to Original"
   → ChapterControls restores cached original content
   → No API call needed
```

## Development Phases

### Phase 1: Authentication Foundation (Existing - Verify & Test)

**Status**: Partially implemented, needs verification

**Tasks**:
1. Verify database migrations are applied (users, auth_sessions tables)
2. Test auth_service.py functions (create_user, verify_password, create_token)
3. Test auth_routes.py endpoints (signup, signin, signout, session)
4. Test auth_middleware.py (get_current_user dependency)
5. Verify frontend AuthProvider context
6. Test SignIn/SignUp components

**Acceptance Criteria**:
- [ ] User can sign up with email/password/name
- [ ] User can sign in with valid credentials
- [ ] Invalid credentials return 401
- [ ] Session token works across page refreshes
- [ ] Sign out invalidates session

### Phase 2: Background Questionnaire (Existing - Complete & Test)

**Status**: Partially implemented, needs UI completion

**Tasks**:
1. Verify UserBackground model constraints
2. Complete BackgroundForm component with all fields:
   - software_experience (dropdown)
   - hardware_experience (dropdown)
   - domain_focus (dropdown)
   - skills (multi-select or tags)
3. Wire form to /profile/background PUT endpoint
4. Add background step to signup flow
5. Update profile page to show/edit background

**Acceptance Criteria**:
- [ ] Signup includes background questionnaire step
- [ ] Background data persists to database
- [ ] Profile page displays background
- [ ] Background can be updated after signup

### Phase 3: Personalization Engine (Existing - Enhance & Test)

**Status**: Implemented, needs testing and refinement

**Tasks**:
1. Review content_service.personalize_content() prompts
2. Add domain_focus to personalization logic
3. Test with sample chapters at different experience levels
4. Verify MDX formatting preservation
5. Implement error handling and fallback
6. Add input/output length validation

**Acceptance Criteria**:
- [ ] Beginner users see simplified content
- [ ] Advanced users see detailed technical content
- [ ] Software-focused users see ROS 2/AI emphasis
- [ ] Hardware-focused users see robotics emphasis
- [ ] Code blocks remain unchanged
- [ ] Headings and structure preserved

### Phase 4: Urdu Translation System (Existing - Enhance & Test)

**Status**: Implemented, needs glossary and validation

**Tasks**:
1. Review content_service.translate_content() prompts
2. Add term preservation glossary to prompt
3. Test with sample chapters containing:
   - Technical terms (ROS 2, LIDAR, etc.)
   - Code blocks
   - File paths
   - Commands
4. Verify RTL rendering in frontend
5. Implement chunked processing for long chapters

**Acceptance Criteria**:
- [ ] Content translates to readable Urdu
- [ ] Technical terms preserved or correctly transliterated
- [ ] Code blocks remain in English
- [ ] RTL direction applied correctly
- [ ] Headings and structure preserved

### Phase 5: Docusaurus UI Integration (Existing - Complete & Test)

**Status**: Partially implemented, needs ChapterControls completion

**Tasks**:
1. Complete ChapterControls component:
   - Button visibility logic (guest vs logged-in vs has_background)
   - Loading states during transformation
   - Error display
   - Reset functionality
2. Integrate into DocItem theme override
3. Style buttons consistently with Docusaurus theme
4. Test on multiple chapter pages
5. Verify no interference with existing ChatWidget

**Acceptance Criteria**:
- [ ] Buttons hidden for guests
- [ ] "Complete Profile" shown if no background
- [ ] Loading spinner during transformation
- [ ] Reset restores original content
- [ ] Works alongside RAG chatbot

### Phase 6: End-to-End Integration (New)

**Tasks**:
1. Full user journey test: signup → background → personalize → translate
2. Cross-browser testing (Chrome, Firefox, Safari)
3. Mobile responsive testing
4. Rate limit enforcement verification
5. Error handling across the stack
6. Performance testing (15s threshold)

**Acceptance Criteria**:
- [ ] Complete user flow works end-to-end
- [ ] Rate limits enforced (10/hour)
- [ ] Errors handled gracefully
- [ ] Performance within thresholds
- [ ] Works on mobile devices

### Phase 7: QA and Acceptance Validation

**Tasks**:
1. Run all acceptance scenarios from spec
2. Security audit (no PII in logs, tokens secure)
3. Verify RAG chatbot unaffected
4. Documentation review
5. Create PHR for completion

**Acceptance Criteria**:
- [ ] All 10 success criteria from spec pass
- [ ] No security vulnerabilities
- [ ] Documentation complete
- [ ] Ready for deployment

## Important Decisions to Document

### Decision 1: Authentication Approach

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| A. Better-Auth Library | Use official Better-Auth npm package | Requires Node.js backend or adapter |
| **B. JWT-Compatible (Chosen)** | Custom JWT auth matching Better-Auth patterns | Works with FastAPI, full control |
| C. OAuth Only | Social login only | Simpler but requires third-party accounts |

**Decision**: Option B - JWT-Compatible implementation
**Rationale**: FastAPI backend already exists, JWT provides equivalent security, patterns match Better-Auth schema for future migration.

### Decision 2: Personalization Rules

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| A. Pure Rule-Based | Static templates per experience level | Predictable but inflexible |
| **B. LLM with Constraints (Chosen)** | Gemini with strict prompts | Flexible but needs guardrails |
| C. Hybrid | Rules + LLM fallback | Complex to maintain |

**Decision**: Option B - LLM with Constraints
**Rationale**: Gemini can adapt naturally to user backgrounds while strict prompts prevent hallucinations. Existing implementation uses this approach successfully.

### Decision 3: Translation Validation

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| A. Manual Review | Human reviews all translations | Accurate but doesn't scale |
| **B. Glossary Enforcement (Chosen)** | LLM prompt includes term glossary | Automated, consistent |
| C. Back-Translation | Translate back and compare | Expensive, slow |

**Decision**: Option B - Glossary Enforcement
**Rationale**: Embedding glossary rules in the LLM prompt ensures consistent term handling. Spot-checks can validate quality periodically.

### Decision 4: Content Caching

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| A. No Caching | Fresh transformation each time | Simple but slow |
| **B. Client-Side (Chosen)** | Cache in React state during session | Fast UX, no storage cost |
| C. Server-Side | Cache in Redis/DB | Persistence across sessions but complex |

**Decision**: Option B - Client-Side caching
**Rationale**: Transformed content cached in ChapterControls state. Original content always available for reset. No server storage needed since transformations are user-specific.

### Decision 5: Frontend Deployment

| Option | Description | Tradeoffs |
|--------|-------------|-----------|
| A. GitHub Pages | Static hosting | Free but limited build |
| **B. Vercel (Chosen)** | Docusaurus-optimized hosting | Free tier, easy deployment |
| C. Self-hosted | Own server | Full control but maintenance |

**Decision**: Option B - Vercel for frontend
**Rationale**: Docusaurus works seamlessly with Vercel. Backend remains on separate hosting (Railway/Render). CORS configured for cross-origin auth.

## Testing Strategy

### Authentication Tests

```python
# test_auth.py
def test_signup_success():
    """POST /auth/signup creates user and returns token"""

def test_signup_duplicate_email():
    """POST /auth/signup with existing email returns 409"""

def test_signin_valid_credentials():
    """POST /auth/signin returns token for valid user"""

def test_signin_invalid_password():
    """POST /auth/signin returns 401 for wrong password"""

def test_session_valid_token():
    """GET /auth/session returns user for valid token"""

def test_session_expired_token():
    """GET /auth/session returns 401 for expired token"""

def test_signout_invalidates_session():
    """POST /auth/signout removes session"""
```

### Background Tests

```python
# test_background.py
def test_create_background():
    """PUT /profile/background creates new background"""

def test_update_background():
    """PUT /profile/background updates existing background"""

def test_get_background():
    """GET /profile/background returns user background"""

def test_background_validation():
    """Invalid enum values return 400"""
```

### Personalization Tests

```python
# test_personalization.py
def test_personalize_beginner():
    """Beginner users get simplified content"""

def test_personalize_advanced():
    """Advanced users get detailed content"""

def test_personalize_preserves_code():
    """Code blocks unchanged after personalization"""

def test_personalize_preserves_headings():
    """Heading structure maintained"""

def test_personalize_rate_limit():
    """11th request in hour returns 429"""

def test_personalize_no_background():
    """Request without background returns 403"""
```

### Translation Tests

```python
# test_translation.py
def test_translate_to_urdu():
    """Content translates to Urdu script"""

def test_translate_preserves_terms():
    """Technical terms preserved or transliterated"""

def test_translate_preserves_code():
    """Code blocks remain in English"""

def test_translate_rtl_direction():
    """Response indicates RTL direction needed"""
```

### UI Tests (Manual Checklist)

- [ ] Buttons hidden for guest users
- [ ] "Complete Profile" shown when no background
- [ ] Loading spinner appears during transformation
- [ ] Error toast on API failure
- [ ] Reset button restores original
- [ ] Urdu content displays RTL
- [ ] Works with existing chat widget

### Integration Tests

- [ ] Full signup → background → personalize flow
- [ ] Full signup → background → translate flow
- [ ] RAG chatbot still works after auth features
- [ ] Cross-browser compatibility (Chrome, Firefox, Safari)
- [ ] Mobile responsive layout

### Performance Tests

- [ ] Auth operations < 2 seconds
- [ ] Personalization < 15 seconds for 5000-word chapter
- [ ] Translation < 15 seconds for 5000-word chapter
- [ ] 50 concurrent authenticated users supported

### Security Tests

- [ ] Passwords hashed with bcrypt
- [ ] JWT tokens cryptographically secure
- [ ] Rate limiting prevents brute force
- [ ] No PII in server logs
- [ ] CORS configured correctly

## Technical Guidelines

1. **Research-Concurrent Approach**: Existing code already implements most features. Focus on testing and refinement rather than reimplementation.

2. **Constitution Compliance**: All code must align with constitution.md principles. Re-check after each phase.

3. **Deterministic Transformations**: LLM prompts include constraints to ensure consistent output. Document any prompt changes.

4. **Better-Auth Patterns**: JWT tokens follow Better-Auth schema for future compatibility. Session table matches Better-Auth structure.

5. **Structured JSON Responses**: All API endpoints return structured JSON with consistent error format.

6. **MDX-Safe Content**: Transformed content must render correctly in Docusaurus. Test with various MDX elements.

7. **Rate Limit Enforcement**: Backend enforces 10 transformations/user/hour. Frontend displays remaining quota.

## Complexity Tracking

> No constitution violations requiring justification. Implementation uses straightforward patterns.

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| Database | Low | 4 tables with simple relationships |
| Authentication | Low | Standard JWT flow, no OAuth complexity |
| LLM Integration | Medium | Prompt engineering for quality control |
| Frontend State | Medium | AuthContext + ChapterControls state |
| Rate Limiting | Low | In-memory tracking per user |

## Next Steps

1. Run `/sp.tasks` to generate detailed task list
2. Execute Phase 1 verification tasks
3. Complete Phase 2 BackgroundForm UI
4. Test Phases 3-4 with sample chapters
5. Complete Phase 5 ChapterControls
6. Run end-to-end integration tests
7. Deploy and validate

---

**Plan Status**: COMPLETE
**Generated**: 2025-12-13
**Ready For**: `/sp.tasks` to generate actionable task list
