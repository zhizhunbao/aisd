---
topic: transformer
dimension: math
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.9 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》, Ch.10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Transformer 数学基础

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $n$ | 输入序列长度（有多少个词） | Sequence length | 正整数，通常 ≤ 512 |
| $d_{model}$ | 模型隐藏维度（每个词的向量长多少） | Model dimension | 原始论文 = 512 |
| $h$ | 注意力头数（同时跑几次注意力） | Number of heads | 原始论文 = 8 |
| $d_k$ | 每个头的 Key/Query 维度 | Key dimension | $d_k = d_{model} / h$ = 64 |
| $d_v$ | 每个头的 Value 维度 | Value dimension | $d_v = d_{model} / h$ = 64 |
| $d_{ff}$ | FFN 隐藏层维度 | Feed-forward dimension | 原始论文 = 2048 |
| $Q$ | 查询矩阵（"我在找什么"） | Query matrix | $\mathbb{R}^{n \times d_k}$ |
| $K$ | 键矩阵（"我能提供什么"） | Key matrix | $\mathbb{R}^{n \times d_k}$ |
| $V$ | 值矩阵（"我的实际内容"） | Value matrix | $\mathbb{R}^{n \times d_v}$ |
| $W^Q, W^K, W^V$ | Q/K/V 的投影权重矩阵 | Projection matrices | $\mathbb{R}^{d_{model} \times d_k}$ |
| $W^O$ | 多头输出投影矩阵 | Output projection | $\mathbb{R}^{h \cdot d_v \times d_{model}}$ |
| $pos$ | 位置索引（第几个词） | Position index | 0, 1, 2, …, n-1 |
| $i$ | 维度索引 | Dimension index | 0, 1, …, d/2-1 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3

---

## 核心公式

### 公式 1: 缩放点积注意力 (Scaled Dot-Product Attention)

**直觉：** 对每个词，算它和所有词的"相关度分数"（Q·K 点积），缩放后用 softmax 变成概率，再加权求和 V。

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V
$$

> 📖 Paper: Vaswani et al., Eq. 1

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $Q$ | 查询矩阵，shape = (n, d_k) | 每个词想"找什么" |
| $K$ | 键矩阵，shape = (n, d_k) | 每个词能"提供什么标签" |
| $V$ | 值矩阵，shape = (n, d_v) | 每个词的"实际内容" |
| $\sqrt{d_k}$ | 缩放因子 | $\sqrt{64} = 8$ |

**推导过程：**

1. **算原始分数：** $S = QK^T$，shape = (n, n)。$S_{ij}$ = 第 i 个词和第 j 个词的相关度
2. **为什么要除以 $\sqrt{d_k}$：** 当 d_k 很大时，Q 和 K 的元素都是均值 0 方差 1 的随机变量，它们的点积的方差 = d_k。方差越大，softmax 输出越极端（几乎全是 0 和 1），梯度消失。除以 $\sqrt{d_k}$ 让方差回到 1
3. **softmax 归一化：** 对每一行做 softmax，把分数变成概率（和为 1）
4. **加权求和：** 用概率乘 V，得到融合了上下文的新表示

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.1

---

### 公式 2: 多头注意力 (Multi-Head Attention)

**直觉：** 一个头只能学一种"看法"，h 个头同时学 h 种"看法"，最后拼起来。

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W^O
$$

其中每个头：

$$
\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

> 📖 Paper: Vaswani et al., Eq. 2-3

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $W_i^Q$ | 第 i 个头的 Query 投影 | $\mathbb{R}^{512 \times 64}$ |
| $W_i^K$ | 第 i 个头的 Key 投影 | $\mathbb{R}^{512 \times 64}$ |
| $W_i^V$ | 第 i 个头的 Value 投影 | $\mathbb{R}^{512 \times 64}$ |
| $W^O$ | 输出投影 | $\mathbb{R}^{512 \times 512}$ |
| $h$ | 头数 | 8 |

**推导过程：**

1. 输入 x 的 shape = (n, 512)
2. 对每个头 i：$Q_i = xW_i^Q$，shape = (n, 64)；K_i 和 V_i 同理
3. 每个头跑一次缩放点积注意力：head_i = Attention(Q_i, K_i, V_i)，shape = (n, 64)
4. 拼接 8 个头：Concat = (n, 512)
5. 投影回原维度：MultiHead = Concat × W^O，shape = (n, 512)
6. **参数量**：每个头 3 个投影矩阵 × 512×64 = 98304；8 个头 = 786432；加上 W^O = 262144；总计注意力参数 ≈ 1M

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.2

---

### 公式 3: 位置编码 (Positional Encoding)

**直觉：** 给每个位置一个独特的"指纹"——不同频率的正弦波组合，类似傅里叶变换。

$$
PE_{(pos, 2i)} = \sin\!\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$

