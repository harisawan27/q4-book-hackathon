---
id: specs
title: Hardware Specifications
sidebar_label: Hardware Specs
description: Required hardware for the lab and digital twin workstations.
---

# Hardware Specifications

To successfully complete the Capstone Project, the following hardware resources are required.

## Digital Twin Workstation

High-performance computing is needed for NVIDIA Isaac Sim and VLA inference.

-   **GPU**: NVIDIA RTX 4070 Ti or higher (12GB+ VRAM recommended).
-   **CPU**: Intel Core i7/i9 (12th Gen+) or AMD Ryzen 9.
-   **RAM**: 64GB DDR5 recommended (32GB Minimum).
-   **OS**: Ubuntu 22.04 LTS.

## Edge AI Compute

For onboard robot processing:

-   **Platform**: NVIDIA Jetson Orin Nano (Development Kit).
-   **Performance**: 40 TOPS.
-   **Memory**: 8GB.

## Robot Platform

The curriculum supports three tiers of physical hardware deployment.

### Tier 1: The Digital Humanoid (Simulation Only)
-   **Cost**: $0
-   **Hardware**: No robot required. All work done in NVIDIA Isaac Sim.
-   **Model**: Unitree H1 or G1 (USD assets provided).

### Tier 2: The Proxy Quadruped (Recommended for Labs)
-   **Cost**: ~$3,000
-   **Model**: **Unitree Go2 (Edu)** or **Xiaomi CyberDog 2**.
-   **Why**: Quadrupeds are mechanically simpler and more robust than bipeds but share the same "floating base" dynamics and perception stack. They are excellent proxies for learning locomotion and navigation.

### Tier 3: The Physical Humanoid (Research Labs)
-   **Cost**: $16,000 - $90,000+
-   **Model**: **Unitree G1** or **Fourier GR-1**.
-   **Why**: Full Sim-to-Real transfer of bipedal locomotion policies. Requires significant safety rigging and maintenance.