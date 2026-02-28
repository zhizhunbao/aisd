# Assignment 1: Image Classification with OpenMMLab (mmpretrain)

> **课程 / Course:** CST8508 Machine Vision  
> **主题 / Topic:** Assignment 1 — Training Deep Learning Models for Image Classification  
> **框架 / Framework:** mmpretrain (OpenMMLab)  
> **数据集 / Dataset:** Oxford Flowers 17

---

## 1. 概述（Overview）

### 1.1 学习目标（Learning Objectives）

本作业的核心目标是通过实践掌握**深度学习图像分类**的完整流程。— The core objective is to master the complete pipeline for **deep learning image classification** through hands-on practice.

- **熟悉 OpenMMLab 技术栈** — Familiarize with the OpenMMLab tech stack for training CV deep learning models
- **掌握 mmpretrain 的配置驱动训练方式** — Master config-driven training with mmpretrain
- **理解数据集准备（SubFolder 格式）** — Understand dataset preparation (SubFolder format)
- **训练并比较两个模型（ResNet-18 vs MobileNet V2）** — Train and compare two models
- **评估模型性能（准确率、F1、混淆矩阵）** — Evaluate model performance with metrics

### 1.2 任务分解（Task Breakdown）

| 部分 — Part                  | 内容 — Content                                                                             | 权重 — Weight |
| ---------------------------- | ------------------------------------------------------------------------------------------ | ------------- |
| 数据集准备 — Dataset Prep    | 下载 Oxford Flowers 17 并组织为 SubFolder 格式 — Download & organize into SubFolder format | 20%           |
| 环境搭建 — Environment Setup | 安装 mmpretrain + 验证 GPU 可用 — Install mmpretrain + verify GPU                          | -             |
| 配置文件 — Config Files      | 理解并编写 ResNet-18 和 MobileNet V2 的训练配置 — Write training configs                   | -             |
| 模型训练 — Model Training    | 训练两个模型各 100 个 epoch — Train two models for 100 epochs each                         | 50%           |
| 模型评估 — Evaluation        | 准确率、F1、混淆矩阵等指标 — Accuracy, F1, confusion matrix                                | 20%           |
| 经验总结 — Lessons Learned   | 困难、解决方案、心得 — Challenges, solutions, takeaways                                    | 10%           |

---

## 2. OpenMMLab 生态系统（OpenMMLab Ecosystem）

### 2.1 什么是 OpenMMLab?（What is OpenMMLab?）

OpenMMLab 是一个**开源计算机视觉工具箱**集合，由香港中文大学 MMLab 开发。— OpenMMLab is a collection of **open-source computer vision toolboxes** developed by MMLab at CUHK.

核心设计理念 — Core Design Philosophy:

- **模块化** — Modular: 所有组件（模型、数据、优化器）通过**注册器（Registry）**统一管理 — All components managed via Registry
- **配置驱动** — Config-driven: 修改模型/数据集/超参数只需改配置文件，不需要改代码 — Change model/dataset/hyperparams by editing config files only
- **统一接口** — Unified interface: 学会一个项目，其他项目（mmdet, mmseg, mmpose）结构类似 — Learn one project, all others follow similar structure

### 2.2 mmpretrain 核心组件（mmpretrain Core Components）

```
mmpretrain/
├── configs/         ← 预定义的模型配置 / Pre-defined model configs
│   ├── resnet/      ← 包含 resnet18/34/50/101/152 的配置
│   ├── mobilenet_v2/
│   └── ...
├── mmpretrain/
│   ├── models/      ← 模型注册表 / Model registry
│   ├── datasets/    ← 数据集加载器 / Dataset loaders
│   └── engine/      ← 训练引擎 / Training engine
└── tools/
    ├── train.py     ← 训练入口 / Training entry point
    └── test.py      ← 测试入口 / Testing entry point
```

### 2.3 配置文件继承机制（Config Inheritance）

mmpretrain 使用**层级继承**（hierarchical inheritance）来组织配置。— mmpretrain uses hierarchical inheritance to organize configs.

