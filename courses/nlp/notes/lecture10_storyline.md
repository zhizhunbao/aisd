# Lecture 10 故事线：从"理解语言"到"回答问题"——BERT 与问答系统

> **Source:** `lecture_10_W26.pdf`
> **核心主题：** BERT 让机器真正"读懂"双向上下文；问答系统则在此基础上让机器"读文章、答问题"——从阅读理解到开放域检索的完整进化链
> **故事线：** 从一个只会"向前读"的学生，到一个能"来回看"的阅读高手，再到一个能"翻书找答案"的考试专家

---

## 🎬 序幕：我们在解决什么问题？

想象一场考试。老师给你一篇文章，然后问："Tesla 在学校学的什么语言？"

作为人类，你会怎么做？

1. **读懂文章** —— 不是逐字阅读，而是理解上下文
2. **定位答案** —— 在文章中找到包含答案的那句话
3. **提取答案** —— 把答案（"German"）从句子中抽出来

这就是**阅读理解 (Reading Comprehension)** —— 也是 NLP 中最实用的任务之一。

但要实现这个过程，机器首先需要一个**真正理解语言**的"大脑"。之前课程中学到的 RNN、LSTM 都有一个致命缺陷——它们只能**单向阅读**（从左到右 or 从右到左），无法像人类一样**同时考虑前后文**。

> **核心问题：** 我们需要一个能**双向理解**上下文的语言模型，然后用它来**回答问题**。

答案分两步：
1. 第一步——**BERT**：一个真正双向的语言理解模型
2. 第二步——**问答系统 (QA)**：把 BERT 的理解能力用到"读文章答问题"的实际任务中

---

## 📚 第一章：BERT 的诞生——为什么需要"双向理解"？

### 1.1 从 RNN 到 BERT 的技术演化

回顾 NLP 技术的进化路径：

```
RNN → LSTM → Bi-LSTM → Attention → Encoder-Decoder → Transformer → BERT
```

每一步都在解决前一步的问题：
- **RNN** ❌ 梯度消失，无法记住长距离依赖
- **LSTM** ✅ 用门控机制解决长距离记忆 ❌ 单向，无法利用未来信息
- **Bi-LSTM** ✅ 双向 ❌ 两个方向是独立的，无法真正交互
- **Transformer** ✅ 自注意力实现全局交互 ❌ GPT 等模型只用了 Decoder（单向）
- **BERT** ✅ 只用 Encoder，**真正的双向** —— 每个词同时看到所有前后文

### 1.2 BERT 在 Transformer 家族中的位置

Transformer 发展出两大分支：

| 分支 | 结构 | 代表 | 特点 |
|------|------|------|------|
| **Encoder-only** | 只用编码器 | **BERT**, RoBERTa, ALBERT | 擅长理解（分类、QA） |
| **Decoder-only** | 只用解码器 | GPT, LLaMA, Mistral | 擅长生成（文本补全、对话） |
| **Encoder-Decoder** | 完整结构 | T5, BART | 擅长翻译、摘要 |

> 💡 **关键思想：** BERT 只用 Encoder 不用 Decoder——因为它的目标不是"生成下一个词"，而是"理解整个句子"。GPT 的单向注意力适合生成（一个词接一个词往后写），但 BERT 的双向注意力更适合理解（同时看前后才能准确判断词义）。

### 1.3 一句话定义

**BERT = 来自 Transformer 的双向编码器表示 (Bidirectional Encoder Representations from Transformers)**

核心特征：
- 训练数据：英语 Wikipedia（约 25 亿词）+ BookCorpus（约 8 亿词，11,000 本书）
- 使用 Transformer 的 **Encoder** 部分
- **双向注意力**：每个词都能看到所有前后文

### 1.4 BERT 的实际影响——Google 搜索

BERT 最广为人知的应用是改进了 Google 搜索。在 BERT 之前，搜索引擎主要靠关键词匹配；BERT 引入后，Google 能**理解查询的含义**，而不仅仅是匹配关键词。

