# Week 2: MDP — 测验题笔记

> **Source:** Quiz 2 (15 questions)
> **See also:** [\_cheatsheet.md](week2_mdp_cheatsheet.md) | [\_math.md](week2_mdp_math.md) | [\_code.md](week2_mdp_code.md)

---

## 选择题 (Multiple Choice)

**Q1.** What is Reinforcement Learning (RL)?

A) All of these answers.
B) RL is a third type of machine learning, along with supervised learning and unsupervised learning.
C) RL is a form of supervised machine learning used for learning to play games.
D) RL is a form of unsupervised machine learning used in control applications.
E) None of these answers.

> **Answer:** B
> **Explanation (Why):**
> RL 是一种**独立**的机器学习范式，通过智能体与环境的"试错"（trial-and-error）交互来学习最优策略，它的目标是最大化累积奖励。它区别于监督学习（没有标记数据）和无监督学习（不仅仅是寻找隐藏结构）。因此，B 是准确的。C（监督学习的子类）和 D（无监督学习的子类）都是概念性错误。

---

**Q2.** Which of the following can be considered primary aspects of a Reinforcement Learning problem setup?

A) Values, Step function, and Actions.
B) Agent, Environment, and Reward.
C) Reward, Environment, and States.
D) Agent, Values, and Step function.
E) None of these answers.

> **Answer:** B
> **Explanation (Why):**
> 任何强化学习问题最底层的核心设定三要素是：**智能体 (Agent)**、**环境 (Environment)** 和 **奖励 (Reward)** 信号。
> ⚠️ **陷阱 (Trap):** C 选项看起来很有迷惑性，因为它提到了 State，但它缺少了最核心的 Agent。在 RL 框架中，State 是 Environment 提供给 Agent 的属性，而 Agent、Environment、Reward 才是定义框架的三个绝对核心组件。Values 是衍生出来的估计量，不是 setup 的一级要素。

---

**Q3.** What is a Markov state?

A) None of these answers.
B) All of these answers.
C) Markov states are states that form a single deterministic chain.
D) Intuitively, a Markov state has the property that all its previous states completely determine its future states.
E) Intuitively, a Markov state has the property that its subsequent states do not depend on its previous states.

> **Answer:** E
> **Explanation (Why):**
> 马尔可夫性质（Markov Property）的定义是："未来只取决于现在，而与过去无关"。即当前状态包含了预测未来所需要的所有历史信息。
> ⚠️ **陷阱 (Trap):** D 选项说"所有先前状态完全决定未来"，恰恰说反了！马尔可夫性的核心就是**不需要**历史（所有先前状态），只需要当前状态。C 选项错在 "deterministic chain"，马尔可夫链通常是随机的（stochastic）转移，不需要是确定性的。

---

**Q4.** What is the relationship between Reinforcement Learning (RL) and Markov Decision Processes (MDPs)?

A) MDPs are a mathematical model of the sequential decision making processes addressed by RL.
B) None of these answers.
C) MDPs are a component of the software used to implement video games.
D) MDPs are known specific strategies developed for playing games like chess, go, and video games played by RL systems.
E) All of these answers.

> **Answer:** A
> **Explanation (Why):**
> MDP 提供了强化学习中**序列决策问题（sequential decision making）**的标准数学形式化框架。RL 算法（如 Q-Learning、SARSA 等）都是在这个数学模型上去求解最优策略的。
> MDP 是模型，不是软件组件（C 错），也不是具体策略（D 错）。

---

**Q5.** What is the Reward Hypothesis of Reinforcement Learning?

A) The Reward Hypothesis basically states that some goals cannot be thought of as maximizing the expected cumulative value of a scalar reward function.
B) The Reward Hypothesis basically states that all goals can be thought of as minimizing the the number of steps to maximize a scalar reward function.
C) The Reward Hypothesis basically states that some goals cannot be thought of as minimizing the the number of steps to maximize a scalar reward function.
D) None of these answers.
E) The Reward Hypothesis basically states that all goals can be thought of as maximizing the expected cumulative value of a scalar reward function.

> **Answer:** E
> **Explanation (Why):**
> 奖励假设（Reward Hypothesis）指出："我们意图实现的**所有目标（all goals）**，都可以形式化为**最大化（maximizing）**一个标量奖励信号的**预期累积值（expected cumulative value）**"。
> ⚠️ **陷阱 (Trap):**
>
> - A 错在说 "some goals cannot"，与基本前提冲突。
> - B 错在说 "minimizing the number of steps"，奖励假设是关于最大化回报，并不要求一定是最小化步数（除非每步给负奖励）。

