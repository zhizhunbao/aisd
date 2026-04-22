# W11: Prompt Optimization, Self-Reflection & Advanced RAG (提示优化、自反思与高级 RAG)

> **本页缩写 (Abbreviations used)**
> **BERT** = Bidirectional Encoder Representations from Transformers  
> **ML** = Machine Learning


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