> 💡 **例子：** 搜索 "can you get medicine for someone pharmacy"——BERT 之前 Google 可能只匹配 "get medicine" 和 "pharmacy" 两个关键词；BERT 之后能理解"for someone"这个关键上下文，返回"代他人取药"的相关结果。

---

## 🎭 第二章：BERT 的核心机制——从输入到输出

### 2.1 模型结构：Base vs Large

| 配置 | BERT-base | BERT-large |
|------|-----------|------------|
| Transformer 层数 | 12 | 24 |
| 隐藏层维度 | 768 | 1024 |
| 注意力头数 | 12 | 16 |
| 参数总量 | **1.1 亿** (110M) | **3.4 亿** (340M) |

> 💡 **类比：** BERT-base 像一个 12 层楼的办公楼，每层有 12 间会议室（注意力头），每间能容纳 768 人（隐藏维度）。BERT-large 则是 24 层楼、16 间会议室、每间容纳 1024 人——更大、更强但更贵。

### 2.2 输入处理：WordPiece + 特殊 Token

BERT 的输入不是"词"而是"子词片段 (subword)"，使用 **WordPiece 算法**：

**Step 1: WordPiece 分词**
- 词汇表大小约 30,500
- 常见词保持完整：`the`, `cat`, `is`
- 罕见词拆成子词：`embeddings` → `em`, `##bed`, `##ding`, `##s`

**Step 2: 添加特殊 Token**
- `[CLS]` —— 放在输入开头，用于整句分类
- `[SEP]` —— 分隔句子对（如问题和段落）
- `[MASK]` —— 用于预训练时掩码
- `[PAD]` —— 填充到固定长度

**Step 3: 三层嵌入叠加**

BERT 的输入嵌入 = Token 嵌入 + 段落嵌入 + 位置嵌入

| 嵌入层 | 作用 | 解释 |
|--------|------|------|
| **Token Embedding** | 词义 | 每个 token 的语义表示 |
| **Segment Embedding** | 句子归属 | 区分 Sentence A 和 Sentence B |
| **Position Embedding** | 位置 | 告诉模型每个 token 在第几位 |

### 2.3 特殊 Token ID

| Token | ID |
|-------|-----|
| `[PAD]` | 0 |
| `[UNK]` | 100 |
| `[CLS]` | 101 |
| `[SEP]` | 102 |
| `[MASK]` | 103 |

### 2.4 输出表示

BERT 对每个输入 token 输出一个向量，但最关键的是：

**`[CLS]` token 的输出向量 = 整个输入句子的浓缩表示**

> 💡 **直觉：** `[CLS]` 像班长——它听了所有同学（token）的发言后，代表全班做总结。文本分类任务就是把这个"总结"送进分类器。

---

## 📖 第三章：BERT 的训练秘密——两大"自主学习"任务

### 3.1 预训练 vs 微调：两阶段训练范式

BERT 的训练是一个**两阶段过程**：

| 阶段 | 目的 | 数据 | 成本 |
|------|------|------|------|
| **① 预训练 (Pre-training)** | 学习通用语言知识 | Wikipedia + BookCorpus（无标注） | 极高（Google 用 64 块 TPU） |
| **② 微调 (Fine-tuning)** | 适配特定任务 | 任务特定的标注数据（少量） | 低（普通 GPU 几小时） |

> 💡 **类比：** 预训练就像从小学到大学的通识教育——你学会了"how language works"；微调就像入职培训——只需要少量培训就能胜任特定岗位（情感分类、问答等）。

### 3.2 预训练任务一：掩码语言模型 MLM (Masked Language Modelling)

**核心思想：** 随机遮住一些词，让 BERT 猜被遮住的是什么。

具体操作——随机选取 **15%** 的 token 进行处理：
- **80%** 替换为 `[MASK]`：`went to the store` → `went to the [MASK]`
- **10%** 替换为随机词：`went to the store` → `went to the running`
- **10%** 保持不变：`went to the store` → `went to the store`

> 💡 **为什么不是 100% 都替换为 [MASK]？** 因为微调时不会看到 `[MASK]`，如果预训练时只见 `[MASK]`，模型会出现**训练-推理不匹配 (train-test mismatch)**。加入 10% 随机词和 10% 原词，让模型学会对**所有位置**保持"警觉"。

