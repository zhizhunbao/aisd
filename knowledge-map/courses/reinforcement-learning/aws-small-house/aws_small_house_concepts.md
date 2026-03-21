---
topic: aws_small_house
dimension: concepts
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: AWS RoboMaker Small House World — https://github.com/aws-robotics/aws-robomaker-small-house-world"
  - "📖 Docs: Gazebo SDF Specification — http://sdformat.org/spec"
  - "📖 Docs: Gazebo Classic Tutorials — https://classic.gazebosim.org/tutorials"
  - "📖 Docs: CST8509 Lab 3 Gazebo — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/labs/CST8509_Lab3_Gazebo.md"
expiry: 12m
status: current
---

# AWS Small House 核心概念

> 📖 Docs: [AWS RoboMaker Small House World](https://github.com/aws-robotics/aws-robomaker-small-house-world)
> 📖 Docs: [Gazebo SDF Specification](http://sdformat.org/spec)

---

## 术语定义

### 仿真世界 (Gazebo World)

Gazebo 中用于模拟整个场景的容器。一个 World 包含了所有物体（Model）、光源、物理引擎配置和插件。AWS Small House 本质上就是一个 `.world` 文件，它告诉 Gazebo："请加载以下家具、墙壁、地板，用以下物理参数模拟它们。"

`.world` 文件使用 **SDF (Simulation Description Format)** 格式书写，是一个特殊的 XML 文件。

> 易混淆：**World vs Scene** — World 是 Gazebo 特有术语，Scene 在 Unity/Unreal 等游戏引擎中使用，两者概念类似但格式完全不同

> 📖 Docs: [Gazebo World Tutorial](https://classic.gazebosim.org/tutorials?tut=components)

### 模型 (Gazebo Model)

World 中的一个独立物体，例如一张桌子、一把椅子、一面墙。每个 Model 由以下部分组成：

- **Visual**（视觉外观）：3D 网格 + 纹理贴图，决定"看起来像什么"
- **Collision**（碰撞体）：简化的几何体，决定"撞到什么"
- **Inertial**（惯性属性）：质量和惯性矩，决定"被撞时怎么动"

AWS Small House 中的家具模型存放在仓库的 `models/` 目录下，每个模型有自己的 `model.sdf` 和纹理文件。

> 易混淆：**Model vs Link** — Model 是逻辑上的"一个物体"，Link 是 Model 内部的"一个刚体零件"。一个 Model 可以有多个 Link（比如机器人有底盘 Link + 轮子 Link），但一面墙只需要一个 Link

> 📖 Docs: [Gazebo Models](https://classic.gazebosim.org/tutorials?tut=build_model)

### SDF 格式 (Simulation Description Format)

Gazebo 专用的 XML 格式，用来描述仿真世界和模型。SDF 比 URDF 功能更强，支持：

- 光源定义
- 物理引擎参数
- 传感器插件
- 静态和动态物体的混合

AWS Small House 的 `worlds/small_house.world` 文件就是一个 SDF World 文件。

> 易混淆：**SDF vs URDF** — URDF 只能描述机器人（有关节的运动链），SDF 可以描述整个世界（包括静态场景）。Create 3 用 URDF/Xacro 描述，但 AWS Small House 用 SDF 描述

> 📖 Docs: [SDF Specification](http://sdformat.org/spec)

### GAZEBO_MODEL_PATH 环境变量

告诉 Gazebo 去哪里找 Model 文件的环境变量。如果 AWS Small House 的 `models/` 目录没加到这个路径里，Gazebo 就找不到家具模型，世界会加载失败或显示空白。

```bash
export GAZEBO_MODEL_PATH=`pwd`/models
```

> 📖 Docs: [AWS Small House README](https://github.com/aws-robotics/aws-robomaker-small-house-world)

### 静态物体 (Static Model)

AWS Small House 中的所有家具默认都是**静态的**（`<static>true</static>`）。这意味着：

- 物理引擎不会模拟它们的运动——它们不会被推倒
- 碰撞检测仍然有效——机器人撞到墙还是会停下来
- 大幅降低了物理计算的开销

如果需要机器人推开物体，要把 `<static>` 改为 `false`，但此时必须确保质量和惯性参数正确。

> 📖 Docs: [AWS Small House README — Disclaimer](https://github.com/aws-robotics/aws-robomaker-small-house-world)

### Launch 文件 (ROS 2 Launch File)

用于一键启动完整仿真环境的脚本。在 Create3 + AWS Small House 场景中，一个 Launch 文件会同时启动：

1. **Gazebo 服务端** (gzserver) — 运行物理仿真
2. **Gazebo 客户端** (gzclient) — 3D 可视化窗口
3. **Create 3 机器人** — 在 World 中生成 (spawn)
4. **ROS 2 节点** — 发布传感器数据、接收控制命令

> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md), Section 6

### Gazebo 插件 (Gazebo Plugin)

扩展 Gazebo 功能的共享库（`.so` 文件）。AWS Small House 场景中关键的插件：

- `libgazebo_ros_camera.so` — 将 Gazebo 虚拟摄像头图像发布为 ROS 2 Topic
- Create 3 的差速驱动插件 — 接收 `/cmd_vel` 并驱动虚拟轮子
- Create 3 的 IMU/Lidar 插件 — 模拟传感器并发布数据

插件是 Gazebo 和 ROS 2 之间的**桥梁**。

> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md), Section 7

### colcon 构建 (colcon build)

ROS 2 的构建工具。构建 AWS Small House + Create 3 仿真环境需要：

```bash
colcon build --symlink-install
```

`--symlink-install` 选项使用符号链接而非复制，修改源文件后无需重新构建。

> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md), Section 5

---

## 概念辨析

### AWS Small House vs 自建 Gazebo World

| 维度 | AWS Small House | 自建 World |
|------|----------------|-----------|
| **开发时间** | 0（即用即得） | 数天到数周 |
| **逼真度** | 高（多房间+家具+纹理） | 取决于建模能力 |
| **可定制性** | 低（只能替换照片纹理） | 高（完全控制） |
| **适用场景** | 室内导航 RL 训练 | 特殊场景模拟 |
| **维护者** | AWS Robotics 团队 | 自己 |

> 📖 Docs: [AWS Small House README](https://github.com/aws-robotics/aws-robomaker-small-house-world)

### SDF World File vs URDF Robot File

| 维度 | SDF World (.world) | URDF Robot (.urdf/.xacro) |
|------|--------------------|-----------------------|
| **描述对象** | 整个仿真世界 | 单个机器人 |
| **内容范围** | 家具+光源+物理参数 | 关节+Link+传感器 |
| **静态物体** | ✅ 支持 | ❌ 不支持 |
| **宏语言** | 无原生支持 | Xacro 宏 |
| **规范组织** | Open Source Robotics Foundation | ROS/OSRF |
| **本场景中** | AWS Small House 房屋 | iRobot Create 3 机器人 |

> 📖 Docs: [SDF Specification](http://sdformat.org/spec), [URDF Tutorial](https://docs.ros.org/en/iron/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html)

### AWS Small House vs AWS Bookstore vs AWS Small Warehouse

| 维度 | Small House | Bookstore | Small Warehouse |
|------|------------|-----------|-----------------|
| **场景类型** | 住宅室内 | 商业书店 | 工业仓库 |
| **RL 适用性** | 室内导航+避障 | 物品搜索+多通道导航 | 仓库物流+路径规划 |
| **空间复杂度** | 中（多房间） | 中（书架通道） | 高（大面积+货架） |
| **CST8509 使用** | ✅ 课程指定 | ❌ 未使用 | ❌ 未使用 |

> 📖 Docs: [AWS RoboMaker Worlds](https://aws.amazon.com/robomaker/)

---

## 核心属性

### 信息架构

    AWS Small House World
    ├── worlds/
    │   └── small_house.world          ← SDF World 主文件
    ├── models/
    │   ├── aws_robomaker_residential_*  ← 家具模型组
    │   │   ├── model.sdf              ← 模型描述
    │   │   ├── model.config           ← 模型元数据
    │   │   └── materials/             ← 纹理贴图
    │   └── ...
    ├── launch/
    │   └── small_house.launch         ← ROS Launch 文件
    └── worlds/
        └── small_house.world          ← Gazebo World 入口

### 适用场景 ✅

- 室内移动机器人导航仿真
- 基于视觉输入的 RL 训练（虚拟摄像头）
- Create 3 机器人 Sim-to-Real 过渡前的测试
- ROS 2 导航栈（Nav2）的验证

### 不适用场景 ❌

- 室外场景仿真（没有室外环境）
- 精确物理交互（家具都是静态的，质量/惯性不准确）
- 高速动态仿真（室内空间有限）
- 多机器人大规模仿真（单房屋规模较小）

> 📖 Docs: [AWS Small House README](https://github.com/aws-robotics/aws-robomaker-small-house-world)

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| World 文件 | `worlds/small_house.world` | SDF 格式的世界描述 |
| 模型目录 | `models/` | 所有家具/墙壁模型 |
| 模型路径变量 | `GAZEBO_MODEL_PATH` | `export GAZEBO_MODEL_PATH=\`pwd\`/models` |
| 物体类型 | 静态 (`<static>true</static>`) | 默认所有家具不会被推动 |
| 构建方式 | `colcon build` | 在 ROS 2 工作空间中构建 |
| Gazebo 版本 | Classic Gazebo 11 | 不是 Ignition/Gazebo Sim |
| GitHub 仓库 | `aws-robotics/aws-robomaker-small-house-world` | 主分支: ros1 |
