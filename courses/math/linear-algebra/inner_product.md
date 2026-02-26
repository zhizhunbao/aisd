# Inner Product | 内积

> **Purpose:** Inner product (dot product) defines angles, orthogonality, and projections — key for SVM hyperplanes and cosine similarity.
> **Primary Source:** MML §3.2, §3.4 — Deisenroth et al.
> **See also:** [vectors_matrices.md](vectors_matrices.md) | [norms_distances.md](norms_distances.md)
> **Prerequisites:** [vectors_matrices.md](vectors_matrices.md)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^n$ | set of all $n$-dimensional real vectors | $n$ 维实数向量集 |

---

## §1 Dot Product (点积)

> 📚 Source: MML §3.2.1, p. 72 — Eq. 3.5

### 1.1 Definition (定义)

The dot product of two vectors multiplies corresponding elements and sums the results.

点积将两个向量的对应元素相乘再求和。

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $\mathbf{x}, \mathbf{y}$ | two vectors | 两个向量 | $\mathbb{R}^n$ |
| $x_i, y_i$ | i-th elements | 第 i 个分量 | $\mathbb{R}$ |
| $\mathbf{x}^\top \mathbf{y}$ | dot product result | 点积结果 | $\mathbb{R}$ |

$\mathbf{x}^\top \mathbf{y} = \sum_{i=1}^{n} x_i y_i$

> 📖 "$\mathbf{x}^\top \mathbf{y}$" reads "x transpose times y." The transpose turns the column vector into a row, making the multiplication a `(1×n)(n×1) = scalar`.

### 1.2 Intuition (直觉理解)

The dot product measures how much two vectors point in the same direction.

点积衡量两个向量在同一方向上的对齐程度。

- Large positive → pointing roughly the same way (大致同向)
- Zero → perpendicular / unrelated (垂直/无关)
- Large negative → pointing in opposite directions (大致反向)

### 1.3 Worked Example (手算例题)

> 📚 Adapted from MML §3.4, Example 3.6

**Problem:** Compute $\mathbf{x}^\top \mathbf{y}$ for $\mathbf{x} = [1, 1]^\top$, $\mathbf{y} = [1, 2]^\top$.

**Solution:**

$\mathbf{x}^\top \mathbf{y} = 1 \times 1 + 1 \times 2 = 3$

### 1.4 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Compute $\mathbf{x}^\top \mathbf{y}$ for $\mathbf{x} = [2, -1, 3]^\top$, $\mathbf{y} = [-1, 4, 2]^\top$. Are they orthogonal?

计算点积，判断是否正交。

> 📐 Original Problem

<details><summary>💡 Hint</summary>

Multiply corresponding elements and sum. Orthogonal iff result = 0.

</details>

<details><summary>✅ Solution</summary>

$\mathbf{x}^\top \mathbf{y} = 2(-1) + (-1)(4) + 3(2) = -2 - 4 + 6 = 0$

Yes, $\mathbf{x} \perp \mathbf{y}$ (orthogonal). ✓

</details>

---

## §2 General Inner Product (一般内积)

> 📚 Source: MML §3.2.2–3.2.3, pp. 72–74 — Definition 3.3

### 2.1 Definition (定义)

An inner product $\langle \cdot, \cdot \rangle$ is any function that takes two vectors and returns a number, satisfying three properties.

内积是取两个向量返回一个数的函数，满足三条性质。

| Property | Formula | 中文 |
| --- | --- | --- |
| Symmetric | $\langle \mathbf{x}, \mathbf{y} \rangle = \langle \mathbf{y}, \mathbf{x} \rangle$ | 对称性 |
| Linear | $\langle \alpha\mathbf{x} + \beta\mathbf{y}, \mathbf{z} \rangle = \alpha\langle \mathbf{x}, \mathbf{z} \rangle + \beta\langle \mathbf{y}, \mathbf{z} \rangle$ | 线性 |
| Positive definite | $\langle \mathbf{x}, \mathbf{x} \rangle \geq 0$; $= 0 \iff \mathbf{x} = \mathbf{0}$ | 正定性 |

> 📚 MML Def. 3.3, p. 73

The dot product is the simplest inner product. ML sometimes uses weighted inner products $\langle \mathbf{x}, \mathbf{y} \rangle = \mathbf{x}^\top A \mathbf{y}$ where $A$ is symmetric positive definite (SVM kernels use this idea).

点积是最简单的内积。ML 有时用加权内积（SVM kernel 的思路）。

### 2.2 Inner Products Induce Norms (内积诱导范数)

> 📚 Source: MML §3.3, Eq. 3.16

Every inner product gives you a norm (length) for free.

每个内积自动给你一个范数。

$\|\mathbf{x}\| := \sqrt{\langle \mathbf{x}, \mathbf{x} \rangle}$

For the dot product: $\|\mathbf{x}\|_2 = \sqrt{\mathbf{x}^\top \mathbf{x}}$ — this is the Euclidean norm.

---

## §3 Angles and Orthogonality (角度与正交)

> 📚 Source: MML §3.4, pp. 76–77 — Eq. 3.25, Def. 3.7

### 3.1 Angle Between Vectors (向量夹角)

| Symbol | Meaning (EN) | 含义 (中文) | Range |
| --- | --- | --- | --- |
| $\omega$ | angle between $\mathbf{x}$ and $\mathbf{y}$ | 夹角 | $[0, \pi]$ |

$\cos \omega = \frac{\langle \mathbf{x}, \mathbf{y} \rangle}{\|\mathbf{x}\| \, \|\mathbf{y}\|}$

