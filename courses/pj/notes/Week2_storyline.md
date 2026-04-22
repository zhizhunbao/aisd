# Week 2 故事线：从"人工盯着看"到"自动化评估工厂"——评估框架与工具

> **Source:** `Module2.1-Evaluation-Frameworks-and-Tools.ipynb`
> **核心主题：** Week 1 我们知道了"为什么要评估"和"用什么方法评估"。Week 2 解决"怎么在生产环境中**系统化、自动化**地执行评估"——从手工评估走向工业级评估流水线。
> **故事线：** 看不见（黑盒 LLM）→ 让它可观测（Observability + Telemetry）→ 用框架自动评估（G-Eval → RAGAS → DeepEval）→ 统一的评估工具栈

---

## 🎬 序幕：我们在解决什么问题？

Week 1 的故事结束时，我们已经掌握了：
- ✅ 有参考评估指标 (ROUGE/BLEU/BERTScore)
- ✅ LLM-as-a-Judge 方法论
- ✅ 五大偏见及缓解策略

但有一个关键问题没解决：

> **在生产环境中，LLM 应用在持续运行。你不可能每次都手动跑 ROUGE、手动写 Judge Prompt。你需要：**
> 1. 一套**可观测性 (Observability)** 基础设施——实时看到 LLM 内部发生了什么
> 2. 一套**自动评估框架**——自动打分、自动报告

> 💡 **核心直觉：** Week 1 教你"怎么做手术"，Week 2 教你"怎么建医院"——从单点技能到系统化基础设施。

---

## 📚 第一章：可观测性 (Observability)——让黑盒变透明

### 1.1 什么是可观测性？

> **一句话定义：** 可观测性 = 仅通过系统的**外部输出**（日志、指标、追踪），就能回答关于系统内部行为的**任意问题**。

与传统监控 (Monitoring) 的区别：

| 维度 | 传统监控 | 可观测性 |
|------|---------|---------|
| **问什么** | 预定义指标（CPU、内存、错误率） | 任意问题（"为什么这个请求慢了？"） |
| **适用场景** | 已知问题的检测 | 未知问题的诊断 |
| **对 GenAI** | 只知道"调用了 LLM"和"用了多少 token" | 知道完整的推理路径、每步延迟、每步输入输出 |

### 1.2 为什么 GenAI 特别需要可观测性？

| 原因 | 说明 |
|------|------|
| **复杂度高** | GenAI 应用涉及多组件（LLM、向量数据库、检索器、解析器等），需要端到端可见性 |
| **非确定性** | LLM 输出不确定，需要追踪每次请求的完整路径来调试 |
| **成本优化** | 通过观察 token 使用和延迟来优化成本 |
| **质量保证** | 实时监控输出质量，及时发现 hallucination 或性能下降 |

> 🔑 **故事转折点：** 知道了需要可观测性。那具体怎么实现？数据从哪来？→ **遥测 (Telemetry)** 和 **OpenTelemetry** 登场！

---

## 🎭 第二章：遥测数据——Spans 与 Traces

### 2.1 遥测 (Telemetry) 的四种信号

可观测性的数据以四种信号形式呈现：

| 信号 | 英文 | 作用 |
|------|------|------|
| **Spans** | 跨度 | 单个操作的计时单元（如一次 LLM 调用） |
| **Traces** | 追踪 | 一次完整请求的端到端路径（多个 Spans 组成） |
| **Metrics** | 指标 | 聚合的数值数据（如平均延迟、错误率） |
| **Logs** | 日志 | 离散的事件记录 |

### 2.2 Span——观测的原子单位

> **一句话定义：** Span = 一次操作的 "计时+元数据" 记录。

**一个 Span 包含什么？**

| 字段 | 说明 | 例子 |
|------|------|------|
| **Name** | 操作名称 | `chat.completions.create` |
| **Parent Span ID** | 父 Span | 指向发起调用的 Span |
| **Start/End Timestamps** | 起止时间 | 2026-04-20T19:00:00Z |
| **Span Context** | 上下文信息 | Trace ID + Span ID |
| **Attributes** | 键值对元数据 | `gen_ai.model: gpt-4`, `tokens: 150` |
| **Events** | 关键时间点 | `"string-format"`, `"error"` |
| **Status** | 状态 | OK / ERROR |

**OpenTelemetry 语义约定 (Semantic Conventions)：** 标准化的属性命名规范

