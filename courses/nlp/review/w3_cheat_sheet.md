# W3: Text Vectorization & Similarity (文本向量化与相似度)

## 1. Definitions (定义)

### Text Representation Methods (文本表示方法)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| OHE (One-Hot Encoding, 独热编码) | 用二进制向量表示词：词所在位置为1，其余全0；不含任何语义信息 | 词表 [cat,dog,fish] → cat=[1,0,0], dog=[0,1,0] |
| BOW (Bag-of-Words, 词袋模型) | 统计每个词在文档中出现的次数，忽略词序 | "the cat sat on the mat" → {the:2, cat:1, sat:1, on:1, mat:1} |
| N-gram (N元组) | 连续N个词组成的词组，部分保留词序信息 | Bigram(2-gram): "I love NLP" → ["I love", "love NLP"] |
| TF-IDF (词频-逆文档频率) | 衡量词对文档的重要性：本文档高频 + 其他文档低频 = 重要 | "NLP" 在本文出现10次但只在5篇中出现 → TF-IDF高 |
| Cosine Similarity (余弦相似度) | 测量两个向量**方向**的相似度，不受向量长度影响，范围 [-1, 1] | cos=1.0 表示方向完全相同; cos=0 表示正交无关 |
| Euclidean Distance (欧氏距离) | 两个向量之间的直线距离，受向量长度影响 | d([1,0], [0,1]) = √2 ≈ 1.41 |
| Edit Distance (编辑距离, Levenshtein) | 把一个字符串变成另一个所需的最少操作次数 (插入/删除/替换) | "kitten"→"sitting" = 3次操作 |
| Feature Explosion (特征爆炸) | N-gram 中 N 增大时，词表大小呈指数增长 (V^N)，导致维度灾难 | Unigram 词表1万 → Bigram 可达1亿 |
| Sparsity (稀疏性) | 向量中大部分元素为0，传统表示法 (OHE/BOW/TF-IDF) 的共同问题 | 词表10000维，一篇文档可能只用到50个词 → 99.5%是0 |
| OOV (Out-of-Vocabulary, 词表外词) | 不在训练词汇表中的词，传统方法无法处理 | "ChatGPT" 在2010年训练的模型里不存在 → OOV |

### Word Embeddings (词嵌入)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Word Embedding (词嵌入) | 把词映射到低维稠密向量空间，语义相似的词在空间中距离更近 | "king" → [0.2, -0.5, 0.8, ...] (300维稠密向量) |
| Word2Vec (词向量) | Google 提出的词嵌入模型，在 Google News (~100B词) 上训练 | 3M词，300维；捕捉语义类比关系 |
| GloVe (全局向量) | Stanford 提出，基于全局词共现矩阵训练的词嵌入 | 在 Wikipedia + Gigaword 上训练，400K词，300维 |
| FastText (快速文本) | Facebook 提出，把词拆成字符 n-gram 之和，能处理 OOV 和拼写错误 | "apple" = vec("<ap") + vec("app") + vec("ple") + vec("le>") |
| Sub-word (子词) | FastText 用的字符级片段，让模型能处理未见过的词 | "apple" → ["<ap","app","ppl","ple","le>"] |
| SimLex-999 (人类语义相似度基准) | 999个词对的人类标注相似度分数数据集，用于评估词嵌入质量 | (happy, cheerful) = 9.55/10; (car, tree) = 0.50/10 |
| Pearson Correlation (皮尔逊相关系数) | 衡量两组分数线性相关性的指标，范围 [-1,1]，越高说明嵌入越接近人类判断 | W2V vs SimLex r=0.45 → 中等相关 |
| Word Analogy (词类比) | 验证嵌入是否捕捉语义关系：A-B+C=? | king-man+woman ≈ queen |

