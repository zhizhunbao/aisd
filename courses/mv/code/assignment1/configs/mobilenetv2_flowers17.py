# ============================================================
# 模型 2 配置文件: MobileNet V2 用于 Oxford Flowers 17 分类
# Model 2 Config: MobileNet V2 for Oxford Flowers 17 Classification
# ============================================================
# MobileNet V2 是轻量级模型(3.4M 参数 vs ResNet-18 的 11M)，适合移动端
# MobileNet V2 is a lightweight model (3.4M params vs ResNet-18's 11M), suitable for mobile devices

# 继承 MobileNet V2 的基础配置（对比 ResNet-18 用 resnet18.py）
# Inherit MobileNet V2 base config (compared to resnet18.py for ResNet-18)
_base_ = [
    'mmpretrain::_base_/models/mobilenet_v2_1x.py',  # MobileNet V2 网络结构
                                                       # MobileNet V2 network architecture
    'mmpretrain::_base_/default_runtime.py',           # 通用运行时配置
                                                       # General runtime config
]

# ============================================================
# 模型配置 / Model Configuration
# ============================================================

model = dict(
    type='ImageClassifier',

    backbone=dict(
        type='MobileNetV2',
        # widen_factor=1.0: 宽度倍数，控制每层通道数缩放比例
        # 1.0=标准宽度（可选 0.5/0.75 做更轻量版本）; 选 1.0 与 ResNet-18 公平对比
        # widen_factor=1.0: Width multiplier, scales channel count per layer
        # 1.0=standard width (0.5/0.75 for lighter versions); 1.0 chosen for fair comparison with ResNet-18
        widen_factor=1.0,
        # 【迁移学习关键】加载 ImageNet 预训练权重
        # backbone 不从随机初始化开始，而是复用在 120 万张 ImageNet 图片上学到的特征
        # [TRANSFER LEARNING KEY] Load ImageNet pretrained weights
        # Backbone starts from learned features instead of random initialization
        init_cfg=dict(type='Pretrained', checkpoint='https://download.openmmlab.com/mmclassification/v0/mobilenet_v2/mobilenet_v2_batch256_imagenet_20200708-3b2dc3af.pth'),
    ),

    # 全局平均池化，和 ResNet-18 一样
    # Global average pooling, same as ResNet-18
    neck=dict(type='GlobalAveragePooling'),

    head=dict(
        type='LinearClsHead',
        # num_classes=17: 17 种花卉
        # num_classes=17: 17 flower categories
        num_classes=17,
        # in_channels=1280: MobileNet V2 最后一层输出 1280 通道
        # 【关键区别】ResNet-18 是 512; MobileNet V2 最后有 1×1 卷积扩展到 1280
        # in_channels=1280: MobileNet V2 last layer outputs 1280 channels
        # [KEY DIFFERENCE] ResNet-18 is 512; MobileNet V2 has a 1×1 conv expanding to 1280
        in_channels=1280,
        # CrossEntropyLoss: 多分类标准损失; loss_weight=1.0 只有一个 loss
        # CrossEntropyLoss: Standard multi-class loss; loss_weight=1.0 for single loss term
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        # topk=(1, 5): top-1 和 top-5 准确率
        # topk=(1, 5): Compute top-1 and top-5 accuracy
        topk=(1, 5),
    ),
)

# ============================================================
# 数据预处理 / Data Preprocessor
# ============================================================
# 和 ResNet-18 完全一样，使用 ImageNet 统计值; 保证公平对比
# Same as ResNet-18, using ImageNet statistics; ensures fair comparison

data_preprocessor = dict(
    mean=[123.675, 116.28, 103.53],   # ImageNet RGB 均值 / ImageNet RGB mean
    std=[58.395, 57.12, 57.375],      # ImageNet RGB 标准差 / ImageNet RGB std
    to_rgb=True,                       # BGR→RGB 转换 / BGR→RGB conversion
)

# ============================================================
# 数据管道 / Data Pipeline
# ============================================================
# 和 ResNet-18 完全相同，只改模型和优化器，其他条件一致保证公平对比
# Identical to ResNet-18; only model and optimizer differ to ensure fair comparison

train_pipeline = [
    dict(type='LoadImageFromFile'),                                # 读取图片 / Load image
    dict(type='RandomResizedCrop', scale=224, backend='pillow'),    # 随机裁剪缩放到 224×224 / Random crop+resize to 224×224
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),     # 50%概率水平翻转 / 50% horizontal flip
    dict(type='PackInputs'),                                       # 打包输入 / Pack inputs
]