| 属性 | 说明 |
|------|------|
| `gen_ai.system` | LLM 提供商（openai, anthropic…） |
| `gen_ai.request.model` | 模型名称（gpt-4, claude-3…） |
| `gen_ai.usage.input_tokens` | 输入 token 数 |
| `gen_ai.usage.output_tokens` | 输出 token 数 |
| `gen_ai.request.temperature` | 温度参数 |

> 💡 **为什么需要语义约定？** 统一不同厂商的数据格式 → 便于跨平台分析和对比 → 支持自动化的成本计算和性能分析。

### 2.3 Trace——完整请求路径

> **一句话定义：** Trace = 一次请求在系统中的完整旅程，由多个 Spans 组成。

```
Trace（用户问 "帮我计算斐波那契数"）
├── Span: Agent 接收任务 (100ms)
│   ├── Span: 规划阶段 (50ms)
│   ├── Span: 调用 LLM 理解任务 (200ms)
│   ├── Span: 调用工具/函数 (150ms)
│   └── Span: 验证结果 (80ms)
└── 总耗时: 580ms
```

**从 Trace 中可以看出：**
- Agent 的推理步骤和决策过程
- 每个步骤的耗时分布（找最长的 → 优化性能）
- 哪些工具被调用了多少次（找重复的 → 优化逻辑）
- 错误发生在哪个环节（找红色的 → 定位 bug）

### 2.4 三种仪表化方法 (Instrumentation)

| 方法 | 英文 | 机制 | 优点 | 缺点 | 代表框架 |
|------|------|------|------|------|---------|
| **SDK/装饰器** | SDK-based | 开发者手动用 SDK 装饰函数 | 最高粒度，可捕获自定义元数据 | 代码侵入性高，厂商锁定 | LangSmith, Langfuse, MLflow |
| **自动仪表化** | Auto (OTel) | Monkey-patch 标准库，运行时自动注入 | 改动极少（一行初始化），厂商中立 | 可能与其他库冲突，控制力较低 | OpenLLMetry, OpenLIT, Arize Phoenix |
| **代理模式** | Proxy-based | 请求经过中间代理服务器 | 零代码改动，语言无关 | 黑盒（只看到输入输出），增加网络延迟 | Helicone, MLflow AI Gateway |

**选择指南：**
- 使用 LangChain → **LangSmith**
- 需要开源方案 → **Arize Phoenix**
- 快速零代码上线 → **Helicone**
- 需要标准化和厂商中立 → **OpenLLMetry**

> 🔑 **故事转折点：** 可观测性基础设施搭好了——我们能看到 LLM 内部发生了什么。但**看到数据不等于评估数据**。我们需要**自动化评估框架**来给输出打分。→ **G-Eval** 登场！

---

## 📖 第三章：G-Eval——让 LLM 自动生成评估步骤

### 3.1 G-Eval 是什么？

> **一句话定义：** G-Eval = 结合 **自动 CoT 推理** 和 **概率加权评分** 的无参考评估框架，与人类判断的对齐度远超传统指标。

**核心三步流程：**

| 步骤 | 做什么 | 详细说明 |
|------|--------|---------|
| **Step 1** | 设计评估 Prompt | 用自然语言明确定义评估任务和评分标准 |
| **Step 2** | 自动 CoT 生成 | LLM 基于任务和标准**自动生成详细的评估步骤** |
| **Step 3** | 概率加权评分 | 不取 LLM 输出的文字分数，而是提取 logprobs 做加权计算 |

### 3.2 概率加权评分公式

$$
score = \sum_{i=1}^{n} p(s_i) \cdot s_i
$$

其中：
- $\{s_1, s_2, ..., s_n\}$ = 评分标准中定义的可能分数集合
- $p(s_i)$ = LLM 生成 token $s_i$ 的概率

> 💡 **为什么用概率加权而不直接用 LLM 输出的分数？** 直接输出受采样随机性影响大；概率加权利用了 LLM 对每个分数的"内心确信度"，更稳定、更准确。

### 3.3 G-Eval 的优越性

| 对比 | ROUGE/BLEU | 人工评估 | G-Eval |
|------|-----------|---------|--------|
| **灵活性** | 低 | 高 | 高 |
| **准确性** | 中 | 高 | 高 |
| **成本** | 低 | 极高 | 中 |
| **与人类对齐** | Spearman ≈ 0.3-0.4 | — | Spearman ≈ 0.514 |

> 🔑 **故事转折点：** G-Eval 解决了通用文本的自动评估。但 GenAI 应用中最重要的场景之一是 **RAG**——检索增强生成。RAG 系统有独特的评估需求（检索器质量 + 生成器质量）。→ **RAGAS** 框架登场！

