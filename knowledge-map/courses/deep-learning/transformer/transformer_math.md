---
topic: transformer
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《SLP3》 Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.10,12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Transformer 数学基础

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $n$ | 序列长度（输入有多少个 token） | sequence length | 正整数 |
| $d_{model}$ | 模型隐藏维度（每个 token 的向量长度） | model dimension | 原始论文 512 |
| $h$ | 注意力头数（并行计算多少组注意力） | number of heads | 原始论文 8 |
| $d_k$ | 每个头的 Key/Query 维度 | key dimension | $d_k = d_{model}/h = 64$ |
| $d_v$ | 每个头的 Value 维度 | value dimension | $d_v = d_{model}/h = 64$ |
| $d_{ff}$ | FFN 中间层维度 | feed-forward dimension | 原始论文 2048 |
| $Q$ | Query 矩阵（"我在找什么"）| query matrix | $\mathbb{R}^{n \times d_k}$ |
| $K$ | Key 矩阵（"我有什么标签"）| key matrix | $\mathbb{R}^{n \times d_k}$ |
| $V$ | Value 矩阵（"我的内容"）| value matrix | $\mathbb{R}^{n \times d_v}$ |
| $W^Q, W^K, W^V$ | Q/K/V 的线性投影权重矩阵 | projection weights | $\mathbb{R}^{d_{model} \times d_k}$ |
| $W^O$ | 多头输出的合并权重矩阵 | output projection | $\mathbb{R}^{hd_v \times d_{model}}$ |
| $X$ | 输入嵌入矩阵 | input embeddings | $\mathbb{R}^{n \times d_{model}}$ |
| $PE$ | 位置编码矩阵 | positional encoding | $\mathbb{R}^{n \times d_{model}}$ |
| $pos$ | token 在序列中的位置索引 | position index | $0, 1, ..., n-1$ |
| $i$ | 嵌入维度索引 | dimension index | $0, 1, ..., d_{model}/2 - 1$ |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 3

---


## 核心公式

### 公式 1: Scaled Dot-Product Attention

**直觉：** 计算"每个 token 应该关注哪些其他 token"的权重，然后用这些权重聚合信息——就像搜索引擎用查询匹配文档标题，再返回文档内容。

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V
$$

> 📖 Paper: Vaswani et al., Eq. 1 (Section 3.2.1)

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $QK^T$ | Q 和 K 的点积矩阵，度量相似度 | $n \times n$ 注意力分数矩阵 |
| $\sqrt{d_k}$ | 缩放因子，防止点积过大 | $\sqrt{64} = 8$ |
| $\text{softmax}(\cdot)$ | 行归一化为概率分布 | 每行和为 1 |

**推导过程：**

$$
\text{Step 1: 计算相似度矩阵 } S = QK^T \in \mathbb{R}^{n \times n}
$$
$$
\text{Step 2: 缩放 } S' = \frac{S}{\sqrt{d_k}} = \frac{QK^T}{\sqrt{d_k}}
$$
$$
\text{Step 3: softmax 归一化 } A = \text{softmax}(S') \text{（按行）}
$$
$$
\text{Step 4: 加权聚合 } \text{Output} = AV \in \mathbb{R}^{n \times d_v}
$$

**为什么要除以 $\sqrt{d_k}$？**

当 Q 和 K 的元素独立且均值为 0、方差为 1 时，点积 $q \cdot k = \sum_{j=1}^{d_k} q_j k_j$ 的方差为 $d_k$。如果 $d_k$ 很大（如 64），点积值会很大，softmax 输出接近 one-hot（梯度接近 0）。除以 $\sqrt{d_k}$ 使方差归一为 1，保持 softmax 输出在有意义的梯度区间。

> 📖 Paper: Vaswani et al., Section 3.2.1, 脚注 4

---

### 公式 2: Multi-Head Attention

**直觉：** 用多组不同的"眼睛"（头）从不同角度看同一个序列——一个头可能关注语法关系，另一个关注语义相似性，还有一个关注位置邻近性。

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h) W^O
$$

$$
\text{where } \text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

> 📖 Paper: Vaswani et al., Eq. 2-3 (Section 3.2.2)

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $W_i^Q \in \mathbb{R}^{d_{model} \times d_k}$ | 第 $i$ 个头的 Query 投影 | $512 \times 64$ |
| $W_i^K \in \mathbb{R}^{d_{model} \times d_k}$ | 第 $i$ 个头的 Key 投影 | $512 \times 64$ |
| $W_i^V \in \mathbb{R}^{d_{model} \times d_v}$ | 第 $i$ 个头的 Value 投影 | $512 \times 64$ |
| $W^O \in \mathbb{R}^{hd_v \times d_{model}}$ | 输出合并投影 | $512 \times 512$ |

