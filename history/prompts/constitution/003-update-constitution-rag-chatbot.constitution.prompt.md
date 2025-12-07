---
id: 003
title: update-constitution-rag-chatbot
stage: constitution
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: User
command: /sp.constitution
labels: ["constitution", "rag", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - (none)
---

## Prompt

/sp.constitution /sp.constitution

Project: Integrated RAG Chatbot for Docusaurus Robotics Book

Core principles:
- Accuracy: All chatbot responses must rely strictly on the book’s content or the user-selected text.
- Transparency: The system must clearly indicate when it cannot answer because the content is outside the retrieved context.
- Reproducibility: All RAG pipeline steps (embedding, retrieval, API calls, schema, metadata) must be documented and traceable.
- Security: No unsafe model actions, unrestricted tool execution, or hallucinations beyond retrieved text.
- Consistency: Chatbot behavior must remain aligned with the book’s technical definitions, modules, and terminology.

Key standards:
- RAG must use: OpenAI Agents/ChatKit SDKs + FastAPI backend + Neon Serverless Postgres + Qdrant Cloud (Free Tier).
- Retrieval must be deterministic and based on:
  - User-selected text (highest priority)
  - Book corpus embeddings stored in Qdrant
- Vector schema:
  - Clear metadata fields (file path, section, heading, paragraph ID)
  - Embeddings must be stored in Qdrant with versioning
- Book content ingestion:
  - Automated pipeline that extracts MD/MDX content from Docusaurus
  - Embeds and syncs updates into Qdrant + Neon
- UI behavior:
  - Chatbot embedded as a panel inside the published book
  - Must support: text selection → “Ask AI about this section”
  - Must provide citations to retrieved chunks
- Answering rules:
  - No answer may include information outside retrieved material
  - If retrieval does not support the answer: return “Not enough information”

Constraints:
- Models: Only OpenAI models via Agents/ChatKit
- Frontend: Must render inside Docusaurus using React/MDX components
- Backend: FastAPI, container-deployable
- Database constraints:
  - Neon: structured metadata + usage logs
  - Qdrant: vector storage only
- No personally identifiable data stored
- Performance: Response latency max 3 seconds under normal load

Success criteria:
- Chatbot fully deploys within the Docusaurus site
- Users can highlight any text and ask questions about it
- Retrieval uses correct embeddings and returns consistent citations
- All answers generated strictly from retrieved context
- Pipeline for embedding/syncing book updates is documented and reproducible
- Backend deploys successfully on standard cloud VM or serverless platform
- No hallucinated answers during validation tests

## Response snapshot

Updated constitution to v2.0.0 reflecting RAG Chatbot principles.

## Outcome

- ✅ Impact: Constitution aligned with new project scope.
- 🧪 Tests: N/A
- 📁 Files: Updated constitution.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Significant pivot in project scope requires careful propagation to specs.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
