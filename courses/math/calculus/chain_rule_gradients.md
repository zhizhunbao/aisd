# Chain Rule & Gradients | 链式法则与梯度

> **Purpose:** Chain rule is the mathematical engine of backpropagation.
> **Primary Source:** MML §5.2.2, §5.6 — Deisenroth et al.
> **See also:** [derivatives.md](derivatives.md) | [gradient_descent.md](../optimization/gradient_descent.md)
> **Prerequisites:** [derivatives.md](derivatives.md)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^n$ | set of all $n$-dimensional real vectors | $n$ 维实数向量集 |

---

## §1 Univariate Chain Rule (一元链式法则)

> 📚 Source: MML §5.1.2, Eq. 5.32, p. 151

When functions are composed, the derivative multiplies each layer's derivative.

函数复合时，导数是各层导数的乘积。

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $f(x)$ | inner function | 内函数 |
| $g(f)$ | outer function | 外函数 |

$\frac{d}{dx}g(f(x)) = g'(f(x)) \cdot f'(x)$

**Example:** $(2x+1)^4$ → $4(2x+1)^3 \cdot 2 = 8(2x+1)^3$

> 📚 MML Example 5.5

### 1.2 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Compute $\frac{d}{dx}\sin(x^2)$.

> 📐 Original Problem

<details><summary>✅ Solution</summary>

$\cos(x^2) \cdot 2x = 2x\cos(x^2)$

</details>

---

## §2 Multivariate Chain Rule (多元链式法则)

> 📚 Source: MML §5.2.2, Eq. 5.48–5.49

For $f(\mathbf{x})$ where $\mathbf{x}$ depends on $t$:

$\frac{df}{dt} = \sum_{i=1}^{n} \frac{\partial f}{\partial x_i} \cdot \frac{\partial x_i}{\partial t}$

> 🔑 "Neighboring dimensions must match" — like matrix multiplication.
> 相邻维度必须匹配。

**Example:** $f(x_1,x_2) = x_1^2 + 2x_2$, $x_1=\sin t$, $x_2=\cos t$:

$\frac{df}{dt} = 2\sin t \cos t + 2(-\sin t) = 2\sin t(\cos t - 1)$

> 📚 MML Example 5.8

### 2.2 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P2.** For $f(x,y) = x^2 y$, where $x = 2t$ and $y = t^2$, compute $\frac{df}{dt}$ at $t = 1$ using the multivariate chain rule.

> 📐 Original Problem — applies MML §5.2.2

<details><summary>✅ Solution</summary>

$\frac{\partial f}{\partial x} = 2xy = 2(2)(1) = 4$, $\frac{\partial x}{\partial t} = 2$

$\frac{\partial f}{\partial y} = x^2 = 4$, $\frac{\partial y}{\partial t} = 2t = 2$

$\frac{df}{dt} = 4 \cdot 2 + 4 \cdot 2 = 16$

</details>

---

## §3 Backpropagation (反向传播)

> 📚 Source: MML §5.6, pp. 159–163 — Eq. 5.111–5.118

### 3.1 Deep Network = Function Composition (深度网络 = 函数复合)

$y = f_K(f_{K-1}(\cdots f_1(\mathbf{x}) \cdots))$

Each layer: $f_i = \sigma(A_{i-1}\mathbf{x}_{i-1} + \mathbf{b}_{i-1})$

### 3.2 Gradient via Chain Rule (通过链式法则求梯度)

$\frac{\partial L}{\partial \theta_i} = \frac{\partial L}{\partial f_K} \cdot \frac{\partial f_K}{\partial f_{K-1}} \cdots \frac{\partial f_{i+2}}{\partial f_{i+1}} \cdot \frac{\partial f_{i+1}}{\partial \theta_i}$

> 🔑 Most of the chain is shared — compute once from output and reuse backward.
> 大部分链共享——从输出端计算一次，反向复用。

### 3.3 Vanishing Gradient (梯度消失)

$\frac{\partial L}{\partial h_1} = \frac{\partial L}{\partial h_{100}} \cdot \prod_{t=2}^{100} \frac{\partial h_t}{\partial h_{t-1}}$

If each factor $< 1$: gradient vanishes exponentially. LSTM solves this with additive cell state update.

如果每个因子 $< 1$：梯度指数级消失。LSTM 通过加法 cell state 更新解决。

> 🔗 **Course Connection:**
> - **W3 CNN:** Backprop through conv + pooling + FC
> - **W4 RNN:** BPTT = chain rule unrolled through time; vanishing gradient → LSTM
> - **All DL:** PyTorch/TF implement auto-differentiation (MML §5.6.2)

### 3.4 Practice Problems (练习题)

#### 🟡 Medium | 中等题

**P3.** For $h = \sigma(Wx)$, $\hat{y} = Vh$, $L = (\hat{y}-y)^2$, derive $\frac{\partial L}{\partial W}$.

> 📐 Original Problem — applies MML §5.6

<details><summary>✅ Solution</summary>

$\frac{\partial L}{\partial W} = 2(\hat{y}-y) \cdot V \cdot \sigma'(Wx) \cdot x$

</details>

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Chain rule (1D) | $(g \circ f)' = g'(f)f'$ | MML §5.1, Eq. 5.32 | All |
| Chain rule (nD) | $\frac{df}{dt} = \sum \frac{\partial f}{\partial x_i}\frac{\partial x_i}{\partial t}$ | MML §5.2, Eq. 5.49 | All DL |
| Backprop | Chain from output backward | MML §5.6, Eq. 5.118 | CNN, RNN |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation | Pages |
| --- | --- | --- | --- |
| §1 | MML | §5.1.2, Eq. 5.32 | p. 151 |
| §2 | MML | §5.2.2, Eq. 5.48–5.49 | pp. 152–154 |
| §3 | MML | §5.6, Eq. 5.111–5.118 | pp. 159–163 |