---
topic: forward_propagation
dimension: math
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow, Bengio & Courville, Deep Learning, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Rumelhart, Hinton & Williams, 'Learning representations by back-propagating errors', Nature 1986 — https://doi.org/10.1038/323533a0"
expiry: 12m
status: current
---

# Forward Propagation 数学基础

> 📚 Book: Goodfellow, Bengio & Courville, [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 "Deep Feedforward Networks"

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $x$ | 输入向量 | Input vector | $\mathbb{R}^{n_0}$ |
| $W^{(l)}$ | 第 $l$ 层的权重矩阵 | Weight matrix of layer $l$ | $\mathbb{R}^{n_l \times n_{l-1}}$ |
| $b^{(l)}$ | 第 $l$ 层的偏置向量 | Bias vector of layer $l$ | $\mathbb{R}^{n_l}$ |
| $z^{(l)}$ | 第 $l$ 层的预激活值（线性变换结果） | Pre-activation of layer $l$ | $\mathbb{R}^{n_l}$ |
| $a^{(l)}$ | 第 $l$ 层的激活值（激活函数输出） | Activation of layer $l$ | 取决于激活函数 |
| $\sigma(\cdot)$ | 激活函数 | Activation function | 逐元素运算 |
| $n_l$ | 第 $l$ 层的神经元数量 | Number of neurons in layer $l$ | 正整数 |
| $L$ | 网络的总层数 | Total number of layers | 正整数 |
| $\hat{y}$ | 网络的最终输出（预测值） | Network output / prediction | 取决于任务 |
| $\mathcal{L}$ | 损失函数值 | Loss value | $\mathbb{R}^+$ |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1, 符号约定

---

## 核心公式

### 公式 1: 单层仿射变换 (Affine Transformation)

**直觉：** 把上一层的输出向量通过矩阵乘法"旋转+缩放"，再平移一下偏置，得到这一层的原始分数。

$$
z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1, Eq.6.2

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $W^{(l)}$ | 本层权重矩阵，形状 $(n_l, n_{l-1})$ | 第 1 层: $(3, 2)$ 矩阵 |
| $a^{(l-1)}$ | 上一层的激活输出 | 对第 1 层来说就是输入 $x$ |
| $b^{(l)}$ | 本层偏置向量，形状 $(n_l,)$ | 第 1 层: 长度为 3 的向量 |
| $z^{(l)}$ | 预激活值 | 送入激活函数前的原始值 |

**推导过程：**

1. 把上一层输出 $a^{(l-1)}$ 看作列向量 $(n_{l-1}, 1)$
2. 权重矩阵 $W^{(l)}$ 形状为 $(n_l, n_{l-1})$
3. 矩阵乘法 $W^{(l)} a^{(l-1)}$ 得到 $(n_l, 1)$ 向量
4. 加上偏置 $b^{(l)}$（广播为 $(n_l, 1)$），得到 $z^{(l)}$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

### 公式 2: 激活函数应用 (Activation)

**直觉：** 把原始分数 $z$ 过一个非线性函数，让网络能学到非线性的关系，否则多个线性层叠加还是线性。

$$
a^{(l)} = \sigma(z^{(l)})
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3, Eq.6.3

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $\sigma$ | 激活函数（ReLU、Sigmoid 等） | ReLU: $\max(0, z)$ |
| $z^{(l)}$ | 仿射变换的输出 | 上一步求得 |
| $a^{(l)}$ | 本层的最终输出 | 送入下一层的输入 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3

---

### 公式 3: 完整的 $L$ 层前向传播 (Full Forward Pass)

**直觉：** 把公式 1 和公式 2 反复叠加 $L$ 次——每一层对上一层的输出做一次仿射变换 + 激活，一层一层传递到最后。

$$
\hat{y} = f(x) = f^{(L)} \circ f^{(L-1)} \circ \cdots \circ f^{(1)}(x)
$$

其中每一层 $f^{(l)}(a) = \sigma^{(l)}(W^{(l)} a + b^{(l)})$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1, Eq.6.4

**展开写法：**

$$
a^{(0)} = x
$$
$$
z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}, \quad l = 1, 2, \ldots, L
$$
$$
a^{(l)} = \sigma^{(l)}(z^{(l)}), \quad l = 1, 2, \ldots, L
$$
$$
\hat{y} = a^{(L)}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

