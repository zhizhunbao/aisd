# Gradient Descent | 梯度下降

> **Purpose:** Gradient descent is the core optimization algorithm for training ML models — it iteratively moves parameters in the direction that reduces the loss function.
> **Primary Source:** MML §7.1 — Deisenroth et al.
> **See also:** [chain_rule_gradients.md](../calculus/chain_rule_gradients.md) | [lagrange_multipliers.md](lagrange_multipliers.md)
> **Prerequisites:** [derivatives.md](../calculus/derivatives.md), [chain_rule_gradients.md](../calculus/chain_rule_gradients.md)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^d$ | set of all $d$-dimensional real vectors | $d$ 维实数向量集 |

---

## §1 Gradient Descent Update Rule (梯度下降更新规则)

> 📚 Source: MML §7.1, Eq. 7.4–7.6, pp. 227–229 — Deisenroth et al.

### 1.1 Problem Setup (问题设定)

We want to find the parameters that minimize a real-valued function (我们要找让函数值最小的参数):

$$\min_{\mathbf{x}} f(\mathbf{x})$$

where $f: \mathbb{R}^d \to \mathbb{R}$ is differentiable but has no closed-form solution.

> 📖 **Reading the notation:** "$\min_{\mathbf{x}} f(\mathbf{x})$" reads "find the $\mathbf{x}$ that makes $f$ smallest." $\min$ = minimize; the subscript says what we're tuning.

### 1.2 Definition (定义)

The gradient points in the direction of steepest **ascent**. To go **downhill**, we move in the **negative** gradient direction (梯度指向"上坡"最陡方向，取负号就是"下坡"):

| Symbol                   | Meaning (EN)                      | 含义 (中文)                    | Type                                     |
| ------------------------ | --------------------------------- | ------------------------------ | ---------------------------------------- |
| $\mathbf{x}_i$           | parameter vector at step $i$      | 第 $i$ 步参数                  | $\mathbb{R}^d$                           |
| $\gamma_i$               | step-size (learning rate)         | 步长（学习率）                 | $\gamma_i \geq 0$                        |
| $\nabla f(\mathbf{x}_i)$ | gradient of $f$ at $\mathbf{x}_i$ | $f$ 在 $\mathbf{x}_i$ 处的梯度 | row vector $\in \mathbb{R}^{1 \times d}$ |

$$\mathbf{x}_{i+1} = \mathbf{x}_i - \gamma_i \left(\nabla f(\mathbf{x}_i)\right)^\top$$

> 📚 MML Eq. 7.6

> 📖 **Reading the notation:** "$(\nabla f)^\top$" — MML uses row-vector gradients, so the transpose converts it to a column vector to match $\mathbf{x}$.

### 1.3 Intuition (直觉理解)

Imagine a ball on a surface: it rolls **downhill**. Gradient descent does the same thing numerically — at each position, it asks "which direction is steepest downhill?" and takes a step in that direction.

想象一个球在山面上：它往**下坡**滚。梯度下降做的事一样 —— 每一步问"哪个方向最陡"，然后朝那走一步。

### 1.4 Convergence (收敛)

> 📚 MML §7.1, below Eq. 7.6

For a suitable step-size $\gamma_i$, the sequence satisfies $f(\mathbf{x}_0) \geq f(\mathbf{x}_1) \geq \ldots$ and converges to a **local minimum**.

> ⚠️ Gradient descent finds a **local** minimum, not necessarily the **global** one. For **convex** functions (e.g., linear regression loss), all local minima are global (MML §7.3).

### 1.5 Worked Example (手算例题)

> 📚 Adapted from MML Example 7.1, p. 228

**Problem:**

$$f(\mathbf{x}) = \frac{1}{2}\mathbf{x}^\top \begin{bmatrix}2&1\\1&20\end{bmatrix}\mathbf{x} - \begin{bmatrix}5\\3\end{bmatrix}^\top\mathbf{x}$$

Starting at $\mathbf{x}_0 = [-3, -1]^\top$ with $\gamma = 0.085$, compute $\mathbf{x}_1$.

**Solution:**

**Step 1: Gradient**

