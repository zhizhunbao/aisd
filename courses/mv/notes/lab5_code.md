# Lab 5 — CNN (Convolutional Neural Network, 卷积神经网络) 代码参考

> **See also:** [lab5_cheatsheet.md](lab5_cheatsheet.md) · [lab5_math.md](lab5_math.md) · [Lab 文档](../labs/CST8508_Lab5.md)
>
> ❌ 本文件不含概念定义、不含数学推导 — 仅 PyTorch API 用法和代码模式

---

## 🔧 Imports 速查

```python
# ── 核心依赖 ────────────────────────────────────────────────────────────────
import os, random, zipfile, urllib.request
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Subset

from torchvision import datasets, transforms
from PIL import Image
from sklearn.metrics import classification_report
```

---

## 🔧 设备检测（Device Detection）

```python
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# 将模型移动到设备
model = model.to(DEVICE)

# 将 tensor 移动到设备（训练循环中）
imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
```

---

## 🔧 数据集加载模式（Dataset Loading Pattern）

### `ImageFolder` — 从文件夹结构加载

```python
# 要求文件夹结构:
# PetImages/
#   Cat/  ← 自动识别为 class 0
#   Dog/  ← 自动识别为 class 1

dataset = datasets.ImageFolder(root="PetImages/", transform=transform)
print(dataset.classes)   # ['Cat', 'Dog']
print(dataset.class_to_idx)  # {'Cat': 0, 'Dog': 1}
```

### 随机划分训练/测试集

```python
random.seed(42)        # 固定种子保证可复现
torch.manual_seed(42)

n = len(full_dataset)
train_n = int(n * 0.8)
idx = list(range(n))
random.shuffle(idx)

train_data = Subset(full_dataset, idx[:train_n])
test_data  = Subset(full_dataset, idx[train_n:])
```

### `DataLoader` 创建

```python
train_loader = DataLoader(train_data, batch_size=32, shuffle=True,  num_workers=2)
test_loader  = DataLoader(test_data,  batch_size=32, shuffle=False, num_workers=2)
# shuffle=True  → 训练集打乱
# shuffle=False → 测试集不打乱（保持可复现的评估）
# num_workers=2 → 多进程数据加载（加速 I/O）
```

---

## 🔧 数据变换（Transforms）

### 训练集变换（含数据增强）

```python
train_transform = transforms.Compose([
    transforms.Resize((128, 128)),          # 统一尺寸
    transforms.RandomHorizontalFlip(),      # 随机水平翻转（概率 0.5）
    transforms.RandomRotation(15),          # 随机旋转 ±15 度
    transforms.ToTensor(),                  # PIL Image → Tensor [0,1]
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],         # ImageNet RGB 均值
        std=[0.229, 0.224, 0.225]           # ImageNet RGB 标准差
    ),
])
```

### 测试集变换（无增强）

```python
test_transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
# ⚠️ 没有 RandomHorizontalFlip 和 RandomRotation
```

---

## 🔧 CNN 模型定义（Model Definition）

### SimpleCNN 完整实现

```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 卷积块：Conv2d + MaxPool（在 forward 中应用 ReLU）
        self.conv1 = nn.Conv2d(in_channels=3,   out_channels=32,  kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32,  out_channels=64,  kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=64,  out_channels=128, kernel_size=3, padding=1)
        self.pool  = nn.MaxPool2d(kernel_size=2, stride=2)  # 每次将尺寸减半
        # 全连接块
        self.fc1     = nn.Linear(128 * 16 * 16, 256)  # Flatten 后的尺寸: 128×16×16=32768
        self.dropout = nn.Dropout(p=0.5)               # 训练时随机丢弃 50%
        self.fc2     = nn.Linear(256, 2)               # 2 输出: Cat / Dog

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # (B, 3, 128, 128) → (B, 32, 64, 64)
        x = self.pool(F.relu(self.conv2(x)))  # (B, 32, 64, 64) → (B, 64, 32, 32)
        x = self.pool(F.relu(self.conv3(x)))  # (B, 64, 32, 32) → (B, 128, 16, 16)
        x = x.view(x.size(0), -1)             # Flatten: (B, 128, 16, 16) → (B, 32768)
        x = F.relu(self.fc1(x))               # (B, 32768) → (B, 256)
        x = self.dropout(x)                    # Dropout
        x = self.fc2(x)                        # (B, 256) → (B, 2)  ← 原始 logits
        return x                               # ⚠️ 返回 logits，不经过 softmax

def define_model():
    model = SimpleCNN().to(DEVICE)
    return model
```

### 关键 API 说明

```python
# 卷积层
nn.Conv2d(in_channels, out_channels, kernel_size, padding=0, stride=1, bias=True)

# 池化层
nn.MaxPool2d(kernel_size, stride=None)  # stride 默认等于 kernel_size

# 全连接层
nn.Linear(in_features, out_features, bias=True)

# Dropout
nn.Dropout(p=0.5)   # p = 丢弃概率

# 激活函数（functional API）
F.relu(x)           # 无参数版本，常用于 forward() 中
```

