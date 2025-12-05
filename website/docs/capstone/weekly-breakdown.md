---
id: weekly-breakdown
title: 13-Week Course Schedule
sidebar_label: Weekly Schedule
description: Week-by-week breakdown of the Physical AI curriculum.
---

# 13-Week Course Schedule

This schedule assumes a standard semester pace with 2 lectures and 1 lab per week.

## Part 1: The Nervous System (Weeks 1-4)

### Week 1: Foundations of Physical AI
-   **Lecture**: Embodied Intelligence, The Perception-Action Loop.
-   **Lab**: Setting up the Development Environment (Ubuntu, Docker, VS Code).

### Week 2: ROS 2 Basics
-   **Lecture**: Nodes, Topics, and Messages. The Pub/Sub architecture.
-   **Lab**: Writing your first Python Node. "Hello Robot".

### Week 3: Advanced ROS 2 Concepts
-   **Lecture**: Services, Actions, and Parameters. QoS (Quality of Service).
-   **Lab**: Creating a closed-loop control system for a simulated joint.

### Week 4: Coordinate Frames & TF2
-   **Lecture**: Rigid Body Dynamics, Quaternions, TF2 library.
-   **Lab**: Visualizing robot states in RViz.

## Part 2: The Digital Twin (Weeks 5-7)

### Week 5: URDF & Simulation
-   **Lecture**: Unified Robot Description Format. Inertial properties.
-   **Lab**: Building a custom URDF for a 2-DOF arm.

### Week 6: Physics Engines (Gazebo vs Isaac)
-   **Lecture**: Contact physics, friction models, time-stepping.
-   **Lab**: Spawning the robot in Gazebo Classic.

### Week 7: NVIDIA Isaac Sim
-   **Lecture**: USD (Universal Scene Description), Omniverse, Photorealism.
-   **Lab**: Importing URDF into Isaac Sim and adding sensors.

## Part 3: The Brain (Weeks 8-10)

### Week 8: Perception Pipelines
-   **Lecture**: CNNs for Object Detection (YOLO). Depth estimation.
-   **Lab**: Integrating a camera feed from Isaac Sim to a ROS 2 Topic.

### Week 9: Reinforcement Learning
-   **Lecture**: RL Basics, PPO, Reward shaping.
-   **Lab**: Training a robot to walk (or balance) using Isaac Gym.

### Week 10: Vision-Language-Action (VLA)
-   **Lecture**: Transformers in Robotics. RT-1, RT-2, GPT-4o.
-   **Lab**: Zero-shot object navigation using VLM prompts.

## Part 4: The Capstone (Weeks 11-13)

### Week 11: Capstone Sprint 1 - Integration
-   **Focus**: Connecting Perception (Isaac) to Actuation (ROS 2).
-   **Milestone**: Robot responds to basic teleoperation and avoids obstacles.

### Week 12: Capstone Sprint 2 - Cognitive Layer
-   **Focus**: Integrating the LLM planner.
-   **Milestone**: Robot executes "Go to the kitchen and find the apple".

### Week 13: Final Demo & Sim-to-Real
-   **Focus**: Polishing and Documentation. Optional Sim-to-Real deployment.
-   **Milestone**: Final Video Presentation and Code Submission.