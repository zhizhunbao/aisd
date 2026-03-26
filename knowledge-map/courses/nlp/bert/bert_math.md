---
topic: bert
dimension: math
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: 12m
status: current
---

# BERT 数学基础

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), NAACL 2019
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------| 
| $L$ | Transformer 层数 | Number of Layers | 12 (Base), 24 (Large) |
| $H$ | 隐藏维度（每个 token 向量的长度） | Hidden Size | 768 (Base), 1024 (Large) |
| $A$ | 注意力头数 | Number of Attention Heads | 12 (Base), 16 (Large) |
| $d_k$ | 每个注意力头的维度 | Head Dimension | $H / A$ = 64 |
| $N$ | 输入序列长度（token 数） | Sequence Length | ≤ 512 |
| $V$ | 词表大小 | Vocabulary Size | ~30,000 |
| $Q, K, V$ | 查询/键/值矩阵 | Query / Key / Value | $\mathbb{R}^{N \times d_k}$ |
| $W^Q, W^K, W^V$ | 线性投影权重矩阵 | Projection Weight Matrices | $\mathbb{R}^{H \times d_k}$ |
| $W^O$ | 多头输出投影矩阵 | Output Projection Matrix | $\mathbb{R}^{H \times H}$ |
| $x_i$ | 第 $i$ 个 token 的输入表示 | Input Representation | $\mathbb{R}^{H}$ |
| $\hat{x}_i$ | MLM 中被 mask 的 token 的预测 | MLM Prediction | $\mathbb{R}^{V}$ |
| $\text{mask}$ | 被遮住的 token 位置集合 | Masked Token Positions | 约 15% 的 $N$ |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2

---

## 核心公式

### 公式 1: 输入表示 (Input Representation)

**直觉：** 每个 token 的向量 = "它是什么词" + "它属于哪个句子" + "它在哪个位置"，三个信息直接加起来。

$$
\mathbf{x}_i = \mathbf{e}_{\text{token}}(w_i) + \mathbf{e}_{\text{segment}}(s_i) + \mathbf{e}_{\text{position}}(i)
$$

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.2, Figure 2

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $\mathbf{e}_{\text{token}}(w_i)$ | 第 $i$ 个 token 的词嵌入 | 查 WordPiece 词表得到 768 维向量 |
| $\mathbf{e}_{\text{segment}}(s_i)$ | 句子段落嵌入（A 或 B） | 句子 A 的 token → $E_A$，句子 B → $E_B$ |
| $\mathbf{e}_{\text{position}}(i)$ | 位置嵌入（可学习） | 第 0 个位置 → $P_0$，第 1 个 → $P_1$，... |

**推导过程：**

1. 对输入文本做 WordPiece 分词，得到 token 序列 $[w_1, w_2, ..., w_N]$
2. 每个 token $w_i$ 查嵌入表得到 $\mathbf{e}_{\text{token}}(w_i) \in \mathbb{R}^H$
3. 根据 token 属于句子 A 还是 B，查段落嵌入表得到 $\mathbf{e}_{\text{segment}}(s_i) \in \mathbb{R}^H$
4. 根据 token 的位置索引 $i$，查位置嵌入表得到 $\mathbf{e}_{\text{position}}(i) \in \mathbb{R}^H$
5. 三者逐元素相加得到最终输入向量 $\mathbf{x}_i \in \mathbb{R}^H$

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.2

---

### 公式 2: 缩放点积注意力 (Scaled Dot-Product Attention)

**直觉：** 每个词问"我应该关注序列中的哪些词？"——用点积衡量相关性，除以 $\sqrt{d_k}$ 防止值太大导致 softmax 饱和。

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V
$$

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Eq. 1, §3.2.1

**参数解释：**

| 参数 | 含义 | 维度 |
|------|------|------|
| $Q$ | 查询矩阵（"我在找什么"） | $N \times d_k$ |
| $K$ | 键矩阵（"我能提供什么"） | $N \times d_k$ |
| $V$ | 值矩阵（"我的实际内容"） | $N \times d_k$ |
| $d_k$ | 每个注意力头的维度 | $H / A = 64$ |
| $QK^T$ | 注意力得分矩阵 | $N \times N$ |

**推导过程：**

1. 计算相似度：$S = QK^T$，维度 $N \times N$，$S_{ij}$ 表示 token $i$ 对 token $j$ 的关注程度
2. 缩放：$S' = S / \sqrt{d_k}$，除以 $\sqrt{64} = 8$，防止点积值过大
3. 归一化：$\alpha = \text{softmax}(S')$，每行归一化为概率分布（和为 1）
4. 加权求和：$\text{output} = \alpha V$，用注意力权重对 Value 加权

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.1

---

### 公式 3: 多头注意力 (Multi-Head Attention)

**直觉：** 一个注意力头只能学一种"关注模式"，多个头可以同时学习不同的关注模式（比如一个头关注语法关系，另一个关注语义相似度），然后拼接起来。

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_A) W^O
$$

