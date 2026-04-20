# W10: BERT & Question Answering (BERT 与问答系统)

## 1. Definitions (定义)

### BERT Core Concepts (BERT 核心概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| BERT (双向编码器表示) | 来自 Transformer 的双向编码器表示 (Bidirectional Encoder Representations from Transformers)，只用 Encoder 实现真正的双向上下文理解 | 在 Wikipedia(25亿词) + BookCorpus(8亿词) 上预训练 |
| Transformer Encoder (Transformer 编码器) | Transformer 中负责编码输入的部分，使用自注意力 (Self-Attention) 让每个 token 看到所有前后文 | BERT 只用 Encoder (理解)；GPT 只用 Decoder (生成) |
| Bidirectional (双向) | BERT 的核心特性——每个 token 同时看到左边和右边所有上下文，不像 GPT 只能看左边 | "I went to the [MASK]" → 同时看 "went to" 和句末来猜 |
| BERT-base | 12 层 Transformer、768 隐藏维度、12 注意力头、110M (1.1亿) 参数的基础版本 | 适合大多数任务的标准配置 |
| BERT-large | 24 层 Transformer、1024 隐藏维度、16 注意力头、340M (3.4亿) 参数的大型版本 | SQuAD 2.0: F1=90.9, EM=84.1 |

### BERT Input & Output (BERT 输入输出)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| WordPiece (子词分词) | BERT 的分词算法，将罕见词拆成常见子词片段，词汇表大小约 30,500 | "embeddings" → ["em", "##bed", "##ding", "##s"] |
| [CLS] Token | 固定放在输入开头的特殊 token (ID=101)，其输出向量用作整个输入的浓缩表示，送入分类器 | 文本分类: [CLS] 输出 → 线性层 → 情感标签 |
| [SEP] Token | 分隔符 token (ID=102)，用于分隔句子对并在末尾标记输入结束 | QA输入: [CLS] Question [SEP] Passage [SEP] |
| [MASK] Token | 掩码 token (ID=103)，在 MLM 预训练中替代被遮住的词 | "went to the [MASK]" → 模型预测 "store" |
| [PAD] Token | 填充 token (ID=0)，将不同长度的输入填充到统一长度 | 短句填充到 max_length=512 |
| [UNK] Token | 未知词 token (ID=100)，表示词汇表中不存在的词 | 极罕见词 → [UNK] |
| Token Embedding (词嵌入) | BERT 三层嵌入之一——每个 token 的语义向量表示 | "cat" → 768维向量 |
| Segment Embedding (段落嵌入) | BERT 三层嵌入之一——区分 Sentence A 和 Sentence B 的标记 | Sentence A → 0; Sentence B → 1 |
| Position Embedding (位置嵌入) | BERT 三层嵌入之一——告诉模型每个 token 在序列中的位置 | 位置 0, 1, 2, ... → 对应位置向量 |

### BERT Training (BERT 训练)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Pre-training (预训练) | BERT 训练第一阶段——在大量无标注文本上学习通用语言知识，任务是 MLM + NSP | Wikipedia + BookCorpus → 通用理解 |
| Fine-tuning (微调) | BERT 训练第二阶段——在预训练模型上加小层，用少量标注数据适配特定任务 | 预训练 BERT + 情感标注数据 → 情感分类器 |
| MLM (掩码语言模型) | Masked Language Modelling——BERT 预训练任务之一，随机遮住 15% 词让模型预测 | 80% 替换 [MASK]、10% 随机词、10% 不变 |
| NSP (下一句预测) | Next Sentence Prediction——BERT 预训练任务之二，判断句子 B 是否是句子 A 的下一句 | A→B 连贯: IsNext ✅; 不连贯: NotNext ❌ |
| Transfer Learning (迁移学习) | 在大数据上学通用能力，再用小数据迁移到特定任务的训练范式，BERT 使其在 NLP 中普及 | 预训练一次 → 微调到 分类/QA/NER 等多任务 |
| Total Loss (总损失) | BERT 预训练的联合损失函数 = MLM 损失 + NSP 损失，两个任务同时训练 | Loss = L_MLM + L_NSP |

