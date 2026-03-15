---
topic: max_pool_layer
dimension: concepts
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: PyTorch nn.MaxPool2d — https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html"
  - "📖 Paper: Springenberg et al., 'Striving for Simplicity', ICLR 2015 — https://arxiv.org/abs/1412.6806"
expiry: 12m
status: current
---

# Max Pool Layer 核心概念

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

---


## 术语定义

### 最大池化 (Max Pooling)

在特征图的每个局部矩形窗口内取最大值作为输出。这是一种下采样操作，不包含任何可学习参数。它的核心作用是：(1) 减少特征图的空间尺寸；(2) 提供近似的平移不变性——如果输入发生微小位移，最大值大概率不变；(3) 保留最强的激活信号（"有没有这个特征"比"特征在哪"更重要）。

> 易混淆：**Max Pooling vs Average Pooling** — Max 保留最强激活（检测特征是否存在），Average 保留整体统计信息（特征的平均强度）。Max 在分类任务中更常用，Average 更适合保留背景信息。

### 池化窗口 / 核大小 (Kernel Size / Pool Size)

池化操作的滑动窗口大小。常见设置为 2×2 或 3×3。窗口越大下采样越激进，但丢失的空间细节也越多。在 PyTorch 中用 `kernel_size` 参数指定。

> 易混淆：**池化的 kernel_size vs 卷积的 kernel_size** — 池化的 kernel 没有可学习权重，只是定义计算 max 的区域大小；卷积的 kernel 包含可学习的权重参数。

### 步长 (Stride)

池化窗口每次移动的像素数。默认值等于 kernel_size（即不重叠池化）。当 stride=2, kernel_size=2 时，输出尺寸恰好为输入的一半。在 PyTorch 中，如果不显式设置 stride，默认等于 kernel_size。

### 填充 (Padding)

在输入边缘补充值，使得边缘像素也能被窗口完整覆盖。Max Pooling 用 $-\infty$ 填充（保证填充值不会被选为最大值）。默认 padding=0。

### 空洞/膨胀 (Dilation)

控制池化窗口内元素之间的间距。dilation=1 表示相邻元素（标准池化），dilation=2 表示每隔一个元素取值。增大 dilation 可以在不增加参数的情况下扩大感受野。

### 平移不变性 (Translation Invariance)

输入发生微小空间位移时，池化输出基本不变的性质。这是 Max Pooling 最核心的归纳偏置：我们关心"某个特征是否存在"，而不关心它精确的位置。

> 易混淆：**平移不变性 vs 平移等变性 (Equivariance)** — 卷积层是等变的（输入平移 → 输出也平移），池化层是不变的（输入平移 → 输出不变）。不变性是更强的性质，但会丢失精确位置信息。

### 感受野 (Receptive Field)

一个输出神经元能"看到"的输入区域大小。Max Pooling 通过下采样间接增大后续卷积层的有效感受野——池化后同样大小的卷积核能覆盖原始输入的更大区域。

### 全局最大池化 (Global Max Pooling)

将整个特征图压缩为单个值（每个通道一个标量），相当于 kernel_size 等于整个特征图尺寸。常用于 NLP 中的 max-over-time pooling 和计算机视觉中替代 Flatten + FC。

> 易混淆：**Global Max Pooling vs Global Average Pooling** — Global Max 取全局最大值（最强特征），Global Average 取全局均值（整体特征），Lin et al. 2014 (NiN) 证明 GAP 可以替代 FC 层减少过拟合。

### 下采样 (Downsampling)

减少特征图空间分辨率的操作。Max Pooling 是最经典的下采样方式；替代方案包括 Strided Convolution（步长卷积）和 Average Pooling。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

---


## 概念辨析

### Max Pooling vs Average Pooling

| 维度 | Max Pooling | Average Pooling |
|------|-------------|-----------------|
| **操作** | 取窗口中最大值 | 取窗口中平均值 |
| **保留信息** | 最强激活（是否存在特征） | 整体统计（特征的平均强度） |
| **梯度传播** | 仅传给最大值位置（稀疏） | 均匀分配给窗口内所有位置 |
| **典型应用** | VGG/ResNet 分类网络 | LeNet-5 / Inception 分支 |
| **对噪声的鲁棒性** | 可能放大噪声极值 | 平滑噪声，但模糊特征 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