**推导过程：**

$$
\text{Step 1: 对每个头 } i=1,...,h \text{，投影 Q/K/V}
$$
$$
Q_i = QW_i^Q, \quad K_i = KW_i^K, \quad V_i = VW_i^V
$$
$$
\text{Step 2: 每个头独立计算注意力}
$$
$$
\text{head}_i = \text{softmax}\left(\frac{Q_i K_i^T}{\sqrt{d_k}}\right) V_i \in \mathbb{R}^{n \times d_v}
$$
$$
\text{Step 3: 拼接所有头}
$$
$$
\text{Concat} = [\text{head}_1; \text{head}_2; ...; \text{head}_h] \in \mathbb{R}^{n \times hd_v}
$$
$$
\text{Step 4: 线性变换回 } d_{model}
$$
$$
\text{MultiHead} = \text{Concat} \cdot W^O \in \mathbb{R}^{n \times d_{model}}
$$

**参数量计算：** 多头注意力的参数量 = $h \times (3 \times d_{model} \times d_k) + hd_v \times d_{model} = 4 \times d_{model}^2$（当 $d_k = d_v = d_{model}/h$ 时，与单头注意力参数量相同）

> 📖 Paper: Vaswani et al., Section 3.2.2

---

### 公式 3: 位置编码 (Positional Encoding)

**直觉：** 给每个位置一个独一无二的"身份证号"——偶数维度用正弦波、奇数维度用余弦波，不同频率的组合使每个位置都有唯一的编码。

$$
PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$
$$
PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$

> 📖 Paper: Vaswani et al., Eq. 4 (Section 3.5)

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $pos$ | 序列中的位置（第几个 token）| 0, 1, 2, ..., n-1 |
| $i$ | 维度对的索引 | 0, 1, ..., $d_{model}/2 - 1$ |
| $10000^{2i/d_{model}}$ | 频率分母，随 $i$ 增大而增大 | $i=0$ 时频率最高，$i$ 大时频率低 |

**为什么选正弦/余弦？**

关键性质：$PE_{pos+k}$ 可以表示为 $PE_{pos}$ 的线性变换（通过旋转矩阵），使得模型能学习**相对位置**关系。这意味着任意固定偏移 $k$ 对应一个固定的线性变换，模型可以通过简单的线性运算推断 token 间的相对距离。

> 📖 Paper: Vaswani et al., Section 3.5

---

### 公式 4: Feed-Forward Network (FFN)

**直觉：** 两层全连接网络对每个位置的表示做非线性变换——第一层"扩展"到高维空间（2048维），第二层"压缩"回原始维度（512维），中间用 ReLU 激活引入非线性。

$$
\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
$$

> 📖 Paper: Vaswani et al., Eq. 5 (Section 3.3)

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $W_1 \in \mathbb{R}^{d_{model} \times d_{ff}}$ | 扩展层权重 | $512 \times 2048$ |
| $W_2 \in \mathbb{R}^{d_{ff} \times d_{model}}$ | 压缩层权重 | $2048 \times 512$ |
| $\max(0, \cdot)$ | ReLU 激活函数 | 负值置零 |

> 📖 Paper: Vaswani et al., Section 3.3

---

### 公式 5: 学习率调度 (Learning Rate Schedule)

**直觉：** 先热身再衰减——训练初始阶段线性增加学习率（避免早期大梯度导致不稳定），达到峰值后按步数的负半次幂衰减。

$$
lr = d_{model}^{-0.5} \cdot \min(step^{-0.5}, \; step \cdot warmup\_steps^{-1.5})
$$

> 📖 Paper: Vaswani et al., Eq. 6 (Section 5.3)

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $d_{model}^{-0.5}$ | 全局缩放因子，与模型维度关联 | $512^{-0.5} \approx 0.044$ |
| $warmup\_steps$ | 预热步数 | 4000 |
| $step^{-0.5}$ | 衰减阶段：学习率 ∝ $1/\sqrt{step}$ | step=10000 时约 0.01 |

> 📖 Paper: Vaswani et al., Section 5.3

---


## 公式关系图

