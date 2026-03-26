---
topic: transformer
dimension: history
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Paper: Bahdanau et al., 'Neural Machine Translation by Jointly Learning to Align and Translate', ICLR 2015 — https://arxiv.org/abs/1409.0473"
  - "📖 Paper: Sutskever et al., 'Sequence to Sequence Learning with Neural Networks', NeurIPS 2014 — https://arxiv.org/abs/1409.3215"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.9-10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: never
status: current
---

# Transformer 的故事线：从"一步一步走"到"一眼看全部"

> **核心主题：** 序列建模从串行走向并行，从局部记忆走向全局注意力
> **故事线：** RNN 太慢 → Attention 打补丁 → Transformer 彻底重构 → 统治整个 AI

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 机器翻译需要处理变长序列，但经典方法要么记不住长句子，要么训练太慢——能不能既快又准？

2013 年之前，机器翻译的主流是统计方法（基于短语的翻译）。神经网络刚开始进入 NLP，人们面临一个根本矛盾：RNN 能处理变长序列，但太慢（串行）且记不住长句子——有没有更好的方式？

> 🔑 **问题提出：** 如何让模型既能理解长序列又能快速训练？

---

## 📚 第一章：Seq2Seq — "压缩一切到一个向量"（2014）

> **关键人物：** Ilya Sutskever (Google Brain → OpenAI)
> **关键论文：** Sutskever et al., [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215), NeurIPS 2014

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Sutskever 肖像 | Wikimedia Commons | `https://commons.wikimedia.org/wiki/File:Ilya_Sutskever_at_NeurIPS_2019.jpg` | CC BY-SA |
| 论文首页 | arXiv | `https://arxiv.org/abs/1409.3215` | 学术引用 |

### 发生了什么？

Sutskever 在 Google Brain 提出了一个优雅的想法：用一个 LSTM（编码器）把整个输入句子"读进去"，压缩成一个固定长度的向量（context vector），然后用另一个 LSTM（解码器）从这个向量逐词"吐出"翻译。这就是 Seq2Seq（Sequence-to-Sequence）。

简单、直觉、能跑——在法英翻译任务上第一次让神经翻译接近了统计翻译的水平。

### 为什么这很重要？

Seq2Seq 证明了"端到端学翻译"是可行的——不需要人工设计语言规则、不需要对齐表、不需要短语表。只需要平行语料，模型自己学。这彻底改变了机器翻译的研究范式。

### 但还有一个问题……

**"一切压缩到一个向量"是个信息瓶颈。** 100 个词的技术文档和 5 个词的短句，都被压成同一个大小的向量。句子越长，信息丢失越严重。翻译质量随句子长度急剧下降。

> 🔑 **故事转折点：** 固定长度的 context vector 装不下长句——需要让解码器"回头看"输入

---

## 📚 第二章：Attention — "每一步都回头看一眼"（2015）

> **关键人物：** Dzmitry Bahdanau (蒙特利尔大学, Mila)
> **关键论文：** Bahdanau et al., [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473), ICLR 2015

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Bahdanau 肖像 | Mila 官网 | `https://mila.quebec/en/directory/dzmitry-bahdanau` | 学术引用 |
| 论文首页 | arXiv | `https://arxiv.org/abs/1409.0473` | 学术引用 |

### 发生了什么？

Bahdanau 意识到信息瓶颈的根源是"只看最后一步的隐藏状态"。他的解决方案：**解码器每生成一个词，都回头看编码器的所有隐藏状态，算一个"注意力分布"决定重点看哪些位置。** 这就是注意力机制（Attention Mechanism）。

具体做法：学一个小型前馈网络，输入是解码器当前状态和编码器每个位置的状态，输出是一个相关度分数。对所有位置做 softmax 得到注意力权重，然后加权求和编码器状态得到上下文向量。

### 为什么这很重要？

注意力机制解决了信息瓶颈——解码器不再只依赖一个固定向量，而是每一步都能"看到"整个输入。长句翻译质量大幅提升。而且注意力权重可以可视化——你能"看到"模型在翻译每个词时重点关注源句的哪个位置，提供了可解释性。

Luong (2015) 进一步提出了更简化的注意力计算（点积注意力），计算更高效。

### 但还有一个问题……

**底层还是 RNN。** 注意力只是 RNN 上面的"补丁"——编码器仍然需要一步一步顺序处理输入，无法并行。训练一个好的翻译模型仍然需要好几天。注意力解决了"准确度"，但没解决"速度"。

> 🔑 **故事转折点：** 注意力本身如此强大，那我们还需要 RNN 吗？——如果只用注意力呢？

---

## 📚 第三章：Transformer — "Attention Is All You Need"（2017）

> **关键人物：** Ashish Vaswani, Noam Shazeer, Niki Parmar 等 (Google Brain / Google Research)
> **关键论文：** Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| 论文首页 | arXiv | `https://arxiv.org/abs/1706.03762` | 学术引用 |
| Transformer 架构图 | 原始论文 Figure 1 | `https://arxiv.org/abs/1706.03762` (Fig.1) | 学术引用 |

### 发生了什么？

Google 的 8 位研究者问了一个大胆的问题：**既然注意力这么好用，为什么还需要 RNN？直接用注意力不行吗？** 答案是：行。他们设计了 Transformer——一个完全基于 Self-Attention 的架构：

1. **Self-Attention**：让序列中的每个位置同时看到所有其他位置（不需要逐步传递）
2. **Multi-Head Attention**：跑 8 次注意力学不同模式，再拼接
3. **Positional Encoding**：没有 RNN 就没有位置信息，用正弦函数注入
4. **残差连接 + 层归一化**：稳定训练
5. **Encoder-Decoder 架构**：编码器做理解，解码器做生成

