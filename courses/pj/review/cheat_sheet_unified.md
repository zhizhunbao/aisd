# W1: LLM Evaluation Principles — Observability & Instrumentation (LLM 评估原则——可观测性与插桩)

## 1. Definitions (定义)

### Observability & Telemetry (可观测性与遥测)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Observability (可观测性) | 通过系统发出的外部信号来诊断内部行为的能力 (ability to diagnose internal behavior from external signals)，无需打开黑箱 | 通过追踪 LLM 请求发现某个 prompt 导致高延迟 |
| Telemetry (遥测) | 系统运行时自动发出的行为数据 (data emitted from a system about its behavior)，包括 Spans/Traces/Metrics/Logs 四类信号 | OpenTelemetry 采集 token 使用量 |
| Span (跨度) | 遥测数据的基本单位，代表一次请求中的单个操作，包含 Name/ParentID/Timestamps/Attributes/Events 等字段 | LLM 调用耗时 234ms 的一条 Span 记录 |
| Trace (追踪) | 一个请求在整个应用中的完整路径，由多个 Span 组成 (path of a request through the application) | AI Agent 计算斐波那契：规划→执行→验证的完整链路 |
| OpenTelemetry (开放遥测) | 开源行业标准的可观测性工具框架 (open source industry standard for instrumenting observability) | 用 `@autotrace` 装饰器自动追踪 LLM 调用 |
| Monitoring (传统监控) | 只能查看预定义指标的被动方式 (passive checking of pre-defined metrics)，无法探索未知问题 | 查看 CPU 使用率、内存占用等固定 dashboard |

### Instrumentation Methods (插桩方法)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| SDK-based Instrumentation (基于 SDK 的插桩) | 开发者手动用装饰器/包装器追踪函数调用 (manually wrap functions using vendor-specific SDK)，粒度最高但代码侵入大 | LangSmith, Langfuse, MLflow |
| Auto-Instrumentation / OTel (自动插桩) | 运行时通过 Monkey-patch 替换标准库函数来自动发出追踪 (replace original function with wrapped function at runtime)，代码改动最少 | OpenLLMetry, Arize Phoenix, OpenLIT |
| Proxy-based Instrumentation (基于代理的插桩) | 应用通过中间件代理路由 LLM 请求，零代码改动但只能看到输入输出 (zero overhead, language agnostic, black-box) | Helicone, MLflow AI Gateway |

## 2. Comparisons (对比)

### Instrumentation Methods (三种插桩方法对比)

| Dimension (维度) | SDK-based | Auto-Instrumentation (OTel) | Proxy-based | Example (示例) |
|-----------|---|---|---|---------| 
| 代码侵入 (Code Intrusion) | 高 | 最小（一行初始化） | 零 | OTel 只需 `@autotrace` |
| 粒度 (Granularity) | 最高 | 中等 | 低（只看输入/输出） | SDK 可捕获自定义中间步骤 |
| 厂商锁定 (Vendor Lock-in) | 高 | 低（标准化） | 低 | OTel 可切换后端 |
| 代表工具 (Tools) | LangSmith, Langfuse | OpenLLMetry, Phoenix | Helicone | — |

### Observability vs Monitoring (可观测性 vs 传统监控)

| Dimension (维度) | Monitoring (传统监控) | Observability (可观测性) | Example (示例) |
|-----------|---|---|---------| 
| 问题类型 | 只能回答已知问题 | 可以探索**未知问题** | Monitoring: "CPU 多少？" vs Observability: "为什么 GPT-4 突然慢了？" |
| 指标范围 | 预定义指标（CPU/内存） | 任何维度的数据信号 | 固定 dashboard vs 灵活查询 |
| 适用场景 | 传统 IT 系统 | LLM/AI 应用（行为不可预测） | LLM 输出随机性→需要 Observability |

## 3. Formulas (公式)

_本周无计算公式。_

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| OpenTelemetry Hello World 练习验证了 Span 追踪的完整流程 | 通过 `TracerProvider` + `ConsoleSpanExporter` + `tracer.start_as_current_span()` 可以手动创建嵌套 Span 并输出到控制台 | `say_hello` → `format` → `println` 三层嵌套 Span |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 混淆 Observability 和 Monitoring (传统监控) | Monitoring 只能看预定义指标（CPU/内存）；**Observability 可以问任何问题** 来探索未知问题 | Observability 能回答"为什么 GPT-4 在周二突然变慢了？" |
| 自动插桩 (OTel) = 完全不用写代码 | OTel 仍需一行初始化代码 (`@autotrace`)，且**可能与其他 monkey-patch 库冲突** | OpenLLMetry 与某些自定义中间件冲突 |

# W2: LLM Evaluation Frameworks — G-Eval, RAGAS, DeepEval, DAG Eval (LLM 评估框架——G-Eval、RAGAS、DeepEval、DAG Eval)

## 1. Definitions (定义)

### Evaluation Paradigms (评估范式)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Reference-Based Evaluation (基于参考的评估) | 将模型输出与标准答案对比来评分的评估方式 (compare output against ground truth) | ROUGE, BLEU, METEOR, BERTScore |
| Reference-Free Evaluation (无参考评估) | 无需标准答案，用 LLM 自身判断输出质量 (evaluate without ground truth) | LLM-as-a-Judge, G-Eval |
| LLM-as-a-Judge (LLM 充当评委) | 用一个 LLM 来评价另一个 LLM 的输出质量 (use LLM to score LLM outputs)，支持单独评分和成对比较 | GPT-4 给 ChatGPT 的回答打 1-5 分 |

### Evaluation Frameworks (评估框架)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| G-Eval (G 评估框架) | 结合自动 Chain-of-Thought (CoT) 推理和概率加权评分的评估框架 (Automatic CoT Reasoning + Probability-Weighted Scoring)，与人类评分对齐更好 | G-Eval Spearman 相关性 0.514 vs ROUGE 约 0.3-0.4 |
| RAGAS (Retrieval Augmented Generation Assessment / 检索增强生成评估) | 专门评估 RAG (Retrieval Augmented Generation) 系统的框架，提供 Faithfulness/Answer Relevance/Context Relevance 三大指标 | 用 RAGAS 评估一个 RAG 问答系统的幻觉程度 |
| DeepEval (深度评估) | 基于 G-Eval 构建的开源评估框架，30+ 即插即用指标 (plug-and-use LLM-evaluated metrics)，支持 RAG/Agent/Chatbot 评估 | 用 DeepEval 自动评估 RAG pipeline 的忠实度 |
| DAG Eval (Directed Acyclic Graph Evaluation / 有向无环图评估) | 用结构化决策树（而非单一 prompt）进行评估的方法 (structured decision-tree approach)，确定性更高、可审计 | 检查摘要是否包含 intro/body/conclusion 三个标题 |

### RAGAS Metrics (RAGAS 指标)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Faithfulness (忠实度) | 衡量生成答案中的声明是否能被检索到的上下文支持 (whether claims in answer can be supported by retrieved context)，直接衡量幻觉程度，$F = V/S$ | 答案有 5 条声明，4 条能在上下文中找到依据 → F = 0.8 |
| Answer Relevance (答案相关性) | 衡量生成的回答是否直接回应原始问题 (whether response directly addresses the question)，$AR = \frac{1}{n}\sum sim(q, q_i)$ | 问"如何安装 Docker"，回答讲了 Docker 安装步骤 → AR 高 |
| Context Relevance (上下文相关性) | 衡量检索到的上下文与原始问题的相关程度 (how relevant the context is)，$CR = E/S$ | 检索到 10 句话，其中 7 句与问题相关 → CR = 0.7 |

## 2. Comparisons (对比)

### G-Eval vs DAG Eval (G-Eval 对比 DAG Eval)

| Dimension (维度) | G-Eval | DAG Eval | Example (示例) |
|-----------|---|---|---------| 
| 评估方式 (Approach) | 单个 prompt 一次性评分 | 决策树逐节点判断 | G-Eval: "请打分 1-10"; DAG: "先检查结构→再评分" |
| 确定性 (Determinism) | 低（依赖 LLM 随机性） | 高（结构化路径） | 同一输入 G-Eval 可能打 7 或 8，DAG 固定输出 |
| 透明度 (Transparency) | 中等（不知为何打这个分） | 高（每步可追踪） | DAG 可以看到在哪一步扣分 |
| 适用场景 (Use Case) | 主观评估（流畅性、创意性） | 结构化评估（JSON Schema 检查） | G-Eval 评风格，DAG 评格式 |

