<!--
SYNC IMPACT REPORT
Version change: 2.0.0 -> 3.0.0
Modified: Project renamed to "User Authentication, Personalization, and Urdu Translation System for the Physical AI & Humanoid Robotics Docusaurus Book"
  - Updated all principles to align with authentication, personalization, and translation requirements
  - Accuracy principle now includes personalization accuracy and translation fidelity
  - Transparency expanded to cover personalization logic and translation source
  - Security updated with privacy-first data handling and authentication requirements
  - Consistency updated for cross-chapter UX and Docusaurus styling
Added sections:
  - Principle VIII: Privacy-First Data Handling
  - Principle IX: Authentication & Authorization
  - User Background Data standards
  - Content Transformation standards (Personalization and Translation)
Removed sections: None (all existing RAG principles preserved and extended)
Templates requiring updates:
  - ✅ plan-template.md: Constitution Check section compatible (uses dynamic principle references)
  - ✅ spec-template.md: Compatible (technology-agnostic template)
  - ✅ tasks-template.md: Compatible (uses dynamic phase structure)
Follow-up: None
-->
# User Authentication, Personalization, and Urdu Translation System for the Physical AI & Humanoid Robotics Docusaurus Book Constitution

## Core Principles

### I. Spec-Driven Development (SDD)
All features start with a specification. We clarify requirements, outline structure, and define content blocks before writing code. The spec file is the source of truth.

### II. Privacy-First Data Handling
All user data (background, preferences, session state) MUST be handled with privacy as the primary concern. PII MUST NOT be exposed in logs, analytics, or error messages. User background data MUST be stored securely with strict access boundaries. Data collection MUST be limited to what is necessary for personalization functionality.

### III. Accuracy
All chatbot responses and personalized content MUST rely strictly on the book's original content. Personalization MUST adapt presentation and complexity without introducing factual distortions. Translations MUST maintain technical correctness and meaning fidelity. Hallucinations or answers derived from outside the retrieved context are unacceptable. Zero hallucination in translated or personalized content is mandatory.

### IV. Transparency
The system MUST clearly indicate:
- When it cannot answer because the content is outside the retrieved context
- Specific citations to retrieved chunks used to generate an answer
- When content has been personalized (showing the "Personalize Content" button state)
- When content has been translated (showing the "Translate to Urdu" button state)
Personalization rules MUST follow deterministic, documented transformation logic.

### V. Reproducibility
All RAG pipeline steps (embedding, retrieval, API calls, schema, metadata) MUST be documented and traceable. Personalization transformations MUST be reversible and reproducible. Translation endpoints MUST be verified and deterministic. The entire pipeline, including content ingestion and deployment, MUST be reproducible by users following the documentation.

### VI. Security
No unsafe model actions, unrestricted tool execution, or hallucinations beyond retrieved text. Authentication MUST use Better-Auth following official best practices. No unauthorized user can access personalization or translation features. All user-triggered transformations MUST be client-visible but not persisted unless explicitly saved. Secrets and tokens MUST NOT be hardcoded; use `.env` and documentation.

### VII. Consistency
Chatbot behavior MUST remain aligned with the book's technical definitions, modules, and terminology. The implementation MUST strictly adhere to the defined technology stack and Docusaurus integration patterns. UI buttons MUST follow Docusaurus styling and not break MDX rendering. User experience MUST be clear and consistent across all chapters.

### VIII. Authentication & Authorization
Authentication provider: Better-Auth (mandatory). Sign-up flow MUST collect user background data (software skills, hardware skills, experience level). Logged-in users MUST be able to:
- Personalize chapter content through a "Personalize Content" button
- Translate chapter content to Urdu through a "Translate to Urdu" button
No chapter content may be modified unless the user is authenticated.

### IX. Knowledge Capture (PHR)
Every user interaction MUST be recorded in a Prompt History Record (PHR). Context is preserved to allow seamless handoffs. PHRs are routed to appropriate subdirectories under `history/prompts/`.

## Operational Standards

### Technology Stack
- **Authentication**: Better-Auth (mandatory provider)
- **RAG Orchestration**: OpenAI Agents / ChatKit SDKs
- **Backend**: FastAPI server (container-deployable)
- **Database**: Neon Serverless Postgres (metadata + logs + user background data) + Qdrant Cloud (vector storage)
- **Frontend**: React/MDX components embedded in Docusaurus
- **Translation**: Verified LLM translation endpoint (backend-only, no client-side LLM)

### User Background Data
- **Collection**: Signup flow collects software skills, hardware skills, experience level
- **Storage**: Stored securely in Neon Postgres with strict access boundaries
- **Usage**: Used for dynamic content personalization based on user expertise
- **Access**: Retrievable only by authenticated user and personalization service

### Content Transformation

#### Personalization
- Logic MUST be modular and reversible
- Transformations adapt complexity based on user background
- Original content integrity MUST be preserved
- Personalization produces accurate, level-adapted text without distortion
- Deterministic, documented transformation logic required

#### Urdu Translation
- Translation MUST rely only on backend APIs, not client-only LLM use
- Translations MUST maintain meaning, technical correctness, and safety
- Verified LLM translation endpoint required
- Translations remain faithful, technically correct, and readable

### Data & Retrieval
- **Vector Schema**: MUST include file path, section, heading, and paragraph ID
- **Ingestion**: Automated pipeline extracting MD/MDX content from Docusaurus to Qdrant/Neon
- **Retrieval Logic**: Deterministic, prioritizing user-selected text, then book corpus embeddings
- **Answering Rule**: If retrieval < threshold or irrelevant -> "Not enough information"

### User Experience
- **Interface**: Chatbot panel within the book + chapter action buttons
- **Chapter Buttons**: Every chapter shows two buttons for logged-in users:
  - "Personalize Content" - adapts content to user background
  - "Translate to Urdu" - translates content to Urdu
- **Interaction**: Support text selection -> "Ask AI about this section"
- **Performance**: Response latency max 3 seconds under normal load
- **Transformation State**: All user-triggered transformations are client-visible but not persisted unless explicitly saved

## Governance

This constitution supersedes all other practices. Amendments require a pull request and version bump.

**Version**: 3.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-12
