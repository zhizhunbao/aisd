# W1: NLP Overview (NLP 概述)

## 1. Definitions (定义)

### Core Terms (核心术语)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| NLP (自然语言处理) | 用计算机处理人类语言的技术领域 (Linguistics×CS×AI)，核心能力：处理、理解、生成 | Siri 语音助手、Google 翻译、ChatGPT |
| NLU (自然语言理解) | NLP 的"读"的部分：让机器读懂文本含义 (Classification, NER, Sentiment) | 输入 "I love this!" → 机器判断为"正面情感" |
| NLG (自然语言生成) | NLP 的"写"的部分：让机器生成人类可读的文本 (Translation, Summarization) | 输入法语 → 输出英语翻译；输入长文 → 输出摘要 |
| NLP = NLU + NLG | NLP 由理解 (Understanding) + 生成 (Generation) 两大能力组成 | 聊天机器人：先理解问题 (NLU)，再生成回答 (NLG) |
| Turing Test (图灵测试, 1950) | 人类评估者分不清对面是人还是机器 → 说明机器通过了测试 | 评估者问问题，50% 时间判断错 → 机器通过 |
| NER (命名实体识别) | 从文本中识别出人名、地名、组织名等专有名词并分类 | "Apple was founded by Steve Jobs in California" → Apple=ORG, Steve Jobs=PERSON |
| Supervised Learning (监督学习) | 用带标签的数据训练模型 — 告诉模型“正确答案是什么” | 给 1000 条邮件打标 spam/not spam → 训练分类器 |
| Unsupervised Learning (无监督学习) | 用无标签的数据发现隐藏模式 — 模型自己找结构 | 把 1000 篇新闻自动聚成 5 个 topic (聚类)

### Knowledge Representation (知识表示)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Document (文档) | 原始或半结构化的文本数据，是 NLP 的输入原料 | 新闻文章、PDF 报告、网页正文 |
| Knowledge (知识) | 从文档中提取的结构化信息 (实体、关系、事实)，机器可直接使用 | "Ottawa is the capital of Canada" → (Ottawa, capital-of, Canada) |
| Corpus (语料库) | 用于 NLP 训练/分析的大规模文本集合 | Wikipedia 全文、IMDb 影评数据集、新闻语料 |

### Zipf's Law & Sparsity (齐普夫定律与稀疏性)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Zipf's Law (齐普夫定律) | 自然语言中词频与排名成反比：freq ∝ 1/rank，少数词极高频，大多数词极低频 | Rank 1: "the" (7%); Rank 2: "of" (3.5%); Rank 10: ~0.7% |
| Log-log Plot (对数-对数图) | 横轴和纵轴都取对数的图，用于验证幂律 (Power Law)：如果数据呈直线则符合 | 横轴=log(rank), 纵轴=log(freq) → 直线 = 符合 Zipf |
| Frequency Distribution (频率分布) | 统计每个词出现的次数并排序，是文本分析的基础操作 | "the":5000次, "cat":12次, "serendipity":1次 |
| Long Tail (长尾) | 齐普夫分布的右侧尾部：大量词只出现极少次数，但占据词表的绝大部分 | 高频词 ("the","is") 占大部分出现次数，稀有词占大部分词表 |
| Hapax Legomena (单次词) | 在语料中只出现一次的词，通常超过总词表的 1/3 | "serendipity" 在一个 7000 词的语料中只出现 1 次 |
| Linear Regression (线性回归) | 用一条直线去拟合数据点，计算斜率和拟合度 (R²) | 对 log(rank) vs log(freq) 做回归 → 得到 α 和 R² |
| Alpha (α, 齐普夫指数) | log-log 线性回归的斜率绝对值，理想值 ≈ 1.0，衡量词频下降速度 | 文学文本 α≈1.4 (词汇集中); 宗教文本 α≈1.6 (词汇分散) |
| R² (决定系数) | 线性回归拟合度，范围 [0,1]，越接近 1 说明齐普夫定律拟合越好 | R²=0.95+ → 数据非常符合齐普夫定律 |

### 4 NLP Challenges (4大挑战)

