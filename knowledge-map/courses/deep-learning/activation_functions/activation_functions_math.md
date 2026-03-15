---
topic: activation_functions
dimension: math
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 §6.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, 'PML1' Ch.13 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
expiry: 12m
status: current
---

# Activation Functions 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5 §5.1

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $z$ | 神经元的线性输出（激活前的值） | pre-activation / logit | $(-\infty, +\infty)$ |
| $g(z)$ | 激活函数 | activation function | 依函数而定 |
| $\sigma(z)$ | Sigmoid 函数 | sigmoid function | $(0, 1)$ |
| $e$ | 自然常数 | Euler's number | $\approx 2.71828$ |
| $\alpha$ | Leaky ReLU/ELU 的负区间斜率 | leaky coefficient | 通常 $0.01$ 或 $0.2$ |
| $W$ | 权重矩阵 | weight matrix | $\mathbb{R}^{m \times n}$ |
| $b$ | 偏置向量 | bias vector | $\mathbb{R}^{m}$ |
| $x$ | 层输入 | input | $\mathbb{R}^{n}$ |
| $\Phi(z)$ | 标准正态分布的累积分布函数 | standard normal CDF | $(0, 1)$ |
| $\phi(z)$ | 标准正态分布的概率密度函数 | standard normal PDF | $[0, 0.3989]$ |
| $K$ | Softmax 的类别数 | number of classes | $\mathbb{Z}^+$ |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---


## 核心公式

### 公式 1: Sigmoid 函数

**直觉：** 把任意实数"压缩"到 0~1 之间，像一个光滑的开关——输入越大越接近"开"(1)，输入越小越接近"关"(0)。

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 4.59

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $z$ | 线性输出 $Wx + b$ | 如 $z = 2.0$ |

**推导 Sigmoid 的梯度（反向传播需要）：**

$$
\text{Step 1: 令 } \sigma = \frac{1}{1 + e^{-z}} = (1 + e^{-z})^{-1}
$$
$$
\text{Step 2: } \frac{d\sigma}{dz} = -(1 + e^{-z})^{-2} \cdot (-e^{-z})
$$
$$
\text{Step 3: } = \frac{e^{-z}}{(1 + e^{-z})^2}
$$
$$
\text{Step 4: } = \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}}
$$
$$
\text{Step 5: } = \sigma(z) \cdot \frac{1 + e^{-z} - 1}{1 + e^{-z}}
$$
$$
\text{Step 6: } = \sigma(z) \cdot (1 - \sigma(z))
$$

**结论：** $\sigma'(z) = \sigma(z)(1 - \sigma(z))$

**梯度消失分析：** 当 $\sigma(z)$ 接近 0 或 1 时，$\sigma'(z) \to 0$。$\sigma'(z)$ 的最大值在 $z=0$ 处，为 $0.25$。这意味着每经过一层，梯度至少缩小为原来的 $\frac{1}{4}$。经过 $n$ 层后，梯度约为 $0.25^n$，这就是梯度消失的数学根源。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3

---

### 公式 2: Tanh 函数

**直觉：** 和 Sigmoid 类似的"压缩"函数，但输出以 0 为中心对称（-1 到 1），使得正负输入都有意义。

$$
\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5

**与 Sigmoid 的关系：**

$$
\tanh(z) = 2\sigma(2z) - 1
$$

**推导 Tanh 的梯度：**

$$
\text{Step 1: 令 } t = \tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}
$$
$$
\text{Step 2: } \frac{dt}{dz} = \frac{(e^z + e^{-z})(e^z + e^{-z}) - (e^z - e^{-z})(e^z - e^{-z})}{(e^z + e^{-z})^2}
$$
$$
\text{Step 3: } = \frac{(e^z + e^{-z})^2 - (e^z - e^{-z})^2}{(e^z + e^{-z})^2}
$$
$$
\text{Step 4: } = 1 - \left(\frac{e^z - e^{-z}}{e^z + e^{-z}}\right)^2
$$
$$
\text{Step 5: } = 1 - \tanh^2(z)
$$

**结论：** $\tanh'(z) = 1 - \tanh^2(z)$

**对比 Sigmoid：** $\tanh'(0) = 1$（vs Sigmoid 的 0.25），梯度最大值是 Sigmoid 的 4 倍，这是 Tanh 收敛更快的数学原因。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

### 公式 3: ReLU 函数

**直觉：** 最简单的非线性——正数原样通过，负数一律为零。像一个"只允许正信号通过"的阀门。

$$
\text{ReLU}(z) = \max(0, z) = \begin{cases} z & \text{if } z > 0 \\ 0 & \text{if } z \leq 0 \end{cases}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3.1, Eq. 6.37

**ReLU 的梯度：**

$$
\text{ReLU}'(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z < 0 \\ \text{undefined} & \text{if } z = 0 \end{cases}
$$

