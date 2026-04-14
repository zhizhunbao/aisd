# W4: Word Embeddings (词嵌入)

## 1. Definitions (定义)

### Core Embedding Concepts (词嵌入核心概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Word Embedding (词嵌入) | 把词映射到低维稠密向量空间 (50-300维)，语义相似的词距离更近 | "king"→[0.2,-0.5,0.8,...] (300维实数向量) |
| Dense Vector (稠密向量) | 每个维度都有非零实数值的向量，与 OHE 的稀疏向量相反 | [0.2, -0.5, 0.8] (3维稠密) vs [0,0,1,0,0] (5维稀疏) |
| Distributional Hypothesis (分布假说) | 出现在相似上下文中的词具有相似含义 — 词嵌入的理论基础 | "cat" 和 "dog" 经常出现在 "pet", "food" 旁边 → 语义相似 |
| Context Window (上下文窗口) | 模型训练时考虑的目标词左右各多少个词 | window=2: "I [love NLP] very" → "NLP"的上下文是 love, very |
| Self-supervision (自监督) | 不需要人工标注，从文本本身构造训练信号 (预测上下文/中心词) | 用 "the cat sat on mat" 自动构造训练样本 |

### Word2Vec (Google, 2013)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Word2Vec | Google 提出的两种神经网络架构 (CBOW/Skip-gram) 学习词嵌入 | 在 Google News (~100B词) 上训练，3M词，300维 |
| CBOW (Continuous Bag-of-Words, 连续词袋) | 用周围上下文词**预测**中心词；训练更快，适合高频词 | 输入 [the, cat, on, the] → 预测 "sat" |
| Skip-gram (跳字模型) | 用中心词**预测**周围上下文词；训练更慢，但对稀有词效果更好 | 输入 "sat" → 预测 [the, cat, on, the] |
| SGNS (Skip-gram Negative Sampling) | Skip-gram的优化训练方法：随机采几个"假"上下文词作为负样本训练分类器 | 正样本:(apricot, jam); 负样本:(apricot, elephant) |
| Negative Sampling (负采样) | 从词表中随机抽取非上下文词作为负例，大幅加速训练 | `negative=5` → 每个正样本配5个随机负样本 |

### GloVe (Stanford, 2014)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| GloVe (Global Vectors, 全局向量) | Stanford 提出，先构建全局词共现矩阵，再分解学习向量 | Wikipedia+Gigaword 训练，400K词，300维 |
| Co-occurrence Matrix (共现矩阵) | 统计语料中每对词在窗口内一起出现的次数 | "I love Math" + "I love Programming" → (I,love)=2, (love,Math)=1 |

### FastText (Facebook, 2016)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| FastText (快速文本) | Facebook 提出，把词拆成字符 n-gram (3-6字符) 之和，能处理 OOV | "apple" = vec("<ap")+vec("app")+vec("ppl")+vec("ple")+vec("le>") |
| Character N-gram (字符n元组) | FastText 的核心：把词拆成 3-6 个字符的片段 | "where" → ["<wh","whe","her","ere","re>","<whe","wher",...] |
| OOV (Out-of-Vocabulary, 词表外词) | 不在训练词汇表中的词，Word2Vec/GloVe 无法处理，FastText 可以 | "ChatGPT" 或拼错的 "appple" |

### WordNet (词典知识库)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| WordNet (词汇关系数据库) | Princeton 的大型英语词汇数据库，用语义关系连接同义词集 | 可查询任何英语词的同义/反义/上下位关系 |
| Synset (同义词集) | 共享同一含义的一组同义词 | {happy, glad, cheerful} 构成一个 synset |
| Synonym (同义词) | 含义相同的词 | happy ↔ glad |
| Antonym (反义词) | 含义相反的词 | hot ↔ cold |
| Hypernym (上位词) | IS-A 关系中的父类 (更抽象) | "animal" 是 "dog" 的上位词 |
| Hyponym (下位词) | IS-A 关系中的子类 (更具体) | "dog" 是 "animal" 的下位词 |
| Meronym (部分词) | PART-OF 关系 | "wheel" 是 "car" 的部分 |
| Holonym (整体词) | HAS-PART 关系 | "car" 是 "wheel" 的整体 |
| Troponym (方式动词) | 表示某种行为的具体方式 | "run" 是 "move" 的方式动词 |
| Entailment (蕴含) | 一个动词隐含另一个 | "snore" 蕴含 "sleep" (打鼾必然在睡觉) |