---

## 🏆 第四章：RAGAS——RAG 系统的专用评估框架

### 4.1 为什么 RAG 需要专门的评估？

RAG 是解决 LLM 三大痛点的高效方案：

| LLM 痛点 | RAG 如何解决 |
|---------|------------|
| **知识截止** | 从外部知识库检索最新信息 |
| **领域知识不足** | 接入专业文档/内部数据 |
| **Hallucination** | 用检索到的证据约束生成 |

但 RAG 评估面临独特挑战：

| 挑战 | 说明 |
|------|------|
| **组件耦合** | 最终答案质量取决于检索器 AND 生成器 |
| **无通用基准** | 没有适用于所有 RAG 的标准基准数据集 |
| **动态漂移** | 知识库更新后评估结果可能过时 |
| **人工评估太贵** | 频繁的人工评估不可持续 |

### 4.2 RAGAS 三大核心指标

| 指标 | 英文 | 衡量什么 | 公式 | 如何计算 |
|------|------|---------|------|---------|
| **忠实度** | Faithfulness (F) | 生成的答案是否被检索到的上下文支持？（直接衡量幻觉程度） | $F = V / S$ | Judge-LLM 提取答案中的每条陈述 → 逐条验证是否能在上下文中找到支持 |
| **答案相关性** | Answer Relevance (AR) | 生成的答案是否直接回答了原始问题？ | $AR = \frac{1}{n} \sum_{i=1}^{n}sim(q, q_i)$ | Judge-LLM 反向生成"这个答案可以回答什么问题？" → 计算与原始问题的余弦相似度 |
| **上下文相关性** | Context Relevance (CR) | 检索到的上下文与问题的相关程度如何？ | $CR = E / S$ | Judge-LLM 提取上下文中**必要的**句子 → 必要句子数 / 总句子数 |

其中：
- $V$ = 被上下文验证的陈述数 (Verified statements)
- $S$ = 答案中的总陈述数 (Total statements)
- $E$ = 上下文中对回答问题**必要的**句子数 (Extracted essential sentences)
- $q$ = 原始问题, $q_i$ = 从答案反向生成的问题

> 💡 **关键洞察：** RAGAS 将 RAG 评估分解为**检索器评估** (Context Relevance) 和**生成器评估** (Faithfulness + Answer Relevance)——这样可以精确定位问题出在哪个组件！

> 🔑 **故事转折点：** G-Eval 解决通用评估，RAGAS 解决 RAG 评估。但实际项目中，你需要一个**统一的工具**来整合所有这些评估能力。→ **DeepEval** 登场！

---

## ⚡ 第五章：DeepEval——一站式评估工具箱

### 5.1 DeepEval 是什么？

> **一句话定义：** DeepEval = 建立在 G-Eval 框架之上的开源评估工具包，提供 30+ 即插即用的 LLM 评估指标，支持端到端和组件级评估。

**六大能力：**

| 能力 | 说明 |
|------|------|
| ① 即插即用 30+ 指标 | 覆盖自定义、RAG、Agent、多轮对话、多模态、安全性 |
| ② 端到端 + 组件级 | 可以整体评估，也可以逐组件评估 |
| ③ 合成数据集生成 | 自动生成测试数据集 |
| ④ 自定义指标 | 支持用户定义自己的评估逻辑 |
| ⑤ SecOps 支持 | 红队测试和安全漏洞扫描 |
| ⑥ 多类型应用 | RAG、Agent、Chatbot 等 |

### 5.2 自定义指标：G-Eval vs DAG Eval

**G-Eval（在 DeepEval 中）：** 用一个自然语言 Prompt 定义评估逻辑。

```
示例 Prompt：
"如果摘要缺少 intro/body/conclusion 中的任何一个标题，得 0 分。
 如果三个标题都有但顺序错误，得 2 分。
 如果三个标题都有且顺序正确，得 10 分。"
```

**DAG Eval：** 用**有向无环图（决策树）**定义结构化的评估流程。

```
评估会议摘要的 DAG：

1. TaskNode: 提取摘要中的标题
   ↓
2. BinaryJudgementNode: 是否包含 intro/body/conclusion？
   ├─ No → VerdictNode: 0分
   └─ Yes → 继续
        ↓
3. NonBinaryJudgementNode: 标题顺序是否正确？
   ├─ 全部正确 → VerdictNode: 10分
   ├─ 两个错位 → VerdictNode: 4分
   └─ 全部错位 → VerdictNode: 2分
```

