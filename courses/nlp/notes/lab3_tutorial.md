# Lab 3 Tutorial: 词嵌入深度教程

> **数学前置：**
> [内积与余弦相似度](../../math/linear-algebra/inner_product.md) | [向量范数](../../math/linear-algebra/norms_distances.md) | [协方差与相关系数](../../math/statistics/mean_variance.md#§3-covariance--correlation-协方差与相关性)
>
> **配套故事线：** [lab3_storyline.md](./lab3_storyline.md)
> **配套 Slides：** [lecture4_slides.md](./lecture4_slides.md)（Week 4: Word Embedding）

---

> **Slides 没讲什么？本教程补充什么？**
>
> | 概念 | Slides 覆盖程度 | 本教程补充 |
> |---|---|---|
> | 余弦相似度 | 公式出现，无推导 | 几何意义、为什么不用欧式距离 |
> | GloVe 目标函数 | 描述原理，无公式 | Weighted least squares 推导 |
> | FastText n-gram 算法 | 示意图 | 完整两步更新机制 |
> | Pearson 相关系数 | 提及"评估"，无公式 | 公式推导 + 与余弦相似度的关系 |
> | 词类比的原理 | 举 king-queen 例子 | 为什么向量算术能编码语义关系 |
> | 词嵌入偏见 | 列为"Limitation" | 偏见来源的数学机制 |
> | **命名由来与历史** | ❌ 无 | → 独立文件 [lab3_history.md](./lab3_history.md) |

---

> 📖 **命名由来与历史** → 独立文件 [lab3_history.md](./lab3_history.md)

---

## §0 前置知识：在看任何公式之前

本教程用到两个数学工具，在数学前置文件中已详细推导，这里只列出**本教程需要的结论**：

> 📎 **来自** [inner_product.md](../../math/linear-algebra/inner_product.md) + [norms_distances.md](../../math/linear-algebra/norms_distances.md)

**内积（点积）：** $\mathbf{u} \cdot \mathbf{v} = \sum_i u_i v_i$

**向量范数：** $\|\mathbf{u}\| = \sqrt{\mathbf{u} \cdot \mathbf{u}} = \sqrt{\sum_i u_i^2}$

**关键几何事实：** $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\| \|\mathbf{v}\| \cos\theta$，其中 $\theta$ 是两向量的夹角。

> 📎 **来自** [mean_variance.md §3](../../math/statistics/mean_variance.md)

**Pearson 相关系数** 是将随机变量先零均值化，再求归一化内积的结果——形式上与余弦相似度同构。

---

## §1 余弦相似度：Slides 只给公式，但没给理由

### 1.1 公式（Slides 给了）

$$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$

### 1.2 Slides 没讲：为什么不用欧式距离？

欧式距离 $d(\mathbf{u}, \mathbf{v}) = \|\mathbf{u} - \mathbf{v}\|$ 对词向量有一个**致命问题**：

**词频影响向量长度。** "apple" 在语料库中出现 100,000 次，它的向量经过更多梯度更新，数值可能比出现 100 次的 "apricot" 大得多。欧式距离把**长度差异**误读为**语义距离**。

$$\|\mathbf{u} - \mathbf{v}\| \text{ —— 受向量长度影响，高频词与低频词"看起来更远"}$$

余弦相似度把两向量都归一化到单位球面上，只比较**方向**，不比较**长度**：

$$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u}}{\|\mathbf{u}\|} \cdot \frac{\mathbf{v}}{\|\mathbf{v}\|}$$

**实验验证：** Lab 3 代码直接调用 `model.similarity(w1, w2)`，gensim 内部实现就是归一化后的内积——即余弦相似度。

### 1.3 几何解释

$$\cos\theta = \begin{cases} 1 & \text{方向完全相同（最相似）} \\ 0 & \text{正交（不相关）} \\ -1 & \text{方向相反（极少发生，除非显式引入对立训练信号）}\end{cases}$$

在词向量空间中，余弦相似度几乎总是正数：词嵌入通过加性组合学习，向量通常指向"正象限"。

### 1.4 余弦相似度 vs SimLex-999 的范围不对等

注意：

- 余弦相似度范围：$[-1, 1]$，实际词向量约 $[0, 1]$  
- SimLex-999 范围：$[0, 10]$，需归一化为 $[0, 1]$ 才能比较

Lab 1 代码的处理：