> 💡 **这就是 BERT "双向"的核心：** 要猜出 [MASK] 位置的词，模型必须**同时看左边和右边**的上下文。不像 GPT 只能看左边（因为 GPT 是自回归的，生成时还没有右边的词）。

### 3.3 预训练任务二：下一句预测 NSP (Next Sentence Prediction)

**核心思想：** 给两个句子，判断 B 是不是 A 的下一句。

| 输入 | 标签 |
|------|------|
| **Sentence A:** The man went to the store. **Sentence B:** He bought a gallon of milk. | **IsNext** ✅ |
| **Sentence A:** The man went to the store. **Sentence B:** Penguins are flightless birds. | **NotNext** ❌ |

**为什么需要 NSP？** 因为很多 NLP 任务需要理解**句子之间的关系**：
- 问答系统需要判断"这个段落是否包含答案"
- 自然语言推理需要判断"前提是否推出结论"

### 3.4 预训练总损失

**总损失 = MLM 损失 + NSP 损失**

两个任务**同时训练**，让 BERT 同时学会：
1. 理解词在上下文中的含义（MLM）
2. 理解句子之间的逻辑关系（NSP）

---

## 📹 第四章：迁移学习与微调——"学一次，用百次"

### 4.1 迁移学习的核心思想

**迁移学习 (Transfer Learning)** 的本质：
- 在大数据上学习**通用能力**（预训练）
- 用小数据**迁移到特定任务**（微调）

```
预训练模型               微调后模型
(对语言没有认知)  ──训练──→  (对语言有很好的理解)  ──微调──→  不同 NLP 任务
                    Wikipedia                    少量标注数据   ├── 情感分析
                    BookCorpus                                  ├── 命名实体识别
                                                                ├── 文本分类
                                                                └── 问答系统 ← 重点！
```

> 💡 **为什么迁移学习革命性？** 在 BERT 之前，每个 NLP 任务都需要从头训练一个模型。BERT 之后，只需一个通用预训练模型 + 少量微调数据就能达到各任务的 SOTA。这就像 ImageNet 预训练对计算机视觉的影响一样深远。

### 4.2 BERT 用于文本分类

文本分类是 BERT 最直接的应用之一：
1. 取 `[CLS]` token 的输出向量（整句表示）
2. 接一个线性分类层
3. 用目标任务的标注数据微调

### 4.3 BERT 变体

| 变体 | 特点 | 指标 |
|------|------|------|
| **BERT-base/large** | 原始版本 | 基准 |
| **DistilBERT** | 知识蒸馏压缩版 | **97%** 性能 / **40%** 更少内存 / **60%** 更快 |
| **BERT-Multilingual** | 多语言版本 | 支持 104 种语言 |

> 💡 **DistilBERT 的价值：** 在移动端和边缘设备上，原始 BERT 太大跑不动。DistilBERT 通过**知识蒸馏 (Knowledge Distillation)** —— 让小模型模仿大模型的行为 —— 实现了几乎无损的压缩。

> 🔑 **故事转折点：** BERT 让机器具备了强大的"阅读理解能力"——它能理解句子的含义、词的上下文。但光能"读懂"还不够，我们还需要机器能**用这种理解能力去回答具体问题**。这就引出了本课的第二大主题——问答系统 (Question Answering)！

---

## 🎭 第五章：问答系统——让机器"回答问题"

### 5.1 问答系统的分类法

问答系统可以从三个维度分类：

**① 按信息源 (Information Source)：**

| 类型 | 数据源 | 示例 |
|------|--------|------|
| **结构化数据** | SQL/NoSQL 数据库 | 查询员工薪资 |
| **非结构化文本** | Wikipedia、新闻、论文 | 搜索医学文献 |
| **对话数据** | 客服日志、论坛、社交媒体 | Stack Overflow 搜索 |

**② 按问题类型 (Question Types)：**

