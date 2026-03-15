---
topic: mlp
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Rumelhart et al., 'Learning representations by back-propagating errors', Nature 1986 — https://www.nature.com/articles/323533a0"
  - "📖 Paper: Cybenko 1989 — https://doi.org/10.1007/BF02551274"
  - "📖 Paper: Glorot & Bengio, AISTATS 2010 — http://proceedings.mlr.press/v9/glorot10a.html"
expiry: 12m
status: current
---

# MLP (Multi-Layer Perceptron) 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $\mathbf{x}$ | 输入向量 | Input vector | $\mathbb{R}^d$ |
| $\mathbf{y}$ | 真实标签 | Ground truth label | 类别索引或实数 |
| $\hat{\mathbf{y}}$ | 模型预测输出 | Predicted output | $\mathbb{R}^K$ 或 $[0,1]^K$ |
| $L$ | 网络层数（不含输入层） | Number of layers | 正整数 |
| $l$ | 层编号 | Layer index | $1, 2, \ldots, L$ |
| $n_l$ | 第 $l$ 层的神经元数量 | Number of units in layer $l$ | 正整数 |
| $\mathbf{W}^{(l)}$ | 第 $l$ 层的权重矩阵 | Weight matrix | $\mathbb{R}^{n_l \times n_{l-1}}$ |
| $\mathbf{b}^{(l)}$ | 第 $l$ 层的偏置向量 | Bias vector | $\mathbb{R}^{n_l}$ |
| $\mathbf{z}^{(l)}$ | 第 $l$ 层的预激活值 | Pre-activation | $\mathbb{R}^{n_l}$ |
| $\mathbf{a}^{(l)}$ | 第 $l$ 层的激活值（后激活） | Activation | $\mathbb{R}^{n_l}$ |
| $\sigma(\cdot)$ | 激活函数 | Activation function | 非线性可微函数 |
| $\mathcal{L}$ | 损失函数 | Loss function | $\mathbb{R}^+ \cup \{0\}$ |
| $\eta$ | 学习率 | Learning rate | $(0, 1)$，常取 $10^{-4}$ ~ $10^{-1}$ |
| $\boldsymbol{\delta}^{(l)}$ | 第 $l$ 层的误差信号（梯度中间量） | Error signal | $\mathbb{R}^{n_l}$ |
| $\theta$ | 所有可学习参数的集合 | Parameters | $\{\mathbf{W}^{(l)}, \mathbf{b}^{(l)}\}_{l=1}^{L}$ |
| $N$ | 训练样本数 | Number of training samples | 正整数 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.1

---


## 核心公式

### 公式 1: 前向传播（单层变换）

**直觉：** 每一层做的事情就两步——先把输入用矩阵乘法"线性混合"，再通过激活函数"扭弯"，给网络注入非线性能力。

$$
\mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}
$$

$$
\mathbf{a}^{(l)} = \sigma(\mathbf{z}^{(l)})
$$

> 📚 Book: Goodfellow et al., Eq.6.4–6.5; Bishop, Eq.5.7

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $\mathbf{a}^{(l-1)}$ | 上一层的输出（第一层时为输入 $\mathbf{x}$） | $\mathbf{a}^{(0)} = \mathbf{x}$ |
| $\mathbf{W}^{(l)}$ | 第 $l$ 层连接权重 | 隐藏层 1 的权重矩阵 |
| $\mathbf{b}^{(l)}$ | 第 $l$ 层偏置 | 允许激活函数平移 |

**推导过程：**

$$
\text{Step 1: 线性变换 } \mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)} \quad \text{（加权求和 + 偏置）}
$$

$$
\text{Step 2: 非线性激活 } \mathbf{a}^{(l)} = \sigma(\mathbf{z}^{(l)}) \quad \text{（逐元素施加激活函数）}
$$

$$
\text{Step 3: 完整网络 } f(\mathbf{x}) = \sigma_L(\mathbf{W}^{(L)} \sigma_{L-1}(\cdots \sigma_1(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}) \cdots) + \mathbf{b}^{(L)})
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

