# W1: NLP Overview (NLP 概述)

## 1. Definitions (定义)

### Core Terms (核心术语)

| Term (术语)                        | Definition (定义)                                                            | Example (示例)                   |
| ---------------------------------- | ---------------------------------------------------------------------------- | -------------------------------- |
| NLP (自然语言处理)                 | 用计算机处理人类语言的技术领域 (Linguistics×CS×AI)，核心：处理、理解、生成 | Siri、Google翻译、ChatGPT        |
| NLU (自然语言理解)                 | NLP 的"读"：让机器读懂文本含义 (Classification, NER, Sentiment)              | "I love this!" → 正面情感       |
| NLG (自然语言生成)                 | NLP 的"写"：让机器生成人类可读文本 (Translation, Summarization)              | 法语→英语翻译；长文→摘要       |
| NLP = NLU + NLG                    | 理解 (Understanding) + 生成 (Generation) 两大能力组成                        | 聊天机器人：先NLU理解→再NLG回答 |
| Turing Test (图灵测试, 1950)       | 人类评估者分不清对面是人还是机器 → 通过测试                                 | 50%时间判断错 → 机器通过        |
| Corpus (语料库)                    | 用于 NLP 训练/分析的大规模文本集合                                           | Wikipedia、IMDb影评、新闻语料    |
| Supervised Learning (监督学习)     | 用带标签数据训练模型 — 告诉模型正确答案                                     | 1000条邮件标spam/not spam→训练  |
| Unsupervised Learning (无监督学习) | 用无标签数据发现隐藏模式                                                     | 1000篇新闻自动聚成5个topic       |

### Zipf's Law & Sparsity (齐普夫定律)

| Term (术语)             | Definition (定义)                                            | Example (示例)                     |
| ----------------------- | ------------------------------------------------------------ | ---------------------------------- |
| Zipf's Law (齐普夫定律) | 词频与排名成反比：freq ∝ 1/rank，少数词极高频，多数词极低频 | "the"(7%);"of"(3.5%);Rank10(~0.7%) |
| Hapax Legomena (单次词) | 在语料中只出现一次的词，通常超过总词表 1/3                   | 词表7000中~2500词仅出现1次         |
| Alpha (α)              | log-log回归斜率绝对值，理想≈1.0，衡量词频下降速度           | 文学α≈1.4; 宗教α≈1.6           |

### 4 NLP Challenges (4大挑战)

| Challenge (挑战)        | Definition (定义)                      | Example (示例)              |
| ----------------------- | -------------------------------------- | --------------------------- |
| Ambiguity (歧义性)      | 同一句话有多种理解：词汇/句法/指代歧义 | "bank"=银行or河岸           |
| Sparsity (稀疏性)       | Zipf定律→超过1/3词只出现一次          | "serendipity"可能只出现1次  |
| Variation (变异性)      | 同义可用不同词/句式表达                | "awesome"="splendid"="fire" |
| Common Knowledge (常识) | 机器缺乏世界常识，无法判断合理性       | "man bites dog"=新闻(反常)  |

### 7 NLP Applications (7大应用)

| Application (应用)            | Type (类型) | Example (示例)     |
| ----------------------------- | ----------- | ------------------ |
| Speech Recognition (语音识别) | NLU         | Siri语音转文字     |
| Dialogue/Chatbot (对话)       | NLU+NLG     | ChatGPT理解+回答   |
| Text Classification (分类)    | NLU         | 垃圾邮件过滤       |
| Sentiment Analysis (情感)     | NLU         | "great!"→Positive |
| Summarization (摘要)          | NLG         | 10页→3句          |
| QA (问答)                     | NLU+NLG     | 知识问答           |
| Generative AI (生成AI)        | NLG         | GPT-4生成文章/代码 |

### NLP Python Libraries (Python NLP库)

| Library     | 特点                     | Example (示例)                  |
| ----------- | ------------------------ | ------------------------------- |
| NLTK        | 经典教学库，功能全但慢   | `nltk.word_tokenize()`        |
| SpaCy       | 工业级，快速Pipeline     | `nlp("I love NLP")` 一次搞定  |
| HuggingFace | 预训练模型平台(BERT/GPT) | `pipeline("sentiment")(text)` |

## 2. Comparisons (对比)

### 3 NLP Approaches (3种方法)

| Approach (方法)     | Method (手段)      | Example (示例)            |
| ------------------- | ------------------ | ------------------------- |
| Heuristics (规则法) | 人工写规则/正则    | `if "not" in text: neg` |
| ML (机器学习)       | 标注数据训练模型   | TF-IDF + LogReg           |
| DL (深度学习)       | 神经网络自动学特征 | BERT, GPT                 |

### AI Hierarchy (AI层级): AI ⊃ ML ⊃ DL

| Level (层级)   | Relationship (关系)        | Example (示例)                      |
| -------------- | -------------------------- | ----------------------------------- |
| AI ⊃ ML ⊃ DL | 嵌套包含关系               | AI:专家系统; ML:SVM; DL:Transformer |
| NLP            | AI的应用领域，横跨所有层级 | 规则NLP→ML NLP→DL NLP             |

## 3. Formulas (公式)

_No formulas this week._

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)          | Correct Answer (正确答案)        | Example (示例)                       |
| -------------------- | -------------------------------- | ------------------------------------ |
| NLP = NLU?           | ❌ NLP = NLU + NLG               | 聊天机器人两部分都需要               |
| AI/ML/DL并列?        | ❌ 嵌套：AI⊃ML⊃DL              | 大圈套小圈                           |
| NLP三种方法哪个最好? | 没有绝对最好，取决于任务和数据量 | 少数据→规则; 中数据→ML; 大数据→DL |

# W2: Text Preprocessing (文本预处理)

## 1. Definitions (定义)

### Core Preprocessing (核心预处理)

| Term (术语)              | Definition (定义)                     | Example (示例)                          |
| ------------------------ | ------------------------------------- | --------------------------------------- |
| Tokenization (分词)      | NLP第一步：文本→离散token            | "I love NLP!" → ["I","love","NLP","!"] |
| Stop Words (停用词)      | 高频但语义贡献低的词，分析前移除      | "the","is","a" → 移除                  |
| Stemming (词干提取)      | 规则暴力砍词尾→词根，快但可能非真词  | "studies"→"studi"; "running"→"run"    |
| Lemmatization (词元化)   | 词典+词性还原标准词形，输出一定是真词 | "studies"→"study"; "better"→"good"    |
| POS Tagging (词性标注)   | 给每个token标语法类别                 | "The(DT) quick(JJ) fox(NN)"             |
| NER (命名实体识别)       | 找出并分类专有名词(人/地/组织)        | "James"=PERSON, "Ottawa"=GPE            |
| Normalization (规范化)   | token→统一基本形式(含Stemming/Lem)   | "Running","ran","runs"→"run"           |
| Noise Removal (噪声移除) | 删除无用元素：标点/HTML/URL           | `<br>Visit http://...` → 正文        |

### Regex (正则表达式)

| Term (术语)      | Definition (定义)            | Example (示例)                           |
| ---------------- | ---------------------------- | ---------------------------------------- |
| `re.match()`   | 只匹配字符串**开头**   | `re.match(r'\d+','abc123')`→None      |
| `re.search()`  | 匹配**任意位置**第一个 | `re.search(r'\d+','abc123')`→'123'    |
| `re.findall()` | 返回**所有**匹配列表   | `re.findall(r'\d+','a1b2')`→['1','2'] |
| `re.sub()`     | 替换所有匹配                 | `re.sub(r'\d+','#','a1b2')`→'a#b#'    |

### Preprocessing Pipeline (流水线顺序)

| Step             | 操作                    | Example (示例)                             |
| ---------------- | ----------------------- | ------------------------------------------ |
| ① Tokenize      | 原始文本→token列表     | "He's running!"→["He","'s","running","!"] |
| ② Noise Removal | 移除标点/停用词/HTML    | →["running"]                              |
| ③ Normalize     | Stemming或Lemmatization | →["run"]                                  |

## 2. Comparisons (对比)

### Stemming vs Lemmatization

| Dimension (维度) | Stemming (词干提取) | Lemmatization (词元化) | Example (示例)                      |
| ---------------- | ------------------- | ---------------------- | ----------------------------------- |
| Method (方法)    | 规则砍词尾          | 词典查找+POS           | Porter规则; WordNet词典             |
| Speed (速度)     | ⚡快(无需词典)      | 🐢慢(需加载词典)       | 大数据优先Stemming                  |
| Output (输出)    | 可能非真词          | 一定是真词             | "better"→Stem:"better"; Lem:"good" |

### NLTK 3 Stemmers

| Stemmer   | 激进程度     | Example (示例)           |
| --------- | ------------ | ------------------------ |
| Porter    | 最温和       | "generously"→"generous" |
| Snowball  | 中等(多语言) | 支持英/法/德等           |
| Lancaster | 最激进       | "generously"→"gener"    |

### SpaCy vs NLTK

| Feature (功能) | SpaCy              | NLTK        | Example (示例)                  |
| -------------- | ------------------ | ----------- | ------------------------------- |
| Stemming       | ❌                 | ✅ 三种     | NLTK:`PorterStemmer().stem()` |
| Lemmatization  | ✅`token.lemma_` | ✅ WordNet  | SpaCy一行; NLTK需指定词性       |
| 设计           | 工业级Pipeline     | 教学Toolkit | SpaCy一次搞定; NLTK每步手动     |

## 3. Formulas (公式)

_No formulas this week._

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)             | Correct Answer (正确答案)                  | Example (示例)                   |
| ----------------------- | ------------------------------------------ | -------------------------------- |
| re.match能匹配任意位置? | ❌ match只匹配开头! search才是任意位置     | `match(r'\d+','abc123')`→None |
| SpaCy可以做Stemming?    | ❌ SpaCy只有Lemmatization; NLTK两个都有    | SpaCy无 `stem()`方法           |
| 预处理顺序随便?         | ❌ 必须 Tokenize→Noise Removal→Normalize | 先Stem再Tokenize=错              |
| 规则法能处理否定?       | ❌ "not bad"→误判负面                     | 需ML/DL才能处理                  |

