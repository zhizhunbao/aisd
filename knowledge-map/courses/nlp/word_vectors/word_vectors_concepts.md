---
topic: word_vectors
dimension: concepts
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space', ICLR 2013 — https://arxiv.org/abs/1301.3781"
  - "📖 Paper: Mikolov et al., 'Distributed Representations of Words and Phrases', NeurIPS 2013 — https://arxiv.org/abs/1310.4546"
  - "📖 Paper: Pennington et al., 'GloVe: Global Vectors for Word Representation', EMNLP 2014 — https://nlp.stanford.edu/pubs/glove.pdf"
  - "📖 Paper: Bojanowski et al., 'Enriching Word Vectors with Subword Information', TACL 2017 — https://arxiv.org/abs/1607.04606"
  - "📖 Paper: Peters et al., 'Deep contextualized word representations' (ELMo), NAACL 2018 — https://arxiv.org/abs/1802.05365"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》, Ch.12 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Word Vectors 核心概念

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 "Vector Semantics and Embeddings"
> 📖 Paper: Mikolov et al., [Efficient Estimation of Word Representations](https://arxiv.org/abs/1301.3781), ICLR 2013

---

## 术语定义

### 分布假说 (Distributional Hypothesis)

语言学中最重要的假设之一：一个词的意思由它经常出现的上下文决定。用 J.R. Firth (1957) 的原话说："You shall know a word by the company it keeps"（你可以通过一个词的伙伴来了解它）。举例："医生"这个词经常和"病人""诊断""治疗"一起出现，所以我们可以从这些上下文推断"医生"的含义。Word2Vec 和 GloVe 的全部理论基础就是这个假设——通过统计词的共现模式来学习词义。

> 别名：**Distributional Semantics**（来自语言学领域）——"分布假说"是原则，"分布语义学"是基于该原则的研究方向

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.3
> 📖 Paper: Firth, J.R. "A Synopsis of Linguistic Theory 1930-1955" (1957)

### 独热编码 (One-Hot Encoding)

最朴素的词表示方法：词表大小为 V，每个词用一个 V 维向量表示，该词对应位置为 1，其余全为 0。例如词表 [cat, dog, fish] 中，"dog" = [0, 1, 0]。问题非常明显：① 维度太高（V 通常 10 万+），② 所有词两两正交（任意两个独热向量的余弦相似度为 0），完全无法表达"cat"和"dog"比"cat"和"fish"更相似这种语义关系。

> 易混淆：**词袋模型 (Bag of Words)** — One-Hot 是单个词的表示，BoW 是把一篇文档中所有词的 One-Hot 加起来（或计数），得到文档级表示，忽略了词序

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.2

### 词嵌入 (Word Embedding)

把每个词映射成一个稠密的、低维的实数向量（通常 50-300 维），让语义相近的词在向量空间中距离相近。"嵌入"这个名字来自数学——把离散对象（词）嵌入（embed）到连续的向量空间中。和 One-Hot 相比，词嵌入的每个维度不再对应某个特定词，而是编码了某种"潜在语义特征"（latent semantic feature），比如某个维度可能编码"是否是动物""是否是正面情感"等。

> 别名：**Distributed Representation**（来自 Hinton 1986）/ **Dense Vector**（与 Sparse Vector 对比）——"分布式表示"强调信息分散在多个维度上（而非 One-Hot 的单个维度），"稠密向量"强调大多数元素非零

> 易混淆：**Embedding vs Encoding** — Embedding 是学习到的表示（可训练参数），Encoding 是确定性函数的输出（如 One-Hot, Positional Encoding）

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.4
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.12 §12.4

### Word2Vec

Mikolov 等人于 2013 年提出的词嵌入学习框架，包含两种架构：CBOW（Continuous Bag of Words）和 Skip-gram。核心思想：训练一个浅层神经网络（只有一个隐藏层），通过上下文来预测词（或反过来），预测任务产生的权重矩阵就是词向量。Word2Vec 不是单一算法，而是一个框架，包括模型架构（CBOW/Skip-gram）+ 训练技巧（负采样/层次 Softmax/子采样）。

> 📖 Paper: Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781), ICLR 2013

