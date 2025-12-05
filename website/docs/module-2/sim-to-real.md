---
id: sim-to-real
title: Sim-to-Real Transfer
sidebar_label: Sim-to-Real
description: Bridging the gap between simulation and reality.
---

# Sim-to-Real Transfer

## The Reality Gap

A policy trained in simulation often fails in the real world because:
1.  **Physics Mismatch**: Friction coefficients are never perfect.
2.  **Sensor Noise**: Real cameras have blur and grain; sim cameras are perfect.
3.  **Latency**: Real actuators have delays.

## Strategies for Success

### 1. Domain Randomization

During training in Isaac Sim, we randomize:
-   **Visuals**: Change floor texture, light color, wall patterns.
-   **Physics**: Randomize robot mass by $\pm 5\%$, friction by $\pm 10\%$.
-   **Perturbations**: Push the robot randomly during walking.

If the policy survives this "hell," the real world just looks like another random variation.

### 2. System Identification (SysID)

Measure the real robot carefully to match the sim parameters.
-   Weigh every link.
-   Measure motor torque curves.

### 3. Action Latency Modeling

Intentionally delay the action in simulation by 1-2 frames (20-40ms) to match the real-world comms delay.

```python
# Example of action delay buffer in Python
class ActionBuffer:
    def __init__(self, latency_steps):
        self.buffer = collections.deque(maxlen=latency_steps)
    
    def get_action(self, current_action):
        self.buffer.append(current_action)
        return self.buffer[0] # Return the oldest action
```