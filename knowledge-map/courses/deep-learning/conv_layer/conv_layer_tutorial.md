---
topic: conv_layer
dimension: tutorial
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: LeCun et al. 1998 — http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf"
  - "📖 Paper: Simonyan & Zisserman, 'Very Deep Convolutional Networks (VGGNet)', ICLR 2015 — https://arxiv.org/abs/1409.1556"
  - "📖 Docs: PyTorch nn.Conv2d — https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html"
expiry: 12m
status: current
---

# Conv Layer (卷积层) 教程

> **前置知识：** MLP (全连接层) | 矩阵乘法 | 信号处理中卷积的基本概念
> **参考来源：** [《Deep Learning》Ch.9](../../../textbooks/goodfellow_deep_learning.pdf) | [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

---


## Section 0: 前置知识速查

1. **全连接层 (MLP)**：$\mathbf{y} = \sigma(\mathbf{Wx} + \mathbf{b})$，每个输出连接**所有**输入
2. **矩阵乘法**：全连接层的核心操作，参数量 = $n_{in} \times n_{out}$
3. **MLP 处理图像的问题**：224×224×3 图像展平为 150,528 维，一层 1024 神经元就有 1.5 亿参数
4. **信号处理中的卷积**：滤波器在信号上滑动做加权求和，提取特定频率/模式

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, Ch.9.1

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **全连接层参数爆炸**：224×224×3 图像用 MLP 处理，第一层就有 ~1.5 亿参数。训练慢、极易过拟合、不可部署到移动端。

- 🔥 **全连接层破坏空间结构**：MLP 首先将图像 flatten 为一维向量。像素 $(0,0)$ 和 $(223,223)$ 在向量中地位相同——空间邻域关系被完全丢弃。"猫的耳朵紧挨着猫的头"这种局部结构信息消失了。

- 🔥 **全连接层缺乏平移不变性**：猫在图像左上角和右下角，MLP 将其视为完全不同的输入模式。要学会"不管猫在哪都能识别"，MLP 需要在每个位置都看到足够的训练样本——数据量需求爆炸。

### 它的核心价值

1. **局部连接 (Sparse Connectivity)**：每个输出神经元只看输入的一小块区域（$K \times K$），而非全部输入。参数量从 $n_{in} \times n_{out}$ 降到 $K^2 \times C_{in} \times C_{out}$——减少几个数量级。

2. **权值共享 (Parameter Sharing)**：同一个滤波器在输入的**所有空间位置**使用相同的权重。学会检测"竖直边缘"后，无论竖直边缘出现在图像哪里，都能被同一个滤波器检测到。

3. **平移等变性 (Translation Equivariance)**：如果输入平移了 $(\Delta x, \Delta y)$，输出特征图也平移相同距离——猫在左上角和右下角产生的特征模式相同，只是位置不同。

4. **保留空间结构**：输出仍然是 2D 特征图，保留了"哪个特征在哪个位置"的信息，为后续的池化、检测、分割等操作提供基础。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.2–9.3

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 卷积操作流程图

```
┌───────────────────────────────────────────────────────────────────────┐
│                    2D 卷积操作流程                                      │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  输入: X ∈ ℝ^{C_in × H × W}                                          │
│       │                                                               │
│       ▼                                                               │
│  ┌─────────────────────────────────────┐                              │
│  │ 滤波器 f_m ∈ ℝ^{C_in × K × K}      │  × C_out 个                 │
│  │                                     │                              │
│  │  对每个空间位置 (i,j):               │                              │
│  │    1. 取出 X 中 K×K×C_in 的局部块   │                              │
│  │    2. 逐元素乘以 f_m 的权重          │                              │
│  │    3. 求和 + 偏置 b_m               │                              │
│  │    4. 结果写入 Y[m][i][j]           │                              │
│  └─────────────────────────────────────┘                              │
│       │                                                               │
│       ▼                                                               │
│  输出: Y ∈ ℝ^{C_out × H_out × W_out}                                 │
│                                                                       │
│  H_out = ⌊(H - K + 2P) / S⌋ + 1                                     │
└───────────────────────────────────────────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

### 2.2 为什么用小核堆叠而不是大核？

**为什么用两层 3×3 代替一层 5×5？**

| 方案 | 感受野 | 参数量 ($C$ 通道) | 非线性 |
|------|--------|------------------|--------|
| 一层 5×5 | 5×5 | $25C^2$ | 1 次 |
| 两层 3×3 | 5×5 | $2 \times 9C^2 = 18C^2$ | 2 次 |

两层 3×3 用 **72% 的参数**达到相同感受野，且多了一次非线性变换——表达能力更强。这就是 VGGNet 的核心发现。

> 📖 Paper: Simonyan & Zisserman, [VGGNet](https://arxiv.org/abs/1409.1556), 2015

### 2.3 卷积的多通道工作机制

```
输入 (3 通道 RGB)          滤波器 (1 个)               输出 (1 张特征图)

┌─────┐ ┌─────┐ ┌─────┐   ┌─────┐ ┌─────┐ ┌─────┐
│  R  │ │  G  │ │  B  │ × │ W_R │ │ W_G │ │ W_B │ → 逐通道卷积后求和
│ H×W │ │ H×W │ │ H×W │   │ K×K │ │ K×K │ │ K×K │
└─────┘ └─────┘ └─────┘   └─────┘ └─────┘ └─────┘
    │       │       │          │       │       │
    └───────┴───────┘          └───────┴───────┘
            │                          │
            ▼                          ▼
    X ∈ ℝ^{3×H×W}            W ∈ ℝ^{3×K×K}
                                       │
                                       ▼
                              Y ∈ ℝ^{1×H_out×W_out}
                              (3 个通道的结果求和 + 偏置)
```

一个滤波器的深度 **必须等于** 输入通道数 $C_{in}$。$C_{out}$ 个滤波器 → $C_{out}$ 张特征图。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

### 2.4 卷积层的反向传播

卷积的反向传播本质上也是卷积操作（或转置卷积）：
- 对权重的梯度：输入与上游梯度做互相关
- 对输入的梯度：上游梯度与翻转后的权重做完整卷积

这使得卷积层可以无缝融入标准的反向传播框架。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.5

---


## Section 3: 局限性

1. **感受野受限**：单层小核只能看到局部信息，捕捉全局依赖需要堆叠很多层 → **应对：空洞卷积增大感受野、Self-Attention 补充全局信息**

2. **平移等变但非旋转/缩放不变**：卷积对平移等变，但对旋转、缩放不具有内在不变性 → **应对：数据增强（旋转/翻转/缩放）、Spatial Transformer Network**

3. **固定核大小难适应多尺度**：$3 \times 3$ 核在所有位置使用相同大小，对不同尺度的物体效果不一 → **应对：多尺度特征金字塔 (FPN)、Inception 多分支并行**

4. **正方形假设**：标准卷积核是正方形，对非正方形结构（如细长文字）不友好 → **应对：可变形卷积 (Deformable Convolution)**

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.4

---


## Section 4: 方案对比

| 方案 | 参数量 | 感受野 | 适用场景 |
|------|--------|--------|---------|
| **全连接层 (FC)** | $n_{in} \times n_{out}$ 巨大 | 全局 | 表格数据 / 分类头 |
| **标准卷积 (Conv)** | $K^2 C_{in} C_{out}$ | 逐层累积 | 图像特征提取 |
| **深度可分离卷积** | $\approx 1/K^2$ 标准卷积 | 同标准卷积 | 移动端 / 轻量模型 |
| **空洞卷积** | 同标准卷积 | $K+(K-1)(d-1)$ 更大 | 密集预测 / 分割 |
| **Self-Attention** | $O(n^2)$ 或 $O(n)$ | 全局 | 长距离依赖 / NLP |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.9](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考 |
| [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) | 📖 论文 | Section 1：卷积网络的起源 |
| [Simonyan & Zisserman 2015](https://arxiv.org/abs/1409.1556) | 📖 论文 | Section 2.2：小核堆叠策略 |
| [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) | 📖 文档 | 实现参考 |