### CBOW (Continuous Bag of Words)

Word2Vec 的两种架构之一。给定一个目标词的上下文窗口内的所有周围词，预测中间的目标词。例如上下文为 "the cat ___ on the"，预测中间词 "sat"。做法是把上下文词的嵌入求平均，然后通过一个线性层预测目标词。CBOW 对高频词效果更好（因为高频词有更多上下文样本），训练速度比 Skip-gram 快。

> 易混淆：**CBOW vs Skip-gram** — CBOW 用上下文预测中心词（多对一），Skip-gram 用中心词预测上下文（一对多）。经验上 Skip-gram 对低频词和小数据集效果更好

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §3.1

### Skip-gram

Word2Vec 的两种架构之一。给定一个中心词，预测其上下文窗口内的每个周围词。例如给定中心词 "sat"，分别预测 "the""cat""on""the" 四个上下文词。每个 (中心词, 上下文词) 构成一个正样本。Skip-gram 对低频词和小语料库效果更好（每个词能产生多个训练样本），是 Word2Vec 最常用的变体。

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §3.2

### 负采样 (Negative Sampling)

Word2Vec 的关键训练技巧。原始 Skip-gram 需要在整个词表（V 个词）上做 Softmax 归一化，计算量 O(V) 太大。负采样的思路：不算全词表概率，改成二分类问题——对于每个正样本 (中心词, 真正上下文词)，随机采样 k 个"噪声词"作为负样本，只训练 (1+k) 个词的参数。负例采样概率按词频的 3/4 次方分布（p(w) ∝ f(w)^{3/4}），既不完全按词频（否则高频词太多），也不完全均匀（否则低频词太多）。

> 别名：**NEG** / **SGNS (Skip-gram with Negative Sampling)**——SGNS 特指 Skip-gram + 负采样组合

