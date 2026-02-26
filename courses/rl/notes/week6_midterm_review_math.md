# Midterm Review: RL 期中复习 — 数学公式

> **See also:** [_cheatsheet.md](week6_midterm_review_cheatsheet.md) | [_code.md](week6_midterm_review_code.md)
> **Source:** Slides Week 1-5 + Quiz 1-4 + Midterm Review Slide 6
> **Coverage:** Weeks 1-5 全部数学公式

---

## ★ 核心公式 (Core Formulas)

### 状态函数 (State Function)

$$S_t = f(H_t)$$

| 符号 | 含义 | Meaning |
|------|------|---------|
| $S_t$ | 时间步 $t$ 的状态 | State at time $t$ |
| $f$ | 程序员选择的摘要函数 | Summary function (programmer's choice) |
| $H_t$ | Complete history: $R_1, O_1, A_1, ..., R_t, O_t, A_t$ | Full sequence of interactions |

---

### 马尔可夫性质 (Markov Property)

$$P(S_{t+1}, R_{t+1} \mid S_t, A_t) = P(S_{t+1}, R_{t+1} \mid S_1, A_1, ..., S_t, A_t)$$

简写: Future depends only on current state, not full history.

---

### 策略 (Policy)

**确定性策略:**

$$a = \pi(s)$$

**随机性策略:**

$$\pi(a \mid s) = P[A = a \mid S = s]$$

约束: $\sum_a \pi(a \mid s) = 1$

---

### 贪婪选择 (Greedy Selection)

$$a = \arg\max_{a'} Q(s, a')$$

含义: 选使 $Q$ 值最大的动作

---

### ε-Greedy 策略

$$a = \begin{cases} \arg\max_{a'} Q(s, a') & \text{with probability } 1-\epsilon \\ \text{random action} & \text{with probability } \epsilon \end{cases}$$

---

### 折扣回报 (Discounted Return)

**展开形式:**

$$G_t = r_{t+1} + \gamma r_{t+2} + \gamma^2 r_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1}$$

**递归形式:**

$$G_t = r_{t+1} + \gamma G_{t+1}$$

| 符号 | 含义 | 取值范围 |
|------|------|----------|
| $G_t$ | 从时间步 $t$ 的折扣回报 | |
| $\gamma$ | 折扣因子 | $0 \le \gamma < 1$ |
| $r_{t+k+1}$ | 未来第 $k$ 步的即时奖励 | |

| $\gamma$ 值 | 效果 |
|-------------|------|
| $\gamma = 0$ | 只看即时奖励 (myopic) |
| $\gamma \to 1$ | 所有奖励同等重要 (may diverge) |
| $0 < \gamma < 1$ | 平衡即时与未来 |

---

### 价值函数 (Value Functions)

**状态价值函数:**

$$V_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$$

**动作价值函数:**

$$Q_\pi(s, a) = \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a]$$

| 符号 | 输入 | 输出 |
|------|------|------|
| $V_\pi(s)$ | State only | Expected return from $s$ |
| $Q_\pi(s, a)$ | State + Action | Expected return from $s$ taking $a$ |

---

### Bellman 方程 — Q-Learning 版

