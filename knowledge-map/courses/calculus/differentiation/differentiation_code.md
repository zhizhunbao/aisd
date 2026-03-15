---
topic: differentiation
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: PyTorch Autograd — https://pytorch.org/docs/stable/autograd.html"
  - "📖 Docs: JAX autodiff — https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html"
  - "📖 Docs: SymPy diff — https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html"
  - "📖 Docs: SciPy misc.derivative — https://docs.scipy.org/doc/scipy/reference/generated/scipy.misc.derivative.html"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# 微分 代码参考

> 📖 Docs: [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)
> 📖 Docs: [JAX autodiff](https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import torch

# ============================================================
# 1. PyTorch 自动微分 / PyTorch Autograd
# ============================================================
# 目标: 求 f(x) = x² + 3x 在 x=2 处的导数
# f'(x) = 2x + 3, f'(2) = 7

x = torch.tensor(2.0, requires_grad=True)  # 标记需要梯度 / Enable gradient tracking
f = x**2 + 3*x                             # 前向计算 / Forward pass
f.backward()                                # 反向传播 / Backward pass
print(f"f'(2) = {x.grad}")                 # f'(2) = 7.0 ✅

# ============================================================
# 2. 数值微分验证 / Numerical gradient check
# ============================================================
h = 1e-5
x_val = 2.0
numerical_grad = ((x_val+h)**2 + 3*(x_val+h) - ((x_val-h)**2 + 3*(x_val-h))) / (2*h)
print(f"数值梯度 = {numerical_grad:.6f}")  # ≈ 7.000000 ✅
```

**测试方法：** 运行后检查 PyTorch 梯度和数值梯度都约等于 7.0

> 📖 Docs: [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)

---

## 完整实现示例

### 示例 1: 多元函数的梯度 + 梯度下降（PyTorch）

```python
import torch
import matplotlib.pyplot as plt

# ============================================================
# 1. 定义目标函数 / Define Objective Function
# ============================================================
# f(x₁, x₂) = x₁² + 2x₂² — 椭圆碗
# 最小值在 (0, 0)，梯度 ∇f = [2x₁, 4x₂]
def f(x):
    """椭圆碗函数 / Elliptical bowl function"""
    return x[0]**2 + 2*x[1]**2

# ============================================================
# 2. 梯度下降 / Gradient Descent
# ============================================================
lr = 0.1                                            # 学习率 / Learning rate
x = torch.tensor([3.0, 2.0], requires_grad=True)    # 初始点 / Starting point
trajectory = [x.detach().clone().numpy()]             # 记录轨迹 / Record path

for step in range(50):
    loss = f(x)                # 前向计算 / Forward pass
    loss.backward()            # 反向传播 / Backward pass
    
    with torch.no_grad():      # 更新时不追踪梯度 / No grad tracking during update
        x -= lr * x.grad       # θ ← θ - η∇L / Gradient descent step
        x.grad.zero_()          # 清零梯度 / Zero gradients
    
    trajectory.append(x.detach().clone().numpy())
    if step % 10 == 0:
        print(f"Step {step}: x={x.detach().numpy()}, f(x)={f(x).item():.4f}")

# ============================================================
# 3. 可视化轨迹 / Visualize Trajectory
# ============================================================
import numpy as np
traj = np.array(trajectory)
x1_grid, x2_grid = np.meshgrid(np.linspace(-4, 4, 100), np.linspace(-3, 3, 100))
z = x1_grid**2 + 2*x2_grid**2

fig, ax = plt.subplots(figsize=(8, 6))
ax.contour(x1_grid, x2_grid, z, levels=20, cmap='viridis')
ax.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=3, label='GD 轨迹')
ax.plot(traj[0, 0], traj[0, 1], 'r*', markersize=15, label='起点')
ax.plot(0, 0, 'g*', markersize=15, label='最优解')
ax.set_xlabel('x₁')
ax.set_ylabel('x₂')
ax.set_title('梯度下降轨迹 / Gradient Descent Trajectory')
ax.legend()
plt.tight_layout()
plt.savefig('gd_trajectory.png', dpi=150)
plt.show()
```

> 📖 Docs: [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.4.3

---

### 示例 2: 神经网络反向传播（手动 vs 自动）

```python
import torch
import torch.nn as nn
import numpy as np

