---
topic: word_vectors
dimension: map
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space', ICLR Workshop 2013 — https://arxiv.org/abs/1301.3781"
  - "📖 Paper: Mikolov et al., 'Distributed Representations of Words and Phrases and their Compositionality', NeurIPS 2013 — https://arxiv.org/abs/1310.4546"
  - "📖 Paper: Pennington et al., 'GloVe: Global Vectors for Word Representation', EMNLP 2014 — https://nlp.stanford.edu/pubs/glove.pdf"
  - "📖 Paper: Bojanowski et al., 'Enriching Word Vectors with Subword Information', TACL 2017 — https://arxiv.org/abs/1607.04606"
  - "📖 Paper: Peters et al., 'Deep contextualized word representations' (ELMo), NAACL 2018 — https://arxiv.org/abs/1802.05365"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Eisenstein, 《Natural Language Processing》, Ch.14 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/eisenstein_nlp.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》, Ch.12 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Word Vectors 知识地图

> 📚 Book: Jurafsky & Martin, [《Speech and Language Processing》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 "Vector Semantics and Embeddings"
> 📖 Paper: Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781), ICLR 2013
> 📖 Paper: Pennington et al., [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf), EMNLP 2014

## 1. 核心问题

- **词向量到底是什么？** → 把每个词映射成一个稠密的、低维的实数向量（通常 100-300 维），让语义相近的词在向量空间中距离相近。例如 "king" 和 "queen" 的向量比 "king" 和 "apple" 的向量更接近
- **为什么不能直接用独热编码（One-Hot）？** → 独热编码的每个词都是正交的（内积为 0），完全无法表达词与词之间的语义关系，而且维度等于词表大小（通常 10 万+），极度稀疏浪费
- **Word2Vec 的核心思想是什么？** → "你能通过一个词的邻居来了解这个词"（Distributional Hypothesis, Firth 1957）。Word2Vec 训练一个浅层神经网络，让目标词和上下文词的向量尽量接近，不相关的词向量尽量远离
- **GloVe 和 Word2Vec 有什么区别？** → Word2Vec 是局部预测模型（逐窗口扫描语料），GloVe 是全局统计模型（先构建全局共现矩阵，再做矩阵分解）。GloVe 的名字就是 "Global Vectors" 的缩写
- **静态词向量的致命缺陷是什么？** → 每个词只有一个固定向量——"bank" 在 "river bank" 和 "bank account" 中获得完全相同的表示，无法处理一词多义。ELMo 和后续的 BERT/GPT 用上下文相关表示解决了这个问题

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 "Vector Semantics and Embeddings"
> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §1-3

---

## 2. 全景位置

```
自然语言处理 NLP
├── 传统方法
│   ├── 规则系统 / 手工特征
│   ├── N-gram 语言模型
│   └── TF-IDF + 逻辑回归
├── 词向量与表示 ← 你在这里
│   ├── 稀疏表示
│   │   ├── One-Hot Encoding (维度 = 词表大小, 正交无语义)
│   │   ├── Bag of Words (忽略词序)
│   │   └── TF-IDF (加权统计)
│   ├── 基于计数的稠密表示
│   │   ├── SVD on Co-occurrence Matrix (截断 SVD 降维)
│   │   └── 【GloVe】 (全局共现矩阵分解, Pennington 2014)
│   ├── 基于预测的稠密表示
│   │   ├── 【Word2Vec CBOW】 (上下文预测中心词, Mikolov 2013)
│   │   ├── 【Word2Vec Skip-gram】 (中心词预测上下文, Mikolov 2013)
│   │   └── 【FastText】 (子词 n-gram, Bojanowski 2017)
│   └── 上下文相关表示
│       ├── 【ELMo】 (双向 LSTM 语境嵌入, Peters 2018)
│       └── → BERT / GPT (Transformer 语境嵌入)
├── 序列模型时代
│   ├── RNN / LSTM / GRU
│   └── Seq2Seq + Attention
├── Transformer 架构
│   └── Self-Attention / Multi-Head Attention
└── 预训练语言模型
    ├── BERT / GPT / T5
    └── LLM (GPT-4, LLaMA, Claude)
```

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.1-6.12
> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §1 "Introduction"

---

## 3. 依赖地图

