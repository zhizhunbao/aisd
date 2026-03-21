---
topic: aws_small_house
dimension: history
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: AWS RoboMaker — https://aws.amazon.com/robomaker/"
  - "📖 Docs: AWS RoboMaker Small House World — https://github.com/aws-robotics/aws-robomaker-small-house-world"
  - "📖 Docs: Open Robotics — https://www.openrobotics.org/"
  - "📖 Docs: Gazebo History — https://gazebosim.org/about"
expiry: never
status: current
---

# AWS Small House 的故事线：从空白世界到标准化仿真场景

> **核心主题：** 机器人仿真从"程序员自己搭场景"到"云平台提供标准化世界"的演进
> **故事线：** 一个关于"为什么不应该让每个开发者重复造轮子"的工程故事

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 机器人研究者有了仿真器（Gazebo），但每次训练都要**自己搭建仿真环境**——这就像有了操作系统但每次都要自己画桌面壁纸

2004 年 Gazebo 诞生后，研究者终于可以在虚拟世界中测试机器人了。但一个关键问题被忽视了很久：**谁来建真实世界的虚拟副本？**

Gazebo 自带几个简单世界（空白世界、一个方块、一面墙），但这些对于训练导航机器人毫无帮助——你不可能在空荡荡的世界里学会避障。研究者要么用 Blender 从零建模，要么用极简的几何体凑合。

> 🔑 **问题提出：** 仿真器有了，但逼真的仿真世界还要自己建——这个门槛挡住了大量想做机器人 RL 的人

---

## 📚 第一章：Gazebo 生态的世界缺口（2004-2017）

> **关键人物：** Andrew Howard, Nate Koenig (Gazebo 创始人)
> **关键论文：** Koenig \& Howard, "Design and Use Paradigms for Gazebo, An Open-Source Multi-Robot Simulator", IROS 2004

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Gazebo 早期界面截图 | Gazebo 官网 | `https://classic.gazebosim.org` | 开源项目 |
| 空白 Gazebo 世界 | Gazebo Tutorials | `https://classic.gazebosim.org/tutorials` | 开源教程 |

### 发生了什么？

Gazebo 从 2004 年开始在 USC（南加州大学）作为 Player/Stage 的 3D 扩展被开发。它解决了"如何模拟物理"的问题——ODE 物理引擎、OGRE 渲染引擎、传感器模拟。

但 Gazebo 的世界生态极度贫乏。官方提供的示例世界只有：
- 一片空地
- 几个简单的几何体障碍物
- 一面墙

研究者如果要训练室内导航机器人，就必须：
1. 学会 Blender/FreeCAD 3D 建模
2. 创建 SDF 格式的模型文件
3. 手动调整碰撞体、纹理、光照
4. 调试物理参数避免穿模

这个过程通常需要**数天到数周**，远超机器人研究本身的工作量。

### 为什么这很重要？

仿真环境的质量直接决定了 RL 训练的有效性。在过于简化的世界中训练出的策略，迁移到真实世界时会完全失效（Sim-to-Real Gap）。一个没有家具的"室内"环境，训练出的导航策略永远不会学到"绕过椅子"这种技能。

### 但还有一个问题……

每个研究组都在重复建造自己的仿真世界，质量参差不齐，而且这些世界几乎不共享——因为没有标准化的仓库结构和发布方式。

> 🔑 **故事转折点：** 2018 年，AWS 决定把机器人仿真做成**云服务**——这意味着他们需要提供**标准化的仿真世界**

---

## 📚 第二章：AWS RoboMaker 和标准化仿真世界的诞生（2018-2019）

> **关键人物：** AWS Robotics 团队
> **关键事件：** AWS re:Invent 2018 发布 AWS RoboMaker

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| AWS RoboMaker Logo | AWS 官网 | `https://aws.amazon.com/robomaker/` | AWS 品牌 |
| Small House 截图 | GitHub README | `https://github.com/aws-robotics/aws-robomaker-small-house-world` | Apache 2.0 |

### 发生了什么？

2018 年 AWS re:Invent 大会上，Amazon 发布了 **AWS RoboMaker**——一个基于云的机器人开发平台。核心卖点之一是：用户可以在 AWS 云上运行 Gazebo 仿真，不需要本地 GPU。

但光有仿真引擎不够——用户还是需要世界。AWS Robotics 团队做了一个关键决策：**开源发布一系列标准化 Gazebo 仿真世界**。

2019 年，以下三个世界作为开源项目发布到 GitHub：

1. **Small House** — 多房间住宅，含家具、画框、地板纹理
2. **Bookstore** — 书架走廊的商业空间
3. **Small Warehouse** — 工业仓库场景

