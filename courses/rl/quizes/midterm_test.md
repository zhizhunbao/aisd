# Reinforcement Learning Midterm Test

CST 8509 − Winter 2026 − Midterm − 15% Todd Kelley
25 M/C Questions (7.5%) + 5 Written Questions (7.5%)

---

## Part 1: Multiple Choice (25 Questions, 1 min each)

---

**Question 1** (1 point)
What is Reinforcement Learning (RL)?
什么是强化学习(RL)？

A) RL is a third type of machine learning, along with supervised learning and unsupervised learning. / RL 是第三种机器学习类型，与监督学习和无监督学习并列
B) None of these answers
C) All of these answers
D) RL is unsupervised machine learning used for control applications
E) RL is supervised machine learning for systems that play games

> **Answer**: A
> RL is neither supervised nor unsupervised — it is a distinct third paradigm based on trial-and-error interaction with an environment.
> RL 既不是监督学习也不是无监督学习，而是基于与环境试错交互的第三种范式。

---

**Question 2** (1 point)
Which of the following statements is true in the context of Reinforcement Learning?
以下哪些说法在强化学习的背景下是正确的？

A) None of these answers
B) Q-learning is a process for learning the action-value function / Q-learning 是学习动作价值函数的过程
C) All of these answers
D) Q-learning cannot be used directly on an environment with continuous actions or continuous states / Q-learning 不能直接用于连续动作或连续状态的环境
E) Q-learning can be applied to environments with manageable numbers of discrete actions and discrete states / Q-learning 可应用于离散动作和离散状态数量可控的环境

> **Answer**: C
> All three statements (B, D, E) are correct: Q-learning learns Q(s,a), requires discrete & manageable state-action spaces, and cannot directly handle continuous spaces.
> B、D、E 三个都对：Q-learning 学习 Q(s,a)，需要离散且可控的状态-动作空间，不能直接处理连续空间。

---

**Question 3** (1 point)
What is a Markov state?
什么是马尔可夫状态？

A) Markov states are states that form a single deterministic chain without cycles
B) None of these answers
C) Intuitively, a Markov state has the property that all its previous states determine whether it is a goal state
D) All of these answers
E) Intuitively, a Markov state has the property that its subsequent states do not depend on its previous states / 直觉上，马尔可夫状态的性质是：后续状态不依赖于之前的状态

> **Answer**: E
> Markov property: the future is independent of the past given the present. $P(s_{t+1}|s_t) = P(s_{t+1}|s_1,...,s_t)$.
> 马尔可夫性质：给定当前状态，未来与过去无关。

---

**Question 4** (1 point)
Which of the following methods of a Gymnasium environment would be called when an episode ends?
当一个 episode 结束时，会调用 Gymnasium 环境的哪个方法？

A) All of these answers
B) None of these answers
C) reset / 重置
D) render
E) step

> **Answer**: C
> When an episode ends (terminated or truncated), `reset()` is called to initialize the environment for the next episode.
> 当 episode 结束时，调用 `reset()` 初始化环境以开始下一个 episode。

---

**Question 5** (1 point)
What is a typical way that Stable-Baselines3 is used?
Stable-Baselines3 的典型使用方式是什么？

A) All of these answers
B) Train a model, then implement an environment based on that model
C) Train an environment, then create a model to be used instead of the environment
D) Create a model based on an environment, then train the model / 基于环境创建模型，然后训练模型
E) None of these answers

> **Answer**: D
> SB3 workflow: define/wrap a Gymnasium environment → instantiate an algorithm (e.g., DQN, PPO) → call `model.learn()` to train.
> SB3 工作流：定义/包装 Gymnasium 环境 → 实例化算法 → 调用 `model.learn()` 训练。

---

**Question 6** (1 point)
What is the Reward Hypothesis of Reinforcement Learning?
强化学习的奖励假说是什么？

A) None of these answers
B) ...some goals cannot be thought of as maximizing the expected cumulative value of a scalar reward function
C) ...all goals can be thought of as maximizing the expected cumulative value of a scalar reward function / 所有目标都可以被视为最大化标量奖励函数的期望累计值
D) ...all goals can be thought of as minimizing the number of steps to maximize a scalar reward function
E) ...some goals cannot be thought of as minimizing the number of steps to maximize a scalar reward function

> **Answer**: C
> Reward Hypothesis: all goals can be described as maximization of expected cumulative scalar reward.
> 奖励假说：所有目标都可以用最大化期望累计标量奖励来描述。

