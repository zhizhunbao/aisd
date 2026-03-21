---
topic: irobot-create3
dimension: map
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Soragna et al., 'Impact of ROS 2 Node Composition in Robotic Systems', IEEE RA-L 2023 — https://arxiv.org/abs/2305.09933"
  - "📖 Paper: Koenig & Howard, 'Design and Use Paradigms for Gazebo', IROS 2004 — https://doi.org/10.1109/IROS.2004.1389727"
  - "📖 Paper: Quigley et al., 'ROS: an open-source Robot Operating System', ICRA Workshop 2009 — https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf"
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Docs: iRobot Create 3 — Hardware Overview — https://iroboteducation.github.io/create3_docs/hw/overview/"
  - "📖 Docs: iRobot Create 3 — ROS 2 API — https://iroboteducation.github.io/create3_docs/api/ros2/"
  - "📖 Docs: iRobot Create 3 — Simulator Setup — https://iroboteducation.github.io/create3_docs/sim/setup/"
  - "💻 Source: create3_sim — https://github.com/iRobotEducation/create3_sim"
  - "💻 Source: irobot_create_msgs — https://github.com/iRobotEducation/irobot_create_msgs"
  - "📖 Docs: ROS 2 Humble — https://docs.ros.org/en/humble/"
expiry: 12m
status: current
---

# iRobot Create 3 知识地图

