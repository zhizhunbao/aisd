---
topic: cnn
dimension: concepts
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.8"
  - "📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)"
  - "📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)"
expiry: 12m
status: current
---

# CNN 核心概念

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8
> 📖 Paper: LeCun et al., [Gradient-Based Learning Applied to Document Recognition (1998)](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)

---


## 术语定义

### 卷积 (Convolution)

卷积是 CNN 的核心操作：用一个小的滤波器（也叫卷积核）在输入图像上滑动，每到一个位置就计算滤波器和覆盖区域的逐元素乘积之和，产生一个输出值。整个滑动过程产生一张特征图（Feature Map）。卷积操作的关键优势是**权值共享**——同一个滤波器在所有位置使用相同的参数，大幅减少参数量。

> 易混淆：**互相关 (Cross-correlation)** — 数学上卷积需要翻转滤波器，但深度学习中的"卷积"实际执行的是互相关（不翻转），因为滤波器权重是学出来的，翻不翻都等价

### 滤波器 / 卷积核 (Filter / Kernel)

一个小的权重矩阵（通常 3×3 或 5×5），在输入上滑动执行卷积操作。每个滤波器学习检测一种特定的模式（如水平边缘、垂直边缘、纹理）。一个卷积层通常有多个滤波器，每个产生一张独立的特征图。

> 易混淆：**权重矩阵 (Weight Matrix)** — MLP 中的权重矩阵是全连接的大矩阵；CNN 滤波器是小的、局部连接的、在空间上共享的

### 特征图 (Feature Map)

一个滤波器在整张输入图上滑动后产生的输出矩阵。每个特征图对应一种被检测到的特征。多个滤波器产生多张特征图，堆叠成输出的"通道"维度。

> 易混淆：**通道 (Channel)** — 输入图像的通道是 RGB（3 通道），卷积层输出的通道就是特征图的个数

### 步长 (Stride)

滤波器每次滑动移动的像素数。stride=1 表示每次移动 1 像素，stride=2 表示每次跳 2 像素。增大步长会缩小输出尺寸，起到下采样的效果。

> 易混淆：**池化 (Pooling)** — 池化也能缩小尺寸，但用的是统计聚合（取最大值/平均值）而非跳步卷积

### 填充 (Padding)

在输入图像边缘补零（或其他值）的操作。目的是控制输出尺寸——如果不填充，每次卷积输出都会缩小；使用 "same" 填充可以保持输出与输入尺寸相同。填充还确保边缘像素被公平地参与计算。

> 易混淆：**Valid vs Same** — Valid 填充 = 不补零，输出变小；Same 填充 = 补零使输出与输入同尺寸

### 池化 (Pooling)

对特征图进行空间下采样的操作。最常见的是**最大池化 (Max Pooling)**：取窗口内的最大值；还有**平均池化 (Average Pooling)**：取窗口内的均值。池化减少参数、降低计算量，同时提供平移不变性。

> 易混淆：**全局平均池化 (Global Average Pooling, GAP)** — 对整张特征图取一个平均值，现代架构（如 ResNet）用 GAP 替代全连接层

### 全连接层 (Fully Connected Layer / Dense Layer)

CNN 末端将特征图展平 (Flatten) 后接的传统神经网络层，每个神经元与前一层所有神经元连接。用于将卷积层提取的特征映射到最终分类输出。

> 易混淆：**1×1 卷积 (1×1 Convolution)** — 看起来像全连接，但只在通道维度做线性组合，保留空间维度

### 激活函数 (Activation Function)

引入非线性变换的函数，接在每次卷积/全连接操作后。CNN 最常用 **ReLU**（Rectified Linear Unit）：f(x) = max(0, x)，计算简单且缓解梯度消失。输出层分类任务用 **Softmax**。

> 易混淆：**Sigmoid vs ReLU** — Sigmoid 将值压缩到 (0,1)，易导致梯度消失；ReLU 正区间梯度恒为 1，训练更快

### 批归一化 (Batch Normalization)

对每个 mini-batch 内的特征图做归一化（减均值除方差），然后学习缩放和平移参数。加速收敛、允许更大学习率、提供轻微正则化效果。

> 易混淆：**层归一化 (Layer Normalization)** — BatchNorm 在 batch 维度归一化，LayerNorm 在特征维度归一化（常用于 NLP/Transformer）

