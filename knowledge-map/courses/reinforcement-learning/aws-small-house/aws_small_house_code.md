---
topic: aws_small_house
dimension: code
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: AWS RoboMaker Small House World — https://github.com/aws-robotics/aws-robomaker-small-house-world"
  - "📖 Docs: iRobot Create 3 Simulator — https://iroboteducation.github.io/create3_docs/sim/setup/"
  - "📖 Docs: CST8509 Lab 3 Gazebo — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/labs/CST8509_Lab3_Gazebo.md"
expiry: 6m
status: current
---

# AWS Small House 代码参考

> 📖 Docs: [AWS Small House README](https://github.com/aws-robotics/aws-robomaker-small-house-world)
> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md)

## 快速开始

### 最简示例 — 3 步启动 AWS Small House

```bash
# ============================================================
# 1. 克隆 AWS Small House 世界到工作空间
#    Clone the AWS Small House world into workspace
# ============================================================
cd ~/create3_ws/src
git clone https://github.com/aws-robotics/aws-robomaker-small-house-world.git

# ============================================================
# 2. 安装依赖并构建
#    Install dependencies and build
# ============================================================
cd ~/create3_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install

# ============================================================
# 3. 加载环境并启动 Gazebo（不含 ROS）
#    Load environment and launch Gazebo (without ROS)
# ============================================================
source install/setup.bash
export GAZEBO_MODEL_PATH=~/create3_ws/src/aws-robomaker-small-house-world/models
gazebo ~/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world
```

**测试方法：** Gazebo GUI 应显示一个多房间住宅，包含家具、画框、灯光

---

## 完整实现示例

### 示例 1: 完整部署 Create3 + AWS Small House 仿真

```bash
# ============================================================
# 1. 前置环境准备 / Environment Setup
# ============================================================

# 安装 Ubuntu Desktop GUI（如果是服务器版本）
# Install Ubuntu Desktop GUI (if server edition)
sudo apt install ubuntu-desktop

# 安装 ROS 2 Humble Desktop 版
# Install ROS 2 Humble Desktop
sudo apt install ros-humble-desktop

# 安装 Classic Gazebo 11
# Install Classic Gazebo 11
curl -sSL http://get.gazebosim.org | sh
# 或者 / or:
# sudo apt install gazebo

# ============================================================
# 2. 创建工作空间并克隆仓库 / Create Workspace & Clone Repos
# ============================================================

# 创建 ROS 2 工作空间
# Create ROS 2 workspace
mkdir -p ~/create3_ws/src
cd ~/create3_ws/src

# 克隆 Create 3 模拟器仓库（humble 分支）
# Clone Create 3 simulator repo (humble branch)
git clone https://github.com/iRobotEducation/create3_sim.git
cd create3_sim
git checkout humble
cd ~/create3_ws/src

# 克隆 AWS Small House 世界
# Clone AWS Small House world
git clone https://github.com/aws-robotics/aws-robomaker-small-house-world.git

# ============================================================
# 3. 安装依赖并构建 / Install Dependencies & Build
# ============================================================
cd ~/create3_ws

# 设置 Ignition 版本变量（即使用 Classic Gazebo 也需要）
# Set Ignition version variable (needed even for Classic Gazebo)
export IGNITION_VERSION=fortress

# 安装 ROS 依赖
# Install ROS dependencies
rosdep install --from-paths src --ignore-src -r -y

# 构建整个工作空间
# Build entire workspace
colcon build --symlink-install

# ============================================================
# 4. 配置 Gazebo 环境 / Configure Gazebo Environment
# ============================================================

# 加载 Gazebo 11 环境变量（关键！否则 ROS 2 插件不工作）
# Source Gazebo 11 setup (CRITICAL! Without this, ROS 2 plugins won't work)
source /usr/share/gazebo-11/setup.sh

# 加载 ROS 2 工作空间
# Source ROS 2 workspace
source ~/create3_ws/install/setup.bash

# 设置模型路径
# Set model path
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/create3_ws/src/aws-robomaker-small-house-world/models

# ============================================================
# 5. 启动 Create3 + AWS Small House 仿真 / Launch Simulation
# ============================================================

# 使用 create3_sim 提供的 Launch 文件启动
# Launch using create3_sim's Launch file
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py \
    world:=~/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world
```

### 示例 2: 添加虚拟摄像头（camera.urdf.xacro）

