# Midterm Review: RL 期中复习 — 概念速查

> **See also:** [_math.md](week6_midterm_review_math.md) | [_code.md](week6_midterm_review_code.md)
> **Source:** Slides Week 1-5 + Quiz 1-4 + Labs 1-2 + Assignment 1
> **Coverage — 覆盖范围:** Weeks 1-5 全部考试范围

---

## Reinforcement Learning — 强化学习基础

### Definition — 定义

- **RL (Reinforcement Learning, 强化学习):** A third type of ML where an agent learns to maximize cumulative reward through trial-and-error interaction — 机器学习的第三种类型，智能体通过试错交互学习最大化累积奖励
- **Agent (智能体):** The learner/decision-maker that interacts with the environment — 与环境交互的学习者/决策者
- **Environment (环境):** Everything outside the agent that it interacts with — Agent 之外的一切，Agent 与之交互的外部世界
- **Reward (奖励):** A scalar feedback signal $R_t$ indicating how well the agent is doing at step $t$ — 标量反馈信号，告诉 Agent 在时间步 $t$ 表现如何
- **Reward Hypothesis (奖励假说):** All goals can be described by the maximization of expected cumulative reward (Quiz 2 Q5) — 所有目标都可以用期望累积奖励的最大化来描述
- **MDP (Markov Decision Process, 马尔可夫决策过程):** An extension of the Markov chain with actions and rewards (Quiz 1 Q2); the mathematical framework for RL problems — 马尔可夫链的扩展，加入了动作和奖励；RL 问题的数学框架
- **Episode (回合):** A single run from starting state to terminal/truncated state (Quiz 2 Q6) — 从起始状态到终止/截断状态的一次完整运行

### Key Points — 关键要点

- RL is the **third** ML paradigm (NOT a subset of supervised or unsupervised) (Quiz 2 Q1) — RL 是第三种 ML 范式（不是监督或无监督学习的子类）
- Two core features: **trial-and-error search** + **delayed reward** — 两个核心特征：**试错搜索** + **延迟奖励**
- NO "correct answer" labels — only reward signals — 没有"正确答案"标签——只有奖励信号
- Agent may accept negative short-term rewards for better long-term return — Agent 可能接受短期负奖励以获得更好的长期回报
- Primary RL setup: **Agent, Environment, Reward** (Quiz 2 Q2) — RL 的核心三要素：**智能体、环境、奖励**

### Traps — 陷阱

