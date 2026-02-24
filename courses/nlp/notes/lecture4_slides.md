# Week 4: 词嵌入 (Word Embedding)

> Source: `lecture_4_W26.pdf`
> Total slides: 54
> Instructor: Hala Own, Ph.D.

---

## 1. 课程议程 (Lesson Agenda)

![Page 1](lecture4_slides_pages/page_001.png)

**CST8507: Natural Language Processing — Week #4: Word Embedding** — CST8507自然语言处理，第4周：词嵌入

![Page 2](lecture4_slides_pages/page_002.png)

**Lesson Agenda:** — 本节课议程：

- ❑ Prediction based Text representation (word Embedding) — 基于预测的文本表示（词嵌入）
- ❑ CBOW, Skip-Gram and SGNS — CBOW、Skip-Gram和SGNS
- ❑ Word2Vec — Word2Vec
- ❑ FastText — FastText
- ❑ Count-Based / Matrix Factorization Methods — 基于计数/矩阵分解的方法
- ❑ GloVe — GloVe

---

## 2. NLP开发生命周期 (NLP Development Life Cycle)

![Page 3](lecture4_slides_pages/page_003.png)

**NLP Development Life Cycle:** Circular pipeline diagram — 8 stages looping: Requirements gathering → Data collection → Text preprocessing → Feature extraction → Model building → Evaluation → Deployment → Gather more data / Improve the model. — NLP开发生命周期循环流程图——8个阶段：需求收集→数据收集→文本预处理→特征提取→模型构建→评估→部署→收集更多数据/改进模型。

---

## 3. 从频率到预测 (From Frequency to Prediction)

### 3.1 文本表示技术全景 (Text Representation Techniques Overview)

![Page 4](lecture4_slides_pages/page_004.png)

**Text Representation Techniques:** Taxonomy listing from traditional frequency-based methods to modern prediction-based and universal representations. — 文本表示方法分类树，从传统频率方法到现代预测方法和通用表示。

- Frequency based Text representation: — 基于频率的文本表示：
  - One-Hot Encoding — 独热编码
  - Bag of Words — 词袋模型
  - Bag of N-Grams — N元词袋
  - TF-IDF — TF-IDF
- Prediction based Text representation (word Embedding) — 基于预测的文本表示（词嵌入）
- Universal Text Representations — 通用文本表示

![Page 5](lecture4_slides_pages/page_005.png)

**Comparing Feature Representations for Audio, Image and Text:** Three-column diagram showing each data modality maps to its own representation form. — 三列示意图，展示语音、图像、文本三种数据模态各自对应不同的表示形式。

Ref: https://www.kdnuggets.com/2018/03/understanding-feature-engineering-deep-learning-methods-text-data.html

### 3.2 频率方法的局限性 (Limitations of Frequency-Based Methods)

![Page 6](lecture4_slides_pages/page_006.png)

**Frequency based Text representation: Limitation:** Lists four key limitations that lead to poor performance on majority of NLP tasks. — 列出四个关键局限性，导致在大多数NLP任务上性能不佳。

- High-dimensional representation — 高维表示
- Sparse — 稀疏
- OOV words — 词汇表外词语
- Lack of semantic meaning — 缺乏语义含义
- → Poor Performance On majority of NLP Tasks — → 在大多数NLP任务上性能不佳


---

## 4. 词语关系与WordNet (Word Relations & WordNet)

### 4.1 词语相似性 (Word Similarity)

![Page 7](lecture4_slides_pages/page_007.png)

**Relation between Word Senses: Word Similarity:** Explains that words can be similar without being synonyms, and introduces semantic fields. — 解释词语可以相似但不是同义词，并引入语义场概念。

- ❑ Cat is not a synonym of dog, but cats and dogs are certainly similar words — Cat不是dog的同义词，但cats和dogs确实是相似的词
- ❑ A semantic field is a set of words which cover a particular semantic domain — 语义场是覆盖特定语义域的一组词
  - ❑ Restaurants: waiter, menu, plate, food, chef — 餐厅：服务员、菜单、盘子、食物、厨师
  - ❑ Houses: door, roof, kitchen, family, bed — 房屋：门、屋顶、厨房、家庭、床