```python
df_analysis['simlex_norm'] = df_analysis['SimLex999'] / 10.0
df_analysis['gap_w2v'] = df_analysis['simlex_norm'] - df_analysis['similarity_w2v']
```

这个 "gap" 就是**低估量**——词嵌入比人类更保守地评估相似度。

---

## §2 GloVe 目标函数：Slides 描述了原理，但没给公式

### 2.1 Slides 告诉我们的

GloVe 构建词-词共现矩阵 $X$，其中 $X_{ij}$ = 词 $i$ 在词 $j$ 的上下文中出现的次数。  
然后学习向量使得 $\mathbf{w}_i \cdot \mathbf{w}_j \approx \log X_{ij}$。

### 2.2 Slides 没有给的：完整目标函数

> 📚 Ref: Pennington et al. (2014) — "GloVe: Global Vectors for Word Representation", Eq. (8)

$$J = \sum_{i,j=1}^{V} f(X_{ij}) \left( \mathbf{w}_i^T \tilde{\mathbf{w}}_j + b_i + \tilde{b}_j - \log X_{ij} \right)^2$$

**符号解释 Symbol Table：**

| 符号 | 含义 |
|---|---|
| $V$ | 词汇表大小 |
| $X_{ij}$ | 词 $j$ 在词 $i$ 上下文中出现的共现次数 |
| $\mathbf{w}_i$ | 词 $i$ 的中心词向量（center vector）|
| $\tilde{\mathbf{w}}_j$ | 词 $j$ 的上下文词向量（context vector）|
| $b_i, \tilde{b}_j$ | 偏置项（bias terms）|
| $f(X_{ij})$ | 权重函数（weighting function）|

### 2.3 权重函数 $f$：解决高频词主导问题

$$f(x) = \begin{cases} \left(\dfrac{x}{x_{\max}}\right)^\alpha & x < x_{\max} \\ 1 & x \geq x_{\max} \end{cases} \quad \text{Pennington et al. (2014), 使用 } x_{\max}=100, \alpha=3/4$$

**意义：** "the"、"a" 等高频词的共现次数极大，不加权重它们会主导损失函数。$f$ 让高频词的权重饱和为 1，给罕见词对一定的权重（不为零）。

### 2.4 为什么 Lab 3 中 GloVe 和 Word2Vec 各有所长？

目标函数的差异直接解释了实验结果：

- **GloVe 使用全局 $X_{ij}$：** 词 $i$ 和词 $j$ 在整个语料库中的总共现次数被编码进向量。Wikipedia 语料覆盖广，描述性文字（boundary/border、hallway/corridor）的全局共现更丰富 → GloVe 在描述词上更好。
- **Word2Vec 使用局部窗口：** 每次只看几个邻居。Google News 的新闻文体使得专业术语（attorney/lawyer、physician/doctor）在相邻句子里频繁共现 → Word2Vec 在专业域词上更好。

---

## §3 FastText 子词建模：完整两步机制

### 3.1 Slides 讲到了（但是示意图）

Slides（Page 47）说有两步更新，但没有给出完整的算法。

### 3.2 完整的 n-gram 表示

> 📚 Ref: Bojanowski et al. (2017) — "Enriching Word Vectors with Subword Information", §2

对词 $w$，构造其字符 n-gram 集合 $G_w \subset \{1, \ldots, G\}$（$G$ 为 n-gram 词典大小）：

$$G_w = \{\text{所有长度 3–6 的字符 n-gram}\} \cup \{w\}$$

词边界标记 `<` 和 `>` 加在词首尾，使得 n-gram 能区分词内位置。

**例子：** `"where"` (n=3)

$$G_{\text{where}} = \{\ \texttt{<wh},\ \texttt{whe},\ \texttt{her},\ \texttt{ere},\ \texttt{re>},\ \texttt{<where>}\ \}$$

词向量为所有 n-gram 向量的和：

$$\mathbf{v}(w) = \sum_{g \in G_w} \mathbf{z}_g$$

其中 $\mathbf{z}_g$ 是 n-gram $g$ 的可训练向量。

### 3.3 两步更新机制（Page 47 说明的细节）

Slides 的 Page 47 指出了一个微妙但重要的不对称设计：

**中心词**（被预测的词）：
$$\mathbf{v}(\text{center}) = \sum_{g \in G_{\text{center}}} \mathbf{z}_g \quad \text{（用 n-gram 向量的和）}$$

