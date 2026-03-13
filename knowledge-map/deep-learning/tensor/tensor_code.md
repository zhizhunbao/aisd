---
topic: tensor
dimension: code
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.3"
  - "📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)"
  - "📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)"
expiry: 6m
status: current
---

# Tensor 代码参考

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)
> 📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import torch
import numpy as np

# === 创建 Tensor (Create Tensors) ===
# 从 Python 列表创建 (From Python list)
t = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(f"Tensor:\n{t}")
print(f"Shape: {t.shape}")     # torch.Size([2, 3])
print(f"Dtype: {t.dtype}")     # torch.int64
print(f"Device: {t.device}")   # cpu

# === 基本运算 (Basic Operations) ===
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])

print(f"加法 (Add): {a + b}")         # tensor([5., 7., 9.])
print(f"点积 (Dot): {torch.dot(a, b)}")  # tensor(32.)
print(f"逐元素乘 (Mul): {a * b}")     # tensor([4., 10., 18.])
```

**测试方法：** 复制到 Python 终端或 Jupyter 运行即可。

> 📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

---


## 完整实现示例

### 示例 1: Tensor 创建大全 (All Creation Methods)

```python
import torch
import numpy as np

# --- 1. 从数据创建 (From data) ---
# 自动推断 dtype (Auto-infer dtype)
t_int = torch.tensor([1, 2, 3])           # int64
t_float = torch.tensor([1.0, 2.0, 3.0])   # float32

# 指定 dtype (Specify dtype)
t_f16 = torch.tensor([1, 2], dtype=torch.float16)

# --- 2. 从 NumPy 创建 (From NumPy — 共享内存!) ---
np_arr = np.array([1.0, 2.0, 3.0])
t_np = torch.from_numpy(np_arr)    # 共享内存 (Shared memory!)
np_arr[0] = 99                      # 修改 NumPy → Tensor 也变
print(f"共享内存验证: {t_np}")       # tensor([99.,  2.,  3.])

# 不共享内存的方式 (Copy, not shared)
t_copy = torch.tensor(np_arr)       # 拷贝，不共享

# --- 3. 工厂函数 (Factory functions) ---
t_zeros = torch.zeros(3, 4)         # 全零 (All zeros)
t_ones = torch.ones(3, 4)           # 全一 (All ones)
t_rand = torch.rand(3, 4)           # 均匀随机 [0, 1)
t_randn = torch.randn(3, 4)         # 标准正态 N(0, 1)
t_eye = torch.eye(3)                # 单位矩阵 (Identity)
t_arange = torch.arange(0, 10, 2)   # [0, 2, 4, 6, 8]
t_linspace = torch.linspace(0, 1, 5) # [0, 0.25, 0.5, 0.75, 1]
t_empty = torch.empty(3, 4)         # 未初始化 (Uninitialized!)

# --- 4. 从已有 Tensor 创建 (From existing tensor) ---
t_like = torch.zeros_like(t_float)   # 相同 shape/dtype
t_new = t_float.new_ones(2, 3)      # 相同 dtype/device
```

> 📖 Docs: [PyTorch Tensor Creation Ops](https://pytorch.org/docs/stable/torch.html#tensor-creation-ops)

---

### 示例 2: Shape 操作 (Shape Manipulation)

```python
import torch

t = torch.arange(24)  # shape: (24,)

# --- reshape / view (改变 shape) ---
t2d = t.reshape(4, 6)          # (4, 6)
t3d = t.reshape(2, 3, 4)       # (2, 3, 4)
t_auto = t.reshape(2, -1)      # (2, 12) — 自动推断 -1 维度

# --- view (必须 contiguous) ---
t_view = t.view(6, 4)          # 等价于 reshape，但要求连续

# --- transpose / permute (转置) ---
t3d = torch.randn(2, 3, 4)
t_t = t3d.transpose(0, 2)      # (4, 3, 2) — 交换维度 0 和 2
t_p = t3d.permute(2, 0, 1)     # (4, 2, 3) — 自由重排维度

# --- squeeze / unsqueeze (压缩/扩展维度) ---
t_s = torch.randn(1, 3, 1, 4)
t_squeezed = t_s.squeeze()      # (3, 4) — 移除所有大小为 1 的维度
t_unsq = t_squeezed.unsqueeze(0) # (1, 3, 4) — 在维度 0 加 1

# --- flatten (展平) ---
t_flat = t3d.flatten()           # (24,) — 完全展平
t_flat2 = t3d.flatten(1)        # (2, 12) — 从维度 1 开始展平
```

> 📖 Docs: [PyTorch torch.Tensor — reshape](https://pytorch.org/docs/stable/generated/torch.Tensor.reshape.html)

---

### 示例 3: 索引与切片 (Indexing & Slicing)

```python
import torch

t = torch.tensor([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])

# --- 基本索引 (Basic indexing) ---
print(t[0])          # tensor([1, 2, 3, 4]) — 第 0 行
print(t[:, 0])       # tensor([1, 5, 9])    — 第 0 列
print(t[1, 2])       # tensor(7)            — 第 1 行第 2 列
print(t[-1])         # tensor([9, 10, 11, 12]) — 最后一行

