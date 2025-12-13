# Tasks: User Authentication, Personalization & Urdu Translation

**Input**: Design documents from `/specs/005-auth-personalization-translation/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec. Manual E2E testing specified in plan.md.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/migrations/`
- **Frontend**: `website/src/`
- **Specs**: `specs/005-auth-personalization-translation/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify project setup and dependencies are ready

- [X] T001 Verify backend dependencies in backend/requirements.txt include passlib, python-jose, bcrypt
- [X] T002 [P] Verify frontend dependencies in website/package.json include required React packages
- [X] T003 [P] Verify CORS configuration in backend/src/main.py allows frontend origin
- [X] T004 [P] Create/verify .env.example files in backend/ and website/ with all required variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Run database migration backend/migrations/005_user_personalization.sql in Neon Postgres
- [X] T006 Verify User model in backend/src/models/auth.py matches data-model.md schema
- [X] T007 [P] Verify UserBackground model in backend/src/models/auth.py with correct enum constraints
- [X] T008 [P] Verify AuthSession model in backend/src/models/auth.py with session_token and expires fields
- [X] T009 [P] Verify TransformationLog model in backend/src/models/auth.py with all audit fields
- [X] T010 Verify auth_service.py in backend/src/services/auth_service.py implements hash_password, verify_password, create_token, verify_token
- [X] T011 Verify auth_middleware.py in backend/src/middleware/auth_middleware.py implements get_current_user dependency
- [X] T012 [P] Verify Pydantic schemas in backend/src/models/auth_schemas.py match contracts/*.yaml definitions
- [X] T013 Register auth router in backend/src/main.py under /api/v1/auth prefix
- [X] T014 [P] Register profile router in backend/src/main.py under /api/v1/profile prefix
- [X] T015 [P] Register content router in backend/src/main.py under /api/v1/content prefix
- [X] T016 Verify rate limiting middleware in backend/src/api/middleware.py for transformation endpoints

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - User Account Registration (Priority: P1) MVP

**Goal**: Allow new visitors to create accounts with email, password, name, and complete background questionnaire

**Independent Test**: Navigate to /signup, fill form, complete questionnaire, verify signin works

### Implementation for User Story 1

- [X] T017 [US1] Implement POST /auth/signup endpoint in backend/src/api/auth_routes.py per contracts/auth.yaml
- [X] T018 [US1] Add email uniqueness validation in signup endpoint in backend/src/api/auth_routes.py
- [X] T019 [US1] Add password strength validation (min 8 chars) in signup endpoint in backend/src/api/auth_routes.py
- [X] T020 [US1] Implement optional background creation during signup in backend/src/api/auth_routes.py
- [X] T021 [P] [US1] Create SignUp component in website/src/components/SignUp/index.tsx with email, password, name fields
- [X] T022 [P] [US1] Create BackgroundForm component in website/src/components/BackgroundForm/index.tsx with all questionnaire fields
- [X] T023 [US1] Integrate BackgroundForm as second step in SignUp flow in website/src/components/SignUp/index.tsx
- [X] T024 [US1] Create /signup page in website/src/pages/signup.tsx using SignUp component
- [X] T025 [US1] Add form validation error display in SignUp component in website/src/components/SignUp/index.tsx
- [X] T026 [US1] Add API client signup function in website/src/lib/auth.ts

**Checkpoint**: User Story 1 complete - new users can register with background

---

## Phase 4: User Story 2 - User Sign In and Sign Out (Priority: P1) MVP

**Goal**: Allow returning users to sign in, maintain session, and sign out

**Independent Test**: Navigate to /signin, enter credentials, verify session active, click signout, verify session ended

### Implementation for User Story 2

- [X] T027 [US2] Implement POST /auth/signin endpoint in backend/src/api/auth_routes.py per contracts/auth.yaml
- [X] T028 [US2] Implement POST /auth/signout endpoint in backend/src/api/auth_routes.py per contracts/auth.yaml
- [X] T029 [US2] Implement GET /auth/session endpoint in backend/src/api/auth_routes.py per contracts/auth.yaml
- [X] T030 [US2] Add secure credential validation (don't reveal which field incorrect) in backend/src/api/auth_routes.py
- [X] T031 [P] [US2] Create SignIn component in website/src/components/SignIn/index.tsx with email and password fields
- [X] T032 [P] [US2] Create AuthProvider context in website/src/components/AuthProvider/index.tsx with user, token, loading states
- [X] T033 [US2] Add signin, signout, checkSession methods to AuthProvider in website/src/components/AuthProvider/index.tsx
- [X] T034 [US2] Create /signin page in website/src/pages/signin.tsx using SignIn component
- [X] T035 [US2] Wrap app with AuthProvider in website/src/theme/Root.tsx
- [X] T036 [P] [US2] Create NavbarAuth component in website/src/components/NavbarAuth/index.tsx showing Sign In/Sign Up or User name/Sign Out
- [X] T037 [US2] Integrate NavbarAuth into Docusaurus navbar in website/src/theme/NavbarItem/index.tsx
- [X] T038 [US2] Add API client signin, signout, getSession functions in website/src/lib/auth.ts
- [X] T039 [US2] Implement session persistence across page refreshes in AuthProvider in website/src/components/AuthProvider/index.tsx

**Checkpoint**: User Story 2 complete - users can sign in, maintain session, sign out

---

## Phase 5: User Story 3 - Content Personalization (Priority: P2)

**Goal**: Logged-in users can personalize chapter content based on their background

**Independent Test**: Login, navigate to chapter, click Personalize Content, verify content adapts to background

### Implementation for User Story 3

- [X] T040 [US3] Implement content_service.personalize_content() in backend/src/services/content_service.py with Gemini LLM
- [X] T041 [US3] Add personalization prompt with experience-level and domain-focus rules in backend/src/services/content_service.py
- [X] T042 [US3] Implement POST /content/personalize endpoint in backend/src/api/content_routes.py per contracts/content.yaml
- [X] T043 [US3] Add background check (return 403 if no background) in personalize endpoint in backend/src/api/content_routes.py
- [X] T044 [US3] Add rate limiting check (10/hour/user) in personalize endpoint in backend/src/api/content_routes.py
- [X] T045 [US3] Add TransformationLog entry on personalization in backend/src/api/content_routes.py
- [X] T046 [P] [US3] Create ChapterControls component in website/src/components/ChapterControls/index.tsx with Personalize button
- [X] T047 [US3] Add personalizeContent API function in website/src/lib/auth.ts
- [X] T048 [US3] Implement content extraction from chapter DOM in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T049 [US3] Add loading state during personalization in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T050 [US3] Cache original content in React state for reset in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T051 [US3] Add Reset to Original button and handler in ChapterControls in website/src/components/ChapterControls/index.tsx

**Checkpoint**: User Story 3 complete - personalization works end-to-end

---

## Phase 6: User Story 4 - Urdu Translation (Priority: P2)

**Goal**: Logged-in users can translate chapter content to Urdu with preserved technical terms

**Independent Test**: Login, navigate to chapter, click Translate to Urdu, verify Urdu content with correct terms

### Implementation for User Story 4

- [X] T052 [US4] Implement content_service.translate_content() in backend/src/services/content_service.py with Gemini LLM
- [X] T053 [US4] Add translation prompt with technical term glossary in backend/src/services/content_service.py
- [X] T054 [US4] Add code block preservation rule in translation prompt in backend/src/services/content_service.py
- [X] T055 [US4] Implement POST /content/translate endpoint in backend/src/api/content_routes.py per contracts/content.yaml
- [X] T056 [US4] Add rate limiting check (10/hour/user) in translate endpoint in backend/src/api/content_routes.py
- [X] T057 [US4] Add TransformationLog entry on translation in backend/src/api/content_routes.py
- [X] T058 [US4] Add Translate to Urdu button to ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T059 [US4] Add translateContent API function in website/src/lib/auth.ts
- [X] T060 [US4] Add loading state during translation in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T061 [US4] Apply RTL direction (dir="rtl") when displaying translated content in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T062 [US4] Share Reset to Original button between personalization and translation states in website/src/components/ChapterControls/index.tsx

**Checkpoint**: User Story 4 complete - translation works end-to-end

---

## Phase 7: User Story 5 - Chapter Controls Visibility (Priority: P3)

**Goal**: Personalize/Translate buttons only visible for logged-in users with completed background

**Independent Test**: View chapter as guest (no buttons), login without background (see prompt), complete background (see buttons)

### Implementation for User Story 5

- [X] T063 [US5] Add useAuth hook usage in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T064 [US5] Hide buttons completely for guest users in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T065 [US5] Show Complete Profile link when logged in but no background in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T066 [US5] Show both buttons when logged in with background in ChapterControls in website/src/components/ChapterControls/index.tsx
- [X] T067 [US5] Integrate ChapterControls into DocItem theme override in website/src/theme/DocItem/index.tsx
- [X] T068 [US5] Style buttons consistently with Docusaurus theme in website/src/components/ChapterControls/styles.module.css

**Checkpoint**: User Story 5 complete - visibility logic correct for all user states

---

## Phase 8: User Story 6 - Profile Management (Priority: P3)

**Goal**: Logged-in users can view and update their profile and background

**Independent Test**: Login, navigate to /profile, view data, update background, verify changes saved

### Implementation for User Story 6

- [X] T069 [US6] Implement GET /profile endpoint in backend/src/api/profile_routes.py per contracts/profile.yaml
- [X] T070 [US6] Implement GET /profile/background endpoint in backend/src/api/profile_routes.py per contracts/profile.yaml
- [X] T071 [US6] Implement PUT /profile/background endpoint in backend/src/api/profile_routes.py per contracts/profile.yaml
- [X] T072 [US6] Add enum validation for background update in backend/src/api/profile_routes.py
- [X] T073 [P] [US6] Create profile page in website/src/pages/profile.tsx showing user info and background
- [X] T074 [US6] Add getProfile, getBackground, updateBackground API functions in website/src/lib/auth.ts
- [X] T075 [US6] Add edit mode to BackgroundForm component in website/src/components/BackgroundForm/index.tsx
- [X] T076 [US6] Integrate editable BackgroundForm in profile page in website/src/pages/profile.tsx
- [X] T077 [US6] Add success/error feedback on profile update in website/src/pages/profile.tsx

**Checkpoint**: User Story 6 complete - profile management works end-to-end

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, logging, and final integration

- [X] T078 [P] Implement GET /content/logs endpoint in backend/src/api/content_routes.py per contracts/content.yaml
- [X] T079 [P] Add error handling for LLM service unavailability in backend/src/services/content_service.py
- [X] T080 Add request/response logging for auth endpoints in backend/src/api/auth_routes.py
- [X] T081 [P] Add request/response logging for content endpoints in backend/src/api/content_routes.py
- [X] T082 Verify RAG chatbot still works after auth integration in backend/src/main.py
- [X] T083 [P] Add error toast/message display in frontend components
- [ ] T084 Run quickstart.md validation - test all API endpoints with curl
- [ ] T085 Run end-to-end user flow test: signup -> background -> personalize -> translate -> profile
- [ ] T086 Verify cross-browser compatibility (Chrome, Firefox, Safari)
- [ ] T087 Verify mobile responsive layout for auth pages and chapter controls

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **US1 Registration (Phase 3)**: Depends on Foundational
- **US2 Sign In/Out (Phase 4)**: Depends on Foundational, can run parallel to US1
- **US3 Personalization (Phase 5)**: Depends on US1+US2 (needs auth flow working)
- **US4 Translation (Phase 6)**: Depends on US1+US2, can run parallel to US3
- **US5 Controls Visibility (Phase 7)**: Depends on US3+US4 (needs buttons to exist)
- **US6 Profile (Phase 8)**: Depends on US1+US2, can run parallel to US3-US5
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS all below)
    ↓
    ├─→ US1 (P1): Registration
    │       ↓
    └─→ US2 (P1): Sign In/Out ←─ (can parallel with US1)
            ↓
    ┌───────┼───────┐
    ↓       ↓       ↓
US3 (P2) US4 (P2) US6 (P3) ←─ (can all parallel)
    ↓       ↓
    └───┬───┘
        ↓
    US5 (P3): Visibility
        ↓
    Phase 9: Polish
```

