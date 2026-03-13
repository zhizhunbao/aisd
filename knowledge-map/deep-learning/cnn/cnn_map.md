---
topic: cnn
dimension: map
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Part 1 Ch.8"
  - "📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)"
  - "📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)"
  - "📖 Docs: [PyTorch Training a Classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)"
expiry: 12m
status: current
---

# CNN (Convolutional Neural Network) 知识地图

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8
> 📖 Paper: LeCun et al., [Gradient-Based Learning Applied to Document Recognition (1998)](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)

## 1. 核心问题

- **CNN 是什么？** → 一种专门处理网格状拓扑数据（如图像）的前馈神经网络，通过卷积操作自动提取空间特征
- **为什么不用 MLP 处理图像？** → 图像像素量巨大（1600×1200×3 = 576万），MLP 全连接将产生数十亿参数，计算和存储不可行
- **CNN 的核心操作是什么？** → 卷积（Convolution）+ 池化（Pooling）+ 全连接（FC），通过权值共享和局部连接大幅减少参数
- **CNN 如何学习特征？** → 浅层学低级特征（边缘、纹理），深层学高级特征（形状、物体部件），端到端训练自动学习
- **现代 CNN 有哪些经典架构？** → LeNet-5 → AlexNet → VGGNet → GoogLeNet → ResNet → EfficientNet，不断变深变强

> 📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)
> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---

## 2. 全景位置

```
深度学习 (Deep Learning)
├── 基础组件
│   ├── 张量与自动微分 (Tensor & Autograd)
│   ├── 损失函数与优化器 (Loss & Optimizer)
│   └── 梯度消失/爆炸 (Vanishing Gradient)  ← 已有知识库
├── 网络架构
│   ├── 全连接网络 (MLP / Fully Connected)
│   ├── 【你在这里】卷积神经网络 (CNN)
│   │   ├── 图像分类 (Image Classification)
│   │   ├── 目标检测 (Object Detection)
│   │   └── 语义分割 (Semantic Segmentation)
│   ├── 循环神经网络 (RNN / LSTM)
│   └── Transformer
├── 训练技巧
│   ├── 数据增强 (Data Augmentation)
│   ├── 正则化 (Dropout, BatchNorm)
│   └── 迁移学习 (Transfer Learning)
└── 框架工具
    └── PyTorch  ← 已有知识库
```

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---

## 3. 依赖地图

```
前置知识                        本主题                          后续方向
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│ 线性代数(矩阵运算) │─────→│                  │─────→│ 目标检测 (YOLO/RCNN) │
│ 微积分(梯度/链式)  │─────→│   CNN            │─────→│ 语义分割 (U-Net)     │
│ MLP (全连接网络)  │─────→│   卷积神经网络    │─────→│ 迁移学习             │
│ 反向传播算法      │─────→│                  │─────→│ 生成模型 (GAN)       │
│ PyTorch 基础     │─────→│                  │─────→│ Vision Transformer   │
└─────────────────┘      └──────────────────┘      └──────────────────────┘
```

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [cnn_map.md](cnn_map.md) | ① 导航 | 第一次接触 CNN、需要全局视角 |
| [cnn_concepts.md](cnn_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [cnn_math.md](cnn_math.md) | ③ 公式 | 推导卷积输出尺寸、理解反向传播 |
| [cnn_tutorial.md](cnn_tutorial.md) | ④ 教程 | Why-First 理解 CNN 设计动机与原理 |
| [cnn_code.md](cnn_code.md) | ⑤ 代码 | 快速上手 PyTorch CNN 实现 |
| [cnn_pitfalls.md](cnn_pitfalls.md) | ⑥ 踩坑 | 调试 CNN 训练问题 |
| [cnn_history.md](cnn_history.md) | ⑦ 历史 | 了解 LeNet→AlexNet→ResNet 演进 |
| [cnn_bridge.md](cnn_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |

> 📖 Docs: 知识地图格式规范

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [cnn_map.md](cnn_map.md) 了解 CNN 在深度学习中的位置
2. 读 [cnn_tutorial.md](cnn_tutorial.md) Section 1 理解 CNN 的动机（为什么不用 MLP）
3. 读 [cnn_concepts.md](cnn_concepts.md) 掌握卷积、池化、步长等核心术语
4. 读 [cnn_math.md](cnn_math.md) 手算一次卷积输出尺寸
5. 跟 [cnn_code.md](cnn_code.md) 快速开始跑一个 CIFAR-10 分类
6. 读 [cnn_history.md](cnn_history.md) 了解 LeNet 到 ResNet 的演进

### 日常参考 🔧

1. 查 [cnn_code.md](cnn_code.md) API 速查表快速搭建网络
2. 查 [cnn_math.md](cnn_math.md) 公式速查计算输出尺寸
3. 查 [cnn_pitfalls.md](cnn_pitfalls.md) 排查训练问题

### 深度研究 🔬

1. 读 [cnn_history.md](cnn_history.md) 完整演进线
2. 读 [cnn_bridge.md](cnn_bridge.md) 探索目标检测、分割等下游任务
3. 阅读原始论文：LeCun 1998, Krizhevsky 2012, He 2015

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

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-12 | 12m | ✅ current |
| Concepts | 2026-03-12 | 12m | ✅ current |
| Math | 2026-03-12 | 12m | ✅ current |
| Tutorial | 2026-03-12 | 12m | ✅ current |
| Code | 2026-03-12 | 6m | ✅ current |
| Pitfalls | 2026-03-12 | 6m | ✅ current |
| History | 2026-03-12 | never | ✅ current |
| Bridge | 2026-03-12 | 12m | ✅ current |