### 公式 2: 常见激活函数

**直觉：** 激活函数是让 MLP 能学习非线性的关键——没有它，多层线性变换等价于一层。

**ReLU (Rectified Linear Unit):**

$$
\text{ReLU}(z) = \max(0, z)
$$

$$
\text{ReLU}'(z) = \begin{cases} 1 & z > 0 \\ 0 & z \leq 0 \end{cases}
$$

**Sigmoid:**

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

$$
\sigma'(z) = \sigma(z)(1 - \sigma(z))
$$

**Tanh:**

$$
\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}} = 2\sigma(2z) - 1
$$

$$
\tanh'(z) = 1 - \tanh^2(z)
$$

**Softmax (输出层多分类):**

$$
\text{softmax}(z_k) = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}, \quad k = 1, \ldots, K
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.2.2, Ch.6.3

---

### 公式 3: 损失函数

**直觉：** 损失函数是模型预测"有多差"的度量——训练就是不断减小这个数值。

**交叉熵损失（分类）：**

$$
\mathcal{L}_{\text{CE}} = -\frac{1}{N} \sum_{i=1}^{N} \sum_{k=1}^{K} y_{ik} \log \hat{y}_{ik}
$$

> 📚 Book: Goodfellow et al., Eq.6.24

**均方误差（回归）：**

$$
\mathcal{L}_{\text{MSE}} = \frac{1}{N} \sum_{i=1}^{N} \|\mathbf{y}_i - \hat{\mathbf{y}}_i\|^2 = \frac{1}{N} \sum_{i=1}^{N} \sum_{k=1}^{K} (y_{ik} - \hat{y}_{ik})^2
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq.5.11

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $N$ | 样本数 | batch size = 32 |
| $K$ | 输出维度（类别数） | MNIST: K=10 |
| $y_{ik}$ | 第 $i$ 个样本的真实标签（one-hot 第 $k$ 位） | $[0,0,1,...,0]$ |
| $\hat{y}_{ik}$ | 第 $i$ 个样本对第 $k$ 类的预测概率 | softmax 输出 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.2

---

### 公式 4: 反向传播（梯度计算）

**直觉：** 反向传播就是链式法则的高效应用——从输出误差往回推，逐层算出每个权重"该为误差承担多少责任"。

**输出层误差信号：**

$$
\boldsymbol{\delta}^{(L)} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(L)}} = \hat{\mathbf{y}} - \mathbf{y} \quad \text{（softmax + 交叉熵的简化形式）}
$$

**隐藏层误差信号递推：**

$$
\boldsymbol{\delta}^{(l)} = \left(\mathbf{W}^{(l+1)\top} \boldsymbol{\delta}^{(l+1)}\right) \odot \sigma'(\mathbf{z}^{(l)})
$$

**权重和偏置的梯度：**

$$
\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \boldsymbol{\delta}^{(l)} \mathbf{a}^{(l-1)\top}
$$

$$
\frac{\partial \mathcal{L}}{\partial \mathbf{b}^{(l)}} = \boldsymbol{\delta}^{(l)}
$$

> 📚 Book: Goodfellow et al., Eq.6.44–6.46; Bishop, Eq.5.54–5.56
> 📖 Paper: Rumelhart et al., [Backpropagation](https://www.nature.com/articles/323533a0), 1986

**推导过程：**

$$
\text{Step 1: 输出层 } \boldsymbol{\delta}^{(L)} = \frac{\partial \mathcal{L}}{\partial \hat{\mathbf{y}}} \cdot \frac{\partial \hat{\mathbf{y}}}{\partial \mathbf{z}^{(L)}} \quad \text{（对 softmax+CE 简化为 } \hat{\mathbf{y}} - \mathbf{y}\text{）}
$$

$$
\text{Step 2: 隐藏层 } \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(l)}} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(l+1)}} \cdot \frac{\partial \mathbf{z}^{(l+1)}}{\partial \mathbf{a}^{(l)}} \cdot \frac{\partial \mathbf{a}^{(l)}}{\partial \mathbf{z}^{(l)}}
$$

