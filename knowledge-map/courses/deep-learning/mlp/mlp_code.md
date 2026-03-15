---
topic: mlp
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: PyTorch nn Module — https://pytorch.org/docs/stable/nn.html"
  - "📖 Docs: PyTorch nn.Linear — https://pytorch.org/docs/stable/generated/torch.nn.Linear.html"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# MLP (Multi-Layer Perceptron) 代码参考

> 📖 Docs: [PyTorch nn Module](https://pytorch.org/docs/stable/nn.html)
> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)


## 快速开始

### 最简示例 — 30 秒上手 (PyTorch)

```python
import torch
import torch.nn as nn

# ============================================================
# 定义一个两层 MLP / Define a two-layer MLP
# ============================================================
model = nn.Sequential(
    nn.Linear(784, 128),   # 全连接层: 784 → 128 / Fully connected: 784 → 128
    nn.ReLU(),             # 激活函数 / Activation function
    nn.Linear(128, 10)     # 输出层: 128 → 10 / Output layer: 128 → 10
)

# 随机输入测试 / Test with random input
x = torch.randn(32, 784)  # batch_size=32, 输入维度=784
output = model(x)          # 前向传播 / Forward pass
print(output.shape)        # torch.Size([32, 10])
```

**测试方法：** 运行上述代码，确认输出 shape 为 `[32, 10]`。无需 GPU，CPU 即可运行。

> 📖 Docs: [PyTorch nn.Sequential](https://pytorch.org/docs/stable/generated/torch.nn.Sequential.html)

---

## 完整实现示例

### 示例 1: MNIST 手写数字分类（PyTorch 完整训练流程）

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
transform = transforms.Compose([
    transforms.ToTensor(),                          # 转为张量 [0,1] / Convert to tensor
    transforms.Normalize((0.1307,), (0.3081,))      # MNIST 均值和标准差 / MNIST mean & std
])

train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST('./data', train=False, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
class MLP(nn.Module):
    """三层 MLP 分类器 / Three-layer MLP classifier"""
    def __init__(self, input_dim=784, hidden1=256, hidden2=128, output_dim=10):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden1),    # 第一隐藏层 / First hidden layer
            nn.ReLU(),                        # 激活函数 / Activation
            nn.Dropout(0.2),                  # 防过拟合 / Prevent overfitting
            nn.Linear(hidden1, hidden2),      # 第二隐藏层 / Second hidden layer
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden2, output_dim)    # 输出层 / Output layer
        )

    def forward(self, x):
        x = x.view(x.size(0), -1)            # 展平: [B,1,28,28] → [B,784] / Flatten
        return self.network(x)

model = MLP()
print(f"参数量 / Parameters: {sum(p.numel() for p in model.parameters()):,}")
# 约 235,146 个参数

# ============================================================
# 3. 训练循环 / Training Loop
# ============================================================
criterion = nn.CrossEntropyLoss()             # 交叉熵损失 / Cross-entropy loss
optimizer = optim.Adam(model.parameters(), lr=1e-3)  # Adam 优化器

def train_epoch(model, loader, criterion, optimizer):
    """训练一个 epoch / Train for one epoch"""
    model.train()                             # 训练模式(启用 Dropout) / Training mode
    total_loss = 0
    correct = 0
    for data, target in loader:
        optimizer.zero_grad()                 # 清零梯度 / Zero gradients
        output = model(data)                  # 前向传播 / Forward pass
        loss = criterion(output, target)      # 计算损失 / Compute loss
        loss.backward()                       # 反向传播 / Backward pass
        optimizer.step()                      # 更新参数 / Update parameters
        total_loss += loss.item()
        correct += (output.argmax(1) == target).sum().item()
    acc = correct / len(loader.dataset)
    return total_loss / len(loader), acc

def evaluate(model, loader, criterion):
    """评估模型 / Evaluate model"""
    model.eval()                              # 评估模式(关闭 Dropout) / Eval mode
    total_loss = 0
    correct = 0
    with torch.no_grad():                     # 不计算梯度 / No gradients needed
        for data, target in loader:
            output = model(data)
            total_loss += criterion(output, target).item()
            correct += (output.argmax(1) == target).sum().item()
    acc = correct / len(loader.dataset)
    return total_loss / len(loader), acc

