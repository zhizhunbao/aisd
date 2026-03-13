---
topic: tensor
dimension: history
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Paper: [Ricci & Levi-Civita, Tensor Analysis (1900)](https://en.wikipedia.org/wiki/Absolute_differential_calculus)"
  - "📖 Paper: [Oliphant, NumPy (2006)](https://numpy.org/doc/stable/)"
  - "📖 Paper: [Paszke et al., PyTorch NeurIPS (2019)](../../.documents/pytorch/paszke_pytorch_neurips2019.pdf)"
  - "📖 Paper: [Abadi et al., TensorFlow (2016)](https://arxiv.org/abs/1603.04467)"
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.3"
expiry: never
status: current
---

# Tensor 的故事线：从数学抽象到深度学习引擎

> **核心主题：** 张量从纯数学概念演变为深度学习的核心数据结构，经历了数学形式化 → 科学计算工具 → GPU 加速框架的三次飞跃
> **故事线：** 一个不断"打怪升级"的问题解决历程

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括
> 如何用一种统一的数学语言描述多维数据，并让计算机高效地处理它？

人类很早就需要处理"多维数据"——物理学家需要描述电磁场中每个点的力的方向和大小，气象学家需要记录不同经度、纬度、高度、时间下的温度……这些数据天然是"多维"的。但早期的数学工具（标量、向量、矩阵）只能分别处理 0 维、1 维、2 维的情况。

> 🔑 **问题提出：** 需要一种能描述任意维度数据的数学对象

---

## 📚 第一章：数学家的张量（1890s-1900s）

> **关键人物：** Gregorio Ricci-Curbastro, Tullio Levi-Civita
> **关键论文：** Ricci & Levi-Civita, "Méthodes de calcul différentiel absolu et leurs applications" (1900)

### 发生了什么？

意大利数学家 Ricci-Curbastro 和他的学生 Levi-Civita 发展了"绝对微分学"（张量分析）。张量被定义为在坐标变换下遵循特定变换规则的数学对象。

```
标量 (0 阶张量): 温度 T — 换坐标系不变
向量 (1 阶张量): 力 F — 换坐标系，分量按一次变换
矩阵 (2 阶张量): 应力 σ — 换坐标系，分量按二次变换
N 阶张量:         — 换坐标系，分量按 N 次变换
```

### 为什么这很重要？

Einstein 在 1915 年的广义相对论中大量使用了张量来描述时空曲率（Riemann 曲率张量）。张量成为了描述物理规律的通用语言——物理定律如果能用张量方程写出来，就自动在所有坐标系下成立。

### 但还有一个问题……

数学张量是纯理论工具，关注的是坐标变换下的不变性。计算机科学家需要的是"怎么高效存储和计算多维数据"——他们不关心坐标变换，只关心"多维数组"。

> 🔑 **故事转折点：** 计算机时代来临，"多维数据"需要从数学抽象变成工程实现

---

## 📚 第二章：NumPy 的多维数组时代（1995-2006）

> **关键人物：** Jim Hugunin (Numeric), Travis Oliphant (NumPy)
> **关键论文：** Travis Oliphant, "Guide to NumPy" (2006)

### 发生了什么？

1995 年，Jim Hugunin 创建了 Numeric — Python 的第一个多维数组库。之后出现了 Numarray 作为竞品。2005 年，Travis Oliphant 将两者合并为 NumPy，提供了 `ndarray`（n-dimensional array）这个统一的多维数组数据结构。

```
NumPy ndarray 的核心设计:
┌─────────────────────────────────┐
│  ndarray                         │
│  ├── shape: (3, 4)              │
│  ├── dtype: float64             │
│  ├── strides: (32, 8)           │ ← 字节步长
│  └── data: 连续内存块            │
└─────────────────────────────────┘
```

ndarray 借用了"张量"（多维数组）的概念，但完全抛弃了数学张量的坐标变换理论。它只关心：**怎么在连续内存中高效存储和访问多维数据**。

### 为什么这很重要？

NumPy 成为了 Python 科学计算生态的基石。SciPy、Pandas、Matplotlib、scikit-learn 都构建在 ndarray 之上。它的 stride 机制（用步长描述多维索引到一维内存的映射）成为后来所有张量库的设计基础。

### 但还有一个问题……

NumPy 只在 CPU 上运行。随着深度学习兴起（2012 AlexNet），模型参数量从几万增长到数百万，CPU 上的矩阵运算太慢了——需要 GPU 并行加速。而且 NumPy 没有自动微分功能，训练神经网络时需要手写反向传播。

> 🔑 **故事转折点：** 深度学习需要 GPU 加速 + 自动微分，NumPy 力不从心

---

## 📚 第三章：Theano 与自动微分的觉醒（2007-2016）

> **关键人物：** Yoshua Bengio, James Bergstra (MILA)
> **关键论文：** Bergstra et al., "Theano: A CPU and GPU Math Compiler" (2010)

### 发生了什么？

蒙特利尔大学的 MILA 团队开发了 Theano，第一个同时支持**符号计算**、**自动微分**和 **GPU 加速**的 Python 深度学习库。

```
Theano 的创新:
1. 符号计算图 — 先定义计算图，再编译执行
2. 自动微分 — T.grad(cost, params) 自动求梯度
3. GPU 透明 — 同一段代码自动在 CPU/GPU 上运行
```

### 为什么这很重要？

Theano 证明了"多维数组 + 计算图 + GPU 加速"这个组合的巨大威力。之后的 TensorFlow（2015）和 PyTorch（2016）都继承了这个核心思路。

### 但还有一个问题……

Theano 使用**静态计算图**——必须先完整定义整个计算图，再一次性编译执行。这让调试极其痛苦（`print` 看不到中间值），也无法用 Python 的 `if/for` 做动态控制流。

> 🔑 **故事转折点：** 研究者需要"像写 Python 一样写深度学习"的灵活性

---

## 📚 第四章：PyTorch Tensor 与动态计算图（2016-至今）

> **关键人物：** Adam Paszke, Soumith Chintala (Meta AI)
> **关键论文：** [Paszke et al., "PyTorch: An Imperative Style, High-Performance Deep Learning Library" (NeurIPS 2019)](../../.documents/pytorch/paszke_pytorch_neurips2019.pdf)

### 发生了什么？

2016 年，Facebook (Meta) AI Research 发布了 PyTorch。它的 Tensor 继承了 NumPy ndarray 的 API 设计，但加入了两个革命性的能力：

```
PyTorch Tensor = NumPy ndarray + GPU 加速 + 动态自动微分

核心创新:
┌──────────────────────────────────────┐
│          torch.Tensor                │
│  ├── NumPy 式 API (shape, stride...) │
│  ├── .to('cuda') → GPU 加速         │
│  ├── requires_grad=True → 动态计算图 │
│  └── .backward() → 自动反向传播      │
└──────────────────────────────────────┘
```

**动态计算图**（Define-by-Run）意味着每次前向传播都会动态构建计算图，可以用普通的 Python `if/for/while` 来控制网络结构。调试就是普通的 Python 调试。

### 为什么这很重要？

PyTorch 让深度学习研究变得极其流畅，研究者可以像写普通 Python 代码一样构建复杂的神经网络。到 2020 年代，PyTorch 在学术研究中的占有率超过 80%，成为事实上的标准。

### 但还有一个问题……

动态计算图的灵活性带来了性能代价——每次前向传播都要重新构建图。PyTorch 通过 `torch.compile`（2022年引入的 TorchDynamo + TorchInductor）等技术弥补了这个差距，在保持灵活性的同时接近静态图的性能。

> 🔑 **故事转折点：** 编译器技术让动态图也能获得静态图级别的性能

---

## 🗺️ 全局回顾：技术演进路线图

```
数学张量 (1900)
    │  纯数学：坐标变换不变性
    ▼
NumPy ndarray (2005)
    │  工程化：连续内存 + stride + 丰富 API
    ▼
Theano (2007)
    │  + 自动微分 + GPU + 静态计算图
    ▼
PyTorch Tensor (2016)
    │  + 动态计算图 + NumPy 式 API
    ▼
torch.compile (2022)
       + 编译优化：动态图也能高性能
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|----------|-------------------| 
| 数学张量 → NumPy | 从纯理论到可计算：如何在计算机中高效表示和操作多维数据 |
| NumPy → Theano | CPU 太慢 + 手写梯度太痛苦：GPU 加速 + 自动微分 |
| Theano → PyTorch | 静态图调试困难 + 不灵活：动态计算图（Define-by-Run） |
| PyTorch → torch.compile | 动态图性能不如静态图：编译器自动优化，两全其美 |

> 📖 Paper: [Paszke et al., PyTorch NeurIPS 2019](../../.documents/pytorch/paszke_pytorch_neurips2019.pdf)
> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3
