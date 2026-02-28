# ============================================================
# 模型 1 配置文件: ResNet-18 用于 Oxford Flowers 17 分类
# Model 1 Config: ResNet-18 for Oxford Flowers 17 Classification
# ============================================================
# 说明：此配置基于 mmpretrain 的 ResNet-18 基础配置，
#       针对 Oxford Flowers 17 数据集（17 类）进行了适配。
# Note: This config is based on mmpretrain's ResNet-18 base config,
#       adapted for the Oxford Flowers 17 dataset (17 classes).
# ============================================================

# 继承 ResNet-18 的基础配置
# Inherit from ResNet-18 base config
_base_ = [
    'mmpretrain::_base_/models/resnet18.py',
    'mmpretrain::_base_/default_runtime.py',
]

# ============================================================
# 模型配置
# Model Configuration
# ============================================================
# 要求：修改分类头为 17 类（Oxford Flowers 17 的类别数）
# Requirement: Modify classification head to 17 classes (Oxford Flowers 17)

model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='ResNet',
        depth=18,
        num_stages=4,
        out_indices=(3,),
        style='pytorch',
    ),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='LinearClsHead',
        # 17 类花卉分类
        # 17 flower categories
        num_classes=17,
        in_channels=512,
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        topk=(1, 5),
    ),
)

# ============================================================
# 数据预处理配置
# Data Preprocessor Configuration
# ============================================================
# 要求：使用 ImageNet 的均值和标准差进行归一化（迁移学习常用做法）
# Requirement: Normalize with ImageNet mean/std (common for transfer learning)

data_preprocessor = dict(
    # RGB 通道的均值
    # Mean values for RGB channels
    mean=[123.675, 116.28, 103.53],
    # RGB 通道的标准差
    # Standard deviation for RGB channels
    std=[58.395, 57.12, 57.375],
    to_rgb=True,
)

# ============================================================
# 训练数据管道
# Training Data Pipeline
# ============================================================
# 要求：对训练数据进行数据增强以防止过拟合
# Requirement: Apply data augmentation to prevent overfitting
# 说明：小数据集（~60 张/类）需要更积极的增强策略
# Note: Small dataset (~60 images/class) needs aggressive augmentation

train_pipeline = [
    dict(type='LoadImageFromFile'),
    # 随机裁剪缩放：模拟不同距离和角度拍摄
    # Random resized crop: Simulate different distances and angles
    dict(type='RandomResizedCrop', scale=224, backend='pillow'),
    # 随机水平翻转：增加方向多样性
    # Random horizontal flip: Increase directional diversity
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(type='PackInputs'),
]

# ============================================================
# 验证数据管道
# Validation Data Pipeline
# ============================================================
# 说明：验证时不做数据增强，保持确定性
# Note: No augmentation during validation for deterministic results

val_pipeline = [
    dict(type='LoadImageFromFile'),
    # 缩放到 256 再中心裁剪为 224，标准的验证流程
    # Resize to 256 then center crop to 224, standard validation procedure
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
        # 训练数据路径（SubFolder 格式）
        # Training data path (SubFolder format)
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
        # 验证数据路径（SubFolder 格式）
        # Validation data path (SubFolder format)
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
# 使用准确率作为评价指标
# Use accuracy as evaluation metric

val_evaluator = dict(type='Accuracy', topk=(1, 5))

# ============================================================
# 优化器与学习率调度器配置
# Optimizer & Learning Rate Scheduler Configuration
# ============================================================
# 说明：小数据集使用较小的学习率，防止过拟合
# Note: Smaller learning rate for small datasets to prevent overfitting

optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0001),
)

# 学习率调度器：使用余弦退火策略
# LR Scheduler: Use cosine annealing strategy
param_scheduler = dict(type='CosineAnnealingLR', by_epoch=True, T_max=100)

# ============================================================
# 训练配置
# Training Configuration
# ============================================================

# 训练 100 个 epoch
# Train for 100 epochs
train_cfg = dict(by_epoch=True, max_epochs=100, val_interval=10)
val_cfg = dict()

# ============================================================
# 运行时配置
# Runtime Configuration
# ============================================================

default_hooks = dict(
    # 每 10 个 epoch 保存一次检查点
    # Save checkpoint every 10 epochs
    checkpoint=dict(type='CheckpointHook', interval=10),
    # 日志记录间隔
    # Logging interval
    logger=dict(type='LoggerHook', interval=10),
)

# 工作目录
# Work directory
work_dir = './work_dirs/resnet18_flowers17'

# ============================================================
# 测试配置（复用验证配置，供 ImageClassificationInferencer 使用）
# Test Configuration (reuse val config for ImageClassificationInferencer)
# ============================================================
test_dataloader = val_dataloader
test_evaluator = val_evaluator