- One way of getting values for word similarity is to ask humans to judge how similar one word is to another — 获取词语相似度数值的一种方式是让人类判断两个词有多相似

### 4.2 WordNet概述 (WordNet Overview)

![Page 8](lecture4_slides_pages/page_008.png)

**WordNet:** A large lexical database of English words, where words are grouped into sets of synonyms called synsets. These synsets are connected by various semantic relationships, such as synonymy, hypernymy, and hyponymy, etc. — WordNet：大型英语词汇数据库，词语被分组为同义词集（synsets），并通过同义、上位、下位等语义关系相连。

Ref: https://wordnet.princeton.edu/

![Page 9](lecture4_slides_pages/page_009.png)

**WordNet: Database of lexical relations for English.** Diagram showing hierarchical tree structure of WordNet's synset relationships. — WordNet：英语词汇关系数据库。图示WordNet同义词集关系的层次树结构。

Ref: https://www.scaler.com/topics/nlp/wordnet-in-nlp/

### 4.3 WordNet核心概念 (WordNet Important Concepts)

![Page 10](lecture4_slides_pages/page_010.png)

**WordNet – Important Concepts:** Lists 8 key relationship types in WordNet. — 列出WordNet中8种关键关系类型。

- ❖ **Synset:** A set of synonyms that share a common meaning — 同义词集：共享同一含义的同义词集合
- ❖ **Hypernym:** A general term that encompasses more specific terms (e.g., "animal" is a hypernym of "dog") — 上位词：包含更具体术语的通用术语（如"animal"是"dog"的上位词）
- ❖ **Hyponym:** A specific term within a broader category (e.g., "dog" is a hyponym of "animal") — 下位词：更广泛类别中的具体术语（如"dog"是"animal"的下位词）
- ❖ **Meronym:** A term that denotes a part of something (e.g., "wheel" is a meronym of "car") — 部分词：表示某物的一部分（如"wheel"是"car"的部分词）
- ❖ **Holonym:** A term that denotes a whole of which the meronym is a part (e.g., "car" is a holonym of "wheel") — 整体词：表示整体（如"car"是"wheel"的整体词）
- ❖ **Antonym:** Words that have opposite meanings (e.g., "hot" and "cold") — 反义词：含义相反的词（如"hot"和"cold"）
- ❖ **Troponym:** A verb that denotes a specific manner of doing something (e.g., "run" is a troponym of "move") — 方式动词：表示某种行为特定方式的动词（如"run"是"move"的方式动词）
- ❖ **Entailment:** A relationship where one verb implies another (e.g., "snore" entails "sleep") — 蕴含：一个动词隐含另一个（如"snore"蕴含"sleep"）

### 4.4 WordNet应用与局限 (WordNet Applications & Limitations)

![Page 11](lecture4_slides_pages/page_011.png)

**WordNet Applications in NLP Tasks: Semantic Text Representation:** The context of each synset is tokenized into words, with each word mapped to a vector representation via the learned embedding matrix. The synset vector is the centroid produced by averaging all context word embeddings. — WordNet在NLP中的应用——语义文本表示：每个同义词集的上下文被分词，每个词通过学习的嵌入矩阵映射到向量，同义词集向量是所有上下文词嵌入的质心。

Ref: Text classification with semantically enriched word embeddings, Cambridge University Press, 2020

![Page 12](lecture4_slides_pages/page_012.png)

**WordNet Applications in NLP Tasks: Query Expansion:** Diagram showing how WordNet can expand search queries by finding synonyms and related terms, then converting words to numerical format. — WordNet用于查询扩展：通过查找同义词和相关术语来扩展搜索查询。

![Page 13](lecture4_slides_pages/page_013.png)

**WordNet: Limitations:** Five key limitations listed. — WordNet的五个关键局限性。

- ❑ Limited Coverage and Static Nature — 覆盖有限且静态
- ❑ Not Computational — 不可计算
- ❑ Domain Specificity — 领域特定性
- ❑ Language Limitation — 语言限制
- ❑ Manual Curation Challenges — 人工维护挑战


---

## 5. 词嵌入基础 (Word Embedding Fundamentals)

### 5.1 关键术语 (Key Terms)

![Page 14](lecture4_slides_pages/page_014.png)

**Key Terms:** Two foundational concepts underlying word embeddings. — 词嵌入的两个基础概念。

