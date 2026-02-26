# Gaussian Distribution | 高斯分布

> **Purpose:** Define the Gaussian (Normal) PDF, explain its parameters μ and σ², and show how it is used as the likelihood function in Gaussian Naive Bayes and EM algorithm.
> **Primary Source:** MML §6.5 (Deisenroth et al.), Eq. 6.62–6.63
> **See also:** [mean_variance.md](mean_variance.md) | [mle.md](mle.md) | [bayes_theorem.md](../probability/bayes_theorem.md)
> **Prerequisites:** [conditional_probability.md](../probability/conditional_probability.md), [bayes_theorem.md](../probability/bayes_theorem.md)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |

---

## §1 Univariate Gaussian PDF (一维高斯概率密度函数)

> 📚 Source: MML §6.5, p. 198, Eq. 6.62

### 1.1 Definition (定义)

$p(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$

| Symbol | Meaning (EN) | 含义 (中文) | Type / Range |
| --- | --- | --- | --- |
| $x$ | Data point | 数据点 | $x \in \mathbb{R}$ |
| $\mu$ | Mean (center of bell) | 均值（钟形曲线中心） | $\mu \in \mathbb{R}$ |
| $\sigma^2$ | Variance (spread) | 方差（分散程度） | $\sigma^2 > 0$ |
| $\sigma$ | Standard deviation | 标准差 | $\sigma > 0$ |
| $\frac{1}{\sqrt{2\pi\sigma^2}}$ | Normalization constant | 归一化常数 | Ensures $\int p(x)dx = 1$ |

Shorthand: $X \sim \mathcal{N}(\mu, \sigma^2)$

### 1.2 Intuition (直觉理解)

The Gaussian is a bell curve: peak at μ, width controlled by σ.

高斯分布是钟形曲线：峰值在 μ，宽度由 σ 控制。

68-95-99.7 Rule: ~68% within $[\mu - \sigma, \mu + \sigma]$, ~95% within $[\mu - 2\sigma, \mu + 2\sigma]$, ~99.7% within $[\mu - 3\sigma, \mu + 3\sigma]$.

> 🔑 Why Gaussian for ML? (1) Central Limit Theorem — sums of many small effects → Gaussian. (2) Maximum entropy among distributions with given mean and variance. (3) Mathematically convenient — products and marginals of Gaussians are also Gaussian.
> 为什么 ML 用高斯？(1) 中心极限定理 (2) 给定均值方差下最大熵 (3) 数学上方便。

### 1.3 Worked Example (手算例题)

> 📚 Adapted from MML §6.5, applied to Week 5 NB gender example

**Problem:** In Gaussian NB, class "Male" has height μ=5.85, σ²=0.035. Compute P(height=5.0 | Male).

GaussianNB 中，"男性"类身高 μ=5.85, σ²=0.035。计算 P(height=5.0 | Male)。

**Solution:**

$(5.0 - 5.85)^2 = 0.7225$, exponent $= -0.7225/0.070 = -10.321$

Normalization: $\frac{1}{\sqrt{2\pi \times 0.035}} = 2.132$

$p = 2.132 \times \exp(-10.321) \approx 7.01 \times 10^{-5}$

> 🔑 This tiny value is fine — it's a density, not a probability. What matters in NB is the ratio between classes.
> 这个极小值没问题——它是密度，不是概率。NB 中重要的是类别之间的比值。

> 🔗 **Course Connection:**
> - **ML W5 GaussianNB:** $P(X_i \mid Y)$ for continuous features uses this exact PDF.
> - **ML W5 Lab4:** Gender classification uses Gaussian PDF for height, weight, foot size.
> - **ML W6 EM:** Each Gaussian component uses this PDF in the E-step likelihood computation.

### 1.4 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Given $\mu = 0, \sigma^2 = 1$ (standard normal), compute $p(x=0)$ and $p(x=2)$. Which is larger and by what factor?

标准正态分布，计算 $p(x=0)$ 和 $p(x=2)$，哪个更大，大多少倍？

> 📚 From: MML §6.5, Eq. 6.62

<details><summary>💡 Hint</summary>

For $x=0$: exponent is 0, so $\exp(0) = 1$. For $x=2$: $(2-0)^2 / (2 \times 1) = 2$.

</details>

<details><summary>✅ Solution</summary>

$p(0) = \frac{1}{\sqrt{2\pi}} \approx 0.3989$

$p(2) = \frac{1}{\sqrt{2\pi}} \exp(-2) \approx 0.0540$

Ratio: $p(0) / p(2) \approx 7.39$ — the peak is ~7.4× higher than 2σ away.

</details>

#### 🟡 Medium | 中等题

**P2.** GaussianNB with 2 classes: Male $\mu_M=5.85, \sigma^2_M=0.035$ and Female $\mu_F=5.42, \sigma^2_F=0.097$. For height=5.5, compute $P(h=5.5 \mid M)$ and $P(h=5.5 \mid F)$. Which class does this feature favor?

GaussianNB 两类，身高=5.5，计算各类的似然，哪个类更高？

> 📐 Original Problem — based on ML W5 Lab4

<details><summary>💡 Hint</summary>

Compute the Gaussian PDF for each class separately.

</details>

<details><summary>✅ Solution</summary>

**Male:** $(5.5-5.85)^2 = 0.1225$, exponent $= -1.75$, $p \approx 0.371$

**Female:** $(5.5-5.42)^2 = 0.0064$, exponent $= -0.033$, $p \approx 1.239$

$P(h=5.5 \mid F) > P(h=5.5 \mid M)$ → favors Female (height 5.5 is closer to female mean 5.42).

Note: $p > 1$ for Female is fine — density can exceed 1.

</details>

#### 🔴 Hard | 挑战题

**P3.** EM E-step: two Gaussian clusters $a: \mu_a=2, \sigma^2_a=1, P(a)=0.6$ and $b: \mu_b=5, \sigma^2_b=1, P(b)=0.4$. For $x=3.5$, compute $P(b \mid x=3.5)$.

EM 的 E-step。两个高斯簇，对 $x=3.5$ 计算软分配。

> 📐 Original Problem — combines MML §6.5 with W6 EM

<details><summary>💡 Hint</summary>

Compute Gaussian PDF for each cluster at $x=3.5$, multiply by mixing weight, then normalize.

</details>

<details><summary>✅ Solution</summary>

Both likelihoods are identical ($|3.5-2| = |3.5-5| = 1.5$, same variance):

$P(x \mid a) = P(x \mid b) = 0.1295$

Weighted: $0.1295 \times 0.6 = 0.0777$, $0.1295 \times 0.4 = 0.0518$

$P(b \mid x=3.5) = \frac{0.0518}{0.1295} = 0.400$, $P(a \mid x=3.5) = 0.600$

Despite being equidistant from both means, $x=3.5$ is assigned 60% to cluster $a$ because $P(a) = 0.6 > P(b) = 0.4$. The prior breaks the tie.

</details>

---

## §2 Gaussian Mixture (高斯混合) — EM Connection

> 📚 Source: MML §6.5, p. 202, Theorem 6.12

### 2.1 Mixture PDF (混合概率密度)

$p(x) = \sum_{k=1}^{K} \pi_k \cdot \mathcal{N}(x \mid \mu_k, \sigma_k^2)$

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $K$ | Number of components | 分量数量 |
| $\pi_k$ | Mixing weight for component $k$ | 分量 $k$ 的混合权重 |
| $\mu_k$ | Mean of component $k$ | 分量 $k$ 的均值 |
| $\sigma_k^2$ | Variance of component $k$ | 分量 $k$ 的方差 |

Constraint: $\sum_{k=1}^K \pi_k = 1$ and $\pi_k > 0$.

> 🔗 **Course Connection:**
> - **ML W6 EM:** The entire EM algorithm fits a GMM. E-step uses Bayes for $P(k \mid x_i)$; M-step updates $\mu_k, \sigma_k^2, \pi_k$.
> - **ML W6 Soft K-Means:** GMM is "soft K-Means" — fractional membership instead of hard assignment.

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Univariate PDF | $\frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$ | MML §6.5 Eq.6.62 | W5 GaussianNB |
| Standard Normal | $\mathcal{N}(0, 1)$ | MML §6.5 | Reference baseline |
| 68-95-99.7 Rule | 68% in $\pm 1\sigma$, 95% in $\pm 2\sigma$, 99.7% in $\pm 3\sigma$ | — | Data interpretation |
| Gaussian Mixture | $\sum_k \pi_k \mathcal{N}(x \mid \mu_k, \sigma_k^2)$ | MML §6.5 Eq.6.80 | W6 EM / GMM |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation | Pages |
| --- | --- | --- | --- |
| §1 | MML | §6.5, Eq. 6.62 | p. 198 |
| §1 | MML | §6.5 (CLT motivation) | p. 197 |
| §2 | MML | §6.5, Theorem 6.12, Eq. 6.80 | p. 202 |