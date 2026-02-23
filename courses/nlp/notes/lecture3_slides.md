# Week 3: 文本向量化与相似度 (Text Vectorization & Similarity)

> Source: `lecture_3_W26.pdf`
> Total slides: 48
> Instructor: Hala Own, Ph.D.

---

## 1. 课程议程 (Lesson Agenda)

![Page 1](lecture3_slides_pages/page_001.png)

**CST8507: Natural Language Processing — Lecture #3: Text Vectorization & Similarity** — CST8507自然语言处理，第3讲：文本向量化与相似度

![Page 2](lecture3_slides_pages/page_002.png)

**Lesson Agenda:** — 本节课议程：

- ❑Assignment 1 & Lab — 作业1和实验
- ❑Introduction to Feature representation — 特征表示概述
- ❑Text representation techniques — 文本表示技术
  - ❑ One-Hot Encoding — 独热编码
  - ❑ Bag of Words model — 词袋模型
  - ❑ Bag of N-Grams model — N元词袋模型
  - ❑ TF-IDF model — TF-IDF模型
- ❑ Word similarity — 词语相似度

---

## 2. NLP开发生命周期 (NLP Development Life Cycle)

![Page 3](lecture3_slides_pages/page_003.png)

**NLP Development Life Cycle:** Circular pipeline diagram — 8 stages looping: Requirements gathering → Data collection → Text preprocessing → Feature extraction → Model building → Evaluation → Deployment → Gather more data / Improve the model. — NLP开发生命周期循环流程图——8个阶段：需求收集→数据收集→文本预处理→特征提取→模型构建→评估→部署→收集更多数据/改进模型。

---

## 3. 特征表示 (Feature Representation)

![Page 4](lecture3_slides_pages/page_004.png)

**Feature Representation:** Three-column diagram showing each data modality (speech, image, text) maps to its own representation form. — 三列示意图，展示语音、图像、文本三种数据模态各自对应不同的表示形式。

![Page 5](lecture3_slides_pages/page_005.png)

**Text Representation Techniques:** Taxonomy tree from traditional sparse methods (One-Hot, BOW, N-Gram, TF-IDF) to modern dense neural embeddings (Word2Vec, GloVe, FastText, BERT). — 文本表示方法全景树状图：从传统稀疏方法（One-Hot/BOW/N-Gram/TF-IDF）到现代稠密神经嵌入（Word2Vec/GloVe/FastText/BERT）。

Ref: An automated approach to aspect-based sentiment analysis of apps reviews using machine and deep learning, September 2023, Automated Software Engineering

> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Bridge from text to math (从文本到数学的桥梁):**
>
> Machine learning models operate on numbers, not words. Feature representation is the critical bridge that converts human-readable text into machine-processable numerical vectors. Without this step, no ML/DL model can process text.
>
> > 机器学习模型操作的是数字而不是文字。特征表示是将人类可读文本转换为机器可处理数值向量的关键桥梁。没有这一步，任何ML/DL模型都无法处理文本。
>
> **(2) Representation determines model ceiling (表示方式决定模型天花板):**
>
> The quality of your text representation directly limits your model's performance. A sophisticated model with poor representations will underperform a simple model with excellent representations. This lecture covers the "traditional" methods — neural methods (Word2Vec, BERT) come later.
>
> > 文本表示的质量直接限制了模型的性能上限。用差的表示方法搭配复杂模型，效果不如用好的表示方法搭配简单模型。本讲覆盖"传统"方法——神经方法（Word2Vec、BERT）后面会讲。
>
> **💡 Intuition:**
> **(1) Evolution from dumb to smart (从笨到聪明的进化):**
>
> Think of text representation as a spectrum: One-Hot ("is this word present?") → BOW ("how many times?") → N-Gram ("what pairs/triples appear?") → TF-IDF ("how important is this word?") → Word2Vec/BERT ("what does this word mean?"). Each step captures more semantic information.
>
> > 把文本表示想象成一个光谱：独热编码（"这个词出现了吗？"）→ 词袋（"出现了几次？"）→ N-Gram（"什么词对/三元组出现了？"）→ TF-IDF（"这个词有多重要？"）→ Word2Vec/BERT（"这个词是什么意思？"）。每一步都捕获更多语义信息。
>
> **⚖️ Compare:**
> **(1) Traditional vs Neural representations (传统方法 vs 神经方法):**
>
> | Feature           | Traditional (This Lecture) | Neural (Later Lectures)  |
> | ----------------- | -------------------------- | ------------------------ |
> | Captures meaning? | No (frequency-based)       | Yes (learned embeddings) |
> | Sparse?           | Yes (mostly zeros)         | No (dense vectors)       |
> | Fixed dimension?  | Vocabulary size            | Configurable (100-768)   |
> | OOV handling?     | Cannot handle              | Sub-word tokenization    |
>
> > | 特性       | 传统方法（本讲） | 神经方法（后续）  |
> > | ---------- | ---------------- | ----------------- |
> > | 捕获语义？ | 否（基于频率）   | 是（学习的嵌入）  |
> > | 稀疏？     | 是（大部分为零） | 否（稠密向量）    |
> > | 固定维度？ | 词表大小         | 可配置（100-768） |
> > | OOV处理？  | 无法处理         | 子词分词          |
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "Why do we need feature representation in NLP?" → ML models require numerical input; text must be converted to vectors. The representation quality determines the model's performance ceiling.
>
> > "为什么NLP需要特征表示？" → ML模型需要数值输入；文本必须转换为向量。表示质量决定模型性能上限。

---

## 4. 向量空间模型 (Vector Space Model)

### 4.1 概念介绍 (Concept Introduction)

![Page 6](lecture3_slides_pages/page_006.png)

**Vector Space Model:** Mathematical model that represents text as numeric vectors in high-dimensional space; similar words end up "nearby." — 数学模型，将文本表示为高维空间中的数值向量；语义相似的词在空间中距离相近。

- Mathematical and algebraic model transforming and representing text document in numeric vector. — 数学和代数模型，将文本文档转换并表示为数值向量。
- Each word = vector — 每个词 = 向量
- Similar words are "nearby in semantic space" — 相似的词在"语义空间中靠近"

### 4.2 向量基础 (Vector Basics)

![Page 7](lecture3_slides_pages/page_007.png)

**Vectors: An introduction:** Slide introducing vectors as objects with both magnitude and direction. — 向量简介：向量是同时具有大小（模）和方向的数学对象。

- A vector is an object that has both a magnitude and a direction. — 向量是同时具有大小和方向的对象。

![Page 8](lecture3_slides_pages/page_008.png)

**Vectors: An introduction (continued):** Formulas for vector length (L₂ norm) and inner product (dot product) in n-dimensional space. — 续：n维空间中向量长度（L₂范数）和内积（点积）的公式推导。

