---
topic: neural_network
dimension: math
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Rumelhart et al. 1986 — https://www.nature.com/articles/323533a0"
  - "📖 Paper: Hornik et al. 1989 — https://doi.org/10.1016/0893-6080(89)90020-8"
expiry: 12m
status: current
---

# Neural Network (神经网络) 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $\mathbf{x}$ | 输入向量 | Input vector | $\mathbb{R}^n$ |
| $\mathbf{y}$ | 真实标签 | Target / ground truth | $\mathbb{R}^k$ 或 $\{0,1\}^k$ |
| $\hat{\mathbf{y}}$ | 网络预测值 | Network output / prediction | $\mathbb{R}^k$ |
| $\mathbf{W}^{(l)}$ | 第 $l$ 层的权重矩阵 | Weight matrix of layer $l$ | $\mathbb{R}^{m_{l} \times m_{l-1}}$ |
| $\mathbf{b}^{(l)}$ | 第 $l$ 层的偏置向量 | Bias vector of layer $l$ | $\mathbb{R}^{m_l}$ |
| $\mathbf{z}^{(l)}$ | 第 $l$ 层的线性组合（激活前） | Pre-activation | $\mathbb{R}^{m_l}$ |
| $\mathbf{h}^{(l)}$ | 第 $l$ 层的激活输出 | Activation / hidden representation | $\mathbb{R}^{m_l}$ |
| $\sigma(\cdot)$ | 激活函数 | Activation function | 非线性函数 |
| $L$ | 网络总层数 | Number of layers | 正整数 |
| $\mathcal{L}$ | 损失函数 | Loss function | $\mathbb{R}^+ \cup \{0\}$ |
| $\eta$ | 学习率 | Learning rate | $(0, 1)$，典型 $10^{-4}$ ~ $10^{-1}$ |
| $N$ | 训练样本数 | Number of training samples | 正整数 |
| $\boldsymbol{\theta}$ | 所有可训练参数 | All trainable parameters | $\{\mathbf{W}^{(l)}, \mathbf{b}^{(l)}\}_{l=1}^L$ |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

## 核心公式

### 公式 1: 单层线性变换（仿射变换）

**直觉：** 每一层做的第一件事就是"加权求和"——把上一层的输出按权重组合起来，再加上偏置。

$$
\mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{h}^{(l-1)} + \mathbf{b}^{(l)}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1, Eq. 6.2

**参数解释：**

| 参数 | 含义 | 示例 |
|------|------|------|
| $\mathbf{W}^{(l)}$ | 当前层的权重矩阵 ($m_l \times m_{l-1}$) | $2 \times 3$ 矩阵：2 个神经元接收 3 个输入 |
| $\mathbf{h}^{(l-1)}$ | 上一层的激活输出 ($m_{l-1} \times 1$) | 3 维向量 |
| $\mathbf{b}^{(l)}$ | 当前层偏置 ($m_l \times 1$) | 2 维向量 |

### 公式 2: 激活函数应用

**直觉：** 光做线性变换不够——多层线性叠加还是线性。加一个非线性函数，才能让网络"弯曲"决策边界。

$$
\mathbf{h}^{(l)} = \sigma(\mathbf{z}^{(l)})
$$

常用激活函数：

| 名称 | 公式 | 输出范围 |
|------|------|---------|
| Sigmoid | $\sigma(z) = \frac{1}{1 + e^{-z}}$ | $(0, 1)$ |
| Tanh | $\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$ | $(-1, 1)$ |
| ReLU | $\text{ReLU}(z) = \max(0, z)$ | $[0, +\infty)$ |
| Softmax | $\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$ | $(0, 1)$，和为 1 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3

### 公式 3: 完整前向传播

**直觉：** 把所有层串起来——输入进去，逐层做"线性变换 + 激活"，最后一层输出就是预测值。

$$
\hat{\mathbf{y}} = f(\mathbf{x}; \boldsymbol{\theta}) = \sigma_L(\mathbf{W}^{(L)} \sigma_{L-1}(\cdots \sigma_1(\mathbf{W}^{(1)} \mathbf{x} + \mathbf{b}^{(1)}) \cdots) + \mathbf{b}^{(L)})
$$

简洁递推形式：