---

**Q6.** What is meant by "episode" in Reinforcement Learning?

A) An episode is a single cycle of performing an action, receiving a reward, and observing the resulting state.
B) An episode is a single run from the starting state to a terminal (or truncated) state.
C) An episode is a single run that does not reach the terminal state.
D) An episode is the number of steps actually taken to reach the terminal state.
E) None of these answers.

> **Answer:** B
> **Explanation (Why):**
> 回合（Episode）是指智能体与环境交互的**一次完整运行序列**，从起始状态开始，直到到达某个终止状态（终端或截断）为止（例如：一局棋的开始到结束，一次迷宫寻宝的开始到找到宝藏/踩到陷阱）。
> ⚠️ **陷阱 (Trap):** A 描述的是一个**时间步 (time step)** 的循环，不是整个回合。D 描述的是该序列的**长度 (步数)**，而不是序列本身。

---

**Q7.** What role does the discount factor $\gamma$ play in Reinforcement Learning?

A) $\gamma$ addresses the problem of infinite cumulative rewards in non-terminating processes.
B) $\gamma$ determines how many times an action is chosen randomly during training.
C) $\gamma$ represents the total discount which is subtracted from the reward function cumulative total.
D) None of these answers.
E) $\gamma$ represents the weighting of the current goal of a Reinforcement Learning problem.

> **Answer:** A
> **Explanation (Why):**
> 折扣因子 $\gamma \in [0, 1)$ 的主要数学作用是防止持续任务（非终止任务）中的累积回报（return）发散到无穷大。通过几何级数衰减 $\gamma^k R_{t+k+1}$，使得未来奖励总和收敛到一个有限值。
> ⚠️ **陷阱 (Trap):**
>
> - B 描述的是探索率 $\epsilon$。
> - C 错在说 "subtracted (减法)"，$\gamma$ 是用于**乘法**权重衰减的，而不是减法。
> - E 是对目标的误解。

---

**Q8.** What is a Policy in Reinforcement Learning?

A) None of these answers.
B) The Policy is a table that assigns a value to each action.
C) The Policy is a function that assigns a value to each action-state pair.
D) The Policy is a function that determines the probability of an agent taking an action.
E) All of these answers.

> **Answer:** D
> **Explanation (Why):**
> 策略（Policy）$\pi(a|s)$ 定义了智能体在特定状态下的行为方式，它是给定状态下各个动作被采取的**概率分布**。
> ⚠️ **陷阱 (Trap):** B 和 C 描述的都是**价值函数 (Value Function)**（分别为状态-动作的 Q 值等），而不是策略。Policy 输出的是动作的概率，Value Function 输出的是预期的累积总回报数字。

---

**Q9.** What is a Value Function in Reinforcement Learning?

A) A Value Function gives a measure of the expected total reward of an episode.
B) A Value Function gives a measure of the expected total reward given a state or state-action pair.
C) None of these answers.
D) A Value Function gives a measure of the expected total number of steps to maximize reward.
E) All of these answers.

> **Answer:** B
> **Explanation (Why):**
> 价值函数（Value Function）衡量的是在一个**特定的状态** $s$ 之下，或者在**特定的状态-动作对** $(s,a)$ 之下，未来能够预期获得的**总回报（ expected total reward / cumulative return）**。它评估"在这个状态有多好"或"做出这个动作有多好"。
> ⚠️ **陷阱 (Trap):** A 的描述过于泛化，没有说明这是针对某个确切的状态点；D 错在评估的是"步数 (number of steps)" 而是"奖励 (reward)"。

---

**Q10.** What is the difference between an action value function and a state value function?

A) None of these answers.
B) State value functions return total reward to termination, and action-value functions return immediate reward of taking the action.
C) State value functions take a state, and action value functions take just actions.
D) Action value functions return the average reward for taking an action, and State value functions return a state's average total future reward.
E) Action value functions take state-action pairs, whereas state value functions take just states.

> **Answer:** E
> **Explanation (Why):**
> 最根本的区别在于它们的输入。状态价值函数 $V(s)$ 只接收**状态**作为参数；而动作价值函数 $Q(s, a)$ 接收**状态-动作对**作为参数。
> ⚠️ **陷阱 (Trap):** B 错在说 Q 函数只返回"即时奖励 (immediate reward)"，其实 Q 函数返回的也是长期的预期总回报。C 错在说 action value 函数"只接受动作"，其实它是接收 (state, action) 两者。

---

**Q11.** Which of the following statements is true about the Bellman equation in Reinforcement Learning?

