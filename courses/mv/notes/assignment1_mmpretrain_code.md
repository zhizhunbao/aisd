# Assignment 1 代码参考 — Code Quick Reference

> **See also:** [概念速查](assignment1_mmpretrain_cheatsheet.md) | [数学公式](assignment1_mmpretrain_math.md)  
> **来源:** CST8508 Assignment 1 代码实践

---

## ⚙️ 环境安装

```bash
# 创建 conda 环境
conda create -n openmmlab python=3.8 -y
conda activate openmmlab

# 安装 PyTorch + CUDA（conda 自动处理兼容性）
conda install pytorch torchvision pytorch-cuda=12.1 -c pytorch -c nvidia

# 安装 OpenMMLab 工具
pip install openmim
mim install mmengine mmcv mmpretrain

# 验证安装
python -c "import mmpretrain; print(mmpretrain.__version__)"
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 📂 数据集准备 (SubFolder 格式)

```python
import os
import shutil
import json

DATA_ROOT = "data/flowers17"
CATEGORIES = [
    "Bluebell", "Buttercup", "Coltsfoot", "Cowslip",
    "Crocus", "Daffodil", "Daisy", "Dandelion",
    "Fritillary", "Iris", "LilyValley", "Pansy",
    "Snowdrop", "Sunflower", "TigerLily", "Tulip", "Windflower"
]

# 创建 SubFolder 目录结构
for split in ["train", "val"]:
    for cat in CATEGORIES:
        os.makedirs(os.path.join(DATA_ROOT, split, cat), exist_ok=True)

# 从 JSON 分割文件移动图片
with open("train_set.json") as f:
    train_files = json.load(f)
for cat, files in train_files.items():
    for fname in files:
        src = os.path.join("jpg", fname)
        dst = os.path.join(DATA_ROOT, "train", cat, fname)
        shutil.copy2(src, dst)

# 验证结构
for split in ["train", "val"]:
    for cat in CATEGORIES:
        n = len(os.listdir(os.path.join(DATA_ROOT, split, cat)))
        print(f"  {split}/{cat}: {n} images")
```

---

## 📝 配置文件模板 (ResNet-18)

```python
# configs/resnet18_flowers17.py

# ① 继承基础配置
_base_ = [
    'mmpretrain::_base_/models/resnet18.py',
    'mmpretrain::_base_/default_runtime.py',
]

# ② 模型：修改分类头
model = dict(
    head=dict(
        num_classes=17,      # ← 改为你的类别数
        in_channels=512,     # ResNet-18 输出 512 维
    ),
)

# ③ 数据预处理（ImageNet 标准）
data_preprocessor = dict(
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
)

# ④ 数据增强管道
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='RandomResizedCrop', scale=224),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(type='PackInputs'),
]

val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='ResizeEdge', scale=256, edge='short'),
    dict(type='CenterCrop', crop_size=224),
    dict(type='PackInputs'),
]

# ⑤ 数据加载器
train_dataloader = dict(
    batch_size=32, num_workers=4,
    dataset=dict(type='CustomDataset',
                 data_prefix='data/flowers17/train',
                 pipeline=train_pipeline),
)
val_dataloader = dict(
    batch_size=32, num_workers=4,
    dataset=dict(type='CustomDataset',
                 data_prefix='data/flowers17/val',
                 pipeline=val_pipeline),
)

# ⑥ 优化器
optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0001),
)

# ⑦ 学习率调度
param_scheduler = dict(type='CosineAnnealingLR', T_max=100)

# ⑧ 训练策略
train_cfg = dict(by_epoch=True, max_epochs=100, val_interval=10)

# ⑨ 评估
val_evaluator = dict(type='Accuracy', topk=(1, 5))

# ⑩ 必须添加（推理器需要）
test_dataloader = val_dataloader
test_evaluator = val_evaluator
```

---

## 🔀 配置文件改模型 (MobileNet V2)

```python
# configs/mobilenetv2_flowers17.py
# 只需改动的部分（对比 ResNet-18）：

_base_ = [
    'mmpretrain::_base_/models/mobilenet_v2_1x.py',  # ← 改基础模型
    'mmpretrain::_base_/default_runtime.py',
]

model = dict(
    head=dict(
        num_classes=17,
        in_channels=1280,     # ← MobileNet V2 输出 1280 维
    ),
)

optim_wrapper = dict(
    optimizer=dict(type='Adam', lr=0.001),  # ← 改优化器
)
```

---

## ▶️ 训练命令

```bash
# 训练 ResNet-18
python -m mmpretrain.tools.train configs/resnet18_flowers17.py

# 训练 MobileNet V2
python -m mmpretrain.tools.train configs/mobilenetv2_flowers17.py

# 指定 GPU
CUDA_VISIBLE_DEVICES=0 python -m mmpretrain.tools.train configs/resnet18_flowers17.py
```

---

## 🔍 模型推理与评估

```python
from mmpretrain import ImageClassificationInferencer

# 初始化推理器
inferencer = ImageClassificationInferencer(
    model='configs/resnet18_flowers17.py',
    pretrained='work_dirs/resnet18_flowers17/epoch_90.pth'
)

# 对单张图片推理
result = inferencer('path/to/image.jpg')[0]
print(f"类别: {result['pred_label']}")
print(f"置信度: {result['pred_score']:.4f}")
print(f"类名: {result['pred_class']}")

# 批量评估验证集
from sklearn.metrics import classification_report, confusion_matrix
import os

val_dir = "data/flowers17/val"
categories = sorted(os.listdir(val_dir))
all_preds, all_labels = [], []

for cat_idx, cat_name in enumerate(categories):
    cat_dir = os.path.join(val_dir, cat_name)
    for img in os.listdir(cat_dir):
        result = inferencer(os.path.join(cat_dir, img))[0]
        all_preds.append(result['pred_label'])
        all_labels.append(cat_idx)

# 生成分类报告
print(classification_report(all_labels, all_preds, target_names=categories))
```

---

## 📊 可视化：混淆矩阵

```python
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=categories, yticklabels=categories)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150)
plt.show()
```

---

## ⚠️ 常见问题速查

| 问题                           | 解决方案                                           |
| ------------------------------ | -------------------------------------------------- |
| `No module named 'mmpretrain'` | `mim install mmpretrain` 或检查 conda 环境是否激活 |
| `KeyError: test_dataloader`    | 配置文件末尾加 `test_dataloader = val_dataloader`  |
| NumPy segfault                 | 用 conda 安装 PyTorch（而非 pip），避免 NumPy 2.x  |
| CUDA out of memory             | 减小 `batch_size`（32 → 16 → 8）                   |
| 训练不收敛                     | 检查学习率是否太大；确认数据增强管道               |
