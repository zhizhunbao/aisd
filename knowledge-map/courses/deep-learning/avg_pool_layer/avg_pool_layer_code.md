---
topic: avg_pool_layer
dimension: code
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📖 Docs: PyTorch nn.AvgPool2d — https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html"
  - "📖 Docs: PyTorch nn.AdaptiveAvgPool2d — https://pytorch.org/docs/stable/generated/torch.nn.AdaptiveAvgPool2d.html"
  - "📖 Docs: TensorFlow AveragePooling2D — https://www.tensorflow.org/api_docs/python/tf/keras/layers/AveragePooling2D"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Avg Pool Layer 代码参考

> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import torch
import torch.nn as nn

# ============================================================
# Average Pooling 最简示例 / Minimal Average Pooling Example
# ============================================================

# 创建输入: batch=1, channels=1, height=4, width=4
# Create input: batch=1, channels=1, height=4, width=4
x = torch.tensor([[[[1.0, 3.0, 2.0, 4.0],
                     [5.0, 6.0, 7.0, 8.0],
                     [9.0, 2.0, 1.0, 0.0],
                     [3.0, 4.0, 5.0, 6.0]]]])

# 2×2 平均池化, stride=2 / 2×2 average pooling, stride=2
pool = nn.AvgPool2d(kernel_size=2)

output = pool(x)
print(f"输入形状 Input shape: {x.shape}")      # [1, 1, 4, 4]
print(f"输出形状 Output shape: {output.shape}")  # [1, 1, 2, 2]
print(f"输出 Output:\n{output}")
# tensor([[[[3.7500, 5.2500],
#           [4.5000, 3.0000]]]])

# ============================================================
# Global Average Pooling / 全局平均池化
# ============================================================

gap = nn.AdaptiveAvgPool2d(1)  # 输出 1×1
gap_output = gap(x)
print(f"GAP 输出: {gap_output.item():.4f}")  # (1+3+2+4+5+6+7+8+9+2+1+0+3+4+5+6)/16 = 4.125
```

**测试方法：** 直接运行，验证局部平均 `[[3.75, 5.25], [4.50, 3.00]]` 和 GAP `4.125`。

> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)

---

## 完整实现示例

### 示例 1: GAP 替代 FC 层的分类网络

```python
import torch
import torch.nn as nn

# ============================================================
# 1. 使用 GAP 的现代 CNN 分类器 / Modern CNN with GAP
# ============================================================

class GAPClassifier(nn.Module):
    """
    使用 Global Average Pooling 替代 FC 层的分类器
    Classifier using GAP instead of FC layers
    """
    def __init__(self, num_classes=10):
        super().__init__()
        # 特征提取器 / Feature extractor
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),   # 32×32→32×32
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, 3, padding=1, stride=2),  # 32→16 (strided conv)
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, 3, padding=1, stride=2), # 16→8
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, num_classes, 1),   # 1×1 conv: 128→num_classes
        )
        # GAP 替代 Flatten + FC / GAP replaces Flatten + FC
        self.gap = nn.AdaptiveAvgPool2d(1)    # 任意 H×W → 1×1

    def forward(self, x):
        x = self.features(x)     # (B, num_classes, H, W)
        x = self.gap(x)          # (B, num_classes, 1, 1)
        x = x.flatten(1)         # (B, num_classes)
        return x


# ============================================================
# 2. 对比参数量 / Compare Parameter Counts
# ============================================================

model_gap = GAPClassifier(num_classes=10)
x = torch.randn(4, 3, 32, 32)
print(f"GAP 模型输出: {model_gap(x).shape}")  # [4, 10]
gap_params = sum(p.numel() for p in model_gap.parameters())
print(f"GAP 模型参数量: {gap_params:,}")

# 对比传统 FC 头 / Compare with traditional FC head
class FCClassifier(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),                        # 32→16
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),                        # 16→8
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),                        # 8→4
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                            # 128×4×4 = 2048
            nn.Linear(128 * 4 * 4, 512),             # 大 FC 层!
            nn.ReLU(),
            nn.Linear(512, num_classes),
        )
    def forward(self, x):
        return self.classifier(self.features(x))

model_fc = FCClassifier(num_classes=10)
fc_params = sum(p.numel() for p in model_fc.parameters())
print(f"FC 模型参数量: {fc_params:,}")
print(f"GAP 减少参数: {(fc_params - gap_params) / fc_params * 100:.1f}%")
```

> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

---

### 示例 2: Inception 风格混合 AvgPool + MaxPool 分支

```python
import torch
import torch.nn as nn

# ============================================================
# Inception Block 中 AvgPool 分支 / AvgPool Branch in Inception
# ============================================================