| 类型 | 说明 | 示例 |
|------|------|------|
| **事实型 (Factoid)** | 有明确答案 | "法国首都是哪里？" |
| **开放域 (Open Domain)** | 任意领域 | "黑洞是怎么形成的？" |
| **封闭域 (Closed Domain)** | 特定领域 | "这个药的副作用是什么？" |
| **复杂/叙事型 (Complex)** | 需要推理 | "描述二战的原因和影响" |

**③ 按答案类型 (Answer Types)：**

| 类型 | 答案来源 |
|------|---------|
| **抽取式 (Extractive)** | 直接从原文中**复制**一个片段 |
| **摘要式/生成式 (Abstractive/Generative)** | 模型**自己组织**语言回答 |
| **事实型 (Factoid)** | 简短事实：名字、日期、数字 |

### 5.2 主要 QA 范式

| 范式 | 代表技术 |
|------|---------|
| **抽取式 QA** | SQuAD + BERT |
| **基于知识的 QA** | 知识图谱查询 |
| **混合方法 QA** | 检索 + 推理 |
| **生成式 QA** | GPT 系列直接生成答案 |
| **检索增强 QA / RAG** | 检索文档 + LLM 生成 |

> 🔑 **关键选择：** 本课聚焦**抽取式 QA**——因为它和 BERT 直接相关，而且是最基础的 QA 范式。后续课程（Lecture 12）将深入 RAG。

---

## 📖 第六章：抽取式 QA——"在文章里找答案"

### 6.1 什么是阅读理解？

**阅读理解 = 给定一段文字 P 和一个问题 Q，在 P 中找到答案 A**

公式表示：**(P, Q) → A**

其中 A 是 P 中的一个**连续片段（跨度 span）**。

> 💡 **直觉：** 就像你做英语阅读理解——文章（Passage）给了你所有信息，问题（Question）告诉你要找什么，答案（Answer）一定在文章里——你只需要**定位**它。

### 6.2 IBM Watson 与 Jeopardy！ —— QA 的里程碑

2011 年，IBM Watson 在 Jeopardy! 节目中击败人类冠军。这是 QA 系统走入公众视野的标志性事件。Watson 使用的是传统的混合架构（检索 + 排序 + 推理），而如今 BERT 类模型极大简化了这个过程。

### 6.3 SQuAD 数据集——QA 的"ImageNet"

**SQuAD (Stanford Question Answering Dataset)** 是 QA 领域最重要的数据集：

| 维度 | 数值 |
|------|------|
| 标注三元组 | 10 万个 (passage, question, answer) |
| 段落来源 | 英语 Wikipedia |
| 段落长度 | 通常 100~150 词 |
| 问题来源 | 众包生成 |
| 答案特点 | 段落中的一个**文本跨度** |

### 6.4 评估指标：EM 与 F1

| 指标 | 含义 | 计算方式 |
|------|------|---------|
| **EM (Exact Match)** | 预测是否与金标准**完全一致** | 完全匹配 = 1, 否则 = 0 |
| **F1 Score** | 预测与金标准的**部分匹配**程度 | 基于 token 级别的精确率和召回率 |

**具体示例：**

- **Q:** What did Tesla do in December 1878?
- **Gold Answers:** {`left Graz`, `left Graz ans`, `left Graz and severed all relations with his family`}
- **Prediction:** `left Graz and severed`

| 指标 | 计算 | 结果 |
|------|------|------|
| EM | max{0, 0, 0} | **0**（和三个金标准都不完全匹配） |
| F1 | max{0.67, 0.67, 0.61} | **0.67**（和第一个金标准部分匹配） |

> 💡 **为什么两个指标都需要？** EM 太严格——"left Graz" 和 "left Graz and severed" 意思差不多但 EM=0。F1 给部分正确的预测一个合理的分数。实际评估中两个指标一起看。

---

## 🏆 第七章：用 BERT 做阅读理解——从 BiDAF 到 BERT

### 7.1 问题建模

**输入：**
- 段落 C = (c₁, c₂, …, cₙ)
- 问题 Q = (q₁, q₂, …, qₘ)，其中 M < N

**输出：** 答案的**起始位置 (start)** 和**结束位置 (end)**

