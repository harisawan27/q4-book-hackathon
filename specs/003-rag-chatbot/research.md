# Research: Integrated RAG Chatbot

**Feature**: `003-rag-chatbot`
**Status**: Researching
**Decisions Needed**: Embedding Model, Chunking Strategy, Streaming Protocol, Qdrant Schema.

## Decision 1: Embedding Model

- **Options**: 
  1. `text-embedding-3-small` (1536 dim, cheaper, fast)
  2. `text-embedding-3-large` (3072 dim, higher accuracy)
  3. `text-embedding-ada-002` (Legacy)

- **Selection**: `text-embedding-3-small`
- **Rationale**: Sufficient accuracy for technical documentation; significantly faster and cheaper than large. Lower latency fits the "under 3s" requirement.
- **Implications**: Qdrant vector size must be 1536.

## Decision 2: Chunking Strategy

- **Options**:
  1. Fixed-size character chunking.
  2. Recursive character chunking (LangChain style).
  3. Markdown-header aware chunking.

- **Selection**: **Markdown-header aware chunking** (split by H2/H3, then recursive).
- **Rationale**: Preserves semantic context of technical modules. A chunk should ideally be a complete concept (e.g., "How to install ROS2").
- **Config**: Chunk size ~1000 tokens, overlap ~200 tokens.

## Decision 3: Streaming Protocol

- **Options**:
  1. WebSockets.
  2. Server-Sent Events (SSE).
  3. Polling.

- **Selection**: **Server-Sent Events (SSE)**.
- **Rationale**: Standard for LLM streaming (OpenAI uses it). Easier to implement through firewalls/proxies than WebSockets. Unidirectional (server -> client) fits the chat response model perfectly.

## Decision 4: Qdrant Schema

- **Collection**: `docusaurus_book`
- **Vector Config**: size: 1536, distance: Cosine.
- **Payload**:
  - `source`: (string) e.g., "modules/intro.md"
  - `url`: (string) e.g., "/docs/intro"
  - `content`: (string) The actual text chunk.
  - `header_path`: (keyword) e.g., "Introduction > Setup"
  - `last_updated`: (datetime)

## Decision 5: RAG Framework

- **Selection**: **LangChain** (Python) or **OpenAI Assistants API** directly?
- **Decision**: **OpenAI Chat Completions API + Custom Qdrant Logic**.
- **Rationale**: Assistants API can be opaque regarding retrieval. Custom logic allows us to prioritize "selected text" vs "global search" explicitly as required by User Story 2. We will use a lightweight abstraction (like LangChain or simple code) but control the retrieval step.

