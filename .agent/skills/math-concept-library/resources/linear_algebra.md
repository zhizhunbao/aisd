# Linear Algebra Concepts (线性代数概念)

---

### Affine Transformation (仿射变换)

**Tags:** `#linear-algebra` `#transformation` `#mv-week2`

**📌 One-line Definition:**

> An affine transformation is any geometric operation expressible as **y = Ax + b** (matrix multiplication + translation) — it can translate, rotate, scale, shear, or any combination, while preserving parallel lines and ratios.
>
> > 仿射变换是任何可以表示为**y = Ax + b**（矩阵乘法+平移）的几何操作 — 可以平移、旋转、缩放、剪切或任意组合，同时保持平行线和比例。

**📐 Formula:**

```
General form: y = Ax + b

In 2D with homogeneous coordinates:
[x']   [a₁₁  a₁₂  tx] [x]
[y'] = [a₂₁  a₂₂  ty] [y]
[1 ]   [ 0    0    1 ] [1]

OpenCV uses 2×3 matrix M:
M = [[a₁₁, a₁₂, tx],
     [a₂₁, a₂₂, ty]]
```

- A = 2×2 linear transformation matrix (rotation, scale, shear)
- b = (tx, ty) = translation vector
- M = combined 2×3 matrix used by `cv2.warpAffine()`

**Common transformation matrices:**

| Transform                   | Matrix M                              |
| --------------------------- | ------------------------------------- |
| Translation by (tx, ty)     | `[[1, 0, tx], [0, 1, ty]]`            |
| Scaling by (sx, sy)         | `[[sx, 0, 0], [0, sy, 0]]`            |
| Rotation by θ around origin | `[[cosθ, -sinθ, 0], [sinθ, cosθ, 0]]` |

**💡 Intuition (直觉理解):**

> **The rubber sheet analogy:**
>
> Imagine your image is printed on a rubber sheet pinned to a board:
>
> - **Translation** = slide the whole sheet (all pins move the same distance)
> - **Rotation** = pin one corner and spin
> - **Scaling** = stretch/compress the rubber
> - **Shearing** = push one edge sideways while holding the opposite edge
>
> **What's preserved:** Parallel lines stay parallel. Points on a straight line stay on a straight line. Distance ratios along a line stay the same.
>
> **What's NOT preserved:** Angles can change. Distances can change. Circles can become ellipses.
>
> > **橡胶片类比：**
> >
> > 想象你的图像印在一块钉在板上的橡胶片上：
> >
> > - **平移** = 滑动整块橡胶（所有钉子移动相同距离）
> > - **旋转** = 钉住一个角，旋转
> > - **缩放** = 拉伸/压缩橡胶
> > - **剪切** = 推一个边，同时固定对面的边
> >
> > **保持的：** 平行线保持平行。直线上的点保持在直线上。沿直线的距离比保持不变。
> >
> > **不保持的：** 角度可能改变。距离可能改变。圆可能变成椭圆。

**⚙️ In Practice (实际使用):**

```python
import cv2
import numpy as np

h, w = img.shape[:2]

# Translation: shift right 50px, down 30px
M_translate = np.float32([[1, 0, 50], [0, 1, 30]])
translated = cv2.warpAffine(img, M_translate, (w, h))

# Rotation: 45° around center, scale 1.0
center = (w // 2, h // 2)
M_rotate = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, M_rotate, (w, h))

# Scaling: simpler to use cv2.resize()
scaled = cv2.resize(img, None, fx=0.5, fy=0.5)
```

**🔗 Related Concepts:**
→ see: Matrix Multiplication (the core operation)

**📚 Appears In:**

- MV Week 2 §12 (Image Transformation Techniques)

---

### Covariance Matrix (协方差矩阵)

**Tags:** `#linear-algebra` `#statistics` `#ml-week1`

**📌 One-line Definition:**

> A square matrix showing how each pair of features varies together — positive means they increase together, negative means one increases as the other decreases.
>
> > 一个方阵，展示每对特征如何共同变化——正值表示同增同减，负值表示一增一减。

**📐 Formula:**

