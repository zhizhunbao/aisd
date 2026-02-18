# 线性代数直觉教程 / Linear Algebra Intuition Tutorial

> **教学理念**: 先建立几何直觉，再学形式化定义，最后用代码验证。
> 每个概念都回答三个问题：**它是什么？为什么重要？怎么算？**

### 🖥️ 配套可视化脚本

```bash
# 安装依赖
pip install numpy matplotlib

# 运行可视化演示（10 个交互式图形 demo）
python linear_algebra_demo.py
```

| Demo 编号 | 对应章节 | 可视化内容 |
|-----------|----------|------------|
| 1 | 向量 | 向量加法、缩放的箭头图 |
| 2 | Span | 不共线 vs 共线向量的张成空间 |
| 3 | 线性变换 | 6 种变换对正方形的效果 |
| 4 | 行列式 | 面积缩放因子 (det>0, <0, =0) |
| 5 | 特征值 | 单位圆→椭圆 + 特征方向 |
| 6 | 投影 | 向量投影 + 直角验证 |
| 7 | 最小二乘 | 数据拟合直线 + 误差线 |
| 8 | SVD | 图像压缩 (秩 1→100 对比) |
| 9 | 方程组 | 唯一解/无穷解/无解的几何图 |
| 10 | 子空间 | Column Space & Null Space |

---

## 目录