**注：** 在 $z=0$ 处不可微。实践中，框架通常将 $z=0$ 的梯度设为 0 或 1（次梯度方法），对训练无显著影响。

**为什么 ReLU 解决了梯度消失：** 在 $z > 0$ 区域，梯度恒为 1。无论经过多少层，只要激活值为正，梯度不会衰减。这是 ReLU 成为深度网络默认选择的数学原因。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3.1

---

### 公式 4: Leaky ReLU 函数

**直觉：** ReLU 的改良版——负区间不完全关闭，留一条"细缝"让梯度流过，防止神经元"死掉"。

$$
\text{LeakyReLU}(z) = \max(\alpha z, z) = \begin{cases} z & \text{if } z > 0 \\ \alpha z & \text{if } z \leq 0 \end{cases}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3.1

**Leaky ReLU 的梯度：**

$$
\text{LeakyReLU}'(z) = \begin{cases} 1 & \text{if } z > 0 \\ \alpha & \text{if } z \leq 0 \end{cases}
$$

**关键优势：** 全域梯度非零（最小为 $\alpha$），完全消除死神经元问题。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

### 公式 5: Softmax 函数

**直觉：** 把一组任意实数变成"概率分布"——每个值变成 0~1 之间的概率，且所有概率加起来等于 1。

$$
\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}, \quad i = 1, 2, \ldots, K
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 4.62
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $z_i$ | 第 $i$ 个类别的 logit（原始分数） | 如 $z = [2.0, 1.0, 0.1]$ |
| $K$ | 类别总数 | 如 $K = 3$ |

**Softmax 的梯度（Jacobian 矩阵）：**

$$
\text{Step 1: 当 } i = j: \quad \frac{\partial \text{Softmax}(z_i)}{\partial z_j} = \text{Softmax}(z_i)(1 - \text{Softmax}(z_j))
$$
$$
\text{Step 2: 当 } i \neq j: \quad \frac{\partial \text{Softmax}(z_i)}{\partial z_j} = -\text{Softmax}(z_i) \cdot \text{Softmax}(z_j)
$$

**数值稳定性技巧：** 直接计算 $e^{z_i}$ 可能溢出。实践中先减去最大值：

$$
\text{Softmax}(z_i) = \frac{e^{z_i - \max(z)}}{\sum_{j} e^{z_j - \max(z)}}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.4 §4.1

---

### 公式 6: Swish / SiLU 函数

**直觉：** 用输入自身乘以它的 Sigmoid 值——输入越正，保留越多；输入为负但不太大时，允许少量负值通过（非单调性）。

$$
\text{Swish}(z) = z \cdot \sigma(z) = \frac{z}{1 + e^{-z}}
$$

> 📖 Paper: Ramachandran et al., "Searching for Activation Functions", arXiv 2017

**Swish 的梯度：**

$$
\text{Step 1: } \text{Swish}'(z) = \sigma(z) + z \cdot \sigma'(z)
$$
$$
\text{Step 2: } = \sigma(z) + z \cdot \sigma(z)(1 - \sigma(z))
$$
$$
\text{Step 3: } = \sigma(z) \left[1 + z(1 - \sigma(z))\right]
$$

> 📖 Paper: Ramachandran et al., arXiv 2017

---

### 公式 7: GELU 函数

**直觉：** 根据输入值的大小，"概率性地"决定保留多少——值越大越可能全部通过，值越小（越负）越可能被"关掉"。

$$
\text{GELU}(z) = z \cdot \Phi(z)
$$

其中 $\Phi(z) = \frac{1}{2}\left[1 + \text{erf}\left(\frac{z}{\sqrt{2}}\right)\right]$ 是标准正态分布的 CDF。

> 📖 Paper: Hendrycks & Gimpel, "Gaussian Error Linear Units (GELUs)", arXiv 2016

**近似公式（实际使用）：**

$$
\text{GELU}(z) \approx 0.5z\left[1 + \tanh\left(\sqrt{\frac{2}{\pi}}(z + 0.044715z^3)\right)\right]
$$

**GELU 的梯度：**

$$
\text{GELU}'(z) = \Phi(z) + z \cdot \phi(z)
$$

其中 $\phi(z) = \frac{1}{\sqrt{2\pi}}e^{-z^2/2}$ 是标准正态 PDF。

> 📖 Paper: Hendrycks & Gimpel, arXiv 2016

---


## 公式关系图

