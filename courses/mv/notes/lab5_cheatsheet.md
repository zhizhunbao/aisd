# Lab 5 — CNN (Convolutional Neural Network, 卷积神经网络) 概念速查

> **See also:** [lab5_math.md](lab5_math.md) · [lab5_code.md](lab5_code.md) · [Lab 文档](../labs/CST8508_Lab5.md) · [输出解读](lab5_output_guide.md)
>
> ❌ 本文件不含公式、不含代码 — 仅概念定义、要点和对比

---

## 📖 核心定义（Definitions）

### CNN (Convolutional Neural Network, 卷积神经网络)
- A neural network architecture that uses **convolutional layers** to automatically learn spatial features from images — 使用卷积层从图像中自动学习空间特征的神经网络架构
- Designed specifically for grid-structured data (images, audio spectrograms) — 专为网格结构数据设计
- Key advantage: **parameter sharing** (共享参数) — same filter applied across the entire image reduces parameter count vs fully-connected

### Convolutional Layer (卷积层) — `Conv2d`
- Applies a learnable **filter/kernel** (滤波器/卷积核) that slides over the input, computing dot products — 可学习的滤波器在输入上滑动，计算点积
- Learns local spatial patterns (edges, textures, shapes) — 学习局部空间特征
- Parameters: number of filters, kernel size, padding, stride

### MaxPooling Layer (最大池化层) — `MaxPool2d`
- Downsamples (downscales) feature maps by taking the **maximum value** in each window — 在每个窗口中取最大值，对特征图进行下采样
- Purpose: reduce spatial dimensions, introduce translation invariance (平移不变性) — 降低空间维度，引入平移不变性
- No learnable parameters — 无可学习参数

### Flatten (展平)
- Converts 3D feature maps (C × H × W) into a 1D vector before fully-connected layers — 将三维特征图展平为一维向量
- Required to bridge convolutional layers and dense layers — 连接卷积层和全连接层的必要步骤

### Fully-Connected Layer (全连接层) — `Linear` / Dense
- Every input node connects to every output node — 每个输入节点连接到每个输出节点
- Learns global combinations of extracted features — 学习提取特征的全局组合
- High parameter count — 参数量大

### Dropout (随机丢弃)
- During training, randomly sets a fraction of activations to zero with probability `p` — 训练时以概率 `p` 随机将激活值置零
- Purpose: prevent overfitting (过拟合) by reducing co-adaptation between neurons — 减少神经元间的共适应，防止过拟合
- At inference time: scaled proportionally, dropout is disabled — 推理时禁用，激活值按比例缩放
- ⚠️ `model.train()` enables dropout; `model.eval()` disables it

### ReLU (Rectified Linear Unit, 线性整流函数)
- Activation function: $f(x) = \max(0, x)$ — 激活函数，负数归零，正数不变
- Solves vanishing gradient (梯度消失) problem better than sigmoid/tanh — 比 sigmoid/tanh 更好地解决梯度消失问题
- Computationally efficient — 计算高效

### CrossEntropyLoss (交叉熵损失)
- Loss function for multi-class classification — 多类分类的损失函数
- Combines `LogSoftmax + NLLLoss` internally — 内部合并了 LogSoftmax 和负对数似然损失
- ⚠️ Input: raw logits (NOT softmax probabilities) — 输入必须是原始 logit，不是 softmax 概率

### Adam Optimizer (自适应矩估计优化器)
- Adaptive learning rate optimizer that computes per-parameter learning rates — 为每个参数计算自适应学习率
- Combines momentum (动量) and RMSProp ideas — 结合了动量和 RMSProp 思想
- Default `lr=1e-3` works well for most problems — 默认学习率通常效果良好

### Data Augmentation (数据增强)
- Artificially expand training set by applying random transformations to images — 通过随机变换扩大训练集
- Reduces overfitting by exposing model to varied versions of training images — 让模型接触更多变化，减少过拟合
- Applied only to training data, NOT test data — 只对训练数据应用，测试数据不增强

### ImageNet Normalization (ImageNet 标准化)
- Mean: `[0.485, 0.456, 0.406]`, Std: `[0.229, 0.224, 0.225]` for RGB channels
- Standard values derived from the ImageNet dataset — 从 ImageNet 数据集得出的标准值
- Helps models converge faster when using pretrained features — 使用预训练特征时加速收敛

---

## 💡 关键要点（Key Points）

### 数据流（Data Flow）
1. Raw images → `ImageFolder` reads class from folder name (folder = class label) — 文件夹名即为类别标签
2. Transform pipeline applied: Resize → Augment (train only) → ToTensor → Normalize
3. `DataLoader` batches data and shuffles training set
4. Model ingests batched tensors → computes logits → loss computed against labels

