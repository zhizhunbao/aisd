# Eigenvalues & SVD | 特征值与 SVD

> **Purpose:** Eigendecomposition and SVD are the backbone of PCA (dimensionality reduction) and matrix approximation.
> **Primary Source:** MML §4.1–4.5 — Deisenroth et al.
> **See also:** [vectors_matrices.md](vectors_matrices.md)
> **Prerequisites:** [vectors_matrices.md](vectors_matrices.md), [inner_product.md](inner_product.md)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^n$ | set of all $n$-dimensional real vectors | $n$ 维实数向量集 |
| $\mathbb{R}^{m \times n}$ | set of all $m \times n$ real matrices | $m \times n$ 实数矩阵集 |

---

## §1 Eigenvalues and Eigenvectors (特征值与特征向量)

> 📚 Source: MML §4.2, pp. 105–113 — Definition 4.6

### 1.1 Definition (定义)

For a square matrix $A \in \mathbb{R}^{n \times n}$, an eigenvector is a non-zero vector that only gets scaled (not rotated) when multiplied by $A$.

特征向量是被 $A$ 只缩放不旋转的非零向量。

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $A$ | square matrix | 方阵 | $\mathbb{R}^{n \times n}$ |
| $\mathbf{x}$ | eigenvector | 特征向量 | $\mathbb{R}^n \setminus \{\mathbf{0}\}$ |
| $\lambda$ | eigenvalue (scaling factor) | 特征值（缩放因子） | $\mathbb{R}$ |

$A\mathbf{x} = \lambda \mathbf{x}$

> 📚 MML Def. 4.6, Eq. 4.25

> 📖 "$A\mathbf{x} = \lambda \mathbf{x}$" means "when matrix $A$ acts on vector $\mathbf{x}$, the result is just $\mathbf{x}$ scaled by $\lambda$."

### 1.2 How to Find Eigenvalues (如何求特征值)

> 📚 MML §4.2, Theorem 4.8, pp. 106–107

**Step 1:** Solve the characteristic polynomial:

$\det(A - \lambda I) = 0$

**Step 2:** Each root $\lambda_i$ is an eigenvalue. Then solve $(A - \lambda_i I)\mathbf{x} = \mathbf{0}$ for eigenvectors.

### 1.3 Worked Example (手算例题)

> 📚 MML Example 4.5, pp. 107–108

**Problem:** Find eigenvalues and eigenvectors of:

$$A = \begin{bmatrix} 4 & 2 \\ 1 & 3 \end{bmatrix}$$

**Solution:**

$\det(A - \lambda I) = (4-\lambda)(3-\lambda) - 2 = \lambda^2 - 7\lambda + 10 = (\lambda-2)(\lambda-5) = 0$

$\lambda_1 = 2, \quad \lambda_2 = 5$

For $\lambda_2 = 5$: $(A - 5I)\mathbf{x} = \mathbf{0}$

$$E_5 = \text{span}\left[\begin{bmatrix}2\\1\end{bmatrix}\right]$$

For $\lambda_1 = 2$: $(A - 2I)\mathbf{x} = \mathbf{0}$

$$E_2 = \text{span}\left[\begin{bmatrix}1\\-1\end{bmatrix}\right]$$

### 1.4 Key Properties (关键性质)

> 📚 MML §4.2, Theorems 4.16–4.17

| Property | Formula | 含义 |
| --- | --- | --- |
| $\det(A) = \prod \lambda_i$ | Determinant = product of eigenvalues | 行列式 = 特征值之积 |
| $\text{tr}(A) = \sum \lambda_i$ | Trace = sum of eigenvalues | 迹 = 特征值之和 |
| Symmetric ⇒ real eigenvalues | MML Theorem 4.15 (Spectral Theorem) | 对称矩阵特征值都是实数 |

---

## §2 Singular Value Decomposition (奇异值分解)

> 📚 Source: MML §4.5, pp. 125–134

### 2.1 Definition (定义)

SVD decomposes any matrix $A \in \mathbb{R}^{m \times n}$ (not just square!) into three matrices.

SVD 把任意矩阵分解为三个矩阵。

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $U$ | left singular vectors | 左奇异向量 | $\mathbb{R}^{m \times m}$, orthogonal |
| $\Sigma$ | singular values (diagonal) | 奇异值（对角） | $\mathbb{R}^{m \times n}$ |
| $V$ | right singular vectors | 右奇异向量 | $\mathbb{R}^{n \times n}$, orthogonal |
| $\sigma_i$ | i-th singular value | 第 i 个奇异值 | $\geq 0$ |