```
              饱和型                                    非饱和型
┌─────────────────────────────┐     ┌──────────────────────────────────┐
│                             │     │                                  │
│  Sigmoid σ(z)               │     │  ReLU max(0,z)                   │
│      │                      │     │      │                           │
│      ├── 梯度: σ(1-σ)       │     │      ├── Leaky ReLU max(αz,z)   │
│      │                      │     │      │                           │
│      ▼                      │     │      ├── ELU α(e^z-1)           │
│  Tanh = 2σ(2z)-1            │     │      │                           │
│      │                      │     │      └── Softplus ln(1+e^z)     │
│      └── 梯度: 1-tanh²      │     │          (ReLU的光滑近似)        │
│                             │     │                                  │
│  Softmax (向量版 Sigmoid)    │     │  Swish = z·σ(z)                 │
│                             │     │      (= ReLU + Sigmoid 混合)     │
└─────────────────────────────┘     │                                  │
                                    │  GELU = z·Φ(z)                   │
                                    │      (= ReLU + 高斯概率 混合)     │
                                    └──────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---


## 手算练习

### 练习 1: Sigmoid 前向 + 反向

**题目：** 给定 $z = 2.0$，计算 $\sigma(z)$ 和 $\sigma'(z)$。

**解答步骤：**

1. 前向：$\sigma(2.0) = \frac{1}{1 + e^{-2.0}} = \frac{1}{1 + 0.1353} = \frac{1}{1.1353} = 0.8808$
2. 梯度：$\sigma'(2.0) = 0.8808 \times (1 - 0.8808) = 0.8808 \times 0.1192 = 0.1050$
3. 验证：梯度远小于 1（仅 0.105），说明即使在不太极端的位置，梯度也已明显衰减

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

### 练习 2: ReLU 和 Leaky ReLU 对比

**题目：** 给定 $z = -3.0$，$\alpha = 0.01$，分别计算 ReLU 和 Leaky ReLU 的输出和梯度。

**解答步骤：**

1. ReLU: $\text{ReLU}(-3.0) = \max(0, -3.0) = 0$，$\text{ReLU}'(-3.0) = 0$（梯度为零→死神经元）
2. Leaky ReLU: $\text{LeakyReLU}(-3.0) = \max(0.01 \times (-3.0), -3.0) = \max(-0.03, -3.0) = -0.03$
3. Leaky ReLU 梯度: $\text{LeakyReLU}'(-3.0) = 0.01$（梯度虽小但非零→神经元仍在学习）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

### 练习 3: Softmax 计算

**题目：** 给定 logits $z = [2.0, 1.0, 0.1]$，计算 Softmax 输出。

**解答步骤：**

1. 计算指数：$e^{2.0} = 7.389$，$e^{1.0} = 2.718$，$e^{0.1} = 1.105$
2. 求和：$\sum = 7.389 + 2.718 + 1.105 = 11.212$
3. 归一化：
   - $P(y=1) = 7.389 / 11.212 = 0.659$
   - $P(y=2) = 2.718 / 11.212 = 0.242$
   - $P(y=3) = 1.105 / 11.212 = 0.099$
4. 验证：$0.659 + 0.242 + 0.099 = 1.000$ ✅

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4

### 练习 4: Tanh 前向 + 梯度

**题目：** 给定 $z = 1.0$，计算 $\tanh(z)$ 和 $\tanh'(z)$。

**解答步骤：**

1. 前向：$\tanh(1.0) = \frac{e^1 - e^{-1}}{e^1 + e^{-1}} = \frac{2.718 - 0.368}{2.718 + 0.368} = \frac{2.350}{3.086} = 0.762$
2. 梯度：$\tanh'(1.0) = 1 - 0.762^2 = 1 - 0.580 = 0.420$
3. 对比 Sigmoid：$\sigma(1.0) = 0.731$，$\sigma'(1.0) = 0.197$。同样 $z=1$，Tanh 的梯度（0.42）是 Sigmoid 的（0.197）的 2 倍以上

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---


## 公式速查表

| 名称 | 公式 | 梯度 | 前置公式 |
|------|------|------|---------|
| Sigmoid | $\sigma(z) = \frac{1}{1+e^{-z}}$ | $\sigma(1-\sigma)$ | 无 |
| Tanh | $\tanh(z) = \frac{e^z-e^{-z}}{e^z+e^{-z}}$ | $1-\tanh^2$ | Sigmoid（$\tanh = 2\sigma(2z)-1$） |
| ReLU | $\max(0, z)$ | 0 或 1 | 无 |
| Leaky ReLU | $\max(\alpha z, z)$ | $\alpha$ 或 1 | ReLU（$\alpha \to 0$ 退化为 ReLU） |
| ELU | $z$ 或 $\alpha(e^z-1)$ | 1 或 $\alpha e^z$ | ReLU |
| Softmax | $\frac{e^{z_i}}{\sum e^{z_j}}$ | $S_i(\delta_{ij} - S_j)$ | Sigmoid（K=2 时退化为 Sigmoid） |
| Swish | $z \cdot \sigma(z)$ | $\sigma + z\sigma(1-\sigma)$ | Sigmoid |
| GELU | $z \cdot \Phi(z)$ | $\Phi(z) + z\phi(z)$ | 正态 CDF/PDF |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5
