---
id: 004
title: Add Authentication, Personalization, and Urdu Translation
stage: constitution
date: 2025-12-12
surface: agent
model: claude-opus-4-5-20251101
feature: user-personalization
branch: 003-rag-chatbot
user: harisawan27
command: /sp.constitution
labels: ["authentication", "personalization", "translation", "better-auth", "urdu"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Project: User Authentication, Personalization, and Urdu Translation System for the Physical AI & Humanoid Robotics Docusaurus Book

Core principles:

Privacy-first handling of user data

Clear, consistent user experience across all chapters

Personalization that preserves technical accuracy

Zero hallucination in translated or personalized content

Smooth integration with existing Docusaurus build, RAG chatbot, and backend infrastructure

Key standards:

Authentication must use Better-Auth following official best practices

Signup flow must collect user background data (software skills, hardware skills, experience level)

All background data must be stored securely with strict access boundaries

Logged-in users must be able to:
• Personalize chapter content through a "Personalize Content" button
• Translate chapter content to Urdu through a "Translate to Urdu" button

Personalization rules must follow deterministic, documented transformation logic

Urdu translation must use a verified LLM translation endpoint

Translations must maintain meaning, technical correctness, and safety

No chapter content may be modified unless the user is authenticated

Constraints:

Authentication provider: Better-Auth (mandatory)

Storage: Existing Neon Postgres (extend schema if needed)

Personalization logic must be modular and reversible

Translation must rely only on backend APIs, not client-only LLM use

All user-triggered transformations must be client-visible but not persisted unless explicitly saved

UI buttons must follow Docusaurus styling and not break MDX rendering

Success criteria:

Sign-up and sign-in flow fully working through Better-Auth

User background successfully stored, retrievable, and used for dynamic personalization

Every chapter shows two buttons for logged-in users:

Personalize Content

Translate to Urdu

Personalization produces accurate, level-adapted text without distortion

Urdu translations remain faithful, technically correct, and readable

No unauthorized user can access personalization

## Response snapshot

Updated the project constitution from v2.0.0 to v3.0.0 with major changes:

1. **Renamed project** to reflect new scope: "User Authentication, Personalization, and Urdu Translation System for the Physical AI & Humanoid Robotics Docusaurus Book"

2. **Added new principles**:
   - Principle II: Privacy-First Data Handling (PII protection, secure storage, minimal data collection)
   - Principle VIII: Authentication & Authorization (Better-Auth mandatory, user background collection, button access control)

3. **Enhanced existing principles**:
   - Accuracy: Now covers personalization accuracy and translation fidelity
   - Transparency: Expanded to cover transformation states (personalization/translation indicators)
   - Security: Updated with authentication requirements and transformation visibility rules
   - Consistency: Updated for cross-chapter UX and Docusaurus styling requirements

4. **Added operational standards**:
   - User Background Data section (collection, storage, usage, access)
   - Content Transformation standards (Personalization and Urdu Translation subsections)
   - Technology Stack updated with Better-Auth and Translation endpoint

5. **Templates validated**: All existing templates (plan, spec, tasks) remain compatible.

## Outcome

- ✅ Impact: MAJOR version bump (2.0.0 → 3.0.0) - fundamental scope expansion
- 🧪 Tests: N/A (constitution update)
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: `/sp.specify` to create feature spec for authentication and personalization
- 🧠 Reflection: Constitution successfully expanded to accommodate user-facing features while preserving RAG chatbot integrity

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation PASS - no unresolved placeholders, version matches report, dates in ISO format
- Prompt variant (if applicable): Standard constitution update
- Next experiment (smallest change to try): Consider splitting into separate features (auth, personalization, translation) during spec phase
