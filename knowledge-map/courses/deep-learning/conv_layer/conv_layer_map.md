---
topic: conv_layer
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5.5.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: LeCun et al., 'Gradient-Based Learning Applied to Document Recognition', Proc. IEEE 1998 — http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf"
  - "📖 Paper: He et al., 'Deep Residual Learning', CVPR 2016 — https://arxiv.org/abs/1512.03385"
  - "📖 Docs: PyTorch nn.Conv2d — https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html"
  - "📖 Docs: TensorFlow Conv2D — https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D"
expiry: 12m
status: current
---

# Conv Layer (卷积层) 知识地图

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9
> 📖 Paper: LeCun et al., [Gradient-Based Learning](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf), 1998

## 1. 核心问题

- **卷积层是什么？** → 用一组可学习的小滤波器在输入特征图上滑动做局部加权求和，输出新的特征图
- **卷积层解决什么问题？** → 利用局部连接 + 权值共享，大幅减少参数量，同时保留空间结构信息
- **输出尺寸怎么算？** → $O = \lfloor(I - K + 2P) / S\rfloor + 1$（输入 $I$，核 $K$，填充 $P$，步长 $S$）
- **参数量怎么算？** → $(K \times K \times C_{in} + 1) \times C_{out}$（含偏置）
- **有哪些变体？** → 标准卷积、1×1 卷积、深度可分离卷积、空洞卷积、转置卷积

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1–9.5

---

## 2. 全景位置

```
深度学习 (Deep Learning)
├── 基础组件层 (Primitive Layers) ← 你在这里
│   ├── 【Conv Layer (卷积层)】 (局部连接+权值共享，提取空间特征)
│   ├── Dense / FC Layer (全连接层，每个神经元连接所有输入)
│   ├── Pooling Layer (池化层，空间下采样)
│   ├── Normalization Layer (BN/LN/GN)
│   └── Activation Layer (ReLU/GELU/Sigmoid)
├── 复合架构 (Composite Architectures)
│   ├── CNN (堆叠 Conv+Pool+Dense)
│   ├── ResNet (Conv + 残差连接)
│   ├── U-Net (Conv + 编码器-解码器)
│   └── Transformer (Self-Attention + FFN)
└── 任务头 (Task Heads)
    ├── 分类头 (FC + Softmax)
    ├── 检测头 (Conv + Anchor)
    └── 分割头 (Conv + Upsample)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

---

## 3. 依赖地图

```
前置知识                          本主题                          后续方向
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│ 线性代数 (矩阵乘法)   │───→│                      │───→│ CNN 完整架构              │
│ 信号处理 (卷积定义)    │───→│                      │───→│ 池化层 (MaxPool/AvgPool)  │
│ MLP (全连接层)         │───→│   Conv Layer         │───→│ 1×1 卷积 / 通道混合       │
│ 感受野 (Receptive Field)│───→│   (卷积层)           │───→│ 深度可分离卷积             │
│ 梯度下降 / 反向传播    │───→│                      │───→│ 空洞/膨胀卷积              │
│                       │    │                      │───→│ 反卷积 / 转置卷积          │
└──────────────────────┘    └──────────────────────┘    └──────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [conv_layer_map.md](conv_layer_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [conv_layer_concepts.md](conv_layer_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [conv_layer_math.md](conv_layer_math.md) | ③ 公式 | 推导输出尺寸、参数量、反向传播 |
| [conv_layer_tutorial.md](conv_layer_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [conv_layer_code.md](conv_layer_code.md) | ⑤ 代码 | 快速上手 PyTorch/Keras 实现 |
| [conv_layer_pitfalls.md](conv_layer_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [conv_layer_history.md](conv_layer_history.md) | ⑦ 历史 | 了解从 Hubel-Wiesel 到现代卷积的演进 |
| [conv_layer_bridge.md](conv_layer_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [conv_layer_first_principles.md](conv_layer_first_principles.md) | ⑨ 第一性原理 | 从公理理解卷积层为什么必须这样设计 |

> 📖 本文件地图覆盖全部 9 个维度

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [conv_layer_map.md](conv_layer_map.md) 了解全局位置
2. 读 [conv_layer_tutorial.md](conv_layer_tutorial.md) Section 1 理解动机
3. 读 [conv_layer_concepts.md](conv_layer_concepts.md) 掌握核心术语
4. 读 [conv_layer_math.md](conv_layer_math.md) 手算一次输出尺寸 + 参数量
5. 跟 [conv_layer_code.md](conv_layer_code.md) 快速开始跑一个 Conv2d 示例
6. 读 [conv_layer_history.md](conv_layer_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [conv_layer_math.md](conv_layer_math.md) 输出尺寸公式和参数量公式
2. 查 [conv_layer_code.md](conv_layer_code.md) API 速查表
3. 查 [conv_layer_pitfalls.md](conv_layer_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [conv_layer_first_principles.md](conv_layer_first_principles.md) 理解卷积的公理基础
2. 读 [conv_layer_bridge.md](conv_layer_bridge.md) 探索变体（深度可分离、空洞卷积等）
3. 阅读 LeCun et al. 1998 原始论文

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
| Map | 2026-03-14 | 12m | ✅ current |
| Concepts | 2026-03-14 | 12m | ✅ current |
| Math | 2026-03-14 | 12m | ✅ current |
| Tutorial | 2026-03-14 | 12m | ✅ current |
| Code | 2026-03-14 | 6m | ✅ current |
| Pitfalls | 2026-03-14 | 6m | ✅ current |
| History | 2026-03-14 | never | ✅ current |
| Bridge | 2026-03-14 | 12m | ✅ current |
| First Principles | 2026-03-14 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.9](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考：卷积操作、池化、架构设计 |
| [《PRML》Ch.5.5.6](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | Math：权值共享、卷积的贝叶斯视角 |
| [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) | 📖 论文 | History：LeNet，卷积网络的经典论文 |
| [He et al. 2016](https://arxiv.org/abs/1512.03385) | 📖 论文 | Bridge：ResNet 中卷积层的使用 |
| [Chollet 2017, Xception](https://arxiv.org/abs/1610.02357) | 📖 论文 | Concepts：深度可分离卷积 |
| [Yu & Koltun 2016](https://arxiv.org/abs/1511.07122) | 📖 论文 | Concepts：空洞卷积 |
| [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) | 📖 文档 | Code：PyTorch 实现参考 |
| [TF Conv2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D) | 📖 文档 | Code：TensorFlow/Keras 实现参考 |