### Sklearn Vectorization API

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| `CountVectorizer` (计数向量器) | 把文本转成词频矩阵（原始计数），所有词权重相等 | "the cat" → [1, 1] |
| `TfidfVectorizer` (TF-IDF向量器) | 把文本转成 TF-IDF 加权矩阵，稀有词权重更高 | "the cat" → [0.0, 0.7] ("the"权重低) |
| `ngram_range=(1,2)` | 同时生成 unigram + bigram 特征 | "I love NLP" → ["I","love","NLP","I love","love NLP"] |
| `max_features` (最大特征数) | 限制词表大小，避免维度灾难 | 10万唯一词 → 只保留频率最高的1万词 |
| `stratify=y` | `train_test_split` 中保持类别分布一致 | 70%正/30%负 → 训练集和测试集保持相同比例 |

### Evaluation Metrics (评估指标)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Confusion Matrix (混淆矩阵) | 分类结果的2×2表格：TP/FP/FN/TN，揭示每个类别的表现 | TP=80, FP=5, FN=10, TN=105 |
| Weighted F1 (加权F1) | 按各类别样本量加权的 F1 分数，适用于不平衡数据集 | 90%A类+10%B类 → weighted F1 考虑不平衡 |
| Accuracy (准确率) | 预测正确的比例，但在不平衡数据集上可能有误导性 | 95% accuracy 但少数类 recall=0% → 实际很差 |

### Evolution of Representations (表示方法演进)

| Stage (阶段) | Methods (方法) | Semantic? (语义?) | Example (示例) |
|-------|---------|-----------|---------|
| Traditional (传统方法) | OHE → BOW → N-gram → TF-IDF | ❌ 不含语义 | 无法知道 "king" 和 "queen" 有关系 |
| Deep (深度方法) | Word2Vec → GloVe → FastText → Contextual | ✅ 含语义 | king-man+woman ≈ queen |

## 2. Comparisons (对比)

### BOW vs N-gram vs TF-IDF

| Dimension (维度) | BOW (词袋) | N-gram (N元组) | TF-IDF (词频-逆文档频率) | Example (示例) |
|-----------|-----|--------|--------|---------|
| Word order (词序) | ❌ 完全忽略 | ⚠️ 局部保留 (N个词内) | ❌ 完全忽略 | "dog bites man" = "man bites dog" (BOW) |
| Vocab size (词表大小) | V | V^N (指数爆炸) | V | V=10K → bigram 可达 100M |
| Weighting (权重) | 原始计数 | 原始计数 | 加权 (稀有词↑ 常见词↓) | "the"=0 权重 vs "serendipity"=高权重 |
| Semantic (语义) | ❌ 无 | ❌ 无 | ❌ 无 | 都不知道 "happy" ≈ "joyful" |
| OOV (词表外) | ❌ 无法处理 | ❌ 无法处理 | ❌ 无法处理 | 新词 "ChatGPT" 在旧模型中不存在 |

### Word2Vec vs GloVe vs FastText (三大词嵌入对比)

| Dimension (维度) | Word2Vec | GloVe | FastText | Example (示例) |
|-----------|----------|-------|----------|---------|
| Provider (来源) | Google | Stanford | Facebook | 三家科技巨头/名校 |
| Training (训练数据) | Google News (100B词) | Wikipedia+Gigaword | Common Crawl | 不同语料 → 不同偏见 |
| OOV Handling (处理新词) | ❌ 无法处理 | ❌ 无法处理 | ✅ 子词组合 | "appple"(错拼): W2V=N/A; FT≈0.95 |
| Method (方法) | 预测上下文 (CBOW/Skip-gram) | 全局共现矩阵 | 字符n-gram之和 | FastText拆词为子片段 |
| Analogy (类比能力) | ✅ 好 | ✅ 好 | ✅ 好 | king-man+woman≈queen |

### Cosine Similarity vs Euclidean Distance (相似度 vs 距离)

| Dimension (维度) | Cosine Similarity (余弦相似度) | Euclidean Distance (欧氏距离) | Example (示例) |
|-----------|-------------------|-------------------|---------|
| Measures (测量的是) | 向量**方向**的相似度 (角度) | 向量**位置**的距离 (直线) | 方向相同但长度不同: cos=1, 但 d≠0 |
| Range (范围) | [-1, 1] | [0, ∞) | cos=0.84 → 非常相似; d=0.5 → 较近 |
| Vector length (向量长度) | ❌ 不受影响 (归一化) | ✅ 受影响 | 文档长短不影响 cos, 但影响 d |
| Best for (适用场景) | 文本相似度 (NLP首选) | 空间距离 (物理位置) | NLP 用 cos; KNN 用 Euclidean |