### Parallel Opportunities

**Within Phase 2 (Foundational)**:
- T006, T007, T008, T009 (models) can run in parallel
- T012, T014, T015 can run in parallel after models

**Within Phase 3 (US1)**:
- T021, T022 (components) can run in parallel before integration

**Within Phase 4 (US2)**:
- T031, T032, T036 (components) can run in parallel

**Within Phase 5 (US3)**:
- T046 can run parallel to backend T040-T045

**Across Phases**:
- US3, US4, US6 can all run in parallel after US1+US2 complete

---

## Parallel Example: User Story 3 + User Story 4

```bash
# After US1+US2 complete, launch both stories in parallel:

# Developer A: User Story 3 (Personalization)
Task: T040-T051 (backend + frontend personalization)

# Developer B: User Story 4 (Translation)
Task: T052-T062 (backend + frontend translation)

# Then merge and complete US5 (visibility logic)
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1 (Registration)
4. Complete Phase 4: User Story 2 (Sign In/Out)
5. **STOP and VALIDATE**: Users can register, sign in, sign out
6. Deploy MVP

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 + US2 → Basic auth working → Deploy (MVP!)
3. Add US3 → Personalization working → Deploy
4. Add US4 → Translation working → Deploy
5. Add US5 → Visibility logic correct → Deploy
6. Add US6 → Profile management → Deploy
7. Polish → Production ready

---

## Summary

| Phase | User Story | Tasks | Priority | Status |
|-------|-----------|-------|----------|--------|
| 1 | Setup | T001-T004 | - | Complete |
| 2 | Foundational | T005-T016 | - | Complete |
| 3 | US1: Registration | T017-T026 | P1 | Complete |
| 4 | US2: Sign In/Out | T027-T039 | P1 | Complete |
| 5 | US3: Personalization | T040-T051 | P2 | Complete |
| 6 | US4: Translation | T052-T062 | P2 | Complete |
| 7 | US5: Controls Visibility | T063-T068 | P3 | Complete |
| 8 | US6: Profile | T069-T077 | P3 | Complete |
| 9 | Polish | T078-T087 | - | E2E Test Needed |

**Total Tasks**: 87
**MVP Tasks (US1+US2)**: 35 (T001-T039, minus some parallel)
**Per-Story Breakdown**:
- US1: 10 tasks
- US2: 13 tasks
- US3: 12 tasks
- US4: 11 tasks
- US5: 6 tasks
- US6: 9 tasks
- Setup: 4 tasks
- Foundational: 12 tasks
- Polish: 10 tasks

**Parallel Opportunities**: 23 tasks marked [P]
**Suggested MVP Scope**: Phases 1-4 (Setup through US2)

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story is independently testable after completion
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Existing code in codebase may need verification rather than creation