# W3: Text Vectorization & Similarity (文本向量化与相似度)

## 1. Definitions (定义)

### Text Representation (文本表示)

| Term (术语)                    | Definition (定义)                              | Example (示例)                              |
| ------------------------------ | ---------------------------------------------- | ------------------------------------------- |
| OHE (One-Hot Encoding)         | 二进制向量：词位置为1其余全0；无语义           | [cat,dog,fish]→cat=[1,0,0]                 |
| BOW (Bag-of-Words)             | 统计词频，忽略词序                             | "the cat sat"→{the:1,cat:1,sat:1}          |
| N-gram (N元组)                 | 连续N个词组成的词组，部分保留词序              | Bigram: "I love NLP"→["I love","love NLP"] |
| TF-IDF                         | 本文档高频+其他文档低频=重要                   | "NLP"在本文10次但只在5篇出现→高            |
| Cosine Similarity (余弦相似度) | 向量**方向**相似度，不受长度影响，[-1,1] | cos=1.0完全相同; cos=0正交无关              |
| Euclidean Distance (欧氏距离)  | 向量直线距离，受长度影响                       | d([1,0],[0,1])=√2≈1.41                    |
| Edit Distance (编辑距离)       | 变成另一字符串的最少操作次数(插入/删除/替换)   | "kitten"→"sitting"=3次                     |
| Sparsity (稀疏性)              | 向量中大部分元素为0(OHE/BOW/TF-IDF共同问题)    | 词表10000维,文档用50个词→99.5%是0          |
| OOV (Out-of-Vocabulary)        | 不在训练词表中的词，传统方法无法处理           | "ChatGPT"在2010年模型→OOV                  |

### Sklearn API

| Term (术语)           | Definition (定义)                  | Example (示例)              |
| --------------------- | ---------------------------------- | --------------------------- |
| `CountVectorizer`   | 文本→词频矩阵(原始计数)           | "the cat"→[1,1]            |
| `TfidfVectorizer`   | 文本→TF-IDF加权矩阵，稀有词权重高 | "the cat"→[0.0,0.7]        |
| `ngram_range=(1,2)` | 同时生成unigram+bigram             | "I love"→5个特征           |
| `stratify=y`        | train_test_split中保持类别分布     | 70%pos/30%neg→两集合同比例 |

### Evaluation Metrics (评估指标)

| Term (术语)                 | Definition (定义)                    | Example (示例)            |
| --------------------------- | ------------------------------------ | ------------------------- |
| Confusion Matrix (混淆矩阵) | TP/FP/FN/TN 的2×2表格               | 揭示每个类别表现          |
| Weighted F1                 | 按类别样本量加权的F1，适用不平衡数据 | 90%A+10%B→weighted更公平 |

## 2. Comparisons (对比)

### BOW vs N-gram vs TF-IDF

| Dimension  | BOW      | N-gram       | TF-IDF             | Example (示例)                       |
| ---------- | -------- | ------------ | ------------------ | ------------------------------------ |
| Word order | ❌忽略   | ⚠️局部保留 | ❌忽略             | "dog bites man"="man bites dog"(BOW) |
| Vocab size | V        | V^N(爆炸)    | V                  | V=10K→bigram=100M                   |
| Weighting  | 原始计数 | 原始计数     | 加权(稀有↑常见↓) | "the"=0; "serendipity"=高            |
| Semantic   | ❌       | ❌           | ❌                 | 都不知道"happy"≈"joyful"            |

### Cosine vs Euclidean

| Dimension    | Cosine     | Euclidean  | Example (示例)              |
| ------------ | ---------- | ---------- | --------------------------- |
| Measures     | 方向(角度) | 位置(直线) | 方向同但长度不同:cos=1,d≠0 |
| Range        | [-1,1]     | [0,∞)     | NLP首选cos                  |
| 向量长度影响 | ❌不受     | ✅受       | 文档长短不影响cos但影响d    |

## 3. Formulas (公式)

### TF-IDF

| Formula (公式)                                                              | Description (说明) | Example (示例)            |
| --------------------------------------------------------------------------- | ------------------ | ------------------------- |
| $\text{TF}(t,d) = \frac{\text{count}(t \in d)}{\text{total words in } d}$ | 词在文档中出现比例 | "cat"3次/100词→0.03      |
| $\text{IDF}(t) = \log\frac{N}{df(t)}$                                     | 出现越少文档越重要 | N=1000,"cat"在10篇→IDF=2 |
| $\text{TF-IDF} = \text{TF} \times \text{IDF}$                             | 两项相乘           | 0.03×2=0.06              |

### Similarity

| Formula (公式)                                                                                         | Description (说明) | Example (示例)                            |
| ------------------------------------------------------------------------------------------------------ | ------------------ | ----------------------------------------- |
| $\cos(\mathbf{A},\mathbf{B}) = \frac{\mathbf{A}\cdot\mathbf{B}}{\|\mathbf{A}\|\times\|\mathbf{B}\|}$ | 余弦相似度         | A·B=0.73,‖A‖=0.81,‖B‖=1.07→cos=0.84 |
| $d(\mathbf{A},\mathbf{B}) = \sqrt{\sum_i(a_i-b_i)^2}$                                                | 欧氏距离           | d([1,0],[0,1])=√2                        |

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)     | Correct Answer (正确答案)    | Example (示例)                  |
| --------------- | ---------------------------- | ------------------------------- |
| BOW保留词序?    | ❌ BOW完全忽略词序！只数词频 | "dog bites man"="man bites dog" |
| TF-IDF含语义?   | ❌ 只是统计权重，不理解语义  | 不知道"happy"≈"joyful"         |
| 余弦受长度影响? | ❌ 不受！只看方向; 欧氏才受  | 长短文档cos不变,Euclidean变     |
| N的N越大越好?   | ❌ V^N指数爆炸，太稀疏反而差 | Uni:10K→Bi:100M→Tri:1T        |

# W4: Word Embeddings (词嵌入)

## 1. Definitions (定义)

### Core Embedding Concepts (核心概念)

| Term (术语)                          | Definition (定义)                              | Example (示例)                     |
| ------------------------------------ | ---------------------------------------------- | ---------------------------------- |
| Word Embedding (词嵌入)              | 词→低维稠密向量(50-300维)，语义相似距离更近   | "king"→[0.2,-0.5,0.8,...](300维)     |
| Distributional Hypothesis (分布假说) | 相似上下文的词有相似含义 — 词嵌入理论基础     | "cat""dog"常在"pet"旁→语义相似    |
| Context Window (上下文窗口)          | 训练时看目标词左右各多少个词                   | window=2: "NLP"的上下文是love,very |
| Static Embedding (静态嵌入)          | 每词一个固定向量，不随上下文变化               | "bank"不管银行/河岸都同一个向量    |
| Contextual Embedding (上下文嵌入)    | 同词不同上下文→不同向量(BERT/GPT)             | "bank"在不同语境向量不同           |
| Embedding Matrix                     | 词表V行×维度D列的查找表; E[word_id]→稠密向量 | V=10000,D=300→矩阵(10000,300)     |
| Cosine Similarity (嵌入空间)         | 词嵌入间的语义相似度度量(同W3)                 | cos(king,queen)≈0.8               |

### Word2Vec (Google 2013) / GloVe (Stanford 2014) / FastText (Facebook 2016)

| Term (术语)   | Definition (定义)                                | Example (示例)                           |
| ------------- | ------------------------------------------------ | ---------------------------------------- |
| CBOW          | 用上下文词**预测**中心词; 更快, 适合高频词 | [the,cat,on,the]→预测"sat"              |
| Skip-gram     | 用中心词**预测**上下文; 更慢, 对稀有词好   | "sat"→预测[the,cat,on,the]              |
| SGNS (负采样) | 随机采"假"上下文词作负样本加速训练               | 正:(apricot,jam); 负:(apricot,elephant)  |
| GloVe         | 基于全局词共现矩阵分解学习向量                   | Wikipedia+Gigaword训练, 400K词, 300维    |
| FastText      | 词→字符n-gram(3-6字符)之和，能处理OOV/拼写错误  | "apple"=vec("<ap")+vec("app")+vec("ple") |

### WordNet (词典知识库)

| Term (术语)       | Definition (定义)                 | Example (示例)          |
| ----------------- | --------------------------------- | ----------------------- |
| Synset (同义词集) | 共享同一含义的一组同义词          | {happy,glad,cheerful}   |
| Hypernym/Hyponym  | 上位词(IS-A父类)/下位词(IS-A子类) | "animal"是"dog"的上位词 |

## 2. Comparisons (对比)

### CBOW vs Skip-gram

| Dimension     | CBOW            | Skip-gram      | Example (示例)                  |
| ------------- | --------------- | -------------- | ------------------------------- |
| Input→Output | 上下文→中心词  | 中心词→上下文 | CBOW一次预测一个; Skip多个      |
| Speed         | ⚡更快          | 🐢更慢         | 大语料优先CBOW                  |
| `sg` param  | `sg=0`(默认!) | `sg=1`       | **默认CBOW不是Skip-gram** |

### Word2Vec vs GloVe vs FastText

| Dimension | Word2Vec    | GloVe         | FastText      | Example (示例)             |
| --------- | ----------- | ------------- | ------------- | -------------------------- |
| Year      | 2013 Google | 2014 Stanford | 2016 Facebook | 三大来源                   |
| OOV       | ❌KeyError  | ❌KeyError    | ✅子词组合    | "appple":W2V=N/A; FT≈0.95 |
| Method    | 局部预测    | 全局共现分解  | 字符n-gram    | 预测vs计数vs子词           |

### Static vs Contextual Embedding