**上下文词**（用来预测的词）：
$$\mathbf{v}(\text{context}) = \mathbf{w}_{\text{context}} \quad \text{（直接用词级别向量，不用 n-gram 展开）}$$

**为什么不对称？**
- 中心词需要子词信息（我们要学习它的向量，子词帮助泛化）
- 上下文词的角色是提供"是否共现"的信号，不需要子词泛化

### 3.4 为什么 "sciience" 相似度低（0.07）？

```
"science"   n-grams (n=3): sci, cie, ien, enc, nce  (5个)
"sciience"  n-grams (n=3): sci, cii, iie, ien, enc, nce  (6个)

共享: sci, ien, enc, nce  (4个)
独有（"sciience"）: cii, iie  (2个"噪声" n-gram)

共享率 ≈ 4/6 ≈ 0.67（但这些独有 n-gram 几乎不存在于训练数据中，
           它们的向量接近零向量）
→ vec("sciience") 被这两个几乎为零的 n-gram 拉偏
→ 与 vec("science") 的余弦相似度骤降至 0.07
```

对比 "bananna"：
```
"banana"   n-grams: ban, ana, nan, ana, na>   ← 注意有重复 n-gram
"bananna"  n-grams: ban, ana, nan, nan, ann, nan  ← 大量重叠
共享率极高 → 相似度 0.78
```

---

## §4 Pearson 相关系数：为什么它是正确的评估指标

### 4.1 公式

> 📚 参见 [mean_variance.md §3.2](../../math/statistics/mean_variance.md)

给定两个数值序列 $X = (x_1,\ldots,x_n)$ 和 $Y = (y_1,\ldots,y_n)$：

$$r(X, Y) = \frac{\sum_i (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_i (x_i - \bar{x})^2} \cdot \sqrt{\sum_i (y_i - \bar{y})^2}}$$

在 Lab 3 中：$X$ = 词嵌入余弦相似度，$Y$ = SimLex999 归一化分数，$n$ = 60（Top 60 词对）。

### 4.2 Pearson 相关 = 归一化向量的余弦相似度

注意：

$$r(X, Y) = \frac{(X - \bar{X}) \cdot (Y - \bar{Y})}{\|X - \bar{X}\| \cdot \|Y - \bar{Y}\|}= \cos(\hat{X}, \hat{Y})$$

其中 $\hat{X}$ 和 $\hat{Y}$ 是 $X$ 和 $Y$ 各自零均值化后的版本。

**洞察：** Pearson 相关系数本质上就是对随机变量做了余弦相似度。评估词嵌入质量时，我们在问：**余弦相似度的排序**和**人类评分的排序**在统计上相关吗？

### 4.3 为什么用 Pearson 而不用 Spearman？

| | Pearson | Spearman |
|---|---|---|
| **假设** | 线性关系 | 单调关系（不要求线性）|
| **依据** | 实际数值差异 | 排名差异 |
| **Lab 3 选择** | ✅（直接的线性假设）| 更保守，不受异常值影响 |

Slides 没有指定用哪个，Lab 3 代码用了 `df.corr()`（pandas 默认 Pearson）。

---

## §5 词类比的线性代数解释

### 5.1 Slides 只给了结果

`king - man + woman ≈ queen`  

为什么向量算术能编码这种关系？Slides 没有解释。

### 5.2 语义方向是向量空间的结构

设在高维词向量空间中，"性别方向"可以近似为一个向量：

$$\mathbf{d}_{\text{gender}} = \mathbf{v}(\text{man}) - \mathbf{v}(\text{woman})$$

如果词嵌入训练得好，这个方向是**稳定的**——即无论是 king/queen、actor/actress、uncle/aunt，从男词到对应女词的偏移量大致相同。

于是：

$$\mathbf{v}(\text{king}) - \mathbf{d}_{\text{gender}} = \mathbf{v}(\text{king}) - \mathbf{v}(\text{man}) + \mathbf{v}(\text{woman}) \approx \mathbf{v}(\text{queen})$$

**这是一个经验规律，不是保证。** 条件：
1. 词嵌入需要足够大的训练语料
2. 被类比的关系需要在语料库中有一致的统计表现
3. 词的多义性不能太强（"king" 在领域内主要指皇权）

