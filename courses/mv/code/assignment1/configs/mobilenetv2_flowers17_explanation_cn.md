# MobileNet V2 配置文件参数解释

## 概述

本配置文件定义了使用 mmpretrain 框架在 Oxford Flowers 17 数据集上训练 MobileNet V2 图像分类模型所需的所有设置。

---

## 1. 基础配置 (`_base_`)

```python
_base_ = [
    'mmpretrain::_base_/models/mobilenet_v2_1x.py',
    'mmpretrain::_base_/default_runtime.py',
]
```

- `mobilenet_v2_1x.py`：定义 MobileNet V2 的默认网络结构（backbone/neck/head），我们继承它，只覆盖要改的部分。
- `default_runtime.py`：通用运行时配置（日志、随机种子、断点续训等）。
- **为什么要继承？** 避免从零写几百行配置，只需覆盖任务相关设置（如 `num_classes`、优化器）。

---

## 2. 模型架构

```python
model = dict(
    type='ImageClassifier',
    backbone=dict(type='MobileNetV2', widen_factor=1.0),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='LinearClsHead',
        num_classes=17,
        in_channels=1280,
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        topk=(1, 5),
    ),
)
```

### 2.1 `type='ImageClassifier'`

顶层模型类型，告诉 mmpretrain 构建一个图像分类模型，包含三个子模块：backbone、neck、head。

### 2.2 Backbone — `MobileNetV2`（特征提取器）

**作用：** 从原始图片中提取视觉特征。输入 224×224×3 像素图片，经过多层卷积，输出 7×7×1280 的特征图。

**原理：**
- 使用**深度可分离卷积**（Inverted Residual Block），而不是标准卷积，大幅减少计算量同时保持精度。
- 每个 block：1×1 卷积扩展通道 → 3×3 深度卷积 → 1×1 卷积压缩通道。
- 浅层检测边缘、颜色等低级特征，深层捕获形状、语义等高级特征。

| 参数 | 值 | 含义 |
|------|-----|------|
| `type` | `'MobileNetV2'` | 使用 MobileNet V2 架构 |
| `widen_factor` | `1.0` | 宽度倍数，控制每层通道数。1.0=标准宽度；0.5 会把所有通道数减半（更小更快但精度降低）。选 1.0 是为了与 ResNet-18 公平对比。 |

### 2.3 Neck — `GlobalAveragePooling`（全局平均池化）

**作用：** 将 backbone 输出的空间特征图压缩为一维向量。

- 输入：7×7×1280（1280 个通道，每个 7×7 像素）
- 操作：对每个通道的 49 个值（7×7）取平均
- 输出：1280 维向量

**为什么？** 去掉空间信息（"在哪里"），只保留"有什么特征"。同时大幅减少参数（7×7×1280=62,720 → 1280）。

### 2.4 Head — `LinearClsHead`（分类头）

**作用：** 一个全连接层，将特征向量映射为类别分数。

- 输入：1280 维向量
- 输出：17 个分数（每种花一个）
- 计算：`y = W × x + b`，W 大小为 (17, 1280)

| 参数 | 值 | 含义 |
|------|-----|------|
| `num_classes` | `17` | Flowers 17 有 17 种花，输出维度 = 17。 |
| `in_channels` | `1280` | 必须与 backbone 最后一层输出通道数一致。MobileNet V2 是 1280（ResNet-18 是 512）。 |
| `CrossEntropyLoss` | `loss_weight=1.0` | 多分类标准损失函数。先 softmax 把分数变概率，再计算 -log(正确类概率)。loss 越小 = 预测越好。`loss_weight=1.0` 因为只有一个 loss。 |
| `topk` | `(1, 5)` | 训练时计算的指标。Top-1：最高分是不是正确类别？Top-5：前 5 个预测里有没有正确答案？ |

---

## 3. 数据预处理

```python
data_preprocessor = dict(
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    to_rgb=True,
)
```

| 参数 | 值 | 含义 |
|------|-----|------|
| `mean` | `[123.675, 116.28, 103.53]` | ImageNet 120 万张图计算出的 RGB 均值。每个像素归一化：`pixel = (pixel - mean) / std`。 |
| `std` | `[58.395, 57.12, 57.375]` | ImageNet 的 RGB 标准差。 |
| `to_rgb` | `True` | OpenCV 默认读取 BGR 格式，转为 RGB 以匹配模型期望的输入。 |

**为什么用 ImageNet 的值？** 标准化输入分布，让模型接收一致的数据。和 ResNet-18 用相同的值，确保公平对比。

---

## 4. 训练数据管道

```python
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='RandomResizedCrop', scale=224, backend='pillow'),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(type='PackInputs'),
]
```

| 步骤 | 类型 | 参数 | 作用 |
|------|------|------|------|
| 1 | `LoadImageFromFile` | — | 从磁盘读取图片。管道必须的第一步。 |
| 2 | `RandomResizedCrop` | `scale=224, backend='pillow'` | 随机选取图片的一块区域，缩放到 224×224。最关键的数据增强——模拟不同拍摄距离和构图。`scale=224` 是 ImageNet 标准输入尺寸。`backend='pillow'` 插值质量更好。 |
| 3 | `RandomFlip` | `prob=0.5, direction='horizontal'` | 50% 概率水平翻转。花左右对称所以有效。不做垂直翻转因为花倒过来不自然。 |
| 4 | `PackInputs` | — | 转为模型输入的 tensor 格式。管道必须的最后一步。 |

**为什么要数据增强？** 数据集每类只有约 60 张图。不增强的话模型会很快记住训练图片（过拟合）。增强创造变化，迫使模型学习通用特征。

