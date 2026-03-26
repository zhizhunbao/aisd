---
topic: bert
dimension: concepts
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Eisenstein, 《Natural Language Processing》, Ch.18 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/eisenstein_nlp.pdf"
  - "📖 Docs: Hugging Face Transformers — https://huggingface.co/docs/transformers/model_doc/bert"
expiry: 12m
status: current
---

# BERT 核心概念

> 📖 Paper: Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805), NAACL 2019
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

---

## 术语定义

### 双向编码器表示 (Bidirectional Encoder Representations from Transformers, BERT)

BERT 是 Google 在 2018 年提出的预训练语言模型。它的核心创新是：用"双向"的方式来理解一个词——同时考虑它左边和右边的所有上下文。之前的模型（如 GPT）只能从左到右单向看，就像只看了半本书就要做阅读理解；而 BERT 能同时看完上下文再决定每个词的含义。

技术上，BERT 使用了 Transformer 的编码器部分（不用解码器），通过两个预训练任务（MLM 和 NSP）在大规模语料上学到通用的语言表示，然后通过微调适配到各种下游任务。

> 别名：**BERT**（通用简称）— 来自 Google AI 论文标题的首字母缩写

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §1 "Introduction"

### 掩码语言模型 (Masked Language Model, MLM)

BERT 的第一个预训练任务。做法很简单：随机把输入文本中 15% 的 token 遮住（mask），然后让模型去猜被遮住的词是什么。这就像做完形填空——因为要猜的词可能出现在句子的任何位置，模型不得不同时使用左右两边的上下文来推测，从而学到了真正的双向表示。

具体策略：在被选中的 15% token 中，80% 替换为 `[MASK]`，10% 替换为随机词，10% 保持不变。这样做是为了让模型不只依赖 `[MASK]` token 的存在。

> 别名：**MLM**（通用简称）/ **完形填空任务** (Cloze Task)（来自教育学领域，Taylor 1953 年提出）— 教育学家 Taylor 最早用"完形填空"来测试阅读理解能力，Devlin 等人把这个思想用到了语言模型的预训练中

> 易混淆：**因果语言模型 (Causal LM, CLM)** — MLM 是双向的，看左右两边来猜被遮的词；CLM（如 GPT）是单向的，只看左边来预测下一个词。MLM 不能直接用于文本生成，CLM 可以

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.1 "Masked LM"

### 下一句预测 (Next Sentence Prediction, NSP)

BERT 的第二个预训练任务。给模型两个句子 A 和 B，让它判断 B 是不是 A 在原始语料中的下一句。训练数据中 50% 是真实的连续句对（标记为 `IsNext`），50% 是随机拼接的句对（标记为 `NotNext`）。

这个任务的设计初衷是让 BERT 学到句子之间的关系，以便处理 QA（问答）和 NLI（自然语言推理）等需要理解句对关系的任务。

> 别名：**NSP**（通用简称）

> 易混淆：**句子顺序预测 (Sentence Order Prediction, SOP)** — NSP 判断"是不是下一句"，SOP（ALBERT 使用）判断"两句话的顺序对不对"。后续研究（RoBERTa）发现 NSP 的效果有争议，甚至不如不用

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.2 "Next Sentence Prediction"

### [CLS] Token

BERT 在每个输入序列的最前面插入的一个特殊标记。在预训练和微调中，`[CLS]` 位置的最终隐藏状态被用作整个序列的聚合表示（aggregate representation），用于分类任务。

为什么用第一个位置？因为 self-attention 让 `[CLS]` 能同等地关注到序列中的每一个 token，所以它的表示可以看作整个句子的"摘要"。

> 易混淆：**[SEP] Token** — `[CLS]` 是序列开头用于分类的标记；`[SEP]` 是用于分隔两个句子的标记（出现在每个句子末尾）

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.2 "Input/Output Representations", Figure 1

### [SEP] Token

