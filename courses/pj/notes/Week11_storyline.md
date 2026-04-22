# Week 11 故事线：让 LLM "自己变更好"——从手写提示到自动优化，从粗暴检索到精准 RAG

> **Source:** `26W-CST8510-Week11-Lecture1.pdf`
> **核心主题：** 不微调模型权重，如何让 LLM 的输出质量持续提升？答案是两条路：优化提示（Prompt Optimization）和优化知识检索（Advanced RAG）。
> **故事线：** LLM 的"自我进化"——从人工写提示 → 让 LLM 自己优化提示 → 让 LLM 自己检查输出 → 让检索系统也变聪明

---

## 🎬 序幕：我们在解决什么问题？

你训练好了一个 LLM（或者直接用 GPT-4），但发现它的表现不够好：

- 同一个数学题，问三次得到三个不同答案——**输出不稳定**
- 提示写得不好，模型表现差——**提示质量依赖人工经验**
- 用 RAG 检索知识，但检索回来的文档不相关——**检索精度差**
- 模型"一本正经地胡说八道"，但它自己不知道——**缺乏自我纠错能力**

> 💡 **核心问题：不动模型权重（不微调），怎么让 LLM 变得更好？**

传统做法是微调（Fine-tuning），但微调需要大量标注数据、GPU 算力和工程投入。本周介绍的方法都属于 **"免微调优化"**——只改变输入（提示）、推理过程（反思）和外部知识获取方式（RAG）：

| 优化维度 | 核心思想 | 代表技术 |
|----------|----------|----------|
| ① 提示优化 (Prompt Optimization) | 改进"问问题的方式" | Self-Consistency, OPRO |
| ② 自反思 (Self-Reflection) | 让 LLM "检查自己的作业" | Feedback-Driven Reflexion, Implicit Reflexion |
| ③ 高级 RAG (Advanced RAG) | 改进"查资料的方式" | 智能分块, 句子窗口检索, 混合搜索, 重排序, 嵌入微调 |

---

## 📚 第一章：提示优化——从"人工调参"到"LLM 自己调"

### 1.1 为什么需要提示优化？

> 🔑 **提示（Prompt）是 LLM 的"方向盘"——方向盘歪了，再强的引擎也跑偏。**

一个事实：同一个 LLM，给它不同的提示，回答质量天差地别。例如：

- ❌ 差提示："What is 15% of 240?" → 模型可能直接猜一个数
- ✅ 好提示："What is 15% of 240? Let's think step by step." → 模型会列出计算过程，正确率飙升

手动写提示有两个致命问题：
1. **依赖人工经验**——好提示需要反复试错，效率低
2. **不可迁移**——在任务 A 上好用的提示，在任务 B 上可能完全不行

所以我们需要 **自动化提示优化**。

### 1.2 方法一：Self-Consistency（自一致性）——投票消除随机性

**一句话定义：** 同一个问题问 N 次，多数投票选答案。

**原理：**

```
Self-Consistency 流程：

  同一个问题 Q
       │
       ├──→ 推理路径 1 → 答案 A
       ├──→ 推理路径 2 → 答案 B
       ├──→ 推理路径 3 → 答案 A
       ├──→ 推理路径 4 → 答案 A
       └──→ 推理路径 5 → 答案 C
                               │
                               ▼
                    多数投票：A 得票 3/5 → 最终答案 = A
```

**为什么有效？** LLM 的输出有随机性（temperature > 0），但正确推理路径在多次采样中出现频率更高——就像"三个臭皮匠赛过诸葛亮"。

**局限性：**
- 需要多次推理 → 计算成本线性增长
- 所有路径都错的情况下，投票也救不了

### 1.3 进阶：Uncertainty Thresholding（不确定性阈值）——知道自己"不知道"

在 Self-Consistency 基础上加一个"守门员"：

