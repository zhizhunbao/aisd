---
topic: word_vectors
dimension: first_principles
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space', ICLR 2013 — https://arxiv.org/abs/1301.3781"
  - "📖 Paper: Levy & Goldberg, 'Neural Word Embedding as Implicit Matrix Factorization', NeurIPS 2014 — https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html"
  - "📖 Paper: Pennington et al., 'GloVe: Global Vectors for Word Representation', EMNLP 2014 — https://nlp.stanford.edu/pubs/glove.pdf"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: 12m
status: current
---

# Word Vectors 第一性原理

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781)
> 📖 Paper: Levy & Goldberg, [Neural Word Embedding as Implicit Matrix Factorization (2014)](https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html)
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6

---

## 核心问题链

> 用"5 个为什么"递归追问，从表层功能到不可再分公理。

1. **Word2Vec 在做什么？** → 把每个词映射成一个稠密的实数向量，让语义相近的词在向量空间中距离接近（表层功能）
2. **为什么语义相近的词应该在向量空间中接近？** → 因为我们假设"语义相近的词出现在相似的上下文中"——Word2Vec 的训练目标就是让共现词的向量点积最大化（动机）
3. **为什么"出现在相似上下文中"就能代表语义相近？** → 因为分布假说：一个词的意思完全由它的使用上下文决定（Firth 1957）。这是一个经验性的语言学观察，不是数学证明（更深层的假设）
4. **分布假说的根基是什么？** → 语言是一个高度规律的系统——同义词在语言使用中的确倾向于出现在相同的语法和语义环境中。这是人类语言的统计性质（基本事实）
5. **能否继续拆分？** → 不能——分布假说是一个关于语言本质的经验公设，无法从更基本的原理推导出来。它依赖于"自然语言具有统计规律性"这个前提 → **到达公理**

---

## 公理与基本假设

### 公理 1: 分布假说 (Distributional Hypothesis)

**陈述：** 在大规模自然语言语料库中，语义相似的词倾向于出现在相似的上下文中。

**白话：** "近朱者赤"——一个词的意思不是由字典定义的，而是由它经常和谁一起出现来决定的。"医生"之所以是医生，是因为它总是和"病人""诊断""治疗"一起出现。

**来源：** 经验观察（Firth 1957, Harris 1954）——从大量语言学语料分析中归纳得出，不是数学证明。

**可验证性：**
- ✅ 成立条件：自然语言文本，足够大的语料库（>1亿词），词频 >5 的常见词
- ❌ 不成立条件：① 语料太小——统计不可靠  ② 罕见词/专业术语——上下文太少  ③ 功能词（"the""is"）——上下文过于泛化，无法区分  ④ 反义词——"hot"和"cold"共享几乎相同的上下文（"the weather is ___"），向量会很接近，但语义是相反的

> 📖 Paper: Firth, J.R. "A Synopsis of Linguistic Theory 1930-1955" (1957)
> 📖 Paper: Harris, Z. "Distributional Structure" (1954)
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.3

### 公理 2: 向量空间可进行语义运算 (Linear Superposition Hypothesis)

**陈述：** 词的语义关系可以用向量空间中的线性运算来近似表示。

**白话：** "king" - "man" + "woman" ≈ "queen"——性别关系被编码成了一个几乎固定的方向，语义关系对应向量运算。

**来源：** 经验发现（Mikolov et al. 2013）——从训练好的词向量中观察到，而非从理论推导得出。后续 Arora et al. (2016) 给出了部分理论解释。

