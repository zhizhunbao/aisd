# Week 1: RL 入门 — 数学公式

> **See also:** [_cheatsheet.md](week1_rl_intro_cheatsheet.md) | [_code.md](week1_rl_intro_code.md)
> **数学前置：** [马尔可夫链与MDP](../../math/probability/markov_chains.md) | [几何级数与折扣回报](../../math/calculus/geometric_series.md) | [Argmax](../../math/general/argmax.md)
> **Source:** Slides CST8509_01 + Quiz 1 + Medium Q-Learning 文章

---

## ★ 数学基础 (Math Foundations)

Week 1 是概念入门，数学内容较少。以下是本周涉及的核心数学符号和公式。

### 概率与条件概率 (Probability & Conditional Probability)

- **条件概率 (Conditional Probability):**

$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$

$A$ = 目标事件 (target event), $B$ = 已知条件 (known condition)

- **随机策略用到条件概率：**

$\pi(a \mid s) = P[A = a \mid S = s]$

$a$ = 动作 (action), $s$ = 状态 (state), $\pi$ = 策略 (policy)

含义 (Meaning)：在状态 $s$ 下选择动作 $a$ 的概率
Meaning: probability of choosing action $a$ in state $s$

---

## 状态与历史 (State & History)

### 状态函数 (State Function)

- **状态是历史的函数 (State as function of history):**

$S_t = f(H_t)$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $S_t$ | 时间步 $t$ 的状态 | State at time step $t$ |
| $f$ | 程序员选择的摘要函数 | Summary function chosen by programmer |
| $H_t$ | 到时间步 $t$ 的完整历史 | Complete history up to time step $t$ |

- **历史的完整定义 (Full history definition):**

$H_t = R_1, O_1, A_1, R_2, O_2, A_2, ..., R_t, O_t, A_t$

$R$ = 奖励 (reward), $O$ = 观测 (observation), $A$ = 动作 (action)

### 马尔可夫性质 (Markov Property)

- **马尔可夫性质的数学定义 (Mathematical definition):**

$P(S_{t+1}, R_{t+1} \mid S_t, A_t) = P(S_{t+1}, R_{t+1} \mid S_1, A_1, S_2, A_2, ..., S_t, A_t)$

含义 (Meaning)：给定当前状态和动作，未来的概率与过去的历史无关
Meaning: given current state and action, future probabilities are independent of past history

简写 (Shorthand)：$P(S_t, R_t)$ 仅取决于 $S_{t-1}$ 和 $A_{t-1}$
Shorthand: $P(S_t, R_t)$ depends only on $S_{t-1}$ and $A_{t-1}$

---

## 策略 (Policy)

### 确定性策略 (Deterministic Policy)

- **确定性策略 (Deterministic policy):**

$a = \pi(s)$

$s$ = 当前状态 (current state), $a$ = 选择的动作 (chosen action), $\pi$ = 策略函数 (policy function)

含义 (Meaning)：给定状态，输出唯一确定的动作
Meaning: given a state, output exactly one action

### 随机性策略 (Stochastic Policy)

- **随机性策略 (Stochastic policy):**

$\pi(a \mid s) = P[A = a \mid S = s]$

含义 (Meaning)：给定状态 $s$，输出动作 $a$ 的概率
Meaning: given state $s$, output probability of action $a$

约束 (Constraint)：$\sum_a \pi(a \mid s) = 1$（所有动作概率之和 = 1）

### 手算：随机策略概率 (Hand Calc: Stochastic Policy)

**题目 (Problem):** 在某状态 $s$ 下，有两个动作 $a_1$ 和 $a_2$。$\pi(a_1 \mid s) = 0.2$，求 $\pi(a_2 \mid s)$。

**解 (Solution):**

$\pi(a_2 \mid s) = 1 - \pi(a_1 \mid s) = 1 - 0.2 = 0.8$

---

## 价值函数 (Value Functions)

### 状态价值函数 (State Value Function)

- **状态价值函数 (State value function):**

$V_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $V_\pi(s)$ | 在策略 $\pi$ 下状态 $s$ 的价值 | Value of state $s$ under policy $\pi$ |
| $\mathbb{E}_\pi$ | 在策略 $\pi$ 下的期望 | Expectation under policy $\pi$ |
| $G_t$ | 从时间步 $t$ 开始的回报 | Return from time step $t$ |

含义 (Meaning)：从状态 $s$ 出发，遵循策略 $\pi$，能获得的期望总回报
Meaning: expected total return starting from state $s$, following policy $\pi$

### 动作价值函数 (Action Value Function)

- **动作价值函数 (Action value function):**

$Q_\pi(s, a) = \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a]$

含义 (Meaning)：在状态 $s$ 采取动作 $a$，然后遵循策略 $\pi$，能获得的期望总回报
Meaning: expected total return starting from state $s$, taking action $a$, then following policy $\pi$

### 贪婪策略 (Greedy Policy)

- **贪婪动作选择 (Greedy action selection):**

$a = \arg\max_{a'} Q(s, a')$

含义 (Meaning)：选择使 $Q$ 值最大的动作
Meaning: choose the action that maximizes $Q$ value

