---
topic: forward_propagation
dimension: bridge
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow, Bengio & Courville, Deep Learning, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Forward Propagation 衔接与扩展

> 📚 Book: Goodfellow, Bengio & Courville, [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 全连接层 (Dense Layer) | 前向传播的"硬件"——每一层的仿射变换由全连接层实现 | [dense_layer_map.md](../dense_layer/dense_layer_map.md) |
| ← 前置 | 激活函数 (Activation Functions) | 前向传播的非线性组件 | [activation_functions_map.md](../activation_functions/activation_functions_map.md) |
| ← 前置 | 张量 (Tensor) | 前向传播操作的数据结构 | [tensor_map.md](../tensor/tensor_map.md) |
| → 后续 | 反向传播 (Backpropagation) | 利用前向传播缓存的中间值计算梯度 | — |
| → 后续 | 损失函数 (Loss Functions) | 前向传播的终点——计算预测与真实值的差距 | [loss_functions_map.md](../loss_functions/loss_functions_map.md) |
| → 后续 | 优化器 (Optimizers) | 用反向传播得到的梯度更新前向传播的参数 | [optimizers_map.md](../optimizers/optimizers_map.md) |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| 全连接层 | 权重矩阵 $W$、偏置 $b$ | 前向传播每层的仿射变换 $z = Wx + b$ |
| 激活函数 | ReLU、Sigmoid 等函数 | 每层仿射变换后应用非线性 $a = \sigma(z)$ |
| 张量 | 多维数组运算 | 所有前向传播的输入/中间值/输出都是张量 |
| 矩阵乘法 | 线性代数基础运算 | 仿射变换的核心运算 |

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| 反向传播 | 计算图、缓存的中间值 ($z$, $a$) | 反向传播沿计算图反向遍历，用中间值计算梯度 |
| 梯度消失 | 激活值的数值范围 | 前向传播中激活值过小会导致反向传播梯度接近零 |
| CNN 前向传播 | 逐层变换的范式 | CNN 用卷积替代矩阵乘法，但前向传播的"逐层 + 激活"范式不变 |
| Transformer | 注意力机制的前向计算 | Transformer 的前向传播包含 Self-Attention + FFN，但基本模式相同 |
| 模型部署 | 固定参数的前向传播 | 推理 = 固定权重后跑一次前向传播，不需要反向传播 |

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 前向传播 | 单层感知机：输入→加权求和→阈值 | 多层深度网络：逐层仿射+激活+残差 | 通用近似定理证明多层必要性 |
| 中间值缓存 | 不需要（无反向传播） | 必须保存供反向传播使用 | 反向传播算法的发明 |
| 激活函数 | 阶跃函数（0/1） | ReLU、GELU、Swish | 阶跃函数不可导，无法反向传播 |
| 批量计算 | 逐样本计算 | Mini-batch 矩阵运算 | GPU 并行加速 |

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Goodfellow Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 最权威的前向传播公式推导 | ⭐⭐ |
| [Rumelhart et al. 1986](https://doi.org/10.1038/323533a0) | 📖 论文 | 前向传播+反向传播的经典原文 | ⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| CNN 前向传播 vs MLP 前向传播 | 卷积 vs 矩阵乘法 | 学完 MLP 后 |
| RNN 前向传播 vs 标准前向传播 | 时间步展开 vs 纯前馈 | 学 RNN 时 |
| Transformer 前向传播 | 注意力 + FFN | 学 Transformer 时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| 模型推理优化 (TensorRT, ONNX) | 前向传播的工业化 | 准备部署模型时 |
| 梯度检查点 (Gradient Checkpointing) | 用计算换显存 | 训练大模型时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 直接前置 | 3 | dense_layer, activation_functions, tensor | 前向传播的组件来源 |
| 直接后续 | 3 | loss_functions, optimizers, vanishing_gradient | 前向传播产出的消费者 |
| 同课程 | 17 | mlp, cnn, transformer, pytorch... | 不同架构的前向传播变体 |
