---
topic: integration_summation
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5-6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Grinstead & Snell, Introduction to Probability, Ch.1-2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/grinstead_snell_probability.pdf"
  - "📚 Book: Bishop, PRML, Ch.1-2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# 积分与求和 核心概念

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5-6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2

---


## 术语定义

### 求和 (Summation)

将一组离散值逐个累加的运算。用符号 $\sum$ 表示。在 ML 中，求和无处不在：损失函数是对样本的求和 $L = \sum_{i=1}^{N} \ell_i$，离散概率的期望是加权求和 $E[X] = \sum_x x \cdot P(x)$，矩阵的迹 $\text{tr}(A) = \sum_i a_{ii}$ 也是求和。求和是积分在离散世界的对应物。

> 易混淆：**求和 vs 积分** — 求和处理可列个（离散）的值，积分处理不可数（连续）的值；积分是求和 $\Delta x \to 0$ 时的极限

### 有限求和 (Finite Sum)

上下界均为有限整数的求和 $\sum_{i=1}^{N} a_i$。项数固定，结果确定。常见公式如等差级数 $\sum_{i=1}^{N} i = N(N+1)/2$、等比级数 $\sum_{i=0}^{N-1} r^i = (1-r^N)/(1-r)$。ML 中的经验风险 $\hat{R} = \frac{1}{N}\sum_{i=1}^{N} L(y_i, \hat{y}_i)$ 就是有限求和。

### 无穷级数 (Infinite Series)

项数趋于无穷的求和 $\sum_{i=0}^{\infty} a_i$。比有限求和多了一个关键问题：是否**收敛**。Taylor 级数 $e^x = \sum_{n=0}^{\infty} x^n / n!$ 是无穷级数。ML 中的 softmax 归一化、generating function、核函数的 Mercer 展开都涉及无穷级数。

> 易混淆：**级数 vs 序列 (sequence)** — 序列 $\{a_n\}$ 是逐项列出的数列；级数 $\sum a_n$ 是将序列做累加，研究的是部分和 $S_N = \sum_{n=1}^{N} a_n$ 的极限

### 不定积分 (Indefinite Integral / Antiderivative)

求一个函数 $F(x)$ 使得 $F'(x) = f(x)$，记作 $\int f(x)\,dx = F(x) + C$。不定积分不给出一个具体的数，而是给出一族函数（差一个常数 $C$）。它是微分的逆运算。在 ML 中很少直接使用不定积分，但它是理解定积分的基石（通过微积分基本定理连接）。

> 易混淆：**不定积分 vs 定积分** — 不定积分结果是函数（+ 常数 C），定积分结果是一个数

### 定积分 (Definite Integral)

在区间 $[a, b]$ 上对函数"求面积"：$\int_a^b f(x)\,dx$。几何上是曲线与 $x$ 轴围成的带符号面积。微积分基本定理说 $\int_a^b f(x)\,dx = F(b) - F(a)$，其中 $F'=f$。在概率论中，连续随机变量的概率就是 PDF 的定积分 $P(a \le X \le b) = \int_a^b p(x)\,dx$。

### 黎曼积分 (Riemann Integral)

定积分的经典定义方式：将区间切分为 $n$ 个小段，取每段上函数值 $f(x_i^*)$ 乘以段宽 $\Delta x_i$，做求和 $\sum_{i=1}^{n} f(x_i^*) \Delta x_i$，然后令最大的 $\Delta x_i \to 0$ 取极限。这是"积分是求和的极限"的精确表述。大多数 ML 中遇到的积分都是黎曼积分。

> 易混淆：**黎曼积分 vs 勒贝格积分** — 黎曼按 $x$ 轴切分求和，勒贝格按 $y$ 轴切分求和；勒贝格积分能处理更多"病态"函数，但 ML 中多数场景黎曼足够

### 多重积分 (Multiple Integral)

对多个变量的积分 $\int\!\int f(x,y)\,dx\,dy$，推广到 $d$ 维。在 ML 中，联合概率分布的归一化 $\int_{\mathbb{R}^d} p(\mathbf{x})\,d\mathbf{x} = 1$ 和边缘化 $p(x) = \int p(x,y)\,dy$ 都是多重积分。高维积分是贝叶斯方法的核心难题。

### 期望 (Expectation)

随机变量 $X$ 在分布 $p$ 下的"加权平均"。离散版用求和 $E[X] = \sum_x x \cdot p(x)$，连续版用积分 $E[X] = \int x \cdot p(x)\,dx$。期望是 ML 中最重要的积分/求和操作之一，损失函数的期望风险、方差 $\text{Var}[X] = E[X^2] - (E[X])^2$、KL 散度等都基于期望。

> 易混淆：**期望 vs 均值 (mean)** — 期望是理论上对分布的积分/求和，均值是对有限样本的经验平均 $\bar{x} = \frac{1}{N}\sum x_i$；大数定律保证样本均值收敛到期望

### 边缘化 (Marginalization)

通过对联合分布中的某些变量积分（或求和）来消去它们，得到剩余变量的分布。连续情况 $p(x) = \int p(x, y)\,dy$，离散情况 $P(X=x) = \sum_y P(X=x, Y=y)$。贝叶斯推断中的模型证据 $p(\mathcal{D}) = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta$ 就是对参数的边缘化。

### 蒙特卡洛积分 (Monte Carlo Integration)

当解析积分不可行时，用随机采样近似积分值：$\int f(x)p(x)\,dx \approx \frac{1}{N}\sum_{i=1}^{N} f(x_i)$，其中 $x_i \sim p(x)$。这是"用求和近似积分"的计算方法。在贝叶斯深度学习（变分推断、MCMC）中是核心工具。

