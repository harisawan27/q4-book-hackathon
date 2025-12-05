---
id: urdf-modeling
title: URDF Modeling Guide
sidebar_label: URDF Modeling
description: How to write URDF files for custom robots.
---

# URDF Modeling Guide

## Basic Structure

A URDF file is an XML file.

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.6 0.4 0.2"/>
      </geometry>
    </visual>
  </link>

  <!-- Wheel Link -->
  <link name="right_wheel">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.2"/>
      </geometry>
    </visual>
  </link>

  <!-- Joint connecting them -->
  <joint name="base_to_right_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.225 0" rpy="1.57 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

</robot>
```

## Key Tips for Humanoids

1.  **Inertia Matrices**: Gazebo will explode if you don't provide accurate inertia (`<inertial>`) tags. Use meshlab or SolidWorks to calculate these.
2.  **Collision Meshes**: Don't use your high-poly visual mesh for collisions. Use simple primitives (boxes, cylinders) or a low-poly convex hull to speed up simulation.
3.  **Xacro**: For complex robots, use Xacro (XML Macros) to avoid repeating code for left/right arms and legs.