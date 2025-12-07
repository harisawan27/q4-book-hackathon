# Feature Specification: Integrated RAG Chatbot

**Feature Branch**: `003-rag-chatbot`
**Created**: 2025-12-07
**Status**: Draft
**Input**: Integrated RAG Chatbot inside the Docusaurus-based Physical AI & Humanoid Robotics Capstone Book.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reader General Q&A (Priority: P1)

A reader wants to ask general questions about the book's content (e.g., "How do I calibrate the sensors?") to get a quick summary without searching manually.

**Why this priority**: Core value proposition; makes the book interactive and accessible.

**Independent Test**: Can be tested by deploying the chatbot with the book index and asking general knowledge questions.

**Acceptance Scenarios**:

1. **Given** the chatbot is open, **When** the user types "What is the ROS2 node graph?", **Then** the system retrieves relevant sections and provides a summarized answer with citations.
2. **Given** the chatbot is open, **When** the user asks a question not in the book, **Then** the system replies that it cannot answer based on the provided content.

---

### User Story 2 - Context-Specific Q&A (Priority: P1)

A reader highlights a specific paragraph in the book and asks a question about it (e.g., "Explain this code snippet" or "What does this term mean here?") to get targeted help.

**Why this priority**: Differentiator feature; provides "tutor-like" assistance.

**Independent Test**: Can be tested by simulating text selection events and verifying the backend prioritizes that context.

**Acceptance Scenarios**:

1. **Given** the user selects a text block about "URDF modeling", **When** they click "Ask AI", **Then** the chatbot opens with the selection quoted.
2. **Given** a selection is active, **When** the user asks "What does this mean?", **Then** the answer is grounded *strictly* in the selected text and immediate context.

---

### User Story 3 - Admin System Management (Priority: P2)

An admin needs to monitor system usage and update the knowledge base when the book content changes.

**Why this priority**: Essential for maintenance and quality control.

**Independent Test**: Can be tested via API endpoints for re-indexing and log retrieval.

**Acceptance Scenarios**:

1. **Given** the book content has changed, **When** the admin triggers the `reindex` endpoint, **Then** the system extracts new MDX content, generates embeddings, and updates Qdrant.
2. **Given** users have interacted with the bot, **When** the admin queries the logs, **Then** they can see a history of questions, retrieved chunks, and generated answers.

### Edge Cases

- **Empty/Irrelevant Selection**: User selects whitespace or non-text elements. System should ignore or prompt for valid selection.
- **Service Outage**: Qdrant or OpenAI API is down. System should show a graceful error message ("AI temporarily unavailable").
- **Rate Limiting**: User spams questions. System should block requests for a cooldown period.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Chat UI MUST be embedded in the documentation platform as a floating widget or sidebar panel.
- **FR-002**: System MUST capture text selection events in the DOM and pass the content to the chat input.
- **FR-003**: The backend MUST implement a RAG pipeline: Embedding -> Vector Search -> Context Assembly -> Generation.
- **FR-004**: System MUST distinguish between "Global Search" (query entire book) and "Context Mode" (query focused on selection).
- **FR-005**: All user interactions (queries, selected text, answers, feedback) MUST be logged to the persistence layer.
- **FR-006**: System MUST enforce rate limiting (e.g., requests per hour per IP) to prevent abuse.
- **FR-007**: The ingestion pipeline MUST be capable of parsing documentation source files (MDX), stripping components, and chunking text by headers.
- **FR-008**: Responses MUST include citations (links to the specific book section) when retrieved from the vector store.
- **FR-009**: System MUST strictly adhere to the "No Hallucination" rule: if relevant context is not found, state "Information not found in book."

### Constraints

- **Tech Stack**: Must use OpenAI Agents, FastAPI, Neon Serverless Postgres, Qdrant Cloud, and Docusaurus.
- **Data Privacy**: No storing of user-selected text unless explicitly allowed (though metadata is logged).
- **Deployment**: Backend must be container-deployable.

### Key Entities *(include if feature involves data)*

- **Conversation Log**: Records the session ID, timestamp, and user metadata.
- **Interaction**: A single Q&A turn (User Query, Selected Context, Retrieved Chunks, AI Response, Feedback).
- **Vector Chunk**: A segment of book content stored in the vector database with metadata (Source File, Header Path, Content Hash).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Retrieval Precision**: Top 3 retrieved chunks contain the correct answer 85% of the time for valid questions.
- **SC-002**: **Response Latency**: 95% of requests complete in under 3 seconds (excluding generation time latency inherent to the LLM provider).
- **SC-003**: **Hallucination Rate**: 0% hallucinations when answering questions in "Context Mode" (selected text).
- **SC-004**: **System Reliability**: System successfully handles valid re-indexing of the full book in under 5 minutes.
- **SC-005**: **User Satisfaction**: Chat widget loads without blocking the main page rendering (Core Web Vitals unaffected).