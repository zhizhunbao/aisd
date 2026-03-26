---
topic: word_vectors
dimension: tutorial
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space', ICLR 2013 — https://arxiv.org/abs/1301.3781"
  - "📖 Paper: Pennington et al., 'GloVe: Global Vectors for Word Representation', EMNLP 2014 — https://nlp.stanford.edu/pubs/glove.pdf"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📖 Docs: Gensim Word2Vec — https://radimrehurek.com/gensim/models/word2vec.html"
expiry: 12m
status: current
---

# Word Vectors 教程

> **前置知识：** 线性代数（矩阵乘法、内积）、概率论（条件概率、Softmax）、梯度下降基础
> **参考来源：** Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6

---

## Section 0: 前置知识速查

1. **矩阵乘法**：两个矩阵相乘 $A_{m×k} \cdot B_{k×n} = C_{m×n}$，词嵌入查表本质是矩阵乘法
2. **内积/点积**：$\mathbf{u} \cdot \mathbf{v} = \sum u_i v_i$，衡量两个向量的"方向一致性"
3. **Softmax**：$\text{softmax}(z_i) = e^{z_i} / \sum_j e^{z_j}$，把任意实数分数转成概率分布
4. **Sigmoid**：$\sigma(x) = 1/(1+e^{-x})$，把实数压到 (0,1) 区间，用于二分类
5. **交叉熵损失**：$-\sum y_i \log \hat{y}_i$，衡量预测分布和真实分布的差距
6. **梯度下降 (SGD)**：$\theta \leftarrow \theta - \eta \nabla_\theta J$，沿损失函数梯度的反方向更新参数

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **痛点 1：独热编码无法表达语义相似性**。如果用 One-Hot 表示词，"cat" = [1,0,0,...], "dog" = [0,1,0,...]，两者的余弦相似度 = 0——但我们知道猫和狗都是动物，应该"比较相似"。One-Hot 把所有词视为完全独立的符号，丢失了全部语义信息
- 🔥 **痛点 2：维度灾难**。词表通常有 10 万+ 个词，One-Hot 就是 10 万维的向量，绝大多数元素为 0。下游模型（如分类器）根本无法高效处理如此高维稀疏的输入
- 🔥 **痛点 3：无法泛化到相似词**。训练数据中见过 "I love this movie"，但没见过 "I adore this film"。如果用 One-Hot，模型无法知道 love≈adore、movie≈film，必须对每个同义词组合都见过样本——这需要天文数量的训练数据
- 🔥 **痛点 4：TF-IDF 仍然是稀疏的**。虽然 TF-IDF 比 One-Hot 好（加了权重），但仍然是 V 维稀疏向量，仍然无法捕捉词语间的语义关系

### 它的核心价值

1. **语义编码**：相似词自动聚到向量空间的相近位置——cos(vec("happy"), vec("joyful")) ≈ 0.7，无需人工标注
2. **维度压缩**：从 V 维（~10 万）压到 d 维（~300），信息密度提升 300 倍
3. **迁移学习**：在大语料上预训练好的词向量可以直接用于小数据集的下游任务——即使任务训练数据很少，预训练向量已经编码了丰富的语言知识
4. **代数性质**：向量运算对应语义运算——"king" - "man" + "woman" ≈ "queen"，这为推理提供了计算工具

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.1-6.4
> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §1 "Introduction"

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 Word2Vec Skip-gram 训练流程

```
语料库: "the cat sat on the mat"
        ↓
┌──────────────────────────────────────────────────────┐
│ Step 1: 滑动窗口生成训练对 (window=2)                  │
│                                                      │
│  中心词="cat" → 上下文: {"the","sat"}                  │
│  中心词="sat" → 上下文: {"cat","on"}                   │
│  中心词="on"  → 上下文: {"sat","the"}                  │
│  ...                                                 │
│  正样本: (cat, the), (cat, sat), (sat, cat), ...     │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ Step 2: 对每个正样本,采 k 个负样本                      │
│                                                      │
│  正: (cat, sat) → σ(c_sat · w_cat) → 尽量=1          │
│  负: (cat, cloud) → σ(-c_cloud · w_cat) → 尽量=1     │
│  负: (cat, banana) → σ(-c_banana · w_cat) → 尽量=1   │
│  ...                                                 │
│  噪声分布: P_n(w) ∝ freq(w)^{3/4}                    │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ Step 3: SGD 更新两个嵌入矩阵                           │
│                                                      │
│  中心词矩阵 W ∈ R^{V×d}                               │
│  上下文矩阵 C ∈ R^{V×d}                               │
│  梯度: ∂J/∂w_cat, ∂J/∂c_sat, ∂J/∂c_cloud, ...      │
│  更新: w ← w - η·∇J                                  │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ Step 4: 训练完成后,取中心词矩阵 W (或 W+C 平均)        │
│                                                      │
│  最终词向量: W 的第 i 行 = 词 i 的 d 维嵌入             │
│  vec("cat") = W[cat_index, :]  (300维实数向量)         │
└──────────────────────────────────────────────────────┘
```

### 2.2 核心设计决策

**为什么用两个嵌入矩阵（W 和 C）而不是一个？**

- **对称性问题**：如果只用一个矩阵，那 $P(c|w) = P(w|c)$（因为点积是对称的），但实际上"cat 的上下文是 sat"和"sat 的上下文是 cat"这两个事件的概率不一定相同
- **训练稳定性**：两个独立矩阵提供更多参数自由度，训练更稳定
- **最终使用**：训练完后通常只用中心词矩阵 W，或取 (W+C)/2