> 💡 **关键洞察：** 抽取式 QA 本质上是一个**指针问题**——模型不需要"生成"答案，只需要在段落中**指出答案在哪**（从第几个 token 到第几个 token）。

### 7.2 BiDAF：BERT 之前的方案

**BiDAF (Bidirectional Attention Flow)** 是 BERT 之前最有影响力的 QA 模型：

架构：Encoding → Attention → Modeling
性能：EM 71.3%, F1 81.2%

但 BiDAF 使用的是 Bi-LSTM + 注意力机制，计算效率和理解深度都不如后来的 BERT。

### 7.3 BERT 做阅读理解的方法

BERT 做 QA 的方式非常优雅：

**输入格式：** `[CLS] Question [SEP] Passage [SEP]`

**预测起始位置：**
- 对段落中每个 token 的输出向量，用一个**起始向量 S** 做点积
- Softmax 归一化后，得分最高的位置就是答案的**开始**

**预测结束位置：**
- 同理，用一个**结束向量 E** 做点积
- 得分最高的位置就是答案的**结束**

> 💡 **直觉：** 想象你用两只荧光笔在文章上划线——一只标"起点"，一只标"终点"。BERT 就是同时学会了"在哪开始划"和"在哪停止划"。

### 7.4 模型对比——SQuAD 2.0 排行榜

| 模型 | F1 | EM |
|------|-----|-----|
| BiDAF | 77.3 | 67.7 |
| **BERT-base** | 88.5 | 80.8 |
| **BERT-large** | 90.9 | 84.1 |
| XLNet | 94.5 | 89.0 |
| RoBERTa | 94.6 | 88.9 |
| ALBERT | 94.8 | 89.3 |

> 💡 **关键观察：**
> - BERT 比 BiDAF F1 提升了 **11+ 个百分点** —— 这是一个巨大的飞跃
> - BERT 之后的变体（XLNet, RoBERTa, ALBERT）进一步优化，F1 达到 94+
> - 这些后续模型都是在 BERT 的双向预训练思路上改进的

> 🔑 **故事转折点：** BERT 在阅读理解上表现很好——但 SQuAD 的段落只有 100~150 词。真实世界的文档可能有**成千上万词**怎么办？而且如果我们不知道答案在**哪篇文章**里呢？这两个问题引出了下一章的内容！

---

## 📚 第八章：处理长文本与开放域 QA

### 8.1 长文本处理——滑动窗口策略

BERT 有 **512 token** 的最大输入限制。当段落超过这个长度时，使用**滑动窗口 (Sliding Window)** 策略：

```python
inputs = tokenizer(
    examples["question"],
    examples["context"],
    max_length=500,          # 最大 token 长度
    truncation="only_second", # 只截断上下文，不截断问题
    stride=25,               # 滑动窗口步长 —— 相邻窗口之间重叠
    return_overflowing_tokens=True,  # 返回溢出的 token
)
```

关键参数：
- `max_length=500`：给问题留出空间（因为问题 + 段落共享 512 token 限额）
- `truncation="only_second"`：永远不截断问题（问题通常短，段落长）
- `stride=25`：相邻窗口重叠 25 个 token，避免答案被截断

> 💡 **类比：** 就像用一个放大镜阅读长文章——放大镜一次只能看一段（窗口），看完后往下移（滑动），但每次跟上一次有一点重叠（stride），确保不遗漏。

### 8.2 从抽取式 QA 到开放域 QA

到目前为止，我们假设"答案一定在给定的段落里"。但如果没有给段落呢？

**开放域 QA (Open Domain QA)** 需要先**找到**包含答案的文档，然后再**提取**答案。这就引出了**检索器-阅读器架构 (Retriever-Reader Architecture)**。

### 8.3 检索器-阅读器架构

```
用户问题 → 检索器 (Retriever) → 候选文档 → 阅读器 (Reader) → 答案
              │                                  │
              │ 在文档库中找到                     │ 在候选文档中定位
              │ 最相关的 k 篇文档                  │ 答案的精确位置
              ▼                                  ▼
         语义搜索                            BERT QA 模型
```

### 8.4 嵌入方法与密集检索

