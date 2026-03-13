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
    'mmpretrain::_base_/models/resnet18.py',     # ResNet-18 网络结构定义（backbone/neck/head 默认值）
    'mmpretrain::_base_/default_runtime.py',      # 通用运行时配置（日志后端、随机种子、断点续训等）
    # 好处：不用从零写所有配置，只需覆盖要改的部分
]

# ② 模型：修改分类头
model = dict(
    head=dict(
        num_classes=17,      # Flowers17 有 17 种花，必须与数据集类别数一致
        in_channels=512,     # ResNet-18 最后一层输出 512 通道（由网络架构决定，不能随意改）
                             # 对比: ResNet-50 是 2048, MobileNetV2 是 1280
    ),
)

# ③ 数据预处理（ImageNet 标准）
data_preprocessor = dict(
    # 归一化公式: pixel = (pixel - mean) / std
    # 这组值是 ImageNet 120万张图片统计得到的 RGB 通道均值和标准差
    # 必须用 ImageNet 的值（而非自己数据集的），因为预训练权重是在 ImageNet 上训练的
    # 输入分布不一致会导致特征提取完全错乱
    mean=[123.675, 116.28, 103.53],   # R=123.675, G=116.28, B=103.53
    std=[58.395, 57.12, 57.375],      # R=58.395,  G=57.12,  B=57.375
)

# ④ 数据增强管道
train_pipeline = [
    dict(type='LoadImageFromFile'),                # 从磁盘读取图片（管道必须的起点）
    dict(type='RandomResizedCrop', scale=224),      # 随机裁剪+缩放到 224×224
    # scale=224: ImageNet 标准输入尺寸，ResNet 就是按这个尺寸设计的
    # RandomResizedCrop 是最核心的增强：随机选区域+随机比例裁剪再缩放
    # 模拟不同拍摄距离和构图，极大增加数据多样性（小数据集~60张/类，非常需要）
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    # prob=0.5: 50%概率翻转，平衡增强与原始分布
    # direction='horizontal': 只水平翻转，不垂直翻转（花朵左右对称自然，上下颠倒不自然）
    dict(type='PackInputs'),                       # 打包为模型输入格式（管道必须的终点）
]

val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='ResizeEdge', scale=256, edge='short'),  # 短边缩放到256，长边等比例缩放
    # 保证图片够大，中心裁剪后不丢失太多信息
    dict(type='CenterCrop', crop_size=224),             # 从正中心取 224×224
    # 验证不用 RandomResizedCrop，因为需要确定性结果保证可复现
    dict(type='PackInputs'),
]

# ⑤ 数据加载器
train_dataloader = dict(
    batch_size=32,       # 每批次32张；RTX 4060 8GB显存够用；太大(如128)在小数据集上泛化差
    num_workers=4,       # 4个子进程并行加载数据，加速读取；通常设为CPU核数的一半
    dataset=dict(type='CustomDataset',          # 通用数据集，按文件夹名自动推断标签
                 data_prefix='data/flowers17/train',  # SubFolder格式: train/Bluebell/xxx.jpg
                 pipeline=train_pipeline),
    # 隐含 shuffle=True: 每个epoch打乱顺序，防止模型记住数据出现顺序
)
val_dataloader = dict(
    batch_size=32, num_workers=4,
    dataset=dict(type='CustomDataset',
                 data_prefix='data/flowers17/val',
                 pipeline=val_pipeline),
    # 隐含 shuffle=False: 验证集不打乱，保证结果可复现
)

# ⑥ 优化器
optim_wrapper = dict(
    optimizer=dict(
        type='SGD',              # 随机梯度下降；ResNet论文原始用SGD，CNN在SGD下通常泛化更好
        lr=0.01,                 # 初始学习率；比ImageNet标准(0.1)小10倍
                                 # 因为小数据集lr太大会梯度震荡、无法收敛
        momentum=0.9,            # 动量因子(经典值)；加速梯度一致方向的更新，抑制震荡
        weight_decay=0.0001,     # L2正则化(经典值)；惩罚过大权重，防止过拟合
    ),
)

# ⑦ 学习率调度
param_scheduler = dict(
    type='CosineAnnealingLR',    # 余弦退火：lr按余弦曲线从初始值平滑降到接近0
                                 # 比StepLR(阶梯式)更平滑，效果通常更好
    T_max=100,                   # 一个余弦周期=100epoch，必须与max_epochs一致
                                 # 这样训练结束时lr刚好降到最低点
)

# ⑧ 训练策略
train_cfg = dict(
    by_epoch=True,       # 按epoch计数（另一种是按iteration，用于大数据集）
    max_epochs=100,      # 训练100轮；小数据集~1000张，100轮足够收敛，再多容易过拟合
    val_interval=10,     # 每10个epoch验证一次；平衡验证频率和训练速度
)

# ⑨ 评估
val_evaluator = dict(
    type='Accuracy',     # 准确率评估器，分类任务最直观的指标
    topk=(1, 5),         # top-1=最高分是否正确; top-5=前5个预测中是否包含正确答案
)

# ⑩ 必须添加（推理器 ImageClassificationInferencer 内部会读 test_dataloader，不设会 KeyError）
test_dataloader = val_dataloader
test_evaluator = val_evaluator
```

---

## 🔀 配置文件改模型 (MobileNet V2)

```python
# configs/mobilenetv2_flowers17.py
# 只需改动的部分（对比 ResNet-18），其余参数完全相同以保证公平对比：

_base_ = [
    'mmpretrain::_base_/models/mobilenet_v2_1x.py',  # ← 改为MobileNetV2基础配置
    # MobileNetV2 是轻量级模型(3.4M参数 vs ResNet-18的11M)，适合移动端
    'mmpretrain::_base_/default_runtime.py',
]

model = dict(
    head=dict(
        num_classes=17,
        in_channels=1280,     # ← MobileNetV2 最后一层输出 1280 通道（ResNet-18是512）
                              # 这是由网络架构决定的，MobileNetV2最后有1×1卷积扩展到1280
    ),
)

optim_wrapper = dict(
    optimizer=dict(
        type='Adam',          # ← 改用Adam（ResNet-18用SGD）
        # 原因: MobileNetV2 用 depthwise separable convolution，梯度分布不均匀
        # Adam 的自适应学习率能更好处理；MobileNet论文也推荐Adam
        lr=0.001,             # ← 比SGD的0.01小10倍
        # Adam内部会自适应缩放每个参数的有效lr，初始lr设太大会不稳定
        # 0.001是Adam论文推荐的经典默认值
    ),
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