$$Q(s, a) = R + \gamma \max_{a'} Q(s', a')$$

含义: Q 值 = 即时奖励 + 折扣后的下一状态最大 Q 值

Quiz 1 Q9: "immediate reward **+** **maximum** expected future rewards"

---

### ★★★ Q-Learning 更新规则 (Midterm 必考 — Slide 6)

$$Q(s, a) \leftarrow Q(s, a) + \alpha \Big[ R + \gamma \max_{a'} Q(s', a') - Q(s, a) \Big]$$

| 符号 | 含义 | Python 变量 |
|------|------|-------------|
| $Q(s, a)$ | 当前 Q 值 | `qtable[state][action]` |
| $\alpha$ | 学习率 (step size) | `alpha` |
| $R$ | 即时奖励 | `reward` |
| $\gamma$ | 折扣因子 | `gamma` |
| $\max_{a'} Q(s', a')$ | 下一状态最大 Q 值 | `max(qtable[next_state])` |
| $R + \gamma \max_{a'} Q(s', a')$ | TD target | — |
| $R + \gamma \max_{a'} Q(s', a') - Q(s,a)$ | TD error | — |

---

## 📝 手算练习 (Hand Calc Exercises)

### 练习 1: 折扣回报计算

**题目:** $\gamma = 0.9$，接下来 3 步奖励 $r_1 = -1, r_2 = -1, r_3 = 10$。求 $G_0$。

**解:**

$$G_0 = r_1 + \gamma r_2 + \gamma^2 r_3$$
$$= (-1) + 0.9 \times (-1) + 0.9^2 \times 10$$
$$= -1 + (-0.9) + 8.1 = \boxed{6.2}$$

---

### 练习 2: Bellman 方程求 Q 值

**题目:** $\gamma = 0.1$，agent 在状态 $s$ 做动作 $a$，获奖励 $r = 0$，到达 $s'$。$Q(s', \text{left}) = 0.3, Q(s', \text{right}) = 0.8, Q(s', \text{up}) = 0.1, Q(s', \text{down}) = 0.5$。求 $Q(s, a)$。

**解:**

Step 1: $\max_{a'} Q(s', a') = \max(0.3, 0.8, 0.1, 0.5) = 0.8$

Step 2: $Q(s, a) = r + \gamma \times \max_{a'} Q(s', a') = 0 + 0.1 \times 0.8 = \boxed{0.08}$

---

### 练习 3: Q-Learning 完整更新

**题目:** 当前 $Q(s, a) = 2.0$，$\alpha = 0.1$，$\gamma = 0.9$。Agent 在 $s$ 做 $a$，获 $r = 1$，到达 $s'$。$Q(s', a'_1) = 3.0, Q(s', a'_2) = 5.0$。求更新后的 $Q(s, a)$。

**解:**

Step 1: $\max_{a'} Q(s', a') = \max(3.0, 5.0) = 5.0$

Step 2: TD target $= r + \gamma \max_{a'} Q(s', a') = 1 + 0.9 \times 5.0 = 5.5$

Step 3: TD error $= 5.5 - Q(s, a) = 5.5 - 2.0 = 3.5$

Step 4: $Q(s, a) \leftarrow 2.0 + 0.1 \times 3.5 = 2.0 + 0.35 = \boxed{2.35}$

---

### 练习 4: ε-Greedy 概率计算

**题目:** 有 4 个动作，$\epsilon = 0.2$，$Q(s, a_1) = 1.5, Q(s, a_2) = 3.0, Q(s, a_3) = 2.0, Q(s, a_4) = 0.5$。求每个动作被选择的概率。

**解:**

Greedy action: $a_2$ (最大 Q 值 = 3.0)

随机概率: $\frac{\epsilon}{|A|} = \frac{0.2}{4} = 0.05$ each

| 动作 | 概率 | 计算 |
|------|------|------|
| $a_1$ | 0.05 | random only |
| $a_2$ | **0.85** | $(1 - \epsilon) + \frac{\epsilon}{|A|} = 0.8 + 0.05$ |
| $a_3$ | 0.05 | random only |
| $a_4$ | 0.05 | random only |

验证: $0.05 + 0.85 + 0.05 + 0.05 = 1.0$ ✅

---

### 练习 5: 随机策略概率

**题目:** 状态 $s$ 下有两个动作 $a_1, a_2$。$\pi(a_1|s) = 0.2$，求 $\pi(a_2|s)$。

**解:**

$$\pi(a_2|s) = 1 - \pi(a_1|s) = 1 - 0.2 = \boxed{0.8}$$

（约束: $\sum_a \pi(a|s) = 1$）

---

## 速查公式表 (Quick Formula Reference)

| 名称 | 公式 | 关键参数 |
|------|------|----------|
| State Function | $S_t = f(H_t)$ | $f$ = 程序员选择 |
| Deterministic Policy | $a = \pi(s)$ | 一对一映射 |
| Stochastic Policy | $\pi(a \mid s) = P[A=a \mid S=s]$ | $\sum_a \pi = 1$ |
| Greedy Selection | $a = \arg\max_{a'} Q(s, a')$ | 选最大 Q 值 |
| Discounted Return | $G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1}$ | $0 \le \gamma < 1$ |
| Return Recursive | $G_t = r_{t+1} + \gamma G_{t+1}$ | |
| State Value | $V_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$ | 只看未来 |
| Action Value | $Q_\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a]$ | 状态+动作 |
| Bellman (Q-Learning) | $Q(s,a) = R + \gamma \max_{a'} Q(s',a')$ | 即时+折扣最大 |
| **Q-Learning Update** | $Q(s,a) \leftarrow Q(s,a) + \alpha[R + \gamma \max Q(s',a') - Q(s,a)]$ | **必考** |
| ε-Greedy | $P(\text{greedy}) = 1-\epsilon$, $P(\text{random}) = \epsilon$ | |