# --- 切片 (Slicing) ---
print(t[:2, 1:3])    # tensor([[2, 3], [6, 7]]) — 前 2 行，第 1-2 列
print(t[..., -1])    # tensor([4, 8, 12]) — 所有行的最后一列

# --- 高级索引 (Advanced indexing) ---
idx = torch.tensor([0, 2])
print(t[idx])        # tensor([[1, 2, 3, 4], [9, 10, 11, 12]])

# --- 布尔索引 (Boolean indexing) ---
mask = t > 6
print(t[mask])       # tensor([7, 8, 9, 10, 11, 12])

# --- 赋值 (Assignment) ---
t[:, 1] = 0          # 第 1 列全部设为 0
print(t)
```

> 📖 Docs: [PyTorch Indexing, Slicing, Joining](https://pytorch.org/docs/stable/torch.html#indexing-slicing-joining)

---

### 示例 4: 数学运算 (Mathematical Operations)

```python
import torch

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b = torch.tensor([[5.0, 6.0], [7.0, 8.0]])

# --- 逐元素运算 (Element-wise) ---
print(a + b)          # 加法 (Addition)
print(a * b)          # Hadamard 乘积 (Element-wise multiply)
print(a ** 2)         # 平方 (Square)
print(torch.sqrt(a))  # 平方根 (Square root)

# --- 矩阵乘法 (Matrix multiplication) ---
print(a @ b)                    # 推荐写法
print(torch.matmul(a, b))      # 等价
print(torch.mm(a, b))          # 仅 2D

# --- 聚合运算 (Aggregation) ---
print(a.sum())         # 所有元素之和 → tensor(10.)
print(a.mean())        # 均值 → tensor(2.5)
print(a.max())         # 最大值 → tensor(4.)
print(a.sum(dim=0))    # 按列求和 → tensor([4., 6.])
print(a.sum(dim=1))    # 按行求和 → tensor([3., 7.])

# --- 单元素取值 (Single element extraction) ---
scalar = a.sum()
print(scalar.item())   # 10.0 — 转为 Python float
```

> 📖 Docs: [PyTorch Math Ops](https://pytorch.org/docs/stable/torch.html#math-operations)

---

### 示例 5: Device 管理 (CPU ↔ GPU)

```python
import torch

t = torch.randn(3, 4)

# --- 检查 GPU 是否可用 (Check GPU availability) ---
if torch.cuda.is_available():
    device = torch.device('cuda')
elif torch.backends.mps.is_available():  # Apple Silicon
    device = torch.device('mps')
else:
    device = torch.device('cpu')

print(f"使用设备 (Using device): {device}")

# --- 移至 GPU (Move to GPU) ---
t_gpu = t.to(device)
print(f"Device: {t_gpu.device}")

# --- 在 GPU 上创建 (Create on GPU directly) ---
t_gpu2 = torch.randn(3, 4, device=device)

# --- 移回 CPU (Move back to CPU) ---
t_cpu = t_gpu.cpu()

# --- 转 NumPy (必须在 CPU 上!) ---
t_np = t_cpu.numpy()

# --- 常见错误避免 (Avoid common error) ---
# 不同设备 Tensor 不能运算！
# t_cpu + t_gpu  # ← RuntimeError!
```

> 📖 Docs: [PyTorch CUDA Semantics](https://pytorch.org/docs/stable/notes/cuda.html)

---

### 示例 6: Autograd 基础 (Automatic Differentiation)

```python
import torch

# --- 创建需要梯度的 Tensor (Create tensor with grad tracking) ---
x = torch.tensor([2.0, 3.0], requires_grad=True)

# --- 前向计算 (Forward pass) ---
y = x ** 2 + 3 * x     # y = x² + 3x
z = y.sum()             # 标量化 (Scalarize)

# --- 反向传播 (Backward pass) ---
z.backward()

# --- 查看梯度 (View gradients) ---
# dy/dx = 2x + 3
print(f"x.grad = {x.grad}")  # tensor([7., 9.]) ← [2*2+3, 2*3+3]

# --- 梯度清零 (Zero gradients — 训练循环中必须!) ---
x.grad.zero_()

# --- 不追踪梯度的场景 (No grad context) ---
with torch.no_grad():
    y_no_grad = x ** 2    # 不会记录计算图
    print(f"requires_grad: {y_no_grad.requires_grad}")  # False
```

> 📖 Docs: [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)

---

### 示例 7: NumPy 互操作 (NumPy Interop)

```python
import torch
import numpy as np

# --- Tensor → NumPy (共享内存!) ---
t = torch.ones(3)
n = t.numpy()          # 共享内存 (Shared memory)
t.add_(1)              # 原地 +1
print(f"Tensor: {t}")  # tensor([2., 2., 2.])
print(f"NumPy:  {n}")  # [2. 2. 2.] ← 也变了！

