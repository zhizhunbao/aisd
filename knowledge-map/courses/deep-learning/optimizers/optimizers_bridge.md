---
topic: optimizers
dimension: bridge
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Optimizers 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 反向传播 | 优化器使用反向传播计算的梯度来更新权重 | — |
| ← 前置 | 损失函数 | 优化器最小化损失函数 | — |
| ← 前置 | 激活函数 | 激活函数的梯度特性影响优化器的效果 | [activation_functions_map.md](../activation_functions/activation_functions_map.md) |
| → 后续 | 学习率调度 | 在训练过程中动态调整学习率 | — |
| → 后续 | 权重初始化 | 初始化策略影响优化器的收敛速度 | — |
| → 后续 | 正则化 | 权重衰减/Dropout 与优化器协同工作 | — |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| 微积分 | 梯度、链式法则 | 优化器使用梯度来确定更新方向 |
| 线性代数 | 向量运算、范数 | 参数更新、动量累积、梯度裁剪 |
| 概率论/统计 | 期望、方差、无偏估计 | Adam 的矩估计和偏差修正 |
| 反向传播 | $\frac{\partial L}{\partial W}$ | 优化器的输入——每个参数的梯度 |
| 损失函数 | $L(y, \hat{y})$ | 优化器最小化的目标函数 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| MLP | solver 参数 | scikit-learn MLPClassifier 的 solver='adam'/'sgd'/'lbfgs' |
| Keras compile | optimizer 参数 | model.compile(optimizer=...) 配置训练策略 |
| CNN 训练 | SGD+Momentum | ImageNet 训练的标准配置（SGD+lr_schedule） |
| Transformer | AdamW | BERT/GPT 训练的标准优化器 |
| 学习率调度 | 学习率概念 | StepLR, CosineAnnealing 等基于初始 lr 的调度策略 |
| 超参数调优 | lr, batch_size | 最重要的两个超参数 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化 |
|------|-------------|-------------|------|
| 默认优化器 | SGD (2010 前) | Adam (2015+) | 自适应学习率成为标准 |
| 学习率设置 | 手动固定值 | 自适应 + 调度器 | 减少人工调参 |
| Transformer 优化器 | Adam (2017) | AdamW (2019+) | 解耦权重衰减 |
| CV 最佳实践 | SGD+固定 lr | SGD+Cosine Annealing | 学习率调度至关重要 |
| sklearn solver | 'lbfgs' 默认 | 'adam' 默认 (>0.22) | 适应更大数据集 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Goodfellow, Deep Learning Ch.8](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 优化器的完整理论基础 | ⭐⭐⭐ |
| [Kingma & Ba, ICLR 2015](https://arxiv.org/abs/1412.6980) | 📖 论文 | Adam 的原始论文，推导简洁优美 | ⭐⭐ |
| [Ruder, arXiv 2016](https://arxiv.org/abs/1609.04747) | 📖 论文 | 最好的梯度下降优化方法综述 | ⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| Wilson et al., NeurIPS 2017 | "Adam 泛化不如 SGD" 的实验分析 | 理解 Adam vs SGD 争论 |
| Loshchilov & Hutter, ICLR 2019 | AdamW 解耦权重衰减 | Transformer 训练时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Keras LR Schedules](https://keras.io/api/optimizers/learning_rate_schedules/) | 学习率调度策略 | 精细调参时 |
| Smith, arXiv 2017 | Cyclical Learning Rates | 想用一次训练找到最优 lr 时 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 网络架构 | 2 | [MLP](../mlp/mlp_map.md), [CNN](../cnn/cnn_map.md) | 不同架构推荐的优化器 |
| 网络组件 | 1 | [Activation Functions](../activation_functions/activation_functions_map.md) | 激活函数梯度影响优化器效果 |
| 训练问题 | 1 | [Vanishing Gradient](../vanishing_gradient/vanishing_gradient_map.md) | 梯度消失使优化器失效 |
| 框架工具 | 2 | [Keras](../keras/keras_map.md), [Scikit-Learn](../../ml/scikit_learn/scikit_learn_map.md) | compile/solver API |
