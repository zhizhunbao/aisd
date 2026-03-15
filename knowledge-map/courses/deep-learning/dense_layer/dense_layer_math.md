---
topic: dense_layer
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 《PRML》 Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Glorot & Bengio, 'Understanding the difficulty of training deep feedforward neural networks', AISTATS 2010 — http://proceedings.mlr.press/v9/glorot10a.html"
  - "📖 Paper: He et al., 'Delving Deep into Rectifiers', ICCV 2015 — https://arxiv.org/abs/1502.01852"
expiry: 12m
status: current
---

# Dense Layer 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $x$ | 输入向量 | input vector | $\mathbb{R}^{n_{in}}$ |
| $W$ | 权重矩阵 | weight matrix | $\mathbb{R}^{n_{out} \times n_{in}}$ |
| $b$ | 偏置向量 | bias vector | $\mathbb{R}^{n_{out}}$ |
| $z$ | 预激活值（线性输出） | pre-activation | $\mathbb{R}^{n_{out}}$ |
| $a$ | 激活后输出 | activation output | $\mathbb{R}^{n_{out}}$ |
| $\sigma$ | 激活函数 | activation function | ReLU/Sigmoid/Tanh 等 |
| $n_{in}$ | 输入特征数 | input features | 正整数 |
| $n_{out}$ | 输出特征数 | output features | 正整数 |
| $\mathcal{L}$ | 损失函数 | loss function | 标量 |
| $\eta$ | 学习率 | learning rate | $(0, 1)$ |
| $\delta$ | 误差信号（loss 对 $z$ 的梯度） | error signal | $\mathbb{R}^{n_{out}}$ |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

## 核心公式

### 公式 1: 前向传播 (Forward Pass)

**直觉：** 把输入向量通过权重矩阵"旋转+缩放+平移"，再经过非线性函数"扭曲"，得到新的表示。

$$
z = Wx + b \quad \text{(仿射变换)}
$$
$$
a = \sigma(z) \quad \text{(非线性激活)}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

**参数解释：**
| 参数 | 含义 | 例子 |
|------|------|------|
| $Wx$ | 矩阵乘法，$n_{out} \times n_{in}$ 乘 $n_{in} \times 1$ 得 $n_{out} \times 1$ | 784→256 的特征映射 |
| $+b$ | 每个输出加一个偏移量 | 允许决策面不经过原点 |
| $\sigma(\cdot)$ | 非线性激活 | ReLU: 负值→0, 正值→不变 |

**推导过程（逐元素展开）：**

$$
z_j = \sum_{i=1}^{n_{in}} w_{ji} x_i + b_j, \quad j = 1, ..., n_{out}
$$
$$
a_j = \sigma(z_j)
$$

每个输出 $z_j$ 是输入 $x$ 所有元素的加权求和加偏置。

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.1

---

### 公式 2: 反向传播 — Dense Layer 的梯度

**直觉：** 已知 loss 对输出的梯度，反推 loss 对输入、权重、偏置的梯度——就像"追溯责任链"。

$$
\delta = \frac{\partial \mathcal{L}}{\partial z} = \frac{\partial \mathcal{L}}{\partial a} \odot \sigma'(z) \quad \text{(误差信号)}
$$
$$
\frac{\partial \mathcal{L}}{\partial W} = \delta \cdot x^T \quad \text{(权重梯度)}
$$
$$
\frac{\partial \mathcal{L}}{\partial b} = \delta \quad \text{(偏置梯度)}
$$
$$
\frac{\partial \mathcal{L}}{\partial x} = W^T \delta \quad \text{(传递给前一层)}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.3

**参数解释：**
| 参数 | 含义 | 维度 |
|------|------|------|
| $\delta$ | loss 对预激活值 $z$ 的梯度 | $n_{out} \times 1$ |
| $\sigma'(z)$ | 激活函数的导数 | $n_{out} \times 1$ |
| $\odot$ | 逐元素乘法 (Hadamard product) | — |
| $\delta x^T$ | 外积 → 权重梯度矩阵 | $n_{out} \times n_{in}$ |
| $W^T \delta$ | 将误差信号传回前一层 | $n_{in} \times 1$ |

**推导过程（链式法则）：**

Step 1: 由链式法则，$z = Wx + b$ 对 $W$ 的梯度：

$$
\frac{\partial z_j}{\partial w_{ji}} = x_i \implies \frac{\partial \mathcal{L}}{\partial w_{ji}} = \delta_j \cdot x_i
$$

写成矩阵形式：$\frac{\partial \mathcal{L}}{\partial W} = \delta x^T$

Step 2: $z$ 对 $b$ 的梯度为单位矩阵：$\frac{\partial \mathcal{L}}{\partial b} = \delta$

Step 3: $z$ 对 $x$ 的梯度：$\frac{\partial z_j}{\partial x_i} = w_{ji} \implies \frac{\partial \mathcal{L}}{\partial x} = W^T \delta$

---

### 公式 3: 参数量计算

**直觉：** Dense Layer 有多少个需要学习的数字？每个输入-输出连接一个权重，再加上每个输出一个偏置。

$$
\text{Params} = n_{in} \times n_{out} + n_{out} = n_{out}(n_{in} + 1)
$$

无偏置时：
$$
\text{Params} = n_{in} \times n_{out}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

**例子快算：**
| 层配置 | 参数量 |
|--------|--------|
| Dense(784, 256) | $784 \times 256 + 256 = 201,\!024$ |
| Dense(256, 10) | $256 \times 10 + 10 = 2,\!570$ |
| Dense(512, 2048) + Dense(2048, 512) | $512 \times 2048 + 2048 + 2048 \times 512 + 512 = 2,\!099,\!712$ |

---

