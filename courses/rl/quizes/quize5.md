# Reinforcement Learning Quiz 5 – Stable-Baselines3

---

**Question 1**
Which of the following is a design principle of Stable-Baselines3 (SB3)?
SB3 的设计原则是什么？

A) SB3 is user-friendly.
B) SB3 focuses on model-free, single agent RL.
C) All of these answers. / 以上全部。
D) SB3 is to be a set of reliable RL algorithms.
E) SB3 favours readability and simplicity over modularity.

> **Answer**: C
> SB3 design: user-friendly, model-free single-agent focus, reliable algorithms, readability over modularity.
> SB3 设计：用户友好、专注 model-free 单智能体、可靠算法、可读性优先于模块化。

---

**Question 2**
Which of the following is a feature of SB3?
SB3 有哪些特性？

A) A selection of on-policy and off-policy algorithms.
B) A clean and simple interface.
C) A callback system.
D) Fully documented.
E) All of these answers. / 以上全部。

> **Answer**: E
> SB3 features: on/off-policy algorithms, clean interface, callback system, full documentation.
> SB3 特性：on/off-policy 算法、简洁接口、回调系统、完整文档。

---

**Question 3**
Which is the proper ordering of steps when using SB3?
使用 SB3 的正确步骤顺序？

A) Save → Train → Define → Load
B) Define → Train → Save → Load / 定义 → 训练 → 保存 → 加载
C) None of these answers.
D) Load → Define → Train → Save
E) Train → Define → Load → Save

> **Answer**: B
> Correct workflow: Define an agent → Train → Save → Load for inference.
> 正确流程：定义智能体 → 训练 → 保存 → 加载推理。

---

**Question 4**
What is the meaning of the `deterministic` parameter in SB3's `predict` method?
SB3 `predict` 方法中 `deterministic` 参数是什么意思？

A) It specifies whether the action should be chosen deterministically or stochastically according to the probability distribution. / 指定动作是确定性选择还是按概率分布随机选择。
B) All of these answers.
C) It specifies whether the environment is deterministic or not.
D) It specifies whether a predefined action sequence should be used.
E) None of these answers.

> **Answer**: A
> `deterministic=True`: always pick the most probable action. `False`: sample from the policy distribution.
> `deterministic=True`：总是选最可能的动作。`False`：从策略分布中采样。

---

**Question 5**
What does the SB3 `model.learn()` method do?
SB3 的 `model.learn()` 做什么？

A) All of these answers.
B) Allows user to select experience collection or policy update.
C) Collects experience with `model.train()` and updates with `model.collect_rollouts()`.
D) Alternates between collecting experience with `model.collect_rollouts()` and updating policy with `model.train()`. / 交替执行经验收集和策略更新。
E) None of these answers.

> **Answer**: D
> `learn()` alternates: `collect_rollouts()` (gather experience) → `train()` (update policy), repeating for the specified timesteps.
> `learn()` 交替执行：`collect_rollouts()`（收集经验）→ `train()`（更新策略）。

---

**Question 6**
What is the SB3 Reinforcement Learning Zoo?
SB3 的 RL Zoo 是什么？

A) All of these answers.
B) A framework for managing experiments and tuning hyperparameters. / 用于管理实验和调优超参数的框架。
C) None of these answers.
D) A training framework for zoo animal agents.
E) A selection of environments for zoo animals.

> **Answer**: B
> RL Zoo = experiment management + hyperparameter tuning framework built on SB3.
> RL Zoo = 基于 SB3 的实验管理 + 超参数调优框架。
