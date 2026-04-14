# W10: BERT & Question Answering (BERT & 问答系统)

## 1. Definitions (定义)

### BERT Architecture (BERT 架构)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| BERT (2018 Google) | Bidirectional Encoder Representations from Transformers，用双向 Transformer Encoder 做语言理解 | 演化路径: RNN→LSTM→Bi-LSTM→Attention→Transformer→**BERT** |
| BERT-base | 12层 Encoder, 768隐藏维度, 12注意力头, 110M参数 | 通用NLP任务的标准选择 |
| BERT-large | 24层 Encoder, 1024隐藏维度, 16注意力头, 340M参数 | 更高精度但需要更多计算资源 |
| Pre-training (预训练) | 在大规模无标注语料 (Wikipedia 2.5B词 + BookCorpus 800M词) 上无监督学习通用语言知识 | 只做一次，非常昂贵 (TPU级算力) |
| Fine-tuning (微调) | 在预训练模型上加一个小分类层，用少量标注数据针对特定任务调整全部权重 | 每个任务做一次，相对便宜 |
| MLM (Masked Language Model, 掩码语言模型) | 随机掩码 15% 的 token (80%→[MASK], 10%→随机词, 10%→保持不变) → 预测被掩码词 | "went to the [MASK]" → 预测 "store" |
| NSP (Next Sentence Prediction, 下一句预测) | 输入 [CLS] sent_A [SEP] sent_B，判断 sent_B 是否是 sent_A 的下一句 | Total Loss = MLM Loss + NSP Loss |
| [CLS] token | 输入序列的第一个特殊 token，经过处理后作为整个序列的聚合表示，用于分类任务 | [CLS] 的输出向量 → 接分类层 → 情感标签 |
| [SEP] token | 分隔两个句子段的特殊 token，在末尾也加一个 | [CLS] sent_A [SEP] sent_B [SEP] |
| [MASK] token | 掩码语言模型中用来替换被遮蔽词的特殊 token | "the cat [MASK] on the mat" → "sat" |
| WordPiece (子词分词) | BERT 的分词算法，将 OOV 词拆成已知子词片段，词汇表约 30,500 | "playing" → "play" + "##ing"; "unhappiness" → "un" + "##hap" + "##pi" + "##ness" |
| BERT Input Embedding (输入嵌入) | Token Embedding + Segment Embedding + Position Embedding 三种嵌入相加 | Segment A=0, Segment B=1 区分两句 |
| Transfer Learning (迁移学习) | 用预训练模型的知识迁移到新任务：预训练→理解语言→微调→解决具体任务 | 预训练: 无语言知识 → 训练: 理解语言 → 微调: 做情感分析 |
| DistilBERT (蒸馏BERT) | 知识蒸馏产物：保留 BERT 97% 的性能，减少 40% 内存，速度快 60% | BERT:110M params → DistilBERT:66M params |

### Question Answering (问答系统)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| QA System (问答系统) | 给定问题自动返回答案的系统，分类维度：信息源、问题类型、答案类型 | Q: "When was BERT released?" → A: "2018" |
| Extractive QA (抽取式QA) | 答案是给定段落中的一个连续文本片段 (span)，BERT 预测起止位置 | (P, Q) → A; 答案一定在段落中 |
| Abstractive QA (生成式QA) | 答案由模型生成，可能不逐字出现在原文中 | 需要 Encoder-Decoder 架构 (非 BERT alone) |
| SQuAD (Stanford QA Dataset) | 斯坦福问答数据集：10万个 (段落, 问题, 答案) 三元组，段落来自 Wikipedia | 最流行的阅读理解数据集 |
| Answer Span (答案跨度) | 答案在段落中的起始(start)和结束(end) token 位置 | start=5, end=7 → 段落中第5到第7个token |
| Reading Comprehension (阅读理解) | 理解一段文本并回答关于其内容的问题 (P, Q) → A | P=Tesla早年经历, Q="What language?", A="German" |
| Factoid QA (事实型问答) | 答案是简短的事实：人名、日期、数字、地点 | Q: "Capital of Canada?" → A: "Ottawa" |
| Open Domain QA (开放域问答) | 从大规模文档集合中检索+阅读来回答任意领域问题 | Wikipedia 全文搜索 + BERT 阅读 |
| Closed Domain QA (封闭域问答) | 在特定领域 (如医疗/法律) 的有限知识库中回答问题 | 医学问答系统只处理PubMed文献 |

