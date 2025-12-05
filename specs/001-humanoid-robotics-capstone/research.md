# Research & Decisions: Humanoid Robotics Capstone

**Feature**: `001-humanoid-robotics-capstone`
**Date**: 2025-12-05

## Research Approach

- **Parallel Research**: Research technical details (ROS 2 commands, Isaac Sim setup) concurrently with content drafting.
- **Source Verification**: All technical claims MUST be sourced from official documentation (ROS 2 Humble, NVIDIA Isaac Sim 2023+, Unity Robotics).
- **Code Generation**: Use AI assistance (Claude/Gemini) to generate boilerplate code, but verify execution.
- **Source Log**: Maintain references for all diagrams and architecture statements.

## Key Decisions

### 1. Book Structure
- **Decision**: **Module-based Structure** (Intro → Modules 1-4 → Capstone).
- **Rationale**: Aligns with the 13-week semester flow and pedagogical progression.
- **Alternatives**: Technology-based structure (grouping by "ROS", "Python", "Sim") was rejected because it fragments the learning experience and makes weekly planning harder.

### 2. Primary Simulator
- **Decision**: **NVIDIA Isaac Sim**.
- **Rationale**: Essential for Vision-Language-Action (VLA) models, photorealistic synthetic data generation, and modern GPU-accelerated physics.
- **Alternatives**: Gazebo-only. Rejected because it lacks the high-fidelity rendering needed for vision-based AI training, though it is used in Module 1/2 for foundations.

### 3. Robotics Hardware Tier
- **Decision**: **Unitree Go2 (Proxy)** and **Humanoid (G1/OP3) as Target**.
- **Rationale**: Unitree Go2 is accessible and affordable for labs, serving as a valid proxy for quadrupedal locomotion and perception. The curriculum targets "Humanoid Robotics", so the simulation focus remains on humanoids, while physical labs may use proxies if full humanoids are cost-prohibitive.
- **Status**: Documented as "Recommended Proxy" vs "Ideal Deployment".

### 4. Hosting Platform
- **Decision**: **GitHub Pages**.
- **Rationale**: Simple, transparent, zero-cost, and integrates natively with the repository's CI/CD.
- **Alternatives**: Netlify/Vercel. Rejected as unnecessary complexity for a static documentation site.

### 5. Tooling
- **Decision**: **Spec-Kit Plus + Docusaurus**.
- **Rationale**: Spec-Kit Plus ensures structured SDD. Docusaurus provides native sidebar categories, MDX support for interactive components, and a polished reading experience compared to MkDocs.
