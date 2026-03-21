---
topic: ros2
dimension: concepts
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Macenski et al., 'Robot Operating System 2: Design, architecture, and uses in the wild', Science Robotics 2022 — https://doi.org/10.1126/scirobotics.abm6074"
  - "📖 Docs: ROS 2 Humble — https://docs.ros.org/en/humble/"
  - "📖 Docs: DDS Specification — https://www.omg.org/spec/DDS/"
expiry: 12m
status: current
---

# ROS 2 核心概念

> 📖 Paper: Macenski et al., [Robot Operating System 2](https://doi.org/10.1126/scirobotics.abm6074), Science Robotics 2022
> 📖 Docs: [ROS 2 Humble](https://docs.ros.org/en/humble/)

---

## 术语定义

### ROS 2 (Robot Operating System 2)

一套用于构建机器人应用的开源软件库和工具集。名字叫"操作系统"但实际上**不是操作系统**。它是一个**中间件框架**——在操作系统（Ubuntu）之上、在应用代码之下，帮你解决机器人开发中最头疼的"模块间通信"问题。你写的感知模块、决策模块、控制模块各自独立运行，ROS 2 负责让它们互相说话。

> 别名：**ROS2**（无空格写法）/ **Robot Operating System 2**（全称）— 社区中"ROS 2"和"ROS2"混用，官方推荐用空格写"ROS 2"

> 易混淆：**ROS 1** — ROS 的第一代，基于 Master 节点的中心化架构；ROS 2 改为无 Master 的分布式架构，底层换成了工业级 DDS 协议

> 📖 Paper: Macenski et al. 2022, Section I

### 节点 (Node)

ROS 2 中的基本计算单元。每个节点是一个独立进程，负责**单一功能**——比如一个节点读摄像头、一个节点做目标检测、一个节点控制电机。节点之间通过 Topic/Service/Action 通信。就像工厂里的工人，每人只做一件事，通过传送带传递工件。

> 别名：**ROS Node** / **计算图节点** — 在 ROS 2 中，所有活跃节点组成"计算图"(Computation Graph)

> 📖 Docs: [About Nodes](https://docs.ros.org/en/humble/Concepts/Basic/About-Nodes.html)

### 话题 (Topic)

节点之间**异步**通信的消息管道。一个节点向话题**发布 (Publish)** 消息，其他节点**订阅 (Subscribe)** 该话题接收消息。发布者和订阅者互相不知道对方的存在（匿名通信），多对多关系。就像广播电台——电台播音，所有收音机都能收听，电台不在乎有几台收音机。

> 易混淆：**Service** — Topic 是异步单向广播（发了就不管），Service 是同步请求-响应（必须等回复）

> 📖 Docs: [About Topics](https://docs.ros.org/en/humble/Concepts/Basic/About-Topics.html)

### 服务 (Service)

节点之间**同步**通信的请求-响应模式。客户端发送请求，服务端处理后返回响应。适合"问一次、答一次"的场景——比如"给我当前电池电量"。不像 Topic 那样持续流式推送。

> 易混淆：**Topic** — Topic 是持续流（摄像头每33ms一帧），Service 是一次性问答（查电量）

> 📖 Docs: [About Services](https://docs.ros.org/en/humble/Concepts/Basic/About-Services.html)

### 动作 (Action)

Topic + Service 的结合体。用于**长时间运行**的任务——比如"导航到目标点"。支持三个功能：(1) 发送目标 Goal，(2) 持续收到反馈 Feedback（还有多远），(3) 最终得到结果 Result（到了没）。还可以中途取消。

> 易混淆：**Service** — Service 只能等最终结果（阻塞），Action 还能实时收到中间反馈，加上可取消

> 📖 Docs: [About Actions](https://docs.ros.org/en/humble/Concepts/Basic/About-Actions.html)

### 消息 (Message / msg)

ROS 2 中 Topic 通信的数据格式定义。是**强类型**的数据结构——比如 `geometry_msgs/Twist` 定义了线速度和角速度各三个分量。消息类型在编译时检查，避免运行时数据格式不匹配。

> 📖 Docs: [About Interfaces](https://docs.ros.org/en/humble/Concepts/Basic/About-Interfaces.html)

### Twist 消息 (geometry_msgs/Twist)

ROS 2 中表达速度命令的标准消息类型。包含两个三维向量：**linear** (线速度: x 前进, y 横移, z 升降) 和 **angular** (角速度: x 横滚, y 俯仰, z 偏航)。在 RL 中，Agent 的动作通常通过 Twist 消息发送给机器人。

> 📖 Docs: [geometry_msgs/Twist](https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html)

### DDS (Data Distribution Service)

ROS 2 底层的**通信协议标准**，由 OMG (Object Management Group) 定义。DDS 是工业级的发布/订阅中间件标准，被用在航空、军事、金融等关键领域。ROS 2 不自己发明通信协议，而是站在 DDS 的肩膀上——这是 ROS 2 与 ROS 1 最根本的架构区别。

> 别名：**Data Distribution Service for Real-Time Systems**（全称）— OMG 标准名

> 易混淆：**TCPROS** — ROS 1 自己发明的通信协议；ROS 2 换成了标准化的 DDS

> 📖 Paper: Macenski et al. 2022, Section II-A; 📖 Docs: [DDS Spec](https://www.omg.org/spec/DDS/)

### QoS (Quality of Service)

DDS 提供的通信质量配置机制。可以控制消息的**可靠性 (Reliable/Best Effort)**、**持久性 (Volatile/Transient Local)**、**队列深度 (Depth)** 等。比如传感器数据允许丢包用 Best Effort，安全命令必须到达用 Reliable。

> 易混淆：**DDS QoS Profiles** — ROS 2 预定义了一些常用 QoS 配置（sensor_data、system_default），不需要从头配

> 📖 Paper: Macenski et al. 2022, Section II-B

### 计算图 (Computation Graph)

ROS 2 系统中所有活跃节点和它们之间的 Topic/Service/Action 连接组成的网络。可以把它想象成一张电路图——节点是元件，Topic/Service/Action 是导线。`ros2 node list` 和 `rqt_graph` 命令可以查看。

> 📖 Docs: [ROS 2 Concepts](https://docs.ros.org/en/humble/Concepts/Basic.html)

### 包 (Package)

ROS 2 中代码组织的基本单位。一个 Package 包含相关的节点、消息定义、launch 文件和配置文件。就像 Python 的 pip 包——`ros2 pkg create` 创建，`colcon build` 编译。

> 📖 Docs: [Creating a Package](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)

### Launch 文件 (Launch File)

一次性启动多个节点、加载参数、执行初始化操作的脚本。可以用 Python 或 XML 写。比如一个 Launch 文件可以同时启动 Gazebo 仿真器 + Create 3 模型 + Rviz 可视化 + RL Agent 节点。

> 📖 Docs: [About Launch](https://docs.ros.org/en/humble/Concepts/Basic/About-Launch.html)

### 参数 (Parameter)

节点的运行时配置值。不需要修改代码就能改变节点行为——比如改摄像头分辨率、改控制频率。可以在启动时通过 Launch 文件设置，也可以运行时动态修改。

> 📖 Docs: [About Parameters](https://docs.ros.org/en/humble/Concepts/Basic/About-Parameters.html)

### colcon

ROS 2 的**构建工具**。替代了 ROS 1 的 catkin_make / catkin build。支持同时编译多个 Package，支持并行编译。

> 别名：**collective construction** — colcon 名字的来源

> 易混淆：**catkin** — ROS 1 的构建工具，ROS 2 不再使用

> 📖 Docs: [Building Packages](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)

### 工作空间 (Workspace)

包含一个或多个 Package 的目录。`colcon build` 在工作空间根目录执行，构建所有 Package。每个工作空间下有 `src/`（源码）、`build/`（构建产物）、`install/`（安装产物）和 `log/`（日志）。

> 📖 Docs: [Creating a Workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)

### ROS 2 Humble Hawksbill

ROS 2 的一个**长期支持 (LTS)** 发布版本，代号"Humble Hawksbill"。2022 年 5 月发布，支持到 2027 年 5 月。课程使用此版本。运行在 Ubuntu 22.04 上。

> 易混淆：**其他版本** — Galactic (EOL)、Foxy (EOL)、Jazzy (2024)、Rolling (滚动开发版)

> 📖 Docs: [ROS 2 Releases](https://docs.ros.org/en/humble/Releases.html)

---

## 概念辨析

### Topic vs Service vs Action

| 维度 | Topic | Service | Action |
|------|-------|---------|--------|
| **通信模式** | 发布/订阅（异步） | 请求/响应（同步） | 目标/反馈/结果（异步） |
| **方向** | 多对多，单向广播 | 一对一，双向 | 一对一，长时间 |
| **持续性** | 持续流 | 一次性 | 长时间 + 中间反馈 |
| **典型场景** | 传感器数据流 | 查询状态 | 导航到目标点 |
| **可取消** | ❌ 不适用 | ❌ 不支持 | ✅ 支持 |
| **示例** | `/camera/image` | `GetBatteryState` | `NavigateToPose` |

> 📖 Docs: [ROS 2 Concepts](https://docs.ros.org/en/humble/Concepts/Basic.html)

### ROS 1 vs ROS 2

| 维度 | ROS 1 | ROS 2 |
|------|-------|-------|
| **通信协议** | 自研 TCPROS/UDPROS | 标准 DDS |
| **架构** | 中心化 (需要 rosmaster) | 分布式 (去中心化) |
| **实时性** | ❌ 不支持 | ✅ 通过 DDS QoS |
| **安全性** | ❌ 无认证 | ✅ DDS-Security (SROS2) |
| **跨平台** | 仅 Linux | Linux/Windows/macOS |
| **多机器人** | 困难 | ✅ Domain ID 隔离 |
| **构建工具** | catkin | colcon |
| **Python 版本** | Python 2 | Python 3 |

> 📖 Paper: Macenski et al. 2022, Section II

### Gazebo vs ROS 2

| 维度 | Gazebo | ROS 2 |
|------|--------|-------|
| **定位** | 3D 物理仿真平台 | 通信中间件框架 |
| **功能** | 模拟物理/传感器/渲染 | 节点间消息通信 |
| **关系** | 需要 ROS 2 与 Agent 通信 | 需要 Gazebo 提供仿真环境 |
| **独立使用** | ✅ 可以独立运行 | ✅ 可以独立运行 |

> 📖 Docs: [Gazebo-ROS 2 Integration](https://gazebosim.org/docs)

---

## 核心属性

### ROS 2 系统架构图

```
    ┌─────────────────────────────────────────────────────┐
    │                    应用层                            │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
    │  │ 感知节点  │  │ 决策节点  │  │ 控制节点  │          │
    │  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
    ├───────┼──────────────┼──────────────┼───────────────┤
    │       │    ROS 2 中间件层           │               │
    │       │  ┌──────────────────────┐   │               │
    │       └──│  rclpy / rclcpp      │───┘               │
    │          │  (Client Library)    │                    │
    │          └──────────┬───────────┘                    │
    │                     │                                │
    │          ┌──────────┴───────────┐                    │
    │          │  RMW (ROS MiddleWare) │                   │
    │          └──────────┬───────────┘                    │
    │                     │                                │
    │          ┌──────────┴───────────┐                    │
    │          │  DDS 实现             │                   │
    │          │  (FastDDS/CycloneDDS) │                   │
    │          └──────────────────────┘                    │
    ├─────────────────────────────────────────────────────┤
    │                  操作系统层                           │
    │             (Ubuntu 22.04 / Windows)                 │
    └─────────────────────────────────────────────────────┘
```

### 适用场景 ✅

- 多传感器融合的机器人系统
- 需要模块化、可复用组件的机器人开发
- 仿真与真实机器人之间零修改切换（Sim-to-Real）
- RL Agent 与仿真环境的通信桥梁
- 多机器人协同系统

### 不适用场景 ❌

- 简单的单一脚本（杀鸡不用牛刀）
- 极低延迟的嵌入式硬实时系统（微秒级）
- 无网络通信需求的纯算法研究
- 资源受限的微控制器（Arduino 级别）

> 📖 Paper: Macenski et al. 2022, Section IV

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| Node | 独立计算进程 | camera_node, controller_node |
| Topic | 异步消息管道 | `/cmd_vel`, `/scan`, `/camera/image` |
| Service | 同步请求-响应 | `/get_battery_state` |
| Action | 长时间任务 | `/navigate_to_pose` |
| Message | 消息数据格式 | `geometry_msgs/Twist` |
| QoS | 通信质量配置 | Reliable, Best Effort |
| Package | 代码组织单位 | `my_robot_pkg` |
| Workspace | Package 集合目录 | `~/ros2_ws/` |
| Launch | 多节点启动脚本 | `robot_launch.py` |
| colcon | 构建工具 | `colcon build --symlink-install` |
| DDS | 底层通信协议 | FastDDS, CycloneDDS |
| Humble | LTS 版本 (2022-2027) | Ubuntu 22.04 配套 |