在 WMT 2014 英德翻译任务上，Transformer 超越了所有已有模型，BLEU 分数达到 28.4——而且训练时间只需要 3.5 天（8 GPU），远快于等效的 RNN 模型。

### 为什么这很重要？

Transformer 不只是"又一个翻译模型"——它从根本上改变了序列建模的方式：

- **从串行到并行**：训练速度提升 ~10-100 倍，让大规模训练成为可能
- **统一架构**：同一个架构可以拆成 Encoder (→BERT)、Decoder (→GPT)、或完整 Enc-Dec (→T5)
- **扩展到其他领域**：视觉 (ViT)、语音 (Whisper)、蛋白质 (AlphaFold2)、代码 (Codex)

这篇论文的引用量超过 13 万次，是 AI 历史上最有影响力的论文之一。

### 但还有一个问题……

**O(n²) 的计算和内存复杂度。** Self-Attention 对序列中所有位置对都要计算注意力分数——序列长度 n=1000 就需要 100 万个注意力分数。对于长文档、高分辨率图像、长音频，这个代价太大了。

> 🔑 **故事转折点：** Transformer 统治了 AI，但 O(n²) 限制了"更长、更大"——高效 Transformer 的竞赛开始了

---

## 📚 第四章：后 Transformer 时代 — "让它更快更长"（2018-2025）

> **关键人物：** Jacob Devlin (Google → BERT), Alec Radford (OpenAI → GPT), 等
> **关键论文：** Devlin et al., [BERT](https://arxiv.org/abs/1810.04805); Radford et al., [GPT](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| BERT 论文首页 | arXiv | `https://arxiv.org/abs/1810.04805` | 学术引用 |
| GPT-3 论文首页 | arXiv | `https://arxiv.org/abs/2005.14165` | 学术引用 |

### 发生了什么？

Transformer 架构一经发明，立即被拆分、重组、放大：

- **BERT (2018)**：只用 Encoder + 双向注意力 + MLM 预训练 → 理解类任务称霸
- **GPT-1/2/3 (2018-2020)**：只用 Decoder + 因果注意力 + 自回归预训练 → 生成类任务称霸
- **T5 (2019)**：完整 Encoder-Decoder + Text-to-Text 统一框架
- **ViT (2020)**：把图像切片成 patch 当 token，纯 Transformer 做视觉
- **高效变体**：Sparse Attention、Linear Attention、Flash Attention、RoPE、ALiBi等解决 O(n²) 问题

### 为什么这很重要？

Transformer 成为了整个 AI 领域的"通用架构"——就像互联网中的 TCP/IP 一样基础。几乎所有 2023-2025 年的 SOTA 模型（GPT-4、Claude、Gemini、LLaMA 3）都基于 Transformer 的变体。

### 但还有一个问题……

**Transformer 是终极架构吗？** 新兴架构如 Mamba（状态空间模型）声称比 Transformer 更高效。未来可能出现 Transformer 和结构化状态空间模型的混合架构。但截至 2025 年，Transformer 仍然是无可争议的王者。

---

## 🗺️ 全局回顾：技术演进路线图

```
2014                    2015                    2017                    2018+
Seq2Seq (Sutskever)     Attention (Bahdanau)    Transformer (Vaswani)   BERT/GPT/T5/ViT...
┌──────────────┐       ┌──────────────┐        ┌──────────────┐        ┌──────────────────┐
│ Encoder-LSTM │──────→│ + Attention  │───────→│ Only Attention│───────→│ Encoder: BERT    │
│ Decoder-LSTM │       │   Mechanism  │        │ No RNN at all │       │ Decoder: GPT     │
│ Fixed Vector │       │ Dynamic Focus│        │ All Parallel  │       │ Both: T5/BART    │
└──────────────┘       └──────────────┘        └──────────────┘        │ Vision: ViT      │
     信息瓶颈               仍然串行                O(n²) 代价           │ LLM: GPT-4等     │
                                                                       └──────────────────┘
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| 统计翻译 → Seq2Seq | 不再需要人工语言规则，端到端学习 |
| Seq2Seq → + Attention | 打破固定长度向量的信息瓶颈 |
| RNN + Attention → Transformer | 从串行到完全并行，训练提速 10-100 倍 |
| 原始 Transformer → BERT/GPT | 从任务特定到预训练 + 微调/提示的通用范式 |

### 🎥 视觉素材总表（视频制作用）

| 章节 | 人物 | 肖像来源 | 论文/事件图片 | 版权 |
|------|------|---------|-------------|------|
| 第一章 | Ilya Sutskever | Wikimedia Commons: `File:Ilya_Sutskever_at_NeurIPS_2019.jpg` | arXiv: `1409.3215` | CC BY-SA |
| 第二章 | Dzmitry Bahdanau | Mila 官网 | arXiv: `1409.0473` | 学术引用 |
| 第三章 | Ashish Vaswani 等 | 论文作者页 | arXiv: `1706.03762` Fig.1 | 学术引用 |
| 第四章 | Jacob Devlin / Alec Radford | Google AI Blog / OpenAI Blog | arXiv: `1810.04805` / `2005.14165` | 学术引用 |

> ⚠️ **素材查找优先级：**
> 1. **Wikimedia Commons** — 首选
> 2. **大学官网/档案馆** — 本校教授的官方照片
> 3. **论文首页截图** — arXiv / Google Scholar
>
> ❌ **禁止：** AI 生成肖像、库存图片网站、无版权标注的图片
