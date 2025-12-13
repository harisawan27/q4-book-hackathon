# Research Findings: Authentication, Personalization & Translation

**Feature**: 005-auth-personalization-translation
**Date**: 2025-12-13
**Status**: Complete

## Research Summary

This document captures research findings for implementing user authentication with Better-Auth patterns, content personalization, and Urdu translation in the existing Docusaurus + FastAPI architecture.

## Research Tasks Completed

### 1. Better-Auth Integration with FastAPI

**Question**: How to integrate Better-Auth authentication patterns with a Python FastAPI backend?

**Finding**: Better-Auth is a TypeScript/JavaScript library designed for Node.js backends. For FastAPI (Python), we implement a JWT-compatible authentication flow that mirrors Better-Auth's schema and patterns.

**Decision**: Implement custom JWT authentication following Better-Auth table structures
**Rationale**:
- FastAPI backend already exists and works well
- JWT provides equivalent security to Better-Auth tokens
- Database schema matches Better-Auth for potential future migration
- Full control over authentication logic

**Alternatives Considered**:
- Node.js microservice for auth only (rejected: added complexity, latency)
- OAuth-only authentication (rejected: requires third-party accounts)
- Session cookies (rejected: less suitable for API-first architecture)

**Implementation Details**:
```python
# Better-Auth compatible table structure implemented in backend/src/models/auth.py
class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    email_verified = Column(DateTime, nullable=True)
    name = Column(String(255))
    image = Column(Text, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class AuthSession(Base):
    __tablename__ = "auth_sessions"
    id = Column(UUID, primary_key=True)
    session_token = Column(String(255), unique=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    expires = Column(DateTime)
```

### 2. LLM-Based Content Personalization

**Question**: Should personalization use rule-based templates or LLM-generated adaptations?

**Finding**: LLM-based personalization with strict prompt constraints provides the best balance of flexibility and accuracy. The existing `content_service.py` already implements this approach.

**Decision**: Use Gemini 2.5 Flash with constrained prompts
**Rationale**:
- Natural language adaptation to user backgrounds
- Strict prompt rules prevent hallucinations
- Preserves markdown structure and code blocks
- Maintains factual integrity of original content

**Prompt Engineering Findings**:
```
Key constraints in personalization prompts:
1. PRESERVE ALL TECHNICAL ACCURACY
2. PRESERVE MARKDOWN STRUCTURE
3. ADAPT EXPLANATIONS based on reader's background
4. MAINTAIN THE SAME LENGTH
5. DO NOT ADD NEW INFORMATION
6. DO NOT REMOVE ANY SECTIONS
```

**Alternatives Considered**:
- Static templates per experience level (rejected: inflexible, limited adaptation)
- Hybrid rule + LLM approach (rejected: complex to maintain)
- Client-side browser translation (rejected: inconsistent, no quality control)

### 3. Urdu Translation Quality Assurance

**Question**: How to ensure technical term accuracy in Urdu translations?

**Finding**: Embedding a glossary of technical terms directly in the LLM prompt ensures consistent handling of robotics and AI terminology.

**Decision**: Glossary enforcement in translation prompts
**Rationale**:
- Automated and scalable
- Consistent term handling across all chapters
- Can be updated centrally when new terms added
- Spot-check validation sufficient for quality assurance

**Glossary Implementation**:
```
Technical Term Glossary (embedded in prompts):
- ROS 2, ROS → Keep as "ROS 2", "ROS"
- LIDAR → Keep as "LIDAR"
- Neural Network → نیورل نیٹ ورک (transliteration)
- Robot → روبوٹ
- Sensor → سینسر
- Python → پائتھون
- Code blocks → Preserve exactly as-is
- File paths → Preserve exactly as-is
```

