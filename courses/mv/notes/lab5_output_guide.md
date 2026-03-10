# Lab 5 实验代码输出解读

> **先读后跑：** 在运行 Lab 5 代码之前先阅读本文档，了解每一行输出的含义，运行后才能立刻读懂数字，无需边跑边查文档。  
> **Lab 文档：** [CST8508_Lab5.md](../labs/CST8508_Lab5.md)

---

## §1 读懂数据加载输出

### 1.1 设备检测（Dataset Setup）

**实际输出：**

```
Using device: cuda
```

**读法：**
- `cuda` → 检测到 NVIDIA GPU，训练将在 GPU 上进行，速度快（通常 10-30x 提升）
- `cpu` → 没有检测到 GPU，训练在 CPU 上进行，速度慢，10 epochs 可能需要数十分钟

**这里的数据说明什么：** 实验运行时使用了 GPU，这是 CNN 训练的推荐配置。

---

### 1.2 数据集加载信息（`load_dataset` 输出）

**实际输出：**

```
Zip / dataset already present, skipping download.
Removed 0 corrupted images.
Dataset ready at: C:\...\PetImages
Train: 19998  Test: 5000  Classes: ['Cat', 'Dog']
```

**读法：**

| 字段 | 含义 | 说明 |
|------|------|------|
| `Train: 19998` | 训练集样本数 | 总样本 × 80% split ratio ≈ 19998 |
| `Test: 5000` | 测试集样本数 | 总样本 × 20% ≈ 5000 |
| `Classes: ['Cat', 'Dog']` | 类别标签列表 | 索引 0 = Cat，索引 1 = Dog |

**为什么 Removed 0：** 数据集中的损坏图片在首次运行时已被清除；再次运行时不会重新发现损坏文件，所以输出 `0`。

**为什么 80/20 分割：** 80% 训练是经验法则，保证模型有足够样本学习特征，20% 测试保证评估结果有统计意义（5000 张图足够区分偶然误差）。

---

## §2 读懂训练过程输出

### 2.1 逐 Epoch 训练日志（`train_model` 输出）

**实际输出：**

```
Epoch [01/10]  train_loss=0.6392  train_acc=0.6245  val_loss=0.5441  val_acc=0.7272
Epoch [02/10]  train_loss=0.5251  train_acc=0.7399  val_loss=0.4814  val_acc=0.7734
Epoch [03/10]  train_loss=0.4643  train_acc=0.7849  val_loss=0.4534  val_acc=0.7886
Epoch [04/10]  train_loss=0.4172  train_acc=0.8099  val_loss=0.3730  val_acc=0.8368
Epoch [05/10]  train_loss=0.3869  train_acc=0.8283  val_loss=0.3536  val_acc=0.8498
Epoch [06/10]  train_loss=0.3607  train_acc=0.8413  val_loss=0.3382  val_acc=0.8592
Epoch [07/10]  train_loss=0.3387  train_acc=0.8548  val_loss=0.3050  val_acc=0.8736
Epoch [08/10]  train_loss=0.3162  train_acc=0.8613  val_loss=0.2999  val_acc=0.8742
Epoch [09/10]  train_loss=0.3018  train_acc=0.8717  val_loss=0.2863  val_acc=0.8770
Epoch [10/10]  train_loss=0.2863  train_acc=0.8809  val_loss=0.2727  val_acc=0.8842
```

**每个字段的含义：**

| 字段 | 值域 | 如何判断好/坏 | 本实验读法 |
|------|------|--------------|-----------|
| `train_loss` | [0, +∞)，越小越好 | <0.3 较好，>1.0 表示欠拟合 | 从 0.64 降到 0.29，说明模型在持续学习 |
| `train_acc` | [0, 1]，越大越好 | >0.85 对二分类较好 | 从 62% 升到 88%，训练效果显著 |
| `val_loss` | [0, +∞)，越小越好 | 应与 train_loss 接近，否则过拟合 | 从 0.54 降到 0.27，与 train_loss 接近，无明显过拟合 |
| `val_acc` | [0, 1]，越大越好 | 应接近 train_acc | 从 72% 升到 88%，与训练准确率差距约 0%，泛化良好 |

**关键观察：**