$$
= \mathbf{W}^{(l+1)\top} \boldsymbol{\delta}^{(l+1)} \odot \sigma'(\mathbf{z}^{(l)})
$$

$$
\text{Step 3: 权重梯度 } \frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{(l)}} \cdot \frac{\partial \mathbf{z}^{(l)}}{\partial \mathbf{W}^{(l)}} = \boldsymbol{\delta}^{(l)} \mathbf{a}^{(l-1)\top}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---

### 公式 5: 参数更新（梯度下降）

**直觉：** 沿着损失函数下降最快的方向迈一小步，反复迈步直到找到低谷。

$$
\mathbf{W}^{(l)} \leftarrow \mathbf{W}^{(l)} - \eta \frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}}
$$

$$
\mathbf{b}^{(l)} \leftarrow \mathbf{b}^{(l)} - \eta \frac{\partial \mathcal{L}}{\partial \mathbf{b}^{(l)}}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5, Ch.8.1

---

### 公式 6: Xavier 初始化

**直觉：** 让每层的输出方差 ≈ 输入方差，避免信号在前向/反向传播中逐层放大或缩小。

$$
W^{(l)} \sim \mathcal{N}\left(0, \frac{2}{n_{l-1} + n_l}\right) \quad \text{或} \quad \mathcal{U}\left(-\sqrt{\frac{6}{n_{l-1}+n_l}}, \sqrt{\frac{6}{n_{l-1}+n_l}}\right)
$$

> 📖 Paper: Glorot & Bengio, [Understanding the difficulty of training deep feedforward neural networks](http://proceedings.mlr.press/v9/glorot10a.html), AISTATS 2010

---


## 公式关系图

```
输入 x
│
▼
公式 1: 前向传播 z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾; a⁽ˡ⁾ = σ(z⁽ˡ⁾)
│ ←── 公式 2: 激活函数 σ (ReLU / sigmoid / tanh)
▼
公式 3: 损失计算 𝓛(ŷ, y)   ←── softmax + 交叉熵 或 MSE
│
▼
公式 4: 反向传播 δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾ᵀδ⁽ˡ⁺¹⁾) ⊙ σ'(z⁽ˡ⁾)
│ ←── 依赖公式 1 保存的中间值 z⁽ˡ⁾, a⁽ˡ⁾
▼
公式 5: 参数更新 W ← W − η·∂𝓛/∂W
│
▼
公式 6: Xavier 初始化   ←── 决定参数的起始值（训练前一次性使用）
```

---


## 手算练习

### 练习 1: 两层 MLP 解 XOR

**题目：** 给定一个两层 MLP（输入 $\mathbf{x} \in \mathbb{R}^2$，隐藏层 2 个 ReLU 神经元，输出 1 个线性神经元），验证以下参数能解 XOR 问题。

$$
\mathbf{W}^{(1)} = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}, \quad \mathbf{b}^{(1)} = \begin{bmatrix} 0 \\ -1 \end{bmatrix}, \quad \mathbf{w}^{(2)} = \begin{bmatrix} 1 \\ -2 \end{bmatrix}, \quad b^{(2)} = 0
$$

**解答步骤：**

1. 输入 $\mathbf{x} = [0, 0]^T$：
   - $\mathbf{z}^{(1)} = [0, -1]^T$
   - $\mathbf{a}^{(1)} = \text{ReLU}([0, -1]) = [0, 0]^T$
   - $y = [1, -2] \cdot [0, 0] + 0 = 0$ ✅ (XOR: 0⊕0=0)

2. 输入 $\mathbf{x} = [1, 0]^T$：
   - $\mathbf{z}^{(1)} = [1, 0]^T$
   - $\mathbf{a}^{(1)} = [1, 0]^T$
   - $y = [1, -2] \cdot [1, 0] + 0 = 1$ ✅ (XOR: 1⊕0=1)

