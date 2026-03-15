---
topic: transformer
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《SLP3》 Ch.9-10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.10,12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Transformer 核心概念

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9-10

---


## 术语定义

### 自注意力 (Self-Attention)

序列中每个位置对**同一序列**中所有其他位置计算注意力权重的机制。每个 token 生成 Query、Key、Value 三个向量，通过 Q 与所有 K 的点积计算"该 token 应该关注哪些其他 token"的权重，然后用这些权重对 V 加权求和。这允许模型在一步内捕获任意距离的依赖关系，而 RNN 需要逐步传递信息。

> 易混淆：**Self-Attention vs Cross-Attention** — Self-Attention 的 Q/K/V 来自同一个序列；Cross-Attention 的 Q 来自一个序列（如 Decoder），K/V 来自另一个序列（如 Encoder 输出）

### 缩放点积注意力 (Scaled Dot-Product Attention)

Transformer 使用的具体注意力计算方式：$\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$。计算 Q 和 K 的点积后除以 $\sqrt{d_k}$（Key 维度的平方根）进行缩放，再通过 softmax 归一化为概率分布，最后与 V 相乘。缩放是为了防止点积值过大导致 softmax 饱和（梯度消失）。

> 易混淆：**Scaled vs Unscaled Dot-Product** — 不缩放时，当 $d_k$ 较大，点积值的方差约为 $d_k$，会把 softmax 推到梯度极小的区域

### 多头注意力 (Multi-Head Attention)

将 Self-Attention 并行执行 $h$ 次（称为 $h$ 个"头"），每个头使用不同的线性投影（不同的 $W^Q, W^K, W^V$ 矩阵）。最后将所有头的输出拼接并通过一个线性层合并。这样不同的头可以关注序列的不同方面（如语法关系、语义关系、位置关系等），类似于 CNN 多个卷积核提取不同特征。

> 易混淆：**多头并行 vs 多层堆叠** — 多头是同一层内的并行计算（关注不同子空间）；多层是纵深堆叠（构建越来越抽象的表示）

### 位置编码 (Positional Encoding)

由于 Self-Attention 对输入位置是无序的（置换不变性），必须显式注入位置信息。原始 Transformer 使用固定的正弦/余弦函数生成位置向量，与词嵌入相加后输入模型。频率从低到高变化，使模型可以学习到相对位置关系。后来的模型（如 BERT）改用可学习的位置嵌入，RoPE 等方案支持外推到训练时未见的长度。

> 易混淆：**固定位置编码 vs 可学习位置嵌入 vs 旋转位置编码(RoPE)** — 原始 Transformer 用固定正弦波；BERT/GPT 用可学习嵌入；LLaMA/GPT-NeoX 用 RoPE 支持长度外推

### 编码器 (Encoder)

Transformer 的左半部分。由 $N$ 个相同的层堆叠而成（原始论文 $N=6$），每层包含：Multi-Head Self-Attention → Add & Norm → Feed-Forward Network → Add & Norm。Encoder 对整个输入序列**双向**编码（每个位置可以看到所有其他位置），输出上下文化的表示序列。

### 解码器 (Decoder)

Transformer 的右半部分。也由 $N$ 个层堆叠，每层包含三个子层：Masked Multi-Head Self-Attention → Add & Norm → Cross-Attention（attend 到 Encoder 输出）→ Add & Norm → Feed-Forward → Add & Norm。Decoder 使用**因果掩码（Causal Mask）**确保位置 $i$ 只能看到 $i$ 之前的位置，实现自回归生成。

> 易混淆：**Encoder-Decoder vs Encoder-only vs Decoder-only** — 原始 Transformer 是 Encoder-Decoder（翻译）；BERT 是 Encoder-only（理解任务）；GPT 是 Decoder-only（生成任务）

### 前馈网络 (Feed-Forward Network, FFN)

