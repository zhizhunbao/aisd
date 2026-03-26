---
topic: bert
dimension: history
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📖 Paper: Mikolov et al., 'Efficient Estimation of Word Representations', 2013 — https://arxiv.org/abs/1301.3781"
  - "📖 Paper: Peters et al., 'Deep contextualized word representations (ELMo)', 2018 — https://arxiv.org/abs/1802.05365"
  - "📖 Paper: Radford et al., 'Improving Language Understanding by Generative Pre-Training (GPT)', 2018"
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', 2017 — https://arxiv.org/abs/1706.03762"
expiry: never
status: current
---

# BERT 的故事线：从静态词向量到双向预训练

> **核心主题：** 如何让计算机真正"理解"一个词在特定语境中的含义
> **故事线：** 一段从"一个词一个固定含义"到"同一个词在不同句子中有不同含义"的打怪升级历程

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 2013 年之前，NLP 的核心难题是：如何把人类语言变成计算机能理解的数字？

计算机不理解文字。最早的做法是 One-Hot Encoding（独热编码）——"cat" = [1,0,0,...,0]，"dog" = [0,1,0,...,0]。问题是：这种表示认为所有词都一样"远"，"cat" 和 "dog" 的距离 = "cat" 和 "computer" 的距离。这显然不对——猫和狗比猫和电脑更"近"才对。

> 🔑 **问题提出：** 我们需要一种"知道词与词之间关系"的表示方法

---

## 📚 第一章：词向量革命（2013）

> **关键人物：** Tomáš Mikolov (Google / Facebook AI)
> **关键论文：** [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781), 2013

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Word2Vec 论文首页 | arXiv | `https://arxiv.org/abs/1301.3781` | 学术引用 |

### 发生了什么？

2013 年，Mikolov 在 Google 提出了 Word2Vec——用神经网络从大量文本中学习词向量。核心思想来自语言学的**分布假说** (Distributional Hypothesis)："一个词的含义由它周围的词决定"（Firth, 1957: "You shall know a word by the company it keeps"）。

Word2Vec 用两种方法实现这个思想：
- **CBOW**：用周围词预测中间词
- **Skip-gram**：用中间词预测周围词

结果是每个词被映射到一个稠密向量空间，词义相近的词距离相近。更神奇的是，向量还能做"类比推理"：$\vec{\text{king}} - \vec{\text{man}} + \vec{\text{woman}} \approx \vec{\text{queen}}$。

### 为什么这很重要？

Word2Vec 第一次大规模证明：词的语义可以被编码到向量中。这彻底改变了 NLP——不再需要手动设计特征，神经网络可以直接学习语义表示。GloVe (Pennington et al., 2014) 和 FastText (Bojanowski et al., 2017) 进一步改进了词向量的训练方法。

### 但还有一个问题……

Word2Vec 给每个词**一个固定向量**。"bank" 在 "river bank" 和 "bank account" 中得到**完全相同**的向量。但人类知道这两个 "bank" 意思完全不同！这叫**一词多义问题** (Polysemy)——静态词向量无法处理。

> 🔑 **故事转折点：** 词向量很好，但不够——同一个词在不同语境中需要不同的表示

---

## 📚 第二章：上下文嵌入先驱 ELMo（2018 年 2 月）