> 易混淆：**蒙特卡洛积分 vs 数值积分（梯形法等）** — 数值积分按固定网格切分（确定性），蒙特卡洛用随机采样；高维时蒙特卡洛的收敛速度 $O(1/\sqrt{N})$ 不依赖维度，而传统数值积分受维度诅咒

### 数值积分 (Numerical Integration / Quadrature)

用确定性数值方法近似定积分的值。包括梯形法则（Trapezoidal Rule）、Simpson 法则、Gauss 求积等。适用于一维或低维的解析不可积函数。SciPy 的 `scipy.integrate.quad` 是标准实现。

### 求和-积分交换 (Interchange of Summation and Integration)

将 $\sum \int$ 变为 $\int \sum$（或反之）。并非总是合法，需要满足数学条件（如 Fubini 定理、一致收敛、Dominated Convergence 定理）。在推导 ML 公式（如对数似然的梯度、EM 算法的 E 步）时经常需要交换顺序。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2, 6.2-6.3
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2.1, 2.1
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3.4-3.5

---


## 概念辨析

### 求和 vs 积分

| 维度 | 求和 (Summation) | 积分 (Integration) |
|------|---|---|
| **对象** | 离散值（可列集） | 连续函数（不可数） |
| **符号** | $\sum_{i} a_i$ | $\int f(x)\,dx$ |
| **几何直觉** | 长条图（柱状图）的面积之和 | 光滑曲线下的面积 |
| **概率应用** | $E[X] = \sum_x x P(x)$ | $E[X] = \int x\,p(x)\,dx$ |
| **计算难度** | 通常直接可算（有限项）或有收敛公式 | 可能无解析解，需数值/MC 方法 |

> 📚 Book: Grinstead & Snell, [《Probability》](../../../textbooks/grinstead_snell_probability.pdf), Ch.1 vs Ch.2

### 解析积分 vs 数值积分 vs 蒙特卡洛积分

| 维度 | 解析积分 | 数值积分 | 蒙特卡洛积分 |
|------|---------|---------|-------------|
| **方法** | 求原函数 $F(b)-F(a)$ | 确定性网格求和 | 随机采样平均 |
| **精度** | 精确 | 高（低维） | 依赖样本量 |
| **高维可行性** | 多数不可行 | 维度诅咒 | 不受维度影响 |
| **典型工具** | 手算 / SymPy | SciPy `quad` | PyTorch / NumPy 采样 |
| **ML 场景** | 高斯分布归一化 | 1D 后验积分 | 变分推断、MCMC |

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11.1

---


## 核心属性

### 信息架构

```
┌───────────────────────────────────────────────────────┐
│              积分与求和 (Integration & Summation)        │
├───────────────────────────────────────────────────────┤
│  离散世界 (Discrete)                                    │
│  ├─ 有限求和: Σ_{i=1}^{N} a_i                          │
│  ├─ 无穷级数: Σ_{n=0}^{∞} a_n (收敛性!)               │
│  └─ 离散期望: E[X] = Σ x·P(x)                         │
├───────────────────────────────────────────────────────┤
│  连续世界 (Continuous)                                   │
│  ├─ 不定积分: ∫f(x)dx = F(x)+C (微分逆运算)           │
│  ├─ 定积分: ∫_a^b f(x)dx (面积)                        │
│  ├─ 多重积分: ∫∫f(x,y)dxdy                             │
│  └─ 连续期望: E[X] = ∫ x·p(x)dx                       │
├───────────────────────────────────────────────────────┤
│  近似方法 (Approximation)                                │
│  ├─ 数值积分: 梯形法 / Simpson / Gauss                  │
│  └─ 蒙特卡洛: 1/N Σ f(x_i), x_i ~ p(x)               │
└───────────────────────────────────────────────────────┘
```

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5

### 适用场景 ✅

- 计算概率分布的归一化常数 $\int p(x)\,dx = 1$
- 计算期望值 $E[f(X)]$（损失函数的期望风险、方差、协方差）
- 贝叶斯推断中的边缘化 $p(\mathcal{D}) = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta$
- 连续分布的 CDF $F(x) = \int_{-\infty}^{x} p(t)\,dt$
- Taylor 级数展开近似复杂函数
- 离散损失函数的计算 $L = \sum_i \ell_i$

### 不适用场景 ❌

- 高维空间中的精确解析积分（多数情况无封闭解，需用近似）
- 非可测函数的积分（需要勒贝格理论，超出黎曼积分范围）
- 发散级数的直接求和（如调和级数 $\sum 1/n$ 发散，不能赋有限值）

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2, 10.1

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| $\sum_{i=1}^{N} i$ | 等差求和 | $= N(N+1)/2$ |
| $\sum_{i=0}^{N-1} r^i$ | 等比求和 | $= (1-r^N)/(1-r)$, $r\neq 1$ |
| $\int x^n\,dx$ | 幂函数积分 | $= x^{n+1}/(n+1) + C$, $n\neq -1$ |
| $\int e^x\,dx$ | 指数积分 | $= e^x + C$ |
| $\int_a^b f(x)\,dx$ | 微积分基本定理 | $= F(b) - F(a)$ |
| $E[X]$ 离散 | 离散期望 | $= \sum_x x \cdot P(x)$ |
| $E[X]$ 连续 | 连续期望 | $= \int x \cdot p(x)\,dx$ |
| 高斯归一化 | $\int_{-\infty}^{+\infty} e^{-x^2/2}\,dx$ | $= \sqrt{2\pi}$ |
| MC 近似 | $\int f(x)p(x)\,dx \approx$ | $\frac{1}{N}\sum f(x_i)$, $x_i \sim p$ |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5
> 📚 Book: Grinstead & Snell, [《Probability》](../../../textbooks/grinstead_snell_probability.pdf), Ch.1-2
