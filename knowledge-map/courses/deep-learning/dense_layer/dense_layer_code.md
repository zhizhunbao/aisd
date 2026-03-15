---
topic: dense_layer
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: PyTorch nn.Linear — https://pytorch.org/docs/stable/generated/torch.nn.Linear.html"
  - "📖 Docs: Keras Dense — https://keras.io/api/layers/core_layers/dense/"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "💻 Source: pytorch/pytorch — https://github.com/pytorch/pytorch"
expiry: 6m
status: current
---

# Dense Layer 代码参考

> 📖 Docs: [PyTorch nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html)
> 📖 Docs: [Keras Dense](https://keras.io/api/layers/core_layers/dense/)

## 快速开始

### 最简示例 — NumPy 手动实现一个 Dense Layer

```python
# ============================================================
# Dense Layer 最简实现: 纯 NumPy / Minimal Dense Layer
# ============================================================
import numpy as np

# 定义参数 / Define parameters
n_in, n_out = 3, 2
W = np.random.randn(n_out, n_in) * 0.01   # 权重矩阵 (2×3)
b = np.zeros(n_out)                         # 偏置 (2,)

# 前向传播 / Forward pass
x = np.array([1.0, 2.0, 3.0])              # 输入 (3,)
z = W @ x + b                               # 仿射变换 z = Wx + b
a = np.maximum(0, z)                         # ReLU 激活

print(f"输入 / Input: {x}")
print(f"线性输出 / Linear output z: {z}")
print(f"激活后 / After ReLU a: {a}")
print(f"参数量 / Parameters: {W.size + b.size}")  # 3×2 + 2 = 8
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1

---

## 完整实现示例

### 示例 1: PyTorch nn.Linear

```python
# ============================================================
# 1. PyTorch Dense Layer / nn.Linear
# ============================================================
import torch
import torch.nn as nn

# 创建 Dense Layer / Create Dense Layer
layer = nn.Linear(in_features=784, out_features=256, bias=True)

# 查看参数 / Inspect parameters
print(f"权重形状 / Weight shape: {layer.weight.shape}")  # (256, 784)
print(f"偏置形状 / Bias shape: {layer.bias.shape}")       # (256,)
print(f"参数量 / Parameters: {sum(p.numel() for p in layer.parameters()):,}")
# 784 × 256 + 256 = 201,024

# 前向传播 / Forward pass
x = torch.randn(32, 784)                    # batch=32, features=784
z = layer(x)                                 # 计算 xW^T + b
a = torch.relu(z)                            # ReLU 激活
print(f"输出形状 / Output shape: {a.shape}")  # (32, 256)
```

### 示例 2: Keras Dense

```python
# ============================================================
# 2. Keras Dense Layer
# ============================================================
import keras
from keras import layers

# 方式 1: 内置激活函数 / Built-in activation
layer1 = layers.Dense(256, activation='relu', input_shape=(784,))

# 方式 2: 分离式（推荐，便于插入 BatchNorm 等）
layer2 = layers.Dense(256, use_bias=False)    # 无偏置
bn = layers.BatchNormalization()               # 归一化
act = layers.Activation('relu')                # 激活

# 构建模型 / Build model
model = keras.Sequential([
    layers.Dense(256, activation='relu', input_shape=(784,)),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')      # 分类输出
])
model.summary()
```

### 示例 3: 从零实现 Dense Layer（教学版）

```python
# ============================================================
# 3. 从零实现 Dense Layer + 反向传播 / From Scratch
# ============================================================
import numpy as np

class DenseLayer:
    """手动实现含前向和反向传播的 Dense Layer"""
    def __init__(self, n_in, n_out, activation='relu'):
        # He 初始化 / He initialization (for ReLU)
        self.W = np.random.randn(n_out, n_in) * np.sqrt(2.0 / n_in)
        self.b = np.zeros(n_out)
        self.activation = activation

        # 缓存用于反向传播 / Cache for backward pass
        self.x = None
        self.z = None

    def forward(self, x):
        """前向传播 / Forward: a = σ(Wx + b)"""
        self.x = x                              # 缓存输入
        self.z = self.W @ x + self.b             # 仿射变换
        if self.activation == 'relu':
            return np.maximum(0, self.z)          # ReLU
        elif self.activation == 'sigmoid':
            return 1 / (1 + np.exp(-self.z))      # Sigmoid
        else:
            return self.z                          # 无激活（线性）

    def backward(self, grad_output, lr=0.01):
        """反向传播 / Backward: 计算梯度并更新参数"""
        # 计算激活函数的导数 / Activation derivative
        if self.activation == 'relu':
            grad_act = (self.z > 0).astype(float)  # ReLU 导数: 0 or 1
        elif self.activation == 'sigmoid':
            s = 1 / (1 + np.exp(-self.z))
            grad_act = s * (1 - s)                  # Sigmoid 导数
        else:
            grad_act = np.ones_like(self.z)          # 线性: 导数为 1

        # 误差信号 / Error signal
        delta = grad_output * grad_act               # δ = ∂L/∂a ⊙ σ'(z)

        # 计算梯度 / Compute gradients
        grad_W = np.outer(delta, self.x)             # ∂L/∂W = δ · xᵀ
        grad_b = delta                                # ∂L/∂b = δ
        grad_x = self.W.T @ delta                    # ∂L/∂x = Wᵀδ

        # 更新参数 / Update parameters
        self.W -= lr * grad_W
        self.b -= lr * grad_b

        return grad_x  # 传递给前一层

# 使用示例 / Usage
layer = DenseLayer(3, 2, activation='relu')
x = np.array([1.0, 2.0, 3.0])
output = layer.forward(x)
print(f"Output: {output}")

# 假设梯度来自后续层 / Assume gradient from next layer
grad = np.array([1.0, -1.0])
grad_input = layer.backward(grad, lr=0.01)
print(f"Gradient to prev layer: {grad_input}")
```

### 示例 4: Dense Layer 在常见架构中的使用

```python
# ============================================================
# 4. Dense Layer 在不同架构中的角色
# ============================================================
import torch.nn as nn

# 4.1 MLP 分类器（全部是 Dense + 激活）
class MLPClassifier(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=256, num_classes=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),    # Dense 1
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(hidden_dim, hidden_dim),   # Dense 2
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(hidden_dim, num_classes),  # Dense 3 (输出层)
        )
    def forward(self, x):
        return self.net(x.flatten(1))             # Flatten → Dense

