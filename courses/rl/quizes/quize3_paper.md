# Reinforcement Learning Quiz 3 (In-Class Paper)

> Source: CST8509 Winter 2026 – Quiz 3 – 3% – Todd Kelley
> 10 MC Questions, 1 Minute Per Question

---

**Question 1** (1 point)
What is a Markov state?
什么是马尔可夫状态？

A) A process of present states that can only be determined from states and actions that have occurred in the past.
B) None of these answers.
C) The process of present states that determine future Learning actions.
D) All of these answers.
E) Intuitively, it implies that all we need to predict future states is the current state, and all previous states can be thrown away. / 预测未来只需当前状态，所有历史状态可以丢弃。

> **Answer**: E
> Markov property: the future depends only on the current state, not on the history of past states.
> 马尔可夫性：未来只取决于当前状态，与历史无关。

---

**Question 2** (1 point)
What are all the actions in Reinforcement Learning?
强化学习中的动作是什么？

A) All of these answers.
B) It implies taking actions to maximize total reward.
C) It implies taking actions to maximize past cumulative reward.
D) None of these answers.
E) It implies taking actions to maximize future cumulative reward. / 采取动作以最大化未来累积奖励。

> **Answer**: E
> In RL, actions aim to maximize expected future cumulative reward, not past or just total reward.
> RL 中，动作的目标是最大化未来累积奖励的期望。

---

**Question 3** (1 point)
What is meant by "episode" in Reinforcement Learning?
"回合(Episode)"是什么意思？

A) An episode is the number of steps actually taken to reach the terminal state.
B) An episode is a single cycle of performing an action, receiving a reward, and observing the resulting state.
C) An episode is a single run from the starting state to a terminal (or truncated) state. / 从起始状态到终止状态的一次完整运行。
D) None of these answers.
E) An episode is a single run that does not reach the terminal state.

> **Answer**: C
> Episode = complete trajectory from start to terminal. B describes a single time step, not a full episode.
> 回合 = 从起始到终止的完整轨迹。B 描述的是单个时间步。

---

**Question 4** (1 point)
What is Reinforcement Learning (RL)?
什么是强化学习？

A) RL is the application of neural network machine learning for robotics.
B) RL is the application of supervised machine learning for control applications.
C) None of these answers.
D) RL is a third type of machine learning, along with supervised learning and unsupervised learning. / RL 是与监督学习、无监督学习并列的第三种机器学习。
E) RL is a form of unsupervised learning where an agent takes actions on an environment.

> **Answer**: D
> RL is the third ML paradigm alongside supervised and unsupervised learning — it learns through agent-environment interaction.
> RL 是机器学习三大范式之一，通过智能体与环境交互来学习。

---

**Question 5** (1 point)
What is the difference between an action value function and a state value function?
动作价值函数和状态价值函数有什么区别？

A) None of these answers.
B) State value functions return a state, and action value functions return immediate reward of taking the action.
C) State value functions take a state and an action, and action value functions take just actions.
D) Action value functions return the average reward for taking an action, and State value functions return a state's average total future reward.
E) Action value functions take a state and an action, and State value functions are about the value of being in a state. / 动作价值函数接受状态和动作，状态价值函数衡量处于某状态的价值。

> **Answer**: E
> $Q(s,a)$: takes state + action → expected return. $V(s)$: takes state only → expected return from that state.
> $Q(s,a)$：状态+动作 → 期望回报。$V(s)$：仅状态 → 该状态的期望回报。

---

**Question 6** (1 point)
What is the Reward Hypothesis of Reinforcement Learning?
奖励假设是什么？

A) All of these answers.
B) It implies that some goals and purposes can be thought of as maximizing the expected value of cumulative scalar reward.
C) None of these answers.
D) It implies that all RL problems are based on reward.
E) It implies that all goals and purposes can be thought of as maximizing the expected value of cumulative scalar reward. / 所有目标都可以表述为最大化累积标量奖励的期望值。

> **Answer**: E
> Reward Hypothesis: ALL goals = maximizing expected cumulative scalar reward. B says "some" — must be "all".
> 奖励假设：所有（不是"某些"）目标 = 最大化累积标量奖励期望。

---

**Question 7** (1 point)
What is RL with respect to supervised and unsupervised learning?
RL 相对于监督学习和无监督学习是什么？

A) RL can be applied but only when supervised learning has been done first.
B) All of these answers.
C) RL is a third type of machine learning. / RL 是第三种机器学习。
D) None of these answers.
E) RL is a variation of unsupervised learning that uses past results.

> **Answer**: C
> RL is a distinct, third paradigm of ML — not a subset of supervised or unsupervised learning.
> RL 是独立的第三种 ML 范式，不是监督或无监督的子集。

---

**Question 8** (1 point)
What is a Policy in Reinforcement Learning?
策略(Policy)是什么？

A) The Policy is a function that assigns a value to each action.
B) The Policy is a function that determines the probability of an agent taking an action. / 决定智能体采取某动作概率的函数。
C) The Policy is a function that assigns a value to each action-state pair.
D) All of these answers.
E) None of these answers.

> **Answer**: B
> Policy $\pi(a|s)$: maps states to action probabilities. A/C describe value functions, not policy.
> 策略 $\pi(a|s)$：状态 → 动作概率。A/C 描述的是价值函数。

---

**Question 9** (1 point)
Which of the following statements is true in the context of Reinforcement Learning?
以下哪个说法是正确的？

A) The policy function is implemented in the environment rather than the agent.
B) None of these answers.
C) The value function is implemented in the environment rather than the agent.
D) The value function and policy function are implemented in the agent rather than the environment. / 价值函数和策略函数在智能体中实现。
E) All of these answers.

> **Answer**: D
> Agent owns: policy $\pi$ + value functions $V/Q$. Environment owns: transitions $P$ + rewards $R$.
> Agent 拥有策略和价值函数。Environment 拥有转移和奖励。

---

**Question 10** (1 point)
What is a Value Function in Reinforcement Learning?
价值函数是什么？

A) A Value Function determines an action and gives a measure of the expected total number of steps to maximize reward.
B) None of these answers.
C) A Value Function takes an action and an episode and gives a measure of the expected immediate reward.
D) All of these answers.
E) A Value Function takes an action and gives a measure of the expected total reward.

> **Answer**: B
> None of the options correctly describe a value function. A value function estimates expected cumulative return from a state $V(s)$ or state-action pair $Q(s,a)$.
> 没有选项正确描述价值函数。价值函数估算从状态 $V(s)$ 或状态-动作对 $Q(s,a)$ 出发的期望累积回报。
