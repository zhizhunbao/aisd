---
topic: transformer
dimension: tutorial
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.9 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》, Ch.10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Bahdanau et al., 'Neural Machine Translation by Jointly Learning to Align and Translate', ICLR 2015 — https://arxiv.org/abs/1409.0473"
expiry: 12m
status: current
---

# Transformer 教程

> **前置知识：** RNN/LSTM 序列模型基础、矩阵乘法、Softmax 概率归一化
> **参考来源：** Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), 2017

---

## Section 0: 前置知识速查

1. **RNN / LSTM**：按顺序一步一步处理序列的神经网络——t=1 → t=2 → … → t=n，每一步的输出依赖上一步
2. **Seq2Seq**：编码器把输入句子压成一个固定向量，解码器从这个向量逐词生成输出句子
3. **注意力机制 (Bahdanau Attention)**：Seq2Seq 的改进——解码器每生成一个词，都回头看整个输入序列，算一个"注意力分布"决定重点看哪些词
4. **矩阵乘法**：两个矩阵相乘得到一个新矩阵——Transformer 几乎所有计算都是矩阵乘法
5. **Softmax**：把任意一组实数变成概率分布（和为 1，全部非负）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **训练慢到崩溃**：RNN 必须一步一步顺序计算（t=1 算完才能算 t=2），完全无法并行。一个 100 词的句子要串行跑 100 步。GPU 有 1000 个核心，但 RNN 只能用 1 个——其他 999 个在发呆。训练一个翻译模型要好几天
- 🔥 **长距离遗忘**：一个 50 词的句子，第 1 个词的信息要经过 49 步才能传到第 50 个词。即使用 LSTM，经过这么多步信息也会严重衰减。模型对长句"记不住前面说了什么"
- 🔥 **Seq2Seq 的瓶颈**：编码器把整个输入句子压缩成一个固定长度的向量——一个 100 词的技术文档和一个 5 词的短句，都被压成同样大小的向量。信息必然丢失
- 🔥 **注意力是补丁不是解决方案**：Bahdanau 注意力缓解了瓶颈问题，但底层仍然是 RNN——训练速度没有本质提升，仍然无法并行

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §1 "Introduction"
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10 §10.7 "The Challenge of Long-Term Dependencies"

### 它的核心价值

1. **完全并行化**：Self-Attention 一次性计算序列中所有位置之间的关系——不需要等上一步完成。训练速度提升 10x-100x
2. **O(1) 路径长度**：任意两个位置之间只需 1 步就能直接交互（通过注意力权重），不像 RNN 需要 O(n) 步。长距离依赖问题从根本上解决
3. **统一架构**：同一个架构稍作修改就能做理解（BERT = Encoder）、生成（GPT = Decoder）、翻译（T5 = Encoder-Decoder）。从此不需要为每个任务设计不同的模型
4. **规模化的基础**：只有能并行才能上大规模——GPT-3 的 175B 参数如果用 RNN 训练，可能需要几年；Transformer 让大模型成为可能

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §1, Table 1

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 整体生命周期

```
输入: "The cat sat on the mat"          输出: "Le chat s'est assis sur le tapis"
          │                                              ▲
          ▼                                              │
  ┌───────────────┐                             ┌───────────────┐
  │  Tokenize &    │                             │  Detokenize    │
  │  Embed (词嵌入) │                             │  (反序列化)    │
  └───────┬───────┘                             └───────┬───────┘
          │                                              │
          ▼                                              │
  ┌───────────────┐                             ┌───────────────┐
  │  + Positional   │                             │  Linear +      │
  │  Encoding       │                             │  Softmax       │
  └───────┬───────┘                             └───────┬───────┘
          │                                              │
          ▼                                              │
  ┌───────────────────────────────────────────────────────┐
  │                                                       │
  │    ENCODER (×6 层)              DECODER (×6 层)        │
  │  ┌─────────────────┐        ┌─────────────────────┐  │
  │  │ Multi-Head       │        │ Masked Multi-Head    │  │
  │  │ Self-Attention   │        │ Self-Attention       │  │
  │  │ + Add & Norm     │        │ + Add & Norm         │  │
  │  ├─────────────────┤        ├─────────────────────┤  │
  │  │ Feed-Forward     │───────→│ Cross-Attention      │  │
  │  │ Network          │  K,V   │ (Q=Dec, K/V=Enc)    │  │
  │  │ + Add & Norm     │        │ + Add & Norm         │  │
  │  └─────────────────┘        ├─────────────────────┤  │
  │                              │ Feed-Forward         │  │
  │                              │ Network              │  │
  │                              │ + Add & Norm         │  │
  │                              └─────────────────────┘  │
  └───────────────────────────────────────────────────────┘
```

### 2.2 核心机制

