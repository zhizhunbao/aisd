# Derivatives & Partial Derivatives | 导数与偏导数

> **Purpose:** Derivatives measure how functions change — the foundation for all gradient-based training in ML.
> **Primary Source:** MML §5.1–5.2 — Deisenroth et al.
> **See also:** [chain_rule_gradients.md](chain_rule_gradients.md)
> **Prerequisites:** None

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^n$ | set of all $n$-dimensional real vectors | $n$ 维实数向量集 |

---

## §1 Univariate Derivative (一元导数)

> 📚 Source: MML §5.1, pp. 147–151 — Definition 5.2

### 1.1 Definition (定义)

The derivative measures the instantaneous rate of change of $f(x)$ — the slope of the tangent line.

导数衡量 $f(x)$ 的瞬时变化率——切线的斜率。

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $f(x)$ | a function | 一个函数 | $\mathbb{R} \to \mathbb{R}$ |
| $\frac{df}{dx}$ | derivative of $f$ w.r.t. $x$ | $f$ 对 $x$ 的导数 | $\mathbb{R}$ |
| $h$ | infinitesimal increment | 无穷小增量 | $h \to 0$ |

$\frac{df}{dx} := \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$

> 📚 MML Def. 5.2, Eq. 5.4

### 1.2 Common Derivatives (常用导数)

> 📚 MML §5.1, pp. 147–148

| Function $f(x)$ | Derivative $f'(x)$ | 中文 |
| --- | --- | --- |
| $x^n$ | $nx^{n-1}$ | 幂函数 |
| $e^x$ | $e^x$ | 指数函数 |
| $\ln x$ | $1/x$ | 对数函数 |
| $\sin x$ | $\cos x$ | 正弦 |
| $\cos x$ | $-\sin x$ | 余弦 |

### 1.3 Differentiation Rules (求导法则)

> 📚 MML §5.1.2, Eq. 5.29–5.32

| Rule | Formula | 中文 |
| --- | --- | --- |
| Sum | $(f + g)' = f' + g'$ | 和 |
| Product | $(fg)' = f'g + fg'$ | 积 |
| Quotient | $(f/g)' = \frac{f'g - fg'}{g^2}$ | 商 |
| Chain | $(g \circ f)' = g'(f) \cdot f'$ | 链式 |

### 1.4 Worked Example (手算例题)

> 📚 Adapted from MML Example 5.2

**Problem:** Find $\frac{d}{dx}(x^4)$ from the definition.

**Solution:** $f'(x) = 4x^3$ (power rule: $nx^{n-1}$ with $n=4$).

### 1.5 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Find $\frac{d}{dx}(3x^2 + 5x - 7)$.

> 📐 Original Problem

<details><summary>💡 Hint</summary>

Apply sum rule and power rule to each term.

</details>

<details><summary>✅ Solution</summary>

$f'(x) = 6x + 5$

</details>

---

## §2 Partial Derivative (偏导数)

> 📚 Source: MML §5.2, pp. 152–154 — Definition 5.5

### 2.1 Definition (定义)

When $f$ depends on multiple variables, the partial derivative w.r.t. one variable treats all others as constants.

当 $f$ 有多个变量时，对一个变量求偏导把其他变量当常数。

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $f(\mathbf{x})$ | function of $n$ variables | $n$ 元函数 |
| $\frac{\partial f}{\partial x_i}$ | partial derivative w.r.t. $x_i$ | 对 $x_i$ 的偏导 |
| $\nabla_\mathbf{x} f$ | gradient vector | 梯度向量 |

$\frac{\partial f}{\partial x_i} = \lim_{h \to 0} \frac{f(x_1, \ldots, x_i + h, \ldots, x_n) - f(\mathbf{x})}{h}$

> 📚 MML Def. 5.5, Eq. 5.39

### 2.2 The Gradient (梯度)

The gradient collects all partial derivatives into a vector.

梯度把所有偏导收集成向量。

$\nabla_\mathbf{x} f = \left[\frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \ldots, \frac{\partial f}{\partial x_n}\right]$

> 📚 MML §5.2, Eq. 5.40