- **Distributional similarity:** the meaning of a word can be understood from the context — **分布相似性：** 一个词的含义可以从其上下文中理解
- **Distributional hypothesis:** words that occur in similar contexts have similar meanings — **分布假说：** 出现在相似上下文中的词具有相似含义

### 5.2 向量语义与词嵌入 (Vector Semantics & Word Embedding)

![Page 15](lecture4_slides_pages/page_015.png)

**Vector Semantics (Word Embedding):** Computational model that learns the linguistic units (words, phrases, or documents) representations based on distributional properties of these units in a large corpus. — 向量语义（词嵌入）：基于语言单位在大语料库中的分布特性来学习其表示的计算模型。

- ❑ Representation linguistic units as vectors in a multi-dimensional space — 将语言单位表示为多维空间中的向量
- ❑ Encoding semantic information using mathematical vectors — 使用数学向量编码语义信息
- ❑ Standard way to represent word meaning in NLP — NLP中表示词义的标准方式

![Page 16](lecture4_slides_pages/page_016.png)

**Word Embedding:** Representation of words as vectors of numbers in a high-dimensional space. It captures semantic and contextual information about the word. — 词嵌入：将词表示为高维空间中的数字向量，捕获词的语义和上下文信息。

- Input: large number of corpus, Vocabulary V, and vector of dimension d — 输入：大量语料库、词汇表V、维度d的向量
- output: f: V → R^d — 输出：f: V → R^d

![Page 17](lecture4_slides_pages/page_017.png)

**Word Embedding — Analogy:** Classic analogy example showing vector arithmetic captures semantic relationships. — 词嵌入类比：经典类比示例，展示向量算术捕获语义关系。

- vector('king') - vector('man') + vector('woman') ≈ vector('queen') — vector('king') - vector('man') + vector('woman') ≈ vector('queen')


---

## 6. Word2Vec架构 (Word2Vec Architectures)

### 6.1 基于预测的表示 (Prediction-Based Representation)

![Page 18](lecture4_slides_pages/page_018.png)

**Prediction based Text representation:** Self-supervision approach introduced by Bengio et al. (2003) and Collobert et al. (2011). — 基于预测的文本表示：Bengio等人（2003）和Collobert等人（2011）提出的自监督方法。

- Big idea: self-supervision — 核心思想：自监督
- Popular embedding method — 流行的嵌入方法
- Very fast to train — 训练速度非常快
- Code available on the web — 网上有现成代码
- Predict rather than count — 预测而非计数

![Page 19](lecture4_slides_pages/page_019.png)

**Prediction Based Text Representation (Word2Vec):** Diagram showing Word2Vec creates dense vector representations of words. Two architectures: CBOW and Skip-gram. — 图示Word2Vec创建词的稠密向量表示。两种架构：CBOW和Skip-gram。

Ref: https://dataaspirant.com/word-embedding-techniques-nlp/

### 6.2 CBOW (连续词袋模型)

![Page 20](lecture4_slides_pages/page_020.png)

**CBOW (Continuous Bag of Words):** Neural network architecture diagram showing context words as input, predicting the target (middle) word as output. — CBOW神经网络架构图：上下文词作为输入，预测目标（中间）词作为输出。

- Goal: Predict the middle word given the words of the context — 目标：给定上下文词，预测中间词

![Page 21](lecture4_slides_pages/page_021.png)

**CBOW with window size=2:** Detailed sliding window visualization. — 窗口大小=2的CBOW详细滑动窗口可视化。

Ref: https://medium.com/co-learning-lounge/nlp-word-embedding-tfidf-bert-word2vec-d7f04340af7f

![Page 22](lecture4_slides_pages/page_022.png)

**CBOW: Simple Example:** Worked example showing input context vectors being averaged and passed through the network to predict the center word. — 简单示例：输入上下文向量取平均后通过网络预测中心词。

### 6.3 Skip-gram

![Page 23](lecture4_slides_pages/page_023.png)

**Skip-gram:** The reverse of CBOW. Takes the middle word as input, predicts context words as output. — Skip-gram——CBOW的反向。以中间词为输入，预测上下文词为输出。

- Goal: Predict the context words given the middle word — 目标：给定中间词，预测上下文词

