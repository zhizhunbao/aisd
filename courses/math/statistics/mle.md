# Maximum Likelihood Estimation | 最大似然估计

> **Purpose:** Define MLE as the method to estimate parameters (μ, σ², class priors, feature likelihoods) from training data — the parameter learning engine behind Naive Bayes and EM.
> **Primary Source:** Barber §10.2 (Barber, Bayesian Reasoning and ML) + MML §8.3 (Deisenroth et al.)
> **See also:** [gaussian_distribution.md](../statistics/gaussian_distribution.md) | [bayes_theorem.md](../probability/bayes_theorem.md) | [week5_naivebayes_math.md](../../ml/notes/week5_naivebayes_math.md)
> **Prerequisites:** [bayes_theorem.md](../probability/bayes_theorem.md), [gaussian_distribution.md](../statistics/gaussian_distribution.md)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |

---

## §1 MLE Principle (最大似然原理)

> 📚 Source: MML §8.3, pp. 271–274 — Parameter Estimation
> 📚 Also: Barber §10.2, p. 204 — ML for Naive Bayes

### 1.1 Definition

Given observed data $\mathcal{D} = \{x_1, \ldots, x_N\}$ and a model with parameters $\theta$:

$$\hat{\theta}_{\text{MLE}} = \arg\max_\theta \; P(\mathcal{D} \mid \theta) = \arg\max_\theta \; \prod_{n=1}^{N} P(x_n \mid \theta)$$

| Symbol                       | Meaning (EN)                    | 含义 (中文)          |
| ---------------------------- | ------------------------------- | -------------------- |
| $\hat{\theta}_{\text{MLE}}$  | MLE estimate of parameters      | 参数的最大似然估计   |
| $\mathcal{D}$                | Observed training data          | 观测到的训练数据     |
| $P(\mathcal{D} \mid \theta)$ | Likelihood of data given params | 给定参数时数据的似然 |
| $\prod_{n=1}^{N}$            | Product over all data points    | 所有数据点的乘积     |

> 🔑 **i.i.d. assumption:** Data points are independently and identically distributed, so the joint likelihood factors into a product. This is the same independence structure Naive Bayes uses.

### 1.2 Log-Likelihood Trick (对数似然技巧)

> 📚 Barber §10.2, Eq. 10.2.2–10.2.3

Since $\log$ is monotonically increasing, maximizing the log-likelihood gives the same $\hat{\theta}$:

$$\hat{\theta}_{\text{MLE}} = \arg\max_\theta \; \sum_{n=1}^{N} \log P(x_n \mid \theta)$$

> 🔑 **Why log?** (1) Products become sums — easier to differentiate. (2) Avoids numerical underflow from multiplying many small probabilities. (3) In Week 5, this is why NB can use $\sum \log P(X_i \mid Y)$ instead of $\prod P(X_i \mid Y)$.

### 1.3 Intuition (直觉理解)

MLE asks: **"Which parameters make the observed data most probable?"**

最大似然问的是：**"什么参数让观测到的数据最有可能出现？"**

It's like a detective reasoning backwards: given the evidence (data), which suspect (parameter) best explains what we see?

---

## §2 MLE for Categorical Features (分类特征的 MLE)

> 📚 Source: Barber §10.2, Eq. 10.2.5–10.2.7

### 2.1 Class Prior (类别先验)

> 📚 Barber §10.2, Eq. 10.2.7

$$\hat{P}(Y = c) = \frac{\text{number of samples in class } c}{N} = \frac{n_c}{N}$$

### 2.2 Categorical Feature Likelihood (分类特征似然)

> 📚 Barber §10.2, Eq. 10.2.5–10.2.6

$$\hat{P}(X_i = v \mid Y = c) = \frac{\text{count of } X_i = v \text{ in class } c}{\text{total samples in class } c} = \frac{n_{v,c}}{n_c}$$

> 🔑 **MLE = counting.** For categorical features, MLE just counts frequencies. No calculus needed!

### 2.3 Connection to Course (课程关联)

> 🔗 **Course Connection:**
>
> - **ML W5 NB:** $P(\text{Refund=No} \mid \text{Evade=No}) = 4/7$ — this IS MLE applied.
> - **ML W5 Laplace:** When $n_{v,c} = 0$, MLE gives $P = 0$ → the entire product dies. Laplace adds pseudocounts: $\frac{n_{v,c} + 1}{n_c + V}$.
> - **Barber §10.2:** MLE with sparse data gives "extremely confident" zero probabilities — a known pitfall.

---

## §3 MLE for Gaussian Parameters (高斯参数的 MLE)

> 📚 Source: MML §8.3, pp. 271–275 — MLE for Gaussian; derived from Eq. 6.62

### 3.1 Derivation (推导)

Given $N$ data points $\{x_1, \ldots, x_N\}$ from class $c$, assumed $\sim \mathcal{N}(\mu, \sigma^2)$:

**Log-likelihood:**

$$\ell(\mu, \sigma^2) = \sum_{n=1}^{N} \log \mathcal{N}(x_n \mid \mu, \sigma^2) = -\frac{N}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{n=1}^{N}(x_n - \mu)^2$$

