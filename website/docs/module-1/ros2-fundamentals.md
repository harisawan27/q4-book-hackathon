---
id: ros2-fundamentals
title: ROS 2 Fundamentals
sidebar_label: ROS 2 Basics
description: Introduction to the Robot Operating System 2.
---

# ROS 2 Fundamentals

## The "Nervous System" of Robotics

If a robot's chassis is the body and the AI is the brain, then **ROS 2 (Robot Operating System 2)** is the nervous system. It provides the standard way for all the different parts (camera, motor driver, path planner) to talk to each other.

## Why ROS 2?

1.  **Real-time Support**: Unlike ROS 1, ROS 2 is built on DDS (Data Distribution Service), allowing for real-time constraints essential for safety-critical humanoid balancing.
2.  **Python & C++**: Write high-performance code in C++ and rapid logic in Python, mixing them seamlessly.
3.  **Ecosystem**: Thousands of pre-built packages for Navigation (Nav2), Manipulation (MoveIt 2), and Perception.

## Core Concepts

### Nodes
A **Node** is the fundamental unit of computation. In a humanoid, you might have:
-   `camera_node`: Reads images from the head.
-   `balance_node`: Calculates torque to keep upright.
-   `face_detect_node`: Finds humans in the image.

### Topics (Pub/Sub)
Nodes communicate via **Topics**. This is a many-to-many broadcasting channel.
-   `camera_node` **Publishes** to `/image_raw`.
-   `face_detect_node` **Subscribes** to `/image_raw`.

```mermaid
graph LR
    A[Camera Node] -- /image_raw --> B[Face Detect Node]
    B -- /face_location --> C[Head Controller Node]
```

## Practical Exercise
*(Detailed in Technical Guide)*

You will install ROS 2 Humble and run the `turtlesim` demo to visualize nodes and topics interacting.