### Reference-Based vs Reference-Free (基于参考 vs 无参考评估)

| Dimension (维度) | Reference-Based (基于参考) | Reference-Free (无参考) | Example (示例) |
|-----------|---|---|---------| 
| 需要标准答案 | ✅ 是 | ❌ 否 | BLEU 需要参考翻译，G-Eval 不需要 |
| 评估依据 | 与参考答案的文本重叠度 | LLM 自身的判断力 | n-gram 匹配 vs 语义理解 |
| 与人类对齐 | ⚠️ 中等 | ✅ G-Eval 更好 | G-Eval Spearman 0.514 vs ROUGE ~0.3 |
| 代表方法 | ROUGE, BLEU, METEOR | G-Eval, LLM-as-a-Judge | — |

## 3. Formulas (公式)

### G-Eval & RAGAS 公式

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $score = \sum_{i=1}^{n} p(s_i) \cdot s_i$ | G-Eval 概率加权评分：对每个可能分数 $s_i$ 乘以 LLM 生成该分数的概率 $p(s_i)$，求和得到最终分数 | 分数 3 概率 0.1，分数 4 概率 0.7，分数 5 概率 0.2 → score = 0.3+2.8+1.0 = 4.1 |
| $F = V / S$ | Faithfulness：$V$ = 被上下文验证的声明数，$S$ = 总声明数 | 5 条声明中 4 条有据 → F = 0.8 |
| $AR = \frac{1}{n} \sum_{i=1}^{n} sim(q, q_i)$ | Answer Relevance：生成 n 个反向问题 $q_i$，计算与原问题 $q$ 的平均余弦相似度 | 3 个反向问题与原问题相似度 0.9, 0.85, 0.8 → AR = 0.85 |
| $CR = E / S$ | Context Relevance：$E$ = 从上下文中提取的与问题相关的句子数，$S$ = 上下文总句子数 | 10 句中 7 句相关 → CR = 0.7 |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| RAGAS 评估只需 4 行代码即可运行 | `from ragas import evaluate` + 准备 question/answer/contexts/ground_truths 字典 + 调用 `evaluate()` | 评估 RAG pipeline 的 faithfulness/answer_relevancy 指标 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 以为 G-Eval 只是简单的 LLM 打分 | G-Eval 有两个创新：①自动生成评估步骤（CoT）②概率加权评分（用 logprobs 而非简单文本输出） | G-Eval 对人类相关性 0.514 远高于 ROUGE 的 0.3 |
| 以为 RAGAS 的 Faithfulness 衡量的是"答案是否正确" | Faithfulness 衡量的是**答案中的声明是否能被检索到的上下文支持**，不管答案绝对正确与否 | 上下文本身有错误信息，忠实度仍可以很高（因为答案忠实于上下文） |
| DAG Eval 和 G-Eval 只能二选一 | 两者可以**混合使用**——在 DAG 中嵌入 G-Eval 节点，结构化检查用 DAG，主观质量评估用 G-Eval | `BinaryJudgementNode(...)` + `GEvalNode(criteria="流畅性")` |
| 以为 Reference-Based 指标足够评估 LLM | ROUGE/BLEU 只衡量**文本重叠**，无法理解语义——G-Eval 等 Reference-Free 方法与人类判断对齐更好 | 同义改写得 ROUGE 分低但实际质量高 |

# W3: Feature Engineering (特征工程)

## 1. Definitions (定义)

### Feature Engineering Core (特征工程核心概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Feature Engineering (特征工程) | 从原始数据中分离信号与噪声的过程 (separating Signals from Noise)，将脏数据转化为 ML 模型可用的高质量特征 | 年龄/收入/品牌名等原始数据 → 清洗/缩放/编码后的特征矩阵 |
| Feature (特征) | ML 模型的输入变量，相当于信号 (Features are Signals)，传统 ML 需要人工设计，深度学习可自动学习 | 用户年龄、购买频率、IP 地址嵌入向量 |

### Missing Values (缺失值处理)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| MCAR (完全随机缺失) | 缺失与任何变量都无关，纯随机误差 (Missing Completely at Random)，是最不严重的类型，不引入偏差 | 问卷因印刷错误漏了一题 |
| MAR (随机缺失) | 缺失与其他已观测变量有关，但与缺失值本身无关 (Missing at Random)，可用统计方法纠正 | 年轻人更不愿填收入——缺失与年龄有关，但与收入本身无关 |
| MNAR (非随机缺失) | 缺失与缺失值本身有关 (Missing Not at Random)，是最严重的类型，引入系统性偏差 | 重度抑郁者不愿回答心理健康问题——越严重越不填 |
| Deletion (删除法) | 通过删除缺失数据来处理，包括行删除和列删除 (Column/Row Deletion)，简单但可能丢失信息 | 某列 80% 缺失 → 删除整列 |
| Imputation (插补法) | 用估计值填充缺失数据 (fill missing with estimated values)，包括 Mean/Median/Mode/KNN，但可能引入偏差或数据泄漏 | 用训练集均值填充缺失的年龄字段 |

### Feature Scaling & Transformation (特征缩放与变换)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Min-Max Normalization (最小最大归一化) | 将特征缩放到 [0,1] 范围，公式 $x' = \frac{x - min(x)}{max(x) - min(x)}$，对离群值敏感 | 年龄 25-65 → 缩放到 0-1 |
| Box-Cox Transformation (Box-Cox 变换) | 将非正态分布的特征变换为近似正态分布 (transform to Normal distribution)，$x' = (x^a - 1)/a$ 当 $a≠0$；$x' = \log(x)$ 当 $a=0$ | 右偏的收入分布 → 变换后接近正态 |
| Discretization / Binning (离散化/分箱) | 将连续特征转换为离散类别 (converting continuous to discrete)，也称 Quantization，需谨慎选择边界 | 年龄 → 0-10/10-18/18-30/30-50/50-65 年龄段 |

### Encoding & Embeddings (编码与嵌入)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Embedding (嵌入) | 将类别变量映射为低维稠密向量 (numerical vector representation of categorical variable)，保留语义关系，维度可控 | "king" → [0.2, 0.8, -0.1, ...] 50 维向量 |
| Word2Vec | 通过预测上下文窗口中相邻词来学习词嵌入的方法 (predict neighboring words in context window) | 单词级嵌入，语义相近的词向量距离近 |
| GloVe | 通过全局共现矩阵分解来学习词嵌入的方法 (global co-occurrence matrix factorization) | 单词级嵌入，捕获全局统计关系 |
| Sentence Transformers (句子变换器) | 用 Transformer 编码整个句子为单一向量的嵌入方法 (Transformer encoding full sentences) | 句子/段落级嵌入 |

### Data Leakage (数据泄漏)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Data Leakage (数据泄漏) | 训练时使用了预测时不应拥有的信息 (using information not expected to be available during prediction)，导致模型指标虚高 | 模型准确率 99%+ → 先查泄漏再庆祝 |
| Feature Leakage (特征泄漏) | 某个特征是目标变量的副本或代理 (feature is duplicate/proxy of target) | 用月薪预测年薪——月薪×12=年薪 |
| Sample Leakage (样本泄漏) | 训练集和测试集之间存在重复样本 (duplicate samples between train and test) | 同一张 CT 图出现在 train 和 test |
| Non-IID Leakage (非 IID 泄漏) | 时序数据被随机拆分导致未来信息泄入过去 (splitting time series randomly) | 用周五的股价"预测"周三的价格 |

### Feature Selection & Importance (特征选择与重要性)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| SHAP (Shapley 加法解释) | 借鉴合作博弈论中的 Shapley 值，通过扰动特征并测量预测变化来公平衡量每个特征的贡献 (average marginal contribution of a feature to overall model score) | Global SHAP bar plot 显示"年收入"是最重要特征 |
| Feature Coverage (特征覆盖率) | 该特征在多大比例的数据中有值 (proportion of data having value for this feature)，覆盖率低则泛化差 | "VIP 等级"只有 5% 用户有值 → 覆盖率太低 |

## 2. Comparisons (对比)

### 传统 ML vs 深度学习 (对特征工程的依赖)

