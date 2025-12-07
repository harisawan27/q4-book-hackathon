# Implementation Plan: Integrated RAG Chatbot

**Branch**: `003-rag-chatbot` | **Date**: 2025-12-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-rag-chatbot/spec.md`

## Summary

This feature integrates a RAG-powered chatbot into the Docusaurus book. It involves a Python FastAPI backend that ingests documentation into Qdrant (vector store), handles queries using OpenAI embeddings and chat completion, and logs interactions to Neon Postgres. The frontend is a React widget embedded in Docusaurus that supports context-aware questions via text selection.

## Technical Context

**Language/Version**: Python 3.11 (Backend), TypeScript 5.0+ (Frontend)
**Primary Dependencies**: FastAPI, OpenAI SDK, Qdrant Client, React, Docusaurus
**Storage**: Neon (Postgres), Qdrant (Vector)
**Testing**: pytest (Backend), Jest (Frontend)
**Target Platform**: Containerized Backend (Docker/Render/Railway), Static Frontend (Vercel/Netlify)
**Project Type**: Web Application (Docusaurus Frontend + API Backend)
**Performance Goals**: <3s p95 response time (excluding LLM generation)
**Constraints**: No PII storage, Strict "No Hallucination" policy

## Constitution Check

*GATE: Passed.*

- **Accuracy**: Enforced via RAG retrieval verification.
- **Transparency**: Citations required in response.
- **Reproducibility**: Ingestion scripts and API defined.
- **Security**: No PII, standard API security.
- **Consistency**: Using Docusaurus components and defined tech stack.

## Project Structure

### Documentation (this feature)

```text
specs/003-rag-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── api.yaml
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/             # FastAPI routes
│   ├── core/            # Config, Security
│   ├── services/        # RAG, Database, Qdrant logic
│   └── models/          # Pydantic models
├── scripts/             # Ingestion scripts
└── tests/

website/ (Existing)
├── src/
│   ├── components/
│   │   └── ChatWidget/  # New Chat UI
│   └── theme/           # Docusaurus theme swizzling (if needed)
```

## 1. Architecture Sketch

**Data Flow**:
1.  **Ingestion**: `Docusaurus MDX` -> `Python Script` -> `Chunking` -> `OpenAI Embedding` -> `Qdrant`.
2.  **Query**: `User` -> `Chat Widget` -> `FastAPI` -> `OpenAI Embedding` -> `Qdrant Search` -> `Context Assembly` -> `OpenAI Chat Completion` -> `FastAPI (SSE)` -> `Chat Widget`.
3.  **Logging**: `FastAPI` -> `Neon Postgres` (Async logging).

## 2. Research Approach

- **Embedding**: Selected `text-embedding-3-small` for speed/cost balance.
- **Chunking**: Header-aware Markdown splitting to preserve context.
- **Validation**: Manual testing of "Context Mode" vs "Global Mode" queries.

## 3. Quality Validation

- **Groundedness**: Validated by verifying citations in responses match retrieved chunks.
- **Selected-Text Compliance**: Test cases where user selects text X and asks question Y; system must prioritize X.
- **Latency**: Measured via API middleware logging.
- **Safety**: Test for "I don't know" responses when context is irrelevant.

## 4. Decisions Needing Documentation

| Decision | Choice | Rationale |
|---|---|---|
| **Embedding** | `text-embedding-3-small` | Efficient, low latency, sufficient for docs. |
| **Streaming** | Server-Sent Events (SSE) | Standard for LLM chat, simpler than WebSockets. |
| **Vector DB** | Qdrant Cloud | Free tier, robust filtering, Python client. |
| **Chunking** | Header-based | Preserves technical context better than fixed chars. |
| **Frontend** | React Portal/Widget | Non-intrusive overlay on Docusaurus pages. |

## 5. Testing Strategy

- **Unit Tests**: Chunking logic, API request validation, Database models.
- **Integration Tests**:
    - `test_indexing`: Run small MD sample -> Verify vectors in Qdrant.
    - `test_chat_api`: Mock OpenAI -> Verify full pipeline flow.
- **E2E Tests**: Manual verification of Chat Widget in Docusaurus build.

## 6. Phased Plan

### Phase 1: Setup & Infrastructure
- [ ] Initialize FastAPI project structure in `backend/`.
- [ ] Set up Neon Postgres and Qdrant Cloud accounts/connection.
- [ ] Implement Database migrations (SQLAlchemy/Alembic).
- [ ] Create basic "Hello World" API endpoint.

### Phase 2: Ingestion Pipeline
- [ ] Implement MDX parser and chunker.
- [ ] Implement OpenAI Embedding service.
- [ ] Create `scripts/index_book.py` to pipeline data to Qdrant.
- [ ] Verify data in Qdrant dashboard.

### Phase 3: Backend RAG Logic
- [ ] Implement `search_service` (Qdrant query + filtering).
- [ ] Implement `chat_service` (OpenAI call + context construction).
- [ ] Create `/chat` endpoint with SSE streaming.
- [ ] Add logging to Neon.

### Phase 4: Frontend Integration
- [ ] Create `ChatWidget` React component in `website/src/components`.
- [ ] Implement SSE consumption hook.
- [ ] Add text selection event listener (`mouseup` handler).
- [ ] Integrate widget into Docusaurus Layout.

### Phase 5: Polish & Deploy
- [ ] Add rate limiting.
- [ ] Add citations rendering in UI.
- [ ] Deploy backend to cloud provider.
- [ ] Configure Docusaurus build to point to production API.