```python
# 继承基础配置 / Inherit base configs
_base_ = [
    'mmpretrain::_base_/models/resnet18.py',      # 模型结构 / Model architecture
    'mmpretrain::_base_/default_runtime.py',       # 运行时默认值 / Runtime defaults
]

# 覆盖特定字段 / Override specific fields
model = dict(
    head=dict(num_classes=17),  # 修改输出类别数 / Change number of output classes
)
```

> 📝 **关键理解 / Key Understanding:** 子配置只需指定**需要修改的部分**，其余从 `_base_` 继承。— Child config only specifies what **needs to change**; the rest is inherited from `_base_`.

---

## 3. 数据集准备（Dataset Preparation）

### 3.1 Oxford Flowers 17 数据集（The Dataset）

Oxford Flowers 17 是一个**小型花卉分类数据集**，来自牛津大学 Visual Geometry Group。— A small flower classification dataset from Oxford's VGG group.

| 属性 — Property            | 值 — Value                                      |
| -------------------------- | ----------------------------------------------- |
| 类别数 — Classes           | 17 种花卉 — 17 flower species                   |
| 总图片数 — Total images    | 1,360                                           |
| 每类约 — Per class         | ~80 张 — ~80 images                             |
| 图片格式 — Format          | JPEG                                            |
| 类别示例 — Example classes | Bluebell, Buttercup, Daisy, Sunflower, Tulip... |

### 3.2 SubFolder 格式（SubFolder Format）

mmpretrain 的 `CustomDataset` 支持 **SubFolder 格式**，无需创建标注文件。— mmpretrain's `CustomDataset` supports SubFolder format without annotation files.

```
data/flowers17/
├── train/
│   ├── Bluebell/       (62 images)
│   ├── Buttercup/      (62 images)
│   ├── ...
│   └── Windflower/     (62 images)
└── val/
    ├── Bluebell/       (16 images)
    ├── Buttercup/      (16 images)
    ├── ...
    └── Windflower/     (16 images)
```

> 📝 **为什么用 SubFolder 格式？ — Why SubFolder format?**
>
> - 不需要创建标注文件 — No annotation files needed
> - 类名自动从文件夹名推断 — Class names inferred from folder names
> - 最简单的数据组织方式 — Simplest data organization method

### 3.3 数据划分（Data Split）

- **训练集 — Training set:** ~1,054 张（每类 62 张） — ~1,054 images (62 per class)
- **验证集 — Validation set:** ~272 张（每类 16 张） — ~272 images (16 per class)
- 划分比例约 **80:20** — Split ratio approximately 80:20

---

## 4. 模型架构（Model Architectures）

### 4.1 ResNet-18（残差网络 / Residual Network）

ResNet 的核心创新是**残差连接（Skip Connection / Shortcut）**，解决了深层网络的梯度消失问题。— ResNet's key innovation is **residual connections (skip connections)**, which solve the vanishing gradient problem in deep networks.

```
输入 → [Conv → BN → ReLU → Conv → BN] + 输入 → ReLU → 输出
Input → [Conv → BN → ReLU → Conv → BN] + Input → ReLU → Output
         \_____残差块 Residual Block_____/  ↗ (skip connection)
```

| 属性 — Property            | ResNet-18 值 — Value        |
| -------------------------- | --------------------------- |
| 层数 — Depth               | 18 层 — 18 layers           |
| 残差阶段 — Stages          | 4 个阶段 — 4 stages         |
| 参数量 — Parameters        | ~11.7M                      |
| 输出特征维度 — Feature dim | 512                         |
| 设计目标 — Design goal     | 准确率优先 — Accuracy first |

### 4.2 MobileNet V2（移动端网络 / Mobile Network）

MobileNet V2 使用**深度可分离卷积（Depthwise Separable Convolution）**和**倒残差结构（Inverted Residual）**来减少计算量。— MobileNet V2 uses depthwise separable convolution and inverted residual blocks to reduce computation.

