---
topic: neural_network
dimension: code
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Docs: PyTorch nn Module — https://pytorch.org/docs/stable/generated/torch.nn.Module.html"
  - "📖 Docs: PyTorch nn.Linear — https://pytorch.org/docs/stable/generated/torch.nn.Linear.html"
  - "📖 Docs: Keras Sequential — https://keras.io/guides/sequential_model/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Neural Network (神经网络) 代码参考

> 📖 Docs: [PyTorch nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)
> 📖 Docs: [Keras Sequential](https://keras.io/guides/sequential_model/)

## 快速开始

### 最简示例 — 30 秒上手 (PyTorch)

```python
import torch
import torch.nn as nn

# ============================================================
# 1. 定义网络 / Define Network
# ============================================================
model = nn.Sequential(
    nn.Linear(2, 4),   # 输入2维 → 隐藏层4个神经元 / Input 2D → 4 hidden units
    nn.ReLU(),          # 激活函数 / Activation function
    nn.Linear(4, 1),   # 隐藏层4 → 输出1维 / 4 hidden → 1 output
    nn.Sigmoid()        # 输出概率 / Output probability
)

# ============================================================
# 2. 前向传播 / Forward Pass
# ============================================================
x = torch.tensor([[1.0, 0.0]])  # 单个样本 / Single sample
y_hat = model(x)                 # 预测 / Prediction
print(f"预测值 / Prediction: {y_hat.item():.4f}")
```

**测试方法：** 直接运行即可看到输出一个 0~1 之间的概率值。

---

## 完整实现示例

### 示例 1: 从零实现神经网络 (NumPy)

```python
import numpy as np

# ============================================================
# 1. 数据准备 / Data Preparation — XOR 问题
# ============================================================
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])  # 4个样本 / 4 samples
y = np.array([[0], [1], [1], [0]])                # XOR 标签 / XOR labels

# ============================================================
# 2. 参数初始化 / Parameter Initialization
# ============================================================
np.random.seed(42)
W1 = np.random.randn(2, 4) * 0.5   # 输入→隐藏层权重 / Input→Hidden weights
b1 = np.zeros((1, 4))               # 隐藏层偏置 / Hidden bias
W2 = np.random.randn(4, 1) * 0.5   # 隐藏层→输出权重 / Hidden→Output weights
b2 = np.zeros((1, 1))               # 输出偏置 / Output bias

# ============================================================
# 3. 激活函数 / Activation Functions
# ============================================================
def sigmoid(z):
    """Sigmoid 激活 / Sigmoid activation"""
    return 1 / (1 + np.exp(-z))

def sigmoid_deriv(a):
    """Sigmoid 导数 / Sigmoid derivative: σ'(z) = σ(z)(1-σ(z))"""
    return a * (1 - a)

# ============================================================
# 4. 训练循环 / Training Loop
# ============================================================
lr = 1.0  # 学习率 / Learning rate
for epoch in range(10000):
    # --- 前向传播 / Forward Pass ---
    z1 = X @ W1 + b1           # 隐藏层线性组合 / Hidden pre-activation
    h1 = sigmoid(z1)            # 隐藏层激活 / Hidden activation
    z2 = h1 @ W2 + b2          # 输出层线性组合 / Output pre-activation
    y_hat = sigmoid(z2)         # 输出层激活 / Output activation

    # --- 损失计算 / Loss Calculation ---
    loss = np.mean((y_hat - y) ** 2)  # MSE 损失 / MSE Loss

    # --- 反向传播 / Backward Pass ---
    delta2 = 2 * (y_hat - y) * sigmoid_deriv(y_hat)  # 输出层误差 / Output error
    dW2 = h1.T @ delta2 / len(X)                      # ∂L/∂W2
    db2 = np.mean(delta2, axis=0, keepdims=True)       # ∂L/∂b2

    delta1 = (delta2 @ W2.T) * sigmoid_deriv(h1)      # 隐藏层误差 / Hidden error
    dW1 = X.T @ delta1 / len(X)                        # ∂L/∂W1
    db1 = np.mean(delta1, axis=0, keepdims=True)       # ∂L/∂b1

    # --- 参数更新 / Parameter Update ---
    W2 -= lr * dW2
    b2 -= lr * db2
    W1 -= lr * dW1
    b1 -= lr * db1

    if epoch % 2000 == 0:
        print(f"Epoch {epoch:5d} | Loss: {loss:.6f}")

# ============================================================
# 5. 验证结果 / Verify Results
# ============================================================
print("\n最终预测 / Final Predictions:")
for i in range(len(X)):
    print(f"  {X[i]} → {y_hat[i, 0]:.4f} (目标/target: {y[i, 0]})")
```

### 示例 2: PyTorch MNIST 分类

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# ============================================================
# 1. 数据加载 / Data Loading
# ============================================================
transform = transforms.Compose([
    transforms.ToTensor(),                          # 图片→张量 / Image→Tensor
    transforms.Normalize((0.1307,), (0.3081,))      # MNIST 标准化 / MNIST normalization
])
train_data = datasets.MNIST('./data', train=True, download=True, transform=transform)
test_data = datasets.MNIST('./data', train=False, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=1000)

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
class SimpleNN(nn.Module):
    """简单三层全连接网络 / Simple 3-layer fully connected network"""
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()                  # 28×28 → 784
        self.layers = nn.Sequential(
            nn.Linear(784, 256),                     # 第一隐藏层 / First hidden layer
            nn.ReLU(),                               # 激活函数 / Activation
            nn.Linear(256, 128),                     # 第二隐藏层 / Second hidden layer
            nn.ReLU(),
            nn.Linear(128, 10)                       # 输出层: 10个数字类别 / Output: 10 classes
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.layers(x)

model = SimpleNN()

# ============================================================
# 3. 训练配置 / Training Configuration
# ============================================================
criterion = nn.CrossEntropyLoss()                    # 交叉熵损失 / Cross-entropy loss
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam 优化器 / Adam optimizer

# ============================================================
# 4. 训练循环 / Training Loop
# ============================================================
for epoch in range(5):
    model.train()
    total_loss = 0
    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()            # 梯度清零 / Clear gradients
        output = model(batch_x)          # 前向传播 / Forward pass
        loss = criterion(output, batch_y) # 计算损失 / Compute loss
        loss.backward()                  # 反向传播 / Backward pass
        optimizer.step()                 # 更新参数 / Update parameters
        total_loss += loss.item()
    print(f"Epoch {epoch+1} | Loss: {total_loss/len(train_loader):.4f}")

# ============================================================
# 5. 测试评估 / Test Evaluation
# ============================================================
model.eval()
correct = 0
with torch.no_grad():
    for batch_x, batch_y in test_loader:
        output = model(batch_x)
        pred = output.argmax(dim=1)
        correct += (pred == batch_y).sum().item()
print(f"测试准确率 / Test Accuracy: {correct/len(test_data)*100:.2f}%")
```

### 示例 3: Keras 实现

```python
import tensorflow as tf
from tensorflow import keras

# ============================================================
# 1. 数据加载 / Data Loading
# ============================================================
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0  # 展平+归一化 / Flatten+normalize
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
model = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(784,)),  # 隐藏层1 / Hidden 1
    keras.layers.Dense(128, activation='relu'),                      # 隐藏层2 / Hidden 2
    keras.layers.Dense(10, activation='softmax')                     # 输出层 / Output
])

