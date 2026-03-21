# CST8509 Lab 3: Gazebo Simulation — Gazebo 仿真环境

**Author:** Peng Wang
**Student Number:** 041107730
**Course:** CST8509 - Reinforcement Learning
**Date:** March 21, 2026

---

## Overview — 概述

This lab covers deploying a Gazebo 11 simulation environment for the iRobot Create 3 robot, including installing the simulator, the AWS Small House world, and adding a virtual camera for future reinforcement learning training.

本实验涵盖为 iRobot Create 3 机器人部署 Gazebo 11 仿真环境，包括安装模拟器、AWS 小房子世界，以及添加虚拟摄像头用于后续强化学习训练。

---

## Step 1: Install Ubuntu Desktop GUI — 安装 Ubuntu Desktop GUI

```bash
sudo apt install ubuntu-desktop
```

**Explanation:**

- Install the Ubuntu Desktop GUI to enable graphical display of Gazebo and RViz. — 安装 Ubuntu Desktop GUI 以启用 Gazebo 和 RViz 的图形显示。
- This step is only needed if you're running Ubuntu Server instead of Desktop. — 仅在运行 Ubuntu Server 而非 Desktop 时需要此步骤。
- The loaner laptop requires a GUI to visualize the simulation environment. — loaner laptop 需要 GUI 来可视化仿真环境。

---

## Step 2: Install ROS 2 Humble Desktop — 安装 ROS 2 Humble Desktop

```bash
sudo apt install ros-humble-desktop
```

**Explanation:**

- Install the desktop version of ROS 2 Humble which includes visualization tools like RViz. — 安装 ROS 2 Humble 桌面版，包含 RViz 等可视化工具。
- This is a prerequisite for the Create 3 simulator. — 这是 Create 3 模拟器的前置依赖。
- The desktop version adds GUI tools on top of the base ROS 2 installation from CST8504. — 桌面版在 CST8504 的基础 ROS 2 安装之上添加了 GUI 工具。

---

## Step 3: Install Classic Gazebo 11 — 安装 Classic Gazebo 11

```bash
curl -sSL http://get.gazebosim.org | sh
# Or alternatively: sudo apt install gazebo
```

**Explanation:**

- Install Classic Gazebo version 11 (not Ignition Gazebo) as the simulation platform. — 安装 Classic Gazebo 版本 11（不是 Ignition Gazebo）作为仿真平台。
- Classic Gazebo 11 is compatible with the AWS Small House world that we need. — Classic Gazebo 11 与我们需要的 AWS 小房子世界兼容。
- There are two versions of Gazebo: Classic (v11) and Ignition/New Gazebo (Fortress, Harmonic). We use Classic. — Gazebo 有两个版本：Classic（v11）和 Ignition/New Gazebo（Fortress、Harmonic）。我们使用 Classic。

---

## Step 4: Clone and Build Create 3 Simulator — 克隆并构建 Create 3 模拟器

```bash
# Create workspace and clone the repository
# 创建工作空间并克隆仓库
mkdir -p ~/create3_ws/src
cd ~/create3_ws/src
git clone https://github.com/iRobotEducation/create3_sim.git
cd create3_sim
git checkout humble

# Set environment variable (works for both Classic and Ignition)
# 设置环境变量（Classic 和 Ignition 通用）
export IGNITION_VERSION=fortress

# Install dependencies using rosdep
# 使用 rosdep 安装依赖
cd ~/create3_ws
rosdep install --from-paths src -y --ignore-src

# Build the workspace
# 构建工作空间
colcon build --symlink-install
```

**Explanation:**

- Clone the iRobot Create 3 simulator from GitHub and switch to the humble branch for ROS 2 Humble compatibility. — 从 GitHub 克隆 iRobot Create 3 模拟器并切换到 humble 分支以兼容 ROS 2 Humble。
- The `export IGNITION_VERSION=fortress` line is required even when using Classic Gazebo. — 即使使用 Classic Gazebo 也需要 `export IGNITION_VERSION=fortress`。
- `rosdep install` resolves and installs all ROS package dependencies. — `rosdep install` 解析并安装所有 ROS 包依赖。
- `colcon build --symlink-install` builds the workspace with symlinks so file changes take effect immediately. — `colcon build --symlink-install` 使用符号链接构建工作空间，使文件更改立即生效。

---

## Step 5: Install and Build AWS Small House World — 安装并构建 AWS 小房子世界

```bash
# Follow instructions from the create3_sim README
# to download and build the AWS small house world
# 按照 create3_sim README 中的说明下载并构建 AWS 小房子世界
```

**Explanation:**

- The AWS Small House is a pre-built Gazebo world that provides a realistic indoor environment for robot simulation. — AWS 小房子是一个预构建的 Gazebo 世界，为机器人仿真提供真实的室内环境。
- It includes furniture, walls, and rooms for the Create 3 to navigate through. — 包含家具、墙壁和房间供 Create 3 导航。
- This environment will be used in Assignment 2 for RL training with the simulated robot. — 此环境将在 Assignment 2 中用于模拟机器人的 RL 训练。

