# Lab 3 概念速查 | Concept Quick Reference

> 速查卡：核心定义 + 关键对比 + 常见陷阱
> 详细推导见：[lab3_tutorial.md](./lab3_tutorial.md) | 故事线：[lab3_storyline.md](./lab3_storyline.md)

---

## Part 1 核心术语

| 术语                                         | 定义                                                 | 关键点                                |
| -------------------------------------------- | ---------------------------------------------------- | ------------------------------------- |
| **词嵌入 Word Embedding**              | 将词映射到稠密低维向量空间$f: V \to \mathbb{R}^d$  | 语义相似的词距离更近                  |
| **分布假说 Distributional Hypothesis** | 出现在相似上下文的词有相似含义（Firth, 1957）        | "一个词由它的同伴定义"                |
| **SimLex-999**                         | 人工标注的 999 个词对语义相似度基准数据集（0–10分） | ⚠️ 衡量相似性，不是相关性           |
| **内在评估 Intrinsic Evaluation**      | 直接评估词向量质量（相似度、类比），不依赖下游任务   | 快速但不反映实际应用                  |
| **外在评估 Extrinsic Evaluation**      | 在下游任务（情感分析、NER）上评估                    | 慢，但反映真实价值                    |
| **OOV (Out-of-Vocabulary, 未登录词)**  | 不在模型词汇表中的词                                 | Word2Vec/GloVe 无法处理               |
| **余弦相似度 Cosine Similarity**       | 衡量两向量方向相似程度                               | 不受向量长度（词频）影响              |
| **Pearson 相关系数**                   | 衡量两数值序列的线性相关程度（$[-1,1]$）           | 在 Lab 评估中量化"嵌入 vs 人类"一致性 |

---

## 三模型核心对比

|                      | **Word2Vec**        | **GloVe**           | **FastText**                  |
| -------------------- | ------------------------- | ------------------------- | ----------------------------------- |
| **提出者/年**  | Mikolov et al. / 2013     | Pennington et al. / 2014  | Bojanowski et al. / 2016 (Facebook) |
| **训练方式**   | 预测（神经网络）          | 计数 + 矩阵分解           | Word2Vec 扩展 + 字符 n-gram         |
| **视野**       | 局部滑动窗口              | 全局共现矩阵              | 局部窗口 + 子词                     |
| **OOV 处理**   | ❌                        | ❌                        | ✅ n-gram 合成                      |
| **拼写错误**   | ❌ 返回 None              | ❌ 返回 None              | ✅ 高相似度（共享 n-gram）          |
| **Lab 3 模型** | word2vec-google-news-300  | glove-wiki-gigaword-300   | cc.en.300.bin                       |
| **词汇量**     | 3M                        | 400K                      | 2M                                  |
| **训练数据**   | Google News               | Wikipedia + Gigaword      | Common Crawl                        |
| **Lab 1 优势** | 专业词（attorney/lawyer） | 描述词（boundary/border） | —                                  |

---

## Part 1: Intrinsic Evaluation 关键概念

| 概念                               | 说明                                                      |
| ---------------------------------- | --------------------------------------------------------- |
| **Top 60 词对**              | SimLex-999 中最高相似度（≥8.72）的 60 对词               |
| **"相似" ≠ "相关"**         | coffee/cup：相关但不相似；smart/intelligent：既相关又相似 |
| **词嵌入系统性低估**         | 词向量余弦相似度普遍低于 SimLex999 归一化值               |
| **vanish ↔ disappear 分高** | 几乎只出现在相同语境，共现模式高度重叠（W2V: 0.90）       |
| **quick ↔ rapid 分低**      | 语境不同（口语 vs 正式），向量方向分离（W2V: 0.50）       |

---

## Part 2: FastText & Analogy 关键概念

| 概念                              | 说明                                                                                      |
| --------------------------------- | ----------------------------------------------------------------------------------------- |
| **字符 n-gram**             | 词被分解为长度 3–6 的字符片段，加词边界标记 `<` `>`                                  |
| **子词合成**                | 词向量 = 所有 n-gram 向量之和，OOV 词可通过共享 n-gram 获得向量                           |
| **词类比 Word Analogy**     | $\text{vec}(A) - \text{vec}(B) + \text{vec}(C) \approx \text{vec}(D)$，语义方向编码关系 |
| **性别偏见**                | 训练数据中的统计偏差被编码进向量，类比运算放大偏见                                        |
| **语义漂移 Semantic Drift** | 类比运算过度减法可能丢失语义（Intelligent - Scientist 几乎消除"智力"）                    |
| **高相似度阈值**            | FastText: banana/bananna = 0.78（大量共享 n-gram）                                        |
| **低相似度陷阱**            | FastText: science/sciience = 0.07（插入字符破坏 n-gram 链）                               |

---

## ⚠️ 常见考试陷阱

1. **余弦相似度 vs 欧式距离：** 词向量用余弦（忽略长度/词频），不用欧式！
2. **SimLex-999 的相似性：** 只衡量语义相似，不是相关性。coffee/cup → **低分**。
3. **Word2Vec 遇到 OOV：** 不会报错但返回 None，代码必须先检查 `key_to_index`！
4. **FastText 也不是万能：** 极端拼写错误（sciience）n-gram 共享率低，相似度也极低。
5. **偏见不只是 FastText 的问题：** Word2Vec 和 GloVe 同样有性别偏见，甚至更严重。
6. **词类比搜索范围的影响：** 限制 50,000 词可能漏掉正确答案（低频词）。