### 公式 4: Batch 前向传播 (Mini-Batch Forward Pass)

**直觉：** 不是一次只算一个样本，而是把一批样本打包成矩阵一起算——GPU 的矩阵运算对批量数据特别快。

$$
Z^{(l)} = W^{(l)} A^{(l-1)} + b^{(l)} \mathbf{1}^T
$$

其中 $A^{(l-1)} \in \mathbb{R}^{n_{l-1} \times m}$，$m$ 是 batch size。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1（矩阵化形式）

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $A^{(l-1)}$ | 上一层所有样本的激活值矩阵 $(n_{l-1}, m)$ | 32 个样本打包 |
| $m$ | 一个 batch 里有多少个样本 | batch_size = 32 |
| $\mathbf{1}^T$ | 全 1 行向量 $(1, m)$，用于广播偏置 | PyTorch 自动广播 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

## 公式关系图

    输入 x = a⁽⁰⁾
         │
         ▼
    ┌──────────────────────────┐
    │ 公式1: z⁽¹⁾= W⁽¹⁾x + b⁽¹⁾  │ ← 仿射变换
    └──────────────────────────┘
         │
         ▼
    ┌──────────────────────────┐
    │ 公式2: a⁽¹⁾= σ(z⁽¹⁾)       │ ← 激活
    └──────────────────────────┘
         │
         ▼
       ··· 重复 L 次 （公式3）···
         │
         ▼
    ŷ = a⁽ᴸ⁾  ← 最终预测
         │
         ▼
    ℒ(ŷ, y)  ← 损失函数

    公式4 是公式1-3 的矩阵化批量版本

---

## 手算练习

### 练习 1: 两层网络的前向传播

**题目：** 给定一个 2 输入、3 隐藏神经元、1 输出的网络（ReLU 激活），计算前向传播。

- 输入：$x = [1.0, 2.0]^T$
- 第 1 层权重：$W^{(1)} = \begin{bmatrix} 0.1 & 0.2 \\ 0.3 & 0.4 \\ 0.5 & 0.6 \end{bmatrix}$，$b^{(1)} = [0.1, 0.1, 0.1]^T$
- 第 2 层权重：$W^{(2)} = [0.2, 0.3, 0.4]$，$b^{(2)} = [0.1]$

**解答步骤：**

1. **第 1 层仿射变换**：
   $z^{(1)} = W^{(1)} x + b^{(1)}$
   $= \begin{bmatrix} 0.1 \times 1.0 + 0.2 \times 2.0 \\ 0.3 \times 1.0 + 0.4 \times 2.0 \\ 0.5 \times 1.0 + 0.6 \times 2.0 \end{bmatrix} + \begin{bmatrix} 0.1 \\ 0.1 \\ 0.1 \end{bmatrix} = \begin{bmatrix} 0.5 \\ 1.1 \\ 1.7 \end{bmatrix} + \begin{bmatrix} 0.1 \\ 0.1 \\ 0.1 \end{bmatrix} = \begin{bmatrix} 0.6 \\ 1.2 \\ 1.8 \end{bmatrix}$

2. **第 1 层激活（ReLU）**：
   $a^{(1)} = \text{ReLU}(z^{(1)}) = \begin{bmatrix} 0.6 \\ 1.2 \\ 1.8 \end{bmatrix}$ （全部为正，ReLU 不改变）

3. **第 2 层仿射变换**：
   $z^{(2)} = W^{(2)} a^{(1)} + b^{(2)}$
   $= 0.2 \times 0.6 + 0.3 \times 1.2 + 0.4 \times 1.8 + 0.1$
   $= 0.12 + 0.36 + 0.72 + 0.1 = 1.3$

4. **输出**：$\hat{y} = 1.3$（回归任务，输出层无激活）

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 仿射变换 | $z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}$ | 每层线性部分 | — |
| 激活 | $a^{(l)} = \sigma(z^{(l)})$ | 引入非线性 | 仿射变换 |
| 完整前向传播 | $\hat{y} = f^{(L)} \circ \cdots \circ f^{(1)}(x)$ | 整体计算流 | 仿射 + 激活 |
| Batch 版本 | $Z^{(l)} = W^{(l)} A^{(l-1)} + b^{(l)} \mathbf{1}^T$ | 批量加速 | 仿射变换 |
