---
topic: neural_network
dimension: bridge
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6,9,10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Neural Network (神经网络) 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, Ch.9, Ch.10

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 线性回归/逻辑回归 | 可看作无隐藏层的单神经元网络 | — |
| ← 前置 | 梯度下降 | 神经网络训练的核心优化算法 | — |
| → 后续 | MLP (多层感知机) | 最基础的前馈网络实例 | [mlp_map.md](../mlp/mlp_map.md) |
| → 后续 | Dense Layer (全连接层) | 神经网络中最常见的层类型 | [dense_layer_map.md](../dense_layer/dense_layer_map.md) |
| → 后续 | Activation Functions | 激活函数的选择直接影响网络性能 | [activation_functions_map.md](../activation_functions/activation_functions_map.md) |
| → 后续 | Loss Functions | 损失函数定义了训练目标 | [loss_functions_map.md](../loss_functions/loss_functions_map.md) |
| → 后续 | Optimizers | 优化器决定参数更新策略 | [optimizers_map.md](../optimizers/optimizers_map.md) |
| → 后续 | CNN (卷积神经网络) | 专门处理网格数据的神经网络变体 | [cnn_map.md](../cnn/cnn_map.md) |
| → 后续 | Transformer | 基于注意力机制的神经网络架构 | [transformer_map.md](../transformer/transformer_map.md) |
| → 后续 | Vanishing Gradient | 深层网络训练的核心挑战 | [vanishing_gradient_map.md](../vanishing_gradient/vanishing_gradient_map.md) |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| 线性代数 | 矩阵乘法、向量运算 | 每层前向传播的核心运算 $\mathbf{z} = \mathbf{Wx} + \mathbf{b}$ |
| 微积分 | 链式法则、偏导数 | 反向传播：逐层计算梯度 |
| 概率论 | 极大似然估计 | 交叉熵损失 = 负对数似然 |
| 优化理论 | 梯度下降 | 参数更新规则 $\theta \leftarrow \theta - \eta \nabla \mathcal{L}$ |

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| MLP | 前向传播、反向传播、激活函数 | MLP 是最直接的全连接前馈网络实例 |
| CNN | 层、权重共享、反向传播 | CNN 在空间维度引入卷积替代全连接 |
| RNN | 层、激活函数、反向传播 | RNN 在时间维度引入循环连接 |
| Transformer | 层堆叠、残差连接、归一化 | Transformer 用注意力替代循环和卷积 |
| GANs | 网络作为函数近似器 | 生成器和判别器都是神经网络 |
| 迁移学习 | 预训练权重、层冻结 | 复用大网络的底层特征表示 |

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 激活函数 | Sigmoid/Tanh（模仿生物神经元发放率） | ReLU/GELU（纯工程考量，利于梯度传播） | Sigmoid 梯度消失 → ReLU 解决 |
| 权重初始化 | 小随机数 | Xavier/He 初始化（根据层宽度自适应缩放） | 理论分析了方差传播条件 |
| 训练方法 | 逐层贪心预训练 + 微调 | 端到端训练（直接 Backprop） | ReLU + BatchNorm + 残差连接使直接训练可行 |
| 网络深度 | 2-3 层（更深训不动） | 100+ 层（ResNet 152 层） | 残差连接解决了退化问题 |
| 宽度理解 | UAT：一层足够宽就行 | 深度比宽度更高效（指数 vs 线性） | 理论 + 实践双重验证 |
| 损失函数 | MSE（一刀切） | 任务特定：CE + Label Smoothing + Focal Loss | 不同任务需要不同的优化目标 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3, Ch.8

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Goodfellow《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 前馈网络的完整理论，包含 UAT 证明思路 | ⭐⭐⭐ |
| [Rumelhart et al. 1986](https://www.nature.com/articles/323533a0) | 📖 论文 | 反向传播的原始论文，简短精炼 | ⭐⭐ |
| [Hornik et al. 1989](https://doi.org/10.1016/0893-6080(89)90020-8) | 📖 论文 | UAT 的严格数学证明 | ⭐⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [SVM vs Neural Network](https://www.cs.toronto.edu/~hinton/) | 核方法 vs 表征学习 | 理解为什么深度学习取代了 SVM |
| [Decision Trees vs NN](../../../textbooks/goodfellow_deep_learning.pdf) | 可解释 vs 黑盒权衡 | 选择模型时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [CS231n](https://cs231n.stanford.edu/) | Stanford CV 课程，一从 NN 基础到 CNN/RNN/GAN | 想系统学习深度学习实践 |
| [Deep Learning Specialization](https://www.deeplearning.ai/) | Andrew Ng 的深度学习系列课 | 从零开始系统学习 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 同课程主题 | 16 | mlp, cnn, transformer, dense_layer, activation_functions | NN 是所有这些主题的共同基础 |
| 下游课程 | 3+ | NLP, Computer Vision, Reinforcement Learning | NN 是所有下游应用的核心工具 |
| 框架主题 | 3 | pytorch, tensorflow, keras | 实现 NN 的三大主流框架 |
