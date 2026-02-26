# Vectors & Matrices | 向量与矩阵运算

> **Purpose:** Core linear algebra operations used in nearly every ML algorithm — matrix-vector products, transposes, and inverses.
> **Primary Source:** MML Ch2 — Deisenroth et al.
> **See also:** [inner_product.md](inner_product.md) | [norms_distances.md](norms_distances.md)
> **Prerequisites:** None (this is the starting point)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^n$ | set of all $n$-dimensional real vectors | $n$ 维实数向量集 |
| $\mathbb{R}^{m \times n}$ | set of all $m \times n$ real matrices | $m \times n$ 实数矩阵集 |
| $\mathbb{N}$ | set of natural numbers (positive integers) | 自然数集（正整数） |

---

## §1 Vectors (向量)

> 📚 Source: MML §2.1–2.2, pp. 25–32 — Deisenroth et al.

### 1.1 Definition (定义)

A vector is an ordered list of numbers.

向量是有序数列。

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $\mathbf{x}$ | a vector | 一个向量 | $\mathbb{R}^n$ |
| $x_i$ | i-th element of $\mathbf{x}$ | $\mathbf{x}$ 的第 $i$ 个分量 | $\mathbb{R}$ |
| $n$ | dimension (number of elements) | 维度（元素个数） | $\mathbb{N}$ |

> 📖 "$\mathbf{x} \in \mathbb{R}^n$" means "$\mathbf{x}$ is a vector with $n$ real-number entries."

$$
\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix} \in \mathbb{R}^n
$$

### 1.2 Basic Operations (基本运算)

> 📚 MML §2.2, Eq. 2.12–2.14

**Vector Addition (向量加法):** element-wise

$$
\mathbf{x} + \mathbf{y} = \begin{bmatrix} x_1 + y_1 \\ \vdots \\ x_n + y_n \end{bmatrix}
$$

**Scalar Multiplication (标量乘法):** multiply every element by $\lambda$

$$
\lambda \mathbf{x} = \begin{bmatrix} \lambda x_1 \\ \vdots \\ \lambda x_n \end{bmatrix}
$$

> 🔗 **Course Connection:**
> - **ML W3 CNN:** Input images are flattened into vectors; weight matrices multiply these vectors
> - **ML W4 RNN:** Hidden state $h_t$ is a vector updated at each time step

---

## §2 Matrices (矩阵)

> 📚 Source: MML §2.2, pp. 28–32 — Deisenroth et al.

### 2.1 Definition (定义)

A matrix is a rectangular array of numbers arranged in rows and columns.

矩阵是按行列排列的数字矩形阵列。

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $A$ | a matrix | 一个矩阵 | $\mathbb{R}^{m \times n}$ |
| $a_{ij}$ | element at row $i$, column $j$ | 第 $i$ 行第 $j$ 列元素 | $\mathbb{R}$ |
| $m$ | number of rows | 行数 | $\mathbb{N}$ |
| $n$ | number of columns | 列数 | $\mathbb{N}$ |

$$
A = \begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{bmatrix} \in \mathbb{R}^{m \times n}
$$

### 2.2 Matrix Multiplication (矩阵乘法)

> 📚 MML §2.2, Eq. 2.15

The product $C = AB$ where $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{n \times p}$ gives $C \in \mathbb{R}^{m \times p}$:

$$
c_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}
$$

> 🔑 $(m \times \mathbf{n}) \cdot (\mathbf{n} \times p) = (m \times p)$ — inner dimensions must match.
> 内维度必须匹配。

### 2.3 Transpose (转置)

> 📚 MML §2.2

Swap rows and columns: if $A \in \mathbb{R}^{m \times n}$, then $A^\top \in \mathbb{R}^{n \times m}$ with $(A^\top)_{ij} = a_{ji}$.

交换行列：$(A^\top)_{ij} = a_{ji}$。

**Properties:**

- $(A^\top)^\top = A$
- $(AB)^\top = B^\top A^\top$ — order reverses (顺序反转)

### 2.4 Inverse (逆矩阵)

> 📚 MML §2.2, Def. 2.3

For a square matrix $A \in \mathbb{R}^{n \times n}$, the inverse $A^{-1}$ satisfies:

$$
A A^{-1} = A^{-1} A = I
$$

where $I$ is the identity matrix. Exists only when $\det(A) \neq 0$.

逆矩阵只有在行列式非零时存在。

### 2.5 Worked Example (手算例题)

**Problem:** Compute $AB$ where:

$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}, \quad B = \begin{bmatrix} 5 \\ 6 \end{bmatrix}
$$

**Solution:**

$$
AB = \begin{bmatrix} 1 \cdot 5 + 2 \cdot 6 \\ 3 \cdot 5 + 4 \cdot 6 \end{bmatrix} = \begin{bmatrix} 17 \\ 39 \end{bmatrix}
$$

### 2.6 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Given $\mathbf{x} = [2, -1, 3]^\top$ and $\mathbf{y} = [1, 4, -2]^\top$, compute $\mathbf{x} + \mathbf{y}$ and $3\mathbf{x}$.

给定 $\mathbf{x} = [2, -1, 3]^\top$，$\mathbf{y} = [1, 4, -2]^\top$，计算 $\mathbf{x} + \mathbf{y}$ 和 $3\mathbf{x}$。

> 📐 Original Problem

<details><summary>💡 Hint</summary>

Vector addition and scalar multiplication are element-wise.

</details>

<details><summary>✅ Solution</summary>

$\mathbf{x} + \mathbf{y} = [3, 3, 1]^\top, \quad 3\mathbf{x} = [6, -3, 9]^\top$

</details>

#### 🟡 Medium | 中等题

**P2.** Verify that $(AB)^\top = B^\top A^\top$ for:

$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}, \quad B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}
$$

验证 $(AB)^\top = B^\top A^\top$。

> 📐 Original Problem

<details><summary>💡 Hint</summary>

Compute $AB$ first, transpose it, then compute $B^\top A^\top$ separately and compare.

</details>

<details><summary>✅ Solution</summary>

$$
AB = \begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}, \quad (AB)^\top = \begin{bmatrix} 19 & 43 \\ 22 & 50 \end{bmatrix}
$$

$$
B^\top A^\top = \begin{bmatrix} 5 & 7 \\ 6 & 8 \end{bmatrix} \begin{bmatrix} 1 & 3 \\ 2 & 4 \end{bmatrix} = \begin{bmatrix} 19 & 43 \\ 22 & 50 \end{bmatrix} \quad \checkmark
$$

</details>

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Vector addition | $\mathbf{x}+\mathbf{y}$ element-wise | MML §2.2 | All |
| Matrix multiply | $c_{ij}=\sum_{k} a_{ik} b_{kj}$ | MML §2.2 | CNN(W3), RNN(W4) |
| Transpose | $(AB)^\top = B^\top A^\top$ | MML §2.2 | Gradient computation |
| Inverse | $AA^{-1}=I$ | MML §2.2 | Linear regression |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Section | Pages |
| --- | --- | --- | --- |
| §1 | MML | §2.1–2.2 | pp. 25–32 |
| §2 | MML | §2.2 | pp. 28–32 |