### CountVectorizer vs TfidfVectorizer

| Dimension (维度) | CountVectorizer (计数) | TfidfVectorizer (TF-IDF) | Example (示例) |
|-----------|-----------------|-----------------|---------|
| Output (输出) | 原始词频计数 | TF-IDF 加权值 | "the":Count=5; TF-IDF≈0.0 |
| Effect (效果) | 所有词权重相同 | 稀有词权重高，常见词权重低 | "NLP" 被加权; "the" 被压低 |
| `ngram_range` | 生成 uni/bi/tri-gram | 同上 + TF-IDF 加权 | (1,2) = unigram + bigram |

## 3. Formulas (公式)

### TF-IDF Calculation (TF-IDF 计算)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\text{TF}(t,d) = \frac{\text{count}(t \in d)}{\text{total words in } d}$ | 词在文档中的出现比例 | "cat" 出现3次, 文档100词 → TF=0.03 |
| $\text{IDF}(t) = \log\frac{N}{df(t)}$ | 逆文档频率：出现在越少文档中的词越重要 | N=1000篇, "cat"出现在10篇 → IDF=log(100)=2 |
| $\text{TF-IDF} = \text{TF} \times \text{IDF}$ | 两项相乘得到最终权重 | 0.03 × 2 = 0.06 |
| $df = N \Rightarrow \text{IDF} = 0$ | 出现在所有文档中的词 → 权重为0 (如 "the") | log(1000/1000)=log(1)=0 |
| $df = 1 \Rightarrow \text{IDF} = \log N$ | 仅出现在1篇中 → 最高权重 | log(1000/1)=log(1000)≈3 |

### Similarity Measures (相似度公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\cos(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \times \|\mathbf{B}\|}$ | 余弦相似度：点积 / 两个模的乘积 | A·B=0.73, ‖A‖=0.81, ‖B‖=1.07 → cos=0.84 |
| $d(\mathbf{A}, \mathbf{B}) = \sqrt{\sum_{i}(a_i - b_i)^2}$ | 欧氏距离：各维差值平方和的平方根 | d([1,0],[0,1]) = √(1+1) = √2 |
| $\text{Lev}(a,b) = \min(\text{insert, delete, substitute})$ | 编辑距离：最少操作次数 | "kitten"→"sitting" = 3次 |

### Cosine Similarity Worked Example (计算演练)

| Step (步骤) | Value (值) | Example (示例) |
|------|-------|---------|
| $\mathbf{w_1} = (0.2, 0.2, 0.3, 0.7)$ | 第一个向量 | 4维TF-IDF向量 |
| $\mathbf{w_2} = (0.3, 0.4, 0.8, 0.5)$ | 第二个向量 | 同维度对比向量 |
| $\mathbf{A} \cdot \mathbf{B} = 0.06+0.08+0.24+0.35 = 0.73$ | 点积 | 对应元素相乘再求和 |
| $\|\mathbf{A}\| = \sqrt{0.04+0.04+0.09+0.49} \approx 0.81$ | 向量A的模 | 各元素平方和开根号 |
| $\|\mathbf{B}\| = \sqrt{0.09+0.16+0.64+0.25} \approx 1.07$ | 向量B的模 | 同上 |
| $\cos = \frac{0.73}{0.81 \times 1.07} \approx 0.84$ | 最终结果 | 0.84 → 两个文档非常相似 |

## 4. Practical / Lab (实战结论)

### 🔑 Key API Distinctions (关键API区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|-------------|--------|---------|
| `CountVectorizer` = 原始计数 | `TfidfVectorizer` = 加权 (稀有词↑) | "the cat" → Count:[1,1]; TF-IDF:[0.0, 0.7] |
| `ngram_range=(1,2)` | 同时生成 unigram + bigram 特征 | "I love NLP" → 5个特征 (3个uni+2个bi) |
| `max_features=10000` | 限制词表大小避免维度灾难 | 100K词 → 保留top 10K |
| `stratify=y` in `train_test_split` | 保持类别分布一致 | 70%pos/30%neg → 两个集合比例相同 |