---

## 回报与折扣 (Return & Discounting)

### 总回报 (Total Return)

- **无折扣回报 (Undiscounted return) — 有问题的定义：**

$R_t = r_{t+1} + r_{t+2} + r_{t+3} + ...$

问题 (Problem)：在无限步任务中可能发散到 $\infty$（Quiz 1 Q4）

- **折扣回报 (Discounted return) — 正确的定义：**

$G_t = r_{t+1} + \gamma r_{t+2} + \gamma^2 r_{t+3} + ... = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1}$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $G_t$ | 从时间步 $t$ 开始的折扣回报 | Discounted return from time step $t$ |
| $\gamma$ | 折扣因子，$0 \le \gamma < 1$ | Discount factor |
| $r_{t+k+1}$ | 未来第 $k$ 步的即时奖励 | Immediate reward $k$ steps in the future |

- **递归形式 (Recursive form):**

$G_t = r_{t+1} + \gamma G_{t+1}$

### 折扣因子的含义 (Meaning of Discount Factor)

| $\gamma$ 值 | 效果（中文） | Effect (English) |
|-------------|------------|------------------|
| $\gamma = 0$ | 只看即时奖励 | Only immediate reward (myopic) |
| $\gamma = 1$ | 所有奖励同等重要（可能发散） | All rewards equally important (may diverge) |
| $0 < \gamma < 1$ | 平衡即时与未来 | Balance immediate and future |

### 手算：折扣回报 (Hand Calc: Discounted Return)

**题目 (Problem):** $\gamma = 0.9$，接下来3步的奖励分别是 $r_1 = -1, r_2 = -1, r_3 = 10$。求 $G_0$。

**解 (Solution):**

Step 1: $G_0 = r_1 + \gamma r_2 + \gamma^2 r_3$

Step 2: $G_0 = (-1) + 0.9 \times (-1) + 0.9^2 \times 10$

Step 3: $G_0 = -1 + (-0.9) + 8.1 = 6.2$

---

## Bellman 方程 (Bellman Equation)

### Q-Learning 的 Bellman 方程 (Bellman Equation for Q-Learning)

- **Bellman 方程（确定性环境，贪婪策略）：**

$Q(s, a) = r + \gamma \max_{a'} Q(s', a')$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $Q(s, a)$ | 在状态 $s$ 采取动作 $a$ 的价值 | Value of taking action $a$ in state $s$ |
| $r$ | 采取动作 $a$ 后的即时奖励 | Immediate reward after taking action $a$ |
| $\gamma$ | 折扣因子 | Discount factor |
| $s'$ | 采取动作 $a$ 后到达的下一个状态 | Next state after taking action $a$ |
| $\max_{a'} Q(s', a')$ | 下一状态中最大的 Q 值 | Maximum Q value in next state |

含义 (Meaning)：一个动作的价值 = 即时奖励 + 折扣后的下一状态最大未来价值
Meaning: value of an action = immediate reward + discounted max future value from next state

Quiz 1 Q9：答案 E — "immediate reward + maximum expected future rewards in next state"

### 手算：Bellman 方程更新 (Hand Calc: Bellman Update)

**题目 (Problem):** $\gamma = 0.1$，agent 在状态 $s$ 采取动作 $a$，获得奖励 $r = 0$，到达状态 $s'$。$s'$ 的 Q 值为 $Q(s', \text{left}) = 0.3, Q(s', \text{right}) = 0.8, Q(s', \text{up}) = 0.1, Q(s', \text{down}) = 0.5$。求 $Q(s, a)$。

**解 (Solution):**

Step 1: $\max_{a'} Q(s', a') = \max(0.3, 0.8, 0.1, 0.5) = 0.8$

Step 2: $Q(s, a) = r + \gamma \times \max_{a'} Q(s', a') = 0 + 0.1 \times 0.8 = 0.08$

---

## 速查公式表 (Quick Formula Reference)

| 名称 (Name) | 公式 (Formula) | 关键参数 (Key Params) |
|-------------|---------------|---------------------|
| 状态函数 State Function | $S_t = f(H_t)$ | $f$ = 程序员选择的函数 |
| 确定性策略 Deterministic Policy | $a = \pi(s)$ | $s$ → $a$ 一对一映射 |
| 随机性策略 Stochastic Policy | $\pi(a \mid s) = P[A=a \mid S=s]$ | $\sum_a \pi(a \mid s) = 1$ |
| 折扣回报 Discounted Return | $G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1}$ | $0 \le \gamma < 1$ |
| 回报递归 Return Recursive | $G_t = r_{t+1} + \gamma G_{t+1}$ | |
| 状态价值 State Value | $V_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$ | 只看未来奖励 |
| 动作价值 Action Value | $Q_\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a]$ | 状态+动作→回报 |
| Bellman (Q-Learning) | $Q(s,a) = r + \gamma \max_{a'} Q(s',a')$ | 即时奖励+折扣最大未来值 |
| 贪婪选择 Greedy Selection | $a = \arg\max_{a'} Q(s, a')$ | 选 Q 值最大的动作 |
