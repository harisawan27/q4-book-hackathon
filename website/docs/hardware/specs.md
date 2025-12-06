---
id: specs
title: Hardware Specifications
sidebar_label: Hardware Specs
description: Required hardware for the lab and digital twin workstations.
---

# Hardware Requirements

This course is technically demanding. It sits at the intersection of three heavy computational loads: **Physics Simulation** (Isaac Sim/Gazebo), **Visual Perception** (SLAM/Computer Vision), and **Generative AI** (LLMs/VLA).

## 1. The "Digital Twin" Workstation (Required per Student)
This is the most critical component. NVIDIA Isaac Sim is an Omniverse application that requires "RTX" (Ray Tracing) capabilities. Standard laptops (MacBooks or non-RTX Windows machines) will **not** work.

*   **GPU (The Bottleneck):** NVIDIA RTX 4070 Ti (12GB VRAM) or higher.
    *   *Why:* You need high VRAM to load the USD (Universal Scene Description) assets for the robot and environment, plus run the VLA models simultaneously.
    *   *Ideal:* RTX 3090 or 4090 (24GB VRAM) allows for smoother "Sim-to-Real" training.
*   **CPU:** Intel Core i7 (13th Gen+) or AMD Ryzen 9.
    *   *Why:* Physics calculations (Rigid Body Dynamics) in Gazebo/Isaac are CPU-intensive.
*   **RAM:** 64 GB DDR5.
    *   *Note:* 32 GB is the absolute minimum but will crash during complex scene rendering.
*   **OS:** Ubuntu 22.04 LTS.
    *   *Note:* While Isaac Sim runs on Windows, ROS 2 (Humble/Iron) is native to Linux. Dual-booting or dedicated Linux machines are mandatory for a friction-free experience.

## 2. The "Physical AI" Edge Kit
Since a full humanoid robot is expensive, students learn "Physical AI" by setting up the nervous system on a desk before deploying it to a robot.

*   **The Brain:** NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB).
    *   *Role:* The industry standard for embodied AI. Students deploy ROS 2 nodes here to understand resource constraints.
*   **The Eyes (Vision):** Intel RealSense D435i or D455.
    *   *Role:* Provides RGB (Color) and Depth (Distance) data. Essential for VSLAM.
*   **The Inner Ear (Balance):** Generic USB IMU (BNO055).
*   **Voice Interface:** USB Microphone/Speaker array (e.g., ReSpeaker) for "Voice-to-Action".

## 3. The Robot Lab
For the "Physical" part of the course, you have three tiers of options:

### Option A: The "Proxy" Approach (Recommended for Budget)
Use a quadruped or robotic arm as a proxy.
*   **Robot:** Unitree Go2 Edu (~$1,800 - $3,000).
*   **Pros:** Durable, excellent ROS 2 support.
*   **Cons:** Not a biped.

### Option B: The "Miniature Humanoid" Approach
Small, table-top humanoids.
*   **Robot:** Unitree G1 (~$16k) or Robotis OP3 (~$12k).
*   **Budget Alternative:** Hiwonder TonyPi Pro (~$600) - *Note: Limited AI capabilities.*

### Option C: The "Premium" Lab
*   **Robot:** Unitree G1 Humanoid.
*   **Why:** One of the few commercial humanoids with an open SDK for ROS 2 control.
