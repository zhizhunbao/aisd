# Reinforcement Learning Quiz 2

---

**Question 1** (1 point)
What is Reinforcement Learning (RL)?
什么是强化学习？

A) All of these answers.
B) RL is a third type of machine learning, along with supervised learning and unsupervised learning. / RL 是与监督学习、无监督学习并列的第三种机器学习范式。
C) RL is a form of supervised machine learning used for learning to play games.
D) RL is a form of unsupervised machine learning used in control applications.
E) None of these answers.

> **Answer**: B
> RL is one of the three ML paradigms (supervised / unsupervised / reinforcement), learning optimal policies through trial-and-error interaction with an environment. Only B correctly positions RL as a peer paradigm. C/D wrongly classify it as a sub-type.
> RL 是机器学习三大范式之一，通过与环境的试错交互学习最优策略。只有 B 正确定位了 RL 的并列关系。C/D 错误地将 RL 归为子类。

---

**Question 2** (1 point)
Which of the following can be considered primary aspects of a Reinforcement Learning problem setup?
以下哪些是强化学习问题设定的核心要素？

A) Values, Step function, and Actions.
B) Agent, Environment, and Reward. / 智能体、环境和奖励。
C) Reward, Environment, and States.
D) Agent, Values, and Step function.
E) None of these answers.

> **Answer**: B
> The three primary elements of RL are Agent, Environment, and Reward. C is close but missing Agent — States are a property of Environment, not a standalone setup element.
> RL 核心三要素是 Agent、Environment、Reward。C 缺少 Agent——States 是环境的属性，不是独立的核心设定要素。

---

**Question 3** (1 point)
What is a Markov state?
什么是马尔可夫状态？

A) None of these answers.
B) All of these answers.
C) Markov states are states that form a single deterministic chain.
D) Intuitively, a Markov state has the property that all its previous states completely determine its future states.
E) Intuitively, a Markov state has the property that its subsequent states do not depend on its previous states. / 马尔可夫状态的后续状态不依赖于先前状态。

> **Answer**: E
> Markov property: future depends only on the current state, not history. E captures this. D says the opposite — that all previous states determine the future, which contradicts the Markov property.
> 马尔可夫性质：未来只取决于当前状态，与历史无关。E 正确。D 恰好相反——说"所有先前状态决定未来"，与马尔可夫性矛盾。

---

**Question 4** (1 point)
What is the relationship between Reinforcement Learning (RL) and Markov Decision Processes (MDPs)?
强化学习和马尔可夫决策过程之间是什么关系？

A) MDPs are a mathematical model of the sequential decision making processes addressed by RL. / MDP 是 RL 所处理的序贯决策过程的数学模型。
B) None of these answers.
C) MDPs are a component of the software used to implement video games.
D) MDPs are known specific strategies developed for playing games like chess, go, and video games played by RL systems.
E) All of these answers.

> **Answer**: A
> MDP is the standard mathematical framework RL uses to describe sequential decision problems. C/D mischaracterize MDP as software components or specific game strategies.
> MDP 是 RL 用于描述序贯决策问题的标准数学框架。C/D 分别将 MDP 误解为软件组件和具体博弈策略。

---

**Question 5** (1 point)
What is the Reward Hypothesis of Reinforcement Learning?
什么是强化学习的奖励假设？

A) The Reward Hypothesis basically states that some goals cannot be thought of as maximizing the expected cumulative value of a scalar reward function.
B) The Reward Hypothesis basically states that all goals can be thought of as minimizing the number of steps to maximize a scalar reward function.
C) The Reward Hypothesis basically states that some goals cannot be thought of as minimizing the number of steps to maximize a scalar reward function.
D) None of these answers.
E) The Reward Hypothesis basically states that all goals can be thought of as maximizing the expected cumulative value of a scalar reward function. / 所有目标都可以表述为最大化标量奖励的累积期望值。

> **Answer**: E
> Reward Hypothesis: all goals = maximizing expected cumulative scalar reward. E contains the key elements — "all goals + maximizing + expected cumulative + scalar reward". A contradicts with "some cannot"; B/C focus on minimizing steps.
> 奖励假设：所有目标 = 最大化累积标量奖励的期望。E 包含关键要素。A 用"some cannot"矛盾；B/C 关注最小化步数。

