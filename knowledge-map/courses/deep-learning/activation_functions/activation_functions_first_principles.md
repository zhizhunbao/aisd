---
topic: activation_functions
dimension: first_principles
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 §6.1, §6.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Cybenko, 'Approximation by Superpositions of a Sigmoidal Function', Mathematics of Control, Signals and Systems, 1989"
  - "📖 Paper: Hornik, 'Approximation capabilities of multilayer feedforward networks', Neural Networks, 1991"
expiry: 12m
status: current
---

# Activation Functions 第一性原理

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.1, §6.3
> 📖 Paper: Cybenko, "Approximation by Superpositions of a Sigmoidal Function", 1989

---


## 核心问题链

> 用"5 个为什么"式的递归追问，从表面功能一路追到不可再分的基本事实。

### 问题链

1. **激活函数在做什么？** → 在线性变换 $z = Wx + b$ 之后施加一个非线性函数 $g(z)$
2. **为什么需要非线性？** → 因为多层线性变换的复合仍然是线性的（矩阵乘法结合律：$W_2 W_1 = W'$），没有非线性就无法逼近非线性函数
3. **为什么需要逼近非线性函数？** → 因为现实世界的绝大多数输入-输出关系是非线性的（图像→标签、语音→文本、文本→翻译）
4. **这个"逼近任意函数"的能力的根基是什么？** → Universal Approximation Theorem：一层足够宽的网络 + 非线性激活可以逼近任意连续函数到任意精度
5. **UAT 的前提是什么？不能再拆分了吗？** → 不能。UAT 的核心前提就是激活函数必须是非常数、有界、连续的非线性函数——这是公理

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.4.1
> 📖 Paper: Cybenko, 1989; Hornik, 1991

---


## 公理与基本假设

> 列出本技术赖以成立的**不可再分的基本事实**。这些是"如果它们不成立，整个技术就崩塌"的根基。

### 公理 1: 矩阵乘法的结合律 (Associativity of Matrix Multiplication)

**陈述：** 对于任意可乘矩阵 $A, B, C$，$(AB)C = A(BC)$。

**白话：** 三个矩阵连乘，不管先乘哪两个，结果一样。这就是说，两层线性变换 $W_2(W_1 x) = (W_2 W_1) x$ 等价于一层。

**来源：** 线性代数基本定理。任何线性代数教科书均可验证。

**可验证性：** 在任何维度、任何数值下都成立。这是数学公理，无例外。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.1

### 公理 2: 非线性打破结合律 (Nonlinearity Breaks Associativity)

**陈述：** 如果在矩阵乘法之间插入非线性函数 $g$，则 $g(W_2 \cdot g(W_1 x)) \neq g(W' x)$，一般不存在等价的单层表示。

**白话：** 加了非线性函数后，两层网络不能被压缩成一层。每一层真的在做"不同的事"。

**来源：** 反证法——如果非线性变换后仍满足结合律，那它就不是非线性的。

**可验证性：** 对任何非仿射函数 $g$ 成立。仿射函数 $g(z) = az + b$ 是唯一的例外（仍为线性）。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.1

### 公理 3: Universal Approximation Theorem (万能逼近定理)

**陈述：** 一个单隐藏层的前馈网络，如果隐藏层有足够多的神经元，且使用非常数、有界、连续的激活函数，则可以以任意精度逼近定义在紧致子集上的任意连续函数。

**白话：** 只要激活函数是"弯的"（非线性）、"光滑的"（连续）、"有边界的"（有界），一层够宽的网络就能学会任何函数。

**来源：** Cybenko, 1989 (Sigmoid)；Hornik, 1991 (推广到一般激活函数)。这是数学定理，有严格证明。

**可验证性：** 定理在理论上永远成立，但实际需要的网络宽度可能是指数级的。ReLU 不满足"有界"条件，但后续研究证明了 ReLU 也满足 UAT（Leshno et al., 1993）。

> 📖 Paper: Cybenko, "Approximation by Superpositions of a Sigmoidal Function", 1989
> 📖 Paper: Hornik, "Approximation capabilities of multilayer feedforward networks", 1991

### 公理 4: 链式法则 (Chain Rule of Calculus)

**陈述：** 对于复合函数 $f(g(x))$，$\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}$。

**白话：** 要求一个"嵌套"函数的梯度，只需把每层的梯度连乘起来。

**来源：** 微积分基本定理。牛顿和莱布尼茨，17 世纪。

**可验证性：** 在函数可微的任何地方都成立。反向传播算法完全建立在此公理之上。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.5

### 公理 5: 梯度下降需要非零梯度 (Gradient Descent Requires Nonzero Gradient)

**陈述：** 梯度下降通过 $W \leftarrow W - \eta \nabla L$ 更新权重。如果 $\nabla L = 0$（但不在全局最优点），学习停止。

**白话：** 优化器依赖梯度来"指路"。如果激活函数在某些区域梯度为零，那些区域的权重就永远学不动了。

**来源：** 优化理论基本原理。

**可验证性：** 是优化算法的固有性质。如果 $g'(z) = 0$，则 $\frac{\partial L}{\partial W}$ 中包含 $g'(z)$ 的项为零。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---


## 从公理到技术的推导链