1. [向量 Vectors](#1-向量-vectors)
2. [线性组合与张成空间 Linear Combination & Span](#2-线性组合与张成空间)
3. [线性无关与基 Linear Independence & Basis](#3-线性无关与基)
4. [矩阵 = 线性变换 Matrix = Linear Transformation](#4-矩阵--线性变换)
5. [矩阵运算 Matrix Operations](#5-矩阵运算)
6. [线性方程组与高斯消元 Systems & Gaussian Elimination](#6-线性方程组与高斯消元)
7. [行列式 Determinant](#7-行列式-determinant)
8. [逆矩阵 Inverse Matrix](#8-逆矩阵-inverse-matrix)
9. [向量空间与子空间 Vector Spaces & Subspaces](#9-向量空间与子空间)
10. [特征值与特征向量 Eigenvalues & Eigenvectors](#10-特征值与特征向量)
11. [正交性与投影 Orthogonality & Projection](#11-正交性与投影)
12. [最小二乘法 Least Squares](#12-最小二乘法-least-squares)
13. [奇异值分解 SVD](#13-奇异值分解-svd)

---

## 1. 向量 Vectors

### 🎯 直觉

**向量就是一个有方向和大小的箭头。** 

想象你站在原点 (0,0)，向量 `[3, 2]` 告诉你："向右走 3 步，向上走 2 步"。

```
    ↑ y
  3 |
  2 |       • (3,2)
    |      ↗
  1 |    /
    |  /
  0 +--------→ x
    0  1  2  3
```

但向量不仅仅是箭头——它本质上是 **一组有序的数字**，可以代表：
- 📍 空间中的位置（坐标）
- 🏃 运动的方向和速度
- 🎨 颜色 RGB (255, 128, 0)
- 📊 机器学习中的特征向量

### 📐 形式化定义

向量是 $\mathbb{R}^n$ 中的一个元素，记作列向量：

$$\vec{v} = \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{bmatrix}$$

**基本运算：**

| 运算 | 公式 | 几何意义 |
|------|------|----------|
| 加法 | $\vec{u} + \vec{v} = \begin{bmatrix} u_1+v_1 \\ u_2+v_2 \end{bmatrix}$ | 首尾相连（平行四边形法则） |
| 缩放 | $c\vec{v} = \begin{bmatrix} cv_1 \\ cv_2 \end{bmatrix}$ | 拉伸/压缩箭头长度 |
| 点积 | $\vec{u} \cdot \vec{v} = u_1v_1 + u_2v_2$ | 投影长度 × 被投影向量长度 |
| 模 | $\|\vec{v}\| = \sqrt{v_1^2 + v_2^2}$ | 箭头的长度 |

### 💻 Python 验证

```python
import numpy as np

u = np.array([3, 2])
v = np.array([1, 4])

print("加法:", u + v)          # [4, 6]
print("缩放:", 2 * u)          # [6, 4]
print("点积:", np.dot(u, v))   # 3*1 + 2*4 = 11
print("模:",  np.linalg.norm(u))  # √(9+4) ≈ 3.61
```

### ⚠️ 常见误区

1. **向量不是点！** 向量 `[3,2]` 从原点出发到 (3,2)，但它也可以从 (1,1) 到 (4,3)——方向和大小相同就是同一个向量
2. **点积结果是标量**，不是向量！$\vec{u} \cdot \vec{v}$ 返回一个数字

### 🧠 自测题

> 向量 $\vec{a} = [1, 0]$ 和 $\vec{b} = [0, 1]$ 的点积是多少？这在几何上意味着什么？

<details>
<summary>答案</summary>

$\vec{a} \cdot \vec{b} = 1 \times 0 + 0 \times 1 = 0$

点积为零说明两个向量 **正交**（垂直）。$\vec{a}$ 沿 x 轴，$\vec{b}$ 沿 y 轴，它们确实垂直！

</details>

---

## 2. 线性组合与张成空间

### 🎯 直觉

**线性组合 = 缩放 + 相加。** 就像调鸡尾酒：取一些基酒，各倒不同分量，混合在一起。

给定向量 $\vec{v}_1, \vec{v}_2$，它们的线性组合是：

$$c_1\vec{v}_1 + c_2\vec{v}_2$$

其中 $c_1, c_2$ 是任意实数。

**张成空间 (Span)** = 通过所有可能的 $c_1, c_2$ 值，你能"到达"的所有点的集合。

```
想象 v₁ = [1, 0]，v₂ = [0, 1]

通过调整 c₁ 和 c₂，你能到达平面上的任意一点！
→ Span({v₁, v₂}) = 整个 R² 平面
```

### 📐 形式化定义

$$\text{Span}(\vec{v}_1, \vec{v}_2, \ldots, \vec{v}_k) = \{c_1\vec{v}_1 + c_2\vec{v}_2 + \cdots + c_k\vec{v}_k \mid c_i \in \mathbb{R}\}$$

**关键情形：**

| 向量组 | Span | 几何图形 |
|--------|------|----------|
| 1 个非零向量 | 一条直线 | 经过原点的线 |
| 2 个不共线向量 | 整个 $\mathbb{R}^2$ | 整个平面 |
| 2 个共线向量 | 一条直线 | 还是那条线 |
| 3 个不共面向量 | 整个 $\mathbb{R}^3$ | 整个空间 |

### 💻 Python 验证

```python
import numpy as np
import matplotlib.pyplot as plt

v1 = np.array([1, 0])
v2 = np.array([0, 1])

# 生成随机线性组合
points = []
for _ in range(1000):
    c1 = np.random.uniform(-3, 3)
    c2 = np.random.uniform(-3, 3)
    points.append(c1 * v1 + c2 * v2)

points = np.array(points)
plt.scatter(points[:, 0], points[:, 1], s=1)
plt.title("Span of [1,0] and [0,1] = R²")
plt.axis('equal')
plt.show()
```

### 🧠 自测题

> $\vec{v}_1 = [1, 2]$，$\vec{v}_2 = [2, 4]$，它们的 Span 是什么？

<details>
<summary>答案</summary>

$\vec{v}_2 = 2\vec{v}_1$，两个向量共线！Span 只是**经过原点的一条直线**（斜率为 2 的直线），不是整个平面。

</details>

---

## 3. 线性无关与基

### 🎯 直觉

**线性无关 (Linear Independence)** = 没有一个向量是"多余的"。

类比：你有三个导航指令——"向东"、"向北"、"向东北"。第三个是多余的，因为你可以通过组合前两个来实现"东北"。这时三个向量**线性相关 (linearly dependent)**。

**基 (Basis)** = 一组 **线性无关** 的向量，它们能 **张成整个空间**。

> 基就像一套"最精简的导航指令"——不多不少，刚好能到达空间中的每一个点。

### 📐 形式化定义

向量组 $\{\vec{v}_1, \ldots, \vec{v}_k\}$ **线性无关**，当且仅当：

$$c_1\vec{v}_1 + c_2\vec{v}_2 + \cdots + c_k\vec{v}_k = \vec{0} \implies c_1 = c_2 = \cdots = c_k = 0$$

翻译：唯一能让线性组合等于零向量的方式，就是所有系数都为零。

**$\mathbb{R}^n$ 的标准基 (Standard Basis)：**

$$\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \quad
\vec{e}_2 = \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \quad
\vec{e}_3 = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$$

**维度 (Dimension)** = 基中向量的个数。$\mathbb{R}^3$ 的维度是 3。

### 💻 Python 验证

```python
import numpy as np

# 检查线性无关性：如果行列式 ≠ 0，则线性无关
v1 = np.array([1, 2])
v2 = np.array([3, 4])
A = np.column_stack([v1, v2])
print("行列式:", np.linalg.det(A))  # -2 ≠ 0 → 线性无关

# 线性相关的例子
v3 = np.array([2, 4])  # = 2 * v1
B = np.column_stack([v1, v3])
print("行列式:", np.linalg.det(B))  # 0 → 线性相关
```

### ⚠️ 常见误区

- **正交 ≠ 线性无关**：正交一定线性无关，但线性无关不一定正交
- **基不唯一**：$\{[1,0], [0,1]\}$ 和 $\{[1,1], [1,-1]\}$ 都是 $\mathbb{R}^2$ 的基

---

## 4. 矩阵 = 线性变换

### 🎯 直觉（这是整个线性代数最重要的直觉！）

**矩阵不只是数字表格——它是一个空间变换！**

$$A = \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}$$

这个矩阵做了什么？它把 $\vec{e}_1 = [1,0]$ 变成了 $[2,0]$，把 $\vec{e}_2 = [0,1]$ 保持为 $[0,1]$。

**几何效果：水平方向拉伸 2 倍！**

```
变换前:          变换后:
  |                |
  □                □□
  |                |
--+--            --+----
  |                |
```

**矩阵的列 = 基向量变换后的去向！**

$$A = \begin{bmatrix} | & | \\ A\vec{e}_1 & A\vec{e}_2 \\ | & | \end{bmatrix}$$

### 📐 常见变换矩阵

| 变换 | 矩阵 | 效果 |
|------|------|------|
| 旋转 θ° | $\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$ | 逆时针旋转 |
| 缩放 | $\begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix}$ | 沿各轴缩放 |
| 剪切 | $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ | 水平倾斜 |
| 反射 | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ | 关于 x 轴翻转 |

### 💻 Python 验证

```python
import numpy as np

# 旋转矩阵: 逆时针旋转 90°
theta = np.pi / 2
R = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])

v = np.array([1, 0])
print("旋转后:", R @ v)  # [0, 1] — 向右变成了向上！

# 组合变换: 先旋转再缩放 = 矩阵乘法
S = np.array([[2, 0], [0, 3]])
combined = S @ R  # 注意顺序：先 R 后 S
print("先旋转再缩放:", combined @ v)  # [0, 3]
```

### ⚠️ 常见误区

- **矩阵乘法不满足交换律！** $AB \neq BA$（先旋转再缩放 ≠ 先缩放再旋转）
- **矩阵乘法 = 变换的组合**：$AB\vec{v}$ 意味着"先做 B 变换，再做 A 变换"

### 🧠 自测题

> 矩阵 $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ 把向量 $[1, 0]$ 变成了什么？这是什么几何变换？

<details>
<summary>答案</summary>

$$\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$$

向右 → 向上，这是 **逆时针旋转 90°**！

</details>

---

## 5. 矩阵运算

### 📐 矩阵乘法

$$C = AB \quad \text{其中} \quad C_{ij} = \sum_{k} A_{ik} B_{kj}$$

**直觉：** $C$ 的第 $i$ 行第 $j$ 列 = $A$ 的第 $i$ 行 · $B$ 的第 $j$ 列 (dot product)

**尺寸规则：** $(m \times \mathbf{n}) \cdot (\mathbf{n} \times p) = (m \times p)$，内部维度必须匹配！

### 转置 Transpose

$$A^T_{ij} = A_{ji}$$

**直觉：** 沿主对角线翻转，行变列、列变行。

$$\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}^T = \begin{bmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{bmatrix}$$

**重要性质：** $(AB)^T = B^T A^T$（注意顺序反转！）

### 💻 Python 验证

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("矩阵乘法:\n", A @ B)
print("转置:\n", A.T)
print("(AB)^T == B^T A^T:", np.allclose((A @ B).T, B.T @ A.T))  # True
```

---

## 6. 线性方程组与高斯消元

### 🎯 直觉

线性方程组就是问："什么输入经过矩阵变换后，得到这个输出？"

$$A\vec{x} = \vec{b} \quad \Leftrightarrow \quad \text{什么 } \vec{x} \text{ 经过变换 } A \text{ 后变成 } \vec{b}\text{？}$$

### 📐 高斯消元 (Gaussian Elimination)

通过行变换把矩阵化为 **行阶梯形 (Row Echelon Form)**：

$$\begin{bmatrix} 1 & 2 & 3 & | & 9 \\ 2 & 5 & 7 & | & 22 \\ 3 & 6 & 10 & | & 29 \end{bmatrix}
\xrightarrow{R_2 - 2R_1}
\begin{bmatrix} 1 & 2 & 3 & | & 9 \\ 0 & 1 & 1 & | & 4 \\ 3 & 6 & 10 & | & 29 \end{bmatrix}
\xrightarrow{R_3 - 3R_1}
\begin{bmatrix} 1 & 2 & 3 & | & 9 \\ 0 & 1 & 1 & | & 4 \\ 0 & 0 & 1 & | & 2 \end{bmatrix}$$

然后**回代 (Back Substitution)：** $x_3 = 2, \quad x_2 = 4 - 2 = 2, \quad x_1 = 9 - 4 - 6 = -1$

### 💻 Python 验证

```python
import numpy as np

A = np.array([[1, 2, 3], [2, 5, 7], [3, 6, 10]])
b = np.array([9, 22, 29])

x = np.linalg.solve(A, b)
print("解:", x)  # [-1, 2, 2]
print("验证 Ax=b:", np.allclose(A @ x, b))  # True
```

### ⚠️ 三种结果

| 情况 | 几何意义 | 条件 |
|------|----------|------|
| **唯一解** | 线/面相交于一点 | $\det(A) \neq 0$ |
| **无解** | 平行不相交 | 矛盾行 $[0\ 0\ 0\ |\ 5]$ |
| **无穷多解** | 重合 | 自由变量存在 |

---

## 7. 行列式 Determinant

### 🎯 直觉

**行列式 = 变换后面积/体积的缩放因子。**

$$\det\begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix} = 6$$

意味着：单位正方形经过这个变换后，面积变成了原来的 **6 倍**！

```
变换前 (面积=1):    变换后 (面积=6):
 1|___|              3|___________|
  |   |               |           |
  +---               +----------
  0   1               0     2
```

**关键意义：**

| $\det(A)$ | 含义 |
|-----------|------|
| $> 0$ | 保持方向（不翻转） |
| $< 0$ | 翻转方向（镜像） |
| $= 0$ | 空间被"压扁"，降维了！**不可逆！** |

### 📐 计算公式

**2×2：**
$$\det\begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc$$

**3×3 (展开)：**
$$\det(A) = a_{11}(a_{22}a_{33} - a_{23}a_{32}) - a_{12}(a_{21}a_{33} - a_{23}a_{31}) + a_{13}(a_{21}a_{32} - a_{22}a_{31})$$

### 💻 Python 验证

```python
import numpy as np

A = np.array([[2, 0], [0, 3]])
print("行列式:", np.linalg.det(A))  # 6.0

# 奇异矩阵（行列式=0）
B = np.array([[1, 2], [2, 4]])
print("行列式:", np.linalg.det(B))  # 0.0 → 不可逆
```

---

## 8. 逆矩阵 Inverse Matrix

### 🎯 直觉

**逆矩阵 = 撤销操作（Ctrl+Z）。**

如果矩阵 $A$ 是"旋转 90°"，那 $A^{-1}$ 就是"旋转 -90°"。

$$A A^{-1} = A^{-1} A = I$$

**什么时候不存在逆？** 当变换把空间"压扁"了（$\det = 0$），你无法还原——就像把一张纸折叠后，无法从折叠状态完美恢复。

### 📐 2×2 逆矩阵公式

$$A^{-1} = \frac{1}{ad-bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

### 💻 Python 验证

```python
import numpy as np

A = np.array([[3, 1], [2, 1]])
A_inv = np.linalg.inv(A)

print("A⁻¹:\n", A_inv)
print("A × A⁻¹ = I:\n", np.round(A @ A_inv))  # 单位矩阵

# 用于解方程: x = A⁻¹b
b = np.array([5, 3])
x = A_inv @ b
print("解:", x)
```

---

## 9. 向量空间与子空间

### 🎯 直觉

**向量空间** = 一个"完整的世界"，在这个世界里你可以随意做加法和缩放，结果还在这个世界里。

**子空间 (Subspace)** = 大世界里的"小世界"，满足同样的规则。

**规则（封闭性）：**
1. 包含零向量 $\vec{0}$
2. 对加法封闭：$\vec{u} + \vec{v}$ 仍在空间内
3. 对标量乘法封闭：$c\vec{v}$ 仍在空间内

### 📐 四个重要子空间

对于矩阵 $A_{m \times n}$：

| 子空间 | 定义 | 直觉 |
|--------|------|------|
| **Column Space** $C(A)$ | $A$ 的列的 Span | 变换 $A$ 能到达的所有输出 |
| **Null Space** $N(A)$ | $A\vec{x} = \vec{0}$ 的所有解 | 被变换"压扁"到原点的所有输入 |
| **Row Space** $C(A^T)$ | $A$ 的行的 Span | — |
| **Left Null Space** $N(A^T)$ | $A^T\vec{y} = \vec{0}$ 的解 | — |

**Rank（秩）** = Column Space 的维度 = 矩阵"真正有效"的维度数

### 💻 Python 验证

```python
import numpy as np

A = np.array([[1, 2, 3], [2, 4, 6]])  # 行2 = 2×行1

# 秩
print("Rank:", np.linalg.matrix_rank(A))  # 1

# Null Space（使用 SVD）
_, s, Vt = np.linalg.svd(A)
null_mask = np.isclose(s, 0, atol=1e-10)
# null_space = Vt 中对应奇异值为 0 的行
```

---

## 10. 特征值与特征向量

### 🎯 直觉（这是线性代数的高潮！）

大多数向量在经过矩阵变换后，方向会改变。但有些特殊的向量，变换后**方向不变**，只是被拉伸或压缩了——这就是 **Eigenvector（特征向量）**。

$$A\vec{v} = \lambda\vec{v}$$

- $\vec{v}$ = 特征向量（方向不变的那些向量）
- $\lambda$ = 特征值（拉伸的倍数）

```
例: A = [[2, 1], [0, 3]]

特征向量 [1,0] → A[1,0] = [2,0] = 2·[1,0]   (λ=2, 拉伸2倍)
特征向量 [1,1] → A[1,1] = [3,3] = 3·[1,1]   (λ=3, 拉伸3倍)
```

### 📐 如何求

1. 解 **特征方程**：$\det(A - \lambda I) = 0$ → 得到 $\lambda$
2. 对每个 $\lambda$，解 $(A - \lambda I)\vec{v} = \vec{0}$ → 得到 $\vec{v}$

**2×2 例题：**

$$A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$$

$$\det(A - \lambda I) = (4-\lambda)(3-\lambda) - 2 = \lambda^2 - 7\lambda + 10 = (\lambda-5)(\lambda-2) = 0$$

$$\lambda_1 = 5, \quad \lambda_2 = 2$$

### 🌍 应用

| 领域 | 应用 |
|------|------|
| **Google PageRank** | 网页重要性 = 转移矩阵的特征向量 |
| **PCA 降维** | 数据主方向 = 协方差矩阵的特征向量 |
| **量子力学** | 可观测量 = 算符的特征值 |
| **振动分析** | 自然频率 = 刚度矩阵的特征值 |

### 💻 Python 验证

```python
import numpy as np

A = np.array([[4, 1], [2, 3]])

eigenvalues, eigenvectors = np.linalg.eig(A)
print("特征值:", eigenvalues)      # [5, 2]
print("特征向量:\n", eigenvectors)

# 验证: Av = λv
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    print(f"Av = {A @ v}, λv = {lam * v}")  # 应该相等
```

### 🧠 自测题

> 单位矩阵 $I$ 的特征值是什么？每个向量都是它的特征向量吗？

<details>
<summary>答案</summary>

$I\vec{v} = 1 \cdot \vec{v}$，所以特征值只有 $\lambda = 1$，而且**每个非零向量都是特征向量**！这说明单位矩阵不改变任何方向。

</details>

---

## 11. 正交性与投影

### 🎯 直觉

**正交 (Orthogonal)** = 垂直，$\vec{u} \cdot \vec{v} = 0$

**投影 (Projection)** = 影子。把向量 $\vec{b}$ 投影到 $\vec{a}$ 上，就像太阳在 $\vec{a}$ 方向照射时 $\vec{b}$ 的影子。

```
        b
       /|
      / |
     /  |  ← 误差 (b - proj)
    /   |
   /    |
  ------+-----→ a
  proj_a(b)
```

### 📐 投影公式

**向量投影：**

$$\text{proj}_{\vec{a}}(\vec{b}) = \frac{\vec{a} \cdot \vec{b}}{\vec{a} \cdot \vec{a}} \vec{a}$$

**矩阵投影（投影到列空间）：**

$$P = A(A^TA)^{-1}A^T$$

### 💻 Python 验证

```python
import numpy as np

a = np.array([1, 0])
b = np.array([3, 4])

proj = (np.dot(a, b) / np.dot(a, a)) * a
print("投影:", proj)    # [3, 0]
print("误差:", b - proj)  # [0, 4] — 垂直于 a！
print("验证正交:", np.dot(a, b - proj))  # 0
```

### Gram-Schmidt 正交化

将任意一组线性无关的向量变成正交（甚至正交归一）的向量组：

```python
def gram_schmidt(V):
    """V 的列是输入向量，返回正交归一化的列"""
    Q = np.zeros_like(V, dtype=float)
    for i in range(V.shape[1]):
        q = V[:, i].astype(float)
        for j in range(i):
            q -= np.dot(Q[:, j], V[:, i]) * Q[:, j]
        Q[:, i] = q / np.linalg.norm(q)
    return Q
```

---

## 12. 最小二乘法 Least Squares

### 🎯 直觉

当方程组 $A\vec{x} = \vec{b}$ **无精确解**时（方程比未知数多），我们找一个"最接近的"解——使误差 $\|A\vec{x} - \vec{b}\|^2$ 最小。

**应用：** 数据拟合直线（线性回归）

### 📐 正规方程

$$A^T A \hat{x} = A^T \vec{b} \quad \Rightarrow \quad \hat{x} = (A^T A)^{-1} A^T \vec{b}$$

### 💻 Python 验证

```python
import numpy as np
import matplotlib.pyplot as plt

# 数据: y ≈ mx + c
x_data = np.array([1, 2, 3, 4, 5])
y_data = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

# 构建 A 矩阵 (加一列1作为截距)
A = np.column_stack([x_data, np.ones(len(x_data))])
# 最小二乘解
x_hat = np.linalg.lstsq(A, y_data, rcond=None)[0]
print(f"y = {x_hat[0]:.2f}x + {x_hat[1]:.2f}")

# 绘图
plt.scatter(x_data, y_data, label='数据')
plt.plot(x_data, A @ x_hat, 'r-', label='拟合直线')
plt.legend()
plt.show()
```

---

## 13. 奇异值分解 SVD

### 🎯 直觉

**SVD 是矩阵分解的"瑞士军刀"。** 任何矩阵都可以分解为三步操作：

$$A = U \Sigma V^T$$

1. $V^T$：旋转输入空间
2. $\Sigma$：沿各轴缩放（对角矩阵）
3. $U$：旋转输出空间

**任何线性变换 = 旋转 → 缩放 → 旋转**

### 📐 关键性质

- $\sigma_1 \geq \sigma_2 \geq \cdots \geq 0$（奇异值有序）
- $\text{rank}(A) =$ 非零奇异值的个数
- **低秩近似**：只保留前 $k$ 个最大的奇异值 → 图像压缩！

### 💻 Python 验证

```python
import numpy as np

A = np.array([[1, 2], [3, 4], [5, 6]])
U, s, Vt = np.linalg.svd(A, full_matrices=False)

print("奇异值:", s)
print("重建:", np.allclose(A, U @ np.diag(s) @ Vt))  # True

# 低秩近似: 只保留最大的奇异值
k = 1
A_approx = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
print(f"秩-{k} 近似:\n", A_approx)
```

### 🌍 应用

| 应用 | 说明 |
|------|------|
| **图像压缩** | 保留前 k 个奇异值，丢弃细节 |
| **推荐系统** | Netflix 用 SVD 预测用户评分 |
| **NLP** | LSA (Latent Semantic Analysis) |
| **伪逆** | $A^+ = V \Sigma^+ U^T$ |

---

## 📊 概念关系图

```
向量 (Vectors)
  ↓
线性组合 → Span → 线性无关 → 基 (Basis)
  ↓                              ↓
矩阵 = 线性变换                  维度
  ↓        ↓
行列式    逆矩阵 ←→ 线性方程组 (Ax=b)
  ↓
特征值/特征向量 → 对角化
  ↓
正交性 → 投影 → 最小二乘
  ↓
SVD（集大成者）
```

---

## 🎓 学习建议

1. **3Blue1Brown 的 "Essence of Linear Algebra"** — 必看，建立几何直觉
2. **Gilbert Strang 的 MIT 18.06** — 最经典的线性代数课
3. **动手算** — 至少手算几个 2×2 例子再用 NumPy
4. **画图** — 每个概念都试着画出几何图形

> 💡 线性代数的核心思想：**一切都是关于空间和变换的。** 矩阵是变换的语言，向量是变换的对象，行列式衡量变换的效果，特征值揭示变换的本质。