# 训练 10 个 epoch / Train for 10 epochs
for epoch in range(1, 11):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer)
    test_loss, test_acc = evaluate(model, test_loader, criterion)
    print(f"Epoch {epoch:2d} | "
          f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | "
          f"Test Loss: {test_loss:.4f} Acc: {test_acc:.4f}")

# ============================================================
# 4. 测试评估 / Evaluation
# ============================================================
final_loss, final_acc = evaluate(model, test_loader, criterion)
print(f"\n最终测试准确率 / Final Test Accuracy: {final_acc:.4f}")
# 预期: ~98%
```

> 📖 Docs: [PyTorch nn Module](https://pytorch.org/docs/stable/nn.html)
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

### 示例 2: scikit-learn MLP（快速原型验证）

```python
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
digits = load_digits()                        # 8x8 手写数字 / 8x8 handwritten digits
X_train, X_test, y_train, y_test = train_test_split(
    digits.data, digits.target, test_size=0.2, random_state=42
)

scaler = StandardScaler()                     # 标准化 / Standardize
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ============================================================
# 2. 模型定义与训练 / Model Definition & Training
# ============================================================
mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64),             # 两个隐藏层 / Two hidden layers
    activation='relu',                        # ReLU 激活 / ReLU activation
    solver='adam',                            # Adam 优化器 / Adam optimizer
    max_iter=200,                             # 最大迭代 / Max iterations
    random_state=42,
    early_stopping=True,                      # 早停 / Early stopping
    validation_fraction=0.1                   # 10% 验证集 / 10% validation
)

mlp.fit(X_train, y_train)

