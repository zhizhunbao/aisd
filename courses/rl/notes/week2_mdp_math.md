# Week 2: MDP — 数学公式

> **See also:** [_cheatsheet.md](week2_mdp_cheatsheet.md) | [_code.md](week2_mdp_code.md)
> **数学前置：** [马尔可夫链与MDP](../../math/probability/markov_chains.md) | [几何级数与折扣回报](../../math/calculus/geometric_series.md) | [Argmax](../../math/general/argmax.md)
> **Source:** Slides CST8509_02 + Quiz 2 + Lab 2

---

## ★ 回报与折扣 (Return & Discounting)

### 无折扣回报 (Undiscounted Return — 有问题)

$$G_t = R_{t+1} + R_{t+2} + R_{t+3} + \cdots + R_T$$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $G_t$ | 从时间步 $t$ 开始的回报 | Return from time step $t$ |
| $R_{t+k}$ | 时间步 $t+k$ 的即时奖励 | Immediate reward at step $t+k$ |
| $T$ | 终止时间步 | Terminal time step |

⚠️ 问题：持续任务中 $T = \infty$，则 $G_t$ 可能发散到 $\infty$（Quiz 2 Q7）

### 折扣回报 (Discounted Return — 正确)

$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $\gamma$ | 折扣因子，$0 \le \gamma < 1$ | Discount factor |
| $\gamma^k$ | 第 $k$ 步未来奖励的衰减权重 | Decay weight for reward $k$ steps in future |

### 递归形式 (Recursive Form)

$$G_t = R_{t+1} + \gamma G_{t+1}$$

含义：当前回报 = 即时奖励 + 折扣后的下一步回报

### 折扣因子含义 (Meaning of $\gamma$)

| $\gamma$ 值 | 效果（中文） | Effect (English) |
|-------------|------------|------------------|
| $\gamma = 0$ | 只看即时奖励（极度近视） | Only immediate reward (myopic) |
| $\gamma \to 1$ | 所有奖励几乎同等重要（更有远见） | All rewards nearly equal weight (farsighted) |
| $0 < \gamma < 1$ | 平衡即时与未来 | Balance immediate and future |

### 手算：折扣回报 (Hand Calc: Discounted Return)

**题目 (Problem):** $\gamma = 0.9$，接下来 3 步奖励为 $R_1 = -1, R_2 = -1, R_3 = 10$，之后终止。求 $G_0$。

**解 (Solution):**

Step 1: $G_0 = R_1 + \gamma R_2 + \gamma^2 R_3$

Step 2: $G_0 = (-1) + 0.9 \times (-1) + 0.9^2 \times 10$

Step 3: $G_0 = -1 + (-0.9) + 8.1 = 6.2$

---

## 策略 (Policy)

### 随机策略 (Stochastic Policy)

$$\pi(a|s) = P[A_t = a | S_t = s]$$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $\pi$ | 策略函数 | Policy function |
| $a$ | 动作 | Action |
| $s$ | 状态 | State |
| $P[\cdot]$ | 概率 | Probability |

约束 (Constraint)：$\sum_a \pi(a|s) = 1$（所有动作概率之和 = 1）

### 确定性策略 (Deterministic Policy)

$$\pi(s) = a$$

含义 (Meaning)：给定状态 $s$，输出唯一确定的动作 $a$

---

## 价值函数 (Value Functions)

### 状态价值函数 (State-Value Function)

$$v_\pi(s) \doteq \mathbb{E}_\pi[G_t | S_t = s]$$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $v_\pi(s)$ | 策略 $\pi$ 下状态 $s$ 的价值 | Value of state $s$ under policy $\pi$ |
| $\mathbb{E}_\pi$ | 遵循策略 $\pi$ 的期望 | Expectation following policy $\pi$ |
| $G_t$ | 从时间步 $t$ 的折扣回报 | Discounted return from step $t$ |

含义 (Meaning)：从状态 $s$ 出发，遵循策略 $\pi$，能获得的期望总回报

### 动作价值函数 (Action-Value Function)

$$q_\pi(s, a) \doteq \mathbb{E}_\pi[G_t | S_t = s, A_t = a]$$

含义 (Meaning)：在状态 $s$ 采取动作 $a$，然后遵循策略 $\pi$，能获得的期望总回报

### V 与 Q 的关系

$$v_\pi(s) = \sum_a \pi(a|s) \cdot q_\pi(s, a)$$

含义 (Meaning)：状态价值 = 各动作价值在策略概率下的加权平均

---

## Bellman 方程 (Bellman Equations)

### 状态价值的 Bellman 方程

$$v_\pi(s) = \mathbb{E}_\pi[R_{t+1} + \gamma \cdot v_\pi(S_{t+1}) | S_t = s]$$

含义 (Meaning)：当前状态的价值 = 即时奖励的期望 + 折扣后下一状态价值的期望

### Q-Learning 的 Bellman 方程（确定性环境）

