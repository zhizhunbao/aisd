# 🎬 Assignment 1 故事线：从零训练一个花卉分类器

> **课程:** CST8508 Machine Vision | **主题:** mmpretrain 图像分类实战  
> **核心问题:** 给你 1360 张花的照片，如何让计算机自动识别花的种类？  
> **数学前置：** [卷积运算](../../math/general/convolution.md) | [交叉熵](../../math/probability/cross_entropy.md) | [梯度下降](../../math/optimization/gradient_descent.md) | [链式法则](../../math/calculus/chain_rule_gradients.md)

---

## 📍 路线图（Roadmap）

```
问题提出          数据准备           模型选择            训练策略            评估反思
  │                │                  │                  │                  │
  ▼                ▼                  ▼                  ▼                  ▼
"怎么让电脑     "数据怎么组织     "用什么网络？      "怎么训练？         "训练得好不好？
 认识花？"       才能喂给模型？"    参数多=好？"       学习率怎么变？"      哪些花容易搞混？"
  │                │                  │                  │                  │
  ▼                ▼                  ▼                  ▼                  ▼
深度学习         SubFolder格式     ResNet-18 vs        SGD vs Adam        Accuracy, F1
图像分类         + 数据增强        MobileNet V2        + 余弦退火         + 混淆矩阵
```

---

## 第一幕：问题 —— 怎么让电脑认花？

### 场景设定

你拿到 1360 张照片，分布在 17 种花卉类别中（Daisy、Sunflower、Tulip……）。每类大约 80 张。人类一眼就能区分向日葵和雏菊，但怎么让计算机也学会？

### 为什么不能用传统方法？

| 方法                             | 问题                                 |
| -------------------------------- | ------------------------------------ |
| 手写规则（"黄色+大圆盘=向日葵"） | 规则太多、太脆弱，换个角度就失效     |
| 传统特征提取（SIFT/HOG + SVM）   | Week 3 学过，对复杂场景效果有限      |
| **深度学习（CNN）**              | ✅ 自动学习特征，Week 4-5 刚学的技术 |

**结论：** CNN 可以从像素自动学习"什么特征区分不同花"——但我们不想从零写训练代码。有没有现成的工具？

---

## 第二幕：工具 —— OpenMMLab 让你专注于"做实验"而非"写代码"

### 问题：从零写 CNN 训练代码太复杂

如果自己写，需要处理：数据加载、数据增强、模型定义、损失函数、优化器、学习率调度、检查点保存、日志记录、GPU 管理……

### 解决方案：OpenMMLab 的"配置驱动"理念

OpenMMLab（mmpretrain）把所有这些**模块化**了：

```
你需要做的：
  1. 写一个配置文件（.py）—— 声明"我要什么模型、什么数据、什么优化器"
  2. 运行一条命令 —— python tools/train.py config.py

框架帮你做的：
  ✓ 自动加载模型结构（从注册表）
  ✓ 自动构建数据管道（加载 → 增强 → 打包）
  ✓ 自动训练循环（前向 → 损失 → 反向 → 更新）
  ✓ 自动保存检查点和日志
```

> **类比：** mmpretrain 之于 CNN 训练，就像 sklearn 之于传统 ML——你不需要手写梯度下降，只需要调用 `fit()`。

### 为什么选 mmpretrain 而不是直接用 PyTorch？

| 方面       | 纯 PyTorch         | mmpretrain                                    |
| ---------- | ------------------ | --------------------------------------------- |
| 代码量     | 几百行训练循环     | 一个配置文件                                  |
| 换模型     | 重写模型定义       | 改一行 `type='ResNet'` → `type='MobileNetV2'` |
| 可复现性   | 取决于你的代码习惯 | 配置文件即完整实验记录                        |
| 预定义模型 | 自己实现           | 100+ 预训练模型可选                           |

**但工具选好了，数据怎么准备？**

---

## 第三幕：数据 —— 从 1360 张散装照片到可训练的格式

### 问题：原始数据只是一堆编号图片

Oxford Flowers 17 下载后只有一个 `jpg/` 文件夹，里面是 `image_0001.jpg` 到 `image_1360.jpg`——没有类别标签！

### 解决方案：SubFolder 格式

mmpretrain 的 `CustomDataset` 支持最简单的组织方式——把图片放到以类名命名的子文件夹中：

```
之前（问题）：                之后（解决）：
jpg/                          data/flowers17/
├── image_0001.jpg            ├── train/
├── image_0002.jpg            │   ├── Bluebell/
├── ...                       │   │   ├── image_0001.jpg
└── image_1360.jpg            │   │   └── ...
                              │   ├── Daisy/
没有标签！                     │   └── ...
                              └── val/
                                  ├── Bluebell/
                                  └── ...
                                  类名 = 文件夹名！
```