| Dimension  | Static (W2V/GloVe/FT) | Contextual (BERT/GPT)     | Example (示例)          |
| ---------- | --------------------- | ------------------------- | ----------------------- |
| 多义词     | ❌一个向量            | ✅不同向量                | "bank"银行vs河岸        |
| 训练       | 一次训练,查表用       | 每次推理重新计算          | Static快;Contextual慢   |
| OOV        | W2V/GloVe❌;FT✅      | ✅子词分词(WordPiece/BPE) | BERT: "##ing"           |
| 上下文范围 | 固定窗口(5-10词)      | 全序列(BERT:512tokens)    | W2V:5词; BERT:512tokens |
| 计算       | 查表O(1)              | 推理O(n²)                | Static快1000×          |

## 3. Formulas (公式)

### Word Analogy (词类比)

| Formula (公式)                            | Description (说明)     | Example (示例)        |
| ----------------------------------------- | ---------------------- | --------------------- |
| $\vec{A}-\vec{B}+\vec{C}\approx\vec{D}$ | A:B = C:D 语义关系类比 | king-man+woman≈queen |

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)               | Correct Answer (正确答案)               | Example (示例)           |
| ------------------------- | --------------------------------------- | ------------------------ |
| W2V默认Skip-gram?         | ❌ 默认CBOW(`sg=0`)!                  | `Word2Vec(data)`→CBOW |
| embedding_dim=vocab_size? | ❌ 完全不同! dim=50-300, vocab=百万级   | 100维嵌入+3M词表         |
| W2V/GloVe能处理OOV?       | ❌ 只有FastText能!                      | `w2v['xyz']`→KeyError |
| GloVe是预测方法?          | ❌ GloVe是计数的(共现矩阵)! W2V才是预测 | GloVe=分解; W2V=预测     |

# W5: Language Models & RNN/LSTM (语言模型 & 循环网络)

## 1. Definitions (定义)

### Language Model (语言模型)

| Term (术语)              | Definition (定义)                                        | Example (示例)                   |
| ------------------------ | -------------------------------------------------------- | -------------------------------- |
| Language Model (LM)      | 给词序列分配概率，核心：预测下一个词 P(wₜ               | context)                         |
| Markov Assumption        | 下一个词只依赖前n-1个词(非全部历史)                      | Bigram: P(wₜ                    |
| Perplexity (困惑度, PP)  | LM标准评估指标，**越低越好**；PP=1完美; PP=V随机猜 | PP=50很好; PP=500差              |
| N-gram LM                | 基于前n-1词计数频率预测                                  | P(books                          |
| Data Sparsity (数据稀疏) | N-gram核心问题：未出现的组合→P=0                        | "opened their quantum"→C=0→P=0 |

### Neural Network (神经网络)

| Term (术语)                   | Definition (定义)                                 | Example (示例)                           |
| ----------------------------- | ------------------------------------------------- | ---------------------------------------- |
| FFNN (前馈网络)               | 信号只向前流(输入→隐藏→输出)，固定输入，无记忆  | 不能处理变长序列                         |
| RNN (循环网络)                | 有自循环连接，逐步处理变长序列，参数每步共享      | h_t=f(W_h·h_{t-1}+W_e·e_t+b)           |
| Hidden State (h_t)            | RNN每步内部记忆，携带前面所有输入的累积信息       | h_3包含w1,w2,w3信息                      |
| Parameter Sharing             | RNN每步用相同W_h，参数不随序列长度增加            | 不管句子多长，同一套W_h                  |
| Embedding Layer               | 词ID→稠密向量的查找表 e(t)=E·x(t)               | `Embedding(10000,100)`                 |
| Vanishing Gradient (梯度消失) | 梯度经多步W_h后指数缩小→无法学长距离依赖         |                                          |
| Exploding Gradient (梯度爆炸) | 梯度指数增大→训练不稳定，用gradient clipping解决 |                                          |
| Backpropagation (反向传播)    | 从输出到输入逐层计算梯度→更新权重                | Loss→output→hidden→input              |
| BPTT (时间反向传播)           | RNN/LSTM的反向传播：沿时间步展开计算梯度          | 每步共享W_h→梯度累乘                    |
| Gradient Clipping             | 梯度超过阈值时裁剪，防止爆炸                      | if ‖g‖>threshold: g=g×threshold/‖g‖ |
| Softmax                       | 实数向量→概率分布(所有>0且和=1)                  | [2.0,1.0,0.1]→[0.7,0.2,0.1]             |
| Cross-Entropy Loss            | 分类标准损失函数                                  | categorical=多; binary=二                |

### LSTM (长短期记忆, Hochreiter & Schmidhuber 1997)

| Term (术语)       | Definition (定义)                                     | Example (示例)                         |
| ----------------- | ----------------------------------------------------- | -------------------------------------- |
| LSTM              | 门控RNN变体，用**加法**更新细胞状态解决梯度消失 | 细胞状态+3个门控制信息流               |
| Cell State (c_t)  | 长期记忆传送带，**加法**(非乘法)更新→梯度保留  | c_t=f_t⊙c_{t-1}**+** i_t⊙c̃_t |
| Forget Gate (f_t) | σ: 决定丢弃多少旧信息(0=全忘,1=全记)                 | 新话题→f≈0→清除旧记忆               |
| Input Gate (i_t)  | σ: 决定存储多少新信息(0=忽略,1=写入)                 | 重要信息→i≈1                         |
| Output Gate (o_t) | σ: 决定输出多少细胞信息                              | h_t=o_t⊙tanh(c_t)                     |

## 2. Comparisons (对比)

### N-gram vs Fixed-window NN vs RNN LM

| Dimension       | N-gram           | Fixed-window NN | RNN            |
| --------------- | ---------------- | --------------- | -------------- |
| Context         | 前n-1词(计数)    | 前n-1词(嵌入)   | 理论上全部历史 |
| Sparsity        | ❌严重(C=0→P=0) | ✅嵌入泛化      | ✅嵌入泛化     |
| Variable length | ❌固定           | ❌固定          | ✅任意长度     |

### RNN vs LSTM

| Dimension      | RNN        | LSTM                           | Example (示例)          |
| -------------- | ---------- | ------------------------------ | ----------------------- |
| Long-range     | ❌梯度消失 | ✅细胞状态保留                 | 10步前信息:RNN丢,LSTM留 |
| Gates          | 无         | 3门:Forget/Input/Output        | 0-1动态控制             |
| Key innovation | —         | 细胞状态用**加法**非乘法 | c_t=f⊙c+i⊙c̃         |

## 3. Formulas (公式)

### Probability & LM

| Formula (公式)                              | Description (说明) | Example (示例)     |
| ------------------------------------------- | ------------------ | ------------------ |
| $P(w_1..w_n)=\prod_t P(w_t|w_1..w_{t-1})$ | 链式法则           | LM的数学基础       |
| $PP=(\prod_i \frac{1}{P(w_i)})^{1/T}$     | 困惑度             | PP=1完美; PP=V随机 |

### LSTM Gates

| Gate        | Formula                                      | Purpose                 |
| ----------- | -------------------------------------------- | ----------------------- |
| Forget      | $f_t=\sigma(W_f[h_{t-1},x_t]+b_f)$         | 丢弃旧信息比例          |
| Input       | $i_t=\sigma(W_i[h_{t-1},x_t]+b_i)$         | 写入新信息比例          |
| Candidate   | $\tilde{c}_t=\tanh(W_c[h_{t-1},x_t]+b_c)$  | 新候选信息              |
| Cell update | $c_t=f_t\odot c_{t-1}+i_t\odot\tilde{c}_t$ | **加法更新=关键** |
| Output      | $o_t=\sigma(W_o[h_{t-1},x_t]+b_o)$         | 控制输出                |
| Hidden      | $h_t=o_t\odot\tanh(c_t)$                   | 过滤后的当前输出        |

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)               | Correct Answer (正确答案)                  | Example (示例)           |
| ------------------------- | ------------------------------------------ | ------------------------ |
| Perplexity越高越好?       | ❌**越低越好**! PP=1完美             | PP=50>>PP=500            |
| RNN能学长距离?            | ❌ 梯度消失! LSTM才能                      | 10步前信息RNN学不到      |
| LSTM用新训练算法?         | ❌ 仍用BPTT! 只是架构不同                  | 训练方法相同，区别在门控 |
| LSTM细胞用乘法更新?       | ❌**加法**! c_t=f⊙c+i⊙c̃          | 加法保持梯度             |
| LSTM units=embedding dim? | ❌ units=hidden dim, 和embedding是两个参数 | units=128≠embed=100     |

# W6: Seq2Seq & Attention (序列到序列 & 注意力)

## 1. Definitions (定义)

### Bi-LSTM (双向LSTM)

| Term (术语)          | Definition (定义)                                       | Example (示例)                        |
| -------------------- | ------------------------------------------------------- | ------------------------------------- |
| Bi-LSTM              | 两个独立LSTM同时左→右和右→左读取，拼接两方向隐状态    | "terribly exciting"→需看右侧判断正面 |
| Output dim           | 2×hidden_size (正向+反向拼接)                          | LSTM(128)→Bi-LSTM输出256维           |
| `return_sequences` | True=所有时间步(Attn需要); False(默认)=只最后一步(分类) | True:shape(10,256); False:shape(256,) |

### Sequence Problem Types (序列问题类型)

| Type (类型)           | Definition (定义)                     | Example (示例) |
| --------------------- | ------------------------------------- | -------------- |
| One-to-One            | 单输入单输出，不涉及序列              | 图像分类       |
| One-to-Many           | 单输入→序列输出                      | 图像描述       |
| Many-to-One           | 序列输入→单输出                      | 情感分析       |
| Many-to-Many Synced   | 等长序列输入输出                      | 词性标注       |
| Many-to-Many Unsynced | 不等长输入输出(**Seq2Seq核心**) | 机器翻译       |

### Seq2Seq (序列到序列)

| Term (术语)           | Definition (定义)                                    | Example (示例)                                  |
| --------------------- | ---------------------------------------------------- | ----------------------------------------------- |
| Seq2Seq               | Encoder读完输入→压缩为固定向量→Decoder逐步生成输出 | "il a m'entarté"→编码→"he hit me with a pie" |
| Encoder Vector        | 编码器最后一步h，编解码器间**唯一桥梁**        | 编码器最终h→解码器初始h                        |
| Bottleneck (信息瓶颈) | 整个输入压缩到固定大小向量→长序列必然丢失信息       | 100词→256d→细节丢失                           |
| Teacher Forcing       | 训练时输入**真实的**前一个词(非模型预测)       | 训练快速稳定收敛                                |
| Auto-regressive       | 推理时只能用自己的**预测**作输入               | 错误向后累积                                    |
| Exposure Bias         | 训练用真实输入vs推理用自身预测的不一致→错误滚雪球   | 训练没见过自己的错误                            |

### Attention (注意力机制)

| Term (术语)      | Definition (定义)                                      | Example (示例)                          |
| ---------------- | ------------------------------------------------------ | --------------------------------------- |
| Attention        | 解码器生成每词时**动态选择性关注**编码器不同位置 | 翻译"he"时重点看"il"; "pie"看"entarté" |
| Attention Score  | dec_state与每个enc_state的点积相似度                   | 4个编码器状态→4个分数                  |
| Attention Weight | softmax后的概率分布(和=1)                              | α=[0.7,0.1,0.1,0.1]                    |
| Context Vector   | 用权重对编码器隐状态加权求和                           | c=0.7·h₁+0.1·h₂+...                 |

## 2. Comparisons (对比)

### Seq2Seq vs Seq2Seq+Attention

| Dimension | Seq2Seq            | +Attention             | Example (示例)   |
| --------- | ------------------ | ---------------------- | ---------------- |
| Info path | 单一固定向量(瓶颈) | 直接访问所有编码器状态 | 瓶颈vs直通       |
| Long seq  | ❌>20词急剧退化    | ✅长句也可             | 100词:原始丢信息 |
| Interpret | ❌黑盒             | ✅权重可视化           | 能看翻译注意哪里 |
| Parallel  | ❌RNN顺序          | ❌仍RNN顺序!           | 都不能并行       |

### Uni-LSTM vs Bi-LSTM

| Dimension  | Uni-LSTM     | Bi-LSTM            | Example (示例)      |
| ---------- | ------------ | ------------------ | ------------------- |
| Direction  | 只看过去(→) | 过去+未来(→+←)   | 反向提供完整上下文  |
| Generation | ✅可以生成   | ❌不能生成(需未来) | 生成用Uni; 分类用Bi |

### 技术演进路线

| From→To              | Problem Solved            | Cost                  |
| --------------------- | ------------------------- | --------------------- |
| 单向→Bi-LSTM         | 方向盲区→看两边          | 不能生成;参数2×      |
| Bi-LSTM→Seq2Seq      | 输入输出不等长            | 信息瓶颈              |
| Seq2Seq→+Attention   | 瓶颈→每步看所有位置      | 仍需RNN顺序;每步O(n)  |
| RNN+Attn→Transformer | RNN不能并行→自注意力并行 | O(n²)内存;需位置编码 |

## 3. Formulas (公式)

### Attention 4 Steps

| Step      | Formula                                        | Description       |
| --------- | ---------------------------------------------- | ----------------- |
| Score     | $e_i=\text{dec}^T\cdot\text{enc}_i$          | 点积相似度        |
| Normalize | $\alpha_i=\text{softmax}(e_i)$               | 概率分布(和=1)    |
| Context   | $\mathbf{c}=\sum_i\alpha_i\cdot\text{enc}_i$ | 加权求和          |
| Output    | $\text{out}=f([\text{dec};\mathbf{c}])$      | 拼接→FC→softmax |

### Conditional LM & Loss

| Formula (公式)                           | Description (说明)                     | Example (示例)             |
| ---------------------------------------- | -------------------------------------- | -------------------------- |
| $P(y|x)=\prod_t P(y_t|y_{<t},x)$       | 条件LM(Seq2Seq数学本质)：以源句x为条件 | 翻译:每词依赖已翻译词+源句 |
| $J=\frac{1}{T}\sum_t -\log P(y_t|...)$ | NMT平均交叉熵损失，端到端反传          | 所有步损失均值→梯度反传   |

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)                 | Correct Answer (正确答案)                         | Example (示例)       |
| --------------------------- | ------------------------------------------------- | -------------------- |
| Bi-LSTM能生成文本?          | ❌ 反向LSTM需未来上下文→无法自回归生成           | 生成必须用单向       |
| Teacher Forcing推理时也用?  | ❌ 推理用自回归(自身预测)! TF**只在训练时** | 训练=真实; 推理=自身 |
| Attention让Seq2Seq可以并行? | ❌ RNN+Attention仍顺序!**Transformer**才能  | RNN必须逐步          |
| 注意力权重是固定参数?       | ❌ 动态计算的(点积+softmax)，每步重算             | 不同输入→不同分布   |

