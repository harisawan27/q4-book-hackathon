---
id: evaluation
title: Evaluation Criteria
sidebar_label: Evaluation
description: How your capstone will be graded.
---

# Evaluation Criteria

The capstone is graded out of **100 points**.

## Functional Requirements (60 points)

| Capability | Criteria | Points |
| :--- | :--- | :--- |
| **Command Parsing** | Robot correctly interprets 3 out of 3 distinct test commands. | 10 |
| **Navigation** | Robot reaches goal within 0.5m tolerance, no collisions. | 10 |
| **Perception** | Robot correctly bounds/segments the target object. | 10 |
| **Manipulation** | Robot successfully grasps and lifts object >10cm. | 20 |
| **System Integration** | The entire loop runs autonomously without manual intervention. | 10 |

## Technical Implementation (30 points)

-   **Code Quality (10)**: Modular ROS 2 nodes, proper use of Topics/Actions, Python/C++ best practices.
-   **Simulation Fidelity (10)**: Accurate physics (no floating objects), realistic sensor noise handling.
-   **Architecture (10)**: Proper separation of concerns (Planner vs Controller).

## Documentation & Presentation (10 points)

-   **Video Demo (5)**: Clear, edited video showing the robot's perspective and 3rd person view.
-   **README (5)**: Clear instructions on how to launch the simulation.

## Bonus Points (Up to +10)

-   **Sim-to-Real (+5)**: Deploying *any* part of the stack to a physical Jetson/Robot.
-   **Voice Response (+2)**: Robot speaks back to the user ("I am fetching the sponge now").
-   **Dynamic Replanning (+3)**: Robot recovers if the object is moved during the task.
