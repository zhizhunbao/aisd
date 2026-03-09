# Lab 3 命名由来与历史 | Name Origins & History

> 回答："为什么叫这个名字？谁起的？什么时候？"  
> 建立元知识——不只记住公式，还知道它们从何而来。
>
> **所属 Lab：** [Lab 3 词嵌入](../labs/CST8507_Lab_3_W26.md)  
> **配套故事线：** [lab3_storyline.md](./lab3_storyline.md)  
> **配套教程：** [lab3_tutorial.md](./lab3_tutorial.md)

---

## 分布假说 Distributional Hypothesis

**谁起的名：** 英国语言学家 **J.R. Firth**（1957），语录：_"You shall know a word by the company it keeps."_  
**为什么这样叫：** "Distributional"（分布的）来自统计学——词在语料库中的出现**分布**（哪些上下文里出现）决定了它的含义。  
**历史意义：** 这句话在 1950 年代几乎只是文学观察，直到 2000 年代深度学习崛起，才被计算化为词嵌入的理论基础。

---

## Word2Vec

**谁起的名：** Google 研究员 **Tomáš Mikolov**，2013 年论文 _"Efficient Estimation of Word Representations in Vector Space"_。  
**名字含义：** "Word" → 处理对象（词）；"2" → to（转换为）；"Vec" → Vector（向量）。直白地描述功能：把词转成向量。  
**为什么 2013 年是转折点：** Mikolov 的创新不是"词嵌入"概念（更早有神经语言模型），而是用**负采样（Negative Sampling）** 把训练从几天压缩到几小时，第一次让大规模词嵌入实用化。  
**Google News 模型：** 论文发布后 Google 开放了在 1000 亿词 Google News 上训练的 300 维预训练模型（即 Lab 3 使用的 `word2vec-google-news-300`），这是第一个被广泛使用的预训练 NLP 模型。

---

## GloVe (Global Vectors for Word Representation)

**谁起的名：** Stanford NLP Group：**Jeffrey Pennington**, Richard Socher, Christopher Manning，2014 年 EMNLP 论文。  
**名字含义：** "Global"（全局）是关键词——与 Word2Vec 只看局部窗口相对，GloVe 利用**全局**共现矩阵。英文名 GloVe 也恰好是手套的意思（一个恰当的比喻：手套"包裹"整个语料库）。  
**为什么 Manning 组做：** Christopher Manning 是斯坦福 NLP 实验室的权威，一直批评纯预测方法忽略全局统计。GloVe 是他们对 Word2Vec "只看局部"的直接回应，试图将计数方法（SVD）和预测方法的优点合并。

---

## FastText

**谁起的名：** Facebook AI Research (FAIR)，核心作者 **Piotr Bojanowski**, Edouard Grave, Armand Joulin, Tomáš Mikolov（是的，Mikolov 离开 Google 后加入了 Facebook）。2016–2017 年论文 _"Enriching Word Vectors with Subword Information"_。  
**名字含义：** "Fast"（快）+ "Text"（文本）——强调其在文本分类任务上速度极快（也是一个文本分类工具，不只是词嵌入工具）；同时子词方法让训练在形态复杂语言（如土耳其语）上也"更快"收敛。  
**为什么叫"子词"而不是"字符"：** 字符（character）是单个字母，子词（subword / character n-gram）是字母序列片段。"子词"是一个更准确的术语：它比字符更有语义，比完整词更小，处于两者之间的粒度。  
**cc.en.300 模型：** Lab 3 使用的 `cc.en.300.bin` 是在 **Common Crawl**（互联网爬虫数据，6500 亿 token）上训练的 300 维英文模型，Facebook 开放下载，是业界常用的强基线。

---

## SimLex-999

**谁起的名：** **Felix Hill**, Roi Reichart, Anna Korhonen，2015 年论文 _"SimLex-999: Evaluating Semantic Models with (Genuine) Similarity Estimation"_，剑桥大学团队。  
**名字含义：** "Sim"（Similarity，相似度）+ "Lex"（Lexical，词汇的）+ "999"（数据集的词对数量）。999 而不是 1000，是因为最终筛选后恰好保留了 999 对有效词对。  
**为什么要创建它：** 当时最流行的评估数据集 WordSimilarity-353（2002 年）混淆了"相似"和"相关"。SimLex-999 被专门设计来**只衡量真正的语义相似度**，是对 WS-353 的直接修正。

---

## 余弦相似度 Cosine Similarity

**历史来源：** "余弦相似度"这个名字来自三角学——向量夹角的余弦值。公式 $\cos\theta = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$ 在信息检索领域由 **Gerard Salton**（向量空间模型之父）在 1970–1980 年代推广用于文档相似度计算。  
**为什么叫"余弦"：** 内积 $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\| \|\mathbf{v}\| \cos\theta$，所以归一化内积恰好等于夹角的余弦——名字直接来自这个几何事实。  
**从文档到词：** Salton 最初用于文档向量（TF-IDF），后来被词嵌入领域直接借用，因为原理完全一样：用方向距离衡量语义距离。

---

## Pearson 相关系数

**谁起的名：** 英国统计学家 **Karl Pearson**（皮尔逊），约 1895–1900 年系统化了相关系数的概念（基于 Francis Galton 和 Auguste Bravais 的早期工作）。  
**为什么叫"皮尔逊"：** Pearson 是第一个给出 $r = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y}$ 这一形式并系统研究其统计性质的人，名字由此沿用。  
**Lab 3 的选择：** 使用 Pearson 而非 Spearman 相关系数，隐含假设嵌入相似度和人类评分之间存在**线性关系**。

---

## 词嵌入性别偏见的发现

**谁首次报告：** **Tolga Bolukbasi**, Kai-Wei Chang, James Zou, Venkatesh Saligrama, Adam Kalai，2016 年 NeurIPS 论文 _"Man is to Computer Programmer as Woman is to Homemaker?"_。  
**标题即论点：** 论文标题直接使用了 Word2Vec 的一个真实输出——"Man : Computer Programmer :: Woman : Homemaker"——以惊人的方式展示了词嵌入中存在的性别刻板印象。  
**历史意义：** 这篇论文启动了 NLP 公平性（Fairness in NLP）这一子领域，促使研究者开始系统研究 AI 中的社会偏见问题。