$$
PE_{(pos, 2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$

> 📖 Paper: Vaswani et al., Eq. 4-5 (§3.5)

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $pos$ | 词在序列中的位置 | 0, 1, 2, …, n-1 |
| $i$ | 编码向量的维度索引 | 0, 1, …, 255（d_model/2 - 1） |
| $d_{model}$ | 模型维度 | 512 |
| $10000$ | 基频常数 | 控制波长范围 |

**推导过程：**

1. 对位置 pos=3，维度 i=0：PE(3, 0) = sin(3/10000^0) = sin(3) ≈ 0.141
2. PE(3, 1) = cos(3/10000^0) = cos(3) ≈ -0.990
3. 低维度 i 小 → 波长短，变化快 → 捕捉近距离位置差异
4. 高维度 i 大 → 波长长，变化慢 → 捕捉远距离位置关系
5. **关键性质：** 任意固定偏移 k，PE(pos+k) 可以表示为 PE(pos) 的线性函数——模型能学会相对位置

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.5

---

### 公式 4: 前馈网络 (Position-wise FFN)

**直觉：** 两层全连接，中间加一个激活函数，对每个位置独立做特征变换。

$$
\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
$$

> 📖 Paper: Vaswani et al., Eq. 6 (§3.3)

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $W_1$ | 第一层线性变换 | $\mathbb{R}^{512 \times 2048}$（升维 4 倍） |
| $b_1$ | 第一层偏置 | $\mathbb{R}^{2048}$ |
| $W_2$ | 第二层线性变换 | $\mathbb{R}^{2048 \times 512}$（降回原维度） |
| $b_2$ | 第二层偏置 | $\mathbb{R}^{512}$ |
| $\max(0, \cdot)$ | ReLU 激活函数 | 引入非线性 |

**推导过程：**

1. 输入 x，shape = (n, 512)
2. 升维：$h = xW_1 + b_1$，shape = (n, 2048)
3. 激活：$h' = \text{ReLU}(h)$，shape = (n, 2048)
4. 降维：$\text{FFN}(x) = h'W_2 + b_2$，shape = (n, 512)
5. **参数量**：512×2048 + 2048 + 2048×512 + 512 ≈ 2.1M（每层）

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.3

---

## 公式关系图

```
位置编码 (Eq.4-5)        输入词嵌入
       │                    │
       └────── + ───────────┘
               │
               ▼
    ┌────────────────────┐
    │  缩放点积注意力      │◄── Q = xW^Q, K = xW^K, V = xW^V
    │  Eq.1: softmax(    │
    │    QK^T/√d_k) · V  │
    └─────────┬──────────┘
              │ × h 个头
              ▼
    ┌────────────────────┐
    │  多头注意力 Eq.2-3   │
    │  Concat(heads)W^O  │
    └─────────┬──────────┘
              │ + 残差 + LayerNorm
              ▼
    ┌────────────────────┐
    │  FFN Eq.6           │
    │  ReLU(xW₁+b₁)W₂+b₂│
    └─────────┬──────────┘
              │ + 残差 + LayerNorm
              ▼
         下一层 / 输出
```

---

## 手算练习

### 练习 1: 缩放点积注意力（3 个词，d_k=2）

**题目：** 给定 3 个词的 Q、K、V（d_k=d_v=2），手算注意力输出。

$$
Q = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{bmatrix}, \quad
K = \begin{bmatrix} 1 & 1 \\ 0 & 1 \\ 1 & 0 \end{bmatrix}, \quad
V = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}
$$

**解答步骤：**

1. **计算 $QK^T$：**

$$
QK^T = \begin{bmatrix} 1 & 0 & 1 \\ 1 & 1 & 0 \\ 2 & 1 & 1 \end{bmatrix}
$$

2. **除以 $\sqrt{d_k} = \sqrt{2} \approx 1.414$：**

$$
\frac{QK^T}{\sqrt{2}} \approx \begin{bmatrix} 0.707 & 0 & 0.707 \\ 0.707 & 0.707 & 0 \\ 1.414 & 0.707 & 0.707 \end{bmatrix}
$$

3. **每行 softmax（以第一行为例）：**

$e^{0.707} \approx 2.028$，$e^{0} = 1$，$e^{0.707} \approx 2.028$

归一化：$[2.028/(2.028+1+2.028), 1/5.056, 2.028/5.056] \approx [0.401, 0.198, 0.401]$

4. **乘 V（以第一行为例）：**

$0.401 \times [1,0] + 0.198 \times [0,1] + 0.401 \times [0,0] = [0.401, 0.198]$

第一个词的输出更多关注第一个词和第三个词的内容。

### 练习 2: 位置编码（pos=3, d=4）

**题目：** 计算 pos=3 在 d_model=4 时的位置编码向量。

**解答步骤：**

1. i=0: PE(3,0) = sin(3/10000^(0/4)) = sin(3/1) = sin(3) ≈ 0.141
2. i=0: PE(3,1) = cos(3/10000^(0/4)) = cos(3) ≈ -0.990
3. i=1: PE(3,2) = sin(3/10000^(2/4)) = sin(3/100) = sin(0.03) ≈ 0.030
4. i=1: PE(3,3) = cos(3/10000^(2/4)) = cos(0.03) ≈ 1.000
5. **PE(3) = [0.141, -0.990, 0.030, 1.000]**

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 缩放点积注意力 | $\text{softmax}(QK^T / \sqrt{d_k})V$ | 计算注意力加权表示 | — |
| 多头注意力 | $\text{Concat}(\text{head}_1..h)W^O$ | 多视角注意力融合 | 缩放点积注意力 |
| 位置编码 (sin) | $\sin(pos / 10000^{2i/d})$ | 偶数维位置信号 | — |
| 位置编码 (cos) | $\cos(pos / 10000^{2i/d})$ | 奇数维位置信号 | — |
| FFN | $\text{ReLU}(xW_1+b_1)W_2+b_2$ | 逐位置非线性变换 | — |
| 残差连接 | $\text{LayerNorm}(x + \text{SubLayer}(x))$ | 梯度直通 + 稳定训练 | 各子层 |
| 注意力复杂度 | $O(n^2 \cdot d)$ | 评估计算开销 | — |
