---
topic: conv_layer
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: LeCun et al. 1998 — http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf"
  - "📖 Paper: Chollet, 'Xception: Deep Learning with Depthwise Separable Convolutions' 2017 — https://arxiv.org/abs/1610.02357"
  - "📖 Paper: Yu & Koltun, 'Multi-Scale Context Aggregation by Dilated Convolutions' 2016 — https://arxiv.org/abs/1511.07122"
  - "📖 Docs: PyTorch nn.Conv2d — https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html"
expiry: 12m
status: current
---

# Conv Layer (卷积层) 核心概念

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9
> 📖 Paper: LeCun et al., [Gradient-Based Learning](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf), 1998

---


## 术语定义

### 卷积 / 互相关 (Convolution / Cross-correlation)

卷积层的核心数学操作。严格来说，数学卷积要求翻转滤波器（$180°$ 旋转），但深度学习中实际执行的是**互相关**（不翻转）——因为滤波器权重是学出来的，翻不翻结果等价。每次计算：滤波器覆盖的局部区域与滤波器逐元素相乘再求和，产生输出特征图上的一个像素值。

> 易混淆：**数学卷积 vs DL "卷积"** — 数学卷积翻转核（$f * g = \int f(\tau)g(t-\tau)d\tau$）；DL 中不翻转，叫互相关但习惯上仍称"卷积"

### 滤波器 / 卷积核 (Filter / Kernel)

可学习的小权重张量，通常为 $K \times K \times C_{in}$（高 × 宽 × 输入通道数）。一个滤波器在整张输入特征图上滑动做局部加权求和，产生**一张特征图**。CNN 的"学习"本质就是学习滤波器中的权重值。

> 易混淆：**滤波器 vs 权重矩阵** — 全连接层的权重矩阵 $W \in \mathbb{R}^{n_{out} \times n_{in}}$ 是密集的；卷积核 $K \in \mathbb{R}^{k \times k \times C_{in}}$ 是稀疏+共享的

### 特征图 / 激活图 (Feature Map / Activation Map)

一个滤波器在输入上滑动后产生的 2D 输出矩阵。每个特征图记录了某一种特征（如边缘、纹理）在空间各位置的**激活强度**。$C_{out}$ 个滤波器产生 $C_{out}$ 张特征图，堆叠成输出张量的通道维度。

### 步长 (Stride)

滤波器每次滑动移动的像素数。$S=1$ 逐像素滑动（输出与输入几乎等大）；$S=2$ 每次跳 2 步（输出尺寸减半）。增大步长是一种**下采样**方式，替代池化层减少空间维度。

> 易混淆：**步长下采样 vs 池化下采样** — 步长卷积同时做特征提取+下采样（有可学习参数）；池化是无参数的固定操作（取 max/avg）

### 填充 (Padding)

在输入特征图边缘补值（通常补零）的操作。两种常用模式：
- **Valid (无填充)**：不补零，输出尺寸 = $(I - K) / S + 1$，每次卷积输出缩小
- **Same (等尺寸填充)**：补 $P = \lfloor K/2 \rfloor$ 圈零，使输出空间尺寸 = 输入空间尺寸（当 $S=1$）

### 通道 (Channel / Depth)

输入张量的第三个维度。RGB 图像有 3 个通道；卷积层的输出通道数 = 滤波器个数。核心要点：**每个滤波器的深度必须等于输入通道数** $C_{in}$，所以一个滤波器实际是 $K \times K \times C_{in}$ 的 3D 张量。

### 感受野 (Receptive Field)

输出特征图上一个像素"能看到"（影响它的值）的原始输入区域大小。单层 $3 \times 3$ 卷积的感受野是 $3 \times 3$；堆叠两层 $3 \times 3$ 的感受野 = $5 \times 5$。深层网络通过堆叠小卷积核获得大感受野，同时比直接用大卷积核参数更少。

> 易混淆：**卷积核大小 vs 感受野** — 卷积核大小是单层的局部视野；感受野是多层累积的等效视野，可远大于单个核

### 1×1 卷积 (Pointwise Convolution)

核大小为 $1 \times 1$ 的卷积。看似不做空间操作，实际在**通道维度**做线性组合——相当于对每个像素位置独立施加一个全连接层。主要用途：升降通道数（如 ResNet bottleneck）、跨通道特征融合。

### 深度可分离卷积 (Depthwise Separable Convolution)

将标准卷积拆分为两步：
1. **Depthwise**（逐通道卷积）：每个通道独立用一个 $K \times K$ 滤波器
2. **Pointwise**（1×1 卷积）：用 $1 \times 1$ 卷积混合通道

参数量从 $K^2 \cdot C_{in} \cdot C_{out}$ 降到 $K^2 \cdot C_{in} + C_{in} \cdot C_{out}$，约减少 $K^2$ 倍。MobileNet、Xception 的核心。

### 空洞卷积 / 膨胀卷积 (Dilated / Atrous Convolution)

在卷积核元素之间插入空洞（零），扩大感受野但不增加参数。膨胀率 $d$：实际核大小 = $K + (K-1)(d-1)$。$d=1$ 退化为标准卷积。常用于语义分割（DeepLab）和 WaveNet。

### 转置卷积 / 反卷积 (Transposed / Deconvolution)

上采样操作——将小特征图"放大"为大特征图。不是卷积的数学逆运算，而是通过在输入元素间插入零再做标准卷积来实现。常用于 GAN 的生成器、语义分割的解码器。

