---
topic: gazebo
dimension: history
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: Gazebo History — https://gazebosim.org/about"
  - "📖 Paper: Koenig & Howard, 'Design and Use Paradigms for Gazebo', IROS 2004"
expiry: never
status: current
---

# Gazebo 仿真器的故事线：从大学实验室到 RL 训练基础设施

> **核心主题：** 机器人仿真从学术工具变成 RL 训练的必备基础设施
> **故事线：** 一个不断追问"怎么让机器人在不摔的情况下学会走路"的技术演进

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 真实机器人太贵、太慢、太脆弱——有没有办法在虚拟世界里训练完，再部署到现实？

2000 年代初，机器人研究者面临一个尴尬的现实：你写了一个导航算法，想测试它。但你只有一台价值几万美元的机器人。如果算法有 bug，机器人撞墙了怎么办？更别提测试需要跑几百次，电池不够、时间不够、人手不够。

> 🔑 **问题提出：** 需要一个物理级别精确的仿真器，让机器人算法在虚拟世界里"先练几百遍"

---

## 📚 第一章：Player/Stage 时代（2000-2004）

> **关键人物：** Brian Gerkey, Andrew Howard, Nate Koenig
> **关键项目：** Player/Stage/Gazebo

### 发生了什么？

2000 年前后，USC（南加州大学）的机器人实验室创建了 **Player/Stage** 项目：
- **Player**：机器人的网络服务器，提供传感器和执行器的统一接口
- **Stage**：2D 多机器人仿真器，能同时仿真几百个简单机器人

但 Stage 只是 2D 的——不能仿真 3D 物理（重力、碰撞、关节）。2004 年，Nate Koenig 和 Andrew Howard 在 USC 创建了 **Gazebo**——一个 3D 物理仿真器，可以仿真室内/室外环境中的真实机器人。

### 为什么这很重要？

Gazebo 是第一个开源的、带物理引擎的 3D 机器人仿真器。它让研究者第一次可以在笔记本上跑完整的机器人实验，然后直接把代码部署到真实机器人上（虽然 Sim-to-Real Gap 还是个问题）。

### 但还有一个问题……

早期 Gazebo 和 Player 绑定，界面简陋，物理引擎不够精确。而且每个实验室各写各的接口，机器人之间无法互通。

> 🔑 **故事转折点：** 需要一个统一的机器人中间件——ROS 诞生了

---

## 📚 第二章：ROS + Gazebo 联姻（2007-2012）

> **关键人物：** Willow Garage, Morgan Quigley
> **关键事件：** ROS 发布 (2007), Gazebo 与 ROS 集成

### 发生了什么？

2007 年，Willow Garage 公司发布了 **ROS (Robot Operating System)**——第一个被广泛采用的机器人中间件。ROS 提供了标准化的消息格式（Topic/Service/Action）、包管理器、调试工具。

Gazebo 迅速与 ROS 集成，成为 ROS 生态中事实上的标准仿真器。`gazebo_ros_pkgs` 桥接包让 Gazebo 中的虚拟传感器可以发布标准 ROS 话题——对 Agent 来说，虚拟摄像头和真实摄像头说的是同一种"语言"。

### 为什么这很重要？

ROS + Gazebo 组合解决了"仿真和真实用不同接口"的问题。代码在仿真中跑通了，换到真实机器人只需要改 launch 文件——不需要改一行算法代码。这为后来 RL 在机器人上的应用铺好了路。

### 但还有一个问题……

ROS 1 不支持实时系统、有安全隐患、单点故障（roscore）。Gazebo 的架构也越来越老旧，难以支持大规模并行仿真。

> 🔑 **故事转折点：** ROS 2 重写了底层，Gazebo 也要重生

---

## 📚 第三章：双线并行——Classic vs Ignition（2014-2022）

> **关键事件：** ROS 2 发布 (2017), Ignition Gazebo 发布 (2019), Ignition 更名为 Gazebo Sim (2022)