### 为什么要分 train/val？

- **训练集（80%）：** 模型从中学习特征
- **验证集（20%）：** 评估模型在没见过的数据上的表现
- 如果不分开 → 模型可能"死记硬背"训练数据但无法泛化

### 额外挑战：小数据集

每类只有 ~60 张训练图片！这远少于 ImageNet 的每类 1000+ 张。

**对策：数据增强**——通过随机裁剪、翻转等手段"生成"更多训练样本：

```
原图 → RandomResizedCrop(224) → 模拟不同拍摄距离
     → RandomFlip(prob=0.5)   → 模拟不同拍摄角度

同一张图每个 epoch 看到的都不一样 → 相当于数据量翻了好几倍
```

**数据准备好了，该选什么模型来训练？**

---

## 第四幕：模型选择 —— "大"模型 vs "小"模型，谁更强？

### 实验设计：公平对比两个模型

| 维度     | ResNet-18（"大"）   | MobileNet V2（"小"）    |
| -------- | ------------------- | ----------------------- |
| 参数量   | ~11.7M              | ~3.4M                   |
| 核心技术 | 标准卷积 + 残差连接 | 深度可分离卷积 + 倒残差 |
| 设计目标 | 准确率优先          | 效率优先（手机/嵌入式） |

### ResNet-18：靠"深度"和"捷径"学习

**核心创新 —— 残差连接（Skip Connection）：**

```
问题：网络越深，梯度越容易消失（vanishing gradient）
     最深处的层几乎学不到任何东西

解决：让输入直接"跳过"一些层，加到输出上
     即使中间层学得不好，至少信息不会丢失

     x → [Conv → BN → ReLU → Conv → BN] → (+x) → ReLU → y
          \_________________________/          ↗
                 学到的"残差"            原始信息直通
```

### MobileNet V2：靠"拆分卷积"省参数

**核心创新 —— 深度可分离卷积：**

```
标准卷积（ResNet 用的）：
  一个滤波器同时处理所有通道
  参数量 = K×K × C_in × C_out
  例：3×3 × 64 × 128 = 73,728 个参数

深度可分离卷积（MobileNet 用的）：
  步骤1：每个通道单独卷积（深度卷积）
  步骤2：用 1×1 卷积混合通道信息（逐点卷积）
  参数量 = K×K × C_in + C_in × C_out
  例：3×3 × 64 + 64 × 128 = 576 + 8,192 = 8,768 个参数

  节省了 88%！
```

### 直觉预期 vs 实际结果

```
直觉预期：                          实际结果：
   "参数多 = 表达能力强              MobileNet V2: 90.07% ✅ 赢了！
    = 更准确"                        ResNet-18:    77.21% ❌
    ResNet-18 应该赢？               参数少的反而更好？！
```

**这是怎么回事？→ 答案在训练策略中。**

---

## 第五幕：训练策略 —— 优化器的选择比模型更重要？

### 实验的另一个变量：优化器不同

| 模型         | 优化器                 | 学习率 |
| ------------ | ---------------------- | ------ |
| ResNet-18    | **SGD** (momentum=0.9) | 0.01   |
| MobileNet V2 | **Adam**               | 0.001  |

### SGD vs Adam 的核心区别

```
SGD（随机梯度下降 + 动量）：
  W_new = W_old - lr × gradient + momentum × 上次的更新

  特点：
  ✓ 在大数据集上收敛到更好的解
  ✗ 需要精心调节 lr 和 momentum
  ✗ 对 lr 敏感——太大震荡，太小卡住

Adam（自适应矩估计）：
  为每个参数自适应调整学习率

  特点：
  ✓ 对超参数不敏感——默认值通常就够用
  ✓ 在小数据集上收敛更快更稳
  ✗ 有时候最终解不如 SGD 调好后的结果
```

### 为什么 Adam 在这里赢了？

```
小数据集效应（每类仅 60 张训练图片）：

SGD + ResNet-18：
  - 梯度噪声大（因为数据少，每个 batch 的统计量波动大）
  - SGD 对噪声更敏感 → 学习过程不稳定
  - 11.7M 参数 in 小数据集 → 过拟合风险高

Adam + MobileNet V2：
  - Adam 自动调节每个参数的学习率 → 对噪声更鲁棒
  - 3.4M 参数 → 模型容量匹配数据量
  - 更快收敛 + 更稳定
```

### 学习率调度：余弦退火（两个模型都用到）

