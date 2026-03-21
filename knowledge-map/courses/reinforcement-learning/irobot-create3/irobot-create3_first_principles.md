---
topic: irobot-create3
dimension: first_principles
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Soragna et al., 'Impact of ROS 2 Node Composition', IEEE RA-L 2023 — https://arxiv.org/abs/2305.09933"
  - "📖 Paper: Quigley et al., 'ROS: an open-source Robot Operating System', ICRA 2009 — https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf"
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Docs: iRobot Create 3 — Simulator — https://iroboteducation.github.io/create3_docs/sim/setup/"
expiry: 12m
status: current
---

# iRobot Create 3 第一性原理

> 📖 Paper: Soragna et al., [ROS 2 Node Composition](https://arxiv.org/abs/2305.09933)
> 📚 Book: Sutton & Barto, [《RL: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1
> 📖 Docs: [Create 3 Simulator](https://iroboteducation.github.io/create3_docs/sim/setup/)

---

## 底层公理

### 公理 1: 接口等价性 (Interface Equivalence)

**表述：** 如果两个系统暴露完全相同的输入/输出接口，那么对调用者来说它们是不可区分的。

**形式化：**

    若 ∀ 输入 I, 系统A(I) ≈ 系统B(I)
    则调用者无法通过接口分辨 A 和 B

**Create 3 的实现：** 仿真 Create 3 和真实 Create 3 暴露**完全相同**的 ROS 2 Topics/Services/Actions/Parameters。因此，RL Agent 的代码对真实和仿真机器人"不可区分"——零修改迁移。

**边界条件：** 接口等价 ≠ 行为等价。仿真中的物理引擎是近似的——摩擦力、惯性、传感器噪声都是模型，不是真实物理。这就是"Sim-to-Real Gap"的根源。

> 📖 Docs: [Simulator](https://iroboteducation.github.io/create3_docs/sim/setup/) — "exposing to the user all the same ROS 2 APIs as the real robot"

### 公理 2: 消息传递解耦 (Message Passing Decoupling)

**表述：** 如果两个模块只通过标准化消息交互（不直接调用内部函数），那么任何一个模块都可以被替换，只要它遵守消息契约。

**形式化：**

    模块A --[标准消息]--> 模块B
    替换A为A'，只要 A'.publish(msg) 格式不变
    B 不需要任何修改

**Create 3 的实现：** ROS 2 的 Topic/Service/Action 就是这种标准化消息契约。Create 3 通过 `/cmd_vel` 接收 `Twist` 消息——不关心发送者是手动控制、PID 控制器还是 DQN Agent。

**为什么重要：** 这是 ROS 生态的核心价值——你可以独立开发和测试每个模块（SLAM、导航、RL Agent），然后用消息接口组合成完整系统。

> 📖 Paper: Quigley et al., [ROS](https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf) — ROS 设计为"structured communications layer"

### 公理 3: RL Agent-环境边界 (Agent-Environment Boundary)

**表述：** 所有 RL 系统都有一个明确的"智能体-环境边界"——智能体只能通过动作影响环境，环境只能通过状态和奖励反馈给智能体。

**形式化：** (📚 Sutton & Barto Ch.1.1)

    Agent → aₜ → Environment → (sₜ₊₁, rₜ₊₁) → Agent

**Create 3 的实现：**

| 概念 | Create 3 实现 |
|------|-------------|
| Agent | RL 算法（运行在外部计算机上） |
| 动作 aₜ | `Twist` 消息 → `/cmd_vel` |
| 环境 | Create 3 + 物理世界（或 Gazebo） |
| 状态 sₜ₊₁ | `/odom` + `/ir_intensity` + `/imu` → 状态向量 |
| 奖励 rₜ₊₁ | 自定义（到达目标、碰撞惩罚等） |

**追问：** 奖励函数不是环境的"自然属性"——它是人类设计的。Create 3 没有内置的"任务奖励"，你必须自己定义"什么行为是好的"。这是 RL 应用的核心设计挑战。

> 📚 Book: Sutton & Barto, [《RL: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1 — Agent-Environment Interface

---

## 追问链

### 追问 1: "为什么 Create 3 能做到仿真=真实？"

→ 因为接口等价性（公理 1）。只要 ROS 2 消息格式不变，调用者就不知道后端是物理硬件还是 Gazebo 物理引擎。

### 追问 2: "那 Sim-to-Real Gap 怎么解释？"

→ 接口等价 ≠ 行为等价。仿真物理引擎的摩擦模型、传感器噪声模型是**近似**。在仿真中训练出的策略可能因为这些近似误差在真实世界中失效。

**应对方案：**
1. **Domain Randomization**：在仿真中随机化物理参数（摩擦、质量、噪声），让策略学会"鲁棒性"
2. **Fine-tuning**：先在仿真中预训练，再在真实机器人上微调（少样本）

### 追问 3: "为什么 ROS 2 而不是直接用 Gymnasium API？"

→ Gymnasium 是"接口标准"（`step(action) → obs, reward, done, info`），而 ROS 2 是"通信基础设施"。两者不在同一层：

    Gymnasium (RL 接口) ──── 调用 ──→ ROS 2 (通信层) ──── 消息 ──→ Create 3 (物理层)

你需要一个"Gym-ROS 2 Wrapper"来桥接——它把 `step()` 翻译成 `publish(Twist)` + `subscribe(Odometry)`。

### 追问 4: "为什么 Node Composition 对 Create 3 是必要的？"

→ Create 3 的嵌入式处理器资源有限。标准 ROS 2 节点每个在独立进程中运行——进程间通信开销很大。Node Composition 把多个节点合并到一个进程，共享内存传递消息——这是让 Create 3 能在嵌入式处理器上运行完整 ROS 2 栈的关键技术。

> 📖 Paper: Soragna et al., [ROS 2 Node Composition](https://arxiv.org/abs/2305.09933) — 实验结果: 28% CPU, 33% RAM 节省

---

## 边界与假设

### Create 3 的隐含假设

| 假设 | 当假设不成立时 |
|------|--------------|
| **地面平坦** | Create 3 无法越过障碍物或爬楼梯 |
| **室内环境** | 户外风/雨/不平地面会导致里程计漂移严重 |
| **Wi-Fi 稳定** | 网络延迟 > 100ms 时实时控制不可靠 |
| **传感器足够** | 没有 LiDAR/深度相机，长走廊区分能力弱 |
| **仿真 ≈ 真实** | 摩擦/惯性差异 → Sim-to-Real Gap |
| **奖励可设计** | 复杂任务的奖励函数设计是开放问题 |

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| Soragna et al., [ROS 2 Node Composition](https://arxiv.org/abs/2305.09933) | 📖 论文 | 公理 1 + 追问 4 |
| Quigley et al., [ROS](https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf) | 📖 论文 | 公理 2 |
| Sutton & Barto, [《RL: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf) Ch.1 | 📚 教科书 | 公理 3 |
| [Create 3 Simulator](https://iroboteducation.github.io/create3_docs/sim/setup/) | 📖 文档 | 接口等价性 |
