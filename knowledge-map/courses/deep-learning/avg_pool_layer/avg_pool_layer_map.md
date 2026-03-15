---
topic: avg_pool_layer
dimension: map
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Lin et al., 'Network in Network', ICLR 2014 — https://arxiv.org/abs/1312.4400"
  - "📖 Paper: LeCun et al., 'Gradient-Based Learning Applied to Document Recognition', Proc. IEEE 1998 — http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf"
  - "📖 Docs: PyTorch nn.AvgPool2d — https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html"
  - "📖 Docs: PyTorch nn.AdaptiveAvgPool2d — https://pytorch.org/docs/stable/generated/torch.nn.AdaptiveAvgPool2d.html"
  - "📖 Docs: TensorFlow AveragePooling2D — https://www.tensorflow.org/api_docs/python/tf/keras/layers/AveragePooling2D"
expiry: 12m
status: current
---

# Avg Pool Layer (平均池化层) 知识地图

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

## 1. 核心问题

- **Average Pooling 是什么？** → 在输入特征图的每个局部窗口中取平均值，输出更小的特征图，实现空间下采样
- **它解决什么问题？** → 减少特征图尺寸/计算量，保留窗口内所有激活的统计信息（而非仅保留最大值）
- **Global Average Pooling (GAP) 是什么？** → 对整个特征图取平均（每通道一个标量），替代全连接层，大幅减少参数量
- **和 Max Pooling 有什么区别？** → Average 保留整体分布信息（平滑），Max 只保留最强激活（尖锐）；Average 梯度均匀分布，Max 梯度仅流向 argmax 位置
- **输出尺寸怎么算？** → $O = \lfloor(I - K + 2P) / S\rfloor + 1$（与 Max Pooling 公式完全相同）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## 2. 全景位置

