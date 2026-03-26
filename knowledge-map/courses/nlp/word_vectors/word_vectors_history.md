---
topic: word_vectors
dimension: history
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space', ICLR 2013 — https://arxiv.org/abs/1301.3781"
  - "📖 Paper: Pennington et al., 'GloVe: Global Vectors for Word Representation', EMNLP 2014 — https://nlp.stanford.edu/pubs/glove.pdf"
  - "📖 Paper: Deerwester et al., 'Indexing by Latent Semantic Analysis', JASIS 1990 — https://doi.org/10.1002/(SICI)1097-4571(199009)41:6<391::AID-ASI1>3.0.CO;2-9"
  - "📖 Paper: Bengio et al., 'A Neural Probabilistic Language Model', JMLR 2003 — https://jmlr.org/papers/v3/bengio03a.html"
  - "📖 Paper: Peters et al., 'Deep contextualized word representations' (ELMo), NAACL 2018 — https://arxiv.org/abs/1802.05365"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: never
status: current
---

# Word Vectors 的故事线：从 One-Hot 到 Contextualized Embedding

> **核心主题：** 人类花了 60 年，从"每个词是一个孤立的符号"走到"每个词由它的邻居定义"
> **故事线：** 一个不断追问"怎样让计算机理解词义"的问题解决历程

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 计算机只认数字——怎样把"猫""狗"这样的符号变成数字，而且还要保留"猫和狗比猫和桌子更相似"这种语义关系？

1950年代，计算机开始处理语言。最朴素的做法是给每个词编一个号——"cat"=1, "dog"=2, "table"=3。但这些数字是任意的，1 和 2 并不比 1 和 3 更"接近"。语言学家 J.R. Firth 在 1957 年提出了一个影响深远的洞察："You shall know a word by the company it keeps"——一个词的意思由它经常出现的上下文决定。但这个语言学洞察要等几十年才被计算机科学真正实现。

> 🔑 **问题提出：** 如何让计算机知道"cat"和"dog"比"cat"和"airplane"更相似？离散符号无法表达连续的语义关系

---

## 📚 第一章：符号孤岛——One-Hot 编码时代（1950s-1980s）

> **关键人物：** 早期 NLP/IR 研究者
> **关键背景：** 信息检索（Information Retrieval）和早期 NLP 系统

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| 早期信息检索系统 | ACM Digital Library | `https://dl.acm.org/` | 学术引用 |

### 发生了什么？

早期的 NLP 和信息检索系统使用最直接的方法表示词：独热编码（One-Hot Encoding）。词表有 V 个词，每个词用一个 V 维向量表示，只有对应位置是 1，其余全是 0。接着出现了词袋模型（Bag of Words）——把一篇文档中所有词的独热向量加起来，得到文档级表示。TF-IDF 在此基础上加了权重：常见词（"the"）降权，罕见词升权。

### 为什么这很重要？

这些方法建立了 NLP 的计算基础——把语言从人类符号变成了机器可处理的数字。TF-IDF 至今仍是信息检索的基线方法。

### 但还有一个问题……

所有词两两正交——"cat"和"dog"的相似度与"cat"和"airplane"的相似度完全一样（都是 0）。语义信息被完全丢弃了。而且维度等于词表大小（10万+维），下游模型很难处理。

> 🔑 **故事转折点：** 1990 年，一群信息检索研究者想到：既然稀疏高维不行，能不能用矩阵分解把它降到低维？

---

## 📚 第二章：矩阵降维——LSA 与分布语义学（1990-2003）

