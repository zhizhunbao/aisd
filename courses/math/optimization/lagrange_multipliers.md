# Lagrange Multipliers & KKT | 拉格朗日乘子与 KKT

> **Purpose:** Lagrange multipliers convert constrained optimization into unconstrained problems — the mathematical foundation of SVM's dual formulation.
> **Primary Source:** MML §7.2–7.3 — Deisenroth et al.
> **See also:** [gradient_descent.md](gradient_descent.md) | [inner_product.md](../linear-algebra/inner_product.md)
> **Prerequisites:** [derivatives.md](../calculus/derivatives.md), [gradient_descent.md](gradient_descent.md)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^D$ | set of all $D$-dimensional real vectors | $D$ 维实数向量集 |

---

## §1 Constrained Optimization (约束优化)

> 📚 Source: MML §7.2, Eq. 7.16–7.17, pp. 233–234 — Deisenroth et al.

### 1.1 Problem Setup (问题设定)

Often we need to minimize a function **subject to constraints** — the solution must satisfy certain conditions (我们经常需要在满足约束条件下最小化函数):

| Symbol            | Meaning (EN)                    | 含义 (中文)        | Type                               |
| ----------------- | ------------------------------- | ------------------ | ---------------------------------- |
| $f(\mathbf{x})$   | objective function to minimize  | 要最小化的目标函数 | $\mathbb{R}^D \to \mathbb{R}$      |
| $g_i(\mathbf{x})$ | inequality constraint functions | 不等式约束函数     | $g_i: \mathbb{R}^D \to \mathbb{R}$ |
| $m$               | number of constraints           | 约束个数           | integer                            |

$$\min_{\mathbf{x}} f(\mathbf{x}) \quad \text{subject to} \quad g_i(\mathbf{x}) \leq 0, \quad i = 1, \ldots, m$$

> 📚 MML Eq. 7.17

### 1.2 Intuition (直觉理解)

Without constraints, we just follow the gradient downhill. With constraints, the optimal point might be on the **boundary** of the feasible region — like finding the lowest point on a hilltop while staying inside a fence.

没有约束时，跟着梯度下山就行。有约束时，最优解可能在可行域的**边界**上 —— 就像在围栏内找最低点。

> 📚 MML Fig. 7.4 illustrates box constraints

### 1.3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Identify the objective function $f$, the constraint function $g$, and rewrite in standard form ($g \leq 0$): "Minimize $x^2 + y^2$ subject to $x + y \geq 2$."
找出目标函数 $f$、约束函数 $g$，并改写为标准形式。

> 📐 Original Problem — applies MML Eq. 7.17

<details><summary>💡 Hint / 提示</summary>

$f(x,y) = x^2+y^2$. For "$\geq$" constraints, multiply by $-1$ to get "$\leq 0$".

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Method: MML §7.2, Eq. 7.17

- **Objective:** $f(x,y) = x^2 + y^2$
- **Constraint:** $x + y \geq 2$ → rewrite as $g(x,y) = 2 - x - y \leq 0$

Standard form: $\min_{x,y} (x^2+y^2)$ subject to $2-x-y \leq 0$.

</details>

#### 🟡 Medium | 中等题

**P2.** For the problem "minimize $x^2$ subject to $x \geq 3$": (a) What is the unconstrained minimum? (b) Is it feasible? (c) What is the constrained minimum?
最小化 $x^2$，约束 $x \geq 3$：(a) 无约束最小值？(b) 可行吗？(c) 有约束最小值？

> 📐 Original Problem — builds intuition for §1.2

<details><summary>✅ Solution / 解答</summary>

**(a)** Unconstrained minimum: $x^* = 0$, $f = 0$.

**(b)** Check feasibility: $0 \geq 3$? **No** — the unconstrained solution is **infeasible**.

**(c)** The constraint forces $x \geq 3$, so the constrained minimum is at the boundary: $x^* = 3$, $f = 9$.

