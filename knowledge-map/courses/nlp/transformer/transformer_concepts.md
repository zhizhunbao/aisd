---
topic: transformer
dimension: concepts
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.9-10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》, Ch.10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Bahdanau et al., 'Neural Machine Translation by Jointly Learning to Align and Translate', ICLR 2015 — https://arxiv.org/abs/1409.0473"
expiry: 12m
status: current
---

# Transformer 核心概念

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9-10

---

## 术语定义

### 自注意力 (Self-Attention)

自注意力是一种让序列中的每个位置"看到"同一序列中所有其他位置的机制。具体做法：对每个词生成三个向量——Query（我在找什么）、Key（我能提供什么）、Value（我的实际内容）。然后计算当前词的 Query 与所有词的 Key 的点积得到"注意力分数"，用 softmax 归一化后加权 Value，得到融合了全局上下文的新表示。

> 别名：**Intra-Attention**（来自早期论文）——因为注意力作用于序列自身内部（intra-），而不是两个不同序列之间（inter-）

> 易混淆：**Cross-Attention** — Self-Attention 是同一序列内部的注意力（Q/K/V 都来自同一序列），Cross-Attention 是两个不同序列之间的注意力（Q 来自一个序列，K/V 来自另一个序列，如 Decoder 关注 Encoder 输出）

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2

### 缩放点积注意力 (Scaled Dot-Product Attention)

Transformer 中实际使用的注意力计算方式。先计算 Q 和 K 的矩阵点积，然后除以 √d_k（维度的平方根）进行缩放，再过 softmax，最后乘 V。除以 √d_k 是因为当维度 d_k 很大时，点积值会变得很大，导致 softmax 进入梯度极小的饱和区（几乎全是 0 和 1），缩放让梯度回到健康范围。

> 易混淆：**加性注意力 (Additive Attention)** — Bahdanau 注意力用一个小型前馈网络计算分数，计算量更大；缩放点积注意力用矩阵乘法，计算效率更高，且可以用高度优化的矩阵乘法硬件加速

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.1

### 多头注意力 (Multi-Head Attention, MHA)

不是只跑一次注意力，而是同时跑 h 次（h 个"头"），每个头使用不同的投影矩阵（W^Q_i, W^K_i, W^V_i），学习不同的注意力模式。然后把 h 个头的输出拼接（Concat）起来，再通过一个线性层融合。好处：不同头可以关注不同类型的关系——一个头学语法依赖，一个头学语义相似性，一个头学位置邻近性。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.2

### Query / Key / Value (查询 / 键 / 值)

注意力机制的三个核心角色。类比：图书馆检索——Query 是你的搜索词，Key 是每本书的标签，Value 是书的实际内容。你用搜索词（Q）和所有标签（K）比较相关度，然后按相关度从对应的书（V）中提取信息。在 Self-Attention 中，Q/K/V 都是从同一个输入 x 通过三个不同的线性变换 W^Q、W^K、W^V 得到的。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.1
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9

### 位置编码 (Positional Encoding)

Self-Attention 本身是排列不变的（Permutation Invariant）——如果打乱输入词的顺序，注意力分数不会变。但语言是有顺序的（"狗咬人"和"人咬狗"意思完全不同），所以必须加入位置信息。原始 Transformer 使用正弦余弦函数生成位置编码，加到词嵌入上：偶数维用 sin，奇数维用 cos，不同频率让每个位置有唯一的"指纹"。

> 别名：**Positional Embedding**（来自 BERT/GPT 论文中可学习版本）——Encoding 是固定的函数输出，Embedding 是可学习的查找表参数

> 易混淆：**绝对位置编码 vs 相对位置编码 (RPE)** — 原始 Transformer 用绝对位置（sin/cos），后续工作如 RoPE（Rotary Position Embedding）和 ALiBi 改用相对位置差，对长序列泛化更好

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.5

### 前馈网络 (Feed-Forward Network, FFN)

Transformer 每个子层除了注意力之外，还有一个逐位置的全连接前馈网络：两层线性变换中间夹一个 ReLU（或 GELU）激活函数。FFN 是按位置独立作用的——对序列中每个位置使用相同参数但独立计算。注意力层负责"融合上下文"，FFN 层负责"非线性特征变换"。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.3

### 残差连接 (Residual Connection)

