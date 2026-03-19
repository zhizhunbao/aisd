---
topic: transfer_learning
dimension: bridge
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.15 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Pan & Yang, 'A Survey on Transfer Learning', IEEE TKDE 2010 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/transfer_learning/A_Survey_on_Transfer_Learning.pdf"
  - "📖 Paper: Zhuang et al., 'A Comprehensive Survey on Transfer Learning', Proc. IEEE 2020 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/transfer_learning/zhuang_2020_transfer_learning_survey.pdf"
expiry: 12m
status: current
---

# Transfer Learning 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.15
> 📖 Paper: Zhuang et al., [A Comprehensive Survey (2020)](../../../.documents/papers/transfer_learning/zhuang_2020_transfer_learning_survey.pdf)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | CNN 架构 | CNN 提供了可迁移的层级特征表示 | [cnn/](../cnn/cnn_map.md) |
| ← 前置 | 优化器 | Fine-tuning 需要精心选择学习率 | [optimizers/](../optimizers/optimizers_map.md) |
| ← 前置 | 损失函数 | KD Loss 基于 KL 散度和交叉熵 | [loss_functions/](../loss_functions/loss_functions_map.md) |
| → 后续 | Transformer | BERT/GPT 是迁移学习最成功的应用 | [transformer/](../transformer/transformer_map.md) |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| [CNN](../cnn/cnn_concepts.md) | 卷积层、特征图 | CNN 层级结构是特征可迁移性的基础 |
| [优化器](../optimizers/optimizers_concepts.md) | Adam, 学习率调度 | Fine-tuning 需要小 LR + warmup |
| [损失函数](../loss_functions/loss_functions_concepts.md) | KL 散度、交叉熵 | KD 使用 KL + CE 双损失 |
| [Transformer](../transformer/transformer_concepts.md) | Self-Attention | BERT/GPT 预训练-微调范式 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.15

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------| 
| NLP (BERT/GPT) | Pre-training + Fine-tuning | BERT 在 11 项基准刷新记录 |
| CV (ViT) | ImageNet 预训练 | ViT 预训练后迁移到各种 CV 任务 |
| 模型压缩 | Knowledge Distillation | 大模型教小模型，部署到边缘设备 |
| Few-shot | 预训练特征 | Foundation Model 无需训练就能做新任务 |

> 📖 Paper: Zhuang et al., [A Comprehensive Survey (2020)](../../../.documents/papers/transfer_learning/zhuang_2020_transfer_learning_survey.pdf)

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------| 
| 迁移对象 | 手工特征迁移 | 深度特征自动迁移 | 深度学习自动学习层级特征 |
| 预训练数据 | ImageNet (120 万) | Web-scale (数十亿) | 数据和算力增长 |
| 迁移方法 | Feature Extraction | LoRA (0.1% 参数) | 模型太大无法 Full Fine-tune |
| NLP 迁移 | Word2Vec (静态) | BERT/GPT (上下文) | Transformer 更深层理解 |

> 📖 Paper: Pan & Yang, [A Survey on Transfer Learning (2010)](../../../.documents/papers/transfer_learning/A_Survey_on_Transfer_Learning.pdf)

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------| 
| [Yosinski 2014](../../../.documents/papers/transfer_learning/yosinski_2014_transferable_features.pdf) | 📖 论文 | 量化每层可迁移性，必读 | ⭐⭐⭐ |
| [ULMFiT 2018](../../../.documents/papers/transfer_learning/howard_2018_ulmfit.pdf) | 📖 论文 | NLP 迁移方法论奠基 | ⭐⭐⭐ |
| [Zhuang 2020](../../../.documents/papers/transfer_learning/zhuang_2020_transfer_learning_survey.pdf) | 📖 论文 | 最全面综述 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [CNN](../cnn/cnn_map.md) | CV 迁移基础 | 了解预训练模型结构 |
| [Transformer](../transformer/transformer_map.md) | NLP 迁移基础 | 了解 BERT/GPT 架构 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| CNN 架构 | 3+ | [conv_layer](../conv_layer/), [max_pool_layer](../max_pool_layer/) | 预训练模型层级结构 |
| 基础组件 | 3+ | [activation_functions](../activation_functions/), [loss_functions](../loss_functions/) | Fine-tuning 基础知识 |
| 框架 | 3 | [pytorch](../pytorch/), [tensorflow](../tensorflow/), [keras](../keras/) | 工程实现 |
