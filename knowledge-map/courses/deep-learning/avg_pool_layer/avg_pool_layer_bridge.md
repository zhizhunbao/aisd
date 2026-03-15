---
topic: avg_pool_layer
dimension: bridge
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Lin et al., 'Network in Network', ICLR 2014 — https://arxiv.org/abs/1312.4400"
  - "📖 Paper: Hu et al., 'Squeeze-and-Excitation Networks', CVPR 2018 — https://arxiv.org/abs/1709.01507"
expiry: 12m
status: current
---

# Avg Pool Layer 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Max Pool Layer | AvgPool 是 MaxPool 的互补方案 | [max_pool_layer_map.md](../max_pool_layer/max_pool_layer_map.md) |
| ← 前置 | Conv Layer | AvgPool 紧跟 Conv 之后做下采样 | [conv_layer_map.md](../conv_layer/conv_layer_map.md) |
| ← 前置 | Dense Layer | GAP 是 Dense/FC 层的零参数替代方案 | [dense_layer_map.md](../dense_layer/dense_layer_map.md) |
| → 后续 | Inception 架构 | AvgPool 作为 Inception 的并行分支之一 | — |
| → 后续 | SE-Net (Squeeze & Excitation) | GAP 作为通道注意力的 Squeeze 操作 | — |
| → 后续 | Mean Pooling (NLP) | GAP 思想在序列维度的应用 (BERT) | [transformer_map.md](../transformer/transformer_map.md) |
| → 后续 | GeM Pooling | Generalized Mean — AvgPool 的参数化推广 | — |
| → 后续 | CAM (Class Activation Map) | GAP 赋能的分类可视化技术 | — |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|----------|-----------|-------------------|
| Max Pool Layer | 滑动窗口、stride、padding 机制 | AvgPool 使用完全相同的窗口滑动逻辑 |
| Max Pool Layer | 输出尺寸公式 | AvgPool 与 MaxPool 共享相同的公式 |
| Conv Layer | 特征图 (Feature Map) | AvgPool 的输入是卷积层输出的特征图 |
| Dense Layer | 参数量/过拟合问题 | GAP 替代 Dense 的动机来自 Dense 的参数量问题 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1–9.3

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|----------|----------------|-----------------|
| ResNet / EfficientNet | GAP 分类头 | GAP + 单层 FC 是标准分类头设计 |
| Inception / GoogLeNet | AvgPool 分支 | 并行 AvgPool 分支与 MaxPool/Conv 分支互补 |
| SE-Net | GAP 作为 Squeeze | 通道统计量生成 → 通道注意力权重 |
| CAM / Grad-CAM | GAP 的可解释性 | 因为 GAP 使通道与类别对应，可以可视化判据 |
| BERT / NLP | Mean Pooling | 对 token 维度取平均生成句子级表示 |
| 图像检索 | GeM Pooling | $L^p$ 范数推广 AvgPool ($p=1$) 到 MaxPool ($p→∞$) |

> 📖 Paper: Hu et al., [SE-Net](https://arxiv.org/abs/1709.01507), CVPR 2018

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化 |
|------|-------------|-------------|------|
| 中间层下采样 | AvgPool (LeNet) | MaxPool 或 Strided Conv | AvgPool 在中间层地位下降 |
| 分类头 | Flatten + FC (VGG) | GAP + 单层 FC (ResNet) | GAP 成为标准分类头 |
| 通道聚合 | 无专门机制 | GAP → SE 注意力 | GAP 从分类头扩展到注意力 |
| NLP 序列表示 | [CLS] token (BERT) | Mean Pooling (Sentence-BERT) | AvgPool 思想进入 NLP |
| 聚合范式 | 固定 Avg 或 Max | GeM (可学习 $L^p$ 范数) | 从离散选择到连续参数化 |

> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------|
| [Goodfellow Ch.9.3–9.4](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 池化的理论基础，AvgPool vs MaxPool 的先验解释 | ⭐⭐ |
| [Lin et al. 2014 (NiN)](https://arxiv.org/abs/1312.4400) | 📖 论文 | GAP 的原始提出，替代 FC 层的理论依据 | ⭐⭐ |
| [Boureau et al. 2010](https://proceedings.mlr.press/v9/boureau10a.html) | 📖 论文 | Max vs Avg Pooling 的理论分析（信噪比证明） | ⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|-------|
| [max_pool_layer](../max_pool_layer/max_pool_layer_map.md) | Avg vs Max 完整对比 | 选择池化方案时 |
| [Radenović et al. 2019](https://arxiv.org/abs/1711.02512) | GeM vs GAP vs GMP 在图像检索中的对比 | 做图像检索时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|-------|
| [Hu et al. 2018 (SE-Net)](https://arxiv.org/abs/1709.01507) | GAP 作为通道注意力核心 | 做通道注意力设计时 |
| [Zhou et al. 2016 (CAM)](https://arxiv.org/abs/1512.04150) | GAP 赋能类别激活可视化 | 需要可解释 AI 时 |
| [Reimers 2019 (Sentence-BERT)](https://arxiv.org/abs/1908.10084) | Mean Pooling 生成句子嵌入 | 做 NLP 句子表示时 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 对比层 | 1 | [max_pool_layer](../max_pool_layer/max_pool_layer_map.md) | AvgPool 与 MaxPool 的互补关系 |
| 前置层 | 2 | [conv_layer](../conv_layer/conv_layer_map.md), [dense_layer](../dense_layer/dense_layer_map.md) | AvgPool 在 Conv→Dense 之间的角色 |
| CNN 架构 | 1 | [cnn](../cnn/cnn_map.md) | GAP 在完整 CNN 中的分类头位置 |
| 后续架构 | 1 | [transformer](../transformer/transformer_map.md) | Mean Pooling 在 Transformer 中的应用 |
| 框架 | 2 | [pytorch](../pytorch/pytorch_map.md), [keras](../keras/keras_map.md) | AvgPool 的双平台 API 差异 |