### 5.3 为什么 "Computer Programmer - Man + Woman ≠ Computer Programmers (female)"？

理想情况：

$$\mathbf{v}(\text{programmer}) - \mathbf{d}_{\text{gender}} \approx \mathbf{v}(\text{female\_programmer})$$

但实际：结果是 "Nursing"。

原因：在训练数据（Google News / Wikipedia）中，"computer programmer" 与 "man" 的共现强度远大于与 "woman"。这导致：

$$\mathbf{v}(\text{programmer}) \approx \mathbf{v}(\text{man}) + \mathbf{\delta}_{\text{tech}}$$

减去 $\mathbf{v}(\text{man})$ 后剩下的 $\mathbf{\delta}_{\text{tech}}$ 并不指向 "female programmer"，而是指向训练数据中与"女性"最接近的职业方向——护理。

> 📚 这一现象在 Bolukbasi et al. (2016) — "Man is to Computer Programmer as Woman is to Homemaker?" 中有系统研究。

### 5.4 实验的搜索局限

Lab 3 代码限制了搜索范围：

```python
CANDIDATE_LIMIT = 50000
candidates = ft_model.get_words()[:CANDIDATE_LIMIT]
```

FastText 有 200 万词汇，只取前 50,000（高频词）。这意味着：

- 如果正确答案是低频词，会被漏掉
- "queen" 足够高频，侥幸在前 50,000 内
- "female computer programmer" 的概念可能用低频词描述，被截断

---

## §6 词嵌入偏见：Slides 列为"Limitation"，但没有解释机制

### 6.1 偏见是怎么"学进去"的？

词嵌入的目标：让相似上下文的词有相近向量。问题在于，训练语料是人类写的，人类写的文本反映了社会现实（及其刻板印象）：

```
Google News 数据里（统计事实，不是价值判断）：
  "She is a nurse"        出现频率：高
  "She is a programmer"   出现频率：低
  "He is a programmer"    出现频率：高
  "He is a nurse"         出现频率：低
```

这些统计规律被词嵌入直接编码为向量空间的几何结构。

### 6.2 为什么关系到 Lab 3 的类比实验？

类比推理放大了这种偏见：

$$\mathbf{v}(\text{doctor}) - \mathbf{v}(\text{man}) + \mathbf{v}(\text{woman})$$

在语料库中 "doctor" 与 "man" 共现更频繁，所以差值向量指向"女性+医疗相关但非主科医生"的方向，得到 "pediatrician"、"midwife"。

### 6.3 Slides 没给的：这不是 FastText 特有的

实验用 FastText，但 Word2Vec 和 GloVe 也有同样的偏见。Bolukbasi et al. (2016) 在 Word2Vec 上首次系统报告了这一现象。

**科研关注：** 去偏方法（debiasing）是 NLP 研究的活跃方向，包括：

- Hard debiasing（投影消除性别方向）
- Soft debiasing（正则化）
- 训练数据平衡
- 对抗训练

---

> 📋 **实验代码输出解读** → 独立文件 [lab3_output_guide.md](./lab3_output_guide.md)  
> 先读该文档，再运行 Part 1/Part 2 实验代码，每行输出的含义都在里面解释了。

---

## 参考索引

| 教程章节 | 核心内容 | Slides 覆盖？ |
|---|---|---|
| §1 余弦相似度 | 为什么不用欧式距离；几何意义 | 公式有，理由无 |
| §2 GloVe 目标函数 | Weighted least squares，$f(x)$ 权重函数 | ❌ 无公式 |
| §3 FastText 完整算法 | 两步不对称更新；n-gram 共享率分析 | 示意图有，公式无 |
| §4 Pearson 相关系数 | 公式推导；与余弦相似度的等价关系 | 仅提及"评估" |
| §5 词类比原理 | 语义方向假设；搜索范围的局限 | 只有例子 |
| §6 词嵌入偏见机制 | 偏见的统计来源；去偏研究方向 | 列为 Limitation |
| 实验输出解读 | → [lab3_output_guide.md](./lab3_output_guide.md)（Part 1 Step 6 + Part 2 全部输出） | ❌ 无 |

---

*生成自：[lecture4_slides.md](./lecture4_slides.md) · [lab3_storyline.md](./lab3_storyline.md)*  
*参考：Bojanowski et al. (2017) · Pennington et al. (2014) · Bolukbasi et al. (2016)*
