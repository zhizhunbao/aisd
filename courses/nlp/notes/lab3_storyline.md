# Lab 3 故事线：词嵌入的三次进化，以及它们暴露的人类偏见

> **Source:** `CST8507 Lab 3_W26.pdf` · [`labs/CST8507_Lab_3_W26.md`](../labs/CST8507_Lab_3_W26.md)
> **Code:** [`code/lab3/lab3_part1.py`](../code/lab3/lab3_part1.py) · [`code/lab3/lab3_part2.py`](../code/lab3/lab3_part2.py)
> **关联 Lecture：** [Lecture 4 故事线](./lecture4_storyline.md)（理论背景）
> **核心主题：** 词嵌入学到了"语义"，但它学到的是 **人类语料库里的语义**——包括偏见。
> **故事线：** 三个模型，三项实验，一个越来越清晰的认知：词嵌入既是镜子，也是放大镜。
>
> **数学前置：** [内积与余弦相似度](../../math/linear-algebra/inner_product.md) | [向量范数](../../math/linear-algebra/norms_distances.md) | [协方差与相关系数](../../math/statistics/mean_variance.md#§3-covariance--correlation-协方差与相关性)

---

## 🎬 序幕：实验要解决什么问题？

Lecture 4 告诉我们，词嵌入把词变成了向量，语义相似的词在空间中距离更近。听起来很美。

但有一个核心问题没有回答：

> **这些向量到底有多"准"？谁来裁判？**

这正是 Lab 3 要做的事——**用实验验证词嵌入的质量**，并探索它们的能力边界。

实验分两个方向攻关：

```
Part 1：内在评估 (Intrinsic Evaluation)          Part 2：子词建模 (Sub-word Modeling)
───────────────────────────────────────          ───────────────────────────────────
问题：模型的相似度判断跟人类一致吗？              问题：拼写错误的词怎么办？
裁判：SimLex-999（999个人工评分词对）             武器：FastText（字符n-gram）
对手：Word2Vec vs GloVe                          实验：类比推理 + 拼写容错对比
```

---

## 📚 第一章：相似度的"黄金标准"——SimLex-999

### 1.1 我们需要一个裁判

词嵌入说 "vanish" 和 "disappear" 很像（余弦相似度 0.90）。这对吗？  
它也说 "creator" 和 "maker" 很像（余弦相似度 0.26）。这又对吗？

**谁说了算？**

答案是：让人类来打分。SimLex-999 收集了 999 个词对，请人类评判每对词的**语义相似度**（0–10分）。这 999 个判断就是"黄金标准"。

> 💡 **类比：** SimLex-999 是语言学的"标准砝码"——不管你的模型是怎么训练的，最终都要放到这台天平上称一称。

### 1.2 "语义相似" vs "语义相关"——SimLex-999 的严格区分

这是 SimLex-999 最重要的设计决策，很多人会踩的坑：

| 词对 | 语义相关？ | 语义相似？ | SimLex-999 怎么看 |
|------|-----------|-----------|-------------------|
| coffee ↔ cup | ✅ 高度相关 | ❌ 不相似 | 低分 |
| smart ↔ intelligent | ✅ 相关 | ✅ 相似 | 高分（9.20）|
| doctor ↔ hospital | ✅ 高度相关 | ❌ 不相似 | 低分 |
| vanish ↔ disappear | ✅ 相关 | ✅ 相似 | 最高分（9.80）|

**关键：** 咖啡和杯子经常一起出现（高共现），所以词嵌入会给它们很高的余弦相似度——但 SimLex-999 不认为它们"语义相似"。余弦相似度高 ≠ 人类认为相似。

### 1.3 实验数据分布

```
Total: 999 pairs
Min similarity:  0.23  ← 几乎完全不相似
Avg similarity:  4.56  ← 中间值
Max similarity:  9.80  ← vanish ↔ disappear（近义词对）
```

我们取 Top 60（相似度最高的词对）来测试模型——这是**最苛刻的测试场景**，因为这些词对人类认为"极度相似"，模型应该得分最高。

---

## 🧮 第二章：Word2Vec vs GloVe——谁更接近人类直觉？

### 2.1 两个模型，两种哲学

| | Word2Vec | GloVe |
|---|---|---|
| **训练哲学** | 预测：给定上下文，猜中心词 | 计数+优化：让向量点积 = log(共现次数) |
| **视野** | 局部滑动窗口 | 全语料库共现矩阵 |
| **数据来源** | Google News（新闻，偏专业/正式）| Wikipedia + Gigaword（百科+新闻，更广泛）|
| **词汇量** | 3,000,000 词 | 400,000 词 |

> 💡 **类比：** Word2Vec 像一个每天读报纸的专家分析师（局部、专业）；GloVe 像一个读完整个图书馆的学者（全局、广博），但词汇量少一些。

### 2.2 实验结果——Who Wins?

**Top 60 词对的部分结果：**

```
词对                   SimLex999   Word2Vec    GloVe      谁赢了
─────────────────────  ─────────  ──────────  ─────────  ──────
vanish ↔ disappear      9.80       0.9004      0.8053     W2V ✅
quick ↔ rapid           9.70       0.4978      0.4990     平手😐
creator ↔ maker         9.62       0.2605      0.1902     W2V（都很差）
attorney ↔ lawyer       9.35       0.8205      0.7753     W2V ✅
hallway ↔ corridor      9.28       0.3219      0.3859     GloVe ✅
boundary ↔ border       9.08       0.3861      0.4661     GloVe ✅
large ↔ huge            9.47       0.6589      0.7354     GloVe ✅
drizzle ↔ rain          9.17       0.6986      0.4477     W2V ✅
```

> 🔑 **模式发现：**
> - **Word2Vec 优势：** 专业/领域术语（attorney/lawyer、physician/doctor），Google News 语料让这些词频繁共现
> - **GloVe 优势：** 空间/描述词（boundary/border、hallway/corridor），Wikipedia 的描述性文字给这些词更一致的语境
> - **两者都差：** quick/rapid、creator/maker——这些词在语料库中出现的**语境不同**（quick 口语，rapid 正式），导致向量方向分离，即使人类认为它们极度相似

### 2.3 ❌ 一个令人不舒服的发现：向量系统性低估人类相似度

对 Top 60 所有词对，词嵌入相似度几乎总是**低于** SimLex999 归一化值。

**为什么？**

语料库中的词不只跟同义词共现——"attorney" 也和 "criminal"、"court"、"judge" 频繁共现，这些"相关但不相似"的词把向量方向拉偏了。

> 🔑 **故事转折点：** Word2Vec 和 GloVe 都面临同一个根本限制——它们只能处理训练词汇表里的词。拼写错误的 "computar"？OOV，直接返回 None。→ **FastText** 登场！

---

## 🔬 第三章：FastText 与字符的魔法——打破 OOV 诅咒

### 3.1 OOV 问题有多严重？

```python
# Word2Vec / GloVe 遇到拼写错误
if word not in model.key_to_index:
    return None  # 完全束手无策
```

真实场景：用户输入 "sciience"（多了一个 i）、"computar"（把 e 拼成 a）。传统模型完全放弃。

这在实际应用中是灾难性的——搜索引擎、聊天机器人、语音识别的输出里充满了拼写变体。

### 3.2 FastText 的根本思路：词不是原子，是分子

**Word2Vec/GloVe 的假设：** 词是不可分割的原子单元。  
**FastText 的假设：** 词是字符片段（n-gram）的组合。

```
"apple"  → <ap + app + ppl + ple + le> + <apple>（整词）
            ↑───────────────────────────────────────────
            这些 n-gram 向量都单独储存，词向量 = 它们的和

"appple" → <ap + app + ppp + ppl + ple + le>
                 ↑───────────────── 共享大量 n-gram ──────
                 → 自动获得接近 "apple" 的向量！
```

$$\text{vec}(w) = \sum_{g \in G_w} \mathbf{z}_g$$

其中 $G_w$ 是词 $w$ 的所有字符 n-gram 集合。

### 3.3 拼写容错实验结果

```
词对 (正确 ↔ 拼写错误)         Word2Vec        FastText
──────────────────────────    ─────────       ──────────
apple   ↔ appple              N/A (OOV)       0.3621
banana  ↔ bananna             N/A (OOV)       0.7789  ← 高！
computer ↔ computar           N/A (OOV)       0.3759
science ↔ sciience            N/A (OOV)       0.0678  ← 注意！
education ↔ edcation          N/A (OOV)       ~0.3–0.5
```

**"sciience" 为什么这么低（0.07）？**

```
"science"  n-grams: sci, cie, ien, enc, nce
"sciience" n-grams: sci, cii, iie, ien, enc, nce
                        ↑───────── 这两个是"噪声"n-gram ─────
                        共享率下降 → 相似度骤降
```

只多了一个字母，就破坏了 n-gram 共享链。FastText 不是万能的——拼写错误越"奇特"，效果越差。

---

## ⚠️ 第四章：类比实验揭示的人类偏见

### 4.1 经典类比成功——但这只是开始

$$\text{vec}(\text{king}) - \text{vec}(\text{man}) + \text{vec}(\text{woman}) \approx \text{vec}(\text{queen})$$

实验结果：queen（相似度 0.6543）。经典通过！向量偏移量确实编码了"皇权"这个抽象方向。

### 4.2 其他类比结果——意外吗？

```
类比                               Top 结果               相似度
─────────────────────────────────  ─────────────────────  ───────
King - Man + Woman                 queen                  0.6543  ✅
Doctor - Man + Woman               pediatrician           0.4673  🤔
Computer Programmer - Man + Woman  Nursing                0.2518  ❌
Career - Man + Woman               careers                0.4761  😐
Intelligent - Scientist + Woman    man                    0.6037  ❌
```

### 4.3 这些结果说明了什么？

**"医生 - 男人 + 女人 = 儿科医生/助产士"**  
不是 "doctor"，而是儿科医生、助产士——偏向女性化的医疗子领域。

**"程序员 - 男人 + 女人 = 护理/母乳喂养"**  
这不是巧合，而是训练数据的**统计现实**：新闻和维基百科里，"计算机程序员"与"男性"共现的频率远高于"女性"。

> 🔑 **核心洞察：** 词嵌入是语料库的镜子。它不创造偏见，它**反映并放大**人类写下来的偏见。模型得到的不是"真相"，而是"文本中的统计规律"。

**"聪明 - 科学家 + 女人 = man/lady/women"**  
减去 "scientist" 把"智力"成分几乎全部抵消，只剩下"人称"成分。这暴露了 **语义漂移（Semantic Drift）**：向量运算不是完美的线性代数，减去的太多可能丢失核心语义。

### 4.4 两个并行的问题

```
问题 A：性别偏见                    问题 B：语义漂移
───────────────────────────────    ─────────────────────────────
训练数据 → 社会偏见被编码进向量     向量运算不线性 → 减法丢失语义
难以检测（数字里隐藏着偏见）        类比越抽象越不可靠
解决方案：去偏（debiasing）算法     解决方案：更丰富的向量空间
仍是 NLP 的开放研究问题            BERT 等上下文模型有所改善
```

---

## 🗺️ Lab 3 全局路线图

```
┌────────────────────────────────────────────────────────────────┐
│                      Lab 3 实验路线图                            │
│                                                                │
│  问题 1：词嵌入跟人类判断有多一致？                              │
│    ↓                                                           │
│  SimLex-999（黄金标准）                                         │
│    ↓                                                           │
│  Top 60 词对 ──→ Word2Vec 余弦相似度  ──┐                      │
│              └─→ GloVe 余弦相似度    ──┼─→ Pearson 相关系数    │
│                                        └─→ 谁更接近人类？       │
│                                                                │
│  结论：两者都低估人类相似度；W2V 擅长专业词；GloVe 擅长描述词  │
│                                                                │
│  ───────────────────────────────────────────────────────────  │
│                                                                │
│  问题 2：OOV 词和拼写错误怎么办？                               │
│    ↓                                                           │
│  FastText（字符 n-gram 子词建模）                               │
│    ↓                                                           │
│  词类比实验 ──→ King-Man+Woman=? ──→ 揭示性别偏见              │
│  拼写容错实验 ──→ W2V=N/A vs FastText=0.78                     │
│                ↓                                               │
│              n-gram 共享率决定容错能力                          │
│                                                                │
│  结论：FastText 解决 OOV；但向量仍然编码了训练数据中的社会偏见  │
└────────────────────────────────────────────────────────────────┘
```

### 三个模型的综合对比

| | Word2Vec | GloVe | FastText |
|---|---|---|---|
| **向量维度** | 300 | 300 | 300 |
| **词汇量** | 3M | 400K | 2M（+ 无限 n-gram）|
| **训练数据** | Google News | Wikipedia+Gigaword | Common Crawl |
| **OOV 处理** | ❌ | ❌ | ✅ 子词合成 |
| **拼写错误** | ❌ | ❌ | ✅（共享 n-gram）|
| **内在评估** | 强（专业词）| 强（描述词）| 未直接测试 |
| **偏见暴露** | Yes | Yes | Yes（类比实验）|

---

## 🎓 考试/复习重点检查清单

### Part 1: 内在评估

- [ ] 解释 SimLex-999 是什么，以及为什么它区分"相似"和"相关"
- [ ] 解释内在评估（Intrinsic）vs 外在评估（Extrinsic）的区别
- [ ] 计算余弦相似度：$\cos(\mathbf{u}, \mathbf{v}) = \dfrac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$
- [ ] 解释为什么 "quick/rapid" SimLex=9.70 但词嵌入相似度只有约 0.50
- [ ] 解释 Pearson 相关系数如何量化模型与人类的一致程度
- [ ] 理解 Word2Vec 在专业词上的优势和 GloVe 在描述词上的优势

### Part 2: FastText 和类比

- [ ] 写出 FastText 的 n-gram 分解过程（加 `<` `>` 边界符）
- [ ] 解释为什么 "bananna" FastText 相似度高（0.78）而 "sciience" 低（0.07）
- [ ] 写出词类比公式：$\text{vec}(A) - \text{vec}(B) + \text{vec}(C) \approx \text{vec}(D)$
- [ ] 解释 "Computer Programmer - Man + Woman = Nursing" 揭示了什么问题
- [ ] 解释词嵌入中的性别偏见来自哪里（训练数据的统计规律）
- [ ] 解释"语义漂移"：为什么 "Intelligent - Scientist + Woman" ≈ "man"

### 代码理解

- [ ] 为什么处理 Word2Vec 时需要先检查 `key_to_index`？
- [ ] FastText 用 `get_word_vector()` 而不是 `key_to_index` 检查，为什么？
- [ ] 词类比搜索为什么限制前 50,000 词而不是全部 200 万词？
- [ ] `scipy.stats.pearsonr` 或 `df['a'].corr(df['b'])` 返回的是什么？

---

*生成自：[labs/CST8507_Lab_3_W26.md](../labs/CST8507_Lab_3_W26.md) · [code/lab3/](../code/lab3/) · [lecture4_storyline.md](./lecture4_storyline.md)*
