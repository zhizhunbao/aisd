# CST8509 期末笔试题 — 完整参考答案

> **Source:** `CST8509_10_Final_Review_slides.md` §5.2 (Slides 11-12)
> **用途：** 期末复习用，每题按"先中文直觉 → 再英文正式答案 → 最后答题要点"的结构组织

---

## Q1. How can Reinforcement Learning be applied to problems where the number of states is huge?
> 强化学习如何应用于状态数量庞大的问题中？

### 💡 中文直觉

传统 Q-Table 像背乘法表——状态多到 300 万种时根本背不完。解决方案是把"背答案"换成"学规律"：用**神经网络替代 Q-Table**（即 Value Function Approximation / 值函数近似），让网络根据状态的**特征**来"推算"价值，而不是逐个记忆。

### ✅ English Answer

When the state space is too large for a tabular approach (e.g., millions of states), RL uses **Value Function Approximation (VFA)** — replacing the Q-Table with a **parameterized function approximator**, typically a **deep neural network**.

**Key techniques:**

1. **DQN (Deep Q-Network):** A neural network takes the **state** as input and outputs estimated **Q-values** for all possible actions. Instead of storing a Q-value for every state-action pair (impossible with millions of states), the network learns **generalizable patterns** from the state representation. This means it can estimate Q-values even for states **never seen during training**.

2. **State Encoding (e.g., One-hot Vectors):** States are encoded as numerical vectors that the neural network can process. For example, in 6×6 block-stacking, each block's position is encoded as a 12-bit one-hot vector, resulting in a 144-dimensional input vector.

3. **PPO (Proximal Policy Optimization):** Instead of approximating the value function, PPO directly learns a **policy function** (mapping from states to action probabilities) using a neural network. This also handles arbitrarily large state spaces.

4. **Curriculum Learning:** To deal with sparse rewards in large state spaces, the problem difficulty is gradually increased — start with easy configurations where the agent can get positive feedback, then progressively increase difficulty.

