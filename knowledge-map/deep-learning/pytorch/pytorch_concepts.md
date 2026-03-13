---
topic: pytorch
dimension: concepts
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Docs: [PyTorch Documentation](https://pytorch.org/docs/stable/) — v2.10"
  - "📖 Paper: [Paszke et al. 2019](https://arxiv.org/abs/1912.01703)"
  - "📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf)"
expiry: 6m
status: current
---

# PyTorch 核心概念

> 📖 Docs: [PyTorch Documentation](https://pytorch.org/docs/stable/) — v2.10
> 📖 Paper: Paszke et al., [PyTorch: An Imperative Style, High-Performance Deep Learning Library](https://arxiv.org/abs/1912.01703), NeurIPS 2019

---


## 术语定义

### 张量 (Tensor)

PyTorch 中最基础的数据结构，本质上是一个**多维数组**，类似于 NumPy 的 `ndarray`，但额外支持 GPU 加速计算和自动微分。所有的模型输入、输出、参数都是 Tensor。`torch.Tensor` 是默认的浮点型张量（`torch.FloatTensor`）。

> 易混淆：**NumPy ndarray** — Tensor 多了 GPU 支持和梯度追踪，ndarray 仅 CPU；两者可通过 `.numpy()` 和 `torch.from_numpy()` 互转但共享内存。

### 自动微分 (Autograd)

PyTorch 的自动求导引擎。当 Tensor 的 `requires_grad=True` 时，Autograd 会在前向传播中动态构建计算图（DAG），记录每一步操作。调用 `.backward()` 时沿图反向传播，基于链式法则自动计算所有叶子节点的梯度。

> 易混淆：**手动求导 / 符号求导** — Autograd 使用的是**反向模式自动微分（reverse-mode AD）**，不是符号微分（Mathematica 风格），也不是数值微分（有限差分）。

### 计算图 (Computational Graph)

Autograd 内部维护的有向无环图（DAG）。**叶子节点**是用户创建的输入 Tensor，**根节点**是最终输出（通常是 loss）。每个中间节点对应一个 `Function`（`.grad_fn`），记录了产生该 Tensor 的操作。PyTorch 的图是**动态的**（每次前向传播重建），这是与 TensorFlow 1.x 静态图的核心区别。

> 易混淆：**静态计算图 (Static Graph)** — TF1.x 先定义图再执行；PyTorch 的动态图允许用 Python `if/for/while` 控制流，每次迭代图的结构可以不同。

### 模块 (nn.Module)

PyTorch 构建神经网络的基类。所有网络层（`nn.Linear`, `nn.Conv2d` 等）和自定义模型都继承自 `nn.Module`。它管理参数（`parameters()`）、子模块（`children()`），并通过 `forward()` 方法定义前向传播逻辑。

> 易混淆：**nn.functional** — `nn.Module` 有状态（持有参数），`nn.functional` 是无状态的纯函数（如 `F.relu`, `F.cross_entropy`）。

### 参数 (Parameter)

`nn.Parameter` 是一种特殊的 Tensor，默认 `requires_grad=True`。当它被赋值为 `nn.Module` 的属性时，会自动注册到模块的参数列表（`module.parameters()`），从而被优化器更新。

> 易混淆：**Buffer** — 用 `register_buffer()` 注册的 Tensor 不参与梯度计算但会随模型保存/加载（如 BatchNorm 的 running_mean）。

### 优化器 (Optimizer)

`torch.optim` 模块中的优化算法实现。常用的有 `SGD`, `Adam`, `AdamW` 等。优化器持有模型参数的引用，调用 `optimizer.step()` 按梯度更新参数，`optimizer.zero_grad()` 清零梯度。

> 易混淆：**学习率调度器 (LR Scheduler)** — Optimizer 负责单步更新，Scheduler（如 `StepLR`, `CosineAnnealingLR`）负责跨 epoch 调整学习率。

### 数据加载器 (DataLoader)

`torch.utils.data.DataLoader` 负责将数据集（`Dataset`）包装成可迭代对象，支持批量加载（batching）、打乱（shuffling）、多进程预取（`num_workers`）和自动填充（`collate_fn`）。是训练循环中数据供给的核心组件。

> 易混淆：**Dataset** — `Dataset` 定义"如何获取一个样本"（`__getitem__`），`DataLoader` 定义"如何把多个样本组装成 batch"。

### 损失函数 (Loss Function)

衡量模型预测与真实标签之间差异的函数。PyTorch 提供了 `nn.CrossEntropyLoss`（分类）、`nn.MSELoss`（回归）等常用实现。损失函数的输出是一个标量 Tensor，调用 `.backward()` 启动反向传播。

> 易混淆：**nn.CrossEntropyLoss vs nn.NLLLoss** — `CrossEntropyLoss` = `LogSoftmax` + `NLLLoss`，输入是 raw logits；`NLLLoss` 输入是 log-probabilities。

### 设备 (Device)

指定 Tensor 的存储和计算位置。`torch.device('cpu')` 使用 CPU，`torch.device('cuda:0')` 使用第一块 GPU。模型和数据必须在同一设备上才能运算，通过 `.to(device)` 迁移。

> 易混淆：**CUDA vs cuDNN** — CUDA 是 NVIDIA GPU 通用计算平台；cuDNN 是 CUDA 上专门针对深度学习优化的加速库。

### Eager Mode（即时执行模式）

PyTorch 的默认执行模式。代码按 Python 顺序逐行执行，每条操作立即获得结果（不需要先编译计算图）。这使得调试非常方便（可直接使用 `print`, `pdb`），但可能牺牲部分运行时优化。

> 易混淆：**Graph Mode / TorchScript / torch.compile** — 通过 JIT 编译或 `torch.compile` 可将 Eager 代码转换为优化的图模式执行，兼顾灵活性和性能。

> 📖 Docs: [PyTorch Documentation](https://pytorch.org/docs/stable/)
> 📖 Paper: Paszke et al., [NeurIPS 2019](https://arxiv.org/abs/1912.01703), Section 2-4

---


## 概念辨析

### Tensor vs NumPy ndarray

| 维度 | Tensor | ndarray |
|------|--------|---------|
| **本质** | 多维数组 + 梯度追踪 | 多维数组 |
| **GPU 支持** | ✅ `.to('cuda')` | ❌ 仅 CPU |
| **自动微分** | ✅ `requires_grad=True` | ❌ 无 |
| **内存共享** | `torch.from_numpy()` 共享 | `.numpy()` 共享 |
| **广播规则** | 与 NumPy 一致 | 标准广播 |
| **生态** | 深度学习 | 科学计算 |

> 📖 Docs: [Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

### nn.Module vs nn.functional

| 维度 | nn.Module | nn.functional |
|------|-----------|---------------|
| **本质** | 类（有状态） | 函数（无状态） |
| **参数管理** | 自动注册 Parameter | 需手动传入权重 |
| **典型用法** | `self.conv = nn.Conv2d(...)` | `F.conv2d(x, weight)` |
| **适用场景** | 有可训练参数的层 | 无参数操作（ReLU, Dropout 推理时） |
| **最佳实践** | 网络结构定义 | `forward()` 中的辅助操作 |

> 📖 Docs: [nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module)
> 📖 Docs: [nn.functional](https://pytorch.org/docs/stable/nn.functional.html)

### 动态图 vs 静态图

| 维度 | 动态图 (PyTorch) | 静态图 (TF1.x) |
|------|------------------|-----------------|
| **构建时机** | 运行时（define-by-run） | 编译时（define-and-run） |
| **控制流** | Python 原生 if/for/while | tf.cond / tf.while_loop |
| **调试** | pdb / print 直接用 | 需专用调试器 |
| **性能优化** | 需 torch.compile 额外优化 | 编译期全图优化 |
| **灵活性** | ✅ 极高 | ⚠️ 受限于图定义 |

> 📖 Paper: Paszke et al., [NeurIPS 2019](https://arxiv.org/abs/1912.01703), Section 2

### model.train() vs model.eval()

| 维度 | train() 模式 | eval() 模式 |
|------|-------------|-------------|
| **Dropout** | 随机丢弃神经元 | 关闭，使用全部神经元 |
| **BatchNorm** | 用当前 batch 统计量 | 用 running 统计量 |
| **梯度计算** | 不受影响（由 requires_grad 控制） | 不受影响 |
| **常搭配** | `optimizer.step()` | `torch.no_grad()` |

> 📖 Docs: [nn.Module.train](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.train)

> 📖 Docs: [PyTorch Documentation](https://pytorch.org/docs/stable/)

---


## 核心属性

### 信息架构

```
┌─────────────────────────────────── PyTorch ────────────────────────────────────┐
│                                                                                │
│  ┌─────────────── torch ───────────────┐  ┌──────── torch.nn ──────────┐      │
│  │ Tensor（多维数组）                   │  │ Module（网络层基类）       │      │
│  │ ├── dtype / shape / device          │  │ ├── Linear, Conv2d, ...   │      │
│  │ ├── requires_grad                   │  │ ├── Parameter             │      │
│  │ └── grad / grad_fn                  │  │ ├── Sequential, ModuleList│      │
│  │                                     │  │ └── forward()             │      │
│  │ Autograd（自动微分引擎）            │  │                           │      │
│  │ ├── 动态计算图 (DAG)                │  │ functional（无状态操作）   │      │
│  │ ├── backward()                      │  │ ├── relu, sigmoid         │      │
│  │ └── Function (grad_fn)             │  │ └── cross_entropy, mse    │      │
│  └─────────────────────────────────────┘  └───────────────────────────┘      │
│                                                                                │
│  ┌──── torch.optim ────┐  ┌──── torch.utils.data ────┐  ┌── torchvision ──┐  │
│  │ SGD, Adam, AdamW    │  │ Dataset                   │  │ transforms      │  │
│  │ LR Schedulers       │  │ DataLoader                │  │ models (预训练) │  │
│  └─────────────────────┘  └───────────────────────────┘  └─────────────────┘  │
│                                                                                │
│  ┌── torch.distributed ──┐  ┌── torch.compile ──┐  ┌── torch.export ──┐      │
│  │ DDP, FSDP             │  │ Dynamo + Inductor  │  │ TorchScript      │      │
│  └────────────────────────┘  └───────────────────┘  └──────────────────┘      │
└────────────────────────────────────────────────────────────────────────────────┘
```

> 📖 Docs: [PyTorch API Reference](https://pytorch.org/docs/stable/pytorch-api.html)

### 适用场景 ✅

- 深度学习研究原型开发（灵活的动态图）
- 需要自定义训练循环的项目
- 动态网络结构（NLP 变长序列、树结构 RNN）
- 学术论文复现（研究社区主流）
- 计算机视觉（torchvision 生态丰富）
- NLP / LLM（Hugging Face 以 PyTorch 为主）

### 不适用场景 ❌

- 移动端/嵌入式部署（TFLite、Core ML 生态更成熟）
- 需要极致推理性能（TensorRT、ONNX Runtime 更专业）
- 纯 CPU 大规模分布式（有些场景 TensorFlow Serving 更成熟）
- 不涉及深度学习的科学计算（NumPy/SciPy 更轻量）

> 📖 Paper: Paszke et al., [NeurIPS 2019](https://arxiv.org/abs/1912.01703)

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 创建 Tensor | 从数据/形状创建 | `torch.tensor([1,2,3])`, `torch.zeros(3,4)` |
| GPU 迁移 | 设备转移 | `x.to('cuda')`, `model.cuda()` |
| 梯度开关 | 控制是否追踪 | `requires_grad=True`, `torch.no_grad()` |
| 反向传播 | 计算梯度 | `loss.backward()` |
| 参数更新 | 优化器一步 | `optimizer.step()` |
| 梯度清零 | 每个 batch 前 | `optimizer.zero_grad()` |
| 保存模型 | 序列化权重 | `torch.save(model.state_dict(), 'model.pth')` |
| 加载模型 | 恢复权重 | `model.load_state_dict(torch.load('model.pth'))` |
| 训练模式 | 启用 Dropout/BN | `model.train()` |
| 评估模式 | 关闭 Dropout/BN | `model.eval()` |

> 📖 Docs: [PyTorch Cheat Sheet](https://pytorch.org/tutorials/beginner/ptcheat.html)