---

## Step 6: Run Simulator with AWS Small House — 运行带 AWS 小房子的模拟器

```bash
# Source the workspace
# 加载工作空间
source ~/create3_ws/install/setup.bash

# Launch the simulator with AWS Small House
# 启动带 AWS 小房子的模拟器
ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py
```

**Explanation:**

- Source the workspace setup to make the built packages available to ROS 2. — 加载工作空间设置以使构建的包可用于 ROS 2。
- The launch command starts both Gazebo (simulation) and RViz (visualization) simultaneously. — 启动命令同时启动 Gazebo（仿真）和 RViz（可视化）。
- Be patient during launch — the GUI may show "not responding" for a few minutes, which is normal. — 启动期间需要耐心——GUI 可能会显示"not responding"几分钟，这是正常的。
- If RViz shows the Create3 as white with errors, try Ctrl+C and relaunch. — 如果 RViz 中 Create3 显示为白色且有错误，尝试 Ctrl+C 后重新启动。

---

## Step 7: Create camera.urdf.xacro — 创建 camera.urdf.xacro

### 7.1 Modify create3.urdf.xacro — 修改 create3.urdf.xacro

Add the following line to include the camera file in `create3.urdf.xacro`:

```xml
<xacro:include filename="$(find irobot_create_description)/urdf/camera.urdf.xacro" />
```

**Explanation:**

- The create3.urdf.xacro file contains the robot description with all its parts. — create3.urdf.xacro 文件包含机器人描述及其所有部件。
- We add an include line similar to the wheel_with_wheeldrop entry to attach our camera. — 我们添加类似 wheel_with_wheeldrop 的引用行来连接摄像头。
- The `$(find ...)` syntax resolves the package path at build time. — `$(find ...)` 语法在构建时解析包路径。

### 7.2 Create camera.urdf.xacro — 创建 camera.urdf.xacro

The camera URDF/Xacro file consists of three parts:

**Part 1: Camera Joint and Link (关节和链接)**

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" >

    <joint name="camera_joint" type="fixed">
        <parent link="base_link"/>
        <child link="camera_link"/>
        <origin xyz="0 0 0.2" rpy="0 0 0"/>
    </joint>

    <link name="camera_link">
        <visual>
            <geometry>
                <box size="0.010 0.03 0.03"/>
            </geometry>
            <material name="red"/>
        </visual>
    </link>

    <material name="red">
        <color rgba="1 0 0 1"/>
    </material>
```

**Explanation:**

- A fixed joint (`camera_joint`) attaches the camera to the robot's `base_link`, positioned 0.2m above. — 固定关节（`camera_joint`）将摄像头连接到机器人的 `base_link`，位于上方 0.2m 处。
- The camera is represented as a small red box (10mm × 30mm × 30mm) for visual identification. — 摄像头表示为一个红色小方块（10mm × 30mm × 30mm）便于视觉识别。
- URDF uses `link` for physical objects and `joint` for connections between links. — URDF 使用 `link` 表示物理对象，`joint` 表示链接之间的连接。

**Part 2: Optical Link (光学链接)**

```xml
    <joint name="camera_optical_joint" type="fixed">
        <parent link="camera_link"/>
        <child link="camera_link_optical"/>
        <origin xyz="0 0 0" rpy="${-pi/2} 0 ${-pi/2}"/>
    </joint>

    <link name="camera_link_optical"></link>
```

**Explanation:**

- ROS uses robot convention (x-forward, y-left, z-up) while cameras use optical convention (x-right, y-down, z-forward). — ROS 使用机器人约定（x 前, y 左, z 上），而摄像头使用光学约定（x 右, y 下, z 前）。
- The optical link applies rotation transforms (`-π/2` on x and z axes) to convert between coordinate frames. — 光学链接应用旋转变换（x 和 z 轴上 `-π/2`）在坐标系之间转换。
- Without this conversion, camera images would appear rotated incorrectly. — 没有此转换，摄像头图像会出现错误的旋转。

**Part 3: Gazebo Camera Plugin (Gazebo 摄像头插件)**

```xml
    <gazebo reference="camera_link">
        <material name="red"/>
        <sensor name="camera" type="camera">
            <pose> 0 0 0 0 0 0 </pose>
            <visualize>true</visualize>
            <update_rate>10</update_rate>
            <camera name="head">
                <horizontal_fov>1.089</horizontal_fov>
                <image>
                    <format>R8G8B8</format>
                    <width>640</width>
                    <height>480</height>
                </image>
                <clip>
                    <near>0.05</near>
                    <far>8.0</far>
                </clip>
            </camera>

            <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
                <ros>
                    <namespace>custom_ns</namespace>
                    <remapping>image_raw:=custom_img</remapping>
                    <remapping>camera_info:=custom_info</remapping>
                </ros>
                <camera_name>camera1</camera_name>
                <frame_name>camera_link_optical</frame_name>
                <hack_baseline>0.7</hack_baseline>
            </plugin>
        </sensor>
    </gazebo>

