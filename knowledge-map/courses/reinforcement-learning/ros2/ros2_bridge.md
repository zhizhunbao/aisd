---
topic: ros2
dimension: bridge
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Macenski et al., 'Robot Operating System 2', Science Robotics 2022 — file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf"
  - "📖 Docs: ROS 2 Humble — https://docs.ros.org/en/humble/"
  - "🧪 课件: CST8509 Week 7 — Gazebo + Dynamic Programming + Monte Carlo"
expiry: 12m
status: current
---

# ROS 2 桥接（衔接其他主题）

> 📖 Paper: [Macenski et al. 2022](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf)
> 📖 Docs: [ROS 2 Humble](https://docs.ros.org/en/humble/)

---

## 上游依赖（学 ROS 2 之前需要会什么？）

| 前置主题 | 需要掌握到什么程度 | 到哪补 |
|---------|------------------|-------|
| **Linux 命令行** | `cd/ls/source/export/管道` 基本操作 | 任何 Linux 入门教程 |
| **Python 3** | 类、回调函数、面向对象 | Python 官方教程 |
| **网络通信概念** | IP/端口/TCP/UDP 的区别 | 计算机网络课 |
| **RL 基础概念** | Agent-环境交互、状态/动作/奖励 | [RL 课程知识地图](../README.md) |

---

## 下游影响（ROS 2 是哪些主题的前置？）

| 后续主题 | 怎么用到 ROS 2 | 链接 |
|---------|---------------|------|
| **Gazebo 仿真器** | Gazebo 通过 ROS 2 Topic 与 Agent 通信；`/cmd_vel` 控制机器人、`/scan` 接收传感器 | [gazebo_map.md](../gazebo/gazebo_map.md) |
| **iRobot Create 3** | Create 3 是原生 ROS 2 机器人；所有控制和传感都通过 ROS 2 Topic/Action | [irobot-create3_map.md](../irobot-create3/irobot-create3_map.md) |
| **Rviz 可视化** | Rviz 订阅 ROS 2 Topic 来渲染传感器数据、机器人模型、导航路径 | [rviz_map.md](../rviz/rviz_map.md) |
| **RL Agent 部署** | RL Agent 作为 ROS 2 Node，通过 Topic 接收状态 (observation)、发送动作 (action) | 课程 Lab 3+ |
| **Sim-to-Real** | 同一套 ROS 2 接口，仿真和真实机器人零修改切换 | 课程最终项目 |

---

## 概念流向图

```
    ┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
    │ Linux 基础   │     │   Python 3   │     │ 网络通信概念      │
    └──────┬──────┘     └──────┬───────┘     └────────┬─────────┘
           │                   │                      │
           └───────────────────┼──────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │     ROS 2        │ ← 你在这里
                    │  (通信中间件)     │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌──────────────┐ ┌───────────┐ ┌──────────────┐
     │   Gazebo      │ │  Create 3  │ │    Rviz       │
     │  (仿真环境)   │ │ (真实机器人)│ │  (可视化)     │
     └──────┬───────┘ └─────┬─────┘ └──────────────┘
            │               │
            └───────┬───────┘
                    │
                    ▼
          ┌──────────────────┐
          │   RL Agent 部署   │
          │  (Sim-to-Real)   │
          └──────────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │ DP / MC / TD     │
          │ (RL 核心算法)     │
          └──────────────────┘
```

---

## 概念演化

| ROS 2 概念 | 在 Gazebo 中的体现 | 在 Create 3 中的体现 |
|-----------|-------------------|---------------------|
| **Node** | Gazebo 自身是一组 Node | Create 3 驱动程序是 Node |
| **Topic `/cmd_vel`** | 仿真中控制虚拟机器人速度 | 真实中控制物理机器人速度 |
| **Topic `/scan`** | Gazebo 模拟激光雷达数据 | Create 3 真实 IR 传感器数据 |
| **Twist 消息** | Agent 输出动作 → Gazebo 执行 | Agent 输出动作 → Create 3 执行 |
| **Launch 文件** | 一键启动 Gazebo + 模型 + Agent | 一键启动 Create 3 驱动 + Agent |
| **QoS** | 仿真中 Best Effort 丢帧可接受 | 真实中 Reliable 确保命令到达 |

> 📖 这就是 Sim-to-Real 的核心：**同一套 ROS 2 接口，只换 Launch 文件里的一行参数**

---

## RL 课程中的位置

```
Week 1-4: RL 理论基础（MDP, Bellman, DP, MC, TD）
              │
              ▼
Week 7:   实践桥梁
              │
    ┌─────────┼──────────┐
    │         │          │
    ▼         ▼          ▼
  ROS 2    Gazebo    Create 3
  (通信)   (仿真)    (硬件)
    │         │          │
    └─────────┼──────────┘
              │
              ▼
Week 8+:  RL Agent 在仿真/真实环境中训练
              │
              ▼
          Sim-to-Real 部署
```

---

## 扩展阅读

### 入门级 📗

| 资源 | 说明 |
|------|------|
| [ROS 2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html) | 官方入门教程，从安装到第一个 Node |
| [The Robotics Back-End](https://roboticsbackend.com/category/ros2/) | 实战导向的 ROS 2 博客 |

### 进阶级 📙

| 资源 | 说明 |
|------|------|
| [ROS 2 Design Docs](https://design.ros2.org/) | ROS 2 架构设计决策文档 |
| [Nav2 Documentation](https://docs.nav2.org/) | 导航框架，ROS 2 原生最重要的应用框架 |
| [MoveIt 2](https://moveit.ai/) | 机械臂操控框架 |

### 学术级 📕

| 资源 | 说明 |
|------|------|
| [Macenski et al. 2022](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf) | ROS 2 架构论文，Science Robotics |
| [Quigley et al. 2009](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/icraoss09-ROS.pdf) | ROS 1 原始论文，理解起源 |
| [DDS Specification](https://www.omg.org/spec/DDS/) | DDS 协议标准文档 |