# ============================================================
# 3. 编译+训练 / Compile+Train
# ============================================================
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # 交叉熵 / Cross-entropy
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)

# ============================================================
# 4. 评估 / Evaluate
# ============================================================
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"测试准确率 / Test Accuracy: {test_acc*100:.2f}%")
```

---

## API 速查

### PyTorch 核心类

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Module` | — | — | 所有网络的基类 / Base class for all networks |
| `nn.Linear(in, out)` | `in_features`, `out_features` | — | 全连接层 y=Wx+b / Fully connected layer |
| ↳ `bias` | `bool` | `True` | 是否包含偏置 / Include bias |
| `nn.Sequential(*layers)` | 层列表 | — | 顺序容器 / Sequential container |
| `nn.ReLU()` | — | — | ReLU 激活 / ReLU activation |
| `nn.Sigmoid()` | — | — | Sigmoid 激活 / Sigmoid activation |
| `nn.Softmax(dim)` | `dim` | — | Softmax 归一化 / Softmax normalization |
| `nn.CrossEntropyLoss()` | — | — | 交叉熵损失（含 Softmax） / CE loss (includes Softmax) |
| `nn.MSELoss()` | — | — | 均方误差损失 / MSE loss |

### PyTorch 训练 API

| 函数 | 说明 |
|------|------|
| `model.train()` | 切换训练模式（启用 Dropout/BN） / Switch to train mode |
| `model.eval()` | 切换评估模式（禁用 Dropout/BN） / Switch to eval mode |
| `optimizer.zero_grad()` | 清除旧梯度 / Clear old gradients |
| `loss.backward()` | 反向传播计算梯度 / Backprop to compute gradients |
| `optimizer.step()` | 一步参数更新 / One parameter update step |
| `torch.no_grad()` | 禁用梯度计算（推理用） / Disable grad computation |

### Keras 核心 API

| 函数/类 | 说明 |
|---------|------|
| `keras.Sequential(layers)` | 序贯模型 / Sequential model |
| `keras.layers.Dense(units, activation)` | 全连接层 / Dense layer |
| `model.compile(optimizer, loss, metrics)` | 配置训练 / Configure training |
| `model.fit(x, y, epochs, batch_size)` | 训练模型 / Train model |
| `model.evaluate(x, y)` | 评估模型 / Evaluate model |
| `model.predict(x)` | 预测 / Predict |

---

## 目录结构模板

### 简单结构

```
project/
├── train.py              ← 训练脚本（含模型定义+训练循环）
├── data/                 ← 数据目录
│   └── mnist/
└── requirements.txt      ← 依赖：torch, torchvision
```

### 标准结构

```
project/
├── config.py             ← 超参数配置
├── dataset.py            ← 数据加载和预处理
├── model.py              ← 模型定义（nn.Module 子类）
├── train.py              ← 训练循环
├── evaluate.py           ← 测试评估
├── utils.py              ← 辅助函数（metrics, logging）
├── data/                 ← 数据
├── checkpoints/          ← 模型检查点
├── logs/                 ← TensorBoard 日志
└── requirements.txt
```