# --- NumPy → Tensor (共享内存!) ---
n2 = np.ones(3)
t2 = torch.from_numpy(n2)    # 共享内存
np.add(n2, 1, out=n2)        # 原地 +1
print(f"NumPy:  {n2}")       # [2. 2. 2.]
print(f"Tensor: {t2}")       # tensor([2., 2., 2.]) ← 也变了！

# --- GPU Tensor → NumPy (必须先移到 CPU!) ---
if torch.cuda.is_available():
    t_gpu = torch.randn(3, device='cuda')
    # t_gpu.numpy()  # ← TypeError!
    n_gpu = t_gpu.cpu().numpy()    # ✅ 先 cpu() 再 numpy()

# --- 有梯度的 Tensor → NumPy (必须先 detach!) ---
t_grad = torch.randn(3, requires_grad=True)
# t_grad.numpy()  # ← RuntimeError!
n_grad = t_grad.detach().numpy()   # ✅ 先 detach() 再 numpy()
```

> 📖 Docs: [PyTorch Tensor Tutorial — Bridge with NumPy](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html#bridge-with-numpy)

---


## API 速查

### 创建 (Creation)

| 函数 | 参数 | 说明 |
|------|------|------|
| `torch.tensor(data)` | data, dtype, device | 从数据创建（拷贝） |
| `torch.from_numpy(ndarray)` | ndarray | 从 NumPy 创建（共享内存） |
| `torch.as_tensor(data)` | data, dtype, device | 智能创建（尽量共享） |
| `torch.zeros(*size)` | size, dtype, device | 全零 |
| `torch.ones(*size)` | size, dtype, device | 全一 |
| `torch.rand(*size)` | size | 均匀 [0,1) |
| `torch.randn(*size)` | size | 标准正态 |
| `torch.arange(start, end, step)` | start, end, step | 等差序列 |
| `torch.linspace(start, end, steps)` | start, end, steps | 等分序列 |
| `torch.eye(n)` | n | 单位矩阵 |
| `torch.empty(*size)` | size | 未初始化 |

### 属性 (Attributes)

| 属性/方法 | 返回类型 | 说明 |
|-----------|---------|------|
| `.shape` / `.size()` | torch.Size | 维度大小 |
| `.ndim` | int | 维度数 |
| `.dtype` | torch.dtype | 数据类型 |
| `.device` | torch.device | 存储设备 |
| `.stride()` | tuple | 内存步长 |
| `.numel()` | int | 元素总数 |
| `.is_contiguous()` | bool | 是否连续存储 |
| `.requires_grad` | bool | 是否追踪梯度 |

### Shape 操作 (Shape Operations)

| 方法 | 说明 | 是否返回 view |
|------|------|-------------|
| `.reshape(*shape)` | 改变 shape | 尽量 view |
| `.view(*shape)` | 改变 shape（必须连续） | 是 |
| `.transpose(d0, d1)` | 交换两个维度 | 是 |
| `.permute(*dims)` | 任意重排维度 | 是 |
| `.squeeze(dim)` | 移除大小为 1 的维度 | 是 |
| `.unsqueeze(dim)` | 在指定位置加维度 | 是 |
| `.flatten(start_dim)` | 展平 | 尽量 view |
| `.contiguous()` | 转为连续存储 | 可能拷贝 |

### 设备操作 (Device Operations)

| 方法 | 说明 |
|------|------|
| `.to(device)` | 移至指定设备 |
| `.cuda()` | 移至默认 GPU |
| `.cpu()` | 移回 CPU |
| `.numpy()` | 转为 NumPy（需 CPU + 无梯度） |
| `.item()` | 单元素转 Python 标量 |

> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

---


## 目录结构模板

### 简单结构

```
project/
├── main.py           # 入口，包含 Tensor 基本操作
└── requirements.txt  # torch, numpy
```

### 标准结构

```
project/
├── data/
│   ├── preprocess.py   # 数据预处理，NumPy → Tensor
│   └── dataset.py      # PyTorch Dataset
├── models/
│   └── model.py        # nn.Module 定义
├── utils/
│   └── tensor_utils.py # Tensor 工具函数
├── train.py            # 训练脚本
├── eval.py             # 评估脚本
└── requirements.txt
```

### 高级结构

```
project/
├── configs/
│   └── config.yaml      # 超参数配置
├── data/
│   ├── preprocess.py    # 数据清洗 + 转换
│   ├── dataset.py       # 自定义 Dataset
│   └── transforms.py    # 数据增强 Tensor 变换
├── models/
│   ├── __init__.py
│   ├── backbone.py      # 特征提取
│   └── head.py          # 分类/检测头
├── engine/
│   ├── trainer.py       # 训练循环
│   └── evaluator.py     # 评估循环
├── utils/
│   ├── tensor_ops.py    # 自定义 Tensor 操作
│   ├── device.py        # Device 管理工具
│   └── checkpoint.py    # 模型保存/加载
├── train.py
├── eval.py
└── requirements.txt
```