$$
\mathbf{h}^{(0)} = \mathbf{x}, \qquad \mathbf{h}^{(l)} = \sigma_l(\mathbf{W}^{(l)} \mathbf{h}^{(l-1)} + \mathbf{b}^{(l)}), \qquad \hat{\mathbf{y}} = \mathbf{h}^{(L)}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1, Eq. 6.1–6.3

### 公式 4: 损失函数（MSE & 交叉熵）

**直觉：** 衡量"猜得有多准"。回归任务用方差（猜的数和真实数差多远），分类任务用交叉熵（猜的概率分布和真实分布差多少）。

**回归 — 均方误差 (MSE):**

$$
\mathcal{L}_{\text{MSE}} = \frac{1}{N} \sum_{i=1}^N \|\hat{\mathbf{y}}_i - \mathbf{y}_i\|^2
$$

**分类 — 交叉熵 (Cross-Entropy):**

$$
\mathcal{L}_{\text{CE}} = -\frac{1}{N} \sum_{i=1}^N \sum_{c=1}^k y_{i,c} \log \hat{y}_{i,c}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.2

### 公式 5: 反向传播（链式法则）

**直觉：** 从输出层的误差开始，用链式法则一层层往回算——每一层对误差贡献了多少？

**输出层梯度：**

$$
\boldsymbol{\delta}^{(L)} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(L)}}
$$

**隐藏层梯度递推：**

$$
\boldsymbol{\delta}^{(l)} = \left(\mathbf{W}^{(l+1)}\right)^T \boldsymbol{\delta}^{(l+1)} \odot \sigma'(\mathbf{z}^{(l)})
$$

**参数梯度：**

$$
\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \boldsymbol{\delta}^{(l)} \left(\mathbf{h}^{(l-1)}\right)^T, \qquad \frac{\partial \mathcal{L}}{\partial \mathbf{b}^{(l)}} = \boldsymbol{\delta}^{(l)}
$$

**推导过程：**（逐步，不跳步）

1. 定义误差信号 $\boldsymbol{\delta}^{(l)} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(l)}}$
2. 输出层：$\boldsymbol{\delta}^{(L)} = \nabla_{\hat{\mathbf{y}}} \mathcal{L} \odot \sigma'(\mathbf{z}^{(L)})$
3. 因为 $\mathbf{z}^{(l)}$ 通过 $\mathbf{h}^{(l)} = \sigma(\mathbf{z}^{(l)})$ 然后 $\mathbf{z}^{(l+1)} = \mathbf{W}^{(l+1)} \mathbf{h}^{(l)} + \mathbf{b}^{(l+1)}$ 影响 $\mathcal{L}$
4. 应用链式法则：$\boldsymbol{\delta}^{(l)} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(l)}} = \frac{\partial \mathbf{z}^{(l+1)}}{\partial \mathbf{h}^{(l)}} ^T \boldsymbol{\delta}^{(l+1)} \odot \sigma'(\mathbf{z}^{(l)}) = (\mathbf{W}^{(l+1)})^T \boldsymbol{\delta}^{(l+1)} \odot \sigma'(\mathbf{z}^{(l)})$
5. 因为 $\mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{h}^{(l-1)} + \mathbf{b}^{(l)}$ ，直接求偏导得 $\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \boldsymbol{\delta}^{(l)} (\mathbf{h}^{(l-1)})^T$

> 📖 Paper: Rumelhart et al., [Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0), Nature 1986
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

### 公式 6: 参数更新（梯度下降）

**直觉：** 算完梯度后，沿梯度反方向走一小步——误差会变小。

$$
\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \eta \nabla_{\boldsymbol{\theta}} \mathcal{L}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.1

---

## 公式关系图

```
输入 x
  │
  ↓
公式 1: z = Wx + b   (仿射变换)
  │
  ↓
公式 2: h = σ(z)     (非线性激活)
  │
  ↓ (重复 L 次)
公式 3: ŷ = f(x;θ)   (完整前向传播 = 公式1+2 的 L 次叠加)
  │
  ↓
公式 4: L = Loss(ŷ, y) (损失计算)
  │
  ↓
公式 5: δ, ∂L/∂W, ∂L/∂b (反向传播 = 链式法则逐层向回)
  │
  ↓
公式 6: θ ← θ - η∇L  (参数更新)
  │
  ↓ (重复 epoch 次)
训练完成
```