> 📖 Paper: Soragna et al., [ROS 2 Node Composition](https://arxiv.org/abs/2305.09933), IEEE RA-L 2023
> 📚 Book: Sutton & Barto, [《RL: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1
> 📖 Docs: [Create 3 Docs](https://iroboteducation.github.io/create3_docs/), [ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/)
> 💻 Source: [create3_sim](https://github.com/iRobotEducation/create3_sim), [irobot_create_msgs](https://github.com/iRobotEducation/irobot_create_msgs)

## 1. 核心问题

- **Create 3 是什么？** → 基于 Roomba 底盘的教育机器人平台，所有接口通过 ROS 2 暴露（Topic/Service/Action/Parameter）
- **它在 RL 训练中扮演什么角色？** → 作为 RL 的物理执行器——Agent 通过 `/cmd_vel` 发 Twist 消息控制它，通过传感器 Topic 获取状态
- **真实 Create 3 和仿真 Create 3 有什么区别？** → 仿真 Create 3 暴露与真实机器人**完全相同的 ROS 2 API**，Agent 代码零修改即可迁移
- **Create 3 有哪些传感器？** → 7 对 IR 接近传感器、4 个悬崖传感器、IMU、光学里程计、轮编码器——全部通过 ROS 2 Topic 发布
- **如何给 Create 3 添加额外传感器（如摄像头）？** → 通过 URDF/Xacro 文件定义新 Link+Joint，用 Gazebo 插件仿真传感器数据

> 📖 Docs: [Create 3 Home](https://iroboteducation.github.io/create3_docs/), [Hardware Overview](https://iroboteducation.github.io/create3_docs/hw/overview/)

---

## 2. 全景位置

    Reinforcement Learning（强化学习课程）
    ├── 基础概念
    │   └── Foundations (Agent/环境/奖励/策略)
    ├── RL 工具箱 ← 你在这里
    │   ├── Gymnasium (RL 环境 Python API 标准)
    │   ├── Stable-Baselines3 (RL 算法库)
    │   ├── Gazebo (3D 物理仿真平台)
    │   ├──【iRobot Create 3】(🤖 教育机器人平台 + ROS 2 全 API)
    │   └── RViz (ROS 2 数据可视化)
    ├── 规划方法
    │   ├── Dynamic Programming
    │   └── Monte Carlo
    ├── 无模型方法
    │   ├── TD / Q-Learning
    │   └── DQN / Function Approximation
    └── 高级主题
        └── Policy Gradient / Actor-Critic / RLHF

> 📖 Docs: [Create 3 Home](https://iroboteducation.github.io/create3_docs/)

---

## 3. 依赖地图

    前置知识                      本主题                       后续方向
    ┌───────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
    │ Foundations        │─────→│                      │─────→│ Gazebo 仿真环境搭建  │
    │ (Agent/环境/奖励)  │─────→│   iRobot Create 3    │─────→│ RL 训练 (DQN/PPO)    │
    │ ROS 2 基础        │─────→│  ├ 硬件: 传感器/执行器│─────→│ Sim-to-Real Transfer │
    │ Linux/Ubuntu      │─────→│  ├ ROS 2 API          │─────→│ 多传感器融合 RL      │
    │ Python 编程       │─────→│  └ URDF 扩展          │      └──────────────────────┘
    └───────────────────┘      └──────────────────────┘

> 📖 Docs: [Create 3 ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [irobot-create3_map.md](irobot-create3_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [irobot-create3_concepts.md](irobot-create3_concepts.md) | ② 概念 | 理解 Create 3 硬件/ROS 2 API 术语 |
| [irobot-create3_math.md](irobot-create3_math.md) | ③ 公式 | 差速运动学、里程计融合、坐标变换 |
| [irobot-create3_tutorial.md](irobot-create3_tutorial.md) | ④ 教程 | Why-First 理解 Create 3 在 RL 中的角色 |
| [irobot-create3_code.md](irobot-create3_code.md) | ⑤ 代码 | 安装仿真器、ROS 2 控制命令、URDF 摄像头 |
| [irobot-create3_pitfalls.md](irobot-create3_pitfalls.md) | ⑥ 踩坑 | 版本混淆、source 遗漏、话题找不到 |
| [irobot-create3_history.md](irobot-create3_history.md) | ⑦ 历史 | 从 Roomba 到 Create 3 的演进 |
| [irobot-create3_bridge.md](irobot-create3_bridge.md) | ⑧ 衔接 | 与 Gazebo、Gymnasium、RViz 的关系 |
| [irobot-create3_first_principles.md](irobot-create3_first_principles.md) | ⑨ 第一性原理 | 追问"为什么 ROS 2 能统一仿真和真实"的底层假设 |

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [irobot-create3_map.md](irobot-create3_map.md) 了解 Create 3 在 RL 工具箱中的位置
2. 读 [irobot-create3_tutorial.md](irobot-create3_tutorial.md) Section 1 理解为什么选 Create 3
3. 读 [irobot-create3_concepts.md](irobot-create3_concepts.md) 掌握硬件和 ROS 2 API 核心术语
4. 跟 [irobot-create3_code.md](irobot-create3_code.md) 部署仿真器并发送控制命令
5. 读 [irobot-create3_pitfalls.md](irobot-create3_pitfalls.md) 预防常见安装和配置问题
6. 读 [irobot-create3_history.md](irobot-create3_history.md) 了解 Create 系列的演进
7. 读 [irobot-create3_first_principles.md](irobot-create3_first_principles.md) 追问底层假设

### 日常参考 🔧

1. 查 [irobot-create3_code.md](irobot-create3_code.md) ROS 2 命令速查
2. 查 [irobot-create3_concepts.md](irobot-create3_concepts.md) Topic/Action/Service 速查表
3. 查 [irobot-create3_pitfalls.md](irobot-create3_pitfalls.md) 排查仿真和通信问题

### 深度研究 🔬

1. 读 [irobot-create3_history.md](irobot-create3_history.md) 完整演进线
2. 读 [irobot-create3_first_principles.md](irobot-create3_first_principles.md) 接口等价性公理
3. 读 [irobot-create3_bridge.md](irobot-create3_bridge.md) 对比 TurtleBot 等替代方案

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
| Map | 2026-03-21 | 12m | ✅ current |
| Concepts | 2026-03-21 | 12m | ✅ current |
| Math | 2026-03-21 | 12m | ✅ current |
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
| Soragna et al., [ROS 2 Node Composition](https://arxiv.org/abs/2305.09933), IEEE RA-L 2023 | 📖 论文 | Create 3 嵌入式 ROS 2 架构 |
| Koenig & Howard, [Gazebo IROS 2004](https://doi.org/10.1109/IROS.2004.1389727) | 📖 论文 | 仿真器的学术基础 |
| Quigley et al., [ROS ICRA 2009](https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf) | 📖 论文 | ROS 中间件架构 |
| Sutton & Barto, [《RL: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf) Ch.1 | 📚 教科书 | RL Agent-环境交互框架 |
| [Create 3 Docs](https://iroboteducation.github.io/create3_docs/) | 📖 文档 | 全文核心参考 |
| [Create 3 Hardware Overview](https://iroboteducation.github.io/create3_docs/hw/overview/) | 📖 文档 | 传感器/执行器硬件 |
| [Create 3 ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/) | 📖 文档 | ROS 2 Topics/Services/Actions |
| [Create 3 Simulator Setup](https://iroboteducation.github.io/create3_docs/sim/setup/) | 📖 文档 | Gazebo 仿真部署 |
| [create3_sim GitHub](https://github.com/iRobotEducation/create3_sim) | 💻 源码 | 仿真器源码和 URDF |
| [irobot_create_msgs GitHub](https://github.com/iRobotEducation/irobot_create_msgs) | 💻 源码 | 自定义 ROS 2 消息定义 |
| [create3_examples GitHub](https://github.com/iRobotEducation/create3_examples) | 💻 源码 | 示例代码 |
| [ROS 2 Humble Docs](https://docs.ros.org/en/humble/) | 📖 文档 | ROS 2 通信机制 |
| [Gazebo Classic Tutorials](https://classic.gazebosim.org/tutorials) | 📖 文档 | URDF/SDF/Gazebo 插件 |
