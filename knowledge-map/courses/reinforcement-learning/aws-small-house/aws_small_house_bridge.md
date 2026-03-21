---
topic: aws_small_house
dimension: bridge
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: AWS RoboMaker Small House World — https://github.com/aws-robotics/aws-robomaker-small-house-world"
  - "📖 Docs: CST8509 Lab 3 Gazebo — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/labs/CST8509_Lab3_Gazebo.md"
expiry: 12m
status: current
---

# AWS Small House 衔接与扩展

> 📖 Docs: [AWS RoboMaker Small House World](https://github.com/aws-robotics/aws-robomaker-small-house-world)
> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Gazebo 仿真器 | AWS Small House 是 Gazebo 中的一个 World | [gazebo_map.md](../gazebo/gazebo_map.md) |
| ← 前置 | ROS 2 通信 | AWS Small House 通过 ROS 2 Topic 与机器人通信 | [ros2_map.md](../ros2/ros2_map.md) |
| ← 前置 | iRobot Create 3 | Create 3 在 AWS Small House 中导航 | [irobot-create3](../irobot-create3/) |
| → 后续 | RL 训练环境 | 训练 Agent 在 AWS Small House 中导航 | — |
| → 后续 | 虚拟摄像头视觉输入 | 摄像头提供状态观测给 RL Agent | — |
| → 后续 | Sim-to-Real Transfer | 从 AWS Small House 训练迁移到真实房间 | — |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| Gazebo | SDF World 格式 | AWS Small House 的 `.world` 文件用 SDF 格式 |
| Gazebo | GAZEBO_MODEL_PATH | 用于定位 AWS Small House 的家具模型 |
| Gazebo | 物理引擎 (ODE) | 模拟 Create 3 与家具的碰撞检测 |
| Gazebo | 插件系统 | `libgazebo_ros_camera.so` 让摄像头发布 ROS 2 Topic |
| ROS 2 | Topic 通信 | 传感器数据和控制指令通过 Topic 传输 |
| ROS 2 | colcon 构建 | 用 `colcon build` 构建 AWS Small House 包 |
| ROS 2 | Launch 文件 | 用 Launch 一键启动 Gazebo + World + Create 3 |
| iRobot Create 3 | URDF/Xacro 描述 | Create 3 模型被 spawn 到 AWS Small House 中 |
| iRobot Create 3 | 差速驱动 | 在 AWS Small House 中用 `/cmd_vel` 控制移动 |

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|--------------------|
| RL 训练（Assignment 2） | 标准化仿真环境 | RL Agent 在此环境中学习导航策略 |
| 虚拟视觉输入 | 摄像头 Topic | Agent 的 observation space 包含虚拟摄像头图像 |
| Sim-to-Real Transfer | 室内场景基准 | 在仿真中训练完后迁移到真实 Create 3 + 真实房间 |
| Nav2 导航栈 | 碰撞障碍物 | 测试 ROS 2 导航栈的避障能力 |
| 多传感器融合 | IMU + Lidar + Camera | 训练使用多种传感器输入的 Agent |

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 仿真世界 | 空白世界 + 简单几何体 | 专业级预构建世界（AWS Small House） | 社区需求 + 云服务商贡献 |
| World 文件格式 | SDF（Classic Gazebo 11） | SDF 新版本（Gazebo Sim） | Gazebo 架构迁移 |
| 模型质量 | 研究者自建、质量参差不齐 | 公司级专业建模 + 开源 | AWS 投入资源做基础设施 |
| 获取方式 | 论坛分享/私有 | GitHub 开源仓库 + 包管理 | 开源文化普及 |

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [AWS RoboMaker 官网](https://aws.amazon.com/robomaker/) | 📖 文档 | 了解 AWS Small House 的上层产品背景 | ⭐ |
| [Gazebo SDF Specification](http://sdformat.org/spec) | 📖 文档 | 理解 `.world` 文件内部结构 | ⭐⭐⭐ |
| [Gazebo Inertia Tutorial](http://gazebosim.org/tutorials?tut=inertia&cat=build_robot) | 📖 文档 | 理解为什么静态/动态物体的物理参数重要 | ⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [AWS Bookstore World](https://github.com/aws-robotics/aws-robomaker-bookstore-world) | 另一种室内场景 | 需要书店/走廊场景时 |
| [AWS Small Warehouse](https://github.com/aws-robotics/aws-robomaker-small-warehouse-world) | 仓库物流场景 | 需要大面积开放空间时 |
| [TurtleBot3 Worlds](https://github.com/ROBOTIS-GIT/turtlebot3_simulations) | TurtleBot3 专用世界 | 用 TurtleBot 而非 Create 3 时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim) | 下一代仿真平台 | 需要 GPU 加速渲染或工业级仿真时 |
| [Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub) | Unity 引擎做机器人仿真 | 需要更好的视觉渲染时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 同课程 RL 工具 | 3 | [Gazebo](../gazebo/), [ROS 2](../ros2/), [Create 3](../irobot-create3/) | AWS Small House 在 Gazebo 内，通过 ROS 2 与 Create 3 集成 |
| 先修 RL 基础 | 1 | [Foundations](../foundations/) | 理解 Agent/环境/状态/动作后才明白为什么需要仿真环境 |
