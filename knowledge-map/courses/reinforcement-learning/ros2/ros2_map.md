---
topic: ros2
dimension: map
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Quigley et al., 'ROS: an open-source Robot Operating System', ICRA Workshop on Open Source Software 2009 — https://www.robotics.stanford.edu/~ang/papers/icraoss09-ROS.pdf"
  - "📖 Paper: Macenski et al., 'Robot Operating System 2: Design, architecture, and uses in the wild', Science Robotics 2022 — https://doi.org/10.1126/scirobotics.abm6074"
  - "📖 Docs: ROS 2 Humble Documentation — https://docs.ros.org/en/humble/"
  - "📖 Docs: ROS 2 Design — https://design.ros2.org/"
  - "📖 Docs: DDS Specification — https://www.omg.org/spec/DDS/"
expiry: 12m
status: current
---

# ROS 2 知识地图

> 📖 Paper: Macenski et al., [Robot Operating System 2: Design, architecture, and uses in the wild](https://doi.org/10.1126/scirobotics.abm6074), Science Robotics 2022
> 📖 Docs: [ROS 2 Humble](https://docs.ros.org/en/humble/)

## 1. 核心问题

- **ROS 2 是什么？** → 一个分布式机器人中间件框架，让不同功能模块（感知/决策/控制）通过标准化消息通信协作
- **为什么从 ROS 1 升级到 ROS 2？** → ROS 1 不支持实时性、安全性、跨平台和多机器人，工业部署面临根本性限制
- **ROS 2 的核心通信机制是什么？** → 基于 DDS (Data Distribution Service) 的发布/订阅 + 服务/客户端 + 动作三种模式
- **ROS 2 如何与 RL 结合？** → 作为 Agent-环境通信桥梁，Gazebo 仿真器通过 ROS 2 Topic 传递状态和动作
- **ROS 2 的版本选哪个？** → 课程使用 Humble Hawksbill (LTS, 2022-2027)，是当前最稳定的长期支持版本

> 📖 Paper: Macenski et al. 2022, Section I; 📖 Docs: [ROS 2 Humble](https://docs.ros.org/en/humble/)

---

## 2. 全景位置

    机器人软件栈
    ├── 操作系统层 (Ubuntu / Windows / macOS)
    ├── 中间件层 ← 你在这里
    │   ├── 【ROS 2】 (通用、标准化、开源)
    │   ├── YARP (iCub 机器人专用)
    │   └── OROCOS (实时控制框架)
    ├── 仿真层
    │   ├── Gazebo (ROS 2 深度集成)
    │   ├── MuJoCo (物理精度高)
    │   └── Isaac Sim (GPU 并行)
    ├── 算法层
    │   ├── 感知 (OpenCV, PCL)
    │   ├── 规划 (Nav2, MoveIt)
    │   └── 学习 (RL: Gymnasium + SB3)
    └── 应用层
        ├── 自动驾驶 (Autoware)
        ├── 无人机 (PX4)
        └── 服务机器人 (Create 3)

> 📖 Paper: Macenski et al. 2022, Fig. 1; 📖 Docs: [ROS 2 Ecosystem](https://docs.ros.org/en/humble/)

---

## 3. 依赖地图

    前置知识                 本主题                   后续方向
    ┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────┐
    │ Linux 基础       │────→│                  │────→│ Gazebo 仿真器         │
    │ Python 编程      │────→│   ROS 2          │────→│ iRobot Create 3      │
    │ 网络通信基础      │────→│                  │────→│ Rviz 可视化           │
    │ RL 基础概念       │────→│                  │────→│ RL Agent 部署         │
    └─────────────────┘     └──────────────────┘     └──────────────────────┘

> 📖 Docs: [ROS 2 Tutorials Prerequisites](https://docs.ros.org/en/humble/Tutorials.html)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [ros2_map.md](ros2_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [ros2_concepts.md](ros2_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| ~~ros2_math.md~~ | ③ 公式 | ~~不适用~~ — ROS 2 是中间件框架，无核心数学内容 |
| [ros2_tutorial.md](ros2_tutorial.md) | ④ 教程 | Why-First 理解 ROS 2 设计动机与原理 |
| [ros2_code.md](ros2_code.md) | ⑤ 代码 | 快速上手 Node/Topic/Service/Action 编程 |
| [ros2_pitfalls.md](ros2_pitfalls.md) | ⑥ 踩坑 | 调试 ROS 2 通信问题 |
| [ros2_history.md](ros2_history.md) | ⑦ 历史 | 了解 ROS 1 → ROS 2 的演进 |
| [ros2_bridge.md](ros2_bridge.md) | ⑧ 衔接 | 找相关主题（Gazebo/Rviz/Create 3） |
| [ros2_first_principles.md](ros2_first_principles.md) | ⑨ 第一性原理 | 追问分布式通信设计的底层公理 |

> 📖 设计参考: Norman《The Design of Everyday Things》(2013), Ch.3

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [ros2_map.md](ros2_map.md) 了解全局位置
2. 读 [ros2_tutorial.md](ros2_tutorial.md) Section 1 理解动机——没有 ROS 2 的世界有多痛苦
3. 读 [ros2_concepts.md](ros2_concepts.md) 掌握 Node/Topic/Service/Action 核心术语
4. 跟 [ros2_code.md](ros2_code.md) 快速开始跑一个 Publisher-Subscriber 示例
5. 读 [ros2_history.md](ros2_history.md) 了解 ROS 1 → ROS 2 的演进故事
6. 读 [ros2_first_principles.md](ros2_first_principles.md) 追问分布式通信的底层设计

### 日常参考 🔧

1. 查 [ros2_code.md](ros2_code.md) API 速查表（ros2 topic/service/action 命令）
2. 查 [ros2_pitfalls.md](ros2_pitfalls.md) 排查 Topic 不通、消息类型不匹配等常见问题
3. 查 [ros2_concepts.md](ros2_concepts.md) 速查表辨析 Topic vs Service vs Action

### 深度研究 🔬

1. 读 [ros2_history.md](ros2_history.md) 完整的 ROS → ROS 2 → DDS 演进线
2. 读 [ros2_first_principles.md](ros2_first_principles.md) 追问 DDS、QoS 的底层公理
3. 读 [ros2_bridge.md](ros2_bridge.md) 探索 Gazebo/Nav2/MoveIt 等下游应用
4. 阅读原始论文: Macenski et al. 2022

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ⬜ 待生成 |
| Concepts | ⬜ 待生成 |
| Math | ~~不适用~~ |
| Tutorial | ⬜ 待生成 |
| Code | ⬜ 待生成 |
| Pitfalls | ⬜ 待生成 |
| History | ⬜ 待生成 |
| Bridge | ⬜ 待生成 |
| First Principles | ⬜ 待生成 |

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
| [Quigley et al. 2009](https://www.robotics.stanford.edu/~ang/papers/icraoss09-ROS.pdf) | 📖 论文 | History（ROS 1 起源） |
| [Macenski et al. 2022](https://doi.org/10.1126/scirobotics.abm6074) | 📖 论文 | 全文核心参考（ROS 2 架构与设计） |
| [ROS 2 Humble Docs](https://docs.ros.org/en/humble/) | 📖 文档 | Concepts/Tutorial/Code（官方参考） |
| [ROS 2 Design Docs](https://design.ros2.org/) | 📖 文档 | Tutorial/First Principles（设计决策） |
| [DDS Specification](https://www.omg.org/spec/DDS/) | 📖 文档 | First Principles（通信协议标准） |
| [ROS Wiki (ROS 1)](http://wiki.ros.org/) | 📖 文档 | History（ROS 1 文档参考） |
| [CST8509 Week 7 Slides](file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf) | 📖 课件 | Bridge（课程上下文） |