```
改进流程：

  Self-Consistency → 得到投票结果
       │
       ├── 一致性 ≥ 阈值 (如 80%) → ✅ 直接返回答案（高置信）
       │
       └── 一致性 < 阈值           → ⚠️ 拒绝回答 / 交给人类处理（低置信）
```

> 💡 **记忆技巧：** Self-Consistency = 投票选答案；Uncertainty Thresholding = 投票 + 如果票数太分散就弃权。关键能力是 **"知道自己不知道"**，避免"一本正经胡说八道"。

### 1.4 方法二：OPRO（Optimization by PROmpting）——让 LLM 自己优化提示

Self-Consistency 解决了"输出不稳定"的问题，但没有解决"提示本身可能不好"的问题。

> 🔑 **故事转折点：** Self-Consistency 只能在给定提示下选最优答案，但如果提示本身就不好呢？→ 我们需要一种方法来 **自动发现更好的提示** → OPRO 登场！

**一句话定义：** 用 LLM 自身作为优化器，迭代生成更好的提示。

**OPRO 三大组件：**

| 组件 | 角色 | 比喻 |
|------|------|------|
| **Meta-Prompt（元提示）** | 包含问题描述 + 历史提示及评分 | 考试资料包 |
| **LLM（优化器）** | 根据历史信息生成新提示 | 学生 |
| **Objective Function（目标函数）** | 评估新提示的效果并打分 | 老师 |

**迭代过程：**

```
OPRO 循环（像师生互动）：

  ┌─────────────────────────────────────────────────┐
  │  Round 1:                                       │
  │  学生写提示 → "Solve this problem" → 老师打 60 分│
  │                                                 │
  │  Round 2:                                       │
  │  学生看到 Round 1 的 60 分，改进 →              │
  │  "Break this down." → 老师打 79.9 分            │
  │                                                 │
  │  Round 3:                                       │
  │  学生看到前两轮的分数，继续改进 →               │
  │  "Take a deep breath and work on this problem   │
  │   step-by-step." → 老师打 80.2 分               │
  │                                                 │
  │  → 收敛！最优提示 = "Take a deep breath..."     │
  └─────────────────────────────────────────────────┘
```

**惊人发现（来自 GSM8K 实验数据）：**

| 排名 | OPRO 发现的提示词 | 准确率 |
|:---:|------|:---:|
| 🥇 | "Take a deep breath and work on this problem step-by-step." | **80.2** |
| 🥈 | "Break this down." | 79.9 |
| 🥉 | "A little bit of arithmetic and a logical approach will help us quickly arrive at the solution to this problem." | 78.5 |
| 4 | "Let's combine our numerical command and clear thinking to quickly and accurately decipher the answer." | 74.5 |

这些提示都包含 **"分步思考"** 的核心思想（CoT 的本质），但 OPRO 能自动发现最优措辞——**LLM 能自动发现甚至超越人类手动设计的提示**。

### 1.5 ❗ 提示优化的局限——只改"问法"不够

提示优化的本质是改进"怎么问问题"，但它有一个根本局限：

- **无法纠正模型自身的知识错误**——如果模型的训练数据中没有某个知识，再好的提示也问不出来
- **无法改进推理逻辑**——模型的推理能力是训练期间固化的

> 🔑 **故事转折点：** 提示优化能改进"问法"，但模型的回答还可能有事实错误或逻辑漏洞。如何让模型自己检查并修正这些问题？→ **自反思（Self-Reflection）**登场！

---

## 🎭 第二章：自反思——让 LLM "检查自己的作业"

### 2.1 为什么需要反思？（Self-evaluation: Reflexion）

人类学习的一个关键能力是"反思"——写完作文回头检查一遍，发现错误后修改。LLM 也可以做到这一点。

反思解决的核心问题：**当 ground truth 不可获取时，如何迭代逼近高置信度输出？**

**三大用途**（来自 slides）：
- a. **纠正错误** — 尤其适用于多步推理或代码生成任务
- b. **提升输出质量** — 尤其针对需求满足度
- c. **增强上下文理解** — 通过对解读的评估

**Reflexion 的工作流程**：

