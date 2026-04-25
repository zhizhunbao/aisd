# Reinforcement Learning Quiz 5 (In-Class Paper)

> Source: CST8509 Winter 2026 – Quiz 5 – 5% – Todd Kelley
> 10 MC Questions, 1 Minute Per Question

---

**Question 1** (1 point)
What is Policy Evaluation?
什么是策略评估(Policy Evaluation)？

A) Policy Evaluation is the process of progressively improving a policy.
B) Policy Evaluation uses the Bellman Equation to find the state value for the current policy. / 策略评估使用贝尔曼方程求当前策略的状态价值。
C) All of these answers.
D) Policy Evaluation is the same as Q-Learning.
E) None of these answers.

> **Answer**: B
> Policy Evaluation computes $V^\pi(s)$ for a given policy $\pi$ using the Bellman expectation equation iteratively.
> 策略评估通过贝尔曼期望方程迭代计算给定策略 $\pi$ 下的 $V^\pi(s)$。

---

**Question 2** (1 point)
Which of the following statements about Policy Iteration is true?
以下关于策略迭代(Policy Iteration)的哪个说法是正确的？

A) None of these answers.
B) Policy Iteration is important theoretically, even though it is not practical.
C) Policy Iteration is important practically, but does not require a model of the environment.
D) Policy Iteration is important practically, even though it requires a model of the environment. / 策略迭代实际很重要，尽管需要环境模型。
E) All of these answers.

> **Answer**: D
> Policy Iteration is practical and effective but requires a complete model (transition probabilities and rewards) — it is a model-based method.
> 策略迭代实用且有效，但需要完整的环境模型——属于 model-based 方法。

---

**Question 3** (1 point)
What is Policy Improvement in Dynamic Programming?
动态规划中的策略改进是什么？

A) None of these answers.
B) Policy Improvement computes a better policy based on the current value function. / 策略改进基于当前价值函数计算更好的策略。
C) All of these answers.
D) Policy Improvement
E) Policy Improvement tries the current policy to compute a better policy.

> **Answer**: B
> Policy Improvement: given $V^\pi(s)$, derive a better policy by acting greedily: $\pi'(s) = \arg\max_a Q^\pi(s,a)$.
> 策略改进：给定 $V^\pi(s)$，通过贪婪选择推导更好的策略。

---

**Question 4** (1 point)
What distinguishes Monte Carlo methods from Dynamic Programming?
蒙特卡洛方法与动态规划有什么区别？

A) All of these answers.
B) Monte Carlo methods are based on averaging sample returns. / 蒙特卡洛方法基于对样本回报取平均。
C) Monte Carlo methods make use of the results of completed episodes.
D) Monte Carlo methods do not rely on having a model of the environment.
E) None of these answers.

> **Answer**: B
> MC methods learn from complete episodes by averaging actual returns, without needing a model. Unlike DP, MC is model-free.
> MC 方法从完整回合中学习，对实际回报取平均，不需要模型。与 DP 不同，MC 是 model-free 的。

---

**Question 5** (1 point)
What is Policy Iteration in Dynamic Programming?
动态规划中的策略迭代是什么？

A) All of these answers.
B) Policy Iteration is an alternative algorithm to Policy Evaluation.
C) Policy Iteration is an algorithm that involves Policy Evaluation and Policy Improvement. / 策略迭代是包含策略评估和策略改进的算法。
D) None of these answers.
E) Policy Iteration is an alternative algorithm to Policy Improvement.

> **Answer**: C
> Policy Iteration alternates: Policy Evaluation (compute $V^\pi$) → Policy Improvement (get better $\pi'$) → repeat until convergence.
> 策略迭代交替执行：策略评估 → 策略改进 → 重复直到收敛。

---

**Question 6** (1 point)
Which of the following statements about Dynamic Programming is true?
以下关于动态规划的哪个说法是正确的？

A) It is a technique to explicitly provide state-action values to the agent.
B) All of these answers.
C) Dynamic Programming is not practical for very large state spaces, but it has important theoretical value. / DP 对很大的状态空间不实用，但有重要的理论价值。
D) None of these answers.
E) It is the process of predicting the state values for a policy.

> **Answer**: C
> DP is theoretically foundational but computationally infeasible for very large state spaces due to the curse of dimensionality.
> DP 是理论基础，但由于维度灾难，对非常大的状态空间在计算上不可行。

---

**Question 7** (1 point)
Which of the following statements is true in the context of RL?
以下哪个关于 RL 的说法是正确的？

A) All of these answers.
B) Temporal Difference methods are a technique that combines Monte Carlo and Dynamic Programming ideas. / TD 方法结合了蒙特卡洛和动态规划的思想。
C) None of these answers.
D) Monte Carlo methods update state estimates at every time step.
E) Temporal Difference methods require a complete model of the environment.

> **Answer**: B
> TD combines MC (learning from experience, model-free) and DP (bootstrapping — updating estimates from other estimates).
> TD 结合了 MC（从经验学习、model-free）和 DP（自举——用估计值更新估计值）。

---

**Question 8** (1 point)
What is Q-Learning?
什么是 Q-Learning？

A) All of these answers.
B) Q-Learning does not require a model of the environment. / Q-Learning 不需要环境模型。
C) None of these answers.
D) Q-Learning is an on-policy algorithm.
E) The Q-table is hand-crafted based on expert knowledge.

> **Answer**: B
> Q-Learning is model-free and off-policy. Update: $Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$.
> Q-Learning 是 model-free 且 off-policy 的。

---

**Question 9** (1 point)
What is Policy Evaluation?
什么是策略评估？

A) Value of Criticism helps to update the policy based on lighting of higher values.
B) Policy Evaluation computes how good it is to be in a state for a given policy. / 策略评估计算在给定策略下处于某状态有多好。
C) None of these answers.
D) Monte Carlo evaluation is based on complete episodes only and does not use bootstrapping.
E) All of these answers.

> **Answer**: B
> Policy Evaluation: compute $V^\pi(s)$ — how good each state is under the current policy $\pi$.
> 策略评估：计算 $V^\pi(s)$——在当前策略 $\pi$ 下每个状态的好坏程度。

---

**Question 10** (1 point)
What is Value Iteration?
什么是值迭代(Value Iteration)？

A) Value Iteration finds an optimal policy by alternating Policy Evaluation and Policy Improvement.
B) None of these answers.
C) Value Iteration finds an optimal policy by directly iterating on the value function. / 值迭代通过直接对价值函数迭代来找到最优策略。
D) All of these answers.
E) Policy Iteration and Value Iteration always converge at the same rate.

> **Answer**: C
> Value Iteration combines evaluation and improvement into one step: $V(s) \leftarrow \max_a [R + \gamma \sum P(s'|s,a) V(s')]$, iterating until convergence.
> 值迭代将评估和改进合为一步，直接迭代 $V(s)$ 直到收敛。