### QA Architecture (问答架构)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Retriever-Reader Architecture (检索-阅读架构) | 两阶段：1)检索器从文档库找相关段落 2)阅读器从段落中提取答案 | Haystack 框架基于此架构 |
| DPR (Dense Passage Retrieval, 密集段落检索) | 双编码器架构：分别训练查询编码器和段落编码器，用嵌入相似度检索 | Q 编码器 + P 编码器 → 余弦相似度 → top-k |
| Haystack (问答框架) | deepset 开发的开源 QA 框架，抽象检索-阅读复杂性，与 Transformers 集成 | 核心组件: Document store + Pipeline |
| RAG (检索增强生成) | 超越抽取式 QA 的下一步：检索相关文档 + LLM 生成答案 | RAG = Retriever + Generator (W12详解) |

## 2. Comparisons (对比)

### BERT-base vs BERT-large

| Dimension (维度) | BERT-base | BERT-large | Example (示例) |
|-----------|-----------|------------|---------|
| Layers (层数) | 12 | 24 | 层数翻倍 |
| Hidden size (隐藏维度) | 768 | 1024 | 更宽的表示 |
| Attention heads (注意力头) | 12 | 16 | 更多关系模式 |
| Parameters (参数) | 110M | 340M | 3倍参数差 |
| 适用场景 | 平衡性能和效率 | 追求最高精度 | base已足够大部分任务 |

### BERT vs GPT

| Dimension (维度) | BERT | GPT | Example (示例) |
|-----------|------|-----|---------|
| Direction (方向) | ✅ 双向 (bidirectional) | 单向 (left→right) | BERT 同时看前后上下文 |
| Architecture (架构) | Encoder-only | Decoder-only | BERT 用 Encoder; GPT 用 Decoder |
| Pre-training (预训练) | MLM + NSP | Next Token Prediction | BERT 挖空填词; GPT 预测下一个 |
| Best for (适合) | 分类、NER、QA (理解任务) | 文本生成 (生成任务) | 理解用 BERT; 生成用 GPT |
| Input (输入) | [CLS] + text + [SEP] | 顺序 prompt | BERT 需要特殊 token |

### Pre-training vs Fine-tuning (预训练 vs 微调)

| Dimension (维度) | Pre-training (预训练) | Fine-tuning (微调) | Example (示例) |
|-----------|-------------|-------------|---------|
| Data (数据) | 海量无标注文本 | 少量任务特定标注数据 | Wikipedia 25亿词 vs 1000条标注情感 |
| Objective (目标) | MLM + NSP (通用语言理解) | 任务特定损失函数 | 掩码预测 vs 情感分类交叉熵 |
| Runs (执行次数) | 一次 (非常昂贵) | 每个任务一次 (便宜) | 预训练需TPU; 微调用单GPU |
| Weights (权重) | 从零开始学习 | 用预训练权重初始化 | 站在巨人(预训练)肩膀上 |

### Extractive vs Abstractive QA (抽取式 vs 生成式问答)

| Dimension (维度) | Extractive (抽取式) | Abstractive (生成式) | Example (示例) |
|-----------|-------------------|---------------------|---------|
| Answer source (答案来源) | 段落中的精确片段 | 生成新文本 | 抽取: 直接摘出; 生成: 重新组织 |
| Model (模型) | BERT / Encoder-only | GPT / Encoder-Decoder | BERT做抽取; T5做生成 |
| Evaluation (评估指标) | EM + F1 (token级别) | ROUGE / BLEU | EM=精确匹配; ROUGE=摘要 |
| Example (例子) | SQuAD 数据集 | 摘要式QA | Q→段落中提取 vs Q→生成新答案 |

### SQuAD Model Benchmarks (SQuAD 模型基准)

| Model (模型) | EM | F1 | Example (示例) |
|-------|------|------|---------|
| BiDAF | 67.7 | 77.3 | LSTM+注意力时代 (2016-2018) |
| BERT-base | 80.8 | 88.5 | Transformer 时代开始 |
| BERT-large | 84.1 | 90.9 | ⚠️ BERT在EM上超越人类! |
| Human (人类) | 82.3 | 91.2 | 但人类推理能力仍更强 |
| RoBERTa | 88.9 | 94.6 | BERT的优化版 |
| ALBERT | 89.3 | 94.8 | 参数共享的轻量BERT |

## 3. Formulas (公式)

### QA Evaluation Metrics (QA 评估指标)

| Metric (指标) | Formula (公式) | Description (说明) | Example (示例) |
|--------|---------|-------------|---------|
| EM (Exact Match, 精确匹配) | $\text{EM} = \mathbb{1}[\text{pred} = \text{truth}]$ | 严格二值：完全匹配=1，否则=0 | pred="2018", truth="2018" → EM=1 |
| F1 (Token-level) | $F_1 = \frac{2 \times P \times R}{P + R}$ | 精确率和召回率的调和平均 (部分得分) | pred和truth有5个重叠token → F1>0 |
| Precision (精确率) | $P = \frac{|\text{pred} \cap \text{truth}|}{|\text{pred}|}$ | 预测的 token 中有多少是正确的 | pred 4个词, 3个正确 → P=0.75 |
| Recall (召回率) | $R = \frac{|\text{pred} \cap \text{truth}|}{|\text{truth}|}$ | 正确答案的 token 中找到了多少 | truth 5个词, 找到3个 → R=0.6 |

