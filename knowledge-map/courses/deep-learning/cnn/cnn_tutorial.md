---
topic: cnn
dimension: tutorial
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.8"
  - "📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)"
  - "📖 Paper: [Krizhevsky et al. 2012 (AlexNet)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)"
  - "📖 Paper: [He et al. 2015 (ResNet)](https://arxiv.org/abs/1512.03385)"
  - "📖 Docs: [PyTorch Training a Classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)"
expiry: 12m
status: current
---

# CNN 教程

> **前置知识：** 线性代数基础、MLP/全连接网络、反向传播、PyTorch 张量操作
> **参考来源：** [PyTorch 60-min Blitz](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html) | [LeCun 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) | [《Deep Learning with PyTorch》Ch.8](../../../textbooks/stevens_deep_learning_with_pytorch.pdf)

---


## Section 0: 前置知识速查

1. **矩阵乘法**：理解 $(m \times n) \cdot (n \times p) = (m \times p)$
2. **MLP 结构**：输入层 → 隐藏层 → 输出层，全连接，反向传播训练
3. **激活函数**：Sigmoid, ReLU, Softmax 的作用和区别
4. **损失函数**：交叉熵损失（分类任务）
5. **PyTorch 基础**：`torch.Tensor`, `nn.Module`, `optimizer.step()`, `loss.backward()`

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.5-7

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **参数爆炸**：一张 1600×1200 RGB 图像有 576 万像素，MLP 第一层 1000 节点就需要 **57.6 亿**个权重，显存直接爆了
- 🔥 **空间信息丢失**：MLP 必须把图像展平成一维向量，相邻像素的空间关系（边缘、纹理、形状）全部丢失
- 🔥 **不具备平移不变性**：MLP 学到"猫在图片左上角"，猫移到右下角就不认识了——因为每个位置用的是不同的权重
- 🔥 **泛化能力差**：参数太多 + 没有结构化先验，小数据集必然过拟合

### 它的核心价值

1. **权值共享**：同一个滤波器在所有位置使用相同参数 → 参数量从数十亿降到数千，模型可训练
2. **局部连接**：每个神经元只看局部区域（如 3×3）→ 自然捕获边缘、纹理等局部模式
3. **平移不变性**：同一个滤波器扫描全图 → 物体在任何位置都能被检测到
4. **层次化特征学习**：浅层学边缘 → 中层学纹理/形状 → 深层学物体部件 → 自动从低级到高级

> 📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)
> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 CNN 的完整流程

```
┌───────────────────────────────────────────────────────────────────────┐
│                        CNN 前向传播流程                                │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Input Image [B, 3, 224, 224]                                        │
│       │                                                               │
│       ▼                                                               │
│  ┌─────────────────┐                                                 │
│  │ Conv2D (3→64)   │──→ BatchNorm ──→ ReLU ──→ MaxPool(2×2)        │
│  └─────────────────┘                                                 │
│       │  输出: [B, 64, 112, 112]                                     │
│       ▼                                                               │
│  ┌─────────────────┐                                                 │
│  │ Conv2D (64→128) │──→ BatchNorm ──→ ReLU ──→ MaxPool(2×2)        │
│  └─────────────────┘                                                 │
│       │  输出: [B, 128, 56, 56]                                      │
│       ▼                                                               │
│  ┌─────────────────┐                                                 │
│  │ Conv2D (128→256)│──→ BatchNorm ──→ ReLU ──→ MaxPool(2×2)        │
│  └─────────────────┘                                                 │
│       │  输出: [B, 256, 28, 28]                                      │
│       ▼                                                               │
│  ┌────────────────────────────┐                                      │
│  │ Global Average Pooling     │                                      │
│  └────────────────────────────┘                                      │
│       │  输出: [B, 256]                                              │
│       ▼                                                               │
│  ┌─────────────────┐                                                 │
│  │ FC (256→10)     │──→ Softmax ──→ 类别概率                        │
│  └─────────────────┘                                                 │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

### 2.2 卷积操作的核心机制

**为什么用卷积而不是全连接？**

本质是两个先验假设：
1. **局部性 (Locality)**：图像中相邻像素的关系比远距离像素更重要。一只鸟的"眼睛"只与周围 5×5 的像素相关，不需要关注远处的天空
2. **平移等变性 (Translation Equivariance)**：一个特征（如边缘）在图像的任何位置都应该用相同的方式检测

**卷积是怎么做的：**

以 6×6 输入、3×3 滤波器为例：

```
输入 (6×6):             滤波器 (3×3):
┌─┬─┬─┬─┬─┬─┐          ┌──┬──┬──┐
│1│0│1│0│1│0│          │ 1│ 0│-1│
├─┼─┼─┼─┼─┼─┤          ├──┼──┼──┤
│0│1│0│1│0│1│          │ 1│ 0│-1│
├─┼─┼─┼─┼─┼─┤          ├──┼──┼──┤
│1│0│1│0│1│0│          │ 1│ 0│-1│
├─┼─┼─┼─┼─┼─┤          └──┴──┴──┘
│0│1│0│1│0│1│
├─┼─┼─┼─┼─┼─┤          输出 (4×4):
│1│0│1│0│1│0│          ┌──┬──┬──┬──┐
├─┼─┼─┼─┼─┼─┤          │  │  │  │  │
│0│1│0│1│0│1│          ├──┼──┼──┼──┤
└─┴─┴─┴─┴─┴─┘          │  │  │  │  │
                        ├──┼──┼──┼──┤