检索器需要将文档和查询都转为**向量**，然后通过**语义相似度**匹配：

| 嵌入方法 | 特点 | 时代 |
|---------|------|------|
| **Word2Vec** | 静态词向量，不考虑上下文 | 2013 |
| **GloVe** | 基于共现矩阵的静态词向量 | 2014 |
| **BERT** | 上下文相关的动态词向量 | 2019+ |

### 8.5 DPR：密集段落检索

**DPR (Dense Passage Retrieval)** 是 Facebook 提出的高效检索方法：

**核心思想：** 用**两个独立的 BERT 编码器**——一个编码问题，一个编码段落——分别生成向量，然后比较相似度。

| 组件 | 功能 |
|------|------|
| **问题编码器 (Question Encoder)** | 将问题转为向量 q |
| **段落编码器 (Passage Encoder)** | 将段落转为向量 p |
| **相似度计算** | sim(q, p) = q·p（点积） |

**双编码器架构的优势：**
- 段落向量可以**离线预计算**并存入向量数据库
- 查询时只需编码问题 + 最近邻搜索
- 检索速度快

> 💡 **DPR vs 传统关键词检索 (TF-IDF/BM25)：** 传统检索靠词汇重叠——"what is the capital of France" 和 "Paris is the capital of France" 有词重叠所以匹配。但 DPR 能理解语义——"法国首都是哪里" 虽然没有词重叠，但语义相同也能匹配。

---

## 📹 第九章：QA 框架与评估——工程落地

### 9.1 Haystack 框架

**Haystack** 是由 deepset 开发的开源 QA 框架，基于检索器-阅读器架构：

- 与 Hugging Face Transformers 紧密集成
- 抽象了复杂的管道搭建
- 核心组件：Document Store（文档存储）+ Pipeline（处理管道）

类似框架还有：
- **DeepPavlov** —— 俄罗斯开发的对话 AI 框架
- **DrQA** —— Facebook 的开放域 QA 系统

### 9.2 评估方法

QA 系统的评估仍然使用 **EM** 和 **F1** 两大指标——和 SQuAD 评估方式一致。

---

## 🚀 第十章：超越抽取式 QA——通向 RAG 的未来

抽取式 QA 有一个根本局限：**答案必须是原文中的一个片段**。但有些问题的答案需要**综合多段信息**或**用自己的话总结**：

| 方式 | 特点 | 局限 |
|------|------|------|
| **抽取式 QA** | 从原文复制片段 | 答案必须是原文子串 |
| **生成式 QA** | 模型自己组织语言 | 可能产生幻觉 |
| **RAG** | 检索 + 生成 | ✅ 综合了两者优势 |

> **RAG (Retrieval-Augmented Generation, 检索增强生成)** = 先检索相关文档（像抽取式 QA 的检索器），再让 LLM 基于检索到的文档**生成**答案（像生成式 QA）。

这就是 Lecture 12 将深入讲解的内容。

---

## 🗺️ 全局回顾：技术演进路线图

```
┌────────────────────────────────────────────────────────────┐
│                      技术演进路线图                          │
│                                                            │
│  Transformer 家族 (Encoder / Decoder / Enc-Dec)            │
│  ❓ 哪种结构最适合"理解"语言？                              │
│           │                                                │
│           ▼                                                │
│  BERT (Encoder-only, 双向注意力)                            │
│  ✅ 真正的双向上下文理解                                    │
│  ✅ 预训练两大任务：MLM + NSP                               │
│  ✅ 迁移学习：一次预训练，多任务微调                         │
│  ❌ 只能"理解"不能"回答问题"                                │
│           │                                                │
│           ▼                                                │
│  BERT for QA (阅读理解)                                     │
│  ✅ 预测答案跨度的起止位置                                  │
│  ✅ SQuAD F1 达到 90+                                       │
│  ❌ 只能处理 512 token 的短段落                              │
│           │                                                │
│           ▼                                                │
│  滑动窗口 + 开放域 QA                                       │
│  ✅ 处理长文本（滑动窗口分块）                              │
│  ✅ 检索器-阅读器架构（先找文档再找答案）                    │
│  ✅ DPR 密集段落检索（语义匹配取代关键词匹配）              │
│  ❌ 答案仍必须是原文片段（抽取式）                          │
│           │                                                │
│           ▼                                                │
│  RAG (检索增强生成)                                          │
│  ✅ 检索 + 生成的结合                                       │
│  ✅ 答案可以综合多段信息                                    │
│  🚀 下一站：Lecture 12 深入 RAG                              │
└────────────────────────────────────────────────────────────┘
```