> 📖 Paper: Mikolov et al., [Distributed Representations](https://arxiv.org/abs/1310.4546), §2

**为什么负采样分布用 f(w)^{3/4} 而不是均匀或纯词频？**

- **纯词频**：高频词（the, is, a）会垄断负样本，低频词几乎不会被选中 → 低频词的向量更新太少
- **均匀分布**：每个词被选概率相同 → 高频词的负样本太少 → 高频词的向量区分度差
- **f(w)^{3/4}**：折中方案——高频词的概率被压低（从 f 降到 f^{0.75}），低频词的概率被提高。0.75 是实验选出的最优值

> 📖 Paper: Mikolov et al., [Distributed Representations](https://arxiv.org/abs/1310.4546), §2.2

### 2.3 GloVe 的工作原理

```
语料库 → 共现矩阵 X (V×V)
              │
              ▼
    ┌─────────────────────────────┐
    │ 核心观察：共现比值包含语义     │
    │                             │
    │ P(solid|ice) / P(solid|steam) >> 1  → ice 和 solid 相关 │
    │ P(water|ice) / P(water|steam) ≈ 1   → water 对两者中性  │
    │                             │
    │ 目标: w_i · w_j + b ≈ log(X_ij)                        │
    │ 损失: f(X_ij) × (w_i·w_j + b_i + b_j - log X_ij)²    │
    └──────────────────┬──────────┘
                       │
                       ▼
    加权最小二乘优化 → 词向量 W
    最终: vec(word) = w + w̃ (两个向量求和)
```

> 📖 Paper: Pennington et al., [GloVe (2014)](https://nlp.stanford.edu/pubs/glove.pdf), §3

---

## Section 3: 局限性

1. **一词多义盲区** → 应对：使用 ELMo / BERT 等上下文嵌入
   - "bank" 在所有上下文中只有一个固定向量，无法区分"河岸"和"银行"
   - 📖 Paper: Peters et al., [ELMo (2018)](https://arxiv.org/abs/1802.05365)

2. **社会偏见继承** → 应对：使用 Bolukbasi et al. (2016) 的去偏方法
   - 训练语料中的偏见会被编码进词向量：vec("doctor")-vec("nurse") ≈ vec("man")-vec("woman")
   - 📖 Paper: Bolukbasi et al., [Man is to Computer Programmer as Woman is to Homemaker?](https://arxiv.org/abs/1607.06520), NeurIPS 2016

3. **形态盲区（Word2Vec/GloVe）** → 应对：使用 FastText（子词 n-gram）
   - "run", "running", "runner" 被视为完全不同的词，无法利用共同的词根信息
   - 📖 Paper: Bojanowski et al., [FastText (2017)](https://arxiv.org/abs/1607.04606)

4. **OOV（未登录词）** → 应对：使用 FastText，或 BPE/WordPiece 子词分词
   - 训练时没见过的词（如新造词、专业术语）无法获得向量表示
   - 📖 Docs: [SentencePiece](https://github.com/google/sentencepiece)

5. **窗口大小敏感** → 应对：根据任务选择窗口，或训练多个窗口大小取最优
   - 小窗口捕捉语法关系，大窗口捕捉语义关系，没有万能窗口

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.11-6.12

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **One-Hot** | 简单直接，无需训练 | 维度爆炸，无语义信息 | 极小词表（<100词） |
| **TF-IDF** | 考虑了词频重要性 | 仍然稀疏高维，无语义 | 文档级分类/检索 |
| **SVD on Co-occurrence** | 数学严谨，最优低秩近似 | O(V²) 内存，增量更新难 | 离线分析，词表小 |
| **Word2Vec (Skip-gram)** | 训练快，低频词好，类比性质强 | 一词一义，无法增量扩展 | 通用词嵌入，静态特征 |
| **GloVe** | 结合统计+预测，全局信息 | 需要先建共现矩阵 | 类比任务，学术研究 |
| **FastText** | 子词处理，OOV 能力，形态丰富语言 | 模型体积大（子词向量多） | 多语言，OOV 场景 |
| **ELMo** | 上下文感知，一词多义 | 基于 LSTM 较慢 | 过渡方案（已被 BERT 取代） |
| **BERT/GPT 嵌入** | 深度上下文，最强语义 | 计算量极大，需要 GPU | 有 GPU 的生产环境 |

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781)
> 📖 Paper: Pennington et al., [GloVe (2014)](https://nlp.stanford.edu/pubs/glove.pdf)
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Mikolov et al. Word2Vec (2013)](https://arxiv.org/abs/1301.3781) | 📖 论文 | Section 2 Skip-gram 流程 |
| [Mikolov et al. Negative Sampling (2013)](https://arxiv.org/abs/1310.4546) | 📖 论文 | Section 2 负采样设计 |
| [Pennington et al. GloVe (2014)](https://nlp.stanford.edu/pubs/glove.pdf) | 📖 论文 | Section 2 GloVe 原理 |
| [Peters et al. ELMo (2018)](https://arxiv.org/abs/1802.05365) | 📖 论文 | Section 3 上下文嵌入 |
| [Bolukbasi et al. Debiasing (2016)](https://arxiv.org/abs/1607.06520) | 📖 论文 | Section 3 偏见问题 |
| [《SLP3》Ch.6](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 📚 教科书 | 全章参考 |
| [Gensim Word2Vec Docs](https://radimrehurek.com/gensim/models/word2vec.html) | 📖 文档 | API 参考 |
