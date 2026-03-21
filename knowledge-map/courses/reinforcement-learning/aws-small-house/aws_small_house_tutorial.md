---
topic: aws_small_house
dimension: tutorial
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: AWS RoboMaker Small House World — https://github.com/aws-robotics/aws-robomaker-small-house-world"
  - "📖 Docs: iRobot Create 3 Simulator — https://iroboteducation.github.io/create3_docs/sim/setup/"
  - "📖 Docs: CST8509 Lab 3 Gazebo — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/labs/CST8509_Lab3_Gazebo.md"
expiry: 12m
status: current
---

# AWS Small House 教程

> **前置知识：** Gazebo Classic 11 已安装、ROS 2 Humble 已配置、create3_sim 已克隆
> **参考来源：** [AWS Small House README](https://github.com/aws-robotics/aws-robomaker-small-house-world), [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md)

---

## Section 0: 前置知识速查

1. **Gazebo Classic 11**：已通过 `sudo apt install gazebo` 或 `curl -sSL http://get.gazebosim.org | sh` 安装
2. **ROS 2 Humble Desktop**：已通过 `sudo apt install ros-humble-desktop` 安装
3. **create3_sim 工作空间**：已在 `~/create3_ws/` 中克隆并切换到 humble 分支
4. **colcon**：ROS 2 构建工具已可用
5. **Ubuntu 22.04**：本教程基于 Ubuntu 22.04 环境

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **没有逼真环境**：Create 3 仿真器启动后只有空白世界——机器人在一片虚无中转圈，没有墙壁可以撞、没有走廊可以导航、没有家具可以避让
- 🔥 **自建世界代价巨大**：从零用 Blender/FreeCAD 建一个多房间住宅模型，仅 3D 建模就需要数天。墙壁厚度、门框尺寸、家具比例都要符合真实世界才有训练价值
- 🔥 **训练无意义**：在空白世界中做 RL 导航训练，学到的策略无法迁移到真实室内环境——因为训练时根本没见过墙壁和障碍物
- 🔥 **不可复现**：如果每个学生自建世界，训练结果无法对比——因为环境不同，策略也不同

### 它的核心价值

1. **即用即得的逼真室内环境**：AWS Robotics 团队用专业工具建好了一套完整的住宅——多个房间、走廊、家具、画框，质量远超学生或普通开发者的自建水平
2. **与 Create 3 无缝集成**：这个世界专门为 ROS 2 + Gazebo Classic 11 设计，Create 3 可以直接在里面``spawn``并开始导航
3. **标准化训练环境**：所有学生用同一个世界，训练结果可对比、可复现
4. **零额外开发**：不需要懂 3D 建模，`colcon build` 后直接可用

> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md), Section 6

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 架构：从仓库到仿真运行

    ┌──────────────────────────────────────────────────────────────┐
    │                      ROS 2 工作空间 (~/create3_ws/)          │
    │                                                              │
    │  ┌──────────────┐    ┌──────────────────┐    ┌───────────┐  │
    │  │ create3_sim   │    │ aws_small_house   │    │ colcon    │  │
    │  │ (机器人描述)  │    │ (世界 + 家具模型) │    │ (构建)    │  │
    │  └──────┬───────┘    └────────┬─────────┘    └─────┬─────┘  │
    │         │                     │                     │        │
    │         └─────────┬──────────┘                     │        │
    │                   ▼                                 │        │
    │         ┌──────────────────┐         colcon build   │        │
    │         │  Launch 文件      │←──────────────────────┘        │
    │         │  (一键启动一切)   │                                │
    │         └────────┬─────────┘                                │
    │                  │                                          │
    │    ┌─────────────┼─────────────┐                           │
    │    ▼             ▼             ▼                           │
    │ gzserver      gzclient     ROS 2 节点                      │
    │ (物理仿真)   (3D 渲染)    (Topic 发布)                     │
    └──────────────────────────────────────────────────────────────┘

### 2.2 核心机制

**为什么用 SDF World 而不是直接在 Launch 中逐个加载模型？**

SDF World 文件是声明式的——"我要这些东西在这些位置"。如果用 Launch 文件逐个 `spawn` 每个家具，会导致：
- 启动顺序依赖问题
- 相对位置难以维护
- 光源和物理参数分散在多个地方

World 文件把整个场景打包成一个单元，Gazebo 服务端一次性加载完毕。

**为什么默认所有家具都是 static？**

物理仿真的计算开销与非静态物体数量**成正比**。AWS Small House 有数十件家具，如果全部模拟物理，Gazebo 帧率会暴跌。对于导航 RL 来说，家具不需要被推动——只需要碰撞检测让机器人停下来。

### 2.3 加载流程

    ┌─────────────────┐
    │ colcon build     │
    │ (编译 + 链接)    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ source setup.sh  │    ← 设置 GAZEBO_MODEL_PATH 等环境变量
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ ros2 launch ...  │    ← Launch 文件启动一切
    └────────┬────────┘
             │
    ┌────────┴────────────────────────────┐
    │                                      │
    ▼                                      ▼
    ┌───────────────────┐    ┌────────────────────────┐
    │ gzserver 读取      │    │ ROS 2 节点 spawn       │
    │ small_house.world  │    │ Create 3 到世界中      │
    │ + 加载所有家具模型 │    │ + 启动传感器插件       │
    └───────────────────┘    └────────────────────────┘

> 📖 Docs: [AWS Small House README](https://github.com/aws-robotics/aws-robomaker-small-house-world)

---

## Section 3: 局限性

1. **只有室内场景** → 如果需要室外仿真（草坪、马路），需要用其他 World 或自建
2. **家具是静态的** → 机器人不能开门、推椅子，如需动态交互要手动修改 `<static>` 标记并校准质量/惯性参数
3. **纹理质量有限** → 相框里的照片可以替换，但家具纹理精度有限，不适合需要精细视觉识别的训练
4. **Gazebo Classic 限定** → 仅兼容 Classic Gazebo 11，不直接兼容 Ignition Gazebo/Gazebo Sim
5. **仓库维护状态** → AWS 官方仓库更新不频繁，可能存在与最新 Gazebo/ROS 2 版本的兼容性问题

> 📖 Docs: [AWS Small House README — Disclaimer](https://github.com/aws-robotics/aws-robomaker-small-house-world)

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **AWS Small House** | 即用即得、多房间真实布局 | 只有室内、不可太定制 | CST8509 Lab 3、导航 RL 训练 |
| **Gazebo 空白世界** | 最简单、零依赖 | 无障碍物、无训练价值 | 测试机器人模型加载 |
| **自建 Gazebo World** | 完全可控 | 巨大开发投入 | 特殊研究场景 |
| **AWS Bookstore** | 书架通道、搜索场景 | 更窄的空间 | 物品搜索 RL |
| **AWS Small Warehouse** | 大面积仓库 | 过于空旷 | 仓库物流 RL |
| **NVIDIA Isaac Sim** | 最先进渲染、GPU 加速 | 硬件要求极高、非 Gazebo | 工业级 Sim-to-Real |

> 📖 Docs: [AWS RoboMaker](https://aws.amazon.com/robomaker/)

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [AWS Small House README](https://github.com/aws-robotics/aws-robomaker-small-house-world) | 💻 源码 | 全文核心参考 |
| [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md) | 📖 课程实验 | Section 2 加载流程 |
| [iRobot Create 3 Docs](https://iroboteducation.github.io/create3_docs/sim/setup/) | 📖 文档 | Section 2 机器人集成 |
| [Gazebo Classic Tutorials](https://classic.gazebosim.org/tutorials) | 📖 文档 | Section 2 SDF 格式 |
