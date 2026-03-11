---
topic: retrieval_lab
dimension: history
created: 2026-03-11
last_verified: 2026-03-11
source_versions:
  - "📚 Book: [manning_intro_to_ir.pdf](../../textbooks/manning_intro_to_ir.pdf) — Ch.1, Ch.6, Ch.11"
  - "📖 Docs: [RRF Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)"
expiry: 12m
status: current
---

# 检索技术演变史 (Retrieval Evolution)

> 📚 Book: Manning et al., [《Introduction to IR》](../../textbooks/manning_intro_to_ir.pdf) (Ch.1, 6, 11)阐述了从布尔检索到概率检索的演进过程。了解历史能更深刻理解 `retrieval_lab` 中各种方法的意义。

---


## 一、为什么要研究检索方法？

在没有搜索引擎或向量数据库之前，人们如何在大量文档中找到需要的信息？

最早的方法很简单：“只要文档里有这几个字，我就要看”。但随之而来三个致命问题：
1. **找不到全貌**：查询必须一字不差（如搜“小狗”找不到“柴犬”或“canine”）。
2. **相关性不一**：文章只是顺带提了一句“苹果”，也被算作匹配，却排在一个满世界种苹果的文章之前。
3. **篇幅偏差**：如果一本书有 1000 页，只要它足够长，总会有命中关键词的零散废话，长文本优势过大。

为了解决这些“笨检索”带来的混乱，检索技术开始了从**完全词法匹配**，到**概率优化**，再到**多路融合**，乃至**AI语义理解**的漫长演变。

---


## 二、技术演进列车 (The Evolution Train)

### Station 1: 布尔与简单 TF (Term Frequency) 时代

起初，检索是二元的（Boolean Retrieval）：
- `(mac AND cheese) OR (pasta AND cheese)`
如果匹配就召回，不匹配就丢弃。

后来，人们意识到“频次”重要性，提出了**词频 (TF)**。在文档里出现 10 次的词肯定比出现 1 次的重要。

**致命缺陷：**
- **无法区分通用词与稀有词**。“的”、“是”出现成败上千次，压过了真正体现主题的专有名词（如“贝叶斯”）。
- 把文章复制几遍，相似度直接翻番，毫无意义。

> 📚 Book: Manning et al., Ch.1 Boolean Retrieval & Ch.6 Term Frequency

### Station 2: TF-IDF 模型（基于频率和逆文档稀缺性）

为了压制“常用废话”，人们引入了 **逆文档频率 (IDF)** 的概念：
> $IDF = \log(N / n)$
某个词包含的文档 $n$ 越多，它的稀少性优势越弱（值越低），最后那些全文档满天飞的停用词就失去了得分权重。

**TF-IDF 解决了“通用词捣乱”问题。**

**致命缺陷：**
- **依然没有长度惩罚**。长文章只是由于自然拼凑就比短文章多得分，哪怕其核心主旨与查询毫无关系。
- **词频没有上限**。出现100遍就比只出现10遍有用吗？并没有，边际效应递减被忽视了。

### Station 3: BM25（概率信息检索基石）

20世纪90年代推出的 **Okapi BM25** 模型正式引爆了工业界。它在 TF-IDF 基础上修补了两个最大的雷：
1. **词频饱和 ($k_1$)**：使用非线性增长控制了单纯出现的堆词现象，到了某个点后再多出现该词也只给予有限增量分。
2. **长度归一化 ($b$)**：对比整库的平均文档长度。如果你比平均水平长，我就狠狠惩罚你的长篇大论带来的冗余匹配。

**目前处于这个阶段的技术：**
- Elasticsearch 默认搜索内核。
- `retrieval_lab` 中的 `BM25Retriever`，以最精简的极简包 `rank_bm25` 直接使用此历史瑰宝跑全文比对。

> 📚 Book: Manning et al., Ch.11 Probabilistic Information Retrieval (Okapi BM25)

### Station 4: PageIndex 与结构化 TOC 匹配

随着书籍或网页拥有了强大的“文档树”结构标签功能，人们意识到：如果关键词直接出现在**标题 (Heading/Title)** 中，这篇文档的相关性大概率远碾压于全文搜索中只有零散引用的句子。

如果把检索重点从“全文堆砌”转移到“章节大纲骨架”上，我们得到了**TOC匹配法**。这种基于先验假设的方法非常快速和硬核，解决大部头教科书时极度精准。

**项目中对应代码：**
`retrieval_lab` 中的 `TOCRetriever` 和 `PageIndexRetriever` 就是这派技术的具像化，将人类编辑出的高质量树状大纲当做了最佳作弊码。

### Station 5: Neural Information Retrieval (NLP与向量时代)

时代进入了由神经网络和Transformer统治的新世纪。既然机器能读懂上下文，“dog”可以被编码在空间里距离“canine”或“puppy”非常接近，我们就再不需要和具体的 ASCII 字符串拼刺刀了。

**Embedding (嵌入向量) + Cosine Similarity (余弦相似度)** 成为了标准范式，人们把这种检索过程叫做“语义相似度检索”。

**项目中对应代码：**
`retrieval_lab` 中的 `VectorRetriever` 便是当前时代的极简缩影。通过 OLLAMA 的本地 `nomic-embed-text` 推理接口生成浮点向量并用 Numpy `a @ b` 最速取 top K。它是 RAG (Retrieval-Augmented Generation) 架构的前向抓手。

### Station 6: 混合多路召回与融合排名 (Hybrid & Ensemble RRF)

到了现代工业级搜索引擎，大家发现没有任何一个单一模型是无敌的：
- BM25 对“特定生僻专有名词/代号/异常字符”找得超准（词汇稀缺）；
- Vector 对“模糊的软性自然语言描述/同义字”抓得极好（语义接近）。

那何不它们一起上，最后再合并榜单（Rank Fusion）呢？不同打分尺度不同能直接加点吗？当然不行（余弦是 0\~1，BM25 是 0\~60）。于是就有了简单的名次倒数求和算法：**Reciprocal Rank Fusion (RRF)**。在2009年发表后因其参数免费、无需再训练权重的特性，统治了混合检索圈。

**项目中对应代码：**
`retrieval_lab` 的终极归宿 `EnsembleRetriever`，用 `rrf_k` (默认60) 来加权平均汇总 TOC、BM25 和 Vector。完美再现了当代理念体系。

> 📖 Docs: Cormack et al. (2009). [Reciprocal Rank Fusion outperforms CombANZ and Borda Count](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)

---


## 三、Retrieval Lab 在历史长河里的位置

在深入阅读和手撸了上述这六代的源码后，你可以体会：

- 我们的 `run_query.py` 将这一部部的进化史打包在了一个不到千行的脚本库中。
- 当你在运行 `--method bm25` 然后转为 `--method vector` 最后再跑完整的 `--method ensemble` 时，实际上你是在经历过去信息检索整整三十年的**基建浓缩进程**。

> 思考：未来的 Retriever 还会有哪类呢？大模型直接生成的知识库 (Model Memory) 是否会替代掉外挂的 `data/` 文件呢？这是 Bridge 维度探索的话题。
