# Argmax & Greedy Selection | Argmax 与贪婪选择

> **Purpose:** Define the $\arg\max$ operator and its use in greedy action selection — the basis for Q-Learning's exploitation step.
> **Primary Source:** Sutton & Barto §2.2, p.27
> **See also:** [markov_chains.md](../probability/markov_chains.md)
> **Prerequisites:** None

---

## §1 Argmax Operator (Argmax 运算符)

> 📚 Source: Sutton & Barto §2.2, Eq. 2.2, p.27

### 1.1 Definition (定义)

$\arg\max$ returns the **argument** (input) that maximizes a function — not the maximum value itself.

$\arg\max$ 返回使函数取最大值的**参数**，而不是最大值本身。

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\arg\max_a f(a)$ | The $a$ that makes $f(a)$ largest | 使 $f(a)$ 最大的那个 $a$ |
| $\max_a f(a)$ | The largest value of $f(a)$ | $f(a)$ 的最大值本身 |

> 📖 **Reading the notation:** "$\arg\max_{a'} Q(s, a')$" = "the action $a'$ that makes $Q(s, a')$ the biggest."

### 1.2 Argmax vs Max (区别)

Given $f(x) = \{f(a)=3, f(b)=7, f(c)=5\}$:

- $\max_x f(x) = 7$ (the value)
- $\arg\max_x f(x) = b$ (the input)

> 🔗 **Course Connection:**
> - **RL all weeks:** Greedy action = $\arg\max_a Q(s,a)$
> - **ML W5 MAP:** $\hat{y} = \arg\max_y P(Y=y \mid X)$

### 1.3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** $Q(s, a_1) = 5, Q(s, a_2) = 3, Q(s, a_3) = 7, Q(s, a_4) = 1$. What is $\arg\max_a Q(s,a)$? What is $\max_a Q(s,a)$?

> 📐 Original Problem
> 💡 **Hint:** Find the action with highest Q, and the highest Q value.

**Solution:** $\arg\max = a_3$ (the action), $\max = 7$ (the value)

---

## §2 Greedy Action Selection (贪婪动作选择)

> 📚 Source: Sutton & Barto §2.2, Eq. 2.2, p.27

### 2.1 Definition (定义)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $a^*$ | Greedy action | 贪婪动作 |
| $Q(s, a)$ | Estimated value of action $a$ in state $s$ | 状态 $s$ 下动作 $a$ 的估计价值 |

$$a^* = \arg\max_{a \in \mathcal{A}} Q(s, a)$$

Always picks the highest-value action — **exploit only, no explore**.

> ⚠️ **Quiz 1 Q8:** "Greedy policy = always take action with highest immediate reward."

### 2.2 Tie-Breaking (平局处理)

When multiple actions share the max Q value, $\arg\max$ is not unique. Common strategies:
- Random among tied actions (most common in RL)
- First occurrence (implementation-dependent)

### 2.3 Worked Example (手算例题)

> 📐 Original Problem — based on Sutton §2.2

$Q(s, \text{left}) = 0.3, Q(s, \text{right}) = 0.8, Q(s, \text{up}) = 0.1$.

$a^* = \arg\max\{0.3, 0.8, 0.1\} = \text{right}$

### 2.4 Practice Problems (练习题)

#### 🟡 Medium | 中等题

**P2.** Q-table row: $Q(s, \text{up})=2.5, Q(s, \text{down})=2.5, Q(s, \text{left})=1.0, Q(s, \text{right})=2.5$. How many valid greedy actions? What would $\varepsilon$-greedy do with $\varepsilon = 0.1$?

> 📐 Original Problem — based on Sutton §2.2
> 💡 **Hint:** Three actions are tied. $\varepsilon$-greedy: with prob $\varepsilon$ random, else greedy.

**Solution:** 3 valid greedy actions (up, down, right — all Q=2.5). With $\varepsilon$-greedy: 10% chance pick uniformly random from all 4 actions; 90% chance pick randomly among the 3 tied greedy actions.

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Argmax | $\arg\max_a f(a)$ = input that maximizes $f$ | Standard math | RL, ML classification |
| Greedy selection | $a^* = \arg\max_a Q(s,a)$ | Sutton §2.2, Eq.2.2 | Q-Learning |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Section | Pages |
| --- | --- | --- | --- |
| §1–2 | Sutton & Barto | §2.2, Eq. 2.2 | p.27 |