---

**Question 6** (1 point)
What is meant by "episode" in Reinforcement Learning?
强化学习中的"回合(Episode)"是什么意思？

A) An episode is a single cycle of performing an action, receiving a reward, and observing the resulting state.
B) An episode is a single run from the starting state to a terminal (or truncated) state. / 从初始状态到终止（或截断）状态的一次完整运行。
C) An episode is a single run that does not reach the terminal state.
D) An episode is the number of steps actually taken to reach the terminal state.
E) None of these answers.

> **Answer**: B
> An episode is a complete interaction sequence from start state to terminal state. A describes a single time step, not a full episode. C/D contradict or misdefine it.
> 回合是从初始状态到终止状态的一次完整交互序列。A 描述的是单个 time step，不是整个回合。

---

**Question 7** (1 point)
What role does the discount factor $\gamma$ play in Reinforcement Learning?
折扣因子 $\gamma$ 在强化学习中起什么作用？

A) $\gamma$ addresses the problem of infinite cumulative rewards in non-terminating processes. / $\gamma$ 解决非终止过程中累积奖励可能无穷的问题。
B) $\gamma$ determines how many times an action is chosen randomly during training.
C) $\gamma$ represents the total discount which is subtracted from the reward function cumulative total.
D) None of these answers.
E) $\gamma$ represents the weighting of the current goal of a Reinforcement Learning problem.

> **Answer**: A
> $\gamma \in [0,1)$ ensures infinite-horizon returns converge via geometric discounting $G_t = \sum \gamma^k R_{t+k+1}$. B confuses with $\epsilon$-greedy exploration; C misunderstands as subtraction; E misdefines the role.
> $\gamma \in [0,1)$ 通过几何衰减使无限步回报收敛。B 混淆了 $\epsilon$-greedy 探索；C 误解为减法；E 错误定义作用。

---

**Question 8** (1 point)
What is a Policy in Reinforcement Learning?
强化学习中的策略(Policy)是什么？

A) None of these answers.
B) The Policy is a table that assigns a value to each action.
C) The Policy is a function that assigns a value to each action-state pair.
D) The Policy is a function that determines the probability of an agent taking an action. / 决定智能体采取某动作概率的函数。
E) All of these answers.

> **Answer**: D
> Policy $\pi(a|s)$ maps states to action probabilities. B/C describe value functions, not policy.
> 策略 $\pi(a|s)$ 将状态映射到动作概率。B/C 描述的是价值函数，不是策略。

---

**Question 9** (1 point)
What is a Value Function in Reinforcement Learning?
强化学习中的价值函数是什么？

A) A Value Function gives a measure of the expected total reward of an episode.
B) A Value Function gives a measure of the expected total reward given a state or state-action pair. / 给定状态或状态-动作对的期望总回报的度量。
C) None of these answers.
D) A Value Function gives a measure of the expected total number of steps to maximize reward.
E) All of these answers.

> **Answer**: B
> Value function estimates expected cumulative return from a given state $V(s)$ or state-action pair $Q(s,a)$. A is about the entire episode, not specific states; D confuses with step count.
> 价值函数估算从给定状态 $V(s)$ 或状态-动作对 $Q(s,a)$ 出发的期望累积回报。A 是整个 episode 的总回报；D 混淆了步数。

---

**Question 10** (1 point)
What is the difference between an action value function and a state value function?
动作价值函数和状态价值函数有什么区别？

A) None of these answers.
B) State value functions return total reward to termination, and action-value functions return immediate reward of taking the action.
C) State value functions take a state, and action value functions take just actions.
D) Action value functions return the average reward for taking an action, and State value functions return a state's average total future reward.
E) Action value functions take state-action pairs, whereas state value functions take just states. / 动作价值函数接受状态-动作对，状态价值函数只接受状态。

> **Answer**: E
> Core difference is the input: $V(s)$ takes states only; $Q(s,a)$ takes state-action pairs. Both output expected cumulative return. C says Q takes "just actions" — wrong, it needs state too.
> 核心区别在于输入：$V(s)$ 只接受状态，$Q(s,a)$ 接受状态-动作对。C 说 Q 只接受动作——错，还需要状态。