### 技术转换总结

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| **RNN/LSTM → BERT** | 单向阅读 → 双向理解上下文 |
| **从头训练 → 迁移学习** | 每个任务都要大量数据 → 预训练一次、微调多次 |
| **BERT 理解 → QA 应用** | 能理解语言 → 能回答具体问题 |
| **BiDAF → BERT QA** | LSTM+Attention → Transformer，F1 从 77 跳到 90+ |
| **抽取式 QA（固定段落）→ 开放域 QA** | 段落已知 → 先检索文档再提取答案 |
| **关键词检索 → DPR 密集检索** | 词汇匹配 → 语义匹配 |
| **抽取式 QA → RAG** | 只能复制原文 → 检索 + 生成综合回答 |

---

## 📝 考试/复习重点检查清单

- [ ] 能说出 BERT 的全称和核心设计思想（双向、Encoder-only）
- [ ] 能列出 BERT-base 和 BERT-large 的四个配置参数（层数、隐藏维度、注意力头数、参数量）
- [ ] 能解释 WordPiece 分词的作用和词汇表大小
- [ ] 能说出 BERT 输入中四个特殊 Token 的名称和用途（[CLS], [SEP], [MASK], [PAD]）
- [ ] 能解释 BERT 的三层嵌入组成（Token + Segment + Position）
- [ ] 能详细描述 MLM 预训练任务的 80/10/10 策略及其原因
- [ ] 能解释 NSP 任务的目的和训练方式
- [ ] 能区分预训练和微调的目标、数据需求和计算成本
- [ ] 能描述 DistilBERT 相对于 BERT 的性能/效率指标（97%/40%/60%）
- [ ] 能写出阅读理解的公式化定义：(P, Q) → A
- [ ] 能解释 SQuAD 数据集的规模和特点
- [ ] 能手算 EM 和 F1 指标的具体示例
- [ ] 能描述 BERT 做 QA 的方法——预测 start/end 位置
- [ ] 能对比 BiDAF 和 BERT 在 SQuAD 上的性能差距
- [ ] 能解释滑动窗口策略的三个关键参数（max_length, truncation, stride）
- [ ] 能画出检索器-阅读器架构的流程
- [ ] 能解释 DPR 的双编码器架构和它比传统检索的优势
- [ ] 能区分抽取式 QA、生成式 QA 和 RAG 的区别
- [ ] 能列出至少 3 个 QA 框架（Haystack, DeepPavlov, DrQA）

---

## 📚 参考资料

- Devlin et al. (2019). *"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"* — BERT 原始论文
- Seo et al. (2017). *"Bidirectional Attention Flow for Machine Comprehension"* — BiDAF 模型
- Rajpurkar et al. (2016). *"SQuAD: 100,000+ Questions for Machine Comprehension of Text"* — SQuAD 数据集
- Karpukhin et al. (2020). *"Dense Passage Retrieval for Open-Domain Question Answering"* — DPR 论文
- *Natural Language Processing with Transformers*, O'Reilly Media, 2022 — Transformer 家族图谱
- *Hands-on Large Language Models*, O'Reilly — BERT 迁移学习图解
- [Jay Alammar: A Visual Guide to Using BERT](http://jalammar.github.io/a-visual-guide-to-using-bert-for-the-first-time/) — BERT 可视化教程
- [SQuAD Explorer](https://rajpurkar.github.io/SQuAD-explorer/) — SQuAD 排行榜
- Dan Jurafsky, Stanford CS224N — 阅读理解与 QA 课件
- 课程 Slides: `lecture_10_W26.pdf` (60 slides) — Hala Own, Ph.D.