| Dimension (维度) | Traditional ML (传统 ML) | Deep Learning (深度学习) | Example (示例) |
|-----------|---|---|---------| 
| 特征来源 | 人工设计 (Manual) | 模型自动学习 (Auto-learned) | SVM 需手工特征 vs CNN 自动提取图像特征 |
| 对特征工程的依赖 | ⭐⭐⭐⭐⭐ 极度依赖 | ⭐⭐ 较少（但数据清洗仍不可少） | RF 需要大量特征工程；Transformer 只需 tokenize |

### 删除法 vs 插补法 (处理缺失值)

| Dimension (维度) | Deletion (删除法) | Imputation (插补法) | Example (示例) |
|-----------|---|---|---------| 
| 做法 | 删除含缺失值的行/列 | 用估计值填充缺失值 | 列删除整列 vs 用均值填充 |
| 优点 | 简单、不引入假数据 | 保留更多数据 | — |
| 缺点 | 数据量减少→准确性降低 | 可能引入偏差、可能导致数据泄漏 | 均值插补会压缩方差 |

### One-Hot vs Embeddings (类别编码)

| Dimension (维度) | One-Hot Encoding | Embeddings (嵌入) | Example (示例) |
|-----------|---|---|---------| 
| 维度 (Dimensionality) | 类别数 = 维度数，高基数爆炸 | 固定低维（50-300 维），不随类别数增长 | 1000 品牌 → 1000 维 vs 50 维 |
| 语义关系 | ❌ 不保留（每个类别独立） | ✅ 语义相似的向量距离近 | "苹果"和"梨"的嵌入向量相近 |
| 新值处理 | ❌ 无法处理未见过的值 | ✅ 通过语义相似性处理 | 新品牌用已有近似品牌的向量 |

### SHAP 的两种用法 (全局 vs 单次预测)

| Dimension (维度) | Global Feature Importance (全局重要性) | Single Prediction Importance (单次预测) | Example (示例) |
|-----------|---|---|---------| 
| 问题 | 哪些特征整体上对模型最重要？ | 对于这一个预测，哪些特征推高/推低了结果？ | Bar plot 排序 vs Waterfall/Force plot |
| 粒度 | 宏观统计 | 微观解释 | "年龄整体排第2" vs "这个用户年龄=65 推高了流失概率" |

## 3. Formulas (公式)

### 特征缩放公式

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $x' = \frac{x - min(x)}{max(x) - min(x)}$ | Min-Max 归一化：将特征缩放到 [0,1] 范围 | 年龄 25, min=18, max=65 → $x' = 7/47 ≈ 0.15$ |
| $x' = (x^a - 1)/a$（$a≠0$）或 $\log(x)$（$a=0$） | Box-Cox 变换：自动找最佳 $a$ 值将偏态分布"拉"成正态 | 右偏收入分布 → 取 log 后接近正态 |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| SHAP 可同时进行全局和单次预测解释 | Google Colab 练习用 Credit Risk Score 数据集演示 SHAP 的全局 bar plot 和单次预测 waterfall plot | 发现"credit_history"在信用评分模型中全局最重要 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 在 train/test 拆分**之前**做插补/缩放 | 所有预处理必须在拆分**之后**做！黄金法则："**先拆分，后处理**"(Split first, process later) | 用全部数据的均值填缺失值 → 测试集信息泄入训练集 |
| 以为插补法不会有风险 | 插补可能导致 **数据泄漏** (Data Leakage)、偏差，且不同方法适用于不同缺失机制 | 用全局均值填 MNAR 型缺失 → 引入系统性偏差 |
| 以为过采样可以在拆分前做 | 过采样 (Oversampling) 必须在拆分**之后**做，否则重复样本跨越 train/test 导致样本泄漏 | 拆分前 SMOTE → test 集出现 train 集的合成近邻 |
| 以为特征越多模型越好 | 特征过多的四大危害：**过拟合 + 泄漏风险 + 内存消耗 + 推理延迟增加** | 100 个特征 vs 精选 20 个 → 后者性能可能更好 |
| SHAP 值高 = 特征一定好 | SHAP 只衡量对模型的重要性，不衡量**泛化能力**——需要同时检查特征覆盖率和分布一致性 | 训练集上 SHAP 很高的特征在新数据上覆盖率仅 5% |
| 缩放时使用全部数据的统计量 | 必须**仅用 train 的统计量**（mean/min/max）来缩放和处理数据 | 用 test + train 的 min/max 做 Min-Max → 信息泄漏 |

# W4: Algorithm Selection, Distributed Training & AutoML (算法选择、分布式训练与 AutoML)

## 1. Definitions (定义)

### Algorithm Selection (算法选择)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Six Rules for Algorithm Selection (六条军规) | 工业界选择 ML 算法的六条实战原则 (practical rules for choosing ML algorithms)：不追 SOTA、从简入手、看学习曲线、评权衡、查假设、用速查表 | 先 Logistic Regression → XGBoost → DNN 逐步升级 |
| SOTA (State-of-the-Art) | 学术基准上的最佳模型 (best model on academic benchmarks)，但不一定适合你的数据、成本高、延迟大 | GPT-4 在 ImageNet 最强，但你的 10MB 表格数据用不着 |
| Model Assumptions (模型假设) | 每个算法隐含的数学假设 (implicit mathematical assumptions)，违反假设→模型静默失败且不报错 | 线性回归假设正态性，朴素贝叶斯假设条件独立 |
| Learning Curve (学习曲线) | 在不同数据量下评估模型性能随训练的变化 (performance vs training samples/epochs)，用于判断过拟合/欠拟合 | 训练误差低但验证误差高 → 过拟合 |

### Distributed Training (分布式训练)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Gradient Checkpointing (梯度检查点) | 前向传播时只保存 √N 个检查点而非所有中间激活值，反向传播时重新计算 (trade 20% compute for 10x memory)，单机内存优化技巧 | 100 层网络只存 10 个检查点 |
| Data Parallelism (数据并行) | 训练数据分片到多台机器，每台持有完整模型副本，各自计算梯度后汇总 (split data, replicate model) | 8 个 GPU 各跑 1/8 的 batch，最后 AllReduce 梯度 |
| Model Parallelism (模型并行) | 模型太大放不下单机，将不同层放在不同机器上 (split model across machines) | 大模型的前 20 层在 GPU 0，后 20 层在 GPU 1 |
| Pipeline Parallelism (流水线并行) | 模型并行 + 微批次交错执行 (model parallel + micro-batch interleaving)，消除机器间的空闲等待"气泡" | Llama 2 70B 训练使用的策略 |
| Straggler Problem (落后者问题) | 同步模式下最慢的机器拖慢全局的问题 (slowest worker blocks all) | 8 台 GPU 中 1 台有硬件故障，其余 7 台空等 |
| Gradient Staleness (梯度过时) | 异步模式下旧梯度更新新权重的问题 (outdated gradient updating newest weights) | Worker A 用 5 步前的旧模型计算的梯度去更新当前模型 |
| DDP (分布式数据并行) | PyTorch DistributedDataParallel，每个 Worker 持有完整模型副本，All-Reduce 汇总梯度 | 模型 < 单卡显存 → 用 DDP |
| FSDP (全分片数据并行) | PyTorch FullyShardedDataParallel，参数/优化器/梯度在 GPU 间分片存储 (shard parameters across GPUs)，极高内存效率 | 模型 > 单卡显存 → 用 FSDP |

### AutoML (自动机器学习)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Soft AutoML (软 AutoML) | 自动化超参数调优 (automated hyperparameter tuning)：Grid Search / Random Search / Bayesian Optimization | 自动搜索学习率、BatchSize、层数的最优组合 |
| Hard AutoML / NAS (硬 AutoML / 神经架构搜索) | 自动设计神经网络架构 (automated network architecture design)，包含搜索空间、搜索策略、性能估计三大组件 | NASNet 在 ImageNet 上击败人工设计的模型 |
| Grid Search (网格搜索) | 穷举所有超参数组合 (exhaustive search over all combinations)，保证最优但维度灾难 | 3 个学习率 × 3 个 batch size = 9 次试验 |
| Random Search (随机搜索) | 随机采样超参数组合 (random sampling of parameter space)，高维空间效率更高但不保证最优 | 随机尝试 20 组参数 |
| Bayesian Optimization (贝叶斯优化) | 用概率模型（代理模型）预测下一个最优采样点 (surrogate model predicts next best point)，样本效率最高 | Bayesian 用 10 次试验就找到接近最优的学习率 |
| NAS Search Space (NAS/Neural Architecture Search 搜索空间) | 定义可选的"积木块" (defines available building blocks)：3×3 Conv、Pooling、Skip Connection 等 | 卷积核大小、跳跃连接类型 |
| NAS Search Strategy (NAS/Neural Architecture Search 搜索策略) | 如何组合积木块的方法 (how to combine building blocks)，需要平衡探索 vs 利用 | RL、进化算法、可微分方法 |
| NASNet | 基于 RL 的 NAS 方法的代表成果 (RL-Based NAS)，Controller (RNN) 提出架构→训练→评估→反馈，击败人工设计模型 | ImageNet SOTA 由 NASNet 自动发现 |
| AmoebaNet | 基于进化算法的 NAS 成果 (Evolutionary NAS)，通过变异-淘汰发现人类直觉从未考虑的高性能架构 | 随机初始化种群→淘汰差的→变异好的→重复 |
| DARTS (Differentiable Architecture Search / 可微分架构搜索) | 将离散架构选择转化为连续优化问题 (differentiable NAS)，用 Supernet + 梯度下降同时优化架构权重 α 和模型参数 w，搜索效率提升 1000 倍 | 数千 GPU 小时 → 几小时 |