# 📝 Concept Short Answers — W1-W6

### C-1: What is Word Embedding? Why better than BOW/TF-IDF? ⭐⭐⭐

**Answer**: Word embedding maps each word to a **low-dimensional dense vector** (50-300d) where semantically similar words are closer. Based on the **Distributional Hypothesis**: words in similar contexts have similar meanings.

**vs BOW/TF-IDF**: ①BOW/TF-IDF = high-dim sparse (V=10K, 99% zeros); Embedding = low-dim dense (300d). ②BOW has no word order or semantics; embeddings capture semantic relations (king-man+woman≈queen). ③BOW cannot handle OOV; FastText uses subword n-grams for OOV.

### C-2: What is the Seq2Seq bottleneck? How does Attention fix it? ⭐⭐⭐

**Answer**: Seq2Seq compresses **entire input** into one fixed-size vector → long sequences lose information (**information bottleneck**). Attention: decoder **dynamically computes** weights over all encoder states at each step → weighted sum → directly accesses all source positions.

**⚠️**: Seq2Seq+Attention still **cannot parallelize** (still uses RNN)! Only Transformer enables full parallelism.

### C-3: Explain RNN vanishing gradient & how LSTM solves it ⭐⭐

**Answer**: During BPTT, gradients pass through $W_h$ at each step → exponential shrinkage (|W_h|<1 → gradient→0) → **cannot learn long-range dependencies**.

**LSTM**: Cell state $c_t$ updated via **addition** (not multiplication): $c_t=f_t\odot c_{t-1}+i_t\odot\tilde{c}_t$. Addition gradient=1 → gradient preserved. 3 gates (Forget/Input/Output) control info flow.

### C-4: Compare Static vs Contextual Embeddings ⭐⭐

**Answer**: **Static** (W2V/GloVe/FastText): one fixed vector per word regardless of context. "bank" always same vector whether financial or river. **Contextual** (BERT/GPT): different vector for same word in different contexts. Each token sees full sequence via self-attention.

**Trade-off**: Static = O(1) lookup, fast; Contextual = O(n²) inference, slow but much more accurate.

### C-5: What is the NLP preprocessing pipeline? ⭐⭐

**Answer**: ①**Tokenization** (text→tokens: "He's running!"→["He","'s","running","!"]) → ②**Noise Removal** (remove punctuation/stopwords/HTML) → ③**Normalization** (Stemming or Lemmatization→base form).

**Stemming vs Lemmatization**: Stemming = rule-based, fast, may produce non-words ("studies"→"studi"); Lemmatization = dictionary-based, slow, always real words ("studies"→"study", "better"→"good").

### C-6: Compare BERT vs GPT ⭐⭐⭐

**Answer**: BERT = **Encoder-only** (bidirectional, sees all context) → understanding (classification/NER/QA). GPT = **Decoder-only** (left-to-right only) → generation (dialogue/creation).

**Pre-training**: BERT = MLM+NSP; GPT = CLM (next word). **Key**: BERT **cannot generate**; GPT can but weaker at understanding. BERT max 512 tokens; GPT up to 128K+.

### C-7: What is TF-IDF? How does it work? ⭐⭐⭐

**Answer**: TF-IDF measures word importance in a document relative to a corpus. **TF** = word frequency in document (count/total). **IDF** = $\log(N/df)$, penalizes words appearing in many documents. TF-IDF = TF × IDF → words frequent in THIS doc but rare across corpus get high weight.

**⚠️ Key trap**: If a word appears in ALL documents, $df=N$ → $IDF=\log(1)=0$ → TF-IDF=0 (word eliminated!). Common words like "the" get zero weight.

### C-8: Compare CBOW vs Skip-gram in Word2Vec ⭐⭐

**Answer**: Both are Word2Vec architectures. **CBOW**: uses surrounding context words to predict center word → faster, better for frequent words. **Skip-gram**: uses center word to predict surrounding context → slower, better for rare/infrequent words.

**Code trap**: Default is CBOW (`sg=0`), NOT Skip-gram! Use `sg=1` for Skip-gram. **OOV**: Neither W2V nor GloVe handles OOV → only FastText can (via character n-grams).

### C-9: What are N-grams? What is the sparsity problem in N-gram LM? ⭐⭐

**Answer**: N-gram = sequence of N consecutive words. N-gram LM predicts next word using previous N-1 words: $P(w_t|w_{t-n+1}...w_{t-1})$. **Sparsity**: most N-gram combinations never appear in training data → count=0 → P=0. This is fatal because one zero probability makes entire sequence probability zero.

**Solution**: Smoothing (e.g., Laplace +1). **Trade-off**: larger N = more context but exponentially more sparsity ($V^N$ possible combinations).

### C-10: Why does NLP prefer Cosine Similarity over Euclidean Distance? ⭐⭐

**Answer**: Cosine measures **direction** (angle between vectors), Euclidean measures **position** (straight-line distance). In NLP, documents of different lengths have different vector magnitudes but similar topics → Cosine is **length-invariant** (unaffected by document length), Euclidean is not.

**Range**: Cosine ∈ [-1,1]; Euclidean ∈ [0,∞). Two docs about same topic: cos≈1 regardless of length, but Euclidean varies with length.

# W9: Transformer (Transformer 架构)

## 1. Definitions (定义)

### Self-Attention (自注意力)

