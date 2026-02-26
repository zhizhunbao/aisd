# Bayes' Theorem | 贝叶斯定理

> **Purpose:** Derive Bayes' theorem from the product rule, define prior/likelihood/posterior/evidence, and introduce the MAP decision rule — the mathematical core of Naive Bayes classification.
> **Primary Source:** MML §6.3 (Deisenroth et al.) + Grinstead §4.1 (Grinstead & Snell)
> **See also:** [conditional_probability.md](conditional_probability.md) (prerequisite)
> **Prerequisites:** [conditional_probability.md](conditional_probability.md) — product rule and total probability

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |

---

## §1 Derivation from Product Rule (从乘法法则推导)

> 📚 Source: MML §6.3, p. 189; Goodfellow §3.11, Eq. 3.42

### 1.1 Derivation (推导)

The product rule gives two ways to write the joint distribution:

$p(x, y) = p(y \mid x) \cdot p(x) \quad \text{...(1)}$

$p(x, y) = p(x \mid y) \cdot p(y) \quad \text{...(2)}$

Equate (1) = (2) and solve for $p(x \mid y)$:

$\boxed{p(x \mid y) = \frac{p(y \mid x) \cdot p(x)}{p(y)}}$

| Symbol | Name (EN) | 名称 (中文) | Role |
| --- | --- | --- | --- |
| $p(x \mid y)$ | Posterior | 后验概率 | What we want — belief about $x$ after seeing $y$ |
| $p(y \mid x)$ | Likelihood | 似然 | How probable is data $y$ if $x$ is true |
| $p(x)$ | Prior | 先验概率 | Belief about $x$ before seeing any data |
| $p(y)$ | Evidence | 证据 / 归一化 | Total probability of $y$ — ensures posterior sums to 1 |

### 1.2 Intuition (直觉理解)

Bayes' theorem flips the direction of conditioning.

贝叶斯定理翻转条件方向。

- Forward: Given the cause, predict the effect → $P(\text{symptoms} \mid \text{disease})$ — easy to estimate from data
- Reverse: Given the effect, infer the cause → $P(\text{disease} \mid \text{symptoms})$ — what we actually want

正向：给定原因，预测结果。反向：给定结果，推断原因。

> 🔑 Posterior ∝ Likelihood × Prior / 后验 ∝ 似然 × 先验

### 1.3 Worked Example (手算例题)

> 📚 Adapted from Grinstead §4.1, pp. 161–163

**Problem:** A disease affects 1% of the population. A test has 95% sensitivity and 90% specificity. A patient tests positive. What is P(disease | positive)?

一种病影响 1% 人口。检测灵敏度 95%，特异度 90%。患者检测阳性，求 P(有病 | 阳性)。

**Solution:**

$P(D) = 0.01, \quad P(\neg D) = 0.99$

$P(+ \mid D) = 0.95, \quad P(+ \mid \neg D) = 0.10$

$P(+) = 0.95 \times 0.01 + 0.10 \times 0.99 = 0.0095 + 0.099 = 0.1085$

$P(D \mid +) = \frac{0.95 \times 0.01}{0.1085} = \frac{0.0095}{0.1085} \approx 0.088$

> ⚠️ Despite a 95% accurate test, P(disease | positive) is only 8.8%! The low prior P(D) = 0.01 dominates. This is the base rate fallacy.
> 尽管检测准确率 95%，P(有病 | 阳性) 只有 8.8%！低先验起主导作用。这就是基率谬误。

> 🔗 **Course Connection:**
> - **ML W5 NB:** $P(Y \mid X) = \frac{P(X \mid Y) \cdot P(Y)}{P(X)}$ — the entire Naive Bayes classifier is this formula with conditional independence.
> - **ML W5 BBN:** Each node uses Bayes to update belief given parent values.

---

## §2 MAP Decision Rule (MAP 决策规则)

> 📚 Source: MML §6.3, p. 189

### 2.1 Definition (定义)

Since evidence $P(X)$ is the same for all classes, classification only needs:

因为证据 $P(X)$ 对所有类别相同，分类只需要：

$\hat{y} = \arg\max_Y \; P(Y \mid X) = \arg\max_Y \; P(X \mid Y) \cdot P(Y)$

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\hat{y}$ | Predicted class label | 预测的类别标签 |
| $\arg\max_Y$ | The $Y$ value that maximizes | 使表达式最大的 $Y$ 值 |
| $P(X \mid Y)$ | Likelihood | 似然 |
| $P(Y)$ | Prior | 先验 |

> 🔑 Why drop $P(X)$? Because $P(X)$ doesn't depend on $Y$ — same denominator for every class. Dropping it doesn't change which class wins.
> 为什么丢掉 $P(X)$？因为它不依赖于 $Y$——对每个类别都是相同的分母。

### 2.2 When You CANNOT Drop Evidence (不能丢掉证据的情况)

MAP gives the winning class but NOT the probability value. If you need $P(Y \mid X)$ as a calibrated probability (e.g., "73% chance this is spam"), you MUST compute $P(X)$ via total probability.

MAP 给出最佳类别但不是概率值。如果需要校准概率，就必须用全概率公式算 $P(X)$。

> 🔗 **Course Connection:**
> - **ML W5 NB:** MAP is the standard NB decision rule.
> - **ML W5 NB + Laplace:** When $P(X_i \mid Y) = 0$, the entire product dies → Laplace smoothing fixes this.
> - **ML W6 EM:** E-step computes full posterior (not MAP) because soft assignments need actual probability values.