> 📖 Paper: Mikolov et al., [Distributed Representations of Words and Phrases](https://arxiv.org/abs/1310.4546), §2.2

### GloVe (Global Vectors for Word Representation)

Pennington 等人于 2014 年提出的词嵌入方法。GloVe 先从语料库构建全局的词-词共现矩阵 X（X_ij = 词 i 和词 j 在窗口内共现的次数），然后训练词向量使得两个词向量的点积近似等于它们共现次数的对数：w_i · w_j + b_i + b_j ≈ log(X_ij)。核心洞察：Word2Vec 隐式地分解了 PMI 矩阵（Levy & Goldberg 2014 证明），GloVe 显式地这样做，结合了计数方法和预测方法的优点。

> 📖 Paper: Pennington et al., [GloVe (2014)](https://nlp.stanford.edu/pubs/glove.pdf), §2-3

### FastText

Bojanowski 等人于 2017 年提出的 Word2Vec 扩展。核心改进：把每个词拆成字符 n-gram（如 "where" → "<wh", "whe", "her", "ere", "re>"，加上特殊边界标记 < 和 >），每个 n-gram 有自己的向量，一个词的向量是其所有字符 n-gram 向量的和。关键优势：① 能处理未登录词 (OOV)——从未见过的词只要包含已知 n-gram 就能计算向量，② 对形态丰富的语言（如土耳其语、芬兰语）效果显著提升。

> 易混淆：**FastText vs Word2Vec** — FastText 是 Word2Vec 的扩展（仍用 Skip-gram + 负采样），核心区别在于词的表示从"整词"变成了"子词 n-gram 求和"

> 📖 Paper: Bojanowski et al., [Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606), §2-3

### ELMo (Embeddings from Language Models)

Peters 等人于 2018 年提出的上下文相关词嵌入。核心思想：用一个双向 LSTM 语言模型（前向 LM + 后向 LM），将每个词在不同层的隐藏状态加权组合，得到该词在特定上下文下的表示。关键突破：同一个词 "bank" 在 "river bank" 和 "bank account" 中会得到不同的向量，解决了静态嵌入的一词多义问题。ELMo 是从 Word2Vec（静态嵌入）到 BERT/GPT（Transformer 上下文嵌入）的过渡桥梁。

> 别名：**Contextualized Word Embedding**（来自 NLP 社区）——ELMo 是第一个被广泛使用的上下文嵌入方法

> 📖 Paper: Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365), NAACL 2018

### 余弦相似度 (Cosine Similarity)

衡量两个词向量语义相似度的标准方法。公式：cos(u, v) = (u · v) / (||u|| × ||v||)，值域 [-1, 1]。只看向量方向不看长度——两个向量完全同向为 1，完全反向为 -1，正交为 0。在词向量空间中，cos(vec("king"), vec("queen")) ≈ 0.75，cos(vec("king"), vec("apple")) ≈ 0.15。比欧氏距离更适合高维稀疏空间（不受向量尺度影响）。

> 易混淆：**余弦相似度 vs 余弦距离** — 余弦距离 = 1 - 余弦相似度，相似度高则距离小

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.4

### 词类比 (Word Analogy)

Word2Vec 最著名的特性："king" - "man" + "woman" ≈ "queen"。向量空间中的线性关系对应语义关系——性别维度上 vec(king)-vec(queen) ≈ vec(man)-vec(woman)。类比任务用来评估词向量质量：给定 a:b::c:?，找 v = vec(b) - vec(a) + vec(c)，然后找和 v 余弦最近的词作为答案。但要注意：类比关系并非总是成立，特别是在偏见（bias）和低频词场景下。

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §4 "Results"
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.10

### TF-IDF (Term Frequency-Inverse Document Frequency)

经典的稀疏向量权重方案。一个词在文档中的重要性 = TF（词频：该词在本文档出现的次数）× IDF（逆文档频率：log(总文档数/包含该词的文档数)）。直觉：如果一个词在某篇文档中出现很多次（高 TF），但在其他文档中很少出现（高 IDF），那它对这篇文档很有标志性。"the"虽然 TF 高，但 IDF 极低（几乎所有文档都有），所以 TF-IDF 权重低。

> 别名：**tf.idf** / **tf-idf**——大小写和连接符在不同文献中不一致，含义相同

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.5

### 共现矩阵 (Co-occurrence Matrix)

统计词与词在某个窗口内同时出现的次数，构建一个 V×V 矩阵（V 为词表大小）。X_ij = 词 i 和词 j 在所有窗口中共现的总次数。GloVe 直接在共现矩阵上训练。共现矩阵也可以用 SVD（截断奇异值分解）降到低维来获得词向量——这是最早的稠密词向量方法（Latent Semantic Analysis, LSA）。

> 别名：**Term-Context Matrix** / **Word-Word Matrix**（来自信息检索领域）——不同文献对同一矩阵起了不同名字，核心都是统计共现

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.6

### 上下文窗口 (Context Window)

定义一个词的"上下文"的滑动窗口大小。例如窗口大小 w=2，目标词 "sat" 在句子 "the cat sat on the mat" 中的上下文为 {the, cat, on, the}（前后各取 2 个词）。窗口大小对词向量性质影响很大：小窗口（w=1-2）学到的是语法/句法关系（名词、动词），大窗口（w=5-10）学到的是语义/主题关系（同主题词）。

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.3

---

## 概念辨析

### 静态嵌入 (Static Embedding) vs 上下文嵌入 (Contextualized Embedding)

| 维度 | 静态嵌入 | 上下文嵌入 |
|------|---------|-----------|
| **本质** | 每个词一个固定向量，与上下文无关 | 每个词的向量随上下文变化 |
| **代表方法** | Word2Vec, GloVe, FastText | ELMo, BERT, GPT |
| **一词多义** | ❌ 无法区分（"bank" 永远是同一个向量） | ✅ 自然处理（"river bank" ≠ "bank account"） |
| **计算成本** | 极低（查表操作） | 高（需要前向推理） |
| **训练数据需求** | 中等（Wikipedia 级别即可） | 大（Transformer 需要大规模语料） |
| **典型维度** | 50-300 | 768-1024 |

> 📖 Paper: Peters et al., [ELMo (2018)](https://arxiv.org/abs/1802.05365), §1
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.12

### 基于计数 (Count-Based) vs 基于预测 (Prediction-Based)

| 维度 | 基于计数 | 基于预测 |
|------|---------|---------|
| **核心做法** | 构建共现矩阵 → 降维（SVD/GloVe） | 训练神经网络预测上下文（Word2Vec） |
| **代表方法** | LSA, PPMI, GloVe | Word2Vec (CBOW/Skip-gram), FastText |
| **利用的统计信息** | 全局共现计数 | 局部上下文窗口 |
| **训练方式** | 矩阵分解 | SGD 在线训练 |
| **理论联系** | Levy & Goldberg (2014) 证明 SGNS 隐式分解了 PMI 矩阵——两者数学上等价 |

> 📖 Paper: Levy & Goldberg, [Neural Word Embedding as Implicit Matrix Factorization](https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html), NeurIPS 2014
> 📖 Paper: Pennington et al., [GloVe (2014)](https://nlp.stanford.edu/pubs/glove.pdf), §2

### CBOW vs Skip-gram

| 维度 | CBOW | Skip-gram |
|------|------|-----------|
| **输入 → 输出** | 上下文词 → 中心词（多对一） | 中心词 → 上下文词（一对多） |
| **训练速度** | 更快（每个窗口一个预测） | 更慢（每个窗口多个预测） |
| **高频词** | 效果好（更多样本求平均） | 一般 |
| **低频词 / 小语料** | 一般 | 效果好（每个词产生多个训练对） |
| **实际使用** | 较少使用 | Word2Vec 默认推荐 |

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §3

---

## 核心属性

### 信息架构

```
词表示方法的谱系

稀疏表示 (Sparse)                   稠密表示 (Dense)
┌───────────────────────┐           ┌──────────────────────────────────┐
│                       │           │                                  │
│  One-Hot Encoding     │           │  基于计数                        │
│  (V 维, 只有一个 1)    │           │  ├── SVD on Co-occurrence (LSA)  │
│                       │           │  └── GloVe (加权矩阵分解)        │
│  Bag of Words         │           │                                  │
│  (V 维, 词频计数)      │           │  基于预测                        │
│                       │           │  ├── Word2Vec CBOW               │
│  TF-IDF               │           │  ├── Word2Vec Skip-gram          │
│  (V 维, 加权)          │           │  └── FastText (子词 n-gram)      │
│                       │           │                                  │
└───────────────────────┘           │  上下文相关                       │
                                    │  ├── ELMo (双向 LSTM)            │
                                    │  ├── BERT (Transformer Encoder)  │
                                    │  └── GPT (Transformer Decoder)   │
                                    │                                  │
                                    └──────────────────────────────────┘
```

### 适用场景 ✅

- 文本分类 / 情感分析的特征输入
- 信息检索和语义搜索
- 词相似度和词类比任务
- 下游 NLP 模型的初始化嵌入层
- 资源受限场景（预训练静态向量体积小、推理快）
- 可视化词语关系（t-SNE / PCA 降维可视化）

### 不适用场景 ❌

- 需要区分一词多义的任务——静态嵌入无法处理
- 句子/文档级语义理解——词向量需要额外的组合机制（求平均太粗糙）
- 高度专业化领域——预训练词向量基于通用语料，医学/法律等领域可能不准
- 动态词表场景——词表固定，新词必须重新训练（FastText 可部分缓解）

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §4
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 典型维度 | 词向量维度 | 100 / 200 / 300 |
| 词表大小 | 常见预训练模型 | 40 万 (GloVe-6B) / 200 万 (FastText) |
| 训练语料 | Word2Vec Google News / GloVe | 1000 亿词 / 60 亿词 |
| 窗口大小 | Skip-gram 上下文窗口 | 5 (常用) / 2-10 (可调) |
| 负采样数 | Skip-gram 负例个数 | k=5 (大语料) / k=15 (小语料) |
| 采样分布 | 负采样的词频分布 | p(w) ∝ f(w)^{3/4} |
| 最小词频 | 过滤低频词阈值 | min_count=5 |
| 子采样阈值 | 高频词下采样 | t = 10⁻⁵ |
| 相似度度量 | 标准方法 | 余弦相似度 cos(u,v) |
| 类比公式 | a:b::c:? | vec(b) - vec(a) + vec(c) |
| 预训练下载 | GloVe 官方 | nlp.stanford.edu/projects/glove/ |

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6
> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), Table 1