## 2. Comparisons (对比)

### 同步 vs 异步数据并行 (梯度汇总模式)

| Dimension (维度) | Synchronous (同步) | Asynchronous (异步) | Example (示例) |
|-----------|---|---|---------| 
| 工作方式 | 等所有 Worker 算完，统一汇总 | 不等待，谁算完谁更新 | 全班一起交作业 vs 谁写完谁交 |
| 致命问题 | **Straggler** (最慢的拖全局) | **Gradient Staleness** (旧梯度更新新权重) | 1 台慢 GPU 拖慢 7 台 vs 用 5 步前的梯度 |
| 解决方案 | 负载均衡、动态资源分配 | 参数稀疏时问题自动缓解 | — |

### DDP vs FSDP (PyTorch 分布式 API)

| Dimension (维度) | DDP | FSDP | Example (示例) |
|-----------|---|---|---------| 
| 模型存储 | 每个 Worker 持有**完整模型副本** | 参数/优化器/梯度在 GPU 间**分片** | 每人一本完整教材 vs 教材拆成章节分着拿 |
| 内存效率 | ⚠️ 冗余存储 | ✅ 极高 | — |
| 适用场景 | 模型**放得进**单卡 | 模型**放不进**单卡 | 7B 模型单卡放得下 用 DDP；70B 放不下 用 FSDP |

### 三种 NAS 方法 (RL vs 进化 vs DARTS)

| Dimension (维度) | RL-Based NAS | Evolutionary NAS | DARTS | Example (示例) |
|-----------|---|---|---|---------| 
| 搜索方式 | 中央控制器"指挥" | 群体变异-淘汰"自涌现" | 连续优化（梯度下降） | RL 有指挥官，进化靠群众，DARTS 靠数学 |
| 搜索时间 | 数千 GPU 小时 | 数千 GPU 小时 | **几小时** | DARTS 效率提升 1000 倍 |
| 代表成果 | NASNet | AmoebaNet | DARTS | — |

### 超参数搜索三方法 (Grid vs Random vs Bayesian)

| Dimension (维度) | Grid Search | Random Search | Bayesian Optimization | Example (示例) |
|-----------|---|---|---|---------| 
| 策略 | 穷举所有组合 | 随机采样 | 概率模型预测下一个最优点 | 地毯式搜索 vs 随机扔飞镖 vs 看上一个飞镖再决定 |
| 保证最优 | ✅ 是 | ❌ 否 | ⚠️ 高概率 | — |
| 高维效率 | ❌ 维度灾难 | ✅ 更高效 | ✅ 样本效率最高 | — |

## 3. Formulas (公式)

### 梯度检查点

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| 内存: $O(\sqrt{N})$ 检查点，时间: $1.2×$ | 梯度检查点的核心权衡：每 $\sqrt{N}$ 个节点标记一个检查点，用 20% 额外计算换 10× 内存容量 | 100 层网络标记 10 个检查点 |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| 实战中混合数据预测连续值首选 Random Forest / GBM | 天然支持数值+类别混合类型、无需太多预处理、可解释性好、处理大数据高效 | 大数据集回归任务 → RF/GBM 优于线性回归和 DNN |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 直接选最新 SOTA 模型 | **不要只用 SOTA**——先问"适不适合"再问"先不先进"，SOTA 在学术基准评估，不一定适合你的数据 | BERT-Large 对 10 行 CSV 表格过于复杂 |
| 梯度检查点"既省时又省内存" | 梯度检查点是用**20% 额外计算换 10× 内存**——时间会增加，不是"免费的午餐" | 训练时间从 10h → 12h，但能装 10× 大的模型 |
| DDP 和 FSDP 可以随意互换 | DDP 适用于模型**放得进单卡**的场景；FSDP 适用于模型**放不进单卡**的超大模型 | 7B 模型用 DDP，175B 模型必须用 FSDP |
| DARTS = 一种强化学习方法 | DARTS 是**可微分方法**，把离散搜索转成连续优化问题，与 RL 完全不同；DARTS 用 Supernet + 梯度下降 | RL-NAS 有 Controller (RNN)，DARTS 没有 |
| 以为所有 NAS 方法都极其昂贵 | DARTS 将搜索时间从数千 GPU 小时降到**几小时**，使普通实验室也能用 NAS | DARTS: 几小时 vs RL-NAS: 数千 GPU 小时 |

# W6: Model Deployment & Compression (模型部署与压缩)

## 1. Definitions (定义)

### Deployment Myths (部署误区)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Model Decay (模型衰退) | 模型性能随时间自然下降 (model performance degrades over time)，根因是数据分布漂移 | 2019 年训练的房价模型在 2020 年疫情后预测失准 |
| Data Distribution Shift (数据分布漂移) | 训练数据和实际使用数据的分布不一致 (mismatch between training and production data)，导致模型衰退 | 训练数据主要是北京用户，上线后全国用户涌入 |

### Scaling Strategies (扩展策略)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Vertical Scaling (垂直扩展) | 给单台机器增加 CPU/内存 (add more resources to single machine)，简单但有天花板 | 从 8GB 升级到 64GB 内存 |
| Horizontal Scaling (水平扩展) | 增加更多机器 (add more machines)，适合无状态服务 | 从 1 台服务器扩展到 10 台 |
| Auto-scaling (自动扩展) | 根据负载自动调节机器数量 (auto-adjust based on load) | AWS Auto Scaling / K8s HPA |
| Microservices (微服务) | 系统拆分为独立服务各自扩展 (split system into independent services) | 推理服务和数据处理服务分开扩展 |
| Hybrid Scaling (混合扩展) | 垂直 + 水平结合 (combine vertical and horizontal)，大多数实际系统采用 | 先升级单机能力，不够再加机器 |

### Prediction Modes (预测模式)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Batch Prediction (批量预测) | 预测结果定期批量生成并存入数据库，用户需要时直接查 (asynchronous, pre-computed)，也叫异步预测 | Netflix 推荐列表——提前算好存着 |
| Online Prediction (在线预测) | 请求到达后立即生成并返回预测结果 (synchronous, real-time)，通过 RESTful API 接收请求 | 在线翻译——输入后立刻返回翻译结果 |

### Model Compression (模型压缩)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Low-Rank Factorization (低秩分解) | 用低维张量替换高维张量 (replace high-dimensional tensors with low-dimensional ones)，减少参数量 | SqueezeNet: 3×3 → 1×1 卷积，参数减少 50% |
| Knowledge Distillation (知识蒸馏) | 用大模型 Teacher 训练小模型 Student (large Teacher trains small Student)，Student 学到 Teacher 的知识用于部署 | DistilBERT: 大小 60%, 能力 97%, 速度 160% |
| Pruning (剪枝) | 将不重要的神经元权重设为零使网络变稀疏 (set unimportant weights to zero → sparse network)，可减少高达 90% 非零参数 | 绝对值 < 阈值的权重设为 0 |
| Quantization (量化) | 用更少的位数表示模型参数 (use fewer bits to represent parameters)，**最常用的压缩方法** | FP32 → FP16 → INT8 |
| DistilBERT | 知识蒸馏的典型成果 (Knowledge Distillation case study)，大小 60%、NLU 能力 97%、推理速度 160%，几乎无损 | BERT → DistilBERT 用于生产推理 |
| SqueezeNet | 低秩分解的典型成果 (Low-Rank Factorization case)，用 1×1 卷积替换 3×3 卷积，准确率与 AlexNet 相当但参数减半 | AlexNet 精度 + 50% 参数量 |

