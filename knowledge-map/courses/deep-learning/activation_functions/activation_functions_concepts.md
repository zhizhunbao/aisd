---
topic: activation_functions
dimension: concepts
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 §6.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, 'PML1' Ch.13 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: Keras Activations — https://keras.io/api/layers/activations/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
expiry: 12m
status: current
---

# Activation Functions 核心概念

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

---


## 术语定义

### 激活函数 (Activation Function)

在神经网络的每个神经元中，线性变换 $z = Wx + b$ 之后施加的非线性函数 $g(z)$。它的作用是引入非线性，使得多层网络能够逼近任意复杂的函数，而不是退化为单层线性模型。激活函数是深度学习的"引擎"——没有它，再深的网络也只是在做矩阵乘法。

> 易混淆：**激活函数 vs 损失函数** — 激活函数作用于每个神经元的输出，引入非线性；损失函数作用于整个网络的最终预测，衡量预测与真实值的差距。两者在计算图中位置不同，目的不同。

### Sigmoid 函数 (Sigmoid / Logistic Function)

将任意实数映射到 $(0, 1)$ 区间的 S 形曲线函数：$\sigma(z) = \frac{1}{1 + e^{-z}}$。历史上是最早被广泛使用的激活函数之一，输出可以解释为概率。但在深层网络中因梯度消失问题逐渐被 ReLU 替代。目前主要用于二分类问题的输出层和 LSTM/GRU 的门控机制。

> 易混淆：**Sigmoid vs Softmax** — Sigmoid 处理单个值输出概率，用于二分类（或多标签分类中每个标签独立）；Softmax 处理向量输出概率分布，所有类别概率之和为 1，用于多分类。

### Tanh 函数 (Hyperbolic Tangent)

将任意实数映射到 $(-1, 1)$ 区间的函数：$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$。它是 Sigmoid 的缩放平移版本：$\tanh(z) = 2\sigma(2z) - 1$。输出零中心化（zero-centered），使得下一层的输入均值接近 0，有助于梯度更新的稳定性。但仍然存在饱和区间的梯度消失问题。

> 易混淆：**Tanh vs Sigmoid** — Tanh 输出范围 $(-1,1)$ 且零中心化，梯度更强；Sigmoid 输出范围 $(0,1)$ 且非零中心化。Tanh 的梯度最大值为 1（在 $z=0$），Sigmoid 的梯度最大值仅为 0.25。

### ReLU (Rectified Linear Unit)

当前深度学习最广泛使用的激活函数：$\text{ReLU}(z) = \max(0, z)$。正区间保持线性，负区间输出 0。计算极其高效（只需比较和赋值），且正区间梯度恒为 1，不会饱和，有效缓解了梯度消失问题。缺点是"死神经元"问题——一旦输入持续为负，该神经元永远不再被激活。

> 易混淆：**ReLU vs Leaky ReLU** — ReLU 在负区间梯度为 0（死神经元风险）；Leaky ReLU 在负区间给一个小斜率 $\alpha$（通常 0.01），保持梯度流通，避免死神经元。

### Leaky ReLU (Leaky Rectified Linear Unit)

ReLU 的改进版本，在负区间保留一个小的线性分量：$\text{LeakyReLU}(z) = \max(\alpha z, z)$，其中 $\alpha$ 是一个小正数（通常 0.01 或 0.2）。这样负区间也有非零梯度，避免了死神经元问题。当 $\alpha$ 是可学习参数时称为 PReLU（Parametric ReLU）。

> 易混淆：**Leaky ReLU vs PReLU vs ELU** — Leaky ReLU 的 $\alpha$ 是固定超参数；PReLU 的 $\alpha$ 是可学习参数；ELU 在负区间用指数函数 $\alpha(e^z - 1)$ 而非线性，输出均值更接近零。

### Softmax 函数 (Softmax Function)

将 $K$ 维实数向量转换为概率分布的函数：$\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$。输出的每个分量都在 $(0,1)$，且所有分量之和为 1。几乎exclusively用于多分类问题的输出层，与交叉熵损失配合使用。

