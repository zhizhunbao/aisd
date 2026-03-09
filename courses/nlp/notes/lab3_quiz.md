# Lab 3 Quiz: 词嵌入 | Word Embeddings

> 配套资料：[故事线](./lab3_storyline.md) | [教程](./lab3_tutorial.md) | [概念速查](./lab3_concepts.md) | [公式速查](./lab3_math.md)

---

## 第一部分：概念理解

**Q1.** SimLex-999 与 WordSimilarity-353 的核心区别是什么？

<details><summary>答案</summary>

SimLex-999 严格衡量**语义相似度（Semantic Similarity）**，不包含"语义相关"的词对。WordSimilarity-353 混合了"相似性"和"相关性"。例如，"coffee" 和 "cup" 在 WS-353 中得分高，但在 SimLex-999 中得分低，因为它们是相关的而非相似的。

</details>

---

**Q2.** 为什么词嵌入实验使用余弦相似度而不是欧氏距离来比较词向量？

<details><summary>答案</summary>

词频高的词会在训练过程中获得更多梯度更新，导致其向量的**长度（模长）**更大。欧氏距离同时受方向和长度影响，而余弦相似度只比较方向，不受向量长度影响——因此能消除词频偏差，更准确地衡量语义相似性。

</details>

---

**Q3.** 下面哪对词在 SimLex-999 中得分更高？为什么？

- A: (coffee, tea)  
- B: (smart, intelligent)

<details><summary>答案</summary>

**B: (smart, intelligent)** 得分更高。  
"smart" 和 "intelligent" 含义高度重叠，是近义词（语义相似）。  
"coffee" 和 "tea" 虽然都是饮料（相关），但含义本身并不相似——SimLex-999 不承认这种相关性为相似性。

</details>

---

**Q4.** Word2Vec 和 GloVe 在训练方式上的根本区别是什么？

<details><summary>答案</summary>

- **Word2Vec**：基于**预测**的方法，用神经网络在局部滑动窗口中预测中心词或上下文词。
- **GloVe**：基于**计数+矩阵分解**的方法，先构建全局词-词共现矩阵，再学习使向量点积等于 log 共现次数的向量。

核心区别：Word2Vec 只看局部窗口，GloVe 利用全局统计信息。

</details>

---

**Q5.** 在 Lab 3 Part 1 实验中，为什么 Word2Vec 在 "attorney ↔ lawyer" 这对词上表现好，而 GloVe 在 "boundary ↔ border" 上表现更好？

<details><summary>答案</summary>

- **"attorney ↔ lawyer"**：这两个词是专业法律术语，在 Google News 语料（Word2Vec 的训练数据）中频繁出现在相邻语境中，使得局部窗口方法效果好。
- **"boundary ↔ border"**：这两个词是描述空间关系的词，在 Wikipedia 等描述性文字中（GloVe 的训练数据 Wikipedia+Gigaword）全局共现统计更丰富，全局矩阵方法更有优势。

</details>

---

## 第二部分：FastText 与子词建模

**Q6.** 解释 FastText 如何为从未在训练中出现过的词（OOV 词）生成向量。

<details><summary>答案</summary>

FastText 将词分解为字符 n-gram（长度 3–6，加词边界标记 `<` `>`），词向量等于所有 n-gram 向量之和：$\mathbf{v}(w) = \sum_{g \in G_w} \mathbf{z}_g$。

对于 OOV 词，即使该词本身未出现在训练数据中，其字符 n-gram 大概率已在其他词中出现过。通过组合这些已学习的 n-gram 向量，FastText 可以为 OOV 词生成有意义的向量。

</details>

---

**Q7.** 以下哪个词对，FastText 的相似度更高？为什么？
- A: science ↔ sciience  
- B: banana ↔ bananna

<details><summary>答案</summary>

**B: banana ↔ bananna** 相似度更高（实验值 ≈ 0.78）。

- "bananna" 与 "banana" 共享大量 n-gram（ban, ana, nan 等），向量相近。
- "sciience" 插入了额外的 "i"，产生了 "cii"、"iie" 等几乎不存在于训练数据的噪声 n-gram，破坏了与 "science" 的 n-gram 共享链，相似度骤降至 ≈ 0.07。

</details>

---

