# ============================================================
# 模型 1 配置文件: ResNet-18 用于 Oxford Flowers 17 分类
# Model 1 Config: ResNet-18 for Oxford Flowers 17 Classification
# ============================================================

# _base_: 继承 mmpretrain 官方的基础配置文件，不用从零写所有配置
# _base_: Inherit from mmpretrain's base configs, no need to write everything from scratch
_base_ = [
    'mmpretrain::_base_/models/resnet18.py',     # ResNet-18 网络结构定义（backbone/neck/head 默认值）
                                                  # ResNet-18 network structure (default backbone/neck/head)
    'mmpretrain::_base_/default_runtime.py',      # 通用运行时配置（日志、随机种子、断点续训等）
                                                  # General runtime config (logging, random seed, resume, etc.)
]

# ============================================================
# 模型配置 / Model Configuration
# ============================================================

model = dict(
    # ImageClassifier: mmpretrain 的图像分类模型入口，因为本任务是图像分类
    # ImageClassifier: mmpretrain's image classification entry point
    type='ImageClassifier',

    backbone=dict(
        type='ResNet',
        # depth=18: ResNet 的层数，可选 18/34/50/101/152
        # 选 18: (1) 作业要求 (2) 参数量小(约11M)适合小数据集(~1000张)，太深容易过拟合
        # depth=18: Number of layers in ResNet, options: 18/34/50/101/152
        # Chose 18: (1) assignment requirement (2) fewer params (~11M), suitable for small dataset
        depth=18,
        # num_stages=4: ResNet 固定 4 个 stage (conv2_x ~ conv5_x)，标准结构不能改
        # num_stages=4: ResNet has exactly 4 stages (conv2_x ~ conv5_x), standard architecture
        num_stages=4,
        # out_indices=(3,): 只取第 4 个 stage 的输出（索引从 0 开始）
        # 分类只需最深层的语义特征（检测才需多层特征如 FPN）
        # out_indices=(3,): Only output from 4th stage (0-indexed)
        # Classification needs only deepest semantic features (detection needs multi-level via FPN)
        out_indices=(3,),
        # style='pytorch': 卷积 padding 方式，PyTorch 和 Caffe 在 stride=2 时处理不同
        # style='pytorch': Conv padding style, PyTorch vs Caffe differ at stride=2
        style='pytorch',
        # 【迁移学习关键】加载 ImageNet 预训练权重
        # backbone 不从随机初始化开始，而是复用在 120 万张 ImageNet 图片上学到的特征
        # 这些特征（边缘、纹理、形状）对花卉分类同样有用
        # [TRANSFER LEARNING KEY] Load ImageNet pretrained weights
        # Backbone starts from learned features instead of random initialization
        # These features (edges, textures, shapes) transfer well to flower classification
        init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet18'),
    ),

    # GlobalAveragePooling: 全局平均池化，将 7×7×512 特征图压缩为 1×1×512 向量
    # 大幅减少参数量，避免全连接层过大；同时具有空间不变性
    # GlobalAveragePooling: Pools 7×7×512 feature map to 1×1×512 vector
    # Drastically reduces parameters; provides spatial invariance
    neck=dict(type='GlobalAveragePooling'),

    head=dict(
        # LinearClsHead: 简单全连接层分类头，512 维输入 → 17 维输出
        # LinearClsHead: Simple FC classification head, 512-dim input → 17-dim output
        type='LinearClsHead',
        # num_classes=17: Oxford Flowers 17 数据集有 17 种花
        # num_classes=17: Oxford Flowers 17 dataset has 17 flower categories
        num_classes=17,
        # in_channels=512: 必须与 backbone 最后一层输出通道数一致
        # ResNet-18 第 4 个 stage 输出 512 通道（ResNet-50 是 2048）
        # in_channels=512: Must match backbone's last layer output channels
        # ResNet-18 stage4 outputs 512 channels (ResNet-50 would be 2048)
        in_channels=512,
        # CrossEntropyLoss: 多分类标准损失，合并 softmax + 负对数似然，数值更稳定
        # loss_weight=1.0: 只有一个 loss，权重为 1
        # CrossEntropyLoss: Standard multi-class loss, combines softmax + NLL, numerically stable
        # loss_weight=1.0: Only one loss term, weight = 1
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        # topk=(1, 5): 同时计算 top-1 和 top-5 准确率
        # top-1 = 最高分是否正确; top-5 = 前 5 个预测中是否包含正确答案
        # topk=(1, 5): Compute both top-1 and top-5 accuracy
        # top-1 = highest prediction correct; top-5 = correct answer in top 5 predictions
        topk=(1, 5),
    ),
)