---

**Question 7** (1 point)
Which of the following is a part of every Gymnasium environment?
以下哪项是每个 Gymnasium 环境的组成部分？

A) A step method / step 方法
B) A neural network
C) None of these answers
D) All of these answers
E) A policy for taking action

> **Answer**: A
> Every Gymnasium environment must implement `step()` (and `reset()`). Neural networks and policies belong to the agent, not the environment.
> 每个 Gymnasium 环境必须实现 `step()`（和 `reset()`）。神经网络和策略属于智能体，不属于环境。

---

**Question 8** (1 point)
What is the relationship between Reinforcement Learning (RL) and Markov Decision Processes (MDPs)?
强化学习(RL)和马尔可夫决策过程(MDP)的关系是什么？

A) MDPs are known specific strategies developed for playing games like chess, go, and video games played by RL systems
B) MDPs are a mathematical model of the sequential decision making processes addressed by RL / MDP 是 RL 所解决的顺序决策过程的数学模型
C) None of these answers
D) MDPs are a component of the software used to implement video games
E) All of these answers

> **Answer**: B
> MDPs provide the formal mathematical framework (states, actions, transitions, rewards) that RL algorithms operate on.
> MDP 提供了 RL 算法运作的正式数学框架（状态、动作、转移、奖励）。

---

**Question 9** (1 point)
Which of the following statements is true about the Bellman equation in Reinforcement Learning?
以下关于贝尔曼方程的说法哪些是正确的？

A) None of these answers
B) It breaks the problem of determining the value of a state into smaller problems recursively / 将确定状态价值的问题递归地分解为更小的问题
C) All of these answers
D) It forms the mathematical basis for the Q-Learning algorithm / 构成 Q-Learning 算法的数学基础
E) It expresses the relationship between the value of a state or a state-action pair, and the value of the successor states / 表达状态（或状态-动作对）的价值与后继状态价值之间的关系

> **Answer**: C
> All three (B, D, E) are correct properties of the Bellman equation.
> B、D、E 三项都是贝尔曼方程的正确性质。

---

**Question 10** (1 point)
Which of the following is a feature of Stable-Baselines3?
以下哪项是 Stable-Baselines3 的功能？

A) All of these answers
B) Environment classes for standard Reinforcement Learning problems
C) None of these answers
D) Callback methods for implementing monitoring, progress bars, and more / 用于实现监控、进度条等的回调方法
E) Rendering methods based on PyGame

> **Answer**: D
> SB3 provides callback methods (e.g., `EvalCallback`, `CheckpointCallback`). SB3 does NOT provide environment classes (that's Gymnasium) or PyGame rendering.
> SB3 提供回调方法。SB3 不提供环境类（那是 Gymnasium）或 PyGame 渲染。

---

**Question 11** (1 point)
Which of the following statements is true in the context of Reinforcement Learning?
在强化学习的背景下，以下哪项说法是正确的？

A) The results of an action are determined by the agent rather than the environment
B) The value function and policy function are implemented in the agent rather than the environment / 价值函数和策略函数在智能体中实现，而非在环境中
C) The policy function is implemented in the environment rather than the agent
D) The value function is implemented in the environment rather than the agent
E) None of these answers

> **Answer**: B
> Agent contains policy and value function. Environment determines transition dynamics and rewards.
> 智能体包含策略和价值函数。环境决定转移动态和奖励。

---

**Question 12** (1 point)
What is Stable-Baselines3?
什么是 Stable-Baselines3？

A) None of these answers
B) A set of video game environment implementations
C) A set of standard Reinforcement Learning problems
D) All of these answers
E) A set of algorithm implementations for Reinforcement Learning / 一套强化学习算法的实现

> **Answer**: E
> SB3 = a library of RL algorithm implementations (DQN, PPO, A2C, SAC, etc.). It is NOT environments or games.
> SB3 = RL 算法实现库（DQN、PPO、A2C、SAC 等）。不是环境或游戏。

---

**Question 13** (1 point)
Which of the following is implemented in Stable-Baselines3?
以下哪项在 Stable-Baselines3 中实现？

A) None of these answers
B) GridWorld environment
C) DQN algorithm / DQN 算法
D) All of these answers
E) CliffWalking environment

> **Answer**: C
> SB3 implements algorithms like DQN. GridWorld and CliffWalking are Gymnasium environments, not SB3.
> SB3 实现 DQN 等算法。GridWorld 和 CliffWalking 是 Gymnasium 环境。