val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='ResizeEdge', scale=256, edge='short', backend='pillow'),  # 短边缩放到 256 / Resize short edge to 256
    dict(type='CenterCrop', crop_size=224),                              # 中心裁剪 224×224 / Center crop to 224×224
    dict(type='PackInputs'),
]

# ============================================================
# 数据加载器 / DataLoader
# ============================================================
# 和 ResNet-18 完全相同 / Same as ResNet-18

train_dataloader = dict(
    batch_size=32,       # 每批 32 张 / 32 images per batch
    num_workers=4,       # 4 个子进程并行加载 / 4 subprocess for parallel loading
    dataset=dict(
        type='CustomDataset',                      # 按文件夹名推断标签 / Infer labels from folder names
        data_prefix='data/flowers17/train',
        with_label=True,                           # 自动提取标签 / Auto-extract labels
        pipeline=train_pipeline,
    ),
    sampler=dict(type='DefaultSampler', shuffle=True),   # 训练打乱 / Shuffle for training
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
    sampler=dict(type='DefaultSampler', shuffle=False),  # 验证不打乱 / No shuffle for validation
)

# ============================================================
# 评估器 / Evaluator
# ============================================================

val_evaluator = dict(type='Accuracy', topk=(1, 5))  # top-1 和 top-5 准确率 / Top-1 and top-5 accuracy

# ============================================================
# 优化器 / Optimizer
# ============================================================
# 【关键区别】MobileNet V2 用 Adam; ResNet-18 用 SGD
# [KEY DIFFERENCE] MobileNet V2 uses Adam; ResNet-18 uses SGD
# 原因: MobileNet V2 用 depthwise separable convolution，梯度分布不均匀
# Adam 的自适应学习率能更好处理; MobileNet 论文推荐 Adam
# Reason: MobileNet V2 uses depthwise separable convolution, gradient distribution is uneven
# Adam's adaptive learning rate handles this better; recommended by MobileNet paper

optim_wrapper = dict(
    optimizer=dict(
        # Adam: 自适应学习率优化器; 内置一阶+二阶动量，不需要单独设 momentum
        # Adam: Adaptive learning rate optimizer; built-in 1st & 2nd order moments, no separate momentum needed
        type='Adam',
        # lr=0.001: 比 SGD 的 0.01 小 10 倍; Adam 内部自适应缩放，初始 lr 太大会不稳定
        # 0.001 是 Adam 论文推荐的经典默认值
        # lr=0.001: 10x smaller than SGD's 0.01; Adam internally scales, too large lr causes instability
        # 0.001 is the classic default recommended by Adam paper
        lr=0.001,
        # weight_decay=0.0001: L2 正则化，和 ResNet-18 一样
        # weight_decay=0.0001: L2 regularization, same as ResNet-18
        weight_decay=0.0001,
    ),
)

# ============================================================
# 学习率调度器 / LR Scheduler
# ============================================================
# 和 ResNet-18 相同: 余弦退火, T_max=100 对应 100 epoch
# Same as ResNet-18: Cosine annealing, T_max=100 matches 100 epochs

param_scheduler = dict(type='CosineAnnealingLR', by_epoch=True, T_max=100)

# ============================================================
# 训练配置 / Training Configuration
# ============================================================
# 和 ResNet-18 完全相同，确保公平对比
# Same as ResNet-18, ensures fair comparison

train_cfg = dict(by_epoch=True, max_epochs=100, val_interval=10)
val_cfg = dict()

# ============================================================
# 运行时钩子 / Runtime Hooks
# ============================================================

default_hooks = dict(
    checkpoint=dict(type='CheckpointHook', interval=10),  # 每 10 epoch 保存 / Save every 10 epochs
    logger=dict(type='LoggerHook', interval=10),           # 每 10 iteration 记日志 / Log every 10 iterations
)

# 工作目录：与 ResNet-18 分开存放，避免互相覆盖
# Work directory: Separate from ResNet-18 to avoid overwriting
work_dir = './work_dirs/mobilenetv2_flowers17'

# ============================================================
# 测试配置 / Test Configuration
# ============================================================
# 复用验证配置; ImageClassificationInferencer 需要这些配置
# Reuse validation config; ImageClassificationInferencer requires these
test_cfg = dict()
test_dataloader = val_dataloader
test_evaluator = val_evaluator