BERT 用来分隔两个句子的特殊标记。在句对任务中（如 QA、NLI），输入格式是 `[CLS] Sentence A [SEP] Sentence B [SEP]`。`[SEP]` 告诉模型这里是句子的分界线。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.2

### [MASK] Token

MLM 预训练中用来替换被遮住的词的特殊标记。模型需要预测 `[MASK]` 位置上原来是什么词。注意：`[MASK]` 只在预训练阶段出现，微调阶段的输入中没有 `[MASK]`，这就造成了预训练和微调之间的不一致——这也是 80/10/10 替换策略的原因。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.1

### WordPiece 分词 (WordPiece Tokenization)

BERT 使用的子词分词算法。它把词拆成更小的有意义的片段（subword），解决两个问题：(1) 减小词表体积（BERT 词表约 30,000 个 token），(2) 处理从未见过的词（OOV）。

例如：`playing` → `play` + `##ing`，其中 `##` 前缀表示这个子词不是一个新词的开头。

> 别名：**子词分词** (Subword Tokenization)（通用概念名）— WordPiece 是 Google 的具体实现，其他实现还有 BPE（Sennrich et al. 2016）和 SentencePiece（Kudo & Richardson 2018）

> 易混淆：**BPE (Byte Pair Encoding)** — WordPiece 和 BPE 都是子词分词，但合并策略不同：BPE 按频率合并最常共现的字符对；WordPiece 按似然增益合并使语言模型困惑度下降最多的字符对

> 📖 Paper: Wu et al., [Google's Neural Machine Translation System](https://arxiv.org/abs/1609.08144), 2016
> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §5.1

### 预训练 (Pre-Training)

在大规模无标注语料上用自监督任务（MLM + NSP）训练模型，让模型学到通用的语言知识。BERT-Base 在 BooksCorpus (800M words) + English Wikipedia (2500M words) 上预训练。这一步计算成本极高（原始论文使用 16 个 TPU），但只需做一次。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.1 "Pre-training BERT"

### 微调 (Fine-Tuning)

在预训练好的 BERT 模型上，加一个任务特定的输出层（通常只是一个线性分类器），然后用有标注的下游任务数据对整个模型进行端到端训练。微调只需要少量数据和少量训练步数（通常 2-4 个 epoch），就能在各种任务上达到很好的效果。

> 易混淆：**特征提取 (Feature Extraction)** — 微调会更新 BERT 所有层的参数；特征提取则冻结 BERT 参数，只训练新加的分类层。微调效果通常更好

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §4 "Experiments"

### Token Embedding

BERT 输入表示的三个组成部分之一。将每个 WordPiece token 映射为一个固定维度的向量（BERT-Base 为 768 维）。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.2, Figure 2

### Segment Embedding

BERT 输入表示的三个组成部分之一。用于区分输入中的句子 A 和句子 B。属于句子 A 的 token 共享一个段嵌入向量 $E_A$，属于句子 B 的共享 $E_B$。单句任务只用 $E_A$。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.2, Figure 2

### Position Embedding

BERT 输入表示的三个组成部分之一。因为 Transformer 的 self-attention 没有位置感知能力，需要给每个位置加一个可学习的位置嵌入向量。BERT 最多支持 512 个位置（即最大序列长度 512）。

> 易混淆：**正弦位置编码 (Sinusoidal Positional Encoding)** — 原始 Transformer (Vaswani 2017) 用固定的正弦/余弦函数；BERT 用可学习的位置嵌入。可学习嵌入更灵活但不具外推能力

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.2

### BERT-Base 与 BERT-Large

BERT 提供了两个预训练版本：

| 参数 | BERT-Base | BERT-Large |
|------|-----------|------------|
| Transformer 层数 (L) | 12 | 24 |
| 隐藏维度 (H) | 768 | 1024 |
| 注意力头数 (A) | 12 | 16 |
| 总参数量 | 110M | 340M |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.1

---

## 概念辨析

### BERT vs GPT

| 维度 | BERT | GPT |
|------|------|-----|
| **方向性** | 双向（同时看左右） | 单向（只看左边） |
| **架构** | Transformer Encoder | Transformer Decoder |
| **预训练任务** | MLM + NSP | 自回归语言建模 (CLM) |
| **擅长什么** | 理解任务（分类、NER、QA）| 生成任务（文本续写、对话）|
| **典型应用** | 文本分类、信息抽取 | ChatGPT、文本生成 |
| **能否生成文本** | 不擅长（非自回归）| 天生擅长 |
| **论文** | Devlin et al., 2019 | Radford et al., 2018 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3, Figure 3
> 📖 Paper: Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), 2018

