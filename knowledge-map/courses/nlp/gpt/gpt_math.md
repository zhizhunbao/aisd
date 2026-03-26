---
topic: gpt
dimension: math
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Radford et al., 'Improving Language Understanding by Generative Pre-Training', OpenAI 2018 — https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》, Ch.10-12 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# GPT 数学基础

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), OpenAI 2018
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $x_i$ | 序列中第 $i$ 个 token | i-th token | 词表中的一个词 |
| $n$ | 序列总长度 | Sequence length | 1 到上下文窗口大小 |
| $V$ | 词表大小 | Vocabulary size | GPT-2: ~50,257 |
| $d_{model}$ | 模型隐藏维度 | Model/hidden dimension | GPT-1: 768; GPT-3: 12,288 |
| $d_k$ | 每个注意力头的维度 | Key/Query dimension | $d_{model} / h$ |
| $h$ | 注意力头数量 | Number of attention heads | GPT-1: 12; GPT-3: 96 |
| $L$ | Transformer 层数 | Number of layers | GPT-1: 12; GPT-3: 96 |
| $Q, K, V$ | 注意力的查询/键/值矩阵 | Query, Key, Value | $\in \mathbb{R}^{n \times d_k}$ |
| $T$ | 温度参数 | Temperature | $(0, +\infty)$, 常用 0.1~2.0 |
| $k$ | Top-k 采样的 k 值 | Top-k parameter | 正整数, 常用 50 |
| $p$ | Top-p 采样的累积概率阈值 | Top-p / Nucleus parameter | $(0, 1]$, 常用 0.9 |
| $\theta$ | 模型所有可学习参数 | Model parameters | — |
| $\mathcal{L}$ | 损失函数 | Loss function | $\geq 0$ |

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3

---

## 核心公式

### 公式 1: 自回归语言模型目标函数

**直觉：** 给定前面所有的词，预测下一个词的概率——把所有位置的预测概率乘起来就是整个句子的概率。训练就是让这个概率尽可能大。

$$
\mathcal{L}(\theta) = - \sum_{i=1}^{n} \log P(x_i \mid x_1, x_2, \ldots, x_{i-1}; \theta)
$$

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), Eq. 1

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $x_i$ | 第 $i$ 个 token | "cat" |
| $x_1, \ldots, x_{i-1}$ | 前面所有 token | "The" |
| $\theta$ | 模型参数 | GPT 的所有权重 |
| $P(x_i \mid \cdot)$ | 给定前文，预测第 $i$ 个词的概率 | $P(\text{cat} \mid \text{The})$ |

**推导过程：**

1. 由链式法则 (chain rule of probability):
   $P(x_1, x_2, \ldots, x_n) = P(x_1) \cdot P(x_2 \mid x_1) \cdot P(x_3 \mid x_1, x_2) \cdots P(x_n \mid x_1, \ldots, x_{n-1})$

2. 取对数（方便计算，避免下溢）:
   $\log P(x_1, \ldots, x_n) = \sum_{i=1}^{n} \log P(x_i \mid x_1, \ldots, x_{i-1})$

3. 取负号（因为我们最小化损失）:
   $\mathcal{L} = - \sum_{i=1}^{n} \log P(x_i \mid x_1, \ldots, x_{i-1}; \theta)$

4. 这就是**负对数似然 (Negative Log-Likelihood, NLL)** 损失

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10 §10.3
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.12 §12.2.3

---

### 公式 2: 缩放点积注意力 (Scaled Dot-Product Attention)

**直觉：** 对于每个词（Query），去查找和它最相关的其他词（Key），然后把相关词的信息（Value）按相关程度加权求和。"缩放"是因为点积值随维度增大会变大，除以 $\sqrt{d_k}$ 防止 softmax 饱和。

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right) V
$$

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Eq. 1

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $Q$ | 查询矩阵 | 当前正在生成的词要"问"什么 |
| $K$ | 键矩阵 | 每个已有的词"提供"什么标签 |
| $V$ | 值矩阵 | 每个已有的词实际包含的信息 |
| $d_k$ | Key 的维度 | $d_{model} / h$ |
| $M$ | 因果掩码矩阵 | 上三角为 $-\infty$，下三角为 0 |

**推导过程：**

1. 计算注意力分数: $S = QK^T$ → 每个 Query 和所有 Key 的相似度，$S \in \mathbb{R}^{n \times n}$
2. 缩放: $S' = S / \sqrt{d_k}$ → 防止维度大时点积值过大导致 softmax 梯度消失
3. 加掩码: $S'' = S' + M$ → 因果掩码把未来位置设为 $-\infty$
4. 归一化: $A = \text{softmax}(S'')$ → 每行变成概率分布（和为 1）
5. 加权求和: $\text{Output} = AV$ → 用注意力权重聚合 Value

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.1

---

### 公式 3: 多头注意力 (Multi-Head Attention)

**直觉：** 一个注意力头只能关注一种"关系"（比如语法关系）。多个头并行运行，每个头学不同的关系（语法、语义、位置等），最后把它们的结果拼起来。

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W^O
$$

$$
\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)
$$

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Eq. 2-3

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $W_i^Q, W_i^K, W_i^V$ | 第 $i$ 个头的投影矩阵 | $\in \mathbb{R}^{d_{model} \times d_k}$ |
| $W^O$ | 输出投影矩阵 | $\in \mathbb{R}^{h \cdot d_k \times d_{model}}$ |
| $h$ | 头的数量 | GPT-1: 12; GPT-3: 96 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.2

---

### 公式 4: 温度采样 (Temperature Sampling)