### Max Pooling vs Strided Convolution

| 维度 | Max Pooling | Strided Convolution |
|------|-------------|---------------------|
| **可学习参数** | 无（零参数） | 有（卷积核权重） |
| **下采样方式** | 固定的 max 操作 | 学习的加权组合 |
| **计算成本** | 更低 | 更高（需要梯度更新） |
| **灵活性** | 操作固定 | 网络自动学习如何下采样 |
| **研究趋势** | 经典方案 | 现代架构倾向使用 (Springenberg et al. 2015) |

> 📖 Paper: Springenberg et al., [Striving for Simplicity](https://arxiv.org/abs/1412.6806), ICLR 2015

### 局部 Max Pooling vs Global Max Pooling

| 维度 | 局部 Max Pooling | Global Max Pooling |
|------|-----------------|---------------------|
| **窗口大小** | 固定小窗口（如 2×2） | 整个特征图 |
| **输出形状** | 缩小的特征图 | 每通道一个标量 |
| **位置** | 网络中间层（Conv 之后） | 网络最后一层（分类头之前） |
| **作用** | 逐步下采样 | 生成全局fixed-size表示 |

> 📖 Docs: [PyTorch nn.AdaptiveMaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AdaptiveMaxPool2d.html)

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────┐
│                    Max Pool Layer 信息流                      │
├──────────────────────────────────────────────────────────────┤
│  输入特征图 (H_in × W_in × C)                                │
│  │                                                           │
│  ▼                                                           │
│  ┌─────────────────────────────────────┐                     │
│  │ 滑动窗口 (kernel_size × kernel_size) │                     │
│  │ 步长 stride, 填充 padding            │                     │
│  │ 每个窗口内取 max → 一个输出值        │                     │
│  └─────────────────────────────────────┘                     │
│  │                                                           │
│  ▼                                                           │
│  输出特征图 (H_out × W_out × C)                               │
│  ※ 通道数 C 不变，空间尺寸缩小                                │
│  ※ 同时记录 argmax 位置索引 (可选)                             │
├──────────────────────────────────────────────────────────────┤
│  关键特性：                                                   │
│  • 无可学习参数 (零参数层)                                     │
│  • 通道独立操作 (每个通道单独池化)                              │
│  • 反向传播：梯度只流向 argmax 位置                            │
└──────────────────────────────────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

### 适用场景 ✅

- 分类任务中需要平移不变性（图像分类、目标识别）
- 特征图尺寸过大需要下采样以减少计算量
- 需要保留最强激活信号（"有没有这个特征"比精确位置重要）
- 经典 CNN 架构中 Conv Block 之后的标准操作（VGG、AlexNet、ResNet）
- NLP 中的 max-over-time pooling（每个卷积 filter 取全局最大值）

### 不适用场景 ❌

- 密集预测任务（语义分割、超分辨率）——需要精确位置信息，Max Pooling 会丢失
- 需要可学习下采样——使用 Strided Convolution 替代
- 输入中极值噪声严重——Average Pooling 更鲁棒
- 现代 Transformer 架构——通常使用 Patch Embedding 而非池化
- 需要可逆操作的生成模型——Max Pooling 不可精确反转（需 MaxUnpool + argmax 索引）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3–9.4

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 类型 | 无参数下采样层 | `nn.MaxPool2d(2)` |
| 可学习参数 | 0 | — |
| 超参数 | kernel_size, stride, padding, dilation, ceil_mode, return_indices | — |
| 默认 stride | 等于 kernel_size | `MaxPool2d(2)` → stride=2 |
| 默认 padding | 0 | — |
| 填充值 | $-\infty$ | 保证不被选为 max |
| 输出通道数 | 等于输入通道数 | C_out = C_in |
| 梯度行为 | 仅传给 argmax 位置 | 其余位置梯度 = 0 |
| 常用配置 | kernel=2, stride=2 | 输出尺寸减半 |
| 替代方案 | Strided Conv, AvgPool, GAP | — |

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)
