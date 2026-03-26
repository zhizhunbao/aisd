---
topic: word_vectors
dimension: bridge
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.6, 9-10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📖 Paper: Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
expiry: 12m
status: current
---

# Word Vectors 衔接与扩展

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6, 9-10

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 文本预处理 (text_preprocessing) | 分词后的 token 序列是词向量的输入 | — |
| ← 前置 | 语言模型 (language_models) | N-gram/神经 LM 为 Word2Vec 提供理论基础 | — |
| → 后续 | Transformer | 词嵌入+位置编码是 Transformer 输入层 | [transformer/](../transformer/transformer_map.md) |
| → 后续 | BERT | Word2Vec 的静态嵌入被 BERT 的上下文嵌入取代 | [bert/](../bert/) |
| → 后续 | GPT | GPT 的 token embedding 继承了词嵌入思想 | [gpt/](../gpt/) |
| → 后续 | 序列模型 (rnn_seq_models) | 词向量作为 RNN/LSTM 的输入嵌入层 | — |

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6, Ch.9

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| 线性代数 | 矩阵乘法、SVD、内积 | 共现矩阵分解 (LSA)、Word2Vec 的嵌入查找、余弦相似度计算 |
| 概率与统计 | 条件概率、最大似然、交叉熵 | Skip-gram 目标函数：P(context \| center) 的 Softmax 建模 |
| 分布假说 (语言学) | "上下文定义语义" | Word2Vec/GloVe 的全部理论基础——从共现中学语义 |
| 文本预处理 | 分词 (Tokenization) | 词表构建、上下文窗口生成的前提 |
| 信息论 | PMI (Pointwise Mutual Information) | SGNS 隐式分解 PMI 矩阵 (Levy & Goldberg 2014) |

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.3-6.8

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| RNN / LSTM / GRU | 预训练词嵌入层 | 用 Word2Vec/GloVe 初始化嵌入矩阵，作为序列模型的输入特征 |
| Transformer | Embedding 层概念 | Transformer 的 Input Embedding = 可学习的词嵌入 + 位置编码 |
| BERT | 静态 → 上下文嵌入的演变 | BERT 用 Transformer Encoder 替代静态嵌入，但 token embedding 层仍是类似的查找表 |
| GPT | Token Embedding 层 | GPT 的输入层 = token embedding(继承自 Word2Vec 思想) + position embedding |
| 文本分类 / 情感分析 | 词向量作为特征 | 用预训练词向量初始化文本分类器的嵌入层，比随机初始化效果显著提升 |
| 信息检索 | 语义相似度 | 用词向量的余弦相似度度量查询-文档的语义匹配（稠密检索的基础） |
| 推荐系统 | Embedding 思想泛化 | Item2Vec (Barkan & Koenigstein 2016) 把 Word2Vec 思想用于商品推荐 |
| 图神经网络 | Node Embedding | Node2Vec (Grover & Leskovec 2016) 把 Skip-gram 思想用于图节点表示 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.4 "Embeddings and Softmax"
> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 词表示 | 稀疏 One-Hot (V 维) | 稠密嵌入 (d 维, d << V) | 维度灾难 + 语义缺失推动降维 |
| 词向量 | 静态 (每词一个固定向量) | 上下文相关 (每次出现不同向量) | 一词多义问题推动上下文化 |
| 嵌入训练 | 单独预训练 + 下游任务固定不训练 | 端到端微调 (预训练+fine-tune) | BERT/GPT 范式转移 |
| 子词处理 | 整词级别 (OOV=零向量) | 子词分词 (BPE/WordPiece) | OOV + 形态丰富语言推动子词化 |
| 嵌入层角色 | 独立的特征提取器 | 端到端模型的第一层 | 深度学习范式统一了特征和分类 |
| 评估方式 | 词类比 + 相似度 | 下游任务 (GLUE/SuperGLUE) | 内在评估不一定和下游表现一致 |

> 📖 Paper: Peters et al., [ELMo (2018)](https://arxiv.org/abs/1802.05365)
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.12

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Levy & Goldberg "Neural Word Embedding as Implicit Matrix Factorization" (2014)](https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html) | 📖 论文 | 证明 SGNS = PMI 矩阵分解，统一了计数和预测方法 | ⭐⭐⭐ |
| [Levy, Goldberg & Dagan "Improving Distributional Similarity" (2015)](https://aclanthology.org/Q15-1016/) | 📖 论文 | 系统对比 Word2Vec/GloVe/SVD，发现超参数比算法更重要 | ⭐⭐⭐ |
| [Bolukbasi et al. "Man is to Computer Programmer as Woman is to Homemaker?" (2016)](https://arxiv.org/abs/1607.06520) | 📖 论文 | 词向量偏见检测和去偏方法 | ⭐⭐ |
| [Goldberg "A Primer on Neural Network Models for NLP" (2016)](https://arxiv.org/abs/1510.00726) | 📖 论文 | Word2Vec 的数学推导教程 | ⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [FastText 官方文档](https://fasttext.cc/docs/en/support.html) | Word2Vec vs FastText（子词处理） | 需要处理 OOV 或形态丰富语言时 |
| [Sentence-BERT](https://arxiv.org/abs/1908.10084) | 词级嵌入 vs 句子级嵌入 | 需要句子/文档相似度时 |
| [Item2Vec](https://arxiv.org/abs/1603.04259) | 词嵌入 vs 商品嵌入 | 研究推荐系统时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [CS224N Lecture 1-2](https://web.stanford.edu/class/cs224n/) | Stanford NLP 课程词向量章节 | 系统学习 NLP 时 |
| [Transformer 知识地图](../transformer/transformer_map.md) | 理解 Transformer 如何使用嵌入层 | 学完词向量后进入下一阶段 |
| [BERT 知识地图](../bert/) | 理解上下文嵌入如何取代静态嵌入 | 深入预训练模型时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| NLP 课程同主题 | 3 | Transformer, BERT, GPT | 词嵌入 → Transformer Input Embedding → 上下文嵌入 |
| 深度学习基础 | — | 前向传播, 神经网络 | SGD, 损失函数, 嵌入层 = nn.Embedding |
| 机器学习基础 | — | 降维, 矩阵分解 | SVD = LSA 的核心, PCA 可视化词向量 |