## 2. Comparisons (对比)

### 批量 vs 在线预测 (核心考试知识点)

| Dimension (维度) | Batch Prediction (批量预测) | Online Prediction (在线预测) | Example (示例) |
|-----------|---|---|---------| 
| 延迟 (Latency) | ✅ 低感知延迟（提前算好） | ⚠️ 可能高延迟 | 查 DB vs 现场推理 |
| 当前上下文 (Context) | ❌ 可能错过当前上下文 | ✅ 捕获当前上下文 | 不知用户"刚搜了什么" vs 实时捕获 |
| 计算效率 (Efficiency) | ✅ 批量推理很高效 | ⚠️ 单条推理开销大 | GPU 批推理 vs 逐条推理 |
| 输入需求 (Input) | ❌ 需要提前知道输入 | ✅ 输入随请求提供 | 预算所有商品推荐 vs 按搜索词推荐 |
| 资源浪费 (Waste) | ❌ 预测可能浪费（算了没人用） | ✅ 按需推理无浪费 | 预测 100 万结果只查 1 万 |
| 特征类型 (Features) | 仅批量特征 | 批量 + 流式特征都可 | — |
| 基础设施 (Infra) | ✅ 相对简单 | ❌ 需额外基础设施 | 定时任务 vs API Gateway + 推理服务 |

### GPU vs CPU 推理 (Roblox 案例)

| Dimension (维度) | GPU (V100) | CPU (Xeon 36 核) | Example (示例) |
|-----------|---|---|---------| 
| 训练 | ✅ 远快于 CPU | ❌ 慢 | — |
| 单条推理成本 | ❌ 贵 | ✅ 便宜 | — |
| 实际吞吐 | 400-500 次/秒 | **3,000 次/秒** | 同等成本下 CPU 吞吐量是 GPU 的 6-7 倍 |

### 四种压缩技术对比

| Dimension (维度) | Low-Rank Factorization | Knowledge Distillation | Pruning | Quantization | Example (示例) |
|-----------|---|---|---|---|---------| 
| 核心思想 | 低维矩阵替代高维 | 大模型教小模型 | 删除不重要权重 | 减少位数表示 | — |
| 比喻 | 简笔画替代油画 | 教授教本科生 | 修剪树枝 | 精装修降简装 | — |
| 常用程度 | 中 | 高 | 中 | **最高** | 量化是工业界最常用 |

### 蒸馏 vs 直接训练小模型

| Dimension (维度) | Knowledge Distillation (知识蒸馏) | Direct Training (直接训练小模型) | Example (示例) |
|-----------|---|---|---------| 
| 迁移学习 (Transfer) | ✅ Student 从 Teacher 学到通用知识 | ❌ 从零学 | DistilBERT 继承 BERT 的语言理解 |
| 正则化 (Regularization) | ✅ soft labels 包含更多信息 | ❌ 只有 hard labels | soft labels 提供类间关系 |
| 泛化 (Generalization) | ✅ Teacher 帮助避免过拟合 | ⚠️ 更容易过拟合 | — |

## 3. Formulas (公式)

### 量化存储计算

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| 存储 = 参数量 × 位数 / 8 | 模型存储占用与精度的关系 | 1 亿参数: FP32=400MB, FP16=200MB, INT8=100MB |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| Roblox 四步优化实现 CPU 上 10 亿次/天 BERT 推理 | BERT(固定128) → DistilBERT(蒸馏) → 动态输入(去 padding) → 量化(INT8) | 三种技术串联：蒸馏 + 动态输入 + 量化 |
| 将 PyTorch 线程数设为 1 反而更快 | 默认多线程导致多 worker 间线程竞争→性能停滞；每进程 1 线程避免切换开销 | 反直觉优化 |
| 在线预测延迟增加 500ms → 用户流量下降 20% | Google 研究：微小延迟对业务影响巨大 | 延迟对用户留存至关重要 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 以为模型上线后性能不会变 | 模型会因 **Data Distribution Shift** 自然衰退，需持续监控和定期重训 | 疫情导致房价模型完全失准 |
| 以为"加机器"是唯一扩展方式 | 有 **5 种扩展策略**：垂直/水平/自动/微服务/混合 | 混合扩展是大多数实际系统的选择 |
| 以为 GPU 推理一定比 CPU 好 | 同等成本下 CPU 推理吞吐量可以是 GPU 的 **6-7 倍** | Xeon 36核: 3000次/秒 vs V100: 400-500次/秒 |
| 量化的最新趋势搞混 | 训练: **FP16/BF16 可用、INT8 不可用**；推理: **INT8 可用** | INT8 训练精度损失太大，暂不可行 |
| 以为知识蒸馏不如直接训练小模型 | 蒸馏比直接训练**效果更好**：迁移学习 + 正则化 + 中间表示 + 改善泛化 | DistilBERT 比同规模直接训练的模型好 |
| 更多线程 = 更高性能 | Roblox 发现**每进程 1 线程**反而最快——多线程导致线程竞争和切换开销 | PyTorch 默认多线程在多 worker 下性能停滞 |
| 以为一个团队只需管理一两个模型 | 大公司如 Uber 同时运行 **200+ 个 ML 模型**，架构必须支持多模型并行管理 | 需求预测、ETA、定价、欺诈检测各有独立模型 |

# W7/W9: MLOps Infrastructure & Tooling (MLOps 基础设施与工具)

## 1. Definitions (定义)

### Four-Layer Architecture (四层架构)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Storage & Compute Layer (存储与计算层) | ML 系统的"地基"，提供数据存储 (HDD/SSD/Cloud) 和算力 (GPU/CPU) (foundation layer providing data storage and compute power) | AWS S3 存数据，A100 GPU 跑训练 |
| Resource Management Layer (资源管理层) | ML 系统的"水电管道"，解决多任务调度、依赖关系和资源分配 (scheduling, dependency management, resource allocation) | Airflow DAG 调度、Slurm 排队、K8s 编排 |
| ML Platform Layer (ML 平台层) | ML 系统的"精装修"工具集，管理模型/特征/部署的全生命周期 (full lifecycle management for models, features, deployment) | SageMaker 部署、MLFlow 模型存储、Feast 特征存储 |
| Development Environment Layer (开发环境层) | ML 工程师的日常工作台 (daily workspace)，包含 IDE + 版本控制 + CI/CD | Jupyter Notebook + Git + GitHub Actions |

### Storage & Compute (存储与计算)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| HDD (机械硬盘) | 传统磁盘存储，便宜但慢 (cheap but slow)，适合冷数据归档 | 历史日志长期存档 |
| SSD (固态硬盘) | 高速闪存存储，快但贵 (fast but expensive)，适合热数据访问 | 模型训练时频繁读取的数据集 |
| Compute Utilization (计算利用率) | 作业实际使用的 FLOPS / 计算单元最大 FLOPS 能力 (actual FLOPS / max FLOPS capability)，实际通常只有 ~50% | 你付了 100% 云费用但只用到 50% 算力 |
| Cloud Repatriation (云回迁) | 将工作负载从公有云搬回自有数据中心 (move workloads from public cloud back to on-premise)，因为云成本约占收入的 50% | a16z 分析：云支出约占收入成本的 50% |

### Development Environment (开发环境)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Stateful Notebook (有状态 Notebook) | 运行后保留变量和数据状态的交互式开发环境 (retains state after execution)，支持断点恢复和代码+文档一体化 | Netflix 在生产环境中使用 Notebook |
| Papermill | Notebook 参数化执行工具 (parameterized notebook execution)，同一个 Notebook 自动跑 N 组超参数 | 一个 Notebook 跑 100 组学习率实验 |
| Commuter | Notebook 共享平台，团队内查看/搜索/共享 Notebook (team-wide notebook sharing platform) | 团队成员浏览共享的分析报告 |
| nbdev | 将代码/文档/测试写在同一个 Notebook 里的开发框架 (code + docs + tests in one notebook) | 一个 Notebook 生成 Python 包 + 文档 + 测试 |

