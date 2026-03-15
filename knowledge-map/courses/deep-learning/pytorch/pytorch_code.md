---
topic: pytorch
dimension: code
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Docs: [PyTorch Tutorials](https://pytorch.org/tutorials/) — v2.10"
  - "📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf)"
expiry: 6m
status: current
---

# PyTorch 代码参考

> 📖 Docs: [PyTorch Official Tutorials](https://pytorch.org/tutorials/)
> 📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf)


## 快速开始

### 最简示例 — 30 秒上手

```python
import torch

# 1. 创建张量 / Create tensor
# 创建一个 2x3 的随机张量 / Create a 2x3 random tensor
x = torch.randn(2, 3)
print(f"Tensor: {x}")
print(f"Shape: {x.shape}, dtype: {x.dtype}, device: {x.device}")

# 2. GPU 加速（如果可用）/ GPU acceleration (if available)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = x.to(device)
print(f"Device: {x.device}")

# 3. 自动微分 / Automatic differentiation
# requires_grad=True 让 PyTorch 追踪操作 / Track operations for gradient
w = torch.tensor([2.0, 3.0], requires_grad=True)
y = (w * 3).sum()           # 前向传播 / Forward pass
y.backward()                 # 反向传播 / Backward pass
print(f"Gradients: {w.grad}")  # dy/dw = [3, 3]
```

**测试方法：** 复制到 Python 终端直接运行，无需安装额外依赖。

> 📖 Docs: [Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

---


## 完整实现示例

### 示例 1: MNIST 手写数字分类（经典入门）

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# ============================================================
# 1. 超参数 / Hyperparameters
# ============================================================
BATCH_SIZE = 64       # 每批样本数 / Samples per batch
EPOCHS = 5            # 训练轮数 / Training epochs
LR = 0.001            # 学习率 / Learning rate
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ============================================================
# 2. 数据准备 / Data Preparation
# transforms.Compose 将多个变换串联 / Chain multiple transforms
# ============================================================
transform = transforms.Compose([
    transforms.ToTensor(),                # PIL → Tensor, 值从 [0,255] → [0,1]
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST 全局均值和标准差 / MNIST mean & std
])

train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST('./data', train=False, transform=transform)

# DataLoader 负责批量化、打乱、多进程加载 / Handles batching, shuffling, multi-process loading
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

# ============================================================
# 3. 模型定义 / Model Definition
# 继承 nn.Module，在 __init__ 中定义层，在 forward 中定义数据流
# Inherit nn.Module, define layers in __init__, data flow in forward
# ============================================================
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()           # 28x28 → 784
        self.fc1 = nn.Linear(784, 128)        # 全连接层 / Fully connected layer
        self.relu = nn.ReLU()                 # 激活函数 / Activation function
        self.dropout = nn.Dropout(0.2)        # 防过拟合 / Prevent overfitting
        self.fc2 = nn.Linear(128, 10)         # 输出 10 个类别 / Output 10 classes

    def forward(self, x):
        x = self.flatten(x)    # [B, 1, 28, 28] → [B, 784]
        x = self.fc1(x)        # [B, 784] → [B, 128]
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)        # [B, 128] → [B, 10] (raw logits)
        return x                # 返回 logits，不加 softmax / Return logits, no softmax

model = SimpleNet().to(DEVICE)
print(model)

# ============================================================
# 4. 损失函数 + 优化器 / Loss Function + Optimizer
# CrossEntropyLoss 内含 softmax，输入是 raw logits
# CrossEntropyLoss includes softmax, input is raw logits
# ============================================================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

# ============================================================
# 5. 训练循环 / Training Loop
# ============================================================
def train(model, loader, criterion, optimizer, device):
    model.train()                          # 启用 Dropout/BN 训练行为 / Enable training mode
    total_loss = 0
    for batch_idx, (data, target) in enumerate(loader):
        data, target = data.to(device), target.to(device)  # 迁移到 GPU / Move to GPU

        optimizer.zero_grad()              # ① 清零梯度 / Zero gradients
        output = model(data)               # ② 前向传播 / Forward pass
        loss = criterion(output, target)   # ③ 计算损失 / Compute loss
        loss.backward()                    # ④ 反向传播 / Backward pass
        optimizer.step()                   # ⑤ 更新参数 / Update parameters

        total_loss += loss.item()
    return total_loss / len(loader)

# ============================================================
# 6. 评估函数 / Evaluation Function
# ============================================================
def evaluate(model, loader, device):
    model.eval()                           # 关闭 Dropout / Disable dropout
    correct = 0
    total = 0
    with torch.no_grad():                  # 禁用梯度计算，节省内存 / No gradients needed
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1)    # 取概率最大的类别 / Class with highest probability
            correct += (pred == target).sum().item()
            total += target.size(0)
    return correct / total

