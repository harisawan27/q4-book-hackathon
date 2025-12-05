# Information Architecture: Humanoid Robotics Capstone Book

**Feature**: `001-humanoid-robotics-capstone`

## Sidebar Structure (`sidebars.ts`)

The book is organized linearly to support the 13-week curriculum.

```typescript
export default {
  capstoneSidebar: [
    {
      type: 'category',
      label: 'Preface',
      items: [
        'intro/index',           // Welcome & Purpose
        'intro/target-audience', // Who this is for
        'intro/foundations'      // Physical AI & Embodied Intelligence
      ],
    },
    {
      type: 'category',
      label: 'Module 1: Robotic Nervous System',
      items: [
        'module-1/ros2-fundamentals',
        'module-1/nodes-and-topics',
        'module-1/setup-guide'
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin',
      items: [
        'module-2/gazebo-unity',
        'module-2/urdf-modeling',
        'module-2/sim-to-real'
      ],
    },
    {
      type: 'category',
      label: 'Module 3: AI-Robot Brain',
      items: [
        'module-3/nvidia-isaac',
        'module-3/perception-pipeline',
        'module-3/training'
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action',
      items: [
        'module-4/vla-foundations',
        'module-4/cognitive-planning',
        'module-4/llm-integration'
      ],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      items: [
        'capstone/project-brief', // Was "requirements"
        'capstone/weekly-breakdown',
        'capstone/evaluation'
      ],
    },
    {
      type: 'category',
      label: 'Lab & Hardware',
      items: [
        'hardware/specs',         // Workstations, Kits, Robots
        'lab/architecture'        // On-prem vs Cloud
      ],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendices/deployment',
        'appendices/glossary'
      ],
    },
  ],
};
```

## Content Entities

### 1. Module Page
- **Frontmatter**: `id`, `title`, `sidebar_label`, `description`.
- **Structure**: Learning Outcomes -> Theoretical Concepts -> Practical Exercise -> Quiz/Check.
- **Code Blocks**: ROS 2 CLI, Python snippets, XML/URDF.

### 2. Hardware Spec
- **Components**: Digital Twin Workstation, Edge AI (Jetson), Sensors, Actuators.
- **Attributes**: Minimum Specs, Recommended Specs, Justification.

### 3. Capstone Project Definition
- **Sections**: Problem Statement, Required Capabilities (Instruction, Planning, Navigation, Detection, Manipulation), Evaluation Criteria.
- **Artifacts**: Simulation Video, Codebase, System Report.

## Diagrams (Visual Assets)

- **ROS 2 Node Graph**: `static/img/diagrams/ros2-node-graph.png`
- **Digital Twin Pipeline**: `static/img/diagrams/digital-twin-pipeline.png` (Gazebo -> Isaac -> Unity)
- **Hardware Architecture**: `static/img/diagrams/hardware-arch.png` (Jetson + Sensors)
- **Sim-to-Real Workflow**: `static/img/diagrams/sim-to-real.png`