# ============================================================
# 数据预处理 / Data Preprocessor
# ============================================================

data_preprocessor = dict(
    # mean/std: ImageNet 120 万张图统计的 RGB 均值和标准差
    # 归一化公式: pixel = (pixel - mean) / std
    # 必须用 ImageNet 值（不是自己数据集的），因为预训练权重在 ImageNet 上训练
    # mean/std: RGB mean and std from 1.2M ImageNet images
    # Normalization: pixel = (pixel - mean) / std
    # Must use ImageNet values (not our dataset's) because pretrained weights expect this distribution
    mean=[123.675, 116.28, 103.53],       # R=123.675, G=116.28, B=103.53
    std=[58.395, 57.12, 57.375],          # R=58.395,  G=57.12,  B=57.375
    # to_rgb=True: OpenCV 默认读 BGR，需转为 RGB（预训练模型用 RGB 训练）
    # to_rgb=True: OpenCV reads BGR by default, convert to RGB (pretrained models use RGB)
    to_rgb=True,
)

# ============================================================
# 训练数据管道 / Training Data Pipeline
# ============================================================
# 小数据集（~60 张/类）需要数据增强防止过拟合
# Small dataset (~60 images/class) requires data augmentation to prevent overfitting

train_pipeline = [
    # 从磁盘读取图片（管道必须的起点）
    # Load image from file (required first step in pipeline)
    dict(type='LoadImageFromFile'),
    # 随机裁剪+缩放到 224×224（最关键的增强手段）
    # scale=224: ImageNet 标准输入尺寸，ResNet 按此尺寸设计
    # 模拟不同拍摄距离和构图，极大增加数据多样性
    # backend='pillow': Pillow 插值质量比 OpenCV 更好
    # Random crop + resize to 224×224 (most critical augmentation)
    # scale=224: ImageNet standard input size, ResNet designed for this
    # Simulates different shooting distances/compositions, greatly increases data diversity
    # backend='pillow': Pillow interpolation quality is better than OpenCV
    dict(type='RandomResizedCrop', scale=224, backend='pillow'),
    # 50% 概率水平翻转; 只水平不垂直（花左右对称，上下颠倒不自然）
    # 50% probability horizontal flip; horizontal only (flowers are left-right symmetric, not up-down)
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    # 打包为模型输入格式（管道必须的终点）
    # Pack into model input format (required last step in pipeline)
    dict(type='PackInputs'),
]

# ============================================================
# 验证数据管道 / Validation Data Pipeline
# ============================================================
# 验证不做随机增强，保证结果可复现
# No random augmentation during validation, ensures reproducible results

val_pipeline = [
    dict(type='LoadImageFromFile'),
    # 短边缩放到 256，长边等比例；保证图片够大，裁剪后不丢太多信息
    # Resize short edge to 256, scale long edge proportionally; ensures enough content after crop
    dict(type='ResizeEdge', scale=256, edge='short', backend='pillow'),
    # 中心裁剪 224×224; 不用 RandomResizedCrop 因为验证需要确定性结果
    # Center crop to 224×224; not RandomResizedCrop because validation needs deterministic results
    dict(type='CenterCrop', crop_size=224),
    dict(type='PackInputs'),
]

# ============================================================
# 数据加载器 / DataLoader
# ============================================================

train_dataloader = dict(
    # batch_size=32: 每批 32 张; RTX 4060 8GB 显存够用; 小数据集 batch 太大泛化差
    # batch_size=32: 32 images per batch; RTX 4060 8GB can handle; too large batch hurts generalization
    batch_size=32,
    # num_workers=4: 4 个子进程并行加载数据，加速读取; 通常设为 CPU 核数一半
    # num_workers=4: 4 subprocess for parallel data loading; usually half of CPU cores
    num_workers=4,
    dataset=dict(
        # CustomDataset: 通用数据集，按文件夹名自动推断标签
        # 结构: data/flowers17/train/Bluebell/xxx.jpg → 标签=Bluebell
        # CustomDataset: Generic dataset, auto-infers labels from folder names
        # Structure: data/flowers17/train/Bluebell/xxx.jpg → label=Bluebell
        type='CustomDataset',
        data_prefix='data/flowers17/train',
        # with_label=True: 自动从子文件夹名提取标签
        # with_label=True: Auto-extract labels from subfolder names
        with_label=True,
        pipeline=train_pipeline,
    ),
    # shuffle=True: 每个 epoch 打乱顺序，防止模型记住数据出现顺序
    # shuffle=True: Shuffle every epoch, prevent model from memorizing data order
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
    # shuffle=False: 验证集不打乱，保证结果可复现
    # shuffle=False: No shuffle for validation, ensures reproducible results
    sampler=dict(type='DefaultSampler', shuffle=False),
)

