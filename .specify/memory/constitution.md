<!--
SYNC IMPACT REPORT
Version change: 1.1.0 -> 2.0.0
Modified: Renamed project to "Integrated RAG Chatbot for Docusaurus Robotics Book". Updated all principles to align with RAG/AI constraints.
Added sections: Transparency, Security, Detailed Technology Stack & Constraints.
Removed sections: Accessibility & Clarity (merged into Consistency), Framework Alignment (merged into Consistency).
Templates requiring updates: None.
Follow-up: None.
-->
# Integrated RAG Chatbot for Docusaurus Robotics Book Constitution

## Core Principles

### I. Spec-Driven Development (SDD)
All features start with a specification. We clarify requirements, outline structure, and define content blocks before writing code. The spec file is the source of truth.

### II. Accuracy
All chatbot responses must rely strictly on the book’s content or the user-selected text. Hallucinations or answers derived from outside the retrieved context are unacceptable.

### III. Transparency
The system must clearly indicate when it cannot answer because the content is outside the retrieved context. It must provide specific citations to the retrieved chunks used to generate an answer.

### IV. Reproducibility
All RAG pipeline steps (embedding, retrieval, API calls, schema, metadata) must be documented and traceable. The entire pipeline, including content ingestion and deployment, must be reproducible by users following the documentation.

### V. Security
No unsafe model actions, unrestricted tool execution, or hallucinations beyond retrieved text. Personally Identifiable Information (PII) must strictly NOT be stored.

### VI. Consistency
Chatbot behavior must remain aligned with the book’s technical definitions, modules, and terminology. The implementation must strictly adhere to the defined technology stack and Docusaurus integration patterns.

### VII. Knowledge Capture (PHR)
Every user interaction must be recorded in a Prompt History Record (PHR). Context is preserved to allow seamless handoffs.

## Operational Standards

### Technology Stack
- **RAG Orchestration**: OpenAI Agents / ChatKit SDKs.
- **Backend**: FastAPI server (container-deployable).
- **Database**: Neon Serverless Postgres (metadata + logs) + Qdrant Cloud (vector storage).
- **Frontend**: React/MDX components embedded in Docusaurus.

### Data & Retrieval
- **Vector Schema**: Must include file path, section, heading, and paragraph ID.
- **Ingestion**: Automated pipeline extracting MD/MDX content from Docusaurus to Qdrant/Neon.
- **Retrieval Logic**: Deterministic, prioritizing user-selected text, then book corpus embeddings.
- **Answering Rule**: If retrieval < threshold or irrelevant -> "Not enough information".

### User Experience
- **Interface**: Chatbot panel within the book.
- **Interaction**: Support text selection -> "Ask AI about this section".
- **Performance**: Response latency max 3 seconds under normal load.

## Governance

This constitution supersedes all other practices. Amendments require a pull request and version bump.

**Version**: 2.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07