每个子层（注意力层、FFN 层）的输出不是直接传给下一层，而是加上子层的输入：output = x + SubLayer(x)。来自 ResNet 的思想——跳过连接让梯度可以直接回传，防止深层网络的梯度消失。Transformer 有 6 个 Encoder 层 + 6 个 Decoder 层，没有残差连接训练会崩。

> 别名：**Skip Connection**（来自计算机视觉 ResNet 论文）——"残差"和"跳跃"描述的是同一件事：让信息跳过中间层直接传递

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.1
> 📖 Paper: He et al., [Deep Residual Learning](https://arxiv.org/abs/1512.03385), CVPR 2016

### 层归一化 (Layer Normalization)

每个子层的残差连接之后，对特征维度做归一化（减均值除标准差），让每一层的输入分布稳定。和 Batch Normalization 不同——BatchNorm 跨样本在 batch 维度归一化，LayerNorm 在每个样本内部跨特征维度归一化，不依赖 batch size，适合变长序列。

> 易混淆：**Pre-LayerNorm vs Post-LayerNorm** — 原始 Transformer 是 Post-LN（先子层再归一化），后续研究发现 Pre-LN（先归一化再子层）训练更稳定，GPT-2 等模型采用 Pre-LN

> 📖 Paper: Ba et al., [Layer Normalization](https://arxiv.org/abs/1607.06450), arXiv 2016
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.1

### 因果掩码 (Causal Mask)

在 Decoder 的 Self-Attention 中，每个位置只能看到它自己和它前面的位置，不能"偷看"未来的词——这就是因果掩码（也叫"look-ahead mask"）。实现方式：在注意力分数矩阵中，把未来位置的值设为 -∞，softmax 后变成 0，等效于"看不到"。

> 别名：**Look-Ahead Mask** / **Autoregressive Mask** / **Upper Triangular Mask** ——都是指同一个三角形掩码，不同论文起了不同名字

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.1

### 填充掩码 (Padding Mask)

一个 batch 中的不同序列长度不同，短序列用特殊的 [PAD] token 补齐到统一长度。但计算注意力时不应该关注这些 [PAD] 位置，所以把 [PAD] 位置的注意力分数设为 -∞（softmax 后变 0）。这和因果掩码是两种不同的掩码，可以同时使用。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3
> 📖 Docs: [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html) — `src_key_padding_mask`

### 编码器 (Encoder)

Transformer 的左半部分。N 个相同的编码器层堆叠，每层包含：① 多头自注意力子层 → ② 逐位置 FFN 子层。每个子层有残差连接和层归一化。编码器的 Self-Attention 是全连接的——每个位置可以看到所有位置，没有掩码限制。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.1

### 解码器 (Decoder)

Transformer 的右半部分。N 个相同的解码器层堆叠，每层包含三个子层：① 带因果掩码的多头自注意力（Masked Self-Attention） → ② 交叉注意力（Cross-Attention，Q 来自 Decoder，K/V 来自 Encoder 输出） → ③ 逐位置 FFN。解码器自回归地逐个生成 token。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.1

### 交叉注意力 (Cross-Attention)

解码器中的第二个注意力子层，连接 Encoder 和 Decoder：Query 来自 Decoder 的当前状态，Key 和 Value 来自 Encoder 的输出。这让 Decoder 在生成每个词时可以"回看"整个输入序列。类比翻译：你在写每个目标语言词时，回头看一眼源语言句子。

> 别名：**Encoder-Decoder Attention** — 原始论文中的叫法，因为它连接的是 Encoder 和 Decoder

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.3

---

## 概念辨析

### Self-Attention vs Cross-Attention

| 维度 | Self-Attention | Cross-Attention |
|------|---------------|-----------------|
| **Q/K/V 来源** | 全部来自同一序列 | Q 来自当前序列，K/V 来自另一序列 |
| **用途** | 让每个位置感知同一序列的全局上下文 | 让一个序列（Decoder）关注另一个序列（Encoder） |
| **出现位置** | Encoder 和 Decoder 中都有 | 仅在 Decoder 中（Encoder-Decoder 架构）|
| **典型应用** | BERT (纯 Self-Attention) | 机器翻译的 Decoder 关注源句 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2

### Encoder-Only vs Decoder-Only vs Encoder-Decoder

| 维度 | Encoder-Only | Decoder-Only | Encoder-Decoder |
|------|-------------|-------------|-----------------|
| **代表模型** | BERT, RoBERTa | GPT, LLaMA | T5, BART, 原始 Transformer |
| **注意力类型** | 双向 Self-Attention | 因果 Self-Attention (单向) | Encoder 双向 + Decoder 因果 + Cross-Attention |
| **预训练目标** | MLM (完形填空) | CLM (预测下一个词) | Span Corruption / Denoising |
| **擅长任务** | 理解类：分类, NER, QA | 生成类：文本续写, 对话 | 翻译, 摘要, 问答 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §1
> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §1
> 📖 Paper: Raffel et al., [T5](https://arxiv.org/abs/1910.10683), §1

### Additive Attention vs Scaled Dot-Product Attention

| 维度 | Additive (Bahdanau) | Scaled Dot-Product (Transformer) |
|------|--------------------|---------------------------------|
| **分数计算** | 小型前馈网络 score = v^T · tanh(W_1·q + W_2·k) | 矩阵点积除以 √d_k |
| **计算效率** | 慢——需要前馈网络 | 快——矩阵乘法可硬件加速 |
| **理论表达力** | 相当（两者都能学任意注意力模式） | 相当 |
| **引入年份** | 2015 (Bahdanau) | 2017 (Vaswani) |

> 📖 Paper: Bahdanau et al., [Attention (2015)](https://arxiv.org/abs/1409.0473), §2
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.2.1

---

## 核心属性

### 信息架构

```
输入序列 x₁ x₂ … xₙ
    │
    ▼
┌──────────────────────────────────┐
│  Input Embedding + Positional    │
│  Encoding                        │
└──────────────────┬───────────────┘
                   │
    ┌──────────────▼──────────────┐
    │     Encoder (N=6 layers)     │
    │  ┌─────────────────────────┐ │
    │  │  Multi-Head Self-Attn   │ │
    │  │  + Add & LayerNorm      │ │
    │  ├─────────────────────────┤ │
    │  │  Feed-Forward Network   │ │
    │  │  + Add & LayerNorm      │ │
    │  └─────────────────────────┘ │
    │         × N layers           │
    └──────────────┬───────────────┘
                   │ Encoder Output
                   │
    ┌──────────────▼──────────────┐
    │     Decoder (N=6 layers)     │
    │  ┌─────────────────────────┐ │
    │  │  Masked Self-Attn       │ │
    │  │  + Add & LayerNorm      │ │
    │  ├─────────────────────────┤ │
    │  │  Cross-Attention        │ │
    │  │  (Q=Dec, K/V=Enc)       │ │
    │  │  + Add & LayerNorm      │ │
    │  ├─────────────────────────┤ │
    │  │  Feed-Forward Network   │ │
    │  │  + Add & LayerNorm      │ │
    │  └─────────────────────────┘ │
    │         × N layers           │
    └──────────────┬───────────────┘
                   │
    ┌──────────────▼──────────────┐
    │  Linear + Softmax → output   │
    └──────────────────────────────┘
```

### 适用场景 ✅

- 机器翻译（Encoder-Decoder 架构）
- 文本理解（Encoder-Only: BERT）
- 文本生成（Decoder-Only: GPT）
- 长距离依赖建模（Self-Attention O(1) 路径长度）
- 大规模并行训练（无顺序依赖）
- 跨模态任务（ViT: 图像, Whisper: 语音）

### 不适用场景 ❌

- 极长序列（>8K tokens）——标准 Self-Attention 的 O(n²) 内存和计算复杂度成为瓶颈
- 实时低延迟场景——自回归解码逐词生成，生成速度受限于序列长度
- 极小数据集——参数量大，容易过拟合
- 资源受限设备——模型参数量和计算量远超 LSTM

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3, §5
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 输入维度 | d_model | 512（原始论文） |
| 头数 | h | 8 |
| 每头维度 | d_k = d_v = d_model / h | 64 |
| FFN 隐藏维度 | d_ff | 2048（= 4 × d_model） |
| Encoder 层数 | N | 6 |
| Decoder 层数 | N | 6 |
| 总参数量 | 基础版 | ~65M |
| 注意力复杂度 | 时间和空间 | O(n² · d) |
| 位置编码 | 正弦余弦 | PE(pos, 2i) = sin(pos/10000^(2i/d)) |
| 优化器 | Adam | β₁=0.9, β₂=0.98, ε=10⁻⁹ |
| 学习率策略 | Warmup + Decay | warmup_steps=4000 |
| Dropout | 各子层 | 0.1 |
| 标签平滑 | 训练时 | ε_ls = 0.1 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Table 3