```
标准卷积 / Standard Conv:
  输入 (H×W×C_in) → 卷积 → 输出 (H×W×C_out)
  参数量: K×K×C_in×C_out

深度可分离卷积 / Depthwise Separable Conv:
  输入 → 深度卷积(K×K×1×C_in) → 逐点卷积(1×1×C_in×C_out) → 输出
  参数量: K×K×C_in + C_in×C_out    ← 大幅减少! / Greatly reduced!
```

| 属性 — Property            | MobileNet V2 值 — Value                          |
| -------------------------- | ------------------------------------------------ |
| 参数量 — Parameters        | ~3.4M（仅占 ResNet-18 的 29%）                   |
| 输出特征维度 — Feature dim | 1280                                             |
| 核心技术 — Core tech       | 深度可分离卷积 — Depthwise separable convolution |
| 设计目标 — Design goal     | 效率优先 — Efficiency first                      |

### 4.3 两模型对比（Model Comparison）

| 方面 — Aspect          | ResNet-18                   | MobileNet V2                     |
| ---------------------- | --------------------------- | -------------------------------- |
| 参数量 — Params        | ~11.7M                      | ~3.4M                            |
| 卷积类型 — Conv type   | 标准卷积 — Standard         | 深度可分离 — Depthwise separable |
| 优化器 — Optimizer     | SGD (lr=0.01, momentum=0.9) | Adam (lr=0.001)                  |
| 特征维度 — Feature dim | 512                         | 1280                             |
| 适用场景 — Use case    | 服务器端 — Server           | 移动端/嵌入式 — Mobile/Edge      |

---

## 5. 配置文件详解（Config File Deep Dive）

### 5.1 完整配置结构（Full Config Structure）

一个 mmpretrain 配置文件包含以下关键部分 — A mmpretrain config contains these key sections:

```python
# ① 模型定义 — Model definition
model = dict(
    type='ImageClassifier',
    backbone=dict(type='ResNet', depth=18),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(type='LinearClsHead', num_classes=17, in_channels=512,
              loss=dict(type='CrossEntropyLoss'),
              topk=(1, 5)),
)

# ② 数据预处理 — Data preprocessor
data_preprocessor = dict(
    mean=[123.675, 116.28, 103.53],   # ImageNet 均值 / ImageNet mean
    std=[58.395, 57.12, 57.375],       # ImageNet 标准差 / ImageNet std
)

# ③ 数据增强管道 — Data augmentation pipeline
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='RandomResizedCrop', scale=224),   # 随机裁剪到 224×224
    dict(type='RandomFlip', prob=0.5),            # 50% 概率水平翻转
    dict(type='PackInputs'),
]

# ④ 数据加载器 — Data loaders
train_dataloader = dict(batch_size=32, num_workers=4, dataset=dict(...))

# ⑤ 优化器 — Optimizer
optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0001),
)

# ⑥ 学习率调度 — LR scheduler
param_scheduler = dict(type='CosineAnnealingLR', T_max=100)

# ⑦ 训练策略 — Training strategy
train_cfg = dict(by_epoch=True, max_epochs=100, val_interval=10)
```

### 5.2 关键配置解释（Key Config Explanations）

#### 数据增强（Data Augmentation）

对于**小数据集**（每类仅 ~60 张），数据增强至关重要。— Data augmentation is crucial for **small datasets** (~60 images per class).

| 增强方式 — Augmentation  | 作用 — Purpose                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| `RandomResizedCrop(224)` | 随机裁剪并缩放到 224×224，模拟不同拍摄距离 — Random crop & resize, simulates different distances |
| `RandomFlip(prob=0.5)`   | 50% 概率水平翻转，增加方向多样性 — 50% horizontal flip, adds directional diversity               |

#### ImageNet 归一化（ImageNet Normalization）

```python
mean = [123.675, 116.28, 103.53]
std  = [58.395, 57.12, 57.375]
```

> 📝 **为什么用 ImageNet 的均值/标准差？ — Why ImageNet mean/std?**
> 即使不使用预训练权重，使用 ImageNet 统计值作为归一化标准是最常见的做法，因为这些值对自然图像具有良好的代表性。— Even without pretrained weights, ImageNet stats are the most common normalization standard for natural images.

#### 余弦退火学习率（Cosine Annealing LR）

