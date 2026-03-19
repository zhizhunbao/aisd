---
topic: transfer_learning
dimension: code
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Docs: PyTorch Transfer Learning Tutorial — https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html"
  - "📖 Docs: TensorFlow Hub — https://www.tensorflow.org/hub"
  - "📖 Docs: Hugging Face Transformers — https://huggingface.co/docs/transformers/"
  - "📖 Paper: Howard & Ruder, 'ULMFiT', ACL 2018 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/transfer_learning/howard_2018_ulmfit.pdf"
expiry: 6m
status: current
---

# Transfer Learning 代码参考

> 📖 Docs: [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
> 📖 Docs: [Hugging Face Transformers](https://huggingface.co/docs/transformers/)

## 快速开始

### 最简示例 — 30 秒上手 PyTorch Fine-tuning

```python
import torch
import torchvision.models as models
import torch.nn as nn

# 1. 加载预训练 ResNet-18 / Load pre-trained ResNet-18
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# 2. 冻结所有层 / Freeze all layers
for param in model.parameters():
    param.requires_grad = False

# 3. 替换分类头（ImageNet 1000 类 → 你的 2 类）/ Replace classifier head
model.fc = nn.Linear(model.fc.in_features, 2)

# 4. 只有新分类头的参数会被训练 / Only new head params will be trained
optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)

print(f"可训练参数 / Trainable params: {sum(p.numel() for p in model.parameters() if p.requires_grad)}")
# 预期 / Expected: 1026 (512*2 + 2)
```

**测试方法：** 复制粘贴直接运行，需要 `pip install torch torchvision`

---

## 完整实现示例

### 示例 1: PyTorch Feature Extraction + Fine-tuning 完整流程

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# 数据增强和标准化 / Data augmentation and normalization
# ImageNet 预训练模型要求特定的归一化参数
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],   # ImageNet 均值 / ImageNet mean
                         [0.229, 0.224, 0.225])    # ImageNet 标准差 / ImageNet std
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 假设数据在 data/train/ 和 data/val/ 下按类别文件夹组织
# Assuming data in data/train/ and data/val/ organized by class folder
# train_dataset = datasets.ImageFolder('data/train', train_transform)
# val_dataset   = datasets.ImageFolder('data/val',   val_transform)
# train_loader  = DataLoader(train_dataset, batch_size=32, shuffle=True)
# val_loader    = DataLoader(val_dataset,   batch_size=32, shuffle=False)

# ============================================================
# 2. 模型设置 / Model Setup
# ============================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载预训练 ResNet-50 / Load pre-trained ResNet-50
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

# 策略 A: Feature Extraction — 冻结所有层
for param in model.parameters():
    param.requires_grad = False

# 替换分类头 / Replace classifier head
num_classes = 10  # 你的类别数 / Your number of classes
model.fc = nn.Sequential(
    nn.Dropout(0.5),
    nn.Linear(model.fc.in_features, num_classes)
)
model = model.to(device)

# ============================================================
# 3. 策略 B: Fine-tuning 高层 / Fine-tune top layers
# ============================================================
def unfreeze_top_layers(model, num_layers=2):
    """解冻最后 num_layers 个 ResNet block / Unfreeze last N ResNet blocks"""
    children = list(model.children())
    # ResNet: [conv1, bn1, relu, maxpool, layer1, layer2, layer3, layer4, avgpool, fc]
    for child in children[-(num_layers + 1):]:  # +1 for fc
        for param in child.parameters():
            param.requires_grad = True

# unfreeze_top_layers(model, num_layers=2)  # 解冻 layer3 + layer4

# ============================================================
# 4. 训练 / Training
# ============================================================
criterion = nn.CrossEntropyLoss()
# 注意只优化 requires_grad=True 的参数 / Only optimize trainable params
optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=1e-3,              # Feature Extraction 用较大 lr
    # lr=1e-4,            # Fine-tuning 用较小 lr
    weight_decay=1e-4
)

# 学习率调度 / LR scheduler
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, total = 0, 0, 0
    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * inputs.size(0)
        correct += (outputs.argmax(1) == labels).sum().item()
        total += labels.size(0)
    return total_loss / total, correct / total

# for epoch in range(num_epochs):
#     train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
#     scheduler.step()
#     print(f"Epoch {epoch}: Loss={train_loss:.4f}, Acc={train_acc:.4f}")
```

### 示例 2: Hugging Face BERT Fine-tuning (NLP)

```python
# ============================================================
# 1. 安装 / Install
# ============================================================
# pip install transformers datasets

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import load_dataset

# ============================================================
# 2. 数据加载 / Data Loading
# ============================================================
dataset = load_dataset("imdb")  # 电影评论情感分类 / Movie review sentiment

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=256)

tokenized = dataset.map(tokenize, batched=True)

# ============================================================
# 3. 加载预训练 BERT + 分类头 / Load pre-trained BERT + classifier
# ============================================================
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2  # 正面/负面 / Positive/Negative
)

# ============================================================
# 4. Fine-tuning 配置 / Fine-tuning config
# ============================================================
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    learning_rate=2e-5,        # ⚠️ BERT Fine-tuning 标准学习率 / Standard BERT LR
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    warmup_steps=500,          # 学习率预热 / LR warmup
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"].select(range(5000)),   # 子集演示 / Subset demo
    eval_dataset=tokenized["test"].select(range(1000)),
)

# trainer.train()
# trainer.evaluate()
```

---

## API 速查

### PyTorch 迁移学习

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `models.resnet50(weights=...)` | `weights` | None | `ResNet50_Weights.IMAGENET1K_V2` 加载预训练 |
| `param.requires_grad` | — | True | 设为 False 冻结该层 |
| `nn.Linear(in_features, num_classes)` | — | — | 替换分类头 |
| `optim.Adam(filter(...), lr=...)` | `lr` | 1e-3 | Fine-tune 时用 1e-4 ~ 1e-5 |
| `lr_scheduler.CosineAnnealingLR()` | `T_max` | — | 余弦退火学习率 |

### Hugging Face Transformers

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `AutoModel.from_pretrained()` | `model_name` | — | 加载预训练模型 |
| `AutoModelForSequenceClassification` | `num_labels` | 2 | 自动加分类头 |
| `TrainingArguments` | `learning_rate` | 5e-5 | BERT Fine-tune: 2e-5~5e-5 |
| ↳ | `warmup_steps` | 0 | 预热步数 |
| ↳ | `weight_decay` | 0 | 权重衰减（推荐 0.01） |
| `Trainer` | — | — | 封装训练循环 |
| `model.save_pretrained()` | `dir` | — | 保存 Fine-tuned 模型 |

---

## 目录结构模板

### 标准结构

```
project/
├── config.py             ← 超参数配置 / Hyperparameter config
├── dataset.py            ← 数据加载与预处理 / Data loading & preprocessing
├── model.py              ← 模型定义（加载预训练 + 替换头）/ Model definition
├── train.py              ← 训练脚本 / Training script
├── evaluate.py           ← 评估脚本 / Evaluation script
├── data/
│   ├── train/            ← 按类别文件夹组织 / Organized by class folder
│   └── val/
├── checkpoints/          ← Fine-tuned 模型权重 / Model checkpoints
└── logs/                 ← TensorBoard 日志 / TensorBoard logs
```