A) None of these answers.
B) It expresses the relationship between the value of a state or a state-action pair, and the value of the successor states.
C) All of these answers.
D) It breaks the problem of determining the value of a state into smaller problems recursively.
E) It forms the mathematical basis for the Q-Learning algorithm in Reinforcement Learning.

> **Answer:** C
> **Explanation (Why):**
> B、D、E 选项都是完全正确的。
>
> - B 正确：贝尔曼方程本质就是定义了当前状态价值与后续状态价值的关系。
> - D 正确：它通过动态规划思想，将未来的无穷级数截断为即时奖励和下一步的价值（递归拆解 $V(s) = R + \gamma V(s')$）。
> - E 正确：由于它定义了最优性的条件（Bellman Optimality Equation），这构成了 Q-Learning 更新的核心规则的数学基石。

---

**Q12.** What does "greedy" mean in the context of Reinforcement Learning?

A) None of these answers.
B) It implies a policy that tries to maximize total reward.
C) It implies a policy where future reward is considered over immediate reward.
D) It implies a policy where immediate reward is considered over future reward.
E) It implies a policy that tries to maximize future reward.

> **Answer:** D
> **Explanation (Why):**
> "贪婪" (Greedy) 选择意味着智能体基于**当前的估计**（通常利用即时最优的信息）来选择它认为最好的动作 ($a = \arg\max Q(s,a)$)，而忽略了为了长远的更好收益而去探索风险较高或当前看起来不那么具有吸引力的选项。换句话说，贪心选择更看重当前的已知利益（immediate reward over future unverified potential）。
> ⚠️ **陷阱 (Trap):** B 描述的是最优策略（Optimal Policy）的终极目标。最优策略往往不总是能用单纯的 greedy 去发现，因为它可能需要长期规划。

---

**Q13.** What is a condition for applying Q-learning to a Reinforcement Learning problem?

A) None of these answers.
B) The complete set of possible states must be known.
C) The complete set of actions must be known.
D) The complete set of actions and the complete set of possible states must be known.
E) The optimal value function must be known.

> **Answer:** D
> **Explanation (Why):**
> 标准的表格法（Tabular）Q-Learning 需要构建一个二维表——**Q-table**。这个表的行是所有可能的状态，列是所有可能的动作。因此，必须已知**完整的状态集 (S) 和完整的动作集 (A)**，且这两者都是离散和有限的，才能构建 Q-table。
> ⚠️ **陷阱 (Trap):** E 选项是错的，因为如果已经知道了"最优价值函数"，RL 的目标就已经达成了，就不需要去学习 (Q-learning) 它了。

---

**Q14.** Which of the following statements is true in the context of Reinforcement Learning?

A) All of these answers.
B) Q-learning is a form of Temporal Distance (TD) learning.
C) Temporal Distance (TD) learning involves learning from differences in time steps as opposed to complete episodes.
D) Temporal Distance (TD) learning does not require that the agent have a model of the environment.
E) None of these answers.

> **Answer:** E
> **Explanation (Why):**
> ⚠️ **极具迷惑性的术语陷阱题！**
> 所有的选项 (B, C, D) 都在描述一个正确的概念，但它们故意使用了一个**根本不存在的术语**："Temporal **Distance**"。
> 强化学习中的 TD 学习英文缩写展开是 **Temporal Difference (时序差分)**，而不是 Temporal Distance。因为术语完全错误，所以包含这个术语的选项全都不能选。正确答案只能是 E (None)。
> （TD 确实能够从时间步差中学习，而且不需要环境模型，Q-Learning 确实是 TD 的一种形式——如果把 Distance 替换成 Difference，选 All）。

---

**Q15.** Which of the following statements is true in the context of Reinforcement Learning?

A) The value function and policy function are implemented in the agent rather than the environment.
B) The results of an action are determined by the agent rather than the environment.
C) The value function is implemented in the environment rather than the agent.
D) The policy function is implemented in the environment rather than the agent.
E) None of these answers.

> **Answer:** A
> **Explanation (Why):**
> 在强化学习模型中（Sutton 教材明确规定了边界）：
>
> - **Agent (智能体)**的内部掌管着："怎么做决策"（策略 Policy）以及 "对状态好坏的评估"（价值函数 Value）。
> - **Environment (环境)**的内部掌管着：接收动作并输出"动作的结果"，即状态流转的概率（Transition dynamics）和发放的奖励（Reward）。
>   ⚠️ **陷阱 (Trap):** B 错在动作的结果肯定是外部环境反馈决定的，不是智能体单方面决定的。C 和 D 错在把评估与决策功能塞给了环境。

---
