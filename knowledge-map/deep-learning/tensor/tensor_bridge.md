---
topic: tensor
dimension: bridge
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.3"
  - "📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)"
  - "📖 Docs: [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)"
expiry: 6m
status: current
---

# Tensor 衔接与扩展

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | NumPy ndarray | Tensor 的设计原型，API 高度一致 | [NumPy 文档](https://numpy.org/doc/stable/) |
| ← 前置 | 线性代数 | 标量/向量/矩阵是 Tensor 的低维特例 | — |
| → 后续 | Autograd（自动微分） | Tensor 开启 `requires_grad` 后进入计算图 | [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html) |
| → 后续 | nn.Module（模型构建） | 模型的参数是 `nn.Parameter`（特殊的 Tensor） | — |
| → 后续 | DataLoader（数据管道） | 将数据批量打包成 Tensor 送入模型 | — |
| → 后续 | PyTorch（框架） | Tensor 是 PyTorch 的核心数据结构 | [pytorch_map.md](../pytorch/pytorch_map.md) |

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|----------|-----------|-------------------| 
| NumPy ndarray | shape, dtype, stride, 广播规则 | PyTorch Tensor 完全继承了这些概念和 API 设计 |
| 线性代数 | 标量/向量/矩阵/转置/乘法 | Tensor 是它们的高维推广，矩阵乘法等操作直接映射 |
| Python 数据结构 | list, tuple | Tensor 可以从嵌套 list 创建，shape 用 tuple 表示 |
| C/C++ 内存模型 | 连续内存, 指针, row-major | Tensor 的 Storage 是一维连续内存，stride 实现多维映射 |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

---


## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|----------|-----------------|-----------------| 
| Autograd | `requires_grad`, 计算图, `.backward()` | Tensor 的操作历史构成 DAG，autograd 沿图反向传播求梯度 |
| nn.Module | `nn.Parameter` (继承 Tensor) | 模型可训练参数是 Tensor 的子类，自动注册到模型 |
| DataLoader | Tensor 作为 batch 数据 | `collate_fn` 将样本组装成 batch Tensor |
| CNN | 4D Tensor (B, C, H, W) | 图像数据的标准 Tensor 布局 |
| RNN/Transformer | 3D Tensor (B, T, D) | 序列数据的标准 Tensor 布局 |
| GPU 并行计算 | `.to(device)`, CUDA Tensor | 模型和数据必须移到 GPU Tensor 才能利用 CUDA 核心 |
| 模型序列化 | `torch.save()` / `torch.load()` | 保存/加载的核心对象就是 Tensor 字典 (state_dict) |

> 📖 Docs: [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)

---


## 概念演变追踪

| 概念 | 在 NumPy 中 | 在 PyTorch 中 | 变化 |
|------|-----------|-------------|------| 
| 多维数组 | `np.ndarray` | `torch.Tensor` | 加入 GPU 和 autograd 支持 |
| 数据类型 | `np.float64` (默认) | `torch.float32` (默认) | 深度学习偏好 32 位以节省内存和加速 |
| 内存布局 | row-major (C) / col-major (F) | row-major 默认 | 保持一致 |
| 共享内存 | view / slice | view / slice + Storage | 增加显式 Storage 层 |
| 广播 | `np.broadcast` | `torch.broadcast_tensors` | 规则相同 |
| 随机数 | `np.random` | `torch.rand` / `torch.randn` | API 类似但独立实现 |
| 设备 | CPU only | CPU + GPU (`device`) | 重大新增 |
| 梯度 | 无 | `requires_grad` + `grad` | 重大新增 |

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------| 
| [《Deep Learning with PyTorch》Ch.3](../../textbooks/stevens_deep_learning_with_pytorch.pdf) | 📚 教科书 | Tensor 的最详细入门加解析 | ⭐⭐ |
| [PyTorch Internals](http://blog.ezyang.com/2019/05/pytorch-internals/) | 📖 博客 | 深入 Storage/Stride/View 底层实现 | ⭐⭐⭐⭐ |
| [Kolda & Bader, Tensor Decompositions (2009)](https://doi.org/10.1137/07070111X) | 📖 论文 | 数学张量分析的权威综述 | ⭐⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------| 
| [TensorFlow Tensor Guide](https://www.tensorflow.org/guide/tensor) | PyTorch vs TF 的 Tensor API 差异 | 需要迁移代码时 |
| [JAX DeviceArray](https://jax.readthedocs.io/en/latest/) | 函数式风格的 Tensor 操作 | 研究 XLA 编译加速时 |
| [NumPy ndarray Internals](https://numpy.org/doc/stable/reference/arrays.ndarray.html) | Tensor 设计的鼻祖 | 理解底层 stride 机制时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------| 
| [PyTorch 知识地图](../pytorch/pytorch_map.md) | PyTorch 框架全貌 | 学完 Tensor 后了解框架整体 |
| [CNN 知识地图](../cnn/cnn_map.md) | 卷积神经网络如何使用 4D Tensor | 学习图像处理和 CNN 时 |
| [Vanishing Gradient 知识地图](../vanishing_gradient/) | 梯度消失问题与 Tensor 的 autograd | 理解训练中的梯度问题时 |

---


## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------| 
| deep-learning | 3 | [pytorch](../pytorch/), [cnn](../cnn/), [vanishing_gradient](../vanishing_gradient/) | Tensor 是所有 DL 主题的基础数据结构 |
| retrieval_lab | 1 | [retrieval_lab](../../retrieval_lab/) | 信息检索中的向量化表示也使用 Tensor |