### BERT Variants (BERT 变体)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| DistilBERT (蒸馏BERT) | 通过知识蒸馏 (Knowledge Distillation) 压缩的 BERT，97% 性能 / 40% 更少内存 / 60% 更快 | 适合移动端和边缘设备部署 |
| BERT-Multilingual (多语言BERT) | 支持 104 种语言的 BERT 版本，结构与 BERT-base 相同 (12层, 768维, 110M参数) | 中/英/法/德/日 等跨语言任务 |
| Knowledge Distillation (知识蒸馏) | 让小模型 (学生) 模仿大模型 (老师) 的输出分布来学习，实现模型压缩 | DistilBERT 从 BERT 蒸馏而来 |

### Question Answering Concepts (问答系统概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Question Answering / QA (问答系统) | 自动回答用自然语言提出的问题的系统，按信息源/问题类型/答案类型分类 | Siri 回答"今天天气如何？" |
| Extractive QA (抽取式问答) | 答案直接从原文中**复制**一个连续文本片段 (span)，而非生成新文本 | 段落含 "German"，直接抽取 |
| Generative QA (生成式问答) | 模型用自己的语言**生成**答案，不限于原文片段——灵活但有幻觉风险 | GPT 组织语言回答 |
| Reading Comprehension (阅读理解) | 给定段落 P 和问题 Q，在 P 中找到答案 A 的任务；公式: (P, Q) → A | Q: "Tesla学了什么语言?" A: "German" |
| Factoid Question (事实型问题) | 有明确的简短事实答案（姓名/日期/数字/地点）的问题类型 | "法国首都是哪里？" → "巴黎" |
| Open Domain QA (开放域问答) | 问题可以涉及任意领域，需要先检索文档再找答案 | "黑洞是怎么形成的？" |
| Closed Domain QA (封闭域问答) | 问题限定在特定领域内，知识库范围有限 | 医疗客服: "这药副作用?" |
| Span (跨度/片段) | 抽取式 QA 中答案在段落中的连续 token 范围，由 start 和 end 位置定义 | 段落第 5 到第 8 个 token |

### QA Datasets & Evaluation (QA 数据集与评估)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| SQuAD (斯坦福问答数据集) | Stanford Question Answering Dataset——10万个 (段落,问题,答案) 三元组，答案是段落中的 span | 段落来自 Wikipedia，100-150 词 |
| EM / Exact Match (精确匹配) | 评估指标——预测答案与金标准完全一致为 1，否则为 0 (取多个gold中的最大值) | 预测"left Graz" vs gold"left Graz" → EM=1 |
| F1 Score (F1 分数) | 评估指标——基于 token 级别的 Precision 和 Recall 的调和平均，给部分匹配打分 | 预测含4/5个正确token → F1≈0.67 |
| Gold Answer (金标准答案) | 人工标注的正确答案，SQuAD 开发/测试集每题收集 3 个金标准用于评估 | {left Graz, left Graz ans, left Graz and severed...} |

### Neural QA Models (神经 QA 模型)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| BiDAF (双向注意力流) | Bidirectional Attention Flow——BERT 之前的 QA 模型，使用 Bi-LSTM + 注意力机制 | SQuAD: EM=71.3, F1=81.2 (远低于BERT) |
| Start/End Prediction (起止预测) | BERT 做 QA 的核心方法——用起始向量 S 和结束向量 E 分别预测答案 span 的开始和结束位置 | 对每个 token 做点积 + softmax → 最高分位置 |
| Sliding Window (滑动窗口) | 处理超过 BERT 512 token 限制的长段落的策略——将段落切成有重叠的窗口逐个输入 | stride=25 → 相邻窗口重叠25 tokens |

### Open Domain QA & Retrieval (开放域 QA 与检索)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Retriever-Reader Architecture (检索器-阅读器架构) | 开放域 QA 的两阶段架构——检索器先找相关文档，阅读器再从中提取答案 | 问题 → Retriever(找文档) → Reader(找答案) |
| DPR (密集段落检索) | Dense Passage Retrieval——用两个独立 BERT 编码器分别编码问题和段落，通过向量相似度检索 | 双编码器: Q-Encoder + P-Encoder → 点积匹配 |
| Dual Encoder (双编码器) | DPR 的核心架构——问题和段落各用一个独立的编码器生成向量，段落向量可离线预计算 | 问题编码器 + 段落编码器 → 分别训练 |
| Document Store (文档存储) | 存储预处理文档的数据库，支持检索器查询——可以是关系型/向量型/图数据库 | Elasticsearch, FAISS |
| Word2Vec | 2013 年提出的静态词嵌入方法，不考虑上下文，每个词只有一个固定向量 | "bank" (银行/河岸) → 同一个向量 |
| GloVe | 2014 年提出的基于共现矩阵的静态词嵌入方法，捕捉全局统计信息 | Global Vectors for Word Representation |
| Haystack (QA框架) | 由 deepset 开发的开源 QA 框架，基于检索器-阅读器架构，与 Transformers 紧密集成 | 核心: Document Store + Pipeline |
| DeepPavlov | 俄罗斯开发的开源对话 AI 和 QA 框架 | 类似 Haystack 的替代方案 |
| DrQA | Facebook 开发的开放域 QA 系统 | 基于 Wikipedia 的 QA |
| RAG (检索增强生成) | Retrieval-Augmented Generation——先检索再生成，是抽取式 QA 的进化方向 | 将在 Lecture 12 深入讲解 |

