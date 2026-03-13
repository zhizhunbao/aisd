---
topic: cnn
dimension: bridge
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.8"
  - "📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)"
  - "📖 Paper: [He et al. 2015 (ResNet)](https://arxiv.org/abs/1512.03385)"
expiry: 12m
status: current
---

# CNN 衔接与扩展

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---


## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | PyTorch 基础 | CNN 的实现框架 | [pytorch_map.md](../pytorch/pytorch_map.md) |
| ← 前置 | 梯度消失 | CNN 深层训练的核心挑战 | [vanishing_gradient_map.md](../vanishing_gradient/vanishing_gradient_map.md) |
| ← 前置 | MLP / 全连接网络 | CNN 是 MLP 的空间特化版 | — |
| → 后续 | 目标检测 (YOLO/R-CNN) | CNN 作为骨干网络提取特征 | — |
| → 后续 | 语义分割 (U-Net) | CNN 编码器-解码器结构 | — |
| → 后续 | 迁移学习 | 复用 CNN 预训练权重 | — |
| → 后续 | Vision Transformer (ViT) | 用注意力替代卷积 | — |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---


## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|----------|-----------|-------------------|
| 线性代数 | 矩阵乘法、转置 | 卷积操作本质是局部矩阵点积 |
| 微积分 | 梯度、链式法则 | 反向传播更新卷积核权重 |
| MLP | 全连接层、激活函数 | CNN 末端的分类器就是 MLP |
| 反向传播 | 误差反向传播算法 | CNN 的端到端训练核心算法 |
| PyTorch 基础 | Tensor, nn.Module, Autograd | CNN 的实现基础 |
| 梯度消失 | 梯度消失/爆炸问题 | CNN 用 ReLU、BatchNorm、残差连接解决 |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.5-8

---


## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|----------|-----------------|-----------------|
| 目标检测 | 特征提取器 (Backbone) | R-CNN/YOLO 用 CNN 提取图像特征 |
| 语义分割 | 编码器架构 | U-Net/DeepLab 用 CNN 做像素级分类 |
| 图像生成 (GAN) | 判别器/生成器 | DCGAN 用卷积/转置卷积生成图像 |
| 迁移学习 | 预训练特征 | 冻结 CNN 浅层，微调深层适应新任务 |
| Vision Transformer | CNN 的局限性分析 | ViT 试图用全局注意力解决 CNN 的局部性限制 |
| 3D 视觉 | 2D 卷积推广 | C3D/I3D 用 3D 卷积处理视频 |
| 1D 信号处理 | 卷积操作推广 | 1D CNN 用于时间序列、文本分类 |

> 📖 Paper: [He et al. 2015 (ResNet)](https://arxiv.org/abs/1512.03385)

---


## 概念演变追踪

| 概念 | 在早期 CNN 中 | 在现代 CNN 中 | 变化 |
|------|-------------|-------------|------|
| 激活函数 | Sigmoid / Tanh | ReLU / GELU / Swish | 解决梯度消失 + 训练更快 |
| 池化 | Average Pooling | Max Pooling → Global Avg Pool | 保留更强激活 → 替代全连接 |
| 归一化 | 无 / LRN | BatchNorm → GroupNorm | 加速收敛 + 正则化 |
| 网络深度 | 5-8 层 (LeNet/AlexNet) | 50-152+ 层 (ResNet) | 残差连接解决退化问题 |
| 卷积核大小 | 5×5, 7×7, 11×11 | 3×3 为主 + 1×1 辅助 | 小核多层 > 大核少层 |
| 分类器 | FC-4096-4096-1000 | GAP-1000 | 参数从数千万降到数千 |
| 训练方式 | 从零训练 | 预训练 + 微调 | 迁移学习成为标准流程 |

> 📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)
> 📖 Paper: [He et al. 2015 (ResNet)](https://arxiv.org/abs/1512.03385)

---


## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------|
| [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) | 📖 论文 | CNN 开山之作，理解设计动机 | ⭐⭐⭐ |
| [Krizhevsky et al. 2012](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) | 📖 论文 | 理解 GPU 训练 + 现代 CNN 设计 | ⭐⭐⭐ |
| [He et al. 2015](https://arxiv.org/abs/1512.03385) | 📖 论文 | 残差连接——深度学习最重要的创新之一 | ⭐⭐⭐⭐ |
| [Stanford CS231n](http://cs231n.stanford.edu/) | 📖 课程 | 最好的 CNN 入门课程 | ⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [ViT 论文](https://arxiv.org/abs/2010.11929) | CNN vs Transformer 在视觉任务的对比 | 了解 CNN 后想看替代方案时 |
| [EfficientNet 论文](https://arxiv.org/abs/1905.11946) | 网络宽度/深度/分辨率的最优缩放 | 需要高效 CNN 设计时 |
| [MobileNet 论文](https://arxiv.org/abs/1704.04861) | 深度可分离卷积——移动端 CNN | 需要轻量化模型时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [YOLO 系列论文](https://arxiv.org/abs/1506.02640) | CNN 在目标检测中的应用 | 学完 CNN 想做检测时 |
| [U-Net 论文](https://arxiv.org/abs/1505.04597) | CNN 在语义分割中的应用 | 需要像素级分类时 |
| [DCGAN 论文](https://arxiv.org/abs/1511.06434) | CNN 在图像生成中的应用 | 想做生成模型时 |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---


## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 框架工具 | 1 | [PyTorch 知识库](../pytorch/pytorch_map.md) | CNN 的实现依赖 PyTorch API |
| 训练问题 | 1 | [梯度消失知识库](../vanishing_gradient/vanishing_gradient_map.md) | CNN 深层训练的核心挑战 |
