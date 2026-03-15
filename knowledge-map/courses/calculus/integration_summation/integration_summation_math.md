---
topic: integration_summation
dimension: math
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

# 积分与求和 数学基础

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5-6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $\sum$ | 求和符号，表示把一系列项加起来 | Summation | — |
| $\int$ | 积分符号，连续函数的"面积" | Integral | — |
| $f(x)$ | 被积函数 / 被求和的项 | Integrand / Summand | 取决于具体函数 |
| $a, b$ | 积分下界和上界 | Lower/Upper bound | $a < b$（通常） |
| $N$ | 求和的项数 | Number of terms | $N \in \mathbb{Z}^+$ |
| $\Delta x$ | 区间小段的宽度 | Interval width | $\Delta x > 0$ |
| $F(x)$ | $f(x)$ 的原函数（不定积分） | Antiderivative | $F'(x) = f(x)$ |
| $p(x)$ | 概率密度函数 (PDF) | Probability density | $p(x) \geq 0$ |
| $P(x)$ | 离散概率质量函数 (PMF) | Probability mass | $0 \leq P(x) \leq 1$ |
| $E[X]$ | 期望值 | Expectation | $\mathbb{R}$ |
| $x_i$ | 第 $i$ 个采样点 / 数据点 | Sample point | 取决于分布 |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5 notation

---


## 核心公式

### 公式 1: 有限求和（等差级数）

**直觉：** 从 1 加到 $N$ 的和，等于首尾配对 × 对数

$$
\sum_{i=1}^{N} i = \frac{N(N+1)}{2}
$$

> 📚 Book: 基础数学常识，Gauss 求和公式

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $N$ | 求和上界 | 如 $N=100$ |

**推导过程：**

$$
\text{Step 1: 记 } S = 1 + 2 + 3 + \cdots + N
$$
$$
\text{Step 2: 反向写 } S = N + (N-1) + \cdots + 1
$$
$$
\text{Step 3: 两式相加 } 2S = (N+1) + (N+1) + \cdots + (N+1) = N \cdot (N+1)
$$
$$
\text{Step 4: } S = \frac{N(N+1)}{2}
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), 基础回顾

---

### 公式 2: 有限求和（等比级数）

**直觉：** 按固定比例 $r$ 递增/递减的数列之和，有封闭公式

$$
\sum_{i=0}^{N-1} r^i = \frac{1 - r^N}{1 - r}, \quad r \neq 1
$$

> 📚 Book: 基础代数

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $r$ | 公比 | 如 $r=0.5$ |
| $N$ | 项数 | 如 $N=10$ |

**推导过程：**

$$
\text{Step 1: 记 } S = 1 + r + r^2 + \cdots + r^{N-1}
$$
$$
\text{Step 2: 乘以 } r: \quad rS = r + r^2 + \cdots + r^N
$$
$$
\text{Step 3: 相减 } S - rS = 1 - r^N
$$
$$
\text{Step 4: } S(1 - r) = 1 - r^N \implies S = \frac{1 - r^N}{1 - r}
$$

当 $|r| < 1$ 且 $N \to \infty$ 时，$r^N \to 0$，得到无穷等比级数：$\sum_{i=0}^{\infty} r^i = \frac{1}{1-r}$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), 基础回顾

---

### 公式 3: 微积分基本定理 (Fundamental Theorem of Calculus)

**直觉：** 定积分 = 原函数在上下界的差值，把"求面积"归结为"找反导数"

$$
\int_a^b f(x)\,dx = F(b) - F(a), \quad \text{其中 } F'(x) = f(x)
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $f(x)$ | 被积函数 | 如 $f(x) = x^2$ |
| $F(x)$ | $f$ 的原函数 | 如 $F(x) = x^3/3$ |
| $a, b$ | 积分区间端点 | 如 $[0, 1]$ |

**推导过程：**

$$
\text{Step 1: 定义 } G(x) = \int_a^x f(t)\,dt
$$
$$
\text{Step 2: 根据极限定义 } G'(x) = \lim_{h \to 0} \frac{G(x+h) - G(x)}{h} = \lim_{h \to 0} \frac{1}{h}\int_x^{x+h} f(t)\,dt = f(x)
$$
$$
\text{Step 3: 所以 } G(x) \text{ 是 } f(x) \text{ 的一个原函数，即 } G(x) = F(x) + C
$$
$$
\text{Step 4: } G(a) = 0 \implies C = -F(a)，故 G(b) = F(b) - F(a) = \int_a^b f(x)\,dx
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2, Theorem 5.2

---

### 公式 4: 连续期望 (Continuous Expectation)

**直觉：** 函数 $g(X)$ 关于概率分布 $p(x)$ 的"加权平均"，权重由概率密度给出

$$
E[g(X)] = \int_{-\infty}^{+\infty} g(x) \cdot p(x)\,dx
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 1.33-1.34

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $g(x)$ | 要求期望的函数 | 如 $g(x) = x$（一阶矩），$g(x) = x^2$（二阶矩） |
| $p(x)$ | 概率密度函数 | 如高斯 $p(x) = \frac{1}{\sqrt{2\pi}\sigma}e^{-(x-\mu)^2/(2\sigma^2)}$ |

