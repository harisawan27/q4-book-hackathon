---
id: project-brief
title: Capstone Project Brief
sidebar_label: Project Brief
description: The official requirement specification for the final project.
---

# Capstone Project: The Autonomous Humanoid

## Overview
**The Autonomous Humanoid** is the culmination of the Physical AI quarter. It is a final project where a simulated robot receives a voice command, plans a path, navigates obstacles, identifies an object using computer vision, and manipulates it.

## Mission
Design and simulate a humanoid robot capable of performing a multi-step service task in a home environment by responding to a verbal command.

## The Challenge
The project integrates the three heavy computational loads of Physical AI:
1.  **Physics Simulation:** Running a stable humanoid simulation in Isaac Sim.
2.  **Visual Perception:** Using SLAM and Computer Vision to understand the world.
3.  **Generative AI:** Using VLA/LLMs to understand intent and plan actions.

## Scenario
**User Command:** "I spilled some water, can you help?"
**Robot Response:**
1.  **Hear:** Transcribe audio to text.
2.  **Think:** Planner decomposes task: `[Find Sponge, Pick Sponge, Go to Spill, Wipe]`.
3.  **Act:**
    *   Navigate to the kitchen (avoiding the cat).
    *   Detect the sponge on the counter.
    *   Grasp the sponge.
    *   Move to the spill location and execute a wiping motion.

## Assessment Criteria
*   **ROS 2 Package Development:** Clean, modular code structure.
*   **Gazebo/Isaac Implementation:** Stable simulation with accurate physics.
*   **Perception Pipeline:** Accurate object detection and mapping.
*   **Conversational AI:** Successful intent parsing and voice feedback.