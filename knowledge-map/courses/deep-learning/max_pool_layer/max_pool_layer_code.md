---
topic: max_pool_layer
dimension: code
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📖 Docs: PyTorch nn.MaxPool2d — https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html"
  - "📖 Docs: PyTorch nn.MaxPool1d — https://pytorch.org/docs/stable/generated/torch.nn.MaxPool1d.html"
  - "📖 Docs: TensorFlow MaxPooling2D — https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPooling2D"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Max Pool Layer 代码参考

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import torch
import torch.nn as nn

# ============================================================
# Max Pooling 最简示例 / Minimal Max Pooling Example
# ============================================================

# 创建输入: batch=1, channels=1, height=4, width=4
# Create input: batch=1, channels=1, height=4, width=4
x = torch.tensor([[[[1.0, 3.0, 2.0, 4.0],
                     [5.0, 6.0, 7.0, 8.0],
                     [9.0, 2.0, 1.0, 0.0],
                     [3.0, 4.0, 5.0, 6.0]]]])

# 2×2 最大池化, 步长=2 (默认等于 kernel_size)
# 2×2 max pooling, stride=2 (default equals kernel_size)
pool = nn.MaxPool2d(kernel_size=2)

# 前向传播 / Forward pass
output = pool(x)
print(f"输入形状 Input shape: {x.shape}")    # [1, 1, 4, 4]
print(f"输出形状 Output shape: {output.shape}")  # [1, 1, 2, 2]
print(f"输出 Output:\n{output}")
# tensor([[[[6., 8.],
#           [9., 6.]]]])
```

**测试方法：** 直接运行脚本，验证输出为 `[[6, 8], [9, 6]]`——每个 2×2 窗口的最大值。

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

---

## 完整实现示例

### 示例 1: 带 argmax 索引的 Max Pooling（手动实现 + API）

```python
import torch
import torch.nn as nn

# ============================================================
# 1. 手动实现 Max Pooling / Manual Implementation
# ============================================================

def manual_max_pool2d(x, kernel_size=2, stride=2):
    """
    手动实现 2D Max Pooling
    Manually implement 2D Max Pooling

    Args:
        x: 输入张量 (B, C, H, W) / Input tensor
        kernel_size: 池化窗口大小 / Pool window size
        stride: 步长 / Stride
    Returns:
        output: 池化输出 / Pooled output
        indices: argmax 位置索引 / Argmax position indices
    """
    B, C, H, W = x.shape
    H_out = (H - kernel_size) // stride + 1  # 输出高度 / Output height
    W_out = (W - kernel_size) // stride + 1  # 输出宽度 / Output width

    output = torch.zeros(B, C, H_out, W_out)   # 输出张量 / Output tensor
    indices = torch.zeros(B, C, H_out, W_out, dtype=torch.long)  # argmax 索引 / Argmax indices

    for m in range(H_out):
        for n in range(W_out):
            # 提取 kernel_size × kernel_size 窗口 / Extract window
            h_start = m * stride         # 窗口起始行 / Window start row
            w_start = n * stride         # 窗口起始列 / Window start col
            window = x[:, :, h_start:h_start+kernel_size,
                              w_start:w_start+kernel_size]

            # 展平窗口，取最大值和位置 / Flatten window, get max and position
            flat = window.reshape(B, C, -1)            # (B, C, K*K)
            output[:, :, m, n] = flat.max(dim=-1)[0]   # 最大值 / Max values
            indices[:, :, m, n] = flat.argmax(dim=-1)  # 位置 / Positions

    return output, indices


# ============================================================
# 2. PyTorch API 对比 / PyTorch API Comparison
# ============================================================

x = torch.randn(1, 3, 8, 8)  # batch=1, channels=3, 8×8

# 手动实现 / Manual implementation
manual_out, manual_idx = manual_max_pool2d(x, kernel_size=2, stride=2)

# PyTorch API (返回 argmax 索引) / PyTorch API (return argmax indices)
pool = nn.MaxPool2d(kernel_size=2, stride=2, return_indices=True)
api_out, api_idx = pool(x)

# 验证结果一致 / Verify results match
print(f"手动 vs API 最大差异: {(manual_out - api_out).abs().max().item():.6f}")
# 应输出 0.000000 / Should output 0.000000

# ============================================================
# 3. 使用 MaxUnpool 反池化 / MaxUnpool for Unpooling
# ============================================================

unpool = nn.MaxUnpool2d(kernel_size=2, stride=2)
reconstructed = unpool(api_out, api_idx, output_size=x.shape)
print(f"反池化形状: {reconstructed.shape}")  # [1, 3, 8, 8]
# 注意：非 argmax 位置为 0 / Note: non-argmax positions are 0
```

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)
> 📖 Docs: [PyTorch nn.MaxUnpool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxUnpool2d.html)

---

### 示例 2: 在 CNN 分类网络中使用 Max Pooling（VGG-style）

```python
import torch
import torch.nn as nn

# ============================================================
# 1. 模型定义 / Model Definition (VGG-style block)
# ============================================================

class SimpleVGGBlock(nn.Module):
    """
    VGG 风格的 Conv + MaxPool 块
    VGG-style Conv + MaxPool block
    """
    def __init__(self, in_channels, out_channels, num_convs=2):
        super().__init__()
        layers = []
        for i in range(num_convs):
            c_in = in_channels if i == 0 else out_channels
            layers.append(nn.Conv2d(c_in, out_channels, 3, padding=1))  # 3×3 卷积 / 3×3 conv
            layers.append(nn.BatchNorm2d(out_channels))                 # 批归一化 / Batch norm
            layers.append(nn.ReLU(inplace=True))                        # 激活函数 / Activation
        layers.append(nn.MaxPool2d(kernel_size=2, stride=2))             # 2×2 池化 / 2×2 pooling
        self.block = nn.Sequential(*layers)

    def forward(self, x):
        return self.block(x)