**推导过程：**

$$
\text{Step 1: 离散情况 } E[g(X)] = \sum_x g(x) \cdot P(x)
$$
$$
\text{Step 2: 将离散求和推广到连续——用 } p(x)\,dx \text{ 替代 } P(x_i)
$$
$$
\text{Step 3: } E[g(X)] = \int_{-\infty}^{+\infty} g(x) \cdot p(x)\,dx
$$

**特殊情况：** 方差 $\text{Var}[X] = E[X^2] - (E[X])^2 = \int x^2 p(x)\,dx - \left(\int x\,p(x)\,dx\right)^2$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 1.33-1.38
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Eq. 3.6

---

### 公式 5: 高斯积分 (Gaussian Integral)

**直觉：** 正态分布归一化的基础——$e^{-x^2}$ 在整个实轴上的积分有优美的封闭解

$$
\int_{-\infty}^{+\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

等价形式：$\int_{-\infty}^{+\infty} e^{-x^2/(2\sigma^2)}\,dx = \sigma\sqrt{2\pi}$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 2.43 (高斯分布归一化)

**推导过程：**

$$
\text{Step 1: 记 } I = \int_{-\infty}^{+\infty} e^{-x^2}\,dx
$$
$$
\text{Step 2: 计算 } I^2 = \left(\int_{-\infty}^{+\infty} e^{-x^2}\,dx\right)\left(\int_{-\infty}^{+\infty} e^{-y^2}\,dy\right) = \int\!\!\int e^{-(x^2+y^2)}\,dx\,dy
$$
$$
\text{Step 3: 极坐标变换 } x = r\cos\theta,\; y = r\sin\theta,\; dx\,dy = r\,dr\,d\theta
$$
$$
\text{Step 4: } I^2 = \int_0^{2\pi}\int_0^{\infty} e^{-r^2} r\,dr\,d\theta = 2\pi \cdot \frac{1}{2} = \pi
$$
$$
\text{Step 5: } I = \sqrt{\pi}
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.6.5 (Gaussian distribution)

---

### 公式 6: 蒙特卡洛近似 (Monte Carlo Approximation)

**直觉：** 无法解析积分时，抽 $N$ 个样本取平均来近似期望

$$
E_{p}[f(X)] = \int f(x)\,p(x)\,dx \approx \frac{1}{N}\sum_{i=1}^{N} f(x_i), \quad x_i \sim p(x)
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11.1, Eq. 11.1

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $N$ | 采样数量 | $N = 10000$ |
| $x_i$ | 从 $p(x)$ 中独立抽取的样本 | — |

**推导过程：**

$$
\text{Step 1: 大数定律 (LLN) — 独立同分布样本的经验均值收敛到期望}
$$
$$
\text{Step 2: } \frac{1}{N}\sum_{i=1}^{N} f(x_i) \xrightarrow{N \to \infty} E_p[f(X)]
$$
$$
\text{Step 3: 误差 } \sim O(1/\sqrt{N}) \text{（与维度无关，这是 MC 的关键优势）}
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11.1
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.17.1

---

### 公式 7: 边缘化公式 (Marginalization)

**直觉：** 不关心某个变量时，对它积分/求和将其"消除"

$$
p(x) = \int p(x, y)\,dy \quad \text{(连续)}
$$
$$
P(X=x) = \sum_{y} P(X=x, Y=y) \quad \text{(离散)}
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 1.10-1.11

**推导过程：**

$$
\text{Step 1: 联合概率定义 } p(x, y) = p(y|x) \cdot p(x)
$$
$$
\text{Step 2: 对 } y \text{ 积分两边}
$$
$$
\text{Step 3: } \int p(x, y)\,dy = p(x) \int p(y|x)\,dy = p(x) \cdot 1 = p(x)
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2

---

### 公式 8: 分部积分 (Integration by Parts)

**直觉：** 积分版的乘积法则——把"难积"的部分转移为"好积"的部分

$$
\int u\,dv = uv - \int v\,du
$$

定积分版本：$\int_a^b u(x)v'(x)\,dx = \bigl[u(x)v(x)\bigr]_a^b - \int_a^b u'(x)v(x)\,dx$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5 (积分技巧)

**推导过程：**

$$
\text{Step 1: 乘积法则 } (uv)' = u'v + uv'
$$
$$
\text{Step 2: 两边积分 } \int (uv)'\,dx = \int u'v\,dx + \int uv'\,dx
$$
$$
\text{Step 3: } uv = \int u'v\,dx + \int uv'\,dx
$$
$$
\text{Step 4: 整理 } \int uv'\,dx = uv - \int u'v\,dx
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5

---


## 公式关系图

```
等差/等比求和 (离散基础)
    │
    │  连续推广
    ▼
黎曼积分定义 ──→ 微积分基本定理 ──→ 定积分求值
    │                   │
    │                   ▼
    │              不定积分技巧
    │              (分部积分、换元)
    │
    ▼
连续期望 E[f(X)] ──→ 方差 Var[X]
    │
    │  无法解析
    ▼
蒙特卡洛近似 ←── 大数定律
    
联合分布 p(x,y) ──→ 边缘化 p(x) = ∫p(x,y)dy
                          │
                          ▼
                    贝叶斯推断: p(D) = ∫p(D|θ)p(θ)dθ

高斯积分 ∫e^{-x²}dx = √π ──→ 高斯分布归一化
```

---


## 手算练习

### 练习 1: 基础定积分

**题目：** 计算 $\int_0^3 (2x + 1)\,dx$

**解答步骤：**

1. 求原函数：$F(x) = x^2 + x$
2. 代入上下界：$F(3) - F(0) = (9 + 3) - (0 + 0) = 12$
3. 结果：$\int_0^3 (2x+1)\,dx = 12$

> 📚 Book: 微积分基本定理应用

### 练习 2: 离散期望

**题目：** 一个骰子的期望值 $E[X]$，$X \in \{1,2,3,4,5,6\}$，每个概率 $P=1/6$

**解答步骤：**

1. 代入公式：$E[X] = \sum_{x=1}^{6} x \cdot \frac{1}{6}$
2. 计算：$= \frac{1}{6}(1+2+3+4+5+6) = \frac{1}{6} \cdot 21 = 3.5$
3. 结果：$E[X] = 3.5$

> 📚 Book: Grinstead & Snell, [《Probability》](../../../textbooks/grinstead_snell_probability.pdf), Ch.1

### 练习 3: 连续期望（指数分布）

**题目：** 指数分布 $p(x) = \lambda e^{-\lambda x}$（$x \geq 0$），求 $E[X]$，取 $\lambda = 2$

**解答步骤：**

1. 代入公式：$E[X] = \int_0^{\infty} x \cdot 2 e^{-2x}\,dx$
2. 分部积分：$u = x, dv = 2e^{-2x}dx \implies du = dx, v = -e^{-2x}$
3. $= \bigl[-xe^{-2x}\bigr]_0^{\infty} + \int_0^{\infty} e^{-2x}\,dx = 0 + \bigl[-\frac{1}{2}e^{-2x}\bigr]_0^{\infty} = \frac{1}{2}$
4. 结果：$E[X] = 1/\lambda = 1/2 = 0.5$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), 概率分布章节

