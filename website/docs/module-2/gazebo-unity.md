---
id: gazebo-unity
title: The Digital Twin
sidebar_label: Digital Twin
description: Building physics-accurate simulations.
---

# The Digital Twin

## Why Simulate?

Training a humanoid robot in the real world is:
1.  **Dangerous**: A 50kg robot falling can hurt people or itself.
2.  **Slow**: Real-time cannot be sped up.
3.  **Expensive**: Parts break.

A **Digital Twin** allows us to train safely, faster than real-time, and at zero marginal cost.

## The Simulation Landscape

### Gazebo (Classic & Ignition)
The standard simulator for ROS.
-   **Pros**: Tight ROS integration, huge community, lightweight.
-   **Cons**: Visual fidelity is low (looks like a game from 2005), contact physics can be unstable for bipedal walking.

### Unity / Unreal
Game engines repurposed for robotics.
-   **Pros**: Incredible visuals, VR support.
-   **Cons**: Integrating with ROS requires bridges (ROS# or TCP connectors), physics engines (PhysX) prioritize stability over accuracy.

### NVIDIA Isaac Sim (Our Choice)
Built on Omniverse.
-   **Pros**: Photorealistic ray-tracing (crucial for vision models), GPU-accelerated physics (PhysX 5), native ROS 2 bridge.
-   **Cons**: Requires heavy GPU hardware.

## URDF: The Robot DNA

To simulate a robot, we must describe it in **URDF (Unified Robot Description Format)**. This XML file defines:
-   **Links**: The rigid parts (thigh, shin, foot).
-   **Joints**: How they connect (hip hinge, knee hinge).
-   **Inertia**: Mass and distribution of weight.
-   **Visuals**: 3D meshes (.dae, .stl) for how it looks.
-   **Collision**: Simplified geometry for physics calculations.