**直觉：** 生成文本时，温度参数就像调节"创造力"的旋钮。温度低→保守安全，温度高→冒险创新。

$$
P(x_i = w) = \frac{\exp(z_w / T)}{\sum_{j=1}^{|V|} \exp(z_j / T)}
$$

> 📖 Paper: Ackley et al., "A Learning Algorithm for Boltzmann Machines", Cognitive Science, 1985

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $z_w$ | 模型对词 $w$ 的原始输出分数 (logit) | 未归一化的预测值 |
| $T$ | 温度 | $T=0.7$ 保守; $T=1.5$ 创意 |
| $\|V\|$ | 词表大小 | ~50,257 |

**推导过程：**

1. $T \rightarrow 0$: $z_w / T \rightarrow \pm\infty$，softmax 变成 argmax → 贪心解码
2. $T = 1$: 标准 softmax → 原始分布
3. $T \rightarrow \infty$: $z_w / T \rightarrow 0$，所有词概率趋于均匀 → 完全随机

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10

---

### 公式 5: 困惑度 (Perplexity)

**直觉：** 困惑度衡量模型对测试文本的"困惑程度"。困惑度越低，说明模型越好地预测了下一个词。直觉上，困惑度 $k$ 意味着模型在每一步平均犹豫于 $k$ 个等概率的选项。

$$
\text{PPL} = \exp\left(- \frac{1}{n} \sum_{i=1}^{n} \log P(x_i \mid x_1, \ldots, x_{i-1})\right)
$$

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10, Eq. 10.13

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $n$ | 测试文本中的 token 数 | 整个测试集的长度 |
| $P(x_i \mid \cdot)$ | 模型预测的条件概率 | 每一步的预测分布 |

**推导过程：**

1. 从负对数似然出发: $\text{NLL} = - \frac{1}{n} \sum_{i=1}^{n} \log P(x_i \mid x_1, \ldots, x_{i-1})$
2. 取指数: $\text{PPL} = \exp(\text{NLL})$
3. 等价于几何平均概率的倒数: $\text{PPL} = \left(\prod_{i=1}^{n} P(x_i \mid x_1, \ldots, x_{i-1})\right)^{-1/n}$

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10 §10.3

---

## 公式关系图

    链式法则 (概率论)
         │
         ▼
    自回归目标函数 (公式 1)  ──────────→  困惑度 (公式 5)
         │                              (= exp(平均NLL))
         │ 模型内部如何算 P(x_i|...)
         ▼
    缩放点积注意力 (公式 2)  ──→  多头注意力 (公式 3)
    + 因果掩码 M                   │
                                  ▼
                           Transformer Decoder Block
                                  │
                                  ▼ (推理时)
                           温度采样 (公式 4)
                           + Top-k / Top-p

---

## 手算练习

### 练习 1: 自回归损失计算

**题目：** 模型对句子 "I love NLP" 的预测概率如下：
- $P(\text{love} \mid \text{I}) = 0.3$
- $P(\text{NLP} \mid \text{I love}) = 0.1$

计算该句子的自回归损失和困惑度（忽略第一个词 "I" 的预测）。

**解答步骤：**

1. 代入公式 1 (NLL):
   $\mathcal{L} = -[\log(0.3) + \log(0.1)]$
   $= -[-1.204 + (-2.303)]$
   $= -(-3.507) = 3.507$

2. 平均 NLL:
   $\text{avg NLL} = 3.507 / 2 = 1.754$

3. 代入公式 5 (困惑度):
   $\text{PPL} = \exp(1.754) = 5.78$

4. **解读：** 模型在这两步上平均犹豫于约 5.78 个等概率选项。

### 练习 2: 温度对概率分布的影响

**题目：** 模型输出 logits 为 $z = [2.0, 1.0, 0.5]$ (三个候选词)。分别计算 $T=0.5$ 和 $T=2.0$ 时的概率分布。

**解答步骤：**

1. **$T = 0.5$ (低温):**
   - 缩放: $z/T = [4.0, 2.0, 1.0]$
   - $\exp$: $[54.60, 7.39, 2.72]$
   - 归一化: 总和 = 64.71
   - 概率: $[0.844, 0.114, 0.042]$ → 分布很尖锐，第一个词概率 84.4%

2. **$T = 2.0$ (高温):**
   - 缩放: $z/T = [1.0, 0.5, 0.25]$
   - $\exp$: $[2.72, 1.65, 1.28]$
   - 归一化: 总和 = 5.65
   - 概率: $[0.481, 0.292, 0.227]$ → 分布更平坦，三个词概率更接近

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 自回归损失 | $\mathcal{L} = -\sum_i \log P(x_i \mid x_{<i})$ | 训练目标 | 链式法则 |
| 缩放点积注意力 | $\text{softmax}(QK^T/\sqrt{d_k} + M) V$ | 计算上下文表示 | — |
| 多头注意力 | $\text{Concat}(\text{head}_1, \ldots, \text{head}_h) W^O$ | 学习多种关系 | 缩放点积注意力 |
| 温度采样 | $P(w) = \text{softmax}(z_w / T)$ | 控制生成多样性 | — |
| 困惑度 | $\text{PPL} = \exp(-\frac{1}{n}\sum_i \log P(x_i \mid x_{<i}))$ | 评估模型质量 | 自回归损失 |
| Top-k 采样 | 取概率最高的 $k$ 个词重新归一化 | 限制候选集 | — |
| Top-p 采样 | 取累积概率 $\geq p$ 的最小词集 | 动态候选集 | — |
