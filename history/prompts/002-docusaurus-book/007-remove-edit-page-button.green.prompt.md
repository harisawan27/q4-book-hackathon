---
id: "007"
title: "remove-edit-page-button"
stage: "green"
date: "2025-12-06"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "docusaurus-book"
branch: "main"
user: "user"
command: "remove-edit-page-button"
labels: ["configuration", "docusaurus", "ui"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "website/docusaurus.config.ts"
tests: []
---

# Prompt
there is a button at bottom of every chapter or page in book "edit this page", remove it

# Response
Removed the `editUrl` property from `website/docusaurus.config.ts`. This disables the "Edit this page" button on documentation pages.