1. **Epoch 1의 val_acc (0.7272) > train_acc (0.6245)：** 这看起来反直觉，实际上是因为：
   - 训练集使用了数据增强（随机翻转、旋转），增强后的图片更难分类，导致训练 loss 偏高
   - 测试集没有增强操作，相对更"容易"，所以 Epoch 1 测试准确率反而更高
   - **这是数据增强的正常现象，不是 bug**

2. **Loss 单调下降：** 10 个 epoch 内 train_loss 和 val_loss 均持续下降，说明还未到收敛上限，继续训练可能进一步提升精度。

3. **val_loss < train_loss：** 整个训练过程中验证 loss 始终低于训练 loss（同样因为增强），模型没有出现过拟合。

---

## §3 读懂评估输出

### 3.1 总体准确率（`evaluate_and_predict` 输出第一行）

**实际输出：**

```
Accuracy: 0.8842
```

**读法：**
- **值域：** [0, 1]
- **含义：** 5000 张测试图中，88.42% 被正确分类
- **如何判断好/坏：**
  - >0.95：极好（通常需要更深的网络或预训练）
  - **0.85–0.95：较好（本实验 0.88 落在此区间）**
  - 0.70–0.85：可接受
  - <0.70：通常意味着模型或数据有问题

**这里的数据说明什么：** 一个仅有 3 个卷积层、从零训练 10 个 epoch 的简单 CNN 达到 88.42%，对于二分类猫狗任务来说是不错的基线结果。

---

### 3.2 分类报告（Classification Report）

**实际输出：**

```
              precision    recall  f1-score   support

         Cat       0.90      0.86      0.88      2478
         Dog       0.87      0.91      0.89      2522

    accuracy                           0.88      5000
   macro avg       0.89      0.88      0.88      5000
weighted avg       0.88      0.88      0.88      5000
```

**逐行解读：**

#### Cat 行

| 指标 | 值 | 含义 |
|------|-----|------|
| `precision = 0.90` | 精确率 90% | 当模型说"这是猫"时，有 90% 真的是猫（误报率低） |
| `recall = 0.86` | 召回率 86% | 所有真实的猫中，模型识别出了 86%（漏报率 14%） |
| `f1-score = 0.88` | F1 值 88% | precision 和 recall 的调和平均，综合两者 |
| `support = 2478` | 支持数 | 测试集中猫的图片总数 |

**解读：** 模型识猫时比较保守——倾向于"宁可认错，不要误报"，所以精确率高（0.90）但召回率略低（0.86）。

#### Dog 行

| 指标 | 值 | 含义 |
|------|-----|------|
| `precision = 0.87` | 精确率 87% | 当模型说"这是狗"时，有 87% 真的是狗 |
| `recall = 0.91` | 召回率 91% | 所有真实的狗中，模型识别出了 91% |
| `f1-score = 0.89` | F1 值 89% | |
| `support = 2522` | 支持数 | 测试集中狗的图片总数 |

**解读：** 模型识狗时更积极——倾向于"多认狗，少漏狗"，所以召回率高（0.91）但精确率略低（0.87）。

#### 汇总行

| 行 | 含义 |
|----|------|
| `accuracy = 0.88` | 所有类别整体正确率（与前一行 Accuracy 输出一致） |
| `macro avg = 0.89/0.88/0.88` | Cat 和 Dog 两行的**简单平均**（不考虑样本数量） |
| `weighted avg = 0.88/0.88/0.88` | Cat 和 Dog 两行的**加权平均**（按 support 加权）；样本均衡时与 macro avg 接近 |

**为什么 macro avg ≠ weighted avg：** Cat 2478 张，Dog 2522 张，样本稍不平衡，但差异很小（<2%），所以两行结果几乎相同。

**整体解读：**

- 猫狗识别准确率均在 88%–91% 区间，模型没有明显偏向某一类别（没有 class imbalance 问题）
- Cat precision > Dog precision，Cat 的"假阳性"更少
- Dog recall > Cat recall，狗的"漏检"更少
- 如果实际应用中"漏检狗"代价更高（如宠物识别系统），则本模型对狗类的召回率（91%）是优势

---

## 参考

- Lab 文档：[CST8508_Lab5.md](../labs/CST8508_Lab5.md)
- 相关笔记：[week4_cnn_intro_slides.md](week4_cnn_intro_slides.md) — CNN 基础
- 相关笔记：[week5_deep_learning_slides.md](week5_deep_learning_slides.md) — 深度学习训练
