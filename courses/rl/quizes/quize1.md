# Reinforcement Learning Quiz 1

---

**Question 1** (1 point)
What is a Markov chain?
什么是马尔可夫链？

A) A chain with a rubber coating
B) A sequence of nodes in a graph with cycles
C) A sequence of nodes in a graph without cycles
D) A mathematical model that experiences transition of states with probabilistic rules / 一种按概率规则进行状态转移的数学模型
E) None of these answers

> **Answer**: D
> A Markov chain is a mathematical model where states transition according to probabilistic rules. Only D describes probabilistic state transitions.
> 马尔可夫链 = 状态按概率规则转移的数学模型。只有 D 涉及概率性状态转移。

---

**Question 2** (1 point)
What is a Markov Decision Process?
什么是马尔可夫决策过程？

A) A process for making a decision between two options
B) The underlying logic of a Turing Machine
C) A process for making a decision between more than two options
D) An extension of the Markov chain with actions and rewards / 在马尔可夫链基础上增加了动作和奖励的扩展
E) None of these answers

> **Answer**: D
> MDP extends the Markov chain by adding actions and rewards. D is the only option that mentions both additions on top of a Markov chain.
> MDP = 马尔可夫链 + 动作 + 奖励。D 是唯一提到在马尔可夫链基础上加入 actions 和 rewards 的选项。

---

**Question 3** (1 point)
In a Markov Decision Process, taking an action in a state always leads to the same result state.
在 MDP 中，在某状态下执行某动作总是会到达相同的结果状态。

A) True
B) False

> **Answer**: B
> MDP transitions are defined by $P(s'|s,a)$; the same state-action pair can lead to different successor states — stochastic, not deterministic.
> MDP 转移由 $P(s'|s,a)$ 定义，同一状态-动作对可到达不同后继状态，是随机的，不是确定性的。

---

**Question 4** (1 point)
What is a problem with defining total reward from a starting point to be the sum of all subsequent rewards?
将总回报定义为从起点开始所有后续奖励之和，会有什么问题？

A) The sum of all subsequent rewards might be negative
B) The sum of all subsequent rewards might be zero
C) The sum of all subsequent rewards might be positive
D) None of these answers
E) The sum of all subsequent rewards might be infinite / 所有后续奖励之和可能为无穷大

> **Answer**: E
> In infinite-horizon tasks, the raw sum can diverge to $\infty$, making policy comparison impossible. This is why the discount factor $\gamma$ is introduced.
> 无限步任务中直接求和可能发散到 $\infty$，无法比较策略。这正是引入折扣因子 $\gamma$ 的原因。

---

**Question 5** (1 point)
What is a policy in Reinforcement Learning?
强化学习中的策略(Policy)是什么？

A) A function that specifies what action to take in a certain state / 指定在某状态下采取什么动作的函数
B) A function that specifies the next state to visit
C) A function that gives the list of all possible actions in a state
D) None of these answers
E) A function that gives the list of all impossible actions in a state

> **Answer**: A
> A policy $\pi(a|s)$ maps a given state to an action to take. A is exactly this definition.
> 策略 $\pi(a|s)$：给定状态 → 告诉你选什么动作。A 正是定义。

---

**Question 6** (1 point)
What is given by the state value function?
状态价值函数给出的是什么？

A) It takes a state and gives the expected total reward we can get starting from that state / 接受一个状态，给出从该状态出发的期望总回报
B) It takes a state and gives an action that results in the highest reward
C) None of these answers
D) It takes an action and a state and gives the expected total reward we can get from taking that action / 接受状态和动作，给出采取该动作的期望总回报
E) It takes an action and gives the state that results from taking that action

> **Answer**: A
> $V(s)$: state → expected cumulative return. B describes the policy's job; D describes $Q(s,a)$.
> $V(s)$：状态 → 期望累计回报。B 是策略的职责；D 描述的是 $Q(s,a)$。

---

**Question 7** (1 point)
What is the action value function?
什么是动作价值函数？

A) It takes a state and gives expected total reward we can get starting from that state
B) It takes a state and an action and gives the state resulting from taking the action
C) It takes a state and an action and gives the immediate reward resulting from taking that action / 接受状态和动作，给出即时奖励
D) It takes a state and an action and gives the expected total reward we can get starting from that state and taking that action / 接受状态和动作，给出从该状态执行该动作后的期望总回报
E) None of these answers

> **Answer**: D
> $Q(s,a)$: state + action → expected cumulative return. A is $V(s)$ (missing action); C is just immediate reward $R$, not cumulative.
> $Q(s,a)$：状态+动作 → 期望累计回报。A 是 $V(s)$（缺动作）；C 只是即时奖励 $R$，不是累计。

---

**Question 8** (1 point)
What is a greedy policy?
什么是贪婪策略？

A) A policy that rotates through all actions
B) A policy that dictates always taking rather than giving
C) None of these answers
D) A policy that dictates always taking the action that results in the highest immediate reward / 总是选择产生最高即时奖励的动作的策略
E) A policy that always specifies the same action

> **Answer**: D
> A greedy policy always selects the action with the highest estimated value: $a = \arg\max_{a'} Q(s, a')$.
> 贪婪策略 = 每次选当前估计价值最高的动作：$a = \arg\max_{a'} Q(s, a')$。

---

**Question 9** (1 point)
What does the Bellman Equation say in the context of Q-Learning?
在 Q-Learning 的语境下，贝尔曼方程表达了什么？

A) ...immediate reward + total **past** rewards from the previous state / 即时奖励 + 之前状态的**历史**回报
B) ...immediate reward **minus** the maximum expected future rewards / 即时奖励 **减去** 最大期望未来回报
C) ...immediate reward + the **minimum** expected future rewards / 即时奖励 + **最小**期望未来回报
D) None of these answers
E) ...immediate reward + the **maximum** expected future rewards in the next state / 即时奖励 + 下一状态的**最大**期望未来回报

> **Answer**: E
> Bellman equation: $Q(s,a) = R + \gamma \max_{a'} Q(s',a')$. Only E says "immediate reward **+** **maximum** future return". A looks backward; B uses minus; C uses minimum.
> 贝尔曼方程：$Q(s,a) = R + \gamma \max_{a'} Q(s',a')$。只有 E 说"即时奖励 + 最大未来回报"。A 回溯过去；B 用减号；C 取最小。