```
深度学习 (Deep Learning)
├── 基础组件层 (Primitive Layers) ← 你在这里
│   ├── Conv Layer (卷积层，提取特征)
│   ├── Dense / FC Layer (全连接层)
│   ├── Pooling Layer (池化层，下采样)
│   │   ├── Max Pool Layer (取局部最大值)
│   │   ├── 【Avg Pool Layer (平均池化)】 (取局部平均值，保留整体统计)
│   │   ├── Global Average Pooling (全局取平均，替代 FC 层)
│   │   ├── Global Max Pooling (全局取最大值)
│   │   └── Adaptive Pooling (自适应输出尺寸)
│   ├── Normalization Layer (BN/LN/GN)
│   └── Activation Layer (ReLU/GELU/Sigmoid)
├── 复合架构 (Composite Architectures)
│   ├── LeNet-5 (Conv + AvgPool 子采样)
│   ├── GoogLeNet/Inception (混合 AvgPool + MaxPool 分支)
│   ├── ResNet (末尾 Global Avg Pool)
│   └── EfficientNet (Squeeze-and-Excitation + GAP)
└── 任务头 (Task Heads)
    ├── 分类头 (GAP → FC → Softmax)
    ├── 特征提取 (GAP 生成固定维表示)
    └── 正则化 (GAP 替代 FC 减少过拟合)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## 3. 依赖地图

```
前置知识                          本主题                          后续方向
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│ 卷积层 (Conv Layer)   │───→│                      │───→│ Global Average Pooling    │
│ Max Pool Layer        │───→│                      │───→│ Inception 多分支架构      │
│ 特征图 (Feature Map)  │───→│   Avg Pool Layer     │───→│ 替代 FC 层 (NiN 设计)     │
│ 步长 (Stride) 概念    │───→│   (平均池化层)       │───→│ Squeeze-and-Excitation    │
│ 感受野 (Receptive Field)│───→│                     │───→│ Mean Pooling (NLP/BERT)   │
│                       │    │                      │───→│ 模型压缩/正则化           │
└──────────────────────┘    └──────────────────────┘    └──────────────────────────┘
```

> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [avg_pool_layer_map.md](avg_pool_layer_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [avg_pool_layer_concepts.md](avg_pool_layer_concepts.md) | ② 概念 | 理解术语定义、辨析 Avg vs Max vs GAP |
| [avg_pool_layer_math.md](avg_pool_layer_math.md) | ③ 公式 | 推导平均操作、输出尺寸、梯度传播 |
| [avg_pool_layer_tutorial.md](avg_pool_layer_tutorial.md) | ④ 教程 | Why-First 理解为什么需要 Average Pooling |
| [avg_pool_layer_code.md](avg_pool_layer_code.md) | ⑤ 代码 | 快速上手 PyTorch/Keras 实现 |
| [avg_pool_layer_pitfalls.md](avg_pool_layer_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [avg_pool_layer_history.md](avg_pool_layer_history.md) | ⑦ 历史 | 了解从 LeNet subsampling 到 GAP 的演进 |
| [avg_pool_layer_bridge.md](avg_pool_layer_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [avg_pool_layer_first_principles.md](avg_pool_layer_first_principles.md) | ⑨ 第一性原理 | 从公理理解 Average Pooling 为什么这样设计 |

> 📖 本文件地图覆盖全部 9 个维度

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [avg_pool_layer_map.md](avg_pool_layer_map.md) 了解全局位置
2. 读 [avg_pool_layer_tutorial.md](avg_pool_layer_tutorial.md) Section 1 理解动机
3. 读 [avg_pool_layer_concepts.md](avg_pool_layer_concepts.md) 掌握核心术语
4. 读 [avg_pool_layer_math.md](avg_pool_layer_math.md) 手算一次平均池化 + GAP
5. 跟 [avg_pool_layer_code.md](avg_pool_layer_code.md) 快速开始跑一个 AvgPool2d 示例
6. 读 [avg_pool_layer_history.md](avg_pool_layer_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [avg_pool_layer_math.md](avg_pool_layer_math.md) 输出尺寸公式速查
2. 查 [avg_pool_layer_code.md](avg_pool_layer_code.md) API 速查表
3. 查 [avg_pool_layer_pitfalls.md](avg_pool_layer_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [avg_pool_layer_first_principles.md](avg_pool_layer_first_principles.md) 理解均值聚合的公理基础
2. 读 [avg_pool_layer_bridge.md](avg_pool_layer_bridge.md) 探索 GAP 在现代架构中的角色
3. 阅读 Lin et al. 2014 Network in Network 原始论文

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-15 | 12m | ✅ current |
| Concepts | 2026-03-15 | 12m | ✅ current |
| Math | 2026-03-15 | 12m | ✅ current |
| Tutorial | 2026-03-15 | 12m | ✅ current |
| Code | 2026-03-15 | 6m | ✅ current |
| Pitfalls | 2026-03-15 | 6m | ✅ current |
| History | 2026-03-15 | never | ✅ current |
| Bridge | 2026-03-15 | 12m | ✅ current |
| First Principles | 2026-03-15 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.9.3](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考：池化定义、平移不变性、先验解释 |
| [Lin et al. 2014 (NiN)](https://arxiv.org/abs/1312.4400) | 📖 论文 | History/Tutorial：Global Average Pooling 替代 FC 层 |
| [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) | 📖 论文 | History：LeNet-5 subsampling 层（Average Pooling 前身） |
| [Szegedy et al. 2015 (GoogLeNet)](https://arxiv.org/abs/1409.4842) | 📖 论文 | Bridge：Inception 架构中 AvgPool 分支 |
| [He et al. 2016 (ResNet)](https://arxiv.org/abs/1512.03385) | 📖 论文 | Bridge：ResNet 末尾 GAP 替代 FC |
| [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html) | 📖 文档 | Code：PyTorch 实现参考 |
| [TF AveragePooling2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/AveragePooling2D) | 📖 文档 | Code：TensorFlow/Keras 实现参考 |