# ============================================================
# 1. 手动反向传播 / Manual Backpropagation
# ============================================================
np.random.seed(42)

# 简单两层网络: x → W₁ → ReLU → W₂ → MSE Loss
# 维度: x(2) → h(3) → y(1)
x = np.array([1.0, 2.0])
y_true = np.array([1.0])
W1 = np.random.randn(3, 2) * 0.5  # 第一层权重 / Layer 1 weights
W2 = np.random.randn(1, 3) * 0.5  # 第二层权重 / Layer 2 weights

# 前向传播 / Forward pass
z1 = W1 @ x                       # 线性变换 / Linear
h1 = np.maximum(0, z1)            # ReLU 激活 / ReLU activation
z2 = W2 @ h1                      # 线性变换 / Linear
loss = 0.5 * (z2 - y_true)**2     # MSE 损失 / MSE loss

# 反向传播 / Backward pass (链式法则)
dL_dz2 = z2 - y_true              # ∂L/∂z₂ = ŷ - y
dL_dW2 = dL_dz2.reshape(-1, 1) @ h1.reshape(1, -1)  # ∂L/∂W₂
dL_dh1 = W2.T @ dL_dz2            # ∂L/∂h₁
dL_dz1 = dL_dh1 * (z1 > 0)        # ReLU 的梯度: 1 if z>0, 0 otherwise
dL_dW1 = dL_dz1.reshape(-1, 1) @ x.reshape(1, -1)   # ∂L/∂W₁

print(f"手动 ∂L/∂W₁:\n{dL_dW1}")

# ============================================================
# 2. PyTorch 自动反向传播 / PyTorch Auto Backprop
# ============================================================
x_t = torch.tensor(x, dtype=torch.float32)
y_t = torch.tensor(y_true, dtype=torch.float32)
W1_t = torch.tensor(W1, dtype=torch.float32, requires_grad=True)
W2_t = torch.tensor(W2, dtype=torch.float32, requires_grad=True)

z1_t = W1_t @ x_t
h1_t = torch.relu(z1_t)
z2_t = W2_t @ h1_t
loss_t = 0.5 * (z2_t - y_t)**2

loss_t.backward()
print(f"\nPyTorch ∂L/∂W₁:\n{W1_t.grad}")

# ============================================================
# 3. 验证一致性 / Verify Consistency
# ============================================================
print(f"\n差异: {np.abs(dL_dW1 - W1_t.grad.numpy()).max():.2e}")  # 应接近 0
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---

### 示例 3: 符号微分 + Jacobian + Hessian（SymPy）

```python
from sympy import symbols, diff, Matrix, Function, exp, hessian, simplify, pprint

# ============================================================
# 1. 符号求导 / Symbolic Differentiation
# ============================================================
x = symbols('x')

# f(x) = e^(-x²/2) 的导数
f = exp(-x**2 / 2)
f_prime = diff(f, x)
print(f"f(x) = {f}")
print(f"f'(x) = {f_prime}")   # -x*exp(-x**2/2)

# ============================================================
# 2. 多元梯度 / Multivariate Gradient
# ============================================================
x1, x2, x3 = symbols('x1 x2 x3')
g = x1**2 * x2 + x2**3 * x3 + x1 * x3

gradient = Matrix([diff(g, v) for v in [x1, x2, x3]])
print(f"\n∇g = {gradient.T}")  # [2*x1*x2 + x3, x1**2 + 3*x2**2*x3, x2**3 + x1]

# ============================================================
# 3. Jacobian 矩阵 / Jacobian Matrix
# ============================================================
f1 = x1**2 + x2
f2 = x1 * x2 + x2**2
F = Matrix([f1, f2])
X = Matrix([x1, x2])
J = F.jacobian(X)
print(f"\nJacobian J =")
pprint(J)  # [[2*x1, 1], [x2, x1+2*x2]]

# ============================================================
# 4. Hessian 矩阵 / Hessian Matrix
# ============================================================
h = x1**2 + 4*x1*x2 + x2**2
H = hessian(h, [x1, x2])
print(f"\nHessian H =")
pprint(H)  # [[2, 4], [4, 2]]
```