---

## 手算练习

### 练习 1: 两层网络前向传播

**题目：** 一个 2→2→1 网络（2 个输入，2 个隐藏神经元，1 个输出），使用 Sigmoid 激活函数。

- 输入：$\mathbf{x} = [1, 0]^T$
- 隐藏层权重：$\mathbf{W}^{(1)} = \begin{bmatrix} 0.5 & 0.3 \\ 0.2 & 0.7 \end{bmatrix}$，偏置 $\mathbf{b}^{(1)} = [0.1, -0.1]^T$
- 输出层权重：$\mathbf{W}^{(2)} = [0.4, 0.6]$，偏置 $b^{(2)} = 0.2$

**解答步骤：**

1. 隐藏层线性组合：$\mathbf{z}^{(1)} = \mathbf{W}^{(1)} \mathbf{x} + \mathbf{b}^{(1)} = \begin{bmatrix} 0.5 \times 1 + 0.3 \times 0 + 0.1 \\ 0.2 \times 1 + 0.7 \times 0 - 0.1 \end{bmatrix} = \begin{bmatrix} 0.6 \\ 0.1 \end{bmatrix}$
2. 隐藏层激活：$\mathbf{h}^{(1)} = \sigma(\mathbf{z}^{(1)}) = \begin{bmatrix} \sigma(0.6) \\ \sigma(0.1) \end{bmatrix} = \begin{bmatrix} 0.6457 \\ 0.5250 \end{bmatrix}$
3. 输出层线性组合：$z^{(2)} = 0.4 \times 0.6457 + 0.6 \times 0.5250 + 0.2 = 0.2583 + 0.3150 + 0.2 = 0.7733$
4. 输出层激活：$\hat{y} = \sigma(0.7733) = 0.6843$
5. 结果：网络输出 $\hat{y} \approx 0.684$

### 练习 2: 反向传播计算梯度

**题目：** 继续练习 1，真实标签 $y = 1$，使用 MSE 损失。求 $\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(2)}}$。

**解答步骤：**

1. 损失：$\mathcal{L} = (\hat{y} - y)^2 = (0.684 - 1)^2 = 0.0999$
2. 输出层误差信号：$\delta^{(2)} = \frac{\partial \mathcal{L}}{\partial z^{(2)}} = 2(\hat{y} - y) \cdot \sigma'(z^{(2)}) = 2 \times (-0.316) \times 0.684 \times (1-0.684) = -0.1367$
3. 权重梯度：$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(2)}} = \delta^{(2)} \cdot (\mathbf{h}^{(1)})^T = -0.1367 \times [0.6457, 0.5250] = [-0.0883, -0.0718]$

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 仿射变换 | $\mathbf{z} = \mathbf{W}\mathbf{h} + \mathbf{b}$ | 每层第一步：线性组合 | — |
| 激活 | $\mathbf{h} = \sigma(\mathbf{z})$ | 每层第二步：引入非线性 | 仿射变换 |
| 前向传播 | $\hat{\mathbf{y}} = f(\mathbf{x};\boldsymbol{\theta})$ | 得到预测值 | 仿射+激活 的 L 次叠加 |
| MSE 损失 | $\mathcal{L} = \frac{1}{N}\sum\|\hat{\mathbf{y}}-\mathbf{y}\|^2$ | 回归任务损失 | 前向传播 |
| 交叉熵损失 | $\mathcal{L} = -\frac{1}{N}\sum y \log \hat{y}$ | 分类任务损失 | 前向传播 |
| 误差信号 | $\boldsymbol{\delta}^{(l)} = (\mathbf{W}^{(l+1)})^T \boldsymbol{\delta}^{(l+1)} \odot \sigma'$ | 逐层回传误差 | 前向传播 + 损失 |
| 权重梯度 | $\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \boldsymbol{\delta}^{(l)} (\mathbf{h}^{(l-1)})^T$ | 计算每层权重梯度 | 误差信号 |
| 参数更新 | $\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \eta \nabla \mathcal{L}$ | 更新所有参数 | 权重梯度 |
