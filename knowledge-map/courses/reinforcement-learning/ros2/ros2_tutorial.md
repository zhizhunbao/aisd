---
topic: ros2
dimension: tutorial
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Macenski et al., 'Robot Operating System 2', Science Robotics 2022 — file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf"
  - "📖 Docs: ROS 2 Humble Tutorials — https://docs.ros.org/en/humble/Tutorials.html"
  - "📖 Docs: ROS 2 Design — https://design.ros2.org/"
  - "📖 Paper: Quigley et al., 'ROS: an open-source Robot Operating System', ICRA 2009 — file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/icraoss09-ROS.pdf"
expiry: 12m
status: current
---

# ROS 2 教程

> **前置知识：** Linux 命令行基础、Python 编程、网络通信概念（IP/端口/协议）
> **参考来源：** [ROS 2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html), [Macenski et al. 2022](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf)

---

## Section 0: 前置知识速查

1. **Linux 命令行**：能 `cd`、`ls`、`source`、`export`、管道 `|`
2. **Python 3 基础**：类、函数、回调、异步概念
3. **网络通信概念**：知道什么是 IP 地址、端口、TCP/UDP 的区别
4. **RL 基础（课程上下文）**：Agent-环境交互循环、状态/动作/奖励

> 📖 Docs: [ROS 2 Prerequisites](https://docs.ros.org/en/humble/Tutorials.html)

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **通信噩梦**：你写了一个摄像头模块、一个目标检测模块、一个控制模块，三个独立进程。没有 ROS 2，你得**自己写 Socket 通信**——定义数据格式、处理序列化/反序列化、管理连接断开重连、处理多线程安全。每新增一个模块，通信代码翻倍。

- 🔥 **推倒重来**：换了传感器？换了机器人？所有通信代码全部重写。你的代码和硬件**紧耦合**，无法复用。

- 🔥 **仿真和真实割裂**：在仿真器里训练好的 RL Agent 要部署到真实 Create 3，如果没有统一接口，需要写两套完全不同的通信代码——仿真一套、真实一套。

- 🔥 **团队协作灾难**：三个人各写各的模块，接口不统一，集成的时候花的时间比写代码还多。

### 它的核心价值

1. **标准化通信**：Topic/Service/Action 三种模式覆盖 99% 的机器人通信需求，不用自己发明轮子
2. **模块解耦**：感知/决策/控制各自独立开发、独立测试、独立部署
3. **Sim-to-Real 零修改**：同一套 ROS 2 代码，在 Gazebo 仿真里跑和在真实 Create 3 上跑，一行代码都不用改
4. **庞大生态**：2000+ 开源 Package——导航、视觉、操控、SLAM，不用从头造轮子

> 📖 Paper: Macenski et al. 2022, Section I "Introduction"
> 📖 Paper: Quigley et al. 2009, Section 1 "Introduction"

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 ROS 2 通信生命周期

```
    ┌──────────────────────────────────────────────────────────────┐
    │                     ROS 2 计算图                              │
    │                                                              │
    │   ┌──────────┐    Topic: /scan      ┌──────────┐            │
    │   │ 激光雷达  │──── publish ────────→│ 导航规划  │            │
    │   │  Node    │                      │  Node    │            │
    │   └──────────┘                      └────┬─────┘            │
    │                                          │                  │
    │   ┌──────────┐    Topic: /cmd_vel        │                  │
    │   │ 电机控制  │←─── subscribe ────────────┘                  │
    │   │  Node    │                                              │
    │   └──────────┘                                              │
    │                                                              │
    │   ┌──────────┐    Service: /get_map  ┌──────────┐            │
    │   │ 地图服务  │←─── request ─────────│ 规划器   │            │
    │   │  Node    │──── response ────────→│  Node    │            │
    │   └──────────┘                      └──────────┘            │
    └──────────────────────────────────────────────────────────────┘
```

### 2.2 核心机制

**为什么用 DDS 而不是自己写通信协议？**

ROS 1 自己发明了 TCPROS/UDPROS 协议。结果十年后发现：

| 问题 | ROS 1 自研协议 | DDS 标准 |
|------|---------------|----------|
| 实时性 | ❌ 无保障 | ✅ QoS 可配置 |
| 安全性 | ❌ 无认证 | ✅ DDS-Security |
| 可靠性 | ❌ 单 Master 挂了全挂 | ✅ 去中心化发现 |
| 跨平台 | ❌ 仅 Linux | ✅ Linux/Windows/macOS |
| 标准化 | ❌ ROS 专用 | ✅ OMG 国际标准 |

DDS 已经在航空（飞行控制）、军事（战场网络）、金融（交易系统）等关键领域使用了 20 年。ROS 2 不重复发明轮子，直接复用这些经过战场验证的基础设施。

> 📖 Paper: Macenski et al. 2022, Section II-A "Middleware layer"

### 2.3 三种通信模式选择指南

```
    你需要通信 ─────→ 数据是持续流？
                          │
                     ┌────┴────┐
                    YES        NO
                     │          │
              用 Topic       需要中间反馈？
              (Pub/Sub)          │
                            ┌───┴───┐
                           YES      NO
                            │        │
                       用 Action   用 Service
                       (Goal +     (Req/Resp)
                        Feedback)
```

> 📖 Docs: [ROS 2 Concepts](https://docs.ros.org/en/humble/Concepts/Basic.html)

---

## Section 3: 局限性

1. **学习曲线陡峭** → 对初学者来说概念太多（Node/Topic/Service/Action/QoS/Launch/Package/Workspace），但可以按"先 Topic → 再 Service → 最后 Action"的顺序渐进学习

2. **性能开销** → DDS 中间层增加了延迟（通常 < 1ms），对微秒级硬实时不够 → 真正的硬实时控制通常直接走 EtherCAT 等协议绕过 ROS 2

3. **版本碎片化** → Foxy/Humble/Jazzy/Rolling 多个版本共存，Package 兼容性问题 → 坚持使用 LTS 版本（当前: Humble）

4. **调试困难** → 分布式系统天生难调试（消息丢了？QoS 不匹配？DDS 发现慢？）→ 使用 `ros2 topic echo` / `rqt_graph` / `ros2 doctor` 工具

> 📖 Paper: Macenski et al. 2022, Section V "Limitations"

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **ROS 2** | 标准化、生态庞大、DDS 工业级 | 学习曲线陡、资源消耗大 | 通用机器人开发、学术研究、RL 训练 |
| **ROS 1** | 文档多、社区成熟 | 无实时性、单 Master、仅 Linux | 遗留项目维护（不推荐新项目） |
| **YARP** | 轻量、iCub 深度集成 | 生态小、社区小 | iCub 类人机器人专用 |
| **OROCOS** | 真正硬实时 | 学习曲线更陡、生态小 | 工业机器人硬实时控制 |
| **自研 Socket** | 完全控制、零依赖 | 重复造轮子、维护噩梦 | 极简嵌入式、一次性原型 |

> 📖 Paper: Macenski et al. 2022, Section I

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Macenski et al. 2022](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf) | 📖 论文 | Section 1-4（全文核心参考） |
| [ROS 2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html) | 📖 文档 | Section 0, 2（官方教程） |
| [ROS 2 Design Docs](https://design.ros2.org/) | 📖 文档 | Section 2（DDS 设计决策） |
| [DDS Specification](https://www.omg.org/spec/DDS/) | 📖 文档 | Section 2（通信协议标准） |
