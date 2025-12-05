<!--
SYNC IMPACT REPORT
Version change: 1.0.0 -> 1.1.0
Modified: Renamed project to "Docusaurus Book Project". Merged core SDD principles with user-provided book production principles.
Added sections: Verified Reproducibility, Accessibility & Clarity, Framework Alignment.
Removed sections: Test-First (Superseded by Verified Reproducibility for book context).
Templates requiring updates: None.
Follow-up: None.
-->
# Docusaurus Book Project Constitution

## Core Principles

### I. Spec-Driven Development (SDD)
All chapters and features start with a specification. We clarify requirements, outline structure, and define content blocks before writing. The spec file is the source of truth.

### II. Verified Reproducibility
All tutorials, code samples, and deployment steps MUST be tested and reproducible. Users (beginners to intermediate) must be able to execute every instruction without error. "Works on my machine" is not acceptable; it must work on Windows and macOS.

### III. Accessibility & Clarity
Use simple, direct language. Avoid unnecessary jargon. Explain *why* before showing *how*. Content is written for humans first, aiming for a consistent "beginner-to-intermediate" tone.

### IV. Framework Alignment (Docusaurus First)
Structure content according to Docusaurus best practices (intro, guides, tutorials, references). The book itself must build with zero warnings. Code examples must adhere to modern JS/TS standards.

### V. Authoritative Source Mandate
Agents MUST prioritize using CLI commands for information gathering. Do not invent APIs or Docusaurus configuration options; verify them against documentation or actual execution.

### VI. Knowledge Capture (PHR)
Every user interaction must be recorded in a Prompt History Record (PHR). Context is preserved to allow seamless handoffs.

## Operational Standards

- **Format**: Markdown source compatible with Docusaurus.
- **Visuals**: Provide screenshots or terminal snippets where helpful.
- **Workflow**: The book is produced using Spec-Kit Plus and the AI Agent (Gemini) as core tools.
- **Scope**: Minimum 6 chapters (Intro, Setup, Building, Writing, Deployment, Advanced).
- **Deliverable**: At least 1 complete working Docusaurus project included.

## Governance

This constitution supersedes all other practices. Amendments require a pull request and version bump.

**Version**: 1.1.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