**G-Eval vs DAG Eval 对比：**

| 特性 | G-Eval | DAG Eval |
|------|--------|----------|
| **评估方式** | 单个 Prompt | 决策树 |
| **确定性** | 低（依赖 LLM） | 高（结构化） |
| **透明度** | 中等 | 高（可追踪每步） |
| **适用场景** | 主观评估（流畅性、创意性） | 结构化评估（JSON 格式、必须包含某些字段） |
| **调试难度** | 较难 | 容易 |

**DAG Eval 的四大优势：**

| 优势 | 英文 | 说明 |
|------|------|------|
| **确定性** | Determinism | 结构化决策树确保结果可复现 |
| **精细控制** | Granular Control | 开发者可定义明确的检查序列 |
| **结构检查** | Structural Evaluation | G-Eval 难以做"是否符合 JSON schema"这类严格结构检查 |
| **模块化** | Modular Design | 可以在 DAG 中嵌入 G-Eval 节点——结合两者优势 |

> 💡 **最佳实践：** G-Eval 用于主观质量评估 + DAG Eval 用于结构化验证 → **混合使用**最强大。

### 5.3 DeepEval 的完整指标体系

| 类别 | 指标 | 适用场景 |
|------|------|---------|
| **自定义** | G-Eval, DAG Eval | 任意自定义评估 |
| **RAG 检索器** | Contextual Relevancy, Contextual Precision, Contextual Recall | 评估检索器是否找到了对的上下文 |
| **RAG 生成器** | Answer Relevancy, Faithfulness | 评估生成器是否基于上下文正确回答 |
| **Agent** | Task Completion, Tool Correctness | 评估 Agent 是否完成任务、工具是否用对 |
| **多轮对话** | Knowledge Retention, Role Adherence, Conversation Completeness/Relevancy | 评估对话质量和一致性 |
| **多模态** | Image Coherence/Helpfulness, Text-to-Image, Multimodal Relevancy/Faithfulness | 评估图文多模态输出 |
| **安全性** | Bias, Toxicity, Misuse, PII Leakage, Role Violation | 评估安全风险 |

---

## 🗺️ 全局回顾：技术演进路线图

```
┌────────────────────────────────────────────────────────────────┐
│  从"手工评估"到"工业级评估"  —  评估框架与工具全链路             │
│                                                                │
│  序幕：Week 1 回顾                                             │
│  ✅ 已掌握 ROUGE/BLEU/BERTScore + LLM-as-Judge + 偏见缓解     │
│  ❌ 问题：在生产环境中怎么系统化、自动化地执行？                 │
│           │                                                    │
│           ▼                                                    │
│  第一章：可观测性 (Observability)                                │
│  ✅ 让黑盒 LLM 变透明，能回答任意诊断问题                       │
│  ❌ 问题：数据怎么采集？                                        │
│           │                                                    │
│           ▼                                                    │
│  第二章：遥测 (Telemetry) — Spans & Traces                      │
│  ✅ Span = 单次操作；Trace = 完整请求路径                       │
│  ✅ OpenTelemetry 标准 + 三种仪表化方法                         │
│  ❌ 问题：看到数据 ≠ 评估数据，需要自动打分！                    │
│           │                                                    │
│           ▼                                                    │
│  第三章：G-Eval                                                 │
│  ✅ 自动 CoT + 概率加权评分                                     │
│  ✅ 与人类对齐度 > 传统指标（Spearman 0.514 vs 0.3-0.4）       │
│  ❌ 问题：RAG 系统需要特殊的评估指标！                          │
│           │                                                    │
│           ▼                                                    │
│  第四章：RAGAS                                                  │
│  ✅ Faithfulness (幻觉)，Answer Relevance，Context Relevance    │
│  ✅ 检索器和生成器可分别评估                                    │
│  ❌ 问题：需要一个统一的工具整合所有能力！                       │
│           │                                                    │
│           ▼                                                    │
│  第五章：DeepEval                                               │
│  ✅ 30+ 即插即用指标（RAG/Agent/Chat/多模态/安全性）            │
│  ✅ G-Eval（主观）+ DAG Eval（结构化）混合使用                  │
│  ✅ 一站式评估工具箱                                            │
└────────────────────────────────────────────────────────────────┘
```

