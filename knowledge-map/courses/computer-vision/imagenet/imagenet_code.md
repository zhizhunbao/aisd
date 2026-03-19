---
topic: imagenet
dimension: code
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Docs: PyTorch torchvision.models — https://pytorch.org/vision/stable/models.html"
  - "📖 Docs: PyTorch torchvision.datasets — https://pytorch.org/vision/stable/datasets.html"
  - "📖 Docs: PyTorch torchvision.transforms — https://pytorch.org/vision/stable/transforms.html"
  - "💻 Source: torchvision models — https://github.com/pytorch/vision/blob/main/torchvision/models/resnet.py"
expiry: 6m
status: current
---

# ImageNet 代码参考

> 📖 Docs: [PyTorch torchvision.models](https://pytorch.org/vision/stable/models.html)
> 📖 Docs: [PyTorch torchvision.transforms](https://pytorch.org/vision/stable/transforms.html)

## 快速开始

### 最简示例 — 30 秒上手（用预训练模型推理）

```python
import torch
from torchvision import models, transforms
from PIL import Image
import urllib.request
import json

# ============================================================
# 1. 加载预训练模型 / Load pre-trained model
# ============================================================
# ResNet-50 在 ImageNet-1K 上预训练，Top-1: 76.1%, Top-5: 92.9%
# ResNet-50 pre-trained on ImageNet-1K, Top-1: 76.1%, Top-5: 92.9%
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
model.eval()  # 切换到推理模式 / Switch to inference mode

# ============================================================
# 2. 定义 ImageNet 标准预处理 / Define standard preprocessing
# ============================================================
# 所有 ImageNet 预训练模型必须用这组变换
# All ImageNet pre-trained models MUST use these transforms
preprocess = transforms.Compose([
    transforms.Resize(256),          # 短边缩放到256 / Resize short edge to 256
    transforms.CenterCrop(224),      # 中心裁剪224×224 / Center crop to 224×224
    transforms.ToTensor(),           # PIL→Tensor, 值域[0,1] / PIL→Tensor, range [0,1]
    transforms.Normalize(            # ImageNet 归一化统计值 / ImageNet normalization
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

# ============================================================
# 3. 加载并预处理图像 / Load and preprocess image
# ============================================================
# 下载测试图像 / Download test image
url = "https://upload.wikimedia.org/wikipedia/commons/2/26/YellowLabradorLooking_new.jpg"
urllib.request.urlretrieve(url, "test_dog.jpg")
img = Image.open("test_dog.jpg").convert("RGB")
input_tensor = preprocess(img).unsqueeze(0)  # 添加 batch 维度 / Add batch dimension

# ============================================================
# 4. 推理得到 Top-5 预测 / Inference and get Top-5 predictions
# ============================================================
with torch.no_grad():
    output = model(input_tensor)                      # logits [1, 1000]
    probabilities = torch.nn.functional.softmax(output[0], dim=0)  # softmax → 概率

# 获取 Top-5 / Get Top-5
top5_prob, top5_idx = torch.topk(probabilities, 5)

# ImageNet 类别名 / ImageNet class names
IMAGENET_CLASSES_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
urllib.request.urlretrieve(IMAGENET_CLASSES_URL, "imagenet_classes.txt")
with open("imagenet_classes.txt") as f:
    categories = [s.strip() for s in f.readlines()]

print("Top-5 预测 / Top-5 Predictions:")
for i in range(5):
    print(f"  {i+1}. {categories[top5_idx[i]]:30s} ({top5_prob[i]:.4f})")
```

**测试方法：** 安装 `pip install torch torchvision Pillow`，运行脚本应输出 "Labrador retriever" 为 Top-1。

> 📖 Docs: [PyTorch torchvision.models](https://pytorch.org/vision/stable/models.html)

---

## 完整实现示例

### 示例 1: 在自定义数据集上微调 ImageNet 预训练模型

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import models, transforms, datasets

# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
# ImageNet 标准变换 (训练时加数据增强)
# Standard ImageNet transforms (with augmentation for training)
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),     # 随机裁剪+缩放 / Random crop & resize
    transforms.RandomHorizontalFlip(),     # 随机水平翻转 / Random horizontal flip
    transforms.ColorJitter(0.4, 0.4, 0.4), # 色彩抖动 / Color jitter
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# 假设自定义数据集在 data/ 下按类别分文件夹
# Assume custom dataset organized in folders by class
train_dataset = datasets.ImageFolder("data/train", transform=train_transform)
val_dataset = datasets.ImageFolder("data/val", transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)

num_classes = len(train_dataset.classes)
print(f"类别数 / Number of classes: {num_classes}")

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
# 加载 ImageNet 预训练 ResNet-50
# Load ImageNet pre-trained ResNet-50
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

# 替换最后的全连接层 (原来是 1000 类 → 改为 num_classes 类)
# Replace final FC layer (orig 1000 classes → num_classes)
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 可选: 冻结底层 (只训练高层 + 新FC)
# Optional: Freeze lower layers (only train top layers + new FC)
for name, param in model.named_parameters():
    if "layer4" not in name and "fc" not in name:
        param.requires_grad = False  # 冻结 / Freeze

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# ============================================================
# 3. 训练设置 / Training Setup
# ============================================================
criterion = nn.CrossEntropyLoss()  # 交叉熵损失 / Cross-entropy loss
# 只优化未冻结的参数 / Only optimize unfrozen parameters
optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()),
                       lr=1e-4, weight_decay=1e-4)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