5. **Experience Replay:** Transitions $(s, a, r, s')$ are stored in a **replay buffer** and randomly sampled for training, improving data efficiency and training stability.

### 📝 答题要点
- ✅ 提到 **Value Function Approximation**（值函数近似）
- ✅ 提到 **Neural Network replaces Q-Table**（神经网络替代Q表）
- ✅ 提到网络能**泛化到未见过的状态**（generalize to unseen states）
- ✅ 可选加分：提及 One-hot encoding、Curriculum Learning、Experience Replay

---

## Q2. Describe at a high level how the DQN algorithm does value function approximation
> 概要描述 DQN 算法是如何进行值函数近似的

### 💡 中文直觉

DQN 的核心思路：训练一个神经网络当"计算器"——你给它任意一个状态（比如 144 维向量），它就能算出每个可能动作的分数（Q 值），哪个分数最高就选哪个动作。这就是"近似"——不是精确的查表结果，而是网络"猜"的，但猜得越来越准。

### ✅ English Answer

DQN replaces the Q-Table with a **Q-Network** (a deep neural network) that **approximates** the Q-value function:

1. **Input:** The current state, encoded as a numerical vector (e.g., a 144-dimensional one-hot encoded vector for block-stacking).

2. **Output:** Estimated Q-values for **every possible discrete action** — one number per action.

3. **Action Selection:** The agent takes the action with the **highest Q-value** (with ε-greedy exploration during training).

4. **Training Process:**
   - The agent interacts with the environment and stores transitions $(s, a, r, s')$ in a **replay buffer**.
   - Random mini-batches are sampled from the replay buffer.
   - For each transition, a **target Q-value** is computed: $y = r + \gamma \max_{a'} Q_{target}(s', a')$, using a separate **target network** (a slowly updated copy of the Q-network).
   - The Q-network's weights are updated to minimize the **MSE loss** between predicted Q-value $Q(s, a)$ and target $y$.

5. **Key Stabilization Mechanisms:**
   - **Replay Buffer:** Breaks correlation between consecutive samples.
   - **Target Network:** Prevents the "moving target" instability (training against a constantly changing objective).

**In essence:** DQN learns a **function** $Q_\theta(s, a)$ parameterized by network weights $\theta$ that maps any state-action pair to an estimated value, instead of storing explicit values in a table.

### 📝 答题要点
- ✅ Neural network takes **state as input**, outputs **Q-values for all actions**
- ✅ Trained using **experience replay** (random sampling from buffer)
- ✅ Uses a **target network** for stable training targets
- ✅ Minimizes **MSE** between predicted and target Q-values
- ✅ Selects action with **highest Q-value** (+ ε-greedy exploration)

---

## Q3. Describe at a high level how the PPO algorithm does value function approximation
> 概要描述 PPO 算法是如何进行值函数近似的

### 💡 中文直觉

PPO 和 DQN 的**方法论完全不同**。DQN 先学"每个动作值多少分（Q 值）"再选分最高的。PPO 则**跳过 Q 值**，直接训练网络输出"每个动作该选的概率"。PPO 属于 Actor-Critic 架构：Actor（演员）学策略，Critic（评论家）学价值——两个网络分工合作。

### ✅ English Answer

PPO (Proximal Policy Optimization) takes a fundamentally **different approach** from DQN. While DQN approximates the **Q-value function** (value-based, indirect), PPO directly approximates the **policy** (policy-based, direct) using an **Actor-Critic architecture**:

1. **Actor Network (Policy Approximation):**
   - Takes the **state** as input.
   - Outputs a **probability distribution over actions** (e.g., "60% left, 30% right, 10% stay").
   - The agent samples actions according to these probabilities — this is its **policy** $\pi_\theta(a|s)$.

2. **Critic Network (Value Function Approximation):**
   - Also takes the **state** as input.
   - Outputs a **single scalar** — the estimated state value $V(s)$ (how good it is to be in this state).
   - This is used to compute the **advantage** $A = Q(s,a) - V(s)$ — "how much better was this action compared to the average?"

3. **Training Process:**
   - The agent collects a batch of experience by running the current policy.
   - The **advantage** is computed for each transition.
   - The **actor** (policy network) is updated to increase the probability of actions with **positive advantage** and decrease those with **negative advantage**.
   - The update is **clipped** to prevent too-large policy changes — this is the "Proximal" part, ensuring stable, conservative updates.
   - The **critic** (value network) is updated to more accurately predict state values.

4. **Key Differences from DQN:**
   - PPO can handle **both discrete and continuous** action spaces (DQN: discrete only).
   - PPO does **not** use a replay buffer (on-policy: uses fresh data only).
   - PPO updates are **more conservative/stable** — less prone to training collapse.

### 📝 答题要点
- ✅ PPO **directly learns a policy** (action probabilities), not Q-values
- ✅ Uses **Actor-Critic** architecture: Actor = policy, Critic = value function
- ✅ Actor outputs **action probability distribution**
- ✅ Critic outputs **state value V(s)** for computing advantage
- ✅ Updates are **clipped** for stability (proximal/conservative)
- ✅ 可选加分：提及 PPO 支持 continuous action spaces, 不需要 Replay Buffer

---

## Q4. Where would a neural network appear in a Reinforcement Learning Problem/Solution?
> 神经网络会在强化学习问题/解决方案中的什么地方出现？

### 💡 中文直觉

神经网络在 RL 中最少有 3 个"藏身之处"：① 当 Q-Table 的替身（估算 Q 值），② 当策略的替身（直接输出动作概率），③ 当环境模型（预测下一个状态和奖励）。在我们的课程中主要用到了前两种。

### ✅ English Answer

Neural networks can appear in **several places** within an RL system:

### 1. **As the Q-Value Function Approximator (Value-Based Methods)**
- **Where:** Inside the **agent**, replacing the Q-Table.
- **Role:** Takes a state as input, outputs estimated Q-values for each action.
- **Example:** **DQN** uses a Q-network (e.g., `[512,512,256]` architecture) — Input: 144-dim one-hot state vector → Output: Q-value for each of the possible actions.
- **Also includes:** The **target network** (a frozen copy used for computing stable training targets).

### 2. **As the Policy Function (Policy-Based Methods)**
- **Where:** Inside the **agent**, directly representing the policy.
- **Role:** Takes a state as input, outputs **action probabilities** (or continuous action parameters).
- **Example:** **PPO's Actor network** — maps states to a probability distribution over actions.

### 3. **As the Value Function Estimator in Actor-Critic**
- **Where:** The **Critic** component of Actor-Critic methods.
- **Role:** Estimates the state value $V(s)$ to compute the advantage for the policy update.
- **Example:** **PPO's Critic network** — ranks how "good" the current state is.

### 4. **As an Environment Model (Model-Based RL)**
- **Where:** Inside the **agent's planning module** (not used in this course, but worth mentioning).
- **Role:** Predicts the next state and reward given current state and action — learned from experience.
- **Example:** World models in MuZero.

### 5. **As Part of Observation Processing**
- **Where:** Between raw sensor data and the RL agent.
- **Role:** Processes high-dimensional inputs (e.g., images) into compact state representations.
- **Example:** CNN layers processing `image_raw` from Gazebo/Create3 camera before feeding into the Q-network.

### 📝 答题要点
- ✅ **Q-Value approximator** (DQN — replacing Q-Table)
- ✅ **Policy function** (PPO Actor — outputting action probabilities)
- ✅ **Value estimator** (PPO Critic — estimating V(s))
- ✅ 可选加分：提及 environment model 或 observation processing (CNN for images)

---

## Q5. What are possible sources of training data for a neural network in a Reinforcement Learning Problem/Solution?
> 在强化学习问题/解决方案中，神经网络训练数据的可能来源有哪些？

### 💡 中文直觉

RL 和传统监督学习最大的不同：**没有预先标注好的数据集**。训练数据来自智能体自己和环境的交互——每走一步就产生一条训练数据 $(s, a, r, s')$。这些数据可以来自真实世界，也可以来自仿真器（如 Gazebo）。

### ✅ English Answer

Unlike supervised learning (which needs a pre-labeled dataset), **RL generates its own training data through interaction**. The possible sources are:

### 1. **Agent-Environment Interaction (Primary Source)**
- Every time step produces a **transition tuple**: $(s_t, a_t, r_t, s_{t+1})$
- Meaning: "In state $s_t$, the agent took action $a_t$, received reward $r_t$, and transitioned to state $s_{t+1}$."
- These transitions are the **raw training data** for the neural network.

### 2. **Replay Buffer (Stored Past Experience)**
- Transitions are stored in an **experience replay buffer** and randomly sampled later for training.
- This provides a **reusable, decorrelated** source of training data.
- Example: `learning_starts=2000` → first 2000 transitions are collected and stored before training begins.

### 3. **Simulation Environments**
- **Gymnasium environments** (e.g., CartPole, FrozenLake, custom BlocksWorld)
- **Gazebo 3D Physics Simulator** with ROS 2 (e.g., Create3 robot in AWS Small House)
- Simulations generate transitions much **faster and safer** than real-world interaction.
- Virtual sensors provide `image_raw`, `stop_status`, etc.

### 4. **Real-World Robot Interaction**
- A physical robot (e.g., iRobot Create3) interacting with the real environment.
- Expensive, slow, and risky — but provides the most realistic data.
- Usually only used for **fine-tuning** after simulation pre-training.

### 5. **Demonstrations / Expert Data (Imitation Learning)**
- Pre-recorded trajectories from a human expert or a trained agent.
- Used to **pre-fill** the replay buffer or pre-train the network before RL training begins.
- Not explicitly covered in this course, but a recognized technique.

### 📝 答题要点
- ✅ **Agent-environment interaction** → transition tuples $(s, a, r, s')$
- ✅ **Replay Buffer** — stored past experiences, randomly sampled
- ✅ **Simulation** (Gymnasium, Gazebo) — fast and safe data generation
- ✅ **Real-world interaction** — expensive but realistic
- ✅ 可选加分：提及 expert demonstrations / imitation learning

---

## Q6. Give an overview of the strategy used in Assignment 2 (Create3 robot training with simulation)
> 概述 Assignment 2 中通过仿真训练 Create3 机器人的策略

### 💡 中文直觉

Assignment 2 搭了一个"虚拟实验室"系统：Gazebo 模拟物理世界 → ROS 2 负责模块间通信 → SB3 算法在里面训练 → 学完后可以直接迁移到真机器人上。就像用飞行模拟器练飞行员，不需要真的去天上冒险。

### ✅ English Answer

Assignment 2 uses a **simulation-based RL pipeline** to train a virtual Create3 robot. The major tools, technologies, and their interactions are:

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│              TRAINING PIPELINE                   │
│                                                  │
│  ┌──────────────────┐    ┌──────────────────┐   │
│  │  SB3 Agent       │    │  Gazebo          │   │
│  │  (DQN / PPO)     │◄──►│  3D Simulator    │   │
│  │  - Q-Network     │    │  - AWS Small House│   │
│  │  - Replay Buffer │    │  - Virtual Create3│   │
│  │  - Policy        │    │  - Physics Engine │   │
│  └────────┬─────────┘    └────────┬─────────┘   │
│           │        ROS 2          │              │
│           │    (Communication)    │              │
│           └───────────────────────┘              │
│            cmd_vel ↑    ↓ image_raw              │
│                        ↓ stop_status             │
└─────────────────────────────────────────────────┘
```

### Components and Their Roles

| Component | Purpose | Interaction |
|---|---|---|
| **Gazebo** (3D Physics Simulator) | Simulates a virtual house (AWS Small House) with a virtual Create3 robot. Handles physics (collisions, movement), virtual sensors (camera), and rendering. | Receives velocity commands → simulates robot motion → returns sensor data |
| **ROS 2** (Communication Framework) | Acts as the "nervous system" connecting all components via topics (publish/subscribe messaging). | Carries `cmd_vel` (velocity commands), `image_raw` (camera images), `stop_status` signals between Agent and Gazebo |
| **Stable-Baselines3 (SB3)** (RL Algorithm Library) | Provides the RL agent implementation (DQN or PPO). The agent's "brain" that decides which actions to take based on observations. | Receives observations + rewards from the Gymnasium wrapper → outputs actions |
| **Gymnasium Environment** (Standardized Interface) | Wraps the ROS2/Gazebo system into the standard `reset()/step()` API that SB3 expects. Converts raw sensor data into observations and computes rewards. | Bridges SB3 ↔ ROS2/Gazebo |
| **Docker** | Containerizes the Python environment and ROS 2 workspace, ensuring reproducible dependencies and isolated environments. | Packages all above components |

### The Training Loop

1. Gymnasium `reset()` → Gazebo resets the simulation to initial state.
2. Agent receives observation ($S_t$: processed `image_raw`) and reward ($R_t$).
3. Agent (SB3 DQN/PPO) computes action ($A_t$).
4. Action is published to `cmd_vel` via ROS 2 → Gazebo moves the virtual robot.
5. Agent waits for `stop_status`, processes new `image_raw`.
6. Gymnasium returns new observation + reward → back to step 2.
7. After training, the learned policy can be deployed to a **real Create3 robot** with minimal changes (sim-to-real transfer).

### Why Simulation?
- **Speed:** Thousands of episodes in hours (vs. days on a real robot).
- **Safety:** No risk of damaging hardware or the environment.
- **Reset:** Instant environment reset after each episode.
- **Cost:** No physical hardware needed during development.

### 📝 答题要点
- ✅ **Gazebo** = 3D physics simulator (simulates robot + environment)
- ✅ **ROS 2** = communication framework (topics: `cmd_vel`, `image_raw`, `stop_status`)
- ✅ **SB3** = RL agent (DQN/PPO algorithm)
- ✅ **Gymnasium** = standardized environment interface (`reset()`/`step()`)
- ✅ Explain the **interaction loop**: observation → action → simulation → new observation
- ✅ 可选加分：提及 Docker, sim-to-real transfer, 为什么用仿真而不是真机

---

## Q7. Suppose you are running an SB3 agent on a gymnasium environment with unsatisfactory results. What areas could you explore to improve results?
> 假设你在 Gymnasium 环境中运行 SB3 智能体但结果不理想，可以探索哪些方向来改善？

### 💡 中文直觉

效果不好时，不要只想到"调参"——这只是五个方向中的一个。你应该系统地检查整个管道：奖励设计 → 网络能力 → 训练策略 → 探索策略 → 超参数。

### ✅ English Answer

There are **multiple areas** to investigate systematically when SB3 results are unsatisfactory:

### 1. 🎯 Reward Design (奖励设计)
- **Is the reward too sparse?** If the agent rarely receives any positive reward, it has no learning signal. 
  - **Fix:** Add intermediate/shaping rewards, or use **curriculum learning** to start with easier variants of the task.
- **Is the reward misleading?** Sutton: reward should communicate **what** to achieve, not **how** to achieve it. Don't reward subgoals — reward the final objective.
- **Scale:** Are reward magnitudes appropriate? Very large/small rewards can destabilize training.

### 2. 🧠 Network Architecture (网络结构)
- **Is the network too small?** The default `[64, 64]` may lack **capacity** to represent complex state-action mappings.
  - **Fix:** Increase to `[512, 512, 256]` or larger — more neurons can learn more patterns.
- **Is the network too shallow?** Shallow networks may fail to learn complex **joint patterns** (e.g., combinations of block positions).
  - **Fix:** Add more layers for better **separation** of features.
- **Wrong policy type?** Using `MlpPolicy` when observations are dictionaries → switch to `MultiInputPolicy`.

### 3. 📚 Training Strategy (训练策略)
- **Curriculum Learning:** Start with simplified versions of the task (`start_flat=True`, low `difficulty_level`), then gradually increase difficulty.
- **`learning_starts`:** Is the agent training too early before accumulating enough diverse experience? Increase the warm-up period.
- **`batch_size`:** Too small → noisy updates; too large → slow learning.
- **Total training steps:** Maybe the agent simply hasn't trained long enough.

### 4. 🔍 Exploration Strategy (探索策略)
- **Epsilon decay schedule:** Is ε-greedy decaying too fast (agent stops exploring prematurely) or too slow (agent won't commit to learned strategy)?
- **Initial exploration phase:** `exploration_initial_eps` and `exploration_final_eps` settings.
- **Entropy bonus (PPO):** Encourage more diverse actions early in training.

### 5. ⚙️ Hyperparameters (超参数)
- **Learning rate ($\alpha$):** Too high → unstable; too low → too slow.
- **Discount factor ($\gamma$):** Too low → myopic (only sees immediate rewards); too high → noisy (far-future rewards add variance).
- **`target_update_interval` (DQN):** How often the target network syncs — affects training stability.
- **Buffer size:** Is the replay buffer too small (forgetting useful old experience)?

### 6. 🌍 Environment Design (环境设计)
- **Observation space:** Is the state representation informative enough? Does the agent have all the information it needs to make good decisions?
- **Action space:** Is it appropriately discretized? Using `DiscreteActionWrapper` if needed for DQN compatibility?
- **Episode length:** Too short (agent can't reach the goal) or too long (wastes time on hopeless episodes)?

### 7. 📈 Monitoring & Debugging (监控与调试)
- **TensorBoard:** Check `ep_rew_mean` curve — is it flat, oscillating, or diverging?
- **Callbacks:** Use `EvalCallback` for periodic evaluation on a separate environment.
- **Algorithm choice:** Maybe DQN is wrong for this task — try PPO (handles continuous actions, more stable updates).

### 📝 答题要点
- ✅ **Reward design** — 是否太稀疏/误导性
- ✅ **Network architecture** — 是否太小/太浅
- ✅ **Curriculum learning** — 是否需要先简单后困难
- ✅ **Exploration rate (epsilon)** — 衰减是否合理
- ✅ **Hyperparameters** — learning_starts, batch_size, learning rate, γ
- ✅ 可选加分：提及 observation space 设计, 算法选型 (DQN ↔ PPO), TensorBoard 监控

---

## 📋 总结：答题速查表

| 题号 | 核心关键词 | 必须提到的概念 |
|---|---|---|
| Q1 | Huge state space | Value Function Approximation, Neural Network replaces Q-Table, generalization |
| Q2 | DQN value approx | Q-Network (input=state, output=Q-values), Replay Buffer, Target Network, MSE loss |
| Q3 | PPO value approx | Actor-Critic, Actor=policy (probabilities), Critic=V(s), clipped updates |
| Q4 | Where NN appears | Q-value approx (DQN), Policy (PPO Actor), Value estimator (PPO Critic) |
| Q5 | Training data sources | Agent-env interaction → $(s,a,r,s')$, Replay Buffer, Simulation (Gazebo), Real-world |
| Q6 | Assignment 2 overview | Gazebo=simulator, ROS2=communication, SB3=agent, Gymnasium=interface, interaction loop |
| Q7 | Improve results | Reward design, network size, curriculum learning, exploration rate, hyperparameters |