![Page 24](lecture4_slides_pages/page_024.png)

**Skip-gram training:** The training objective is to minimize the summed prediction error across all context words in the output layer. — 训练目标是最小化输出层所有上下文词的预测误差之和。

![Page 25](lecture4_slides_pages/page_025.png)

**Skip-gram: Example:** Neural network diagram showing input word mapped to hidden layer (embedding), then predicting multiple context words. — 神经网络图，展示输入词映射到隐藏层（嵌入），然后预测多个上下文词。

Ref: https://aegis4048.github.io/demystifying_neural_network_in_skip_gram_language_modeling

### 6.4 Skip-gram预测示例 (Skip-gram Prediction Examples)

![Page 26](lecture4_slides_pages/page_026.png)

**Step 1:** "the cat sat on the mat", center="the"(pos 1), context: ⟨start⟩, ⟨start⟩, cat, sat.

![Page 27](lecture4_slides_pages/page_027.png)

**Step 2:** center="cat", context: ⟨start⟩, the, sat, on.

![Page 28](lecture4_slides_pages/page_028.png)

**Step 3:** center="sat", context: the, cat, on, the.

![Page 29](lecture4_slides_pages/page_029.png)

**Step 4:** center="on", context: cat, sat, the, mat.

![Page 30](lecture4_slides_pages/page_030.png)

**Step 5:** center="the"(pos 5), context: sat, on, mat, ⟨end⟩.

![Page 31](lecture4_slides_pages/page_031.png)

**Step 6:** center="mat", context: on, the, ⟨end⟩, ⟨end⟩.

### 6.5 Skip-gram vs CBOW对比

![Page 32](lecture4_slides_pages/page_032.png)

**Skip-gram vs CBOW:** — 两种架构的总结对比。

- CBOW is comparatively faster to train than skip-gram and better for frequently occurring words — CBOW训练速度比skip-gram更快，对高频词效果更好
- Skip-gram is slower but works well for smaller amount of data — Skip-gram较慢但对少量数据效果好
- CBOW is an easier classification problem than Skip-gram — CBOW是比Skip-gram更简单的分类问题


---

## 7. SGNS与训练优化 (SGNS & Training Optimization)

![Page 33](lecture4_slides_pages/page_033.png)

**Skip-gram Negative Sampling (SGNS): Approach:** — SGNS四步流程。

1. Treat the target word t and a neighboring context word c as positive examples — 将目标词t和相邻上下文词c作为正样本
2. Randomly sample other words in the lexicon to get negative examples — 从词典中随机采样其他词作为负样本
3. Use logistic regression to train a classifier to distinguish those two cases — 使用逻辑回归训练分类器区分两种情况
4. Use the learned weights as the embeddings — 使用学到的权重作为嵌入

![Page 34](lecture4_slides_pages/page_034.png)

**SGNS: how to learn vectors:** Maximize similarity of positive pairs (w, c_pos), minimize similarity of negative pairs (w, c_neg). — 最大化正样本对相似度，最小化负样本对相似度。

![Page 35](lecture4_slides_pages/page_035.png)

**SGNS: Training example:** "... lemon, a tablespoon of apricot jam a pinch ..." — target="apricot", context: c1="tablespoon", c2="of", c3="jam", c4="a". — SGNS训练示例。


---

## 8. 预训练模型与代码 (Pretrained Models & Code)

### 8.1 Word2Vec

![Page 36](lecture4_slides_pages/page_036.png)

**Pretrained Word Embeddings Models:** Three major pretrained models. — 三个主要预训练模型。

- Word2vec (Mikolov et al.) 2013
- Fasttext 2016
- GloVe (Pennington, Socher, Manning) 2014

![Page 37](lecture4_slides_pages/page_037.png)

**Google's Word2Vec:** — Google预训练Word2Vec模型详情。

- Gensim package: Google's pre-trained Word2Vec model in Python — Gensim包：Python中Google的预训练Word2Vec模型
- Trained on 3 million words/phrases from 100 billion words of Google News — 在Google新闻的1000亿词中的300万词/短语上训练
- Vector length: 50, 100, 300 — 向量长度：50、100、300

![Page 38](lecture4_slides_pages/page_038.png)

**Word2Vec — Code:** — Word2Vec代码。

