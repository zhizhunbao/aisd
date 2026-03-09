# Lab 3 实验代码输出解读

> **先读这份文档，再去运行实验代码**——你就能理解每一行打印的含义，不需要边运行边猜。

- **§1** → Part 1：Word2Vec + GloVe vs SimLex999 评估输出（Step 6）
- **§2** → Part 2：FastText 词类比 + 拼写容错对比输出（Step 2/3/5）

关联教程：[lab3_tutorial.md](./lab3_tutorial.md)

---

## §1 读懂 Part 1 Step 6 输出

### 1.1 Pearson 相关系数（Step 6.1）

```
Pearson Correlation with SimLex999 (top 60 pairs):
  Word2Vec: 0.0931
  GloVe:    -0.0065
```

**读法：** Pearson 值域 $[-1, 1]$。
- $r \approx 1$：模型打分与人类评分**完全同向**——高分对应高分，低分对应低分。
- $r \approx 0$：两者**没有线性关系**——模型打分随机，与人类判断无关。
- $r < 0$：**反向**——人类觉得相似的，模型反而打低分。

**这里的数据说明什么：**  
Word2Vec 的 0.09 和 GloVe 的 -0.01 都接近 0，意味着**在最高相似度的 60 个词对里**，两个模型的余弦相似度与人类评分几乎没有线性对应关系。

**为什么会这样？**  
我们取的是 SimLex999 里**最高分**的 60 对（都分布在 8.5–10 区间）。人类评分非常集中，没有太多排名差异，Pearson 相关性自然很低。这是一个**数据子集选择导致的量程压缩效应**，不代表模型差——换成全部 999 对通常会得到 0.4–0.6 的相关性。

---

### 1.2 低估示例（Step 6.2）

```
Word2Vec underestimates (largest gaps):
  creator      - maker         SimLex=9.62  W2V=0.2605  Gap=0.7015
  acquire      - get           SimLex=8.82  W2V=0.2062  Gap=0.6758
```

**读法：**
- `SimLex=9.62` → 人类评分（10 分满分），归一化后约 0.962
- `W2V=0.2605` → Word2Vec 余弦相似度
- `Gap=0.7015` → `SimLex/10 - W2V = 0.962 - 0.261 = 0.701`（gap 越大，低估越严重）

**为什么 creator-maker 低估严重？**  
"creator" 在训练数据里多见于技术语境（content creator、God the creator），"maker" 多见于手工/产品语境。两词**共现频率低**，向量方向差异大，导致余弦相似度偏低——但人类语义上明确认为两者极其相似（都是"制造者"的同义词）。

这是词嵌入的典型局限：**语义相似 ≠ 上下文共现频率相似**。

---

### 1.3 平均相似度对比（Step 6.3 前半）

```
Average similarity (Word2Vec): 0.5875
Average similarity (GloVe):    0.5716
```

**读法：**  
对前 60 个高相似度词对，两个模型给出的平均余弦相似度约在 0.57–0.59。这相当于**向量夹角约 54°**，并非"很相近"。

**为什么平均值这么低？**  
人类评分 9+ 分的词对，意味着人类认为两词**几乎等义**。但词嵌入把"能出现在相同语境"当作相似性依据，同义词不一定总是同现，反而是"king"和它的常见搭配（throne、queen）更常共现。

**两模型的差异原因：**  
Word2Vec 稍高，说明 Google News 的新闻文体里高频专业词（attorney/lawyer、physician/doctor）的局部共现信号更强；GloVe 稍低，因为全局共现矩阵在通用语料里对这类词的统计更"稀释"。

---

### 1.4 两模型差异最大的词对（Step 6.3 后半）

```
Pairs with largest difference between Word2Vec and GloVe:
  drizzle      - rain          W2V=0.6986  GloVe=0.4477  Diff=0.2508
  friend       - buddy         W2V=0.6972  GloVe=0.4680  Diff=0.2293
  insane       - crazy         W2V=0.7339  GloVe=0.5081  Diff=0.2258
```

**读法：**  
`Diff` = `|W2V - GloVe|`，差值越大，说明两种训练方式在该词对上的"判断"差异越大。

**为什么 drizzle-rain 差异最大？**
- Word2Vec（Google News）：新闻天气预报里"drizzle" 和 "rain" 频繁出现在相邻句子，**局部共现强** → 高相似度 0.70
- GloVe（Wikipedia + Gigaword）：Wikipedia 对 drizzle 的描述是气象学定义，语境远比 rain 正式，**全局共现比例低** → 低相似度 0.45

**为什么 insane-crazy 也差异大？**  
两词都是非正式口语词汇，Google News 里出现在相同语境（报道犯罪/极端事件）频率远高于 Wikipedia 的学术语境。局部窗口（Word2Vec）比全局矩阵（GloVe）更能捕捉这类口语共现信号。

**总结规律：**