# ============================================================
# 评估器 / Evaluator
# ============================================================

# Accuracy: 准确率评估器，分类任务最直观的指标
# topk=(1, 5): 同时报告 top-1 和 top-5
# Accuracy: Most intuitive metric for classification
# topk=(1, 5): Report both top-1 and top-5 accuracy
val_evaluator = dict(type='Accuracy', topk=(1, 5))

# ============================================================
# 优化器 / Optimizer
# ============================================================

optim_wrapper = dict(
    optimizer=dict(
        # SGD: 随机梯度下降; ResNet 论文原始用 SGD; CNN 在 SGD 下通常泛化更好
        # SGD: Stochastic Gradient Descent; original ResNet paper uses SGD; CNNs generalize better with SGD
        type='SGD',
        # lr=0.01: 初始学习率; 比 ImageNet 标准(0.1)小 10 倍
        # 小数据集 lr 太大会梯度震荡、无法收敛
        # lr=0.01: Initial learning rate; 10x smaller than ImageNet standard (0.1)
        # Too large lr on small dataset causes gradient oscillation and divergence
        lr=0.01,
        # momentum=0.9: 动量因子(经典值); 加速一致方向的梯度更新，抑制震荡
        # momentum=0.9: Momentum factor (classic value); accelerates consistent gradient directions, dampens oscillation
        momentum=0.9,
        # weight_decay=0.0001: L2 正则化(经典值); 惩罚过大权重，防止过拟合
        # weight_decay=0.0001: L2 regularization (classic value); penalizes large weights, prevents overfitting
        weight_decay=0.0001,
    ),
)

# ============================================================
# 学习率调度器 / LR Scheduler
# ============================================================

# CosineAnnealingLR: 余弦退火，lr 按余弦曲线平滑降到接近 0; 比 StepLR 更平滑效果更好
# T_max=100: 余弦周期=100 epoch，与 max_epochs 一致，训练结束时 lr 降到最低点
# CosineAnnealingLR: Cosine annealing, lr smoothly decreases following cosine curve; smoother than StepLR
# T_max=100: Cosine period = 100 epochs, matches max_epochs, lr reaches minimum at training end
param_scheduler = dict(type='CosineAnnealingLR', by_epoch=True, T_max=100)

# ============================================================
# 训练配置 / Training Configuration
# ============================================================

# by_epoch=True: 按 epoch 计数（大数据集可按 iteration）
# max_epochs=100: 训练 100 轮; 小数据集~1000 张足够收敛，再多容易过拟合
# val_interval=10: 每 10 epoch 验证一次; 平衡验证频率和训练速度
# by_epoch=True: Count by epoch (large datasets may use iteration)
# max_epochs=100: Train 100 epochs; ~1000 images sufficient to converge, more risks overfitting
# val_interval=10: Validate every 10 epochs; balances evaluation frequency and training speed
train_cfg = dict(by_epoch=True, max_epochs=100, val_interval=10)
val_cfg = dict()

# ============================================================
# 运行时钩子 / Runtime Hooks
# ============================================================

default_hooks = dict(
    # CheckpointHook: 每 10 epoch 保存权重; 100 epochs 共 10 次，可回溯最佳模型
    # CheckpointHook: Save weights every 10 epochs; 10 saves total, allows selecting best model
    checkpoint=dict(type='CheckpointHook', interval=10),
    # LoggerHook: 每 10 iteration 打印 loss; 太频繁刷屏，太少看不到进度
    # LoggerHook: Print loss every 10 iterations; too frequent clutters output, too rare loses visibility
    logger=dict(type='LoggerHook', interval=10),
)

# 工作目录：权重文件和日志保存位置
# Work directory: where checkpoints and logs are saved
work_dir = './work_dirs/resnet18_flowers17'

# ============================================================
# 测试配置 / Test Configuration
# ============================================================
# 复用验证配置; ImageClassificationInferencer 需要 test_dataloader，不设会 KeyError
# Reuse validation config; ImageClassificationInferencer requires test_dataloader, missing causes KeyError
test_cfg = dict()
test_dataloader = val_dataloader
test_evaluator = val_evaluator
