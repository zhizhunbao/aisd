---
topic: rviz
dimension: map
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — Gazebo, Dynamic Programming & Monte Carlo — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: RViz2 User Guide — https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html"
  - "📖 Docs: TurtleBot4 RViz — https://turtlebot.github.io/turtlebot4-user-manual/software/rviz.html"
expiry: 12m
status: current
---

# RViz 可视化工具 知识地图

> 📖 Slides: CST8509 Week 7 Slide 16; 📖 Docs: [RViz2 User Guide](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

## 1. 核心问题

- **RViz 是什么？** → ROS 2 的 3D 可视化工具，用于查看机器人状态、传感器数据、坐标系、路径规划等——机器人世界的"调试窗口"
- **RViz 和 Gazebo 有什么区别？** → Gazebo 做**仿真**（物理引擎让机器人动），RViz 做**可视化**（只看不动）。Gazebo 是"虚拟世界"，RViz 是"监视器"
- **RViz 能显示什么？** → 机器人模型 (URDF)、TF 坐标系树、点云、激光扫描、摄像头图像、路径、Marker 几何体等
- **RViz 在 RL 中有什么用？** → 调试 Agent 行为——看机器人在仿真中是不是往对的方向走、传感器数据对不对、奖励区域在哪
- **Displays、Tools、Panels 分别是什么？** → Displays 是 3D 世界中的可视化元素，Tools 是交互工具，Panels 是状态面板

> 📖 Slides: CST8509 Week 7 Slide 16; 📖 Docs: [RViz2](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

---

## 2. 全景位置

    Reinforcement Learning（强化学习课程）
    ├── 基础概念
    │   └── Foundations (Agent/环境/奖励/策略)
    ├── RL 工具箱
    │   ├── Gymnasium (环境接口)
    │   ├── Stable-Baselines3 (算法库)
    │   ├── Gazebo (🤖 机器人仿真)
    │   └──【RViz】(🔍 可视化调试) ← 你在这里
    ├── 规划方法
    │   ├── MDP / Dynamic Programming
    │   └── Monte Carlo
    ├── 无模型方法
    │   └── TD / Q-Learning / DQN
    └── 高级主题
        └── Policy Gradient / Actor-Critic / RLHF

> 📖 Slides: CST8509 Week 7 Slide 3, RL Toolbox

---

## 3. 依赖地图

    前置知识                      本主题                        后续方向
    ┌───────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
    │ ROS 2 基础        │─────→│                  │─────→│ SLAM 可视化          │
    │ (Topic/Node)      │─────→│      RViz        │─────→│ Navigation 调试      │
    │ Gazebo 仿真       │─────→│  ├ Display 管理  │─────→│ 自定义 RViz 插件     │
    │ URDF 机器人描述   │─────→│  ├ 坐标系 (TF)   │─────→│ Multi-Robot 可视化   │
    │ Linux 基础        │─────→│  └ 传感器数据查看 │      └──────────────────────┘
    └───────────────────┘      └──────────────────┘

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [rviz_map.md](rviz_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [rviz_concepts.md](rviz_concepts.md) | ② 概念 | 理解 Display/Tool/Panel/TF 术语 |
| [rviz_math.md](rviz_math.md) | ③ 公式 | TF 坐标变换的数学基础 |
| [rviz_tutorial.md](rviz_tutorial.md) | ④ 教程 | Why-First 理解 RViz 在 RL 调试中的角色 |
| [rviz_code.md](rviz_code.md) | ⑤ 代码 | 启动 RViz、添加 Display、launch 文件集成 |
| [rviz_pitfalls.md](rviz_pitfalls.md) | ⑥ 踩坑 | Fixed Frame 错误、TF 问题、性能优化 |
| [rviz_history.md](rviz_history.md) | ⑦ 历史 | 从 RViz (ROS 1) 到 RViz2 (ROS 2) 的演进 |
| [rviz_bridge.md](rviz_bridge.md) | ⑧ 衔接 | 与 Gazebo、rqt、PlotJuggler 的关系 |
| [rviz_first_principles.md](rviz_first_principles.md) | ⑨ 第一性原理 | 追问"可视化对 RL 调试为什么不可或缺" |

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [rviz_map.md](rviz_map.md) 了解 RViz 在 RL 工具箱中的位置
2. 读 [rviz_tutorial.md](rviz_tutorial.md) Section 1 理解为什么需要可视化调试
3. 读 [rviz_concepts.md](rviz_concepts.md) 掌握 Display/TF/Fixed Frame 核心术语
4. 跟 [rviz_code.md](rviz_code.md) 启动 RViz 并添加机器人模型和激光扫描
5. 读 [rviz_pitfalls.md](rviz_pitfalls.md) 预防 Fixed Frame 和 TF 常见问题
6. 读 [rviz_history.md](rviz_history.md) 了解 RViz 到 RViz2 的演进

### 日常参考 🔧

1. 查 [rviz_code.md](rviz_code.md) 启动命令和 Display 配置速查
2. 查 [rviz_pitfalls.md](rviz_pitfalls.md) 排查 TF 和显示问题

### 深度研究 🔬

1. 读 [rviz_first_principles.md](rviz_first_principles.md) 可视化调试的底层价值
2. 读 [rviz_bridge.md](rviz_bridge.md) 探索 rqt、PlotJuggler 等替代工具

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
| [CST8509 Week 7 Slides](../../../courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf) | 📖 课件 | RViz 在 RL 工具箱中的定位 |
| [RViz2 User Guide](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html) | 📖 文档 | RViz2 完整使用指南 |
| [TurtleBot4 RViz Manual](https://turtlebot.github.io/turtlebot4-user-manual/software/rviz.html) | 📖 文档 | RViz 实际使用案例 |
| [ROS 2 Humble TF2 Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html) | 📖 文档 | TF 坐标系变换 |