```
Reflexion 循环：

  Task → Proposed Solution → Test Generation → Internal Tests → Self-reflection
                                                                      │
                                                                      ▼
                                                               Refined Solution → Output
```

### 2.2 方法一：Feedback-Driven Reflexion（反馈驱动的反思）

**定义：** 由用户负面反馈触发的迭代修改，基于自评的结构化修正。

**工作流程（以航班延误客服为例）：**

```
Feedback-Driven Reflexion：

  用户问："My flight has been delayed. Where can I go for more info?"
       │
       ▼
  LLM 初始回答（❌ 质量差）："Please visit our Flight Status page."
       │
       ├── 用户标记 "Poor (General)" ──→ 修正提示：提升 relevance + specificity
       │
       └── 用户标记 "Incomplete (Specific)" ──→ 修正提示：提升 completeness + accuracy
       │
       ▼
  LLM 改进后回答（✅ 高质量）：
  1. Airport Website — 查看实时航班状态
  2. Airline Kiosk — 咨询机场代理
  3. Airport Information Screens — 查看出发/到达信息屏
```

> 💡 **类比：** 就像餐馆服务——客人说"不好吃"（👎），厨师才去改菜。

### 2.3 方法二：Implicit Reflexion（隐式反思）——自动自检

**定义：** 在所有请求发送给用户之前，自动进行自评审查（无需用户反馈触发）。

**工作流程：**

```
Implicit Reflexion：

  用户问："My flight has been delayed. Where can I go for more info?"
       │
       ▼
  LLM 初始回答（🟡 待审查）："Please visit our Flight Status page."
       │
       ▼
  ┌── Hidden Self-Reflection Layer ──────────────────────────────────┐
  │  "Evaluate the relevance of your response...                    │
  │   Offer a more specific and helpful solution IF NECESSARY."     │
  └──────────────────────────────────────────────────────────────────┘
       │
       ▼
  LLM 改进后回答（✅ 高质量）：同样生成 3 条具体建议
```

> 💡 **关键区别：** 注意 "**if necessary**" — 只有自评发现问题时才修改，不是每次都改。

### 2.4 两种反思方法对比

| 维度 | Feedback-Driven Reflexion | Implicit Reflexion |
|------|:---:|:---:|
| 触发方式 | 用户负面反馈（👍/👎） | 自动（每次回答前） |
| 额外开销 | 低（只在用户不满时触发） | 高（每次请求都多一步） |
| 响应延迟 | 二次请求时增加 | 首次请求就增加 |
| 质量保证 | 事后补救 | 事前预防 |
| 适用场景 | 聊天界面、对话系统 | 关键业务、不允许低质量输出 |

### 2.5 ❗ 反思的局限——模型的知识边界

反思能修正推理过程中的错误，但无法弥补 **模型训练数据中缺失的知识**。

- 例如：模型不知道"2024 年谁赢了奥运会 100 米金牌"，反思 100 次也不会凭空产生这个知识。

> 🔑 **故事转折点：** 提示优化改进了"问法"，反思改进了"推理过程"，但模型本身的知识是有限的。如何让模型获取它不知道的知识？→ **RAG（检索增强生成）** 是答案。但标准 RAG 检索质量不够好 → 我们需要 **高级 RAG** 技术！

---

## 📖 第三章：高级 RAG——让"查资料"也变聪明

### 3.1 回顾：Naive RAG 的流程与问题

标准 RAG 的四步流程：

```
Naive RAG：

  文档集 ──→ ① 分块（Chunking）──→ ② 嵌入（Embedding）──→ 向量数据库
                                                               │
  用户查询 ──→ 嵌入 ──→ 向量检索 ──→ ③ 取 Top-K 文档 ──→ ④ LLM 生成回答
```

每一步都可能出问题：

