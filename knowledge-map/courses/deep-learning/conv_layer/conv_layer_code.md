---
topic: conv_layer
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: PyTorch nn.Conv2d — https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html"
  - "📖 Docs: TensorFlow Conv2D — https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Conv Layer (卷积层) 代码参考

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
> 📖 Docs: [TF/Keras Conv2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D)


## 快速开始

### 最简示例 — 30 秒上手 (PyTorch)

```python
import torch
import torch.nn as nn

# ============================================================
# 单个卷积层 / Single convolutional layer
# ============================================================
conv = nn.Conv2d(
    in_channels=3,      # 输入通道 (RGB) / Input channels
    out_channels=16,     # 输出通道 (滤波器数) / Output channels
    kernel_size=3,       # 卷积核 3×3 / Kernel size
    stride=1,            # 步长 1 / Stride
    padding=1            # 填充 1 → 保持尺寸 / Padding for same size
)

x = torch.randn(1, 3, 32, 32)    # [B, C_in, H, W]
y = conv(x)
print(f"输入: {x.shape}")         # torch.Size([1, 3, 32, 32])
print(f"输出: {y.shape}")         # torch.Size([1, 16, 32, 32])
print(f"参数: {sum(p.numel() for p in conv.parameters())}")   # (3×3×3+1)×16 = 448
```

**测试方法：** 运行后确认输出 shape 和参数量。CPU 即可运行。

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

---

## 完整实现示例

### 示例 1: 4 种 CNN 架构对比（对应作业需求）

```python
import torch
import torch.nn as nn

# ============================================================
# Model 1: Conv + Dense (无池化)
# ============================================================
class Model1_ConvDense(nn.Module):
    """Conv layers + Dense layers as hidden layers"""
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),   # [B,3,32,32] → [B,32,32,32]  P=(3×3×3+1)×32=896
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, padding=1),  # [B,32,32,32] → [B,64,32,32] P=(3×3×32+1)×64=18496
            nn.ReLU(),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                     # [B,64,32,32] → [B,65536]
            nn.Linear(64*32*32, 128),         # P=65536×128+128=8388736
            nn.ReLU(),
            nn.Linear(128, num_classes),      # P=128×10+10=1290
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

# ============================================================
# Model 2: Conv + MaxPool + Dense
# ============================================================
class Model2_ConvMaxPoolDense(nn.Module):
    """Conv + MaxPool + Dense layers"""
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),   # → [B,32,32,32]  P=896
            nn.ReLU(),
            nn.MaxPool2d(2, 2),               # → [B,32,16,16]  P=0
            nn.Conv2d(32, 64, 3, padding=1),  # → [B,64,16,16]  P=18496
            nn.ReLU(),
            nn.MaxPool2d(2, 2),               # → [B,64,8,8]    P=0
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                     # → [B,4096]
            nn.Linear(64*8*8, 128),           # P=4096×128+128=524416
            nn.ReLU(),
            nn.Linear(128, num_classes),      # P=1290
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

# ============================================================
# Model 3: Conv + AvgPool + Dense
# ============================================================
class Model3_ConvAvgPoolDense(nn.Module):
    """Conv + AvgPool + Dense layers"""
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),   # → [B,32,32,32]  P=896
            nn.ReLU(),
            nn.AvgPool2d(2, 2),               # → [B,32,16,16]  P=0
            nn.Conv2d(32, 64, 3, padding=1),  # → [B,64,16,16]  P=18496
            nn.ReLU(),
            nn.AvgPool2d(2, 2),               # → [B,64,8,8]    P=0
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                     # → [B,4096]
            nn.Linear(64*8*8, 128),           # P=524416
            nn.ReLU(),
            nn.Linear(128, num_classes),      # P=1290
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

# ============================================================
# Model 4: Conv + MaxPool + AvgPool + Dense
# ============================================================
class Model4_ConvMaxAvgDense(nn.Module):
    """Conv + MaxPool + AvgPool + Dense layers"""
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),   # → [B,32,32,32]  P=896
            nn.ReLU(),
            nn.MaxPool2d(2, 2),               # → [B,32,16,16]  P=0
            nn.Conv2d(32, 64, 3, padding=1),  # → [B,64,16,16]  P=18496
            nn.ReLU(),
            nn.AvgPool2d(2, 2),               # → [B,64,8,8]    P=0
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                     # → [B,4096]
            nn.Linear(64*8*8, 128),           # P=524416
            nn.ReLU(),
            nn.Linear(128, num_classes),      # P=1290
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

# ============================================================
# 验证所有模型 / Verify all models
# ============================================================
x = torch.randn(2, 3, 32, 32)  # CIFAR-10 尺寸
for name, Model in [("Model1", Model1_ConvDense),
                     ("Model2", Model2_ConvMaxPoolDense),
                     ("Model3", Model3_ConvAvgPoolDense),
                     ("Model4", Model4_ConvMaxAvgDense)]:
    model = Model()
    y = model(x)
    params = sum(p.numel() for p in model.parameters())
    print(f"{name}: output={y.shape}, params={params:,}")
```

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

---

### 示例 2: 打印每层输出尺寸和参数量

