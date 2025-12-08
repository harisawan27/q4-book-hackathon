# Tasks: Integrated RAG Chatbot

**Feature**: `003-rag-chatbot`
**Input**: Design documents from `/specs/003-rag-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (src/api, src/core, src/services, src/models, scripts)
- [x] T002 Initialize Python environment and create requirements.txt with FastAPI, OpenAI, Qdrant dependencies
- [x] T003 [P] Configure backend linting (ruff) and formatting (black)
- [x] T004 Initialize Docusaurus website directory structure for ChatWidget component in `website/src/components/ChatWidget`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Setup environment variables handling (Config class) in `backend/src/core/config.py` (OPENAI_KEY, QDRANT_URL, NEON_URL)
- [x] T006 [P] Setup Qdrant connection client factory in `backend/src/core/database.py`
- [x] T007 [P] Setup Neon Postgres connection (SQLAlchemy async) in `backend/src/core/database.py`
- [x] T008 Implement logging configuration in `backend/src/core/logging.py`
- [x] T009 Create Pydantic base models (Interaction, VectorChunk) in `backend/src/models/rag.py`
- [x] T010 Setup FastAPI app factory with CORS middleware in `backend/src/main.py`
- [x] T011 Implement Qdrant collection initialization script in `backend/scripts/init_qdrant.py`

**Checkpoint**: Foundation ready - database connections and app skeleton are in place.

---

## Phase 3: User Story 1 - Reader General Q&A (Priority: P1) 🎯 MVP

**Goal**: Users can ask general questions and get grounded answers from the full book context.

**Independent Test**: Manually ingest a sample doc, start API, and curl the /chat endpoint with a general question.

### Implementation for User Story 1

- [x] T012 [US1] Create MDX parser and header-based chunker service in `backend/src/services/ingestion.py`
- [x] T013 [US1] Implement OpenAI embedding generation service in `backend/src/services/embedding.py`
- [x] T014 [US1] Implement Qdrant indexing logic (upsert vectors) in `backend/src/services/vector_store.py`
- [x] T015 [US1] Create ingestion CLI script `backend/scripts/index_book.py` to process `website/docs`
- [x] T016 [US1] Implement vector search service (retrieval) in `backend/src/services/retrieval.py`
- [x] T017 [US1] Implement chat completion service (context assembly + OpenAI call) in `backend/src/services/chat.py`
- [x] T018 [US1] Create `/chat` endpoint with SSE streaming support in `backend/src/api/routes.py`
- [x] T019 [US1] Create basic Chat UI Widget structure in `website/src/components/ChatWidget/index.tsx`
- [x] T020 [US1] Implement API client in React to stream SSE responses in `website/src/components/ChatWidget/api.ts`

**Checkpoint**: System can ingest docs and answer general questions via the API and basic UI.

---

## Phase 4: User Story 2 - Context-Specific Q&A (Priority: P1)

**Goal**: Users can select text in the book and ask questions specifically about that selection.

**Independent Test**: Select text in the UI, verify the API request includes `selected_text`, and verify the answer quotes/references that selection.

### Implementation for User Story 2

- [x] T021 [US2] Update `backend/src/models/rag.py` to include `selected_text` field in request schema
- [x] T022 [US2] Modify `backend/src/services/retrieval.py` to prioritize selected text (hybrid search or context boosting)
- [x] T023 [US2] Update `backend/src/services/chat.py` prompt to handle "Context Mode" instructions
- [x] T024 [US2] Implement text selection event listener hook `useTextSelection.ts` in `website/src/components/ChatWidget/hooks.ts`
- [x] T025 [US2] Update `website/src/components/ChatWidget/index.tsx` to display selected text quote in input area
- [x] T026 [US2] Update API client in `website/src/components/ChatWidget/api.ts` to send selection payload

**Checkpoint**: Text selection triggers context-aware mode in Chat UI and Backend.

---

## Phase 5: User Story 3 - Admin System Management (Priority: P2)

**Goal**: Admin can re-index content via API and view interaction logs.

**Independent Test**: Trigger /index endpoint, check Qdrant for updates. Check Neon DB for new log entries after a chat.

### Implementation for User Story 3

- [x] T027 [US3] Create SQLAlchemy models for `Session`, `Message`, `Feedback` in `backend/src/models/db.py`
- [x] T028 [US3] Implement async logging service in `backend/src/services/logging_service.py` (write to Neon)
- [x] T029 [US3] Integrate logging into `/chat` endpoint in `backend/src/api/routes.py`
- [x] T030 [US3] Create `/index` endpoint for admin-triggered ingestion in `backend/src/api/routes.py`
- [x] T031 [US3] Create `/feedback` endpoint for message upvotes/downvotes in `backend/src/api/routes.py`
- [x] T032 [US3] Add feedback UI buttons (Thumbs Up/Down) to `website/src/components/ChatWidget/MessageBubble.tsx`

**Checkpoint**: Full loop complete: Indexing API, Chat Logging, User Feedback.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T033 [P] Add rate limiting middleware in `backend/src/api/middleware.py`
- [x] T034 [P] Improve error handling for OpenAI/Qdrant timeouts in `backend/src/api/routes.py`
- [x] T035 [P] Style Chat Widget with Docusaurus theme variables (CSS Module) in `website/src/components/ChatWidget/styles.module.css`
- [x] T036 Update `README.md` and `specs/003-rag-chatbot/quickstart.md` with final deployment instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1. Blocks all US phases.
- **User Story 1 (Phase 3)**: Depends on Phase 2. MVP.
- **User Story 2 (Phase 4)**: Depends on Phase 3 (extends Chat logic).
- **User Story 3 (Phase 5)**: Depends on Phase 3 (logging) & Phase 2 (DB setup).

### Parallel Opportunities

- **Setup/Foundational**: Config, DB clients, and Logging can be built in parallel.
- **US1**: Ingestion scripts (Backend) and Chat Widget UI (Frontend) can be built in parallel.
- **US3**: Admin API and Feedback UI can be built in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. **Focus**: Ingest docs -> Simple RAG Chat.
2. **Goal**: Verify retrieval quality and latency < 3s.
3. **Outcome**: A working "Ask the Book" button.

### Incremental Delivery

1. **MVP**: Global search only (US1).
2. **Increment 1**: Add "Context Mode" (Text Selection) (US2).
3. **Increment 2**: Add Logging, Feedback, and Admin controls (US3).