---

**Question 14** (1 point)
Which of the following is a step in creating and using a custom Gymnasium environment?
以下哪项是创建和使用自定义 Gymnasium 环境的步骤？

A) None of these answers
B) Instantiate the environment with gymnasium.make / 用 gymnasium.make 实例化环境
C) Register the name of the custom environment in the registry / 在注册表中注册自定义环境名称
D) Define a class that inherits from the Gymnasium Env class / 定义一个继承 Gymnasium Env 类的类
E) All of these answers / 以上全部

> **Answer**: E
> All three steps are required: define class (inheriting Env), register it, then use `gymnasium.make()`.
> 三个步骤都需要：定义类（继承 Env）、注册、用 `gymnasium.make()` 实例化。

---

**Question 15** (1 point)
What is the difference between an action value function and a state value function?
动作价值函数和状态价值函数有什么区别？

A) State value functions return total reward to termination, and action-value functions return immediate reward of taking the action
B) Action value functions return the average reward for taking an action, and State value functions return a state's average total future reward
C) None of these answers
D) State value functions take a state, and action value functions take just actions
E) Action value functions take state-action pairs, whereas state value functions take just states / 动作价值函数接受状态-动作对，而状态价值函数只接受状态

> **Answer**: E
> $V(s)$: input = state only. $Q(s,a)$: input = state + action. Both return expected cumulative return.
> $V(s)$：输入 = 仅状态。$Q(s,a)$：输入 = 状态+动作。两者都返回期望累计回报。

---

**Question 16** (1 point)
What is meant by "episode" in Reinforcement Learning?
强化学习中 "episode" 是什么意思？

A) None of these answers
B) An episode is a single run that cycles through the terminal state multiple times
C) An episode is a single run from the starting state to a terminal (or truncated) state / 一个 episode 是从起始状态到终止（或截断）状态的一次完整运行
D) An episode is a single cycle of performing an action, receiving a reward, and observing the resulting state
E) An episode is a number equal to the number of steps actually taken to reach the terminal state

> **Answer**: C
> Episode = one complete trajectory from start to terminal/truncated state. D describes a single time step, not an episode.
> Episode = 从起始到终止/截断状态的一条完整轨迹。D 描述的是单个时间步，不是 episode。

---

**Question 17** (1 point)
What are vectorized environments in the context of Stable-Baselines3?
在 Stable-Baselines3 中，什么是向量化环境？

A) They are used for representing multi-dimensional observations
B) They are a method for training an agent on more than one copy of an environment / 在多个环境副本上训练智能体的方法
C) All of these answers
D) They are a method for training multiple agents on a single environment
E) None of these answers

> **Answer**: B
> Vectorized environments run multiple copies of the same environment in parallel to speed up data collection for training.
> 向量化环境并行运行同一环境的多个副本，以加速训练数据收集。

---

**Question 18** (1 point)
What is a Policy in Reinforcement Learning?
强化学习中的策略(Policy)是什么？

A) The Policy is a function that assigns a value to each action-state pair
B) None of these answers
C) All of these answers
D) The Policy is a table that assigns a value to each action
E) The Policy is a function that determines the probability of an agent taking an action / 策略是决定智能体采取某个动作的概率的函数

> **Answer**: E
> Policy $\pi(a|s)$: maps state → probability distribution over actions. A describes Q-function, not policy.
> 策略 $\pi(a|s)$：状态 → 动作上的概率分布。A 描述的是 Q 函数，不是策略。

---

**Question 19** (1 point)
What is a condition for applying Q-learning to a Reinforcement Learning problem?
将 Q-learning 应用于强化学习问题的条件是什么？

A) The optimal value function must be known
B) The complete set of actions must be known
C) The complete set of possible states must be known
D) The complete set of actions and the complete set of possible states must be small enough to implement a q-table / 动作和状态的完整集合必须足够小，以实现 Q 表
E) None of these answers

> **Answer**: D
> Q-learning stores Q-values in a table indexed by (state, action). Both sets must be discrete and small enough to fit in memory.
> Q-learning 在以（状态，动作）为索引的表中存储 Q 值。两者都必须是离散的且足够小以放入内存。

---

**Question 20** (1 point)
Why role does the discount factor γ play in Reinforcement Learning?
折扣因子 γ 在强化学习中起什么作用？