> **关键人物：** Matthew Peters (Allen Institute for AI)
> **关键论文：** [Deep contextualized word representations](https://arxiv.org/abs/1802.05365), NAACL 2018

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| ELMo 论文首页 | arXiv | `https://arxiv.org/abs/1802.05365` | 学术引用 |

### 发生了什么？

2018 年 2 月，Peters 等人提出了 ELMo (Embeddings from Language Models)——第一个真正的上下文词表示方法。

ELMo 的做法是：
1. 在大规模语料上训练一个 2 层 BiLSTM 语言模型
2. 对每个词，取 BiLSTM 各层的隐藏状态，加权组合为最终表示
3. 同一个词在不同句子中，因为上下文不同，BiLSTM 的隐藏状态不同，所以得到不同的向量

"river bank" 中的 "bank" 和 "bank account" 中的 "bank" 终于得到了不同的向量。

### 为什么这很重要？

ELMo 证明了两件大事：
1. **上下文词表示远优于静态词向量**——在 6 个 NLP 基准上平均提升 6%
2. **语言模型的内部表示包含丰富的语言知识**——不同层捕捉不同层次的信息（底层→语法，高层→语义）

这开创了"预训练语言模型 + 下游任务"的范式。

### 但还有一个问题……

ELMo 有两个限制：
1. **浅层双向**：BiLSTM 由一个前向 LSTM 和一个后向 LSTM **独立训练**，最后拼接。它们各自看到的是"半个"上下文，并没有真正融合左右信息。
2. **基于 LSTM**：序列处理慢（不能并行），长距离依赖仍然困难。

> 🔑 **故事转折点：** 上下文嵌入有效了，但 BiLSTM 架构限制了双向融合的深度——有没有更强的架构？

---

## 📚 第三章：Transformer 降临与 GPT（2017-2018 年 6 月）

> **关键人物：** Ashish Vaswani (Google Brain) / Alec Radford (OpenAI)
> **关键论文：** [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017 + [Improving Language Understanding by Generative Pre-Training (GPT)](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), 2018

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Transformer 论文首页 | arXiv | `https://arxiv.org/abs/1706.03762` | 学术引用 |

### 发生了什么？

2017 年中，Vaswani 等人在 Google 提出了 Transformer 架构——完全基于 self-attention，不用 RNN/LSTM。Transformer 能并行处理序列中的所有位置，训练速度极快，而且 self-attention 天然擅长捕捉长距离依赖。

2018 年 6 月，OpenAI 的 Radford 等人把 Transformer 的 **Decoder** 部分拿来做预训练，提出了 GPT (Generative Pre-Training)。做法是：
1. 在大量文本上训练单向语言模型（从左到右预测下一个词）
2. 微调到下游任务

GPT 在 12 个任务中的 9 个刷新了最优记录。

### 为什么这很重要？

GPT 证明了 **Transformer + 大规模预训练 + 微调** 的范式极其强大。一个模型预训练一次，微调就能搞定各种任务。

### 但还有一个问题……

GPT 是**单向的**——它用的是 Transformer Decoder（有因果掩码），只能从左到右。但很多理解任务（分类、NER、QA）需要同时看左右上下文。一个词的含义可能完全取决于它后面的词。

> 🔑 **故事转折点：** Transformer 预训练太强了，但单向限制了它在理解任务上的表现——能不能做到"双向"？

---

## 📚 第四章：BERT 横空出世（2018 年 10 月）

> **关键人物：** Jacob Devlin (Google AI Language)
> **关键论文：** [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805), NAACL 2019

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| BERT 论文首页 | arXiv | `https://arxiv.org/abs/1810.04805` | 学术引用 |

### 发生了什么？

2018 年 10 月，Google AI 的 Jacob Devlin 等人发布了 BERT。核心创新极其优雅：

**问题：** 标准语言模型只能单向。直接做双向语言模型会让模型"偷看"到答案。

**答案：** 不做"预测下一个词"。改成**"遮住某些词，猜它们是什么"——掩码语言模型 (MLM)**。因为被遮住的词看不到自己，模型只能依赖两侧的上下文来推测，从而实现真正的深度双向融合。

BERT 还有第二个预训练任务 NSP (Next Sentence Prediction)——判断两个句子是否连续。

结果是毁灭性的：BERT 在 GLUE、MultiNLI、SQuAD v1.1、SQuAD v2.0 等 **11 个 NLP 基准上全面刷新最优**。

### 为什么这很重要？

1. **证明了双向上下文在理解任务上碾压单向**
2. **统一了微调范式**——同一架构适用于分类/序列标注/QA/NLI
3. **引发了 NLP 界的 "BERT 革命"**——之后的几年里，绝大多数 NLP 论文都基于 BERT 或其变体
4. **开源模型和代码**——学术界和工业界都能用

### 但还有一个问题……

1. NSP 是否真的有用？后来 RoBERTa 证明去掉 NSP 效果更好。
2. 80/10/10 掩码策略是启发式的，造成了预训练和微调的不一致。
3. BERT 的训练效率不高——只学 15% 被 mask 的 token，85% 的输入没有产生梯度信号。

> 🔑 **故事转折点：** BERT 改变了 NLP，但它的设计还有改进空间——BERT 家族即将扩展

---

## 📚 第五章：BERT 家族扩展（2019-2020）

> **关键人物：** Yinhan Liu (Facebook AI) / Victor Sanh (HuggingFace) / Kevin Clark (Google/Stanford)
> **关键论文：** [RoBERTa](https://arxiv.org/abs/1907.11692) / [DistilBERT](https://arxiv.org/abs/1910.01108) / [ALBERT](https://arxiv.org/abs/1909.11942) / [ELECTRA](https://arxiv.org/abs/2003.10555)

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| RoBERTa 论文首页 | arXiv | `https://arxiv.org/abs/1907.11692` | 学术引用 |
| ELECTRA 论文首页 | arXiv | `https://arxiv.org/abs/2003.10555` | 学术引用 |

### 发生了什么？

BERT 发布后，研究者从不同角度改进它：

**RoBERTa (2019.7)** — Facebook AI：
- 去掉了 NSP 任务（证明 NSP 有害无益）
- 用更多数据（160GB vs BERT 的 16GB）
- 训练更长时间
- 动态掩码（每次 epoch 重新随机 mask，而不是固定）
- 结果：在所有基准上超越 BERT

**DistilBERT (2019.10)** — HuggingFace：
- 知识蒸馏：用 BERT-Base 当"教师"，训练一个 6 层的"学生"模型
- 保留 97% 的性能，体积减小 40%，速度提升 60%
- 让 BERT 可以部署到资源受限的环境

**ALBERT (2019.9)** — Google：
- 跨层参数共享：12 层共享同一组参数
- Factorized Embedding：嵌入矩阵分解降低参数
- SOP (Sentence Order Prediction) 替代 NSP
- 12M 参数达到 BERT-Base 的效果

**ELECTRA (2020.3)** — Google/Stanford：
- 完全消除 [MASK] 不一致问题
- 用"替换 Token 检测"代替 MLM：一个小生成器生成假 token，大判别器判断每个 token 是真是假
- 所有 token 都产生梯度信号（不只是 15%），训练效率大幅提升
- 用 1/4 的计算量达到 RoBERTa 的效果

### 为什么这很重要？

BERT 家族展示了预训练语言模型的优化空间：更好的训练策略 (RoBERTa)、更小的模型 (DistilBERT/ALBERT)、更高效的训练目标 (ELECTRA)。这些工作为后续 LLM 时代奠定了基础。

### 但还有一个问题……

BERT 系列都是编码器模型，不能做生成任务。同一时期，GPT-2 和 GPT-3 的出现表明：同样的预训练思路用在解码器上，规模足够大时会涌现出令人惊叹的生成能力。NLP 的下一个时代属于大语言模型。

> 🔑 **故事转折点：** BERT 家族优化了理解，GPT 家族推进了生成——两条路线分别发展

---

## 🗺️ 全局回顾：技术演进路线图

    静态词向量时代           上下文嵌入时代           预训练模型时代
    ┌──────────┐          ┌──────────┐          ┌──────────────────────┐
    │ Word2Vec │──→──→──→│  ELMo    │──→──→──→│  GPT (单向)          │
    │ (2013)   │          │ (2018.2) │          │  (2018.6)            │
    │ GloVe    │          │ BiLSTM   │          │  Transformer Decoder │
    │ FastText │          └──────────┘          └──────────┬───────────┘
    └──────────┘                                          │
                                                          ▼
                                               ┌──────────────────────┐
                                               │  BERT (双向)          │
                                               │  (2018.10)           │
                                               │  Transformer Encoder │
                                               └──────────┬───────────┘
                                                          │
                              ┌────────────┬───────────┬──┴─────────┐
                              ▼            ▼           ▼            ▼
                        ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
                        │ RoBERTa │ │DistilBERT│ │ ALBERT   │ │ ELECTRA  │
                        │(2019.7) │ │(2019.10) │ │(2019.9)  │ │(2020.3)  │
                        │更强训练  │ │知识蒸馏  │ │参数共享  │ │替换检测  │
                        └──────────┘ └──────────┘ └──────────┘ └──────────┘

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| One-Hot → Word2Vec | 词的语义关系可以被向量空间表达 |
| Word2Vec → ELMo | 同一个词在不同语境中得到不同的表示（解决一词多义） |
| ELMo → GPT | 从 BiLSTM 升级到 Transformer，训练更快、上下文更长 |
| GPT → BERT | 从单向变成双向，理解任务大幅提升 |
| BERT → RoBERTa | 更好的训练策略（去 NSP、更多数据、动态掩码） |
| BERT → DistilBERT | 模型变小一半，性能只降 3%（知识蒸馏） |
| BERT → ALBERT | 参数从 110M 降到 12M（参数共享 + 嵌入分解） |
| BERT → ELECTRA | 训练效率提升 4 倍（所有 token 都学习，不只是 15%） |

### 🎥 视觉素材总表（视频制作用）

| 章节 | 人物 | 肖像来源 | 论文/事件图片 | 版权 |
|------|------|---------|-------------|------|
| 第一章 | Tomáš Mikolov | 大学官网 | arXiv: `1301.3781` | 学术引用 |
| 第二章 | Matthew Peters | Allen AI 官网 | arXiv: `1802.05365` | 学术引用 |
| 第三章 | Ashish Vaswani / Alec Radford | Google / OpenAI 官网 | arXiv: `1706.03762` | 学术引用 |
| 第四章 | Jacob Devlin | Google AI 官网 | arXiv: `1810.04805` | 学术引用 |
| 第五章 | Yinhan Liu / Victor Sanh | Facebook AI / HuggingFace | 各论文首页 | 学术引用 |

> ⚠️ **素材查找优先级：**
> 1. **Wikimedia Commons** — 首选，多数科学家有公有领域肖像
> 2. **大学官网/档案馆** — 本校教授的官方照片
> 3. **论文首页截图** — arXiv / Google Scholar
>
> ❌ **禁止：** AI 生成肖像、库存图片网站、无版权标注的图片
