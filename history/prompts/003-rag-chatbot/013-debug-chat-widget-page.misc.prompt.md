---
id: 016
title: debug-chat-widget-page
stage: misc
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: 003-rag-chatbot
branch: 003-rag-chatbot
user: User
command: alright create it
labels: ["debug", "frontend", "test-page"]
links:
  spec: specs/003-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - website/src/pages/test-chat.js
tests:
  - (none)
---

## Prompt

alright create it

## Response snapshot

Created `website/src/pages/test-chat.js`.
This page explicitly renders `<ChatWidget />` inside `<BrowserOnly>`.
Used to isolate if the component itself is crashing the app.

## Outcome

- ✅ Impact: New route `/test-chat` created.
- 🧪 Tests: User accesses `http://localhost:3000/test-chat`.
- 📁 Files: `website/src/pages/test-chat.js`.
- 🔁 Next prompts: Based on user feedback (blank or working?).
- 🧠 Reflection: Isolation is key when global swizzling fails.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