Transformer 每层中Self-Attention 之后的两层全连接网络：$\text{FFN}(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2$。中间层维度通常是模型维度的 4 倍（如 $d_{model}=512$，FFN 中间层 $d_{ff}=2048$）。FFN 对每个位置**独立**应用相同的变换，负责非线性特征变换和容量扩展。

> 易混淆：**FFN vs Attention** — Attention 处理 token 间交互（哪些 token 相关）；FFN 处理单个 token 的特征变换（学习模式匹配）。最近研究认为 FFN 是"知识存储"的关键

### 残差连接 (Residual Connection)

每个子层（Attention 或 FFN）的输出与输入相加：$\text{output} = \text{LayerNorm}(x + \text{Sublayer}(x))$。这使得梯度可以不经过子层直接回传到更早的层，缓解深层网络的梯度消失问题，同时允许模型学习"增量修正"而非"从零重建"。

### 层归一化 (Layer Normalization)

对同一样本的所有特征维度做归一化：$\text{LN}(x) = \frac{x - \mu}{\sigma} \cdot \gamma + \beta$，其中 $\mu, \sigma$ 是沿特征维度计算的均值和标准差。与 Batch Normalization 不同，Layer Norm 不依赖 batch 中其他样本，适合变长序列和小 batch 场景。

> 易混淆：**Layer Norm vs Batch Norm** — BN 沿 batch 维度归一化（依赖 batch 大小）；LN 沿特征维度归一化（与 batch 无关）。Transformer 用 LN 因为序列任务的 batch 大小常变化

### 注意力掩码 (Attention Mask)

在计算注意力权重前，将某些位置的分数设为 $-\infty$（softmax 后变为 0），阻止模型"看到"这些位置。两种常见掩码：(1) **Padding Mask**：屏蔽 padding token，避免对填充内容的无意义关注；(2) **Causal Mask**（又称 Look-Ahead Mask）：上三角矩阵，确保 Decoder 中位置 $i$ 只能 attend 到 $\leq i$ 的位置。

### Query / Key / Value (Q/K/V)

注意力机制的三个核心向量。**Query** 是"我在找什么"；**Key** 是"我有什么标签"；**Value** 是"我的实际内容"。类比信息检索：Q 是搜索查询，K 是文档标题（用于匹配），V 是文档正文（匹配后返回的内容）。每个输入 token 通过三个可学习的线性投影矩阵 $W^Q, W^K, W^V$ 分别生成 Q、K、V。

### 教师强制 (Teacher Forcing)

Decoder 训练时的技巧：不使用模型自己的预测结果作为下一步输入，而是直接使用**真实标签序列**（ground truth）。这加速了收敛但导致训练与推理的分布不一致（exposure bias）。推理时没有 ground truth，必须使用模型自己的输出做自回归生成。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 3
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9.1-9.7
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10.4, 12

---


## 概念辨析

### Self-Attention vs Cross-Attention vs Additive Attention

| 维度 | Self-Attention | Cross-Attention | Additive Attention (Bahdanau) |
|------|---------------|----------------|-------------------------------|
| **Q/K/V 来源** | 全部来自同一序列 | Q 来自 Decoder，K/V 来自 Encoder | Q 来自 Decoder hidden state |
| **计算方式** | 点积 + 缩放 | 点积 + 缩放 | 加性（MLP 计算得分）|
| **并行性** | 完全并行 | 完全并行 | 完全并行 |
| **用途** | 序列内部建模 | 跨序列对齐（翻译等） | 早期 Seq2Seq 注意力 |
| **典型模型** | Transformer 所有层 | Transformer Decoder 第二子层 | Bahdanau NMT |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 3.2

### Encoder-only vs Decoder-only vs Encoder-Decoder

| 维度 | Encoder-only | Decoder-only | Encoder-Decoder |
|------|-------------|-------------|----------------|
| **代表模型** | BERT, RoBERTa | GPT, LLaMA, PaLM | T5, BART, 原始 Transformer |
| **注意力方向** | 双向（看全文） | 单向/因果（只看左边） | Encoder 双向 + Decoder 因果 |
| **预训练任务** | Masked LM (填空) | Next Token Prediction | Span Corruption / 去噪 |
| **擅长任务** | 文本分类、NER、句子相似 | 文本生成、对话、代码 | 翻译、摘要、问答 |
| **推理方式** | 单次前向传播 | 自回归逐 token 生成 | Encoder 一次 + Decoder 自回归 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805)
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.10

### Transformer vs RNN vs CNN（序列建模）