| Challenge (挑战) | Definition (定义) | Example (示例) |
|-----------|-----------|---------|
| Ambiguity (歧义性) | 同一句话有多种理解方式：词汇歧义 / 句法歧义 / 指代歧义 | "bank" = 银行 or 河岸？"I saw her with a telescope" = 谁拿望远镜？ |
| Sparsity (稀疏性) | 齐普夫定律 (Zipf's Law)：词频 ∝ 1/排名，超过 1/3 的词只出现一次 | 语料中 "the" 占 7%，但 "serendipity" 可能只出现 1 次 |
| Variation (变异性) | 同一个意思可以用完全不同的词/句式表达 (词汇/地域/社会/风格/代际差异) | "awesome" vs "splendid" vs "fire" 都表示"很好" |
| Common Knowledge (常识知识) | 机器缺乏人类的世界常识，无法判断合理性 | "man bites dog" = 新闻 (反常)；"dog bites man" = 不是新闻 (正常) |

### NLP Preprocessing Preview (NLP预处理术语预览 — W2详解)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Tokenization (分词) | 把文本切分成最小有意义的单元 (token) | "I love NLP" → ["I", "love", "NLP"] |
| Stopwords (停用词) | 高频但无实际意义的词，通常在分析前移除 | "the", "is", "at", "a" → 移除后保留实义词 |
| Stemming (词干提取) | 粗暴地砍掉词尾，得到词根 (可能不是真词) | "studies" → "studi" (Porter); "running" → "run" |
| Lemmatization (词元化) | 用词典还原到标准词形 (一定是真词) | "studies" → "study"; "better" → "good" |
| POS Tagging (词性标注) | 给每个词标上语法类别 (名词/动词/形容词等) | "The(DT) quick(JJ) fox(NN) runs(VBZ)" |
| TF-IDF (词频-逆文档频率) | 衡量一个词对文档的重要性：在本文档高频 + 在其他文档低频 = 重要 | "NLP" 在本文出现 10 次但整体语料只出 5 篇 → TF-IDF 高 |
| Data Leakage (数据泄漏) | 训练时不小心用了测试集的信息，导致模型性能虚高，实际部署表现差 | ✖ 先 TF-IDF fit 全部数据再拆分 → 测试集信息泄漏到训练 |
| Train/Test Split (训练/测试拆分) | 把数据分成训练集和测试集，模型只在训练集上学，测试集用来评估 | 80% 训练 / 20% 测试；必须在预处理之前拆分 |

### NLP Python Libraries (Python NLP 工具库)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| NLTK | 最经典的 NLP 教学工具库，功能全但慢，适合学习和原型验证 | `nltk.word_tokenize("I love NLP")` → ['I','love','NLP'] |
| SpaCy | 工业级 NLP 库，速度快、管道化设计，适合生产部署 | `nlp("I love NLP")` → 一次调用完成分词+词性+NER |
| HuggingFace Transformers | 预训练模型 (BERT/GPT) 的开源平台，一行代码调用最先进模型 | `pipeline("sentiment-analysis")("I love NLP")` → Positive |

## 2. Comparisons (对比)

### Structured vs Unstructured Knowledge (结构化 vs 非结构化知识)

| Dimension (维度) | Structured (结构化) | Unstructured (非结构化) | Example (示例) |
|-----------|---------------------|------------------------|---------|
| Nature (本质) | 精确、可直接操作 (Precise, Actionable) | 模糊、需要解析 (Ambiguous) | 数据库表格 vs 一封邮件正文 |
| Scope (规模) | 针对特定任务的少量数据 | 企业数据中 >80% 是非结构化的 | CRM 数据库 vs 客户邮件+聊天记录 |
| Humans (人类) | 能读但很慢 (Can read, but slowly) | 量太大记不住 (Can't remember all) | 读 1 万行表格 vs 读 1 万封邮件 |
| Computers (计算机) | 可直接查询使用 (Use quickly) | 需要 NLP 技术才能处理 | SQL 查询 vs NLP 文本分析 |

### 7 NLP Applications (7大应用分类)

| Application (应用) | Type (类型) | Example (示例) |
|-------------|------|---------|
| Speech Recognition (语音识别) | NLU | Siri 把语音转成文字 |
| Dialogue/Chatbot (对话机器人) | NLU+NLG | ChatGPT 理解问题 + 生成回答 |
| Text Classification (文本分类) | NLU | 邮件分类：垃圾邮件 vs 正常邮件 |
| Sentiment Analysis (情感分析) | NLU | "This movie is great!" → Positive |
| Summarization (文本摘要) | NLG | 10 页论文 → 3 句话摘要 |
| QA (问答系统) | NLU+NLG | "What is NLP?" → 生成答案 |
| Generative AI (生成式AI) | NLG | GPT-4 生成文章/代码/诗歌 |

### 3 NLP Approaches (3种方法)

| Approach (方法) | Method (具体手段) | Example (示例) |
|----------|--------|---------|
| Heuristics (启发式/规则法) | 人工写规则和正则表达式 (Rules / Regex) | `if "not" in text: sentiment = negative` |
| ML (机器学习) | 用标注数据训练模型 (Supervised / Unsupervised) | TF-IDF + Logistic Regression 分类垃圾邮件 |
| DL (深度学习) | 用神经网络自动学习特征 (RNN, LSTM, Transformer) | BERT 做情感分析，GPT 做文本生成 |

### AI Hierarchy (AI层级关系)

| Level (层级) | Relationship (关系) | Example (示例) |
|-------|-------------|---------|
| AI ⊃ ML ⊃ DL | 嵌套包含关系：AI 最大，ML 是 AI 的子集，DL 是 ML 的子集 | AI: 专家系统; ML: SVM; DL: Transformer |
| NLP (自然语言处理) | NLP 是 AI 的应用领域，横跨所有层级 (规则→ML→DL 都能做 NLP) | 规则 NLP: 正则; ML NLP: TF-IDF; DL NLP: BERT |

## 3. Formulas (公式)

_No formulas this week._

## 4. Practical / Lab (实战结论)

### 🔑 NLP 能做什么 vs 不能做什么 (Key Capabilities)

| 能力 (Capability) | 能做 ✅ | 不能做 ❌ | Example (示例) |
|------|--------|---------|---------|
| 文本分类 (Classification) | 把文本分到预定义类别 | 理解文本的"真正含义" | 垃圾邮件过滤：spam / not spam |
| 情感分析 (Sentiment) | 判断正面/负面情绪 | 理解讽刺和反语 | "Great, another Monday" → 机器判 Positive (实际是讽刺) |
| 翻译 (Translation) | 语言间转换 | 完美处理文化隐喻 | "It's raining cats and dogs" → 机器可能直译 |

### 📊 NLP 开发 8 步周期 (Dev Life Cycle) — 考试要记顺序！

| Step (步骤) | 做什么 (What) | Example (示例) |
|------|--------|---------|
| ① Requirement (需求) | 明确要解决什么问题 | "我要做一个情感分析系统" |
| ② Data Collection (数据收集) | 获取训练数据 | 下载 IMDb 影评数据集 |
| ③ Preprocessing (预处理) | 清洗和规范化文本 | 去掉 HTML 标签、转小写、分词 |
| ④ Feature Extraction (特征提取) | 把文本变成数字向量 | TF-IDF、Word2Vec |
| ⑤ Model Building (建模) | 选择和训练模型 | LogReg、LSTM、BERT |
| ⑥ Evaluation (评估) | 测试模型效果 | Accuracy=91%, F1=0.89 |
| ⑦ Deployment (部署) | 上线到生产环境 | Flask API / Docker 容器 |
| ⑧ Iteration (迭代) | 根据反馈改进重来 | 发现新类型垃圾邮件 → 加数据重训 |

### 📊 Lab 1 结论: Zipf's Law 验证实验

| Finding (发现) | Detail (详情) | Example (示例) |
|---------|--------|---------|
| 齐普夫定律 (Zipf's Law) 在真实文本中成立 | Log-log 图 (对数图) 呈直线，R²>0.95 说明拟合极好 | 文学文本 R²=0.95+; 宗教文本 R²=0.95+ |
| 文学文本 vs 信息文本的 alpha 不同 | 文学文本 alpha 较低 (~1.4) = 词汇更集中；信息文本 alpha 较高 (~1.6) = 词汇更分散 | Emma(小说): α≈1.39; Bible(宗教): α≈1.63 |
| 去停用词 (Remove Stopwords) 后齐普夫定律仍成立 | alpha 值变化但直线形态保持 → 定律对预处理鲁棒 | 去停用词后: α 变化 ≈ +0.1, R² 仍 >0.93 |
| 只保留名词 (Nouns Only) 后仍然成立 | POS 过滤 (词性筛选) 后分布still follows Zipf → 定律跨词性稳定 | 名词: α≈1.2, R²>0.90 |
| 超过 1/3 的词只出现一次 (Hapax Legomena) | 稀疏性是 NLP 的核心挑战，大量词没有足够统计数据 | 词表 7000 词中 ~2500 词仅出现 1 次 |
| `nltk.FreqDist()` 统计词频 | NLTK 原生频率分布工具，直接输入 token 列表 | `fdist = FreqDist(tokens)` → `fdist.most_common(20)` |
| `scipy.stats.linregress()` 验证齐普夫 | 对 log(rank) vs log(freq) 做线性回归，得 alpha 和 R² | slope=-1.4, R²=0.95 → 验证 freq ∝ 1/rank^α |

### ⚠️ W1 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------|
| NLP = NLU? | ❌ NLP = NLU (理解) + NLG (生成)，两部分缺一不可 | 聊天机器人需要 NLU 理解问题 + NLG 生成回答 |
| AI, ML, DL 是并列关系? | ❌ 嵌套包含：AI ⊃ ML ⊃ DL (大圈套小圈) | DL 是 ML 的子集，ML 是 AI 的子集 |
| 数据先预处理再拆分? | ❌ 必须先拆分 (Split) 再预处理，否则数据泄漏 (Data Leakage) | ✅ split → fit TF-IDF on train only; ❌ fit on all → split |
| NLP 三种方法哪个最好? | 没有绝对最好，取决于任务和数据量 | 少数据 → 规则法; 中数据 → ML; 大数据 → DL |