## 2. Comparisons (对比)

### BERT-base vs BERT-large (BERT 基础版 vs 大型版)

| Dimension (维度) | BERT-base | BERT-large | Example (示例) |
|-----------|-----------|------------|---------|
| Layers (层数) | 12 | 24 | 深度翻倍 |
| Hidden Size (隐藏维度) | 768 | 1024 | 更宽的表示 |
| Attention Heads (注意力头) | 12 | 16 | 更多并行注意力模式 |
| Parameters (参数量) | 110M (1.1亿) | 340M (3.4亿) | 约3倍差距 |
| SQuAD F1 | 88.5 | 90.9 | Large 只高 2.4 个点 |
| SQuAD EM | 80.8 | 84.1 | Large 只高 3.3 个点 |

### MLM vs NSP (BERT 两大预训练任务对比)

| Dimension (维度) | MLM (掩码语言模型) | NSP (下一句预测) | Example (示例) |
|-----------|-----|-----|---------|
| Goal (目标) | 学习**词级**上下文理解 | 学习**句子间**关系理解 | MLM: 猜被遮的词; NSP: 判断句子关系 |
| Input (输入) | 单个句子中 15% token 被处理 | 两个句子 A 和 B | [MASK] vs Sentence A + B |
| Output (输出) | 预测被遮 token 的原始词 | 二分类: IsNext / NotNext | "store" vs ✅/❌ |
| 解决什么? | 双向理解每个词的含义 | 理解段落、推理、问答等句间任务 | 词义消歧 vs 段落连贯性 |

### MLM 80/10/10 策略 (MLM Masking Strategy)

| Dimension (维度) | 80% → [MASK] | 10% → 随机词 | 10% → 不变 | Example (示例) |
|-----------|-------------|-------------|-----------|---------|
| 操作 | 替换为 [MASK] token | 替换为随机词 | 保持原词不动 | store→[MASK] / store→running / store→store |
| 目的 | 让模型学会预测被遮的词 | 避免训练-推理不匹配 | 让模型对所有位置保持警觉 | 微调时没有 [MASK] |

### Pre-training vs Fine-tuning (预训练 vs 微调)

| Dimension (维度) | Pre-training (预训练) | Fine-tuning (微调) | Example (示例) |
|-----------|------------|----------|---------| 
| Goal (目标) | 学习通用语言知识 | 适配特定下游任务 | 通识教育 vs 入职培训 |
| Data (数据) | 海量无标注文本 | 少量任务特定标注数据 | Wikipedia+BookCorpus vs SQuAD标注 |
| Cost (成本) | 极高 (Google 用 64 块 TPU) | 低 (普通 GPU 几小时) | 数百万美元 vs 数百美元 |
| Frequency (频率) | 做一次 | 每个任务做一次 | 训练BERT一次 → 微调到多任务 |
| Tasks (目标任务) | MLM + NSP | 分类/QA/NER 等 | 通用 → 特定 |

### SQuAD 2.0 Model Comparison (SQuAD 2.0 模型对比)

| Model (模型) | F1 | EM | Architecture (架构) | Example (示例) |
|-------|------|------|------|---------|
| BiDAF | 77.3 | 67.7 | Bi-LSTM + Attention | BERT 前最强 QA 模型 |
| BERT-base | 88.5 | 80.8 | Transformer Encoder (12层) | F1 比 BiDAF 高 11+ 点 |
| BERT-large | 90.9 | 84.1 | Transformer Encoder (24层) | 更大但仅略好于base |
| XLNet | 94.5 | 89.0 | Permutation LM | 排列组合预训练 |
| RoBERTa | 94.6 | 88.9 | Optimized BERT | 去掉NSP + 更多数据 |
| ALBERT | 94.8 | 89.3 | Parameter Sharing | 参数共享压缩 |