### Containerization (容器化)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Docker Container (Docker 容器) | 轻量级、独立、可执行的软件包，包含运行所需的一切 (self-contained executable package with code + runtime + tools + libraries + settings) | 解决"在我电脑上能跑"的环境一致性问题 |
| Docker Image (Docker 镜像) | 容器的构建"配方" (recipe/blueprint for building containers)，由 Dockerfile 定义 | Dockerfile → docker build → image → container |
| Pod | Kubernetes 中最小的部署单元，一组紧密协作的容器 (smallest deployable unit in K8s, group of tightly-coupled containers)，共享 IP 和端口空间，是扩缩容的原子单位 | Model API 容器 + Logging 容器 = 1 个 Pod |

### Resource Management (资源管理)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Cron | 最原始的任务调度工具，在固定时间运行任务 (run tasks at fixed times)，致命缺陷：不理解任务间的依赖关系 | 每天凌晨 2 点跑数据清洗脚本 |
| Scheduler (调度器) | 管 **When + What** 的升级版 Cron (manages when to run and what resources needed)，理解 DAG 依赖关系 | Slurm, Airflow |
| Orchestrator (编排器) | 管 **Where** 的底层资源调配 (manages where to get resources)，动态增减实例 | Kubernetes |
| DAG (有向无环图) | 定义任务之间先后依赖关系的图结构 (directed acyclic graph defining task dependencies) | 数据清洗 → 特征工程 → 训练 → 评估 |
| Airflow | Airbnb 开发的第一代工作流管理工具，有三大致命缺陷：单体架构/不可参数化/静态 DAG | DAG 写在 Python 里但不能动态创建步骤 |

### ML Platform (ML 平台)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Model Deployment (模型部署) | 将模型推送到生产环境并暴露为 API 端点 (push model to production and expose API endpoints)，最成熟的 ML 平台组件 | AWS SageMaker, Azure AzureML, GCP VertexAI |
| Model Store (模型存储) | 管理模型全生命周期元数据的系统 (system managing full model lifecycle metadata)，需存储 **8 类元数据** | 定义/参数/函数/依赖/数据/代码/制品/标签 |
| Feature Store (特征存储) | 保证训练和推理特征 100% 一致的管理系统 (ensure training-serving feature consistency)，解决 Management/Computation/Consistency 三大问题 | Feast（批量特征强）, Tecton（在线+批量） |

## 2. Comparisons (对比)

### Scheduler vs Orchestrator (调度器 vs 编排器)

| Dimension (维度) | Scheduler (调度器) | Orchestrator (编排器) | Example (示例) |
|-----------|---|---|---------| 
| 关心什么 | **When** + **What** | **Where** | 何时运行 vs 从哪里获取资源 |
| 抽象层级 | 高层：DAG、优先队列、用户配额 | 底层：机器、实例、集群、副本 | — |
| 代表工具 | Slurm, Airflow | **Kubernetes** | — |
| 比喻 | 餐厅经理（安排点菜顺序） | 厨房主管（调配厨师和灶台） | — |

### Docker 五大优势

| Dimension (维度) | Without Docker | With Docker | Example (示例) |
|-----------|---|---|---------| 
| Portability | 环境依赖不可移植 | 一次构建到处运行 | 本地训练 → 云端部署无需修改 |
| Consistency | 开发/测试/生产不一致 | 行为完全相同 | 告别"在我机器上能跑" |
| Isolation | 多模型互相干扰 | 容器间完全隔离 | 多个模型版本可并行运行 |
| Scalability | 手动扩容 | 一键伸缩容 | 流量高峰时自动扩容 |
| Version Control | 环境不可版本化 | 镜像可版本化共享 | Docker Hub 分享环境 |

### Airflow vs 新一代编排器 (Argo/Prefect)

| Dimension (维度) | Airflow | Argo / Prefect | Example (示例) |
|-----------|---|---|---------| 
| 架构 | **单体** (一个步骤失败整个重启) | 微服务架构 | 单步骤失败不影响其他步骤 |
| 参数化 | **不可参数化** (不能向 DAG 传参) | 支持参数化 | 不同学习率用同一个工作流 |
| DAG 类型 | **静态 DAG** (运行时不能动态创建步骤) | 动态 DAG | 根据中间结果自动调整后续步骤 |

### Feast vs Tecton (特征存储)

| Dimension (维度) | Feast | Tecton | Example (示例) |
|-----------|---|---|---------| 
| 批量特征 (Batch) | ✅ 擅长 | ✅ 支持 | 离线计算的统计特征 |
| 流式特征 (Streaming) | ⚠️ 弱 | ✅ 同时支持在线和批量 | 实时点击流特征 |
| 集成深度 | 轻量 | 需要深度集成 | — |

## 3. Formulas (公式)

### 计算利用率

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $Utilization = \frac{Actual\ FLOPS}{Max\ FLOPS}$ | 计算利用率 = 实际 FLOPS / 最大 FLOPS 能力，实际通常只有 ~50% | 付了 100% 云费用只用到 50% 算力 |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| Model Store 需要 8 类元数据 | "定参函依数码品标"——Model Definition / Parameters / Featurize&Predict / Dependencies / Data / Model Gen Code / Experiment Artifacts / Tags | 仅存 model.pt 远远不够 |
| Feature Store 核心价值是保证一致性 | 训练时用"过去7天平均消费"，推理时却用"过去30天平均消费" → 预测完全不可信；Feature Store 统一管理计算逻辑 | 训练-推理特征不一致是常见 bug |
| Slurm 脚本是声明式资源请求 | `#SBATCH --mem-per-cpu=4096` 声明需要什么，调度器自动排队分配 | 这种声明式哲学也是 K8s 的设计核心 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 混淆 Scheduler 和 Orchestrator | Scheduler 管 **When + What**（时间和需求），Orchestrator 管 **Where**（资源位置）——**两者不是同一层** | Airflow(调度) + K8s(编排) 配合使用 |
| 以为 Pod = Container | Pod 是一组容器的"组队"，是 K8s 扩缩容的**原子单位**；Pod 中的容器共享 IP 和端口空间  | 一个 Pod 可以包含 Model API + Logging 两个容器 |
| 以为 Notebook 只是实验工具 | Netflix 在**生产环境**中使用 Notebook | Notebook 的有状态特性使其适合生产数据管道 |
| 以为 Airflow 是最佳工作流工具 | Airflow 有**三大致命缺陷**：单体/不可参数化/静态 DAG；新一代 Argo/Prefect 已解决 | 试不同学习率 → Airflow 需要创建 N 个工作流 |
| Model Store 只需存权重文件 | 需要 **8 类元数据**：定义/参数/函数/依赖/数据/代码/制品/标签——缺一不可 | 没有 Dependencies 信息 → 无法重现环境 |
| 云计算利用率接近 100% | 实际计算利用率通常只有 **~50%**——一半算力在"空转" | 云支出约占上市公司收入成本的 50% |

# W11: Prompt Optimization, Self-Reflection & Advanced RAG (提示优化、自反思与高级 RAG)

## 1. Definitions (定义)

### Prompt Optimization (提示优化)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Self-Consistency (自一致性) | 同一个问题向 LLM 询问 N 次，通过多数投票选出最终答案 (sample N times, majority vote)，消除 LLM 输出的随机性 | 5 次采样：3 次答 A、1 次 B、1 次 C → 最终答案 = A |
| Uncertainty Thresholding (不确定性阈值) | 在 Self-Consistency 基础上加置信度守门员 (adding confidence gate)：一致性 ≥ 阈值→返回答案；< 阈值→拒绝回答交给人类——让 LLM **"知道自己不知道"** | 投票 80% 一致→自信回答；仅 40% 一致→弃权 |
| OPRO (Optimization by PROmpting) | 用 LLM 自身作为优化器，迭代生成更好的提示 (use LLM itself as optimizer to iteratively improve prompts)，包含 Meta-Prompt / LLM Optimizer / Objective Function 三大组件 | OPRO 发现 "Take a deep breath and work step-by-step" 准确率 80.2% |
| Meta-Prompt (元提示) | OPRO 的输入组件，包含问题描述 + 历史提示及其评分 (problem description + history of prompts and their scores) | 考试资料包 |
| Chain-of-Thought / CoT (思维链) | 让 LLM 逐步推理而非直接给答案的提示策略 (step-by-step reasoning)，是 OPRO 自动发现的最优提示的本质 | "Let's think step by step" |