**Set $\frac{\partial \ell}{\partial \mu} = 0$:**

$$\hat{\mu}_{\text{MLE}} = \frac{1}{N}\sum_{n=1}^N x_n = \bar{x}$$

**Set $\frac{\partial \ell}{\partial \sigma^2} = 0$:**

$$\hat{\sigma}^2_{\text{MLE}} = \frac{1}{N}\sum_{n=1}^N (x_n - \hat{\mu})^2$$

| Symbol                        | Meaning (EN)          | 含义 (中文)     | Note                     |
| ----------------------------- | --------------------- | --------------- | ------------------------ |
| $\hat{\mu}_{\text{MLE}}$      | MLE mean estimate     | 均值的 MLE 估计 | = sample mean 样本均值   |
| $\hat{\sigma}^2_{\text{MLE}}$ | MLE variance estimate | 方差的 MLE 估计 | Divide by $N$, not $N-1$ |

> ⚠️ **MLE variance divides by $N$, not $N-1$.** The $N-1$ version (ddof=1) is the **unbiased** estimate. In Week 5 Lab4, code uses `ddof=1` (sample variance) — this is a correction for small samples, not pure MLE.

### 3.2 Worked Example (手算例题)

> 📚 Adapted from Barber §10.2 + ML W5 Lab4 data structure

**Problem:** Class "Male" heights: {6.0, 5.9, 5.7, 5.8}. Compute MLE for $\mu$ and $\sigma^2$.

**Solution:**

**Step 1: Mean**
$$\hat{\mu} = \frac{6.0 + 5.9 + 5.7 + 5.8}{4} = \frac{23.4}{4} = \mathbf{5.85}$$

**Step 2: Variance (MLE, dividing by N)**
$$\hat{\sigma}^2 = \frac{(6.0-5.85)^2 + (5.9-5.85)^2 + (5.7-5.85)^2 + (5.8-5.85)^2}{4}$$

$$= \frac{0.0225 + 0.0025 + 0.0225 + 0.0025}{4} = \frac{0.05}{4} = \mathbf{0.0125}$$

**Step 3: Compare with sample variance (ddof=1)**
$$s^2 = \frac{0.05}{3} = \mathbf{0.0167}$$

> 💡 Lab4 uses ddof=1 → $s^2 = 0.0167$. Pure MLE → $\hat{\sigma}^2 = 0.0125$. Difference is small for large $N$ but matters for $N=4$.

### 3.3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** A dataset of 20 emails: 12 spam, 8 not-spam. Among spam emails, the word "free" appears in 9 of them. Compute $\hat{P}(\text{spam})$ and $\hat{P}(\text{``free''} \mid \text{spam})$ using MLE.
20 封邮件：12 垃圾，8 正常。垃圾邮件中 9 封含 "free"。用 MLE 计算 $\hat{P}(\text{spam})$ 和 $\hat{P}(\text{``free''} \mid \text{spam})$。

> 📚 From: 📐 Original Problem — applies Barber §10.2 Eq. 10.2.6–10.2.7

<details><summary>💡 Hint / 提示</summary>

MLE for categorical = counting. $\hat{P}(\text{class}) = n_c / N$, $\hat{P}(\text{feature} \mid \text{class}) = n_{v,c} / n_c$.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Method: Barber §10.2, Eq. 10.2.6–10.2.7

$$\hat{P}(\text{spam}) = \frac{12}{20} = \mathbf{0.6}$$

$$\hat{P}(\text{``free''} \mid \text{spam}) = \frac{9}{12} = \mathbf{0.75}$$

</details>

#### 🟡 Medium | 中等题

**P2.** Given 5 data points from one class: {2, 4, 6, 8, 10}. (a) Compute MLE estimates $\hat{\mu}$ and $\hat{\sigma}^2$ (divide by N). (b) Compute the Gaussian PDF value $P(x=7 \mid \hat{\mu}, \hat{\sigma}^2)$. (c) Explain why this value alone is NOT a probability.
5 个数据 {2,4,6,8,10}。(a) 计算 MLE 的 $\hat{\mu}$ 和 $\hat{\sigma}^2$。(b) 计算 $P(x=7)$。(c) 解释为什么这个值不是概率。

> 📚 From: 📐 Original Problem — MML §8.3 MLE + §6.5 Gaussian PDF

<details><summary>💡 Hint / 提示</summary>

(a) Mean = average; variance = average of squared deviations. (b) Substitute into Gaussian PDF. (c) Think about PDF vs PMF — density can exceed 1.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Method: MML §8.3 (MLE) + §6.5 Eq. 6.62 (Gaussian PDF)

**(a)** $\hat{\mu} = (2+4+6+8+10)/5 = 30/5 = \mathbf{6}$

$\hat{\sigma}^2 = \frac{(2-6)^2 + (4-6)^2 + (6-6)^2 + (8-6)^2 + (10-6)^2}{5} = \frac{16+4+0+4+16}{5} = \frac{40}{5} = \mathbf{8}$