class InceptionBlock(nn.Module):
    """
    简化版 Inception 模块: 4 个并行分支
    Simplified Inception module: 4 parallel branches
    """
    def __init__(self, in_channels, ch1x1, ch3x3, ch5x5, ch_pool):
        super().__init__()
        # 分支 1: 1×1 卷积 / Branch 1: 1×1 conv
        self.branch1 = nn.Sequential(
            nn.Conv2d(in_channels, ch1x1, 1), nn.ReLU()
        )
        # 分支 2: 3×3 卷积 / Branch 2: 3×3 conv
        self.branch2 = nn.Sequential(
            nn.Conv2d(in_channels, ch3x3, 3, padding=1), nn.ReLU()
        )
        # 分支 3: 5×5 卷积 / Branch 3: 5×5 conv
        self.branch3 = nn.Sequential(
            nn.Conv2d(in_channels, ch5x5, 5, padding=2), nn.ReLU()
        )
        # 分支 4: AvgPool + 1×1 卷积 / Branch 4: AvgPool + 1×1 conv
        self.branch4 = nn.Sequential(
            nn.AvgPool2d(kernel_size=3, stride=1, padding=1),  # 保持尺寸
            nn.Conv2d(in_channels, ch_pool, 1), nn.ReLU()       # 降维
        )

    def forward(self, x):
        b1 = self.branch1(x)
        b2 = self.branch2(x)
        b3 = self.branch3(x)
        b4 = self.branch4(x)
        # 在通道维度拼接 / Concatenate along channel dimension
        return torch.cat([b1, b2, b3, b4], dim=1)


block = InceptionBlock(256, ch1x1=64, ch3x3=128, ch5x5=32, ch_pool=32)
x = torch.randn(4, 256, 14, 14)
print(f"Inception 输出: {block(x).shape}")  # [4, 256, 14, 14]
```

> 📖 Paper: Szegedy et al., [GoogLeNet](https://arxiv.org/abs/1409.4842), CVPR 2015

---

### 示例 3: Keras/TensorFlow Average Pooling

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ============================================================
# Keras GAP 分类器 / Keras GAP Classifier
# ============================================================

model = keras.Sequential([
    layers.Input(shape=(32, 32, 3)),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.AveragePooling2D(pool_size=2, strides=2),   # 局部 AvgPool: 32→16
    layers.Conv2D(128, 3, padding='same', activation='relu'),
    layers.AveragePooling2D(pool_size=2, strides=2),   # 16→8
    layers.Conv2D(10, 1, activation='relu'),            # 1×1 conv: 128→10
    layers.GlobalAveragePooling2D(),                    # GAP: 8×8→1
    layers.Activation('softmax'),                       # 分类 / Classification
])

model.summary()
```

> 📖 Docs: [TF AveragePooling2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/AveragePooling2D)

---

## API 速查

### PyTorch AvgPool

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.AvgPool1d(kernel_size)` | `kernel_size` | — | 1D 平均池化 |
| ↳ | `stride` | kernel_size | 步长 |
| ↳ | `padding` | 0 | 零填充 |
| ↳ | `ceil_mode` | False | True 用 ceil 计算输出 |
| ↳ | `count_include_pad` | True | 零填充是否计入均值分母 |
| `nn.AvgPool2d(kernel_size)` | `kernel_size` | — | 2D 平均池化 |
| ↳ | 参数同上 | — | — |
| `nn.AvgPool3d(kernel_size)` | `kernel_size` | — | 3D 平均池化 |
| `nn.AdaptiveAvgPool2d(output_size)` | `output_size` | — | 自适应输出尺寸 |
| ↳ | `output_size=1` | — | **Global Average Pooling** |
| ↳ | `output_size=(H, W)` | — | 自适应到指定 H×W |

### Keras/TF AveragePooling

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `layers.AveragePooling1D(pool_size)` | `pool_size` | 2 | 1D 平均池化 |
| `layers.AveragePooling2D(pool_size)` | `pool_size` | (2,2) | 2D 平均池化 |
| ↳ | `strides` | pool_size | 步长 |
| ↳ | `padding` | 'valid' | 'valid' 或 'same' |
| `layers.GlobalAveragePooling2D()` | — | — | **全局平均池化** |
| `layers.GlobalAveragePooling1D()` | — | — | 1D 全局平均（NLP 序列） |

### 常用工具

| 函数 | 说明 |
|------|------|
| `torch.nn.functional.avg_pool2d(input, kernel_size)` | 函数式 API |
| `torch.mean(input, dim=[2,3])` | 手动 GAP：对 H,W 维取均值 |
| `input.mean(dim=[2,3], keepdim=True)` | 保持维度的手动 GAP |

> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)

---

## 目录结构模板

### 简单结构

```
project/
├── model.py              ← 含 AvgPool/GAP 的 CNN 模型
├── train.py              ← 训练脚本
└── data/
    ├── train/
    └── val/
```

### 标准结构

```
project/
├── config.py             ← 超参数（pool 类型选择等）
├── models/
│   ├── resnet.py          ← GAP + FC 分类头
│   └── inception.py       ← 混合 AvgPool + MaxPool 分支
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
│   └── pool_ablation.yaml  ← AvgPool vs MaxPool vs GAP 消融实验
├── models/
│   ├── pooling.py          ← 自定义池化层（GeM、混合池化等）
│   ├── backbone.py         ← 骨干网络
│   └── head.py             ← GAP 分类头
├── trainers/
├── utils/
├── train.py
├── evaluate.py
└── requirements.txt
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9