| 步骤 | Naive RAG 的问题 | 后果 |
|------|-----------------|------|
| ① 分块 | 固定大小切割 → 在句子中间截断 | 检索到不完整的信息 |
| ② 嵌入 | 通用嵌入模型 → 不懂领域术语 | 语义匹配不准 |
| ③ 检索 | 单一检索方式 → 关键词或语义只取其一 | 漏掉相关文档 |
| ④ 生成 | 无排序机制 → 不相关文档混入 | LLM 生成错误回答 |

### 3.2 改进一：更智能的分块（Better Chunking）

分块是 RAG 的 **第一步，也是影响最大的一步**——如果文档切得不好，后续再怎么优化也挽救不了。

**五种分块策略（从简单到智能）：**

| 分块策略 | 原理 | 优势 | 劣势 |
|----------|------|------|------|
| **Fixed-size** | 按固定 token 数切割 + 重叠窗口 | 简单、快速 | 可能截断句子 |
| **Recursive** | 按 `\n\n` → `\n` → `.` 逐级递归拆分 | LangChain 默认方法，效果不错 | 仍基于格式而非语义 |
| **Document-based** | 利用文档结构（Markdown 标题/HTML 标签） | 尊重文档原始结构 | 依赖文档有清晰结构 |
| **Semantic** | 计算相邻句子嵌入相似度，骤降处切割 | 按语义分组，质量高 | 计算成本高 |
| **Agentic** | 用 LLM 判断分块边界 | 最智能 | 最慢、最贵 |

> 💡 **记忆口诀：** "固递文语智"——从固定到递归到文档到语义到智能，逐级升级。

**核心原则：好的分块 = 每个 chunk 包含完整的一个语义单元。**

### 3.3 改进二：扩展上下文窗口（Extending Context Window）

最"暴力"的改进：用更大的上下文窗口，一次性塞入更多检索文档。

- GPT-3.5 上下文 = 4K tokens → GPT-4 Turbo = 128K tokens → Gemini = 1M tokens

**优势：** 简单粗暴，不需要改架构。

**致命问题——"Lost in the Middle"（中间丢失）：**
- 研究发现 LLM 对输入的 **开头和结尾** 关注度高
- **中间部分** 的信息容易被忽略
- 塞进去的文档越多，中间部分的利用率越低

> 💡 **类比：** 就像看一篇 100 页的论文，你记得开头摘要和最后结论，但中间第 47 页的内容基本忘了。

### 3.4 改进三：混合搜索（Hybrid Search）

Naive RAG 只用一种检索方式（通常是语义搜索），但 **不同类型的查询适合不同的检索方式**：

| 查询类型 | 最佳检索方式 | 例子 |
|----------|-------------|------|
| 精确术语 | 关键词搜索 (BM25) | "Error code 0x800F0922" |
| 概念理解 | 语义搜索 (Dense Retrieval) | "如何解决安装失败" |
| 混合需求 | 两者结合 | "Docker container networking 常见问题" |

**Hybrid Search = 关键词搜索 + 语义搜索 + 分数融合**

融合方法：**Reciprocal Rank Fusion (RRF)** — 将两种搜索各自的排名进行加权合并，取综合排名最高的文档。

> 💡 **类比：** 关键词搜索像字典查词——精确但死板；语义搜索像问专家——理解意思但可能"跑题"。Hybrid = 字典 + 专家一起查，互补短板。

### 3.5 改进四：重排序（Reranking）——两阶段检索

这是 Advanced RAG 中 **效果最显著** 的改进。

> 🔑 **核心洞察：** 初始检索需要"快"（从百万文档中筛出 Top-100），精排需要"准"（从 Top-100 中选出 Top-5）。两种需求需要 **两种不同的模型**。

**两阶段流水线：**

