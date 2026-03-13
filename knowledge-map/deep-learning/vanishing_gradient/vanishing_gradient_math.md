---
topic: vanishing_gradient
dimension: math
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Paper: [Hochreiter (1991)](https://www.bioinf.jku.at/publications/older/2304.pdf)"
  - "📖 Paper: [Hochreiter & Schmidhuber (1997)](https://www.bioinf.jku.at/publications/older/2604.pdf)"
  - "📖 Paper: [Pascanu et al. (2013)](https://arxiv.org/abs/1211.5063)"
expiry: 12m
status: current
---

# 梯度消失 (Vanishing Gradient) 数学基础

> 📖 Paper: Pascanu et al., "On the difficulty of training Recurrent Neural Networks" (2013)
> 📖 Paper: Hochreiter & Schmidhuber, "Long Short-Term Memory" (1997)

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $h_t$ | 第 t 步的隐藏状态 | Hidden state at time t | $\mathbb{R}^d$ |
| $x_t$ | 第 t 步的输入 | Input at time t | $\mathbb{R}^n$ |
| $W_h$ | 隐藏状态到隐藏状态的权重矩阵 | Hidden-to-hidden weights | $\mathbb{R}^{d \times d}$ |
| $W_e$ | 输入到隐藏状态的权重矩阵 | Input-to-hidden weights | $\mathbb{R}^{d \times n}$ |
| $b$ | 偏置向量 | Bias vector | $\mathbb{R}^d$ |
| $\sigma$ | Sigmoid 激活函数 | Sigmoid activation | $(0, 1)$ |
| $J$ | 总损失函数 | Total loss | $\mathbb{R}^+$ |
| $J_t$ | 第 t 步的损失 | Loss at time t | $\mathbb{R}^+$ |
| $T$ | 总时间步数 | Total timesteps | $\mathbb{N}^+$ |
| $\eta$ | 学习率 | Learning rate | $(0, 1)$ |
| $f_t$ | LSTM 遗忘门输出 | Forget gate output | $[0, 1]^d$ |
| $i_t$ | LSTM 输入门输出 | Input gate output | $[0, 1]^d$ |
| $o_t$ | LSTM 输出门输出 | Output gate output | $[0, 1]^d$ |
| $c_t$ | LSTM 细胞状态 | Cell state | $\mathbb{R}^d$ |
| $\tilde{c}_t$ | LSTM 候选细胞状态 | Candidate cell state | $[-1, 1]^d$ |

> 📖 Paper: Pascanu et al. (2013), Section 2
> 📖 Paper: Hochreiter & Schmidhuber (1997), Section 2

---


## 核心公式

### 公式 1: RNN 前向传播

**直觉：** 每一步的隐藏状态 = 上一步的记忆（通过 $W_h$）+ 新输入（通过 $W_e$），经过激活函数压缩

$$
h_t = \sigma(W_h \cdot h_{t-1} + W_e \cdot e_t + b)
$$

> 📖 Paper: Pascanu et al. (2013), Eq. 1

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $e_t$ | 第 t 步的词嵌入向量 | "students" → [0.3, -0.1, ...] |
| $\sigma$ | 非线性激活 | 通常为 tanh 或 sigmoid |

---

### 公式 2: BPTT 梯度链式法则（核心！）

**直觉：** 对远处时间步 k 计算梯度，需要把 $\frac{\partial h_T}{\partial h_k}$ 展开成一连串乘法——这就是消失的根源

$$
\frac{\partial J_T}{\partial W_h} = \sum_{t=1}^{T} \frac{\partial J_T}{\partial h_T} \cdot \left( \prod_{j=t+1}^{T} \frac{\partial h_j}{\partial h_{j-1}} \right) \cdot \frac{\partial h_t}{\partial W_h}
$$

> 📖 Paper: Pascanu et al. (2013), Eq. 5-6

**推导过程：**

$$
\text{Step 1: 总损失对 W_h 的梯度（链式法则）}
$$
$$
\frac{\partial J}{\partial W_h} = \sum_{t=1}^{T} \frac{\partial J_t}{\partial W_h}
$$
$$
\text{Step 2: 每步损失通过 h_T 回传}
$$
$$
\frac{\partial J_T}{\partial W_h} = \frac{\partial J_T}{\partial h_T} \cdot \frac{\partial h_T}{\partial W_h}
$$
$$
\text{Step 3: h_T 对 W_h 的全微分需展开所有中间 h}
$$
$$
\frac{\partial h_T}{\partial W_h} = \sum_{t=1}^{T} \frac{\partial h_T}{\partial h_t} \cdot \frac{\partial^+ h_t}{\partial W_h}
$$
$$
\text{Step 4: h_T 对 h_t 是一连串雅可比矩阵的连乘}
$$
$$
\frac{\partial h_T}{\partial h_t} = \prod_{j=t+1}^{T} \frac{\partial h_j}{\partial h_{j-1}}
$$

> 📖 Paper: Pascanu et al. (2013), Section 2

---

### 公式 3: 单步雅可比矩阵

**直觉：** 每一步的梯度传递 = 激活函数的导数 × 权重矩阵，两者都可能 < 1

$$
\frac{\partial h_j}{\partial h_{j-1}} = \text{diag}(\sigma'(z_j)) \cdot W_h
$$

其中 $z_j = W_h \cdot h_{j-1} + W_e \cdot e_j + b$

> 📖 Paper: Pascanu et al. (2013), Eq. 7

**关键观察：**
- $\sigma'_{\text{sigmoid}}(z) = \sigma(z)(1 - \sigma(z))$，最大值 = 0.25
- $\sigma'_{\text{tanh}}(z) = 1 - \tanh^2(z)$，最大值 = 1（仅在 z=0 时）
- 连乘 T-t 次后：$\left\|\prod_{j=t+1}^{T} \text{diag}(\sigma'(z_j)) \cdot W_h\right\| \leq (\gamma_{max})^{T-t}$

当 $\gamma_{max} < 1$ 时 → **梯度指数衰减**（消失）
当 $\gamma_{max} > 1$ 时 → **梯度指数增长**（爆炸）

> 📖 Paper: Hochreiter (1991), Diploma thesis — 首次证明此结论

---

### 公式 4: LSTM 前向传播（解决方案）

**直觉：** LSTM 把记忆更新从"乘法"改成"加法"，让梯度可以像坐高速公路一样畅通回传

$$
f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \quad \text{(遗忘门)}
$$
$$
i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \quad \text{(输入门)}
$$
$$
\tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c) \quad \text{(候选状态)}
$$
$$
c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t \quad \text{(★ 加法更新 ★)}
$$
$$
o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \quad \text{(输出门)}
$$
$$
h_t = o_t \odot \tanh(c_t) \quad \text{(隐藏状态)}
$$

> 📖 Paper: Hochreiter & Schmidhuber (1997), Section 2

---

### 公式 5: LSTM 细胞状态梯度（为什么不消失）

**直觉：** 细胞状态的梯度回传时，乘的是遗忘门的值（接近 1），而不是小于 1 的激活函数导数

$$
\frac{\partial c_T}{\partial c_t} = \prod_{j=t+1}^{T} f_j
$$

> 📖 Paper: Hochreiter & Schmidhuber (1997), Section 4

**关键对比：**

| | RNN 梯度连乘 | LSTM 细胞梯度连乘 |
|---|---|---|
| 连乘因子 | $\text{diag}(\sigma') \cdot W_h$ | $f_j$（遗忘门值）|
| 典型值 | $\leq 0.25 \times \|W_h\|$ → 经常 < 1 | 可以学到接近 1 → 梯度保持 |
| 控制方式 | 固定（由激活函数决定） | **可学习**（门是训练参数） |

---


## 公式关系图

```
公式 1 (RNN前向)
    │
    ├── 展开 T 步 ──→ 公式 2 (BPTT梯度链)
    │                    │
    │                    └── 每步分解 ──→ 公式 3 (雅可比矩阵)
    │                                       │
    │                                       └── γ_max < 1 ──→ 梯度消失！
    │
    └── 改进架构 ──→ 公式 4 (LSTM前向)
                        │
                        └── 加法更新 ──→ 公式 5 (LSTM梯度保持)
```

---


## 手算练习

### 练习 1: Sigmoid 梯度消失速度

**题目：** 假设 RNN 有 5 个时间步，所有 sigmoid 导数恰好在最大值 0.25，权重 $\|W_h\| = 1$。从第 5 步回传到第 1 步，梯度缩小了多少倍？

**解答步骤：**

1. 连乘因子 = $0.25 \times 1 = 0.25$（每步）
2. 回传 4 步 → $0.25^4 = 0.00390625$
3. 结果：梯度缩小约 **256 倍**！仅 5 步就几乎消失

> 📖 Paper: Hochreiter (1991) — 首次计算此类衰减率

### 练习 2: tanh 与 sigmoid 对比

**题目：** 同样 5 步 RNN，tanh 导数在 z=0 处最大值为 1，在 z=1 处约为 0.42。假设所有 z=1，$\|W_h\|=1$。梯度缩小多少倍？

**解答步骤：**

1. tanh'(1) = 1 - tanh²(1) ≈ 1 - 0.76² ≈ 1 - 0.58 ≈ 0.42
2. 连乘因子 = $0.42 \times 1 = 0.42$（每步）
3. 回传 4 步 → $0.42^4 ≈ 0.031$
4. 结果：梯度缩小约 **32 倍**。比 sigmoid 好但仍然严重

### 练习 3: LSTM 遗忘门梯度保持

**题目：** LSTM 5 步，遗忘门 $f_j = 0.95$（每步保留 95% 记忆）。细胞状态梯度缩小多少倍？

**解答步骤：**

1. $\frac{\partial c_5}{\partial c_1} = \prod_{j=2}^{5} f_j = 0.95^4$
2. $0.95^4 ≈ 0.8145$
3. 结果：梯度仅缩小约 **1.23 倍**！远好于 RNN 的 256 倍

> 📖 Paper: Hochreiter & Schmidhuber (1997) — LSTM 梯度保持机制

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| RNN 前向 | $h_t = \sigma(W_h h_{t-1} + W_e e_t + b)$ | 理解递归结构 | — |
| BPTT 梯度 | $\frac{\partial J}{\partial W_h} = \sum_t \prod_j \frac{\partial h_j}{\partial h_{j-1}}$ | 理解消失根因 | RNN 前向 |
| 单步雅可比 | $\frac{\partial h_j}{\partial h_{j-1}} = \text{diag}(\sigma') \cdot W_h$ | 分析消失速度 | BPTT 梯度 |
| LSTM 细胞更新 | $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$ | LSTM 核心机制 | — |
| LSTM 梯度保持 | $\frac{\partial c_T}{\partial c_t} = \prod f_j$ | 理解为什么不消失 | LSTM 细胞更新 |

> 📖 Paper: Pascanu et al. (2013) | Hochreiter & Schmidhuber (1997)
