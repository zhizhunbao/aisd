# ============================================================
# 模型 2 配置文件: MobileNet V2 用于 Oxford Flowers 17 分类
# Model 2 Config: MobileNet V2 for Oxford Flowers 17 Classification
# ============================================================
# 说明：MobileNet V2 是轻量级模型，适合移动端和嵌入式设备。
#       相比 ResNet-18 参数量更少，推理速度更快。
# Note: MobileNet V2 is a lightweight model for mobile/embedded devices.
#       Has fewer parameters and faster inference than ResNet-18.
# ============================================================

# 继承 MobileNet V2 的基础配置
# Inherit from MobileNet V2 base config
_base_ = [
    'mmpretrain::_base_/models/mobilenet_v2_1x.py',
    'mmpretrain::_base_/default_runtime.py',
]

# ============================================================
# 模型配置
# Model Configuration
# ============================================================
# 要求：修改分类头为 17 类
# Requirement: Modify classification head to 17 classes
# MobileNet V2 的最终特征维度为 1280（与 ResNet-18 的 512 不同）
# MobileNet V2 final feature dimension is 1280 (differs from ResNet-18's 512)

model = dict(
    type='ImageClassifier',
    backbone=dict(type='MobileNetV2', widen_factor=1.0),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='LinearClsHead',
        # 17 类花卉分类
        # 17 flower categories
        num_classes=17,
        in_channels=1280,
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        topk=(1, 5),
    ),
)

# ============================================================
# 数据预处理配置
# Data Preprocessor Configuration
# ============================================================

data_preprocessor = dict(
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    to_rgb=True,
)

# ============================================================
# 训练数据管道
# Training Data Pipeline
# ============================================================
# 说明：与 ResNet-18 使用相同的数据管道以便公平对比
# Note: Same pipeline as ResNet-18 for fair comparison

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='RandomResizedCrop', scale=224, backend='pillow'),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(type='PackInputs'),
]

# ============================================================
# 验证数据管道
# Validation Data Pipeline
# ============================================================

val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='ResizeEdge', scale=256, edge='short', backend='pillow'),
    dict(type='CenterCrop', crop_size=224),
    dict(type='PackInputs'),
]

# ============================================================
# 数据加载器配置
# DataLoader Configuration
# ============================================================

train_dataloader = dict(
    batch_size=32,
    num_workers=4,
    dataset=dict(
        type='CustomDataset',
        data_prefix='data/flowers17/train',
        with_label=True,
        pipeline=train_pipeline,
    ),
    sampler=dict(type='DefaultSampler', shuffle=True),
)

val_dataloader = dict(
    batch_size=32,
    num_workers=4,
    dataset=dict(
        type='CustomDataset',
        data_prefix='data/flowers17/val',
        with_label=True,
        pipeline=val_pipeline,
    ),
    sampler=dict(type='DefaultSampler', shuffle=False),
)

# ============================================================
# 评估器配置
# Evaluator Configuration
# ============================================================

val_evaluator = dict(type='Accuracy', topk=(1, 5))

# ============================================================
# 优化器与学习率调度器配置
# Optimizer & Learning Rate Scheduler Configuration
# ============================================================
# MobileNet V2 通常使用 Adam 优化器（对比 ResNet 的 SGD）
# MobileNet V2 typically uses Adam optimizer (vs SGD for ResNet)
# 这也是本次实验想对比的一个方面
# This is also an aspect we want to compare in this experiment

optim_wrapper = dict(
    optimizer=dict(type='Adam', lr=0.001, weight_decay=0.0001),
)

# 学习率调度器
# LR Scheduler
param_scheduler = dict(type='CosineAnnealingLR', by_epoch=True, T_max=100)

# ============================================================
# 训练配置
# Training Configuration
# ============================================================

train_cfg = dict(by_epoch=True, max_epochs=100, val_interval=10)
val_cfg = dict()

# ============================================================
# 运行时配置
# Runtime Configuration
# ============================================================

default_hooks = dict(
    checkpoint=dict(type='CheckpointHook', interval=10),
    logger=dict(type='LoggerHook', interval=10),
)

work_dir = './work_dirs/mobilenetv2_flowers17'

# ============================================================
# 测试配置（复用验证配置，供 ImageClassificationInferencer 使用）
# Test Configuration (reuse val config for ImageClassificationInferencer)
# ============================================================
test_dataloader = val_dataloader
test_evaluator = val_evaluator