| Term (术语)     | Definition (定义)                          | Example (示例)                    |
| --------------- | ------------------------------------------ | --------------------------------- |
| Self-Attention  | 每个词同时评估所有其他词的相关性并加权聚合 | "it was tired"→"it"学到关注"cat" |
| Query (Q)       | "我在找什么信息"→W_Q变换                  | "it"的Q="谁是我指代的对象"        |
| Key (K)         | "我能提供什么"→W_K变换                    | "cat"的K="我是动物主语"           |
| Value (V)       | "我的实际信息"→W_V变换                    | "cat"的V=cat的语义                |
| Multi-Head Attn | h个独立注意力头，各学不同关系模式          | Head1语法; Head2语义; Head3位置   |

### Transformer Architecture

| Term (术语)         | Definition (定义)                                 | Example (示例)                        |
| ------------------- | ------------------------------------------------- | ------------------------------------- |
| Transformer (2017)  | 完全依赖自注意力，抛弃RNN，全部并行               | "Attention Is All You Need"→GPT,BERT |
| Positional Encoding | sin/cos函数为每位置生成唯一向量+词嵌入相加        | Transformer无循环→需显式位置         |
| Scaled Dot-Product  | Attn(Q,K,V)=softmax(QK^T/√d_k)V; ÷√d_k防过尖锐 | d_k=64→÷8稳定梯度                   |
| FFN (前馈网络)      | 每位置独立做两层线性+ReLU                         | 512→2048→512                        |
| Residual+LayerNorm  | output=LayerNorm(x+Sublayer(x))                   | 梯度通过残差路径回传                  |
| Masked Self-Attn    | 解码器将未来位置设-∞→只看已生成                 | 生成"love"时只看"I"                   |
| Cross-Attention     | 解码器Q查询编码器KV→从源句提取信息               | Q=解码器; KV=编码器                   |
| Softmax Output      | 解码器最后一层在整个词表上输出下一词概率分布      | P("he")=0.85→选"he"                  |

### Transformer 三大分支

| Branch          | 代表模型           | 适合任务          |
| --------------- | ------------------ | ----------------- |
| Encoder-only    | BERT, RoBERTa      | 理解(分类/NER/QA) |
| Decoder-only    | GPT, LLaMA, Claude | 生成(对话/创作)   |
| Encoder-Decoder | T5, BART           | 翻译/摘要         |

### Transformer Base Configuration (标准配置)

| Parameter       | Value | Example (示例)          |
| --------------- | ----- | ----------------------- |
| d_model         | 512   | 词嵌入+位置编码维度     |
| d_ff            | 2048  | FFN内部维度(4×d_model) |
| h (heads)       | 8     | 8个注意力头             |
| d_k = d_model/h | 64    | 每个头的维度            |
| N (layers)      | 6     | 编码器/解码器各6层      |

## 2. Comparisons (对比)

### RNN vs Transformer

| Dimension | RNN/LSTM           | Transformer  | Example (示例)          |
| --------- | ------------------ | ------------ | ----------------------- |
| 序列处理  | 顺序(逐步)         | 并行(一次性) | RNN:O(n)步;Trans:O(1)步 |
| 位置信息  | 隐式(处理顺序)     | 显式(PE)     | 必须加PE否则不知词序    |
| 长距离    | 多步传播(梯度消失) | O(1)路径     | 任意两词直接连接        |
| 内存      | O(n)               | O(n²)       | 注意力矩阵n×n          |

### Encoder vs Decoder (编码器 vs 解码器)

| Dimension  | Encoder (编码器) | Decoder (解码器)                    | Example (示例)             |
| ---------- | ---------------- | ----------------------------------- | -------------------------- |
| 注意力类型 | 自注意力(看全部) | 掩码自注意力+交叉注意力             | 编码器双向; 解码器只看左   |
| 掩码       | 无掩码(全部可见) | 下三角掩码(屏蔽未来)                | 未来位置设-∞              |
| KV来源     | 全部来自自身     | Self-Attn自身; Cross-Attn来自编码器 | Cross-Attn: KV=编码器输出  |
| 处理       | 并行处理整个输入 | 自回归逐步生成                      | 编码器一次看完; 解码器逐词 |

### Single-Head vs Multi-Head Attention

| Dimension | Single-Head  | Multi-Head         | Example (示例)               |
| --------- | ------------ | ------------------ | ---------------------------- |
| 模式      | 只学一种关系 | h个头同时学h种关系 | 语法+语义+位置并行           |
| 输出      | 单个d维向量  | h个d/h维拼接后投影 | 8头×64维=512维→投影回512维 |

## 3. Formulas (公式)

### Scaled Dot-Product Attention

| Formula (公式)                                                  | Description (说明) | Example (示例)   |
| --------------------------------------------------------------- | ------------------ | ---------------- |
| $\text{Attn}(Q,K,V)=\text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$ | 完整注意力公式     | 权重×V=加权输出 |
| $FFN(Z)=\text{ReLU}(ZW_1+b_1)W_2+b_2$                         | 前馈网络           | 512→2048→512   |
| $PE(pos,2i)=\sin(pos/10000^{2i/d})$                           | 偶数维位置编码     | sin/cos交替      |

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)                  | Correct Answer (正确答案)             | Example (示例)                  |
| ---------------------------- | ------------------------------------- | ------------------------------- |
| Transformer用RNN?            | ❌ 完全抛弃RNN/LSTM!                  | 纯自注意力+PE                   |
| 自注意力自带位置?            | ❌ 集合操作不区分词序→必须加PE       | "I love NLP"="NLP love I"(无PE) |
| √d_k可以省?                 | ❌ 不能! d大→softmax太尖→梯度消失   | 训练崩溃                        |
| Cross-Attn的QKV都来自解码器? | ❌**Q来自解码器, KV来自编码器** | Q=问题; KV=信息源               |
| FFN对整个序列操作?           | ❌ position-wise独立做                | 位置间不交互                    |

# W10: BERT & QA (BERT 与问答系统)

## 1. Definitions (定义)

### BERT (Bidirectional Encoder Representations from Transformers)

| Term (术语)          | Definition (定义)                             | Example (示例)                              |
| -------------------- | --------------------------------------------- | ------------------------------------------- |
| BERT                 | 只用Encoder实现真正双向上下文理解             | Wikipedia(25亿词)+BookCorpus(8亿词)         |
| BERT-base            | 12层/768维/12头/110M参数                      | SQuAD F1=88.5, EM=80.8                      |
| BERT-large           | 24层/1024维/16头/340M参数                     | SQuAD F1=90.9, EM=84.1                      |
| WordPiece (子词分词) | 罕见词→常见子词片段; 词表~30,500             | "embeddings"→["em","##bed","##ding","##s"] |
| [CLS]                | 输入开头特殊token→输出用作整个输入的浓缩表示 | 分类:[CLS]输出→线性层→标签                |
| [SEP]                | 分隔句子对                                    | [CLS]Question[SEP]Passage[SEP]              |
| [MASK]               | MLM预训练中替代被遮住的词                     | "the [MASK]"→模型预测"store"               |
| Token Embedding      | 三层嵌入之一：每个token的语义向量表示         | "cat"→768维向量                            |
| Segment Embedding    | 三层嵌入之二：区分Sentence A(0)和B(1)         | A→0; B→1                                  |
| Position Embedding   | 三层嵌入之三：token在序列中的位置             | 位置0,1,2→对应位置向量                     |

### BERT Training (BERT 训练)

| Term (术语)           | Definition (定义)                                        | Example (示例)      |
| --------------------- | -------------------------------------------------------- | ------------------- |
| Pre-training (预训练) | 大量无标注文本学通用语言知识: MLM+NSP                    | 一次训练(64块TPU)   |
| Fine-tuning (微调)    | 预训练上加小层，少量标注数据适配任务                     | 普通GPU几小时       |
| MLM (掩码语言模型)    | 随机遮15%词让模型预测; 80%→[MASK], 10%→随机, 10%→不变 | 避免训练-推理不匹配 |
| NSP (下一句预测)      | 判断B是否是A的下一句: IsNext/NotNext                     | 学习句间关系        |
| DistilBERT            | 知识蒸馏压缩BERT: 97%性能/40%小/60%快                    | 110M→66M参数       |

### Question Answering (问答系统)

| Term (术语)            | Definition (定义)                               | Example (示例)           |
| ---------------------- | ----------------------------------------------- | ------------------------ |
| Extractive QA (抽取式) | 答案从原文**复制**连续span                | 段落含"German"→直接抽取 |
| Generative QA (生成式) | 模型自己**生成**答案                      | GPT组织新语言回答        |
| SQuAD                  | Stanford QA Dataset: 10万(段落,问题,答案)三元组 | 答案是段落中span         |
| EM (Exact Match)       | 预测完全一致=1否则=0                            | 严格匹配                 |
| F1 Score (QA)          | token级P×R调和平均，给部分匹配打分             | 大部分正确也有分         |
| Start/End Prediction   | BERT用S/E向量预测答案span的起止位置             | 对每token做点积+softmax  |
| Sliding Window         | 超过512token→切成有重叠窗口逐个输入            | stride=25→重叠25tokens  |

### Open Domain QA

| Term (术语)        | Definition (定义)                    | Example (示例)            |
| ------------------ | ------------------------------------ | ------------------------- |
| Retriever-Reader   | 两阶段: 先检索候选文档→再提取答案   | Retriever(找)→Reader(读) |
| DPR (密集段落检索) | 两个独立BERT编码器分别编码问题和段落 | Q-Encoder≠P-Encoder      |

## 2. Comparisons (对比)

### BERT-base vs BERT-large

| Dimension | BERT-base | BERT-large | Example (示例) |
| --------- | --------- | ---------- | -------------- |
| Layers    | 12        | 24         | 深度翻倍       |
| Hidden    | 768       | 1024       | 更宽表示       |
| Heads     | 12        | 16         | 更多注意力模式 |
| Params    | 110M      | 340M       | 约3倍差距      |
| SQuAD F1  | 88.5      | 90.9       | Large只高2.4点 |

### SQuAD Model Comparison

