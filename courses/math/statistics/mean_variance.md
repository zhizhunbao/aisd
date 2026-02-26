# Mean, Variance & Standard Deviation | 均值、方差、标准差

> **Purpose:** Define expected value, mean, variance, covariance, and correlation — the fundamental summary statistics used in every ML algorithm.
> **Primary Source:** MML §6.4 (Deisenroth et al.)
> **See also:** [gaussian_distribution.md](gaussian_distribution.md)
> **Prerequisites:** None — this is a starting point for statistics.

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^D$ | set of all $D$-dimensional real vectors | $D$ 维实数向量集 |

---

## §1 Expected Value & Mean (期望值与均值)

> 📚 Source: MML §6.4.1, pp. 187–188 — Definition 6.3, 6.4

### 1.1 Definition (定义)

Expected value of a function $g(x)$ of random variable $X$:

$E_X[g(x)] = \int_X g(x) \, p(x) \, dx \quad \text{(continuous)} \qquad E_X[g(x)] = \sum_{x \in \mathcal{X}} g(x) \, p(x) \quad \text{(discrete)}$

> 📚 MML §6.4.1, Eq. 6.28–6.29

Mean = expected value with $g(x) = x$:

$\mu = E_X[x]$

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $E_X[\cdot]$ | expectation operator w.r.t. $X$ | 关于 $X$ 的期望算子 | linear operator |
| $g(x)$ | function of random variable | 随机变量的函数 | $\mathbb{R} \to \mathbb{R}$ |
| $p(x)$ | probability density/mass | 概率密度/质量 | $\geq 0$ |
| $\mu$ | mean (population) | 总体均值 | $\in \mathbb{R}^D$ |

### 1.2 Empirical Mean (样本均值)

> 📚 Source: MML §6.4.2, p. 192 — Definition 6.9

Given $N$ observations $x_1, \ldots, x_N \in \mathbb{R}^D$:

$\bar{x} = \frac{1}{N} \sum_{n=1}^{N} x_n$

### 1.3 Key Property: Linearity (线性性)

> 📚 Source: MML §6.4.1, p. 189 — Eq. 6.34a–6.34d

$E[af(x) + bg(x)] = a \, E[f(x)] + b \, E[g(x)]$

> 🔑 This linearity makes it possible to split $E[(x - \mu)^2]$ into $E[x^2] - (E[x])^2$ (the raw-score formula).
> 这个线性性使得我们可以把 $E[(x - \mu)^2]$ 拆成 $E[x^2] - (E[x])^2$。

> 🔗 **Course Connection:**
> - **ML W1 Preprocessing:** Feature centering subtracts the empirical mean: $x' = x - \bar{x}$
> - **ML W6 K-Means:** Centroid = empirical mean of cluster: $\mathbf{m}_i = \frac{1}{|C_i|} \sum_{\mathbf{x} \in C_i} \mathbf{x}$
> - **ML W6 EM:** M-step updates $\mu_b$ as the weighted mean

---

## §2 Variance & Standard Deviation (方差与标准差)

> 📚 Source: MML §6.4.1, pp. 190–193 — Definition 6.7, Eq. 6.43–6.45

### 2.1 Definition (定义)

Variance = expected squared deviation from the mean:

方差 = 与均值偏差的平方的期望：

$V_X[x] = E_X[(x - \mu)^2]$

Standard deviation = square root of variance:

$\sigma(x) = \sqrt{V_X[x]}$

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $V_X[x]$ or $\sigma^2$ | variance | 方差 | $\geq 0$ |
| $\sigma(x)$ or $\sigma$ | standard deviation | 标准差 | $\geq 0$ |
| $\mu$ | mean | 均值 | $\in \mathbb{R}$ |

### 2.2 Raw-Score Formula (原始分数公式)

> 📚 Source: MML §6.4.3, p. 193 — Eq. 6.44

$V_X[x] = E_X[x^2] - (E_X[x])^2$