```xml
<?xml version="1.0"?>
<!-- ============================================================ -->
<!-- camera.urdf.xacro — 为 Create 3 添加虚拟摄像头                -->
<!-- camera.urdf.xacro — Add virtual camera to Create 3           -->
<!-- ============================================================ -->
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" >

    <!-- ======================================================== -->
    <!-- Part 1: 关节和链接 / Joint and Link                       -->
    <!-- 将摄像头固定在 Create 3 基座上方 0.2m 处                   -->
    <!-- Fix camera 0.2m above Create 3 base_link                 -->
    <!-- ======================================================== -->
    <joint name="camera_joint" type="fixed">
        <parent link="base_link"/>
        <child link="camera_link"/>
        <!-- 摄像头位于基座正上方 0.2m / Camera sits 0.2m above base -->
        <origin xyz="0 0 0.2" rpy="0 0 0"/>
    </joint>

    <link name="camera_link">
        <visual>
            <geometry>
                <!-- 摄像头外形：1cm x 3cm x 3cm 的方块 -->
                <!-- Camera shape: 1cm x 3cm x 3cm box -->
                <box size="0.010 0.03 0.03"/>
            </geometry>
            <material name="red"/>
        </visual>
    </link>

    <material name="red">
        <color rgba="1 0 0 1"/>
    </material>

    <!-- ======================================================== -->
    <!-- Part 2: 光学链接 / Optical Link                           -->
    <!-- ROS 坐标系 (x前/y左/z上) → 光学坐标系 (x右/y下/z前)       -->
    <!-- ROS frame (x-fwd/y-left/z-up) → Optical (x-right/y-down/z-fwd) -->
    <!-- ======================================================== -->
    <joint name="camera_optical_joint" type="fixed">
        <parent link="camera_link"/>
        <child link="camera_link_optical"/>
        <!-- 旋转 -90° 绕 X 轴和 Z 轴 / Rotate -90° around X and Z -->
        <origin xyz="0 0 0" rpy="${-pi/2} 0 ${-pi/2}"/>
    </joint>

    <link name="camera_link_optical"></link>

    <!-- ======================================================== -->
    <!-- Part 3: Gazebo 摄像头插件 / Gazebo Camera Plugin          -->
    <!-- 让虚拟摄像头在 Gazebo 中工作并发布 ROS 2 Topic             -->
    <!-- Make virtual camera work in Gazebo and publish ROS 2 topics -->
    <!-- ======================================================== -->
    <gazebo reference="camera_link">
        <material name="red"/>
        <sensor name="camera" type="camera">
            <pose> 0 0 0 0 0 0 </pose>
            <visualize>true</visualize>
            <!-- 每秒 10 帧 / 10 frames per second -->
            <update_rate>10</update_rate>
            <camera name="head">
                <!-- 水平视场角 ~62° / Horizontal FOV ~62° -->
                <horizontal_fov>1.089</horizontal_fov>
                <image>
                    <format>R8G8B8</format>
                    <!-- 640x480 分辨率 / 640x480 resolution -->
                    <width>640</width>
                    <height>480</height>
                </image>
                <clip>
                    <!-- 近/远裁剪面 / Near/far clipping planes -->
                    <near>0.05</near>
                    <far>8.0</far>
                </clip>
            </camera>

            <!-- ROS 2 摄像头插件 / ROS 2 Camera Plugin -->
            <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
                <ros>
                    <namespace>custom_ns</namespace>
                    <!-- 图像 Topic: /custom_ns/camera1/custom_img -->
                    <remapping>image_raw:=custom_img</remapping>
                    <!-- 相机信息 Topic: /custom_ns/camera1/custom_info -->
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

### 示例 3: 构建摄像头并验证

```bash
# ============================================================
# 构建带摄像头的 Create 3 / Build Create 3 with Camera
# ============================================================

# 重新构建 irobot_create_description 包
# Rebuild irobot_create_description package
cd ~/create3_ws
colcon build --symlink-install --packages-select irobot_create_description

# 关键：加载 Gazebo 11 环境变量（否则摄像头 Topic 不出现！）
# CRITICAL: Source Gazebo 11 setup (camera topics won't appear without this!)
source /usr/share/gazebo-11/setup.sh

# 加载工作空间
# Source workspace
source install/setup.bash

# 重新启动仿真
# Restart simulation
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py \
    world:=~/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world

# ============================================================
# 在另一个终端中验证摄像头 / Verify camera in another terminal
# ============================================================

# 检查摄像头 Topic 是否出现
# Check if camera topics appear
ros2 topic list | grep custom

# 预期输出 / Expected output:
# /custom_ns/camera1/custom_img
# /custom_ns/camera1/custom_info
```

---

## API 速查

### Gazebo 环境变量

| 变量 | 用途 | 默认值 | 说明 |
|------|------|--------|------|
| `GAZEBO_MODEL_PATH` | 模型搜索路径 | `/usr/share/gazebo-11/models` | 多路径用 `:` 分隔 |
| `GAZEBO_RESOURCE_PATH` | 资源搜索路径 | 系统默认 | World 文件搜索路径 |
| `IGNITION_VERSION` | Ign 版本 | — | 设为 `fortress` |

### Create 3 控制命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"` | 解除停靠 | 机器人离开充电底座 |
| `ros2 action send_goal /dock irobot_create_msgs/action/DockServo "{}"` | 停靠 | 机器人回到充电底座 |
| `ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "..."` | 移动控制 | 前进/后退/转弯 |
| `ros2 topic echo /custom_ns/camera1/custom_img` | 查看图像 | 验证摄像头输出 |

### 关键文件路径

| 文件 | 路径 | 用途 |
|------|------|------|
| World 文件 | `src/aws-robomaker-small-house-world/worlds/small_house.world` | Gazebo 世界描述 |
| 家具模型 | `src/aws-robomaker-small-house-world/models/` | 所有 3D 模型 |
| URDF 入口 | `src/create3_sim/.../urdf/create3.urdf.xacro` | Create 3 描述 |
| 摄像头文件 | `src/create3_sim/.../urdf/camera.urdf.xacro` | 虚拟摄像头（自建） |

---

## 目录结构模板

### CST8509 Lab 3 标准结构

```
~/create3_ws/                          ← ROS 2 工作空间根目录
├── src/
│   ├── create3_sim/                   ← Create 3 模拟器（git clone）
│   │   └── irobot_create_common/
│   │       └── irobot_create_description/
│   │           └── urdf/
│   │               ├── create3.urdf.xacro    ← 原始机器人描述
│   │               └── camera.urdf.xacro     ← 自建虚拟摄像头
│   └── aws-robomaker-small-house-world/     ← AWS Small House（git clone）
│       ├── worlds/
│       │   └── small_house.world            ← SDF World 主文件
│       ├── models/                          ← 家具模型目录
│       │   ├── aws_robomaker_residential_*/
│       │   └── ...
│       └── launch/
│           └── small_house.launch           ← ROS Launch 文件
├── build/                             ← 构建输出（自动生成）
├── install/                           ← 安装输出（自动生成）
└── log/                               ← 构建日志（自动生成）
```