| 维度 | Transformer | RNN/LSTM | CNN (for sequences) |
|------|------------|---------|-------------------|
| **长距离依赖** | $O(1)$ — 直接 attend | $O(n)$ — 逐步传递 | $O(\log n)$ — 多层叠加 |
| **并行度** | 完全并行 | 串行（顺序依赖） | 完全并行 |
| **计算复杂度** | $O(n^2 \cdot d)$ | $O(n \cdot d^2)$ | $O(k \cdot n \cdot d^2)$ |
| **位置信息** | 需要显式位置编码 | 隐式（顺序处理）| 局部窗口隐含 |
| **内存需求** | 高（$n^2$ 注意力矩阵）| 低 | 中 |
| **适合场景** | 中短序列 + 充足算力 | 在线/流式场景 | 需要局部模式 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Table 1
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10

---


## 核心属性

### 信息架构

```
┌────────────────────────────────────────────────────────────────────┐
│                     Transformer 架构                               │
├────────────────────────────────────────────────────────────────────┤
│  输入层                                                            │
│  ├─ Input Embedding (词嵌入)                                       │
│  └─ Positional Encoding (位置编码，与嵌入相加)                      │
├────────────────────────────────────────────────────────────────────┤
│  Encoder (×N 层)                                                   │
│  ├─ Multi-Head Self-Attention                                      │
│  │   └─ h 个 Scaled Dot-Product Attention 头 → Concat → Linear    │
│  ├─ Add & Layer Norm (残差 + 归一化)                                │
│  ├─ Position-wise Feed-Forward Network (FFN)                       │
│  └─ Add & Layer Norm                                               │
├────────────────────────────────────────────────────────────────────┤
│  Decoder (×N 层)                                                   │
│  ├─ Masked Multi-Head Self-Attention (因果掩码)                    │
│  ├─ Add & Layer Norm                                               │
│  ├─ Multi-Head Cross-Attention (Q=Decoder, K/V=Encoder)           │
│  ├─ Add & Layer Norm                                               │
│  ├─ Position-wise Feed-Forward Network                             │
│  └─ Add & Layer Norm                                               │
├────────────────────────────────────────────────────────────────────┤
│  输出层                                                            │
│  ├─ Linear (映射到词表大小)                                        │
│  └─ Softmax (生成下一个 token 的概率分布)                           │
└────────────────────────────────────────────────────────────────────┘
```

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Figure 1

### 适用场景 ✅

- **机器翻译**：原始 Transformer 的设计目标，En↔De/Fr 等语言对
- **文本生成**：GPT 系列自回归生成（对话、文章、代码）
- **文本理解**：BERT 系列双向编码（分类、NER、问答）
- **计算机视觉**：ViT 将图像分割为 patch 序列，用 Transformer 编码
- **语音识别**：Whisper 等语音模型基于 Encoder-Decoder Transformer
- **多模态任务**：CLIP（图文对齐）、DALL-E（文生图）等

### 不适用场景 ❌

- **超长序列（>100K token）**：标准 Self-Attention 的 $O(n^2)$ 复杂度导致显存爆炸 → 需要线性注意力/稀疏注意力
- **实时流式处理**：Encoder 需要看到完整输入才能编码 → 需要 streaming 改造
- **极低延迟推理**：自回归 Decoder 逐 token 生成速度慢 → 需要推测解码（Speculative Decoding）
- **极小数据/模型**：Transformer 在数据量小时不如 LSTM/CNN → 需要预训练+微调

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 6

---


## 速查表

| 项 | 说明 | 原始论文配置 |
|-----|------|-------------|
| $d_{model}$ | 模型隐藏维度 | 512 |
| $h$ | 注意力头数 | 8 |
| $d_k = d_v = d_{model}/h$ | 每头的维度 | 64 |
| $d_{ff}$ | FFN 中间层维度 | 2048 |
| $N$ | Encoder/Decoder 层数 | 6 |
| 位置编码 | 正弦/余弦固定编码 | $PE_{pos,2i} = \sin(pos/10000^{2i/d})$ |
| 优化器 | Adam | $\beta_1=0.9, \beta_2=0.98, \epsilon=10^{-9}$ |
| 学习率 | Warmup + 衰减 | $lr = d_{model}^{-0.5} \cdot \min(step^{-0.5}, step \cdot warmup^{-1.5})$ |
| Warmup 步数 | 线性预热 | 4000 |
| Dropout | 残差/注意力/嵌入 | 0.1 |
| Label Smoothing | 标签平滑 | $\epsilon_{ls} = 0.1$ |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Table 3, Section 5