For the dot product: $\cos \omega = \frac{\mathbf{x}^\top \mathbf{y}}{\|\mathbf{x}\|_2 \|\mathbf{y}\|_2}$

This is exactly cosine similarity from [norms_distances.md §3](norms_distances.md).

这就是余弦相似度。

### 3.2 Orthogonality (正交)

> 📚 MML Def. 3.7, p. 77

Two vectors $\mathbf{x}, \mathbf{y}$ are orthogonal (perpendicular) if and only if:

$\langle \mathbf{x}, \mathbf{y} \rangle = 0 \quad \text{(written } \mathbf{x} \perp \mathbf{y}\text{)}$

If additionally $\|\mathbf{x}\| = 1 = \|\mathbf{y}\|$, they are orthonormal (正交归一).

> 🔗 **Course Connection:**
> - **ML W2 SVM:** The hyperplane is defined by $\mathbf{w}^\top \mathbf{x} + b = 0$ — the weight vector $\mathbf{w}$ is orthogonal to the decision boundary. The margin = $\frac{2}{\|\mathbf{w}\|}$.
> - **ML W6 Clustering:** Cosine similarity = inner product of unit vectors. Used in text clustering.

### 3.3 Practice Problems (练习题)

#### 🟡 Medium | 中等题

**P3.** For $\mathbf{x} = [1, 1]^\top$ and $\mathbf{y} = [1, 2]^\top$, compute the angle $\omega$ between them using the dot product.

求 $\mathbf{x}$ 与 $\mathbf{y}$ 的夹角。

> 📚 From: MML §3.4, Example 3.6

<details><summary>💡 Hint</summary>

$\cos \omega = \frac{\mathbf{x}^\top \mathbf{y}}{\|\mathbf{x}\|_2 \|\mathbf{y}\|_2}$. Compute numerator and denominator separately.

</details>

<details><summary>✅ Solution</summary>

> 📚 MML §3.4, Eq. 3.25

$\mathbf{x}^\top \mathbf{y} = 3, \quad \|\mathbf{x}\| = \sqrt{2}, \quad \|\mathbf{y}\| = \sqrt{5}$

$\cos \omega = \frac{3}{\sqrt{2}\sqrt{5}} = \frac{3}{\sqrt{10}} \approx 0.949$

$\omega = \arccos(0.949) \approx 0.32 \text{ rad} \approx 18°$

</details>

#### 🔴 Hard | 挑战题

**P4.** In SVM, the decision boundary is $\mathbf{w}^\top \mathbf{x} + b = 0$. Explain geometrically why $\mathbf{w}$ is perpendicular to the boundary. Show that the distance from the origin to the hyperplane is $\frac{|b|}{\|\mathbf{w}\|}$.

解释为什么 $\mathbf{w}$ 垂直于决策边界，并证明原点到超平面的距离公式。

> 📐 Original Problem — connects MML §3.4 to SVM

<details><summary>💡 Hint</summary>

Take two points $\mathbf{x}_1, \mathbf{x}_2$ on the boundary. Show $\mathbf{w}^\top(\mathbf{x}_1 - \mathbf{x}_2) = 0$.

</details>

<details><summary>✅ Solution</summary>

**Part 1:** If $\mathbf{x}_1, \mathbf{x}_2$ are both on the boundary: $\mathbf{w}^\top \mathbf{x}_1 + b = 0$ and $\mathbf{w}^\top \mathbf{x}_2 + b = 0$. Subtract: $\mathbf{w}^\top(\mathbf{x}_1 - \mathbf{x}_2) = 0$. So $\mathbf{w} \perp (\mathbf{x}_1 - \mathbf{x}_2)$ for any two boundary points → $\mathbf{w}$ is normal to the boundary.

**Part 2:** The closest point on the boundary to origin is in the direction of $\mathbf{w}$: $\mathbf{x}_0 = t\frac{\mathbf{w}}{\|\mathbf{w}\|}$. Substitute into $\mathbf{w}^\top \mathbf{x}_0 + b = 0$:

$t \frac{\mathbf{w}^\top \mathbf{w}}{\|\mathbf{w}\|} + b = 0 \implies t\|\mathbf{w}\| = -b \implies t = \frac{-b}{\|\mathbf{w}\|}$

Distance $= |t| = \frac{|b|}{\|\mathbf{w}\|}$. $\blacksquare$

</details>

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Dot product | $\mathbf{x}^\top \mathbf{y} = \sum x_i y_i$ | MML §3.2.1, Eq. 3.5 | SVM, cosine sim. |
| Norm from inner product | $\|\mathbf{x}\| = \sqrt{\langle \mathbf{x}, \mathbf{x} \rangle}$ | MML §3.3, Eq. 3.16 | All |
| Cosine of angle | $\cos\omega = \frac{\langle \mathbf{x}, \mathbf{y} \rangle}{\|\mathbf{x}\|\|\mathbf{y}\|}$ | MML §3.4, Eq. 3.25 | Clustering |
| Orthogonality | $\langle \mathbf{x}, \mathbf{y} \rangle = 0$ | MML Def. 3.7 | SVM hyperplane |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation | Pages |
| --- | --- | --- | --- |
| §1 | MML | §3.2.1, Eq. 3.5 | p. 72 |
| §2 | MML | §3.2.2–3.2.3, Def. 3.3 | pp. 72–74 |
| §3 | MML | §3.4, Eq. 3.25, Def. 3.7 | pp. 76–77 |