---
topic: convolution
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Oppenheim & Willsky, Signals and Systems, 2nd Ed. Ch.2–4"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: never
status: current
---

# 卷积 (Convolution) 核心概念 — 信号处理视角

> 📚 Book: Oppenheim & Willsky, 《Signals and Systems》, Ch.2–4

---


## 术语定义

### 卷积 (Convolution)

两个函数之间的一种数学运算。连续形式：$(f * g)(t) = \int_{-\infty}^{\infty} f(\tau) \cdot g(t - \tau) \, d\tau$。操作步骤：(1) 翻转其中一个函数 $g(\tau) \to g(-\tau)$；(2) 平移翻转后的函数 $g(t-\tau)$；(3) 对两个函数逐点相乘后积分。卷积描述了一个系统对输入信号的"加权叠加"效果。

> 易混淆：**互相关 (Cross-correlation)** — 互相关不翻转：$(f \star g)(t) = \int f(\tau) g(t+\tau) d\tau$。当 $g$ 是偶函数（关于 0 对称）时两者等价。深度学习中的"卷积"实际是互相关。

### 互相关 (Cross-correlation)

衡量两个函数在不同位移下的相似度：$(f \star g)(t) = \int f(\tau) g(t+\tau) d\tau$。和卷积唯一的区别是**没有翻转**。互相关在模式匹配中更直观——滑动模板在信号上寻找最相似的位置。