### Embedding Evaluation (嵌入评估)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Intrinsic Evaluation (内在评估) | 直接评估嵌入质量：词相似度、词类比任务 | SimLex-999 相关度、king-man+woman=queen 准确率 |
| Extrinsic Evaluation (外在评估) | 用下游任务间接评估：情感分析、文本分类、NER 的准确率 | 用 W2V 做情感分析 acc=85% vs GloVe acc=83% |
| Static Embedding (静态嵌入) | 每个词只有一个固定向量，不随上下文变化 | "bank" 不管是"银行"还是"河岸"都是同一个向量 |
| Contextual Embedding (上下文嵌入) | 同一个词在不同上下文中有不同向量 (BERT/GPT等) | "bank"在"river bank"和"bank account"中向量不同 |

## 2. Comparisons (对比)

### CBOW vs Skip-gram (两种 Word2Vec 架构)

| Dimension (维度) | CBOW (连续词袋) | Skip-gram (跳字模型) | Example (示例) |
|-----------|------|-----------|---------|
| Input→Output | 上下文词 → 预测中心词 | 中心词 → 预测上下文词 | CBOW: [the,cat,on,the]→sat; Skip: sat→[the,cat,on,the] |
| Speed (速度) | ⚡ 更快 (一次预测一个词) | 🐢 更慢 (一次预测多个词) | 大语料优先 CBOW |
| Best for (适合) | 高频词 (频繁出现的词) | 低频/稀有词 | 常见词用 CBOW; 专业术语用 Skip-gram |
| `sg` parameter (参数) | `sg=0` (默认!) | `sg=1` | **考试常考**: 默认是 CBOW 不是 Skip-gram |
| 难度 | 更简单的分类问题 | 更难的分类问题 | CBOW 有多个输入做平均 |

### Word2Vec vs GloVe vs FastText (三大嵌入模型)

| Dimension (维度) | Word2Vec | GloVe | FastText | Example (示例) |
|-----------|----------|-------|----------|---------|
| Year/Origin (年份/来源) | 2013 Google | 2014 Stanford | 2016 Facebook | 三大科技巨头/名校 |
| Approach (方法) | 局部上下文预测 | 全局共现矩阵 + 分解 | 字符 n-gram 之和 | 预测 vs 计数 vs 子词 |
| OOV Handling (新词处理) | ❌ KeyError | ❌ KeyError | ✅ 子词组合仍有向量 | "appple": W2V=崩, FT≈0.95 |
| Misspelling (拼写错误) | ❌ 无法处理 | ❌ 无法处理 | ✅ 共享字符n-gram | "computar" vs "computer" |
| Training Data (训练数据) | Google News 100B词 | Wikipedia+Gigaword 6B | Common Crawl | 数据量越大效果越好 |

### Static vs Contextual Embeddings (静态 vs 上下文嵌入)

| Dimension (维度) | Static (W2V/GloVe/FastText) | Contextual (BERT/GPT) | Example (示例) |
|-----------|----------------------------------|----------------------|---------|
| 一词一向量? | ✅ 一个词 = 一个固定向量 | ❌ 同词不同上下文 = 不同向量 | "bank" 在任何语境向量相同(Static) |
| 多义词 | ❌ 无法区分不同意思 | ✅ 根据上下文生成不同嵌入 | "bank"=银行 vs 河岸 → Static 混淆 |
| OOV | 取决于方法 (FastText可以) | WordPiece 子词分词处理 | BERT: "unhappiness"→["un","##happiness"] |

### WordNet Limitations (WordNet 局限性)

| Limitation (局限) | Detail (详情) | Example (示例) |
|----------|--------|---------|
| Limited Coverage (覆盖有限) | 静态词库，不含新词和网络用语 | "selfie", "bitcoin" 可能不在 WordNet 中 |
| Not Computational (不可计算) | 不能直接用向量计算相似度 | 无法做 king-man+woman=queen |
| Manual Curation (人工维护) | 需要语言学家手动更新，成本高 | 新词每年产生数千个 |

