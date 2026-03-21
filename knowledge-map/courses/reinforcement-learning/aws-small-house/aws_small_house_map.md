---
topic: aws_small_house
dimension: map
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: AWS RoboMaker Small House World — https://github.com/aws-robotics/aws-robomaker-small-house-world"
  - "📖 Docs: iRobot Create 3 Simulator — https://iroboteducation.github.io/create3_docs/sim/setup/"
  - "📖 Docs: Gazebo Classic Tutorials — https://classic.gazebosim.org/tutorials"
  - "📖 Docs: CST8509 Lab 3 Gazebo — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/labs/CST8509_Lab3_Gazebo.md"
expiry: 12m
status: current
---

# AWS Small House 知识地图

> 📖 Docs: [AWS RoboMaker Small House World](https://github.com/aws-robotics/aws-robomaker-small-house-world)
> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md)

## 1. 核心问题

- **AWS Small House 是什么？** → 一个由 AWS Robotics 团队创建的 Gazebo 仿真世界（World），包含多个房间和家具，用于机器人导航和 RL 训练
- **为什么不自己建世界？** → 从零建一个逼真的室内环境需要大量 3D 建模工作（墙壁、家具、纹理），AWS 已经做好了现成的
- **它和 Create 3 是什么关系？** → Create 3 在这个虚拟房屋里导航，就像真实 Create 3 在真实房间里走一样——同样的 ROS 2 Topic，同样的传感器数据
- **为什么叫 "Small House"？** → AWS 提供了多种仿真世界（Small House、Bookstore、Small Warehouse），Small House 是最适合室内导航 RL 的场景