$$$\nabla f(\mathbf{x}_0) = \mathbf{x}_0^\top\begin{bmatrix}2&1\\1&20\end{bmatrix} - \begin{bmatrix}5\\3\end{bmatrix}^\top = [-7, -23] - [5, 3] = [-12, -26]$$$

**Step 2: Update**

$$\mathbf{x}_1 = [-3, -1]^\top - 0.085 \cdot [-12, -26]^\top = [-3, -1]^\top + [1.02, 2.21]^\top = [-1.98, 1.21]^\top$$

### 1.6 Connection to Course (课程关联)

> 🔗 **Course Connection:**
>
> - **ML W3 CNN:** Training = gradient descent on cross-entropy loss w.r.t. weights/biases
> - **ML W4 RNN:** BPTT computes gradients, then gradient descent updates weights
> - **All DL:** `optimizer.step()` in PyTorch IS one gradient descent iteration

### 1.7 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Given $f(x) = x^2 + 4x + 4$, starting at $x_0 = 3$ with $\gamma = 0.1$, compute $x_1$ and $x_2$.
给定 $f(x) = x^2+4x+4$，从 $x_0=3$，$\gamma=0.1$ 开始，计算 $x_1$ 和 $x_2$。

> 📐 Original Problem — applies MML Eq. 7.6

<details><summary>💡 Hint / 提示</summary>

$f'(x) = 2x + 4$. Apply the update rule: $x_{i+1} = x_i - \gamma f'(x_i)$.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Method: MML §7.1, Eq. 7.6

$f'(x) = 2x + 4$

**Step 1:** $f'(3) = 10$. $x_1 = 3 - 0.1(10) = \mathbf{2.0}$

**Step 2:** $f'(2) = 8$. $x_2 = 2 - 0.1(8) = \mathbf{1.2}$

Note: the minimum is at $x = -2$ where $f'(x) = 0$. We're approaching it.

</details>

---

## §2 Step-Size / Learning Rate (步长 / 学习率)

> 📚 Source: MML §7.1.1, pp. 229–230

### 2.1 Effect of Step-Size (步长的影响)

| Step-size  | Effect (EN)                         | 效果 (中文)          |
| ---------- | ----------------------------------- | -------------------- |
| Too small  | Converges but very slowly           | 收敛但极慢           |
| Just right | Smooth convergence to minimum       | 平稳收敛到最小值     |
| Too large  | Overshoots, oscillates, may diverge | 超调、震荡、可能发散 |

### 2.2 Adaptive Heuristics (自适应启发)

> 📚 MML §7.1.1, citing Toussaint (2012)

- If $f$ **increases** after a step → step was too large; **undo** and **decrease** $\gamma$
- If $f$ **decreases** → step could have been larger; try **increasing** $\gamma$

> 🔑 Modern frameworks use adaptive optimizers (Adam, RMSProp) that adjust learning rates per-parameter automatically.

### 2.3 Practice Problems (练习题)

#### 🟡 Medium | 中等题

**P2.** For $f(x) = x^2 + 4x + 4$, what happens if $\gamma = 1.5$? Starting from $x_0 = 3$, compute $x_1, x_2, x_3$ and explain why the algorithm diverges.
同样的函数，但 $\gamma = 1.5$。计算 $x_1, x_2, x_3$，解释为什么发散。

> 📐 Original Problem — demonstrates MML §7.1.1 step-size issue

<details><summary>💡 Hint / 提示</summary>

Apply the same update rule. Watch whether $|x_i|$ grows or shrinks.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Method: MML §7.1.1 — step-size too large

$x_1 = 3 - 1.5(10) = \mathbf{-12}$

$f'(-12) = -20$. $x_2 = -12 - 1.5(-20) = \mathbf{18}$

$f'(18) = 40$. $x_3 = 18 - 1.5(40) = \mathbf{-42}$

$|x_i|$ is growing: $3 → 12 → 18 → 42$. The algorithm **overshoots** and **diverges** because $\gamma$ is too large.

For a quadratic $f(x) = ax^2 + bx + c$, convergence requires $\gamma < 1/a = 1$. Here $\gamma = 1.5 > 1$, so it diverges.

</details>

---

