---
id: 019
title: fix-qdrant-async-client
stage: green
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: 003-rag-chatbot
branch: 003-rag-chatbot
user: User
command: it appears now but not replying and on backend cmd logs "AttributeError: 'QdrantClient' object has no attribute 'search'"...
labels: ["bugfix", "backend", "qdrant", "async"]
links:
  spec: specs/003-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/core/database.py
  - backend/src/services/retrieval.py
tests:
  - (none)
---

## Prompt

it appears now but not replying and on backend cmd logs "AttributeError: 'QdrantClient' object has no attribute 'search'"...

## Response snapshot

The user encountered `AttributeError: 'QdrantClient' object has no attribute 'search'`.
This is likely a sync/async mismatch or client initialization issue.
I refactored `database.py` to export `get_async_qdrant_client()` using `AsyncQdrantClient`.
I updated `retrieval.py` to use this async client and await `client.search()`.

## Outcome

- ✅ Impact: Backend retrieval should now work correctly with `await`.
- 🧪 Tests: User needs to retry chat.
- 📁 Files: `backend/src/core/database.py`, `backend/src/services/retrieval.py`.
- 🔁 Next prompts: Confirm chat works.
- 🧠 Reflection: Using async client is better for FastAPI anyway.

## Evaluation notes (flywheel)

- Failure modes observed: AttributeError on sync client method in async context (or unexpected API change).
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