滤波器在输入上              │  │  │  │  │
逐步滑动，每个位置          ├──┼──┼──┼──┤
计算点积+偏置              │  │  │  │  │
                        └──┴──┴──┴──┘
```

> 📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)

### 2.3 池化操作的作用

**Max Pooling 示例（2×2 窗口，stride=2）：**

```
输入 (4×4):              输出 (2×2):
┌──┬──┬──┬──┐           ┌──┬──┐
│ 1│ 3│ 2│ 4│           │ 3│ 4│    ← 每个 2×2 块取最大值
├──┼──┼──┼──┤           ├──┼──┤
│ 5│ 2│ 1│ 0│           │ 5│ 3│
├──┼──┼──┼──┤           └──┴──┘
│ 0│ 1│ 3│ 2│
├──┼──┼──┼──┤
│ 4│ 2│ 1│ 3│
└──┴──┴──┴──┘
```

池化的三大好处：
1. **降维**：4×4 变 2×2，参数和计算量减半
2. **抗过拟合**：更少的参数意味着更少的过拟合风险
3. **平移不变性**：物体稍微移动几个像素，池化后的结果变化不大

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

### 2.4 从边缘到语义的层次化学习

```
Layer 1 (浅层)          Layer 3 (中层)         Layer 5+ (深层)
┌─────────┐           ┌─────────┐           ┌─────────┐
│ ─ │ ╱ │  │           │ 角 │纹理│           │ 眼睛│耳朵│
│ ─ │ ╲ │  │  ──→     │ 圆 │条纹│  ──→     │ 鼻子│脸 │
│ │ │ ─ │  │           │ 弧 │网格│           │ 轮子│车 │
└─────────┘           └─────────┘           └─────────┘
 检测边缘方向             组合成纹理/形状         组合成物体部件
```

这是 CNN 最强大的特性——**自动**从低级特征逐步组合出高级语义特征，不需要人工设计特征提取器。

> 📖 Paper: [Krizhevsky et al. 2012 (AlexNet)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)

---


## Section 3: 局限性

1. **对旋转/缩放不变性有限**：CNN 天然具有平移不变性，但旋转 90° 后可能认不出 → 需要数据增强或特殊架构
2. **需要大量标注数据**：从头训练深层 CNN 通常需要几万到几百万张标注图片 → 小数据集靠迁移学习
3. **计算资源消耗大**：深层 CNN（如 ResNet-152）有数千万参数，训练需要 GPU → 不适合资源受限设备
4. **可解释性差**：内部学到的特征难以人类理解 → 需要 Grad-CAM 等可视化工具
5. **对对抗样本脆弱**：人眼看不出区别的微小扰动可以让 CNN 完全分类错误

> 📖 Paper: [He et al. 2015 (ResNet)](https://arxiv.org/abs/1512.03385)

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **MLP** | 结构简单，任何数据类型 | 参数爆炸、无空间感知 | 小规模表格数据 |
| **CNN** | 权值共享、空间特征、效果优秀 | 计算量大、需要大数据 | 图像/视频/2D信号 |
| **Vision Transformer (ViT)** | 全局注意力、可扩展性强 | 需要更多数据和计算 | 超大规模图像任务 |
| **传统 CV (SIFT/HOG)** | 不需要训练、可解释 | 泛化差、手工设计 | 简单/低资源场景 |

> 📖 Paper: [Krizhevsky et al. 2012 (AlexNet)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)
> 📖 Paper: [He et al. 2015 (ResNet)](https://arxiv.org/abs/1512.03385)

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning with PyTorch》Ch.8](../../../textbooks/stevens_deep_learning_with_pytorch.pdf) | 📚 教科书 | 全文核心参考 |
| [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) | 📖 论文 | Section 1, 2（CNN 设计动机） |
| [Krizhevsky et al. 2012 (AlexNet)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) | 📖 论文 | Section 2.4（层次化学习） |
| [He et al. 2015 (ResNet)](https://arxiv.org/abs/1512.03385) | 📖 论文 | Section 3（局限性与深度网络） |
| [PyTorch 60-min Blitz](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html) | 📖 文档 | Section 0（前置知识） |