| Model      | F1   | EM   | Architecture          |
| ---------- | ---- | ---- | --------------------- |
| BiDAF      | 77.3 | 67.7 | Bi-LSTM+Attention     |
| BERT-base  | 88.5 | 80.8 | Transformer Enc(12层) |
| BERT-large | 90.9 | 84.1 | Transformer Enc(24层) |
| XLNet      | 94.5 | 89.0 | Permutation LM        |
| RoBERTa    | 94.6 | 88.9 | 去NSP+更多数据        |

### MLM 80/10/10 Strategy

| 比例 | 操作     | 目的                | Example (示例) |
| ---- | -------- | ------------------- | -------------- |
| 80%  | →[MASK] | 学预测被遮词        | store→[MASK]  |
| 10%  | →随机词 | 避免训练-推理不匹配 | store→running |
| 10%  | →不变   | 对所有位置保持警觉  | store→store   |

### MLM vs NSP

| Dimension | MLM            | NSP                  | Example (示例)         |
| --------- | -------------- | -------------------- | ---------------------- |
| Goal      | 词级上下文理解 | 句间关系理解         | 猜遮的词 vs 判断句关系 |
| Output    | 预测被遮token  | 二分类IsNext/NotNext | 词义消歧 vs 段落连贯性 |

### Pre-training vs Fine-tuning

| Dimension | Pre-training  | Fine-tuning | Example (示例)         |
| --------- | ------------- | ----------- | ---------------------- |
| Data      | 海量无标注    | 少量标注    | Wikipedia vs SQuAD     |
| Cost      | 极高(TPU集群) | 低(普通GPU) | $百万 vs $百         |
| Frequency | 做一次        | 每任务一次  | 训练BERT一次→微调多次 |

### EM vs F1

| Dimension | EM                        | F1                     | Example (示例)            |
| --------- | ------------------------- | ---------------------- | ------------------------- |
| 匹配方式  | 完全一致                  | 部分匹配               | EM太严格; F1宽容          |
| 取值      | 0或1                      | 0到1                   | EM=0但F1=0.67→大部分正确 |
| 多个gold  | 取max{match(pred,gold_i)} | 取max{F1(pred,gold_i)} | max{0.67,0.67,0.61}=0.67  |

### Extractive vs Generative vs RAG

| Dimension | Extractive     | Generative     | RAG                |
| --------- | -------------- | -------------- | ------------------ |
| 答案来源  | 从原文复制span | 模型组织新语言 | 检索+生成          |
| 准确度    | ✅可追溯       | ⚠️可能幻觉   | ✅基于文档         |
| 灵活性    | ❌必须原文子串 | ✅综合多段     | ✅检索+综合        |
| 代表      | BERT+SQuAD     | GPT系列        | LangChain+VectorDB |

### Sparse vs Dense Retrieval

| Dimension | Sparse(TF-IDF/BM25) | Dense(DPR/BERT)  | Example (示例)              |
| --------- | ------------------- | ---------------- | --------------------------- |
| 匹配方式  | 关键词重叠          | 向量语义匹配     | 共同词vs含义                |
| 同义词    | ❌不同词=不匹配     | ✅语义相近=匹配  | "car"≠"automobile"(Sparse) |
| 预计算    | 不需要              | ✅段落向量离线存 | DPR:存入向量DB              |

## 3. Formulas (公式)

### QA Evaluation

| Formula (公式)                                                    | Description (说明) | Example (示例)          |
| ----------------------------------------------------------------- | ------------------ | ----------------------- |
| $\text{Precision}=\frac{|pred\cap gold|}{|pred|}$               | 预测中多少正确     | 5个token中4个正确→0.8  |
| $\text{Recall}=\frac{|pred\cap gold|}{|gold|}$                  | 正确中多少被预测   | 6个token中4个找到→0.67 |
| $\text{F1}=\frac{2PR}{P+R}$                                     | 调和平均           | P=0.8,R=0.67→F1≈0.73  |
| $\text{BERT Input}=\text{Token}+\text{Segment}+\text{Position}$ | 三层嵌入叠加       | 词义+句归属+位置        |

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)           | Correct Answer (正确答案)                           | Example (示例)             |
| --------------------- | --------------------------------------------------- | -------------------------- |
| BERT双向=Bi-LSTM?     | ❌ 完全不同! Bi-LSTM两方向拼接; BERT用全局自注意力  | BERT每token真正同时看所有  |
| BERT能生成文本?       | ❌ 只用Encoder! 不能自回归生成                      | 生成用GPT(Decoder)         |
| MLM 15%都替换[MASK]?  | ❌ 80%[MASK]+10%随机+10%不变                        | 避免训练-推理不匹配        |
| SQuAD答案可不在段落?  | ❌ 答案必须是段落中连续span                         | 不能生成新文本             |
| [CLS]只用于分类?      | ❌ 是整个输入浓缩表示; QA中start/end用段落token输出 | 分类:[CLS]; QA:段落各token |
| EM=0意味完全错误?     | ❌ EM=0不是完全匹配; F1=0.67说明大部分正确          | EM太严格                   |
| BERT能处理任意长文本? | ❌ 最大512tokens! 超过需滑动窗口                    | 1000词→切多个500token窗口 |
| DistilBERT性能差很多? | ❌ 97%性能/40%小/60%快→值得                        | 3%性能换40%内存+60%速度    |
| DPR用一个编码器?      | ❌ 两个独立编码器→双编码器架构                     | Q-Encoder≠P-Encoder       |

# W12: LLM & RAG (大语言模型 & 检索增强生成)

## 1. Definitions (定义)

### LLM Core (LLM 核心)

| Term (术语)          | Definition (定义)                              | Example (示例)                        |
| -------------------- | ---------------------------------------------- | ------------------------------------- |
| LLM (大语言模型)     | 参数>1B，基于Transformer，能理解和生成类人文本 | GPT-4, LLaMA-70B                      |
| Hallucination (幻觉) | 模型自信地生成事实不正确的信息 — 核心风险     | "BERT was released in 2020"(实际2018) |
| Temperature          | 控制随机性: 0→确定性; 1→创造性               | T=0:总是"Paris"; T=1:可能"Lyon"       |
| Top-k / Top-p        | 采样策略: Top-k=k个最高概率; Top-p=累积概率p   | Top-k=50; Top-p=0.9                   |
| Knowledge Cutoff     | 知识受限于训练数据截止日期                     | 无法获取最新信息                      |
| Context Window       | LLM一次能处理的最大token数                     | GPT-4:128K; BERT:512                  |
| In-Context Learning  | 通过prompt中的示例学习(不更新参数)             | Few-shot 给几个例子→LLM学会          |
| Emergent Abilities   | 模型超过某规模后涌现新能力                     | <100B不会CoT; >100B突然会             |

### RAG (检索增强生成)

| Term (术语)           | Definition (定义)                                        | Example (示例)           |
| --------------------- | -------------------------------------------------------- | ------------------------ |
| RAG                   | 检索文档→增强提示→基于文档生成答案; 解决知识过时和幻觉 | 领域精确/可追溯/成本可控 |
| Chunking (分块)       | 长文档切小段用于嵌入                                     | 固定512tok vs 按段落     |
| Vector Store (向量DB) | 存储文档嵌入，支持相似度搜索                             | Chroma, Faiss, Milvus    |
| Retriever             | 查询嵌入在向量DB中搜索最相关文档块                       | cosine→top-k chunks     |

### RAG Pipeline (6步)

| Step       | Operation        | Example (示例)        |
| ---------- | ---------------- | --------------------- |
| 1.Parse    | 文档→文本       | PDF/HTML→纯文本      |
| 2.Chunk    | 文本→块         | 256-512tok+50overlap  |
| 3.Embed    | 块→向量→存DB   | Sentence-BERT         |
| 4.Retrieve | 查询→top-k      | cosine相似搜索        |
| 5.Augment  | 检索结果→prompt | context+question→LLM |
| 6.Generate | LLM生成答案      | 有据可依              |

## 2. Comparisons (对比)

### RAG vs Pure LLM

| Dimension     | Pure LLM         | RAG              | Example (示例)                |
| ------------- | ---------------- | ---------------- | ----------------------------- |
| Knowledge     | 仅训练数据(静态) | 动态(检索最新)   | RAG可访问最新信息             |
| Hallucination | ⚠️高           | ✅基于文档(减少) | 有RAG:"2018"(对)              |
| Transparency  | ❌黑箱           | ✅展示源文档     | "According to Ch.3..."        |
| Cost          | 高(需大模型)     | 低(小模型+检索)  | Qwen0.5B+RAG≈GPT-4 on domain |

### RAG vs Fine-tuning

| Dimension | RAG             | Fine-tuning   | Example (示例)    |
| --------- | --------------- | ------------- | ----------------- |
| 知识更新  | ✅实时(换文档)  | ❌需重训      | RAG随时更新       |
| 成本      | 低(向量DB)      | 高(GPU训练)   | FT需标注数据+GPU  |
| 透明度    | ✅展示源文档    | ❌模型黑箱    | RAG可追溯         |
| 适用      | 领域QA/知识密集 | 行为/风格调整 | QA用RAG; 风格用FT |

## 3. Formulas (公式)

### Retrieval Metrics

| Metric | Formula                                      | Example (示例)           |
| ------ | -------------------------------------------- | ------------------------ |
| P@k    | relevant in top-k / k                        | top-5中3个相关→P@5=0.6  |
| R@k    | relevant in top-k / total relevant           | 10个相关找到3个→R@5=0.3 |
| MRR    | 1 / rank of first relevant                   | 第2位→MRR=0.5           |
| DCG@k  | $\sum_{i=1}^{k} \frac{rel_i}{\log_2(i+1)}$ | 惩罚排在后面的正确结果   |
| NDCG@k | DCG@k / IDCG@k                               | 考虑整体排序质量         |

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)          | Correct Answer (正确答案)          | Example (示例)         |
| -------------------- | ---------------------------------- | ---------------------- |
| LLM"理解"语言?       | ❌ 模式匹配非推理!                 | 9.11>9.9? LLM可能说Yes |
| RAG完全解决幻觉?     | ❌ 减少但不消除! 可能检索错误段落  | 错误chunk→仍可能错    |
| Temperature越高越好? | ❌ 高→创造但不准; 低→准但单调    | 精确QA用T=0            |
| RAG=Fine-tuning?     | ❌ RAG=运行时检索; FT=修改模型权重 | 完全不同!              |