**(b)** $P(x=7) = \frac{1}{\sqrt{2\pi(8)}} \exp\!\left(-\frac{(7-6)^2}{2(8)}\right) = \frac{1}{\sqrt{50.27}} \exp(-0.0625)$

$= \frac{1}{7.09} \times 0.9394 = \mathbf{0.1325}$

**(c)** This is a **density**, not a probability. For continuous distributions, $P(X = \text{exact value}) = 0$. The density tells us the relative likelihood of values near $x=7$. Only an interval integral $\int_a^b p(x)dx$ gives a probability. Densities CAN exceed 1 (e.g., narrow Gaussians with small σ).

</details>

#### 🔴 Hard | 挑战题

**P3.** Derive why MLE mean = sample mean for a Gaussian. Start from the log-likelihood, take the derivative w.r.t. $\mu$, set to 0, and solve. Then: the EM M-step updates $\mu_k$ with a **weighted** mean: $\hat{\mu}_k = \frac{\sum_i r_{ik} x_i}{\sum_i r_{ik}}$. Explain how this is a generalization of MLE where each data point has fractional ownership $r_{ik}$ instead of hard assignment.
推导为什么高斯 MLE 均值 = 样本均值。从对数似然开始推导。然后：EM M-step 用加权均值更新 $\mu_k$，解释这如何是 MLE 的推广。

> 📚 From: MML §8.3 MLE derivation + MML §11.2 EM M-step

<details><summary>💡 Hint / 提示</summary>

The log-likelihood is $-\frac{1}{2\sigma^2}\sum(x_n - \mu)^2 + \text{const}$. Differentiate w.r.t. μ; the derivative of $(x_n - \mu)^2$ is $-2(x_n - \mu)$.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Derivation: MML §8.3, pp. 271–274

**MLE Derivation:**

**Step 1:** Log-likelihood (keeping only μ-dependent terms):

$$\ell(\mu) = -\frac{1}{2\sigma^2}\sum_{n=1}^{N}(x_n - \mu)^2 + \text{const}$$

**Step 2:** Differentiate w.r.t. μ:

$$\frac{\partial \ell}{\partial \mu} = \frac{1}{\sigma^2}\sum_{n=1}^{N}(x_n - \mu) = \frac{1}{\sigma^2}\left(\sum_{n=1}^N x_n - N\mu\right)$$

**Step 3:** Set to 0 and solve:

$$\sum_{n=1}^N x_n - N\mu = 0 \implies \hat{\mu} = \frac{1}{N}\sum_{n=1}^N x_n = \bar{x} \quad \text{∎}$$

**EM Generalization:**

In hard assignment (K-Means / NB), each point belongs to exactly one cluster: $r_{ik} \in \{0, 1\}$. Then:

$$\hat{\mu}_k = \frac{\sum_i r_{ik} x_i}{\sum_i r_{ik}} = \frac{\sum_{x_i \in C_k} x_i}{|C_k|} = \text{regular mean}$$

In soft assignment (EM), $r_{ik} = P(k \mid x_i) \in [0,1]$. Each point contributes fractionally to every cluster. The update $\hat{\mu}_k = \frac{\sum_i r_{ik} x_i}{\sum_i r_{ik}}$ is the **responsibility-weighted MLE** — a natural generalization where counting is replaced by fractional counting.

> 📚 Source: MML §11.2, pp. 356–365 — EM Parameter Learning via Maximum Likelihood

</details>

---

## Quick Reference (速查表)

| Concept           | Formula                                                     | Source         | Used In           |
| ----------------- | ----------------------------------------------------------- | -------------- | ----------------- |
| MLE principle     | $\hat{\theta} = \arg\max_\theta P(\mathcal{D} \mid \theta)$ | MML §8.3       | All ML training   |
| Log-likelihood    | $\max \sum_n \log P(x_n \mid \theta)$                       | Barber §10.2   | NB, EM            |
| Class prior MLE   | $\hat{P}(c) = n_c / N$                                      | Barber §10.2.7 | W5 NB prior       |
| Categorical MLE   | $\hat{P}(v \mid c) = n_{v,c} / n_c$                         | Barber §10.2.6 | W5 NB categorical |
| Gaussian mean MLE | $\hat{\mu} = \bar{x}$                                       | MML §8.3       | W5 GaussianNB     |
| Gaussian var MLE  | $\hat{\sigma}^2 = \frac{1}{N}\sum(x_n - \bar{x})^2$         | MML §8.3       | W5 GaussianNB     |
| EM weighted MLE   | $\hat{\mu}_k = \frac{\sum r_{ik} x_i}{\sum r_{ik}}$         | MML §11.2      | W6 EM M-step      |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation    | Pages       |
| ------- | -------- | ------------------- | ----------- |
| §1      | MML      | §8.3                | pp. 271–274 |
| §1      | Barber   | §10.2, Eq. 10.2.2   | p. 204      |
| §2      | Barber   | §10.2, Eq. 10.2.5–7 | pp. 204–205 |
| §3      | MML      | §8.3                | pp. 271–275 |
| §3 P3   | MML      | §11.2               | pp. 356–365 |