**Alternatives Considered**:
- Manual review of all translations (rejected: doesn't scale)
- Back-translation validation (rejected: expensive, slow)
- Google Translate API (rejected: less control over technical terms)

### 4. Content Caching Strategy

**Question**: Should transformed content be cached server-side or client-side?

**Finding**: Client-side caching in React state provides the best user experience without additional infrastructure.

**Decision**: Client-side caching in ChapterControls component
**Rationale**:
- No additional infrastructure (Redis, etc.)
- Instant reset to original content
- User-specific transformations don't pollute shared cache
- Refresh/reload triggers fresh transformation if desired

**Implementation Pattern**:
```typescript
// ChapterControls state management
const [originalContent, setOriginalContent] = useState(content);
const [displayContent, setDisplayContent] = useState(content);
const [contentState, setContentState] = useState<'original' | 'personalized' | 'translated'>('original');

const handleReset = () => {
  setDisplayContent(originalContent);
  setContentState('original');
};
```

**Alternatives Considered**:
- Server-side Redis cache (rejected: added complexity, user-specific data)
- Database storage of transformations (rejected: storage costs, privacy concerns)
- No caching at all (rejected: slow reset experience)

### 5. Rate Limiting Implementation

**Question**: How to enforce per-user rate limits for transformation APIs?

**Finding**: In-memory rate limiting with user-specific tracking is sufficient for current scale.

**Decision**: In-memory timestamp tracking per user ID
**Rationale**:
- Simple implementation
- Works for single-instance deployment
- Easy to upgrade to Redis later if needed
- Resets on server restart (acceptable for current scale)

**Implementation Pattern**:
```python
# Existing implementation in backend/src/api/content_routes.py
from collections import defaultdict
from datetime import datetime, timedelta

user_transform_timestamps: dict[str, list[datetime]] = defaultdict(list)

def check_rate_limit(user_id: str, limit: int = 10, window_seconds: int = 3600) -> bool:
    now = datetime.now()
    cutoff = now - timedelta(seconds=window_seconds)

    # Clean old timestamps
    user_transform_timestamps[user_id] = [
        ts for ts in user_transform_timestamps[user_id] if ts > cutoff
    ]

    if len(user_transform_timestamps[user_id]) >= limit:
        return False

    user_transform_timestamps[user_id].append(now)
    return True
```

### 6. Frontend Authentication State

**Question**: How to share authentication state across Docusaurus components?

**Finding**: React Context API with AuthProvider wrapping the app root provides clean state management.

**Decision**: AuthProvider context in Root.tsx theme override
**Rationale**:
- Standard React pattern
- Works with Docusaurus theme system
- Accessible from any component via useAuth hook
- Handles loading and error states

**Implementation Pattern**:
```typescript
// website/src/theme/Root.tsx
import { AuthProvider } from '../components/AuthProvider';

export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}

// Any component can access auth state
const { user, isAuthenticated, hasBackground } = useAuth();
```

### 7. Docusaurus DocItem Integration

**Question**: How to inject ChapterControls into doc pages without forking Docusaurus core?

**Finding**: Docusaurus theme swizzling allows overriding DocItem component to add custom controls.

**Decision**: Swizzle DocItem and add ChapterControls
**Rationale**:
- Official Docusaurus extension point
- No core modifications needed
- Updates safely with Docusaurus upgrades
- Controls appear consistently on all doc pages

**Implementation Pattern**:
```typescript
// website/src/theme/DocItem/index.tsx
import DocItem from '@theme-original/DocItem';
import ChapterControls from '../../components/ChapterControls';

export default function DocItemWrapper(props) {
  return (
    <>
      <ChapterControls />
      <DocItem {...props} />
    </>
  );
}
```

### 8. RTL Support for Urdu Content

**Question**: How to properly render Urdu text with right-to-left direction?

**Finding**: CSS `dir="rtl"` attribute on the content container provides proper RTL rendering.

**Decision**: Apply dir="rtl" when displaying translated content
**Rationale**:
- Standard HTML/CSS approach
- Browsers handle text alignment and punctuation
- Code blocks remain LTR automatically
- Reversible when switching back to English

**Implementation Pattern**:
```tsx
<div
  dir={contentState === 'translated' ? 'rtl' : 'ltr'}
  className="chapter-content"
>
  {displayContent}
</div>
```

## Existing Implementation Analysis

### Backend Services (Already Implemented)

| Service | File | Status | Notes |
|---------|------|--------|-------|
| auth_service.py | backend/src/services/ | Complete | JWT, password hashing, user CRUD |
| content_service.py | backend/src/services/ | Complete | Personalization & translation |
| auth_routes.py | backend/src/api/ | Complete | All auth endpoints |
| profile_routes.py | backend/src/api/ | Complete | Background CRUD |
| content_routes.py | backend/src/api/ | Complete | Transform endpoints |
| auth_middleware.py | backend/src/middleware/ | Complete | JWT verification |

### Frontend Components (Partially Implemented)

| Component | Directory | Status | Needs Work |
|-----------|-----------|--------|------------|
| AuthProvider | website/src/components/ | Complete | None |
| SignIn | website/src/components/ | Complete | None |
| SignUp | website/src/components/ | Complete | Add background step |
| BackgroundForm | website/src/components/ | Partial | Complete all fields |
| NavbarAuth | website/src/components/ | Complete | None |
| ChapterControls | website/src/components/ | Partial | Complete button logic |
| lib/auth.ts | website/src/lib/ | Complete | None |

### Database Schema (Needs Verification)

| Table | Migration | Status |
|-------|-----------|--------|
| users | 005_user_personalization.sql | Verify applied |
| user_backgrounds | 005_user_personalization.sql | Verify applied |
| auth_sessions | 005_user_personalization.sql | Verify applied |
| transformation_logs | 005_user_personalization.sql | Verify applied |

## Technical Decisions Summary

| Decision | Choice | Key Reason |
|----------|--------|------------|
| Auth approach | JWT-compatible (not Better-Auth library) | FastAPI backend compatibility |
| Personalization method | LLM with strict prompts | Flexible yet controlled |
| Translation quality | Glossary in prompts | Automated term consistency |
| Content caching | Client-side React state | Simple, user-specific |
| Rate limiting | In-memory per-user | Sufficient for scale |
| Auth state | React Context | Standard pattern |
| Doc integration | DocItem swizzle | Official extension point |
| RTL support | CSS dir attribute | Browser-native rendering |

## Open Questions Resolved

1. ✅ Better-Auth integration → JWT-compatible implementation
2. ✅ Personalization accuracy → LLM with constraints
3. ✅ Translation term handling → Embedded glossary
4. ✅ Caching strategy → Client-side state
5. ✅ Rate limiting → In-memory tracking
6. ✅ Auth state sharing → React Context
7. ✅ Doc page integration → Theme swizzle
8. ✅ RTL rendering → CSS dir attribute

## References

- Better-Auth documentation: https://www.better-auth.com/docs
- FastAPI JWT implementation: https://fastapi.tiangolo.com/tutorial/security/
- Docusaurus theming: https://docusaurus.io/docs/swizzling
- Gemini API: https://ai.google.dev/docs
- RTL CSS: https://developer.mozilla.org/en-US/docs/Web/CSS/direction

---

**Research Status**: COMPLETE
**Next Step**: Proceed to Phase 1 (Data Model & Contracts)