> 📖 Docs: [AWS RoboMaker Small House World README](https://github.com/aws-robotics/aws-robomaker-small-house-world)

---

## 2. 全景位置

    Reinforcement Learning（强化学习课程）
    ├── 基础概念
    │   └── Foundations (Agent/环境/奖励/策略)
    ├── RL 工具箱
    │   ├── Gymnasium (环境接口)
    │   ├── Stable-Baselines3 (算法库)
    │   ├── Gazebo (🤖 机器人仿真)
    │   │   └── 仿真世界 ← 你在这里
    │   │       ├──【AWS Small House】(🏠 室内导航世界)
    │   │       ├── AWS Bookstore (📚 书店世界)
    │   │       └── AWS Small Warehouse (🏭 仓库世界)
    │   ├── iRobot Create 3 (教育机器人)
    │   └── RViz (可视化)
    └── 算法
        ├── Dynamic Programming / Monte Carlo
        └── TD / Q-Learning / DQN / Policy Gradient

> 📖 Docs: [CST8509 Lab 3 Gazebo](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md)

---

## 3. 依赖地图

    前置知识                      本主题                         后续方向
    ┌────────────────────┐      ┌───────────────────────┐      ┌──────────────────────────┐
    │ Gazebo Classic 11  │─────→│                       │─────→│ RL 训练环境搭建           │
    │ ROS 2 Humble       │─────→│   AWS Small House     │─────→│ 虚拟摄像头 + 视觉输入     │
    │ create3_sim 仓库   │─────→│   ├ SDF World 文件    │─────→│ Sim-to-Real Transfer     │
    │ colcon 构建工具     │─────→│   ├ 3D 家具模型      │─────→│ 自主导航策略              │
    │ Ubuntu 22.04       │─────→│   └ Gazebo 插件      │      └──────────────────────────┘
    └────────────────────┘      └───────────────────────┘

> 📖 Docs: [create3_sim humble 分支](https://github.com/iRobotEducation/create3_sim)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [aws_small_house_map.md](aws_small_house_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [aws_small_house_concepts.md](aws_small_house_concepts.md) | ② 概念 | 理解 World/Model/SDF/Plugin 术语 |
| ~~aws_small_house_math.md~~ | ~~③ 公式~~ | ~~不适用：纯工程工具~~ |
| [aws_small_house_tutorial.md](aws_small_house_tutorial.md) | ④ 教程 | Why-First 理解为什么用现成世界 |
| [aws_small_house_code.md](aws_small_house_code.md) | ⑤ 代码 | 安装、构建、启动 AWS 世界 |
| [aws_small_house_pitfalls.md](aws_small_house_pitfalls.md) | ⑥ 踩坑 | 构建失败、模型路径、版本问题 |
| [aws_small_house_history.md](aws_small_house_history.md) | ⑦ 历史 | AWS RoboMaker 仿真世界的演进 |
| [aws_small_house_bridge.md](aws_small_house_bridge.md) | ⑧ 衔接 | 与 Gazebo、Create 3、RViz 的关系 |
| [aws_small_house_first_principles.md](aws_small_house_first_principles.md) | ⑨ 第一性原理 | 追问仿真世界的本质假设 |

> 📖 Docs: [AWS RoboMaker Small House World](https://github.com/aws-robotics/aws-robomaker-small-house-world)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [aws_small_house_map.md](aws_small_house_map.md) 了解 AWS Small House 在 RL 工具链中的位置
2. 读 [aws_small_house_tutorial.md](aws_small_house_tutorial.md) Section 1 理解为什么用现成仿真世界
3. 读 [aws_small_house_concepts.md](aws_small_house_concepts.md) 掌握 World/Model/SDF/Plugin 术语
4. 跟 [aws_small_house_code.md](aws_small_house_code.md) 下载、构建并启动 AWS Small House
5. 读 [aws_small_house_pitfalls.md](aws_small_house_pitfalls.md) 预防构建和路径问题
6. 读 [aws_small_house_history.md](aws_small_house_history.md) 了解 AWS RoboMaker 仿真世界的由来
7. 读 [aws_small_house_first_principles.md](aws_small_house_first_principles.md) 追问仿真世界保真度的底层假设

### 日常参考 🔧

1. 查 [aws_small_house_code.md](aws_small_house_code.md) 安装和启动命令速查
2. 查 [aws_small_house_concepts.md](aws_small_house_concepts.md) SDF/Model 格式参考
3. 查 [aws_small_house_pitfalls.md](aws_small_house_pitfalls.md) 排查构建和运行问题

### 深度研究 🔬

1. 读 [aws_small_house_history.md](aws_small_house_history.md) 完整演进线
2. 读 [aws_small_house_first_principles.md](aws_small_house_first_principles.md) 仿真保真度的本质
3. 读 [aws_small_house_bridge.md](aws_small_house_bridge.md) 对比其他仿真世界和 Sim-to-Real

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ~~不适用~~ |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-21 | 12m | ✅ current |
| Concepts | 2026-03-21 | 12m | ✅ current |
| Math | — | — | ~~不适用~~ |
| Tutorial | 2026-03-21 | 12m | ✅ current |
| Code | 2026-03-21 | 6m | ✅ current |
| Pitfalls | 2026-03-21 | 6m | ✅ current |
| History | 2026-03-21 | never | ✅ current |
| Bridge | 2026-03-21 | 12m | ✅ current |
| First Principles | 2026-03-21 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [AWS RoboMaker Small House World](https://github.com/aws-robotics/aws-robomaker-small-house-world) | 💻 源码 | World 文件、模型定义、构建方法 |
| [CST8509 Lab 3 Gazebo](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md) | 📖 课程实验 | 安装部署流程、虚拟摄像头集成 |
| [iRobot Create 3 Simulator](https://iroboteducation.github.io/create3_docs/sim/setup/) | 📖 文档 | Create3 仿真器设置和集成 |
| [create3_sim GitHub](https://github.com/iRobotEducation/create3_sim) | 💻 源码 | Create3 Gazebo 插件和 Launch 文件 |
| [Gazebo Classic 11 Docs](https://classic.gazebosim.org/tutorials) | 📖 文档 | SDF 格式、World 文件、Gazebo 插件 |
| [ROS 2 Humble Docs](https://docs.ros.org/en/humble/) | 📖 文档 | ROS 2 话题通信、colcon 构建 |
| [AWS RoboMaker](https://aws.amazon.com/robomaker/) | 📖 文档 | AWS RoboMaker 服务概述 |