```
学习率变化曲线 / LR Schedule:

lr  ↑ 0.01 ╮
    │       ╲
    │        ╲  缓慢下降
    │         ╲
    │          ╲
    │           ╲______
    └──────────────────→ epoch
    0     50        100

开始：大学习率 → 快速探索参数空间
结束：小学习率 → 精细调整最终结果
```

---

## 第六幕：评估 —— 不只看"总分"，还要看"哪里扣分"

### 总分只是第一步

Top-1 Accuracy 告诉你"整体对了多少"——但不告诉你"哪些花容易搞混"。

### 混淆矩阵揭示真相

```
             预测
           Daisy  Cowslip  Coltsfoot
真  Daisy  [16     0        0     ]  ← 完美！
实  Cowslip [ 0     8        6     ]  ← 经常被误判为 Coltsfoot
    Coltsf [ 0     4       12     ]  ← 也容易被误判为 Cowslip
```

**规律：** 视觉特征显著的花（Sunflower、Daisy）准确率高；视觉相似的花（Cowslip vs Coltsfoot）互相混淆。

### 评估指标全景

| 层次 | 指标             | 回答的问题                     |
| ---- | ---------------- | ------------------------------ |
| 整体 | Top-1 Accuracy   | 总共对了多少？                 |
| 整体 | Top-5 Accuracy   | 正确答案在前 5 个预测里吗？    |
| 每类 | Precision        | 我说是 X 类的，有多少真的是？  |
| 每类 | Recall           | X 类的花，我找到了多少？       |
| 综合 | F1-Score         | Precision 和 Recall 的平衡指标 |
| 全局 | Confusion Matrix | 哪些类别互相混淆？             |

---

## 第七幕：反思 —— 踩过的坑和学到的经验

### 坑 1：环境搭建（最大的时间消耗）

```
时间线：
  Day 1: 在 Google Colab 上尝试 → PyTorch 2.10+cu128 没有 mmcv wheel ❌
  Day 2: 在 Colab 上编译 mmcv → Python 3.12 不兼容 pkg_resources ❌
  Day 3: 切换到本地 WSL + conda → 按照官方教程一步步来 ✅

教训：不要和版本兼容性作斗争——直接用官方推荐的版本组合
```

### 坑 2：NumPy 版本冲突

```
问题：NumPy 2.x 和 PyTorch 2.1.2 不兼容 → 段错误（segfault）
尝试：手动降级 NumPy → 还是出错
解决：用 conda（而非 pip）管理包 → conda 自动处理二进制兼容性
```

### 坑 3：推理需要 test_dataloader

```
问题：ImageClassificationInferencer 需要 test_dataloader
     但我们的配置只定义了 train_dataloader 和 val_dataloader

解决：在配置末尾加一行
     test_dataloader = val_dataloader
     test_evaluator = val_evaluator
```

---

## 🎯 考试 Checklist

| #   | 知识点                             | 关键词                         |
| --- | ---------------------------------- | ------------------------------ |
| 1   | OpenMMLab 的核心设计理念           | 模块化、配置驱动、注册器       |
| 2   | SubFolder 数据格式的优势           | 无需标注文件、类名从文件夹推断 |
| 3   | ResNet 的核心创新                  | 残差连接 / Skip Connection     |
| 4   | MobileNet V2 的核心创新            | 深度可分离卷积 / 倒残差结构    |
| 5   | SGD vs Adam 在小数据集上的表现差异 | Adam 更鲁棒、SGD 需要细调      |
| 6   | 余弦退火学习率的工作原理           | 开始大、结束小、按余弦衰减     |
| 7   | 数据增强对小数据集的重要性         | RandomResizedCrop、RandomFlip  |
| 8   | Top-1 vs Top-5 Accuracy 的区别     | 第一名 vs 前五名               |
| 9   | Precision vs Recall 的区别         | "精准" vs "全面"               |
| 10  | 混淆矩阵的实际用途                 | 找出容易互相混淆的类别         |

---

## 📚 参考资料

- 教程文件: [assignment1_mmpretrain_tutorial.md](assignment1_mmpretrain_tutorial.md)
- 速查概念: [assignment1_mmpretrain_cheatsheet.md](assignment1_mmpretrain_cheatsheet.md)
- 速查公式: [assignment1_mmpretrain_math.md](assignment1_mmpretrain_math.md)
- 速查代码: [assignment1_mmpretrain_code.md](assignment1_mmpretrain_code.md)
- 演示代码: [assignment1_mmpretrain_complete_demo.py](assignment1_mmpretrain_complete_demo.py)