```python
import torch
import torch.nn as nn

def layer_summary(model, input_size=(1, 3, 32, 32)):
    """打印模型每层的名称、输出形状、参数量"""
    x = torch.randn(*input_size)
    print(f"{'Layer':<30} {'Output Shape':<20} {'Params':>10}")
    print("-" * 62)

    total_params = 0
    for name, layer in model.named_modules():
        if name == '':  # 跳过根模块
            continue
        if isinstance(layer, (nn.Conv2d, nn.Linear, nn.MaxPool2d, nn.AvgPool2d,
                              nn.ReLU, nn.Flatten, nn.Dropout)):
            x = layer(x)
            params = sum(p.numel() for p in layer.parameters())
            total_params += params
            print(f"{name:<30} {str(list(x.shape)):<20} {params:>10,}")

    print("-" * 62)
    print(f"{'Total':<30} {'':<20} {total_params:>10,}")

# 使用示例
model = Model2_ConvMaxPoolDense()
layer_summary(model)
```

> 📖 Docs: [PyTorch nn Module](https://pytorch.org/docs/stable/nn.html)

---

### 示例 3: 从零实现 2D 卷积（NumPy，理解原理）

```python
import numpy as np

def conv2d_naive(X, W, b, stride=1, padding=0):
    """从零实现 2D 卷积 / Naive 2D convolution from scratch

    Args:
        X: 输入 [C_in, H, W]
        W: 滤波器 [C_out, C_in, K, K]
        b: 偏置 [C_out]
        stride: 步长
        padding: 填充
    Returns:
        Y: 输出 [C_out, H_out, W_out]
    """
    C_in, H, W = X.shape
    C_out, _, K, _ = W.shape

    # 填充 / Padding
    if padding > 0:
        X = np.pad(X, ((0,0), (padding,padding), (padding,padding)), mode='constant')
    _, H_pad, W_pad = X.shape

    # 输出尺寸 / Output size
    H_out = (H_pad - K) // stride + 1
    W_out = (W_pad - K) // stride + 1
    Y = np.zeros((C_out, H_out, W_out))

    # 卷积操作 / Convolution operation
    for m in range(C_out):                          # 每个滤波器
        for i in range(H_out):                      # 每个输出行
            for j in range(W_out):                  # 每个输出列
                # 提取局部区域 / Extract local patch
                h_start = i * stride
                w_start = j * stride
                patch = X[:, h_start:h_start+K, w_start:w_start+K]
                # 逐元素乘法 + 求和 + 偏置 / Element-wise multiply + sum + bias
                Y[m, i, j] = np.sum(patch * W[m]) + b[m]

    return Y

# 测试 / Test
X = np.random.randn(3, 8, 8)              # 3通道 8×8
W = np.random.randn(16, 3, 3, 3)          # 16个 3×3 滤波器
b = np.zeros(16)
Y = conv2d_naive(X, W, b, stride=1, padding=1)
print(f"输入: {X.shape}")                  # (3, 8, 8)
print(f"输出: {Y.shape}")                  # (16, 8, 8) → 保持尺寸
print(f"参数量: {W.size + b.size}")        # 3×3×3×16 + 16 = 448
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

---

## API 速查

### PyTorch Conv2d

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `in_channels` | int | 必填 | 输入通道数 |
| `out_channels` | int | 必填 | 输出通道数 = 滤波器数 |
| `kernel_size` | int/tuple | 必填 | 卷积核大小 |
| `stride` | int/tuple | `1` | 步长 |
| `padding` | int/tuple/str | `0` | 填充。`'same'`=保持尺寸 |
| `dilation` | int/tuple | `1` | 膨胀率（空洞卷积） |
| `groups` | int | `1` | 分组卷积。`=in_channels`时为 depthwise |
| `bias` | bool | `True` | 是否有偏置 |

### 常用卷积配置

| 用途 | PyTorch 代码 | 效果 |
|------|-------------|------|
| 保持尺寸 | `Conv2d(C, C, 3, padding=1)` | $H_{out} = H_{in}$ |
| 尺寸减半 | `Conv2d(C, 2C, 3, stride=2, padding=1)` | $H_{out} = H_{in}/2$ |
| 通道变换 | `Conv2d(C_in, C_out, 1)` | 1×1 卷积 |
| 深度可分离 | `Conv2d(C, C, 3, groups=C, padding=1)` + `Conv2d(C, C_out, 1)` | 参数减 ~9× |
| 空洞卷积 | `Conv2d(C, C, 3, dilation=2, padding=2)` | 感受野扩大 |

### Keras/TensorFlow Conv2D

| 参数 | 说明 |
|------|------|
| `filters` | 输出通道数 |
| `kernel_size` | 核大小 |
| `strides` | 步长（注意复数形式） |
| `padding` | `'valid'` 或 `'same'` |
| `activation` | 可直接指定激活函数 |
| `input_shape` | 第一层需要指定 |

```python
# Keras 等价写法
tf.keras.layers.Conv2D(16, (3,3), padding='same', activation='relu', input_shape=(32,32,3))
```

> 📖 Docs: [TF Conv2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D)

---

## 目录结构模板

```
cnn_project/
├── models/
│   ├── model1_conv_dense.py        ← Conv + Dense
│   ├── model2_conv_maxpool.py      ← Conv + MaxPool + Dense
│   ├── model3_conv_avgpool.py      ← Conv + AvgPool + Dense
│   └── model4_conv_mixed.py        ← Conv + MaxPool + AvgPool + Dense
├── train.py                        ← 训练脚本
├── evaluate.py                     ← 评估与可视化
├── utils.py                        ← 模型摘要打印、参数统计
├── data/                           ← 数据集
├── checkpoints/                    ← 模型权重
└── requirements.txt                ← torch, torchvision
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.11