```
Cov(X, Y) = (1/n) × Σᵢ (xᵢ - x̄)(yᵢ - ȳ)

For d features, the covariance matrix C is d×d:
C[i][j] = Cov(feature_i, feature_j)
C[i][i] = Var(feature_i)  (diagonal = variances)
```

- The matrix is always symmetric: C[i][j] = C[j][i]
- Diagonal elements = variance of each feature
- Off-diagonal elements = covariance between two features

**💡 Intuition (直觉理解):**

> **The classroom analogy:** In a class, if students who score high on math also score high on physics (positive covariance), while those who score high on math tend to score low on art (negative covariance), the covariance matrix captures all these pairwise relationships in one table.
>
> > **课堂类比：** 如果数学分高的学生物理也高（正协方差），而数学高的艺术反而低（负协方差），协方差矩阵就在一张表中捕捉了所有这些配对关系。

**🔢 Worked Example:**

```
Iris data (4 features, standardized):

        sepal_L  sepal_W  petal_L  petal_W
sepal_L  [1.01   -0.11    0.87     0.82  ]
sepal_W  [-0.11   1.01   -0.42    -0.36  ]
petal_L  [0.87   -0.42    1.01     0.97  ]  ← High correlation with petal_W!
petal_W  [0.82   -0.36    0.97     1.01  ]

petal_L & petal_W have covariance 0.97 → nearly identical information
→ PCA can compress these into one principal component
```

**🔗 Related Concepts:**
→ see: PCA (Step 2 uses this matrix)
→ see: Eigenvalues/Eigenvectors (extracted from this matrix in PCA)

**📚 Appears In:**

- ML Week 1 §4.3 (PCA Step 2 — Calculate Covariance Matrix)

---

### Eigenvalues & Eigenvectors (特征值与特征向量)

**Tags:** `#linear-algebra` `#dimensionality_reduction` `#ml-week1`

**📌 One-line Definition:**

> Given a square matrix A, an eigenvector v is a non-zero vector whose direction doesn't change when multiplied by A (only scaled); the eigenvalue λ is the scaling factor. In PCA, eigenvectors give directions of maximum variance and eigenvalues give the amount of variance.
>
> > 给定方阵 A，特征向量 v 是被 A 乘后方向不变（只缩放）的非零向量；特征值 λ 是缩放系数。在 PCA 中，特征向量给出最大方差方向，特征值给出方差大小。

**📐 Formula:**

```
A × v = λ × v

where:
  A = square matrix (e.g., covariance matrix)
  v = eigenvector (direction)
  λ = eigenvalue (magnitude of variance along that direction)

Explained variance ratio for component k:
  ratio_k = λ_k / Σᵢ λᵢ
```

**💡 Intuition (直觉理解):**

> **The weather vane analogy:** Imagine a wind pattern over a field. Each eigenvector points in a direction the "wind blows strongest" (most variance). The eigenvalue tells you HOW STRONG that wind is. The biggest eigenvalue = the dominant wind direction = PC1.
>
> > **风向标类比：** 想象一片田野上的风场。每个特征向量指向"风吹得最猛"的方向（最大方差）。特征值告诉你那个方向的风有多强。最大特征值 = 主导风向 = PC1。

**🔢 Worked Example:**

```
Iris covariance matrix eigenvalues:
  λ₁ = 2.94 → ratio = 2.94/4.03 = 73%
  λ₂ = 0.92 → ratio = 0.92/4.03 = 23%
  λ₃ = 0.15 → ratio = 0.15/4.03 = 4%
  λ₄ = 0.02 → ratio = 0.02/4.03 = 0.5%

Cumulative: PC1+PC2 = 96% → Keep only 2 PCs, discard rest!
```

**🔗 Related Concepts:**
→ see: Covariance Matrix (eigenvalues/vectors extracted from it)
→ see: PCA (uses eigendecomposition as core step)
→ see: Scree Plot (plots eigenvalues to find optimal number of PCs)

**📚 Appears In:**

- ML Week 1 §4.4 (PCA Step 3 — Eigen Values and Eigen Vectors)