$$Q(s, a) = r + \gamma \max_{a'} Q(s', a')$$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $Q(s, a)$ | 状态 $s$ 动作 $a$ 的价值 | Value of action $a$ in state $s$ |
| $r$ | 即时奖励 | Immediate reward |
| $\gamma$ | 折扣因子 | Discount factor |
| $s'$ | 下一状态 | Next state |
| $\max_{a'} Q(s', a')$ | 下一状态最大 Q 值 | Max Q-value in next state |

### SARSA 的 Bellman 方程

$$Q(s, a) = r + \gamma Q(s', a')$$

区别：这里 $a'$ 是**实际选择**的下一动作，不是最大值动作

---

## Q-Learning vs SARSA 更新规则 (Update Rules)

### Q-Learning 更新（含学习率）

$$Q(S, A) \leftarrow Q(S, A) + \alpha \left[ R + \gamma \max_{a'} Q(S', a') - Q(S, A) \right]$$

| 符号 | 含义（中文） | Meaning (English) |
|------|------------|-------------------|
| $\alpha$ | 学习率，$0 < \alpha \le 1$ | Learning rate |
| $R + \gamma \max_{a'} Q(S', a')$ | TD 目标 | TD target |
| $R + \gamma \max_{a'} Q(S', a') - Q(S, A)$ | TD 误差 | TD error |

### SARSA 更新（含学习率）

$$Q(S, A) \leftarrow Q(S, A) + \alpha \left[ R + \gamma Q(S', A') - Q(S, A) \right]$$

区别仅在于 TD 目标：$Q(S', A')$ vs $\max_{a'} Q(S', a')$

### 手算：Q-Learning 更新 (Hand Calc: Q-Learning Update)

**题目 (Problem):** $\alpha = 0.5$, $\gamma = 0.9$。当前 $Q(s, a) = 2.0$。Agent 执行 $a$ 后得到 $R = -1$，到达 $s'$。$Q(s', \text{left}) = 1.0, Q(s', \text{right}) = 3.0$。求新 $Q(s, a)$。

**解 (Solution):**

Step 1: $\max_{a'} Q(s', a') = \max(1.0, 3.0) = 3.0$

Step 2: TD target = $R + \gamma \max Q = -1 + 0.9 \times 3.0 = 1.7$

Step 3: TD error = $1.7 - Q(s, a) = 1.7 - 2.0 = -0.3$

Step 4: $Q(s, a) \leftarrow 2.0 + 0.5 \times (-0.3) = 2.0 - 0.15 = 1.85$

### 手算：SARSA 更新 (Hand Calc: SARSA Update)

**题目 (Problem):** 同上，但 agent 的 ε-greedy 选择了 $A' = \text{left}$（$Q(s', \text{left}) = 1.0$）。

**解 (Solution):**

Step 1: $Q(S', A') = Q(s', \text{left}) = 1.0$

Step 2: TD target = $R + \gamma Q(S', A') = -1 + 0.9 \times 1.0 = -0.1$

Step 3: TD error = $-0.1 - 2.0 = -2.1$

Step 4: $Q(s, a) \leftarrow 2.0 + 0.5 \times (-2.1) = 2.0 - 1.05 = 0.95$

> ⚠️ 注意差异：Q-Learning 更新到 1.85，SARSA 更新到 0.95。因为 SARSA 用了较差的实际动作值。

---

## 贪婪选择 (Greedy Selection)

$$a^* = \arg\max_{a'} Q(s, a')$$

含义 (Meaning)：选择使当前 Q 值估计最大的动作

⚠️ 贪婪 = 优先即时奖励（Quiz 2 Q12: D）。这不一定是全局最优。

---

## 速查公式表 (Quick Formula Reference)

| 名称 (Name) | 公式 (Formula) | 关键参数 (Key Params) |
|-------------|---------------|---------------------|
| 折扣回报 Discounted Return | $G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$ | $0 \le \gamma < 1$ |
| 回报递归 Return Recursive | $G_t = R_{t+1} + \gamma G_{t+1}$ | |
| 随机策略 Stochastic Policy | $\pi(a \mid s) = P[A_t=a \mid S_t=s]$ | $\sum_a \pi(a \mid s) = 1$ |
| 状态价值 State Value | $v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$ | 只看未来奖励 |
| 动作价值 Action Value | $q_\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a]$ | 状态+动作→回报 |
| V 与 Q 关系 | $v_\pi(s) = \sum_a \pi(a \mid s) q_\pi(s,a)$ | V 是 Q 的加权平均 |
| Bellman (V) | $v_\pi(s) = \mathbb{E}[R + \gamma v_\pi(S')]$ | 即时 + 折扣后继 |
| Q-Learning 更新 | $Q \leftarrow Q + \alpha[R + \gamma \max Q' - Q]$ | Off-policy |
| SARSA 更新 | $Q \leftarrow Q + \alpha[R + \gamma Q(S',A') - Q]$ | On-policy |
| 贪婪选择 Greedy | $a = \arg\max_{a'} Q(s, a')$ | 选当前最大 Q |
