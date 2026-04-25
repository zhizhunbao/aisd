# Reinforcement Learning Quiz 4 – Antonin Raffin

---

**Question 1**
According to Antonin Raffin, what makes Reinforcement Learning difficult?
Antonin Raffin 认为什么让 RL 很难？

A) There is a sensitivity to hyperparameters and the random seed.
B) Algorithms can be sample inefficient.
C) Data collection is done by the agent rather than a human.
D) The appropriate reward function can be tricky to determine.
E) All of these answers. / 以上全部。

> **Answer**: E
> RL is difficult due to hyperparameter sensitivity, sample inefficiency, agent-driven data collection, and reward function design challenges — all combined.
> RL 难在超参数敏感、样本效率低、数据由智能体自行收集、奖励函数设计困难——全部叠加。

---

**Question 2**
What is reward hacking in RL?
什么是奖励黑客(Reward Hacking)？

A) A phenomenon where an algorithm maximizes reward without learning the desired behavior. / 算法最大化了奖励但没有学到期望行为。
B) It is an ad hoc process that results in a poor reward function.
C) It is the process of iteratively determining the optimal reward function.
D) All of these answers.
E) None of these answers.

> **Answer**: A
> Reward hacking: the agent exploits loopholes in the reward function to get high rewards without actually solving the intended task.
> 奖励黑客：智能体利用奖励函数的漏洞获得高奖励，但实际没有解决预期任务。

---

**Question 3**
What does Antonin Raffin recommend as RL best practices?
Antonin Raffin 推荐的 RL 最佳实践？

A) All of these answers. / 以上全部。
B) Use recommended hyperparameters for a particular algorithm.
C) Don't rely on a previously successful algorithm to be successful on a new problem.
D) Save a record of all experiment parameters, including random seed.
E) Do quantitative evaluation with multiple runs when comparing.

> **Answer**: A
> Best practices include: use recommended hyperparameters, don't assume transferability, record all parameters for reproducibility, and run multiple seeds for comparison.
> 最佳实践：使用推荐超参数、不假设可迁移性、记录所有参数以便复现、多次运行取比较。

---

**Question 4**
What questions should an RL practitioner ask when solving a new problem?
解决新问题时 RL 从业者应问什么？

A) None of these answers.
B) Do you really need RL?
C) Is RL compatible with safety guarantees?
D) Is RL compatible with stability guarantees?
E) All of these answers (questions). / 以上全部。

> **Answer**: E
> Before applying RL, ask: is RL really necessary? Are there safety/stability constraints that RL might violate?
> 应用 RL 前先问：真的需要 RL 吗？有安全/稳定性约束吗？

---

**Question 5**
What is involved in defining a custom task for RL?
为 RL 定义自定义任务涉及什么？

A) Define the observation space.
B) Define the reward function.
C) Define the termination conditions.
D) Define the action space.
E) All of these answers. / 以上全部。

> **Answer**: E
> Custom task = observation space + action space + reward function + termination conditions.
> 自定义任务 = 观测空间 + 动作空间 + 奖励函数 + 终止条件。

---

**Question 6**
What is involved in defining the observation space?
定义观测空间涉及什么？

A) Normalize values.
B) Ensure enough information to solve the task.
C) Don't break the Markov assumption.
D) None of these answers.
E) All of these answers (A/B/C). / 以上全部（A/B/C 都正确）。

> **Answer**: E
> Observation space design: normalize values, include sufficient information, and preserve the Markov property.
> 观测空间设计：归一化、包含足够信息、保持马尔可夫性。

---

**Question 7**
What is involved in defining the action space?
定义动作空间涉及什么？

A) Determine whether discrete or continuous actions.
B) Normalize continuous action spaces.
C) Evaluate complexity vs performance trade-offs.
D) Consider interactions between action space size and learning speed.
E) All of these answers. / 以上全部。

> **Answer**: E
> Action space design: discrete vs continuous, normalize if continuous, balance complexity and performance.
> 动作空间设计：离散还是连续、连续需归一化、平衡复杂度与性能。

---

**Question 8**
What does Raffin recommend regarding the reward function?
Raffin 对奖励函数有什么建议？

A) Consider primary rewards (main goal) and secondary rewards (desirable behavior).
B) Avoid reward hacking.
C) Consider sparse vs shaped rewards.
D) Start simple, then do reward shaping.
E) All of these answers. / 以上全部。

> **Answer**: E
> Reward design: primary + secondary rewards, avoid hacking, sparse vs shaped, start simple then shape.
> 奖励设计：主要+次要奖励、避免黑客、稀疏 vs 塑形、从简单开始再塑形。

---

**Question 9**
Recommendations for choosing the RL algorithm?
选择 RL 算法的建议？

A) Choose more time-tested, older algorithms if possible.
B) All of these answers.
C) None of these answers.
D) Choose more recently developed algorithms.
E) Consider your actions and whether the algorithm is designed for continuous or discrete actions. / 考虑你的动作类型以及算法是否适配。

> **Answer**: E
> Algorithm choice should be driven by whether your action space is continuous or discrete, not just algorithm age.
> 选算法应根据动作空间是连续还是离散来决定，而非仅看算法新旧。

---

**Question 10**
What to do if your RL system doesn't work the first time?
RL 系统第一次不工作怎么办？

A) Increase training budget.
B) Use a trusted implementation (e.g. stable-baselines3).
C) Check best practices compliance.
D) Simplify, then gradually add complexity.
E) All of these answers. / 以上全部。

> **Answer**: E
> Debug: increase training budget, use trusted implementations, follow best practices, and simplify first.
> 调试：增加训练预算、使用可信实现、遵循最佳实践、先简化再复杂化。
