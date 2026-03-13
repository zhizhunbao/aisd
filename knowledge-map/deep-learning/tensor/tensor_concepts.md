---
topic: tensor
dimension: concepts
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.3"
  - "📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)"
  - "📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)"
expiry: 12m
status: current
---

# Tensor 核心概念

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3
> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## 术语定义

### 张量 (Tensor)

多维数组，是深度学习中数据的统一表示形式。一个 Tensor 中所有元素必须是相同数据类型。它可以理解为标量、向量、矩阵的高维推广——标量是 0 维 Tensor，向量是 1 维 Tensor，矩阵是 2 维 Tensor，以此类推。

> 易混淆：**NumPy ndarray** — ndarray 也是多维数组，但不支持 GPU 和 autograd

### 形状 (Shape)

描述 Tensor 每个维度的大小。例如 `torch.Size([3, 4])` 表示 3 行 4 列的二维 Tensor。在 PyTorch 中通过 `tensor.shape` 或 `tensor.size()` 获取。

> 易混淆：**Rank / 维度数** — shape 描述每个维度的大小，rank 只是维度的数量

### 阶 / 秩 (Rank / ndim)

Tensor 的维度数量，又叫"阶"。标量的 rank 是 0，向量是 1，矩阵是 2。在 PyTorch 中通过 `tensor.ndim` 或 `len(tensor.shape)` 获取。

> 易混淆：**矩阵的秩 (matrix rank)** — 矩阵的秩是指线性无关列/行向量的最大数量，与 Tensor 的 rank（维度数）完全不同

### 数据类型 (dtype)

Tensor 中元素的数据类型。PyTorch 常用类型包括 `torch.float32`（默认浮点数）、`torch.int64`（默认整数）、`torch.bool` 等。dtype 决定了精度和内存占用。

> 易混淆：**Python 原生类型** — `float` 是 64 位的，PyTorch 默认 `float32` 是 32 位

### 设备 (Device)

Tensor 所在的计算硬件。`cpu` 表示主内存，`cuda:0` 表示第一块 NVIDIA GPU。参与运算的 Tensor 必须在同一个 device 上。

> 易混淆：**Storage** — device 决定 Tensor 存在哪里，Storage 是底层内存分配的具体实现

### 步长 (Stride)

在内存中从一个维度的某个元素跳到下一个元素所需跳过的元素数。例如一个 `(3, 4)` 行优先 Tensor 的 stride 是 `(4, 1)` — 跳一行需跨 4 个元素，跳一列只需跨 1 个元素。Stride 是理解 Tensor 视图 (view) 的关键。

> 易混淆：**Shape** — shape 描述逻辑维度大小，stride 描述内存中的物理布局

### 视图 (View)

共享底层数据但具有不同 shape/stride 的 Tensor。通过 `reshape()` / `view()` / 转置等操作创建。修改 view 会同时修改原 Tensor 的数据（零拷贝）。

> 易混淆：**Copy (副本)** — view 共享内存（零拷贝），copy 分配新内存（`clone()` 创建副本）

### 自动微分 (Autograd)

PyTorch 的自动微分引擎。当 `requires_grad=True` 时，PyTorch 会记录对该 Tensor 的所有操作，在 `.backward()` 时自动计算梯度。这是训练神经网络的基础。

> 易混淆：**数值微分** — autograd 是精确的符号/链式微分，不是有限差分的近似

### 原地操作 (In-place Operation)

直接修改 Tensor 自身数据的操作，在 PyTorch 中以下划线 `_` 结尾（如 `add_()`, `copy_()`）。节省内存但破坏计算图历史，可能导致 autograd 出错。

> 易混淆：**Out-of-place 操作** — 返回新 Tensor，不修改原数据，autograd 友好

### 广播 (Broadcasting)

不同 shape 的 Tensor 做逐元素运算时，自动扩展较小 Tensor 以匹配较大 Tensor 的规则。规则：从最右维度对齐，每个维度大小要么相等、要么其中一个是 1。

> 易混淆：**显式 expand / repeat** — broadcasting 隐式扩展不分配新内存，repeat 会复制数据

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3
> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## 概念辨析

### Tensor vs NumPy ndarray