# ============================================================
# 4. 训练循环 / Training Loop
# ============================================================
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)        # logits [B, num_classes]
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)  # Top-1 预测 / Top-1 prediction
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    scheduler.step()
    train_acc = 100 * correct / total
    print(f"Epoch [{epoch+1}/{num_epochs}] Loss: {running_loss/len(train_loader):.4f} "
          f"Train Acc: {train_acc:.2f}%")

    # ============================================================
    # 5. 验证 / Validation
    # ============================================================
    model.eval()
    val_correct = 0
    val_total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    val_acc = 100 * val_correct / val_total
    print(f"  Val Acc: {val_acc:.2f}%")
```

> 📖 Docs: [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

### 示例 2: 提取 ImageNet 预训练特征（Feature Extraction）

```python
import torch
from torchvision import models, transforms
from PIL import Image

# ============================================================
# 1. 加载无分类头的预训练模型 / Load pre-trained model without classifier
# ============================================================
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
# 去掉最后的 avgpool + fc, 只保留特征提取部分
# Remove avgpool + fc, keep only feature extraction
feature_extractor = torch.nn.Sequential(*list(model.children())[:-2])
feature_extractor.eval()

# ============================================================
# 2. 预处理 / Preprocessing
# ============================================================
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

img = Image.open("test_image.jpg").convert("RGB")
input_tensor = preprocess(img).unsqueeze(0)

# ============================================================
# 3. 提取特征图 / Extract feature maps
# ============================================================
with torch.no_grad():
    features = feature_extractor(input_tensor)  # [1, 2048, 7, 7]

print(f"特征维度 / Feature shape: {features.shape}")
# 全局平均池化得到特征向量 / Global average pooling → feature vector
feature_vector = features.mean(dim=[2, 3])  # [1, 2048]
print(f"特征向量 / Feature vector: {feature_vector.shape}")
```

---

## API 速查

### torchvision.models

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `models.resnet50()` | `weights` | `None` | ResNet-50 模型 |
| ↳ `weights` | `ResNet50_Weights` | `None` | `IMAGENET1K_V1`(旧) / `IMAGENET1K_V2`(新, 推荐) |
| `models.resnet101()` | `weights` | `None` | ResNet-101 模型 |
| `models.vgg16()` | `weights` | `None` | VGG-16 模型 |
| `models.mobilenet_v3_large()` | `weights` | `None` | 轻量级模型 |
| `models.vit_b_16()` | `weights` | `None` | Vision Transformer |

### torchvision.transforms

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `Resize(size)` | `size` | — | 短边缩放到 size |
| `CenterCrop(size)` | `size` | — | 中心裁剪 |
| `RandomResizedCrop(size)` | `size` | — | 随机裁剪+缩放 (训练用) |
| ↳ `scale` | `tuple` | `(0.08, 1.0)` | 裁剪面积比例范围 |
| `RandomHorizontalFlip()` | `p` | `0.5` | 随机水平翻转概率 |
| `Normalize(mean, std)` | `mean, std` | — | ImageNet: `[0.485,0.456,0.406]`, `[0.229,0.224,0.225]` |
| `ToTensor()` | — | — | PIL Image → Tensor, 范围 [0, 1] |

### ImageNet 标签工具

| 工具 | 用途 | 说明 |
|------|------|------|
| `torchvision.models.ResNet50_Weights.IMAGENET1K_V2.meta["categories"]` | 获取 1000 类名 | PyTorch 内置 |
| `imagenet_classes.txt` | 类别名文本文件 | 从 PyTorch Hub 下载 |
| 类别索引 0-999 | synset 到数字映射 | 按字母序排列的 synset ID |

> 📖 Docs: [torchvision.models](https://pytorch.org/vision/stable/models.html)

---

## 目录结构模板

### 简单结构

```
project/
├── inference.py          ← 用预训练模型推理
├── test_image.jpg        ← 测试图片
└── imagenet_classes.txt  ← 类别名映射
```

### 标准结构

```
project/
├── config.py             ← 超参数配置
├── dataset.py            ← 数据加载 + ImageNet 变换
├── model.py              ← 模型定义 (加载预训练 + 替换FC)
├── train.py              ← 微调训练循环
├── evaluate.py           ← 计算 Top-1/Top-5 准确率
├── utils.py              ← 辅助函数
├── data/
│   ├── train/            ← 按类别分文件夹
│   │   ├── class_0/
│   │   └── class_1/
│   └── val/
├── checkpoints/          ← 模型权重
└── logs/                 ← TensorBoard 日志
```