### 关键概念对比总结

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| 黑盒 LLM → Observability | 让不可见的内部行为变得可观测，支持诊断和优化 |
| 日志 → OpenTelemetry (Spans + Traces) | 结构化遥测数据，标准化采集规范，支持跨平台分析 |
| SDK 仪表化 → Auto/Proxy 仪表化 | 减少代码侵入，实现零/低改动的可观测性 |
| ROUGE/BLEU → G-Eval | 从表面 n-gram 重叠升级为带 CoT 推理的概率加权评估，对齐人类判断 |
| 通用评估 → RAGAS | 为 RAG 系统提供组件级评估（检索器 vs 生成器），精准定位瓶颈 |
| 多框架散装 → DeepEval | 统一 30+ 指标到一个工具箱，支持 RAG/Agent/Chat/多模态/安全性 |
| G-Eval 单 Prompt → DAG Eval 决策树 | 解决 G-Eval 在结构化验证上的不足，提高确定性和可解释性 |

---

## 📋 最佳实践速查（考试必记）

| # | 最佳实践 | 原因 |
|---|---------|------|
| 1 | 先搭建 **Observability** 基础设施，再做评估 | 看不见内部就无法评估 |
| 2 | 用 **OpenTelemetry** 标准化遥测数据 | 厂商中立，避免锁定 |
| 3 | 选对**仪表化方法**（SDK/Auto/Proxy）| SDK 最精细，Proxy 零改动，Auto 是折中 |
| 4 | G-Eval 用**概率加权评分**，不要直接取文字输出 | 概率加权更稳定、更准确 |
| 5 | 评估 RAG 时，用 RAGAS **分别评估检索器和生成器** | 精准定位瓶颈在哪个组件 |
| 6 | **Faithfulness** 指标是检测 hallucination 的直接手段 | V/S = 被验证陈述数 / 总陈述数 |
| 7 | 主观评估用 **G-Eval**，结构化验证用 **DAG Eval** | 各有所长，混合最佳 |
| 8 | 用 **DeepEval** 作为统一评估平台 | 30+ 指标即插即用 |
| 9 | 多云环境下用 OpenTelemetry 作为**统一层** | 避免云厂商锁定 |

---

## 📝 考试/复习重点检查清单

- [ ] 能解释**可观测性 (Observability)** 与**监控 (Monitoring)** 的区别
- [ ] 能说出可观测性对 GenAI 特别重要的**四个原因**
- [ ] 能定义 **Span** 和 **Trace** 并解释它们的关系
- [ ] 能列出一个 Span 包含的主要字段（Name, Parent ID, Timestamps, Attributes, Events, Status）
- [ ] 能列出 OpenTelemetry **语义约定**中用于 GenAI 的标准属性名
- [ ] 能比较三种**仪表化方法**（SDK / Auto / Proxy）的优缺点
- [ ] 能解释 **G-Eval** 的三步流程（设计 Prompt → 自动 CoT → 概率加权）
- [ ] 能写出 G-Eval 的**概率加权评分公式** $score = \sum p(s_i) \cdot s_i$
- [ ] 能说出 G-Eval 相比 ROUGE/BLEU 在人类对齐度上的优势
- [ ] 能解释 **RAG** 的基本架构（Retriever + Generator）
- [ ] 能说出 RAG 评估面临的**四大挑战**
- [ ] 能定义 RAGAS 的**三大核心指标**（Faithfulness, Answer Relevance, Context Relevance）并写出公式
- [ ] 能解释 **Faithfulness** 如何直接衡量 hallucination
- [ ] 能区分 RAGAS 指标中哪些评估**检索器**、哪些评估**生成器**
- [ ] 能说出 **DeepEval** 的**六大能力**
- [ ] 能比较 **G-Eval vs DAG Eval** 的适用场景
- [ ] 能列出 DeepEval 的**六大指标类别**（自定义、RAG、Agent、对话、多模态、安全性）
- [ ] 能说出 DAG Eval 相比 G-Eval 的**四大优势**（确定性、精细控制、结构检查、模块化）

---

## 📚 参考资料

- [Week2_slides.md](Week2_slides.md) — 原始 slides 格式化笔记
- [Module2.1-Evaluation-Frameworks-and-Tools.md](Module2.1-Evaluation-Frameworks-and-Tools.md) — 课程 Notebook 详细笔记
- Module2.1-Evaluation-Frameworks-and-Tools.ipynb — 课程 Notebook
- Course: CST8510 Artificial Intelligence Software Development
- Instructor: Dr. Hari M Koduvely
- G-Eval Paper: "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"
- RAGAS Paper: "RAGAS: Automated Evaluation of Retrieval Augmented Generation"
- OpenTelemetry Documentation: https://opentelemetry.io/docs/
- DeepEval Documentation: https://docs.confident-ai.com/
