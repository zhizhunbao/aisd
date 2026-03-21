---
topic: irobot-create3
dimension: math
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: iRobot Create 3 — ROS 2 API — https://iroboteducation.github.io/create3_docs/api/ros2/"
  - "📖 Docs: ROS REP-105 Coordinate Frames — https://www.ros.org/reps/rep-0105.html"
  - "📖 Docs: ROS REP-120 Coordinate Frames — https://www.ros.org/reps/rep-0120.html"
expiry: 12m
status: current
---

# iRobot Create 3 数学基础

> 📖 Docs: [Create 3 ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/), [REP-105](https://www.ros.org/reps/rep-0105.html)

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------| 
| v | 线速度（前进/后退快慢） | Linear Velocity | ℝ (m/s) |
| ω | 角速度（左转/右转快慢） | Angular Velocity | ℝ (rad/s) |
| x, y | 平面坐标 | Position | ℝ (m) |
| θ | 机器人朝向角 | Heading / Yaw | [0, 2π] (rad) |
| Δt | 控制周期 | Time Step | ℝ⁺ (s) |
| L | 轮距（两轮间距） | Wheel Base | ℝ⁺ (m) |
| r | 轮半径 | Wheel Radius | ℝ⁺ (m) |
| N | 编码器分辨率 | Encoder Resolution | ℤ⁺ (ticks/rev) |

> 📖 Docs: [Create 3 ROS 2 API — Parameters](https://iroboteducation.github.io/create3_docs/api/ros2/) — `wheel_base`, `wheels_radius`, `wheels_encoder_resolution` 均为只读参数

---

## 核心公式

### 公式 1: 差速驱动运动学 (Differential Drive Kinematics)

**直觉：** Create 3 有两个独立驱动轮。给 `/cmd_vel` 发 Twist 消息 (v, ω)，机器人的新位置由以下公式决定。

$$
\begin{aligned}
x_{t+1} &= x_t + v \cdot \cos(\theta_t) \cdot \Delta t \\
y_{t+1} &= y_t + v \cdot \sin(\theta_t) \cdot \Delta t \\
\theta_{t+1} &= \theta_t + \omega \cdot \Delta t
\end{aligned}
$$

**参数解释：**

| 参数 | 含义 | Create 3 对应 |
|------|------|--------------| 
| v | 前进速度 | `Twist.linear.x`，受 `max_speed` 参数限制 |
| ω | 旋转速度 | `Twist.angular.z` |
| θₜ | 当前朝向 | 从 `/odom` 中的四元数提取 yaw |
| Δt | 控制周期 | `/cmd_vel` 发布频率的倒数 |

> 📖 Docs: [Create 3 ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/) — `/cmd_vel` 接受 `geometry_msgs/msg/Twist`

### 公式 2: 轮编码器到轮速计算

**直觉：** Create 3 的 `/wheel_ticks` 话题报告每个轮子转了多少"格"。要算出实际走了多远，需要知道每格对应多少弧度。

$$
v_{wheel} = \frac{\Delta ticks}{N} \cdot 2\pi \cdot r \cdot \frac{1}{\Delta t}
$$

**参数解释：**

| 参数 | 含义 | Create 3 参数 |
|------|------|--------------|
| Δticks | 两次采样间的 tick 差 | `/wheel_ticks` 话题 |
| N | 编码器分辨率 | `wheels_encoder_resolution` 只读参数 |
| r | 轮半径 | `wheels_radius` 只读参数 |

> 📖 Docs: [Create 3 ROS 2 API — Parameters](https://iroboteducation.github.io/create3_docs/api/ros2/)

### 公式 3: ROS 2 坐标系变换 (odom → base_link)

**直觉：** Create 3 在 `/tf` 中发布 `odom → base_link` 变换。位置用 (x, y, z) 表示，朝向用四元数 (x, y, z, w) 表示。从四元数提取 yaw（平面朝向角）：

$$
\theta = \text{atan2}(2(wz + xy),\ 1 - 2(y^2 + z^2))
$$

**参数解释：**

| 参数 | 含义 |
|------|------|
| w, x, y, z | 四元数分量，从 `/tf` 或 `/odom` 的 `pose.orientation` 获取 |
| θ | 提取的 yaw 角——机器人在平面上的朝向 |

> 📖 Docs: [REP-105](https://www.ros.org/reps/rep-0105.html), [REP-120](https://www.ros.org/reps/rep-0120.html) — ROS 2 标准坐标系定义

---

## 公式关系图

    /cmd_vel (v, ω)
         │
         └──→ 差速运动学 → 新位置 (x, y, θ)
                   │
                   └──→ Create 3 物理执行 → 轮编码器 tick
                              │
                              ├──→ 轮速计算 → v_left, v_right
                              └──→ 融合里程计 (轮+IMU+光学)
                                        │
                                        └──→ /odom + /tf (pose 四元数)
                                                  │
                                                  └──→ yaw 提取 → RL 状态的 θ

---

## 手算练习

### 练习 1: Twist 命令后的位移

**题目：** Create 3 初始位置 (0, 0)，朝向 θ=0（朝 x 正方向）。发 Twist: v=0.3 m/s, ω=0。Δt=2s。2 步后机器人在哪？

**解答：**

1. x₁ = 0 + 0.3 × cos(0) × 2 = **0.6 m**
2. y₁ = 0 + 0.3 × sin(0) × 2 = **0 m**
3. θ₁ = 0 + 0 × 2 = **0 rad**

结果：直线前进到 (0.6, 0)，朝向不变 ✅

### 练习 2: 四元数转 yaw

**题目：** `/odom` 返回 orientation: x=0, y=0, z=0.383, w=0.924。求 yaw。

**解答：**

θ = atan2(2(0.924×0.383 + 0×0), 1 - 2(0² + 0.383²))
θ = atan2(2×0.354, 1 - 2×0.147)
θ = atan2(0.708, 0.706)
θ ≈ **0.785 rad ≈ 45°** ✅

---

## 公式速查表

| 名称 | 公式 | 用途 |
|------|------|------|
| 差速运动学 | x' = x + v·cosθ·Δt | Twist → 新位置 |
| 角度更新 | θ' = θ + ω·Δt | Twist → 新朝向 |
| 轮速 | v = Δticks/N · 2πr / Δt | 编码器 → 线速度 |
| yaw 提取 | θ = atan2(2(wz+xy), 1-2(y²+z²)) | 四元数 → 朝向角 |
