---
id: "008"
title: "preview-website"
stage: "misc"
date: "2025-12-06"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "docusaurus-book"
branch: "main"
user: "user"
command: "preview-website"
labels: ["docusaurus", "preview", "server"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files: []
tests: []
---

# Prompt
run website so i can preview

# Response
Started the Docusaurus development server via `Start-Process npm -ArgumentList "start" -WorkingDirectory "website"`.

This launched a separate process to run the server. You should see the website open at http://localhost:3000 shortly.