## §3 Gradient Descent with Momentum (带动量的梯度下降)

> 📚 Source: MML §7.1.2, Eq. 7.11–7.12, pp. 230–231

### 3.1 Problem

When the optimization surface is a long, thin valley, gradient descent **zigzags** between the valley walls and converges very slowly (在狭长谷底，梯度下降来回锯齿，收敛极慢).

### 3.2 Solution: Momentum

Add a **memory** of the previous update to smooth out oscillations (加上"记忆"来平滑震荡):

| Symbol               | Meaning (EN)         | 含义 (中文)     | Range          |
| -------------------- | -------------------- | --------------- | -------------- |
| $\alpha$             | momentum coefficient | 动量系数        | $[0, 1]$       |
| $\Delta\mathbf{x}_i$ | update at step $i$   | 第 $i$ 步更新量 | $\mathbb{R}^d$ |

$$\mathbf{x}_{i+1} = \mathbf{x}_i - \gamma_i (\nabla f(\mathbf{x}_i))^\top + \alpha \Delta\mathbf{x}_i$$

$$\Delta\mathbf{x}_i = \alpha \Delta\mathbf{x}_{i-1} - \gamma_{i-1}(\nabla f(\mathbf{x}_{i-1}))^\top$$

> 📚 MML Eq. 7.11–7.12, citing Rumelhart et al. (1986)

> 🔑 Like a heavy ball that resists sudden direction changes — it "remembers" where it was going. 像一个重球有惯性，不会突然掉头。

### 3.3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P3.** In the momentum formula, if $\alpha = 0$, what does the update simplify to? If $\alpha = 0.9$ and the gradient is pointing in the same direction for 5 steps, does momentum speed up or slow down convergence?
当 $\alpha=0$ 时公式简化成什么？若梯度连续 5 步同方向，动量是加速还是减速？

> 📐 Original Problem — conceptual understanding of MML Eq. 7.11

<details><summary>✅ Solution / 解答</summary>

When $\alpha = 0$: $\Delta\mathbf{x}_i = 0$, so the update becomes standard gradient descent $\mathbf{x}_{i+1} = \mathbf{x}_i - \gamma(\nabla f)^\top$. Momentum disappears.

When $\alpha = 0.9$ and gradients align: momentum **accumulates** in that direction ($0.9 + 0.9^2 + \ldots$), effectively increasing the step-size. This **speeds up** convergence along consistent directions while **dampening** oscillations in zigzag directions.

</details>

---

## §4 Stochastic Gradient Descent (随机梯度下降)

> 📚 Source: MML §7.1.3, Eq. 7.13–7.15, pp. 231–232

### 4.1 Problem

When the objective is a sum over all $N$ data points (当目标函数是 $N$ 个数据的损失之和):

$$L(\theta) = \sum_{n=1}^{N} L_n(\theta)$$

> 📚 MML Eq. 7.13

**Full batch** gradient requires computing $\nabla L_n$ for ALL $n$ — expensive for large datasets.

### 4.2 Solution: Mini-Batch SGD

Instead of summing over all $N$, randomly sample a **subset** and use that as a gradient estimate (随机抽一部分数据估计梯度):

| Variant        | Data Per Step | Accuracy       | Speed            |
| -------------- | ------------- | -------------- | ---------------- |
| Batch GD       | All $N$       | Exact gradient | Slow             |
| Mini-batch SGD | $B \ll N$     | Approximate    | Fast             |
| Pure SGD       | 1 sample      | Very noisy     | Fastest per step |

> 📚 MML §7.1.3: "We only require that the gradient is an **unbiased estimate** of the true gradient."

### 4.3 Connection to Course (课程关联)

> 🔗 **Course Connection:**
>
> - **ML W3 CNN:** Keras `model.fit(batch_size=32)` uses mini-batch SGD
> - **ML W4 RNN:** Same — training on sequences with batches
> - **All DL:** "SGD" in PyTorch/TF is actually **mini-batch** SGD by default

### 4.4 Practice Problems (练习题)

#### 🟡 Medium | 中等题