> 展示如何**仅从上述公理出发**，一步步逻辑推导出完整的技术方案。
> 每一步必须标注"用了哪个公理"，不允许跳步或引入未声明的假设。

### Step 1: {公理 1} → 线性网络无论多深都等价于单层

**推理：** 由公理 1（结合律），$W_n \cdots W_2 W_1 x = W' x$。增加线性层不增加表达能力。

**结果：** 纯线性网络只能表示线性函数——直线/超平面。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.1

### Step 2: {公理 2} → 引入非线性使每层不可约

**推理：** 由公理 2，$g(W_2 g(W_1 x)) \neq g(W' x)$。插入非线性后，每层做的变换不能被单层替代。

**结果：** 深度变得有意义——N 层非线性网络的表达能力远超单层。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.1

### Step 3: {公理 3} → 非线性网络可以逼近任意函数

**推理：** 由 UAT（公理 3），一层足够宽的非线性网络可以逼近任意连续函数。多层网络在实践中更高效地做到这一点。

**结果：** 激活函数赋予了神经网络理论上无限的表达能力。

> 📖 Paper: Cybenko, 1989

### Step 4: {公理 4} → 反向传播可以计算梯度

**推理：** 由链式法则（公理 4），可以逐层计算 $\frac{\partial L}{\partial W_i} = \frac{\partial L}{\partial a_n} \cdot g'(z_n) \cdot \cdots \cdot g'(z_i) \cdot \frac{\partial z_i}{\partial W_i}$。

**结果：** 存在有效算法训练非线性网络——反向传播。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.5

### Step 5: {公理 5 + Step 4} → 激活函数必须有"好"的梯度

**推理：** 由公理 5，梯度为零时学习停止。由 Step 4，总梯度是各层 $g'(z_i)$ 的乘积。如果某层 $g'(z_i) \approx 0$（如 Sigmoid 饱和），总梯度 → 0，底层权重停止更新。

**结果：** 好的激活函数必须满足：在大部分输入区域，梯度不为零且不过小。这就是 **ReLU 优于 Sigmoid 的第一性原理解释**。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3

### 推导链全景图

```
公理 1 (结合律) ───┐
                   ├──→ 推论 A: 纯线性网络 = 单层 ──┐
公理 2 (非线性打破) ┘                                │
                                                     ├──→ 推论 C: 需要梯度好的激活函数
公理 3 (UAT) ──→ 推论 B: 非线性网络可逼近任意函数 ──┤     (= ReLU > Sigmoid)
                                                     │          │
公理 4 (链式法则) ──→ 推论 D: 反向传播可计算梯度 ───┤          ▼
                                                     │   完整技术: 激活函数设计原则
公理 5 (需非零梯度) ─────────────────────────────────┘   1. 必须非线性
                                                         2. 梯度不能消失
                                                         3. 计算要高效
```

---


## 如果公理不成立？

> 逐个"拔掉"公理，分析技术会如何崩塌。这揭示了技术的**真正边界**。

### 公理 1 失效：矩阵乘法不满足结合律

**如果不成立：** 在标准实数矩阵运算中，结合律永远成立。但如果使用非标准数值系统（如有限精度浮点数的极端舍入），近似的结合律可能不严格成立。

**技术后果：** 如果结合律不成立，那么即使没有激活函数，多层线性网络也不会退化为单层——激活函数的必要性减弱。

**替代方案：** 不适用。结合律是数学公理，在实数域永远成立。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

### 公理 3 失效：UAT 不成立

**如果不成立：** 如果目标函数不连续、定义域不紧致、或激活函数是常数/纯线性。

**技术后果：** 网络无法保证逼近目标函数。即使训练到收敛，也可能存在不可消除的逼近误差。

**替代方案：** 对于不连续函数，可以用分段拟合、决策树等非参数方法。实际上 ReLU 虽不满足 UAT 的原始"有界"条件，但 Leshno et al. (1993) 证明了更宽松的条件下 ReLU 也满足 UAT。

> 📖 Paper: Cybenko, 1989; Leshno et al., 1993

### 公理 5 失效：梯度为零但不在最优点

**如果不成立：** 这正是 Sigmoid 和 ReLU 面临的实际情况——Sigmoid 饱和区梯度 ≈ 0，ReLU 负区间梯度 = 0。

**技术后果：** Sigmoid → 梯度消失，深层网络无法训练；ReLU → 死神经元，部分网络容量浪费。

**替代方案：** Leaky ReLU（全域非零梯度）、GELU/Swish（负区间梯度小但非零）、BatchNorm（缓解饱和）、ResNet 残差连接（梯度直通）。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3, Ch.8

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
| 公理 1 结合律 | 矩阵乘法 $(AB)C = A(BC)$ | 实数域永远成立 | 多层线性 ≠ 单层（激活函数不再必要） |
| 公理 2 非线性打破 | $g(W_2 g(W_1 x)) \neq g(W'x)$ | $g$ 非仿射 | 每层不可约，深度有意义 |
| 公理 3 UAT | 一层+非线性 ≈ 任意函数 | 激活连续非常数、域紧致 | 网络表达力受限 |
| 公理 4 链式法则 | $\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}$ | 函数可微 | 无法反向传播 |
| 公理 5 需非零梯度 | $\nabla L = 0$ → 学习停止 | 优化器固有性质 | Sigmoid 梯度消失、ReLU 死神经元 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