```python
# Install gensim library
# conda install -c conda-forge gensim

# Gensim Word2Vec Model Training
model = Word2Vec(text, min_count=1, vector_size=50, window=5,
                 sg=1, negative=5)
```

- `min_count=1`: include words appearing at least 1 time — 包含至少出现1次的词
- `vector_size=50`: embedding dimension — 嵌入维度
- `window=5`: context window size — 上下文窗口大小
- `sg=1`: 1=Skip-gram, 0=CBOW — 1=Skip-gram, 0=CBOW
- `negative=5`: number of negative samples — 负样本数量

![Page 39](lecture4_slides_pages/page_039.png)

**Demo:** In-class code demonstration. — 课堂代码演示。

---

## 9. GloVe (全局向量模型)

### 9.1 GloVe概述 (GloVe Overview)

![Page 40](lecture4_slides_pages/page_040.png)

**The GloVe (Global Vector for word representation):** Unsupervised learning model for dense word vectors, invented at Stanford by Pennington et al. — GloVe（全局词向量表示）：斯坦福大学Pennington等人发明的无监督稠密词向量模型。

- Unsupervised learning model that can be used to obtain dense word vectors — 可用于获取稠密词向量的无监督学习模型
- Invented in Stanford by Pennington et al. — 斯坦福大学Pennington等人发明

Ref: https://nlp.stanford.edu/projects/glove/ | https://github.com/stanfordnlp/GloVe

### 9.2 GloVe算法与共现矩阵 (GloVe Algorithm & Co-Occurrence Matrix)

![Page 41](lecture4_slides_pages/page_041.png)

**GloVe Algorithm:** Diagram showing the GloVe training process — builds a word-word co-occurrence matrix, then factorizes it to learn vectors. — GloVe算法图示——构建词-词共现矩阵，然后分解它来学习向量。

![Page 42](lecture4_slides_pages/page_042.png)

**GloVe: Co-Occurrence Matrix:** Example with "I love Programming. I love Math. I tolerate Biology." and window size=1. — 共现矩阵示例：句子"I love Programming. I love Math. I tolerate Biology."，窗口大小=1。

### 9.3 预训练GloVe向量 (Pretrained GloVe Vectors)

![Page 43](lecture4_slides_pages/page_043.png)

**GloVe: Pretrained Vectors:** Available pretrained vectors from Stanford. — 斯坦福大学提供的预训练向量。

- Wikipedia 2014 + Gigaword 5: 6B tokens, 400K vocab, 50d/100d/200d/300d vectors — 维基百科2014+Gigaword 5：60亿token，40万词表，50/100/200/300维向量
- Common Crawl (42B tokens): 1.9M vocab, 300d — Common Crawl（420亿token）：190万词表，300维
- Common Crawl (840B tokens): 2.2M vocab, 300d — Common Crawl（8400亿token）：220万词表，300维
- Twitter (2B tweets, 27B tokens): 1.2M vocab, 25d/50d/100d/200d — Twitter（20亿推文，270亿token）：120万词表


---

## 10. FastText模型 (FastText Model)

### 10.1 OOV问题与FastText方案 (OOV Problem & FastText Solution)

![Page 44](lecture4_slides_pages/page_044.png)

**Dealing with OOV:** Traditional methods to handle Out-of-Vocabulary words, and FastText as a better solution. — 处理OOV的传统方法以及FastText作为更好的解决方案。

- Use a Default Vector — 使用默认向量
- Fallback to a Similar Word — 回退到相似词
- Train Your Own Embeddings — 训练自己的嵌入
- **Better Solution: The FastText Model** — **更好的解决方案：FastText模型**

### 10.2 FastText概述 (FastText Overview)

![Page 45](lecture4_slides_pages/page_045.png)

**The FastText Model:** Introduced by Facebook in 2016 as an extension of Word2Vec. — Facebook于2016年推出，作为Word2Vec的扩展。

- Introduced by Facebook in 2016 as an extension and supposedly improvement of the vanilla Word2Vec model — Facebook于2016年作为Word2Vec的扩展和改进推出
- Framework for learning word representations and performing robust, fast, and accurate text classifications — 用于学习词表示和执行鲁棒、快速、准确文本分类的框架

Ref: Bojanowski et al., 2017 — Enriching Word Vectors with Subword Information | https://fasttext.cc/