### Extractive QA vs Generative QA vs RAG (抽取式 vs 生成式 vs RAG)

| Dimension (维度) | Extractive QA (抽取式) | Generative QA (生成式) | RAG (检索增强) | Example (示例) |
|-----------|------------|------------|------|---------|
| Answer Source (答案来源) | 直接从原文复制 span | 模型自己组织语言 | 检索文档 + 生成 | 复制 vs 写 vs 查+写 |
| Accuracy (准确度) | ✅ 基于原文，可追溯 | ⚠️ 可能幻觉 | ✅ 基于文档，减少幻觉 | 有据可查 vs 编造风险 |
| Flexibility (灵活性) | ❌ 答案必须是原文子串 | ✅ 可综合多段信息 | ✅ 检索+综合 | span 限制 vs 自由生成 |
| Representative (代表) | BERT + SQuAD | GPT 系列 | LangChain + VectorDB | 见 W12 详解 RAG |

### EM vs F1 Evaluation Metrics (评估指标对比)

| Dimension (维度) | EM (精确匹配) | F1 Score (F1 分数) | Example (示例) |
|-----------|------|------|---------|
| 匹配方式 | 必须完全一致 | 允许部分匹配 | "left Graz" ≠ "left Graz and severed" (EM=0) |
| 取值 | 0 或 1 | 0 到 1 之间 | EM太严格; F1更宽容 |
| 计算基础 | 字符串完全匹配 | token 级别 Precision × Recall | 部分正确也有分 |
| 多个 gold | 取各 gold 比较的 max | 取各 gold 比较的 max | max{0.67, 0.67, 0.61} = 0.67 |

### Sparse vs Dense Retrieval (稀疏检索 vs 密集检索)

| Dimension (维度) | Sparse (TF-IDF/BM25) | Dense (DPR/BERT) | Example (示例) |
|-----------|------|------|---------|
| 匹配方式 | 关键词重叠 (词汇匹配) | 向量相似度 (语义匹配) | 靠共同词 vs 靠含义 |
| 同义词处理 | ❌ 不同词 = 不匹配 | ✅ 语义相近 = 匹配 | "car"≠"automobile" vs 语义相近 |
| 计算方式 | 倒排索引查找 | 向量空间余弦相似度 | 精确查找 vs 最近邻搜索 |
| 段落预计算 | 不需要 | ✅ 向量可离线预计算 | DPR: 段落向量存入向量DB |

## 3. Formulas (公式)

### Reading Comprehension (阅读理解公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| (P, Q) → A | 阅读理解核心公式：给定段落 P 和问题 Q，输出答案 A (A 是 P 中的 span) | P="Tesla studied German..." Q="What language?" → A="German" |
| C = (c₁, ..., cₙ), Q = (q₁, ..., qₘ) | 段落和问题的 token 序列表示，其中 M < N | 段落通常比问题长得多 |
| Input Embedding = Token + Segment + Position | BERT 的三层嵌入叠加构成最终输入表示 | 词义 + 句子归属 + 位置信息 |
| Total Loss = L_MLM + L_NSP | BERT 预训练总损失 = 掩码语言模型损失 + 下一句预测损失 | 两个任务同时训练 |

### Evaluation Metrics (评估指标公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| EM = max{match(pred, gold_i)} for i=1..k | 精确匹配：预测与每个 gold 比较，取最大值 (0 或 1) | pred="left Graz and severed" vs 3个gold → max{0,0,0}=0 |
| F1 = max{F1(pred, gold_i)} for i=1..k | F1 分数：与每个 gold 的 token 级别 F1，取最大值 | max{0.67, 0.67, 0.61} = 0.67 |
| Precision = \|pred ∩ gold\| / \|pred\| | token 级别精确率：预测中有多少是正确的 | 预测5 token中4个正确 → P=0.8 |
| Recall = \|pred ∩ gold\| / \|gold\| | token 级别召回率：正确答案中有多少被预测到 | 正确6 token中4个被找到 → R=0.67 |
| F1 = 2 × P × R / (P + R) | F1 是 Precision 和 Recall 的调和平均 | P=0.8, R=0.67 → F1≈0.73 |

