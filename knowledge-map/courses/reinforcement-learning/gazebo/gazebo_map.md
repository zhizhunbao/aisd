---
topic: gazebo
dimension: map
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — Gazebo, Dynamic Programming & Monte Carlo — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: Gazebo Simulator — https://gazebosim.org/home"
  - "📖 Docs: ROS 2 Humble — https://docs.ros.org/en/humble/"
  - "📖 Docs: iRobot Create 3 Simulator — https://iroboteducation.github.io/create3_docs/sim/setup/"
expiry: 12m
status: current
---

# Gazebo 仿真器 知识地图

> 📖 Slides: CST8509 Week 7, [Gazebo, DP & MC](../../../courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf)
> 📖 Docs: [Gazebo](https://gazebosim.org/home), [ROS 2](https://docs.ros.org/en/humble/), [Create 3 Sim](https://iroboteducation.github.io/create3_docs/sim/setup/)

## 1. 核心问题

- **为什么 RL 需要仿真器？** → 真实机器人训练太慢、太危险、太贵；仿真器让 Agent 无限试错，不怕摔不会累
- **Gazebo 是什么？** → 一个开源机器人仿真平台，提供物理引擎、渲染、传感器仿真，通过 ROS 2 与 RL Agent 集成
- **Classic Gazebo 和 Ignition Gazebo 有什么区别？** → Classic Gazebo (v11) 是老版本，Ignition Gazebo 已更名为 Gazebo Sim，是新架构；课程用 Classic Gazebo 11
- **Gazebo 怎么和 RL 接上？** → Gazebo 通过 ROS 2 话题发布传感器数据（状态），接收 Twist 消息（动作），Gymnasium 环境包装 ROS 2 接口
- **URDF/SDF/Xacro 是什么？** → 三种机器人描述格式，用于定义机器人的外形、关节、传感器等

> 📖 Slides: CST8509 Week 7 Slides 3-16

---

## 2. 全景位置

    Reinforcement Learning（强化学习课程）
    ├── 基础概念
    │   └── Foundations (Agent/环境/奖励/策略)
    ├── RL 工具箱
    │   ├── Gymnasium (环境接口)
    │   ├── Stable-Baselines3 (算法库)
    │   ├──【Gazebo】(🤖 机器人仿真) ← 你在这里
    │   └── Rviz (可视化)
    ├── 规划方法
    │   ├── MDP / Dynamic Programming
    │   └── Monte Carlo
    ├── 无模型方法
    │   ├── TD / Q-Learning
    │   └── DQN / Function Approximation
    └── 高级主题
        └── Policy Gradient / Actor-Critic / RLHF

> 📖 Slides: CST8509 Week 7 Slide 3, RL Toolbox

---

## 3. 依赖地图

    前置知识                      本主题                      后续方向
    ┌───────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
    │ Foundations        │─────→│                  │─────→│ Sim-to-Real Transfer │
    │ (Agent/环境/奖励)  │─────→│     Gazebo       │─────→│ Model-Based RL       │
    │ Linux/Ubuntu 基础  │─────→│  ├ 物理仿真      │─────→│ 多传感器融合 RL      │
    │ ROS 2 基础        │─────→│  ├ ROS 2 集成    │─────→│ Robot Learning       │
    │ Python 编程       │─────→│  └ URDF/SDF 描述  │      └──────────────────────┘
    └───────────────────┘      └──────────────────┘

> 📖 Slides: CST8509 Week 7 Slides 6-12

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [gazebo_map.md](gazebo_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [gazebo_concepts.md](gazebo_concepts.md) | ② 概念 | 理解 Gazebo/ROS2/URDF 术语 |
| [gazebo_math.md](gazebo_math.md) | ③ 公式 | Gazebo 物理引擎中的坐标变换和运动学 |
| [gazebo_tutorial.md](gazebo_tutorial.md) | ④ 教程 | Why-First 理解为什么仿真对 RL 不可或缺 |
| [gazebo_code.md](gazebo_code.md) | ⑤ 代码 | 安装、启动 Gazebo + Create3 仿真器 |
| [gazebo_pitfalls.md](gazebo_pitfalls.md) | ⑥ 踩坑 | 版本混淆、安装失败、ROS 2 通信问题 |
| [gazebo_history.md](gazebo_history.md) | ⑦ 历史 | 从 Player/Stage 到 Gazebo Sim 的演进 |
| [gazebo_bridge.md](gazebo_bridge.md) | ⑧ 衔接 | 与 Gymnasium、MuJoCo、Isaac 的关系 |
| [gazebo_first_principles.md](gazebo_first_principles.md) | ⑨ 第一性原理 | 追问"为什么仿真能替代真实"的底层假设 |

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [gazebo_map.md](gazebo_map.md) 了解 Gazebo 在 RL 工具箱中的位置
2. 读 [gazebo_tutorial.md](gazebo_tutorial.md) Section 1 理解为什么 RL 需要仿真
3. 读 [gazebo_concepts.md](gazebo_concepts.md) 掌握 Gazebo/ROS2/URDF/SDF 核心术语
4. 跟 [gazebo_code.md](gazebo_code.md) 安装 Gazebo 11 并启动 Create3 仿真
5. 读 [gazebo_pitfalls.md](gazebo_pitfalls.md) 预防常见安装和配置问题
6. 读 [gazebo_history.md](gazebo_history.md) 了解机器人仿真的演进
7. 读 [gazebo_first_principles.md](gazebo_first_principles.md) 追问仿真的底层假设

### 日常参考 🔧

1. 查 [gazebo_code.md](gazebo_code.md) 安装和启动命令速查
2. 查 [gazebo_concepts.md](gazebo_concepts.md) URDF/SDF 格式参考
3. 查 [gazebo_pitfalls.md](gazebo_pitfalls.md) 排查仿真和 ROS 2 问题

### 深度研究 🔬

1. 读 [gazebo_history.md](gazebo_history.md) 完整演进线
2. 读 [gazebo_first_principles.md](gazebo_first_principles.md) Sim-to-Real Gap 的本质
3. 读 [gazebo_bridge.md](gazebo_bridge.md) 对比 MuJoCo/Isaac Sim 等替代方案

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
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
| Map | 2026-03-19 | 12m | ✅ current |
| Concepts | 2026-03-19 | 12m | ✅ current |
| Math | 2026-03-19 | 12m | ✅ current |
| Tutorial | 2026-03-19 | 12m | ✅ current |
| Code | 2026-03-19 | 6m | ✅ current |
| Pitfalls | 2026-03-19 | 6m | ✅ current |
| History | 2026-03-19 | never | ✅ current |
| Bridge | 2026-03-19 | 12m | ✅ current |
| First Principles | 2026-03-19 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [CST8509 Week 7 Slides](../../../courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf) | 📖 课件 | Gazebo 仿真和 RL 架构 |
| [Gazebo Docs](https://gazebosim.org/home) | 📖 文档 | 仿真器安装和使用 |
| [ROS 2 Humble Docs](https://docs.ros.org/en/humble/) | 📖 文档 | ROS 2 话题和节点通信 |
| [iRobot Create 3 Docs](https://iroboteducation.github.io/create3_docs/sim/setup/) | 📖 文档 | Create3 仿真器设置 |
| [create3_sim GitHub](https://github.com/iRobotEducation/create3_sim) | 💻 源码 | Create3 Gazebo 插件 |
| [URDF Tutorial](https://docs.ros.org/en/iron/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html) | 📖 文档 | URDF 机器人描述 |
