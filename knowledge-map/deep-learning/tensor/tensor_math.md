---
topic: tensor
dimension: math
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.3"
  - "📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)"
  - "📖 Paper: [Kolda & Bader, Tensor Decompositions (2009)](https://doi.org/10.1137/07070111X)"
expiry: 12m
status: current
---

# Tensor 数学基础

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3
> 📖 Paper: [Kolda & Bader, Tensor Decompositions and Applications (2009)](https://doi.org/10.1137/07070111X)

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $\mathcal{T}$ | 一个 Tensor | Tensor | 任意阶多维数组 |
| $n$ | Tensor 的阶（维度数） | Order / Rank (ndim) | $n \geq 0$ |
| $d_i$ | 第 $i$ 维的大小 | Size of dimension $i$ | $d_i \geq 1$ |
| $\mathbf{s}$ | shape 向量 | Shape | $(d_1, d_2, \ldots, d_n)$ |
| $s_i$ | 第 $i$ 维的 stride | Stride | 正整数 |
| $\alpha$ | 标量乘数 | Scalar | $\mathbb{R}$ |
| $\mathbf{A}, \mathbf{B}$ | 矩阵（2 阶 Tensor） | Matrix | $\mathbb{R}^{m \times n}$ |
| $\odot$ | 逐元素乘法 | Hadamard product | 两个 Tensor shape 相同 |

> 📖 Paper: [Kolda & Bader, Tensor Decompositions (2009)](https://doi.org/10.1137/07070111X)

---


## 核心公式

### 公式 1: Tensor 元素总数

**直觉：** Tensor 有多少个元素？就是所有维度大小相乘。

$$
N = \prod_{i=1}^{n} d_i = d_1 \times d_2 \times \cdots \times d_n
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $N$ | 元素总数 | `tensor.numel()` 返回值 |
| $d_i$ | 第 $i$ 维大小 | shape 中的每个数 |

**推导过程：**

$$
\text{Step 1: 一个 (3, 4) 矩阵} \quad N = 3 \times 4 = 12
$$
$$
\text{Step 2: 一个 (2, 3, 4) 的 3D Tensor} \quad N = 2 \times 3 \times 4 = 24
$$

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---

### 公式 2: Stride 与内存偏移

**直觉：** 给定多维索引 $(i_1, i_2, \ldots, i_n)$，如何找到元素在一维连续内存中的位置？

$$
\text{offset} = \sum_{k=1}^{n} i_k \times s_k
$$

其中 $s_k$ 是第 $k$ 维的 stride。

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $\text{offset}$ | 从存储起始位置的偏移量 | 一维数组中的下标 |
| $i_k$ | 第 $k$ 维的索引 | 多维下标 |
| $s_k$ | 第 $k$ 维的 stride | `tensor.stride()[k]` |

**推导过程：**

$$
\text{Step 1: 设 shape = (3, 4)，行优先存储}
$$
$$
\text{Step 2: stride = (4, 1)，即跳一行需跨 4 个元素}
$$
$$
\text{Step 3: 访问 T[2][1] → offset = 2 \times 4 + 1 \times 1 = 9}
$$
$$
\text{Step 4: 即一维数组中第 9 个元素（从 0 开始）}
$$

> 📖 Paper: [Kolda & Bader, Tensor Decompositions (2009)](https://doi.org/10.1137/07070111X)

---

### 公式 3: 默认 Stride 计算

**直觉：** 新创建的（行优先连续存储）Tensor，每个维度的 stride 是多少？

$$
s_k = \prod_{j=k+1}^{n} d_j \quad (k < n), \quad s_n = 1
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $s_k$ | 第 $k$ 维的 stride | `tensor.stride()[k]` |
| $d_j$ | 后续维度的大小 | shape 中后面的元素 |

**推导过程：**

$$
\text{Step 1: shape = (2, 3, 4)}
$$
$$
\text{Step 2: } s_3 = 1 \quad \text{(最后一维 stride 永远是 1)}
$$
$$
\text{Step 3: } s_2 = d_3 = 4
$$
$$
\text{Step 4: } s_1 = d_2 \times d_3 = 3 \times 4 = 12
$$
$$
\text{Step 5: stride = (12, 4, 1)}
$$

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---

### 公式 4: 矩阵乘法 (线性变换核心)

**直觉：** 两个矩阵相乘，结果的每个元素是左矩阵一行和右矩阵一列的点积。

$$
\mathbf{C} = \mathbf{A} \mathbf{B}, \quad C_{ij} = \sum_{k=1}^{p} A_{ik} B_{kj}
$$

其中 $\mathbf{A} \in \mathbb{R}^{m \times p}$, $\mathbf{B} \in \mathbb{R}^{p \times n}$, $\mathbf{C} \in \mathbb{R}^{m \times n}$。

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

**推导过程：**

$$
\text{Step 1: } \mathbf{A} = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}, \mathbf{B} = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}
$$
$$
\text{Step 2: } C_{11} = 1 \times 5 + 2 \times 7 = 19
$$
$$
\text{Step 3: } C_{12} = 1 \times 6 + 2 \times 8 = 22
$$
$$
\text{Step 4: } C_{21} = 3 \times 5 + 4 \times 7 = 43
$$
$$
\text{Step 5: } C_{22} = 3 \times 6 + 4 \times 8 = 50
$$
$$
\text{Step 6: } \mathbf{C} = \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}
$$

