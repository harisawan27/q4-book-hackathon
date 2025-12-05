---
id: foundations
title: Physical AI & Embodied Intelligence
sidebar_label: Physical AI
description: Core concepts of Physical AI and how they differ from traditional AI.
---

# Physical AI & Embodied Intelligence

## What is Physical AI?

**Physical AI** refers to AI systems that interact directly with the physical world. Unlike "Digital AI" (like ChatGPT or image generators) that lives on servers and processes data, Physical AI must handle the unpredictability, physics, and constraints of reality.

### Key Characteristics

1.  **Embodiment**: The intelligence is housed within a physical body (robot) that constrains and enables its actions.
2.  **Interaction**: The system learns by interacting with the environment, not just by observing static datasets.
3.  **Real-time Constraints**: Decisions must be made within milliseconds to ensure stability and safety.

## The Rise of Humanoid Robotics

Humanoid robots represent the ultimate challenge in Physical AI. They are designed to operate in environments built for humans (stairs, doors, tools) but face significant stability and control challenges.

### Why Now?

-   **Compute**: GPUs (like Jetson Orin) are now powerful enough to run neural networks at the edge.
-   **Simulation**: Simulators (Isaac Sim) allow training robots in "gyms" for millions of hours before physical deployment.
-   **Foundation Models**: VLA (Vision-Language-Action) models allow robots to understand semantic instructions ("Pick up the red apple") without hard-coded rules.

## The Feedback Loop

The core loop of any physical AI agent is:

1.  **Perception**: Sensors (Cameras, LiDAR, IMU) $\rightarrow$ State Estimation.
2.  **Reasoning**: State $\rightarrow$ Action Plan (LLM/VLA).
3.  **Control**: Action Plan $\rightarrow$ Motor Torques (Low-level control).
4.  **Actuation**: Motors move the robot $\rightarrow$ World State changes.
