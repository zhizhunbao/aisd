---
topic: avg_pool_layer
dimension: concepts
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Lin et al., 'Network in Network', ICLR 2014 — https://arxiv.org/abs/1312.4400"
  - "📖 Docs: PyTorch nn.AvgPool2d — https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html"
expiry: 12m
status: current
---

# Avg Pool Layer 核心概念

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

---


## 术语定义

### 平均池化 (Average Pooling)

在特征图的每个局部矩形窗口内取所有值的算术平均作为输出。与 Max Pooling 一样不含可学习参数，是一种纯粹的下采样操作。核心特点是保留窗口内所有激活的整体统计信息，输出更"平滑"——不像 Max Pooling 那样只保留最强信号。

> 易混淆：**Average Pooling vs Max Pooling** — Average 保留整体强度分布（平滑），Max 只保留最强特征（尖锐）。Average 梯度均匀分给窗口所有位置，Max 梯度仅传给 argmax 位置。

### 全局平均池化 (Global Average Pooling, GAP)

将整个特征图压缩为每通道一个标量——对 H×W 的空间维度取全局平均。Lin et al. (2014) 提出用 GAP 直接替代全连接层，使输出通道数等于类别数，大幅减少参数量。GAP 已成为现代 CNN（ResNet、EfficientNet、MobileNet）的标准分类头设计。

> 易混淆：**Global Average Pooling vs Flatten + FC** — GAP 将每个通道压成 1 个数（0 参数），Flatten + FC 把所有空间位置展平后接大权重矩阵（百万级参数）。GAP 不易过拟合且不受输入尺寸限制。

### 局部平均池化 (Local Average Pooling)

使用固定大小的窗口（如 2×2）在特征图上滑动，每个窗口输出该窗口内的平均值。这是与 Global Average Pooling 相对的概念——窗口不覆盖整个特征图，而是一个局部区域。

### 核大小 (Kernel Size / Pool Size)

池化窗口的空间尺寸。局部 AvgPool 常用 2×2 或 3×3。对于 GAP，kernel_size = 整个特征图的 H×W（或使用 AdaptiveAvgPool2d(1)）。

### count_include_pad 参数

控制边缘填充的零是否参与平均值计算。`count_include_pad=True`（默认）时，填充的零也计入分母 → 边缘区域平均值被拉低；`count_include_pad=False` 时，分母只算有效像素 → 更准确但边缘处理不同。

> 易混淆：**count_include_pad=True vs False** — Max Pooling 用 -∞ 填充（不影响 max），Average Pooling 用 0 填充，若计入分母就会拉低边缘均值，这是 AvgPool 特有的边缘效应。

### 自适应平均池化 (Adaptive Average Pooling)

指定输出尺寸（而非 kernel_size），由框架自动计算所需的 kernel_size 和 stride。`AdaptiveAvgPool2d(1)` 等价于全局平均池化，额外好处是不依赖输入尺寸，适配任意分辨率。

### 子采样 (Subsampling)

LeNet-5 中的历史名称，是 Average Pooling 的前身。它在 2×2 窗口内取平均后乘以一个可学习标量并加偏置——比纯 Average Pooling 多了两个参数。现代框架中已不使用这种设计。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)

---


## 概念辨析

### Average Pooling vs Max Pooling

| 维度 | Average Pooling | Max Pooling |
|------|-----------------|-------------|
| **操作** | 取窗口中平均值 | 取窗口中最大值 |
| **保留信息** | 整体统计（特征强度分布） | 最强激活（特征是否存在） |
| **梯度传播** | 均匀分给窗口内所有位置 | 仅传给最大值位置（稀疏） |
| **对噪声** | 平滑噪声，更鲁棒 | 可能放大噪声极值 |
| **对弱特征** | 保留弱特征信号 | 丢弃弱特征 |
| **平移不变性** | 较弱 | 较强 |
| **典型应用** | Inception 分支、LeNet、GAP | VGG、AlexNet、ResNet 中间层 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

### Global Average Pooling vs Flatten + FC

| 维度 | GAP | Flatten + FC |
|------|-----|-------------|
| **参数量** | 0（无可学习参数） | 巨大（如 512×7×7×4096 = 1 亿+） |
| **过拟合风险** | 低 | 高（需 Dropout） |
| **输入尺寸依赖** | 不依赖（任意 H×W） | 依赖（必须固定 H×W） |
| **可解释性** | 高（通道 = 类别概率） | 低（黑盒权重矩阵） |
| **表达能力** | 较低（仅均值统计） | 较高（全连接映射） |

> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────┐
│                   Avg Pool Layer 信息流                       │
├──────────────────────────────────────────────────────────────┤
│  输入特征图 (H_in × W_in × C)                                │
│  │                                                           │
│  ▼  局部 AvgPool:                                             │
│  ┌─────────────────────────────────────┐                     │
│  │ 滑动窗口 (K × K), stride=S          │                     │
│  │ 每个窗口: sum(所有值) / (K × K)      │                     │
│  │ → 输出 (H_out × W_out × C)          │                     │
│  └─────────────────────────────────────┘                     │
│                                                               │
│  ▼  Global Avg Pool (GAP):                                    │
│  ┌─────────────────────────────────────┐                     │
│  │ 窗口 = 整个特征图 (H × W)            │                     │
│  │ 每通道: sum(H×W 个值) / (H × W)      │                     │
│  │ → 输出 (1 × 1 × C) = C 个标量       │                     │
│  └─────────────────────────────────────┘                     │
├──────────────────────────────────────────────────────────────┤
│  关键特性：                                                   │
│  • 无可学习参数 (零参数层)                                     │
│  • 通道独立操作 (每个通道单独池化)                              │
│  • 反向传播：梯度均匀分配给窗口内所有位置                       │
│  • 边缘效应：count_include_pad 影响边缘均值                    │
└──────────────────────────────────────────────────────────────┘
```

> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)

### 适用场景 ✅

- Global Average Pooling 替代 FC 层（减少参数量和过拟合，NiN/GoogLeNet/ResNet）
- Inception 架构中的并行 AvgPool 分支（与 MaxPool 分支互补）
- 需要平滑输出的任务（特征强度估计而非特征检测）
- 梯度流要求均匀的场景（避免 Max Pooling 的梯度稀疏性）
- 变尺寸输入的分类任务（AdaptiveAvgPool2d(1) 万能适配）

### 不适用场景 ❌

- 需要强平移不变性——Max Pooling 效果更好
- 特征高度稀疏（大部分为零）——Average 被零值拉低，Max 更好
- 需要保留空间位置信息——任何池化都不合适
- LeNet 风格的中间层下采样——现代架构已改用 Strided Conv

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 类型 | 无参数下采样层 | `nn.AvgPool2d(2)` |
| 可学习参数 | 0 | — |
| 超参数 | kernel_size, stride, padding, ceil_mode, count_include_pad | — |
| 默认 stride | 等于 kernel_size | `AvgPool2d(2)` → stride=2 |
| 默认 padding | 0 | — |
| 填充值 | 0（可能影响均值！） | 与 MaxPool 的 -∞ 不同 |
| 输出通道数 | 等于输入通道数 | C_out = C_in |
| 梯度行为 | 均匀分配给窗口内所有位置 | $\partial y / \partial x_i = 1/(K^2)$ |
| Global Avg Pool | `nn.AdaptiveAvgPool2d(1)` | 每通道→1个标量 |
| 主要用途 | GAP 替代 FC 层；Inception 分支 | ResNet 末尾 |

> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)
