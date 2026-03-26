---
topic: neural_network
dimension: first_principles
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Paper: Hornik et al., 'Multilayer feedforward networks are universal approximators', Neural Networks 1989 — https://doi.org/10.1016/0893-6080(89)90020-8"
  - "📖 Paper: Cybenko, 'Approximation by superpositions of a sigmoidal function', 1989 — https://doi.org/10.1007/BF02551274"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
expiry: 12m
status: current
---

# Neural Network (神经网络) 第一性原理

> 📖 Paper: Hornik et al., [Universal Approximation Theorem](https://doi.org/10.1016/0893-6080(89)90020-8), 1989
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 核心问题链

> 用"5 个为什么"递归追问，从表层功能到不可再分公理。

1. **Neural Network 在做什么？** → 学习一个函数 $f: \mathbb{R}^n \rightarrow \mathbb{R}^k$ 来映射输入到输出
2. **为什么要用层叠的仿射变换 + 非线性？** → 因为任何足够复杂的函数都可以被这种结构逼近（万能近似定理 UAT）
3. **为什么 UAT 成立？** → 因为非线性激活函数允许网络用有限多个"阶梯函数"去逼近任意形状（Stone-Weierstrass 定理的推论）
4. **为什么梯度下降能找到好的参数？** → 因为损失函数关于参数是可微的（可微可组合性），链式法则保证梯度可以高效计算
5. **能否继续拆分？** → 不能 → 到达三个不可再分公理

---

## 公理与基本假设

### 公理 1: 可微函数的可组合性 (Composability of Differentiable Functions)

**陈述：** 如果 $f$ 和 $g$ 都是可微函数，则复合函数 $f \circ g$ 也是可微的，且其导数可由链式法则计算：$(f \circ g)' = f'(g(x)) \cdot g'(x)$。

**白话：** 把好几个"可以求导的"运算串起来，结果还是可以求导的，而且有一个简单公式（链式法则）算导数。

**来源：** 微积分基本定理（Leibniz / Newton, 17 世纪）

**可验证性：**
- ✅ 成立条件：所有组成函数在对应点可微
- ❌ 不成立条件：函数不可微（如 ReLU 在 $x=0$ 处不可微，但次梯度实践中可用）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

### 公理 2: 万能近似性 (Universal Approximation)

**陈述：** 对于任意连续函数 $f^*: [0,1]^n \rightarrow \mathbb{R}$ 和任意 $\epsilon > 0$，存在一个单隐藏层网络 $f(x) = \sum_{i=1}^{M} v_i \sigma(w_i^T x + b_i)$（其中 $\sigma$ 是非常量、有界、单调递增的连续函数），使得 $\sup_x |f(x) - f^*(x)| < \epsilon$。

**白话：** 只要神经元足够多，一层网络就能无限逼近任意连续函数。

**来源：** Cybenko (1989), Hornik et al. (1989)

**可验证性：**
- ✅ 成立条件：目标函数连续、定义在紧集上、激活函数满足条件
- ❌ 不成立条件：目标函数不连续（如方波）；实践中"足够宽"可能需要指数级神经元

> 📖 Paper: Hornik et al., [Universal Approximation Theorem](https://doi.org/10.1016/0893-6080(89)90020-8), 1989
> 📖 Paper: Cybenko, [Approximation by Superpositions of Sigmoidal Functions](https://doi.org/10.1007/BF02551274), 1989

### 公理 3: 数据的流形假设 (Manifold Hypothesis)

**陈述：** 真实世界的高维数据实际上集中在低维流形附近。

**白话：** 虽然一张 256×256 的图片有 65536 个像素（维度），但"有意义的图片"只占这个空间的极小一部分——它们分布在一个低维的"曲面"上。

**来源：** 经验观察 + 统计分析（Tenenbaum et al. 2000, Roweis & Saul 2000）

**可验证性：**
- ✅ 成立条件：自然数据（图像、语音、文本）——大量实证支持
- ❌ 不成立条件：随机噪声（没有内在低维结构）；高度离散的数据

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.5.11.3

### 公理 4: 经验风险最小化原则 (Empirical Risk Minimization, ERM)

**陈述：** 在有限训练数据上最小化经验损失 $\hat{\mathcal{L}} = \frac{1}{N}\sum_{i=1}^N \ell(f(x_i), y_i)$ 是逼近真实风险（在整个数据分布上的期望损失）的合理策略。

**白话：** 在训练数据上犯最少的错，通常在新数据上也不会犯太多错（只要数据够代表、模型不太复杂）。

**来源：** 统计学习理论 — Vapnik (1982)

**可验证性：**
- ✅ 成立条件：训练数据是 i.i.d. 从真实分布采样的；模型复杂度适当
- ❌ 不成立条件：数据有严重偏差 (distribution shift)；模型过拟合

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.5.2

---

## 从公理到技术的推导链

### Step 1: 从公理 3 出发 → 学习是可能的

**推理：** 因为数据集中在低维流形上（公理 3），所以一个足够灵活的函数只需要学习这个低维结构，而不是整个高维空间。这让"从有限样本学习"变得可行。

**结果：** 学习问题从"在无穷维空间找映射"简化为"在低维流形附近找映射"。

### Step 2: 从公理 2 出发 → 神经网络可以表达

**推理：** 因为万能近似定理（公理 2），单隐藏层网络可以逼近任意连续函数——包括从流形到标签的映射。所以神经网络有足够的表达能力。

**结果：** 存在一组参数 $\theta^*$ 使得网络 $f(x;\theta^*)$ 可以很好地逼近目标函数。

### Step 3: 从公理 1 出发 → 参数可以高效优化

**推理：** 因为可微函数的可组合性（公理 1），整个网络关于参数是可微的。链式法则给出了反向传播算法，使得梯度计算的复杂度只是前向传播的常数倍。

**结果：** 可以用梯度下降高效搜索最优参数。

### Step 4: 从公理 4 出发 → 训练目标是合理的

**推理：** 经验风险最小化（公理 4）保证了：在训练数据上最小化损失的参数，在测试数据上也有接近的表现（只要模型复杂度和数据量匹配）。

**结果：** 完整的神经网络学习管线——前向传播 → 损失计算 → 反向传播 → 参数更新——在理论上有充分的基础。

### 推导链全景图

```
公理 3 (数据在低维流形) ─────────┐
                                ├──→ 学习可行 ──→ 表达存在 ──→ 可优化 ──→ Neural Network
公理 2 (万能近似定理) ───────────┤
                                │
公理 1 (可微可组合 → 链式法则) ──┤
                                │
公理 4 (ERM → 训练在有限数据有效) ┘
```

---

## 如果公理不成立？

### 公理 1 失效：函数不可微

**如果不成立：** 网络使用了不可微的操作（如硬阈值激活、离散采样）
**技术后果：** 无法用反向传播计算梯度，标准 SGD 失效
**替代方案：** 直通估计器 (Straight-Through Estimator)、进化算法、REINFORCE 策略梯度

### 公理 2 失效：网络不够宽/深

**如果不成立：** 网络太小，表达能力不足以逼近目标函数
**技术后果：** 无论怎么训练都有不可消除的逼近误差（欠拟合）
**替代方案：** 增加网络容量（更宽或更深）、使用更适合的归纳偏置（CNN 对图像、Transformer 对序列）

### 公理 3 失效：数据没有低维结构

**如果不成立：** 数据实际上均匀分布在高维空间，没有内在的低维结构
**技术后果：** 维度灾难——需要指数级的训练数据才能学到有意义的映射
**替代方案：** 显式降维（PCA）、强归纳偏置、或者承认问题不适合神经网络

### 公理 4 失效：训练-测试分布不同

**如果不成立：** 训练数据和测试数据来自不同分布 (distribution shift / covariate shift)
**技术后果：** 训练损失低但测试损失高，模型在真实环境失效
**替代方案：** 领域自适应 (Domain Adaptation)、分布外泛化 (OOD Generalization)、不变风险最小化 (IRM)

---

## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
| 可微可组合性 | 串起来还能求导 | 所有层的运算可微 | 无法反向传播 |
| 万能近似 (UAT) | 一层足够宽就能逼近任意连续函数 | 函数连续、紧集、足够多神经元 | 欠拟合 |
| 流形假设 | 真实数据在低维曲面上 | 自然数据 (图像/语音/文本) | 维度灾难 |
| ERM 原则 | 训练集上犯最少错 ≈ 测试集上犯最少错 | i.i.d. 采样 + 模型适当 | 分布偏移下失效 |
