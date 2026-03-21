---
topic: irobot-create3
dimension: concepts
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Soragna et al., 'Impact of ROS 2 Node Composition in Robotic Systems', IEEE RA-L 2023 — https://arxiv.org/abs/2305.09933"
  - "📖 Paper: Quigley et al., 'ROS: an open-source Robot Operating System', ICRA Workshop 2009 — https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf"
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Docs: iRobot Create 3 — Hardware Overview — https://iroboteducation.github.io/create3_docs/hw/overview/"
  - "📖 Docs: iRobot Create 3 — ROS 2 API — https://iroboteducation.github.io/create3_docs/api/ros2/"
  - "💻 Source: irobot_create_msgs — https://github.com/iRobotEducation/irobot_create_msgs"
expiry: 12m
status: current
---

# iRobot Create 3 核心概念

> 📖 Paper: Soragna et al., [ROS 2 Node Composition](https://arxiv.org/abs/2305.09933), IEEE RA-L 2023
> 📖 Docs: [Create 3 Hardware](https://iroboteducation.github.io/create3_docs/hw/overview/), [ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/)

---

## 术语定义

### iRobot Create 3

基于 Roomba 扫地机器人底盘的教育机器人平台。它不是为扫地设计的，而是为教育者、学生和开发者提供一个可编程的移动机器人。所有传感器数据通过 ROS 2 发布，所有执行器通过 ROS 2 订阅/服务/动作控制。

> 别名：**Create® 3** / **Create3**（iRobot 商标写法）— 都是同一个东西

> 📖 Docs: [Create 3 Home](https://iroboteducation.github.io/create3_docs/)

### Roomba 底盘 (Roomba Chassis)

Create 3 的硬件基础——iRobot 的 Roomba 扫地机器人平台。包含差速驱动轮、悬崖传感器、碰撞传感器、充电对接站。Create 3 去掉了吸尘功能，保留了导航和传感硬件，加上了开放的 ROS 2 接口。

> 易混淆：**Roomba** 是消费产品（扫地），**Create 3** 是教育/开发平台（编程）——硬件相似但软件接口完全不同

> 📖 Docs: [Hardware Overview](https://iroboteducation.github.io/create3_docs/hw/overview/)

### 多区碰撞器 (Multizone Bumper)

Create 3 前方的弧形碰撞传感器，配有 7 对 IR（红外）接近传感器。可以在物理接触之前通过红外检测障碍物（接近检测），也可以在物理碰撞时触发（碰撞检测）。数据通过 `/hazard_detection` 和 `/ir_intensity` ROS 2 话题发布。

> 📖 Docs: [Hardware Overview](https://iroboteducation.github.io/create3_docs/hw/overview/)

### 悬崖传感器 (Cliff Sensor)

Create 3 底部的 4 个向下的红外传感器，检测地面是否存在（防止跌落楼梯或桌边）。数据同样通过 `/hazard_detection` 话题中的 `CLIFF` 类型发送。这是 Create 3 安全系统的关键组件。

> 📖 Docs: [Hardware Overview](https://iroboteducation.github.io/create3_docs/hw/overview/)

### 光学里程计传感器 (Optical Odometry Sensor / Optical Flow Sensor)

Create 3 底部的一个向下的光学传感器，通过追踪地面纹理的移动来估计机器人位移。与轮编码器和 IMU 融合后生成高质量的里程计估计。

> 别名：**光学流传感器**（计算机视觉领域）/ **光学里程计**（机器人领域）— 本质都是用图像运动估计物理运动

> 📖 Docs: [Hardware Overview](https://iroboteducation.github.io/create3_docs/hw/overview/)

### IMU (惯性测量单元 / Inertial Measurement Unit)

Create 3 内置的 3D 陀螺仪 + 3D 加速度计。用于测量机器人的旋转速度和线性加速度。与轮编码器和光学里程计融合后，输出到 `/odom` 话题和 `/tf` 变换树。

> 📖 Docs: [Create 3 ROS 2 API — Coordinate System](https://iroboteducation.github.io/create3_docs/api/ros2/)

### 轮编码器 (Wheel Encoder)

每个驱动轮上的旋转传感器，测量轮子转了多少圈（分辨率由 `wheels_encoder_resolution` 参数决定）。是差速驱动里程计的基础数据来源。数据通过 `/wheel_ticks` 和 `/wheel_vels` 话题发布。

> 📖 Docs: [Create 3 ROS 2 API — Parameters](https://iroboteducation.github.io/create3_docs/api/ros2/)

### 融合里程计 (Fused Odometry)

Create 3 将轮编码器、IMU 和光学流传感器的数据融合，生成一个综合的位姿估计。输出为 `nav_msgs/msg/Odometry` 消息发布到 `/odom` 话题，同时在 `/tf` 变换树中维护 `odom → base_link` 和 `odom → base_footprint` 变换。

> 易混淆：**轮式里程计** 只用轮编码器（容易打滑漂移），**融合里程计** 综合多传感器（更准确）

> 📖 Docs: [Create 3 ROS 2 API — Coordinate System](https://iroboteducation.github.io/create3_docs/api/ros2/)

### 充电座 (Home Base Charging Station / Dock)

Create 3 自带的充电站。机器人可以通过 ROS 2 Action `/dock` 自动导航回充电站对接，`/undock` 解除对接。对接状态通过 `/dock_status` 话题发布。

> 📖 Docs: [Create 3 ROS 2 API — Actions](https://iroboteducation.github.io/create3_docs/api/ros2/)

### 安全反射 (Reflexes)

Create 3 内置的一组自主安全行为——碰撞反射（`REFLEX_BUMP`）、悬崖反射（`REFLEX_CLIFF`）、轮悬空反射（`REFLEX_WHEEL_DROP`）等。默认开启，通过 `safety_override` 参数可以设为 `full`（禁用所有反射，用于 RL 全权控制）。

> 📖 Docs: [Create 3 Safety](https://iroboteducation.github.io/create3_docs/api/safety/)

### /cmd_vel 话题

Agent 控制 Create 3 运动的核心话题。接受 `geometry_msgs/msg/Twist` 类型消息，包含线速度 (linear.x) 和角速度 (angular.z)。在 RL 中，这就是 Agent 输出的**动作**。

> 📖 Docs: [Create 3 ROS 2 API — Topics](https://iroboteducation.github.io/create3_docs/api/ros2/)

### irobot_create_msgs

iRobot 为 Create 3 定义的自定义 ROS 2 消息包。标准 ROS 2 消息（如 `geometry_msgs/Twist`、`sensor_msgs/Imu`）不够用的地方，用这个包定义自定义类型（如 `HazardDetectionVector`、`DockStatus`、`WheelVels` 等）。

> 💻 Source: [irobot_create_msgs](https://github.com/iRobotEducation/irobot_create_msgs)

### ROS 2 Node Composition (节点组合)

ROS 2 的一种优化技术——把多个节点合并到同一个进程中运行，减少 CPU 和内存开销。Create 3 的嵌入式处理器资源有限，iRobot 论文指出没有 Node Composition，Create 3 就不可能运行完整的 ROS 2 栈。

> 📖 Paper: Soragna et al., [ROS 2 Node Composition](https://arxiv.org/abs/2305.09933), IEEE RA-L 2023 — 实验显示 Composition 节省 28% CPU、33% RAM

### base_link / base_footprint

ROS 2 中两个标准坐标系。`base_link` 在机器人旋转中心、与地面相交的高度；`base_footprint` 是 `base_link` 的 2D 投影（去除俯仰和横滚），适合 2D 地图应用。

> 📖 Docs: [ROS REP-105](https://www.ros.org/reps/rep-0105.html), [REP-120](https://www.ros.org/reps/rep-0120.html)

---

## 概念辨析

### 真实 Create 3 vs 仿真 Create 3

| 维度 | 真实 Create 3 | 仿真 Create 3 (Gazebo) |
|------|--------------|----------------------|
| **ROS 2 API** | ✅ 完全相同 | ✅ 完全相同 |
| **传感器精度** | ✅ 真实物理 | ⚠️ 近似（有噪声模型） |
| **训练速度** | 实时（1x） | 可加速（gzserver 无头模式） |
| **安全性** | ⚠️ 可能撞坏 | ✅ 随便摔 |
| **成本** | 💰 需硬件 | 💻 只需计算资源 |
| **代码迁移** | — | ✅ 零修改部署 |

> 📖 Docs: [Create 3 Simulator](https://iroboteducation.github.io/create3_docs/sim/setup/)

### ROS 2 Topic vs Service vs Action

| 维度 | Topic | Service | Action |
|------|-------|---------|--------|
| **模式** | 发布/订阅 (Pub/Sub) | 请求/响应 (Req/Res) | 目标/反馈/结果 |
| **阻塞?** | ❌ 异步 | ✅ 同步阻塞 | ❌ 异步+反馈 |
| **Create 3 示例** | `/cmd_vel`、`/odom` | `/e_stop`、`/robot_power` | `/dock`、`/undock`、`/drive_distance` |
| **RL 中的角色** | 状态观察 + 动作发送 | 紧急停止 | 高层动作（停靠/导航） |

> 📖 Paper: Quigley et al., [ROS](https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf), ICRA 2009

---

## 核心属性

### Create 3 在 RL 系统中的位置

```
    RL Agent (DQN/PPO)
         │
         ├─ 动作 → /cmd_vel (Twist)
         │
    Gymnasium 包装器
         │
         ├─ ROS 2 桥接
         │
    Create 3 (真实 或 Gazebo 仿真)
         │
         ├─ 传感器 → /odom, /scan, /imu, /ir_intensity
         ├─ 危险检测 → /hazard_detection
         ├─ 对接状态 → /dock_status
         └─ 摄像头 → /custom_ns/camera1/custom_img (需要 URDF 添加)
```

### 适用场景 ✅

- 室内导航 RL 训练（平坦地面环境）
- 避障策略学习（碰撞器 + IR 传感器）
- 视觉 RL（添加虚拟摄像头后）
- ROS 2 算法教学和验证

### 不适用场景 ❌

- 户外/非平坦地形（Create 3 只有两轮 + 前脚轮）
- 机械臂操作（没有操作器）
- 高速运动（max_speed 参数限制）
- 多楼层导航（无法爬楼梯）

> 📖 Docs: [Hardware Overview](https://iroboteducation.github.io/create3_docs/hw/overview/)

---

## 速查表

| 项 | 说明 | ROS 2 话题/接口 |
|-----|------|----------------|
| Create 3 | 基于 Roomba 的教育机器人 | 所有传感器/执行器通过 ROS 2 |
| 碰撞器 | 前方 7 对 IR 接近传感器 | `/ir_intensity`, `/hazard_detection` |
| 悬崖传感器 | 底部 4 个防跌落传感器 | `/hazard_detection` (CLIFF) |
| IMU | 3D 陀螺仪 + 加速度计 | `/imu` |
| 轮编码器 | 两轮旋转计数 | `/wheel_ticks`, `/wheel_vels` |
| 光学里程计 | 底部光学流传感器 | 融合到 `/odom` |
| 融合里程计 | 轮+IMU+光学融合位姿 | `/odom`, `/tf` |
| 运动控制 | 线速度+角速度 | `/cmd_vel` (Twist) |
| 对接 | 自动回充电站 | Action: `/dock`, `/undock` |
| 导航 | 导航到指定位置 | Action: `/navigate_to_position` |
| 安全反射 | 内置碰撞/悬崖保护 | Param: `safety_override` |
| 灯环 | 6 个 RGB LED | `/cmd_lightring` |
| 喇叭 | 可编程声音 | `/cmd_audio` |
