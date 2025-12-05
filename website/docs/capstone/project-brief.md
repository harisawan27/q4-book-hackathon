---
id: project-brief
title: Capstone Project Brief
sidebar_label: Project Brief
description: The official requirement specification for the final project.
---

# Capstone Project: The Service Humanoid

## Mission Statement

**"Design and simulate a humanoid robot capable of performing a multi-step service task in a home environment by responding to a verbal command."**

You will not build physical hardware. You will build the **Brain** and **Nervous System** of a robot in a high-fidelity Digital Twin.

## The 5 Key Capabilities

Your robot must demonstrate the following capabilities in a single continuous simulation run:

### 1. Instruction Reception (Audio/Text)
-   **Input**: The user types or speaks a command like "I spilled some water, can you help?"
-   **Requirement**: The system must transcribe (if audio) and parse the intent.

### 2. Cognitive Planning (The "Brain")
-   **Process**: An LLM (local Llama 3 or API-based GPT-4) must decompose the high-level intent into executable steps.
-   **Example**: "Help with spill" $\rightarrow$ `[Find Sponge, Pick Sponge, Go to Spill, Wipe]`.

### 3. Navigation (Nav2)
-   **Action**: The robot must move from its start position to the target objects without colliding with furniture.
-   **Tech**: ROS 2 Nav2 stack with SLAM or pre-mapped environment.

### 4. Detection (Perception)
-   **Action**: Identify the target object (sponge, apple, cup) in the scene.
-   **Tech**: YOLO or Isaac Sim Ground Truth segmentation.

### 5. Manipulation (MoveIt)
-   **Action**: Use the arm to grasp the object and manipulate it.
-   **Requirement**: Successful grasp and transport without dropping.

## Deliverables

1.  **Codebase**: A GitHub repository containing your ROS 2 packages and Isaac Sim USD stages.
2.  **Demo Video**: A 2-minute screen recording of the simulation performing the task.
3.  **System Report**: A 5-page architecture document explaining your node graph and AI pipeline.
