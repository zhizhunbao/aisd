---
topic: convolution
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Oppenheim & Willsky, Signals and Systems, 2nd Ed. Ch.2–4"
  - "📖 Paper: Cooley & Tukey, FFT 1965 — https://doi.org/10.1090/S0025-5718-1965-0178586-1"
expiry: never
status: current
---

# 卷积 (Convolution) 数学基础 — 信号处理视角

> 📚 Book: Oppenheim & Willsky, 《Signals and Systems》, Ch.2–4

---


## 符号对照表

| 符号 | 含义 | 英文 | 取值 |
|------|------|------|------|
| $f(t), g(t)$ | 连续时间信号 | Continuous-time signals | $\mathbb{R} \to \mathbb{R}$ |
| $f[n], g[n]$ | 离散时间序列 | Discrete-time sequences | $\mathbb{Z} \to \mathbb{R}$ |
| $*$ | 卷积运算符 | Convolution operator | — |
| $\star$ | 互相关运算符 | Cross-correlation operator | — |
| $\delta(t)$ | 连续狄拉克 δ 函数 | Dirac delta | 面积 = 1 的脉冲 |
| $\delta[n]$ | 离散单位脉冲 | Kronecker delta | $\delta[0]=1$, 其余 0 |
| $h(t), h[n]$ | 脉冲响应 | Impulse response | LTI 系统特征函数 |
| $\tau, k$ | 积分/求和变量（哑变量） | Dummy variable | — |
| $F(\omega), H(\omega)$ | 频域表示（傅里叶变换） | Fourier transform | $\mathbb{R} \to \mathbb{C}$ |
| $N$ | 序列长度 | Sequence length | 正整数 |

> 📚 Book: Oppenheim & Willsky, Ch.1–2

---


## 核心公式

### 公式 1: 连续卷积定义

**直觉：** 把输入信号拆成无穷多个微小的脉冲，每个脉冲通过系统产生一个缩放平移的脉冲响应，然后把所有响应叠加起来。

$$
(f * g)(t) = \int_{-\infty}^{\infty} f(\tau) \cdot g(t - \tau) \, d\tau
$$

> 📚 Book: Oppenheim & Willsky, Eq.2.87

**操作步骤：**

$$
\text{Step 1: 翻转 } g(\tau) \to g(-\tau) \quad \text{（关于 } \tau=0 \text{ 做镜像翻转）}
$$
$$
\text{Step 2: 平移 } g(-\tau) \to g(t-\tau) \quad \text{（向右移动 } t \text{ 个单位）}
$$
$$
\text{Step 3: 相乘积分 } \int f(\tau) \cdot g(t-\tau) \, d\tau \quad \text{（重叠区域的加权面积）}
$$

---

### 公式 2: 离散卷积定义

**直觉：** 连续卷积的离散版本——积分变求和，函数变序列。

$$
(f * g)[n] = \sum_{k=-\infty}^{\infty} f[k] \cdot g[n - k]
$$

> 📚 Book: Oppenheim & Willsky, Eq.2.39

**输出长度：** 若 $f$ 长度 $N_1$，$g$ 长度 $N_2$，则 $f*g$ 长度 = $N_1 + N_2 - 1$

---

### 公式 3: 互相关定义

**直觉：** 衡量两个信号在不同偏移下有多"像"。和卷积几乎一样，但不翻转。

$$
(f \star g)(t) = \int_{-\infty}^{\infty} f(\tau) \cdot g(t + \tau) \, d\tau
$$

**与卷积的关系：**