### MLM vs CLM

| 维度 | MLM (BERT) | CLM (GPT) |
|------|-----------|-----------|
| **训练目标** | 预测被遮住的 token | 预测下一个 token |
| **上下文方向** | 双向 | 单向（左到右）|
| **掩码比例** | 15% 的 token 被选中 | 不需要掩码 |
| **预训练/微调不一致** | 有（微调无 `[MASK]`）| 没有 |
| **生成能力** | 弱 | 强 |
| **理解能力** | 强 | 较弱 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.1

### Fine-Tuning vs Feature Extraction

| 维度 | Fine-Tuning | Feature Extraction |
|------|-------------|-------------------|
| **参数更新** | 整个 BERT + 新层 | 只更新新加的层 |
| **BERT 参数** | 可学习 | 冻结 |
| **效果** | 通常更好 | 可能较差 |
| **计算资源** | 需要 GPU | 可以用 CPU |
| **适用场景** | 数据量适中 | 资源极度有限 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §5.3 "Feature-based Approach with BERT"

---

## 核心属性

### 信息架构

    输入文本: "我 喜欢 自然 语言 处理"
         │
         ▼
    ┌─────────────────────────────────────────────┐
    │  WordPiece 分词                               │
    │  [CLS] 我 喜欢 自然 语言 处理 [SEP]             │
    └─────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────┐
    │  Input Representation = Token + Segment + Position │
    └─────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────┐
    │  12/24 层 Transformer Encoder                    │
    │  (Self-Attention → FFN → LayerNorm)           │
    └─────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────┐
    │  输出: 每个 token 一个上下文向量               │
    │  [CLS] → 分类; 各 token → 序列标注            │
    └─────────────────────────────────────────────┘

### 适用场景 ✅

- **文本分类**：情感分析、主题分类、垃圾邮件检测
- **序列标注**：命名实体识别 (NER)、词性标注 (POS Tagging)
- **句对任务**：自然语言推理 (NLI)、语义相似度
- **阅读理解 / QA**：SQuAD 抽取式问答
- **特征提取**：作为文本编码器生成上下文嵌入

### 不适用场景 ❌

- **开放式文本生成**：BERT 不是自回归模型，不适合续写/对话/翻译
- **超长文档**：最大 512 token 限制，长文档需要截断或分块
- **实时推理**：BERT-Large (340M 参数) 推理速度较慢
- **低资源部署**：需要 GPU，不适合边缘设备（可考虑 DistilBERT）

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §4
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 模型类型 | Transformer Encoder (双向) | 12 层 (Base) / 24 层 (Large) |
| 预训练任务 | MLM + NSP | 15% token 被 mask |
| 输入格式 | `[CLS] Sent_A [SEP] Sent_B [SEP]` | 句对输入 |
| 输入表示 | Token + Segment + Position | 三者相加 |
| 最大序列长度 | 512 tokens | WordPiece 分词后的长度 |
| 词表大小 | ~30,000 | WordPiece |
| [CLS] 用途 | 分类任务的聚合表示 | 情感分析：[CLS] → 正/负 |
| 微调方式 | 加任务特定头 + 端到端训练 | 2-4 epoch, lr ~ 2e-5 |
| BERT-Base 参数 | L=12, H=768, A=12 | 110M 参数 |
| BERT-Large 参数 | L=24, H=1024, A=16 | 340M 参数 |
