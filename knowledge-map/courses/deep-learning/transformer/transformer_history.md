---
topic: transformer
dimension: history
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Paper: Bahdanau et al., 'Neural Machine Translation by Jointly Learning to Align and Translate', ICLR 2015 — https://arxiv.org/abs/1409.0473"
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📚 Book: Jurafsky & Martin, 《SLP3》 Ch.9-10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: never
status: current
---

# Transformer 的故事线：从循环网络到注意力就是一切

> **核心主题：** 序列建模从"逐步传递信息"到"一步看全局"的范式转变
> **故事线：** 一个不断突破"顺序瓶颈"的求解历程

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 如何让神经网络理解一段文本的含义并生成另一段文本（如翻译、摘要）？核心挑战是：语言是**顺序的**，但GPU擅长**并行**——如何调和这个矛盾？

1980 年代至 2010 年代初，序列建模被循环神经网络（RNN）统治。RNN 的核心思想是"一个 token 接一个 token 地处理"，就像人类逐字阅读一样。但这个"逐字阅读"的假设在 GPU 时代成了严重的性能瓶颈——GPU 有数千个计算核心，但 RNN 只让它们一次处理一个 token。

> 🔑 **问题提出：** 能否设计一种架构，既能理解序列的含义，又能充分利用 GPU 的并行计算能力？

---

## 📚 第一章：RNN 与 Seq2Seq 的辉煌与瓶颈（1986-2014）

