---
id: 012
title: fix-blank-page-ssr
stage: green
date: 2025-12-07
surface: agent
model: gemini-2.0-flash-exp
feature: 003-rag-chatbot
branch: 003-rag-chatbot
user: User
command: the website is not showing after following instructions. just a black plan page
labels: ["bugfix", "frontend", "ssr", "browser-only"]
links:
  spec: specs/003-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - website/src/theme/Root.js
tests:
  - (none)
---

## Prompt

the website is not showing after following instructions. just a black plan page

## Response snapshot

Diagnosed the "blank page" as a Server-Side Rendering (SSR) issue common in Docusaurus when using browser-specific APIs (like `window`) in global components.
Wrapped `<ChatWidget />` in `<BrowserOnly>` in `website/src/theme/Root.js` to ensure it only renders on the client.

## Outcome

- ✅ Impact: Website should load correctly now, with the widget appearing after hydration.
- 🧪 Tests: User needs to refresh the page.
- 📁 Files: `website/src/theme/Root.js` updated.
- 🔁 Next prompts: Confirmation of fix.
- 🧠 Reflection: Should have used `BrowserOnly` by default for any component interacting with `window` in Docusaurus.

## Evaluation notes (flywheel)

- Failure modes observed: Blank page (SSR crash).
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