- ⚠️ MDP transitions are **stochastic** $P(s'|s,a)$ — same state+action can lead to different states (Quiz 1 Q3: FALSE) — MDP 的转移是**随机的**——同一状态+动作可能导致不同的下一状态
- ⚠️ Undiscounted sum of rewards may be **infinite** → need discount factor $\gamma$ (Quiz 1 Q4) — 无折扣的奖励总和可能**无穷大** → 需要折扣因子 $\gamma$
- ⚠️ "Temporal Distance" is the **WRONG** term — correct is "Temporal **Difference**" (Quiz 2 Q14: answer E None) — "Temporal Distance" 是**错误**术语——正确的是"Temporal **Difference**"（时序差分）

### Compare — 对比：三大 ML 范式

| | Supervised — 监督学习 | Unsupervised — 无监督学习 | **Reinforcement — 强化学习** |
|---|---|---|---|
| Feedback — 反馈 | Labeled examples — 带标签样本 | None — 无 | **Reward signal — 奖励信号** |
| Goal — 目标 | Learn mapping — 学习映射 | Find structure — 发现结构 | **Maximize reward — 最大化奖励** |
| Data — 数据 | (input, label) pairs — (输入,标签)对 | Unlabeled data — 无标签数据 | **State-action-reward sequences — 状态-动作-奖励序列** |
| Exploration? — 需要探索？ | No — 否 | No — 否 | **Yes — 是** |

---

## Markov Property — 马尔可夫性质

### Definition — 定义

- **Markov Property (马尔可夫性质):** Future depends only on current state, NOT history (Quiz 2 Q3: answer E) — 未来只取决于当前状态，与历史无关
- **Markov Chain (马尔可夫链):** A mathematical model with probabilistic state transitions (Quiz 1 Q1) — 具有概率状态转移的数学模型

### Key Points — 关键要点

- State = compressed history: $S_t = f(H_t)$ — 状态 = 历史的压缩：$S_t = f(H_t)$
- Programmer chooses function $f$ — critically affects learning — 程序员选择函数 $f$——直接影响学习效果
- Environment state $S_t^{env}$ is always Markov — 环境状态 $S_t^{env}$ 始终满足马尔可夫性
- Full history $H_t$ is trivially Markov — 完整历史 $H_t$ 平凡地满足马尔可夫性

### Traps — 陷阱

- ⚠️ Position alone is NOT Markov for moving objects — need position + velocity — 仅位置对运动物体不满足马尔可夫性——需要位置+速度
- ⚠️ Quiz 2 Q3: "subsequent states **do not depend** on previous states" — this IS the correct Markov description (answer E) — "后续状态**不依赖于**先前状态"——这**是**正确的马尔可夫描述
- ⚠️ "Previous states **completely determine** future" is WRONG — that's the opposite of Markov — "先前状态**完全决定**未来"是**错误的**——这恰好与马尔可夫性质相反

---

## Policy — 策略

### Definition — 定义

- **Policy (策略, $\pi$):** Function mapping states to actions — 将状态映射到动作的函数
- **Deterministic Policy (确定性策略):** $a = \pi(s)$ — one action per state — 每个状态对应唯一动作
- **Stochastic Policy (随机性策略):** $\pi(a|s) = P[A=a|S=s]$ — probability distribution over actions — 在动作上的概率分布
- **Greedy Policy (贪婪策略):** Always pick $\arg\max_{a'} Q(s, a')$ — immediate reward maximization (Quiz 1 Q8, Quiz 2 Q12) — 总是选择使 Q 值最大的动作——即时奖励最大化
- **ε-Greedy Policy (ε-贪婪策略):** With probability $1-\epsilon$ pick greedy, with $\epsilon$ pick random — 以 $1-\epsilon$ 概率贪婪选择，$\epsilon$ 概率随机选择

### Key Points — 关键要点

- Policy determines behavior — core of an RL agent — 策略决定行为——RL 智能体的核心
- Policy is in the **Agent**, NOT the Environment (Quiz 2 Q15: answer A) — 策略在**智能体**中，不在环境中
- $\pi(a|s)$ is a probability distribution: $\sum_a \pi(a|s) = 1$ — $\pi(a|s)$ 是概率分布：所有动作概率之和 = 1

### Traps — 陷阱

- ⚠️ **Greedy** = immediate reward over future reward (Quiz 2 Q12: answer D), NOT "maximize total reward" — **贪婪** = 即时奖励优先于未来奖励，不是"最大化总回报"
- ⚠️ Policy $\pi$ maps state→action. Don't confuse with value function which maps state→value — 策略 $\pi$ 将状态映射到动作。别与价值函数（状态→值）混淆

---

## Value Functions — 价值函数

### Definition — 定义

- **State Value Function (状态价值函数) $V(s)$:** Expected return from state $s$ — takes STATE, gives return (Quiz 1 Q6) — 从状态 $s$ 出发的期望回报——输入状态，输出回报
- **Action Value Function (动作价值函数) $Q(s,a)$:** Expected return from state $s$ taking action $a$ — takes STATE+ACTION, gives return (Quiz 1 Q7) — 在状态 $s$ 采取动作 $a$ 的期望回报——输入状态+动作，输出回报

### Key Points — 关键要点

- Value function evaluates **future** rewards only — does NOT include past rewards — 价值函数只评估**未来**奖励——不包括过去的奖励
- $V(s)$ is in the **Agent**, not Environment (Quiz 2 Q15) — $V(s)$ 在**智能体**中，不在环境中
- We make decisions based on **value** (long-term), not reward (immediate) — 我们基于**价值**（长期）做决策，而非奖励（即时）

### Traps — 陷阱

- ⚠️ $V(s)$ takes **only state** → return. $Q(s,a)$ takes **state + action** → return (Quiz 2 Q10: answer E) — $V(s)$ 只接受**状态**→回报。$Q(s,a)$ 接受**状态+动作**→回报
- ⚠️ Don't confuse: Policy = chooses action, Value function = evaluates how good — 别混淆：策略 = 选动作，价值函数 = 评估好坏

### Compare — 对比：$V(s)$ vs $Q(s,a)$

| | $V(s)$ — 状态价值 | $Q(s,a)$ — 动作价值 |
|---|---|---|
| Input — 输入 | State only — 仅状态 | State + Action — 状态+动作 |
| Output — 输出 | Expected return — 期望回报 | Expected return — 期望回报 |
| Used for — 用途 | Evaluate states — 评估状态 | Choose actions directly — 直接选择动作 |

---

## Bellman Equation — 贝尔曼方程

### Definition — 定义

- **Bellman Equation (贝尔曼方程):** Expresses value as immediate reward + discounted successor value (Quiz 2 Q11: All correct — B, D, E) — 将价值表示为即时奖励 + 折扣后继值
- Recursive decomposition of value function — 价值函数的递归分解

### Key Points — 关键要点

- Forms mathematical basis for Q-Learning (Quiz 2 Q11 E) — 构成 Q-Learning 的数学基础
- Breaks value computation into recursive sub-problems (Quiz 2 Q11 D) — 将价值计算分解为递归子问题
- Relates current value to successor values (Quiz 2 Q11 B) — 将当前值与后继值关联

---

## Q-Learning — Q-Learning 算法

### Definition — 定义

- **Q-Learning:** Off-policy TD learning algorithm — learns optimal policy regardless of current behavior — 离策略 TD 学习算法——无论当前行为如何，都学习最优策略
- **SARSA:** On-policy TD learning — learns the policy being followed — 在策略 TD 学习——学习当前正在执行的策略
- **Off-policy (离策略):** Updates target uses best action regardless of what was actually taken — 更新目标使用最佳动作，不管实际采取了什么动作
- **On-policy (在策略):** Updates use the action actually taken — 更新使用实际采取的动作

### Key Points — 关键要点

- Q-Learning requires known, finite state set $S$ AND action set $A$ (Quiz 2 Q13: answer D) — Q-Learning 需要已知且有限的状态集 $S$ **和**动作集 $A$
- TD (Temporal Difference) is model-free, step-by-step learning — TD（时序差分）是无模型的、逐步学习
- Q-Learning is a form of TD learning — Q-Learning 是 TD 学习的一种

### Traps — 陷阱

- ⚠️ Q-Learning needs **BOTH** state set AND action set known (not just one — Quiz 2 Q13) — Q-Learning 需要**同时**知道状态集和动作集（不是只知道一个）
- ⚠️ Terminal state Q-values **must** be set to 0 (no future states) — 终止状态的 Q 值**必须**设为 0（没有后续状态）
- ⚠️ "Temporal **Distance**" is WRONG — correct is "Temporal **Difference**" (Quiz 2 Q14) — "Temporal **Distance**"是错误的——正确的是"Temporal **Difference**"

### Compare — 对比：Q-Learning vs SARSA (Midterm Slide 4)

| | Q-Learning | SARSA |
|---|---|---|
| Type — 类型 | Off-policy — 离策略 | On-policy — 在策略 |
| Update target — 更新目标 | $\max_{a'} Q(s',a')$ — 最大值 | $Q(s', a')$ (actual action — 实际动作) |
| CliffWalking result — 结果 | **Shortest path — 最短路径** (along cliff — 沿悬崖) | **Safe path — 安全路径** (away from cliff — 远离悬崖) |
| Why — 原因 | max ignores exploration danger — max 忽略探索的危险 | considers ε-greedy randomness — 考虑了 ε-greedy 的随机性 |

---

## Gymnasium (Midterm Slide 7-8)

### Definition — 定义

- **Gymnasium:** A framework for creating RL environments with a standard interface — 一个用于创建 RL 环境的框架，具有标准接口
- **Wrapper (包装器):** Modifies existing environment without altering underlying code — 在不修改底层代码的情况下修改现有环境的行为

### Key Points — 关键要点

- Standard API: `reset()`, `step()`, `render()` — 标准 API：`reset()` 重置，`step()` 执行，`render()` 渲染
- `step()` returns: `(next_state, reward, terminated, truncated, info)` — `step()` 返回 5 个值
- Custom env needs: `__init__`, `reset`, `step`, optional `render` — 自定义环境需要实现的方法
- Wrapper: initialize base env → pass to wrapper constructor — 先初始化基础环境 → 传给 wrapper 构造函数

---

## Stable-Baselines3 — SB3 框架 (Midterm Slide 9)

### Definition — 定义

- **SB3:** A set of reliable RL algorithm implementations — 一套可靠的强化学习算法实现

### Key Points — 关键要点

- **Vectorized environments (矢量化环境):** Run algorithm on multiple env copies simultaneously → faster training — 同时在多个环境副本上运行算法 → 加速训练
- **Callbacks (回调函数):** Custom code for monitoring, auto-saving, model manipulation, progress bars — 自定义代码用于监控、自动保存、模型操作、进度条

---

## Antonin Raffin RL Best Practices — RL 最佳实践 (Quiz 4)

### Key Points — 关键要点

- RL is hard: hyperparameter sensitivity + sample inefficiency + agent collects own data + reward design — RL 很难：超参敏感 + 采样低效 + 智能体自行采集数据 + 奖励设计困难
- **Reward hacking (奖励作弊):** Algorithm maximizes reward without learning desired behavior — 算法最大化奖励但没有学到期望的行为
- Best practices: use recommended hyperparams, don't rely on previous success, record all params, quantitative evaluation over multiple runs — 最佳实践：使用推荐超参、不依赖过去的成功经验、记录所有参数、多次运行做定量评估
- Before starting: Do you really need RL? Safety/stability guarantees? — 开始前先问：真的需要 RL 吗？安全性/稳定性有保证吗？
- Custom task definition: observation space + action space + reward function + termination conditions — 自定义任务定义：观测空间 + 动作空间 + 奖励函数 + 终止条件
- Observation space: normalize + enough info + don't break Markov assumption — 观测空间：归一化 + 足够信息 + 不违反马尔可夫假设
- Action space: discrete vs continuous + normalize continuous + complexity vs performance tradeoff — 动作空间：离散 vs 连续 + 连续必须归一化 + 权衡复杂度/性能
- Reward: start simple + avoid hacking + primary/secondary rewards + sparse/shaped — 奖励：从简单开始 + 防止作弊 + 主/次奖励 + 稀疏/塑形
- Algorithm choice: consider action type (continuous vs discrete) — 选算法：考虑动作类型（连续 vs 离散）
- Not working? Increase training budget + trusted implementation + check best practices + simplify first — 不好用？增加训练时间 + 可信实现 + 检查最佳实践 + 先简化再复杂化

---

## Agent Taxonomy — Agent 分类速查表

### Compare — 对比：按组件分类

| Type — 类型 | Policy — 策略 | Value Fn — 价值函数 | Model — 模型 |
|------|--------|----------|-------|
| **Value Based — 基于价值** | ❌ implicit — 隐式 | ✅ | Optional — 可选 |
| **Policy Based — 基于策略** | ✅ | ❌ | Optional — 可选 |
| **Actor Critic — 演员-评论家** | ✅ actor — 演员 | ✅ critic — 评论家 | Optional — 可选 |

### Compare — 对比：按模型分类

| Type — 类型 | Has Model? — 有模型？ |
|------|------------|
| **Model Free — 无模型** | ❌ — learns from experience only — 仅从经验学习 |
| **Model Based — 基于模型** | ✅ — can plan ahead — 可以提前规划 |

> 💡 **Q-Learning = Value Based + Model Free — Q-Learning 是基于价值的无模型方法**

---

## Agent vs Environment — 智能体 vs 环境的职责 (Quiz 2 Q15)

| Component — 组件 | Location — 位置 | Function — 功能 |
|-----------|----------|----------|
| Policy $\pi$ — 策略 | **Agent — 智能体** | Choose actions — 选择动作 |
| Value Function $V/Q$ — 价值函数 | **Agent — 智能体** | Evaluate states/actions — 评估状态/动作 |
| Transition $P(s'|s,a)$ — 状态转移 | **Environment — 环境** | Determine next state — 决定下一状态 |
| Reward $R$ — 奖励 | **Environment — 环境** | Provide feedback — 提供反馈 |
| Action results — 动作结果 | **Environment — 环境** | NOT the agent — 不是智能体的职责 |
