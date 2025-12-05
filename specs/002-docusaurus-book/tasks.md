---
description: "Task list template for feature implementation"
---

# Tasks: Docusaurus Technical Book

**Input**: Design documents from `specs/002-docusaurus-book/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Build validation and cross-platform checks are included as standard tasks.

**Organization**: Tasks are grouped by Docusaurus implementation phases, mapping to the Reader Journey (P1) and Workflow (P2) stories.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Docusaurus 3.x project and configure environment

- [x] T001 Initialize Docusaurus 3.x project with classic preset in `website/` root
- [x] T002 [P] Configure `docusaurus.config.ts` (title: "Physical AI & Humanoid Robotics", url, baseUrl)
- [x] T003 [P] Clean up default content (remove `blog/`, `docs/intro.md`)
- [x] T004 Install `docusaurus-lunr-search` for local search capability
- [x] T005 [P] Setup GitHub Actions workflow for deployment (`.github/workflows/deploy.yml`)

---

## Phase 2: Foundational (Information Architecture)

**Purpose**: Define the "Book" structure using sidebars and folders

**⚠️ CRITICAL**: Must match `data-model.md` exactly to support content ingestion

- [x] T006 Create folder structure in `website/docs/` (intro/, module-1/, module-2/, etc.)
- [x] T007 Configure `sidebars.ts` to implement the linear "bookSidebar" defined in data-model.md
- [x] T008 Create placeholder index files for all categories (e.g., `docs/module-1/index.md`) to prevent build errors
- [x] T009 [P] Update `src/pages/index.tsx` (Landing Page) to link to "Preface" (Start Reading)

**Checkpoint**: `npm run start` should show the empty book structure with correct navigation

---

## Phase 3: User Story 1 - Reader Journey (Priority: P1)

**Goal**: Readers can access all chapters (Robotics Content) in a logical order

**Independent Test**: Build completes successfully; Navigation flows linearly from Preface to Appendix

### Content Ingestion: Preface & Module 1 (ROS 2)
- [x] T010 [P] [US1] Create `docs/intro/index.md` (Preface)
- [x] T011 [P] [US1] Create `docs/intro/target-audience.md`
- [x] T012 [P] [US1] Create `docs/module-1/ros2-fundamentals.md`
- [x] T013 [P] [US1] Create `docs/module-1/nodes-and-topics.md`
- [x] T014 [P] [US1] Create `docs/module-1/setup-guide.md`

### Content Ingestion: Module 2 (Digital Twin)
- [x] T015 [P] [US1] Create `docs/module-2/gazebo-unity.md`
- [x] T016 [P] [US1] Create `docs/module-2/urdf-modeling.md`
- [x] T017 [P] [US1] Create `docs/module-2/sim-to-real.md`

### Content Ingestion: Module 3 (Isaac)
- [x] T018 [P] [US1] Create `docs/module-3/nvidia-isaac.md`
- [x] T019 [P] [US1] Create `docs/module-3/perception-pipeline.md`
- [x] T020 [P] [US1] Create `docs/module-3/training.md`

### Content Ingestion: Module 4 (VLA)
- [x] T021 [P] [US1] Create `docs/module-4/vla-foundations.md`
- [x] T022 [P] [US1] Create `docs/module-4/cognitive-planning.md`
- [x] T023 [P] [US1] Create `docs/module-4/llm-integration.md`

### Content Ingestion: Capstone & Lab
- [x] T024 [P] [US1] Create `docs/capstone/requirements.md`
- [x] T025 [P] [US1] Create `docs/capstone/weekly-breakdown.md`
- [x] T026 [P] [US1] Create `docs/hardware/specs.md`
- [x] T027 [P] [US1] Create `docs/lab/architecture.md`

### Content Ingestion: Appendices
- [x] T028 [P] [US1] Create `docs/appendices/deployment.md`
- [x] T029 [P] [US1] Create `docs/appendices/glossary.md`

**Checkpoint**: All content pages exist (even if draft). Sidebar navigation works.

---

## Phase 4: User Story 2 - Workflow Adoption (Priority: P2)

**Goal**: Showcase the AI-driven workflow within the book itself

- [x] T030 [P] [US2] Update `docs/appendices/deployment.md` with specific Spec-Kit Plus / Agent workflow details used in this project
- [x] T031 [P] [US2] Verify `docs/module-1/setup-guide.md` instructions work on Windows
- [x] T032 [P] [US2] Verify `docs/module-1/setup-guide.md` instructions work on macOS

---

## Phase 5: Polish & Deployment

**Purpose**: Final validation and publishing

- [x] T033 Run `npm run build` locally to verify static generation
- [x] T034 [P] Add diagram images (placeholders or real) to `static/img/` and reference in docs
- [x] T035 Perform final link check (manual or plugin)
- [x] T036 Trigger GitHub Pages deployment (push to main)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on T001. Blocks content creation.
- **User Story 1 (Phase 3)**: Depends on Foundational (folder structure must exist).
- **User Story 2 (Phase 4)**: Can run parallel with Phase 3 content creation, but verification tasks (T031/T032) require content.

### Implementation Strategy

1. **Skeleton First**: Complete Phase 1 & 2 to get a working "Empty Book".
2. **Content Fill**: Execute Phase 3 tasks in parallel blocks (Module 1, Module 2...).
3. **Verify & Ship**: Run Phase 5 tasks to publish the artifacts.