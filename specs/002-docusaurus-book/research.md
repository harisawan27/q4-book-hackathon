# Research & Decisions: Docusaurus Technical Book

**Date**: 2025-12-05

## Decisions

### 1. Framework Choice
- **Decision**: Docusaurus 3.x (Latest)
- **Rationale**: Native support for sidebar-driven documentation (perfect for books), React-based for extensibility, MDX support for interactive components, and proven scalability.
- **Alternatives Considered**:
  - *MkDocs (Material)*: Good, but less flexible for React components and custom layouts compared to Docusaurus.
  - *GitBook*: Proprietary/Paid limits; Docusaurus is open source.

### 2. Hosting Platform
- **Decision**: GitHub Pages
- **Rationale**: Free, integrated with the repo (CI/CD via Actions), supports custom domains, standard for open source docs.
- **Alternatives Considered**:
  - *Vercel/Netlify*: Good options, but GitHub Pages keeps everything in one ecosystem for this specific "book" project requirement.

### 3. Content Structure (Architecture)
- **Decision**: Module-based folders with explicit `sidebars.ts` configuration.
- **Rationale**: Ensures strict ordering of chapters (Introduction -> Setup -> etc.) which is critical for a book format, unlike a "knowledge base" graph.

### 4. Search Provider
- **Decision**: Local Search (e.g., `docusaurus-lunr-search` or standard Algolia if free tier available). *Refinement: Start with `docusaurus-lunr-search` or generic local search plugin for zero-config offline capability.*
- **Rationale**: Keeps the project self-contained without requiring external API keys for setup (easier for readers to reproduce).

### 5. Robotics/Sim Content Integration
- **Decision**: The "content" of the book will be the Robotics material defined in the spec input, but structured into the Docusaurus folders.
- **Rationale**: The spec provided detailed robotics content (ROS 2, Isaac, etc.) which serves as the *subject matter* for the book chapters.

## Validation Strategy

- **Build**: `npm run build` must pass.
- **Links**: CI job to check broken links.
- **Reproducibility**: "Clean install" test on a fresh Windows/Mac environment.