| 维度 | Tensor (PyTorch) | ndarray (NumPy) |
|------|-----------------|-----------------|
| **本质** | 多维数组 + 计算图 | 多维数组 |
| **GPU 支持** | ✅ 原生支持 `.to('cuda')` | ❌ 需要 CuPy 等第三方库 |
| **自动微分** | ✅ `requires_grad=True` | ❌ 不支持 |
| **内存共享** | ✅ `torch.from_numpy()` 共享 | ✅ `.numpy()` 共享 |
| **API 风格** | 与 NumPy 高度相似 | 科学计算的事实标准 |
| **默认浮点** | `float32` | `float64` |
| **适用场景** | 深度学习训练/推理 | 通用科学计算/数据处理 |

> 📖 Docs: [PyTorch Tensor Tutorial — Bridge with NumPy](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html#bridge-with-numpy)

### view vs clone (副本)

| 维度 | view（视图） | clone（副本） |
|------|-------------|--------------|
| **内存** | 共享底层数据（零拷贝） | 新分配内存，完整复制 |
| **获取方式** | `reshape()`, `view()`, 切片, `transpose()` | `clone()`, `.detach().clone()` |
| **修改影响** | 修改 view 会改变原 Tensor | 互不影响 |
| **性能** | 快，无内存开销 | 慢，需要拷贝 |
| **使用场景** | 改变 shape 但不改数据 | 需要独立副本时 |

> 📖 Docs: [Tensor Views](https://pytorch.org/docs/stable/tensor_view.html)

### 连续存储 (contiguous) vs 非连续 (non-contiguous)

| 维度 | contiguous | non-contiguous |
|------|-----------|---------------|
| **含义** | 内存中元素按 stride 连续排列 | 转置等操作后 stride 不连续 |
| **检查** | `tensor.is_contiguous()` → True | `tensor.is_contiguous()` → False |
| **影响** | `view()` 可直接使用 | `view()` 报错，需先 `.contiguous()` |
| **场景** | 新创建的 Tensor | `transpose()` / `permute()` 后 |

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────┐
│               torch.Tensor                    │
├──────────────────────────────────────────────┤
│  逻辑属性                                     │
│  ├── shape (torch.Size)    维度大小           │
│  ├── ndim (int)            维度数量           │
│  ├── dtype (torch.dtype)   数据类型           │
│  └── device (torch.device) 存储设备           │
├──────────────────────────────────────────────┤
│  物理属性                                     │
│  ├── stride (tuple)        内存步长           │
│  ├── storage()             底层 Storage       │
│  ├── is_contiguous()       是否连续存储       │
│  └── data_ptr()            内存地址           │
├──────────────────────────────────────────────┤
│  计算图属性                                   │
│  ├── requires_grad (bool)  是否追踪梯度       │
│  ├── grad (Tensor)         累积梯度           │
│  ├── grad_fn (Function)    创建此 Tensor 的操作│
│  └── is_leaf (bool)        是否叶节点         │
└──────────────────────────────────────────────┘
```

> 📖 Docs: [PyTorch Tensor Attributes](https://pytorch.org/docs/stable/tensor_attributes.html)

### 适用场景 ✅

- 深度学习模型的输入、输出、参数表示
- 图像数据 (B, C, H, W)、文本序列 (B, T, D)、表格数据 (B, F)
- GPU 并行计算加速
- 需要自动微分的数值优化
- 与 NumPy 生态无缝衔接的科学计算

### 不适用场景 ❌

- 不规则（ragged）数据结构（如不同长度的列表嵌套）
- 纯 CPU、不需要梯度的简单科学计算（用 NumPy 更直接）
- 需要稀疏表示的超大规模数据（虽然 PyTorch 有稀疏 Tensor 支持，但不如 SciPy 成熟）

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 创建 Tensor | 从数据创建 | `torch.tensor([1, 2, 3])` |
| 从 NumPy 创建 | 共享内存 | `torch.from_numpy(np_arr)` |
| 全零/全一 | 指定 shape | `torch.zeros(3, 4)` / `torch.ones(3, 4)` |
| 随机初始化 | 均匀分布 [0,1) | `torch.rand(3, 4)` |
| 查看属性 | shape/dtype/device | `t.shape`, `t.dtype`, `t.device` |
| 转 GPU | 移至 CUDA 设备 | `t.to('cuda')` / `t.cuda()` |
| 转 NumPy | 转回 ndarray | `t.numpy()` / `t.detach().cpu().numpy()` |
| 改变 shape | 不改数据 | `t.reshape(2, 6)` / `t.view(2, 6)` |
| 矩阵乘法 | 2D 矩阵乘 | `t1 @ t2` / `torch.matmul(t1, t2)` |
| 开启梯度 | 用于训练 | `t.requires_grad_(True)` |
| 原地操作 | 注意 `_` 后缀 | `t.add_(5)` |

> 📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