$A = U \Sigma V^\top$

> 📚 MML §4.5, Theorem 4.22

### 2.2 Relationship to Eigendecomposition (与特征分解的关系)

> 📚 MML §4.5, pp. 127–128

| | Eigendecomposition | SVD |
| --- | --- | --- |
| Input | Square matrix only | Any matrix |
| Formula | $A = P D P^{-1}$ | $A = U\Sigma V^\top$ |
| Connection | Eigenvalues of $A^\top A$ | $\sigma_i^2$ are eigenvalues of $A^\top A$ |

The singular values $\sigma_i$ are the square roots of the eigenvalues of $A^\top A$.

奇异值是 $A^\top A$ 的特征值的平方根。

### 2.3 Low-Rank Approximation (低秩近似)

> 📚 MML §4.6, pp. 135–139

Keep only the $k$ largest singular values to get the best rank-$k$ approximation.

保留最大的 $k$ 个奇异值，得到最佳秩-$k$ 近似。

$A_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^\top$

> 🔑 This is the mathematical basis of PCA: project data onto the top-$k$ eigenvectors of the covariance matrix.
> 这是 PCA 的数学基础：将数据投影到协方差矩阵的前 $k$ 个特征向量上。

> 🔗 **Course Connection:**
> - **PCA:** Eigendecomposition of the covariance matrix $\frac{1}{N}X^\top X$ gives principal components. SVD of the centered data matrix does the same thing.
> - **ML W6 EM/GMM:** Covariance matrix eigenvalues describe cluster shape (elongated vs circular).

---

## §3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Find the eigenvalues of:

$$A = \begin{bmatrix} 3 & 0 \\ 0 & 5 \end{bmatrix}$$

求对角矩阵的特征值。

> 📐 Original Problem

<details><summary>💡 Hint</summary>

For a diagonal matrix, the eigenvalues are the diagonal entries.

</details>

<details><summary>✅ Solution</summary>

$\lambda_1 = 3, \quad \lambda_2 = 5$. Verify: $\det(A) = 15 = 3 \times 5$ ✓, $\text{tr}(A) = 8 = 3 + 5$ ✓.

</details>

#### 🟡 Medium | 中等题

**P2.** Given the following matrix, find eigenvalues, eigenvectors, and verify $\det(A) = \prod \lambda_i$.

$$A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$$

求特征值、特征向量，并验证行列式性质。

> 📐 Original Problem — based on MML §4.2

<details><summary>💡 Hint</summary>

$\det(A - \lambda I) = (2-\lambda)^2 - 1 = 0$.

</details>

<details><summary>✅ Solution</summary>

$(2-\lambda)^2 - 1 = 0 \implies \lambda^2 - 4\lambda + 3 = 0 \implies \lambda_1 = 1, \lambda_2 = 3$

$\lambda_1 = 1$: $(A-I)\mathbf{x}=\mathbf{0}$ → $\mathbf{x}_1 = [1, -1]^\top$

$\lambda_2 = 3$: $(A-3I)\mathbf{x}=\mathbf{0}$ → $\mathbf{x}_2 = [1, 1]^\top$

$\det(A) = 4 - 1 = 3 = 1 \times 3 = \lambda_1 \lambda_2$ ✓

</details>

---

## Quick Reference (速查表)

| Concept | Formula | Source | Used In |
| --- | --- | --- | --- |
| Eigenvalue equation | $A\mathbf{x} = \lambda\mathbf{x}$ | MML §4.2, Eq. 4.25 | PCA |
| Characteristic polynomial | $\det(A - \lambda I) = 0$ | MML §4.2, Thm. 4.8 | PCA |
| SVD | $A = U\Sigma V^\top$ | MML §4.5, Thm. 4.22 | PCA, low-rank approx. |
| $\det = \prod \lambda_i$ | MML Thm. 4.16 | — | Theory |
| $\text{tr} = \sum \lambda_i$ | MML Thm. 4.17 | — | Theory |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation | Pages |
| --- | --- | --- | --- |
| §1 | MML | §4.2, Def. 4.6, Eq. 4.25 | pp. 105–113 |
| §2 | MML | §4.5, Thm. 4.22 | pp. 125–134 |
| §2.3 | MML | §4.6 | pp. 135–139 |