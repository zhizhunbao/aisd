---
topic: forward_propagation
dimension: code
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Docs: PyTorch nn.Module — https://pytorch.org/docs/stable/generated/torch.nn.Module.html"
  - "📖 Docs: PyTorch nn.Linear — https://pytorch.org/docs/stable/generated/torch.nn.Linear.html"
  - "📚 Book: Stevens, Antiga & Viehmann, Deep Learning with PyTorch, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/stevens_deep_learning_with_pytorch.pdf"
expiry: 6m
status: current
---

# Forward Propagation 代码参考

> 📖 Docs: [PyTorch nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)

## 快速开始

### 最简示例 — 30 秒上手

```python
import torch
import torch.nn as nn

# ============================================================
# 1. 定义一个两层网络 / Define a 2-layer network
# ============================================================
model = nn.Sequential(
    nn.Linear(2, 3),   # 第1层: 2输入 → 3隐藏 / Layer 1: 2 inputs → 3 hidden
    nn.ReLU(),          # 激活函数 / Activation function
    nn.Linear(3, 1),   # 第2层: 3隐藏 → 1输出 / Layer 2: 3 hidden → 1 output
)

# ============================================================
# 2. 前向传播 / Forward propagation
# ============================================================
x = torch.tensor([[1.0, 2.0]])  # 输入: 1个样本, 2个特征 / Input: 1 sample, 2 features
y_hat = model(x)                # 调用 model(x) 就是前向传播 / Calling model(x) IS forward prop
print(f"预测值 / Prediction: {y_hat}")
```

**测试方法：** 运行后会输出一个浮点数预测值（每次不同，因为权重随机初始化）

> 📖 Docs: [PyTorch nn.Sequential](https://pytorch.org/docs/stable/generated/torch.nn.Sequential.html)

---

## 完整实现示例

### 示例 1: 手动实现前向传播（不用 nn.Module）

```python
import torch

# ============================================================
# 1. 初始化参数 / Initialize parameters
# ============================================================
torch.manual_seed(42)
W1 = torch.randn(3, 2, requires_grad=True)  # 第1层权重 / Layer 1 weights: (3, 2)
b1 = torch.zeros(3, requires_grad=True)     # 第1层偏置 / Layer 1 bias: (3,)
W2 = torch.randn(1, 3, requires_grad=True)  # 第2层权重 / Layer 2 weights: (1, 3)
b2 = torch.zeros(1, requires_grad=True)     # 第2层偏置 / Layer 2 bias: (1,)

# ============================================================
# 2. 手动前向传播 / Manual forward propagation
# ============================================================
x = torch.tensor([[1.0, 2.0]])  # 输入 / Input: (1, 2)

# 第1层: 仿射变换 + 激活 / Layer 1: affine + activation
z1 = x @ W1.T + b1              # z1 = W1·x + b1, shape: (1, 3)
a1 = torch.relu(z1)             # a1 = ReLU(z1), shape: (1, 3)

# 第2层: 仿射变换 / Layer 2: affine (无激活, 回归任务)
z2 = a1 @ W2.T + b2             # z2 = W2·a1 + b2, shape: (1, 1)
y_hat = z2                      # 输出 / Output

print(f"z1 = {z1}")
print(f"a1 = {a1}")
print(f"y_hat = {y_hat}")
```

### 示例 2: 用 nn.Module 自定义网络的前向传播

```python
import torch
import torch.nn as nn

# ============================================================
# 1. 定义网络类 / Define network class
# ============================================================
class SimpleNet(nn.Module):
    def __init__(self, in_features, hidden_features, out_features):
        super().__init__()
        # 层定义 / Layer definitions
        self.fc1 = nn.Linear(in_features, hidden_features)   # 全连接层1 / FC layer 1
        self.fc2 = nn.Linear(hidden_features, out_features)  # 全连接层2 / FC layer 2
        self.relu = nn.ReLU()                                # 激活函数 / Activation

    def forward(self, x):
        """前向传播: 数据从输入流向输出 / Forward pass: data flows from input to output"""
        z1 = self.fc1(x)      # 仿射变换 / Affine: z1 = W1·x + b1
        a1 = self.relu(z1)    # 激活 / Activation: a1 = ReLU(z1)
        z2 = self.fc2(a1)     # 仿射变换 / Affine: z2 = W2·a1 + b2
        return z2              # 返回预测值 / Return prediction

# ============================================================
# 2. 实例化并执行前向传播 / Instantiate and run forward pass
# ============================================================
model = SimpleNet(in_features=784, hidden_features=128, out_features=10)
x = torch.randn(32, 784)  # 32个样本, 784维特征 / 32 samples, 784-dim features
y_hat = model(x)           # 前向传播! / Forward propagation!
print(f"输出形状 / Output shape: {y_hat.shape}")  # torch.Size([32, 10])

# ============================================================
# 3. 训练 vs 推理模式 / Training vs inference mode
# ============================================================
# 训练时: 构建计算图 / Training: builds computation graph
model.train()
y_hat_train = model(x)

# 推理时: 关闭计算图, 省显存 / Inference: no graph, saves memory
model.eval()
with torch.no_grad():
    y_hat_infer = model(x)
```

> 📖 Docs: [PyTorch nn.Module.forward](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.forward)

---

## API 速查

### nn.Linear — 全连接层（前向传播的核心组件）

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Linear(in_features, out_features)` | `in_features` | — | 输入特征维度 / Input dimension |
| ↳ | `out_features` | — | 输出特征维度 / Output dimension |
| ↳ | `bias` | `True` | 是否包含偏置项 $b$ / Include bias |

### nn.Sequential — 顺序容器

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Sequential(*layers)` | `*layers` | — | 按顺序排列的层 / Layers in order |
| 调用 `model(x)` | — | — | 依次对 $x$ 执行每层的前向传播 |

### 推理优化

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `model.eval()` | — | — | 切换到推理模式 / Switch to eval mode |
| `torch.no_grad()` | — | — | 关闭梯度追踪, 不缓存中间值 / Disable grad |
| `torch.inference_mode()` | — | — | 比 no_grad 更快 (PyTorch 1.9+) |

---

## 目录结构模板

### 简单结构

```
project/
├── model.py              ← 网络定义 (含 forward 方法)
├── train.py              ← 训练循环 (前向+反向+优化)
├── predict.py            ← 推理脚本 (仅前向传播)
└── data/
    ├── train/
    └── val/
```

### 标准结构

```
project/
├── config.py             ← 超参数配置
├── dataset.py            ← 数据加载
├── model.py              ← 网络定义
├── train.py              ← 训练循环
├── evaluate.py           ← 评估脚本
├── utils.py              ← 工具函数
├── data/
├── checkpoints/          ← 保存模型权重
└── logs/                 ← TensorBoard 日志
```