> **关键人物：** Jeffrey Elman、Ilya Sutskever、Kyunghyun Cho
> **关键论文：** [Sutskever et al. "Sequence to Sequence Learning with Neural Networks", NeurIPS 2014](https://arxiv.org/abs/1409.3215)

### 发生了什么？

1986 年，Jordan 提出了循环网络的概念；1990 年，Elman 简化了结构，提出了经典的 Simple RNN。但 vanilla RNN 有严重的**梯度消失**问题。

1997 年，Hochreiter & Schmidhuber 发明了 LSTM，用门控机制缓解了梯度消失。2014 年，Cho 等人提出了更简洁的 GRU。同年，Sutskever 等人在 Google 提出了 **Seq2Seq** 架构：用一个 RNN（Encoder）将输入序列编码为固定长度向量，再用另一个 RNN（Decoder）从这个向量解码输出序列。

Seq2Seq 在机器翻译上取得了突破性成绩，成为了 NMT（Neural Machine Translation）的标准范式。

### 为什么这很重要？

Seq2Seq 第一次实现了端到端的序列到序列映射，不再需要手工设计翻译规则或统计短语表。但更重要的是，它揭示了一个深层次的**信息瓶颈**：整个输入序列被压缩成一个固定长度的向量，输入越长，丢失的信息越多。

### 但还有一个问题……

当翻译一个长句子时，Decoder 只能通过一个固定向量来"回忆"整个输入。就像让你读完一整本书后只能记住一段话的概要——你必然会忘记很多细节。BLEU 分数随句子长度增加而急剧下降。

> 🔑 **故事转折点：** 如果 Decoder 每步生成时能"回头看"原文呢？——注意力机制的想法萌发

---

## 📚 第二章：注意力机制——打破信息瓶颈（2015）

> **关键人物：** Dzmitry Bahdanau、Minh-Thang Luong
> **关键论文：** [Bahdanau et al. "Neural Machine Translation by Jointly Learning to Align and Translate", ICLR 2015](https://arxiv.org/abs/1409.0473)

### 发生了什么？

2015 年，Bahdanau 等人提出了**加性注意力机制**：Decoder 在生成每个输出 token 时，不再只看最后一个隐藏状态，而是对 Encoder 的**所有**隐藏状态计算权重，加权求和得到一个"上下文向量"。哪些输入位置与当前输出最相关，就给它们更高的权重。

同年，Luong 等人提出了**点积注意力**等更高效的变体。

注意力机制一举解决了长句子翻译质量下降的问题，BLEU 分数不再随长度衰减。

### 为什么这很重要？

注意力机制的本质贡献是**直接连接**：Decoder 的每个位置可以直接"看到"Encoder 的任何位置，不需要信息逐步通过 RNN 传递。这从根本上解决了信息瓶颈问题，并且注意力权重的可视化展示了模型"在关注什么"，提供了一定的可解释性。

### 但还有一个问题……

Encoder 本身仍然是 RNN——信息仍然需要通过 RNN 逐步传递。一个长度为 1000 的句子，Encoder 仍然需要 1000 步串行计算。注意力改善了 Decoder 对 Encoder 输出的利用，但没有改变 Encoder 自身的并行化瓶颈。

> 🔑 **故事转折点：** 能不能连 Encoder 也用注意力替代 RNN？如果一个序列内部的每个位置都能直接 attend 到所有其他位置呢？

---

## 📚 第三章：Attention Is All You Need（2017）

> **关键人物：** Ashish Vaswani、Noam Shazeer、Niki Parmar（Google Brain & Google Research）
> **关键论文：** [Vaswani et al. "Attention Is All You Need", NeurIPS 2017](https://arxiv.org/abs/1706.03762)

### 发生了什么？

2017 年，Google 的 8 位研究者发表了"Attention Is All You Need"——标题本身就是一个大胆的宣言。他们提出了 **Transformer** 架构：

1. **完全抛弃 RNN 和 CNN**：序列建模**只用注意力机制**
2. **Self-Attention**：序列中每个位置 attend 到同一序列的所有其他位置，一步完成全局信息交互
3. **Multi-Head Attention**：多组并行的注意力头捕获不同模式
4. **Positional Encoding**：用正弦/余弦函数注入位置信息（因为纯注意力无法区分位置）
5. **Encoder-Decoder + 残差 + LayerNorm**：标准化的模块堆叠

在 WMT 2014 英德翻译任务上，Transformer 达到了 28.4 BLEU（超过之前所有模型），且**训练时间只需 3.3 天**（在 8 块 P100 GPU 上），远快于当时最好的 RNN 模型。

### 为什么这很重要？

Transformer 是深度学习历史上最具影响力的架构之一。它的重要性不仅在于翻译性能的提升，更在于：
- **并行化**：训练速度比 RNN 快一个数量级，使得大规模预训练成为可能
- **可扩展性**：简单地堆叠更多层和增大维度就能持续提升性能，开启了"scaling law"
- **通用性**：同一架构在 NLP、CV、语音等所有领域全面成功

### 但还有一个问题……

原始 Transformer 是为机器翻译设计的 Encoder-Decoder 架构。问题是：能否用 Transformer 解决更广泛的 NLP 任务（分类、问答、命名实体识别等）？是否需要不同的训练策略？

> 🔑 **故事转折点：** 如果只用 Encoder 做理解，或只用 Decoder 做生成呢？——BERT 和 GPT 的分化

---

## 📚 第四章：BERT 与 GPT——Transformer 的两条路线（2018-2019）

> **关键人物：** Jacob Devlin (BERT/Google)、Alec Radford (GPT/OpenAI)
> **关键论文：** [Radford et al. "Improving Language Understanding by Generative Pre-Training", 2018](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) | [Devlin et al. "BERT", NAACL 2019](https://arxiv.org/abs/1810.04805)

### 发生了什么？

2018 年，两个独立的团队分别探索了 Transformer 的两种变体：

**GPT（OpenAI，2018.6）**：只用 **Decoder**（单向/因果注意力），通过**自回归预训练**（预测下一个 token）在大规模文本上学习语言模型。然后在下游任务上微调。

**BERT（Google，2018.10）**：只用 **Encoder**（双向注意力），通过**掩码语言模型（MLM）**预训练（随机遮挡 15% 的 token 并预测），学习双向上下文表示。在 11 个 NLP 基准上全面刷新纪录。

BERT 的 MLM 让模型可以同时看到左右上下文（"The [MASK] sat on the mat" → 预测 cat），而 GPT 只能看到左侧上下文。

### 为什么这很重要？

这标志着"**预训练 + 微调**"范式的确立：
- 在大规模无标注文本上预训练一个通用的语言模型
- 在小规模标注数据上微调到特定任务

这彻底改变了 NLP 的研究范式：不再为每个任务从零训练模型，而是站在预训练模型的"肩膀"上。

### 但还有一个问题……

BERT-base 有 110M 参数，当时已算"大"模型。但研究者很快发现：**模型越大性能越好**。那么，这个 scaling 的极限在哪里？

> 🔑 **故事转折点：** Scaling Law 的发现——模型参数、数据量和计算量的关系被量化

---

## 📚 第五章：大语言模型时代（2020-至今）

> **关键人物：** Tom Brown (GPT-3/OpenAI)、Jared Kaplan (Scaling Laws)、Google (PaLM/Gemini)、Meta (LLaMA)
> **关键论文：** [Brown et al. "Language Models are Few-Shot Learners", NeurIPS 2020](https://arxiv.org/abs/2005.14165)

### 发生了什么？

2020 年，OpenAI 发布了 GPT-3（175B 参数），展示了"大力出奇迹"：不需要微调，仅通过**提示词（prompt）**就能完成翻译、问答、代码生成等任务（Few-Shot / Zero-Shot Learning）。

关键里程碑：
- **2020 GPT-3**：175B 参数，In-Context Learning
- **2020 T5**：Google 的 Encoder-Decoder，"text-to-text" 统一框架
- **2021 Scaling Laws**：Kaplan et al. 量化了参数量、数据量和计算量的幂律关系
- **2022 ChatGPT**：GPT-3.5 + RLHF，对话式 AI 引爆公众关注
- **2023 GPT-4**：多模态（文本+图像），估计 1.8T 参数 MoE
- **2023 LLaMA**：Meta 发布开源 LLM，开启开源 LLM 浪潮
- **2024+ Vision Transformer, Diffusion Transformers**：Transformer 向 CV、生成式 AI 全面扩展

### 为什么这很重要？

Transformer 从一个翻译架构演变为通用的人工智能基础设施。所有现代 AI 系统（ChatGPT、Claude、Gemini、Copilot）的核心都是 Transformer。这是深度学习迄今为止最成功的单一架构。

### 但还有一个问题……

$O(n^2)$ 的注意力复杂度限制了序列长度，Mamba 等替代架构开始挑战 Transformer。Transformer 是否会被取代？目前尚无定论。

> 🔑 **故事转折点：** 效率与规模的矛盾——线性注意力、稀疏注意力、状态空间模型等替代方案开始涌现

---

## 🗺️ 全局回顾：技术演进路线图

```
1986: Elman                     Simple RNN
      │                         (顺序处理，梯度消失)
      ▼
1997: Hochreiter, Schmidhuber   LSTM
      │                         (门控缓解梯度消失)
      ▼
2014: Sutskever, Cho            Seq2Seq + GRU
      │                         (Encoder-Decoder 架构)
      │
      ╳  信息瓶颈 ── 整个输入压缩为单一向量
      │
      ▼
2015: Bahdanau, Luong           Attention Mechanism
      │                         (Decoder 可以回看 Encoder)
      │
      ╳  Encoder 仍是 RNN ── 无法并行
      │
      ▼
2017: Vaswani et al.            Transformer
      │                         (纯注意力，完全并行)
      ├──────────────────────────────┐
      ▼                              ▼
2018: Radford (OpenAI)          2018: Devlin (Google)
      GPT (Decoder-only)              BERT (Encoder-only)
      │                               │
      ▼                               ▼
2020: Brown et al.              T5, BART
      GPT-3 (175B)              (Encoder-Decoder)
      │
      ▼
2022: ChatGPT (RLHF)
      │
      ▼
2023+: GPT-4, LLaMA, Gemini, ViT, Whisper...
       (全领域 Transformer)
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| RNN → LSTM | 梯度消失 → 门控机制保留长期记忆 |
| LSTM → Seq2Seq | 单一任务 → 通用序列到序列映射 |
| Seq2Seq → Attention | 信息瓶颈 → Decoder 可直接访问 Encoder 所有位置 |
| Attention + RNN → Transformer | 串行瓶颈 → 完全并行的 Self-Attention |
| Transformer → BERT/GPT | 任务特定 → 预训练 + 微调的通用范式 |
| BERT/GPT → GPT-3/LLM | 微调 → In-Context Learning / Prompt 范式 |