**Q8.** 写出 FastText 对单词 "where" 进行 3-gram 分解的结果（需包含词边界标记）。

<details><summary>答案</summary>

加词边界标记后词为 `<where>`，3-gram 分解为：

`<wh`, `whe`, `her`, `ere`, `re>`

（加上整词本身 `<where>`，共 6 个 n-gram）

</details>

---

## 第三部分：词类比与偏见

**Q9.** 写出词类比推理的数学公式，并解释为什么 king - man + woman ≈ queen。

<details><summary>答案</summary>

公式：$\mathbf{v}(D) \approx \mathbf{v}(A) - \mathbf{v}(B) + \mathbf{v}(C)$

解释：向量空间中存在一个稳定的"性别方向" $\mathbf{d} = \mathbf{v}(\text{man}) - \mathbf{v}(\text{woman})$。$\mathbf{v}(\text{king}) - \mathbf{v}(\text{man})$ 提取出"皇权"方向，再加上 $\mathbf{v}(\text{woman})$ 就在女性语义空间中找到具有相同"皇权"方向的词，即 "queen"。

</details>

---

**Q10.** Lab 3 中，"Computer Programmer - Man + Woman" 得到的结果是 "Nursing"，而不是 "Female Programmer"。这说明了什么问题？

<details><summary>答案</summary>

这说明词嵌入从训练数据中学到了**性别偏见**。在训练语料（Google News 等）中，"computer programmer" 绝大多数与男性语境共现，"nurse/nursing" 绝大多数与女性语境共现。词嵌入将这些统计偏差编码为向量空间的几何结构，类比运算放大了这种偏见，得到了刻板印象的结果，而不是理想的"语义等价的女性职业版本"。

</details>

---

**Q11.** "Intelligent - Scientist + Woman" 的结果是 "man/lady/women" 而不是智力相关的词。解释为什么会出现语义漂移。

<details><summary>答案</summary>

这是**语义漂移（Semantic Drift）**。向量运算不是完美线性的——减去 "scientist" 不仅去除了"科学家"的职业含义，还过度移除了"智力/认知"的语义成分，因为 "scientist" 在向量空间中承载了大量"智力"意义。剩下的向量只剩下"人称"成分，指向 "man/lady/women"。类比推理对复杂抽象关系的可靠性较低。

</details>

---

## 第四部分：代码理解

**Q12.** 以下代码有什么问题？如何修复？

```python
sim = w2v_model.similarity('apple', 'appple')
```

<details><summary>答案</summary>

**问题：** "appple" 不在 Word2Vec 词汇表中（OOV 词），直接调用 `.similarity()` 会抛出 KeyError。

**修复：**
```python
if 'apple' in w2v_model.key_to_index and 'appple' in w2v_model.key_to_index:
    sim = w2v_model.similarity('apple', 'appple')
else:
    sim = None  # OOV
```

</details>

---

**Q13.** 在词类比搜索中，为什么 Lab 3 代码将候选词限制在前 50,000 个词，而不是搜索全部 200 万词？

<details><summary>答案</summary>

计算效率。对 200 万个候选词，每次都需要：获取词向量、归一化、计算点积。逐一比较 200 万词的时间成本极高，对每个类比查询来说不可接受。限制到高频的前 50,000 词可以在保持大多数情况下找到正确答案的同时（正确答案通常是高频词），大幅减少计算时间。

**副作用：** 如果正确答案是低频词，可能被漏掉。

</details>

---

**Q14.** 下面代码计算的是什么？结果反映了什么含义？

```python
corr_w2v = df_valid_w2v['similarity_w2v'].corr(df_valid_w2v['SimLex999'])
```

<details><summary>答案</summary>

计算的是 **Pearson 相关系数**，衡量 Word2Vec 余弦相似度分数与 SimLex999 人工评分之间的线性相关程度。

- 值越接近 1：Word2Vec 的相似度判断与人类判断越一致（模型越"准"）
- 值越接近 0：两者无相关
- Top 60 词对是最苛刻的测试场景，如果在这里相关性低，说明模型对最明显的近义词也对不准

</details>

---

*题目覆盖：SimLex-999 · 余弦相似度 · Word2Vec vs GloVe · FastText n-gram · 词类比 · 性别偏见 · Pearson 相关系数 · OOV 处理*