```
Input Embedding ──────────────────────────────────────────────┐
       +                                                       │
Positional Encoding (公式 3) ──→ 带位置信息的输入              │
                                    │                          │
                                    ▼                          │
                     ┌──────────────────────────┐              │
                     │ Multi-Head Attention (公式 2)│           │
                     │  ├─ head_i = Attention()   │            │
                     │  │   └─ Scaled Dot-Product │            │
                     │  │     Attention (公式 1)   │            │
                     │  └─ Concat → W^O           │            │
                     └──────────────────────────┘              │
                                    │                          │
                        Add & LayerNorm (残差连接)             │
                                    │                          │
                                    ▼                          │
                     ┌──────────────────────────┐              │
                     │    FFN (公式 4)            │             │
                     │  ReLU(xW₁+b₁)W₂+b₂      │              │
                     └──────────────────────────┘              │
                                    │                          │
                        Add & LayerNorm                        │
                                    │                          │
                               重复 N 层                       │
                                    │                          │
                        Linear → Softmax → 输出                │
                                                               │
                     训练时使用: LR Schedule (公式 5) ──────────┘
```

---


## 手算练习

### 练习 1: 计算 Scaled Dot-Product Attention（3 个 token，$d_k=2$）

**题目：** 给定 3 个 token 的 Q、K、V 矩阵（$d_k = d_v = 2$）：

$Q = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{bmatrix}, \quad K = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0.5 & 0.5 \end{bmatrix}, \quad V = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0.5 & 0.5 \end{bmatrix}$

计算 $\text{Attention}(Q, K, V)$。

**解答步骤：**

1. 计算 $QK^T$：

$QK^T = \begin{bmatrix} 1 & 0 & 0.5 \\ 0 & 1 & 0.5 \\ 1 & 1 & 1 \end{bmatrix}$

2. 除以 $\sqrt{d_k} = \sqrt{2} \approx 1.414$：

$\frac{QK^T}{\sqrt{2}} = \begin{bmatrix} 0.707 & 0 & 0.354 \\ 0 & 0.707 & 0.354 \\ 0.707 & 0.707 & 0.707 \end{bmatrix}$

3. softmax（按行）：

行 1: $\text{softmax}([0.707, 0, 0.354]) \approx [0.42, 0.21, 0.30]$（需精确计算 $e^{0.707}/(e^{0.707}+e^0+e^{0.354})$）

行 2: $\text{softmax}([0, 0.707, 0.354]) \approx [0.21, 0.42, 0.30]$

行 3: $\text{softmax}([0.707, 0.707, 0.707]) = [0.333, 0.333, 0.333]$（三者相等）

4. 乘以 $V$：

$\text{Output} = A \cdot V$（注意力权重 × Value 矩阵）

**关键观察：** 第 3 个 token 的 Q 与所有 K 的点积相等（均为 0.707），因此它**均匀关注**所有 token——这说明相似的 Q 和 K 会得到更高的注意力分数。

> 📖 Paper: Vaswani et al., Section 3.2.1

### 练习 2: 计算参数量（Transformer-base 配置）

**题目：** 计算原始 Transformer-base（$d_{model}=512, h=8, d_{ff}=2048, N=6$，词表大小 $V=37000$）仅 Encoder 部分的参数量。

**解答步骤：**

1. 词嵌入层：$V \times d_{model} = 37000 \times 512 = 18,944,000$
2. 每层多头注意力：$4 \times d_{model}^2 = 4 \times 512^2 = 1,048,576$
3. 每层 FFN：$2 \times d_{model} \times d_{ff} = 2 \times 512 \times 2048 = 2,097,152$
4. 每层 LayerNorm（×2）：$2 \times 2 \times d_{model} = 2048$
5. 每层总计：$1,048,576 + 2,097,152 + 2,048 = 3,147,776$
6. Encoder 6 层：$6 \times 3,147,776 = 18,886,656$
7. 总计（含嵌入）：$18,944,000 + 18,886,656 \approx 37.8M$

> 📖 Paper: Vaswani et al., Table 3

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| Scaled Dot-Product Attention | $\text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$ | 注意力计算核心 | 无 |
| Multi-Head Attention | $\text{Concat}(\text{head}_1,...,\text{head}_h)W^O$ | 多角度并行注意力 | 公式 1 |
| 位置编码 | $\sin(pos/10000^{2i/d})$ / $\cos(pos/10000^{2i/d})$ | 注入位置信息 | 无 |
| FFN | $\max(0, xW_1+b_1)W_2+b_2$ | 逐位置非线性变换 | 无 |
| 学习率调度 | $d^{-0.5} \cdot \min(s^{-0.5}, s \cdot w^{-1.5})$ | Warmup + 衰减 | 无 |
| Self-Attention 复杂度 | $O(n^2 \cdot d)$ | 时间复杂度分析 | 公式 1 |
| 参数量（每层） | $4d_{model}^2 + 2d_{model}d_{ff}$ | 模型大小估算 | 公式 2, 4 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 3-5