其中每个头：

$$
\text{head}_i = \text{Attention}(X W_i^Q, X W_i^K, X W_i^V)
$$

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Eq. 2-3, §3.2.2

**参数解释：**

| 参数 | 含义 | 维度 |
|------|------|------|
| $W_i^Q, W_i^K, W_i^V$ | 第 $i$ 个头的投影矩阵 | $H \times d_k$ |
| $W^O$ | 输出投影矩阵 | $H \times H$ |
| $A$ | 头数 | 12 (Base) |
| 每个 head 输出 | 一种关注模式的结果 | $N \times d_k$ |
| Concat 后 | 所有头拼接 | $N \times (A \cdot d_k) = N \times H$ |

**推导过程：**

1. 对每个头 $i = 1, ..., A$：用 $W_i^Q, W_i^K, W_i^V$ 对输入 $X$ 做线性投影
2. 对每个头 $i$：计算缩放点积注意力，得到 $\text{head}_i \in \mathbb{R}^{N \times d_k}$
3. 拼接所有头：$\text{Concat}(\text{head}_1, ..., \text{head}_A) \in \mathbb{R}^{N \times H}$
4. 用 $W^O$ 做最终线性投影：输出 $\in \mathbb{R}^{N \times H}$

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.2

---

### 公式 4: MLM 损失函数 (Masked Language Model Loss)

**直觉：** 对于每个被 mask 的位置，模型输出一个概率分布（预测每个词的可能性），我们用交叉熵损失来衡量预测和真实词之间的差距，然后对所有被 mask 的位置求平均。

$$
\mathcal{L}_{\text{MLM}} = -\frac{1}{|\mathcal{M}|} \sum_{i \in \mathcal{M}} \log P(w_i | \mathbf{h}_i)
$$

其中：

$$
P(w_i | \mathbf{h}_i) = \text{softmax}(\mathbf{h}_i W_e^T + b)_{w_i}
$$

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.1

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $\mathcal{M}$ | 被 mask 的 token 位置集合 | 15% 的位置被选中 |
| $\mathbf{h}_i$ | 位置 $i$ 的最终隐藏状态 | 768 维向量 (BERT-Base) |
| $W_e$ | 词嵌入权重矩阵（共享） | $V \times H$ |
| $w_i$ | 位置 $i$ 的真实 token | 原来被 mask 前的词 |
| $P(w_i \| \mathbf{h}_i)$ | 模型预测的概率 | softmax 后的第 $w_i$ 个元素 |

**推导过程：**

1. BERT 编码器处理整个输入序列，得到每个位置的隐藏状态 $\mathbf{h}_i \in \mathbb{R}^H$
2. 对每个被 mask 的位置 $i \in \mathcal{M}$：
   - 计算 logits：$\mathbf{z}_i = \mathbf{h}_i W_e^T + b \in \mathbb{R}^V$
   - 计算概率分布：$P = \text{softmax}(\mathbf{z}_i)$
   - 取真实 token $w_i$ 对应的概率：$P(w_i | \mathbf{h}_i)$
3. 对所有被 mask 的位置求平均交叉熵：$\mathcal{L}_{\text{MLM}} = -\frac{1}{|\mathcal{M}|} \sum_{i \in \mathcal{M}} \log P(w_i | \mathbf{h}_i)$

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.1

---

### 公式 5: NSP 损失函数 (Next Sentence Prediction Loss)

**直觉：** 拿 [CLS] 的最终表示做一个二分类——判断句子 B 是不是句子 A 的真正下一句。

$$
\mathcal{L}_{\text{NSP}} = -[y \log P(\text{IsNext}) + (1 - y) \log (1 - P(\text{IsNext}))]
$$

其中：

$$
P(\text{IsNext}) = \sigma(\mathbf{h}_{\text{[CLS]}} W_{\text{NSP}} + b_{\text{NSP}})
$$

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.2

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $y$ | 真实标签 | 1 = IsNext, 0 = NotNext |
| $\mathbf{h}_{\text{[CLS]}}$ | [CLS] token 的最终隐藏状态 | 768 维 (Base) |
| $W_{\text{NSP}}$ | NSP 分类器权重 | $H \times 2$ |
| $\sigma$ | sigmoid 函数 | 输出 [0, 1] 的概率 |

### 公式 6: 总损失函数

**直觉：** 预训练时，MLM 和 NSP 两个任务的损失直接相加，同时优化。

$$
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{MLM}} + \mathcal{L}_{\text{NSP}}
$$

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3

---