# ============================================================
# 3. 评估 / Evaluation
# ============================================================
y_pred = mlp.predict(X_test)
print(f"准确率 / Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))
# 预期: ~97%+
```

> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

### 示例 3: 从零实现 MLP（NumPy，理解原理）

```python
import numpy as np

# ============================================================
# 1. 激活函数定义 / Activation Functions
# ============================================================
def relu(z):
    """ReLU 激活函数 / ReLU activation function"""
    return np.maximum(0, z)

def relu_derivative(z):
    """ReLU 导数 / ReLU derivative"""
    return (z > 0).astype(float)

def softmax(z):
    """Softmax 函数 / Softmax function"""
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # 数值稳定 / Numerical stability
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

# ============================================================
# 2. MLP 类定义 / MLP Class Definition
# ============================================================
class SimpleMLP:
    """从零实现的两层 MLP / Two-layer MLP implemented from scratch"""

    def __init__(self, input_dim, hidden_dim, output_dim):
        # He 初始化 / He initialization
        self.W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, output_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros((1, output_dim))

    def forward(self, X):
        """前向传播 / Forward propagation"""
        self.z1 = X @ self.W1 + self.b1       # 线性变换 / Linear transform
        self.a1 = relu(self.z1)               # ReLU 激活 / ReLU activation
        self.z2 = self.a1 @ self.W2 + self.b2 # 输出层 / Output layer
        self.a2 = softmax(self.z2)            # Softmax / Softmax
        return self.a2

    def backward(self, X, y_onehot, lr=0.01):
        """反向传播 + 参数更新 / Backprop + parameter update"""
        m = X.shape[0]                        # 批大小 / Batch size

        # 输出层梯度 / Output layer gradient
        dz2 = self.a2 - y_onehot              # softmax + CE 的梯度 / Gradient of softmax+CE
        dW2 = (self.a1.T @ dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m

        # 隐藏层梯度 / Hidden layer gradient
        dz1 = (dz2 @ self.W2.T) * relu_derivative(self.z1)
        dW1 = (X.T @ dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m

        # 参数更新 / Parameter update
        self.W2 -= lr * dW2
        self.b2 -= lr * db2
        self.W1 -= lr * dW1
        self.b1 -= lr * db1

    def predict(self, X):
        """预测类别 / Predict class"""
        probs = self.forward(X)
        return np.argmax(probs, axis=1)

# ============================================================
# 3. 训练示例 / Training Example
# ============================================================
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

digits = load_digits()
X = StandardScaler().fit_transform(digits.data)
y = digits.target

# one-hot 编码 / One-hot encoding
y_onehot = np.zeros((len(y), 10))
y_onehot[np.arange(len(y)), y] = 1

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
y_train_oh = np.zeros((len(y_train), 10))
y_train_oh[np.arange(len(y_train)), y_train] = 1

model = SimpleMLP(input_dim=64, hidden_dim=128, output_dim=10)

for epoch in range(500):
    model.forward(X_train)
    model.backward(X_train, y_train_oh, lr=0.1)
    if (epoch + 1) % 100 == 0:
        pred = model.predict(X_test)
        acc = np.mean(pred == y_test)
        print(f"Epoch {epoch+1}: Test Accuracy = {acc:.4f}")

# 预期: ~95%+
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5 (Backpropagation)

---

## API 速查

### PyTorch 核心层

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Linear(in, out)` | `in_features` | 必填 | 全连接层：y = xW^T + b |
| ↳ `bias` | `bool` | `True` | 是否包含偏置 |
| `nn.ReLU()` | `inplace` | `False` | ReLU 激活，推荐默认 |
| `nn.LeakyReLU(α)` | `negative_slope` | `0.01` | 解决 dying ReLU |
| `nn.Sigmoid()` | — | — | Sigmoid 激活 |
| `nn.Tanh()` | — | — | Tanh 激活 |
| `nn.Dropout(p)` | `p` | `0.5` | 训练时随机关闭神经元 |
| `nn.BatchNorm1d(n)` | `num_features` | 必填 | 批归一化 |
| `nn.Sequential(*layers)` | 层列表 | — | 按顺序堆叠层 |

### PyTorch 损失函数

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `nn.CrossEntropyLoss()` | — | 内含 softmax + NLLLoss |
| `nn.MSELoss()` | — | 均方误差 |
| `nn.BCEWithLogitsLoss()` | — | 二分类（内含 sigmoid） |

### PyTorch 优化器

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `optim.SGD(params, lr)` | `lr`, `momentum`, `weight_decay` | 随机梯度下降 |
| `optim.Adam(params, lr)` | `lr=1e-3`, `betas=(0.9, 0.999)` | 自适应学习率 |
| `optim.AdamW(params, lr)` | `lr`, `weight_decay` | 解耦权重衰减 |

### PyTorch 初始化

| 函数 | 说明 |
|------|------|
| `nn.init.xavier_uniform_(w)` | Xavier 均匀初始化（sigmoid/tanh） |
| `nn.init.xavier_normal_(w)` | Xavier 正态初始化 |
| `nn.init.kaiming_uniform_(w)` | He 均匀初始化（ReLU） |
| `nn.init.kaiming_normal_(w)` | He 正态初始化（ReLU） |
| `nn.init.zeros_(b)` | 零初始化（偏置常用） |

### 常用工具

| 函数 | 说明 |
|------|------|
| `model.train()` | 切换训练模式（启用 Dropout/BN） |
| `model.eval()` | 切换评估模式（关闭 Dropout/BN） |
| `torch.no_grad()` | 上下文管理器，禁用梯度计算 |
| `optimizer.zero_grad()` | 清零梯度（每次迭代前调用） |
| `loss.backward()` | 反向传播计算梯度 |
| `optimizer.step()` | 更新参数 |

> 📖 Docs: [PyTorch nn Module](https://pytorch.org/docs/stable/nn.html)
> 📖 Docs: [PyTorch Optim](https://pytorch.org/docs/stable/optim.html)

---

## 目录结构模板

### 简单结构

```
mlp_project/
├── train.py              ← 训练脚本（含模型定义、训练循环）
├── data/                 ← 数据集目录
│   └── mnist/
└── requirements.txt      ← torch, torchvision
```

### 标准结构

```
mlp_project/
├── config.py             ← 超参数配置
├── dataset.py            ← 数据加载与预处理
├── model.py              ← MLP 模型定义
├── train.py              ← 训练脚本
├── evaluate.py           ← 评估与可视化
├── utils.py              ← 辅助函数
├── data/                 ← 数据集
├── checkpoints/          ← 模型权重保存
└── logs/                 ← 训练日志
```

### 高级结构

```
mlp_project/
├── configs/
│   ├── default.yaml      ← 默认超参数
│   └── experiment.yaml   ← 实验配置
├── models/
│   ├── mlp.py            ← MLP 模型
│   └── layers.py         ← 自定义层
├── datasets/
│   ├── mnist.py
│   └── transforms.py
├── trainers/
│   └── trainer.py        ← 通用训练器
├── utils/
│   ├── metrics.py
│   └── visualization.py
├── train.py              ← 入口脚本
├── evaluate.py
├── predict.py
├── checkpoints/
├── logs/
└── requirements.txt
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.11 (Practical Methodology)