- x = (x₁, x₂, x₃, ..., xₙ) is a vector in an n-dimensional vector space — x = (x₁, x₂, x₃, ..., xₙ) 是n维向量空间中的一个向量
- Length of x is given by (extension of Pythagoras's theorem): — x的长度由（勾股定理的推广）给出：
  - |x|² = x₁² + x₂² + x₃² + ... + xₙ²
  - |x| = √(x₁² + x₂² + x₃² + ... + xₙ²) (L₂ Norm / L₂范数)
- If x₁ and x₂ are vectors: — 如果x₁和x₂是向量：
  - Inner product (or dot product) is given by: x₁·x₂ = x₁₁x₂₁ + x₁₂x₂₂ + x₁₃x₂₃ + ... + x₁ₙx₂ₙ — 内积（或点积）为：x₁·x₂ = x₁₁x₂₁ + x₁₂x₂₂ + x₁₃x₂₃ + ... + x₁ₙx₂ₙ

### 4.3 文本向量化 (Text Vectorizing)

![Page 9](lecture3_slides_pages/page_009.png)

**Text Vectorizing:** Defines vectorizing (encoding text as integers) and feature vector (n-dimensional numerical representation of a text). — 定义向量化（将文本编码为整数）和特征向量（文本的n维数值表示）。

- **Vectorizing:** Process of encoding text as integers to create feature vectors. — **向量化：** 将文本编码为整数以创建特征向量的过程。
- **Feature Vector:** n-dimensional vector of numerical features that represent a text object. — **特征向量：** 表示文本对象的n维数值特征向量。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Vector Space Model — VSM (向量空间模型):**
>
> A mathematical framework that represents text documents as vectors in a multi-dimensional space where each dimension corresponds to a unique word in the vocabulary. Two documents' similarity can then be computed using geometric operations (dot product, cosine angle).
>
> > 一种数学框架，将文本文档表示为多维空间中的向量，其中每个维度对应词表中的一个唯一词。然后可以使用几何运算（点积、余弦角）计算两个文档的相似度。
>
> **(2) Key math operations (关键数学运算):**
>
> L₂ Norm (magnitude): ‖x‖ = √(Σxᵢ²) measures vector length. Dot product: x·y = Σxᵢyᵢ measures "how much two vectors point in the same direction." These two operations form the foundation of cosine similarity (covered in §9).
>
> > L₂范数（模）：‖x‖ = √(Σxᵢ²) 衡量向量长度。点积：x·y = Σxᵢyᵢ 衡量"两个向量指向同一方向的程度"。这两个运算构成余弦相似度的基础（见§9）。
>
> **🎯 Why:**
> **(1) Geometric thinking enables similarity (几何思维实现相似度计算):**
>
> Once text is a vector, all of linear algebra becomes available: distance = dissimilarity, angle = semantic closeness, projection = shared meaning. This is WHY we transform text — to leverage centuries of mathematical tools.
>
> > 一旦文本变成向量，所有线性代数工具都可用了：距离=不相似度，角度=语义亲近度，投影=共有含义。这就是我们为什么要转换文本——利用几个世纪的数学工具。
>
> **💡 Intuition:**
> **(1) Map analogy (地图类比):**
>
> Imagine each word is a city on a map. Words with similar meanings are close together ("happy" near "joyful"), while unrelated words are far apart ("happy" far from "database"). VSM builds this "word map" using frequency patterns.
>
> > 想象每个词是地图上的一个城市。含义相似的词靠在一起（"happy"靠近"joyful"），不相关的词距离较远（"happy"远离"database"）。VSM通过频率模式构建这张"词汇地图"。
>
> **⚠️ Pitfall:**
> **(1) High dimensionality curse (高维诅咒):**
>
> In VSM, each unique word is a dimension. A corpus with 100,000 unique words creates 100,000-dimensional vectors that are mostly zeros (sparse). This wastes memory and computation — motivating dimensionality reduction techniques like TF-IDF weighting and later, dense embeddings.
>
> > 在VSM中，每个唯一词是一个维度。有100,000个唯一词的语料库创建100,000维的向量，且大部分为零（稀疏）。这浪费内存和计算——推动了降维技术如TF-IDF加权，以及后来的稠密嵌入。
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> "Given vectors a=[1,2,3] and b=[4,5,6], compute the dot product." → a·b = 1×4 + 2×5 + 3×6 = 4+10+18 = 32.
>
> > "给定向量a=[1,2,3]和b=[4,5,6]，计算点积。" → a·b = 1×4 + 2×5 + 3×6 = 4+10+18 = 32。
>
> **(2) 概念题 (Conceptual):**
>
> "What is a feature vector?" → An n-dimensional vector of numerical features that represents a text object, where each dimension corresponds to a vocabulary term.
>
> > "什么是特征向量？" → 表示文本对象的n维数值特征向量，其中每个维度对应一个词表术语。

---

## 5. 独热编码 (One-Hot Encoding)

![Page 10](lecture3_slides_pages/page_010.png)

**Text Representation: One-Hot Encoding:** Shows tokenization of "This is an example" into 4 words, then encoding each word as a 4-dim binary vector with exactly one 1. — 展示将"This is an example"分词为4词，每个词用一个4维二进制向量表示，只有对应位为1。

- Each unique word in a text converts into a binary vector. — 文本中的每个唯一词都转换为二进制向量。
- Only one element is "hot" (set to 1) and all others are "cold" (set to 0), indicating the presence of that word. — 只有一个元素是"热的"（设为1），其余都是"冷的"（设为0），表示该词是否出现。
- "This is an example"
  - Split Text Into Words (Tokenization): ['This','is','an','example'] — 将文本分割成词（分词）：['This','is','an','example']
  - Numerically Encode Words (One-Hot Encoding): — 数值编码词（独热编码）：
    - This → [1,0,0,0]
    - is → [0,1,0,0]
    - an → [0,0,1,0]
    - example → [0,0,0,1]

![Page 11](lecture3_slides_pages/page_011.png)

**One-Hot Encoding for Documents:** Vocabulary × Documents matrix where each row is a one-hot vector and each column represents one document. — 词表×文档矩阵，每行是一个独热向量，每列代表一个文档。

![Page 12](lecture3_slides_pages/page_012.png)

**One-Hot Encoding — Discussion:** Slide summarizing pros and cons: simple but sparse, no semantic relationships, high dimensionality. — 总结优缺点：简单直观，但稀疏、无语义关系、高维度。

> **📝 Notes:**
>
> **📌 What:**
> **(1) One-Hot Encoding — OHE (独热编码):**
>
> Each unique word in the vocabulary gets its own dimension. A word is represented as a binary vector with a single 1 at its position index and 0s everywhere else. Vocabulary size = vector dimension.
>
> > 词表中每个唯一词获得自己的维度。一个词被表示为一个二进制向量，在其位置索引处为1，其余全为0。词表大小=向量维度。
>
> **🎯 Why:**
> **(1) Simplest form of numerical representation (最简单的数值表示形式):**
>
> OHE is the most basic way to convert categorical data (words) into numbers. It's the "hello world" of text representation — simple enough to understand and implement, but limited. Understanding its weaknesses motivates learning BOW, TF-IDF, and embeddings.
>
> > OHE是将分类数据（词）转换为数字的最基本方式。它是文本表示的"hello world"——简单到可以理解和实现，但能力有限。理解它的弱点推动了学习BOW、TF-IDF和嵌入。
>
> **💡 Intuition:**
> **(1) Light switch analogy (灯光开关类比):**
>
> Imagine a room with 10,000 light switches (one per word in your vocabulary). For each word, you flip ONE switch ON and leave all others OFF. This is extremely wasteful — 9,999 switches are always off! And two words like "happy" and "glad" have NO relationship in their switch patterns.
>
> > 想象一个有10,000个灯光开关的房间（每个词一个）。对于每个词，你打开一个开关，其余全部关闭。这极其浪费——9,999个开关总是关着的！而且"happy"和"glad"两个词的开关模式之间没有任何关系。
>
> **⚖️ Compare:**
> **(1) OHE vs BOW vs TF-IDF:**
>
> | Feature             | One-Hot Encoding          | BOW                          | TF-IDF                       |
> | ------------------- | ------------------------- | ---------------------------- | ---------------------------- |
> | Values              | 0 or 1 (binary)           | Integer counts               | Weighted floats              |
> | Per-word?           | Yes (one vector per word) | No (one vector per document) | No (one vector per document) |
> | Captures frequency? | No                        | Yes                          | Yes (weighted)               |
> | Semantic info?      | None                      | None                         | Slightly (via rarity)        |
>
> > | 特性       | 独热编码           | 词袋                 | TF-IDF               |
> > | ---------- | ------------------ | -------------------- | -------------------- |
> > | 值         | 0或1（二进制）     | 整数计数             | 加权浮点数           |
> > | 每个词？   | 是（每词一个向量） | 否（每文档一个向量） | 否（每文档一个向量） |
> > | 捕获频率？ | 否                 | 是                   | 是（加权）           |
> > | 语义信息？ | 无                 | 无                   | 略有（通过稀有度）   |
>
> **⚠️ Pitfall:**
> **(1) No semantic relationships (无语义关系):**
>
> OHE treats every word as equally different from every other word. The distance between "cat" and "dog" is the same as between "cat" and "quantum" — there is zero notion of meaning or similarity. This is the fundamental limitation that later methods try to fix.
>
> > OHE将每个词视为与其他所有词等距。"cat"和"dog"之间的距离与"cat"和"quantum"之间的距离相同——完全没有含义或相似性的概念。这是后续方法试图解决的根本局限。
>
> **(2) Curse of dimensionality (维度灾难):**
>
> If your vocabulary has 50,000 words, each vector has 50,000 dimensions with only ONE non-zero entry. This extreme sparsity wastes memory and makes distance calculations meaningless (all vectors are equidistant in Euclidean space!).
>
> > 如果词表有50,000个词，每个向量有50,000个维度但只有一个非零项。这种极端稀疏浪费内存，并使距离计算失去意义（所有向量在欧几里得空间中等距!）。
>
> **📝 Exam:**
> **(1) 编码题 (Encoding):**
>
> "Encode the sentence 'I love NLP' using one-hot encoding." → Vocabulary: {I, love, NLP}. I=[1,0,0], love=[0,1,0], NLP=[0,0,1].
>
> > "用独热编码编码句子'I love NLP'。" → 词表：{I, love, NLP}。I=[1,0,0], love=[0,1,0], NLP=[0,0,1]。
>
> **(2) 概念题 (Conceptual):**
>
> "What is the main disadvantage of one-hot encoding?" → It cannot capture semantic relationships between words; all words are equally distant from each other. Also, very high dimensionality for large vocabularies.
>
> > "独热编码的主要缺点是什么？" → 它无法捕获词之间的语义关系；所有词彼此等距。此外，大词表会导致极高的维度。

---

## 6. 词袋模型 (Bag of Words — BOW)

### 6.1 概念介绍 (Concept Introduction)

![Page 13](lecture3_slides_pages/page_013.png)

**Bag of Words (BOW):** Illustrates the "bag" concept — words are treated as an unordered collection, ignoring grammar and position, only tracking frequency. — 图解"词袋"概念：词被视为无序集合，忽略语法和位置，只记录出现频率。

- Document is represented as an unordered collection of its tokens, disregarding word order, and syntax etc., while keeping track of word presence or frequency — 文档被表示为其词符的无序集合，忽略词序、语法等，同时跟踪词的出现与否或频率

Ref: https://sep.com/blog/a-bag-of-words-levels-of-language/

### 6.2 计数向量化 (Count Vectorization)

![Page 14](lecture3_slides_pages/page_014.png)

**BOW Technique: Count Vectorization:** Diagram showing 3 sample documents being mapped into a shared vocabulary then converted to count vectors (Document-Term Matrix). — 图示3个示例文档被映射到共享词表后转换为计数向量（文档-词项矩阵）。

![Page 15](lecture3_slides_pages/page_015.png)

**Count Vectorization for Documents — Code Example:** sklearn CountVectorizer code and the resulting Document-Term Matrix output. — sklearn CountVectorizer 代码及其输出的文档-词项矩阵。

```python
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
corpus = ['This is the first document.',
          'This is the second document.',
          'And the third one. One is fun.']
cv = CountVectorizer()
X = cv.fit_transform(corpus)
pd.DataFrame(X.toarray(), columns=cv.get_feature_names())
```

Output: Document-Term Matrix showing word frequencies across all documents. — 输出：文档-词项矩阵，展示所有文档中每个词的频次。

### 6.3 词序丢失问题 (Word Order Loss)

![Page 16](lecture3_slides_pages/page_016.png)

**Bag of Words (BOW) — Word Order Issue:** Demonstrates that "John is quicker than Mary" and "Mary is quicker than John" produce the same BOW vector — completely losing the opposite meaning. — 演示"John is quicker than Mary"和"Mary is quicker than John"产生相同BOW向量——含义相反但表示完全相同。

- "John is quicker than Mary" and "Mary is quicker than John" produce the same BOW vector — word order is completely lost. — "John is quicker than Mary"和"Mary is quicker than John"产生相同的BOW向量——词序完全丢失。

![Page 17](lecture3_slides_pages/page_017.png)

**Bag of Words (BOW) — Additional example:** Another document pair showing identical BOW representations despite different word order. — 另一个文档对示例，展示不同词序产生相同BOW表示。

### 6.4 优缺点 (Advantages & Disadvantages)

![Page 18](lecture3_slides_pages/page_018.png)

**Bag of Words (BOW) — Advantages vs Disadvantages:** Two-column summary slide comparing BOW's strengths (simple, efficient, language-agnostic) against its weaknesses (no word order, sparse, no semantics, OOV). — 双列摘要幻灯片对比BOW的优点（简单、高效、语言无关）和缺点（无词序、稀疏、无语义、OOV）。

| Advantages                                                                            | Disadvantages                                     |
| ------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Simplicity and Interpretability — 简单性与可解释性                                    | Ignores context and word order — 忽略上下文和词序 |
| Works well for text classification and information retrieval — 适合文本分类和信息检索 | High-dimensional feature space — 高维特征空间     |
| Computational Efficiency — 计算效率高                                                 | Sparsity — 稀疏性                                 |
| Language Agnostic — 语言无关性                                                        | Lack of semantic information — 缺乏语义信息       |
|                                                                                       | Out Of Vocabulary (OOV) — 词汇表外词语（OOV）     |

> **📝 Notes:**
>
> **📌 What:**
> **(1) Bag of Words — BOW (词袋模型):**
>
> BOW represents a document as a fixed-length vector of word frequencies. Each dimension = one vocabulary word; each value = how many times that word appears. "Bag" = unordered — word position is completely discarded.
>
> > BOW将文档表示为词频的固定长度向量。每个维度=一个词表词；每个值=该词出现的次数。"袋"=无序——词的位置被完全丢弃。
>
> **(2) Document-Term Matrix (文档-词项矩阵):**
>
> When you apply BOW to a corpus, you get a matrix where rows = documents, columns = vocabulary terms. This is called a Document-Term Matrix (DTM). `CountVectorizer` in sklearn builds this automatically.
>
> > 当你对语料库应用BOW时，得到一个矩阵，行=文档，列=词表词项。这叫做文档-词项矩阵（DTM）。sklearn的`CountVectorizer`会自动构建。
>
> **🎯 Why:**
> **(1) First step beyond binary (超越二进制的第一步):**
>
> OHE only records presence/absence (0 or 1). BOW records frequency — "the" appears 5 times is different from "quantum" appearing 1 time. Frequency carries information about topic and importance.
>
> > OHE只记录存在/不存在（0或1）。BOW记录频率——"the"出现5次与"quantum"出现1次是不同的。频率携带关于主题和重要性的信息。
>
> **💡 Intuition:**
> **(1) Shopping bag analogy (购物袋类比):**
>
> BOW is like dumping all words from a document into a shopping bag and shaking it. You know WHAT items are in the bag and HOW MANY of each, but you've lost all information about the ORDER they were arranged on the shelf. "Dog bites man" and "Man bites dog" become identical bags.
>
> > BOW就像把文档中的所有词倒进购物袋然后摇一摇。你知道袋子里有什么以及每种有多少，但你失去了它们在架子上排列顺序的所有信息。"Dog bites man"和"Man bites dog"变成了相同的袋子。
>
> **⚠️ Pitfall:**
> **(1) Word order blindness (词序盲):**
>
> "John is quicker than Mary" and "Mary is quicker than John" have identical BOW vectors despite having opposite meanings. For sentiment analysis, "not good" loses its negation when order is discarded. Use N-grams (§7) to partially recover order.
>
> > "John is quicker than Mary"和"Mary is quicker than John"的BOW向量完全相同，尽管含义相反。对于情感分析，当顺序被丢弃时"not good"失去了否定。使用N-grams（§7）部分恢复词序。
>
> **(2) Common words dominate (常见词主导):**
>
> Words like "the", "is", "a" appear frequently in EVERY document, dominating the vector values but carrying zero discriminative power. This is exactly WHY TF-IDF (§8) was invented — to downweight common words.
>
> > 像"the"、"is"、"a"这样的词在每个文档中频繁出现，主导向量值但携带零区分能力。这正是TF-IDF（§8）被发明的原因——降低常见词的权重。
>
> **📝 Exam:**
> **(1) 编码题 (Encoding):**
>
> "Apply Count Vectorizer to: D1='cat dog cat', D2='dog bird'." → Vocab: {bird, cat, dog}. D1=[0,2,1], D2=[1,0,1].
>
> > "对D1='cat dog cat'，D2='dog bird'应用计数向量化。" → 词表：{bird, cat, dog}。D1=[0,2,1]，D2=[1,0,1]。
>
> **(2) 推理题 (Reasoning):**
>
> "Why can BOW fail for sentiment analysis?" → Because it discards word order; "not good" becomes {not:1, good:1}, losing the negation and appearing positive.
>
> > "为什么BOW在情感分析中可能失败？" → 因为它丢弃词序；"not good"变成{not:1, good:1}，失去否定显得积极。

---

## 7. N-Gram词袋模型 (Bag of N-Grams — BON)

### 7.1 概念介绍 (Concept Introduction)

![Page 19](lecture3_slides_pages/page_019.png)

**Bag of N-Grams (BON):** Introduces the concept — instead of single words, uses N consecutive words as features. Reduces the word-order problem of plain BOW. — 介绍N-Gram概念：以N个连续词为特征单元，部分保留了BOW中完全丢失的词序信息。

### 7.2 N-Gram类型 (N-Gram Types)

![Page 20](lecture3_slides_pages/page_020.png)

**Bag of N-Grams (BON) — Types:** Three types shown with example "I am learning NLP": Unigrams (single words), Bigrams (2-word sequences), Trigrams (3-word sequences). — 以"I am learning NLP"为例展示三种粒度：Unigram（单词）、Bigram（双词序列）、Trigram（三词序列）。

- Unigrams are the unique words present in the sentence. — Unigram是句子中出现的唯一词语。
- Bigram is the combination of 2 words. — Bigram是2个词的组合。
- Trigram is 3 words. — Trigram是3个词。
- Example: "I am learning NLP" — 示例："I am learning NLP"
  - Unigrams: "am", "learning", "NLP"
  - Bigrams: "am learning", "learning NLP"
  - Trigrams: "am learning NLP"

### 7.3 优缺点 (Advantages & Disadvantages)

![Page 21](lecture3_slides_pages/page_021.png)

**Bag of N-Grams (BON) — Advantages vs Disadvantages:** Two-column slide; left: captures context/word-order, simple and efficient; right: sparsity, expensive, ignores overall meaning, OOV, hard to choose N. — 双列对比；左：捕获上下文/词序、简单高效；右：稀疏、计算开销大、忽略整体语义、OOV、N难以选择。

| Advantages                                                                      | Disadvantages                                                            |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| It captures some context and word-order information — 捕获部分上下文和词序信息  | Sparsity — 稀疏性                                                        |
| Simple and efficient method for representing text data — 简单高效的文本表示方法 | Computationally expensive — 计算开销大                                   |
|                                                                                 | Ignores the overall structure and meaning of a text — 忽略整体结构和语义 |
|                                                                                 | Choice of N — N的选择困难                                                |
|                                                                                 | Out Of Vocabulary (OOV) — 词汇表外词语                                   |

> **📝 Notes:**
>
> **📌 What:**
> **(1) N-Gram (N元组):**
>
> An N-gram is a contiguous sequence of N tokens from text. Unigram (N=1): single words. Bigram (N=2): pairs of consecutive words. Trigram (N=3): triples. BON uses these multi-word units as features instead of single words.
>
> > N-gram是文本中N个连续token的序列。Unigram（N=1）：单词。Bigram（N=2）：连续词对。Trigram（N=3）：三联词。BON使用这些多词单元而非单词作为特征。
>
> **🎯 Why:**
> **(1) Partially recovers word order (部分恢复词序):**
>
> BOW's fatal flaw is losing word order. Bigrams partially fix this: "not good" as a single bigram feature retains the negation that BOW destroys. "Machine learning" as a bigram captures the compound concept that two separate unigrams miss.
>
> > BOW的致命缺陷是丢失词序。Bigram部分修复了这个问题："not good"作为单个bigram特征保留了BOW摧毁的否定。"Machine learning"作为bigram捕获了两个独立unigram遗漏的复合概念。
>
> **💡 Intuition:**
> **(1) Word pair context (词对上下文):**
>
> Think of unigrams as individual LEGO bricks — you know the colors but not the shape. Bigrams are like taking photos of every pair of connected bricks — you start seeing edges and joints. Trigrams show even more structure, but the number of possible photos explodes.
>
> > 把unigram想象成单个乐高积木——你知道颜色但不知道形状。Bigram就像拍摄每对相连积木的照片——你开始看到边缘和连接。Trigram展示更多结构，但可能的照片数量爆炸式增长。
>
> **⚠️ Pitfall:**
> **(1) Exponential explosion of features (特征的指数级爆炸):**
>
> With a vocabulary of V words: unigrams = V features, bigrams = V² possible features, trigrams = V³. For V=10,000: bigrams can be up to 100 million features! Most are empty (sparse), but the computational cost grows fast. This is why N>3 is rarely used.
>
> > 对于V个词的词表：unigram = V个特征，bigram = V²个可能特征，trigram = V³。当V=10,000时：bigram最多可达1亿个特征！大多数是空的（稀疏），但计算成本快速增长。这就是为什么N>3很少使用。
>
> **(2) Choice of N is critical (N的选择至关重要):**
>
> Too small N (unigram) = no context. Too large N = too sparse, too specific, overfitting. In practice, N=1+2 (unigrams + bigrams combined) works best for most classification tasks. Use `CountVectorizer(ngram_range=(1,2))` in sklearn.
>
> > N太小（unigram）= 无上下文。N太大 = 太稀疏、太具体、过拟合。实践中，N=1+2（unigram + bigram组合）对大多数分类任务效果最好。在sklearn中使用`CountVectorizer(ngram_range=(1,2))`。
>
> **⚖️ Compare:**
> **(1) BOW vs BON:**
>
> | Feature       | BOW (Unigrams)                   | BON (N-Grams)                         |
> | ------------- | -------------------------------- | ------------------------------------- |
> | Word order    | Completely lost                  | Partially preserved (within N-window) |
> | Feature count | V                                | V + V² + ... (exponential)            |
> | "not good"    | {not:1, good:1} — loses negation | {"not good":1} — keeps negation       |
> | Computation   | Fast                             | Much slower for large N               |
>
> > | 特性       | BOW（Unigrams）           | BON（N-Grams）           |
> > | ---------- | ------------------------- | ------------------------ |
> > | 词序       | 完全丢失                  | 部分保留（N窗口内）      |
> > | 特征数量   | V                         | V + V² + ...（指数级）   |
> > | "not good" | {not:1, good:1}——失去否定 | {"not good":1}——保留否定 |
> > | 计算       | 快速                      | 大N时慢得多              |
>
> **📝 Exam:**
> **(1) 提取题 (Extraction):**
>
> "List all bigrams of 'I love NLP'." → "I love", "love NLP".
>
> > "列出'I love NLP'的所有bigram。" → "I love"、"love NLP"。
>
> **(2) 对比题 (Comparison):**
>
> "Why are N-grams better than BOW for sentiment analysis?" → N-grams preserve local word order, so negation phrases like "not good" remain intact as a single feature rather than being split into two separate words.
>
> > "为什么N-gram在情感分析中比BOW更好？" → N-gram保留局部词序，因此否定短语如"not good"作为一个完整特征保留，而不是被拆成两个独立的词。

---

## 8. TF-IDF模型 (Term Frequency-Inverse Document Frequency)

### 8.1 直觉理解 (TF-IDF Intuition)

![Page 22](lecture3_slides_pages/page_022.png)

**Term Frequency-Inverse Document Frequency — Intuition:** Explains the core idea: rare words get higher weight, common words get lower weight; similarity = shared rare words. — 核心思想：稀有词权重高，常见词权重低；两文档越相似，共有的稀有词越多。

- TF-IDF assigns more weight to rare words and less weight to commonly occurring words. — TF-IDF给稀有词赋予更高权重，给常见词赋予更低权重。
- Tells us how frequent a word is in a document relative to its frequency in the entire corpus. — 告诉我们一个词在文档中的频率相对于其在整个语料库中的频率。
- Tells us that two documents are similar when they have more rare words in common. — 告诉我们当两个文档共有更多稀有词时，它们更相似。

![Page 23](lecture3_slides_pages/page_023.png)

**TF-IDF score = TF × IDF** — TF-IDF分数 = 词频 × 逆文档频率

### 8.2 词频 (Term Frequency)

![Page 24](lecture3_slides_pages/page_024.png)

**Term Frequency:** Motivates normalizing raw count by document length — TF(term) = count / total terms. — 词频：用文档长度归一化原始计数——TF(词) = 词出现次数 / 文档总词数。

- So far, we've been recording the term (word) count — 目前我们只是记录词的原始计数
- A better way to compare is by a normalized term frequency: (term count) / (total terms) — 更好的做法是用归一化词频：词计数 / 总词数
- TF(term) = (Number of times term appears in document) / (Total number of terms in document) — TF(词) = 词在文档中出现次数 / 文档中总词数

### 8.3 逆文档频率 (Inverse Document Frequency)

![Page 25](lecture3_slides_pages/page_025.png)

**Inverse Document Frequency:** Introduces the need to weight by global rarity — words appearing in all documents should get low weight. — 逆文档频率：引入全局稀有度加权——在所有文档中都出现的词应获得低权重。

- Besides term frequency, another thing to consider is how common a word is among all the documents — 除了词频，还需要考虑词在所有文档中的普遍程度
- Rare words should get additional weight — 稀有词应获得额外权重
- Measures the importance of the term across a corpus — 衡量词在整个语料库中的重要性

![Page 26](lecture3_slides_pages/page_026.png)

**IDF Formula:** IDF(term) = log(N / df) where N = total docs, df = docs containing the term. Log compresses extreme values. — IDF公式：IDF(词) = log(N / df)，N=总文档数，df=包含该词的文档数；log压缩极端值。

- IDF(term) = log(Total number of documents / Number of documents containing the term) — IDF(词) = log(总文档数 / 包含该词的文档数)
- Words that appear in many documents get a low IDF score — 在很多文档中出现的词得到低IDF分数
- Words that appear in only a few documents get a high IDF score — 只在少数文档中出现的词得到高IDF分数

### 8.4 TF-IDF计算 (TF-IDF Calculation)

![Page 27](lecture3_slides_pages/page_027.png)

**TF-IDF score = TF × IDF** — TF-IDF分数 = TF × IDF，兼顾局部频率与全局稀有度

### 8.5 TF-IDF示例 (TF-IDF Example)

![Page 28](lecture3_slides_pages/page_028.png)

**TF-IDF Example — Documents:** Four example documents about sky/sun/brightness used to demonstrate TF-IDF computation. — 四个关于天空/太阳/亮度的示例文档，用于演示TF-IDF计算。

- The sky is blue.
- The sun is bright today.
- The sun in the sky is bright.
- We can see the shining sun, the bright sun.

![Page 29](lecture3_slides_pages/page_029.png)

**TF-IDF Example — Calculation:** Matrix showing TF, IDF, and TF-IDF scores for each term across all four documents. — 矩阵展示4个文档中每个词的TF、IDF、TF-IDF分值。

### 8.6 课堂练习 (Group Work)

![Page 30](lecture3_slides_pages/page_030.png)

**Group Work: Compute TF-IDF** — 小组作业：计算TF-IDF

- D1: Dog bites man.
- D2: Man bites dog.
- D3: Dog eats meat.
- D4: Man eats food.

### 8.7 CountVectorizer vs TfidfVectorizer

![Page 31](lecture3_slides_pages/page_031.png)

**Count Vectorizer vs TF-IDF Vectorizer — Code:** Side-by-side sklearn code using CountVectorizer and TfidfVectorizer on the same corpus. — sklearn代码对比：在相同语料库上使用CountVectorizer和TfidfVectorizer。

```python
import pandas as pd
corpus = ['This is the first document.', 'This is the second document.', 'And the third one. One is fun.']

# original Count Vectorizer
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()
pd.DataFrame(X, columns=cv.get_feature_names())

# new TF-IDF Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
cv_tfidf = TfidfVectorizer()
X_tfidf = cv_tfidf.fit_transform(corpus).toarray()
pd.DataFrame(X_tfidf, columns=cv_tfidf.get_feature_names())
```

![Page 32](lecture3_slides_pages/page_032.png)

**Count Vectorizer vs TF-IDF Vectorizer — Output:** Side-by-side output showing how common words ("the", "is") get high counts in CountVectorizer but low TF-IDF weights. — 对比输出：常见词（"the"、"is"）在CountVectorizer中计数高，但TF-IDF权重低。

### 8.8 为什么需要log (Why We Need log)

![Page 33](lecture3_slides_pages/page_033.png)

**Why we need log():** Chart/explanation showing that without log, IDF for a very rare word could be millions — log compresses the scale to a manageable range. — 说明若无log，极稀有词的IDF值可达百万级；log将其压缩到可用范围内。

### 8.9 TF-IDF局限性 (TF-IDF Limitations)

![Page 34](lecture3_slides_pages/page_034.png)

**TF-IDF Limitations:** Five listed limitations — no word relationships, sparsity, no semantic understanding, poor for small corpora, OOV. — 五项局限性：无词间关系、稀疏、无语义理解、小语料库效果差、OOV问题。

- Miss information about the relationships between words — 缺失词语之间的关系信息
- Sparsity — 稀疏性
- Lack of semantic understanding — 缺乏语义理解
- Not well suited for small corpora — 不适合小语料库
- Out Of Vocabulary (OOV) words — 词汇表外词语（OOV）

> **📝 Notes:**
>
> **📌 What:**
> **(1) TF-IDF — Term Frequency-Inverse Document Frequency (词频-逆文档频率):**
>
> A statistical weighting scheme that combines two signals: how often a word appears in a document (TF) and how rare it is across all documents (IDF). TF-IDF = TF × IDF. Common words get low scores; rare but frequent-in-document words get high scores.
>
> > 一种统计加权方案，结合两个信号：一个词在文档中出现的频率（TF）和它在所有文档中的稀有程度（IDF）。TF-IDF = TF × IDF。常见词得到低分；在文档中频繁但整体稀有的词得到高分。
>
> **🎯 Why:**
> **(1) BOW treats all words equally (BOW平等对待所有词):**
>
> In BOW, "the" appearing 10 times gets a feature value of 10, dominating the vector. But "the" appears in EVERY document — it has zero discriminative power. TF-IDF solves this by multiplying frequency by rarity: "the" gets high TF but near-zero IDF, resulting in a low TF-IDF score.
>
> > 在BOW中，"the"出现10次获得特征值10，主导了向量。但"the"出现在每个文档中——它有零区分能力。TF-IDF通过将频率乘以稀有度来解决："the"获得高TF但接近零的IDF，最终TF-IDF分数很低。
>
> **(2) Rare words are better discriminators (稀有词是更好的区分器):**
>
> If "quantum" appears only in 2 out of 1000 documents, it strongly signals what those documents are about. TF-IDF automatically boosts such rare, topical words. This is the core insight: importance ∝ (local frequency) × (global rarity).
>
> > 如果"quantum"只在1000个文档中的2个中出现，它强烈地指示了那些文档的主题。TF-IDF自动提升这类稀有的主题词。核心洞察：重要性 ∝ 本地频率 × 全局稀有度。
>
> **💡 Intuition:**
> **(1) Newspaper headline analogy (报纸头条类比):**
>
> Imagine you're trying to identify what a newspaper article is about. Words like "the" and "is" appear in every article — useless clues. But "earthquake" in one article? That's a strong signal! TF-IDF is like a detective who ignores common words and focuses on the unusual ones.
>
> > 想象你试图识别一篇报纸文章的主题。"the"和"is"出现在每篇文章中——无用的线索。但某篇文章中的"earthquake"？那是一个强信号！TF-IDF就像一个侦探，忽略常见词，专注于不寻常的词。
>
> **📐 Formula:**
> **(1) TF breakdown (TF公式拆解):**
>
> TF(term, doc) = (Count of term in doc) / (Total terms in doc).
>
> - Numerator counts raw occurrences of the specific word.
> - Denominator normalizes by document length — a word appearing 5 times in a 100-word doc is more significant than 5 times in a 10,000-word doc.
>
> > TF(词, 文档) = 词在文档中的出现次数 / 文档中的总词数。
> >
> > - 分子统计特定词的原始出现次数。
> > - 分母按文档长度归一化——一个词在100词文档中出现5次比在10,000词文档中出现5次更重要。
>
> **(2) IDF breakdown (IDF公式拆解):**
>
> IDF(term) = log(N / df), where N = total documents, df = documents containing the term.
>
> - N/df = ratio of total documents to the term's document frequency. Rare words → high ratio → high IDF.
> - log() compresses the scale — without it, a word in 1 out of 1,000,000 documents would get a weight of 1,000,000, which is impractical.
>
> > IDF(词) = log(N / df)，其中N = 总文档数，df = 包含该词的文档数。
> >
> > - N/df = 总文档数与词的文档频率的比值。稀有词 → 高比值 → 高IDF。
> > - log()压缩尺度——没有它，在1,000,000文档中只出现1次的词会获得1,000,000的权重，这不切实际。
>
> **🔢 Example:**
> **(1) TF-IDF calculation (TF-IDF计算):**
>
> **Problem:** 4 documents: D1="Dog bites man", D2="Man bites dog", D3="Dog eats meat", D4="Man eats food". Compute TF-IDF for "dog" in D1.
> **Solution:**
>
> - TF("dog", D1) = 1/3 = 0.333 (1 appearance out of 3 words)
> - IDF("dog") = log(4/2) = log(2) ≈ 0.301 ("dog" appears in D1,D2,D3 — wait, actually D1,D2,D3 = 3 docs, so IDF=log(4/3)≈0.125)
> - TF-IDF = 0.333 × 0.125 ≈ 0.042
>
> > **题目：** 4个文档：D1="Dog bites man"，D2="Man bites dog"，D3="Dog eats meat"，D4="Man eats food"。计算D1中"dog"的TF-IDF。
> > **解：**
> >
> > - TF("dog", D1) = 1/3 = 0.333（3个词中出现1次）
> > - IDF("dog") = log(4/3) ≈ 0.125（"dog"出现在D1、D2、D3共3个文档中）
> > - TF-IDF = 0.333 × 0.125 ≈ 0.042
>
> **⚖️ Compare:**
> **(1) CountVectorizer vs TfidfVectorizer:**
>
> | Feature       | CountVectorizer        | TfidfVectorizer             |
> | ------------- | ---------------------- | --------------------------- |
> | Output values | Raw integer counts     | Weighted floats (0-1 range) |
> | Common words  | High values (dominant) | Low values (downweighted)   |
> | Rare words    | Low values (buried)    | High values (boosted)       |
> | sklearn class | `CountVectorizer`      | `TfidfVectorizer`           |
>
> > | 特性      | CountVectorizer   | TfidfVectorizer       |
> > | --------- | ----------------- | --------------------- |
> > | 输出值    | 原始整数计数      | 加权浮点数（0-1范围） |
> > | 常见词    | 高值（主导）      | 低值（降权）          |
> > | 稀有词    | 低值（被淹没）    | 高值（提升）          |
> > | sklearn类 | `CountVectorizer` | `TfidfVectorizer`     |
>
> **⚠️ Pitfall:**
> **(1) Still no semantic understanding (仍然没有语义理解):**
>
> TF-IDF treats "happy" and "joyful" as completely unrelated words — they get separate dimensions with no connection. It only measures statistical importance, not meaning. This is the fundamental limitation that word embeddings (Word2Vec, GloVe) later solve.
>
> > TF-IDF将"happy"和"joyful"视为完全不相关的词——它们获得独立的维度，没有联系。它只衡量统计重要性，而不是含义。这是词嵌入（Word2Vec、GloVe）后来解决的根本局限。
>
> **(2) Small corpora problem (小语料库问题):**
>
> IDF is based on document frequency across the corpus. With only 5 documents, a word appearing in 2 gives IDF = log(5/2) = 0.4. With 1,000,000 documents, the same ratio gives more meaningful weights. TF-IDF works best with large corpora.
>
> > IDF基于语料库中的文档频率。只有5个文档时，一个词出现在2个中给出IDF = log(5/2) = 0.4。有1,000,000个文档时，相同比率给出更有意义的权重。TF-IDF在大语料库中效果最好。
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> "Given a corpus of 4 documents, compute the TF-IDF score for a specific word." → Show TF calculation (count/total), IDF calculation (log(N/df)), then multiply. Must show all steps.
>
> > "给定4个文档的语料库，计算特定词的TF-IDF分数。" → 展示TF计算（计数/总数）、IDF计算（log(N/df)），然后相乘。必须展示所有步骤。
>
> **(2) 推理题 (Reasoning):**
>
> "Why does TF-IDF use log in IDF?" → To compress the scale. Without log, a word appearing in 1 out of 1,000,000 documents would get a weight of 1,000,000 — impractical and would dominate all other features.
>
> > "为什么TF-IDF在IDF中使用log？" → 为了压缩尺度。没有log，在1,000,000文档中只出现1次的词会获得1,000,000的权重——不切实际且会主导所有其他特征。

---

## 9. 文本相似度度量 (Text Similarity Measures)

### 9.1 概述 (Overview)

![Page 35](lecture3_slides_pages/page_035.png)

**Text Similarity Measure (lexical similarity):** Defines text similarity as a computational measure of how alike two documents are, with 6 application areas listed. — 定义文本相似度：衡量两个文档相似程度的计算度量，列举了6个应用领域。

- Computational measure of the degree to which two or more documents are semantically or lexically alike. — 计算两个或多个文档在语义或词汇上相似程度的度量。
- Applications: Speech Recognition, Machine Translation, Plagiarism Detection, Information Retrieval, Text Classification, Search engine — 应用：语音识别、机器翻译、抄袭检测、信息检索、文本分类、搜索引擎

![Page 36](lecture3_slides_pages/page_036.png)

**Text Similarity Measures — Types:** Five common similarity measures listed as agenda items. — 列出5种常见的文本相似度度量方法。

- ❑Jaccard Similarity — Jaccard相似度
- ❑Cosine Similarity — 余弦相似度
- ❑Euclidean Distance — 欧几里得距离
- ❑Hamming Distance — 汉明距离
- ❑Levenshtein Distance — Levenshtein距离（编辑距离）

### 9.2 Levenshtein距离 (Levenshtein Distance)

![Page 37](lecture3_slides_pages/page_037.png)

**Text Similarity: Levenshtein distance:** Defines edit distance (min operations to transform one word into another) with example kitten→sitting = 3 operations. — 定义编辑距离（将一个词转换为另一个词所需的最少操作数），以kitten→sitting = 3步为例。

- Levenshtein distance: Minimum number of operations to get from one word to another. — Levenshtein距离：从一个词转换到另一个词所需的最少操作数。
- Levenshtein operations are: — Levenshtein操作包括：
  - ▪ Deletions: Delete a character — 删除：删除一个字符
  - ▪ Insertions: Insert a character — 插入：插入一个字符
  - ▪ Mutations: Change a character — 替换：更改一个字符
- Example: kitten → sitting — 示例：kitten → sitting
  - ▪ kitten → sitten (1 letter change) — kitten → sitten（1次替换）
  - ▪ sitten → sittin (1 letter change) — sitten → sittin（1次替换）
  - ▪ sittin → sitting (1 letter insertion) — sittin → sitting（1次插入）
  - Levenshtein distance = 3 — Levenshtein距离 = 3

### 9.3 欧几里得距离 (Euclidean Distance)

![Page 38](lecture3_slides_pages/page_038.png)

**Text Similarity: Euclidean Distance:** Geometric illustration showing the straight-line distance between two vector endpoints in 2D space. — 几何示意图：2D空间中两个向量端点之间的直线距离（"直线"距离）。

Ref: http://dataaspirant.com/2015/04/11/five-most-popular-similarity-measures-implementation-in-python/

### 9.4 余弦相似度 (Cosine Similarity)

![Page 39](lecture3_slides_pages/page_039.png)

**Text Similarity: Cosine:** Formula cos(θ) = (A·B)/(‖A‖‖B‖) — measures angle between vectors, not magnitude. Values range 0 (orthogonal) to 1 (identical direction). — 余弦公式：cos(θ) = (A·B)/(‖A‖‖B‖)，衡量向量夹角而非长度，值域0（正交）到1（同向）。

- Measures how similar two vectors are by comparing the angle between them — 通过比较向量之间的角度来衡量两个向量的相似性
- cos(θ) = (A · B) / (‖A‖ ‖B‖)

![Page 40](lecture3_slides_pages/page_040.png)

**Cosine Similarity: Example:** Two doc vectors shown — Doc1=[1,1,0,1] for "I love NLP", Doc2=[1,1,1,0] for "I love you". Cosine similarity = 0.667. — 两个文档向量示例：Doc1=[1,1,0,1]对应"I love NLP"，Doc2=[1,1,1,0]对应"I love you"，余弦相似度 = 0.667。

- Step 1: Put each document in vector format — 步骤1：将每个文档转换为向量格式
- Step 2: Find the cosine of the angle between the documents — 步骤2：计算文档间向量夹角的余弦值
- "I love NLP" → Doc1: [1, 1, 0, 1]
- "I love you" → Doc2: [1, 1, 1, 0]
- Cosine similarity = 0.667

### 9.5 课堂练习 (In-Class Exercises)

![Page 41](lecture3_slides_pages/page_041.png)

**Your turn — Cosine similarity with word co-occurrence data:** Word co-occurrence matrix for 3 words (cherry, digital, information) × 3 contexts (pie, data, computer). Compute cosine similarity between word vectors. — 词共现矩阵：3个词（cherry/digital/information）× 3个上下文（pie/data/computer），计算词向量间的余弦相似度。

|             | pie | data | computer |
| ----------- | --- | ---- | -------- |
| cherry      | 442 | 8    | 2        |
| digital     | 5   | 1683 | 1670     |
| information | 5   | 3982 | 3325     |

![Page 42](lecture3_slides_pages/page_042.png)

**Your turn — Document similarity exercise:** Three short documents (d₁/d₂/d₃) using animal words. Compute pairwise cosine similarity using Count Vectorizer and TF-IDF. — 三个简短文档（d₁/d₂/d₃）使用动物词汇，分别用CountVectorizer和TF-IDF计算两两余弦相似度。

- d₁: ant ant bee
- d₂: dog bee dog hog dog ant dog
- d₃: cat gnu dog eel fox

Use cosine measure to compute pairwise similarity using Count Vectorizer, BOW, and TF-IDF. — 使用余弦相似度度量，分别用计数向量化、BOW和TF-IDF计算两两相似度。

> **📝 Notes:**
>
> _(To be added by note_taking skill)_

---

## 10. 文档相似度实战 (Document Similarity in Practice)

### 10.1 CountVectorizer结果 (Count Vectorizer Results)

![Page 43](lecture3_slides_pages/page_043.png)

**Document Similarity: Example — Five documents:** Five short sentences all containing the word "hot" but with different contexts (weather, chocolate, encoding, latte, sale). — 五个含"hot"的短句，但上下文各不同（天气/巧克力/编码/拿铁/促销）。

- "The weather is hot under the sun"
- "I make my hot chocolate with milk"
- "One hot encoding"
- "I will have a chai latte with milk"
- "There is a hot sale today"

![Page 44](lecture3_slides_pages/page_044.png)

**Document Similarity: Example — Count Vectorizer Output:** Similarity matrix showing CountVectorizer ranks doc1 & doc3 as most similar (0.408) because both share "hot" — but this is misleading since "hot" is too common. — 相似度矩阵：CountVectorizer将doc1和doc3排为最相似（0.408），因为都有"hot"——但这具有误导性，因为"hot"太常见。

- Top similarity: (0.408, "The weather is hot under the sun" vs "One hot encoding") — 最高相似度：（0.408，"The weather is hot under the sun" vs "One hot encoding"）
- These two documents are most similar, but it's just because the term "hot" is a popular word — 这两个文档最相似，但仅仅因为"hot"是个常见词
- "Milk" seems to be a better differentiator, so how can we mathematically highlight that? — "Milk"似乎是更好的区分词，那么如何在数学上突显这一点？

### 10.2 TF-IDF结果 (TF-IDF Results)

![Page 45](lecture3_slides_pages/page_045.png)

**Document Similarity: Example with TF-IDF:** After TF-IDF reweighting, doc2 & doc4 become most similar (0.232) because they both share "milk" — a rarer word — showing TF-IDF gives smarter similarity. — TF-IDF重新加权后，doc2和doc4变得最相似（0.232），因为两者共有"milk"（稀有词），体现了TF-IDF更智能的相似度判断。

- Top similarity: (0.232, "I make my hot chocolate with milk" vs "I will have a chai latte with milk") — 最高相似度：（0.232，"I make my hot chocolate with milk" vs "I will have a chai latte with milk"）
- By weighting "milk" (rare) > "hot" (popular), we get a smarter similarity score — 通过将"milk"（稀有）权重 > "hot"（常见）权重，我们得到了更智能的相似度分数

> **📝 Notes:**
>
> _(To be added by note_taking skill)_

---

## 11. 讨论与伦理 (Discussion & Ethics)

![Page 46](lecture3_slides_pages/page_046.png)

**Discussion:** Open question slide — What are the ethical concerns related to frequency-based text representation? — 开放式讨论：基于频率的文本表示法有哪些伦理问题？

---

## 12. 总结 (Summary)

![Page 47](lecture3_slides_pages/page_047.png)

**Summary — Today we discussed:** Recap slide listing all 4 representation methods and 3 similarity measures covered. — 总结幻灯片，列举本节课覆盖的4种文本表示方法和3种相似度度量。

- ➢ Traditional methods for text representation: — 传统文本表示方法：
  - ❑ One-hot encoding — 独热编码
  - ❑ Bag of words — 词袋模型
  - ❑ Bag of N-grams — N元词袋
  - ❑ TF-IDF
- ➢ Similarity measures: — 相似度度量：
  - ❑ Lexical Similarity – Levenshtein — 词汇相似度 – 编辑距离
  - ❑ Lexical Similarity – Cosine — 词汇相似度 – 余弦相似度
  - ❑ Lexical Similarity – Euclidean distance — 词汇相似度 – 欧几里得距离
