---
description: "Task list template for feature implementation"
---

# Tasks: Humanoid Robotics Capstone Book

**Input**: Design documents from `specs/001-humanoid-robotics-capstone/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md
**Tests**: Build validation and cross-platform checks included.

**Organization**: Tasks are grouped by implementation phase, then by user story to ensure modular delivery.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1 (Curriculum), US2 (Student Capstone)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Docusaurus 3.x project with classic preset in `website/` root
- [x] T002 [P] Configure `docusaurus.config.ts` (title, url, baseUrl, sidebar config)
- [x] T003 [P] Install `docusaurus-lunr-search` for offline search capability
- [x] T004 [P] Setup GitHub Actions workflow `.github/workflows/deploy.yml`
- [x] T005 Create sidebar structure in `website/sidebars.ts` matching `data-model.md`
- [x] T006 Create folder structure in `website/docs/` per `data-model.md`
- [x] T007 [P] Add placeholder diagram images to `website/static/img/diagrams/`

**Checkpoint**: Docusaurus skeleton is running with correct navigation structure.

---

## Phase 2: Foundational (Information Architecture)

**Purpose**: Create the shell for all modules to support User Stories

- [x] T008 Create `website/docs/intro/index.md` (Preface)
- [x] T009 [P] Create `website/docs/intro/foundations.md` (Physical AI concepts)
- [x] T010 [P] Create `website/docs/appendices/glossary.md` (Terminology)
- [x] T011 [P] Create `website/docs/appendices/deployment.md` (Deployment guide)
- [x] T012 [P] Create `website/docs/hardware/specs.md` (Hardware requirements shell)
- [x] T013 [P] Create `website/docs/lab/architecture.md` (Lab setup shell)

**Checkpoint**: All top-level sections exist; navigation works; build passes.

---

## Phase 3: User Story 1 - Curriculum Review (Priority: P1) 🎯 MVP

**Goal**: Deliver comprehensive module specifications for academic approval.

**Independent Test**: Reviewer can see learning outcomes, weekly breakdown, and resource needs.

### Implementation for US1

- [x] T014 [US1] Implement Learning Outcomes in `website/docs/intro/index.md`
- [x] T015 [P] [US1] Create `website/docs/capstone/weekly-breakdown.md` with 13-week schedule
- [x] T016 [P] [US1] Update `website/docs/hardware/specs.md` with Workstation & Robot tiers
- [x] T017 [P] [US1] Implement Module 1 content in `website/docs/module-1/ros2-fundamentals.md`
- [x] T018 [P] [US1] Implement Module 2 content in `website/docs/module-2/gazebo-unity.md`
- [x] T019 [P] [US1] Implement Module 3 content in `website/docs/module-3/nvidia-isaac.md`
- [x] T020 [P] [US1] Implement Module 4 content in `website/docs/module-4/vla-foundations.md`

**Checkpoint**: Full curriculum details are visible.

---

## Phase 4: User Story 2 - Student Capstone Planning (Priority: P2)

**Goal**: Provide clear project requirements and technical guides for students.

**Independent Test**: Student can identify the 5 key capabilities and has technical guides to start.

### Implementation for US2

- [x] T021 [P] [US2] Create `website/docs/capstone/project-brief.md` with 5 key capabilities
- [x] T022 [P] [US2] Create `website/docs/capstone/evaluation.md` with success criteria
- [x] T023 [P] [US2] Create `website/docs/module-1/nodes-and-topics.md` (Technical Guide)
- [x] T024 [P] [US2] Create `website/docs/module-1/setup-guide.md` (Technical Guide)
- [x] T025 [P] [US2] Create `website/docs/module-2/urdf-modeling.md` (Technical Guide)
- [x] T026 [P] [US2] Create `website/docs/module-2/sim-to-real.md` (Technical Guide)
- [x] T027 [P] [US2] Create `website/docs/module-3/perception-pipeline.md` (Technical Guide)
- [x] T028 [P] [US2] Create `website/docs/module-3/training.md` (Technical Guide)
- [x] T029 [P] [US2] Create `website/docs/module-4/cognitive-planning.md` (Technical Guide)
- [x] T030 [P] [US2] Create `website/docs/module-4/llm-integration.md` (Technical Guide)

**Checkpoint**: Technical depth added; students have a complete project brief.

---

## Phase 5: Polish & Deployment

**Purpose**: Final validation and publishing

- [x] T031 [P] Verify all internal links and sidebar navigation
- [x] T032 [P] Add Intro/Target Audience content to `website/docs/intro/target-audience.md`
- [x] T033 Run `npm run build` locally to verify static generation
- [x] T034 Push to `main` branch to trigger GitHub Pages deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Story 1 (Phase 3)**: Depends on Foundational. Delivers Academic Review artifacts.
- **User Story 2 (Phase 4)**: Depends on Foundational. Can run parallel to US1 tasks if different authors working.
- **Polish (Phase 5)**: Final step.

### User Story Dependencies

- **US1 (Curriculum)**: Focuses on "What" and "Why" (Outcomes, Schedule, Specs).
- **US2 (Student)**: Focuses on "How" (Technical guides, Setup, Code).

### Parallel Opportunities

- All content creation tasks (T017-T030) are parallelizable once the folder structure (T006) exists.
- Hardware specs (T016) and Weekly Breakdown (T015) are independent.

## Implementation Strategy

1. **Skeleton First**: Complete Phase 1 & 2 to get a working "Book Shell".
2. **Curriculum View**: Complete Phase 3 to satisfy the Academic Reviewer (P1).
3. **Student View**: Complete Phase 4 to satisfy the Student/Technical requirements (P2).
4. **Ship**: Build and Deploy.
