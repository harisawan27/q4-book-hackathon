---
id: setup-guide
title: Setup Guide
sidebar_label: Setup Guide
description: Installing ROS 2 and VS Code.
---

# Setup Guide

## Operating System

We strictly recommend **Ubuntu 22.04 LTS**.
-   **Windows Users**: Use WSL2 (Windows Subsystem for Linux).
-   **Mac Users**: Use a Docker Container (native ROS 2 on macOS is experimental).

## 1. Installing ROS 2 Humble

Set locale:
```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Add repository:
```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
```

Install:
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install ros-humble-desktop
```

## 2. Environment Setup

Add this to your `~/.bashrc`:
```bash
source /opt/ros/humble/setup.bash
```

## 3. VS Code Extensions

Install these extensions:
-   **Python** (Microsoft)
-   **C/C++** (Microsoft)
-   **ROS** (Microsoft) - *Essential for debugging*