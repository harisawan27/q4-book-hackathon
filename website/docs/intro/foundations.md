---
id: foundations
title: Physical AI & Embodied Intelligence
sidebar_label: Physical AI
description: Core concepts of Physical AI and how they differ from traditional AI.
---

# Physical AI & Embodied Intelligence

## Weeks 1-2: Introduction to Physical AI

This section lays the groundwork for the transition from purely digital algorithms to embodied systems that must respect the laws of physics.

### Foundations of Physical AI and Embodied Intelligence
Physical AI refers to AI systems that interact directly with the physical world. Unlike "Digital AI" (like ChatGPT) that lives on servers, Physical AI is **embodied**—it is housed within a physical body (robot) that constrains and enables its actions.
*   **From digital AI to robots that understand physical laws:** We explore how latency, gravity, friction, and mechanical limits fundamentally change how we design AI algorithms.

### Overview of the Humanoid Robotics Landscape
Humanoid robots are the ultimate challenge in Physical AI. They are designed to operate in environments built for humans (stairs, doors, tools) but face significant stability and control challenges. We will examine current state-of-the-art platforms and the shift towards general-purpose humanoids.

### Sensor Systems
A robot's ability to perceive the world is the first step in the feedback loop. We cover the essential sensors that act as the robot's senses:
*   **LiDAR:** For precise distance mapping and SLAM.
*   **Cameras (RGB & Depth):** For visual recognition and spatial awareness.
*   **IMUs (Inertial Measurement Units):** The "inner ear" for balance and orientation.
*   **Force/Torque Sensors:** For tactile feedback and interaction control.

## The Core Loop
The fundamental cycle of any physical AI agent involves:
1.  **Perception**: Sensors --> State Estimation.
2.  **Reasoning**: State --> Action Plan (LLM/VLA).
3.  **Control**: Action Plan --> Motor Torques.
4.  **Actuation**: Motors move the robot --> World State changes.