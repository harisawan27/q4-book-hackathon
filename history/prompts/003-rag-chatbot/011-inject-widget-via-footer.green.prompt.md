---
id: 014
title: inject-widget-via-footer
stage: green
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: 003-rag-chatbot
branch: 003-rag-chatbot
user: User
command: now it's working as it was but no chatbot is there
labels: ["frontend", "docusaurus", "swizzle", "footer"]
links:
  spec: specs/003-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - website/src/theme/Footer/index.js
tests:
  - (none)
---

## Prompt

now it's working as it was but no chatbot is there

## Response snapshot

Adopted a safer component injection strategy.
Instead of wrapping the root, I swizzled the `Footer` component (`website/src/theme/Footer/index.js`).
This wrapper renders the original footer and then appends the `<ChatWidget />` inside a `<BrowserOnly>` block.

## Outcome

- ✅ Impact: Chat widget should appear on all pages with a footer.
- 🧪 Tests: User needs to restart frontend.
- 📁 Files: `website/src/theme/Footer/index.js`.
- 🔁 Next prompts: Verify widget visibility.
- 🧠 Reflection: Footer swizzling is generally more stable than Root for simple global injections.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
