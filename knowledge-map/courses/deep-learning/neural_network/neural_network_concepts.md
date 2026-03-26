---
topic: neural_network
dimension: concepts
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: McCulloch & Pitts 1943 — https://doi.org/10.1007/BF02478259"
  - "📖 Paper: Rosenblatt 1958 — https://doi.org/10.1037/h0042519"
  - "📖 Paper: Rumelhart et al. 1986 — https://www.nature.com/articles/323533a0"
expiry: 12m
status: current
---

# Neural Network (神经网络) 核心概念

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

---

## 术语定义

### 人工神经元 (Artificial Neuron)

一个计算单元，接收多个输入，对每个输入乘以一个权重，求和后加上偏置，再通过一个非线性激活函数产生输出。用数学写就是 $y = \sigma(\mathbf{w}^T \mathbf{x} + b)$。它是神经网络的最小构成单元。

> 别名：**Unit**（Goodfellow 用法）/ **Node**（图论视角）/ **Processing Element**（早期文献）— 都指同一个计算单元，名称取决于作者的学科背景
> 易混淆：**生物神经元 (Biological Neuron)** — 生物神经元通过脉冲频率编码信息，人工神经元是实数值函数，只是隐喻关系

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 感知机 (Perceptron)

最早的人工神经元模型之一，由 Frank Rosenblatt 在 1958 年提出。它只有一层计算：输入→加权求和→阈值函数→输出 0 或 1。感知机只能解决线性可分的问题（如 AND、OR），无法解决 XOR。

> 易混淆：**多层感知机 (MLP)** — 虽然名字里有"感知机"，但 MLP 有多层 + 非线性激活，能力远超单层感知机；名字是历史遗留

