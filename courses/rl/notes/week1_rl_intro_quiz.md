# Reinforcement Learning Quiz 2
> Source: `quizes/quize2.md` | Week 1 — RL Intro

Question 1 (1 point)
What is Reinforcement Learning (RL)?

Question 1 options:
A) All of these answers.
B) RL is a third type of machine learning, along with supervised learning and unsupervised learning.
C) RL is a form of supervised machine learning used for learning to play games.
D) RL is a form of unsupervised machine learning used in control applications.
E) None of these answers.

> **Answer**: B
> **Explanation**:
> RL 是机器学习三大范式之一（监督/无监督/强化），通过智能体与环境的试错交互学习最优策略；**为什么是 B**：只有 B 正确定位了 RL 与其他两种范式的并列关系。C/D 错误地将 RL 归为监督或无监督的子类；A/E 因此不成立。
> **Key**: RL is the third ML paradigm alongside supervised and unsupervised learning.

Question 2 (1 point)
Which of the following can be considered primary aspects of a Reinforcement Learning problem setup?

Question 2 options:
A) Values, Step function, and Actions.
B) Agent, Environment, and Reward.
C) Reward, Environment, and States.
D) Agent, Values, and Step function.
E) None of these answers.

> **Answer**: B
> **Explanation**:
> RL 框架的核心三要素是 Agent（智能体）、Environment（环境）和 Reward（奖励）；**为什么是 B**：只有 B 同时包含这三个标准要素。
>   - **C 错**：看似合理但缺少 Agent——States 是环境的属性，不是独立的核心设定要素。
>   - A/D 包含 Values 和 Step function，这些是派生概念而非核心设定；E 不成立。
> **Key**: Primary RL setup: Agent, Environment, Reward.

Question 3 (1 point)
What is a Markov state?

Question 3 options:
A) None of these answers.
B) All of these answers.
C) Markov states are states that form a single deterministic chain.
D) Intuitively, a Markov state has the property that all its previous states completely determine its future states.
E) Intuitively, a Markov state has the property that its subsequent states do not depend on its previous states.

> **Answer**: E
> **Explanation**:
> 马尔可夫性质："未来只取决于当前状态，与历史无关"；**为什么是 E**：E 说"后续状态不依赖于先前状态"，正是马尔可夫性的直观表述。
>   - **D 错**：说"所有先前状态完全决定未来"——恰好相反，马尔可夫性强调只需当前状态，不需要历史。
>   - **C 错**：马尔可夫状态不要求形成"单一确定性链"，转移可以是概率性的。
>   - B 不成立（C/D 不正确）；A 不成立（E 正确）。
> **Key**: Markov property — future depends only on current state, not history.

Question 4 (1 point)
What is the relationship between Reinforcement Learning (RL) and Markov Decision Processes (MDPs)?

Question 4 options:
A) MDPs are a mathematical model of the sequential decision making processes addressed by RL.
B) None of these answers.
C) MDPs are a component of the software used to implement video games.
D) MDPs are known specific strategies developed for playing games like chess, go, and video games played by RL systems.
E) All of these answers.

> **Answer**: A
> **Explanation**:
> MDP 是 RL 用于描述序贯决策问题的标准数学框架；**为什么是 A**：A 准确描述了 MDP 与 RL 的关系。C/D 分别将 MDP 误解为软件组件和具体博弈策略，与 MDP 作为通用数学模型的定位不符；B/E 因此不成立。
> **Key**: MDP provides the formal mathematical framework for RL's sequential decision problems.

Question 5 (1 point)
What is the Reward Hypothesis of Reinforcement Learning?

Question 5 options:
A) The Reward Hypothesis basically states that some goals cannot be thought of as maximizing the expected cumulative value of a scalar reward function.
B) The Reward Hypothesis basically states that all goals can be thought of as minimizing the the number of steps to maximize a scalar reward function.
C) The Reward Hypothesis basically states that some goals cannot be thought of as minimizing the the number of steps to maximize a scalar reward function.
D) None of these answers.
E) The Reward Hypothesis basically states that all goals can be thought of as maximizing the expected cumulative value of a scalar reward function.