> 🔑 This illustrates why constrained optimization matters: the "best" unconstrained answer may violate the constraints.

</details>

---

## §2 The Lagrangian (拉格朗日函数)

> 📚 Source: MML §7.2, Eq. 7.20a–7.20b, pp. 234–235

### 2.1 Constructing the Lagrangian (构造拉格朗日函数)

The idea: replace the hard constraint with a **penalty term** using a multiplier $\lambda_i$ for each constraint (用乘子 $\lambda_i$ 把硬约束变成惩罚项):

| Symbol                                          | Meaning (EN)                  | 含义 (中文)                 | Constraint                              |
| ----------------------------------------------- | ----------------------------- | --------------------------- | --------------------------------------- |
| $\lambda_i$                                     | Lagrange multiplier for $g_i$ | 第 $i$ 个约束的拉格朗日乘子 | $\lambda_i \geq 0$                      |
| $\boldsymbol{\lambda}$                          | vector of all multipliers     | 所有乘子组成的向量          | $\boldsymbol{\lambda} \in \mathbb{R}^m$ |
| $\mathcal{L}(\mathbf{x}, \boldsymbol{\lambda})$ | the Lagrangian                | 拉格朗日函数                | $\mathbb{R}^{D+m} \to \mathbb{R}$       |

$$\mathcal{L}(\mathbf{x}, \boldsymbol{\lambda}) = f(\mathbf{x}) + \sum_{i=1}^{m} \lambda_i g_i(\mathbf{x}) = f(\mathbf{x}) + \boldsymbol{\lambda}^\top \mathbf{g}(\mathbf{x})$$

> 📚 MML Eq. 7.20a–7.20b, citing Boyd & Vandenberghe (2004), Ch. 4

> 📖 **Reading the notation:** "$\boldsymbol{\lambda}^\top \mathbf{g}(\mathbf{x})$" — stack all constraints into a vector $\mathbf{g}$ and all multipliers into $\boldsymbol{\lambda}$, then take their dot product. This is just a compact way to write $\sum \lambda_i g_i$.

### 2.2 Why λ ≥ 0? (为什么 λ 非负?)

> 📐 补充推导 (Supplementary — not from textbook)

If $g_i(\mathbf{x}) \leq 0$ (constraint satisfied), the penalty $\lambda_i g_i \leq 0$ — it **decreases** the Lagrangian, which is fine. If the constraint is violated ($g_i > 0$), increasing $\lambda_i$ **increases** the Lagrangian, penalizing the violation. This "adversarial" interplay between $\mathbf{x}$ (minimizing) and $\boldsymbol{\lambda}$ (maximizing penalty) enforces the constraints.

### 2.3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P3.** Write the Lagrangian for: $\min x^2 + y^2$ subject to $x + y \leq 1$.
写出拉格朗日函数。

> 📐 Original Problem — applies MML Eq. 7.20

<details><summary>💡 Hint / 提示</summary>

Rewrite the constraint as $g(x,y) = x + y - 1 \leq 0$. Add $\lambda \cdot g$ to the objective.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Method: MML §7.2, Eq. 7.20a

Constraint: $g(x,y) = x + y - 1 \leq 0$

$$\mathcal{L}(x, y, \lambda) = x^2 + y^2 + \lambda(x + y - 1), \quad \lambda \geq 0$$

</details>

#### 🟡 Medium | 中等题

**P4.** For the Lagrangian in P3, find the optimal solution: (a) compute $\nabla_x \mathcal{L} = 0$ and $\nabla_y \mathcal{L} = 0$, (b) check whether the constraint is active.
求解 P3 的最优解。

> 📐 Original Problem — applies MML §7.2 method

<details><summary>💡 Hint / 提示</summary>

Set partial derivatives to zero: $2x + \lambda = 0$, $2y + \lambda = 0$. This gives $x = y$. Check if the unconstrained minimum $(0,0)$ satisfies $g \leq 0$.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Method: MML §7.2 — Lagrange multiplier approach