> **关键人物：** Scott Deerwester, Susan Dumais (Bell Labs → Microsoft Research)
> **关键论文：** Deerwester et al., [Indexing by Latent Semantic Analysis](https://doi.org/10.1002/(SICI)1097-4571(199009)41:6<391::AID-ASI1>3.0.CO;2-9), JASIS 1990

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Susan Dumais 肖像 | Microsoft Research | `https://www.microsoft.com/en-us/research/people/sdumais/` | 学术引用 |
| LSA 论文首页 | Wiley Online Library | `https://doi.org/10.1002/(SICI)1097-4571(199009)41:6<391::AID-ASI1>3.0.CO;2-9` | 学术引用 |

### 发生了什么？

Deerwester 等人提出了潜在语义分析（Latent Semantic Analysis, LSA）：构建词-文档共现矩阵，然后用截断 SVD（Singular Value Decomposition）降维到 k 维（通常 100-300）。降维后的向量就是"词向量"——维度低，而且语义相近的词在低维空间中距离接近。同时期，PMI（Pointwise Mutual Information）被引入作为更好的共现权重——比原始计数更能突出"真正相关"的词对。

### 为什么这很重要？

LSA 是第一个把分布假说（Firth 1957）变成可计算方法的工作。它证明了：① 从共现统计可以自动学出语义 ② 低维表示确实能捕捉词语间的相似关系。这个思路影响了此后所有的词向量方法。

### 但还有一个问题……

SVD 的计算复杂度是 O(V² × k)——词表 10 万时矩阵已经是 100亿元素。无法在大规模语料上运行。而且 SVD 是离线批处理，每次语料更新都要重新分解整个矩阵，无法增量学习。

> 🔑 **故事转折点：** 2003 年，Bengio 提出了一个全新思路——用神经网络来学习词表示

---

## 📚 第三章：神经网络登场——Neural Language Model（2003-2012）

> **关键人物：** Yoshua Bengio (Université de Montréal, 2018 图灵奖)
> **关键论文：** Bengio et al., [A Neural Probabilistic Language Model](https://jmlr.org/papers/v3/bengio03a.html), JMLR 2003

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Yoshua Bengio 肖像 | Wikimedia Commons | `https://commons.wikimedia.org/wiki/File:Yoshua_Bengio_-_2017.jpg` | CC BY-SA 4.0 |
| Neural LM 论文首页 | JMLR | `https://jmlr.org/papers/v3/bengio03a.html` | 学术引用 |

### 发生了什么？

Bengio 等人用一个前馈神经网络来做语言建模：输入前 n-1 个词的嵌入向量（可学习的查找表），预测第 n 个词。关键创新：嵌入层的权重矩阵——一个 V×d 矩阵，每一行就是一个词的 d 维向量——是作为网络参数一起训练的。训练完语言模型后，嵌入矩阵就是词向量。

### 为什么这很重要？

这是第一次用神经网络端到端学习词的分布式表示。它证明了：① 神经网络可以同时学习词表示和语言模型 ② 学出的词向量确实编码了语义信息。但当时计算资源有限，这个方法在大语料上很慢。

### 但还有一个问题……

Bengio 的模型要在整个词表上做 Softmax（O(V) 计算），训练速度很慢。而且模型结构较深，难以在数十亿词的语料上训练。需要一个更简单、更快的方法。

> 🔑 **故事转折点：** 2013 年，Google 的 Mikolov 极大地简化了模型——去掉隐藏层，只保留嵌入层

---

## 📚 第四章：Word2Vec 革命——词嵌入的 ImageNet 时刻（2013）

> **关键人物：** Tomas Mikolov (Google → Facebook AI)
> **关键论文：** Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781), ICLR 2013; [Distributed Representations of Words and Phrases](https://arxiv.org/abs/1310.4546), NeurIPS 2013

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Tomas Mikolov | 个人学术页 | `https://scholar.google.com/citations?user=oBu8kMMAAAAJ` | 学术引用 |
| Word2Vec 论文首页 | arXiv | `https://arxiv.org/abs/1301.3781` | 学术引用 |

### 发生了什么？

Mikolov 做了一个大胆的简化：把 Bengio 的深层网络砍成只有一个线性投影层。两个变体：CBOW（上下文预测中心词）和 Skip-gram（中心词预测上下文）。同年第二篇论文引入了三个关键训练技巧：① 负采样（负样本替代全词表 Softmax，复杂度从 O(V) 降到 O(k)）② 高频词子采样（降低 "the" 等无意义高频词的影响）③ 短语检测（把 "New York" 当作一个词处理）。

### 为什么这很重要？

Word2Vec 是词嵌入蒸得 NLP 领域的"ImageNet时刻"——它让词向量变得简单、快速、强大。在单台机器上，几小时就能在数十亿词的语料上训练出高质量词向量。更令人惊叹的是词类比性质："king" - "man" + "woman" ≈ "queen"——向量空间的线性运算对应了语义关系。这个发现让整个 NLP 社区兴奋不已。

### 但还有一个问题……

Word2Vec 是逐窗口扫描语料的——它只看到局部上下文，没有利用全局共现统计。而 LSA 利用了全局信息但计算太慢。能不能把两者的优点结合起来？

> 🔑 **故事转折点：** 2014 年，Stanford NLP 组找到了一种方法，既利用全局共现，又保持 Word2Vec 的效率

---

## 📚 第五章：GloVe——全局与局部的统一（2014）

> **关键人物：** Jeffrey Pennington, Richard Socher, Christopher Manning (Stanford NLP)
> **关键论文：** Pennington et al., [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf), EMNLP 2014

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Christopher Manning 肖像 | Stanford CS | `https://nlp.stanford.edu/manning/` | 学术引用 |
| GloVe 论文首页 | Stanford NLP | `https://nlp.stanford.edu/pubs/glove.pdf` | 学术引用 |

### 发生了什么？

Pennington 等人提出 GloVe（Global Vectors）：先从语料构建全局词-词共现矩阵，然后训练词向量使得两个词的向量点积近似等于它们共现次数的对数。关键洞察：共现比值（ratio）而非绝对值包含了最有区分度的语义信息——P(solid|ice)/P(solid|steam) >> 1 说明 "solid" 和 "ice" 语义相关。

同年，Levy & Goldberg (2014) 从理论上证明了 Word2Vec 的 SGNS 其实在隐式地分解 PMI 矩阵——也就是说，Word2Vec（预测方法）和 SVD/GloVe（计数方法）在数学上是等价的！这是词嵌入理论的重要统一。

### 为什么这很重要？

GloVe 把计数方法和预测方法统一了：它显式地做了 Word2Vec 隐式在做的事。在多个基准测试上，GloVe 和 Word2Vec 效果相当，但 GloVe 的训练更可控（直接优化共现矩阵）。Stanford 公开的 GloVe 预训练向量成为学术界最广泛使用的词嵌入基准。

### 但还有一个问题……

Word2Vec 和 GloVe 都给每个词一个固定向量——"bank" 无论出现在 "river bank" 还是 "bank account" 中，都是同一个向量。一词多义怎么办？

> 🔑 **故事转折点：** 2017-2018 年，研究者开始用深层网络为每个词在每个上下文中生成不同的向量

---

## 📚 第六章：上下文嵌入——ELMo 打破静态魔咒（2018）

> **关键人物：** Matthew Peters (AI2 - Allen Institute for Artificial Intelligence)
> **关键论文：** Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365), NAACL 2018

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| ELMo 论文首页 | arXiv | `https://arxiv.org/abs/1802.05365` | 学术引用 |
| AI2 Logo | Allen Institute for AI | `https://allenai.org/` | 学术引用 |

### 发生了什么？

Peters 等人训练了一个双向 LSTM 语言模型（左到右 LM + 右到左 LM），然后把每个词在不同层的隐藏状态加权组合，得到上下文相关的词表示——同一个词 "bank" 在 "river bank" 和 "bank account" 中会得到完全不同的向量。他们把这个方法叫做 ELMo（Embeddings from Language Models）。

### 为什么这很重要？

ELMo 打破了"一词一向量"的魔咒。在 6 个 NLP 基准任务上平均提升 25% 以上。更重要的是，它建立了 "pretrain + fine-tune" 的范式：先在大语料上预训练语言模型，再在特定任务上微调。这个范式直接催生了 BERT 和 GPT。

### 但还有一个问题……

ELMo 基于 LSTM——仍有顺序计算的瓶颈，无法高效并行。而且 LSTM 的"上下文窗口"受限于梯度消失，看不了太远。需要一种更强大、更可并行化的架构……

> 🔑 **故事转折点：** 2017 年 Transformer 的出现 + 2018年 BERT/GPT 的"大爆炸"——词表示的故事在这里收尾，下一章是 Transformer 和预训练模型的故事

---

## 🗺️ 全局回顾：技术演进路线图

```
1957: 分布假说 (Firth)
       │
1990: LSA/SVD ── 计数 + 矩阵分解 → 第一代稠密词向量
       │                                      │
2003: Neural LM (Bengio) ── 神经网络学嵌入      │ ← Levy & Goldberg 2014:
       │                                      │    两者数学等价!
2013: Word2Vec (Mikolov) ── 极简模型 + 负采样   │
       │                                      │
2014: GloVe (Pennington) ── 全局统计 + 预测 ──┘
       │
2017: FastText (Bojanowski) ── 子词 n-gram, 解决 OOV
       │
2018: ELMo (Peters) ── 上下文相关嵌入 (双向 LSTM)
       │
2018: BERT (Devlin) + GPT (Radford) ── Transformer 上下文嵌入
       └──→ 词向量时代结束，进入预训练语言模型时代
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| One-Hot → LSA/SVD | 从稀疏正交 → 稠密低维，捕捉语义相似性 |
| LSA → Neural LM | 从离线矩阵分解 → 在线端到端学习，可扩展 |
| Neural LM → Word2Vec | 从深层网络 → 极简架构 + 负采样，训练快 100 倍 |
| Word2Vec → GloVe | 从局部窗口 → 全局共现统计，理论统一 |
| GloVe → FastText | 从整词 → 子词 n-gram，解决 OOV |
| FastText → ELMo | 从静态一词一向量 → 上下文相关，解决一词多义 |
| ELMo → BERT/GPT | 从 LSTM → Transformer，更强更快更深 |

### 🎥 视觉素材总表（视频制作用）

| 章节 | 人物 | 肖像来源 | 论文/事件图片 | 版权 |
|------|------|---------|-------------|------|
| 第二章 | Susan Dumais | Microsoft Research 官网 | LSA 论文 (Wiley) | 学术引用 |
| 第三章 | Yoshua Bengio | Wikimedia Commons: `File:Yoshua_Bengio_-_2017.jpg` | JMLR 论文 | CC BY-SA 4.0 |
| 第四章 | Tomas Mikolov | Google Scholar | arXiv: 1301.3781 | 学术引用 |
| 第五章 | Christopher Manning | Stanford NLP 官网 | Stanford NLP GloVe 页面 | 学术引用 |
| 第六章 | Matthew Peters | AI2 官网 | arXiv: 1802.05365 | 学术引用 |

> ⚠️ **素材查找优先级：**
> 1. **Wikimedia Commons** — 首选，多数科学家有公有领域肖像
> 2. **大学官网/档案馆** — 本校教授的官方照片
> 3. **论文首页截图** — arXiv / Google Scholar
>
> ❌ **禁止：** AI 生成肖像、库存图片网站、无版权标注的图片
