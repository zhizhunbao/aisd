---
topic: activation_functions
dimension: bridge
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6, Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
expiry: 12m
status: current
---

# Activation Functions 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 线性代数（矩阵乘法） | 激活函数作用于线性变换 $z=Wx+b$ 的输出 | — |
| ← 前置 | 微积分（链式法则） | 反向传播需要激活函数的梯度 | — |
| ← 前置 | MLP（多层感知器） | 激活函数是 MLP 每层的核心组件 | [mlp_map.md](../mlp/mlp_map.md) |
| → 后续 | Dense Layer | Dense 层包含线性变换 + 激活 | [dense_layer_map.md](../dense_layer/dense_layer_map.md) |
| → 后续 | Conv Layer | 卷积后也需要激活函数 | [conv_layer_map.md](../conv_layer/conv_layer_map.md) |
| → 后续 | 梯度消失 / 爆炸问题 | 激活函数选择直接决定梯度行为 | [vanishing_gradient_map.md](../vanishing_gradient/vanishing_gradient_map.md) |
| → 后续 | Transformer | GELU 是 Transformer 的标配激活 | [transformer_map.md](../transformer/transformer_map.md) |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| 线性代数 | 矩阵乘法 $z = Wx + b$ | 激活函数的输入 $z$ 是线性变换的输出 |
| 微积分 | 链式法则、导数 | 反向传播需要计算 $g'(z)$，激活函数的梯度是训练的关键 |
| 概率论 | 概率分布、CDF | Sigmoid 输出概率，Softmax 输出概率分布，GELU 用标准正态 CDF |
| 感知机 | 阈值函数 | 激活函数是阈值函数（阶跃函数）的光滑可微替代品 |

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| MLP | ReLU/Sigmoid/Tanh | 隐藏层用 ReLU，输出层根据任务选激活 |
| Dense Layer | `activation` 参数 | Dense 层的核心参数之一 |
| Conv Layer | `activation` 参数 | 卷积后施加激活函数提取非线性特征 |
| CNN 架构 | ReLU 家族 | AlexNet→ResNet 全部使用 ReLU 系列 |
| Transformer | GELU | BERT/GPT 的 FFN 层使用 GELU |
| RNN/LSTM | Sigmoid + Tanh | 门控机制用 Sigmoid，隐藏状态用 Tanh |
| 权重初始化 | 激活函数的梯度特性 | He 初始化专为 ReLU 设计，Xavier 专为 Sigmoid/Tanh 设计 |
| 梯度消失问题 | 饱和 vs 非饱和 | 激活函数的饱和性是梯度消失的根本原因之一 |
| BatchNorm | 激活前/后 | BatchNorm 通常放在激活函数之前，与激活函数协同工作 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, Ch.8

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化 |
|------|-------------|-------------|------|
| 隐藏层默认激活 | Sigmoid (1986-2010) | ReLU (2010-至今) | Sigmoid 梯度消失 → ReLU 梯度恒1 |
| Transformer 激活 | ReLU (Vaswani 2017) | GELU (BERT 2018+) | GELU 更光滑，表现更稳定 |
| 负区间处理 | 截断为 0 (ReLU) | 保留小梯度 (Leaky/ELU) | 避免死神经元 |
| 设计方法 | 手工设计 + 直觉 | 自动搜索 (NAS for activation) | Swish 是机器搜索到的最优解 |
| 二分类输出 | Sigmoid + MSE | Sigmoid + BCE | 从回归损失换为交叉熵，梯度更好 |
| scikit-learn 命名 | `'logistic'` (Sigmoid) | 仍然是 `'logistic'` | 不同于 Keras 的 `'sigmoid'`，需要注意 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Goodfellow, Deep Learning Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 激活函数的数学理论和设计动机 | ⭐⭐⭐ |
| Nair & Hinton, ICML 2010 | 📖 论文 | ReLU 的原始提出，理解为什么简单有效 | ⭐⭐ |
| Glorot & Bengio, AISTATS 2010 | 📖 论文 | 深度分析 Sigmoid/Tanh 在深层网络中的问题 | ⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| Ramachandran et al., arXiv 2017 | Swish vs ReLU 在多种任务上的对比 | 需要选择最优激活函数时 |
| Hendrycks & Gimpel, arXiv 2016 | GELU vs ReLU vs ELU 的理论和实验对比 | 设计 Transformer 网络时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| He et al., ICCV 2015 | PReLU + He 初始化，激活函数与初始化的协同设计 | 深层 CNN 架构设计时 |
| Klambauer et al., NeurIPS 2017 | SELU + 自归一化网络，激活函数可以替代 BatchNorm | 探索无 BN 的网络设计时 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 网络架构 | 2 | [MLP](../mlp/mlp_map.md), [CNN](../cnn/cnn_map.md) | 激活函数在不同架构中的使用方式 |
| 网络层 | 2 | [Dense Layer](../dense_layer/dense_layer_map.md), [Conv Layer](../conv_layer/conv_layer_map.md) | `activation` 参数的具体用法 |
| 池化层 | 2 | [Max Pool](../max_pool_layer/max_pool_layer_map.md), [Avg Pool](../avg_pool_layer/avg_pool_layer_map.md) | 池化层不需要激活函数 |
| 训练问题 | 1 | [Vanishing Gradient](../vanishing_gradient/vanishing_gradient_map.md) | 激活函数选择如何影响梯度传播 |
| 框架工具 | 2 | [Keras](../keras/keras_map.md), [Scikit-Learn](../../ml/scikit_learn/scikit_learn_map.md) | 不同框架中的激活函数 API |
| 高级架构 | 1 | [Transformer](../transformer/transformer_map.md) | GELU 在 Transformer 中的角色 |
