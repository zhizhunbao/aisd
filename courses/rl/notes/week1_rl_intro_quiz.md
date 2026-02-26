# Week 1: RL 入门 — 自测题

> **Source:** Based on Slides CST8509_01, Quiz 1, Lab 1, Sutton Ch.1

---

## 选择题 (Multiple Choice)

**Q1.** Which of the following best describes reinforcement learning?

A) Learning from labeled examples provided by a supervisor
B) Finding hidden structure in unlabeled data
C) Learning to maximize cumulative reward through trial-and-error interaction
D) Learning to minimize prediction error on a test set

> **Answer:** C
> RL 通过试错交互最大化累积奖励，这是它与监督学习（A）和无监督学习（B）的本质区别。

---

**Q2.** What are the two most important distinguishing features of RL according to Sutton?

A) Gradient descent and backpropagation
B) Trial-and-error search and delayed reward
C) Feature extraction and dimensionality reduction
D) Exploration and exploitation

> **Answer:** B
> Sutton §1.1 明确指出 trial-and-error search 和 delayed reward 是 RL 最重要的两个区分特征。D 是 RL 的一个挑战，但不是定义性特征。

---

**Q3.** In the agent-environment interaction, what does the agent receive at each time step?

A) Only a reward signal
B) A reward and an observation
C) An observation and an action
D) A reward, an observation, and it performs an action

> **Answer:** D
> 每个时间步：agent 接收 Reward + Observation，并执行 Action。$H_t = R_1, O_1, A_1, ..., R_t, O_t, A_t$

---

**Q4.** What is the Markov Property?

A) The future depends on the entire history of states
B) The probability of the next state depends only on the current state and action, not on earlier history
C) All states have equal probability of being visited
D) The agent always knows the environment state

> **Answer:** B
> 马尔可夫性质："给定当前状态，未来与过去无关。" $P(S_t, R_t)$ 仅取决于 $S_{t-1}$ 和 $A_{t-1}$。

---

**Q5.** A particle is moving in a straight line. Which of the following constitutes a Markov state?

A) Position only
B) Velocity only
C) Position and velocity
D) None of the above

> **Answer:** C
> 仅位置不是 Markov（不知道运动方向和速度）。位置+速度包含了预测未来所需的全部信息。

---

**Q6.** What is the difference between $V(s)$ and $Q(s,a)$?

A) $V(s)$ takes a state and action; $Q(s,a)$ takes only a state
B) $V(s)$ gives immediate reward; $Q(s,a)$ gives expected total reward
C) $V(s)$ takes only a state and gives expected return; $Q(s,a)$ takes a state and action and gives expected return
D) They are the same function with different notation

> **Answer:** C
> $V(s)$：状态→期望回报。$Q(s,a)$：状态+动作→期望回报。Quiz 1 Q6 和 Q7 的核心区别。

---

**Q7.** In Q-Learning, the Bellman equation states that $Q(s,a)$ equals:

A) Immediate reward minus maximum future reward
B) Immediate reward plus minimum future reward
C) Immediate reward plus maximum expected future reward in the next state
D) Sum of all past rewards

> **Answer:** C
> $Q(s,a) = r + \gamma \max_{a'} Q(s', a')$。即时奖励 + 折扣后的下一状态最大 Q 值。

---

**Q8.** Why can't we simply define total reward as the sum of all subsequent rewards?

A) The sum might be negative
B) The sum might be zero
C) The sum might be positive
D) The sum might be infinite

> **Answer:** D
> 在无限步任务中，直接求和可能发散到无穷大。这就是引入折扣因子 $\gamma$ 的原因。

---

**Q9.** Which RL agent type has both a policy and a value function?

A) Value Based
B) Policy Based
C) Actor Critic
D) Model Free

> **Answer:** C
> Actor Critic = Policy (actor) + Value Function (critic)。Value Based 只有 V/Q，Policy Based 只有 π。

---

**Q10.** The exploration-exploitation tradeoff:

A) Exists in all types of machine learning
B) Is unique to reinforcement learning
C) Only applies to model-based methods
D) Is solved by always choosing the greedy action

> **Answer:** B
> Sutton §1.1 明确指出探索-利用困境是 RL 独有的，在监督学习和无监督学习中不存在。

---

## 判断题 (True/False)

**T1.** In an MDP, taking an action in a state always leads to the same result state.

> **Answer:** False
> MDP 的转移是随机的：$P(s'|s,a)$。同一状态-动作对可以到达不同的下一状态。

---

**T2.** The value function includes rewards already received by the agent.

> **Answer:** False
> 价值函数只看未来奖励，不包括已经收到的奖励。在 Atari 游戏中，好事发生后价值下降，因为那个奖励已经"过去了"。

---

**T3.** A greedy policy always takes the action with the highest immediate reward.

> **Answer:** True
> 贪婪策略：$a = \arg\max_{a'} Q(s, a')$，总是选当前估计价值最高的动作。

---

**T4.** All reinforcement learning methods require a model of the environment.

> **Answer:** False
> Model-free 方法（如 Q-Learning）不需要环境模型，直接从经验中学习。

---

**T5.** The full history $H_t$ is always a valid Markov state.

> **Answer:** True
> 完整历史包含了所有信息，因此平凡地满足马尔可夫性质。但它不实用（太冗余）。

---

## 简答题 (Short Answer)

**S1.** Given $\gamma = 0.9$ and rewards $r_1 = -1, r_2 = -1, r_3 = -1, r_4 = 10$, calculate the discounted return $G_0$.

> **Answer:**
> $G_0 = (-1) + 0.9(-1) + 0.81(-1) + 0.729(10)$
> $= -1 - 0.9 - 0.81 + 7.29 = 4.58$
>
> 虽然前3步都是负奖励，但第4步的大正奖励（经折扣后）使得总回报为正。这体现了"牺牲短期换长期"的 RL 核心思想。

---

**S2.** In the Cliff Walking environment (Lab 1), why is the per-step reward set to -1 instead of 0?

> **Answer:**
> 每步 -1 的设计鼓励 agent 找到**最短路径**。如果每步奖励为 0，agent 没有动力尽快到达目标——它可以无限游荡而不受惩罚。负的每步奖励使得更短的路径获得更高的总回报（更少的 -1 累积）。