$\frac{\partial \mathcal{L}}{\partial x} = 2x + \lambda = 0 \implies x = -\lambda/2$

$\frac{\partial \mathcal{L}}{\partial y} = 2y + \lambda = 0 \implies y = -\lambda/2$

So $x = y = -\lambda/2$.

**Check:** Unconstrained minimum $(0,0)$ satisfies $0 + 0 -1 = -1 \leq 0$ ✓. Constraint is **inactive**, so $\lambda = 0$.

**Answer:** $(x^*, y^*) = (0, 0)$, $\lambda^* = 0$, $f^* = 0$.

If the constraint were $x + y \leq -1$ (tighter), the unconstrained min violates it, and we'd need $\lambda > 0$, giving $x = y = -1/2$, $f = 1/2$.

</details>

---

## §3 Lagrangian Duality (拉格朗日对偶)

> 📚 Source: MML §7.2, Eq. 7.22–7.27, pp. 234–235

### 3.1 Primal and Dual (原始与对偶)

> 📚 MML Definition 7.1, p. 234

The **primal** problem minimizes over $\mathbf{x}$ with constraints. The **dual** problem maximizes over $\boldsymbol{\lambda}$:

| Problem    | Formula                                                                                                                                                      | Optimization                         |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| **Primal** | $\min_\mathbf{x} f(\mathbf{x})$ s.t. $g_i(\mathbf{x}) \leq 0$                                                                                                | minimize over $\mathbf{x}$           |
| **Dual**   | $\max_{\boldsymbol{\lambda} \geq 0} D(\boldsymbol{\lambda})$ where $D(\boldsymbol{\lambda}) = \min_\mathbf{x} \mathcal{L}(\mathbf{x}, \boldsymbol{\lambda})$ | maximize over $\boldsymbol{\lambda}$ |

### 3.2 Weak Duality (弱对偶)

> 📚 MML Eq. 7.27

The dual value is always a **lower bound** on the primal value:

$$\max_{\boldsymbol{\lambda} \geq 0} \min_{\mathbf{x}} \mathcal{L}(\mathbf{x}, \boldsymbol{\lambda}) \leq \min_{\mathbf{x}} \max_{\boldsymbol{\lambda} \geq 0} \mathcal{L}(\mathbf{x}, \boldsymbol{\lambda})$$

This follows from the **minimax inequality** (MML Eq. 7.23).

### 3.3 Strong Duality (强对偶)

> 📚 MML §7.3, p. 236

For **convex** optimization problems, weak duality becomes **equality** — the primal and dual solutions are the same. This is why SVM can be solved via its dual form.

### 3.4 Connection to Course (课程关联)

> 🔗 **Course Connection:**
>
> - **ML W2 SVM:** The SVM primal $\min \frac{1}{2}\|\mathbf{w}\|^2$ s.t. $y_i(\mathbf{w}^\top\mathbf{x}_i + b) \geq 1$ is converted to its dual using Lagrange multipliers. The dual involves only dot products $\mathbf{x}_i^\top\mathbf{x}_j$, enabling the kernel trick (MML §12.2–12.3).

### 3.5 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P5.** State whether each statement is true or false: (a) The dual optimal value can be larger than the primal optimal value. (b) For convex problems, primal = dual. (c) λ can be negative.
判断真假：(a) 对偶最优值能大于原始最优值？(b) 凸问题原始=对偶？(c) λ 可以为负？

> 📐 Original Problem — conceptual check on MML §7.2–7.3

<details><summary>✅ Solution / 解答</summary>

**(a) False.** Weak duality guarantees $\text{dual} \leq \text{primal}$. (MML Eq. 7.27)

**(b) True.** Strong duality holds for convex problems. (MML §7.3)

**(c) False.** For inequality constraints $g_i \leq 0$, we require $\lambda_i \geq 0$. (MML Eq. 7.20)

</details>

---

## §4 Quadratic Programming (二次规划)