```
两阶段检索：

  Stage 1: 初始检索（Bi-Encoder）— 快速
  ┌───────────────────────────────────────┐
  │  Query → Encoder → Query 向量        │
  │  Doc   → Encoder → Doc 向量          │  各自独立编码
  │  → 余弦相似度 → Top-K 候选           │
  └───────────────────────────────────────┘
           │
           ▼ Top-K 候选文档（如 100 篇）
  Stage 2: 重排序（Cross-Encoder）— 精准
  ┌───────────────────────────────────────┐
  │  [Query + Doc₁] → Encoder → Score₁   │
  │  [Query + Doc₂] → Encoder → Score₂   │  拼接后联合编码
  │  ...                                  │
  │  → 按 Score 排序 → Top-N 精选        │
  └───────────────────────────────────────┘
```

**Bi-Encoder vs Cross-Encoder 深度对比：**

| 维度 | Bi-Encoder | Cross-Encoder |
|------|:---:|:---:|
| 编码方式 | Query, Doc **分别**编码 | Query+Doc **拼接后联合**编码 |
| 速度 | ✅ 快（Doc 向量可预计算） | ❌ 慢（每对 Query-Doc 重新计算） |
| 精度 | ⚠️ 中等（无法捕获深层交互） | ✅ 高（BERT 的注意力机制捕获交叉关系） |
| 使用场景 | 海量候选初筛 | 少量候选精排 |
| 比喻 | 快速筛简历 | 一对一面试 |

**Reranking 的权衡：**
- ✅ 显著提升检索质量
- ❌ 增加延迟（Cross-Encoder 对每对 Query-Doc 都要编码一次）
- ❌ 增加计算成本

### 3.6 改进五：微调嵌入模型（Fine-Tuning Embedding Models）

最后一个改进方向：**让嵌入模型更懂你的领域**。

**问题：** 通用嵌入模型（如 OpenAI text-embedding-ada-002）在标准语料上训练，可能不理解你的领域专有术语。

**例子：**
- 在医学领域，"MI" = Myocardial Infarction（心肌梗塞）
- 在金融领域，"MI" = Market Intelligence（市场情报）
- 通用嵌入模型无法区分这两个"MI"

**解决方案：** 用你的领域数据微调嵌入模型，让它学会领域特定的语义关系。

**为什么微调 Embedding 而不是微调 LLM？**

| 维度 | 微调 Embedding | 微调 LLM |
|------|:---:|:---:|
| 模型大小 | 小（~100M 参数） | 大（~7B+ 参数） |
| 训练成本 | ✅ 低 | ❌ 高 |
| 训练数据 | 少量 query-doc 对 | 大量高质量文本 |
| 改进目标 | 检索精度 | 生成质量 |
| 性价比 | ✅ 极高 | ⚠️ 看场景 |

> 💡 **记忆技巧：** 微调 Embedding = 给搜索引擎换一副"领域眼镜"；微调 LLM = 让"作家"学你的写作风格。前者便宜 100 倍。

---

## 🗺️ 全局回顾：技术演进路线图

```
┌──────────────────────────────────────────────────────────────────────┐
│  LLM "免微调"优化全景图                                              │
│                                                                      │
│  问题1：提示写得不好 → 输出质量差                                    │
│         │                                                            │
│         ▼                                                            │
│  Prompt Optimization（提示优化）                                     │
│  ├── Self-Consistency：多次采样 + 投票                               │
│  ├── Uncertainty Thresholding：投票 + 置信度判断                     │
│  └── OPRO：LLM 自己迭代优化提示                                     │
│         │                                                            │
│         ▼                                                            │
│  问题2：一次性输出有错误 → 需要自我纠正                              │
│         │                                                            │
│         ▼                                                            │
│  Self-Reflection（自反思）                                           │
│  ├── Self-Feedback：自己检查自己（低成本但有盲点）                   │
│  └── External Feedback：外部工具验证（高可靠但需集成）               │
│         │                                                            │
│         ▼                                                            │
│  问题3：模型知识有限 → 需要外部知识                                  │
│         │                                                            │
│         ▼                                                            │
│  Advanced RAG（高级 RAG）                                            │
│  ├── Better Chunking：智能分块 → 保留语义完整性                      │
│  ├── Sentence Window Retrieval：句子级精确匹配 + 扩展上下文窗口     │
│  ├── Hybrid Search：关键词 + 语义双路检索                            │
│  ├── Reranking：Bi-Encoder 初筛 + Cross-Encoder 精排                │
│  └── Fine-tune Embeddings：领域适配嵌入模型（性价比最高）            │
│                                                                      │
│  完整优化链路：                                                      │
│  优化"怎么问" → 优化"推理过程" → 优化"查资料"                        │
│  (提示优化)     (自反思)         (高级 RAG)                          │
└──────────────────────────────────────────────────────────────────────┘
```

