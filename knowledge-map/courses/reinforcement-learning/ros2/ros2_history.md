---
topic: ros2
dimension: history
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Quigley et al., 'ROS: an open-source Robot Operating System', ICRA 2009 — file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/icraoss09-ROS.pdf"
  - "📖 Paper: Macenski et al., 'Robot Operating System 2', Science Robotics 2022 — file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf"
  - "📖 Docs: ROS 2 Design — https://design.ros2.org/"
  - "📖 Docs: ROS History — https://www.ros.org/blog/history/"
expiry: never
status: current
---

# ROS 2 历史演进

> 📖 Paper: [Quigley et al. 2009](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/icraoss09-ROS.pdf), [Macenski et al. 2022](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf)

---

## 故事线

### 前传 — 机器人软件的黑暗时代（~2006 年前）

**关键矛盾：** 每个实验室都在重复造轮子

2006 年之前，机器人研究者面临一个荒谬的现实：写一个导航程序，90% 的代码在处理通信、驱动、数据格式转换——和"机器人怎么导航"本身无关。斯坦福大学、MIT、CMU 各自有自己的内部框架，互不兼容。一个学生换了实验室，之前写的所有代码都得重写。

> 📖 Paper: Quigley et al. 2009, Section 1 "Introduction"

---

### 第 1 幕 — ROS 诞生：Willow Garage 的赌博（2007-2010）

**关键人物：** Morgan Quigley（斯坦福博士生）、Scott Hassan（Google 早期员工、Willow Garage 创始人）、Brian Gerkey

**剧情：** Quigley 在斯坦福做 STAIR 项目（Stanford AI Robot），写了一个名为 "Switchyard" 的机器人通信框架。2007 年，Scott Hassan 创建 Willow Garage 公司，把 Quigley 和一批顶级机器人工程师招进来，将 Switchyard 的理念发展成 **ROS (Robot Operating System)**。

**核心设计决策：**
- **开源 BSD 许可**：任何人可以免费使用，包括商业用途
- **去中心化 Package 管理**：任何人可以贡献 Package
- **语言无关**：一开始就支持 C++ 和 Python
- **"精瘦核心 + 丰富生态"**：核心只做通信，其他全部是可选 Package

**技术选择：**
- 自研通信协议 TCPROS/UDPROS
- 中心化架构：需要 `rosmaster` 作为注册中心
- 仅支持 Linux

2010 年 Willow Garage 发布 PR2 机器人（成本 40 万美元），免费赠送 11 台给全球实验室，条件是用 ROS 做研究并开源代码。这个策略**极其成功**——ROS 生态爆炸式增长。

> 📖 Paper: Quigley et al. 2009, Section 2-5

---

### 第 2 幕 — ROS 成为事实标准，但裂缝出现（2010-2014）

**剧情：** ROS 从学术界扩展到工业界，暴露出根本性问题：

| 问题 | 痛苦程度 | 根因 |
|------|---------|------|
| rosmaster 单点故障 | 🔴 致命 | 中心化架构——master 挂了所有通信中断 |
| 没有实时性保障 | 🔴 致命 | TCPROS 无 QoS，工业机器人不敢用 |
| 没有安全机制 | 🟡 严重 | 任何人可以发布任何 Topic，无认证 |
| 仅 Linux | 🟡 严重 | Windows/macOS 用户无法参与 |
| Python 2 绑定 | 🟡 严重 | Python 2 即将 EOL |

**关键事件：** 2013 年 Willow Garage 解散（Scott Hassan 撤资），ROS 的维护权转交给新成立的 **Open Robotics**（Brian Gerkey 创立）。

> 📖 Paper: Macenski et al. 2022, Section I

---

### 第 3 幕 — ROS 2 诞生：重新开始（2014-2017）

**剧情：** Open Robotics 意识到 ROS 1 的问题不是修修补补能解决的——需要从头设计。2014 年启动 ROS 2 项目。

**核心设计决策（这次不再自研通信协议）：**