### 📊 Lab 3 Part 1 结论: Word2Vec vs GloVe (SimLex-999 评估)

| Finding (发现) | Detail (详情) | Example (示例) |
|---------|--------|---------|
| 两个模型与人类判断的相关性都是中等水平 | Pearson 相关系数 ≈ 0.4-0.5，说明嵌入捕捉了部分但非全部语义 | W2V: r≈0.45; GloVe: r≈0.42 |
| 嵌入会低估某些高相似度词对 | 人类认为很相似但嵌入 cosine 值低 → 嵌入缺乏某些常识 | (smart, clever): SimLex=9.0 但 W2V≈0.5 |
| Word2Vec 和 GloVe 对同一词对可能差异大 | 训练数据不同导致不同语义偏向 | 某些词 W2V 和 GloVe 差 >0.3 |
| `model.similarity(w1, w2)` 计算余弦相似度 | gensim API，直接返回两个词的 cosine 值 | `w2v_model.similarity("king","queen")` → ~0.65 |

### 📊 Lab 3 Part 2 结论: FastText 子词与拼写错误

| Finding (发现) | Detail (详情) | Example (示例) |
|---------|--------|---------|
| FastText 能处理拼写错误，Word2Vec 不能 | FastText 用子词 (sub-word) 组合向量 → OOV词也有向量; W2V 返回 N/A | "appple"(拼错): FT≈0.95; W2V=N/A |
| king-man+woman ≈ queen 类比成功 | 验证词嵌入确实捕捉了性别等语义关系 | similarity ≈ 0.65 |
| 词嵌入存在性别偏见 (Gender Bias) | "programmer-man+woman" → nursing/caregiving 而非 programmer | 反映训练数据中的社会偏见 |
| 抽象类比会产生语义漂移 (Semantic Drift) | "intelligent-scientist+woman" → 只剩 "person" 成分，丢失智力含义 | 减去太多语义 → 结果无意义 |

### 📊 Assignment 1 结论

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------|
| TF-IDF + LogReg 经常能媲美词嵌入方法 | 简单基线出人意料地强，不一定需要复杂模型 | TF-IDF+LogReg: 85% vs W2V+LogReg: 84% |
| 必须先拆分数据再做预处理 | ⚠️ 避免数据泄漏 (Data Leakage)！考试重点！ | ❌ fit TF-IDF on ALL → split; ✅ split → fit on train only |
| 不平衡分类用 `average='weighted'` F1 | 普通 F1 不考虑类别样本量差异 | 90%A+10%B → weighted F1 更公平 |
| 混淆矩阵比准确率更有用 | 准确率可能有误导性，混淆矩阵揭示每个类别的问题 | 95% acc 但少数类 recall=0% |

### ⚠️ W3 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------|
| BOW 保留词序? | ❌ BOW 完全忽略词序！只数词频 | "dog bites man" = "man bites dog" (BOW 中相同) |
| TF-IDF 包含语义信息? | ❌ TF-IDF 只是统计权重，不理解语义 | 不知道 "happy" ≈ "joyful" |
| 余弦相似度受向量长度影响? | ❌ 不受长度影响！只看方向 (角度)；欧氏距离才受长度影响 | 长文档vs短文档: cos不变, 但 Euclidean变大 |
| Word2Vec 能处理拼写错误? | ❌ Word2Vec 无法处理 OOV 词！FastText 才可以 (子词机制) | "appple": W2V=N/A; FastText≈0.95 |
| N-gram 的 N 越大越好? | ❌ N 越大词表指数爆炸 (V^N)，特征太稀疏反而效果差 | Unigram:10K → Bigram:100M → Trigram:1T |
| IDF=0 是什么意思? | 该词出现在所有文档中 (df=N) → 完全没有区分度 → 权重为0 | "the" 在每篇文档都有 → IDF=log(N/N)=0 |