### 10.3 子词生成 (Subword Generation)

![Page 46](lecture4_slides_pages/page_046.png)

**FastText: Sub-word generation:** Diagram showing how a word is decomposed into character n-grams. — 图示词如何被分解为字符n-gram。

Ref: https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.vec.gz

![Page 47](lecture4_slides_pages/page_047.png)

**FastText: Subword Generation Detail:** — FastText子词生成详情。

- For a word, we generate character n-grams of length 3 to 6 present in it — 对一个词，生成其中长度3到6的字符n-gram
- Two-step vector representation updating: — 两步向量表示更新：
  1. First, the embedding for the center word is calculated by taking a sum of vectors for the character n-grams and the whole word itself — 首先，中心词的嵌入通过对字符n-gram和整个词本身的向量求和来计算
  2. For the actual context words, we directly take their word vector from the embedding table without adding the character n-grams — 对于实际上下文词，直接从嵌入表中获取词向量，不添加字符n-gram

### 10.4 FastText优点 (FastText Advantages)

![Page 48](lecture4_slides_pages/page_048.png)

**Advantages of FastText:** — FastText的优点。

- Capture fine level more gradual information — 捕获更细粒度的信息
- Solve OOV — 解决OOV问题
- Open-source, free, lightweight library — 开源、免费、轻量级库
- Handle text data in various languages — 处理多种语言的文本数据
- Has a simple and intuitive API — 有简单直观的API


---

## 11. 词嵌入优缺点总结 (Word Embedding Benefits & Limitations)

![Page 49](lecture4_slides_pages/page_049.png)

**Word Embedding: Benefits:** Four key benefits. — 词嵌入的四个关键优点。

- Dimensionality reduction — 降维
- Semantic meaning — 语义含义
- Handling Out-of-Vocabulary (OOV) — 处理OOV（FastText）
- Transfer learning — 迁移学习
- → Improved Performance On NLP Tasks — → 在NLP任务上性能提升

![Page 50](lecture4_slides_pages/page_050.png)

**Word Embedding - Limitations:** Six key limitations. — 词嵌入的六个关键局限性。

- Context Insensitivity — 上下文不敏感
- Bias — 偏见
- Limited Semantic Adaptation — 有限的语义适应
- Dimensionality — 维度
- Resource Intensive — 资源密集
- OOV words — OOV问题


---

## 12. 通用文本表示与评估 (Universal Text Representations & Evaluation)

![Page 51](lecture4_slides_pages/page_051.png)

**Universal Text Representations:** Preview of next-generation contextual models. — 下一代上下文模型预告。

- Contextual word representations — 上下文词表示
- Advanced neural language models — 高级神经语言模型
- Complex architectures involving multiple passes through the text and multiple reads from left to right and right to left to model the context of language — 复杂架构，涉及对文本的多次遍历和从左到右、从右到左的多次读取以建模语言上下文
- ELMo, BERT, ULMFiT — ELMo、BERT、ULMFiT

![Page 52](lecture4_slides_pages/page_052.png)

**Word Embedding - Evaluation:** Two evaluation methods. — 两种评估方法。

1. **Intrinsic Evaluation** — Assessing quality independently of any specific task. Focus on internal properties: Word Similarity, Analogy Tasks, … — **内在评估** — 独立于任何特定任务评估质量。关注内部属性：词相似度、类比任务等
2. **Extrinsic Evaluation** — Assessing quality based on performance in downstream NLP tasks like: Text classification, NER, etc. — **外在评估** — 基于下游NLP任务（文本分类、NER等）的性能评估质量


---

## 13. 本周总结 (Week Summary)

![Page 53](lecture4_slides_pages/page_053.png)

**Week 4 Summary:** — 第4周总结。

- ❖ WordNet and word senses — WordNet与词义
- ❖ Distributed representation — 分布式表示
- ❖ Word Embedding — 词嵌入
- ❖ Word2Vec — Word2Vec
- ❖ GloVe — GloVe
- ❖ FastText — FastText
- ❖ Evaluation of Word Embeddings — 词嵌入评估
- ❖ Problems with Word Embedding — 词嵌入的问题

![Page 54](lecture4_slides_pages/page_054.png)

**Q&A** — 问答环节