</robot>
```

**Explanation:**

- The `libgazebo_ros_camera.so` plugin bridges Gazebo camera simulation with ROS 2 topics. — `libgazebo_ros_camera.so` 插件将 Gazebo 摄像头仿真与 ROS 2 topics 桥接。
- Camera publishes 640×480 RGB images at 10 Hz to topic `/custom_ns/camera1/custom_img`. — 摄像头以 10 Hz 频率向 topic `/custom_ns/camera1/custom_img` 发布 640×480 RGB 图像。
- The horizontal FOV of 1.089 radians (≈62.4°) simulates a typical laptop webcam field of view. — 1.089 弧度（≈62.4°）的水平视场角模拟典型笔记本摄像头的视野。
- Near/far clip planes (0.05m–8.0m) define the visible range of the camera. — 近/远裁剪面（0.05m–8.0m）定义摄像头的可见范围。

---

## Step 8: Build and Verify Camera — 构建和验证摄像头

```bash
# Build only the description package (faster rebuild)
# 仅构建描述包（更快的重建）
cd ~/create3_ws
colcon build --symlink-install --packages-select irobot_create_description

# IMPORTANT: Source the Gazebo 11 setup for camera plugin
# 重要：加载 Gazebo 11 设置以启用摄像头插件
source /usr/share/gazebo-11/setup.sh

# Optional: Add to ~/.bashrc for automatic loading
# 可选：添加到 ~/.bashrc 以自动加载
echo source /usr/share/gazebo-11/setup.sh >> ~/.bashrc

# Relaunch the simulator
# 重新启动模拟器
source ~/create3_ws/install/setup.bash
ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py

# Verify camera topics are present
# 验证摄像头 topics 是否存在
ros2 topic list
```

**Explanation:**

- Use `--packages-select` to rebuild only the changed package, saving build time. — 使用 `--packages-select` 仅重建更改的包，节省构建时间。
- The `source /usr/share/gazebo-11/setup.sh` command is CRITICAL — without it, camera topics will not appear. — `source /usr/share/gazebo-11/setup.sh` 命令至关重要——不执行此步骤，摄像头 topics 不会出现。
- After relaunching, `ros2 topic list` should show `/custom_ns/camera1/custom_img` and `/custom_ns/camera1/custom_info`. — 重新启动后，`ros2 topic list` 应显示 `/custom_ns/camera1/custom_img` 和 `/custom_ns/camera1/custom_info`。

---

## Step 9: View Camera in RViz — 在 RViz 中查看摄像头

```bash
# In RViz GUI:
# 1. Click "Add" button
# 2. Select "Image" display type
# 3. Set topic to: /custom_ns/camera1/custom_img
# 在 RViz GUI 中：
# 1. 点击"Add"按钮
# 2. 选择"Image"显示类型
# 3. 将 topic 设置为：/custom_ns/camera1/custom_img

# Undock the Create 3 to navigate
# 解除 Create 3 停靠以开始导航
ros2 action send_goal /undock irobot_create_msgs/action/Undock {}

# Drive the Create 3 (example: rotate)
# 驱动 Create 3（示例：旋转）
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.2}, angular: {z: 0.5}}'
```

**Explanation:**

- RViz's Image display subscribes to the camera topic and shows real-time video from the simulated camera. — RViz 的 Image 显示订阅摄像头 topic 并显示模拟摄像头的实时视频。
- The undock action releases the Create 3 from its charging dock so it can move freely. — 解除停靠操作使 Create 3 从充电底座释放，可以自由移动。
- Navigate the robot around the AWS Small House while monitoring the camera feed in RViz. — 在 RViz 中监控摄像头画面的同时，在 AWS 小房子中导航机器人。

---

## Submission — 提交

### File Submitted — 提交的文件

| File | Description |
|------|-------------|
| `camera.urdf.xacro` | Virtual camera URDF/Xacro definition for Create 3 simulation — Create 3 仿真的虚拟摄像头 URDF/Xacro 定义 |

### Demonstration Checklist — 演示检查清单

- [ ] Running simulation with camera added to Create 3 — 运行带摄像头的 Create 3 仿真
- [ ] Undock Create 3 and drive it around the AWS Small House — 解除 Create 3 停靠并在 AWS 小房子中驾驶
- [ ] Camera image simulated and projected in Gazebo GUI — Gazebo GUI 中模拟和投影的摄像头图像
- [ ] Camera image monitored in RViz — RViz 中监控的摄像头图像