---

## 5. 验证数据管道

```python
val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='ResizeEdge', scale=256, edge='short', backend='pillow'),
    dict(type='CenterCrop', crop_size=224),
    dict(type='PackInputs'),
]
```

| 步骤 | 类型 | 参数 | 作用 |
|------|------|------|------|
| 1 | `LoadImageFromFile` | — | 读取图片。 |
| 2 | `ResizeEdge` | `scale=256, edge='short'` | 短边缩到 256 像素，长边等比例缩放。保证图片够大，裁剪后不丢太多信息。 |
| 3 | `CenterCrop` | `crop_size=224` | 从中心裁剪 224×224。没有随机性——保证每次结果完全一样。 |
| 4 | `PackInputs` | — | 打包为 tensor 格式。 |

**为什么验证不做随机增强？** 验证必须是确定性的。同一张图每次必须产生相同结果，才能公平地跟踪模型各 epoch 的性能改进。

---

## 6. 数据加载器

```python
train_dataloader = dict(
    batch_size=32,
    num_workers=4,
    dataset=dict(type='CustomDataset', data_prefix='data/flowers17/train',
                 with_label=True, pipeline=train_pipeline),
    sampler=dict(type='DefaultSampler', shuffle=True),
)
```

| 参数 | 值 | 含义 |
|------|-----|------|
| `batch_size` | `32` | 每次送 32 张图进模型。RTX 4060 8GB 显存够用。小数据集用太大 batch 反而泛化差。 |
| `num_workers` | `4` | 4 个子进程并行加载数据，加速读取。通常设为 CPU 核数的一半。 |
| `CustomDataset` | — | 通用数据集类，按文件夹名自动推断标签。如 `train/Tulip/001.jpg` → 标签 "Tulip"。 |
| `data_prefix` | `'data/flowers17/train'` | 训练图片的根目录。 |
| `with_label` | `True` | 自动从子文件夹名提取标签。 |
| `shuffle` | 训练 `True` / 验证 `False` | 训练打乱顺序（防止模型记住数据出现顺序）。验证不打乱（可复现）。 |

---

## 7. 评估器

```python
val_evaluator = dict(type='Accuracy', topk=(1, 5))
```

| 参数 | 值 | 含义 |
|------|-----|------|
| `type` | `'Accuracy'` | 在验证集上计算分类准确率。 |
| `topk` | `(1, 5)` | Top-1：最高分的类别正确的图片比例。Top-5：正确类别在前 5 个预测中的图片比例。 |

---

## 8. 优化器

```python
optim_wrapper = dict(
    optimizer=dict(type='Adam', lr=0.001, weight_decay=0.0001),
)
```

| 参数 | 值 | 含义 |
|------|-----|------|
| `type` | `'Adam'` | 自适应学习率优化器。和 ResNet-18 用的 SGD 不同，Adam 自动为每个参数调整学习率，更适合 MobileNet V2 的深度可分离卷积。 |
| `lr` | `0.001` | 初始学习率，Adam 论文的经典默认值。比 SGD 的 0.01 小因为 Adam 内部会缩放梯度。 |
| `weight_decay` | `0.0001` | L2 正则化系数。惩罚过大的权重，防止过拟合。标准值。 |

---

## 9. 学习率调度器

```python
param_scheduler = dict(type='CosineAnnealingLR', by_epoch=True, T_max=100)
```

| 参数 | 值 | 含义 |
|------|-----|------|
| `type` | `'CosineAnnealingLR'` | 余弦退火：学习率按余弦曲线平滑下降。比阶梯式下降(StepLR)更平滑，通常收敛更好。 |
| `by_epoch` | `True` | 每个 epoch 调整一次学习率（不是每个 iteration）。 |
| `T_max` | `100` | 完整余弦周期 = 100 个 epoch，与 `max_epochs` 一致。训练结束时 lr 正好降到最低点。 |

---

## 10. 训练配置

```python
train_cfg = dict(by_epoch=True, max_epochs=100, val_interval=10)
val_cfg = dict()
```

| 参数 | 值 | 含义 |
|------|-----|------|
| `by_epoch` | `True` | 按 epoch 计数（一个 epoch = 遍历完整数据集一次）。 |
| `max_epochs` | `100` | 训练 100 轮。约 1000 张图 100 轮足够收敛，再多容易过拟合。 |
| `val_interval` | `10` | 每 10 个 epoch 验证一次。平衡验证频率和训练速度。 |

---

## 11. 运行时钩子

```python
default_hooks = dict(
    checkpoint=dict(type='CheckpointHook', interval=10),
    logger=dict(type='LoggerHook', interval=10),
)
```

| 参数 | 值 | 含义 |
|------|-----|------|
| `CheckpointHook` | `interval=10` | 每 10 个 epoch 保存一次权重(.pth 文件)。共保存 10 次，可以事后选最佳模型。 |
| `LoggerHook` | `interval=10` | 每 10 个 iteration 打印一次 loss。太频繁刷屏，太少看不到进度。 |

---

## 12. 工作目录

```python
work_dir = './work_dirs/mobilenetv2_flowers17'
```

所有训练产出（权重文件、日志、配置备份）保存在此目录。与 ResNet-18 分开存放避免互相覆盖。

---

## 13. 测试配置

```python
test_cfg = dict()
test_dataloader = val_dataloader
test_evaluator = val_evaluator
```

复用验证配置用于测试。mmpretrain 的 `ImageClassificationInferencer` 需要这些配置，不设置会报 KeyError。
