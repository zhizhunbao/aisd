---
topic: word_vectors
dimension: math
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space', ICLR 2013 — https://arxiv.org/abs/1301.3781"
  - "📖 Paper: Mikolov et al., 'Distributed Representations of Words and Phrases', NeurIPS 2013 — https://arxiv.org/abs/1310.4546"
  - "📖 Paper: Pennington et al., 'GloVe: Global Vectors for Word Representation', EMNLP 2014 — https://nlp.stanford.edu/pubs/glove.pdf"
  - "📖 Paper: Levy & Goldberg, 'Neural Word Embedding as Implicit Matrix Factorization', NeurIPS 2014 — https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: 12m
status: current
---

# Word Vectors 数学基础

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 "Vector Semantics and Embeddings"
> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781)
> 📖 Paper: Pennington et al., [GloVe (2014)](https://nlp.stanford.edu/pubs/glove.pdf)

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $V$ | 词表大小（有多少不同的词） | Vocabulary size | 通常 10⁴ ~ 10⁶ |
| $d$ | 词向量维度 | Embedding dimension | 通常 50 ~ 300 |
| $w$ | 中心词（正在关注的词） | Center/Target word | — |
| $c$ | 上下文词（窗口内的邻居词） | Context word | — |
| $\mathbf{w}$ | 中心词向量（d 维） | Center word vector | $\mathbb{R}^d$ |
| $\mathbf{c}$ | 上下文词向量（d 维） | Context word vector | $\mathbb{R}^d$ |
| $W$ | 中心词嵌入矩阵 | Center embedding matrix | $\mathbb{R}^{V \times d}$ |
| $C$ | 上下文词嵌入矩阵 | Context embedding matrix | $\mathbb{R}^{V \times d}$ |
| $L$ | 上下文窗口半径 | Context window radius | 通常 2~10 |
| $k$ | 负采样个数 | Number of negative samples | 通常 5~15 |
| $X_{ij}$ | 词 i 和词 j 的共现次数 | Co-occurrence count | $\geq 0$ |
| $\sigma(\cdot)$ | Sigmoid 函数 | Sigmoid function | $(0, 1)$ |

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.8

---

## 核心公式

### 公式 1: Skip-gram 原始目标函数

**直觉：** 让中心词的向量能预测出它周围的上下文词——如果一个词的向量能准确预测它的邻居，说明这个向量捕捉了语义信息。

$$
J = -\frac{1}{T} \sum_{t=1}^{T} \sum_{-L \leq j \leq L, j \neq 0} \log P(w_{t+j} \mid w_t)
$$

其中：

$$
P(c \mid w) = \frac{\exp(\mathbf{c}^\top \mathbf{w})}{\sum_{v=1}^{V} \exp(\mathbf{c}_v^\top \mathbf{w})}
$$

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), Eq. 1-2

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $T$ | 语料库总词数 | 10 亿 |
| $L$ | 窗口半径 | L=2 → 前后各取 2 个词 |
| $P(c \mid w)$ | 给定中心词 w 预测上下文词 c 的概率 | P("cat" \| "sat") |
| 分母 $\sum_{v}$ | 对整个词表 V 做归一化 | V=10 万个词的求和 |

**推导过程：**

1. **起点**：给定语料库 $w_1, w_2, \ldots, w_T$，我们希望最大化对数似然：每个中心词应该能预测出它窗口内的上下文词
2. **条件概率**：用两个词向量的点积衡量"相关度"，点积越大→概率越高
3. **归一化**：用 Softmax 把点积分数转成概率分布——分子是目标对的 exp(点积)，分母是对所有 V 个词的 exp(点积) 求和
4. **问题**：分母要对 V 个词求和，V 通常 10 万+，每步训练都要算 O(V)，太慢 → 需要负采样

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §2

---

### 公式 2: Skip-gram with Negative Sampling (SGNS)

**直觉：** 与其在 10 万个词上做 Softmax，不如简化成二分类："这对 (中心词, 上下文词) 是真的还是假的？"——正样本是真正的邻居对，负样本是随机配对的假邻居。

