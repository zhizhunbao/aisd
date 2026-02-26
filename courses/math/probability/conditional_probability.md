# Conditional Probability | 条件概率

> **Purpose:** Define conditional probability, product rule, total probability, and independence — the four building blocks for Bayes' theorem and Naive Bayes classification.
> **Primary Source:** MML §6.3 (Deisenroth et al.) + Grinstead §4.1 (Grinstead & Snell)
> **See also:** [bayes_theorem.md](bayes_theorem.md)
> **Prerequisites:** None — this is the starting point for probability.

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |

---

## §1 Conditional Probability Definition (条件概率定义)

> 📚 Source: Grinstead §4.1, p. 143 — Definition 4.1
> 📚 Also: MML §6.3, p. 189; Goodfellow §3.5, Eq. 3.5

### 1.1 Definition (定义)

$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0$

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $P(A \mid B)$ | Probability of A given B | 已知 B 发生时 A 的概率 | $\in [0, 1]$ |
| $P(A \cap B)$ | Joint probability of A and B | A 和 B 同时发生的概率 | $\in [0, 1]$ |
| $P(B)$ | Marginal probability of B | B 发生的（边缘）概率 | $\in (0, 1]$ |

### 1.2 Intuition (直觉理解)

Conditional probability = shrinking the universe. Before observing B, the sample space is Ω (all outcomes). After observing B, the sample space shrinks to B alone. We re-normalize: among outcomes inside B, what fraction also belongs to A?

条件概率 = 缩小宇宙。观察到 B 之前，样本空间是 Ω。观察到 B 之后，样本空间缩小为 B。重新归一化：在 B 里面的结果中，有多少也属于 A？

> 📚 Grinstead §4.1, p. 143 — "restricting the sample space"

### 1.3 Worked Example (手算例题)

> 📚 Adapted from Grinstead §4.1, p. 144

**Problem:** Two fair dice. A = sum is 8, B = first die is 5. Find P(A|B).

两个公平骰子。A = 和为 8，B = 第一个骰子为 5。求 P(A|B)。

**Solution:**

$P(A) = \frac{5}{36}, \quad P(B) = \frac{6}{36} = \frac{1}{6}$

$P(A \cap B) = \frac{1}{36} \quad \text{(only (5,3))}$

$P(A \mid B) = \frac{1/36}{6/36} = \frac{1}{6} \approx 0.167$

> ⚠️ $P(B \mid A) = \frac{1/36}{5/36} = \frac{1}{5} = 0.2 \neq P(A \mid B)$. Conditioning direction matters!
> 条件方向很重要！

> 🔗 **Course Connection:**
> - **ML W5 Naive Bayes:** The entire classifier is built on $P(Y \mid X)$ — posterior given features. Training data gives us $P(X \mid Y)$ (likelihood); Bayes' theorem flips the direction.
> - **ML W5 BBN:** Each node's CPT stores $P(\text{child} \mid \text{parents})$.

### 1.4 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** A bag has 4 red and 6 blue balls. B = "ball is red". A = "ball has a star" (2 of 4 red balls have stars, 1 of 6 blue balls has a star). Find P(A|B).

一个袋子有 4 红 6 蓝球。B = "抽到红球"，A = "球上有星"。求 P(A|B)。

> 📚 Inspired by Grinstead §4.1 urn examples

<details><summary>💡 Hint</summary>

Once you know the ball is red (B), you're only looking at the 4 red balls. How many of those have stars?

</details>

<details><summary>✅ Solution</summary>

$P(B) = 4/10 = 0.4$. $P(A \cap B)$ = red balls with stars = 2/10 = 0.2.

$P(A \mid B) = \frac{0.2}{0.4} = 0.5$

Or directly: given red, 2 out of 4 have stars → 2/4 = 0.5. ✓

</details>

#### 🟡 Medium | 中等题

**P2.** Two urns. Urn I: 2 black + 3 white balls. Urn II: 1 black + 1 white ball. Choose an urn at random (equal probability), then draw a ball. Given that the ball drawn is black, what is the probability it came from Urn I?

两个壶。壶 I：2 黑 + 3 白。壶 II：1 黑 + 1 白。等概率选壶后抽球。已知抽到黑球，求来自壶 I 的概率。

> 📚 From: Grinstead §4.1, pp. 146–148

<details><summary>💡 Hint</summary>

Build a forward probability tree: P(Urn) × P(Black | Urn) for each urn. Then apply Bayes.

</details>

<details><summary>✅ Solution</summary>

$P(I \cap B) = \frac{1}{2} \times \frac{2}{5} = \frac{1}{5}, \quad P(II \cap B) = \frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$

$P(B) = \frac{1}{5} + \frac{1}{4} = \frac{9}{20}$

$P(I \mid B) = \frac{1/5}{9/20} = \frac{4}{9} \approx 0.444$

</details>

#### 🔴 Hard | 挑战题

**P3.** Show that $P(A \mid B) \neq P(B \mid A)$ in general. Then explain: in Naive Bayes, we want $P(Y \mid X)$ but training data gives us $P(X \mid Y)$. Why can't we just use $P(X \mid Y)$ directly? Give a concrete counter-example.