学习率按余弦函数从初始值逐渐衰减到接近 0。— Learning rate decays from initial value to near 0 following a cosine curve.

```
lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(π * t / T_max))

示例 / Example:
  初始 lr = 0.01, T_max = 100
  Epoch 0:   lr = 0.01    （最高 / Max）
  Epoch 50:  lr = 0.005   （中间 / Mid）
  Epoch 100: lr ≈ 0.0     （接近0 / Near 0）
```

> 📝 **优势 — Advantage:** 开始时用大学习率快速收敛，后期用小学习率精细调整。— Start with large LR for fast convergence, end with small LR for fine-tuning.

---

## 6. 训练与评估结果（Training & Evaluation Results）

### 6.1 训练环境（Training Environment）

| 组件 — Component | 版本 — Version        |
| ---------------- | --------------------- |
| 操作系统 — OS    | Ubuntu 22.04 (WSL2)   |
| GPU              | NVIDIA RTX 4060 (8GB) |
| Python           | 3.8 (conda)           |
| PyTorch          | 2.4.1 + CUDA 12.1     |
| mmengine         | 0.10.7                |
| mmcv             | 2.2.0                 |
| mmpretrain       | 1.2.0                 |

### 6.2 训练曲线（Training Curves）

**ResNet-18 验证准确率 — ResNet-18 Validation Accuracy:**

| Epoch | Top-1 (%) | Top-5 (%) |
| ----- | --------- | --------- |
| 10    | 38.97     | 80.51     |
| 20    | 52.57     | 91.54     |
| 50    | 69.49     | 95.96     |
| 90    | **77.21** | **97.79** |
| 100   | 76.47     | 98.16     |

**MobileNet V2 验证准确率 — MobileNet V2 Validation Accuracy:**

| Epoch | Top-1 (%) | Top-5 (%) |
| ----- | --------- | --------- |
| 10    | 55.88     | 92.65     |
| 20    | 63.60     | 95.22     |
| 50    | 84.93     | 98.90     |
| 90    | **90.07** | **98.53** |
| 100   | 89.71     | 98.90     |

### 6.3 最终结果（Final Results — Best Epoch 90）

| 指标 — Metric       | ResNet-18 | MobileNet V2 | 差距 — Gap |
| ------------------- | --------- | ------------ | ---------- |
| Top-1 Accuracy      | 77.21%    | **90.07%**   | +12.86%    |
| Top-5 Accuracy      | 97.79%    | **98.53%**   | +0.74%     |
| Macro Avg Precision | 0.78      | **0.91**     | +0.13      |
| Macro Avg Recall    | 0.77      | **0.90**     | +0.13      |
| Macro Avg F1-Score  | 0.77      | **0.90**     | +0.13      |

> 📝 **意外发现 — Surprising Finding:** 参数量仅为 ResNet-18 的 29% 的 MobileNet V2 反而准确率高出 **13 个百分点**！原因可能是：— MobileNet V2, with only 29% of ResNet-18's parameters, outperformed it by 13%! Possible reasons:
>
> - Adam 优化器在小数据集上收敛更好 — Adam optimizer converges better on small datasets
> - MobileNet V2 参数更少，在小数据集上过拟合风险更低 — Fewer parameters = lower overfitting risk on small datasets
> - SGD 可能需要更精细的超参数调优 — SGD may need more careful hyperparameter tuning

### 6.4 每类表现分析（Per-Category Analysis）

**高准确率类别（视觉特征显著）— High accuracy (distinctive visual features):**

- Daisy, Sunflower, TigerLily — 这些花有独特的形状和颜色 — Distinctive shape and color

**低准确率类别（视觉相似）— Low accuracy (visually similar):**

- Cowslip vs Coltsfoot — 形状相似的黄色小花 — Similar small yellow flowers
- Buttercup vs Dandelion — 都是黄色花朵 — Both yellow flowers

---

## 7. 评估指标详解（Evaluation Metrics Explained）

### 7.1 Top-K 准确率（Top-K Accuracy）

