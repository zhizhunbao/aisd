---
topic: rviz
dimension: concepts
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: RViz2 User Guide — https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html"
expiry: 12m
status: current
---

# RViz 可视化工具 核心概念

> 📖 Docs: [RViz2 User Guide](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

---

## 术语定义

### RViz / RViz2

ROS 2 的 3D 可视化工具。全称 **R**obot **Viz**ualization。它订阅 ROS 2 话题上的数据（传感器数据、机器人状态），然后在 3D 窗口中渲染出来。就像一个"监控摄像头"——你能看到机器人周围的世界，但你不能通过 RViz 让机器人动。ROS 1 时代叫 RViz，ROS 2 时代叫 RViz2，但日常习惯都叫 RViz。

> 易混淆：**Gazebo** — Gazebo 做物理仿真（让机器人动），RViz 做数据可视化（让你看）。你通常同时开着两者：Gazebo 跑仿真，RViz 看数据

> 📖 Slides: CST8509 Week 7 Slide 16

### Display

RViz 中的核心概念——每个 Display 是一种可视化元素。你可以添加多个 Display 来同时显示不同类型的数据。比如一个 Display 显示机器人模型，一个显示激光扫描，一个显示路径。每个 Display 订阅一个特定的 ROS 2 话题。

> 📖 Docs: [RViz2 User Guide — Displays](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

### 常用 Display 类型

| Display | 订阅消息类型 | 显示什么 |
|---------|------------|---------|
| **RobotModel** | URDF (参数) | 机器人3D模型，链接和关节 |
| **TF** | `tf2_msgs/TFMessage` | 所有坐标系的位置和方向 |
| **LaserScan** | `sensor_msgs/LaserScan` | 2D 激光扫描点 |
| **PointCloud2** | `sensor_msgs/PointCloud2` | 3D 点云 (LiDAR) |
| **Image** | `sensor_msgs/Image` | 摄像头图像 (2D 窗口) |
| **Path** | `nav_msgs/Path` | 机器人路径或轨迹 |
| **Marker** | `visualization_msgs/Marker` | 自定义几何体 (箭头/球/线) |
| **MarkerArray** | `visualization_msgs/MarkerArray` | 一组自定义几何体 |
| **Map** | `nav_msgs/OccupancyGrid` | 2D 占据栅格地图 |
| **Odometry** | `nav_msgs/Odometry` | 里程计位姿 (箭头) |
| **Grid** | — | 地面网格参考线 |

### Fixed Frame

RViz 中最重要的设置之一。Fixed Frame 定义了可视化世界的"参考原点"——所有数据都相对于这个坐标系绘制。通常设为 `map`（全局地图）或 `odom`（里程计原点）或 `base_link`（机器人中心）。**设错了 Fixed Frame 什么都看不到**。

> 📖 Docs: [RViz2 User Guide — Global Options](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

### TF (Transform)

ROS 2 的坐标系变换系统。每个机器人部件（底盘、摄像头、车轮）都有自己的坐标系 (frame)，TF 维护它们之间的实时位置关系。RViz 依赖 TF 知道"摄像头在机器人的什么位置"来正确渲染。

> 📖 Docs: [ROS 2 TF2 Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html)

### TF 树 (TF Tree)

所有坐标系之间的父子关系构成的树状结构。根节点通常是 `map` 或 `odom`，叶节点是各传感器坐标系。RViz 可以显示完整的 TF 树，帮你理解"摄像头相对于底盘在哪"。

### Tool（交互工具）

RViz 工具栏上的交互工具，用于在 3D 视图中执行操作：

| Tool | 功能 |
|------|------|
| **Move Camera** | 拖拽旋转/缩放视角（默认） |
| **Interact** | 与交互式 Marker 交互 |
| **Select** | 选择3D场景中的物体 |
| **2D Pose Estimate** | 点击设置机器人初始位姿（导航用） |
| **2D Nav Goal** | 点击设置导航目标点 |
| **Measure** | 测量两点之间的距离 |
| **Publish Point** | 点击发布一个3D坐标到话题 |

### Panel（面板）

RViz 界面中的附加面板，提供非3D的信息或控制：

| Panel | 功能 |
|-------|------|
| **Displays** | 管理所有 Display（最重要的面板） |
| **Views** | 控制摄像机视角 |
| **Tool Properties** | 当前工具的属性 |
| **Time** | ROS 时间和仿真时间 |

### Views（视图模式）

RViz 中看 3D 世界的方式：

| View | 说明 |
|------|------|
| **Orbit** | 围绕焦点旋转（默认，最常用） |
| **FPS** | 第一人称视角 |
| **TopDownOrtho** | 俯视正交视图 |
| **XYOrbit** | 绕 Z 轴旋转 |
| **ThirdPersonFollower** | 第三人称跟随机器人 |

### .rviz 配置文件

RViz 的配置保存文件（YAML 格式），记录了当前的 Display 列表、各 Display 的话题/颜色/大小设置、视角、Fixed Frame 等。可以通过 launch 文件自动加载，避免每次手动配置。

---

## 概念辨析

### RViz vs Gazebo

| 维度 | RViz | Gazebo |
|------|------|--------|
| **核心功能** | 数据可视化 | 物理仿真 |
| **物理引擎** | ❌ 无 | ✅ ODE/Bullet/DART |
| **能让机器人动吗？** | ❌ 只能看 | ✅ 可以 |
| **数据来源** | 订阅 ROS 2 话题 | 自己计算物理 |
| **何时用** | 调试、查看传感器数据 | 训练 RL、测试算法 |
| **关系** | 通常同时用 | 通常同时用 |

### RViz vs rqt

| 维度 | RViz | rqt |
|------|------|-----|
| **可视化类型** | 3D 场景 | 2D 图表/面板 |
| **擅长** | 空间位置关系 | 时间序列、话题监控 |
| **典型场景** | 看机器人在哪、激光扫描形状 | 看奖励曲线、话题频率 |
| **插件生态** | Display 插件 | rqt_plot, rqt_graph 等 |

### RViz vs PlotJuggler

| 维度 | RViz | PlotJuggler |
|------|------|-------------|
| **维度** | 3D 空间 | 2D 时间序列 |
| **擅长** | 空间可视化 | 数值趋势分析 |
| **RL 用途** | 看 Agent 行为轨迹 | 看奖励/损失曲线 |

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| RViz2 | ROS 2 的 3D 可视化工具 | `rviz2` 启动 |
| Display | 可视化元素 | RobotModel, LaserScan, TF |
| Fixed Frame | 可视化参考坐标系 | `map`, `odom`, `base_link` |
| TF | 坐标系变换系统 | `base_link → camera_link` |
| Tool | 交互工具 | Move Camera, 2D Nav Goal |
| Panel | 信息面板 | Displays, Views, Time |
| .rviz | 配置保存文件 | `my_config.rviz` |
| Marker | 自定义几何体 | 箭头标注奖励区域 |