**为什么用 Self-Attention 而不是 RNN？**

| 决策点 | RNN 做法 | Transformer 做法 | 为什么更好 |
|--------|---------|-----------------|----------|
| 词间交互 | 信息通过隐藏状态逐步传递 | 所有词同时互相看（矩阵乘法） | 并行 + 路径短 |
| 长距离依赖 | O(n) 步传递，信息衰减 | O(1) 直接连接 | 不衰减 |
| 并行度 | 完全串行 | 完全并行 | 训练快 10-100 倍 |
| 代价 | O(n) 内存 | O(n²) 内存 | 内存换速度 |

**为什么要缩放（除以 √d_k）？**

当 Q 和 K 的维度 d_k 很大时，它们的点积值的方差 ≈ d_k。如果 d_k=64，点积值的标准差就有 8 左右。softmax 对输入值的大小很敏感——输入太大，输出就趋近 one-hot（一个接近 1，其他接近 0），梯度几乎为 0。除以 √d_k 把方差拉回到 1，让 softmax 保持在梯度健康的区间。

**为什么用多头而不是一个大注意力？**

单头注意力：d_model=512 维的向量做一次注意力。多头注意力：拆成 8 份（每份 64 维），每份独立做注意力，再拼回来。计算量差不多（因为每个头维度更小），但能学到**不同类型**的注意力模式。实验证明多头比单头效果好（Vaswani 论文 Table 3）。

**为什么 FFN 要先升维再降维（512 → 2048 → 512）？**

注意力层负责"融合上下文"（哪些词和我相关），FFN 负责"加工信息"（对融合后的表示做非线性变换）。先升到 4 倍维度是为了给模型更大的"工作空间"——在高维空间里做特征组合比在低维空间里更容易。然后降回原维度保持维度一致。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3, §4, Table 1

---

## Section 3: 局限性

1. **O(n²) 复杂度** → Self-Attention 对序列中所有位置对都要计算一次注意力，内存和计算量随序列长度 n 的平方增长。处理 8K tokens 的文档需要 64M 个注意力分数。应对策略：Sparse Attention（只关注部分位置）、Linear Attention、Flash Attention（优化 GPU 内存访问）

2. **没有天生的位置感知** → 必须额外注入位置信息（Positional Encoding）。不同的位置编码方案各有优缺点——正弦余弦编码理论上可外推到更长序列，但实践中超过训练长度效果急剧下降。应对策略：RoPE（旋转位置编码）、ALiBi 等相对位置方案

3. **自回归生成慢** → Decoder 逐个 token 生成，每生成一个词都要跑一次完整的前向传播。100 个词需要 100 次前向。应对策略：KV Cache（缓存已算过的 Key/Value）、推测解码（Speculative Decoding）

4. **参数量大，小数据易过拟合** → 即使基础版 Transformer 也有 ~65M 参数。小训练集容易过拟合。应对策略：预训练 + 微调范式（在大语料上预训练，小数据集只微调）

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §4, Table 1
> 📖 Paper: Tay et al., [Efficient Transformers: A Survey](https://arxiv.org/abs/2009.06732), 2022

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **RNN / LSTM** | 参数少；天然理解顺序 | 无法并行；长距离遗忘 | 低资源场景、短序列 |
| **CNN (序列)** | 可并行；局部特征提取好 | 感受野有限；需多层堆叠才能看远 | 文本分类（短文本） |
| **Transformer (Full)** | 完全并行；全局注意力；统一架构 | O(n²) 内存；需位置编码 | 翻译、预训练模型、通用 NLP |
| **Sparse Transformer** | O(n√n) 复杂度 | 需精心设计注意力模式 | 长文档处理 |
| **Linear Attention** | O(n) 复杂度 | 表达力可能下降 | 超长序列（>16K） |
| **RNN + Attention** | 兼顾顺序和全局 | 仍然无法并行（RNN 部分） | 低延迟推理、边缘设备 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Table 1
> 📖 Paper: Tay et al., [Efficient Transformers: A Survey](https://arxiv.org/abs/2009.06732)

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Vaswani et al. "Attention Is All You Need" (2017)](https://arxiv.org/abs/1706.03762) | 📖 论文 | 全文核心参考 |
| [Bahdanau et al. "Attention Mechanism" (2015)](https://arxiv.org/abs/1409.0473) | 📖 论文 | Section 0, 1——注意力机制起源 |
| [《Deep Learning》Ch.10](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | Section 0——序列模型基础 |
| [《SLP3》Ch.9](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 📚 教科书 | Section 2——Transformer 架构详解 |
| [Tay et al. "Efficient Transformers" (2022)](https://arxiv.org/abs/2009.06732) | 📖 论文 | Section 3, 4——高效变体对比 |