### 感受野 (Receptive Field)

输出特征图中的一个像素"对应"回输入图像的区域大小。网络越深，后层神经元的感受野越大，能"看到"更大范围的输入。这解释了为什么深层能学到高级特征。

> 易混淆：**卷积核大小 (Kernel Size)** — 卷积核大小是单层的局部视野，感受野是多层累积后的等效视野

### 迁移学习 (Transfer Learning)

将在大数据集（如 ImageNet）上预训练好的 CNN 模型迁移到新任务。通常冻结浅层（保留通用特征），只微调深层或分类头。小数据集场景下效果显著。

> 易混淆：**微调 (Fine-tuning) vs 特征提取 (Feature Extraction)** — 微调会更新部分预训练权重；特征提取完全冻结预训练网络只训练新分类头

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8
> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

---


## 概念辨析

### CNN vs MLP

| 维度 | CNN | MLP |
|------|-----|-----|
| **连接方式** | 局部连接 + 权值共享 | 全连接 |
| **参数量** | 少（滤波器参数 × 层数） | 巨大（输入维度 × 隐层宽度） |
| **空间关系** | 保留空间结构 | 忽略空间结构（展平输入） |
| **平移不变性** | 有（权值共享带来） | 无 |
| **典型应用** | 图像、视频、2D 信号 | 表格数据、简单分类 |

> 📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)

### Max Pooling vs Average Pooling

| 维度 | Max Pooling | Average Pooling |
|------|-------------|-----------------|
| **操作** | 取窗口最大值 | 取窗口平均值 |
| **保留信息** | 最强激活（边缘/纹理） | 整体统计信息 |
| **常见用途** | 中间层下采样 | 最后一层（GAP 接分类） |
| **梯度** | 只传回最大值位置 | 均匀分配到所有位置 |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

### Valid Padding vs Same Padding

| 维度 | Valid Padding | Same Padding |
|------|--------------|--------------|
| **补零** | 不补零 | 补零使输出=输入尺寸 |
| **输出尺寸** | (n - f + 1) | n（与输入相同） |
| **边缘信息** | 边缘像素参与次数少 | 边缘像素被公平使用 |
| **用途** | 想要缩小尺寸时 | 想要保持尺寸时 |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────┐
│  CNN 架构                                     │
├──────────────────────────────────────────────┤
│ 输入层 (Input)                                │
│  └─ 图像张量 [B, C, H, W]                    │
├──────────────────────────────────────────────┤
│ 特征提取器 (Feature Extractor)                │
│  ├─ Conv → BatchNorm → ReLU → Pool (×N)      │
│  └─ 浅层：边缘/纹理 → 深层：形状/语义        │
├──────────────────────────────────────────────┤
│ 分类器 (Classifier)                           │
│  ├─ Flatten / Global Avg Pool                 │
│  ├─ FC → ReLU → Dropout                      │
│  └─ FC → Softmax                              │
└──────────────────────────────────────────────┘
```

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

### 适用场景 ✅

- 图像分类（ImageNet, CIFAR-10）
- 目标检测（YOLO, Faster R-CNN）
- 语义分割（U-Net, DeepLab）
- 人脸识别
- 医学影像分析
- 视频理解（3D CNN / C3D）
- 一维信号处理（1D CNN 用于时序/文本）

### 不适用场景 ❌

- 纯表格数据（用 XGBoost / MLP 更合适）
- 超长序列建模（RNN/Transformer 更擅长）
- 图结构数据（需要 GNN）
- 极小数据集且无预训练模型（过拟合风险高）

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 输入格式 | [B, C, H, W] | [32, 3, 224, 224] |
| 典型卷积核 | 3×3 (最常用), 5×5, 1×1 | `nn.Conv2d(3, 64, 3, padding=1)` |
| 典型池化 | 2×2, stride=2 | `nn.MaxPool2d(2, 2)` |
| 参数计算 | (K×K×C_in + 1) × C_out | 3×3×3×64 + 64 = 1,792 |
| 输出尺寸 | ⌊(n+2p-f)/s + 1⌋ | (224+2×1-3)/1+1 = 224 |
| 经典深度 | 5(LeNet) → 16(VGG) → 152(ResNet) | 越深效果越好（有残差连接时） |

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