# W13: LLM Compression & Prompt Engineering (压缩 & 提示工程)

## 1. Definitions (定义)

### Model Compression (模型压缩)

| Term (术语)                   | Definition (定义)                                | Example (示例)                    |
| ----------------------------- | ------------------------------------------------ | --------------------------------- |
| Quantization (量化)           | 降低权重精度: FP32→FP16→INT8→INT4; 无需重训练 | 65B×4B=260GB→65B×1B=65GB(INT8) |
| Knowledge Distillation (蒸馏) | 小"学生"模仿大"教师"输出分布                     | BERT→DistilBERT: 97%性能,60%小   |
| Pruning (剪枝)                | 移除不重要权重/神经元; 可能需重训恢复            | 移除90%权重→重训                 |

### Transfer Learning & PEFT

| Term (术语)             | Definition (定义)                                       | Example (示例)             |
| ----------------------- | ------------------------------------------------------- | -------------------------- |
| Transfer Learning       | 冻结预训练模型，只训分类头(~0.1%参数)                   | 最快最节省                 |
| Full Fine-tuning        | 调全部参数(100%)，效果最好但内存极高                    | 灾难性遗忘风险             |
| LoRA                    | 冻结原模型，只训两个小低秩矩阵A(d×r)B(r×d)，参数减98% | W'=W+ΔW; ΔW=A×B; r=4~16 |
| QLoRA                   | LoRA+4bit量化基座→消费级GPU可训大模型                  | 65B→48GB GPU可训!         |
| Catastrophic Forgetting | 全量微调可能丢失预训练知识                              | FT on task A后task B变差   |

### Prompt Engineering (提示工程)

| Term (术语)  | Definition (定义)                           | Example (示例)                                    |
| ------------ | ------------------------------------------- | ------------------------------------------------- |
| Prompt 4要素 | Context+Instructions+Input+Output Indicator | "你是数据科学家, 做情感分析, 文本:…, Sentiment:" |
| Zero-shot    | 只给指令，不给示例                          | "Translate: Hello→French"                        |
| Few-shot     | 指令+2-5个示例                              | 给示例后classify                                  |
| CoT (思维链) | "Let's think step by step"→展示推理过程    | 数学/逻辑/多步骤                                  |
| Role-based   | "You are a [expert]"→赋予角色              | "You are a cardiologist"                          |

## 2. Comparisons (对比)

### Quantization vs Pruning vs Distillation

| Dimension   | Quantization | Pruning      | Distillation | Example (示例)         |
| ----------- | ------------ | ------------ | ------------ | ---------------------- |
| What        | 降精度       | 移除连接     | 训练新小模型 | 精度↓vs连接↓vs新模型 |
| Re-training | ❌不需要     | ⚠️可能需要 | ✅需要       | 量化最快               |
| Size        | ~2-8×       | ~2-10×      | 取决于学生   | INT8≈4×              |

### Transfer vs Full Fine-tune vs LoRA

| Dimension      | Transfer | Full FT | LoRA    | Example (示例)           |
| -------------- | -------- | ------- | ------- | ------------------------ |
| Params trained | ~0.1%    | 100%    | ~0.1-1% | LoRA极省内存             |
| Memory         | 低       | 非常高  | 低      | 7B全量→40GB+; LoRA→8GB |
| Forgetting     | 低风险   | 高风险  | 低风险  | 全量微调可能丢预训练知识 |

### 量化大小计算 (必记!)

| Model (参数) | FP32(×4) | FP16(×2) | INT8(×1) | INT4(×0.5) |
| ------------ | --------- | --------- | --------- | ----------- |
| 340M         | 1.3GB     | 680MB     | 340MB     | 170MB       |
| 7B           | 28GB      | 14GB      | 7GB       | 3.5GB       |
| 70B          | 280GB     | 140GB     | 70GB      | 35GB        |

### Floating Point Formats (浮点格式)

| Format | Bits | Range         | Example (示例)     |
| ------ | ---- | ------------- | ------------------ |
| FP32   | 32   | ±3.4×10³⁸ | 标准训练精度       |
| FP16   | 16   | ±65504       | 混合精度训练       |
| BF16   | 16   | ±3.4×10³⁸ | 同FP32范围但精度低 |
| INT8   | 8    | -128~127      | 推理量化           |
| INT4   | 4    | -8~7          | 极致压缩           |

## 3. Formulas (公式)

### Quantization Size

| Formula (公式)                      | Description (说明) | Example (示例)  |
| ----------------------------------- | ------------------ | --------------- |
| $\text{FP32}: N\times4\text{B}$   | 每参数4字节        | 340M×4=1.36GB  |
| $\text{INT8}: N\times1\text{B}$   | 每参数1字节        | 340M×1=340MB   |
| $\text{INT4}: N\times0.5\text{B}$ | 每参数0.5字节      | 340M×0.5=170MB |

### LoRA Math

| Formula (公式)                         | Description (说明)       | Example (示例)     |
| -------------------------------------- | ------------------------ | ------------------ |
| $W'=W+\Delta W;\;\Delta W=A\times B$ | 低秩分解: d²→2dr(r≪d) | r=4,d=768→98%减少 |

## 5. Exam Traps (考试陷阱)

| Trap (陷阱)              | Correct Answer (正确答案)                | Example (示例)              |
| ------------------------ | ---------------------------------------- | --------------------------- |
| LoRA训练所有参数?        | ❌ 只训小适配矩阵(~0.1%)! 基座冻结       | 7B:全量=7B params; LoRA≈7M |
| 大小规则                 | FP32=×4, FP16=×2, INT8=×1, INT4=×0.5 | **必记!**             |
| QLoRA只是LoRA?           | ❌ QLoRA=LoRA+4bit量化基座!              | 65B→48GB GPU可训           |
| Quantization改变参数值?  | ❌ 不改变值只降精度! 剪枝才移除参数      | 值不变精度降                |
| Zero-shot总比Few-shot好? | ❌ Few-shot通常更稳定!                   | 复杂任务→Few-shot必须      |

---

# 📝 简答题速查 (Short Answer Quick Reference)

> **考试策略**: 5道核心题覆盖 W3/W9/W10/W12/W13，每题6分=30分。先写公式→代入数值→写结论。
> **时间分配**: 每题≤8分钟，先做会的，公式记不清也要写思路拿步骤分。

## 🔴 核心5题 (必考，每题6分)

### SA-1: TF-IDF + Cosine Similarity (W3) [2+2+2]

**公式三件套**:
$\text{TF}=\frac{count}{total}$ | $\text{IDF}=\log_2\frac{N}{df}$ | $\text{TF-IDF}=\text{TF}\times\text{IDF}$

$\cos(\mathbf{A},\mathbf{B})=\frac{\mathbf{A}\cdot\mathbf{B}}{\|\mathbf{A}\|\times\|\mathbf{B}\|}$

**⚠️ 陷阱**: 共同词 $df=N \Rightarrow \text{IDF}=\log_2 1=0$ → 被消除!

**完整例题**: D1="the cat sat on the mat", D2="the dog sat on the log" (N=2)

- **(a)** TF(cat,D1)=1/6≈0.167, IDF(cat)=log₂(2/1)=1.0, **TF-IDF=0.167**
- **(b)** 共同词(the,sat,on) IDF=0→消除; D1=[0,1/6,0,0,1/6,0,0], D2=[0,0,0,0,0,1/6,1/6]
- **(c)** D1·D2=0 → **cos=0** (独有词不重叠)

**向量计算模板**: w₁=(0.2,0.2,0.3,0.7) w₂=(0.3,0.4,0.8,0.5) → 点积=0.73, ‖w₁‖=√0.66≈0.81, ‖w₂‖=√1.14≈1.07 → cos≈**0.84**

### SA-2: Transformer Attention (W9) [2+2+2]

**(a) 公式**: $\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$

**(b) QKV**: $Q=XW_Q$(找什么), $K=XW_K$(提供什么), $V=XW_V$(实际内容); Cross-Attn: Q=解码器,KV=编码器

**(c) 为什么÷$\sqrt{d_k}$**: $d_k$大→$QK^T$方差~$d_k$→softmax过尖[0.99,0.005]→梯度≈0→训练崩; ÷$\sqrt{d_k}$→方差~1→softmax平滑[0.4,0.3]→梯度健康

**参数速记**: $d_{model}=768, h=12, d_k=64, N=12$ | $PE_{(pos,2i)}=\sin(pos/10000^{2i/d})$

**数值计算模板**: $Q=[1,0], K_1=[1,0], K_2=[0,1], V_1=[10,0], V_2=[0,10], d_k=2$

1. 点积: $Q \cdot K_1^T=1, \; Q \cdot K_2^T=0$
2. 缩放: $\frac{1}{\sqrt{2}}≈0.707, \; \frac{0}{\sqrt{2}}=0$
3. Softmax: $e^{0.707}≈2.03, e^0=1 \Rightarrow \alpha_1≈0.67, \alpha_2≈0.33$
4. 输出: $0.67\times[10,0]+0.33\times[0,10]≈\mathbf{[6.7, 3.3]}$

### SA-3: BERT MLM + NSP (W10) [3+1+2]

**(a) MLM**: 随机选**15%** token → 80%→[MASK] | 10%→随机词 | 10%→不变

**(b) NSP**: [CLS]SentA[SEP]SentB[SEP] → 二分类IsNext/NotNext(各50%); $\mathcal{L}=\mathcal{L}_{MLM}+\mathcal{L}_{NSP}$

**(c) 为什么80/10/10**: 100%[MASK]→推理时无[MASK]→**训练-推理不匹配**; 10%随机→强制关注所有位置; 10%不变→保持正常token表示