# ============================================================
# 7. 主训练流程 / Main Training Flow
# ============================================================
for epoch in range(1, EPOCHS + 1):
    train_loss = train(model, train_loader, criterion, optimizer, DEVICE)
    accuracy = evaluate(model, test_loader, DEVICE)
    print(f"Epoch {epoch}: Loss={train_loss:.4f}, Accuracy={accuracy:.4f}")

# ============================================================
# 8. 保存和加载模型 / Save & Load Model
# 推荐保存 state_dict 而非整个模型 / Recommend saving state_dict, not entire model
# ============================================================
torch.save(model.state_dict(), 'mnist_model.pth')

# 加载 / Load
loaded_model = SimpleNet().to(DEVICE)
loaded_model.load_state_dict(torch.load('mnist_model.pth', weights_only=True))
loaded_model.eval()
```

> 📖 Docs: [Quickstart Tutorial](https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)
> 📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.5-7

---

### 示例 2: 自定义 Dataset（通用模式）

```python
import torch
from torch.utils.data import Dataset, DataLoader
import os
from PIL import Image

# ============================================================
# 自定义数据集：实现 __len__ 和 __getitem__
# Custom Dataset: implement __len__ and __getitem__
# ============================================================
class CustomImageDataset(Dataset):
    def __init__(self, img_dir, labels, transform=None):
        """
        Args:
            img_dir:    图片目录路径 / Path to image directory
            labels:     标签列表 / List of labels
            transform:  数据变换 / Data transforms
        """
        self.img_dir = img_dir
        self.labels = labels
        self.transform = transform
        self.img_names = os.listdir(img_dir)

    def __len__(self):
        """返回数据集大小 / Return dataset size"""
        return len(self.img_names)

    def __getitem__(self, idx):
        """
        返回单个样本 (image, label)
        Return single sample (image, label)
        """
        img_path = os.path.join(self.img_dir, self.img_names[idx])
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label

# 使用 / Usage
# dataset = CustomImageDataset('path/to/images', labels, transform=transform)
# loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)
```

> 📖 Docs: [Dataset & DataLoader](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)

---

### 示例 3: 迁移学习（Transfer Learning）

```python
import torch
import torch.nn as nn
from torchvision import models

# ============================================================
# 加载预训练 ResNet18，替换最后的分类头
# Load pretrained ResNet18, replace the final classification head
# ============================================================
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# 冻结所有预训练层 / Freeze all pretrained layers
for param in model.parameters():
    param.requires_grad = False

# 替换最后一层：1000 类 → 自定义类数 / Replace final layer: 1000 → custom classes
num_classes = 10
model.fc = nn.Linear(model.fc.in_features, num_classes)
# 新层的参数默认 requires_grad=True / New layer params default to requires_grad=True

# 只优化新层 / Only optimize the new layer
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)