### BERT QA Sliding Window Parameters (BERT QA 滑动窗口参数)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| max_length = 500 | 问题 + 段落共享的最大 token 数 (给问题留空间) | BERT 限制 512，留 12 给特殊 token |
| truncation = "only_second" | 只截断段落 (context)，永远不截断问题 (question) | 问题短且完整很关键 |
| stride = 25 | 相邻滑动窗口重叠的 token 数，防止答案被截断 | 窗口1: [0, 500], 窗口2: [475, 975] |

## 4. Practical / Lab (实战结论)

### 📊 Key Technical Conclusions (关键技术结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| BERT QA 本质是指针问题 | 不生成答案，只预测答案在段落中的 start 和 end 位置 | 对每个 token 做点积+softmax → 最高分 = 答案边界 |
| 滑动窗口 stride 影响准确率 | stride 太大可能截断答案; 太小增加计算量; stride=25 是常用值 | stride=25: 重叠25 tokens 确保答案不丢失 |
| DPR 段落向量可离线预计算 | 查询时只需编码问题 + 最近邻搜索，大幅提升检索速度 | 百万级文档 → 预编码 → 毫秒级检索 |
| BERT 比 BiDAF F1 提升 11+ 点 | 从 77.3 → 88.5 (base) / 90.9 (large)，是 QA 领域的巨大飞跃 | Transformer 取代 LSTM 的标志性结果 |
| MLM 的 80/10/10 不是随意设定 | 100% [MASK] 会导致训练-推理不匹配; 10%随机+10%不变让模型保持警觉 | 微调时没有 [MASK] → 需要预训练也见过"正常"token |
| NSP 对句间关系任务有帮助 | QA、自然语言推理等任务需要理解两个句子的逻辑关系 | "这个段落包含答案吗？" 需要 NSP 能力 |

_No lab code for this week._

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| BERT 是双向的 = Bi-LSTM? | ❌ 完全不同! Bi-LSTM 两方向独立处理再合并; BERT 用自注意力让每个 token 真正同时看到所有前后文 | Bi-LSTM: 两个单向拼接; BERT: 全局注意力 |
| BERT 能生成文本? | ❌ BERT 只用 Encoder，擅长理解 (分类/QA)，不能像 GPT 那样自回归生成文本 | 生成用 GPT (Decoder); 理解用 BERT (Encoder) |
| MLM 15% 都替换为 [MASK]? | ❌ 只有 80% 变 [MASK]，10% 变随机词，10% 保持不变——为了避免训练-推理不匹配 | 100% [MASK] → 微调时模型从没见过正常 token |
| [CLS] token 只用于分类? | ❌ [CLS] 是整个输入的浓缩表示，用于分类/QA 的起始信号; 但 QA 中 start/end 预测用的是段落 token 的输出 | 分类: [CLS]输出; QA: 段落各token输出 |
| SQuAD 答案可以不在段落中? | ❌ SQuAD 是抽取式数据集，答案必须是段落中的一个连续 span，不能在段落外 | 答案 = 段落[start:end]，不能生成新文本 |
| EM=0 意味着完全错误? | ❌ EM=0 只说明不是完全匹配; F1 可能很高 (如 0.67)，说明大部分内容是正确的 | pred="left Graz and severed" → EM=0 但 F1=0.67 |
| BERT 能处理任意长文本? | ❌ BERT 最大输入 512 tokens! 超过需要用滑动窗口策略切分成多个窗口分别输入 | 1000 词文档 → 需要切成多个 500 token 窗口 |
| DistilBERT 性能差很多? | ❌ DistilBERT 保留了 BERT 97% 的性能，但内存减少 40%、速度快 60%——牺牲极小 | 3% 性能换 40% 内存 + 60% 速度 = 值得 |
| DPR 用一个编码器同时编码问题和段落? | ❌ DPR 用**两个独立的**编码器，分别编码问题和段落——双编码器架构 | Q-Encoder ≠ P-Encoder，各自独立训练 |
| 开放域 QA 只需要一个 Reader? | ❌ 开放域 QA 需要 Retriever + Reader 两阶段——先检索候选文档，再从中提取答案 | 没有 Retriever → 不知道去哪找答案 |
| BERT 预训练 = 微调? | ❌ 预训练: 大量无标注数据学通用知识(昂贵); 微调: 少量标注数据适配特定任务(便宜) | 预训练一次(TPU集群) → 微调多次(普通GPU) |