| 词对类型 | Word2Vec 表现 | GloVe 表现 | 原因 |
|---|---|---|---|
| 专业词同义词（attorney-lawyer）| ✅ 较好 | ⚠️ 稍差 | 新闻语境局部共现强 |
| 描述性词对（boundary-border）| ⚠️ 稍差 | ✅ 较好 | Wikipedia 全局统计更丰富 |
| 口语/俚语（insane-crazy）| ✅ 较好 | ⚠️ 稍差 | 口语词在新闻里共现频繁 |
| 上下位关系词（cop-sheriff）| ⚠️ 稍差 | ⚠️ 稍差 | 两模型都难以区分相似与相关 |

---

## §2 读懂 Part 2 输出

### 2.1 Step 2 类比相似度分数

```
King - Man + Woman = ?
  Top 5 results:
    queen                 similarity: 0.6543
    kings                 similarity: 0.5410
    ...

Computer Programmer - Man + Woman = ?
  Top 5 results:
    Nursing               similarity: 0.2518
    Breastfeeding         similarity: 0.2449
    ...
```

**读法：** 这里的 similarity 是向量运算结果 $\vec{king} - \vec{man} + \vec{woman}$ 与词汇表中每个词的余弦相似度，越高越"方向接近"。

**这里的数据说明什么：**

| 类比 | top-1 结果 | similarity | 解读 |
|------|-----------|------------|------|
| king - man + woman | queen | 0.6543 | ✅ 经典案例，语义方向保留良好 |
| computer_programmer - man + woman | Nursing | 0.2518 | ⚠️ 性别偏见：模型把"职业+女性"映射到了护理类词 |
| doctor - man + woman | pediatrician | 0.4673 | ⚠️ 偏见：女医生 → 儿科医生（刻板印象） |
| intelligent - scientist + woman | man | 0.6037 | ⚠️ 严重偏见：intelligent 的"女性联想"仍然是 man |

**为什么 similarity 差这么多：**
- `king-queen` 分数高（0.65）：这对词在训练语料中语境极为对称，向量关系干净
- `computer_programmer` 类比分数低（~0.25）：
  1. `computer_programmer` 在语料中出现次数少，向量估计噪声大
  2. 训练数据本身这个职业的女性上下文就更少，向量空间里"程序员"方向和"女性"方向没有交集

**反直觉点：** `computer_programmer - man + woman` 结果不是 `computer_programmer`——这不是 FastText 崩了，而是它**忠实反映了训练数据里的社会偏见**。偏差来自数据，不来自算法。

---

### 2.2 Step 3 模型打印的 Observations 怎么读

```
1. Gender Bias in Word Embeddings: ...
2. Analogy Quality: ...
3. Sub-word Advantage: ...
```

**这三条不是评估分数，而是代码里硬编码的文本说明**（`print()` 字符串），Lab 让你对照自己的 Step 2 输出去验证：

| Observation | 验证方式 |
|-------------|---------|
| Gender Bias | 看 computer_programmer / doctor 类比的 top-1 是否是女性相关词 |
| Analogy Quality | 对比 king-queen（高分）vs 其他（低分）的分值差距 |
| Sub-word Advantage | 确认即使 `computer_programmer` 在词汇表里稀有，FastText 也能输出向量（不报 KeyError） |

---

### 2.3 Step 5 拼写错误对比分数

```
Correct: apple,    Misspelled: appple
  Word2Vec Similarity: N/A (word not in vocabulary)
  FastText Similarity: 0.3621

Correct: banana,   Misspelled: bananna
  Word2Vec Similarity: N/A (word not in vocabulary)
  FastText Similarity: 0.7789

Correct: science,  Misspelled: sciience
  Word2Vec Similarity: N/A (word not in vocabulary)
  FastText Similarity: 0.0678
```

**读法：** 这里的 similarity 是正确拼写词向量 vs 错误拼写词向量的余弦相似度，越高表示 FastText 越能识别两者"是同一个词"。

**N/A 是什么意思：** Word2Vec 是整词查表，`appple` 根本不在词汇表里，直接抛出 KeyError，代码捕获后输出 `N/A`。这不是 similarity = 0，而是"无法计算"。

**为什么 FastText 的分数差异这么大：**

| 单词对 | FastText 分 | 原因 |
|--------|-------------|------|
| banana / bananna | 0.7789 | 错误只是多一个 `n`，n-gram 重叠度极高（`ban`, `ana`, `nan`, `ana` 几乎全中） |
| apple / appple | 0.3621 | 多一个 `p`，n-gram 里多出 `ppp` 这个从不出现的片段，稀释了相似度 |
| science / sciience | 0.0678 | 多一个 `i` 插在词中部，破坏了 `sci`, `cie`, `ien`, `enc` 等核心 n-gram，损失最大 |

**结论公式（直觉）：** FastText 的鲁棒性 ∝ 错别字改动位置的 n-gram 破坏程度。末尾加字母 < 中间插字母。

---

*关联教程：[lab3_tutorial.md](./lab3_tutorial.md)*  
*生成自：Lab 3 Part 1 & Part 2 实验代码输出*
