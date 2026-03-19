---
topic: gazebo
dimension: math
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: Gazebo Simulator — https://gazebosim.org/home"
  - "📖 Docs: ROS 2 geometry_msgs/Twist — https://docs.ros.org/en/humble/p/geometry_msgs/"
expiry: 12m
status: current
---

# Gazebo 仿真器 数学基础

> 📖 Docs: [Gazebo](https://gazebosim.org/home), [ROS 2 geometry_msgs](https://docs.ros.org/en/humble/p/geometry_msgs/)

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| v | 线速度 | Linear Velocity | ℝ³ (m/s) |
| ω | 角速度 | Angular Velocity | ℝ³ (rad/s) |
| x, y, z | 三维空间坐标 | Position | ℝ (m) |
| θ | 旋转角度 | Rotation Angle | [0, 2π] (rad) |
| Δt | 仿真时间步长 | Simulation Time Step | ℝ⁺ (s) |
| R | 旋转矩阵 | Rotation Matrix | SO(3) |
| T | 齐次变换矩阵 | Homogeneous Transform | SE(3) |
| f | 仿真频率 | Simulation Frequency | ℝ⁺ (Hz) |

---

## 核心公式

### 公式 1: Twist 速度命令（差速驱动机器人运动学）

**直觉：** Create 3 是差速驱动机器人（两个轮子独立转）。给定线速度 v 和角速度 ω，机器人的运动轨迹就确定了。RL Agent 输出的"动作"就是 (v, ω) 这对值。

$$
\begin{aligned}
x_{t+1} &= x_t + v \cdot \cos(\theta_t) \cdot \Delta t \\
y_{t+1} &= y_t + v \cdot \sin(\theta_t) \cdot \Delta t \\
\theta_{t+1} &= \theta_t + \omega \cdot \Delta t
\end{aligned}
$$

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| v | 前进速度 (linear.x) | Twist.linear.x = 0.5 m/s → 前进 |
| ω | 旋转速度 (angular.z) | Twist.angular.z = 1.0 rad/s → 左转 |
| θₜ | 当前朝向角 | 机器人面朝的方向 |
| Δt | 仿真步长 | Gazebo 默认 0.001s |

> 📖 差速驱动运动学基础，Create 3 使用此模型

### 公式 2: 仿真时间 vs 训练时间

**直觉：** 仿真的一大优势是可以"加速时间"。实时因子 (Real-Time Factor) 表示仿真跑得比现实快多少倍。

$$
T_{train} = \frac{N_{episodes} \times T_{episode}}{RTF}
$$

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| T_train | 实际训练总耗时 | 如果 = 10 小时，意味着你要等 10 小时 |
| N_episodes | 训练需要的总回合数 | DQN 通常需要 10⁵~10⁶ 个 episode |
| T_episode | 每个回合的仿真时长 | 一个导航任务 30 秒 |
| RTF | 实时因子 | RTF=5 → 仿真速度是现实的 5 倍 |

### 公式 3: 2D 坐标变换（世界坐标系 ↔ 机器人坐标系）

**直觉：** Gazebo 中有"世界坐标系"和"机器人坐标系"。传感器数据在机器人坐标系下，但 RL 状态可能需要世界坐标。需要用旋转+平移来转换。

$$
\begin{bmatrix} x^{world} \\ y^{world} \end{bmatrix} = 
\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}
\begin{bmatrix} x^{robot} \\ y^{robot} \end{bmatrix} +
\begin{bmatrix} t_x \\ t_y \end{bmatrix}
$$

**参数解释：**

| 参数 | 含义 |
|------|------|
| (x^world, y^world) | 在世界坐标系中的位置 |
| (x^robot, y^robot) | 在机器人坐标系中的位置 |
| θ | 机器人在世界坐标系中的朝向 |
| (tₓ, tᵧ) | 机器人在世界坐标系中的位置 |

---

## 公式关系图

    Twist 命令 (v, ω)
         │
         ├──→ 差速运动学 → 新位置 (x, y, θ)
         │         │
         │         └──→ Gazebo 物理引擎（真实仿真 vs 运动学近似）
         │
         └──→ 轮速分解
                   │
                   └──→ 左右轮速度 → 电机控制

    坐标变换
         │
         ├──→ 机器人坐标系 → 世界坐标系（报告位置）
         └──→ 世界坐标系 → 机器人坐标系（传感器数据）

---

## 手算练习

### 练习 1: Twist 命令导致的位移

**题目：** Create 3 初始位置 (0, 0)，朝向 θ=0（朝右）。发送 Twist: v=0.5 m/s, ω=0。仿真步长 Δt=1s。1 步后机器人在哪？

**解答：**

1. x₁ = 0 + 0.5 × cos(0) × 1 = 0 + 0.5 × 1 = **0.5 m**
2. y₁ = 0 + 0.5 × sin(0) × 1 = 0 + 0.5 × 0 = **0 m**
3. θ₁ = 0 + 0 × 1 = **0 rad**

结果：机器人直线前进到 (0.5, 0)，朝向不变 ✅

### 练习 2: 带旋转的运动

**题目：** 还是从 (0, 0, θ=0) 开始，Twist: v=1 m/s, ω=π/2 rad/s，Δt=1s。

**解答：**

1. x₁ = 0 + 1 × cos(0) × 1 = **1 m**
2. y₁ = 0 + 1 × sin(0) × 1 = **0 m**
3. θ₁ = 0 + (π/2) × 1 = **π/2 rad** (90°，朝上)

注意：这是离散近似（欧拉法），实际曲线运动要用弧线积分。但在小步长下，近似足够准确。

---

## 公式速查表

| 名称 | 公式 | 用途 |
|------|------|------|
| 差速运动学 | x' = x + v·cosθ·Δt | 给定 Twist 计算新位置 |
| 角速度更新 | θ' = θ + ω·Δt | 计算新朝向 |
| 训练时间 | T = N·T_ep / RTF | 估算仿真训练总耗时 |
| 坐标变换 | p_w = R·p_r + t | 机器人坐标转世界坐标 |
| 仿真频率 | f = 1/Δt | 典型值 1000 Hz |