证明一般情况下 $P(A \mid B) \neq P(B \mid A)$。然后解释为什么不能直接用 $P(X \mid Y)$ 分类。

> 📐 Original Problem — based on Grinstead §4.1 + MML §6.3

<details><summary>💡 Hint</summary>

Think of a medical test: P(positive | disease) = 0.99 but P(disease | positive) could be very low if the disease is rare.

</details>

<details><summary>✅ Solution</summary>

**Part 1:** From the product rule: $P(A \mid B) = \frac{P(A \cap B)}{P(B)}$ and $P(B \mid A) = \frac{P(A \cap B)}{P(A)}$. Equal only if $P(A) = P(B)$. ∎

**Part 2:** Disease classification with P(disease) = 0.001:

- $P(\text{cough} \mid \text{disease}) = 0.9$, $P(\text{cough} \mid \text{healthy}) = 0.1$, $P(\text{healthy}) = 0.999$

Likelihood alone: $0.9 > 0.1$ → predict disease.

But Bayes: $P(\text{disease}|\text{cough}) = \frac{0.9 \times 0.001}{0.9 \times 0.001 + 0.1 \times 0.999} = \frac{0.0009}{0.1008} \approx 0.009$

Only 0.9% chance! The prior P(disease) = 0.001 dominates.

</details>

---

## §2 Product Rule & Total Probability (乘法法则与全概率)

> 📚 Source: MML §6.3, p. 189

### 2.1 Product Rule (乘法法则)

$p(x, y) = p(y \mid x) \cdot p(x) = p(x \mid y) \cdot p(y)$

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $p(x, y)$ | Joint distribution | 联合分布 |
| $p(y \mid x)$ | Conditional of Y given X | Y 给定 X 的条件 |
| $p(x)$ | Marginal of X | X 的边缘分布 |

> 🔑 Writing the joint two ways and equating → directly derives Bayes' theorem.
> 把联合分布写成两种形式并令其相等 → 直接推导出贝叶斯定理。

### 2.2 Law of Total Probability (全概率公式)

> 📚 MML §6.3, p. 189; Grinstead §4.1, p. 154

$P(B) = \sum_{i} P(B \mid A_i) \cdot P(A_i)$

where $A_1, \ldots, A_n$ are mutually exclusive, exhaustive events.

> 🔑 This is how we compute the evidence $P(X)$ in Bayes' theorem: sum over all class labels.
> 这就是贝叶斯定理中计算证据 $P(X)$ 的方法：对所有类别标签求和。

> 🔗 **Course Connection:**
> - **ML W5 NB:** Evidence $P(X) = \sum_Y P(X \mid Y) \cdot P(Y)$ — the denominator in Bayes.
> - **ML W5 NB MAP:** MAP drops $P(X)$ because it's the same for all classes.
> - **ML W6 EM:** E-step posterior uses total probability in the denominator.

---

## §3 Independence & Conditional Independence (独立性与条件独立)

> 📚 Source: Grinstead §4.1, pp. 155–158; MML §6.4, p. 192

### 3.1 Definition (定义)

A and B are independent if and only if:

$P(A \cap B) = P(A) \cdot P(B) \quad \Longleftrightarrow \quad P(A \mid B) = P(A)$

Conditional independence given C:

$P(A \cap B \mid C) = P(A \mid C) \cdot P(B \mid C)$

> ⚠️ Pairwise independence ≠ mutual independence. Mutual requires ALL subsets satisfy the product rule.
> 两两独立 ≠ 相互独立。相互独立要求所有子集都满足乘法法则。

> 🔗 **Course Connection:**
> - **ML W5 NB:** The "Naive" assumption: $P(X_1, \ldots, X_d \mid Y) = \prod_{i=1}^{d} P(X_i \mid Y)$ — features are conditionally independent given the class.
> - **ML W5 NB limitations:** Correlated features violate this assumption, making probability estimates inaccurate — though NB often still classifies correctly.

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Conditional prob | $P(A \mid B) = \frac{P(A \cap B)}{P(B)}$ | Grinstead §4.1 | W5 NB posterior |
| Product rule | $p(x,y) = p(y \mid x) \cdot p(x)$ | MML §6.3 | Bayes derivation |
| Total probability | $P(B) = \sum_i P(B \mid A_i) P(A_i)$ | MML §6.3 | W5 NB evidence |
| Independence | $P(A \cap B) = P(A) P(B)$ | Grinstead §4.1 | Coin/dice probs |
| Cond. independence | $P(A \cap B \mid C) = P(A \mid C) P(B \mid C)$ | MML §6.4 | W5 NB assumption |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Section | Pages |
| --- | --- | --- | --- |
| §1 | Grinstead | §4.1, Def. 4.1 | pp. 143–144 |
| §1 | MML | §6.3 | p. 189 |
| §1 | Goodfellow | §3.5, Eq. 3.5 | p. 59 |
| §2 | MML | §6.3, Eq. 6.20–6.22 | pp. 189–191 |
| §2 | Grinstead | §4.1 | p. 154 |
| §3 | Grinstead | §4.1 | pp. 155–158 |
| §3 | MML | §6.4, Def. 6.6 | p. 192 |