> 易混淆：**Softmax vs Sigmoid** — 见 Sigmoid 条目。核心区别：Softmax 的输出是互斥的（和为 1），适合"从 K 个类中选 1 个"；Sigmoid 的输出是独立的，适合"每个标签独立判断是/否"。

### ELU (Exponential Linear Unit)

在负区间使用指数函数代替 Leaky ReLU 的线性部分：$\text{ELU}(z) = z \text{ if } z > 0$，$\text{ELU}(z) = \alpha(e^z - 1) \text{ if } z \le 0$。输出均值更接近零（自归一化性质），且负区间提供噪声鲁棒性。缺点是包含指数计算，比 ReLU 慢。

### Swish / SiLU (Sigmoid Linear Unit)

由 Google Brain 团队通过自动搜索发现的激活函数：$\text{Swish}(z) = z \cdot \sigma(z)$，其中 $\sigma$ 是 Sigmoid 函数。它是光滑的、非单调的（在负区间有一个小的负峰），在某些深度网络中表现优于 ReLU。PyTorch 中称为 SiLU。

### GELU (Gaussian Error Linear Unit)

基于高斯分布累积分布函数的激活函数：$\text{GELU}(z) = z \cdot \Phi(z)$，其中 $\Phi(z)$ 是标准正态分布的 CDF。GELU 是 Transformer 架构（BERT, GPT 等）中的默认激活函数。它可以看作是对输入进行"概率性"的保留或丢弃。

### Identity / Linear (恒等函数)

