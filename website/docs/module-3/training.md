---
id: training
title: Reinforcement Learning Training
sidebar_label: RL Training
description: Training policies with Isaac Gym.
---

# Reinforcement Learning Training

## Why RL?

Classical control (PID, MPC) works great for known dynamics. Walking on uneven terrain with a humanoid involves contact discontinuities that are hard to model. RL allows the robot to "learn to walk" by trial and error.

## The Setup: OmniIsaacGymEnvs

NVIDIA provides a repository of pre-built environments.

1.  **Clone**: `git clone https://github.com/NVIDIA-Omniverse/OmniIsaacGymEnvs`
2.  **Config**: Edit `task/Humanoid.yaml`.

## Reward Function

The "magic" is in the reward function.

$$
R = R_{pos} + R_{upright} + R_{control} - C_{impact}
$$

-   $R_{pos}$: Reward for moving forward velocity.
-   $R_{upright}$: Reward for keeping the head above the waist.
-   $R_{control}$: Penalty for using too much energy (torque).
-   $C_{impact}$: Penalty for knees hitting the ground.

## Training Loop

Run the training script:

```bash
python scripts/rlgames_train.py task=Humanoid headless=True
```

You will see an FPS of 10,000+ because thousands of robots are simulating on the GPU.

## Policy Export

Once trained (reward converges), export the policy to ONNX:

```bash
python scripts/rlgames_train.py task=Humanoid test=True checkpoint=runs/Humanoid/nn/Humanoid.pth export=True
```

This `.onnx` file can now be loaded into a standard ROS 2 node for inference on the Jetson.