> 易混淆：**卷积 vs 互相关** — 卷积翻转，互相关不翻转。$(f * g)(t) = (f \star g')(t)$，其中 $g'(\tau) = g(-\tau)$。对于可学习滤波器（DL），翻不翻等价。

### 脉冲响应 (Impulse Response)

线性时不变 (LTI) 系统对单位脉冲 $\delta(t)$ 的输出 $h(t)$。一旦知道 $h(t)$，就能通过卷积计算系统对**任意输入**的输出：$y(t) = x(t) * h(t)$。脉冲响应完全刻画了一个 LTI 系统。

### 线性时不变系统 (LTI System)

满足两个条件的系统：(1) **线性**——输入加倍，输出也加倍；两个输入的叠加等于两个输出的叠加；(2) **时不变**——输入延迟 $t_0$，输出也延迟 $t_0$。LTI 系统的输出 = 输入与脉冲响应的卷积。

> 易混淆：**LTI vs 非线性系统** — 非线性系统（如 ReLU）不满足叠加原理，不能用卷积完全描述

### 离散卷积 (Discrete Convolution)

连续卷积的离散版本：$(f * g)[n] = \sum_{k=-\infty}^{\infty} f[k] \cdot g[n-k]$。将积分替换为求和，函数替换为序列。这是计算机中实际使用的形式。

### 循环卷积 (Circular Convolution)

对有限长序列，将序列视为**周期性延拓**后做卷积：$(f \circledast g)[n] = \sum_{k=0}^{N-1} f[k] \cdot g[(n-k) \bmod N]$。FFT 计算的是循环卷积——要得到线性卷积需要补零。

> 易混淆：**线性卷积 vs 循环卷积** — 线性卷积输出长度 = $N_1 + N_2 - 1$；循环卷积输出长度 = $\max(N_1, N_2)$。补零到 $N_1+N_2-1$ 后循环卷积 = 线性卷积。

### 卷积定理 (Convolution Theorem)

时域的卷积等于频域的逐点相乘：$\mathcal{F}\{f * g\} = \mathcal{F}\{f\} \cdot \mathcal{F}\{g\}$。反过来也成立：时域的逐点相乘等于频域的卷积。这是 FFT 加速卷积的理论基础。

### 狄拉克 δ 函数 (Dirac Delta)

一个在 $t=0$ 处无穷高、无穷窄、面积为 1 的"函数"（严格说是分布）：$\int \delta(t) dt = 1$，且 $f(t) * \delta(t) = f(t)$——δ 是卷积运算的**单位元**（恒等元素）。

### 傅里叶变换 (Fourier Transform)

将时域信号分解为不同频率的正弦/余弦分量：$F(\omega) = \int f(t) e^{-j\omega t} dt$。傅里叶变换将卷积（复杂的积分）变成逐点相乘（简单的乘法），是理解和加速卷积的关键工具。

> 📚 Book: Oppenheim & Willsky, Ch.2.4, Ch.3.4, Ch.4.4
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

---


## 概念辨析

### 卷积 vs 互相关

| 维度 | 卷积 (Convolution) | 互相关 (Cross-correlation) |
|------|--------------------|--------------------------| 
| **定义** | $\int f(\tau) g(t-\tau) d\tau$ | $\int f(\tau) g(t+\tau) d\tau$ |
| **核翻转** | ✅ 翻转 $g$ | ❌ 不翻转 |
| **数学性质** | 交换律 $f*g = g*f$ | 不满足交换律 |
| **物理含义** | 系统对输入的加权叠加 | 两个信号的相似度度量 |
| **DL 使用** | ❌ DL 不用真卷积 | ✅ DL 的"卷积"实际是互相关 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

### 连续卷积 vs 离散卷积

| 维度 | 连续卷积 | 离散卷积 |
|------|---------|---------|
| **操作数** | 连续函数 $f(t), g(t)$ | 离散序列 $f[n], g[n]$ |
| **运算** | 积分 $\int$ | 求和 $\sum$ |
| **输出** | 连续函数 | 离散序列 |
| **长度** | 两函数支撑集之和 | $N_1 + N_2 - 1$ |
| **计算** | 解析求解或数值积分 | 直接求和或 FFT |

> 📚 Book: Oppenheim & Willsky, Ch.2.4

### 线性卷积 vs 循环卷积

| 维度 | 线性卷积 | 循环卷积 |
|------|---------|---------|
| **序列处理** | 无边界假设（超出范围=0） | 周期延拓（首尾相连） |
| **输出长度** | $N_1 + N_2 - 1$ | $N$（取两者较大） |
| **FFT 关系** | FFT 计算的不是线性卷积 | FFT 直接算出的就是循环卷积 |
| **转换方法** | 补零到 $N_1+N_2-1$ 后用 FFT | 线性卷积的特例 |

> 📚 Book: Oppenheim & Willsky, Ch.8

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────────┐
│                    卷积运算过程                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  输入信号 f(t)     脉冲响应 h(t)                                  │
│       │                  │                                        │
│       │         Step 1: 翻转 h(τ) → h(-τ)                        │
│       │         Step 2: 平移 h(-τ) → h(t-τ)                      │
│       │                  │                                        │
│       ▼                  ▼                                        │
│       f(τ) ───── × ───── h(t-τ)                                  │
│               逐点相乘                                            │
│                  │                                                │
│         Step 3: ∫ 积分（或 Σ 求和）                               │
│                  │                                                │
│                  ▼                                                │
│              y(t) = (f * h)(t)                                   │
│                                                                  │
│  等价频域方法:                                                     │
│  F(ω)·H(ω) = Y(ω)    ←── 卷积定理                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

> 📚 Book: Oppenheim & Willsky, Ch.2.4

### 卷积的代数性质

| 性质 | 公式 | 白话 |
|------|------|------|
| 交换律 | $f * g = g * f$ | 谁先谁后无所谓 |
| 结合律 | $(f * g) * h = f * (g * h)$ | 级联 LTI 系统顺序无关 |
| 分配律 | $f * (g + h) = f*g + f*h$ | 并联 LTI 系统 |
| 单位元 | $f * \delta = f$ | 脉冲是卷积的"1" |
| 微分 | $(f * g)' = f' * g = f * g'$ | 微分可以提到任一侧 |
| 平移 | $f(t) * \delta(t-t_0) = f(t-t_0)$ | 与延迟脉冲卷积 = 平移 |

> 📚 Book: Oppenheim & Willsky, Ch.2.4

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 连续卷积 | $\int f(\tau)g(t-\tau)d\tau$ | 信号通过滤波器 |
| 离散卷积 | $\sum f[k]g[n-k]$ | 数字信号处理 |
| 循环卷积 | $\sum f[k]g[(n-k)\bmod N]$ | FFT 计算 |
| 卷积定理 | $\mathcal{F}\{f*g\} = F \cdot G$ | FFT 加速 |
| 输出长度 | $N_1 + N_2 - 1$ | 长度 5 * 长度 3 → 长度 7 |
| 单位元 | $f * \delta = f$ | 恒等变换 |
| DL "卷积" | 实际是互相关（不翻转） | `nn.Conv2d` |

> 📚 Book: Oppenheim & Willsky, Ch.2–4