# 4.2 CNN 分类头（Conv → Flatten → Dense）
class CNNClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 5 * 5, 128),          # Dense 分类头
            nn.ReLU(),
            nn.Linear(128, 10),                   # 输出层
        )
    def forward(self, x):
        x = self.features(x)
        x = x.flatten(1)                           # Flatten
        return self.classifier(x)

# 4.3 Transformer FFN（两层 Dense 构成）
class TransformerFFN(nn.Module):
    def __init__(self, d_model=512, d_ff=2048):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)  # 扩展
        self.linear2 = nn.Linear(d_ff, d_model)  # 压缩
    def forward(self, x):
        return self.linear2(torch.relu(self.linear1(x)))
```

> 📖 Docs: [nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html)

---

## API 速查

### PyTorch nn.Linear

| 参数 | 类型 | 默认值 | 说明 |
|-----|----|-------|------|
| `in_features` | int | 必需 | 输入特征数 $n_{in}$ |
| `out_features` | int | 必需 | 输出特征数 $n_{out}$ |
| `bias` | bool | `True` | 是否包含偏置 |

| 属性 | 形状 | 说明 |
|------|-----|------|
| `.weight` | `(out_features, in_features)` | 权重矩阵 |
| `.bias` | `(out_features,)` | 偏置向量 |

### Keras Dense

| 参数 | 类型 | 默认值 | 说明 |
|-----|----|-------|------|
| `units` | int | 必需 | 输出维度 $n_{out}$ |
| `activation` | str/None | `None` | 激活函数 |
| `use_bias` | bool | `True` | 是否包含偏置 |
| `kernel_initializer` | str | `'glorot_uniform'` | 权重初始化 |
| `bias_initializer` | str | `'zeros'` | 偏置初始化 |

### 常用初始化

| PyTorch | Keras | 适用激活 |
|---------|-------|---------|
| `nn.init.xavier_uniform_(layer.weight)` | `'glorot_uniform'` | Sigmoid/Tanh |
| `nn.init.xavier_normal_(layer.weight)` | `'glorot_normal'` | Sigmoid/Tanh |
| `nn.init.kaiming_uniform_(layer.weight)` | `'he_uniform'` | ReLU |
| `nn.init.kaiming_normal_(layer.weight)` | `'he_normal'` | ReLU |

> 📖 Docs: [PyTorch nn.init](https://pytorch.org/docs/stable/nn.init.html)
> 📖 Docs: [Keras Initializers](https://keras.io/api/layers/initializers/)

---

## 目录结构模板

```
dense-layer-demo/
├── dense_from_scratch.py   ← 纯 NumPy 实现
├── dense_pytorch.py        ← PyTorch nn.Linear 示例
├── dense_keras.py          ← Keras Dense 示例
└── test_dense.py           ← 测试（前向+梯度验证）
```
