---
id: vla-foundations
title: Vision-Language-Action (VLA)
sidebar_label: VLA Models
description: The frontier of Embodied AI.
---

# Vision-Language-Action (VLA) Models

## The "ChatGPT Moment" for Robotics

Traditional robotics required hard-coding every behavior:
*`if (object == 'apple') then (pick_up)`*

**VLA Models** (like Google's RT-2 or generic GPT-4o integrations) allow us to control robots with natural language and common sense.

## How VLA Works

1.  **Input**:
    -   **Vision**: Image from robot's camera.
    -   **Language**: Instruction "Put the empty soda can in the recycling bin."
2.  **Reasoning**:
    -   The model identifies "soda can" and "recycling bin" in the image.
    -   It understands "empty" implies trash.
    -   It retrieves general knowledge: "Soda cans go in recycling, not trash."
3.  **Action Tokenization**:
    -   The output isn't text; it's **action tokens**. These translate directly to end-effector coordinates (x, y, z, gripper_open).

## Cognitive Planning Pipeline

For our humanoid capstone, we use a modular approach:

1.  **Planner (LLM)**: High-level reasoning.
    -   *Input*: "Clean the table."
    -   *Output*: Sequence ["Find apple", "Pick apple", "Place in bowl"].
2.  **Policy (VLA/Diffusion)**: Mid-level skill execution.
    -   *Input*: "Pick apple" + Image.
    -   *Output*: Trajectory for the arm.
3.  **Controller (ROS 2)**: Low-level safety.
    -   *Input*: Trajectory.
    -   *Output*: Motor currents, ensuring no collisions.