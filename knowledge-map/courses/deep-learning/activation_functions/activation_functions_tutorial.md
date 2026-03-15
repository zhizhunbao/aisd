---
topic: activation_functions
dimension: tutorial
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 §6.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Docs: Keras Activations — https://keras.io/api/layers/activations/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
expiry: 12m
status: current
---

# Activation Functions 教程

> **前置知识：** 线性代数基础 | 微积分链式法则 | 神经网络前向传播
> **参考来源：** [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | [Keras Activations](https://keras.io/api/layers/activations/) | [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---


## Section 0: 前置知识速查

1. **线性变换**：$z = Wx + b$，把输入 $x$ 经过权重矩阵和偏置，得到线性输出 $z$
2. **链式法则**：$\frac{\partial L}{\partial W} = \frac{\partial L}{\partial g} \cdot \frac{\partial g}{\partial z} \cdot \frac{\partial z}{\partial W}$，反向传播的数学基础
3. **前向传播**：输入 → 线性变换 → 激活函数 → 下一层，逐层串联
4. **梯度下降**：$W \leftarrow W - \eta \frac{\partial L}{\partial W}$，用梯度更新权重

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.5

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **线性退化**：没有激活函数，两层线性变换 $W_2(W_1 x) = (W_2 W_1) x = W'x$ 等价于一层。无论堆多少层，整个网络就是一个矩阵乘法，只能画直线/超平面，无法做 XOR 这样简单的非线性分类
- 🔥 **表达力为零**：Universal Approximation Theorem 要求至少一层非线性激活。没有它，网络无法逼近任意函数，深度学习毫无意义
- 🔥 **特征无法分层**：CNN 的"底层学边缘、中层学纹理、高层学物体"完全依赖非线性激活来引入层次化特征提取能力

### 它的核心价值

1. **引入非线性**：使多层网络能学习任意复杂的输入-输出映射关系
2. **使深度有意义**：每多加一层非线性，网络的表达能力指数级增长
3. **控制梯度流**：好的激活函数能让梯度在反向传播中既不消失也不爆炸
4. **任务适配**：输出层的激活函数将网络输出映射到任务所需的形式（概率、分类、实数值）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.1, §6.3
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5 §5.1

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 激活函数在网络中的位置

```
┌────────────────────────────────────────────────────────────────┐
│                    单个神经元的计算流程                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  输入 x ──→ 线性变换 z = Wx + b ──→ 激活函数 a = g(z) ──→ 输出│
│                                                                │
│  ┌─────────┐     ┌──────────────┐     ┌──────────────┐        │
│  │ x₁ x₂ x₃│ ──→ │ z = Σ(wᵢxᵢ)+b│ ──→ │ a = g(z)    │ ──→ a │
│  └─────────┘     └──────────────┘     └──────────────┘        │
│                   Pre-activation       Post-activation         │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                    多层网络的数据流                              │
│                                                                │
│  Input → [Dense + ReLU] → [Dense + ReLU] → [Dense + Softmax]  │
│           隐藏层 1          隐藏层 2          输出层            │
│           (特征提取)        (特征组合)       (任务输出)         │
└────────────────────────────────────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.1

### 2.2 为什么非线性是必要的？

**为什么用非线性函数而不是线性函数？**

数学证明极其简单：假设用 Identity（$g(z)=z$）作为激活函数：

- 第一层：$h_1 = W_1 x + b_1$
- 第二层：$h_2 = W_2 h_1 + b_2 = W_2(W_1 x + b_1) + b_2 = (W_2 W_1)x + (W_2 b_1 + b_2) = W'x + b'$

这就是一个单层线性模型！无论叠多少层，结果都等价于 $y = W'x + b'$，因为**矩阵乘法满足结合律**。

非线性激活函数打破了这个结合律，使得 $g(W_2 \cdot g(W_1 x)) \neq g(W' x)$，每一层才能做不同的变换。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.1

### 2.3 每种激活函数如何计算

**Sigmoid — 压缩到概率：**

输入任意实数 $z$，经过 $\sigma(z) = \frac{1}{1+e^{-z}}$ 输出 $(0,1)$：
- $z=+10$ → $\sigma \approx 0.9999$（"几乎确定是正类"）
- $z=0$ → $\sigma = 0.5$（"不确定"）
- $z=-10$ → $\sigma \approx 0.0001$（"几乎确定是负类"）

**Tanh — 零中心化压缩：**

$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$ 输出 $(-1,1)$：
- $z=+3$ → $\tanh \approx 0.995$
- $z=0$ → $\tanh = 0$（对称中心）
- $z=-3$ → $\tanh \approx -0.995$

零中心化意味着正负输入都有信号传递，梯度更新更对称。

**ReLU — 正通负断：**

$\text{ReLU}(z) = \max(0,z)$，计算只需要一次比较：
- $z=5.0$ → $\text{ReLU} = 5.0$（原样通过，梯度=1）
- $z=0$ → $\text{ReLU} = 0$
- $z=-5.0$ → $\text{ReLU} = 0$（完全截断，梯度=0）

**Softmax — 竞争性概率分配：**

给定 $K$ 个类别的原始分数 $[z_1, z_2, ..., z_K]$，先取指数再归一化：
- 分数最高的类获得最大概率
- 所有概率之和为 1
- 增大某类的分数会减小其他类的概率（零和竞争）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2, §6.3
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

### 2.4 激活函数如何影响反向传播

```
前向传播:   x ──→ z=Wx+b ──→ a=g(z) ──→ Loss

反向传播:   ∂L/∂W ←── ∂L/∂a · g'(z) ←── ∂L/∂Loss
                       ▲
                       │
            激活函数的梯度 g'(z) 是关键！

Sigmoid:  g'(z) = σ(1-σ)     最大 0.25  → 每层至少缩小 4 倍
Tanh:     g'(z) = 1-tanh²    最大 1.0   → 缩小但比 Sigmoid 好
ReLU:     g'(z) = 0 或 1     正区间恒 1  → 不缩小！
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3, §6.5

---


## Section 3: 局限性

1. **ReLU 死神经元**：如果一个神经元的输入 $z$ 始终为负（例如由于不当初始化或过大的学习率），其 ReLU 输出永远为 0，梯度永远为 0，该神经元"死了" → 使用 Leaky ReLU 或调整初始化/学习率
2. **Sigmoid/Tanh 梯度消失**：深层网络中，梯度经过多次相乘后趋近于 0，导致底层权重几乎不更新 → 使用 ReLU 系列或 BatchNorm
3. **Softmax 数值溢出**：$e^{z_i}$ 当 $z_i$ 很大时溢出 → 实践中减去 $\max(z)$ 后再计算
4. **没有"万能"激活函数**：不同任务和架构可能需要不同的激活函数。ReLU 虽然是隐藏层的默认选择，但在 Transformer 中 GELU 通常效果更好
5. **非光滑性**：ReLU 在 $z=0$ 不可微，理论上影响优化。实践中影响可忽略（次梯度方法有效），但追求光滑性可选 Swish/GELU

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.13

---


## Section 4: 方案对比

### 隐藏层激活函数选择

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **ReLU** | 计算最快，正区间无梯度消失 | 死神经元，非零中心化 | CNN/MLP 默认选择 |
| **Leaky ReLU** | 无死神经元，计算快 | 需要调 α | GAN, 深层 CNN |
| **ELU** | 自归一化，负区间光滑 | 含 exp 运算 | 需要自归一化的网络 |
| **Tanh** | 零中心化，梯度更强 | 饱和区梯度消失 | RNN 隐藏层 |
| **Sigmoid** | 输出可解释为概率 | 梯度消失严重 | 仅用于门控机制 |
| **GELU** | 光滑，概率性保留 | 计算较 ReLU 慢 | Transformer (BERT/GPT) |
| **Swish/SiLU** | 光滑，非单调 | 计算成本中等 | EfficientNet 等 |

### 输出层激活函数选择

| 任务类型 | 推荐激活 | 配套损失函数 | 输出范围 |
|---------|---------|------------|---------|
| **二分类** | Sigmoid | Binary Cross-Entropy | $(0, 1)$ |
| **多分类** | Softmax | Categorical Cross-Entropy | $(0,1)$, 和=1 |
| **回归** | Identity (Linear) | MSE / MAE | $(-\infty, +\infty)$ |
| **多标签分类** | Sigmoid (per label) | Binary Cross-Entropy (per label) | $(0, 1)$ per label |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2, §6.3

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考 |
| [《PRML》Ch.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | Sigmoid/Softmax 公式 |
| [《PML1》Ch.13](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 激活函数对比 |
| [Keras Activations](https://keras.io/api/layers/activations/) | 📖 文档 | Section 4 API |
| [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html) | 📖 文档 | Section 4 参数说明 |