**速记**: BERT-base: 12层/768维/12头/110M | 输入=Token+Segment+Position Embedding | WordPiece~30.5K

### SA-4: RAG Pipeline (W12) [3+2+1]

**(a) 6步** ← 口诀 **P-C-E-R-A-G**:
①Parse(文档→文本) ②Chunk(256-512tok+overlap) ③Embed(块→向量) ④Retrieve(cosine→top-k) ⑤Augment(块→prompt) ⑥Generate(LLM生成)

**(b) 2优势**: ①解决知识过时(运行时检索最新文档) ②减少幻觉+可追溯(可引用源"Ch.3,p.45")

**(c) 消除幻觉?** ❌减少但不消除! retriever可能检索错误chunk→LLM仍可能错 | RAG≠FT(RAG不改权重)

### SA-5: Compression + Memory (W13) [3+2+1]

**(a) 三种压缩**:

| 方法         | 做什么             | 重训?        | 例子                          |
| ------------ | ------------------ | ------------ | ----------------------------- |
| Quantization | 降精度FP32→INT8   | ❌不需要     | BERT 1.36GB→340MB            |
| Pruning      | 移除权重(设0)      | ⚠️可能需要 | 移除90%→微调                 |
| Distillation | 学生模仿教师软概率 | ✅需训练     | BERT→DistilBERT 97%质量60%小 |

**(b) 显存计算**: $\text{Memory}=N\times\text{bytes}$ → $\boxed{\text{FP32}=\times4,\;\text{FP16}=\times2,\;\text{INT8}=\times1,\;\text{INT4}=\times0.5}$

| 模型 | FP32 | FP16 | INT8 | INT4  |
| ---- | ---- | ---- | ---- | ----- |
| 7B   | 28GB | 14GB | 7GB  | 3.5GB |

**(c) LoRA**: 冻结基座,只训 $A(d\times r),B(r\times d)$, $r\ll d$; $d^2\to 2dr$(98%减); QLoRA=LoRA+4bit基座

**LoRA 计算模板**: BERT-base, $d=768$, $r=8$, 只对 Q+V 加 LoRA

- 原始 Q+V 每层: $768^2 \times 2 = 1,179,648$
- LoRA 每层: $(768\times8 + 8\times768)\times 2 = 24,576$
- 全12层: $24,576\times12 = 294,912 \approx 295K$ → 占比 $\frac{295K}{14.2M}\approx\mathbf{2.08\%}$

## 🟡 备选题 (按出题可能性排序)

### B-1: Retrieval Metrics (W12) ⭐⭐⭐

**公式**: $P@k=\frac{rel_{top-k}}{k}$ | $R@k=\frac{rel_{top-k}}{total_{rel}}$ | $MRR=\frac{1}{rank_1}$ | $DCG@k=\sum_{i=1}^{k}\frac{rel_i}{\log_2(i+1)}$ | $NDCG@k=\frac{DCG@k}{IDCG@k}$

**完整例题**: 搜索返回5个结果, relevance=[1,0,1,1,0], 总共有4个相关文档

- **P@5** = 3 relevant in top-5 / 5 = **0.6**
- **R@5** = 3 found / 4 total relevant = **0.75**
- **MRR** = first relevant at position 1 → 1/1 = **1.0**
- **DCG@5** = $\frac{1}{\log_2 2}+\frac{0}{\log_2 3}+\frac{1}{\log_2 4}+\frac{1}{\log_2 5}+\frac{0}{\log_2 6}$ = $1+0+0.5+0.431+0$ = **1.931**
- **IDCG@5** (理想排序=[1,1,1,1,0]) = $\frac{1}{1}+\frac{1}{0.631}+\frac{1}{0.5}+\frac{1}{0.431}+0$ = $1+\frac{1}{1.585}+0.5+0.431+0$ = **2.562**
- **NDCG@5** = 1.931 / 2.562 = **0.754**

**⚠️ 陷阱**: $\log_2$ 底数是2不是10! IDCG用**理想排序**(相关文档全排前面)。MRR只看**第一个**相关结果的位置。

## 🟢 Concept Short Answers (概念描述简答)

### C-1: What is Word Embedding? Why better than BOW/TF-IDF? ⭐⭐⭐

**Answer**: Word embedding maps each word to a **low-dimensional dense vector** (50-300d) where semantically similar words are closer. Based on the **Distributional Hypothesis**: words in similar contexts have similar meanings.

**vs BOW/TF-IDF**: ①BOW/TF-IDF = high-dim sparse (V=10K, 99% zeros); Embedding = low-dim dense (300d). ②BOW has no word order or semantics; embeddings capture semantic relations (king-man+woman≈queen). ③BOW cannot handle OOV; FastText uses subword n-grams for OOV.

### C-2: What is Attention? What problem does it solve? ⭐⭐⭐

**Answer**: Seq2Seq has an **information bottleneck**: entire input compressed into one fixed-size vector → long sequences lose information. Attention solution: decoder **dynamically computes** weights over all encoder states at each step → weighted sum → no longer depends on single vector.

**4 steps**: ①Score: $e_i=\text{dec}^T\cdot\text{enc}_i$ ②Normalize: softmax→probs ③Context: $c=\sum\alpha_i\cdot h_i$ ④Output: [dec;c]→FC

**⚠️**: Seq2Seq+Attention still **cannot parallelize** (still uses RNN)! Only Transformer enables parallelism.

### C-3: Compare BERT vs GPT architecture and use cases ⭐⭐⭐

**Answer**: BERT = **Encoder-only** (bidirectional self-attention, sees full context) → excels at **understanding** tasks (classification/NER/QA). GPT = **Decoder-only** (masked self-attention, sees only left context) → excels at **generation** tasks (dialogue/creation).

**Pre-training**: BERT = MLM (predict masked word) + NSP; GPT = CLM (predict next word). **Key**: BERT **cannot generate** (no Decoder); GPT generates well but weaker at understanding than BERT.

### C-4: Explain Transfer Learning in NLP ⭐⭐

**Answer**: Pre-train on **massive unlabeled text** (learn general language knowledge) → then fine-tune with **small labeled data** for specific tasks. Value: pre-training is extremely expensive (64 TPUs, millions $, months) → done once; fine-tuning is cheap (1 GPU, hours) → done per task.

**3 strategies**: ①Transfer Learning (freeze base, train classifier head only, ~0.1%) ②Full Fine-tuning (all 100% params, best but catastrophic forgetting risk) ③LoRA (freeze base + small adapter matrices, ~0.1-1%, best cost-performance)

### C-5: Explain RNN vanishing gradient & how LSTM solves it ⭐⭐

**Answer**: During backpropagation, gradients pass through $W_h$ at each step → exponential shrinkage (|W_h|<1 → gradient→0) → **cannot learn long-range dependencies** (info from 10+ steps ago is lost).

**LSTM solution**: Introduces **cell state** $c_t$ updated via **addition** (not multiplication): $c_t=f_t\odot c_{t-1}+i_t\odot\tilde{c}_t$. Addition gradient = 1 → gradient flows directly → long-term info preserved. 3 gates (Forget/Input/Output) dynamically control information flow.

### C-6: What is RAG? What LLM problems does it solve? ⭐⭐

**Answer**: RAG = Retrieval-Augmented Generation. **6-step pipeline**: Parse→Chunk→Embed→Retrieve→Augment→Generate (mnemonic **P-C-E-R-A-G**).

**Solves 3 problems**: ①**Knowledge cutoff** (retrieves latest docs at runtime) ②**Hallucination** (generates based on retrieved docs, traceable to source) ③**Cost** (small model + retrieval ≈ large model performance on domain)

**⚠️**: RAG **reduces but does NOT eliminate** hallucination! Retriever may fetch wrong chunks. RAG ≠ Fine-tuning (RAG does not modify model weights!)

### C-7: What is the Transformer? Why is it better than RNN? ⭐⭐⭐

**Answer**: Transformer (2017, "Attention Is All You Need") replaces RNN with **self-attention** — every token attends to all other tokens simultaneously. Key advantages: ①**Parallelizable** (no sequential dependency like RNN) ②**O(1) path length** between any two words (vs RNN's O(n) steps → vanishing gradient) ③**Multi-head attention** learns multiple relationship types simultaneously.

**Trade-off**: O(n²) memory for attention matrix (vs RNN's O(n)). Requires **positional encoding** since self-attention has no inherent position awareness.

### C-8: What is Knowledge Distillation? ⭐⭐

**Answer**: Train a small **student** model to mimic a large **teacher** model's output probability distribution (soft labels), not just hard labels. The student learns the teacher's "dark knowledge" — e.g., teacher says P(cat)=0.7, P(dog)=0.2, P(car)=0.1 → student learns cat≈dog≠car.

**Example**: BERT (110M) → DistilBERT (66M): **97% performance, 40% smaller, 60% faster**. Requires retraining (unlike quantization which needs no retraining).

### C-9: What is LoRA? Why is it important? ⭐⭐

**Answer**: LoRA (Low-Rank Adaptation) **freezes** the pre-trained model and adds two small trainable matrices $A(d×r)$ and $B(r×d)$ where $r \ll d$. Update: $W'=W+\Delta W$, $\Delta W=A×B$. Parameters reduced from $d^2$ to $2dr$ (**~98% reduction**).

**Why important**: Full fine-tuning of 7B model needs 40GB+ VRAM; LoRA needs ~8GB. **QLoRA** = LoRA + 4-bit quantized base → 65B model trainable on 48GB consumer GPU!

### C-10: Compare Extractive QA vs Generative QA ⭐⭐

**Answer**: **Extractive QA** (BERT+SQuAD): answer is copied as a **continuous span** from the passage (start/end position prediction). Advantage: traceable, no hallucination. Limitation: answer must exist verbatim in text.

**Generative QA** (GPT): model **generates** new text as answer. Advantage: flexible, can synthesize from multiple sources. Risk: may hallucinate. **RAG** combines both: retrieve docs (like extractive) then generate answer (like generative).