### BERT Input Format (BERT 输入格式)

| Component (组件) | Description (说明) | Example (示例) |
|-----------|-------------|---------|
| [CLS] sent_A [SEP] sent_B [SEP] | BERT 标准输入格式 | [CLS] How old are you [SEP] I am 20 [SEP] |
| Token + Segment + Position Embedding | 三种嵌入相加得到最终输入表示 | 每个 token 同时有词义+句段+位置信息 |
| Segment A = 0, Segment B = 1 | 区分两个句子段 | 问题=Segment 0; 上下文=Segment 1 |

### BERT Pre-training Loss (预训练损失)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{MLM}} + \mathcal{L}_{\text{NSP}}$ | 总损失 = 掩码语言模型损失 + 下一句预测损失 | 两个任务联合训练 |

### Long Passage Handling (长文本处理)

| Parameter (参数) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| `max_length=512` | BERT 最大输入长度限制 | 超过512 token 必须截断或分段 |
| `truncation="only_second"` | 只截断上下文(第二个输入)，保留完整问题 | 问题短不截; 段落长截断 |
| `stride=25` | 滑动窗口步长，让长段落分块时有重叠 | 避免答案恰好在分割边界丢失 |

## 4. Practical / Lab (实战结论)

### 🔑 Key BERT Distinctions (关键BERT区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|-------------|--------|---------| 
| BERT 输入 = [CLS] + text_A + [SEP] + text_B + [SEP] | 固定格式；[CLS] 用于分类聚合 | `[CLS] How old are you [SEP] I am 20 [SEP]` |
| WordPiece 处理 OOV | "playing" → "play" + "##ing" (子词分词) | "unhappiness" → "un" + "##hap" + "##pi" + "##ness" |
| `padding=True, truncation=True` | 批处理时必须同时设置两者 | 长度5,8,12的句子 → 全部padding到12 |
| `num_labels=2` 在分类头 | 必须匹配任务的类别数 | 二分类情感→2; 5星评分→5 |
| `max_length=512` 是BERT硬限制 | 超过512 token 必须截断; 用 stride 处理长文本 | 1000词文档 → 只用前512 tokens |
| MLM 15% masking 的三种策略 | 80% [MASK] + 10% 随机词 + 10% 保持不变 → 防止模型只依赖 [MASK] | "store" → 80%→[MASK]; 10%→"running"; 10%→"store" |

### 📊 Lab 4 Conclusions (实验4结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| 微调 DistilBERT > TF-IDF + LogReg | 上下文嵌入优于词袋模型，特别是处理否定等语义 | "not bad" → DistilBERT正确; TF-IDF误判 |
| DistilBERT = 97% BERT, 40% 更小 | 部署首选，实用权衡最佳 | 66M vs 110M params; 推理快2倍 |
| 基线对比是**必须的** | 没有基线 → 无法声称改进 | 表格: TF-IDF 85% → DistilBERT 91% = +6% |
| 混淆矩阵揭示逐类弱点 | 不平衡类别 → 检查每类指标 | 总体 90% 但 neutral recall=20% |

### ⚠️ W10 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| Extractive QA 的答案可以不在段落中? | ❌ 答案**必须**在段落中! Abstractive QA 才是生成新文本 | BERT 提取 start/end 位置 → 段落子串 |
| BERT 可以做文本生成? | ❌ BERT 是 Encoder-only → 只做理解任务! 生成用 GPT (Decoder) | BERT→分类/NER/QA; GPT→文本生成 |
| EM=精确匹配 和 F1 含义一样? | ❌ EM=严格(0或1); F1=部分得分(token重叠) | pred:"November 2018"; truth:"2018" → EM=0, F1=0.5 |
| BERT 超越人类说明 AI 更聪明? | ❌ BERT 在 SQuAD EM超越人类，但人类推理能力仍更强 | BERT EM=84.1 vs Human EM=82.3 但trick questions仍失败 |
| BERT 可以处理任意长度文本? | ❌ 最大512 tokens! 长文本需要截断或滑动窗口(stride) | `max_length=512, stride=25` |
| MLM 只用 [MASK] 替换? | ❌ 80% [MASK] + 10% 随机词 + 10% 保持不变; 避免预训练-微调不匹配 | 微调时没有 [MASK] → 需要模型也能处理正常词 |
