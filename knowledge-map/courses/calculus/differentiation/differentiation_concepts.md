---
topic: differentiation
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.4,6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Boyd & Vandenberghe, Convex Optimization, Ch.2-3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/boyd_convex_optimization.pdf"
expiry: 12m
status: current
---

# 微分 核心概念

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---


## 术语定义

### 导数 (Derivative)

函数 $f(x)$ 在点 $x$ 处的瞬时变化率，定义为极限 $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$。几何上是函数图像在该点的切线斜率。导数存在意味着函数在该点"光滑"（没有尖角或跳跃）。一元函数的导数是标量。

> 易混淆：**导数 vs 微分** — 导数 $f'(x)$ 是一个数（变化率）；微分 $df = f'(x)\,dx$ 是一个无穷小量（变化量的线性近似）。口语中常混用，但严格来说不同

### 偏导数 (Partial Derivative)

多元函数 $f(x_1, x_2, \ldots, x_n)$ 对其中一个变量 $x_i$ 求导，保持其他变量不变：$\frac{\partial f}{\partial x_i}$。偏导数度量"只沿一个方向变化时，函数如何变化"。它是多元微分的基础构件。

> 易混淆：**偏导数 vs 全导数** — 偏导数只考虑一个变量的变化；全导数（全微分）考虑所有变量同时变化 $df = \sum_i \frac{\partial f}{\partial x_i} dx_i$

### 梯度 (Gradient)

标量函数 $f: \mathbb{R}^n \to \mathbb{R}$ 的所有偏导数组成的向量 $\nabla f = \left[\frac{\partial f}{\partial x_1}, \ldots, \frac{\partial f}{\partial x_n}\right]^\top$。梯度指向函数值增长最快的方向，其大小是最大增长率。梯度下降的核心就是沿梯度的反方向更新参数 $\theta \leftarrow \theta - \eta \nabla_\theta L$。

> 易混淆：**梯度 vs 导数** — 一元函数的导数是标量；多元函数的梯度是向量。梯度是导数在多维空间的推广

### Jacobian 矩阵 (Jacobian Matrix)

向量函数 $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$ 的一阶偏导矩阵 $\mathbf{J} \in \mathbb{R}^{m \times n}$，其中 $J_{ij} = \frac{\partial f_i}{\partial x_j}$。Jacobian 描述了向量输入的微小变化如何映射为向量输出的微小变化。当 $m=1$ 时，Jacobian 退化为梯度的转置。

> 易混淆：**Jacobian vs 梯度** — 梯度用于 $f: \mathbb{R}^n \to \mathbb{R}$（标量输出），是列向量；Jacobian 用于 $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$（向量输出），是矩阵

### Hessian 矩阵 (Hessian Matrix)

标量函数 $f: \mathbb{R}^n \to \mathbb{R}$ 的二阶偏导矩阵 $\mathbf{H} \in \mathbb{R}^{n \times n}$，其中 $H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}$。Hessian 描述函数的局部曲率。正定 Hessian 意味着严格局部极小值；特征值决定了各方向的弯曲程度。牛顿法利用 Hessian：$\theta \leftarrow \theta - \mathbf{H}^{-1} \nabla f$。

> 易混淆：**Hessian vs Jacobian** — Hessian 是标量函数的二阶偏导矩阵（$n \times n$）；Jacobian 是向量函数的一阶偏导矩阵（$m \times n$）

### 链式法则 (Chain Rule)

复合函数的导数等于各层导数的乘积。一元版：$(f \circ g)'(x) = f'(g(x)) \cdot g'(x)$。多元版：$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial x}$（Jacobian 矩阵乘法）。它是反向传播的数学基础——深度网络是多层复合函数，链式法则让梯度能从输出逐层传回输入。

### 方向导数 (Directional Derivative)

函数 $f$ 在方向 $\mathbf{u}$（单位向量）上的变化率 $D_\mathbf{u} f = \nabla f \cdot \mathbf{u}$。梯度方向的方向导数最大（= $\|\nabla f\|$），负梯度方向最小，垂直于梯度的方向为零。这是"梯度是最陡上升方向"的精确表述。

### 自动微分 (Automatic Differentiation / Autograd)

自动地对计算机程序精确求导的技术。将程序分解为基本运算（加减乘除、指数、三角函数等），利用链式法则自动组合各运算的已知导数。有前向模式和反向模式两种。PyTorch、JAX、TensorFlow 都使用反向模式自动微分（反向传播的高效实现）。

> 易混淆：**自动微分 vs 数值微分 vs 符号微分** — 自动微分精确且高效（程序化链式法则）；数值微分简单但有舍入误差（$\frac{f(x+h)-f(x)}{h}$）；符号微分精确但表达式膨胀（SymPy 风格）

### 反向传播 (Backpropagation)

深度学习中用反向模式自动微分计算损失函数关于所有参数的梯度的算法。从输出端（损失 $L$）开始，沿计算图反向传播梯度，逐层应用链式法则。一次前向传播 + 一次反向传播就能算出所有参数的梯度，时间复杂度与前向传播相当。

### 计算图 (Computational Graph)

将数学表达式表示为有向无环图 (DAG)，节点是运算，边是数据流。PyTorch 在前向传播时动态构建计算图，反向传播时沿图的逆序计算梯度。计算图是自动微分的数据结构基础。