> 📖 Docs: [SymPy calculus](https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html)

---

## API 速查

### PyTorch Autograd

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `tensor.requires_grad_(True)` | — | — | 启用梯度追踪 / Enable gradient tracking |
| `tensor.backward()` | `gradient` | `None` | 反向传播计算梯度 / Compute gradients |
| `tensor.grad` | — | — | 访问累积梯度 / Access accumulated gradients |
| `tensor.grad.zero_()` | — | — | 清零梯度 / Zero out gradients |
| `torch.no_grad()` | — | — | 上下文：禁用梯度 / Context: disable grad |
| `torch.autograd.grad(y, x)` | `y, x` | — | 函数式梯度 / Functional gradient |
| `torch.autograd.functional.jacobian(f, x)` | `f, x` | — | 计算 Jacobian |
| `torch.autograd.functional.hessian(f, x)` | `f, x` | — | 计算 Hessian |

### SymPy 符号微分

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `diff(expr, x)` | 表达式, 变量 | 一阶导数 / First derivative |
| `diff(expr, x, n)` | 表达式, 变量, 阶数 | $n$ 阶导数 / $n$-th derivative |
| `diff(expr, x1, x2)` | 表达式, 变量1, 变量2 | 混合偏导 $\partial^2 f/\partial x_1 \partial x_2$ |
| `Matrix.jacobian(X)` | 变量矩阵 | Jacobian 矩阵 |
| `hessian(expr, vars)` | 表达式, 变量列表 | Hessian 矩阵 |

### 数值微分

| 函数 | 说明 |
|------|------|
| `scipy.misc.derivative(f, x0, dx=1e-5)` | 中心差分数值导数 |
| `(f(x+h)-f(x-h))/(2*h)` | 手动中心差分（精度 $O(h^2)$） |
| `torch.autograd.gradcheck(f, inputs)` | 对比自动微分 vs 数值微分（验证用） |

### 常用工具

| 函数 | 说明 |
|------|------|
| `torch.optim.SGD(params, lr)` | SGD 优化器（使用梯度） |
| `torch.optim.Adam(params, lr)` | Adam 优化器（自适应学习率） |
| `loss.backward()` + `optimizer.step()` | 标准训练循环 |

> 📖 Docs: [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)
> 📖 Docs: [SymPy calculus](https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html)

---

## 目录结构模板

### 简单结构

```
differentiation_demo/
├── autograd_demo.py         ← PyTorch 自动微分
├── numerical_grad.py        ← 数值微分 + gradient checking
└── symbolic_diff.py         ← SymPy 符号微分
```

### 标准结构

```
differentiation_project/
├── autograd/
│   ├── basic.py             ← 基础自动微分
│   ├── custom_function.py   ← 自定义 autograd Function
│   └── jacobian_hessian.py  ← Jacobian / Hessian 计算
├── optimization/
│   ├── gradient_descent.py  ← 手动 GD 实现
│   ├── adam.py              ← Adam 实现
│   └── newton.py            ← 牛顿法（二阶）
├── visualization/
│   ├── grad_flow.py         ← 梯度流可视化
│   └── loss_landscape.py    ← 损失曲面可视化
├── tests/
│   └── grad_check.py        ← 数值梯度验证
└── requirements.txt
```

> 📖 Docs: [PyTorch](https://pytorch.org/) / [SymPy](https://docs.sympy.org/)