"Mean of the square minus the square of the mean."

"平方的均值 减去 均值的平方。"

**Derivation:**

$V[x] = E[(x-\mu)^2] = E[x^2 - 2\mu x + \mu^2] = E[x^2] - 2\mu^2 + \mu^2 = E[x^2] - \mu^2 \quad \blacksquare$

### 2.3 Empirical Variance (样本方差)

> 📚 Source: MML §6.4.2, p. 192 — Definition 6.9, Eq. 6.42

$\hat{\sigma}^2 = \frac{1}{N} \sum_{n=1}^{N} (x_n - \bar{x})^2$

> ⚠️ This is the biased estimate (divides by $N$). The unbiased estimate divides by $N - 1$. MML uses the biased version throughout.
> 这是有偏估计（除以 $N$）。无偏估计除以 $N - 1$。

### 2.4 Pairwise Distance Equivalence (成对距离等价)

> 📚 Source: MML §6.4.3, p. 193 — Eq. 6.45

$\frac{1}{N^2} \sum_{i,j=1}^{N} (x_i - x_j)^2 = 2 \, V[x]$

> 🔑 Sum of $N^2$ pairwise distances = 2 × variance. This explains why K-Means SSE captures the same information as pairwise distances within a cluster.
> $N^2$ 个成对距离之和 = 2 × 方差。这解释了为什么 K-Means SSE 与簇内成对距离包含相同信息。

### 2.5 Worked Example (手算例题)

> 📚 Adapted from MML §6.4.3

**Problem:** Data = {2, 4, 4, 4, 5, 5, 7, 9}. Compute (a) mean, (b) variance, (c) standard deviation.

**Solution:**

**(a) Mean:** $\bar{x} = \frac{40}{8} = 5$

**(b) Variance:** $V = \frac{9+1+1+1+0+0+4+16}{8} = \frac{32}{8} = 4$

**(c) Standard deviation:** $\sigma = \sqrt{4} = 2$

> 🔗 **Course Connection:**
> - **ML W1 Preprocessing:** Standardization: $z = \frac{x - \bar{x}}{\sigma}$
> - **ML W5 NB-Gaussian:** Likelihood per attribute: $P(x_i | Y) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)$
> - **ML W6 EM M-step:** Weighted variance: $\sigma_b^2 = \frac{\sum b_i (x_i - \mu_b)^2}{\sum b_i}$

### 2.6 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Compute the mean and variance of $X = \{1, 3, 5, 7\}$.

计算 $X = \{1, 3, 5, 7\}$ 的均值和方差。

> 📐 Original Problem

<details><summary>💡 Hint</summary>

Mean = sum / count. Variance = average of squared deviations from the mean.

</details>

<details><summary>✅ Solution</summary>

$\bar{x} = \frac{16}{4} = 4$

$V = \frac{9+1+1+9}{4} = \frac{20}{4} = 5$, $\sigma = \sqrt{5} \approx 2.24$

</details>

#### 🟡 Medium | 中等题

**P2.** Prove the raw-score formula: $V[x] = E[x^2] - (E[x])^2$. Then verify numerically using {1, 3, 5, 7}.

证明原始分数公式，然后用 {1, 3, 5, 7} 验证。

> 📚 From: MML §6.4.3, Eq. 6.44

<details><summary>💡 Hint</summary>

Expand $E[(x - \mu)^2]$ using linearity of expectation.

</details>

<details><summary>✅ Solution</summary>

**Proof:** $V[x] = E[(x-\mu)^2] = E[x^2] - 2\mu E[x] + \mu^2 = E[x^2] - \mu^2 \quad \blacksquare$

**Verification:** $E[x^2] = \frac{1+9+25+49}{4} = 21$, $(E[x])^2 = 16$, $V = 21 - 16 = 5$ ✓

</details>

---

## §3 Covariance & Correlation (协方差与相关性)

