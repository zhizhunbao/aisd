# CST8509 期末笔试题 — 参考答案（老师原话版）

> **Source:** `CST8509_10_Final_Review_slides.md` §5.2 (Slides 11-12)
> **答案来源:** 从老师各周 slides 原文提取，标注了出处

---

## Q1. How can RL be applied to problems where the number of states is huge?

**Q1. 当状态数量巨大时，RL 如何应用？**

Estimate value function with **function approximation**. **w** is a vector of weights of a neural network. v̂(s, w) ≈ v_π(s) or q̂(s, a, w) ≈ q_π(s, a). **Generalize from seen states to unseen states**. Update parameter w using MC or TD learning. DQN and PPO are two common approaches.

> 用**函数近似**估计值函数。**w** 是神经网络的权重向量。v̂(s, w) ≈ v_π(s) 或 q̂(s, a, w) ≈ q_π(s, a)。**从已见状态泛化到未见状态**。用 MC 或 TD 学习更新参数 w。DQN 和 PPO 是两种常见方法。

📎 *Source: Week 9 Slide 5 — "Value Function Approximation"*

---

## Q2. Describe at a high level how the DQN algorithm does value function approximation

**Q2. 从高层次描述 DQN 算法如何进行值函数近似**

DQN is similar to Q-learning except: **no Q-table, we have Q-network instead**. Q-network implements an approximation of Q. **Input to Q-network is State, output is action values** (same number of outputs as actions). There are two neural networks: **Online Network** (actively updated via gradients to minimize MSE loss based on TD error) and **Target Network** (a lagged copy, updated less frequently using hard update or soft update/Polyak update, governed by tau parameter). Transitions (s,a,r,s') are stored in a **Replay Buffer** to break temporal correlations.

> DQN 与 Q-Learning 类似，但区别在于：**没有 Q 表，取而代之的是 Q 网络**。Q 网络实现了 Q 函数的近似。**Q 网络的输入是状态，输出是动作价值**（输出数量等于动作数量）。有两个神经网络：**在线网络**（通过梯度主动更新，最小化基于 TD 误差的 MSE 损失）和**目标网络**（滞后副本，使用硬更新或软更新/Polyak 更新进行较低频率的更新，由 tau 参数控制）。转移 (s,a,r,s') 存入**经验回放缓冲区**以打破时间相关性。

📎 *Source: Week 9 Slides 6-7, 10 — "Value function approximation and DQN", "DQN Online and Target Networks", "DQN training"*

---

## Q3. Describe at a high level how the PPO algorithm does value function approximation

**Q3. 从高层次描述 PPO 算法如何进行值函数近似**

PPO has an **Actor Network** and a **Critic Network (Value function)**. The Actor outputs action probabilities (the policy). The Critic estimates state value V(s) — this is the value function approximation part. Unlike DQN, PPO supports continuous action spaces.

> PPO 包含 **Actor 网络**和 **Critic 网络（价值函数）**。Actor 输出动作概率（策略）。Critic 估计状态价值 V(s)——这就是值函数近似的部分。与 DQN 不同，PPO 支持连续动作空间。

📎 *Source: Week 9 Slide 11 — "PPO and value function approximation"*

---

## Q4. Where would a neural network appear in an RL Problem/Solution?

**Q4. 神经网络会出现在 RL 问题/解决方案的哪些地方？**

1. **Q-Network** (DQN) — implements an approximation of Q; input is State, output is action values
2. **Actor Network** (PPO) — outputs action probabilities (the policy)
3. **Critic Network** (PPO) — estimates state value V(s), the value function
4. **Observation processing** — e.g., processing `image_raw` from camera before the agent

> 1. **Q 网络**（DQN）— 实现 Q 函数的近似；输入是状态，输出是动作价值
> 2. **Actor 网络**（PPO）— 输出动作概率（策略）
> 3. **Critic 网络**（PPO）— 估计状态价值 V(s)，即价值函数
> 4. **观测处理** — 如处理摄像头的 `image_raw`

📎 *Source: Week 9 Slides 6, 11 + Week 10 Slide 3*

---

## Q5. What are possible sources of training data for a neural network in RL?

**Q5. RL 中神经网络的训练数据可能来自哪些来源？**

1. **Agent-Environment Interaction** — Agent collects (s, a, r, s') transitions from the environment
2. **Replay Buffer** — Transitions are stored to break temporal correlations; Online Q-Network trains on random batches from the buffer
3. **Simulation** — Gazebo simulation (faster, safer, cheaper than real robot)
4. **Real-World** — physical robot interaction (expensive, slow)

> 1. **智能体与环境交互** — Agent 从环境中收集 (s, a, r, s') 转移
> 2. **经验回放缓冲区** — 存储转移数据以打破时间相关性；在线 Q 网络从缓冲区随机抽取批次进行训练
> 3. **仿真** — Gazebo 仿真（比真实机器人更快、更安全、更便宜）
> 4. **真实世界** — 物理机器人交互（昂贵、缓慢）

📎 *Source: Week 9 Slide 10 — "DQN training" + Week 10 Slide 3*

---

## Q6. Give an overview of the Assignment 2 strategy (Create3 robot training with simulation)

**Q6. 概述 Assignment 2 的策略（使用仿真训练 Create3 机器人）**

![RL Architecture (Source: Slide 3)](CST8509_10_Final_Review_slides_pages/page_003.png)

- **Gazebo** = 3D physics simulator (virtual AWS Small House + robot)
- **ROS 2** = communication framework; nodes communicating via topics: publish to `cmd_vel`, wait for `stop_status`, process `image_raw`, return observation + reward
- **SB3** = RL agent (Q-Learning or Stable-baselines3: DQN or PPO)
- **Gymnasium** = standard Agent/Environment cycle: $S_t$, $R_t$ → Agent → $A_t$ → Environment → $S_{t+1}$, $R_{t+1}$

Simulation is used because it's faster, safer, and cheaper than real-robot training.

> - **Gazebo** = 3D 物理仿真器（虚拟 AWS 小屋 + 机器人）
> - **ROS 2** = 通信框架；节点通过话题通信：发布到 `cmd_vel`，等待 `stop_status`，处理 `image_raw`，返回观察值 + 奖励
> - **SB3** = RL 智能体（Q-Learning 或 Stable-baselines3: DQN 或 PPO）
> - **Gymnasium** = 标准的智能体/环境循环：$S_t$, $R_t$ → 智能体 → $A_t$ → 环境 → $S_{t+1}$, $R_{t+1}$
>
> 使用仿真是因为比真实机器人训练更快、更安全、更便宜。

📎 *Source: Week 10 Slide 3 — "RL Diagrams with virtual Create"*

---

## Q7. SB3 agent with unsatisfactory results — what areas to explore?

**Q7. SB3 智能体效果不理想——应该从哪些方面排查？**

1. **Reward shaping** — add intermediate rewards
2. **Network capacity** — increase Q-network structure from `[64,64]` to `[512,512,256]` (more capacity and separation)
3. **Curriculum Learning** — make problem easier at beginning, increase difficulty; use `difficulty_level` and `start_flat`
4. **Exploration** — adjust ε-greedy schedule
5. **Hyperparameters** — `learning_starts`, `learning_rate`, batch size, γ
6. **Algorithm** — try PPO instead of DQN (or vice versa)

> 1. **奖励塑形** — 添加中间奖励
> 2. **网络容量** — 将 Q 网络结构从 `[64,64]` 增加到 `[512,512,256]`（更多容量和分离性）
> 3. **课程学习** — 一开始让问题更容易，逐步增加难度；使用 `difficulty_level` 和 `start_flat`
> 4. **探索** — 调整 ε-greedy 计划
> 5. **超参数** — `learning_starts`、`learning_rate`、batch size、γ
> 6. **算法** — 尝试 PPO 替代 DQN（或反之）

📎 *Source: Week 10 Slides 4, 6-7 — "DQN on Block-Stacking", "Curriculum Learning", "Q-network structure"*
