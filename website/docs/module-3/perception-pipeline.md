---
id: perception-pipeline
title: Perception Pipeline
sidebar_label: Perception Pipeline
description: Detecting objects with Isaac Sim and ROS 2.
---

# Perception Pipeline

## Architecture

We use a modular perception stack:

1.  **Input**: RGB-D images from RealSense D435i (Simulated or Real).
2.  **Processing**: YOLOv8 (You Only Look Once) for 2D bounding boxes.
3.  **Depth Fusion**: Combining 2D box with Depth map to get 3D coordinates $(x, y, z)$.
4.  **Output**: TF2 Transform broadcast of the object.

## Step 1: Publishing Images from Isaac

In Isaac Sim Action Graph:
-   Add `ROS2 Camera Helper`.
-   Set Topic Name: `/camera/color/image_raw`.
-   Set Type: `rgb`.

## Step 2: YOLO Node

```python
from ultralytics import YOLO
import cv2
from cv_bridge import CvBridge

class YoloNode(Node):
    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, '/camera/color/image_raw', self.callback, 10)

    def callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        results = self.model(cv_image)
        
        for result in results:
            boxes = result.boxes
            # ... publish detection ...
```

## Step 3: 3D Projection

Given pixel $(u, v)$ and depth $d$, and camera intrinsics $(f_x, f_y, c_x, c_y)$:

$$
x = \frac{(u - c_x) \cdot d}{f_x}
$$
$$
y = \frac{(v - c_y) \cdot d}{f_y}
$$
$$
z = d
$$

This gives us the position of the object in the Camera Frame. We then use TF2 to transform it to the `base_link` frame.