---

## §3 General Form for Multiple Hypotheses (多假设通用形式)

> 📚 Source: Grinstead §4.1, pp. 161–163

### 3.1 Formula (公式)

Given mutually exclusive, exhaustive hypotheses $H_1, \ldots, H_m$ and evidence $E$:

$P(H_i \mid E) = \frac{P(H_i) \cdot P(E \mid H_i)}{\sum_{k=1}^{m} P(H_k) \cdot P(E \mid H_k)}$

This is exactly Naive Bayes with $m$ classes.

这就是 $m$ 类的朴素贝叶斯。

### 3.2 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** A factory has 3 machines. Machine A produces 50% of items (2% defective), B produces 30% (3% defective), C produces 20% (5% defective). An item is found defective. Which machine most likely produced it?

工厂有 3 台机器。A 生产 50%（2% 次品），B 生产 30%（3% 次品），C 生产 20%（5% 次品）。发现一个次品，最可能来自哪台机器？

> 📐 Original Problem

<details><summary>💡 Hint</summary>

Compute $P(\text{Machine}_i) \times P(\text{defective} \mid \text{Machine}_i)$ for each machine. MAP answer = highest product.

</details>

<details><summary>✅ Solution</summary>

$P(A) \times P(D \mid A) = 0.50 \times 0.02 = 0.010$

$P(B) \times P(D \mid B) = 0.30 \times 0.03 = 0.009$

$P(C) \times P(D \mid C) = 0.20 \times 0.05 = 0.010$

MAP: Tie between A and C (both 0.010).

Full posterior: $P(D) = 0.029$

$P(A \mid D) = 34.5\%$, $P(B \mid D) = 31.0\%$, $P(C \mid D) = 34.5\%$

</details>

#### 🟡 Medium | 中等题

**P2.** Two fair dice. You observe that the sum is 8. Compute the posterior probability distribution over the value of the first die.

两个骰子，已知和为 8。计算第一个骰子值的后验分布。

> 📐 Original Problem — extends Grinstead §4.1 dice example

<details><summary>💡 Hint</summary>

List all outcomes where sum = 8: (2,6), (3,5), (4,4), (5,3), (6,2). Each has equal probability 1/36.

</details>

<details><summary>✅ Solution</summary>

Outcomes with sum=8: {(2,6), (3,5), (4,4), (5,3), (6,2)}. $P(\text{sum}=8) = 5/36$.

For $k \in \{2,3,4,5,6\}$: $P(\text{first}=k \mid \text{sum}=8) = \frac{(1/6)(1/6)}{5/36} = \frac{1}{5}$

$P(\text{first}=1 \mid \text{sum}=8) = 0$

Posterior is uniform over {2,3,4,5,6}, each with probability 1/5.

</details>

#### 🔴 Hard | 挑战题

**P3.** Derive Bayes' theorem from the product rule (show all steps). Then explain: why does Naive Bayes replace $P(X \mid Y)$ with $\prod_{i=1}^d P(X_i \mid Y)$? What breaks when this assumption is violated?

从乘法法则推导贝叶斯定理。然后解释朴素贝叶斯的条件独立假设及其违反时的后果。

> 📚 From: MML §6.3 + Grinstead §4.1

<details><summary>💡 Hint</summary>

Part 1: Write $p(x,y)$ two ways, equate, solve. Part 2: Think about correlated features like height/weight.

</details>

<details><summary>✅ Solution</summary>

**Part 1 — Derivation:**

Step 1: $p(x,y) = p(y \mid x) \cdot p(x)$

Step 2: $p(x,y) = p(x \mid y) \cdot p(y)$

Step 3: Equate → $p(x \mid y) = \frac{p(y \mid x) \cdot p(x)}{p(y)}$ ∎

**Part 2 — Conditional Independence:**

The assumption: $P(X_1, \ldots, X_d \mid Y) = \prod_{i=1}^d P(X_i \mid Y)$

Without it, estimating $P(X_1, \ldots, X_d \mid Y)$ requires a table of size $|X_1| \times \cdots \times |X_d|$ per class — exponentially many entries.

Breaking example: $X_1$ = height, $X_2$ = shoe size. These are correlated. NB treats them as independent, overestimating joint probabilities for rare combinations. With more features, errors compound and can flip classification.

</details>

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Bayes' theorem | $p(x \mid y) = \frac{p(y \mid x) \cdot p(x)}{p(y)}$ | MML §6.3 | W5 NB core |
| Evidence | $P(y) = \sum_x P(y \mid x) P(x)$ | MML §6.3 | W5 NB denominator |
| MAP rule | $\hat{y} = \arg\max_Y P(X \mid Y) P(Y)$ | MML §6.3 | W5 NB classification |
| Multi-hypothesis | $P(H_i \mid E) = \frac{P(H_i) P(E \mid H_i)}{\sum_k P(H_k) P(E \mid H_k)}$ | Grinstead §4.1 | W5 NB multi-class |
| NB factorization | $P(X \mid Y) = \prod_i P(X_i \mid Y)$ | MML §6.4 | W5 NB assumption |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Section | Pages |
| --- | --- | --- | --- |
| §1 | MML | §6.3 | p. 189 |
| §1 | Goodfellow | §3.11, Eq. 3.42 | p. 70 |
| §1 | Grinstead | §4.1 | pp. 146–148 |
| §2 | MML | §6.3 | p. 189 |
| §3 | Grinstead | §4.1 | pp. 161–163 |