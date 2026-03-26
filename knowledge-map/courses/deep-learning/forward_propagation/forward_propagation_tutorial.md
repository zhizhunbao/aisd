---
topic: forward_propagation
dimension: tutorial
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow, Bengio & Courville, Deep Learning, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: PyTorch nn.Module — https://pytorch.org/docs/stable/generated/torch.nn.Module.html"
  - "📖 Docs: PyTorch nn.Linear — https://pytorch.org/docs/stable/generated/torch.nn.Linear.html"
expiry: 12m
status: current
---

# Forward Propagation 教程

> **前置知识：** 矩阵乘法、激活函数（ReLU/Sigmoid）、全连接层概念
> **参考来源：** Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## Section 0: 前置知识速查

1. **矩阵乘法**：$(m, n) \times (n, p) \to (m, p)$，行乘列求和
2. **激活函数**：ReLU($z$) = max(0, $z$)，引入非线性
3. **全连接层**：每个神经元与上一层所有神经元相连，由权重矩阵 $W$ 和偏置 $b$ 参数化

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **没有前向传播，神经网络无法产生任何输出**：你定义了网络结构和参数，但数据进不去、结果出不来——就像搭了管道但没通水
- 🔥 **没有前向传播，反向传播无法工作**：反向传播需要前向传播过程中保存的中间值（$z$ 和 $a$）来计算梯度；没有前向传播就没有这些中间值
- 🔥 **不理解前向传播，会不知道 shape mismatch 错误从哪来**：RuntimeError 说矩阵维度不匹配，但你不知道每一层的输入输出形状是怎么算的

### 它的核心价值

1. **从输入到输出的计算流**：把一个任意复杂的函数分解成一连串简单操作——每层做一次矩阵乘法 + 一次非线性变换
2. **自动构建计算图**：PyTorch 在前向传播时自动记录每一步运算，为反向传播提供"回忆路径"
3. **推理的核心**：训练完成后的模型部署、线上预测，本质上就是固定参数后跑一次前向传播

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

    ┌─────────────┐
    │  输入数据 x   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────────────────┐
    │  Layer 1: 仿射变换       │  z₁ = W₁·x + b₁
    │  Layer 1: 激活           │  a₁ = ReLU(z₁)
    │  [缓存 z₁, a₁ 到内存]    │
    └──────┬──────────────────┘
           │
           ▼
    ┌─────────────────────────┐
    │  Layer 2: 仿射变换       │  z₂ = W₂·a₁ + b₂
    │  Layer 2: 激活           │  a₂ = ReLU(z₂)
    │  [缓存 z₂, a₂ 到内存]    │
    └──────┬──────────────────┘
           │
           ▼
    ┌─────────────────────────┐
    │  输出层: 仿射变换         │  z₃ = W₃·a₂ + b₃
    │  输出层: Softmax / 恒等   │  ŷ = softmax(z₃)
    └──────┬──────────────────┘
           │
           ▼
    ┌─────────────────────────┐
    │  损失计算                 │  ℒ = CrossEntropy(ŷ, y)
    └─────────────────────────┘

### 2.2 核心机制

**为什么每层都需要激活函数？**

如果没有激活函数，多层线性变换的组合仍然是线性变换：
$W_2(W_1 x + b_1) + b_2 = W_2 W_1 x + W_2 b_1 + b_2 = W' x + b'$

这等价于一个单层网络，深度白费了。激活函数打破线性，让每一层都能在上一层的基础上构建更复杂的特征。

**为什么要缓存中间值？**

反向传播需要用到前向传播的中间结果。例如：
- ReLU 的导数需要知道 $z$ 是正还是负
- 全连接层参数的梯度 $\frac{\partial \mathcal{L}}{\partial W} = \frac{\partial \mathcal{L}}{\partial z} \cdot a^T$ 需要上一层的激活值 $a$

这就是训练时显存远大于推理的原因——中间值全要存着。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3, Ch.6.5

---

## Section 3: 局限性

1. **显存瓶颈** → 前向传播需要缓存所有层的中间值供反向传播使用，深网络的显存消耗与层数成正比。**应对：** 梯度检查点（Gradient Checkpointing）——只保存部分层的中间值，需要时重新前向计算
2. **计算是串行的** → 每一层必须等上一层算完才能开始（层间依赖）。**应对：** 流水线并行（Pipeline Parallelism）可以跨设备重叠不同 micro-batch 的不同层
3. **数值不稳定** → 深层网络中，数值可能在逐层传播中变得极大或极小（梯度消失/爆炸的前兆从前向传播就开始了）。**应对：** BatchNorm、残差连接、合理的权重初始化

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.2.1

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **标准前向传播** | 简单直接，自动生成计算图 | 内存随深度线性增长 | 大部分训练和推理 |
| **梯度检查点** | 显存占用降为 $O(\sqrt{L})$ | 计算时间增加约 33% | 深网络、大模型训练 |
| **推理模式 (`torch.no_grad()`)** | 不构建计算图，不缓存中间值 | 无法反向传播 | 纯推理/部署 |
| **混合精度前向传播 (AMP)** | FP16 计算更快，显存减半 | 部分层需要 FP32 保持精度 | GPU 训练加速 |

> 📖 Docs: [PyTorch Automatic Mixed Precision](https://pytorch.org/docs/stable/amp.html)

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考 |
| [PyTorch nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html) | 📖 文档 | Section 2 流程 |
| [PyTorch AMP](https://pytorch.org/docs/stable/amp.html) | 📖 文档 | Section 4 方案对比 |