### Self-Reflection (自反思)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Reflexion (反思) | 让 LLM "检查自己的作业"的迭代修正框架 (iterative self-correction framework)，用于纠正错误、提升质量、增强理解 | Task → Solution → Test → Self-reflection → Refined Solution |
| Feedback-Driven Reflexion (反馈驱动反思) | 由用户负面反馈（👍/👎）触发的修正 (triggered by user negative feedback)，事后补救，低额外开销 | 用户标记"Poor" → LLM 重新生成更详细答案 |
| Implicit Reflexion (隐式反思) | 在所有回答发送给用户之前自动自评审查 (automatic self-review before every response)，事前预防，但每次增加一步延迟 | 隐藏层自评："if necessary，提供更具体答案" |

### Advanced RAG (高级 RAG)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Naive RAG (朴素 RAG) | 标准四步 RAG：分块→嵌入→检索 Top-K→LLM 生成 (basic chunking → embedding → retrieval → generation)，每步都可能出问题 | 固定大小切割→在句子中间截断→检索到不完整信息 |
| Fixed-size Chunking (固定大小分块) | 按固定 token 数切割 + 重叠窗口 (split by fixed token count + overlap)，简单快速但可能截断句子 | 每 512 tokens 切一块，重叠 50 tokens |
| Recursive Chunking (递归分块) | 按 `\n\n` → `\n` → `.` 逐级递归拆分 (recursive splitting by separators)，LangChain 默认方法 | 先按段落分，段落太长再按句子分 |
| Document-based Chunking (文档结构分块) | 利用文档结构如 Markdown 标题/HTML 标签来分块 (split by document structure)，尊重原始结构 | 按 `## 标题` 分块 |
| Semantic Chunking (语义分块) | 计算相邻句子嵌入相似度，骤降处切割 (split where embedding similarity drops sharply)，按语义分组质量最高但计算成本高 | 相似度突然从 0.9 降到 0.3 → 在此处切割 |
| Agentic Chunking (智能体分块) | 用 LLM 判断分块边界 (LLM decides chunk boundaries)，最智能但最慢最贵 | LLM 判断"这段讲的是新话题" |
| Lost in the Middle (中间丢失) | LLM 对输入的开头和结尾关注度高，中间部分信息容易被忽略 (LLM attends to beginning and end, neglects middle) | 100 页论文记得摘要和结论，第 47 页忘了 |
| Hybrid Search (混合搜索) | 关键词搜索 (BM25) + 语义搜索 (Dense Retrieval) + 分数融合 (score fusion)，互补短板 | 精确术语用 BM25，概念理解用语义搜索 |
| RRF (Reciprocal Rank Fusion) | 将多路搜索各自的排名加权合并，取综合排名最高的文档 (weighted combination of rankings from multiple retrieval methods) | BM25 排名 + 语义排名 → 融合后选 Top-5 |
| Reranking (重排序) | 两阶段检索：Bi-Encoder 快速初筛 + Cross-Encoder 精准精排 (two-stage: fast initial retrieval + precise re-ranking)，Advanced RAG 中效果最显著的改进 | 从 100 万文档筛 Top-100 再精排选 Top-5 |
| Bi-Encoder (双编码器) | Query 和 Doc 分别独立编码为向量再算相似度 (encode separately, compare vectors)，快但精度中等 | 快速筛简历 |
| Cross-Encoder (交叉编码器) | Query 和 Doc 拼接后联合编码打分 (concatenate and encode jointly)，精准但慢（BERT 注意力捕获交叉关系） | 一对一面试 |
| Fine-tune Embedding (微调嵌入模型) | 用领域数据微调嵌入模型使其理解领域术语 (domain-adapt embedding model)，成本远低于微调 LLM（~100M vs ~7B+ 参数） | 医学领域 "MI" = 心肌梗塞 vs 金融领域 "MI" = 市场情报 |

## 2. Comparisons (对比)

### Feedback-Driven vs Implicit Reflexion (两种反思方法)

| Dimension (维度) | Feedback-Driven Reflexion | Implicit Reflexion | Example (示例) |
|-----------|---|---|---------| 
| 触发方式 | 用户负面反馈（👍/👎） | 自动（每次回答前） | 事后补救 vs 事前预防 |
| 额外开销 | 低（只在用户不满时触发） | 高（每次请求多一步） | — |
| 质量保证 | 事后补救 | 事前预防 | — |
| 适用场景 | 聊天界面、对话系统 | 关键业务、不允许低质量输出 | 客服聊天 vs 医疗报告 |

### Bi-Encoder vs Cross-Encoder (重排序核心)

| Dimension (维度) | Bi-Encoder (双编码器) | Cross-Encoder (交叉编码器) | Example (示例) |
|-----------|---|---|---------| 
| 编码方式 | Query, Doc **分别**编码 | Query+Doc **拼接后联合**编码 | 各自独立 vs 拼在一起 |
| 速度 | ✅ 快（Doc 向量可预计算） | ❌ 慢（每对重新计算） | — |
| 精度 | ⚠️ 中等 | ✅ 高（BERT 注意力捕获交叉关系） | — |
| 使用场景 | 海量候选初筛 (Stage 1) | 少量候选精排 (Stage 2) | 从 100 万→100 vs 从 100→5 |

### 五种分块策略 (从简单到智能)

| Dimension (维度) | Fixed-size | Recursive | Document-based | Semantic | Agentic | Example (示例) |
|-----------|---|---|---|---|---|---------| 
| 依据 | 固定 token 数 | 分隔符递归 | 文档结构 | 嵌入相似度 | LLM 判断 | — |
| 质量 | 低 | 中 | 中高 | 高 | 最高 | — |
| 成本 | 最低 | 低 | 低 | 中高 | 最高 | — |

### 微调 Embedding vs 微调 LLM (性价比)

| Dimension (维度) | Fine-tune Embedding | Fine-tune LLM | Example (示例) |
|-----------|---|---|---------| 
| 模型大小 | 小（~100M 参数） | 大（~7B+ 参数） | — |
| 训练成本 | ✅ 低 | ❌ 高 | 便宜 100 倍 |
| 改进目标 | 检索精度 | 生成质量 | 给搜索引擎换"领域眼镜" vs 让"作家"学你的风格 |

## 3. Formulas (公式)

_No formulas this week._

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| OPRO 在 GSM8K 上自动发现的最优提示 | "Take a deep breath and work on this problem step-by-step." = **80.2%** 准确率 | 超越人工 "Let's think step by step" |
| OPRO Top 提示都包含"分步思考"核心 | #1: 80.2%, #2 "Break this down" 79.9%, #3 "arithmetic and logical approach" 78.5% | LLM 能自动发现甚至超越人类手动设计的提示 |
| 好的分块 = 每个 chunk 包含完整的语义单元 | 分块是 RAG 第一步也是影响最大的一步——切得不好后续再怎么优化也挽救不了 | 在句子中间截断 → 检索到不完整信息 |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 以为 Self-Consistency 能解决所有问题 | Self-Consistency 只消除随机性，**不能改进提示本身的质量**；如果所有路径都错，投票也救不了 | 5 次都用差提示→5 个错答案→投票还是错 |
| 以为提示优化能弥补知识缺失 | 提示优化只改进"问问题的方式"，**无法纠正模型训练数据中缺失的知识** | 模型不知道 2024 奥运结果，再好的提示也问不出 |
| 混淆 Implicit Reflexion 的 "if necessary" | Implicit Reflexion 不是**每次都修改**，而是自评发现问题时才修改——"if necessary" 是关键 | 如果自评认为答案已足够好，则不修改直接返回 |
| 以为更大的上下文窗口就能解决 RAG 问题 | **Lost in the Middle**：LLM 对开头和结尾关注度高，中间部分容易被忽略；塞越多文档中间利用率越低 | 128K 窗口塞满文档，中间的关键信息仍被忽视 |
| 以为 Reranking 只是简单的排序 | Reranking 是**两种完全不同的模型**：Bi-Encoder（快，独立编码）+ Cross-Encoder（慢，联合编码）——两阶段流水线 | Bi-Encoder 筛 100 个候选 → Cross-Encoder 精排选 5 个 |
| 以为微调 LLM 是提升 RAG 性能的最佳方式 | **微调 Embedding 的性价比远超微调 LLM**：成本低 100 倍、数据需求少、只改进检索质量 | 微调 Embedding = 换"领域眼镜"；微调 LLM = 换整个"大脑" |

# W12: LLM Fine-Tuning & LoRA (LLM 微调与 LoRA)

## 1. Definitions (定义)

