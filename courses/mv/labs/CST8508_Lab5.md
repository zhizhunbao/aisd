# CST8508 Machine Vision — Lab 5: Cats vs Dogs Image Classification — 猫狗图像分类

> **Course — 课程:** CST8508 Machine Vision  
> **Lab — 实验:** Lab 5  
> **Topic — 主题:** End-to-End CNN Image Classification — 端到端卷积神经网络图像分类  
> **Framework — 框架:** PyTorch  
> **Dataset — 数据集:** [Microsoft Cats vs Dogs](https://www.microsoft.com/en-us/download/details.aspx?id=54765)  
> 📋 输出解读 → [lab5_output_guide.md](../notes/lab5_output_guide.md)

---

## Objective — 实验目标

Implement an end-to-end Convolutional Neural Network (CNN) to classify images from the Cats vs. Dogs dataset. — 实现一个端到端的卷积神经网络（CNN），对猫狗数据集中的图像进行分类。

> **Note:** Do not forget to change the runtime type of your notebook to GPU so you can train on a GPU. — 注意：不要忘记将 Notebook 的运行时类型切换为 GPU，以便使用 GPU 训练。

---

## Lab Instructions — 实验说明

- Implement each function in a modular fashion. — 以模块化方式实现每个函数。
- Ensure functions interact with each other seamlessly. — 确保各函数之间无缝协作。
- Document each step with comments for clarity. — 为每个步骤添加注释以保持清晰。
- After implementing all parts, run the entire pipeline on the Cats vs. Dogs dataset and analyze the results. — 实现所有部分后，在猫狗数据集上运行完整流程并分析结果。

This lab will provide a comprehensive understanding of building and training a CNN for image classification, from data preprocessing to model evaluation. — 本实验将提供从数据预处理到模型评估的完整 CNN 图像分类构建与训练体验。

---

## Dataset Setup — 数据集准备

```python
# ── Dataset Setup ────────────────────────────────────────────────────────
# 自动下载并解压 Microsoft Cats vs Dogs 数据集，同时清除损坏图片
# Auto-download Microsoft Cats vs Dogs dataset and remove corrupted images

import os, zipfile, urllib.request
from pathlib import Path
from PIL import Image

DATASET_URL  = "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip"
ZIP_PATH     = Path("kagglecatsanddogs_5340.zip")
DATASET_PATH = Path("PetImages")   # ← load_dataset 使用此路径

# 1. 下载 / Download (~786 MB)
if not ZIP_PATH.exists() and not DATASET_PATH.exists():
    print("Downloading dataset (~786 MB) ...")
    urllib.request.urlretrieve(DATASET_URL, ZIP_PATH)
    print("Download complete.")
else:
    print("Zip / dataset already present, skipping download.")

# 2. 解压 / Extract
if not DATASET_PATH.exists():
    print("Extracting ...")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(".")
    print("Extraction complete.")

# 3. 清理损坏图片（此数据集存在部分无效 JPEG）
# Remove corrupted images (known issue with this dataset)
removed = 0
for img_path in DATASET_PATH.rglob("*.jpg"):
    try:
        with Image.open(img_path) as img:
            img.verify()
    except Exception:
        img_path.unlink()
        removed += 1
print(f"Removed {removed} corrupted images.")
print(f"Dataset ready at: {DATASET_PATH.resolve()}")
```

---

## Part 1: Data Loading and Augmentation — 第一部分：数据加载与增强

**Function `load_dataset(path)`** — 函数说明

Load the Cats vs. Dogs dataset from the given path. Split into training and test sets. Define transforms for augmentation and normalization. — 从给定路径加载猫狗数据集，划分训练集和测试集，定义数据增强与归一化变换。

| Parameter — 参数 | Description — 描述 |
|---|---|
| `path` | Path to the `PetImages/` directory — `PetImages/` 目录路径 |
| `split_ratio` | Fraction of data used for training (default 0.8) — 训练集比例（默认 0.8） |

**Returns — 返回值:** `train_loader, test_loader` — PyTorch DataLoader objects for train/test splits — 训练集和测试集的 DataLoader 对象

```python
import os, random
import torch
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

random.seed(42)
torch.manual_seed(42)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

def load_dataset(path, split_ratio=0.8):
    # Load images from path
    train_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    test_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    # Split into training and test sets
    full = datasets.ImageFolder(root=path, transform=train_transform)
    n = len(full)
    train_n = int(n * split_ratio)
    idx = list(range(n))
    random.shuffle(idx)
    train_data = Subset(full, idx[:train_n])
    test_data  = Subset(datasets.ImageFolder(root=path, transform=test_transform), idx[train_n:])

    # Normalize pixel values (handled inside transforms above)
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True,  num_workers=2)
    test_loader  = DataLoader(test_data,  batch_size=32, shuffle=False, num_workers=2)
    print(f"Train: {train_n}  Test: {n - train_n}  Classes: {full.classes}")
    return train_loader, test_loader
```

**Key transforms — 关键变换：**

| Transform — 变换 | Applied to — 应用于 | Purpose — 目的 |
|---|---|---|
| `Resize((128, 128))` | Train + Test | Standardize input size — 统一输入尺寸 |
| `RandomHorizontalFlip()` | Train only | Data augmentation — 数据增强（水平翻转） |
| `RandomRotation(15)` | Train only | Data augmentation — 数据增强（随机旋转 ±15°） |
| `ToTensor()` | Train + Test | Convert PIL Image to tensor [0,1] — 转为张量 |
| `Normalize([0.485, 0.456, 0.406], ...)` | Train + Test | ImageNet mean/std normalization — ImageNet 均值/标准差标准化 |

---

## Part 2: Model Definition — 第二部分：模型定义

**Function `define_model()`** — 函数说明

Define a CNN model with layers (Conv2D, MaxPooling, Flatten, Dense). Include activation functions and the optimizer. — 定义包含卷积层、池化层、全连接层的 CNN 模型，包括激活函数。

**Model Architecture — 模型架构：`SimpleCNN`**

```
Input (3 × 128 × 128)
    ↓ Conv2d(3→32, k=3) + ReLU + MaxPool2d(2) → (32 × 64 × 64)
    ↓ Conv2d(32→64, k=3) + ReLU + MaxPool2d(2) → (64 × 32 × 32)
    ↓ Conv2d(64→128, k=3) + ReLU + MaxPool2d(2) → (128 × 16 × 16)
    ↓ Flatten → (32768,)
    ↓ Linear(32768→256) + ReLU + Dropout(0.5)
    ↓ Linear(256→2)
Output: logits for [Cat, Dog]
```

```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # Conv2D → MaxPooling blocks
        self.conv1 = nn.Conv2d(3,  32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool  = nn.MaxPool2d(2, 2)
        # Dense layers after Flatten
        self.fc1     = nn.Linear(128 * 16 * 16, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2     = nn.Linear(256, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))   # 128→64
        x = self.pool(F.relu(self.conv2(x)))   # 64→32
        x = self.pool(F.relu(self.conv3(x)))   # 32→16
        x = x.view(x.size(0), -1)              # Flatten
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

def define_model():
    model = SimpleCNN().to(DEVICE)
    return model
```

**Layer summary — 层参数说明：**

| Layer — 层 | Output Shape — 输出形状 | Parameters — 参数量 |
|---|---|---|
| `Conv2d(3, 32, 3, padding=1)` | 32 × 128 × 128 | 3×3×3×32 + 32 = **896** |
| `MaxPool2d(2)` | 32 × 64 × 64 | 0 |
| `Conv2d(32, 64, 3, padding=1)` | 64 × 64 × 64 | 3×3×32×64 + 64 = **18,496** |
| `MaxPool2d(2)` | 64 × 32 × 32 | 0 |
| `Conv2d(64, 128, 3, padding=1)` | 128 × 32 × 32 | 3×3×64×128 + 128 = **73,856** |
| `MaxPool2d(2)` | 128 × 16 × 16 | 0 |
| `Flatten` | 32,768 | 0 |
| `Linear(32768, 256)` | 256 | 32768×256 + 256 = **8,389,120** |
| `Dropout(0.5)` | 256 | 0 |
| `Linear(256, 2)` | 2 | 256×2 + 2 = **514** |
| **Total — 总计** | | **≈ 8.48M parameters** |

---

## Part 3: Model Training — 第三部分：模型训练

**Function `train_model(model, train_loader, test_loader, epochs=10)`** — 函数说明

Train the model using the training set with validation data. Set epochs and batch size. — 使用训练集和验证数据训练模型，设置训练轮次和批次大小。

**Returns — 返回值:** `history` — Dictionary containing per-epoch metrics — 包含每轮次指标的字典（`train_loss`, `train_acc`, `val_loss`, `val_acc`）

```python
import torch.optim as optim

def train_model(model, train_loader, test_loader, epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    # Train the model using fit()
    for epoch in range(1, epochs + 1):
        # Set epochs, batch size
        model.train()
        train_loss, correct, total = 0.0, 0, 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            out = model(imgs)
            loss = criterion(out, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * imgs.size(0)
            correct += (out.argmax(1) == labels).sum().item()
            total += labels.size(0)
        train_loss /= total
        train_acc = correct / total

        # Use validation data
        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        with torch.no_grad():
            for imgs, labels in test_loader:
                imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
                out = model(imgs)
                val_loss += criterion(out, labels).item() * imgs.size(0)
                val_correct += (out.argmax(1) == labels).sum().item()
                val_total += labels.size(0)
        val_loss /= val_total
        val_acc = val_correct / val_total

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        print(f"Epoch [{epoch:02d}/{epochs}]  train_loss={train_loss:.4f}  train_acc={train_acc:.4f}  val_loss={val_loss:.4f}  val_acc={val_acc:.4f}")

    return history
```

**Training configuration — 训练配置：**

| Setting — 设置 | Value — 值 | Description — 说明 |
|---|---|---|
| Optimizer — 优化器 | `Adam(lr=1e-3)` | Adaptive moment estimation — 自适应矩估计 |
| Loss function — 损失函数 | `CrossEntropyLoss` | Multi-class classification loss — 多类分类损失 |
| Epochs — 训练轮次 | 10 | Number of full passes through training data — 完整遍历训练数据的次数 |
| Batch size — 批次大小 | 32 | Samples per gradient update — 每次梯度更新的样本数 |

---

## Part 4: Model Evaluation — 第四部分：模型评估

**Function `evaluate_and_predict(model, test_loader)`** — 函数说明

Evaluate the model's performance on the test dataset. Return accuracy. — 评估模型在测试集上的性能，返回准确率。

**Returns — 返回值:** `accuracy, predictions, actual_labels` — Accuracy scalar and per-sample prediction/ground-truth lists — 准确率标量以及每个样本的预测结果和真实标签列表

```python
def evaluate_and_predict(model, test_loader):
    model.eval()
    predictions, actual_labels = [], []

    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs = imgs.to(DEVICE)
            preds = model(imgs).argmax(1)
            predictions.extend(preds.cpu().tolist())
            actual_labels.extend(labels.tolist())

    accuracy = sum(p == a for p, a in zip(predictions, actual_labels)) / len(actual_labels)
    print(f"Accuracy: {accuracy:.4f}")

    from sklearn.metrics import classification_report
    print(classification_report(actual_labels, predictions, target_names=['Cat', 'Dog']))

    return accuracy, predictions, actual_labels
```

**Output metrics — 输出指标：**

| Metric — 指标 | Description — 描述 |
|---|---|
| Accuracy — 准确率 | Overall fraction of correct predictions — 整体正确预测比例 |
| Precision — 精确率 | TP / (TP + FP) — 预测为正类中实际正确的比例 |
| Recall — 召回率 | TP / (TP + FN) — 实际正类中被正确预测的比例 |
| F1-Score | Harmonic mean of precision and recall — 精确率与召回率的调和平均 |
| Support — 支持数 | Number of test samples per class — 每个类别的测试样本数 |

> 📋 Want to understand what the numbers mean? → [lab5_output_guide.md](../notes/lab5_output_guide.md)

---

## Running the Code — 运行完整流程

```python
train_loader, test_loader = load_dataset(str(DATASET_PATH))
model = define_model()
train_model(model, train_loader, test_loader, epochs=10)
accuracy, predictions, actual_labels = evaluate_and_predict(model, test_loader)
```

**Expected output — 预期输出：**

```
Using device: cuda
Train: 19998  Test: 5000  Classes: ['Cat', 'Dog']
Epoch [01/10]  train_loss=0.6392  train_acc=0.6245  val_loss=0.5441  val_acc=0.7272
Epoch [02/10]  train_loss=0.5251  train_acc=0.7399  val_loss=0.4814  val_acc=0.7734
...
Epoch [10/10]  train_loss=0.2863  train_acc=0.8809  val_loss=0.2727  val_acc=0.8842
Accuracy: 0.8842
              precision    recall  f1-score   support

         Cat       0.90      0.86      0.88      2478
         Dog       0.87      0.91      0.89      2522

    accuracy                           0.88      5000
   macro avg       0.89      0.88      0.88      5000
weighted avg       0.88      0.88      0.88      5000
```

> 📋 输出解读 → [lab5_output_guide.md](../notes/lab5_output_guide.md)
