---
topic: rviz
dimension: bridge
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: RViz2 — https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html"
expiry: 12m
status: current
---

# RViz 可视化工具 衔接与扩展

> 📖 Slides: CST8509 Week 7; 📖 Docs: [RViz2](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Foundations | Agent/环境/奖励的基本概念 | [foundations](../foundations/foundations_map.md) |
| ← 前置 | Gazebo | RViz 订阅 Gazebo 发布的 ROS 2 话题 | [gazebo](../gazebo/gazebo_map.md) |
| ← 前置 | ROS 2 基础 | RViz 是 ROS 2 生态工具 | — |
| → 后续 | SLAM 可视化 | 用 RViz 查看地图构建过程 | — |
| → 后续 | Navigation 调试 | 用 2D Nav Goal 设置导航目标 | — |
| → 后续 | 自定义 RViz 插件 | 开发特定 Display 类型 | — |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| Gazebo | 仿真数据发布 | RViz 订阅 Gazebo 通过 ROS 2 发的话题 |
| Gazebo | URDF 机器人模型 | RViz 的 RobotModel Display 读取同一个 URDF |
| Foundations | 状态 (State) | RViz 可视化 Agent 的观察状态 |
| Foundations | 动作 (Action) | 用 Marker 箭头显示 Agent 选择的动作方向 |

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|--------------------|
| SLAM | TF 可视化 | 调试 SLAM 建图时坐标系是否正确 |
| Navigation | 2D Nav Goal | 在 RViz 中直接设置导航目标 |
| Multi-Robot | 多模型显示 | 同时可视化多个机器人的状态 |
| 自定义插件 | Display 插件系统 | 开发 RL 特有的可视化（如值函数热力图） |

---

## 概念演变追踪

| 概念 | 在 ROS 1 | 在 ROS 2 | 变化原因 |
|------|---------|---------|---------|
| 可视化工具 | RViz (roscpp) | RViz2 (rclcpp) | ROS 2 重写 |
| 通信方式 | TCPROS | DDS | 更可靠的中间件 |
| 平台支持 | Linux 为主 | Linux/macOS/Windows | 跨平台需求 |
| 插件开发 | pluginlib (ROS 1) | pluginlib (ROS 2) | API 更新 |

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [RViz2 User Guide](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html) | 📖 文档 | 官方完整指南 | ⭐⭐ |
| [RViz2 Plugin Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-Plugin-Development.html) | 📖 文档 | 开发自定义 Display | ⭐⭐⭐ |
| [TF2 Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html) | 📖 文档 | 理解 RViz 依赖的 TF 系统 | ⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [rqt](https://docs.ros.org/en/humble/Concepts/Intermediate/About-RQt.html) | RViz vs rqt 2D 图表 | 需要看时间序列数据时 |
| [PlotJuggler](https://github.com/facontidavide/PlotJuggler) | 高级时序分析 | 详细分析奖励/值趋势 |
| [Foxglove Studio](https://foxglove.dev/) | Web 端可视化 | 远程调试时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| RL 课程 | 2 主题 | foundations, gazebo | RViz 是 Gazebo 仿真的可视化伙伴 |
| Computer Vision 课程 | 2+ 主题 | object_detection | RViz 可显示检测结果 Marker |