$$
(f \star g)(t) = f(-t) * g(t) = (f * g')(t) \quad \text{其中 } g'(\tau) = g(-\tau)
$$

> DL 中的"卷积"实际执行的是互相关，因为滤波器权重是可学习的，翻不翻等价。

> 📚 Book: Oppenheim & Willsky, Ch.2.6

---

### 公式 4: 卷积定理 ⭐

**直觉：** 时域做卷积（复杂的积分）= 频域做乘法（简单的逐点相乘）。这是 FFT 加速卷积的理论基础。

$$
\mathcal{F}\{f * g\} = F(\omega) \cdot G(\omega)
$$

$$
\mathcal{F}\{f \cdot g\} = \frac{1}{2\pi} F(\omega) * G(\omega)
$$

> 📚 Book: Oppenheim & Willsky, Theorem 4.4

**FFT 加速卷积的流程：**

$$
f * g = \mathcal{F}^{-1}\{\mathcal{F}\{f\} \cdot \mathcal{F}\{g\}\}
$$

| 方法 | 复杂度 | 何时更快 |
|------|--------|---------|
| 直接卷积 | $O(N_1 \cdot N_2)$ | 短序列 ($N < 64$) |
| FFT 卷积 | $O(N \log N)$ | 长序列 ($N > 64$) |

> 📖 Paper: Cooley & Tukey, [FFT Algorithm](https://doi.org/10.1090/S0025-5718-1965-0178586-1), 1965

---

### 公式 5: LTI 系统输出

**直觉：** 知道系统的脉冲响应 $h(t)$，就能通过卷积计算系统对**任意输入** $x(t)$ 的输出。

$$
y(t) = x(t) * h(t) = \int_{-\infty}^{\infty} x(\tau) h(t - \tau) d\tau
$$

频域表示：$Y(\omega) = X(\omega) \cdot H(\omega)$

> 📚 Book: Oppenheim & Willsky, Ch.2.4

---

### 公式 6: 常见卷积结果

| $f(t)$ | $g(t)$ | $(f*g)(t)$ |
|--------|--------|-----------|
| $\delta(t)$ | $g(t)$ | $g(t)$（恒等元） |
| $\delta(t-t_0)$ | $g(t)$ | $g(t-t_0)$（平移） |
| $u(t)$ 阶跃 | $u(t)$ 阶跃 | $t \cdot u(t)$（斜坡） |
| $e^{-at}u(t)$ | $e^{-bt}u(t)$ | $\frac{e^{-bt}-e^{-at}}{a-b}u(t)$ ($a \neq b$) |
| 矩形脉冲 $\Pi(t)$ | $\Pi(t)$ | 三角脉冲 $\Lambda(t)$ |

> 📚 Book: Oppenheim & Willsky, Ch.2.4

---


## 公式关系图

```
公式 1: 连续卷积 f*g = ∫f(τ)g(t-τ)dτ
│
├─── 离散化 ──→ 公式 2: 离散卷积 Σf[k]g[n-k]
│                    │
│                    └──→ 公式 4: 卷积定理 F{f*g} = F·G
│                              │
│                              └──→ FFT 加速: O(NlogN)
│
├─── 不翻转 ──→ 公式 3: 互相关 ∫f(τ)g(t+τ)dτ
│                    │
│                    └──→ 深度学习 "卷积" (实为互相关)
│
└─── LTI ──→ 公式 5: y(t) = x(t) * h(t)
                  │
                  └──→ 公式 6: 常见卷积结果表
```

---


## 手算练习

### 练习 1: 两个矩形脉冲的卷积

**题目：** $f[n] = [1, 1, 1]$（$n=0,1,2$），$g[n] = [1, 2]$（$n=0,1$），求 $f * g$。

**解答步骤：**

1. 翻转 $g$：$g[-k] = [2, 1]$（$k=0$ 对应 2，$k=-1$ 对应 1）
2. 逐位计算：
   - $n=0$：$f[0]g[0] = 1 \times 1 = 1$
   - $n=1$：$f[0]g[1] + f[1]g[0] = 1 \times 2 + 1 \times 1 = 3$
   - $n=2$：$f[1]g[1] + f[2]g[0] = 1 \times 2 + 1 \times 1 = 3$
   - $n=3$：$f[2]g[1] = 1 \times 2 = 2$
3. 结果：$f * g = [1, 3, 3, 2]$，长度 = $3 + 2 - 1 = 4$ ✓

> 📚 Book: Oppenheim & Willsky, Ch.2.4

### 练习 2: 用卷积定理验证

**题目：** 验证练习 1 的结果可以用 DFT 相乘得到。

**解答：** 补零到 $N=4$：$f' = [1,1,1,0]$, $g' = [1,2,0,0]$

$F = \text{DFT}(f') = [3, 1-j, -1, 1+j]$

$G = \text{DFT}(g') = [3, 1-2j, -1, 1+2j]$

$Y = F \cdot G = [9, (1-j)(1-2j), 1, (1+j)(1+2j)] = [9, -1-3j, 1, -1+3j]$

$y = \text{IDFT}(Y) = [1, 3, 3, 2]$ ✓ 与直接卷积一致！

---


## 公式速查表

| 名称 | 公式 | 用途 |
|------|------|------|
| 连续卷积 | $\int f(\tau)g(t-\tau)d\tau$ | LTI 系统分析 |
| 离散卷积 | $\sum f[k]g[n-k]$ | 数字信号处理 |
| 互相关 | $\int f(\tau)g(t+\tau)d\tau$ | 模式匹配 / DL |
| 卷积定理 | $\mathcal{F}\{f*g\} = F \cdot G$ | FFT 加速 |
| LTI 输出 | $y = x * h$ | 已知 h 求任意输出 |
| 输出长度 | $N_1 + N_2 - 1$ | 计算结果长度 |
| δ 卷积 | $f * \delta = f$ | 恒等变换 |
| 平移 | $f * \delta_{t_0} = f(t-t_0)$ | 延迟 |

> 📚 Book: Oppenheim & Willsky, Ch.2–4