> 🔑 The gradient points in the direction of steepest ascent of $f$. To minimize, go in the opposite direction → gradient descent.
> 梯度指向 $f$ 的最陡上升方向。要最小化，走反方向 → 梯度下降。

### 2.3 Worked Example (手算例题)

> 📚 MML Example 5.7, p. 147

**Problem:** Find $\nabla f$ for $f(x_1, x_2) = x_1^2 x_2 + x_1 x_2^3$.

**Solution:**

$\frac{\partial f}{\partial x_1} = 2x_1 x_2 + x_2^3, \quad \frac{\partial f}{\partial x_2} = x_1^2 + 3x_1 x_2^2$

$\nabla f = [2x_1 x_2 + x_2^3, \;\; x_1^2 + 3x_1 x_2^2]$

> 🔗 **Course Connection:**
> - **ML W3 CNN:** Weight updates use $\frac{\partial L}{\partial w_{ij}}$ — partial derivative of loss w.r.t. each weight
> - **ML W4 RNN:** BPTT computes $\frac{\partial L}{\partial W_h}$ summed over all time steps
> - **All training:** $\theta_{new} = \theta_{old} - \gamma \nabla_\theta L$ (gradient descent update)

### 2.4 Practice Problems (练习题)

#### 🟡 Medium | 中等题

**P2.** Compute the gradient of $f(x, y) = x^2 e^y + \sin(xy)$.

计算 $f(x, y) = x^2 e^y + \sin(xy)$ 的梯度。

> 📐 Original Problem — applies product rule and chain rule

<details><summary>💡 Hint</summary>

For $\frac{\partial}{\partial x}[\sin(xy)]$, use chain rule with inner function $u = xy$.

</details>

<details><summary>✅ Solution</summary>

$\frac{\partial f}{\partial x} = 2xe^y + y\cos(xy)$

$\frac{\partial f}{\partial y} = x^2 e^y + x\cos(xy)$

$\nabla f = [2xe^y + y\cos(xy), \;\; x^2 e^y + x\cos(xy)]$

</details>

#### 🔴 Hard | 挑战题

**P3.** The MSE loss is $L = \frac{1}{N}\sum_{i=1}^{N}(y_i - \mathbf{w}^\top \mathbf{x}_i)^2$. Derive $\nabla_\mathbf{w} L$. Show that setting it to zero gives the normal equation.

推导 MSE 损失对权重的梯度，令其为零得到正规方程。

> 📐 Original Problem — connects MML §5.2 to linear regression

<details><summary>💡 Hint</summary>

Let $e_i = y_i - \mathbf{w}^\top \mathbf{x}_i$. Use chain rule: $\frac{\partial}{\partial \mathbf{w}}(e_i^2) = 2e_i \cdot (-\mathbf{x}_i)$.

</details>

<details><summary>✅ Solution</summary>

$\nabla_\mathbf{w} L = \frac{-2}{N}\sum_{i=1}^{N}(y_i - \mathbf{w}^\top \mathbf{x}_i)\mathbf{x}_i$

In matrix form with $X \in \mathbb{R}^{N \times d}$, $\mathbf{y} \in \mathbb{R}^N$:

$\nabla_\mathbf{w} L = \frac{-2}{N}X^\top(\mathbf{y} - X\mathbf{w})$

Setting to zero: $X^\top X \mathbf{w}^* = X^\top \mathbf{y}$ → $\mathbf{w}^* = (X^\top X)^{-1}X^\top \mathbf{y}$ (Normal Equation)

</details>

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Derivative | $\lim_{h\to 0} \frac{f(x+h)-f(x)}{h}$ | MML §5.1, Eq. 5.4 | All |
| Power rule | $(x^n)' = nx^{n-1}$ | MML §5.1 | All |
| Gradient | $\nabla f = [\frac{\partial f}{\partial x_1}, \ldots]$ | MML §5.2, Eq. 5.40 | All training |
| Chain rule | $(g\circ f)' = g'(f) \cdot f'$ | MML §5.1, Eq. 5.32 | Backprop |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation | Pages |
| --- | --- | --- | --- |
| §1 | MML | §5.1, Def. 5.2, Eq. 5.4 | pp. 147–151 |
| §2 | MML | §5.2, Def. 5.5, Eq. 5.39–5.40 | pp. 152–154 |