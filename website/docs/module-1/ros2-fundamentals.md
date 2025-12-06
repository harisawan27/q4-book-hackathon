---
id: ros2-fundamentals
title: ROS 2 Fundamentals
sidebar_label: ROS 2 Fundamentals
description: The Robotic Nervous System.
---

# Module 1: The Robotic Nervous System (ROS 2)

**Focus:** Middleware for robot control.  
**Weeks 3-5: ROS 2 Fundamentals**

## Overview
ROS 2 (Robot Operating System 2) acts as the central nervous system for modern robots. It provides the communications infrastructure that allows different parts of the robot (sensors, actuators, AI models) to talk to each other in real-time.

## Core Concepts
### ROS 2 Architecture
Understanding the underlying DDS (Data Distribution Service) middleware that powers ROS 2's real-time capabilities.

### Nodes, Topics, and Services
*   **Nodes:** The fundamental processing units. Each node performs a specific task (e.g., reading a camera, controlling a motor).
*   **Topics:** The "blood vessels" of the system. Nodes publish data to topics and subscribe to them to receive data (Asynchronous communication).
*   **Services:** A request/response pattern for synchronous communication (e.g., "Turn on the light" -> "Done").
*   **Actions:** For long-running tasks that need feedback (e.g., "Navigate to point B").

## Building ROS 2 Packages
### Python Agents (`rclpy`)
We focus on bridging Python-based AI agents to ROS controllers. You will learn how to write efficient ROS 2 nodes using Python (`rclpy`) to interface with deep learning frameworks like PyTorch or TensorFlow.

### Launch Files and Parameter Management
*   **Launch Files:** Managing complex robot startups with dozens of nodes using Python-based launch files.
*   **Parameters:** dynamic configuration of node behavior without recompilation.

## URDF for Humanoids
While detailed modeling happens in Module 2, we introduce the **Unified Robot Description Format (URDF)** here. You will learn how to define the kinematic tree of a humanoid robot—joints, links, and limits—so ROS knows what the robot looks like.