## 公式关系图

    输入文本
        │
        ▼
    ┌───────────────────────────┐
    │ 公式 1: Input Representation│
    │ x = e_token + e_seg + e_pos│
    └───────────────────────────┘
        │
        ▼
    ┌───────────────────────────┐
    │ 公式 2: Scaled Dot-Product  │
    │ Attention(Q,K,V)           │
    └───────────────────────────┘
        │ (× A 个头)
        ▼
    ┌───────────────────────────┐
    │ 公式 3: Multi-Head Attention│
    │ Concat + W^O              │
    └───────────────────────────┘
        │ (× L 层)
        ▼
    ┌─────────────┬─────────────┐
    │ mask 位置    │ [CLS] 位置   │
    ▼             ▼             
    ┌──────────┐  ┌──────────┐  
    │ 公式 4:   │  │ 公式 5:   │  
    │ MLM Loss │  │ NSP Loss │  
    └──────────┘  └──────────┘  
        │             │
        ▼             ▼
    ┌───────────────────────────┐
    │ 公式 6: Total Loss         │
    │ L = L_MLM + L_NSP         │
    └───────────────────────────┘

---

## 手算练习

### 练习 1: 缩放点积注意力

**题目：** 假设序列长度 $N = 3$，头维度 $d_k = 2$。给出以下矩阵，计算 $\text{Attention}(Q, K, V)$：

$$
Q = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{bmatrix}, \quad
K = \begin{bmatrix} 1 & 1 \\ 0 & 1 \\ 1 & 0 \end{bmatrix}, \quad
V = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{bmatrix}
$$

**解答步骤：**

1. 计算 $QK^T$：

$$
QK^T = \begin{bmatrix} 1 & 0 & 1 \\ 1 & 1 & 0 \\ 2 & 1 & 1 \end{bmatrix}
$$

2. 缩放：$\sqrt{d_k} = \sqrt{2} \approx 1.414$

$$
\frac{QK^T}{\sqrt{d_k}} = \begin{bmatrix} 0.707 & 0 & 0.707 \\ 0.707 & 0.707 & 0 \\ 1.414 & 0.707 & 0.707 \end{bmatrix}
$$

3. Softmax（每行独立归一化）：

- 第 1 行：$\text{softmax}([0.707, 0, 0.707]) = [0.394, 0.213, 0.394]$
- 第 2 行：$\text{softmax}([0.707, 0.707, 0]) = [0.388, 0.388, 0.224]$
- 第 3 行：$\text{softmax}([1.414, 0.707, 0.707]) = [0.476, 0.262, 0.262]$

4. 加权求和 $\alpha V$：

- 第 1 行：$0.394 \times [1,0] + 0.213 \times [0,1] + 0.394 \times [1,1] = [0.788, 0.607]$
- 第 2 行：$0.388 \times [1,0] + 0.388 \times [0,1] + 0.224 \times [1,1] = [0.612, 0.612]$
- 第 3 行：$0.476 \times [1,0] + 0.262 \times [0,1] + 0.262 \times [1,1] = [0.738, 0.524]$

### 练习 2: MLM 损失计算

**题目：** 假设词表 $V = 4$（词: A, B, C, D），一个 token 被 mask，模型输出 logits $[2.0, 1.0, 0.5, 0.1]$，真实 token 是 A（索引 0）。计算 MLM 损失。

**解答步骤：**

1. Softmax：$\exp([2.0, 1.0, 0.5, 0.1]) = [7.389, 2.718, 1.649, 1.105]$
2. 总和：$7.389 + 2.718 + 1.649 + 1.105 = 12.861$
3. 概率分布：$P = [0.574, 0.211, 0.128, 0.086]$
4. 真实 token A 的概率：$P(A) = 0.574$
5. 损失：$\mathcal{L} = -\log(0.574) = 0.555$

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 输入表示 | $x_i = e_{\text{token}} + e_{\text{seg}} + e_{\text{pos}}$ | 构造 BERT 输入 | — |
| 缩放点积注意力 | $\text{softmax}(QK^T / \sqrt{d_k}) V$ | 计算 token 间关注度 | 输入表示 |
| 多头注意力 | $\text{Concat}(\text{head}_1, ..., \text{head}_A) W^O$ | 捕捉多种关注模式 | 缩放点积注意力 |
| MLM 损失 | $-\frac{1}{\|\mathcal{M}\|} \sum_{i \in \mathcal{M}} \log P(w_i \| \mathbf{h}_i)$ | 预训练目标 1 | 多头注意力 |
| NSP 损失 | $-[y \log P + (1-y) \log(1-P)]$ | 预训练目标 2 | 多头注意力 |
| 总损失 | $\mathcal{L}_{\text{MLM}} + \mathcal{L}_{\text{NSP}}$ | 预训练优化目标 | MLM + NSP |