### Fine-Tuning Basics (微调基础)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| LLM Fine-Tuning (LLM 微调) | 用领域数据"再训练"一个已经学过通用知识的模型，使其在特定任务上成为专家 (re-train a pre-trained model on domain-specific data to become a specialist)——从"全科医生"到"专科医生" | Home Cook (Homer) → Sushi Chef (Kenji) |
| Pre-trained LLM (预训练大语言模型) | 在海量通用数据上训练好的模型 (model trained on massive general data)，拥有广泛但浅层的知识——像"家庭厨师"什么都会一点 | GPT-4, Llama-3 |
| Full Fine-Tuning (全量微调) | 更新模型的全部参数 (update all parameters, billions)，效果最强但成本极高且可能导致灾难性遗忘 | 需要多张 H100 GPU |
| Catastrophic Forgetting (灾难性遗忘) | 微调学了新领域知识后忘记了原有通用知识 (learning new domain knowledge causes forgetting of general knowledge) | 学了网络安全后忘了怎么翻译 |

### LoRA (低秩适配)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| LoRA (Low-Rank Adaptation) | 冻结原始权重 + 训练低秩适配器矩阵的微调方法 (freeze original weights, train small low-rank adapter matrices)，核心公式 $W_{new} = W_{orig} + A \times B$，不到 1% 的参数即可达到接近全量微调的效果 | d=4096, r=16 → LoRA 参数仅占 0.78% |
| $W_{orig}$ (原始权重) | 预训练模型的原始权重矩阵 (original pre-trained weights)，大小 d×d，状态 **Frozen（冻结不动）** | 一本 1000 页的百科全书 |
| $A$ (低秩矩阵 A) | LoRA 适配器的下投影矩阵 (down-projection matrix)，大小 d×r（r≪d），状态 **Trainable** | 便利贴的一半 |
| $B$ (低秩矩阵 B) | LoRA 适配器的上投影矩阵 (up-projection matrix)，大小 r×d（r≪d），状态 **Trainable** | 便利贴的另一半 |
| Rank $r$ (秩) | LoRA 适配器的秩/维度 (rank of adapter)，r≪d，决定适配器的大小和表达能力 | r=16 时仅 0.78% 参数 |
| Base LLM (基座模型) | LoRA 架构中的核心通用知识层 (generalist core)，参数 Billions 级，**Frozen** 状态 | Llama-3-8B |
| LoRA Adapter (LoRA 适配器) | LoRA 架构中的新任务/领域技能层 (specialist layer)，参数 Millions 级，**Updatable** 状态 | 网络安全 Adapter |

### Fine-Tuning Frameworks (微调框架)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Unsloth | 极致速度和低显存的微调框架 (speed + low VRAM optimized)，适合个人学习和单卡消费级 GPU | RTX 4090 上微调 Llama-3 |
| Axolotl | 面向可复现性和大规模训练的微调框架 (reproducibility + large-scale)，原生多卡支持最佳 | H100 集群上训练 70B 模型 |
| LLaMA-Factory | 易用一体化微调框架 (easy all-in-one)，提供 Web UI (LlamaBoard)，不写代码即可微调 | 通过网页界面一键启动微调 |
| HF PEFT | HuggingFace 的 Parameter-Efficient Fine-Tuning 库，纯 Python API，最灵活适合深度集成 (flexible API for custom integration) | 嵌入到已有 ML pipeline 中 |

## 2. Comparisons (对比)

### Full Fine-Tuning vs LoRA

| Dimension (维度) | Full Fine-Tuning (全量微调) | LoRA (低秩适配) | Example (示例) |
|-----------|---|---|---------| 
| 更新范围 | **全部**参数 | 冻结原始 + 训练小型适配器 | 重新印刷整本书 vs 贴便利贴 |
| 参数量 | Billions（数十亿） | Millions（百万级，<1%） | d=4096: 1677 万 vs 13 万 |
| 计算成本 | ❌ 极高 | ✅ 低 | 多张 H100 vs 单张 RTX 4090 |
| 灾难性遗忘 | ⚠️ 可能 | ✅ 不会（原始权重冻结） | 学了寿司忘了做意面 vs 不会忘 |
| 多任务切换 | ❌ 每个任务一份完整模型 | ✅ 换个 Adapter 就行 | 存 N 个完整模型 vs 存 N 个小 Adapter |
| 效果 | ✅ 最强 | ✅ 接近全量微调 | — |

### 微调决策：何时微调 vs 不微调

| Dimension (维度) | ✅ 需要微调 | ❌ 不需要/不该微调 | Example (示例) |
|-----------|---|---|---------| 
| 复杂任务 | ✅ 像专家一样完成高难度工作 | — | 像资深开发者一样写代码 |
| 简单任务 | — | ❌ 杀鸡用牛刀 → 用 Prompt Engineering | 简单 Q&A |
| 数据变化快 | — | ❌ 训完就过时 → 用 RAG 实时检索 | 股票价格预测 |
| 低质量数据 | — | ❌ GIGO 比不微调更差 → 先清洗数据 | 充满噪声的标注 |
| 隐私限制 | — | ❌ 敏感数据不能训练 → RAG + 本地部署 | 医疗患者数据 |

### 四大微调框架选型

| Dimension (维度) | Unsloth | Axolotl | LLaMA-Factory | HF PEFT | Example (示例) |
|-----------|---|---|---|---|---------| 
| 定位 | 极致速度/低显存 | 可复现性/大规模 | 易用一体化 | 核心逻辑/灵活 | — |
| 界面 | Python / No-code | YAML 配置 | **Web UI** | Python API | — |
| 硬件 | 单卡消费级 | 多卡 H100/A100 | 灵活 | 任意 | — |
| 上手难度 | 低~中 | 高 | **低** | 中~高 | — |
| 适合场景 | 个人/小项目 | 企业大规模 | 快速上手 | 深度集成 | — |

## 3. Formulas (公式)

### LoRA 核心公式

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $W_{new} = W_{orig} + A \times B$ | LoRA 核心公式：最终权重 = 冻结的原始权重 + 低秩适配器贡献 | d=4096, r=16 → Adapter 参数仅 0.78% |
| $LoRA\ params = d \times r + r \times d = 2dr$ | LoRA 适配器参数量：两个低秩矩阵 A(d×r) 和 B(r×d) 的参数总和 | d=4096, r=16 → 2×4096×16 = 131,072 |
| $Ratio = \frac{2dr}{d^2} = \frac{2r}{d}$ | LoRA 参数占原始参数的比例 | r=16, d=4096 → 比例 ≈ 0.78% |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| Colab 微调 Llama 完整流程 5 步 | ① 加载 Base Model → ② 配置 LoRA (rank, alpha) → ③ 准备领域数据 → ④ 训练 Adapter → ⑤ 合并推理 | 用网络安全 Q&A 数据微调 Llama-3-8B |
| LoRA 实现了"训练民主化" | 消费级 GPU（如 RTX 4090）就能微调大模型，不再需要 H100 集群 | 个人开发者也能微调 8B 模型 |
| 同一个 Base LLM + 不同 LoRA Adapter = 不同领域专家 | 医疗/法律/代码 Adapter 随时切换，只需存储小型 Adapter 文件 | 医疗 LoRA + 法律 LoRA + 代码 LoRA 共享同一 Base |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| 一遇到 LLM 不够好就想微调 | 微调是**"最后手段"**——先试 Prompt Engineering，再试 RAG，都不行才微调 | 简单格式问题用 Few-shot 就够了 |
| 以为全量微调总是比 LoRA 好 | LoRA 效果**接近全量微调**，但成本低得多且**无灾难性遗忘** | Full FT 可能反而因遗忘把通用能力弄差 |
| 以为 LoRA 需要更新所有参数 | LoRA **冻结全部原始权重** ($W_{orig}$ = Frozen)，只训练两个小矩阵 $A$ 和 $B$ | 原始的 Billions 参数一个不动 |
| 搞混 LoRA 中各矩阵的状态 | $W_{orig}$: **Frozen** / Billions；$A$, $B$: **Trainable** / Millions (< 1%) | 考试会考哪个是冻结的、哪个是可训练的 |
| 以为微调后就不需要管了 | 如果数据分布变化快（如股票），微调模型也会**过时**——这种场景应该用 RAG 而非微调 | 股票模型微调 → 下个月就失效 |
| 以为低质量数据微调会"至少有点用" | 低质量数据微调 **Garbage In → Garbage Out**，效果可能比不微调更差 | 充满错误标注的数据 → 模型学到错误模式 |