---

**Question 11** (1 point)
Which of the following statements is true about the Bellman equation in Reinforcement Learning?
以下关于贝尔曼方程的哪些说法是正确的？

A) None of these answers.
B) It expresses the relationship between the value of a state or a state-action pair, and the value of the successor states.
C) All of these answers. / 以上全部正确。
D) It breaks the problem of determining the value of a state into smaller problems recursively.
E) It forms the mathematical basis for the Q-Learning algorithm in Reinforcement Learning.

> **Answer**: C
> B/D/E all correctly describe different aspects of the Bellman equation: B — relates current and successor values; D — recursive decomposition; E — mathematical basis of Q-Learning.
> B/D/E 分别正确描述了贝尔曼方程的不同方面：B — 当前值与后继值的关系；D — 递归分解；E — Q-Learning 的数学基础。

---

**Question 12** (1 point)
What does "greedy" mean in the context of Reinforcement Learning?
强化学习中"贪婪"是什么意思？

A) None of these answers.
B) It implies a policy that tries to maximize total reward.
C) It implies a policy where future reward is considered over immediate reward.
D) It implies a policy where immediate reward is considered over future reward. / 优先考虑即时奖励而非未来奖励的策略。
E) It implies a policy that tries to maximize future reward.

> **Answer**: D
> Greedy = always pick $\arg\max Q$, prioritizing immediate gain. B describes the optimal policy goal, not greedy specifically. C/E say future over immediate — that's the opposite.
> 贪婪 = 总是选 $\arg\max Q$，优先即时利益。B 是最优策略的目标；C/E 恰好说反了。

---

**Question 13** (1 point)
What is a condition for applying Q-learning to a Reinforcement Learning problem?
将 Q-learning 应用于强化学习问题的条件是什么？

A) None of these answers.
B) The complete set of possible states must be known.
C) The complete set of actions must be known.
D) The complete set of actions and the complete set of possible states must be known. / 必须知道完整的动作集合和状态集合。
E) The optimal value function must be known.

> **Answer**: D
> Tabular Q-learning requires known, finite state set $S$ and action set $A$ to build the Q-table ($|S| \times |A|$). B/C each miss one requirement; E — if optimal value is known, no learning needed.
> 表格式 Q-learning 需要已知有限的状态集 $S$ 和动作集 $A$ 来构建 Q 表。B/C 各缺一个；E — 若最优值已知则无需学习。

---

**Question 14** (1 point)
Which of the following statements is true in the context of Reinforcement Learning?
以下哪个说法在强化学习的语境下是正确的？

A) All of these answers.
B) Q-learning is a form of Temporal Distance (TD) learning.
C) Temporal Distance (TD) learning involves learning from differences in time steps as opposed to complete episodes.
D) Temporal Distance (TD) learning does not require that the agent have a model of the environment.
E) None of these answers.

> **Answer**: E
> ⚠️ **Terminology trap**: all options use "Temporal **Distance**" — the correct term is "Temporal **Difference**" (TD). B/C/D concepts would be valid for TD, but wrong terminology makes them all invalid.
> ⚠️ **术语陷阱**：所有选项用了"Temporal Distance"——正确术语是"Temporal **Difference**"(TD)。B/C/D 描述的概念对 TD 成立，但术语错误导致全部无效。

---

**Question 15** (1 point)
Which of the following statements is true in the context of Reinforcement Learning?
以下哪个说法在强化学习的语境下是正确的？

A) The value function and policy function are implemented in the agent rather than the environment. / 价值函数和策略函数在智能体中实现，而非环境中。
B) The results of an action are determined by the agent rather than the environment.
C) The value function is implemented in the environment rather than the agent.
D) The policy function is implemented in the environment rather than the agent.
E) None of these answers.

> **Answer**: A
> Agent owns policy $\pi$ and value functions $V/Q$; Environment owns transitions $P(s'|s,a)$ and rewards $R$. B/C/D all misplace responsibilities.
> Agent 拥有策略 $\pi$ 和价值函数 $V/Q$；Environment 拥有转移 $P(s'|s,a)$ 和奖励 $R$。B/C/D 都放错了位置。