> 📖 Paper: Rosenblatt, [The Perceptron](https://doi.org/10.1037/h0042519), 1958

### 前馈神经网络 (Feedforward Neural Network)

信息只沿**一个方向**流动的网络：输入层 → 隐藏层 → 输出层，没有循环连接。MLP 是最典型的前馈网络。"前馈"强调的是信息流方向——对比循环网络 (RNN)，后者有反馈连接。

> 别名：**Feedforward Network**（Goodfellow 用法）/ **Acyclic Network**（图论视角）— 从计算图看就是一个无环有向图 (DAG)

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 隐藏层 (Hidden Layer)

位于输入层和输出层之间的计算层。称为"隐藏"是因为在训练数据中**只能看到输入和输出**，中间层的理想值（目标值）不是直接给出的，需要网络自行学习。隐藏层是网络学习特征表示的地方。

> 易混淆：**输入层 (Input Layer)** — 输入层不做任何计算，只是把原始数据传递进来；隐藏层才有权重和激活函数

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 权重 (Weights)

连接两个神经元之间的参数，决定上一层输出对当前神经元的影响强度。权重越大，对应输入的影响越大。训练神经网络的本质就是找到一组合适的权重值。

> 别名：**Parameters**（广义说法）/ **Connection Strengths**（生物启发视角）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.1

### 偏置 (Bias)

每个神经元附加的常数项，它让激活函数的阈值能够平移。没有偏置的话，所有超平面都必须过原点。偏置给模型增加了一个自由度。

> 易混淆：**统计偏差 (Statistical Bias)** — 统计中的 bias 指估计量与真值的系统性偏移，完全不同

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 激活函数 (Activation Function)

施加在神经元输出上的**非线性函数**。没有激活函数，多层网络等价于单层线性变换（因为线性函数的复合还是线性）。常见的有 Sigmoid、Tanh、ReLU、Softmax。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3

### 前向传播 (Forward Pass / Forward Propagation)

数据从输入层经过每一层的计算（线性变换 + 激活函数），逐层传递到输出层，最终产生预测值的过程。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 反向传播 (Backpropagation)

利用链式法则从输出层向输入层逐层计算损失函数对每个参数的梯度的算法。它不是优化算法本身，而是高效计算梯度的方法，与 SGD 等优化器配合使用。

> 别名：**Backprop**（口语简称）/ **Error Backpropagation**（Bishop 用法）/ **Reverse-mode Automatic Differentiation**（数学视角）— 从自动微分的角度看，反向传播就是"反向模式自动微分"在计算图上的应用
> 易混淆：**梯度下降 (Gradient Descent)** — 反向传播只负责算梯度，梯度下降才是用梯度更新参数的优化步骤

> 📖 Paper: Rumelhart et al., [Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0), Nature 1986
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

### 损失函数 (Loss Function)

衡量网络预测值与真实值之间差距的函数。训练的目标是最小化损失函数。常见的有 MSE（回归）、交叉熵 (Cross-Entropy, 分类)。

> 别名：**Cost Function**（统计学习视角）/ **Objective Function**（优化视角）/ **Error Function**（PRML 用法）— 名字不同但都在衡量同一件事

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.2

### 万能近似定理 (Universal Approximation Theorem, UAT)

数学定理：一个具有至少一个隐藏层的前馈网络，只要隐藏层足够宽（神经元足够多），可以以任意精度逼近定义在紧集上的任意连续函数。注意：它只证明了**存在性**，没有说如何找到那组参数。

> 📖 Paper: Hornik et al., [Universal Approximators](https://doi.org/10.1016/0893-6080(89)90020-8), 1989
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.4.1

### 表征学习 (Representation Learning)

让网络自动从原始数据中学习有用的中间表示（特征），而不是手动设计特征。神经网络每一层都在将输入变换成越来越抽象的表征。深度学习的核心优势在于：利用深层网络学习层次化表征。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.1.2, Ch.15

### 深度 vs 宽度 (Depth vs Width)

深度指网络的层数，宽度指每层的神经元数。UAT 说一层足够宽就行，但实践表明：增加深度比增加宽度更高效——深层网络可以用指数级更少的参数逼近同样的函数。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.4.1

---

## 概念辨析

### 神经网络 (Neural Network) vs 深度学习 (Deep Learning)

| 维度 | Neural Network | Deep Learning |
|------|----------------|---------------|
| **本质** | 一种计算模型/架构 | 使用深层神经网络的机器学习范式 |
| **层数** | 可以是 1 层（感知机）也可以很多层 | 强调多层（通常 > 2 隐藏层） |
| **历史** | 1943 年开始 | 2006 年 Hinton 重新定义 |
| **关系** | 更广的概念 | 神经网络的子集 + 训练技巧 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.1

### 前馈网络 (Feedforward) vs 循环网络 (Recurrent)

| 维度 | Feedforward | Recurrent |
|------|-------------|-----------|
| **信息流** | 单向：输入→输出 | 有环：输出可以反馈到输入 |
| **适用** | 固定维度输入 (图像/表格) | 变长序列 (文本/时序) |
| **计算图** | DAG（有向无环图） | 有环图 |
| **代表** | MLP, CNN | RNN, LSTM, GRU |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 vs Ch.10

### 反向传播 (Backpropagation) vs 梯度下降 (Gradient Descent)

| 维度 | Backpropagation | Gradient Descent |
|------|-----------------|------------------|
| **做什么** | 计算梯度 | 用梯度更新参数 |
| **是什么** | 算法 (反向模式自动微分) | 优化方法 |
| **独立性** | 不关心怎么用梯度 | 不关心梯度怎么来的 |
| **关系** | 反向传播算出梯度 → 交给梯度下降去更新 | — |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---

## 核心属性

### 信息架构

```
输入 x ∈ ℝⁿ
    │
    ├──→ [层 1: W₁x + b₁] ──→ [σ₁(·)] ──→ h₁ ∈ ℝᵐ¹
    │
    ├──→ [层 2: W₂h₁ + b₂] ──→ [σ₂(·)] ──→ h₂ ∈ ℝᵐ²
    │
    ├──→ ...
    │
    └──→ [层 L: WLhL₋₁ + bL] ──→ [σL(·)] ──→ ŷ ∈ ℝᵏ
                                                │
                                          Loss(ŷ, y)
```

### 适用场景 ✅

- 输入-输出之间存在复杂的非线性映射
- 有足够多的标注数据
- 可接受黑盒模型（不需要完全可解释）
- 分类、回归、生成、序列建模等任务

### 不适用场景 ❌

- 数据量极少（< 100 样本）→ 用简单规则或小模型
- 需要完全可解释性（如医疗/法律决策）→ 用决策树或线性模型
- 推理资源极有限（嵌入式最小设备）→ 考虑模型压缩/传统算法
- 数据有清晰的物理规律 → 先用物理模型

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.5.2, Ch.6.4

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 最小单元 | 人工神经元：y = σ(wᵀx + b) | ReLU(3×0.5 + 2×0.3 + 0.1) = 2.2 |
| 训练 = | 最小化 Loss(ŷ, y) | MSE, Cross-Entropy |
| 梯度计算 | 反向传播（链式法则） | ∂L/∂w = ∂L/∂ŷ · ∂ŷ/∂z · ∂z/∂w |
| 参数更新 | 梯度下降家族 | w ← w - η·∂L/∂w |
| 理论保证 | UAT：一层网络可逼近任意连续函数 | 但需要指数级宽度 |
| 深度优势 | 深网络用少得多的参数表达复杂函数 | O(n) vs O(2ⁿ) |
| 核心超参 | 层数、每层宽度、激活函数、学习率 | 2 隐藏层, 128 units, ReLU, 0.001 |