- **Top-1:** 模型最高概率的预测是否正确 — Is the model's top prediction correct?
- **Top-5:** 正确类别是否在模型前 5 个预测中 — Is the correct class in the top 5 predictions?

### 7.2 混淆矩阵（Confusion Matrix）

混淆矩阵显示每个类别的预测分布，帮助识别**哪些类别容易混淆**。— Shows prediction distribution per class, helps identify **which classes are confused with each other**.

```
              预测 / Predicted
            Daisy  Tulip  Rose
    Daisy   [15    0      1  ]   ← 大多数正确 / mostly correct
真   Tulip   [0     10     6  ]   ← 常被误判为 Rose / confused with Rose
实   Rose    [1     3      12 ]   ← 偶尔被误判 / occasional misclass
```

### 7.3 Precision, Recall, F1-Score

| 指标 — Metric | 公式 — Formula      | 含义 — Meaning                                                                             |
| ------------- | ------------------- | ------------------------------------------------------------------------------------------ |
| **Precision** | TP / (TP + FP)      | 预测为正的样本中，实际为正的比例 — Of predicted positives, how many are actually positive  |
| **Recall**    | TP / (TP + FN)      | 实际为正的样本中，被正确预测的比例 — Of actual positives, how many are correctly predicted |
| **F1-Score**  | 2 × P × R / (P + R) | Precision 和 Recall 的调和平均 — Harmonic mean of P and R                                  |

---

## 8. 经验教训（Lessons Learned）

### 8.1 环境搭建（Environment Setup）

- **关键教训 — Key lesson:** 环境搭建是工作量的一半！— Environment setup is half the battle!
- Conda + 官方推荐版本（Python 3.8 + PyTorch 2.4.1）是最可靠的路径 — Conda + official versions is the most reliable path
- 避免混用 pip/conda，避免 bleeding-edge Python 版本 — Avoid mixing pip/conda, avoid latest Python

### 8.2 配置驱动训练（Config-Driven Training）

- 改模型/数据集/超参数**只需改配置，不需改代码** — Changing model/dataset/hyperparams only requires config edits
- 实验可完全复现 — Experiments are fully reproducible

### 8.3 自动化（Automation）

- 将整个流程封装为 shell 脚本 → 一键运行 — Wrap entire pipeline in shell script → one command to run
- `setup → check → train → evaluate → copy results`

---

## 9. 关键命令参考（Key Commands Reference）

```bash
# 安装 mmpretrain / Install mmpretrain
pip install openmim
mim install mmengine mmcv mmpretrain

# 训练模型 / Train a model
python -m mmpretrain.tools.train configs/resnet18_flowers17.py

# 使用推理器评估 / Evaluate with inferencer
from mmpretrain import ImageClassificationInferencer
inferencer = ImageClassificationInferencer(
    model='configs/resnet18_flowers17.py',
    pretrained='work_dirs/resnet18_flowers17/epoch_90.pth'
)
result = inferencer('path/to/image.jpg')[0]
print(result['pred_label'], result['pred_score'])
```

---

## 10. 总结（Summary）

```
┌─────────────────────────────────────────────────────────────────┐
│  Assignment 1 核心知识链 — Core Knowledge Chain                  │
│                                                                  │
│  数据准备      →  配置文件      →  模型训练      →  模型评估     │
│  Dataset Prep     Config Files     Training         Evaluation   │
│  (SubFolder)      (_base_ 继承)    (epoch, lr)      (metrics)    │
│                                                                  │
│  关键工具 — Key Tools:                                           │
│  - mmpretrain (OpenMMLab 图像分类工具箱)                        │
│  - ResNet-18 vs MobileNet V2 (经典 vs 轻量级)                  │
│  - SGD vs Adam (优化器对比)                                     │
│  - Confusion Matrix + F1 (评估指标)                             │
│                                                                  │
│  核心发现 — Key Finding:                                         │
│  MobileNet V2 (3.4M params) > ResNet-18 (11.7M params)         │
│  小数据集 + Adam → 更好的收敛                                   │
│  Small dataset + Adam → Better convergence                      │
└─────────────────────────────────────────────────────────────────┘
```