$$
J_{\text{SGNS}} = -\sum_{(w,c) \in D^+} \left[ \log \sigma(\mathbf{c}^\top \mathbf{w}) + \sum_{i=1}^{k} \mathbb{E}_{c_i \sim P_n(w)} \log \sigma(-\mathbf{c}_i^\top \mathbf{w}) \right]
$$

> 📖 Paper: Mikolov et al., [Distributed Representations](https://arxiv.org/abs/1310.4546), Eq. 4

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $D^+$ | 正样本集合（真正的中心-上下文对） | {("sat", "cat"), ("sat", "on"), …} |
| $\sigma(x)$ | Sigmoid 函数 $\sigma(x)=1/(1+e^{-x})$ | 把点积压到 (0,1) 区间 |
| $k$ | 负采样个数 | k=5 |
| $P_n(w)$ | 噪声分布 $P_n(w) \propto f(w)^{3/4}$ | 按词频 3/4 次方采样 |
| $\mathbf{c}^\top \mathbf{w}$ | 中心词和上下文词的向量点积 | 高→认为是真邻居 |

**推导过程：**

1. **目标简化**：原始 Softmax 的分母 $\sum_V$ 太大 → 改成 k+1 个二分类
2. **正样本项** $\log \sigma(\mathbf{c}^\top \mathbf{w})$：希望真正的 (w, c) 对点积大 → σ 趋向 1 → log 趋向 0（最大化）
3. **负样本项** $\log \sigma(-\mathbf{c}_i^\top \mathbf{w})$：希望随机配的 (w, c_i) 对点积小 → $-\mathbf{c}_i^\top \mathbf{w}$ 大 → σ 趋向 1 → log 趋向 0
4. **噪声分布**：$P_n(w) \propto f(w)^{3/4}$，3/4 次方让低频词被采到的概率比纯词频分布更高（避免高频词垄断负样本）
5. **关键洞察**：Levy & Goldberg (2014) 证明 SGNS 在无穷数据极限下，隐式地分解了 PMI 矩阵：$\mathbf{w}^\top \mathbf{c} \approx \text{PMI}(w, c) - \log k$

> 📖 Paper: Levy & Goldberg, [Neural Word Embedding as Implicit Matrix Factorization](https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html), NeurIPS 2014, Theorem 1

---

### 公式 3: GloVe 目标函数

**直觉：** 两个词向量的点积应该近似等于它们在语料库中共现次数的对数——共现越多的词对，向量点积越大。同时用一个加权函数，让共现次数太少的词对别太影响训练，太多的也别太霸道。

$$
J_{\text{GloVe}} = \sum_{i=1}^{V} \sum_{j=1}^{V} f(X_{ij}) \left( \mathbf{w}_i^\top \tilde{\mathbf{w}}_j + b_i + \tilde{b}_j - \log X_{ij} \right)^2
$$

其中加权函数：

$$
f(x) = \begin{cases} (x/x_{\max})^\alpha & \text{if } x < x_{\max} \\ 1 & \text{otherwise} \end{cases}
$$

> 📖 Paper: Pennington et al., [GloVe (2014)](https://nlp.stanford.edu/pubs/glove.pdf), Eq. 8-9

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $X_{ij}$ | 词 i 和词 j 的全局共现次数 | X("the","cat") = 50000 |
| $\mathbf{w}_i$ | 词 i 的中心词向量 | d=300 维 |
| $\tilde{\mathbf{w}}_j$ | 词 j 的上下文词向量 | d=300 维 |
| $b_i, \tilde{b}_j$ | 偏置项 | 标量 |
| $f(X_{ij})$ | 加权函数（限制极高频共现的影响） | — |
| $x_{\max}$ | 加权函数截断点 | 100 |
| $\alpha$ | 加权函数指数 | 0.75 |

**推导过程：**

1. **起点**：定义共现概率比值 $P_{ik}/P_{jk}$ = 词 k 和词 i 共现 vs 词 k 和词 j 共现的比值
2. **关键观察**：如果 i = "ice"，j = "steam"，k = "solid" → $P_{ik}/P_{jk}$ 很大（"solid" 和 "ice" 关系密切，和 "steam" 无关）
3. **数学约束**：我们希望找到词向量使得 $F(\mathbf{w}_i, \mathbf{w}_j, \tilde{\mathbf{w}}_k) = P_{ik}/P_{jk}$
4. **简化**：要求 F 只依赖 $\mathbf{w}_i - \mathbf{w}_j$ 的方向 → 选择点积形式 → 取对数 → 得到 $\mathbf{w}_i^\top \tilde{\mathbf{w}}_k = \log P(k|i) = \log X_{ik} - \log X_i$
5. **对称化**：吸收 $\log X_i$ 到偏置项 $b_i$ 中 → 最终形式 $\mathbf{w}_i^\top \tilde{\mathbf{w}}_j + b_i + \tilde{b}_j = \log X_{ij}$
6. **最小化**：用加权最小二乘拟合，$f(X_{ij})$ 降低稀有共现的噪声影响

> 📖 Paper: Pennington et al., [GloVe (2014)](https://nlp.stanford.edu/pubs/glove.pdf), §3 "The GloVe Model"

---

### 公式 4: 余弦相似度

**直觉：** 衡量两个词有多"像"——只看向量方向不看长度。方向完全一样 = 1，完全相反 = -1，毫无关系 = 0。

$$
\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \cdot \|\mathbf{v}\|} = \frac{\sum_{i=1}^d u_i v_i}{\sqrt{\sum_{i=1}^d u_i^2} \cdot \sqrt{\sum_{i=1}^d v_i^2}}
$$

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.4, Eq. 6.10

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $\mathbf{u}, \mathbf{v}$ | 两个词的嵌入向量 | vec("king"), vec("queen") |
| $d$ | 向量维度 | 300 |
| $\|\mathbf{u}\|$ | 向量 u 的 L2 范数 | $\sqrt{u_1^2 + \ldots + u_d^2}$ |

---

### 公式 5: PMI (Pointwise Mutual Information)

**直觉：** 两个词的实际共现频率比"随机碰巧共现"高多少倍？PMI 高说明两个词确实有关联，不是巧合。

$$
\text{PMI}(w, c) = \log \frac{P(w, c)}{P(w) \cdot P(c)} = \log \frac{X_{wc} \cdot |D|}{X_w \cdot X_c}
$$

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.6, Eq. 6.17

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $P(w, c)$ | 词 w 和 c 的联合概率 | 共现次数 / 总窗口数 |
| $P(w), P(c)$ | 各自的边缘概率 | 词频 / 总词数 |
| $X_{wc}$ | 共现次数 | X("data","science") = 500 |
| \|D\| | 总窗口数（归一化常数） | — |

> 📖 Paper: Levy & Goldberg, [Neural Word Embedding as Implicit Matrix Factorization](https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html), NeurIPS 2014

---

## 公式关系图

```
分布假说 (Firth 1957)
    │
    ▼
共现矩阵 X_{ij}
    │
    ├──→ PMI(w,c) = log(P(w,c)/(P(w)·P(c)))
    │       │
    │       └──→ SVD 降维 → 词向量 (LSA)
    │
    ├──→ GloVe: w·c + b ≈ log(X_{ij})  ← 显式矩阵分解
    │
    └──→ Skip-gram Softmax: P(c|w) = softmax(c·w)
            │
            └──→ 负采样 SGNS: σ(c·w) vs σ(-c_neg·w)
                    │
                    └──→ Levy & Goldberg 2014:
                         SGNS ≈ PMI - log(k)  ← 隐式矩阵分解

余弦相似度: cos(u,v) = u·v / (||u||·||v||)  ← 评估所有词向量
```

---

## 手算练习

### 练习 1: Skip-gram 负采样前向计算

**题目：** 给定 3 维词向量，中心词 "sat" = [0.5, 0.3, -0.2]，正上下文 "cat" = [0.4, 0.6, 0.1]，负样本 "cloud" = [-0.3, 0.1, 0.8]。计算 SGNS 的单步损失。

**解答步骤：**

1. 正样本点积：$\mathbf{c}_{cat}^\top \mathbf{w}_{sat} = 0.4 \times 0.5 + 0.6 \times 0.3 + 0.1 \times (-0.2) = 0.20 + 0.18 - 0.02 = 0.36$
2. $\sigma(0.36) = 1/(1+e^{-0.36}) = 1/(1+0.698) = 0.589$
3. 正样本损失：$-\log \sigma(0.36) = -\log(0.589) = 0.529$
4. 负样本点积：$\mathbf{c}_{cloud}^\top \mathbf{w}_{sat} = (-0.3)(0.5) + 0.1(0.3) + 0.8(-0.2) = -0.15 + 0.03 - 0.16 = -0.28$
5. $\sigma(-(-0.28)) = \sigma(0.28) = 1/(1+e^{-0.28}) = 0.570$
6. 负样本损失：$-\log \sigma(0.28) = -\log(0.570) = 0.562$
7. **总损失 = 0.529 + 0.562 = 1.091**

### 练习 2: 余弦相似度计算

**题目：** vec("king") = [0.8, 0.3, -0.5], vec("queen") = [0.7, 0.4, -0.3]。

**解答步骤：**

1. 点积：$0.8 \times 0.7 + 0.3 \times 0.4 + (-0.5) \times (-0.3) = 0.56 + 0.12 + 0.15 = 0.83$
2. ||king|| = $\sqrt{0.64 + 0.09 + 0.25} = \sqrt{0.98} = 0.990$
3. ||queen|| = $\sqrt{0.49 + 0.16 + 0.09} = \sqrt{0.74} = 0.860$
4. **cos = 0.83 / (0.990 × 0.860) = 0.83 / 0.851 = 0.975**（非常相似）

### 练习 3: 词类比

**题目：** vec("king") = [0.8, 0.3, -0.5], vec("man") = [0.6, 0.2, 0.1], vec("woman") = [0.5, 0.5, -0.1]。求 king - man + woman。

**解答步骤：**

1. vec("king") - vec("man") = [0.8-0.6, 0.3-0.2, -0.5-0.1] = [0.2, 0.1, -0.6]
2. + vec("woman") = [0.2+0.5, 0.1+0.5, -0.6+(-0.1)] = **[0.7, 0.6, -0.7]**
3. 这个结果向量应该最接近 vec("queen") —— 用余弦相似度在词表中找最近邻

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| Skip-gram Softmax | $P(c \mid w) = \text{softmax}(\mathbf{c}^\top \mathbf{w})$ | 原始目标函数 | — |
| SGNS 损失 | $-\log \sigma(\mathbf{c}^\top \mathbf{w}) - \sum \log \sigma(-\mathbf{c}_i^\top \mathbf{w})$ | 实际训练目标 | Skip-gram |
| GloVe 损失 | $f(X_{ij})(\mathbf{w}_i^\top \tilde{\mathbf{w}}_j + b_i + \tilde{b}_j - \log X_{ij})^2$ | 全局共现拟合 | 共现矩阵 |
| 余弦相似度 | $\cos(\mathbf{u},\mathbf{v}) = \mathbf{u} \cdot \mathbf{v} / (\|\mathbf{u}\| \|\mathbf{v}\|)$ | 词相似度评估 | — |
| PMI | $\log(P(w,c) / (P(w) P(c)))$ | 共现显著性 | 共现矩阵 |
| 噪声分布 | $P_n(w) \propto f(w)^{3/4}$ | 负采样概率 | 词频统计 |
| 词类比 | $\mathbf{v}_b - \mathbf{v}_a + \mathbf{v}_c$ | a:b::c:? | 余弦相似度 |
