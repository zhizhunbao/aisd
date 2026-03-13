---
topic: cnn
dimension: code
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.8"
  - "📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)"
  - "📖 Docs: [PyTorch Training a Classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)"
expiry: 6m
status: current
---

# CNN 代码参考

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
> 📖 Docs: [PyTorch Training a Classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import torch
import torch.nn as nn

# 定义一个最简 CNN: 1个卷积层 + 1个全连接层
# Define a minimal CNN: 1 conv layer + 1 FC layer
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # 输入3通道(RGB), 输出16个特征图, 3×3卷积核
        # Input: 3 channels (RGB), Output: 16 feature maps, 3×3 kernel
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)               # 2×2 最大池化 / max pooling
        self.relu = nn.ReLU()
        self.fc = nn.Linear(16 * 16 * 16, 10)        # 展平后全连接到10类 / flatten → 10 classes

    def forward(self, x):                              # x: [B, 3, 32, 32]
        x = self.pool(self.relu(self.conv1(x)))        # → [B, 16, 16, 16]
        x = x.view(x.size(0), -1)                     # 展平 / flatten → [B, 4096]
        x = self.fc(x)                                 # → [B, 10]
        return x

# 测试 / Test
model = SimpleCNN()
dummy = torch.randn(1, 3, 32, 32)                     # 假输入: 1张32×32 RGB图
output = model(dummy)
print(f"Output shape: {output.shape}")                 # torch.Size([1, 10])
```

**测试方法：** 复制代码到 Python 终端运行，应输出 `torch.Size([1, 10])`

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

---


## 完整实现示例

### 示例 1: CIFAR-10 分类器（经典教材风格）

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),                 # 数据增强: 随机水平翻转 / augmentation: random flip
    transforms.RandomCrop(32, padding=4),              # 数据增强: 随机裁剪 / augmentation: random crop
    transforms.ToTensor(),                             # 转为张量 [0,1] / convert to tensor
    transforms.Normalize((0.4914, 0.4822, 0.4465),     # CIFAR-10 均值 / mean
                         (0.2470, 0.2435, 0.2616))     # CIFAR-10 标准差 / std
])

# 下载并加载 CIFAR-10 训练集和测试集
# Download and load CIFAR-10 train/test sets
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False, num_workers=2)

# CIFAR-10 的 10 个类别 / 10 classes
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
class CIFAR10Net(nn.Module):
    """
    经典 CNN 架构: 3 个卷积块 + 2 个全连接层
    Classic CNN: 3 conv blocks + 2 FC layers
    """
    def __init__(self):
        super().__init__()
        # 卷积块1: Conv → BN → ReLU → MaxPool
        # Conv block 1: Conv → BN → ReLU → MaxPool
        self.conv_block1 = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),            # [B,3,32,32] → [B,32,32,32]
            nn.BatchNorm2d(32),                        # 批归一化 / batch normalization
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)                         # → [B,32,16,16]
        )
        # 卷积块2 / Conv block 2
        self.conv_block2 = nn.Sequential(
            nn.Conv2d(32, 64, 3, padding=1),           # → [B,64,16,16]
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)                         # → [B,64,8,8]
        )
        # 卷积块3 / Conv block 3
        self.conv_block3 = nn.Sequential(
            nn.Conv2d(64, 128, 3, padding=1),          # → [B,128,8,8]
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)                         # → [B,128,4,4]
        )
        # 分类器 / Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),                              # → [B, 128*4*4] = [B, 2048]
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),                           # 防过拟合 / prevent overfitting
            nn.Linear(256, 10)                         # 10 类输出 / 10 classes
        )

    def forward(self, x):
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        x = self.conv_block3(x)
        x = self.classifier(x)
        return x

# ============================================================
# 3. 训练循环 / Training Loop
# ============================================================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CIFAR10Net().to(device)
criterion = nn.CrossEntropyLoss()                      # 交叉熵损失 / cross-entropy loss
optimizer = optim.Adam(model.parameters(), lr=0.001)   # Adam 优化器 / optimizer

num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in trainloader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()                          # 清零梯度 / zero gradients
        outputs = model(images)                        # 前向传播 / forward pass
        loss = criterion(outputs, labels)              # 计算损失 / compute loss
        loss.backward()                                # 反向传播 / backward pass
        optimizer.step()                               # 更新权重 / update weights

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    train_acc = 100. * correct / total
    print(f'Epoch [{epoch+1}/{num_epochs}] Loss: {running_loss/len(trainloader):.4f} Acc: {train_acc:.2f}%')

# ============================================================
# 4. 测试评估 / Evaluation
# ============================================================
model.eval()
correct = 0
total = 0
with torch.no_grad():                                 # 推理时不计算梯度 / no grad for inference
    for images, labels in testloader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

print(f'Test Accuracy: {100. * correct / total:.2f}%')
```