> 易混淆：**反卷积 vs 上采样+卷积** — "反卷积"名称有误导性（不是逆操作）；现代实践常用双线性上采样+标准卷积替代

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1–9.5
> 📖 Paper: Chollet, [Xception](https://arxiv.org/abs/1610.02357), 2017
> 📖 Paper: Yu & Koltun, [Dilated Convolutions](https://arxiv.org/abs/1511.07122), 2016

---


## 概念辨析

### 卷积层 vs 全连接层

| 维度 | 卷积层 (Conv) | 全连接层 (Dense/FC) |
|------|-------------|-------------------|
| **连接方式** | 局部连接（只看 $K \times K$ 区域） | 全连接（看所有输入） |
| **参数共享** | ✅ 同一滤波器在所有位置使用 | ❌ 每个连接独立参数 |
| **参数量** | $(K^2 \cdot C_{in} + 1) \times C_{out}$ | $(n_{in} + 1) \times n_{out}$ |
| **空间信息** | ✅ 保留空间结构 | ❌ 展平后丢失 |
| **平移等变性** | ✅ 猫在左上角和右下角产生相同特征 | ❌ 位置变化需要重新学习 |
| **典型参数量** | 3×3×64×128+128 = 73,856 | 784×128+128 = 100,480 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.2

### 标准卷积 vs 深度可分离卷积

| 维度 | 标准卷积 | 深度可分离卷积 |
|------|---------|--------------|
| **操作** | 一步完成空间+通道混合 | 分两步：空间 (DW) + 通道 (PW) |
| **参数量** | $K^2 \cdot C_{in} \cdot C_{out}$ | $K^2 \cdot C_{in} + C_{in} \cdot C_{out}$ |
| **计算量** | $K^2 \cdot C_{in} \cdot C_{out} \cdot H \cdot W$ | $(K^2 + C_{out}) \cdot C_{in} \cdot H \cdot W$ |
| **压缩比** | 基准 | 约 $1/K^2$（$K=3$ 时约 $1/9$） |
| **使用场景** | 参数不敏感的场景 | 移动端、边缘设备（MobileNet） |

> 📖 Paper: Chollet, [Xception](https://arxiv.org/abs/1610.02357), 2017

### Valid Padding vs Same Padding

| 维度 | Valid | Same |
|------|-------|------|
| **补零** | 不补零 | 补 $\lfloor K/2 \rfloor$ 圈零 |
| **输出尺寸** ($S=1$) | $I - K + 1$ | $I$（保持不变） |
| **边缘信息** | 边缘像素参与次数少 | 边缘被公平使用 |
| **PyTorch** | `padding=0`（默认） | `padding=K//2` 或 `padding='same'` |

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────────┐
│                    Conv Layer 内部结构                             │
├──────────────────────────────────────────────────────────────────┤
│  输入: X ∈ ℝ^{C_in × H × W}                                     │
│  └─ 3D 张量: 通道 × 高 × 宽                                      │
├──────────────────────────────────────────────────────────────────┤
│  滤波器组: W ∈ ℝ^{C_out × C_in × K × K}                         │
│  ├─ C_out 个滤波器，每个是 C_in × K × K 的 3D 张量               │
│  └─ 偏置: b ∈ ℝ^{C_out}                                         │
├──────────────────────────────────────────────────────────────────┤
│  操作: 对每个滤波器 f_i (i=1..C_out):                             │
│  ├─ 在 X 的空间维度上滑动（步长 S，填充 P）                       │
│  ├─ 每个位置: 逐元素乘法 + 求和 + 偏置                            │
│  └─ 产生一张 H_out × W_out 的特征图                              │
├──────────────────────────────────────────────────────────────────┤
│  输出: Y ∈ ℝ^{C_out × H_out × W_out}                            │
│  └─ H_out = ⌊(H + 2P - K) / S⌋ + 1                             │
└──────────────────────────────────────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

### 适用场景 ✅

- 图像分类、目标检测、语义分割
- 视频理解（3D 卷积 / 2+1D 卷积）
- 一维时序信号处理（1D 卷积用于音频、文本）
- 特征提取（作为更大架构的前端）
- 输入具有网格状拓扑结构（像素、频谱图等）

### 不适用场景 ❌

- 纯表格数据（无空间/时间结构，用 MLP 或树模型）
- 图结构数据（用图卷积 GCN）
- 全局依赖关系（卷积的感受野受限，长距离用 Transformer/Self-Attention）
- 可变大小非网格输入（点云等，用 PointNet）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 输入形状 (PyTorch) | `[B, C_in, H, W]` | `[32, 3, 224, 224]` |
| 输入形状 (TF/Keras) | `[B, H, W, C_in]` | `[32, 224, 224, 3]` |
| 输出尺寸 | $\lfloor(I - K + 2P) / S\rfloor + 1$ | $(224-3+2)/1+1 = 224$ |
| 参数量 | $(K \times K \times C_{in} + 1) \times C_{out}$ | $(3×3×3+1)×64 = 1{,}792$ |
| 常用核大小 | 3×3 (最常用), 1×1, 5×5, 7×7 | `Conv2d(3, 64, 3, padding=1)` |
| 常用步长 | 1 (保持尺寸), 2 (下采样) | `Conv2d(64, 128, 3, stride=2)` |
| 同尺寸填充 | $P = \lfloor K/2 \rfloor$ | $K=3 → P=1$; $K=5 → P=2$ |

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