### 训练循环要点（Training Loop Essentials）
- `optimizer.zero_grad()` must be called before each backward pass — 每次反向传播前必须清零梯度
- `loss.backward()` computes gradients — 计算梯度
- `optimizer.step()` updates parameters — 更新参数
- `model.train()` / `model.eval()` must be set appropriately — 训练/评估模式必须正确切换

### GPU 使用（GPU Usage）
- `torch.device("cuda")` uses GPU; `"cpu"` uses CPU
- All tensors AND the model must be moved to the same device — 张量和模型必须在同一设备上
- `.to(DEVICE)` moves tensors; `.to(DEVICE)` also works for model

### 数据集划分（Dataset Split）
- Lab uses random shuffle with fixed seed (`random.seed(42)`) for reproducibility — 固定随机种子保证可复现性
- 80% train / 20% test split — 训练/测试 8:2 分割
- `Subset` is used to create views of the original dataset — 使用 `Subset` 创建数据集视图，不复制数据

---

## ⚠️ 常见陷阱（Common Traps）

| 陷阱 | 错误做法 | 正确做法 | 来源 |
|------|---------|---------|------|
| Dropout 模式未切换 | 推理时忘记 `model.eval()` | 评估前调用 `model.eval()`，训练前调用 `model.train()` | lab |
| 梯度累积 | 未调用 `optimizer.zero_grad()` | 每个 batch 前必须清零梯度 | lab |
| 测试集增强 | 对测试集也用随机翻转、旋转 | 测试集只做 Resize + ToTensor + Normalize | lab |
| 设备不一致 | 模型在 CPU，张量在 GPU | 模型和张量必须在同一 device | lab |
| CrossEntropyLoss 输入 | 传入 softmax 概率 | 传入原始 logits（未经 softmax）| lab |
| Epoch 1 val_acc > train_acc | 误判为 bug | 正常现象：训练用了增强（更难），测试未增强 | lab |
| 损坏图片 | 跳过清理步骤 | 'cat' 数据集含损坏 JPEG，需预先清除 | lab |

---

## 📊 对比表（Comparison Tables）

### 训练集 vs 测试集变换对比

| 变换 | 训练集 | 测试集 | 原因 |
|------|--------|--------|------|
| `Resize((128,128))` | ✅ | ✅ | 统一输入尺寸 |
| `RandomHorizontalFlip()` | ✅ | ❌ | 增强：测试集不增强，避免评估偏差 |
| `RandomRotation(15)` | ✅ | ❌ | 增强：测试集不增强 |
| `ToTensor()` | ✅ | ✅ | PIL→Tensor 必须 |
| `Normalize(...)` | ✅ | ✅ | 统一像素值范围 |

### model.train() vs model.eval() 行为对比

| 行为 | `model.train()` | `model.eval()` |
|------|----------------|----------------|
| Dropout | ✅ 随机丢弃激活值 | ❌ 禁用，输出缩放补偿 |
| BatchNorm | 用当前 batch 统计值 | 用训练时的移动平均值 |
| 梯度计算 | 通常需要 | 通常需要 `torch.no_grad()` |
| 使用场景 | 训练循环 | 验证/推理 |

### CNN vs 全连接网络（Fully-Connected Network）对比

| 维度 | CNN (卷积神经网络) | FC Network (全连接网络) |
|------|----------|----------|
| 输入方式 | 保留空间结构 (H×W×C) | 展平为 1D 向量 |
| 参数量 | 少（权重共享） | 多（每连接独立权重） |
| 局部特征 | ✅ 自动学习 | ❌ 需手工设计 |
| 平移不变性 | ✅ 池化层提供 | ❌ 无 |
| 适用数据 | 图像、时序 | 表格、嵌入向量 |

### 评估指标对比（Precision vs Recall）

| 指标 | 公式 | 强调方向 | 适用场景 |
|------|------|---------|---------|
| Precision (精确率) | TP/(TP+FP) | 降低误报 | 垃圾邮件过滤（误判代价高）|
| Recall (召回率) | TP/(TP+FN) | 降低漏报 | 疾病检测（漏报代价高）|
| F1-Score | 2×P×R/(P+R) | 综合平衡 | 类别不平衡时 |
| Accuracy | (TP+TN)/总数 | 整体正确率 | 类别平衡时 |

---

## 🔗 SimpleCNN 架构速览

```
Input:  3 × 128 × 128  (RGB image — RGB 图像)
     ↓ Conv2d(3→32)  + ReLU + MaxPool2d       → 32 × 64 × 64
     ↓ Conv2d(32→64) + ReLU + MaxPool2d       → 64 × 32 × 32
     ↓ Conv2d(64→128)+ ReLU + MaxPool2d       → 128 × 16 × 16
     ↓ Flatten                                 → 32,768
     ↓ Linear(32768→256) + ReLU + Dropout(0.5)→ 256
     ↓ Linear(256→2)                           → 2 (Cat logit, Dog logit)
Output: argmax → class prediction (0=Cat, 1=Dog)
```