A) γ addresses the problem of infinite cumulative rewards in non-terminating processes / γ 解决非终止过程中累计奖励无穷大的问题
B) None of these answers
C) γ represents the total discount which is subtracted from the total reward after an episode
D) γ determines how many times an action is chosen randomly during training
E) γ represents the weighting of the current goal of a Reinforcement Learning problem

> **Answer**: A
> Without γ < 1, the sum of rewards in infinite-horizon tasks diverges to ∞. The discount factor ensures convergence: $G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$.
> 没有 γ < 1，无限步任务的奖励和发散到 ∞。折扣因子确保收敛。

---

**Question 21** (1 point)
What does "greedy" mean in the context of Reinforcement Learning?
在强化学习中，"贪婪(greedy)"是什么意思？

A) None of these answers
B) It implies a policy where future reward is considered over immediate reward
C) It implies a policy that tries to maximize future reward
D) It implies a policy where immediate reward is considered over future reward / 意味着优先考虑即时奖励而非未来奖励的策略
E) It implies a policy that tries to maximize total reward

> **Answer**: D
> Greedy = always pick the action with the highest current estimated value (immediate best), without exploring alternatives.
> 贪婪 = 总是选当前估计价值最高的动作（即时最优），不探索替代方案。

---

**Question 22** (1 point)
What is Gymnasium in the context of Reinforcement Learning?
在强化学习的背景下，什么是 Gymnasium？

A) None of these answers
B) A set of standard algorithms for solving Reinforcement Learning problems
C) An algorithm for determining optimal hyper-parameter values
D) A library and API standard for environments that includes a number of pre-defined reference environments / 一个用于环境的库和 API 标准，包含若干预定义的参考环境
E) All of these answers

> **Answer**: D
> Gymnasium (successor to OpenAI Gym) provides a standard API for RL environments plus built-in reference environments (CartPole, MountainCar, etc.).
> Gymnasium 提供 RL 环境的标准 API 加上内置的参考环境。

---

**Question 23** (1 point)
What is a Value Function in Reinforcement Learning?
强化学习中的价值函数是什么？

A) A Value Function gives a measure of the expected total reward given a state or state-action pair / 价值函数给出给定状态或状态-动作对的期望总回报
B) A Value Function gives a measure of the expected total number of steps to maximize reward
C) None of these answers
D) All of these answers
E) A Value Function gives a measure of the expected total reward of an episode

> **Answer**: A
> $V(s)$ or $Q(s,a)$: expected cumulative return from a specific state (or state-action pair), not of the entire episode.
> $V(s)$ 或 $Q(s,a)$：从特定状态（或状态-动作对）出发的期望累计回报，不是整个 episode 的。

---

**Question 24** (1 point)
Which of the following can be considered primary aspects of a Reinforcement Learning problem setup?
以下哪项可以被视为强化学习问题设置的主要方面？

A) Values, Step function, and Actions
B) None of these answers
C) Reward, Environment, and Models
D) Agent, Values, and Step function
E) Agent, Environment, and Reward / 智能体、环境和奖励

> **Answer**: E
> The three primary aspects: Agent (decision maker), Environment (world), Reward (feedback signal).
> 三个主要方面：智能体（决策者）、环境（世界）、奖励（反馈信号）。

---

**Question 25** (1 point)
Which of the following methods of a Gymnasium environment returns an observation?
Gymnasium 环境的哪些方法返回观测(observation)？

A) make
B) step / step 方法
C) None of these answers
D) render
E) All of these answers

> **Answer**: B
> `step()` returns `(observation, reward, terminated, truncated, info)`. `reset()` also returns an observation, but it's not listed. `make()` returns the env object; `render()` returns visual output.
> `step()` 返回 `(observation, reward, terminated, truncated, info)`。`reset()` 也返回观测但未列出。

---

## Part 2: Written Questions (5 Questions, 25 marks)

---

**Question 26** (4 marks)
What is the purpose of this Python code and what does it?
这段 Python 代码的目的是什么？它做了什么？

```python
class DiscreteActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.dims = env.action_space.nvec
        self.action_space = gym.spaces.Discrete(np.prod(self.dims))
    def action(self, action):
        return np.unravel_index(action, self.dims)
```

