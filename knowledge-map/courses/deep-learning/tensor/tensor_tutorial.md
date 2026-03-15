---
topic: tensor
dimension: tutorial
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.3"
  - "📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)"
  - "📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)"
expiry: 12m
status: current
---

# Tensor 教程

> **前置知识：** Python 基础、NumPy ndarray 概念、线性代数（矩阵/向量）
> **参考来源：** [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) | [《Deep Learning with PyTorch》Ch.3](../../textbooks/stevens_deep_learning_with_pytorch.pdf)

---


## Section 0: 前置知识速查

1. **Python list/嵌套 list** — 能创建 `[[1,2],[3,4]]` 这样的二维数据
2. **NumPy ndarray** — 多维数组的核心操作（创建、切片、广播）
3. **线性代数基础** — 标量、向量、矩阵的含义和基本运算
4. **GPU 概念** — CPU 和 GPU 的区别（不必了解 CUDA 编程）

> 📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🐌 **NumPy 无法利用 GPU** — 大规模矩阵运算（如训练 ResNet）只能在 CPU 上计算，训练一个 epoch 可能要几小时
- 🔗 **手动求导极其痛苦** — 神经网络有数百万参数，手动推导和实现每个参数的梯度几乎不可能
- 🔄 **数据搬运繁琐** — 在 NumPy、GPU 库、深度学习框架之间来回转换数据格式，代码冗长且易出错
- 📦 **没有统一的数据抽象** — 图像是 (H, W, C)、文本是 (T, D)、表格是 (N, F)，每种数据需要不同的处理方式

### 它的核心价值

1. **统一数据表示** — 标量到高维数组用同一种数据结构描述
2. **GPU 原生加速** — 一行代码 `.to('cuda')` 即可将计算搬到 GPU
3. **自动微分集成** — `requires_grad=True` 开启，`.backward()` 自动计算所有参数梯度
4. **与 NumPy 无缝衔接** — `torch.from_numpy()` 和 `.numpy()` 零拷贝互转
5. **丰富的运算库** — 1200+ 操作覆盖线性代数、统计、采样等

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3
> 📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 Tensor 的内存模型

```
┌──────────────────────────────────────────┐
│             torch.Tensor (逻辑层)         │
│  shape = (2, 3)                          │
│  stride = (3, 1)                         │
│  dtype = float32                         │
│  device = cpu                            │
│  storage_offset = 0                      │
├──────────────────────────────────────────┤
│           torch.Storage (物理层)          │
│  一维连续内存: [a b c d e f]              │
│  对应逻辑布局:                            │
│    [[a, b, c],      ← 第 0 行            │
│     [d, e, f]]      ← 第 1 行            │
└──────────────────────────────────────────┘
```

**关键设计：** Tensor 的"逻辑 shape"和"物理存储"是分开的。多个 Tensor 可以共享同一块 Storage，只是通过不同的 shape、stride、offset 来"看"数据的不同视角（View）。

### 2.2 Stride 机制

Stride 告诉 PyTorch 如何将多维索引映射到一维内存地址：

```
给定 T[i][j]，内存位置 = i * stride[0] + j * stride[1]

shape  = (2, 3)
stride = (3, 1)    ← 行优先 (C-contiguous)

T[1][2] → 1*3 + 2*1 = 5   ← 一维数组第 5 个位置
```

**为什么 stride 重要？** `transpose()` 不搬数据，只交换 stride：

```
原始:   shape = (2, 3), stride = (3, 1)
转置后: shape = (3, 2), stride = (1, 3)    ← 变成非连续 (non-contiguous)
```

### 2.3 autograd 计算图

```
              x (叶节点, requires_grad=True)
              │
              ▼
         y = x * 2    ←  MulBackward
              │
              ▼
         z = y.sum()  ←  SumBackward
              │
         z.backward() ←  反向传播，自动计算 dz/dx
              │
              ▼
         x.grad = 2   ←  梯度存在 x.grad 中
```

每次对 Tensor 做运算，PyTorch 自动构建一个有向无环图 (DAG)，记录每一步操作。调用 `.backward()` 时沿着图反向传播，用链式法则求梯度。

### 2.4 Device 转移

```
CPU Tensor  ──.to('cuda')──→  GPU Tensor
     ↑                              │
     └──.to('cpu') / .cpu()────────┘
```

- **注意：** 跨设备拷贝是**有代价的**（PCIe 带宽瓶颈）
- **规则：** 参与同一运算的 Tensor 必须在同一 device 上

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3
> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## Section 3: 局限性

1. **同构数据** — 所有元素必须是相同 dtype，不能像 Python list 混合不同类型
2. **固定 shape** — 创建后 shape 固定（除非重新创建），不支持追加元素
3. **GPU 内存受限** — GPU 显存远小于 CPU 内存，大 Tensor 容易 OOM
4. **autograd 有开销** — `requires_grad=True` 的 Tensor 在前向传播时需要额外记录操作历史，消耗更多内存
5. **Python GIL** — 虽然底层是 C++ 实现，但 Python 层的循环操作仍受 GIL 限制

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------| 
| PyTorch Tensor | GPU/autograd 原生支持; 动态计算图; Pythonic API | GPU 内存有限; 生态不如 NumPy 广 | 深度学习训练/推理 |
| NumPy ndarray | 科学计算生态最广; 性能优化成熟 | 无 GPU; 无 autograd | 通用科学计算/数据预处理 |
| TensorFlow Tensor | GPU/TPU 支持; 静态图性能优化强 | API 学习曲线陡; 调试较难 | 生产部署/TPU 场景 |
| JAX DeviceArray | 函数式风格; XLA 编译优化; 支持用 `jit` 加速 | 社区相对小; 不适合复杂动态逻辑 | 研究级高性能计算 |
| CuPy ndarray | NumPy API 兼容; GPU 加速 | 无 autograd; 仅限 CUDA GPU | NumPy 用户的 GPU 加速 |

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf) Ch.3 | 📚 教科书 | Section 0-3, 核心概念 |
| [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) | 📖 官方教程 | Section 0-2, 代码示例 |
| [PyTorch torch.Tensor Docs](https://pytorch.org/docs/stable/tensors.html) | 📖 官方文档 | Section 2-4, API 参考 |
| [PyTorch Broadcasting Semantics](https://pytorch.org/docs/stable/notes/broadcasting.html) | 📖 官方文档 | Section 2, Broadcasting |
| [Kolda & Bader, Tensor Decompositions (2009)](https://doi.org/10.1137/07070111X) | 📖 论文 | 数学基础 |
