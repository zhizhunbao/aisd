# W2: LLM Evaluation Frameworks — G-Eval, RAGAS, DeepEval, DAG Eval (LLM 评估框架——G-Eval、RAGAS、DeepEval、DAG Eval)

> **本页缩写 (Abbreviations used)**
> **BERT** = Bidirectional Encoder Representations from Transformers  
> **GPT** = Generative Pre-trained Transformer  
> **METEOR** = Metric for Evaluation of Translation with Explicit ORdering  



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