```
前置知识                       本主题                         后续方向
┌───────────────────────┐     ┌────────────────────────┐     ┌───────────────────────────┐
│ 线性代数               │────→│                        │────→│ RNN / LSTM / GRU           │
│ (矩阵乘法, SVD, 内积)  │     │                        │     │ (词向量作为输入嵌入)        │
├───────────────────────┤     │                        │────→│ Transformer                │
│ 概率与统计             │────→│   Word Vectors         │     │ (Input Embedding 层)       │
│ (条件概率, 交叉熵)     │     │   (Word2Vec / GloVe /  │────→│ BERT / GPT                 │
├───────────────────────┤     │    FastText / ELMo)    │     │ (上下文嵌入取代静态嵌入)    │
│ 分布假说               │────→│                        │────→│ 文本分类 / 情感分析         │
│ (Firth 1957)          │     │                        │     │ (预训练向量作为特征)        │
├───────────────────────┤     │                        │────→│ 信息检索 / 推荐系统         │
│ 语料库与分词            │────→│                        │     │ (语义相似度匹配)           │
│ (Tokenization)        │     │                        │     │                           │
└───────────────────────┘     └────────────────────────┘     └───────────────────────────┘
```

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6
> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §1-4

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [word_vectors_map.md](word_vectors_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [word_vectors_concepts.md](word_vectors_concepts.md) | ② 概念 | 理解 Word2Vec/GloVe/FastText/ELMo 等术语 |
| [word_vectors_math.md](word_vectors_math.md) | ③ 公式 | 推导 Skip-gram 目标函数、负采样、GloVe 代价函数 |
| [word_vectors_tutorial.md](word_vectors_tutorial.md) | ④ 教程 | Why-First 理解词向量的设计动机与原理 |
| [word_vectors_code.md](word_vectors_code.md) | ⑤ 代码 | 快速上手 Gensim/PyTorch 训练词向量 |
| [word_vectors_pitfalls.md](word_vectors_pitfalls.md) | ⑥ 踩坑 | 词表溢出/OOV/类比失败/偏见等常见问题 |
| [word_vectors_history.md](word_vectors_history.md) | ⑦ 历史 | 从 One-Hot 到 Word2Vec 到 ELMo 的技术演进 |
| [word_vectors_bridge.md](word_vectors_bridge.md) | ⑧ 衔接 | 连接 Transformer / BERT / GPT / 下游任务 |
| [word_vectors_first_principles.md](word_vectors_first_principles.md) | ⑨ 第一性原理 | 追问"为什么上下文能定义语义" |

> 📖 Docs: Norman, 《The Design of Everyday Things》(2013), Ch.3 "Knowledge in the World"

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [word_vectors_map.md](word_vectors_map.md) 了解词向量在 NLP 全景中的位置
2. 读 [word_vectors_tutorial.md](word_vectors_tutorial.md) Section 1 理解"为什么需要词向量"
3. 读 [word_vectors_concepts.md](word_vectors_concepts.md) 掌握分布假说 / Word2Vec / GloVe / 负采样等核心术语
4. 读 [word_vectors_math.md](word_vectors_math.md) 手算一次 Skip-gram + 负采样的梯度
5. 跟 [word_vectors_code.md](word_vectors_code.md) 用 Gensim 30 秒加载预训练词向量
6. 读 [word_vectors_history.md](word_vectors_history.md) 了解从稀疏表示到稠密嵌入的技术演进
7. 读 [word_vectors_first_principles.md](word_vectors_first_principles.md) 追问分布假说的根基

### 日常参考 🔧

1. 查 [word_vectors_code.md](word_vectors_code.md) Gensim / PyTorch API 速查表
2. 查 [word_vectors_math.md](word_vectors_math.md) 目标函数和损失函数速查
3. 查 [word_vectors_pitfalls.md](word_vectors_pitfalls.md) 排查 OOV / 偏见 / 训练不收敛问题

### 深度研究 🔬

1. 读 [word_vectors_history.md](word_vectors_history.md) 完整演进线
2. 读 [word_vectors_first_principles.md](word_vectors_first_principles.md) 追问"向量空间语义学"的哲学根基
3. 读 [word_vectors_bridge.md](word_vectors_bridge.md) 对比静态嵌入 vs 上下文嵌入
4. 阅读原始论文 [Word2Vec](https://arxiv.org/abs/1301.3781) 和 [GloVe](https://nlp.stanford.edu/pubs/glove.pdf)

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-24 | 12m | ✅ current |
| Concepts | 2026-03-24 | 12m | ✅ current |
| Math | 2026-03-24 | 12m | ✅ current |
| Tutorial | 2026-03-24 | 12m | ✅ current |
| Code | 2026-03-24 | 6m | ✅ current |
| Pitfalls | 2026-03-24 | 6m | ✅ current |
| History | 2026-03-24 | never | ✅ current |
| Bridge | 2026-03-24 | 12m | ✅ current |
| First Principles | 2026-03-24 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Mikolov et al. "Efficient Estimation of Word Representations in Vector Space" (2013)](https://arxiv.org/abs/1301.3781) | 📖 论文 | 全文核心参考——Word2Vec (CBOW + Skip-gram) 原始论文 |
| [Mikolov et al. "Distributed Representations of Words and Phrases" (2013)](https://arxiv.org/abs/1310.4546) | 📖 论文 | Math, Tutorial——负采样、层次 Softmax、短语嵌入 |
| [Pennington et al. "GloVe: Global Vectors for Word Representation" (2014)](https://nlp.stanford.edu/pubs/glove.pdf) | 📖 论文 | Concepts, Math, History——GloVe 共现矩阵分解 |
| [Bojanowski et al. "Enriching Word Vectors with Subword Information" (2017)](https://arxiv.org/abs/1607.04606) | 📖 论文 | Concepts, Code——FastText 子词 n-gram |
| [Peters et al. "Deep contextualized word representations" (ELMo, 2018)](https://arxiv.org/abs/1802.05365) | 📖 论文 | Concepts, History, Bridge——上下文相关嵌入 |
| [《SLP3》Ch.6](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 📚 教科书 | Vector Semantics and Embeddings 全章 |
| [《NLP》Ch.14](../../../textbooks/eisenstein_nlp.pdf) | 📚 教科书 | 词表示理论与数学推导 |
| [《Deep Learning》Ch.12](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 表示学习基础理论 |
| [Gensim Word2Vec Docs](https://radimrehurek.com/gensim/models/word2vec.html) | 📖 文档 | Code——API 接口和使用方法 |
| [PyTorch nn.Embedding Docs](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html) | 📖 文档 | Code——嵌入层实现 |