class SimpleCNN(nn.Module):
    """
    简单 CNN 分类器: 3 个 VGG Block + FC 头
    Simple CNN classifier: 3 VGG blocks + FC head
    """
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            SimpleVGGBlock(3, 64, num_convs=2),    # 32→16 (假设输入 32×32)
            SimpleVGGBlock(64, 128, num_convs=2),   # 16→8
            SimpleVGGBlock(128, 256, num_convs=2),  # 8→4
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),               # 全局平均池化 → 1×1
            nn.Flatten(),                           # 展平 / Flatten
            nn.Linear(256, num_classes),            # 分类头 / Classification head
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


# ============================================================
# 2. 测试推理 / Test Inference
# ============================================================

model = SimpleCNN(num_classes=10)
x = torch.randn(4, 3, 32, 32)  # batch=4, CIFAR-10 大小 / CIFAR-10 size

# 打印每层输出形状 / Print shape at each layer
print("输入:", x.shape)
for i, block in enumerate(model.features):
    x = block(x)
    print(f"Block {i}: {x.shape}")  # 32→16→8→4
x = model.classifier(x)
print(f"输出: {x.shape}")  # [4, 10]

# 参数统计 / Parameter count
total_params = sum(p.numel() for p in model.parameters())
print(f"总参数量: {total_params:,}")
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---

### 示例 3: Keras/TensorFlow Max Pooling

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ============================================================
# 1. Keras 简单示例 / Keras Simple Example
# ============================================================

model = keras.Sequential([
    layers.Input(shape=(32, 32, 3)),              # 输入形状 / Input shape
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(pool_size=2, strides=2),  # 32→16
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(pool_size=2, strides=2),  # 16→8
    layers.GlobalAveragePooling2D(),               # 8×8→1
    layers.Dense(10, activation='softmax'),        # 分类头 / Classification head
])

model.summary()

# ============================================================
# 2. 验证输出形状 / Verify Output Shape
# ============================================================

import numpy as np
x = np.random.randn(1, 32, 32, 3).astype('float32')
output = model.predict(x, verbose=0)
print(f"输出形状: {output.shape}")  # (1, 10)
```

> 📖 Docs: [TF MaxPooling2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPooling2D)

---

## API 速查

### PyTorch MaxPool

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.MaxPool1d(kernel_size)` | `kernel_size` | — | 1D 最大池化（序列/NLP） |
| ↳ | `stride` | kernel_size | 步长，默认等于 kernel_size |
| ↳ | `padding` | 0 | 填充（用 -∞） |
| ↳ | `dilation` | 1 | 膨胀系数 |
| ↳ | `return_indices` | False | 返回 argmax 索引（用于 MaxUnpool） |
| ↳ | `ceil_mode` | False | True 用 ceil 计算输出尺寸 |
| `nn.MaxPool2d(kernel_size)` | `kernel_size` | — | 2D 最大池化（图像） |
| ↳ | 参数同上 | — | — |
| `nn.MaxPool3d(kernel_size)` | `kernel_size` | — | 3D 最大池化（视频/体积） |
| `nn.AdaptiveMaxPool2d(output_size)` | `output_size` | — | 自适应输出尺寸 |
| `nn.MaxUnpool2d(kernel_size)` | `kernel_size` | — | 反池化（需要 indices） |

### Keras/TF MaxPooling

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `layers.MaxPooling1D(pool_size)` | `pool_size` | 2 | 1D 最大池化 |
| ↳ | `strides` | pool_size | 步长 |
| ↳ | `padding` | 'valid' | 'valid' 或 'same' |
| `layers.MaxPooling2D(pool_size)` | `pool_size` | (2,2) | 2D 最大池化 |
| ↳ | `strides` | pool_size | 步长 |
| ↳ | `padding` | 'valid' | 'valid' 或 'same' |
| `layers.GlobalMaxPooling2D()` | — | — | 全局最大池化 |

### 常用工具

| 函数 | 说明 |
|------|------|
| `torch.nn.functional.max_pool2d(input, kernel_size)` | 函数式 API，不需要实例化 |
| `torch.topk(input, k, dim)` | 取前 k 个最大值（K-Max Pooling） |
| `output.argmax(dim)` | 手动获取最大值索引 |

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)
> 📖 Docs: [TF MaxPooling2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPooling2D)

---

## 目录结构模板

### 简单结构

```
project/
├── model.py              ← 含 MaxPool 的 CNN 模型定义
├── train.py              ← 训练脚本
└── data/
    ├── train/
    └── val/
```

### 标准结构

```
project/
├── config.py             ← 超参数 (pool_size, stride 等)
├── models/
│   ├── vgg.py            ← VGG-style Conv+MaxPool 架构
│   └── resnet.py         ← ResNet (仅首层 MaxPool)
├── train.py
├── evaluate.py
├── data/
├── checkpoints/
└── logs/
```

### 高级结构

```
project/
├── configs/
│   └── pool_ablation.yaml  ← 池化方案消融实验配置
├── models/
│   ├── blocks.py           ← ConvBlock + MaxPool 模块
│   ├── backbone.py         ← 骨干网络
│   └── head.py             ← 分类/检测头
├── trainers/
├── utils/
├── train.py
├── evaluate.py
├── checkpoints/
├── logs/
└── requirements.txt
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9
