---
topic: forward_propagation
dimension: concepts
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow, Bengio & Courville, Deep Learning, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Rumelhart, Hinton & Williams, 'Learning representations by back-propagating errors', Nature 1986 — https://doi.org/10.1038/323533a0"
  - "📖 Docs: PyTorch nn.Module — https://pytorch.org/docs/stable/generated/torch.nn.Module.html"
expiry: 12m
status: current
---

# Forward Propagation 核心概念

> 📚 Book: Goodfellow, Bengio & Courville, [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 "Deep Feedforward Networks"

---

## 术语定义

### 前向传播 (Forward Propagation / Forward Pass)

数据从输入层开始，经过每一个隐藏层的"线性变换 + 非线性激活"处理，一路流向输出层，最终产出预测值的完整计算过程。就像水流过一系列管道，每个管道对水做一次变换。在训练阶段，前向传播的结果用来计算损失；在推理阶段，前向传播的结果就是最终的预测。

> 别名：**Forward Pass**（PyTorch/工程领域）/ **前向计算**（中文教材）— 都是同一件事，只是工程侧更常用 "pass" 强调"跑一遍"

> 易混淆：**反向传播 (Backpropagation)** — 前向传播计算输出和损失值，反向传播利用前向传播保存的中间结果沿相反方向计算梯度；两者互为搭档，不是替代关系

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3 "Hidden Units"

### 仿射变换 (Affine Transformation)

对输入向量做一次"矩阵乘法 + 加偏置"的运算，即 $z = Wx + b$。这是每一层在激活函数之前做的事情。"仿射"这个名字来自数学——它保留了平行性和比例关系，但不要求通过原点（因为有偏置 $b$）。

> 别名：**线性变换 (Linear Transformation)**（工程口语中常混用）— 严格来说，"线性变换"不包含偏置项 $b$，没有 $b$ 时必须通过原点；加了 $b$ 就是仿射变换

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 权重 (Weights)

连接两层之间的参数矩阵 $W$，决定了每个输入特征对下一层每个神经元的贡献大小。权重是神经网络需要"学习"的核心参数，通过梯度下降迭代更新。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 偏置 (Bias)

每个神经元额外附带的标量参数 $b$，加在仿射变换的结果上。它的作用是让激活函数的输入可以整体平移，不必经过原点。没有偏置的话，当所有输入都是 0 时输出也只能是 0。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 激活值 / 激活 (Activation)

每个神经元在接收仿射变换结果 $z$ 后，经过激活函数 $\sigma(z)$ 得到的输出值 $a$。"激活"一词借鉴自生物神经科学——神经元被"激活"才会发出信号。

> 易混淆：**激活函数 (Activation Function)** — 激活函数是那个函数本身（如 ReLU、Sigmoid），激活值是把具体数字代入函数后得到的结果

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3

### 预激活 (Pre-activation)

激活函数之前的中间结果 $z = Wx + b$，也叫 logits（在输出层使用 Softmax 之前时）。这个值在反向传播时需要被记住（缓存），用来计算梯度。

> 别名：**logits**（输出层 Softmax 之前）/ **net input**（早期神经网络文献）— logits 特指分类任务最后一层的原始分数

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.2.2

### 计算图 (Computational Graph)

用有向无环图（DAG）表示前向传播中的每一步运算：节点代表变量或运算，边代表数据流向。PyTorch 在前向传播时自动构建计算图，反向传播时沿着图的反方向计算梯度。

> 别名：**计算流图**（TensorFlow 早期术语）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5.1

### 中间变量缓存 (Intermediate Cache)

前向传播过程中保存的中间计算结果（如每一层的预激活值 $z$ 和激活值 $a$）。这些值在反向传播计算梯度时是必需的，所以必须暂存在内存中。这就是为什么训练时的显存占用远大于推理——推理不需要保存中间值。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5.2

---

## 概念辨析

### 前向传播 vs 反向传播

| 维度 | 前向传播 (Forward Propagation) | 反向传播 (Backpropagation) |
|------|------|------|
| **本质** | 计算预测值和损失 | 计算梯度（偏导数） |
| **数据流方向** | 输入层 → 输出层 | 输出层 → 输入层 |
| **数学核心** | 矩阵乘法 + 激活函数 | 链式法则 |
| **内存需求** | 需缓存中间值 | 消费前向传播缓存的中间值 |
| **训练 vs 推理** | 两者都需要 | 仅训练时需要 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

### 仿射变换 vs 线性变换

| 维度 | 仿射变换 | 线性变换 |
|------|---------|---------|
| **公式** | $z = Wx + b$ | $z = Wx$ |
| **是否过原点** | 不一定 | 必须过原点 |
| **有无偏置** | 有 $b$ | 无 |
| **在神经网络中** | 实际使用的都是仿射变换 | 口语中常说"线性层"但其实是仿射 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

### 训练模式 vs 推理模式 (前向传播的差异)

| 维度 | 训练模式 (Training) | 推理模式 (Inference) |
|------|------|------|
| **计算图** | 构建并保存 | 不构建 (`torch.no_grad()`) |
| **中间值缓存** | 保存（供反向传播用） | 不保存 |
| **Dropout** | 随机丢弃神经元 | 所有神经元参与 |
| **BatchNorm** | 使用当前 batch 统计量 | 使用全局滑动平均 |
| **显存占用** | 高 | 低 |

> 📖 Docs: [PyTorch model.train() vs model.eval()](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.train)

---

## 核心属性

### 信息架构

    输入 x
      │
      ▼
    ┌────────────────────┐
    │ Layer 1             │
    │ z₁ = W₁x + b₁      │  ← 仿射变换
    │ a₁ = σ(z₁)          │  ← 激活函数
    └────────────────────┘
      │
      ▼
    ┌────────────────────┐
    │ Layer 2             │
    │ z₂ = W₂a₁ + b₂     │
    │ a₂ = σ(z₂)          │
    └────────────────────┘
      │
      ▼
     ŷ (预测)
      │
      ▼
    L(ŷ, y) = 损失值

### 适用场景 ✅

- 所有基于神经网络的模型都使用前向传播
- 分类、回归、生成、序列建模等任务
- 无论是 MLP、CNN、RNN 还是 Transformer

### 不适用场景 ❌

- 基于规则的专家系统（不需要神经网络）
- 基于检索的方法（如 KNN 不涉及参数和前向传播）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 前向传播公式 | $a^{(l)} = \sigma(W^{(l)} a^{(l-1)} + b^{(l)})$ | 每一层的通用计算 |
| 输入层 | $a^{(0)} = x$ | 不做任何变换 |
| 输出层 | 取决于任务：Softmax（分类）、恒等（回归） | $\hat{y} = \text{softmax}(z^{(L)})$ |
| 训练时注意 | 需要保存中间值供反向传播使用 | `z` 和 `a` 都要存 |
| 推理时优化 | 用 `torch.no_grad()` 关闭计算图 | 减少显存占用 |