```
    ROS 1 的教训                         ROS 2 的决策
    ─────────────                       ─────────────
    自研 TCPROS 不靠谱          ───→     用工业标准 DDS
    rosmaster 单点故障          ───→     去掉 master，分布式发现
    无实时性                    ───→     DDS QoS 策略
    无安全性                    ───→     DDS-Security (SROS2)
    仅 Linux                   ───→     跨平台 (Linux/Win/Mac)
    Python 2                    ───→     Python 3
    catkin 构建系统              ───→     colcon + ament
```

**为什么选 DDS？** DDS（Data Distribution Service）是 OMG 组织 2004 年就发布的标准，经过航空、军事、金融等行业 10+ 年验证。ROS 2 团队评估了多个选项：

| 方案 | 优点 | 最终决定 |
|------|------|---------|
| 继续用 TCPROS | 兼容 ROS 1 | ❌ 无法满足实时/安全需求 |
| ZeroMQ + Protobuf | 轻量 | ❌ 没有 QoS、没有发现机制 |
| **DDS** | 标准化、实时、安全、已验证 | ✅ 采用 |

> 📖 Paper: Macenski et al. 2022, Section II "Architecture"
> 📖 Docs: [Why DDS](https://design.ros2.org/articles/ros_on_dds.html)

---

### 第 4 幕 — ROS 2 走向成熟（2017-2025）

**版本演进：**

| 时间 | 版本 | 代号 | 关键里程碑 |
|------|------|------|-----------|
| 2017-12 | ROS 2 Ardent | 第一个正式版 | DDS 基础通信、rclcpp/rclpy |
| 2018-12 | ROS 2 Crystal | 生命周期节点 | 节点状态管理 |
| 2019-05 | ROS 2 Dashing | 第一个 LTS | 稳定 API，可用于生产 |
| 2020-06 | ROS 2 Foxy | LTS (2023 EOL) | Nav2 导航框架成熟 |
| 2021-05 | ROS 2 Galactic | 短期支持 | 新 CMake API |
| **2022-05** | **ROS 2 Humble** | **LTS (2027)** | **课程使用版本** ← 你在这里 |
| 2023-05 | ROS 2 Iron | 短期支持 | Type adaptation |
| 2024-05 | ROS 2 Jazzy | LTS (2029) | 最新 LTS |

**生态融合：**
- 2019: **Navigation2 (Nav2)** 发布——ROS 2 原生导航框架
- 2020: **Gazebo Sim** 新一代仿真器，原生 ROS 2 集成
- 2021: **iRobot Create 3** 发布——第一款原生 ROS 2 教育机器人
- 2022: **MoveIt 2** 稳定——ROS 2 原生操控框架
- 2024: Open Robotics 并入 **Intrinsic**（Alphabet 子公司），获得 Google 资源

> 📖 Paper: Macenski et al. 2022, Section III "Ecosystem"

---

## 关键转折点总结

```
2007         2010         2013         2014         2022         2024
  │            │            │            │            │            │
  ▼            ▼            ▼            ▼            ▼            ▼
ROS 诞生    PR2 赠送    Willow 解散   ROS 2 启动   Humble LTS   Intrinsic
(Stanford)  (生态爆发)  (Open Robotics) (DDS 架构)  (课程版本)   (Google)
  │            │            │            │            │            │
  └────────────┴────────────┴────────────┴────────────┴────────────┘
         ROS 1 时代 (自研协议)          ROS 2 时代 (DDS 标准)
```

**核心教训：** 不要自己发明通信协议——站在巨人（DDS）的肩膀上。ROS 2 的成功证明了"复用经过验证的基础设施"远比"从头设计"更明智。

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Quigley et al. 2009](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/icraoss09-ROS.pdf) | 📖 论文 | 第 1-2 幕（ROS 1 起源与设计） |
| [Macenski et al. 2022](file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf) | 📖 论文 | 第 2-4 幕（ROS 2 架构与演进） |
| [ROS 2 Design: Why DDS](https://design.ros2.org/articles/ros_on_dds.html) | 📖 文档 | 第 3 幕（DDS 选型决策） |
| [ROS History](https://www.ros.org/blog/history/) | 📖 文档 | 全文（时间线核实） |