## 3. Formulas (公式)

### Word Analogy (词类比公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\vec{A} - \vec{B} + \vec{C} \approx \vec{D}$ | A之于B等于C之于D (语义关系类比) | king-man+woman ≈ queen |
| $\vec{king} - \vec{man} + \vec{woman} \approx \vec{queen}$ | 性别类比 | 验证嵌入捕捉了性别关系 |
| $\vec{Paris} - \vec{France} + \vec{Italy} \approx \vec{Rome}$ | 首都-国家类比 | 验证嵌入捕捉了地理关系 |

### Embedding Dimensions (嵌入维度)

| Parameter (参数) | Value (值) | Note (说明) | Example (示例) |
|-----------|-------|------|---------|
| Embedding dim (嵌入维度) | 50–300 | ≠ 词表大小！考试常考 | `vector_size=100` → 每词100维向量 |
| Default Word2Vec | 100 | Gensim 默认维度 | 可改为 300 以提升效果 |
| Pre-trained GloVe/FastText | 300 | 预训练通常用 300 维 | 300d 是性能和效率的平衡点 |
| Vocabulary size | 数十万到数百万 | 远大于嵌入维度 | W2V:3M词; GloVe:400K词 |

## 4. Practical / Lab (实战结论)

### 🔑 Key API Distinctions (关键API区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|-------------|--------|---------|
| `sg=0`=CBOW; `sg=1`=Skip-gram | 考试常考！默认是 CBOW (sg=0) | `Word2Vec(sents, sg=0)` → CBOW |
| `vector_size` ≠ vocabulary size | 嵌入维度 (50-300) vs 词表大小 (百万级) — 两个完全不同的概念 | `vector_size=100` → 100维; vocab可能3M词 |
| `window=5` | 上下文窗口大小：窗口越大捕捉越全局的关系 | window=2→局部语法; window=10→全局话题 |
| `min_count=2` | 出现次数少于此值的词被忽略，减少噪声 | "serendipity"出现1次 → 被排除 |
| `negative=5` | SGNS 中每个正样本配的负样本数量 | 正:(apricot,jam) + 5个随机负样本 |
| `most_similar(positive, negative)` | Word2Vec 类比 API | `most_similar(positive=['king','woman'], negative=['man'])` → queen |

### 📊 Lab 3 结论 (已在W3详述，此处补充W4新增知识点)

| Finding (发现) | Detail (详情) | Example (示例) |
|---------|--------|---------|
| 预训练 300d >> 自训练小语料 | 数据量比架构更重要，Google News 100B词远超你的10K语料 | 预训练:高质量; 自训练10K:效果差 |
| 词嵌入存在偏见 (Bias) | 训练数据的社会偏见会被嵌入学到 | "programmer-man+woman" → nursing (性别刻板印象) |
| 静态嵌入不区分多义词 | "bank" 的银行和河岸义共享同一向量，这是根本局限 | bank(银行)和bank(河岸) → 向量完全一样 |

### ⚠️ W4 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------|
| Word2Vec 默认是 Skip-gram? | ❌ 默认是 CBOW (`sg=0`)！Skip-gram 需要手动设 `sg=1` | `Word2Vec(data)` → 用的是 CBOW |
| embedding_dim = vocabulary_size? | ❌ 完全不同！embedding_dim=50-300，vocab 可以是百万级 | 100维嵌入 + 3M词表 → 两个独立概念 |
| Word2Vec/GloVe 能处理 OOV? | ❌ 只有 FastText 能处理！W2V/GloVe 遇到新词直接报 KeyError | `w2v_model['xyz123']` → KeyError |
| 词嵌入能区分多义词? | ❌ 静态嵌入 (W2V/GloVe/FT) 一词一向量，不区分！需要 BERT 等上下文嵌入 | "bank" 只有一个向量 |
| GloVe 是预测方法? | ❌ GloVe 是基于计数的 (共现矩阵分解)! W2V 才是预测方法 | GloVe=计数+分解; W2V=神经网络预测 |
| WordNet 可以做向量计算? | ❌ WordNet 是词典数据库，不能做向量算术 | 无法计算 king-man+woman=queen |
