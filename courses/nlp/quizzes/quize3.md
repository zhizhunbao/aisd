# CST8507 NLP Quiz 3 — 文本表示 (Text Representation)

Topic: Edit Distance, Bag of Words, TF-IDF, Cosine Similarity, CountVectorizer

---

## Question 1 (1 point)

Given the words "intention" and "execution", what is the minimum number of operations required to transform "intention" into "execution"?

Question 1 options:

A) 3

B) 4

C) 5

D) 6

> **Answer**: C
> **Explanation**:
> This is the classic Levenshtein edit distance problem, with allowed operations: insertion, deletion, substitution. **Why 5**: Through dynamic programming, transforming "intention" → "execution" requires a minimum of 5 operations.
>
> > 这是经典的 Levenshtein 编辑距离（Edit Distance）问题，允许的操作有插入、删除、替换。**为什么是 5**：通过动态规划计算，"intention" → "execution" 最少需要 5 步操作。
>
> - **$d(s_1, s_2)$**: Edit distance — the minimum number of operations to transform string $s_1$ into $s_2$
>
> > - **$d(s_1, s_2)$**: 编辑距离 — 将字符串 $s_1$ 转换为 $s_2$ 的最小操作数
>
> **Key**: Levenshtein (edit) distance = minimum insertions, deletions, substitutions to transform one string into another.

---

## Question 2 (1 point)

In a Bag of Words representation, the order of words in a document is crucial, and each word is treated as dependent on its surrounding words.

Question 2 options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> The core characteristic of BoW (Bag of Words) is that it **ignores word order** and treats each word as an independent feature. **Why False**: The statement claims "word order is crucial" and "words are dependent on context" — these are exactly what BoW does NOT have. BoW only cares about word frequency.
>
> > BoW（词袋模型）的核心特征就是**忽略词序**，每个词被视为独立的特征。**为什么是 False**：题干说"词序至关重要"和"词与上下文相关"，这恰好是 BoW 不具备的特性。BoW 只关注词频。
>
> **Key**: Bag of Words ignores word order and treats each word independently — only word frequency matters.

---

## Question 3 (1 point)

The inverse document frequency (IDF) of a word is calculated by dividing the total number of documents by the number of documents containing the word.

Question 3 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> The IDF formula is $IDF(t) = \log\frac{N}{df(t)}$, where $N$ is the total number of documents and $df(t)$ is the number of documents containing word $t$. **Why True**: The statement describes exactly the core IDF calculation logic — total documents divided by documents containing the word (usually with log applied).
>
> > IDF 的计算公式为 $IDF(t) = \log\frac{N}{df(t)}$，其中 $N$ 是总文档数，$df(t)$ 是包含词 $t$ 的文档数。**为什么是 True**：题干描述的正是 IDF 的核心计算逻辑——用总文档数除以包含该词的文档数（通常取对数）。
>
> - **$N$**: Total number of documents in corpus (语料库总文档数)
> - **$df(t)$**: Number of documents containing word $t$ (包含词 $t$ 的文档数)
> - **$IDF(t) = \log\frac{N}{df(t)}$**: Inverse Document Frequency (逆文档频率)
>
> **Key**: $IDF(t) = \log\frac{N}{df(t)}$ — words appearing in fewer documents get higher IDF scores.

---

## Question 4 (1 point)

If the cosine similarity between the word vectors for Word A and Word B is close to 1, it means that Word A and Word B are considered highly similar in meaning.

Question 4 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> Cosine similarity measures the directional angle between two vectors, with value range $[-1, 1]$. **Why True**: When cosine similarity is close to 1, the two vectors point in nearly the same direction, indicating high semantic similarity in embedding space.
>
> > 余弦相似度衡量两个向量的方向夹角，值域为 $[-1, 1]$。**为什么是 True**：当余弦相似度接近 1 时，两个向量方向近乎一致，在词嵌入空间中表示语义高度相似。
>
> - **$\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{||\vec{A}|| \times ||\vec{B}||}$**: Cosine similarity formula (余弦相似度公式)
> - Close to 1 = same direction (similar); close to 0 = orthogonal (unrelated); close to -1 = opposite (contrary)
>
> > - 接近 1 = 方向一致（相似）；接近 0 = 正交（无关）；接近 -1 = 方向相反（相反）
>
> **Key**: Cosine similarity close to 1 → vectors point in same direction → semantically similar.

---

## Question 5 (1 point)

One of the disadvantages of using TF-IDF is:

Question 5 options:

A) It produces low-dimensional dense vectors

B) It considers the context and semantic relationships between words

C) It does not consider the context and semantic relationships between words

D) It captures word order information

> **Answer**: C
> **Explanation**:
> TF-IDF is a bag-of-words statistical method with no semantic understanding capability. **Why C**: TF-IDF only computes word frequency and document frequency — it cannot capture contextual relationships or word meaning.
>
> > TF-IDF 是基于词袋模型的统计方法，不具备语义理解能力。**为什么是 C**：TF-IDF 只统计词频和文档频率，无法捕捉上下文关系或词义。
>
> - **A**: TF-IDF produces high-dimensional sparse vectors (vocabulary size), not low-dimensional dense ones.
> - **B/D**: These are capabilities TF-IDF does NOT have — it understands neither semantic relationships nor word order.
>
> > - **A 错**：TF-IDF 产生的是高维稀疏向量（词汇表大小），不是低维密集向量。
> > - **B/D 错**：这些是 TF-IDF **不具备**的能力——它既不理解语义关系，也不保留词序。
>
> **Key**: TF-IDF is a bag-of-words statistical method — no context, no semantics, no word order. High-dimensional and sparse.

