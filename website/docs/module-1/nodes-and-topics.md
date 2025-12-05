---
id: nodes-and-topics
title: "Guide: Nodes & Topics"
sidebar_label: Nodes & Topics
description: Hands-on guide to writing ROS 2 nodes.
---

# Technical Guide: Writing Your First Node

## Prerequisites
-   ROS 2 Humble installed.
-   Colcon build tool ready.

## 1. Create a Package

In your workspace `src` folder:

```bash
ros2 pkg create --build-type ament_python my_first_pkg --dependencies rclpy
```

## 2. Writing a Publisher

Create `my_first_pkg/simple_publisher.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
```

## 3. Running the Node

Build and source:
```bash
colcon build
source install/setup.bash
ros2 run my_first_pkg simple_publisher
```

## 4. Inspecting Topics

Open a new terminal:
```bash
ros2 topic list
ros2 topic echo /topic
```