这些世界：
- 使用标准 Gazebo SDF 格式
- 所有模型有精细的纹理贴图
- 以 Apache 2.0 开源许可发布
- 可直接在本地 Gazebo 中使用，不强制依赖 AWS 云

### 为什么这很重要？

这是**第一次**由商业公司为机器人社区提供**生产质量**的开源仿真世界。其意义：

1. **降低了入门门槛**：研究者和学生不再需要学 3D 建模
2. **标准化了基准环境**：不同团队在同一世界中训练，结果可以对比
3. **树立了模式**：后来 NVIDIA Isaac Sim、Unity Robotics Hub 都采用了类似的"预构建世界"策略

### 但还有一个问题……

AWS Small House 的家具质量/惯性参数不准确（README 中的 Disclaimer 明确承认了这一点），而且这些世界主要兼容 Classic Gazebo 11——随着 Gazebo 生态向 Ignition/Gazebo Sim 迁移，兼容性成了问题。

> 🔑 **故事转折点：** 教育机构发现这些世界非常适合教学用途——特别是与 iRobot Create 3 教育机器人结合做 RL 训练

---

## 📚 第三章：教育场景中的应用（2022-至今）

> **关键人物：** iRobot Education 团队, CST8509 课程
> **关键事件：** Create 3 模拟器 + AWS Small House 成为 RL 教学标准环境

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Create 3 in AWS House | CST8509 Lab 3 截图 | 本地文件 | 课程材料 |
| iRobot Create 3 | iRobot Education | `https://edu.irobot.com/create3` | iRobot 品牌 |

### 发生了什么？

iRobot Education 在 2022 年发布了 Create 3 教育机器人及其 Gazebo 模拟器（create3_sim）。这个模拟器需要一个仿真世界让机器人在里面活动。

AWS Small House 成了完美选择：
- **兼容性**：同样基于 Classic Gazebo 11 + ROS 2 Humble
- **复杂度适中**：比空白世界真实，比工业场景简单，适合教学
- **教学价值**：学生可以在虚拟房屋中用 ROS 2 命令控制机器人导航
- **可扩展**：学生可以添加虚拟摄像头（URDF/Xacro），为后续 RL 训练做准备

CST8509 课程（Algonquin College 的强化学习课程）将 "Gazebo + Create 3 + AWS Small House" 定为 Lab 3 的标准环境，学生在此环境中完成：
1. 部署仿真环境
2. 添加虚拟摄像头
3. 用 ROS 2 命令控制机器人导航
4. 为 Assignment 2 的 RL 训练做准备

### 为什么这很重要？

这证明了 AWS 开源仿真世界的价值不仅限于工业研发——在教育场景中同样是"基础设施级"的贡献。一个教授不需要自建仿真环境就可以开设机器人 RL 课程。

### 但还有一个问题……

Classic Gazebo 11 已经是"遗产"软件（legacy），未来 ROS 2 版本将只支持 Gazebo Sim（原 Ignition Gazebo）。AWS Small House 的 Classic Gazebo 版本终将过时，需要移植到新架构。

> 🔑 **下一步问题：** 仿真世界如何跟上 Gazebo 生态的架构迁移？需要社区或 AWS 进行 SDF → 新格式的迁移工作

---

## 🗺️ 全局回顾：技术演进路线图

    2004                2018              2019              2022              未来
    │                   │                 │                 │                 │
    Gazebo 诞生         AWS RoboMaker     Small House       Create 3 +        Gazebo Sim
    (空白世界)          (云仿真平台)      开源发布          教育应用           迁移
    │                   │                 │                 │                 │
    ────────────────────────────────────────────────────────────────────────────
    "仿真器有了          "需要标准化       "从工业到         "从研究到          "架构
     但世界没有"          仿真世界"        教育全覆盖"       教学全打通"        大迁移"

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| 空白世界 → AWS Small House | 不再需要每个人自建仿真环境 |
| 本地建模 → 开源仓库 | 标准化了仿真世界的获取和使用方式 |
| 工业场景 → 教育场景 | 降低了 RL + 机器人课程的开课门槛 |
| Classic Gazebo → Gazebo Sim | （进行中）适应新的仿真架构 |

### 🎥 视觉素材总表（视频制作用）

| 章节 | 人物/组织 | 肖像/Logo 来源 | 论文/事件图片 | 版权 |
|------|----------|---------------|-------------|------|
| 第一章 | Nate Koenig | OSRF 官网 | Gazebo 早期截图 | 开源 |
| 第二章 | AWS Robotics | AWS 官网 Logo | Small House GitHub 截图 | Apache 2.0 |
| 第三章 | iRobot Education | iRobot 官网 | Lab 3 仿真截图 | 课程材料 |
