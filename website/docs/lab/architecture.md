---
id: architecture
title: Lab Architecture
sidebar_label: Lab Architecture
description: Setup for On-premise vs Cloud-native robotics labs.
---

# Lab Architecture

The Physical AI curriculum can be deployed in two primary configurations: On-Premise or Hybrid Cloud.

## Option A: On-Premise (Recommended)

Best for low-latency control and local simulation.

-   **Student Station**: 1 High-end Workstation per team.
-   **Robot Network**: Dedicated Wi-Fi 6 Router (Isolated).
-   **Sim-to-Real**: Direct Ethernet connection for initial deployment.

## Option B: Hybrid Cloud

Best for remote access to simulation resources.

-   **Simulation Server**: Cloud instances (AWS g5.xlarge or Azure NVads A10) running Isaac Sim headless.
-   **Client**: Thin client laptops for students accessing sim via WebRTC / Omniverse Streaming.
-   **Deployment**: Over-the-air (OTA) updates to robots in the physical lab.

## Architecture Diagram

*(Placeholder for Network Topology Diagram)*