> **Answer**: E
> **Explanation**:
> 奖励假设："所有目标都可以表述为最大化标量奖励的累积期望值"；**为什么是 E**：E 准确包含了关键要素——"all goals + maximizing + expected cumulative + scalar reward"。
>   - **A 错**：说"some goals cannot"，与假设的"all goals can"直接矛盾。
>   - **B 错**：说"minimizing steps"，奖励假设关注最大化累积奖励，不是最小化步数。
>   - **C 错**：同时包含"some"和"minimizing"两个错误。
>   - D 不成立。
> **Key**: Reward Hypothesis — all goals = maximizing expected cumulative scalar reward.

Question 6 (1 point)
What is meant by "episode" in Reinforcement Learning?

Question 6 options:
A) An episode is a single cycle of performing an action, receiving a reward, and observing the resulting state.
B) An episode is a single run from the starting state to a terminal (or truncated) state.
C) An episode is a single run that does not reach the terminal state.
D) An episode is the number of steps actually taken to reach the terminal state.
E) None of these answers.

> **Answer**: B
> **Explanation**:
> 回合（Episode）是从初始状态到终止状态的一次完整交互序列；**为什么是 B**：B 准确描述了"从起始到终止/截断的单次运行"。
>   - **A 错**：描述的是单个 time step（一次动作-奖励-观察循环），不是一整个回合。
>   - C 说"没有到达终止状态"，与 Episode 定义矛盾；D 描述的是步数，不是 Episode 本身；E 不成立。
> **Key**: Episode — a complete run from start state to terminal/truncated state.

Question 7 (1 point)
What role does the discount factor $\gamma$ play in Reinforcement Learning?

Question 7 options:
A) $\gamma$ addresses the problem of infinite cumulative rewards in non-terminating processes.
B) $\gamma$ determines how many times an action is chosen randomly during training.
C) $\gamma$ represents the total discount which is subtracted from the reward function cumulative total.
D) None of these answers.
E) $\gamma$ represents the weighting of the current goal of a Reinforcement Learning problem.

> **Answer**: A
> **Explanation**:
> 折扣因子 $\gamma \in [0, 1)$ 通过降低未来奖励权重使无限步回报收敛；**为什么是 A**：A 准确指出 $\gamma$ 解决的是"非终止过程中累积奖励可能无穷"的问题。
>   - **B 错**：随机选动作由探索策略（如 $\epsilon$-greedy）控制，不是 $\gamma$。
>   - **C 错**：$\gamma$ 是乘法衰减因子 ($\gamma^k$)，不是从总和中减去的"折扣总额"。
>   - **E 错**：$\gamma$ 控制未来奖励的衰减权重，不是"当前目标的权重"。
>   - D 不成立。
>   - **$\gamma$**: 折扣因子 (Discount factor)，$0 \le \gamma < 1$
>   - **$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$**: 折扣回报公式
> **Key**: $\gamma \in [0,1)$ ensures infinite-horizon returns converge via geometric discounting.

Question 8 (1 point)
What is a Policy in Reinforcement Learning?

Question 8 options:
A) None of these answers.
B) The Policy is a table that assigns a value to each action.
C) The Policy is a function that assigns a value to each action-state pair.
D) The Policy is a function that determines the probability of an agent taking an action.
E) All of these answers.

> **Answer**: D
> **Explanation**:
> 策略 $\pi(a|s)$ 是"给定状态，决定采取各动作概率"的映射；**为什么是 D**：D 说"确定智能体采取某动作的概率"，与 $\pi(a|s)$ 定义一致。
>   - **B 错**：为动作赋值的是价值函数，不是策略。
>   - **C 错**：为状态-动作对赋值是 $Q(s,a)$（动作价值函数），不是策略。
>   - A/E 因此不成立。
>   - **$\pi(a|s)$**: 在状态 $s$ 下采取动作 $a$ 的条件概率
> **Key**: Policy $\pi(a|s)$ — maps states to action probabilities. Not a value function.

