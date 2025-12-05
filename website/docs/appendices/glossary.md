---
id: glossary
title: Glossary of Terms
sidebar_label: Glossary
description: Definitions for key terms in ROS 2, Isaac Sim, and Robotics.
---

# Glossary

## Robotics & ROS 2

-   **Node**: A process that performs computation. Nodes communicate with each other using Topics, Services, and Actions.
-   **Topic**: A named bus over which nodes exchange messages. Pub/Sub model.
-   **URDF (Unified Robot Description Format)**: An XML format for representing a robot model.
-   **TF (Transform)**: A system for keeping track of multiple coordinate frames over time.

## Simulation & AI

-   **Digital Twin**: A virtual representation of a physical object or system that spans its lifecycle, updated from real-time data, and uses simulation, machine learning and reasoning to help decision-making.
-   **Isaac Sim**: NVIDIA's robotics simulation platform based on Omniverse (USD).
-   **Sim-to-Real**: The process of transferring policies learned in simulation to a physical robot.
-   **Domain Randomization**: A technique to improve Sim-to-Real transfer by varying simulation parameters (lighting, friction, mass) during training.

## Foundation Models

-   **VLA (Vision-Language-Action)**: A model trained on internet-scale data to take text/image inputs and output low-level robot actions.
-   **Zero-shot Learning**: The ability of a model to perform a task it wasn't explicitly trained on.