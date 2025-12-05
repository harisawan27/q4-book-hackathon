import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
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

export default sidebars;
