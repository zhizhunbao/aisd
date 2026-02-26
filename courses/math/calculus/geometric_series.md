# Geometric Series & Discounted Return | 几何级数与折扣回报

> **Purpose:** Define geometric series convergence and its application to discounted return in RL — why $G_t$ doesn't diverge.
> **Primary Source:** Sutton & Barto §3.3, pp.54–56
> **See also:** [markov_chains.md](../probability/markov_chains.md)
> **Prerequisites:** None

---

## §1 Geometric Series (几何级数)

> 📚 Source: Standard calculus; applied in Sutton & Barto §3.3, p.55

### 1.1 Definition (定义)

An infinite geometric series with ratio $\gamma$:

| Symbol | Meaning (EN) | 含义 (中文) | Constraint |
| --- | --- | --- | --- |
| $\gamma$ | Common ratio | 公比 | $0 \le \gamma < 1$ |

$$\sum_{k=0}^{\infty} \gamma^k = 1 + \gamma + \gamma^2 + \gamma^3 + \cdots = \frac{1}{1 - \gamma}$$

> 📖 **Reading the notation:** Add up $1 + \gamma + \gamma^2 + \ldots$ forever. When $\gamma < 1$, each term shrinks, so the total is finite = $\frac{1}{1-\gamma}$. When $\gamma = 1$: $1+1+1+\ldots = \infty$.

### 1.2 Why It Matters for RL (为什么 RL 需要)

In continuing tasks (no terminal state), total reward $\sum R$ may be infinite. Multiplying by $\gamma^k$ ensures convergence:

If $|R_t| \le R_{\max}$, then $|G_t| \le \frac{R_{\max}}{1 - \gamma}$

> ⚠️ **Quiz 1 Q4:** "Sum of all subsequent rewards might be infinite" — this is why we need $\gamma$.

### 1.3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Compute $\sum_{k=0}^{\infty} 0.5^k$.

> 📚 Direct application of geometric series formula
> 💡 **Hint:** $\gamma = 0.5$, plug into $\frac{1}{1-\gamma}$.

**Solution:** $\frac{1}{1 - 0.5} = 2$

#### 🟡 Medium | 中等题

**P2.** If $\gamma = 0.9$ and max reward per step is 1, what is the upper bound on $|G_t|$?

> 📐 Original Problem — based on Sutton §3.3
> 💡 **Hint:** $|G_t| \le R_{\max} \cdot \frac{1}{1-\gamma}$

**Solution:** $|G_t| \le 1 \cdot \frac{1}{1-0.9} = 10$

---

## §2 Discounted Return (折扣回报)

> 📚 Source: Sutton & Barto §3.3, Eq. 3.8, p.55

### 2.1 Definition (定义)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $G_t$ | Discounted return from step $t$ | 从步骤 $t$ 的折扣回报 |
| $\gamma$ | Discount factor, $0 \le \gamma < 1$ | 折扣因子 |
| $R_{t+k+1}$ | Reward $k$ steps ahead | 未来第 $k$ 步奖励 |

$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots$$

**Recursive form (递归形式):**

$$G_t = R_{t+1} + \gamma G_{t+1}$$

> 📚 Sutton §3.3, Eq. 3.9, p.55

### 2.2 Effect of $\gamma$ (折扣因子效果)

| $\gamma$ | Behavior | $\frac{1}{1-\gamma}$ |
| --- | --- | --- |
| $0$ | Only immediate reward (myopic) | 1 |
| $0.9$ | Far-sighted | 10 |
| $0.99$ | Very far-sighted | 100 |
| $1$ | No discounting (may diverge) | $\infty$ |

### 2.3 Worked Example (手算例题)

> 📐 Original Problem — based on Sutton §3.3

$\gamma = 0.9$, rewards $R_1 = -1, R_2 = -1, R_3 = 10$.

$G_0 = (-1) + 0.9(-1) + 0.81(10) = -1 - 0.9 + 8.1 = 6.2$

Negative short-term + large future reward → positive total. Core RL idea: sacrifice short-term for long-term.

### 2.4 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P3.** $\gamma = 0.5$, rewards $R_1 = 2, R_2 = 4, R_3 = 8$. Compute $G_0$.

> 📐 Original Problem
> 💡 **Hint:** $G_0 = R_1 + \gamma R_2 + \gamma^2 R_3$

**Solution:** $G_0 = 2 + 0.5(4) + 0.25(8) = 2 + 2 + 2 = 6$

#### 🟡 Medium | 中等题

**P4.** Constant reward $R = 1$ forever. Show $G_0 = \frac{1}{1-\gamma}$.

> 📚 From: Sutton §3.3, p.55
> 💡 **Hint:** Substitute $R_{t+k+1} = 1$ into $G_t$ formula.

**Solution:** $G_0 = \sum_{k=0}^{\infty} \gamma^k \cdot 1 = \frac{1}{1-\gamma}$

#### 🔴 Hard | 挑战题

**P5.** Prove the recursive form: $G_t = R_{t+1} + \gamma G_{t+1}$.

> 📚 From: Sutton §3.3, Eq. 3.9, p.55
> 💡 **Hint:** Factor $\gamma$ from the second term onward, then re-index.

**Solution:**

$G_t = R_{t+1} + \sum_{k=1}^{\infty} \gamma^k R_{t+k+1} = R_{t+1} + \gamma \sum_{j=0}^{\infty} \gamma^j R_{(t+1)+j+1} = R_{t+1} + \gamma G_{t+1}$ ∎

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Geometric series | $\sum \gamma^k = \frac{1}{1-\gamma}$ | Calculus | Convergence proof |
| Discounted return | $G_t = \sum \gamma^k R_{t+k+1}$ | Sutton §3.3, Eq.3.8 | RL all weeks |
| Recursive return | $G_t = R_{t+1} + \gamma G_{t+1}$ | Sutton §3.3, Eq.3.9 | Bellman equation |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Section | Pages |
| --- | --- | --- | --- |
| §1 | Standard calculus | Geometric series | — |
| §1–2 | Sutton & Barto | §3.3, Eq. 3.8–3.9 | pp.54–56 |