### 练习 4: 高斯积分变体

**题目：** 验证标准正态分布 $p(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$ 的积分为 1

**解答步骤：**

1. $\int_{-\infty}^{+\infty} \frac{1}{\sqrt{2\pi}} e^{-x^2/2}\,dx$
2. 令 $u = x/\sqrt{2}$，则 $dx = \sqrt{2}\,du$
3. $= \frac{1}{\sqrt{2\pi}} \cdot \sqrt{2} \int_{-\infty}^{+\infty} e^{-u^2}\,du = \frac{\sqrt{2}}{\sqrt{2\pi}} \cdot \sqrt{\pi} = 1$ ✅
4. 结果：积分 = 1，归一化验证通过

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 2.43

### 练习 5: 蒙特卡洛估计

**题目：** 用 4 个样本 $x_1=0.2, x_2=0.5, x_3=0.8, x_4=0.3$（均匀分布 $U[0,1]$）估计 $\int_0^1 x^2\,dx$

**解答步骤：**

1. 解析答案：$\int_0^1 x^2\,dx = [x^3/3]_0^1 = 1/3 \approx 0.333$
2. MC 估计：$p(x) = 1$（均匀分布），$\hat{I} = \frac{1}{4}\sum f(x_i) = \frac{1}{4}(0.04 + 0.25 + 0.64 + 0.09) = \frac{1.02}{4} = 0.255$
3. 误差：$|0.333 - 0.255| = 0.078$（样本太少，但随 $N$ 增大会收敛）

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11.1

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 等差求和 | $\sum_{i=1}^N i = N(N+1)/2$ | 基础离散累加 | 无 |
| 等比求和 | $\sum_{i=0}^{N-1} r^i = (1-r^N)/(1-r)$ | 衰减/增长序列 | 无 |
| 微积分基本定理 | $\int_a^b f(x)\,dx = F(b)-F(a)$ | 定积分求值 | 不定积分 |
| 连续期望 | $E[g(X)] = \int g(x)p(x)\,dx$ | 损失/方差/协方差 | 定积分 |
| 高斯积分 | $\int_{-\infty}^{+\infty} e^{-x^2}\,dx = \sqrt{\pi}$ | 正态分布归一化 | 极坐标变换 |
| MC 近似 | $E_p[f] \approx \frac{1}{N}\sum f(x_i)$ | 高维/无解析解 | 大数定律 |
| 边缘化 | $p(x) = \int p(x,y)\,dy$ | 消去变量 | 联合概率 |
| 分部积分 | $\int u\,dv = uv - \int v\,du$ | 简化复杂积分 | 乘积法则 |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5-6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1-2
