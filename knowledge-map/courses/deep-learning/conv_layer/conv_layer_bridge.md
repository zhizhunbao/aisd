---
topic: conv_layer
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: He et al. 2016 — https://arxiv.org/abs/1512.03385"
  - "📖 Paper: Vaswani et al. 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Paper: Liu et al., 'A ConvNet for the 2020s (ConvNeXt)', CVPR 2022 — https://arxiv.org/abs/2201.03545"
expiry: 12m
status: current
---

# Conv Layer (卷积层) 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | MLP (全连接层) | 卷积层是带约束的全连接层（局部连接+权值共享） | [mlp/](../mlp/) |
| ← 前置 | 线性代数（矩阵乘法） | 卷积可展开为 im2col 矩阵乘法 | — |
| ← 前置 | 信号处理（卷积/互相关） | DL 的"卷积"实际是互相关操作 | — |
| → 后续 | 池化层 (Pooling) | 常跟在 Conv 后做空间下采样 | — |
| → 后续 | BatchNorm | 常插在 Conv 和 ReLU 之间做归一化 | — |
| → 后续 | 残差连接 (ResNet) | 让深层卷积网络可训练 | — |
| → 后续 | U-Net (编码器-解码器) | Conv 下采样 + 转置 Conv 上采样 | — |
| → 后续 | Transformer (ViT) | 用 patch embedding 替代卷积提取特征 | — |
| → 后续 | ConvNeXt | 用 Transformer 设计理念改造纯卷积架构 | — |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| MLP (全连接层) | 线性变换 $\mathbf{Wx}+\mathbf{b}$、反向传播 | 卷积层是受限的线性变换（局部连接+共享权重） |
| 线性代数 | 矩阵乘法、Toeplitz 矩阵 | im2col 将卷积展开为矩阵乘法高效计算 |
| 信号处理 | 卷积定义 $f*g$ | 命名来源，但 DL 实际用互相关 |
| 微积分 | 链式法则 | 卷积层反向传播梯度计算 |
| 视觉神经科学 | 感受野、简单/复杂细胞 | 启发了局部连接和池化的设计 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| CNN 完整架构 | Conv + Pool + FC 的组合模式 | LeNet/VGG/ResNet 都是 Conv 层的不同堆叠方式 |
| 目标检测 (YOLO/Faster-RCNN) | 多尺度特征图 | 检测头在不同大小的 Conv 特征图上做预测 |
| 语义分割 (DeepLab/U-Net) | 空洞卷积 + 转置卷积 | 密集预测需要保持分辨率并上采样 |
| GAN 生成器 | 转置卷积 | 从噪声上采样生成图像 |
| Transformer (ViT) | Patch embedding = 大步长卷积 | ViT 用 Conv(16,16,stride=16) 将图像切成 patch |
| ConvNeXt | 深度可分离 + 大核 (7×7) | 用 Transformer 设计理念重新设计纯 Conv 架构 |
| 1D/3D 任务 | Conv1d / Conv3d | 音频、文本、视频的时序/空间特征提取 |

> 📖 Paper: [He et al. 2016](https://arxiv.org/abs/1512.03385)
> 📖 Paper: [Liu et al. 2022, ConvNeXt](https://arxiv.org/abs/2201.03545)

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化原因 |
|------|-------------|-------------|---------|
| 核大小 | 5×5, 7×7, 11×11 (LeNet, AlexNet) | 3×3 为主导 (VGGNet 至今) | 小核堆叠：相同感受野、更少参数、更多非线性 |
| 下采样方式 | MaxPool 2×2 为标准 | stride=2 的 Conv 替代 Pool | 可学习的下采样优于固定操作 |
| 通道调整 | 直接改变 Conv 的 out_channels | 1×1 卷积做通道升降 (Bottleneck) | 减少参数的同时灵活控制通道数 |
| 标准卷积 | 唯一选择 | 深度可分离卷积 (MobileNet) | 移动端需要：参数减 ~9× |
| 固定感受野 | Conv + Pool 逐步扩大 | 空洞卷积直接扩大 | 分割任务需要大感受野但不降分辨率 |
| 卷积 vs 注意力 | 卷积是唯一选择 | Conv + Self-Attention 混合 | Transformer 在长距离依赖上更强 |
| 归一化方式 | 无 → BatchNorm (2015) | GroupNorm / LayerNorm | BN 在小 batch 不稳定；GN/LN 更鲁棒 |

> 📖 Paper: [Liu et al. 2022, ConvNeXt](https://arxiv.org/abs/2201.03545)

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------|
| [Goodfellow Ch.9](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 卷积操作最完整的教科书级讲解 | ⭐⭐⭐ |
| [Dumoulin & Visin 2016](https://arxiv.org/abs/1603.07285) | 📖 论文 | 卷积算术指南，可视化每种卷积配置的效果 | ⭐⭐ |
| [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) | 📖 论文 | LeNet 原始论文，理解卷积网络的起源 | ⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Liu et al. 2022, ConvNeXt](https://arxiv.org/abs/2201.03545) | Conv vs Transformer | 理解卷积在 Transformer 时代的定位 |
| [Chollet 2017, Xception](https://arxiv.org/abs/1610.02357) | 标准卷积 vs 深度可分离 | 需要做轻量化时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [He et al. 2016](https://arxiv.org/abs/1512.03385) | ResNet 中卷积层的使用范式 | 设计深层 Conv 网络时 |
| [Vaswani et al. 2017](https://arxiv.org/abs/1706.03762) | Transformer 与 Conv 的关系 | 理解 patch embedding 等概念时 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf)

---

## 与工作区已有知识库的关联

| 类别 | 代表 | 学习点 |
|------|------|--------|
| 深度学习架构 | [CNN](../cnn/), [MLP](../mlp/) | Conv Layer 是 CNN 的核心组件；MLP 是 Conv 的无约束版本 |
| 基础组件 | [Tensor](../tensor/), [梯度消失](../vanishing_gradient/) | Conv 操作依赖 Tensor 运算；深层 Conv 面临梯度消失 |
| 框架 | [PyTorch](../pytorch/) | Conv Layer 的实现和使用 |
