# ResNet-18 Configuration File Explanation

## Overview

This configuration file defines everything needed to train a ResNet-18 image classification model on the Oxford Flowers 17 dataset using the mmpretrain framework. The file is structured into the following sections:

---

## 1. Base Configs (`_base_`)

```python
_base_ = [
    'mmpretrain::_base_/models/resnet18.py',
    'mmpretrain::_base_/default_runtime.py',
]
```

- `resnet18.py`: Defines the default ResNet-18 network architecture (backbone, neck, head). We inherit this and override only the parts we need to change.
- `default_runtime.py`: Provides standard runtime settings such as logging, random seed, and resume-from-checkpoint support.
- **Why inherit?** Avoids writing hundreds of lines from scratch. We only override task-specific settings (e.g., `num_classes`, optimizer).

---

## 2. Model Architecture

```python
model = dict(
    type='ImageClassifier',
    backbone=dict(type='ResNet', depth=18, num_stages=4, out_indices=(3,), style='pytorch'),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='LinearClsHead',
        num_classes=17,
        in_channels=512,
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        topk=(1, 5),
    ),
)
```

### 2.1 `type='ImageClassifier'`

The top-level model type. This tells mmpretrain to build an image classification model with three sub-modules: backbone, neck, and head.

### 2.2 Backbone — `ResNet`

**What it does:** The backbone is the **feature extractor**. It takes the raw input image (224×224×3 pixels) and transforms it through multiple convolutional layers into a high-level feature map (7×7×512).

**How it works:**
- Uses **residual connections** (skip connections) that add the input of a layer block to its output, allowing gradients to flow directly through the network and enabling deeper architectures.
- Each stage doubles the channels and halves the spatial resolution.
- Early layers detect low-level features (edges, colors). Deeper layers capture high-level semantics (shapes, object parts).

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `type` | `'ResNet'` | Use ResNet architecture |
| `depth` | `18` | Number of layers. Options: 18/34/50/101/152. Chose 18 because: (1) assignment requirement, (2) fewer parameters (~11M), suitable for small dataset (~1000 images). Deeper networks risk overfitting on small data. |
| `num_stages` | `4` | ResNet has exactly 4 stages (conv2_x through conv5_x). This is the standard ResNet architecture and cannot be changed. |
| `out_indices` | `(3,)` | Output only from the 4th stage (0-indexed). Classification needs only the deepest semantic features. Object detection would need multi-level features (e.g., FPN). |
| `style` | `'pytorch'` | Padding style for convolutions. PyTorch and Caffe differ in how padding is handled at stride=2. We use PyTorch since that's our framework. |

**Data flow through stages:**

| Stage | Output Size | What It Learns |
|-------|------------|----------------|
| Conv1 | 56×56×64 | Basic edges and color changes |
| Stage1 | 56×56×64 | Simple textures (stripes, spots) |
| Stage2 | 28×28×128 | Complex textures (petal veins, leaf patterns) |
| Stage3 | 14×14×256 | Local parts (petal shapes, pistils) |
| Stage4 | 7×7×512 | Overall semantics ("this is a flower structure") |

### 2.3 Neck — `GlobalAveragePooling`

**What it does:** Compresses the backbone's spatial feature map into a 1D vector.

- Input: 7×7×512 (feature map with 512 channels, each 7×7 pixels)
- Operation: Average all 49 values (7×7) in each channel
- Output: 512-dimensional vector

**Why?** Removes spatial information ("where"), keeps only feature presence ("what"). Also dramatically reduces parameters compared to flattening (7×7×512 = 25,088 → 512).

### 2.4 Head — `LinearClsHead`

**What it does:** A single fully connected (linear) layer that maps the feature vector to class scores.

- Input: 512-dim vector
- Output: 17 scores (one per flower category)
- Operation: `y = W × x + b` where W is a (17, 512) weight matrix

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `num_classes` | `17` | Oxford Flowers 17 has 17 flower categories. Output dimension = 17. |
| `in_channels` | `512` | Must match backbone's last layer output channels. ResNet-18 stage4 outputs 512 channels (ResNet-50 would be 2048, MobileNet V2 is 1280). |
| `CrossEntropyLoss` | `loss_weight=1.0` | Standard multi-class loss function. Applies softmax to convert raw scores into probabilities, then computes -log(probability of correct class). Lower loss = better prediction. `loss_weight=1.0` because there is only one loss term. |
| `topk` | `(1, 5)` | Metrics computed during training. Top-1: is the highest score the correct class? Top-5: is the correct class among the top 5 predictions? |

---

## 3. Data Preprocessor