**可验证性：**
- ✅ 成立条件：某些规律的语义关系（性别、首都-国家、单复数、时态）
- ❌ 不成立条件：① 复杂/不规则的关系（"因果""部分-整体"）  ② 低频词——向量不够准确  ③ 带偏见的关系——反映的是统计偏差而非真实语义  ④ 多对多关系——"大"的反义词可以是"小""少""矮"等（不是唯一映射）

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §4
> 📖 Paper: Arora et al., [A Latent Variable Model Approach to PMI-based Word Embeddings](https://arxiv.org/abs/1502.03520), TACL 2016

### 公理 3: 低秩近似假设 (Low-Rank Approximation)

**陈述：** 自然语言的词-词共现矩阵（V×V 维）可以用远低于 V 的维度 d（d << V）来近似，且保留大部分语义信息。

**白话：** 虽然词表有 10 万个词（10万×10万的矩阵），但真正独立的"语义维度"只有几百个——就像虽然有 10 万个人，但描述一个人只需要几十个特征（身高、体重、年龄…）。

**来源：** 矩阵分析理论（Eckart-Young 定理）+ 经验验证（LSA/SVD 在低维度下效果好）。

**可验证性：**
- ✅ 成立条件：自然语言语料，d 在 100-500 范围
- ❌ 不成立条件：① d 太小（<50）——信息丢失太多  ② 高度专业化语料——某些领域的语义空间可能需要更高维度  ③ 多语言混合语料——不同语言的语义结构可能不共享低秩假设

> 📖 Paper: Deerwester et al., [LSA (1990)](https://doi.org/10.1002/(SICI)1097-4571(199009)41:6<391::AID-ASI1>3.0.CO;2-9)
> 📖 Paper: Levy & Goldberg, [NWE as Implicit MF (2014)](https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html)

---

## 从公理到技术的推导链

### Step 1: 从公理 1 (分布假说) 出发 → 共现统计有语义信息

**推理：** 如果"语义相似的词出现在相似的上下文中"（公理 1），那么统计一个词和哪些上下文词共同出现，就能得到该词的"语义指纹"。共现频率高的词对语义相关。

**结果：** 构建词-词共现矩阵 X（V×V），X_ij = 词 i 和词 j 在窗口内共现的次数。

### Step 2: 从公理 3 (低秩假设) 出发 → 可以降维

**推理：** 共现矩阵 X 是 V×V 维（太大），但公理 3 说真正的"语义维度"只有 d 个。所以 X 可以近似分解为 X ≈ W · W^T，其中 W 是 V×d 矩阵。

**结果：** LSA 用 SVD 实现这个分解；GloVe 通过最小化 f(X_ij)(w_i · w_j + b - log X_ij)² 来拟合；Word2Vec 通过 SGNS 隐式地分解 PMI 矩阵。

### Step 3: 从公理 2 (线性运算假设) 出发 → 向量类比

**推理：** 如果语义关系对应向量方向（公理 2），且词向量通过共现统计学到了语义（Step 1-2），那么训练好的词向量应该自然地展现向量类比性质。

**结果：** vec("king") - vec("man") + vec("woman") ≈ vec("queen")

### Step 4: → 完整的 Word2Vec / GloVe 技术

**推理：** 把 Step 1-3 组合：① 用大语料统计共现（分布假说）② 用浅层网络/矩阵分解学低维表示（低秩假设）③ 得到的向量用余弦相似度衡量语义距离 + 用向量运算做类比推理（线性运算假设）

**结果：** Word2Vec (Skip-gram + 负采样) 和 GloVe 在数学上是同一件事的两种实现方式（Levy & Goldberg 2014 证明）

### 推导链全景图

```
公理 1: 分布假说 ──────────────┐
(上下文≈语义)                   │
                               ├──→ 共现统计可编码语义 ──→ 共现矩阵 X
                               │
公理 3: 低秩假设 ──────────────┤
(V维→d维近似)                   ├──→ X ≈ W·Wᵀ ──→ 词向量 W ∈ R^{V×d}
                               │                      │
                               │     ┌─── LSA (SVD)    │
                               │     ├─── GloVe (显式)  │
                               │     └─── SGNS (隐式)   │
                               │                      │
公理 2: 线性运算 ──────────────┘                       │
(语义≈向量方向)                                        ▼
                                              词类比 + 余弦相似度
```

---

## 如果公理不成立？

### 公理 1 失效：分布假说不成立

**如果不成立：** 语义相似的词不一定出现在相似的上下文中——例如极其罕见的同义词，或者在特殊语域中含义变化的词。

**技术后果：**
- 词向量无法正确反映语义相似性
- "bank"（银行）和 "bank"（河岸）的问题就是部分失效——两者的上下文足够不同，但被强制合并成一个向量
- 反义词（"good" vs "bad"）共享几乎相同的上下文，向量距离很近，但语义相反

**替代方案：**
- 上下文嵌入（ELMo/BERT）——不再假设一词一义，而是为每次出现生成不同向量
- 多义词嵌入（Sense Embeddings）——每个词义分别学一个向量

### 公理 2 失效：线性运算假设不成立

**如果不成立：** 语义关系不是简单的向量加减——例如"因果关系""讽刺""隐喻"等复杂语义关系。

**技术后果：**
- 词类比任务大面积失败
- 不规则关系（"good" → "better" 而非 "gooder"）无法用线性运算捕捉
- 在实际应用中，类比准确率通常只有 40-75%

**替代方案：**
- 非线性模型（深层 Transformer）——用多层非线性变换建模复杂关系
- 知识图谱嵌入（TransE/TransR）——专门为关系建模设计的表示方法

### 公理 3 失效：低秩假设不成立

**如果不成立：** 词的语义空间的"有效维度"不是几百个，而是需要更高维度才能准确表示。

**技术后果：**
- 词向量质量上限受限于维度 d
- 实验中 d 从 50 增加到 300 通常有提升，但从 300 增加到 1000 提升很小——说明低秩假设在 d=300 左右是合理的
- 对于极大词表或极特殊领域，可能需要更高维度

**替代方案：**
- 使用更高维度的 Transformer 嵌入（BERT: 768 维, GPT-3: 12288 维）
- 稀疏编码方法（Sparse Coding）——保留高维但要求稀疏

---

## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
| 分布假说 | 上下文定义语义 | 大语料 + 常见词 | 反义词接近、多义词混淆 |
| 线性运算假设 | 语义关系 ≈ 向量方向 | 规律的关系（性别、首都） | 类比失败、复杂关系无法捕捉 |
| 低秩假设 | V 维可降到 d 维 | d ∈ [100, 500] + 通用语料 | 信息丢失、细粒度语义缺失 |
