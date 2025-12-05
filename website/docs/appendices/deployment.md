---
id: deployment
title: Deployment Guide
sidebar_label: Deployment
description: How to build and deploy this documentation book.
---

# Deployment Guide

This book is built using **Docusaurus 3** and deployed via **GitHub Pages**.

## Prerequisites

-   Node.js 18+ (LTS)
-   Git

## Local Development

To run the book locally:

1.  Clone the repository.
2.  Navigate to the `website/` directory.
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Start the dev server:
    ```bash
    npm start
    ```

The site will be available at `http://localhost:3000`.

## Building for Production

To generate static files:

```bash
npm run build
```

The output will be in the `build/` directory.

## Deployment Workflow

This repository uses GitHub Actions to automatically deploy changes to the `gh-pages` branch.

1.  Commit changes to the `main` branch.
2.  Push to GitHub.
3.  The `.github/workflows/deploy.yml` workflow will trigger.
4.  Wait for the action to complete.
5.  View the live site at the repository's GitHub Pages URL.