> **Answer**:
> This wrapper converts a **MultiDiscrete** action space into a single **Discrete** action space, enabling algorithms like DQN (which only support Discrete actions) to work with multi-dimensional action environments.
>
> - `self.dims = env.action_space.nvec` — stores the shape of each action dimension (e.g., `[3, 3]`)
> - `self.action_space = gym.spaces.Discrete(np.prod(self.dims))` — flattens to a single integer space (e.g., 9 actions)
> - `np.unravel_index(action, self.dims)` — converts the flat integer back to multi-dimensional indices (e.g., `5 → (1, 2)`)
>
> 这个 wrapper 将 **MultiDiscrete** 动作空间转换为单个 **Discrete** 动作空间，使 DQN（只支持离散动作）能处理多维动作环境。
> - `nvec` 存储每个动作维度的大小
> - `np.prod` 将所有维度相乘得到总动作数
> - `np.unravel_index` 将扁平整数还原为多维索引

---

**Question 27** (4 marks)
Explain the meaning of "return" in the context of Reinforcement Learning.
解释强化学习中 "return" 的含义。

> **Answer**:
> **Return** $G_t$ is the **total discounted cumulative reward** from time step $t$ onward:
> $$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$
>
> - It is the quantity that the agent tries to **maximize**
> - The discount factor $\gamma \in [0,1]$ ensures the sum converges for infinite-horizon tasks
> - $\gamma$ close to 0 → agent is short-sighted; $\gamma$ close to 1 → agent values future rewards more
>
> **Return** $G_t$ 是从时间步 $t$ 起的**总折扣累计奖励**。智能体的目标是最大化 return。折扣因子 $\gamma$ 确保无限步任务中求和收敛。

---

**Question 28** (10 marks)
Draw the diagram that represents the primary aspects of a Reinforcement Learning problem/solution with agent-env interaction.
画出表示强化学习问题/解决方案主要方面的智能体-环境交互图。

> **Answer**:
> ```
>         Action (A_t)
>    Agent ──────────────► Environment
>      ▲                       │
>      │    Reward (R_{t+1})    │
>      │◄──────────────────────│
>      │    State  (S_{t+1})    │
>      │◄──────────────────────│
> ```
>
> **Key components**:
> 1. **Agent** — observes state, selects action via policy $\pi$
> 2. **Environment** — receives action, returns next state and reward
> 3. **State** $S_t$ — current observation of the environment
> 4. **Action** $A_t$ — agent's chosen action
> 5. **Reward** $R_{t+1}$ — scalar feedback signal
>
> The loop: $S_t, R_t \rightarrow$ Agent $\rightarrow A_t \rightarrow$ Environment $\rightarrow S_{t+1}, R_{t+1}$
>
> 循环：$S_t, R_t \rightarrow$ 智能体 $\rightarrow A_t \rightarrow$ 环境 $\rightarrow S_{t+1}, R_{t+1}$

---

**Question 29** (5 marks)
In Reinforcement Learning, what is an action-value function, and how could it be used to solve a Reinforcement Learning problem?
在强化学习中，什么是动作价值函数？它如何被用来解决强化学习问题？

> **Answer**:
> The **action-value function** $Q(s,a)$ gives the **expected cumulative return** starting from state $s$, taking action $a$, then following policy $\pi$:
> $$Q_\pi(s,a) = E_\pi[G_t | S_t=s, A_t=a]$$
>
> **How to use it to solve RL problems (Q-Learning)**:
> 1. Initialize Q-table with zeros
> 2. For each step: observe state $s$, choose action $a$ (ε-greedy), get reward $r$ and next state $s'$
> 3. Update: $Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$
> 4. Repeat until convergence
> 5. Extract optimal policy: $\pi^*(s) = \arg\max_a Q(s,a)$
>
> 动作价值函数 $Q(s,a)$：从状态 $s$ 执行动作 $a$ 后的期望累计回报。通过 Q-Learning 迭代更新 Q 表，收敛后提取最优策略。

---

**Question 30** (2 marks)
What is an observation in Reinforcement Learning?
强化学习中的观测(observation)是什么？

> **Answer**:
> An **observation** is the information the agent receives from the environment about its current state. It can be:
> - **Full state** (fully observable): e.g., grid position in GridWorld
> - **Partial observation** (partially observable): e.g., camera image (`image_raw`) in robotics
>
> In Gymnasium, observations are returned by `reset()` and `step()`, and their format is defined by `observation_space`.
>
> **观测** = 智能体从环境获取的关于当前状态的信息。可以是完全状态（如网格位置）或部分观测（如摄像头图像）。在 Gymnasium 中由 `reset()` 和 `step()` 返回。