Question 9 (1 point)
What is a Value Function in Reinforcement Learning?

Question 9 options:
A) A Value Function gives a measure of the expected total reward of an episode.
B) A Value Function gives a measure of the expected total reward given a state or state-action pair.
C) None of these answers.
D) A Value Function gives a measure of the expected total number of steps to maximize reward.
E) All of these answers.

> **Answer**: B
> **Explanation**:
> 价值函数估算从给定状态或状态-动作对出发的期望累积回报；**为什么是 B**：B 涵盖了 $V(s)$（给定状态）和 $Q(s,a)$（给定状态-动作对）两种形式。
>   - **A 错**：价值函数针对特定状态/状态-动作对，不是整个 episode 的总回报。
>   - **D 错**：衡量的是期望总回报，不是"最大化回报所需的步数"。
>   - C/E 因此不成立。
>   - **$V(s)$**: 状态价值函数 | **$Q(s,a)$**: 动作价值函数
> **Key**: Value function = expected cumulative return from a state ($V$) or state-action pair ($Q$).

Question 10 (1 point)
What is the difference between an action value function and a state value function?

Question 10 options:
A) None of these answers.
B) State value functions return total reward to termination, and action-value functions return immediate reward of taking the action.
C) State value functions take a state, and action value functions take just actions.
D) Action value functions return the average reward for taking an action, and State value functions return a state's average total future reward.
E) Action value functions take state-action pairs, whereas state value functions take just states.

> **Answer**: E
> **Explanation**:
> 核心区别在于输入：$V(s)$ 只接受状态，$Q(s,a)$ 接受状态-动作对；**为什么是 E**：E 准确描述了两者的输入差异。
>   - **B 错**：$V(s)$ 返回期望累积回报（非"到终止的总回报"），$Q(s,a)$ 也非"即时奖励"。
>   - **C 错**：$Q(s,a)$ 的输入是状态-动作对，不是"只有动作"。
>   - **D 错**："平均回报"不准确，$V$ 和 $Q$ 都是期望值。
>   - A 不成立。
>   - **$V(s)$**: 状态 → 期望回报 | **$Q(s,a)$**: 状态-动作对 → 期望回报
> **Key**: $V(s)$ takes states; $Q(s,a)$ takes state-action pairs. Both output expected cumulative return.

Question 11 (1 point)
Which of the following statements is true about the Bellman equation in Reinforcement Learning?

Question 11 options:
A) None of these answers.
B) It expresses the relationship between the value of a state or a state-action pair, and the value of the successor states.
C) All of these answers.
D) It breaks the problem of determining the value of a state into smaller problems recursively.
E) It forms the mathematical basis for the Q-Learning algorithm in Reinforcement Learning.

> **Answer**: C (All)
> **Explanation**:
> 贝尔曼方程将价值递归分解：当前价值 = 即时奖励 + 折扣后继价值；**为什么是 C (All)**：B/D/E 都正确描述了贝尔曼方程的不同方面。
>   - **B ✓**：确实表达了当前值与后继值的关系。
>   - **D ✓**：确实将价值计算递归拆解为子问题。
>   - **E ✓**：Q-Learning 更新规则直接源自贝尔曼最优性方程。
>   - A 不成立（B/D/E 都正确）。
>   - **$V(s) = \mathbb{E}[R + \gamma V(s')]$**: 贝尔曼方程
> **Key**: Bellman equation: value = reward + discounted successor value. Recursive, foundational to Q-Learning.

Question 12 (1 point)
What does "greedy" mean in the context of Reinforcement Learning?

Question 12 options:
A) None of these answers.
B) It implies a policy that tries to maximize total reward.
C) It implies a policy where future reward is considered over immediate reward.
D) It implies a policy where immediate reward is considered over future reward.
E) It implies a policy that tries to maximize future reward.

