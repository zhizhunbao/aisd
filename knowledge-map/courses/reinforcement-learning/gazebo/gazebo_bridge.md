---
topic: gazebo
dimension: bridge
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: Gazebo Simulator — https://gazebosim.org/home"
expiry: 12m
status: current
---

# Gazebo 仿真器 衔接与扩展

> 📖 Slides: CST8509 Week 7; 📖 Docs: [Gazebo](https://gazebosim.org/home)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Foundations | Agent/环境/奖励的基本概念，Gazebo 是环境的物理实现 | [foundations](../foundations/foundations_map.md) |
| ← 前置 | ROS 2 基础 | Gazebo 通过 ROS 2 话题与 Agent 通信 | — |
| ← 前置 | Linux 基础 | Gazebo 运行在 Ubuntu 上 | — |
| → 后续 | Dynamic Programming | 有了仿真环境，可以用 DP 求解已知模型的最优策略 | — |
| → 后续 | Monte Carlo | 用仿真器生成完整 episode 来估计值函数 | — |
| → 后续 | Sim-to-Real Transfer | 仿真训练的策略部署到真实机器人 | — |
| → 后续 | Model-Based RL | 从仿真数据学习环境模型 | — |
| → 平行 | RViz 可视化 | Gazebo 数据的 3D 可视化调试工具 | [rviz](../rviz/rviz_map.md) |

> 📖 Slides: CST8509 Week 7 Slide 12

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| Foundations | Agent-环境交互循环 | Gazebo 充当环境，产生状态和奖励 |
| Foundations | 状态 (State) | Gazebo 传感器数据成为 Agent 的观察 |
| Foundations | 动作 (Action) | Agent 输出 Twist 消息控制机器人 |
| Gymnasium | `step()/reset()` API | Gymnasium 包装器桥接 Gazebo 的 ROS 2 接口 |

> 📖 Slides: CST8509 Week 7 Slides 3, 10-12

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|--------------------|
| Dynamic Programming | 环境模型（已知转移概率） | 如果 Gazebo 模型完全已知，可以直接用 DP 求解 |
| Monte Carlo | Episode 采样 | 在 Gazebo 中运行完整 episode 收集回报 |
| TD / Q-Learning | 在线交互 | 每步从 Gazebo 获取 (s, a, r, s') 做 TD 更新 |
| DQN | 高维观察 | Gazebo 摄像头提供图像作为 DQN 的输入 |
| Sim-to-Real | 仿真策略 | 在 Gazebo 训练的策略直接部署到真实 Create 3 |
| Model-Based RL (Dyna) | 仿真经验 | 用 Gazebo 数据训练环境模型，再用模型生成额外经验 |

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------| 
| 机器人仿真 | 2D 多机器人仿真 (Stage 2000) | 3D 物理+渲染+传感器 (Gazebo 2004) | 真实世界是 3D 的 |
| 仿真接口 | 各实验室自己写 | ROS/ROS 2 标准话题 | 需要统一接口做 Sim-to-Real |
| 仿真用途 | SLAM/导航算法验证 | RL 训练（大量 episode 采样） | DRL 需要大量交互 |
| 仿真精度 | "差不多就行" | Domain Randomization + System ID | Sim-to-Real Gap 是部署瓶颈 |
| 仿真规模 | 单实例 | GPU 并行几千实例 (Isaac) | RL 对样本效率的需求 |

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Gazebo Tutorials](https://classic.gazebosim.org/tutorials) | 📖 官方教程 | Classic Gazebo 完整教程 | ⭐⭐ |
| [Create 3 Docs](https://iroboteducation.github.io/create3_docs/) | 📖 文档 | Create 3 仿真和真实机器人的完整文档 | ⭐⭐ |
| [ROS 2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html) | 📖 文档 | ROS 2 从零到 Topic/Service/Action | ⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [MuJoCo Docs](https://mujoco.readthedocs.io/) | Gazebo vs MuJoCo 物理精度和 RL 集成 | 想做非 ROS 的 RL 时 |
| [Isaac Sim Docs](https://docs.omniverse.nvidia.com/isaacsim/) | Gazebo vs Isaac GPU 并行能力 | 需要大规模并行训练时 |
| [PyBullet Docs](https://pybullet.org/) | 轻量替代方案 | 不需要 ROS 的快速原型 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Sim-to-Real Transfer Survey](https://arxiv.org/abs/2009.13303) | 从仿真到真实的全面综述 | 想部署到真实机器人时 |
| [Domain Randomization](https://arxiv.org/abs/1703.06907) | OpenAI 的 Sim-to-Real 经典方法 | 想降低 Sim-to-Real Gap 时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| RL 课程 | 1 主题 | foundations | Gazebo 是 RL 环境的物理实现 |
| Deep Learning 课程 | 15+ 主题 | cnn | Gazebo 摄像头图像可输入 DQN 的 CNN |
| Computer Vision 课程 | 2+ 主题 | object_detection | Gazebo 虚拟摄像头 → CV 算法验证 |