### 发生了什么？

2017 年 ROS 2 正式发布，改用 DDS 中间件，解决了 ROS 1 的大部分问题。同时 Open Robotics 开始开发 **Ignition Gazebo**——Gazebo 的全新重写版本，模块化架构，支持更好的物理引擎和渲染。

2022 年 Ignition Gazebo 更名为"Gazebo"（和旧版同名！），造成了极大的命名混乱：
- 旧版：Classic Gazebo / Gazebo 11
- 新版：Gazebo Sim / Gazebo Harmonic / Gazebo（不加后缀）

### 为什么这很重要？

课程选择 Classic Gazebo 11 是因为：
1. Create 3 的仿真包已经为 Classic 写好了
2. ROS 2 Humble 与 Classic 兼容性成熟
3. 社区教程丰富，出了问题好查

但长期来看，新版 Gazebo Sim 是未来方向。

### 但还有一个问题……

深度强化学习需要**大规模并行**（同时跑几千个仿真实例）。Gazebo 的架构不太适合这种场景。

> 🔑 **故事转折点：** NVIDIA Isaac Sim 和 MuJoCo 开始抢 Gazebo 的 RL 市场

---

## 📚 第四章：RL 仿真器竞争格局（2020-今）

> **关键事件：** MuJoCo 开源 (2022), Isaac Sim + Isaac Gym, Gazebo 融入 ROS 2 生态

### 发生了什么？

2020 年代，RL 训练对仿真器提出了新需求：要快（GPU 并行）、要准（物理精确）、要易用（Gymnasium 接口）。三个主要竞争者出现：

- **MuJoCo**：DeepMind 2022 开源，物理精度最高，Gymnasium 原生支持，成为 RL 研究标准
- **Isaac Sim**：NVIDIA 推出，GPU 并行支持最好，可以同时跑数千个环境实例
- **Gazebo**：ROS 2 生态最强，机器人应用最成熟，但 GPU 并行能力弱

Gazebo 的定位逐渐从"通用仿真器"转向"ROS 2 生态中的机器人应用仿真器"——特别适合需要 ROS 2 话题通信的真实机器人部署场景（正是课程的使用场景）。

### 为什么这很重要？

对课程来说：Gazebo 是完美选择，因为目标是"在仿真中训练 Create 3 然后部署到真实机器人"。ROS 2 + Gazebo 提供了最平滑的 Sim-to-Real 路径。

---

## 🗺️ 全局回顾：技术演进路线图

```mermaid
graph LR
    A["🤖 Player/Stage\n2D 仿真 2000\nUSC"] --> B["🏗️ Gazebo 诞生\n3D 物理仿真 2004\nKoenig & Howard"]
    B --> C["🔗 ROS + Gazebo\n统一中间件 2007-12\nWillow Garage"]
    C --> D["🔀 双线并行\nClassic vs Ignition\n2014-22"]
    D --> E["⚔️ RL 仿真竞争\nMuJoCo/Isaac/Gazebo\n2020-今"]
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|------------------|
| 2D 仿真 → Gazebo 3D | 真实世界是 3D 的，需要重力和碰撞 |
| 各自接口 → ROS + Gazebo | 仿真和真实用同一个接口 |
| Classic → Ignition | 老架构扩展不动了 |
| Gazebo → MuJoCo/Isaac 竞争 | RL 需要 GPU 并行和更精确物理 |

---

## 🎥 视觉素材总表（视频制作用）

| 章节 | 事件 | 图片来源 | 版权 |
|------|------|---------|------|
| 第一章 | Player/Stage/Gazebo | USC Robotics Lab | 学术使用 |
| 第二章 | Willow Garage / ROS | Wikimedia Commons | CC BY-SA |
| 第三章 | Classic vs Ignition | gazebosim.org | 开源截图 |
| 第四章 | MuJoCo / Isaac Sim | DeepMind / NVIDIA | 学术引用 |
