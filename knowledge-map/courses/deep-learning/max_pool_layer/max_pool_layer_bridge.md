---
topic: max_pool_layer
dimension: bridge
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3–9.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Springenberg et al., 'Striving for Simplicity', ICLR 2015 — https://arxiv.org/abs/1412.6806"
  - "📖 Paper: Lin et al., 'Network in Network', ICLR 2014 — https://arxiv.org/abs/1312.4400"
expiry: 12m
status: current
---

# Max Pool Layer 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Conv Layer (卷积层) | MaxPool 紧跟 Conv 之后做下采样 | [conv_layer_map.md](../conv_layer/conv_layer_map.md) |
| ← 前置 | Dense Layer (全连接层) | MaxPool 减少的尺寸直接影响 FC 参数量 | [dense_layer_map.md](../dense_layer/dense_layer_map.md) |
| ← 前置 | CNN 架构 | MaxPool 是 CNN 逐层缩小的关键组件 | [cnn_map.md](../cnn/cnn_map.md) |
| → 后续 | Global Average Pooling | GAP 替代 FC 层的现代设计 | — |
| → 后续 | Strided Convolution | 可学习的下采样替代 Max Pooling | — |
| → 后续 | RoI Pooling / Align | 目标检测中 Max Pooling 的区域化扩展 | — |
| → 后续 | MaxUnpool (反池化) | 分割任务中恢复空间分辨率 | — |
| → 后续 | Attention 机制 | 更灵活的全局信息聚合替代方案 | [transformer_map.md](../transformer/transformer_map.md) |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|----------|-----------|-------------------|
| Conv Layer | 特征图 (Feature Map) | Max Pooling 的输入就是卷积层输出的特征图 |
| Conv Layer | 滑动窗口 (Sliding Window) | Max Pooling 同样使用滑动窗口在输入上移动 |
| Conv Layer | 步长 (Stride) | Max Pooling 的 stride 控制窗口移动速度和下采样率 |
| Conv Layer | 填充 (Padding) | Max Pooling 的 padding 使用 -∞ 填充（与 Conv 的零填充不同） |
| MLP | 感受野 (Receptive Field) | Max Pooling 通过下采样间接扩大后续层的感受野 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1–9.3

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|----------|----------------|-----------------|
| CNN 架构 | 空间下采样 | VGG/AlexNet 的 Conv Block 后必跟 MaxPool 实现逐层缩小 |
| 目标检测 | RoI Pooling | Faster R-CNN 将 MaxPool 推广到不规则 RoI 区域 |
| 语义分割 | MaxUnpool + argmax | SegNet 用前向的 argmax 索引做反池化恢复分辨率 |
| NLP | Max-over-time pooling | Kim (2014) TextCNN 用全局 Max Pooling 从序列中提取特征 |
| 3D 视觉 | MaxPool3d | 视频理解和医学图像中的 3D 版本 |
| Adaptive Pooling | AdaptiveMaxPool | 自适应输出尺寸，支持变尺寸输入 |

> 📖 Paper: Ren et al., [Faster R-CNN](https://arxiv.org/abs/1506.01497), NeurIPS 2015

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化 |
|------|-------------|-------------|------|
| 下采样方式 | MaxPool 2×2 stride 2 是唯一标准做法 | Strided Conv / Patch Merging 替代 | 从固定操作到可学习操作 |
| 分类头 | MaxPool → Flatten → FC 大全连接层 | GAP → 1×1 Conv 或直接 FC | GAP 替代了对池化+FC 的依赖 |
| 池化位置 | 每个 Conv Block 后都接 MaxPool | 仅首层或不用，靠 stride 控制尺寸 | ResNet 开始减少使用频率 |
| 平移不变性来源 | 主要依赖 MaxPool 提供 | Data Augmentation + 更深网络提供 | 不再唯一依赖池化 |
| NLP 中的池化 | Max-over-time pooling (TextCNN) | [CLS] token 或 Mean Pooling (BERT) | Attention 替代了显式池化 |

> 📖 Paper: Springenberg et al., [Striving for Simplicity](https://arxiv.org/abs/1412.6806), ICLR 2015

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------|
| [Goodfellow Ch.9.3–9.4](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 池化的理论基础：平移不变性、无限强先验 | ⭐⭐ |
| [Boureau et al. 2010](https://proceedings.mlr.press/v9/boureau10a.html) | 📖 论文 | 对 Max vs Average Pooling 的理论分析 | ⭐⭐⭐ |
| [Scherer et al. 2010](https://link.springer.com/chapter/10.1007/978-3-642-15825-4_10) | 📖 论文 | 首次系统比较 Max Pooling vs Average Pooling | ⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|-------|
| [Springenberg et al. 2015](https://arxiv.org/abs/1412.6806) | Strived Conv 能否替代 MaxPool | 设计新 CNN 架构时 |
| [Lin et al. 2014 (NiN)](https://arxiv.org/abs/1312.4400) | GAP vs FC+MaxPool | 减少模型参数量时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|-------|
| [Ren et al. 2015 (Faster R-CNN)](https://arxiv.org/abs/1506.01497) | RoI Pooling: MaxPool 在目标检测中的扩展 | 做目标检测时 |
| [Badrinarayanan et al. 2017 (SegNet)](https://arxiv.org/abs/1511.00561) | MaxUnpool: 用 argmax 索引做反池化做分割 | 做语义分割时 |
| [Kim 2014 (TextCNN)](https://arxiv.org/abs/1408.5882) | Max-over-time pooling: NLP 中的全局 Max Pooling | 做文本分类时 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 前置层 | 2 | [conv_layer](../conv_layer/conv_layer_map.md), [dense_layer](../dense_layer/dense_layer_map.md) | MaxPool 连接 Conv 和 Dense 的桥梁作用 |
| CNN 架构 | 1 | [cnn](../cnn/cnn_map.md) | MaxPool 在完整 CNN 中的位置和作用 |
| 后续架构 | 1 | [transformer](../transformer/transformer_map.md) | Attention 如何替代了池化的信息聚合功能 |
| 框架 | 2 | [pytorch](../pytorch/pytorch_map.md), [keras](../keras/keras_map.md) | MaxPool 的双平台 API 和实现差异 |
| 数学基础 | 1 | [tensor](../tensor/tensor_map.md) | 张量操作是 MaxPool 的底层实现基础 |
