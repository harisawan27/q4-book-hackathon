# Information Architecture (Data Model): Docusaurus Book

**Purpose**: Define the structure of the book's content (sidebar) and file organization.

## Sidebar Structure (`sidebars.ts`)

The sidebar will be strictly ordered to guide the reader linearly, like a book.

```typescript
export default {
  bookSidebar: [
    {
      type: 'category',
      label: 'Preface',
      collapsible: false,
      items: ['intro/index', 'intro/target-audience'],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System',
      items: [
        'module-1/ros2-fundamentals',
        'module-1/nodes-and-topics',
        'module-1/setup-guide',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin',
      items: [
        'module-2/gazebo-unity',
        'module-2/urdf-modeling',
        'module-2/sim-to-real',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: AI-Robot Brain',
      items: [
        'module-3/nvidia-isaac',
        'module-3/perception-pipeline',
        'module-3/training',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action',
      items: [
        'module-4/vla-foundations',
        'module-4/cognitive-planning',
        'module-4/llm-integration',
      ],
    },
    {
      type: 'category',
      label: 'Capstone & Lab',
      items: [
        'capstone/requirements',
        'capstone/weekly-breakdown',
        'hardware/specs',
        'lab/architecture',
      ],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendices/deployment',
        'appendices/glossary',
      ],
    },
  ],
};
```

## File System Layout (`docs/`)

```text
docs/
├── intro/
│   ├── index.md (Preface)
│   └── target-audience.md
├── module-1/
│   ├── ros2-fundamentals.md
│   ├── nodes-and-topics.md
│   └── setup-guide.md
├── module-2/
│   ├── gazebo-unity.md
│   ├── urdf-modeling.md
│   └── sim-to-real.md
├── module-3/
│   ├── nvidia-isaac.md
│   ├── perception-pipeline.md
│   └── training.md
├── module-4/
│   ├── vla-foundations.md
│   ├── cognitive-planning.md
│   └── llm-integration.md
├── capstone/
│   ├── requirements.md
│   └── weekly-breakdown.md
├── hardware/
│   └── specs.md
├── lab/
│   └── architecture.md
└── appendices/
    ├── deployment.md
    └── glossary.md
```

## Frontmatter Contract

Every markdown file MUST have:

```yaml
---
id: <unique-kebab-case-id>
title: <Human Readable Title>
description: <SEO description for meta tags>
sidebar_label: <Short Title for Sidebar>
---
```
