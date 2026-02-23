# CST8507 NLP Quiz 4 — 词嵌入 (Word Embeddings)

Topic: TF-IDF, Word Embeddings, Word2Vec (CBOW & Skip-gram), GloVe, Self-Supervised Learning

---

## Question 1 (1 point)

While TF-IDF is useful for some applications (like search engines), its high-dimensional nature can make it difficult to use efficiently for tasks like deep learning-based NLP.

Options:

- [x] True
- [ ] False

> **Answer**: A (True)
> **Explanation**:
> TF-IDF produces vectors with dimensions equal to vocabulary size (typically tens to hundreds of thousands), and these vectors are highly sparse. **Why True**: Deep learning models work better with low-dimensional dense vectors (e.g., Word2Vec's 100–300 dimensions); high-dimensional sparse vectors lead to computational inefficiency and overfitting.
>
> > TF-IDF 产生的向量维度等于词汇表大小（通常数万到数十万），且向量高度稀疏。**为什么是 True**：深度学习模型更适合处理低维密集向量（如 Word2Vec 的 100-300 维），高维稀疏向量会导致计算效率低下和过拟合。
>
> **Key**: TF-IDF = high-dimensional sparse vectors; DL prefers low-dimensional dense embeddings.

---

## Question 2 (1 point)

Which of the following equations should hold for an effective word embedding?

Options:

- [ ] e_boy − e_brother ≈ e_sister − e_girl
- [x] e_boy − e_girl ≈ e_brother − e_sister
- [ ] e_boy − e_girl ≈ e_sister − e_brother

> **Answer**: e*boy − e_girl ≈ e_brother − e_sister
> **Explanation**:
> Effective word embeddings capture semantic relationships through vector arithmetic (analogy reasoning). **Why this option**: The difference between boy and girl represents the "gender" relationship; the difference between brother and sister should reflect the same "gender" relationship: $e*{boy} - e*{girl} \approx e*{brother} - e\_{sister}$.
>
> > 有效的词嵌入能通过向量运算捕捉语义关系（类比推理）。**为什么是第二项**：boy 和 girl 的差异代表"性别"关系，brother 和 sister 的差异也应体现相同的"性别"关系。
>
> - **Option 1**: boy - brother represents a "role type" difference, not parallel with sister - girl.
> - **Option 3**: Direction is reversed — sister - brother is opposite to boy - girl.
>
> > - **第一项错**：boy - brother 表示"角色类型"差异，与 sister - girl 不对等。
> > - **第三项错**：方向反了，sister - brother 与 boy - girl 方向相反。
>
> **Key**: Word analogy: $e_{boy} - e_{girl} \approx e_{brother} - e_{sister}$ — same semantic relationship (gender) preserved in vector space.

---

## Question 3 (1 point)

The self-supervision method in neural language modeling avoids the need for hand-labeled supervision signals by using surrounding words as implicit training data for classifiers.

Options:

- [x] True
- [ ] False

> **Answer**: A (True)
> **Explanation**:
> Self-supervised learning generates training signals from the data itself, requiring no manual labeling. **Why True**: Language models automatically obtain supervision signals by predicting missing or next words from context (e.g., CBOW predicts center word from context, Skip-gram predicts context from center word).
>
> > 自监督学习（Self-Supervised Learning）从数据本身生成训练信号，无需人工标注。**为什么是 True**：语言模型通过预测上下文中的缺失词或下一个词来自动获得监督信号（如 CBOW 用上下文预测中心词，Skip-gram 用中心词预测上下文）。
>
> **Key**: Self-supervised learning generates labels from data itself (e.g., predicting missing/next words from context).

---

## Question 4 (1 point)

One advantage of GloVe over other word embedding methods is that it is global in the sense that it considers the entire corpus to learn relationships between words, and local in the sense that it considers the co-occurrence of words within a limited context window.

Options:

- [x] True
- [ ] False

> **Answer**: A (True)
> **Explanation**:
> GloVe (Global Vectors for Word Representation) combines two information sources. **Why True**:
>
> - **Global**: Uses the entire corpus to build a global word co-occurrence matrix, counting co-occurrence across all word pairs.
> - **Local**: Co-occurrence statistics are based on a limited context window, only considering nearby words.
> - This combination captures both global statistical patterns and local contextual relationships.
>
> > GloVe（全局词向量表示）结合了两种信息来源。**为什么是 True**：
> >
> > - **全局（Global）**：利用整个语料库构建全局词共现矩阵。
> > - **局部（Local）**：共现统计基于有限的上下文窗口。
> > - 这种结合使 GloVe 既能捕捉全局统计规律，又能反映局部上下文关系。
>
> **Key**: GloVe = **Glo**bal (corpus-wide co-occurrence matrix) + **Ve**ctors (local context window). Combines both perspectives.

---

## Question 5 (1 point)

Suppose you learn a word embedding for a vocabulary of 1000 words. Should the embedding vectors be 1000 dimensional to capture the full range of variation and meaning in those words?

Options:

- [ ] True
- [x] False

> **Answer**: B (False)
> **Explanation**:
> The core value of word embeddings lies in **dimensionality reduction** — representing word meaning in far fewer dimensions than vocabulary size. **Why False**: 1000 dimensions equals one-hot encoding size, which defeats the purpose of embeddings. Typical embedding dimensions are 50–300, compressing semantic information into a low-dimensional dense space.
>
> > 词嵌入的核心价值在于**降维**——用远低于词汇表大小的维度来表示词义。**为什么是 False**：1000 维就等于 one-hot 编码的维度，失去了嵌入的意义。典型的嵌入维度为 50-300 维，通过学习将语义信息压缩到低维密集空间。
>
> **Key**: Embedding dim ≪ vocabulary size. Typical: 50–300 dimensions. 1000-dim = one-hot — defeats the purpose.

---

## Question 6 (1 point)

What is the default dimensionality of word embeddings in the Gensim Word2Vec method?

Options:

- [ ] 4000
- [ ] 120
- [x] 100
- [ ] 10

> **Answer**: 100
> **Explanation**:
> The default vector dimension parameter in Gensim's Word2Vec model is `vector_size = 100`. **Why 100**: This is the Gensim default setting, providing a balance between accuracy and computational efficiency for most tasks.
>
> > Gensim 库中 Word2Vec 模型的默认向量维度参数 `vector_size = 100`。**为什么是 100**：这是 Gensim 的默认设置，在大多数任务中提供了准确性和计算效率的平衡。
>
> - 4000 is too large (computationally expensive); 10 is too small (insufficient expressiveness); 120 is not the default.
>
> > - 4000 太大（计算昂贵）；10 太小（表达力不足）；120 不是默认值。
>
> **Key**: Gensim Word2Vec default: `vector_size=100`. Adjustable based on corpus size and task needs.

---

## Question 7 (1 point)

Word2Vec consists of two main techniques: CBOW (Continuous Bag of Words) and Skip-gram.

Options:

- [x] True
- [ ] False

> **Answer**: A (True)
> **Explanation**:
> Word2Vec includes two training architectures. **Why True**:
>
> - **CBOW**: Predicts the center word from context words (Context → Word), better for frequent words.
> - **Skip-gram**: Predicts context words from the center word (Word → Context), better for rare words and small corpora.
>
> > Word2Vec 包含两种训练架构。**为什么是 True**：
> >
> > - **CBOW**：用上下文词预测中心词（Context → Word），适合高频词。
> > - **Skip-gram**：用中心词预测上下文词（Word → Context），适合低频词和小语料。
>
> **Key**: Word2Vec = CBOW (context→word, frequent words) + Skip-gram (word→context, rare words).

---

## Question 8 (1 point)

Is the goal of the Skip-Gram model to determine the central word based on its surrounding context words?

Options:

- [ ] True
- [x] False

> **Answer**: B (False)
> **Explanation**:
> ⚠️ **Easy to confuse**: The statement describes CBOW's function, not Skip-gram's. **Why False**: Skip-gram's goal is to predict surrounding context words FROM the center word (Word → Context) — the opposite of what the statement says.
>
> > ⚠️ **易混淆题**：题干描述的是 CBOW 的功能，而非 Skip-gram。**为什么是 False**：Skip-gram 的目标是用中心词预测周围的上下文词（Word → Context），与题干所述相反。
>
> - **Skip-gram**: Input center word → predict context words
> - **CBOW**: Input context words → predict center word (what the statement actually describes)
>
> > - **Skip-gram**：输入中心词 → 预测上下文词
> > - **CBOW**：输入上下文词 → 预测中心词（题干描述的就是这个）
>
> **Key**: Skip-gram: **center word → context words**. CBOW: context words → center word. Don't confuse them!

---

## Question 9 (1 point)

Most modern NLP algorithms do not use embeddings as the representation of word meaning.

Options:

- [ ] True
- [x] False

> **Answer**: B (False)
> **Explanation**:
> Modern NLP heavily relies on word embeddings as the foundational representation. **Why False**: From Word2Vec, GloVe to pre-trained models like BERT and GPT, embeddings are the core component. Virtually all modern NLP algorithms use embeddings to represent word meaning.
>
> > 现代 NLP 高度依赖词嵌入作为基础表示。**为什么是 False**：从 Word2Vec、GloVe 到 BERT、GPT 等预训练模型，嵌入都是核心组件。几乎所有现代 NLP 算法都使用嵌入来表示词义。
>
> **Key**: Modern NLP relies heavily on embeddings (Word2Vec, GloVe, BERT, GPT). Embeddings are THE standard word representation.

---

## Quick Review Notes / 快速复习

| Concept / 概念           | Key Point / 要点                                            |
| ------------------------ | ----------------------------------------------------------- |
| TF-IDF                   | Sparse, high-dimensional, no semantics / 稀疏、高维、无语义 |
| Embeddings / 词嵌入      | Dense, low-dimensional, semantic / 密集、低维、有语义       |
| Self-supervised / 自监督 | Data generates its own labels / 数据自生成标签              |
| GloVe                    | Global statistics + local context / 全局统计 + 局部上下文   |
| Word2Vec                 | CBOW + Skip-gram                                            |
| CBOW                     | Context → Word / 上下文 → 中心词                            |
| Skip-gram                | Word → Context / 中心词 → 上下文                            |
