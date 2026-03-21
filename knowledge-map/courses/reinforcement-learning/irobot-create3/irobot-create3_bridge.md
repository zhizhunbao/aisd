---
topic: irobot-create3
dimension: bridge
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Docs: iRobot Create 3 — https://iroboteducation.github.io/create3_docs/"
  - "📖 Docs: Gymnasium — https://gymnasium.farama.org/"
  - "📖 Docs: Gazebo — https://classic.gazebosim.org/"
expiry: 12m
status: current
---

# iRobot Create 3 衔接地图

> 📚 Book: Sutton & Barto, [《RL: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1
> 📖 Docs: [Create 3](https://iroboteducation.github.io/create3_docs/), [Gymnasium](https://gymnasium.farama.org/)

---

## 前置主题 → Create 3

### 从 RL Foundations 到 Create 3

| 你已经学到的 | 在 Create 3 中怎么用 |
|-------------|---------------------|
| Agent-环境循环 (📚 Sutton Ch.1) | Agent 通过 ROS 2 接口与 Create 3（环境）交互 |
| 状态 s | 从 `/odom`、`/ir_intensity`、`/imu` 组装状态向量 |
| 动作 a | 发 Twist 消息到 `/cmd_vel`（连续动作）或离散化为前进/后退/左转/右转 |
| 奖励 r | 自定义设计——如到达目标+1、碰撞-1、每步-0.01 |
| 回合 Episode | 从 `/undock` 开始，碰撞/超时/到达目标时 `/dock` 结束 |

### 从 Gazebo 到 Create 3

| 你已经学到的 | 在 Create 3 中怎么用 |
|-------------|---------------------|
| Gazebo 世界文件 (.world) | Create 3 仿真运行在 Gazebo 世界中 |
| URDF/Xacro 机器人模型 | Create 3 的模型已在 create3_sim 中定义 |
| Gazebo 传感器插件 | 可以通过 URDF 添加摄像头/LiDAR 等额外传感器 |
| `ros2 launch` | 用 `create3_gazebo.launch.py` 启动仿真 |

---

## Create 3 → 后续主题

### 到 DQN / Policy Gradient

| Create 3 中学到的 | 下一步怎么用 |
|------------------|-------------|
| `/odom` → 状态向量 (x, y, θ) | 作为 DQN 的输入状态 |
| `/cmd_vel` → 离散化动作 | 作为 DQN 的动作空间 |
| 碰撞检测 → 负奖励 | 设计 DQN 的奖励函数 |
| 仿真加速训练 | DQN 需要大量经验——仿真器可以跑比实时更快 |

### 到 Sim-to-Real Transfer

| Create 3 中学到的 | 下一步怎么用 |
|------------------|-------------|
| 仿真 = 真实 API | 代码零修改部署到真实 Create 3 |
| Gazebo 传感器噪声 | 理解 Sim-to-Real Gap 的来源 |
| `safety_override=full` (仿真) | 真实机器人**保留**反射——需要设计兼容安全反射的策略 |

### 到 Multi-Sensor RL

| Create 3 中学到的 | 下一步怎么用 |
|------------------|-------------|
| 融合里程计 (轮+IMU+光学) | 多传感器融合是导航 RL 的基础 |
| 虚拟摄像头 URDF | 视觉 RL (Image → Action) |
| IR 接近传感器阵列 | 多传感器输入的状态空间设计 |

---

## 同层横向关系

### Create 3 ↔ Gymnasium

| 维度 | Create 3 | Gymnasium |
|------|---------|-----------|
| **角色** | 物理/仿真执行层 | RL 环境 API 标准 |
| **接口** | ROS 2 (Topics/Actions) | `step()` / `reset()` |
| **连接方式** | 需要自定义 Wrapper 桥接 ROS 2 → Gym API | 直接使用 |
| **训练速度** | 接近实时 | 取决于环境实现 |
| **关系** | Create 3 是"底层"，Gym 是"上层" | Gym 调用 Create 3 的 ROS 2 接口 |

### Create 3 ↔ TurtleBot 4

| 维度 | Create 3 | TurtleBot 4 |
|------|---------|-------------|
| **底盘** | Roomba i 系列 | **也是 Create 3 底盘** + 扩展板 |
| **额外硬件** | 无 | LiDAR + 深度摄像头 + Raspberry Pi 4 |
| **ROS 2 API** | Create 3 原生 Topics | Create 3 Topics + Navigation2 Stack |
| **价格** | ~$300 | ~$1200 |
| **适合** | RL 入门、ROS 2 教学 | SLAM + 自主导航研究 |

> 📖 Docs: [Create 3 Home](https://iroboteducation.github.io/create3_docs/)

---

## 连接图

```
    RL Foundations ──→ Create 3 ──→ DQN / PPO 训练
    (Agent/环境)       (物理平台)     (算法应用)
         │                │               │
         ↓                ↓               ↓
    Gymnasium ←──── ROS 2 桥接 ────→ Sim-to-Real
    (环境 API)       (Topic/Action)    (仿真→真实)
         │                │
         ↓                ↓
    状态空间设计      Gazebo 仿真 ────→ Multi-Sensor RL
    (obs/reward)     (物理引擎)         (视觉+里程计)
```

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| Sutton & Barto, [《RL: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf) Ch.1 | 📚 教科书 | Agent-环境循环对应 |
| [Create 3 Docs](https://iroboteducation.github.io/create3_docs/) | 📖 文档 | 全文核心参考 |
| [Gymnasium Docs](https://gymnasium.farama.org/) | 📖 文档 | Gym 接口对比 |
| [Gazebo Classic](https://classic.gazebosim.org/) | 📖 文档 | 仿真平台对比 |