> 📚 Source: MML §6.4.1, pp. 190–191 — Definition 6.5, 6.8

### 3.1 Covariance (协方差)

$\text{Cov}[x, y] = E[(x - E[x])(y - E[y])] = E[xy] - E[x]E[y]$

> 📚 MML §6.4.1, Eq. 6.35–6.36

- $\text{Cov}[x,y] > 0$: X increases → Y increases (正相关)
- $\text{Cov}[x,y] < 0$: X increases → Y decreases (负相关)
- $\text{Cov}[x,y] = 0$: uncorrelated (不相关) — but NOT necessarily independent

> ⚠️ Zero covariance ≠ independence. Covariance only measures linear dependence.
> 零协方差 ≠ 独立。协方差只衡量线性依赖。

### 3.2 Correlation (相关系数)

> 📚 Source: MML §6.4.1, p. 191 — Definition 6.8

$\text{corr}[x, y] = \frac{\text{Cov}[x, y]}{\sqrt{V[x] \, V[y]}} \in [-1, 1]$

> 🔑 Correlation = normalized covariance = cosine of the angle between random variables (as vectors).
> 相关系数 = 归一化的协方差 = 随机变量（作为向量）之间夹角的余弦。

### 3.3 Affine Transformation Rules (仿射变换规则)

> 📚 Source: MML §6.4.4, p. 194 — Eq. 6.50–6.51

For $\mathbf{y} = A\mathbf{x} + \mathbf{b}$:

$E[\mathbf{y}] = A\boldsymbol{\mu} + \mathbf{b}, \qquad V[\mathbf{y}] = A \Sigma A^\top$

> 🔗 **Course Connection:**
> - **ML W1 Preprocessing:** Covariance matrix reveals feature correlations
> - **ML W6 EM:** Covariance matrix $\Sigma$ is a parameter of each Gaussian component in GMM
> - **PCA:** Eigenvalues of the covariance matrix give the variance along principal components

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Mean | $\mu = E[x]$ | MML §6.4.1, Def. 6.4 | All algorithms |
| Empirical mean | $\bar{x} = \frac{1}{N}\sum x_n$ | MML §6.4.2, Eq. 6.41 | K-Means centroid |
| Variance | $V[x] = E[(x-\mu)^2]$ | MML §6.4.1, Eq. 6.43 | NB-Gaussian, EM |
| Raw-score | $V[x] = E[x^2] - (E[x])^2$ | MML §6.4.3, Eq. 6.44 | Bias-variance decomp. |
| Std deviation | $\sigma = \sqrt{V[x]}$ | MML §6.4.1, p. 190 | Standardization |
| Covariance | $\text{Cov}[x,y] = E[xy]-E[x]E[y]$ | MML §6.4.1, Eq. 6.36 | PCA, GMM |
| Correlation | $\frac{\text{Cov}[x,y]}{\sigma_x \sigma_y}$ | MML §6.4.1, Eq. 6.40 | Feature analysis |
| Affine mean | $E[Ax+b] = A\mu + b$ | MML §6.4.4, Eq. 6.50 | Linear regression |
| Affine var | $V[Ax+b] = A\Sigma A^\top$ | MML §6.4.4, Eq. 6.51 | PCA |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation | Pages |
| --- | --- | --- | --- |
| §1 | MML | §6.4.1, Def. 6.3–6.4, Eq. 6.28–6.32 | pp. 187–188 |
| §1 | MML | §6.4.2, Def. 6.9, Eq. 6.41 | p. 192 |
| §2 | MML | §6.4.1, Def. 6.7, Eq. 6.38–6.43 | pp. 190–193 |
| §2 | MML | §6.4.3, Eq. 6.44–6.45 | p. 193 |
| §3 | MML | §6.4.1, Def. 6.5–6.8, Eq. 6.35–6.40 | pp. 190–191 |
| §3 | MML | §6.4.4, Eq. 6.50–6.51 | p. 194 |