print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad)}")
```

> 📖 Docs: [Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

---


## API 速查

### Tensor 创建

| 函数 | 说明 | 默认 dtype |
|------|------|-----------|
| `torch.tensor(data)` | 从 Python 列表/数组创建 | 推断自 data |
| `torch.zeros(shape)` | 全零张量 | float32 |
| `torch.ones(shape)` | 全一张量 | float32 |
| `torch.randn(shape)` | 标准正态分布随机 | float32 |
| `torch.rand(shape)` | [0,1) 均匀分布随机 | float32 |
| `torch.arange(start, end, step)` | 等差序列 | int64 |
| `torch.from_numpy(ndarray)` | NumPy 转 Tensor（共享内存） | 同 ndarray |
| `torch.empty(shape)` | 未初始化张量 | float32 |

### Tensor 操作

| 操作 | 方法 | 说明 |
|------|------|------|
| 形状变换 | `x.view(shape)` / `x.reshape(shape)` | view 要求连续内存 |
| 转置 | `x.T` / `x.permute(dims)` | permute 支持任意维度 |
| 拼接 | `torch.cat([a,b], dim=0)` | 沿已有维度拼接 |
| 堆叠 | `torch.stack([a,b], dim=0)` | 新增维度后拼接 |
| 索引 | `x[0, :, 2:]` | NumPy 风格索引 |
| 设备转移 | `x.to(device)` | CPU ↔ GPU |
| 类型转换 | `x.float()` / `x.long()` | 快捷类型转换 |
| 分离梯度 | `x.detach()` | 从计算图分离 |

### nn.Module 常用层

| 层 | 类 | 关键参数 |
|-----|-----|---------|
| 全连接 | `nn.Linear(in, out)` | `bias=True` |
| 2D 卷积 | `nn.Conv2d(in_ch, out_ch, kernel)` | `stride, padding` |
| 池化 | `nn.MaxPool2d(kernel)` | `stride` |
| BatchNorm | `nn.BatchNorm2d(features)` | `momentum=0.1` |
| Dropout | `nn.Dropout(p)` | `p=0.5` |
| ReLU | `nn.ReLU(inplace=False)` | `inplace` 节省内存 |
| LSTM | `nn.LSTM(input, hidden)` | `num_layers, bidirectional` |
| Embedding | `nn.Embedding(vocab, dim)` | `padding_idx` |

### 优化器

| 优化器 | 类 | 典型 lr |
|--------|-----|--------|
| SGD | `optim.SGD(params, lr)` | 0.01 - 0.1 |
| Adam | `optim.Adam(params, lr)` | 0.001 |
| AdamW | `optim.AdamW(params, lr)` | 0.001 |

> 📖 Docs: [torch.nn](https://pytorch.org/docs/stable/nn.html)
> 📖 Docs: [torch.optim](https://pytorch.org/docs/stable/optim.html)

---


## 目录结构模板

### 简单结构

```
my_project/
├── train.py           # 训练脚本 / Training script
├── model.py           # 模型定义 / Model definition
├── dataset.py         # 数据加载 / Data loading
├── requirements.txt
└── data/              # 数据目录 / Data directory
```

### 标准结构

```
my_project/
├── configs/
│   └── default.yaml       # 超参数配置 / Hyperparameter config
├── data/
│   ├── raw/               # 原始数据 / Raw data
│   └── processed/         # 预处理后 / Processed data
├── models/
│   ├── __init__.py
│   ├── backbone.py        # 主干网络 / Backbone network
│   └── head.py            # 任务头 / Task head
├── utils/
│   ├── __init__.py
│   ├── metrics.py         # 评估指标 / Evaluation metrics
│   └── transforms.py      # 数据变换 / Data transforms
├── train.py
├── evaluate.py
├── predict.py
└── requirements.txt
```

### 高级结构（Lightning 风格）

```
my_project/
├── configs/
├── src/
│   ├── data/
│   │   ├── datamodule.py      # Lightning DataModule
│   │   └── transforms.py
│   ├── models/
│   │   ├── lightning_module.py # Lightning Module
│   │   └── components/
│   ├── utils/
│   └── __init__.py
├── scripts/
│   ├── train.py
│   └── evaluate.py
├── tests/
├── checkpoints/
├── logs/
└── pyproject.toml
```

> 📖 Docs: [PyTorch Lightning Project Structure](https://lightning.ai/docs/pytorch/stable/)