### 数值微分 (Numerical Differentiation)

用有限差分近似导数：$f'(x) \approx \frac{f(x+h)-f(x)}{h}$（前向差分）或 $\frac{f(x+h)-f(x-h)}{2h}$（中心差分）。简单易实现，常用于验证自动微分的结果（gradient checking），但有舍入误差和截断误差。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.1-5.4
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5
> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.2-3

---


## 概念辨析

### 梯度 vs Jacobian vs Hessian

| 维度 | 梯度 (Gradient) | Jacobian | Hessian |
|------|---|---|---|
| **输入→输出** | $f: \mathbb{R}^n \to \mathbb{R}$ | $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$ | $f: \mathbb{R}^n \to \mathbb{R}$ |
| **阶数** | 一阶 | 一阶 | 二阶 |
| **结果维度** | 向量 $\in \mathbb{R}^n$ | 矩阵 $\in \mathbb{R}^{m \times n}$ | 矩阵 $\in \mathbb{R}^{n \times n}$ |
| **元素** | $\frac{\partial f}{\partial x_i}$ | $\frac{\partial f_i}{\partial x_j}$ | $\frac{\partial^2 f}{\partial x_i \partial x_j}$ |
| **ML 用途** | 梯度下降 | 变换的局部线性化 | 牛顿法、凸性判断 |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2-5.4

### 自动微分 vs 数值微分 vs 符号微分

| 维度 | 自动微分 (AD) | 数值微分 | 符号微分 |
|------|---|---|---|
| **精度** | 精确（机器精度） | 近似（$O(h^2)$ 误差） | 精确 |
| **效率** | 高（$O(1)$ 倍前向代价） | 中（需 $O(n)$ 次评估） | 低（表达式膨胀） |
| **可处理对象** | 程序/代码 | 黑箱函数 | 数学公式 |
| **典型工具** | PyTorch, JAX, TensorFlow | `scipy.misc.derivative` | SymPy, Mathematica |
| **ML 主要用途** | 训练 (backprop) | gradient checking | 理论推导 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────┐
│            微分 (Differentiation)                      │
├──────────────────────────────────────────────────────┤
│  一元微分                                              │
│  ├─ 导数: f'(x) = lim [f(x+h)-f(x)]/h               │
│  ├─ 基本求导法则: 幂/指数/对数/三角                     │
│  └─ 链式法则: (f∘g)' = f'(g(x))·g'(x)               │
├──────────────────────────────────────────────────────┤
│  多元微分                                              │
│  ├─ 偏导数: ∂f/∂x_i                                   │
│  ├─ 梯度: ∇f ∈ ℝⁿ (一阶)                             │
│  ├─ Jacobian: J ∈ ℝᵐˣⁿ (向量→向量)                   │
│  └─ Hessian: H ∈ ℝⁿˣⁿ (二阶)                        │
├──────────────────────────────────────────────────────┤
│  计算方法                                              │
│  ├─ 解析微分: 手动推导                                  │
│  ├─ 符号微分: SymPy                                    │
│  ├─ 数值微分: 有限差分                                  │
│  └─ 自动微分: PyTorch / JAX (前向/反向模式)            │
├──────────────────────────────────────────────────────┤
│  ML 应用                                               │
│  ├─ 反向传播 (Backpropagation)                         │
│  ├─ 梯度下降 (SGD / Adam / ...)                        │
│  └─ 牛顿法 / 二阶优化                                  │
└──────────────────────────────────────────────────────┘
```

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5

### 适用场景 ✅

- 训练神经网络：反向传播计算损失对参数的梯度
- 优化任何可微目标函数：梯度下降、Adam、L-BFGS
- 灵敏度分析：输入变化 $dx$ 如何影响输出 $dy$
- Taylor 展开近似：$f(x+h) \approx f(x) + f'(x)h + \frac{1}{2}f''(x)h^2$
- 最优性条件判断：$\nabla f = 0$ 且 $\mathbf{H} \succ 0$

### 不适用场景 ❌

- 不可微函数的优化：如 $f(x) = |x|$ 在 $x=0$ 处不可微（需次梯度 / 近端算子）
- 离散目标函数：如组合优化（排列、子集选择）——没有连续的"变化率"
- 高阶导数计算量大：Hessian 的存储是 $O(n^2)$，大规模模型中不实用

> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.3

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| $(x^n)' = nx^{n-1}$ | 幂函数求导 | $(x^3)' = 3x^2$ |
| $(e^x)' = e^x$ | 指数函数求导 | — |
| $(\ln x)' = 1/x$ | 对数函数求导 | — |
| $(\sin x)' = \cos x$ | 正弦求导 | — |
| $(f \cdot g)' = f'g + fg'$ | 乘积法则 | — |
| $(f/g)' = (f'g - fg')/g^2$ | 商法则 | — |
| $(f \circ g)' = f'(g) \cdot g'$ | 链式法则 | — |
| $\nabla f = [\partial f/\partial x_i]$ | 梯度 | $\nabla(x_1^2+x_2^2) = [2x_1, 2x_2]^\top$ |
| $J_{ij} = \partial f_i/\partial x_j$ | Jacobian | — |
| $H_{ij} = \partial^2 f/\partial x_i \partial x_j$ | Hessian | — |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5, Table 5.1