$f(z) = z$，即不施加任何非线性变换。仅用于回归任务的输出层，使网络能输出任意实数值。在隐藏层中使用 Identity 会使网络退化为线性模型，失去深度学习的意义。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.13
> 📖 Docs: [Keras Activations](https://keras.io/api/layers/activations/)

---


## 概念辨析

### Sigmoid vs Tanh vs ReLU（隐藏层激活函数三大流派）

| 维度 | Sigmoid | Tanh | ReLU |
|------|---------|------|------|
| **输出范围** | $(0, 1)$ | $(-1, 1)$ | $[0, +\infty)$ |
| **零中心化** | ❌ 否 | ✅ 是 | ❌ 否 |
| **梯度最大值** | 0.25 | 1.0 | 1.0 |
| **梯度消失** | ⚠️ 严重（两端饱和） | ⚠️ 中等（两端饱和） | ✅ 正区间无饱和 |
| **计算成本** | 高（指数运算） | 高（指数运算） | 低（比较+赋值） |
| **死神经元** | ❌ 不存在 | ❌ 不存在 | ⚠️ 存在 |
| **主要用途** | 输出层（二分类）、门控 | 隐藏层（RNN）、隐藏层 | 隐藏层（CNN/MLP 默认） |
| **年代** | 1980s-2000s 主流 | 1990s-2000s 主流 | 2010s-至今 主流 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3

### ReLU 家族对比（ReLU vs Leaky ReLU vs ELU vs Swish vs GELU）

| 维度 | ReLU | Leaky ReLU | ELU | Swish/SiLU | GELU |
|------|------|------------|-----|------------|------|
| **负区间行为** | 输出 0 | 线性 $\alpha z$ | 指数 $\alpha(e^z-1)$ | 非单调小负峰 | 概率性保留 |
| **光滑性** | ❌ 不光滑（z=0） | ❌ 不光滑 | ✅ 光滑（z=0） | ✅ 光滑 | ✅ 光滑 |
| **死神经元** | ⚠️ 有 | ✅ 无 | ✅ 无 | ✅ 无 | ✅ 无 |
| **计算成本** | 最低 | 低 | 中（含 exp） | 中（含 sigmoid） | 中（含 erf/近似） |
| **典型应用** | CNN/MLP 默认 | GAN, 深层 CNN | 自归一化网络 | EfficientNet | Transformer (BERT/GPT) |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.13
> 📖 Docs: [PyTorch Activations](https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity)

### 隐藏层激活 vs 输出层激活

| 维度 | 隐藏层激活 | 输出层激活 |
|------|-----------|-----------|
| **目的** | 引入非线性，提取特征 | 将输出映射到任务所需的范围 |
| **选择依据** | 梯度流通性、计算效率 | 任务类型（分类/回归） |
| **常用函数** | ReLU, Leaky ReLU, GELU | Sigmoid, Softmax, Linear |
| **可以不用吗？** | ❌ 不行，会退化为线性 | ✅ 可以（Linear = 不加激活） |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────┐
│              Activation Functions 体系                │
├──────────────────────────────────────────────────────┤
│  饱和型 (Saturating)                                  │
│  ├─ Sigmoid        σ(z) = 1/(1+e^(-z))              │
│  ├─ Tanh           tanh(z) = (e^z-e^(-z))/(e^z+e^(-z)) │
│  └─ Softmax        Softmax(z_i) = e^(z_i)/Σe^(z_j) │
├──────────────────────────────────────────────────────┤
│  非饱和型 (Non-Saturating)                            │
│  ├─ ReLU           max(0, z)                         │
│  ├─ Leaky ReLU     max(αz, z)                        │
│  ├─ PReLU          max(α_learned·z, z)               │
│  └─ ELU            z if z>0; α(e^z-1) if z≤0        │
├──────────────────────────────────────────────────────┤
│  自动搜索/设计型 (Searched/Designed)                   │
│  ├─ Swish/SiLU     z · σ(z)                          │
│  ├─ GELU           z · Φ(z)                          │
│  └─ Mish           z · tanh(softplus(z))             │
├──────────────────────────────────────────────────────┤
│  特殊用途                                             │
│  ├─ Identity       z (回归输出层)                     │
│  └─ Softplus       ln(1+e^z) (ReLU的光滑近似)        │
└──────────────────────────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3

### 适用场景 ✅

- **ReLU**：CNN 和 MLP 隐藏层的默认选择，计算高效
- **Sigmoid**：二分类输出层、LSTM/GRU 门控单元
- **Softmax**：多分类输出层（互斥类别）
- **Tanh**：RNN 隐藏层、需要零中心化输出的场景
- **GELU**：Transformer 架构（BERT、GPT）
- **Leaky ReLU**：GAN 的判别器、深层网络防死神经元
- **Identity**：回归任务输出层

### 不适用场景 ❌

- **Sigmoid/Tanh 用于深层网络隐藏层**：梯度消失导致深层权重几乎不更新
- **ReLU 用于输出层**：只能输出非负值，无法表示负数结果
- **Softmax 用于隐藏层**：会将特征压缩为概率分布，丢失信息
- **Identity 用于所有隐藏层**：网络退化为线性模型

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

---


## 速查表

| 函数 | 公式 | 输出范围 | 梯度 | 推荐场景 |
|------|------|---------|------|---------|
| Sigmoid | $\frac{1}{1+e^{-z}}$ | $(0,1)$ | $\sigma(1-\sigma)$ | 二分类输出层、门控 |
| Tanh | $\frac{e^z-e^{-z}}{e^z+e^{-z}}$ | $(-1,1)$ | $1-\tanh^2$ | RNN 隐藏层 |
| ReLU | $\max(0,z)$ | $[0,+\infty)$ | 0 或 1 | CNN/MLP 隐藏层（默认） |
| Leaky ReLU | $\max(\alpha z, z)$ | $(-\infty,+\infty)$ | $\alpha$ 或 1 | 深层网络、GAN |
| ELU | $z$ 或 $\alpha(e^z-1)$ | $(-\alpha,+\infty)$ | 1 或 $\alpha e^z$ | 自归一化网络 |
| Softmax | $\frac{e^{z_i}}{\sum e^{z_j}}$ | $(0,1)$, 和=1 | Jacobian 矩阵 | 多分类输出层 |
| Swish/SiLU | $z\cdot\sigma(z)$ | $\approx(-0.28,+\infty)$ | $\sigma(z)+z\sigma(z)(1-\sigma(z))$ | EfficientNet |
| GELU | $z\cdot\Phi(z)$ | $\approx(-0.17,+\infty)$ | $\Phi(z)+z\phi(z)$ | Transformer |
| Identity | $z$ | $(-\infty,+\infty)$ | 1 | 回归输出层 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3
> 📖 Docs: [Keras Activations](https://keras.io/api/layers/activations/)