> 📚 Source: MML §7.3.2, Eq. 7.45–7.52, pp. 241–242

### 4.1 Standard Form (标准形式)

The SVM optimization is a **quadratic program** — quadratic objective with linear constraints:

| Symbol       | Meaning (EN)              | 含义 (中文)  |
| ------------ | ------------------------- | ------------ |
| $Q$          | positive definite matrix  | 正定矩阵     |
| $\mathbf{c}$ | linear coefficient vector | 线性系数向量 |
| $A$          | constraint matrix         | 约束矩阵     |

$$\min_{\mathbf{x}} \frac{1}{2}\mathbf{x}^\top Q \mathbf{x} + \mathbf{c}^\top \mathbf{x} \quad \text{s.t.} \quad A\mathbf{x} \leq \mathbf{b}$$

> 📚 MML Eq. 7.45

### 4.2 Lagrangian and Dual (拉格朗日与对偶)

> 📚 MML Eq. 7.48–7.52

$$\mathcal{L}(\mathbf{x}, \boldsymbol{\lambda}) = \frac{1}{2}\mathbf{x}^\top Q\mathbf{x} + (\mathbf{c} + A^\top\boldsymbol{\lambda})^\top\mathbf{x} - \boldsymbol{\lambda}^\top\mathbf{b}$$

Setting $\nabla_\mathbf{x}\mathcal{L} = 0$: $Q\mathbf{x} + \mathbf{c} + A^\top\boldsymbol{\lambda} = 0 \implies \mathbf{x} = -Q^{-1}(\mathbf{c} + A^\top\boldsymbol{\lambda})$

Substituting back gives the **dual**:

$$\max_{\boldsymbol{\lambda} \geq 0} -\frac{1}{2}(\mathbf{c}+A^\top\boldsymbol{\lambda})^\top Q^{-1}(\mathbf{c}+A^\top\boldsymbol{\lambda}) - \boldsymbol{\lambda}^\top\mathbf{b}$$

> 📚 MML Eq. 7.52

### 4.3 Practice Problems (练习题)

#### 🔴 Hard | 挑战题

**P6.** The SVM primal is: $\min_{\mathbf{w},b} \frac{1}{2}\|\mathbf{w}\|^2$ s.t. $y_i(\mathbf{w}^\top\mathbf{x}_i + b) \geq 1$ for all $i$. (a) Rewrite the constraints in $g_i \leq 0$ form. (b) Write the Lagrangian. (c) Find $\frac{\partial \mathcal{L}}{\partial \mathbf{w}} = 0$ and explain what it means.
SVM 原始问题：(a) 改写约束；(b) 写拉格朗日函数；(c) 求 $\partial \mathcal{L}/\partial \mathbf{w} = 0$ 并解释含义。

> 📚 From: MML §12.2, Eq. 12.12–12.16

<details><summary>💡 Hint / 提示</summary>

(a) $y_i(\mathbf{w}^\top\mathbf{x}_i + b) \geq 1$ becomes $1 - y_i(\mathbf{w}^\top\mathbf{x}_i + b) \leq 0$. (c) The result shows $\mathbf{w}$ is a linear combination of training data weighted by $\alpha_i y_i$.

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Derivation: MML §12.2, pp. 380–388

**(a)** $g_i(\mathbf{w}, b) = 1 - y_i(\mathbf{w}^\top\mathbf{x}_i + b) \leq 0$

**(b)** $\mathcal{L}(\mathbf{w}, b, \boldsymbol{\alpha}) = \frac{1}{2}\|\mathbf{w}\|^2 + \sum_{i=1}^N \alpha_i \left[1 - y_i(\mathbf{w}^\top\mathbf{x}_i + b)\right]$, where $\alpha_i \geq 0$.

**(c)** $\frac{\partial \mathcal{L}}{\partial \mathbf{w}} = \mathbf{w} - \sum_{i=1}^N \alpha_i y_i \mathbf{x}_i = 0$