**P4.** A dataset has $N = 10000$ samples. Compare total gradient computations per epoch for: (a) Batch GD, (b) Mini-batch SGD with $B = 100$, (c) Pure SGD ($B = 1$). Which has the most parameter updates per epoch?
$N=10000$。比较一个 epoch 的梯度计算量和参数更新次数。

> 📐 Original Problem — applies MML §7.1.3

<details><summary>✅ Solution / 解答</summary>

| Method               | Gradient evals/epoch | Parameter updates/epoch |
| -------------------- | -------------------- | ----------------------- |
| Batch GD             | 10000                | **1**                   |
| Mini-batch ($B=100$) | 10000                | **100**                 |
| Pure SGD ($B=1$)     | 10000                | **10000**               |

All three evaluate the same total gradients per epoch ($N = 10000$). The difference: Batch GD makes **1 very accurate** update; SGD makes **10000 noisy** updates. Mini-batch is the practical middle ground — enough noise to escape local minima, enough accuracy for stable convergence.

</details>

#### 🔴 Hard | 挑战题

**P5.** The objective for linear regression (MML Eq. 7.9) is $\|A\mathbf{x} - \mathbf{b}\|^2$. (a) Derive the gradient (Eq. 7.10). (b) Explain why gradient descent may converge slowly based on the condition number $\kappa = \sigma_{\max}/\sigma_{\min}$.
线性回归目标 $\|A\mathbf{x}-\mathbf{b}\|^2$：(a) 推导梯度；(b) 根据条件数解释收敛慢的原因。

> 📚 From: MML Example 7.2, Eq. 7.9–7.10, p. 230

<details><summary>💡 Hint / 提示</summary>

(a) Expand $(A\mathbf{x}-\mathbf{b})^\top(A\mathbf{x}-\mathbf{b})$ and differentiate. (b) Think about the eigenvalue ratio of $A^\top A$.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Derivation: MML Example 7.2, pp. 230

**(a)** $f(\mathbf{x}) = \mathbf{x}^\top A^\top A \mathbf{x} - 2\mathbf{b}^\top A \mathbf{x} + \mathbf{b}^\top\mathbf{b}$

$$\nabla_\mathbf{x} f = 2(A\mathbf{x} - \mathbf{b})^\top A$$

> 📚 MML Eq. 7.10

**(b)** $\kappa = \sigma_{\max}/\sigma_{\min}$ measures the ratio of most vs. least curved direction. Large $\kappa$ = long narrow valley → gradient descent zigzags. Convergence rate: $\left(\frac{\kappa-1}{\kappa+1}\right)^2$ — when $\kappa \gg 1$ this approaches 1, meaning very slow convergence.

</details>

---

## Quick Reference (速查表)

| Concept          | Formula                                                                              | Source                    | Used In        |
| ---------------- | ------------------------------------------------------------------------------------ | ------------------------- | -------------- |
| GD update rule   | $\mathbf{x}_{i+1} = \mathbf{x}_i - \gamma(\nabla f)^\top$                            | MML §7.1, Eq. 7.6         | All training   |
| Momentum         | $\mathbf{x}_{i+1} = \mathbf{x}_i - \gamma(\nabla f)^\top + \alpha\Delta\mathbf{x}_i$ | MML §7.1.2, Eq. 7.11      | CNN, RNN       |
| SGD objective    | $L(\theta) = \sum_{n=1}^N L_n(\theta)$                                               | MML §7.1.3, Eq. 7.13      | Large-scale ML |
| Linear reg. grad | $\nabla = 2(A\mathbf{x}-\mathbf{b})^\top A$                                          | MML Example 7.2, Eq. 7.10 | Regression     |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation          | Pages       |
| ------- | -------- | ------------------------- | ----------- |
| §1      | MML      | §7.1, Eq. 7.4–7.6         | pp. 227–229 |
| §1.5    | MML      | Example 7.1               | p. 228      |
| §2      | MML      | §7.1.1                    | pp. 229–230 |
| §3      | MML      | §7.1.2, Eq. 7.11–7.12     | pp. 230–231 |
| §4      | MML      | §7.1.3, Eq. 7.13–7.15     | pp. 231–232 |
| §4 P5   | MML      | Example 7.2, Eq. 7.9–7.10 | p. 230      |
