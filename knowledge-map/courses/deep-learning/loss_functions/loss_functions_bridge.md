---
topic: loss_functions
dimension: bridge
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Loss Functions 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 概率论 / MLE | 损失函数 = 负对数似然 | — |
| ← 前置 | 信息论 / 熵 | 交叉熵衡量分布差距 | — |
| ← 前置 | 激活函数 | 输出层激活与 loss 一起决定梯度行为 | [activation_functions_map.md](../activation_functions/activation_functions_map.md) |
| → 后续 | Optimizers | 优化器最小化损失函数 | [optimizers_map.md](../optimizers/optimizers_map.md) |
| → 后续 | Metrics | Loss 用于训练，Metrics 用于评估 | — |
| → 后续 | 正则化 | L1/L2 正则化项加在 loss 上 | — |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| 概率论 | MLE, 概率分布 | 损失函数 = 负对数似然；MSE ← 高斯，CE ← Bernoulli/Categorical |
| 信息论 | 熵, KL 散度 | 交叉熵 = 熵 + KL 散度；最小化 CE = 最小化 KL |
| 微积分 | 偏导数, 链式法则 | 计算 loss 对每个参数的梯度 |
| 激活函数 | Sigmoid, Softmax | 输出层激活与 loss 配对设计（梯度消除饱和） |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3, Ch.6

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| Optimizers | loss 值和梯度 | 优化器接收 $\nabla L$ 来更新权重 |
| 反向传播 | $\partial L / \partial \hat{y}$ | 反向传播的起点——从 loss 层开始 |
| Keras compile | `loss` 参数 | `model.compile(loss=...)` |
| 正则化 | 基础 loss | $L_{\text{total}} = L_{\text{data}} + \lambda L_{\text{reg}}$ |
| 模型评估 | training/val loss | 通过 loss 曲线判断过拟合/欠拟合 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, Ch.7

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化 |
|------|-------------|-------------|------|
| 分类损失 | MSE (1980s MLP) | Cross-Entropy (1990s+) | 消除 Sigmoid 饱和梯度问题 |
| 不平衡处理 | 过采样/欠采样 | Focal Loss (2017) | 在 loss 层面自适应权重 |
| 标签格式 | one-hot + CCE | 整数 + Sparse CCE | 节省内存，使用更方便 |
| 数值稳定 | clip + log | `from_logits=True` | 在 loss 内部做 log-softmax 更稳定 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Goodfellow, Deep Learning Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 损失函数与输出单元的完整理论 | ⭐⭐⭐ |
| [Bishop, PRML Ch.4](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 交叉熵从 MLE 推导的经典讲解 | ⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| Lin et al., ICCV 2017 | Focal vs Standard CE 在目标检测中的效果 | 处理类别不平衡时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Keras Losses API](https://keras.io/api/losses/) | 所有可用 loss 函数和用法 | 选择和使用 loss 时 |
| Szegedy et al., 2016 | Label Smoothing 原始论文 | 要减少模型过度自信时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 训练组件 | 1 | [Optimizers](../optimizers/optimizers_map.md) | 优化器最小化 loss 函数 |
| 网络组件 | 1 | [Activation Functions](../activation_functions/activation_functions_map.md) | 输出层激活与 loss 配对 |
| 网络架构 | 2 | [MLP](../mlp/mlp_map.md), [CNN](../cnn/cnn_map.md) | 不同架构使用的 loss 配置 |
| 框架工具 | 2 | [Keras](../keras/keras_map.md), [Scikit-Learn](../../ml/scikit_learn/scikit_learn_map.md) | compile(loss=...) 和 隐式 loss |