### 公式 4: Xavier 初始化

**直觉：** 让每层的输出方差与输入方差保持一致，防止信号在层间逐渐放大（爆炸）或缩小（消失）。

$$
W \sim \mathcal{N}\left(0, \frac{2}{n_{in} + n_{out}}\right) \quad \text{(Xavier Normal)}
$$
$$
W \sim \mathcal{U}\left(-\sqrt{\frac{6}{n_{in} + n_{out}}}, \sqrt{\frac{6}{n_{in} + n_{out}}}\right) \quad \text{(Xavier Uniform)}
$$

> 📖 Paper: [Glorot & Bengio 2010](http://proceedings.mlr.press/v9/glorot10a.html)

**推导直觉：** 对于 $z = Wx$，假设 $x$ 的方差为 $\text{Var}(x)$，要让 $\text{Var}(z) = \text{Var}(x)$：

$$
\text{Var}(z_j) = n_{in} \cdot \text{Var}(w) \cdot \text{Var}(x)
$$

要 $\text{Var}(z) = \text{Var}(x)$，则 $\text{Var}(w) = 1/n_{in}$。考虑反向传播也需要保持，取折中 $\text{Var}(w) = 2/(n_{in}+n_{out})$。

---

### 公式 5: He 初始化

**直觉：** Xavier 假设激活函数是线性的，但 ReLU 会将一半的值置零（负值被截断），因此需要将方差翻倍补偿。

$$
W \sim \mathcal{N}\left(0, \frac{2}{n_{in}}\right) \quad \text{(He Normal，适合 ReLU)}
$$

> 📖 Paper: [He et al. 2015](https://arxiv.org/abs/1502.01852)

**推导直觉：** ReLU 将约 50% 的值置零，有效输出方差减半：$\text{Var}(a) = \frac{1}{2} n_{in} \cdot \text{Var}(w) \cdot \text{Var}(x)$。要 $\text{Var}(a) = \text{Var}(x)$，则 $\text{Var}(w) = 2/n_{in}$。

---

## 公式关系图

```
输入 x ──────────────────────────────────────────────────┐
  │                                                       │
  ├─→ z = Wx + b (公式 1: 前向传播)                       │
  │       │                                               │
  │       ├─→ a = σ(z) (激活)                             │
  │       │                                               │
  │   [Loss 计算: L = loss(a, y_true)]                   │
  │       │                                               │
  │       ├─→ δ = ∂L/∂z (公式 2: 误差信号)                │
  │       │       │                                       │
  │       │       ├─→ ∂L/∂W = δ · xᵀ (权重梯度) ──→ 更新 W│
  │       │       ├─→ ∂L/∂b = δ (偏置梯度) ──→ 更新 b    │
  │       │       └─→ ∂L/∂x = Wᵀδ (传递给前一层)         │
  │       │                                               │
  │   参数量 = n_in × n_out + n_out (公式 3)              │
  │                                                       │
  └─→ W 初始化: Xavier (公式 4) 或 He (公式 5) ───────────┘
```

---

## 手算练习

### 练习 1: 前向传播（2→3 Dense Layer）

**题目：** 给定一个 Dense Layer ($n_{in}=2, n_{out}=3$)，无激活函数：

$W = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}, \quad b = \begin{bmatrix} 0.1 \\ 0.2 \\ 0.3 \end{bmatrix}, \quad x = \begin{bmatrix} 1 \\ -1 \end{bmatrix}$

计算输出 $z = Wx + b$。

**解答：**

$$
z = \begin{bmatrix} 1(1)+2(-1)+0.1 \\ 3(1)+4(-1)+0.2 \\ 5(1)+6(-1)+0.3 \end{bmatrix} = \begin{bmatrix} -0.9 \\ -0.8 \\ -0.7 \end{bmatrix}
$$

如果加 ReLU：$a = \max(0, z) = [0, 0, 0]^T$（全部为负，全被截断）

**参数量：** $2 \times 3 + 3 = 9$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 练习 2: 反向传播梯度计算

**题目：** 沿用练习 1 的 $W, x$，假设 $\delta = [1, 0, -1]^T$（已知的误差信号），计算权重梯度和传回前一层的梯度。

**解答：**

$$
\frac{\partial \mathcal{L}}{\partial W} = \delta x^T = \begin{bmatrix} 1 \\ 0 \\ -1 \end{bmatrix} \begin{bmatrix} 1 & -1 \end{bmatrix} = \begin{bmatrix} 1 & -1 \\ 0 & 0 \\ -1 & 1 \end{bmatrix}
$$

$$
\frac{\partial \mathcal{L}}{\partial x} = W^T \delta = \begin{bmatrix} 1 & 3 & 5 \\ 2 & 4 & 6 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \\ -1 \end{bmatrix} = \begin{bmatrix} -4 \\ -4 \end{bmatrix}
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.3

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 前向传播 | $z = Wx + b; \; a = \sigma(z)$ | 层的核心计算 | 无 |
| 权重梯度 | $\partial\mathcal{L}/\partial W = \delta x^T$ | 更新权重 | 公式 1 |
| 偏置梯度 | $\partial\mathcal{L}/\partial b = \delta$ | 更新偏置 | 公式 1 |
| 输入梯度 | $\partial\mathcal{L}/\partial x = W^T\delta$ | 传递误差 | 公式 1 |
| 参数量 | $n_{in} \times n_{out} + n_{out}$ | 模型大小估算 | 无 |
| Xavier 初始化 | $\mathcal{N}(0, 2/(n_{in}+n_{out}))$ | sigmoid/tanh 层初始化 | 无 |
| He 初始化 | $\mathcal{N}(0, 2/n_{in})$ | ReLU 层初始化 | 无 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, 8.4