> **Answer**: D
> **Explanation**:
> 贪婪策略指总是选当前估计值最高的动作，即优先即时利益；**为什么是 D**：D 说"即时奖励优先于未来奖励"，正是贪婪定义。
>   - **B 错**："最大化总回报"是最优策略的目标，不是贪婪的特征——贪婪只看当前最优，可能牺牲长期回报。
>   - **C 错**：与贪婪定义相反——贪婪恰恰不考虑未来。
>   - **E 错**："最大化未来奖励"同样不是贪婪。
>   - A 不成立。
>   - **$a = \arg\max_{a'} Q(s, a')$**: 贪婪选择公式
> **Key**: Greedy — always pick $\arg\max Q$, prioritizing immediate over future reward.

Question 13 (1 point)
What is a condition for applying Q-learning to a Reinforcement Learning problem?

Question 13 options:
A) None of these answers.
B) The complete set of possible states must be known.
C) The complete set of actions must be known.
D) The complete set of actions and the complete set of possible states must be known.
E) The optimal value function must be known.

> **Answer**: D
> **Explanation**:
> 表格式 Q-learning 需要有限且已知的状态集 $S$ 和动作集 $A$ 来构建 Q 表；**为什么是 D**：D 同时要求完整的状态集合和动作集合，缺一不可。
>   - **B 错**：只提到状态集合，缺少动作集合要求。
>   - **C 错**：只提到动作集合，缺少状态集合要求。
>   - **E 错**：Q-learning 的目的是学习最优价值函数，如果已知就无需学习了。
>   - A 不成立。
>   - **$Q$-table**: $|S| \times |A|$ 维度，存储每个状态-动作对的价值
> **Key**: Tabular Q-learning requires known, finite state set $S$ and action set $A$ for the Q-table.

Question 14 (1 point)
Which of the following statements is true in the context of Reinforcement Learning?

Question 14 options:
A) All of these answers.
B) Q-learning is a form of Temporal Distance (TD) learning.
C) Temporal Distance (TD) learning involves learning from differences in time steps as opposed to complete episodes.
D) Temporal Distance (TD) learning does not require that the agent have a model of the environment.
E) None of these answers.

> **Answer**: E
> **Explanation**:
> ⚠️ **术语陷阱**：所有选项使用了错误术语 "Temporal Distance"，正确术语是 **Temporal Difference (TD)**（时序差分）。
> **为什么是 E (None)**：B/C/D 的概念描述对 TD 而言部分成立，但术语错误（Distance ≠ Difference）导致全部无效。
>   - **B 错**：术语错误。若改为 TD，Q-learning 确实是 TD 的一种。
>   - **C 错**：术语错误。若改为 TD，TD 确实逐步更新而非等完整 episode。
>   - **D 错**：术语错误。若改为 TD，TD 确实是 model-free。
>   - A 因此不成立。
>   - **TD (Temporal Difference)**: 利用相邻时间步估计值差异进行学习
> **Key**: Correct term is **Temporal Difference** (not Distance). TD is model-free, step-by-step learning.

Question 15 (1 point)
Which of the following statements is true in the context of Reinforcement Learning?

Question 15 options:
A) The value function and policy function are implemented in the agent rather than the environment.
B) The results of an action are determined by the agent rather than the environment.
C) The value function is implemented in the environment rather than the agent.
D) The policy function is implemented in the environment rather than the agent.
E) None of these answers.

> **Answer**: A
> **Explanation**:
> 在 RL 框架中，策略和价值函数属于 Agent，状态转移和奖励由 Environment 负责；**为什么是 A**：A 正确描述了策略和价值函数都在 Agent 端。
>   - **B 错**：动作的结果（下一状态和奖励）由环境决定，不是智能体。
>   - **C 错**：价值函数在 Agent 中，不在 Environment。
>   - **D 错**：策略在 Agent 中，不在 Environment。
>   - E 不成立。
>   - **Agent**: $\pi$ (Policy) + $V/Q$ (Value function) | **Environment**: $P(s'|s,a)$ + $R$
> **Key**: Agent owns policy $\pi$ and value functions $V/Q$; Environment owns transitions $P$ and rewards $R$.