```python
data_preprocessor = dict(
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    to_rgb=True,
)
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `mean` | `[123.675, 116.28, 103.53]` | RGB channel means computed from 1.2 million ImageNet images. Each pixel is normalized: `pixel = (pixel - mean) / std`. |
| `std` | `[58.395, 57.12, 57.375]` | RGB channel standard deviations from ImageNet. |
| `to_rgb` | `True` | OpenCV reads images as BGR by default. This converts to RGB to match the expected input format. |

**Why use ImageNet values?** Standardizes input distribution so the model receives consistent data. Same values as MobileNet V2 to ensure fair comparison.

---

## 4. Training Data Pipeline

```python
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='RandomResizedCrop', scale=224, backend='pillow'),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(type='PackInputs'),
]
```

| Step | Type | Parameters | What It Does |
|------|------|------------|-------------|
| 1 | `LoadImageFromFile` | — | Reads the image file from disk into memory. Required first step. |
| 2 | `RandomResizedCrop` | `scale=224, backend='pillow'` | Randomly selects a region of the image, then resizes it to 224×224. This is the most critical data augmentation — simulates different viewing distances and compositions. `scale=224` is the ImageNet standard input size. `backend='pillow'` for better interpolation quality. |
| 3 | `RandomFlip` | `prob=0.5, direction='horizontal'` | Flips the image horizontally with 50% probability. Flowers are naturally left-right symmetric, so horizontal flip is valid. Vertical flip is not used because upside-down flowers are unnatural. |
| 4 | `PackInputs` | — | Converts the processed image into tensor format for the model. Required last step. |

**Why data augmentation?** The dataset has only ~60 images per class. Without augmentation, the model would quickly memorize the training images (overfitting). Augmentation creates variations, forcing the model to learn general features.

---

## 5. Validation Data Pipeline

```python
val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='ResizeEdge', scale=256, edge='short', backend='pillow'),
    dict(type='CenterCrop', crop_size=224),
    dict(type='PackInputs'),
]
```

| Step | Type | Parameters | What It Does |
|------|------|------------|-------------|
| 1 | `LoadImageFromFile` | — | Read image from disk. |
| 2 | `ResizeEdge` | `scale=256, edge='short'` | Resize the short edge to 256 pixels, scale long edge proportionally. Ensures the image is large enough for cropping. |
| 3 | `CenterCrop` | `crop_size=224` | Crop a 224×224 region from the center. No randomness — guarantees reproducible evaluation results every time. |
| 4 | `PackInputs` | — | Pack into tensor format. |

**Why no random augmentation?** Validation must be deterministic. The same image must produce the same result every time, so we can fairly track model improvement across epochs.

---

## 6. DataLoader

```python
train_dataloader = dict(
    batch_size=32,
    num_workers=4,
    dataset=dict(type='CustomDataset', data_prefix='data/flowers17/train',
                 with_label=True, pipeline=train_pipeline),
    sampler=dict(type='DefaultSampler', shuffle=True),
)
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `batch_size` | `32` | Number of images processed per iteration. 32 fits in RTX 4060 (8GB). Larger batches on small datasets can hurt generalization. |
| `num_workers` | `4` | Number of subprocesses loading data in parallel. Speeds up data loading. Typically set to half the CPU core count. |
| `CustomDataset` | — | A generic dataset class that automatically infers class labels from subfolder names. e.g., `train/Tulip/001.jpg` → label "Tulip". |
| `data_prefix` | `'data/flowers17/train'` | Root directory of training images. |
| `with_label` | `True` | Automatically extract labels from subfolder names. |
| `shuffle` | `True` (train) / `False` (val) | Training: shuffle every epoch to prevent the model from memorizing data order. Validation: no shuffle for reproducibility. |

---

## 7. Evaluator

```python
val_evaluator = dict(type='Accuracy', topk=(1, 5))
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `type` | `'Accuracy'` | Compute classification accuracy on the validation set. |
| `topk` | `(1, 5)` | Top-1: percentage of images where the highest-scoring class is correct. Top-5: percentage where the correct class is in the top 5 predictions. |

---

## 8. Optimizer

```python
optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0001),
)
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `type` | `'SGD'` | Stochastic Gradient Descent. The original ResNet paper uses SGD. CNNs typically generalize better with SGD than adaptive optimizers like Adam. |
| `lr` | `0.01` | Initial learning rate. 10× smaller than the ImageNet standard (0.1) because small datasets with too large lr cause gradient oscillation and divergence. |
| `momentum` | `0.9` | Momentum factor (classic value). Accelerates updates in consistent gradient directions and dampens oscillation. Current gradient contributes 10%, historical direction contributes 90%. |
| `weight_decay` | `0.0001` | L2 regularization coefficient. Penalizes large weights to prevent overfitting. Standard value. |

---

## 9. Learning Rate Scheduler

```python
param_scheduler = dict(type='CosineAnnealingLR', by_epoch=True, T_max=100)
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `type` | `'CosineAnnealingLR'` | Learning rate decreases following a cosine curve. Smoother than step decay (StepLR), generally leads to better convergence. |
| `by_epoch` | `True` | Adjust learning rate once per epoch (not per iteration). |
| `T_max` | `100` | One full cosine cycle = 100 epochs. Matches `max_epochs` so lr reaches its minimum at the end of training. |

---

## 10. Training Configuration

```python
train_cfg = dict(by_epoch=True, max_epochs=100, val_interval=10)
val_cfg = dict()
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `by_epoch` | `True` | Count training progress by epochs (one pass through the entire dataset). |
| `max_epochs` | `100` | Train for 100 epochs. With ~1000 images, 100 epochs is sufficient to converge without severe overfitting. |
| `val_interval` | `10` | Run validation every 10 epochs. Balances evaluation frequency and training speed. |

---

## 11. Runtime Hooks

```python
default_hooks = dict(
    checkpoint=dict(type='CheckpointHook', interval=10),
    logger=dict(type='LoggerHook', interval=10),
)
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `CheckpointHook` | `interval=10` | Save model weights every 10 epochs. Creates 10 checkpoints total. Allows selecting the best-performing model afterwards. |
| `LoggerHook` | `interval=10` | Print training loss every 10 iterations. Provides visibility into training progress without cluttering the output. |

---

## 12. Work Directory

```python
work_dir = './work_dirs/resnet18_flowers17'
```

Directory where all training outputs are saved: checkpoints (.pth files), logs, and config backups. Separate from MobileNet V2's work directory to avoid overwriting.

---

## 13. Test Configuration

```python
test_cfg = dict()
test_dataloader = val_dataloader
test_evaluator = val_evaluator
```

Reuses the validation settings for testing. Required by mmpretrain's `ImageClassificationInferencer` — without these, inference would raise a KeyError.