---

## 🔧 训练循环（Training Loop）

```python
def train_model(model, train_loader, test_loader, epochs=10):
    criterion = nn.CrossEntropyLoss()                   # 损失函数（含 Softmax）
    optimizer = optim.Adam(model.parameters(), lr=1e-3) # Adam 优化器
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, epochs + 1):
        # ── 训练阶段 ─────────────────────────────────────────────────────────
        model.train()  # 开启 Dropout / BatchNorm 训练模式
        train_loss, correct, total = 0.0, 0, 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)

            optimizer.zero_grad()          # 清零梯度（必须！否则梯度累积）
            out  = model(imgs)             # 前向传播 → logits (B, 2)
            loss = criterion(out, labels)  # 计算损失
            loss.backward()               # 反向传播，计算梯度
            optimizer.step()              # 更新参数

            train_loss += loss.item() * imgs.size(0)
            correct    += (out.argmax(1) == labels).sum().item()
            total      += labels.size(0)

        train_loss /= total
        train_acc   = correct / total

        # ── 验证阶段 ─────────────────────────────────────────────────────────
        model.eval()  # 关闭 Dropout，使用 BatchNorm 的移动平均
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():  # 禁用梯度计算（节省显存，加速推理）
            for imgs, labels in test_loader:
                imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
                out = model(imgs)
                val_loss    += criterion(out, labels).item() * imgs.size(0)
                val_correct += (out.argmax(1) == labels).sum().item()
                val_total   += labels.size(0)

        val_loss /= val_total
        val_acc   = val_correct / val_total

        # 记录并打印
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        print(f"Epoch [{epoch:02d}/{epochs}]  train_loss={train_loss:.4f}  "
              f"train_acc={train_acc:.4f}  val_loss={val_loss:.4f}  val_acc={val_acc:.4f}")

    return history
```

---

## 🔧 模型评估（Model Evaluation）

```python
def evaluate_and_predict(model, test_loader):
    model.eval()
    predictions, actual_labels = [], []

    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs  = imgs.to(DEVICE)
            preds = model(imgs).argmax(dim=1)          # 取概率最大的类别索引
            predictions.extend(preds.cpu().tolist())   # GPU tensor → Python list
            actual_labels.extend(labels.tolist())

    accuracy = sum(p == a for p, a in zip(predictions, actual_labels)) / len(actual_labels)
    print(f"Accuracy: {accuracy:.4f}")

    # sklearn 分类报告：precision / recall / f1 per class
    print(classification_report(actual_labels, predictions, target_names=['Cat', 'Dog']))

    return accuracy, predictions, actual_labels
```

---

## 🔧 完整流程调用（Full Pipeline）

```python
# 1. 准备数据
train_loader, test_loader = load_dataset(str(DATASET_PATH))

# 2. 初始化模型
model = define_model()   # SimpleCNN().to(DEVICE)

# 3. 训练
history = train_model(model, train_loader, test_loader, epochs=10)

# 4. 评估
accuracy, predictions, actual_labels = evaluate_and_predict(model, test_loader)

# 5. （可选）保存模型
torch.save(model.state_dict(), "simple_cnn.pth")

# 5. （可选）加载模型
loaded_model = define_model()
loaded_model.load_state_dict(torch.load("simple_cnn.pth"))
loaded_model.eval()
```

---

## 🔧 常用独立代码片段（Snippets）

### 查看参数量

```python
total_params = sum(p.numel() for p in model.parameters())
trainable    = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Total params: {total_params:,}")      # 8,482,882
print(f"Trainable:    {trainable:,}")
```

### 可视化训练曲线

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(history["train_loss"], label="Train")
ax1.plot(history["val_loss"],   label="Val")
ax1.set_title("Loss"); ax1.legend()

ax2.plot(history["train_acc"], label="Train")
ax2.plot(history["val_acc"],   label="Val")
ax2.set_title("Accuracy"); ax2.legend()
plt.tight_layout(); plt.show()
```

### 检查单张预测

```python
import torchvision.transforms as T
from PIL import Image

def predict_single(model, image_path):
    transform = T.Compose([
        T.Resize((128, 128)),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    img = Image.open(image_path).convert("RGB")
    x = transform(img).unsqueeze(0).to(DEVICE)   # (1, 3, 128, 128)
    model.eval()
    with torch.no_grad():
        logits = model(x)                          # (1, 2)
        probs  = torch.softmax(logits, dim=1)      # ← 手动加 softmax 获取概率
        pred   = logits.argmax(1).item()
    labels = ["Cat", "Dog"]
    print(f"Prediction: {labels[pred]}  (Cat: {probs[0,0]:.3f}, Dog: {probs[0,1]:.3f})")
```

### 损坏图片清理

```python
from pathlib import Path
from PIL import Image

def remove_corrupted(root_dir):
    removed = 0
    for img_path in Path(root_dir).rglob("*.jpg"):
        try:
            with Image.open(img_path) as img:
                img.verify()
        except Exception:
            img_path.unlink()
            removed += 1
    print(f"Removed {removed} corrupted images.")
```