> 📖 Docs: [PyTorch Training a Classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---

### 示例 2: 迁移学习 — 使用预训练 ResNet-18

```python
import torch
import torch.nn as nn
import torchvision.models as models

# ============================================================
# 迁移学习: 加载预训练 ResNet-18，替换最后的分类头
# Transfer Learning: Load pretrained ResNet-18, replace classifier head
# ============================================================

# 加载预训练模型 / Load pretrained model
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# 冻结所有卷积层参数（不更新） / Freeze all conv layers (no gradient update)
for param in model.parameters():
    param.requires_grad = False

# 替换最后的全连接层 / Replace final FC layer
# ResNet-18 原始输出 1000 类(ImageNet)，改为我们的类别数
# Original: 1000 classes (ImageNet) → Our number of classes
num_classes = 10
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 只训练新的 FC 层 / Only train the new FC layer
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)

# 查看可训练参数 / Check trainable parameters
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"Trainable: {trainable:,} / Total: {total:,} ({100*trainable/total:.1f}%)")
# 输出约: Trainable: 5,130 / Total: 11,181,642 (0.05%)
```

> 📖 Docs: [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

---

### 示例 3: 自定义数据集的 CNN（ImageFolder）

```python
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# ============================================================
# 使用 ImageFolder 加载自定义图片目录
# Load custom image directory with ImageFolder
# ============================================================
# 目录结构 / Directory structure:
#   data/train/cats/  ← 猫的图片
#   data/train/dogs/  ← 狗的图片
#   data/val/cats/
#   data/val/dogs/

transform = transforms.Compose([
    transforms.Resize((224, 224)),                     # 统一尺寸 / resize to uniform size
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],        # ImageNet 均值 / mean
                         [0.229, 0.224, 0.225])         # ImageNet 标准差 / std
])

# ImageFolder 自动用子文件夹名作为类别标签
# ImageFolder automatically uses subfolder names as class labels
train_dataset = datasets.ImageFolder('data/train', transform=transform)
val_dataset = datasets.ImageFolder('data/val', transform=transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

print(f"Classes: {train_dataset.classes}")             # ['cats', 'dogs']
print(f"Train size: {len(train_dataset)}")
```

> 📖 Docs: [PyTorch Data Loading Tutorial](https://pytorch.org/tutorials/beginner/data_loading_tutorial.html)

---


## API 速查

### 卷积层

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Conv2d(in, out, kernel)` | `in_channels, out_channels, kernel_size` | — | 2D 卷积层 |
| ↳ `stride` | int 或 tuple | `1` | 步长 |
| ↳ `padding` | int, tuple, 或 `'same'` | `0` | 填充 |
| ↳ `bias` | bool | `True` | 是否加偏置 |
| ↳ `groups` | int | `1` | 分组卷积 (depthwise 时 = in_channels) |
| `nn.Conv1d` | 同上 | — | 1D 卷积（时序/文本） |
| `nn.ConvTranspose2d` | 同上 | — | 转置卷积（上采样） |

### 池化层

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.MaxPool2d(kernel)` | `kernel_size` | — | 最大池化 |
| ↳ `stride` | int | `= kernel_size` | 步长 |
| `nn.AvgPool2d(kernel)` | `kernel_size` | — | 平均池化 |
| `nn.AdaptiveAvgPool2d(output)` | `output_size` | — | 自适应平均池化（GAP 用 `(1,1)`） |

### 归一化与正则化

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `nn.BatchNorm2d(num_features)` | 通道数 | 批归一化（CNN 标配） |
| `nn.Dropout(p)` | 丢弃概率 | 随机丢弃（全连接层用） |
| `nn.Dropout2d(p)` | 丢弃概率 | 随机丢弃整个通道（卷积层用） |

### 常用工具

| 函数 | 说明 |
|------|------|
| `torchvision.models.resnet18(weights=...)` | 加载预训练模型 |
| `torchvision.transforms.Compose([...])` | 数据预处理流水线 |
| `torchvision.datasets.CIFAR10(...)` | CIFAR-10 数据集 |
| `torchvision.datasets.ImageFolder(...)` | 从文件夹加载自定义数据集 |

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
> 📖 Docs: [torchvision.models](https://pytorch.org/vision/stable/models.html)

---


## 目录结构模板

### 简单结构

```
cnn_project/
├── train.py              ← 训练脚本
├── model.py              ← 模型定义
└── data/
    ├── train/
    │   ├── class_a/
    │   └── class_b/
    └── val/
        ├── class_a/
        └── class_b/
```

### 标准结构

```
cnn_project/
├── config.py             ← 超参数配置
├── dataset.py            ← 自定义 Dataset
├── model.py              ← 模型定义
├── train.py              ← 训练循环
├── evaluate.py           ← 评估脚本
├── utils.py              ← 工具函数
├── data/
│   ├── train/
│   ├── val/
│   └── test/
├── checkpoints/          ← 模型权重保存
└── logs/                 ← TensorBoard 日志
```

### 高级结构

```
cnn_project/
├── configs/
│   ├── resnet18.yaml
│   └── vgg16.yaml
├── models/
│   ├── __init__.py
│   ├── resnet.py
│   └── vgg.py
├── datasets/
│   ├── __init__.py
│   ├── cifar10.py
│   └── custom.py
├── trainers/
│   ├── __init__.py
│   └── classifier.py
├── utils/
│   ├── metrics.py
│   ├── visualization.py
│   └── augmentation.py
├── train.py
├── evaluate.py
├── predict.py
├── checkpoints/
├── logs/
└── requirements.txt
```

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8