$$\implies \mathbf{w} = \sum_{i=1}^N \alpha_i y_i \mathbf{x}_i$$

**Meaning:** $\mathbf{w}$ is a **weighted sum of training points**. Only points with $\alpha_i > 0$ contribute — these are the **support vectors**. The decision boundary depends only on these critical points, not all data.

> 📚 MML Eq. 12.16

</details>

---

## §5 Equality Constraints (等式约束)

> 📚 Source: MML §7.2 Remark, Eq. 7.28, p. 235

For equality constraints $h_j(\mathbf{x}) = 0$, we add them to the Lagrangian with **unconstrained** multipliers (不要求非负):

$$\mathcal{L}(\mathbf{x}, \boldsymbol{\lambda}, \boldsymbol{\nu}) = f(\mathbf{x}) + \sum_{i=1}^m \lambda_i g_i(\mathbf{x}) + \sum_{j=1}^n \nu_j h_j(\mathbf{x})$$

> 📖 **Why unconstrained?** An equality $h = 0$ is equivalent to two inequalities $h \leq 0$ AND $-h \leq 0$. Combining the two $\lambda$'s (both $\geq 0$) gives an unconstrained $\nu = \lambda_+ - \lambda_-$.

### 5.1 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P7.** Write the Lagrangian for: $\min x^2 + y^2$ subject to $x + y = 4$ (equality constraint).
写出等式约束的拉格朗日函数。

> 📐 Original Problem — applies MML Eq. 7.28

<details><summary>✅ Solution / 解答</summary>

> 📚 Method: MML §7.2 Remark, Eq. 7.28

Constraint: $h(x,y) = x + y - 4 = 0$

$$\mathcal{L}(x, y, \nu) = x^2 + y^2 + \nu(x + y - 4)$$

Note: $\nu$ is **unconstrained** (no $\nu \geq 0$ requirement), unlike inequality multipliers $\lambda \geq 0$.

Setting $\partial\mathcal{L}/\partial x = 2x+\nu = 0$ and $\partial\mathcal{L}/\partial y = 2y+\nu = 0$ gives $x = y = -\nu/2$. Substituting into $x+y=4$: $-\nu = 4$, so $\nu = -4$, $x = y = 2$, $f = 8$.

</details>

---

## Quick Reference (速查表)

| Concept        | Formula                                                                                                      | Source               | Used In  |
| -------------- | ------------------------------------------------------------------------------------------------------------ | -------------------- | -------- |
| Lagrangian     | $\mathcal{L} = f + \sum \lambda_i g_i$                                                                       | MML §7.2, Eq. 7.20   | SVM dual |
| Weak duality   | $\max\min \leq \min\max$                                                                                     | MML §7.2, Eq. 7.27   | Theory   |
| Strong duality | Equality for convex problems                                                                                 | MML §7.3             | SVM      |
| QP             | $\min \frac{1}{2}\mathbf{x}^\top Q\mathbf{x} + \mathbf{c}^\top\mathbf{x}$ s.t. $A\mathbf{x} \leq \mathbf{b}$ | MML §7.3.2, Eq. 7.45 | SVM      |
| SVM weight     | $\mathbf{w} = \sum \alpha_i y_i \mathbf{x}_i$                                                                | MML §12.2, Eq. 12.16 | SVM dual |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation          | Pages       |
| ------- | -------- | ------------------------- | ----------- |
| §1      | MML      | §7.2, Eq. 7.16–7.17       | pp. 233–234 |
| §2      | MML      | §7.2, Eq. 7.20a–7.20b     | pp. 234–235 |
| §3      | MML      | §7.2, Eq. 7.22–7.27; §7.3 | pp. 234–236 |
| §4      | MML      | §7.3.2, Eq. 7.45–7.52     | pp. 241–242 |
| §4 P6   | MML      | §12.2, Eq. 12.12–12.16    | pp. 380–388 |
| §5      | MML      | §7.2 Remark, Eq. 7.28     | p. 235      |