---

## Question 6 (1 point)

Given the following TF values for a word across different documents:

| Document | TF Calculation | TF Value |
| -------- | -------------- | -------- |
| d1       | 25/127         | ≈ 0.1969 |
| d2       | 3/250          | = 0.0120 |
| d3       | 20/650         | ≈ 0.0308 |
| d9       | 15/125         | = 0.1200 |
| d1000    | 20/800         | = 0.0250 |

The proposed ascending order by TF is: [d2, d1000, d3, d1, d9]

Question 6 options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> Calculate and sort TF values: d2(0.012) < d1000(0.025) < d3(0.031) < d9(0.120) < d1(0.197). **Why False**: The proposed order [d2, d1000, d3, **d1, d9**] has d1 and d9 swapped.
>
> > 计算各文档的 TF 值并排序：d2(0.012) < d1000(0.025) < d3(0.031) < d9(0.120) < d1(0.197)。**为什么是 False**：题目给出的排序 [d2, d1000, d3, **d1, d9**] 中，d1 和 d9 的位置反了。
>
> - **Correct ascending order (正确升序)**: [d2, d1000, d3, d9, d1]
> - **$TF(t,d) = \frac{f(t,d)}{|d|}$**: Term Frequency = word count in document / total words in document
>
> > - **$TF(t,d) = \frac{f(t,d)}{|d|}$**: 词频 = 词在文档中出现的次数 / 文档总词数
>
> **Key**: Correct ascending TF order: [d2, d1000, d3, d9, d1]. The proposal swapped d1 and d9.

---

## Question 7 (1 point)

Given two word vectors:

- $w_1 = (0.2, 0.2, 0.3, 0.7)$
- $w_2 = (0.3, 0.4, 0.8, 0.5)$

Calculate the cosine similarity.

> **Answer**: ≈ 0.8421
> **Explanation**:
> Step-by-step cosine similarity calculation:
>
> 1. **Dot product**: $w_1 \cdot w_2 = 0.2 \times 0.3 + 0.2 \times 0.4 + 0.3 \times 0.8 + 0.7 \times 0.5 = 0.06 + 0.08 + 0.24 + 0.35 = 0.73$
> 2. **Magnitude**: $||w_1|| = \sqrt{0.04 + 0.04 + 0.09 + 0.49} = \sqrt{0.66} \approx 0.8124$
> 3. **Magnitude**: $||w_2|| = \sqrt{0.09 + 0.16 + 0.64 + 0.25} = \sqrt{1.14} \approx 1.0677$
> 4. **Cosine similarity**: $\cos(\theta) = \frac{0.73}{0.8124 \times 1.0677} \approx \frac{0.73}{0.8674} \approx 0.8421$
>
> > 余弦相似度计算步骤：
> >
> > 1. **点积**：$w_1 \cdot w_2 = 0.06 + 0.08 + 0.24 + 0.35 = 0.73$
> > 2. **模长**：$||w_1|| = \sqrt{0.66} \approx 0.8124$
> > 3. **模长**：$||w_2|| = \sqrt{1.14} \approx 1.0677$
> > 4. **结果**：$\cos(\theta) = \frac{0.73}{0.8124 \times 1.0677} \approx 0.8421$
>
> **Key**: $\cos(\theta) = \frac{w_1 \cdot w_2}{||w_1|| \times ||w_2||} = \frac{0.73}{0.8124 \times 1.0677} \approx 0.8421$

---

## Question 8 (1 point)

```python
cv = CountVectorizer(ngram_range=(1,2)).fit(
    ["I love NLP", "He love NLP", "good man"]
)
cv.transform(["love"]).toarray()
```

Claimed output: `array([[0, 0, 1, 0, 0, 0, 0]], dtype=int64)`

Question 8 options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> `CountVectorizer(ngram_range=(1,2))` generates a vocabulary of both unigrams and bigrams. **Why False**: The training corpus produces more than 7 features, so the vector length should be longer than claimed.
>
> > `CountVectorizer(ngram_range=(1,2))` 会生成 unigram 和 bigram 的词汇表。**为什么是 False**：训练语料会生成超过 7 个特征词，向量维度不止 7。
>
> - **Vocabulary includes (词汇表包含)**: unigrams ("good", "he", "love", "man", "nlp") + bigrams ("good man", "he love", "love nlp") = at least 8 features
> - Input `"love"` only matches unigram "love", so only that position is 1, but the vector dimension should be 8+, not 7
>
> > - 输入 `"love"` 只匹配 unigram "love"，除 "love" 位置为 1 外其余为 0，但向量维度应为 8+，不是 7
>
> **Key**: `CountVectorizer(ngram_range=(1,2))` creates both unigrams and bigrams. The claimed vector length (7) is incorrect.