### 关键概念对比总结

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| 手动提示 → Self-Consistency | 消除 LLM 输出的随机性 |
| Self-Consistency → Uncertainty Thresholding | 知道自己"不知道"，避免错误输出 |
| 手动提示 → OPRO | 自动发现最优提示，消除人工试错 |
| 一次性输出 → Feedback-Driven Reflexion | 用户反馈触发修正，事后补救 |
| Feedback-Driven → Implicit Reflexion | 自动自检，事前预防，无需用户触发 |
| Character Splitting → Semantic Chunking | 从按字符切 → 按语义聚类，质量提升 |
| 单一检索 → Hybrid Search | 关键词 + 语义互补，覆盖更多查询类型 |
| 无排序 → Reranking | Bi-Encoder 初筛 + Cross-Encoder 精排 |
| 通用嵌入 → Fine-tune Embeddings | 领域适配，性价比远超微调 LLM |

---

## 📝 考试/复习重点检查清单

### 提示优化 (Prompt Optimization)

- [ ] 能解释 **Self-Consistency** 的工作原理（多次采样 + 多数投票）
- [ ] 能解释 **Uncertainty Thresholding** 如何在 Self-Consistency 基础上增加置信度判断
- [ ] 能画出 **OPRO** 的三大组件（Meta-Prompt, LLM Optimizer, Objective Function）及循环流程
- [ ] 能列出 OPRO 在 GSM8K 上的 Top 发现（"Take a deep breath and work on this problem step-by-step." = 80.2）
- [ ] 能说出 Prompt Optimization 的局限性（只改问法，无法弥补知识缺失）

### 自反思 (Self-Reflection)

- [ ] 能对比 **Feedback-Driven Reflexion vs Implicit Reflexion** 的触发方式和适用场景
- [ ] 能解释 Reflexion 的三大用途（纠正错误、提升质量、增强理解）
- [ ] 能画出 Reflexion 的工作流程（Task → Proposed Solution → Test → Self-reflection → Refined Solution）

### 高级 RAG (Advanced RAG)

- [ ] 能列出 Naive RAG 的四步流程及每步可能出现的问题
- [ ] 能列出 **3 种分块策略**（Character Splitting, Unstructured Chunking, Semantic Chunking）及各自优劣
- [ ] 能解释 **Sentence Window Retrieval** 的原理（句子级精确匹配 + 扩展上下文窗口）
- [ ] 能解释 **Hybrid Search** 的原理（关键词 + 语义双路 + RRF 融合）
- [ ] 能对比 **Bi-Encoder vs Cross-Encoder**（速度 vs 精度的权衡）
- [ ] 能画出 **Reranking 两阶段流水线**（Bi-Encoder 初筛 → Cross-Encoder 精排）
- [ ] 能解释为什么 **微调 Embedding 比微调 LLM 更具性价比**
- [ ] 能说出 Reranking 的核心权衡（质量提升 vs 延迟/成本增加）

---

## 📚 参考资料

- [Week11_slides.md](Week11_slides.md) — 原始 slides 格式化笔记
- Course: CST8510 Artificial Intelligence Software Development
- Reference: *Large Language Models as Optimizers* (OPRO paper)
- Reference: *Beyond Fine-tuning Approaches in LLM Optimization* (Superwise)
- Reference: *Advanced RAG Techniques: an Illustrated Overview*
- Reference: *Relevance Revolution: How Re-ranking Transforms RAG Systems*
