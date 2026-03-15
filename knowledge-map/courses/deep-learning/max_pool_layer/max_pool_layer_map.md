---
topic: max_pool_layer
dimension: map
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5.5.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: LeCun et al., 'Gradient-Based Learning Applied to Document Recognition', Proc. IEEE 1998 — http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf"
  - "📖 Docs: PyTorch nn.MaxPool2d — https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html"
  - "📖 Docs: PyTorch nn.MaxPool1d — https://pytorch.org/docs/stable/generated/torch.nn.MaxPool1d.html"
  - "📖 Docs: TensorFlow MaxPooling2D — https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPooling2D"
expiry: 12m
status: current
---

# Max Pool Layer (最大池化层) 知识地图

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
> 📖 Paper: LeCun et al., [Gradient-Based Learning](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf), 1998

## 1. 核心问题

- **Max Pooling 是什么？** → 在输入特征图的每个局部窗口中取最大值，输出更小的特征图，实现空间下采样
- **它解决什么问题？** → 减少特征图尺寸/参数量，引入平移不变性，增大后续层的感受野
- **输出尺寸怎么算？** → $O = \lfloor(I - K + 2P) / S\rfloor + 1$（输入 $I$，核 $K$，填充 $P$，步长 $S$）
- **Max Pooling 有参数吗？** → 没有可学习参数（零参数层），只有超参数 kernel_size / stride / padding
- **和 Average Pooling 有什么区别？** → Max 取最大值（保留最强激活），Average 取平均值（保留整体分布信息）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## 2. 全景位置

```
深度学习 (Deep Learning)
├── 基础组件层 (Primitive Layers) ← 你在这里
│   ├── Conv Layer (卷积层，提取特征)
│   ├── Dense / FC Layer (全连接层)
│   ├── Pooling Layer (池化层，下采样)
│   │   ├── 【Max Pool Layer (最大池化)】 (取局部最大值，最常用)
│   │   ├── Average Pool Layer (取局部平均值)
│   │   ├── Global Average Pooling (全局取平均，替代 FC 层)
│   │   ├── Global Max Pooling (全局取最大值)
│   │   └── Adaptive Pooling (自适应输出尺寸)
│   ├── Normalization Layer (BN/LN/GN)
│   └── Activation Layer (ReLU/GELU/Sigmoid)
├── 复合架构 (Composite Architectures)
│   ├── LeNet-5 (Conv + AvgPool)
│   ├── AlexNet (Conv + MaxPool)
│   ├── VGGNet (Conv + MaxPool 标准范式)
│   ├── ResNet (Conv + MaxPool + Skip Connections)
│   └── Modern CNNs (Strided Conv 替代 MaxPool)
└── 任务头 (Task Heads)
    ├── 分类头 (FC + Softmax)
    ├── 检测头 (RoI Pooling)
    └── 分割头 (UnPooling / Upsample)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3–9.4

---

## 3. 依赖地图

```
前置知识                          本主题                          后续方向
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│ 卷积层 (Conv Layer)   │───→│                      │───→│ CNN 完整架构 (LeNet→ResNet)│
│ 特征图 (Feature Map)  │───→│                      │───→│ Global Average Pooling    │
│ 步长 (Stride) 概念    │───→│   Max Pool Layer     │───→│ Strided Conv 替代方案     │
│ 感受野 (Receptive Field)│───→│   (最大池化层)       │───→│ RoI Pooling (目标检测)    │
│ 平移不变性概念         │───→│                      │───→│ MaxUnpool (反池化)        │
│                       │    │                      │───→│ Adaptive Pooling          │
└──────────────────────┘    └──────────────────────┘    └──────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [max_pool_layer_map.md](max_pool_layer_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [max_pool_layer_concepts.md](max_pool_layer_concepts.md) | ② 概念 | 理解术语定义、辨析 Max vs Avg vs Global Pooling |
| [max_pool_layer_math.md](max_pool_layer_math.md) | ③ 公式 | 推导输出尺寸、梯度传播 |
| [max_pool_layer_tutorial.md](max_pool_layer_tutorial.md) | ④ 教程 | Why-First 理解为什么需要 Max Pooling |
| [max_pool_layer_code.md](max_pool_layer_code.md) | ⑤ 代码 | 快速上手 PyTorch/Keras 实现 |
| [max_pool_layer_pitfalls.md](max_pool_layer_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [max_pool_layer_history.md](max_pool_layer_history.md) | ⑦ 历史 | 了解从早期池化到现代替代方案的演进 |
| [max_pool_layer_bridge.md](max_pool_layer_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [max_pool_layer_first_principles.md](max_pool_layer_first_principles.md) | ⑨ 第一性原理 | 从公理理解 Max Pooling 为什么必须这样设计 |

> 📖 本文件地图覆盖全部 9 个维度

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [max_pool_layer_map.md](max_pool_layer_map.md) 了解全局位置
2. 读 [max_pool_layer_tutorial.md](max_pool_layer_tutorial.md) Section 1 理解动机
3. 读 [max_pool_layer_concepts.md](max_pool_layer_concepts.md) 掌握核心术语
4. 读 [max_pool_layer_math.md](max_pool_layer_math.md) 手算一次输出尺寸 + 梯度传播
5. 跟 [max_pool_layer_code.md](max_pool_layer_code.md) 快速开始跑一个 MaxPool2d 示例
6. 读 [max_pool_layer_history.md](max_pool_layer_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [max_pool_layer_math.md](max_pool_layer_math.md) 输出尺寸公式速查
2. 查 [max_pool_layer_code.md](max_pool_layer_code.md) API 速查表
3. 查 [max_pool_layer_pitfalls.md](max_pool_layer_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [max_pool_layer_first_principles.md](max_pool_layer_first_principles.md) 理解平移不变性的公理基础
2. 读 [max_pool_layer_bridge.md](max_pool_layer_bridge.md) 探索 Strided Conv / GAP 替代方案
3. 阅读 Goodfellow Ch.9.3–9.4 原文

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
| [《Deep Learning》Ch.9.3](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考：池化操作定义、平移不变性、先验解释 |
| [《PRML》Ch.5.5.6](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | Math：卷积网络中的权值共享与池化视角 |
| [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) | 📖 论文 | History：LeNet-5 中 subsampling 层（池化前身） |
| [Krizhevsky et al. 2012, AlexNet](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) | 📖 论文 | History：Max Pooling 在大规模视觉的标志性应用 |
| [Springenberg et al. 2015](https://arxiv.org/abs/1412.6806) | 📖 论文 | Bridge：Strided Conv 替代 Max Pooling 的研究 |
| [Lin et al. 2014, NiN](https://arxiv.org/abs/1312.4400) | 📖 论文 | Bridge：Global Average Pooling 替代 FC 层 |
| [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html) | 📖 文档 | Code：PyTorch 实现参考 |
| [TF MaxPooling2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPooling2D) | 📖 文档 | Code：TensorFlow/Keras 实现参考 |