> 📖 Docs: [PyTorch torch.matmul](https://pytorch.org/docs/stable/generated/torch.matmul.html)

---

### 公式 5: Broadcasting 规则

**直觉：** 两个 shape 不同的 Tensor 如何对齐？从最右边维度开始比较，要么相等，要么其中一个是 1。

$$
\text{对于维度 } k: \quad d_k^A = d_k^B \quad \text{或} \quad d_k^A = 1 \quad \text{或} \quad d_k^B = 1
$$

$$
\text{输出 shape: } d_k^{\text{out}} = \max(d_k^A, d_k^B)
$$

> 📖 Docs: [PyTorch Broadcasting Semantics](https://pytorch.org/docs/stable/notes/broadcasting.html)

**推导过程：**

$$
\text{Step 1: A.shape = (3, 1), B.shape = (1, 4)}
$$
$$
\text{Step 2: 维度 0: } \max(3, 1) = 3
$$
$$
\text{Step 3: 维度 1: } \max(1, 4) = 4
$$
$$
\text{Step 4: 输出 shape = (3, 4)}
$$

> 📖 Docs: [PyTorch Broadcasting Semantics](https://pytorch.org/docs/stable/notes/broadcasting.html)

---


## 公式关系图

```
元素总数 (公式 1) ──→ Stride 计算 (公式 3)
                          ↓
                    内存偏移 (公式 2) ──→ view/reshape 可行性判断
                                                    ↓
                                             contiguous 检查

矩阵乘法 (公式 4) ──→ 神经网络线性层
                          ↓
Broadcasting (公式 5) ──→ 逐元素运算的 shape 推导
```

---


## 手算练习

### 练习 1: Stride 计算

**题目：** 给定 `shape = (2, 3, 4)` 的行优先 Tensor，计算 stride，然后求 `T[1][2][3]` 的内存偏移。

**解答步骤：**

1. stride = ($d_2 \times d_3$, $d_3$, 1) = (12, 4, 1)
2. offset = $1 \times 12 + 2 \times 4 + 3 \times 1 = 12 + 8 + 3 = 23$
3. 结果 = 第 23 个元素（从 0 开始计数）

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

### 练习 2: Broadcasting Shape 推导

**题目：** `A.shape = (5, 3, 1)`, `B.shape = (3, 4)`，求 `(A + B).shape`。

**解答步骤：**

1. 右对齐: A = (5, 3, 1), B = (_, 3, 4)（B 前面补 1 → (1, 3, 4)）
2. 维度 0: max(5, 1) = 5
3. 维度 1: max(3, 3) = 3 ✅ 相等
4. 维度 2: max(1, 4) = 4
5. 结果 shape = (5, 3, 4)

> 📖 Docs: [PyTorch Broadcasting Semantics](https://pytorch.org/docs/stable/notes/broadcasting.html)

### 练习 3: 矩阵乘法

**题目：** A = [[2, 0], [1, 3]], B = [[1, 4], [2, 1]]，求 A @ B。

**解答步骤：**

1. $C_{11} = 2 \times 1 + 0 \times 2 = 2$
2. $C_{12} = 2 \times 4 + 0 \times 1 = 8$
3. $C_{21} = 1 \times 1 + 3 \times 2 = 7$
4. $C_{22} = 1 \times 4 + 3 \times 1 = 7$
5. 结果 = [[2, 8], [7, 7]]

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 元素总数 | $N = \prod d_i$ | 计算内存占用 | — |
| 内存偏移 | $\text{offset} = \sum i_k s_k$ | 理解多维索引 → 内存地址 | Stride |
| 默认 Stride | $s_k = \prod_{j>k} d_j$ | 判断 contiguous | 元素总数 |
| 矩阵乘法 | $C_{ij} = \sum_k A_{ik} B_{kj}$ | 线性变换 | — |
| Broadcasting | $d_k^{\text{out}} = \max(d_k^A, d_k^B)$ | shape 推导 | — |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3
> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)
