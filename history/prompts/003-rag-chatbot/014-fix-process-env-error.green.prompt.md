---
id: 017
title: fix-process-env-error
stage: green
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: 003-rag-chatbot
branch: 003-rag-chatbot
user: User
command: that page logs errror "Uncaught runtime errors: ERROR process is not defined...
labels: ["bugfix", "frontend", "webpack", "env-vars"]
links:
  spec: specs/003-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - website/src/components/ChatWidget/api.ts
tests:
  - (none)
---

## Prompt

that page logs errror "Uncaught runtime errors: ERROR process is not defined...

## Response snapshot

The error `ReferenceError: process is not defined` occurs because Docusaurus (Webpack 5+) does not polyfill `process` in the browser by default.
I fixed this in `api.ts` by adding a safety check: `typeof process !== 'undefined'`.

## Outcome

- ✅ Impact: The ChatWidget should now load without crashing the site.
- 🧪 Tests: User needs to refresh the test page.
- 📁 Files: `website/src/components/ChatWidget/api.ts`.
- 🔁 Next prompts: If test page works, re-apply Footer injection.
- 🧠 Reflection: Modern bundlers are strict. Always use safe access for env vars or Docusaurus specific hooks.

## Evaluation notes (flywheel)

- Failure modes observed: `process is not defined` runtime error.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