3. 输入 $\mathbf{x} = [0, 1]^T$：
   - $\mathbf{z}^{(1)} = [1, 0]^T$
   - $\mathbf{a}^{(1)} = [1, 0]^T$
   - $y = 1$ ✅ (XOR: 0⊕1=1)

4. 输入 $\mathbf{x} = [1, 1]^T$：
   - $\mathbf{z}^{(1)} = [2, 1]^T$
   - $\mathbf{a}^{(1)} = [2, 1]^T$
   - $y = [1, -2] \cdot [2, 1] + 0 = 2 - 2 = 0$ ✅ (XOR: 1⊕1=0)

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1 (Example 6.1: XOR)

### 练习 2: 单样本反向传播

**题目：** 单隐藏层 MLP（输入 $x=2$，隐藏层 1 个 sigmoid 神经元，输出 1 个线性神经元），$w_1 = 0.5, b_1 = 0, w_2 = 1, b_2 = 0$，真实标签 $y=1$，使用 MSE 损失。计算 $\frac{\partial \mathcal{L}}{\partial w_1}$。

**解答步骤：**

1. **前向传播：**
   - $z_1 = w_1 \cdot x + b_1 = 0.5 \times 2 + 0 = 1.0$
   - $a_1 = \sigma(1.0) = \frac{1}{1+e^{-1}} \approx 0.731$
   - $\hat{y} = w_2 \cdot a_1 + b_2 = 1 \times 0.731 + 0 = 0.731$
   - $\mathcal{L} = \frac{1}{2}(y - \hat{y})^2 = \frac{1}{2}(1 - 0.731)^2 \approx 0.0362$

2. **反向传播：**
   - $\frac{\partial \mathcal{L}}{\partial \hat{y}} = -(y - \hat{y}) = -(1 - 0.731) = -0.269$
   - $\frac{\partial \hat{y}}{\partial a_1} = w_2 = 1$
   - $\frac{\partial a_1}{\partial z_1} = \sigma(z_1)(1-\sigma(z_1)) = 0.731 \times 0.269 \approx 0.197$
   - $\frac{\partial z_1}{\partial w_1} = x = 2$

3. **链式法则：**
   - $\frac{\partial \mathcal{L}}{\partial w_1} = -0.269 \times 1 \times 0.197 \times 2 \approx -0.106$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.3

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 前向传播 | $\mathbf{a}^{(l)} = \sigma(\mathbf{W}^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)})$ | 逐层计算输出 | 无 |
| ReLU | $\max(0, z)$ | 隐藏层激活 | 前向传播 |
| Sigmoid | $1/(1+e^{-z})$ | 二分类输出 / 旧版隐藏层 | 前向传播 |
| Softmax | $e^{z_k} / \sum_j e^{z_j}$ | 多分类输出 | 前向传播 |
| 交叉熵 | $-\sum y_k \log \hat{y}_k$ | 分类损失 | Softmax |
| MSE | $\frac{1}{N}\sum\|y-\hat{y}\|^2$ | 回归损失 | 前向传播 |
| 误差反传 | $\boldsymbol{\delta}^{(l)} = (\mathbf{W}^{(l+1)\top}\boldsymbol{\delta}^{(l+1)}) \odot \sigma'(\mathbf{z}^{(l)})$ | 反向传播梯度 | 损失函数 |
| 权重梯度 | $\partial\mathcal{L}/\partial\mathbf{W}^{(l)} = \boldsymbol{\delta}^{(l)}\mathbf{a}^{(l-1)\top}$ | 更新权重 | 误差反传 |
| 参数更新 | $W \leftarrow W - \eta \cdot \nabla_W \mathcal{L}$ | SGD 优化 | 权重梯度 |
| Xavier 初始化 | $W \sim \mathcal{N}(0, 2/(n_{in}+n_{out}))$ | 初始化权重 | 无 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5
