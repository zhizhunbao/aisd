---
marp: true
theme: default
class: invert
paginate: false
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&display=swap');
  section {
    background: linear-gradient(160deg, #0d1117 0%, #161b22 40%, #1a1f36 100%);
    color: #c9d1d9;
    font-family: 'Noto Sans SC', 'Microsoft YaHei UI', sans-serif;
    font-size: 24px;
    padding: 50px 70px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  h1 { color: #f0c040; font-size: 46px; font-weight: 900; margin-bottom: 12px; }
  h2 { color: #58a6ff; font-size: 34px; font-weight: 700; margin-bottom: 10px; }
  h3 { color: #7ee787; font-size: 26px; font-weight: 700; }
  strong { color: #f0c040; }
  em { color: #d2a8ff; font-style: normal; }
  code { background: rgba(110,118,129,0.2); color: #79c0ff; padding: 2px 6px; border-radius: 6px; font-size: 22px; }
  pre { background: rgba(13,17,23,0.8); border: 1px solid #30363d; border-radius: 12px; padding: 20px; font-size: 20px; line-height: 1.5; }
  pre code { background: none; padding: 0; }
  table { font-size: 20px; margin: 16px auto; border-collapse: collapse; width: 90%; }
  th { background: rgba(88,166,255,0.15); color: #58a6ff; padding: 10px 14px; border-bottom: 2px solid #30363d; }
  td { padding: 8px 14px; border-bottom: 1px solid #21262d; }
  blockquote { border-left: 4px solid #f0c040; background: rgba(240,192,64,0.08); padding: 10px 20px; border-radius: 0 8px 8px 0; margin: 12px 0; font-size: 22px; color: #e6edf3; }
  ul, ol { line-height: 1.7; }
---

# Lecture 10 故事线

## 从 Transformer 到 BERT，从阅读理解到问答系统

> **核心主题：** 如何用一个预训练好的语言理解模型，让机器像人一样阅读文章、回答问题？
> **故事线：** 先造一个"读得懂"的大脑（BERT），再教它"回答问题"的技能（QA）

---

## 🎬 序幕：上一讲留下的悬念

上一讲（Lecture 9）我们学了 Transformer 架构——一个基于自注意力的全并行序列模型。但 Transformer 只是一个**架构蓝图**，它本身不知道任何语言知识。

> 类比：Transformer 是一栋写字楼的建筑图纸，但里面没有员工、没有数据、什么都不会做。

---

## 核心问题

> **怎么把这个空壳架构变成一个真正"懂语言"的模型？**

答案就是 **BERT** —— 用海量文本预训练 Transformer 编码器，让它学会理解语言。

---

# 📚 第一章：BERT

## 给 Transformer 编码器注入语言知识

---

## 1.1 BERT 的核心身份

**BERT = Bidirectional Encoder Representations from Transformers**

> BERT 就是把 Transformer 的**编码器**拿出来，用大量文本预训练，让它成为一个"通用语言理解引擎"。

| 关键词 | 含义 |
|---|---|
| **Bidirectional** | 每个词同时看到左边和右边的所有词（真正的双向注意力）|
| **Encoder** | 只用 Transformer 的编码器部分（不含解码器）|
| **Representations** | 输出的是每个词的**上下文化向量表示** |
| **Pre-trained** | 先在海量无标签文本上训练，再针对具体任务微调 |

---

## 1.2 BERT 在 Transformer 家族中的位置

```
Transformer (2017)
    ├── Encoder-only → BERT (2018) → 理解任务（分类、QA、NER）
    ├── Decoder-only → GPT  (2018) → 生成任务（文本续写、对话）
    └── Encoder-Decoder → T5, BART → 序列到序列（翻译、摘要）
```

> 💡 记忆技巧：BERT 只有编码器 = 只能"读"不能"写"。GPT 只有解码器 = 只能"写"不能"读全文"。T5 两个都有 = 又能读又能写。

---

## 1.3 为什么 BERT 选择"只用编码器"？

因为 BERT 的目标是**理解**，不是生成。

- 文本分类：读完文章判断情感 → 需要理解
- 命名实体识别：找出人名地名 → 需要理解
- 问答：从段落中找答案 → 需要理解

> 这些任务都不需要逐词生成文本，而需要**深度理解每个词在上下文中的含义**。编码器的双向注意力正好擅长这个。

---

## 1.4 BERT 的两个尺寸

| 配置 | BERT-base | BERT-large |
|---|:---:|:---:|
| Transformer 层数 | 12 | 24 |
| 隐藏维度 | 768 | 1024 |
| 注意力头数 | 12 | 16 |
| 参数量 | **1.1 亿** | **3.4 亿** |

> 💡 选择建议：先用 BERT-base（快、便宜），只在需要最后几个百分点性能时才换 BERT-large。

---

## 1.5 ❗ 空壳变"懂事"—— 预训练是关键

BERT 的架构虽然设计好了，但**初始化的权重是随机的**——它什么语言知识都没有。

> 🔑 **故事转折点：** 架构有了，但模型还是空的。接下来的关键是：用什么方法让 BERT "读书学习"？

---

# 🎭 第二章：BERT 的"读书方法"

## 预训练

---

## 2.1 输入怎么准备？

BERT 看到的不是原始文字，而是经过三层处理的输入：

```
原始文本: "I love NLP"
    ↓
WordPiece 分词: [I, love, NL, ##P]
    ↓
添加特殊 token: [CLS] I love NL ##P [SEP]
    ↓
三种嵌入叠加:
  Token Embedding  → "你是什么词"
  Segment Embedding → "你在哪个句子"
  Position Embedding → "你在什么位置"
```

---

## 特殊 token 的作用

| Token | 作用 |
|---|---|
| `[CLS]` | 放在开头，其最终输出作为**整个句子的表示**（用于分类）|
| `[SEP]` | 分隔两个句子（用于句子对任务，如 QA）|
| `[MASK]` | 遮住某个词让 BERT 预测（用于 MLM 训练）|
| `[PAD]` | 填充短句子使长度一致 |

> 💡 类比：`[CLS]` 是班长，在全班讨论结束后负责总结汇报。`[SEP]` 是分界线，告诉模型"这是第一段结束、第二段开始"。

---

## 2.2 预训练任务一：掩码语言模型（MLM）

核心思想：**完形填空**。

随机选取 15% 的词进行处理：
- **80%** 的概率替换为 `[MASK]` → 主要学习信号
- **10%** 的概率替换为随机词 → 防止模型只在看到 `[MASK]` 时才认真预测
- **10%** 的概率保持不变 → 教模型"有时候答案就是原词"

```
原文: The cat sat on the mat
掩码: The cat [MASK] on the mat
BERT 要预测: [MASK] → "sat"
```

---

### ⚠️ 为什么需要 80-10-10 策略？

如果 100% 用 `[MASK]`，BERT 会学到一个"捷径"：只在看到 `[MASK]` 这个特殊符号时才预测。

但微调时输入里没有 `[MASK]`，造成训练和使用之间的**不匹配**。

> 10% 随机词和 10% 保持不变就是为了打破这种捷径。

---

## 2.3 预训练任务二：下一句预测（NSP）

核心思想：**判断两句话是否连贯**。

```
输入: [CLS] 我今天去了超市 [SEP] 买了很多水果 [SEP]
标签: IsNext ✅

输入: [CLS] 我今天去了超市 [SEP] 恐龙已经灭绝了 [SEP]
标签: NotNext ❌
```

50% 的样本是真正的下一句（IsNext），50% 是随机拼接的（NotNext）。

> ⚠️ 后来 RoBERTa 发现去掉 NSP 效果反而更好。ALBERT 用"句子顺序预测（SOP）"替代了 NSP。但 NSP 作为最早的设计思路值得理解。

---

## 2.4 总损失函数

```
Total Loss = MLM Loss + NSP Loss
```

两个任务同时训练，让 BERT 同时学会：
- **词级理解**（哪个词应该在这里）
- **句级理解**（这两句话是否有逻辑关联）

---

## 2.5 ❗ 预训练完成了，但还不能直接用

预训练后的 BERT "懂语言"了，但它不知道任何具体任务——不知道怎么做分类、不知道怎么回答问题。

> 🔑 **故事转折点：** 预训练给了 BERT "通识教育"，但要完成具体工作，还需要"岗位培训" —— 微调(Fine-tuning)。

---

# 📖 第三章：微调

## 一个预训练模型走天下

---

## 3.1 迁移学习的革命

BERT 之前的世界：
```
任务 A（情感分类）→ 从零开始训练模型 A
任务 B（命名实体）→ 从零开始训练模型 B
任务 C（问答系统）→ 从零开始训练模型 C
```

BERT 之后的世界：
```
预训练 BERT（一次，很贵）
    ├── + 分类层 → 微调 → 情感分类模型（几小时）
    ├── + 序列标注层 → 微调 → NER 模型（几小时）
    └── + 跨度预测层 → 微调 → QA 模型（几小时）
```

---

## 传统 vs BERT 迁移学习

| 维度 | 传统方法 | BERT 迁移学习 |
|---|:---:|:---:|
| 每个任务所需数据 | 数万~数百万 | 数百~数千 |
| 每个任务训练时间 | 数天 | 数小时 |
| 模型共享 | 无 | 共享一个骨干 |
| 新任务成本 | 从零开始 | 加一层 + 微调 |

> 💡 类比：预训练 = 大学4年通识教育。微调 = 入职后2周岗前培训。大学教育很贵（TPU 训练数天），但入职培训很便宜（GPU 几小时）。

---

## 3.2 BERT 用于文本分类

最简单的微调方式：

```
输入: [CLS] This movie is amazing! [SEP]
       ↓ BERT 编码 ↓
[CLS] → 768 维向量 → Linear(768, num_classes) → softmax → 类别预测
```

就是这么简单——取 `[CLS]` 的输出，加一个线性层，训练几个 epoch 就行。

---

## 3.3 BERT 变体：更高效的选择

| 模型 | 核心创新 | 相比 BERT |
|---|---|---|
| **DistilBERT** | 知识蒸馏 | 97% 性能，小 40%，快 60% |
| **RoBERTa** | 去掉 NSP，更多数据，更长训练 | 性能更好 |
| **ALBERT** | 参数共享，分解嵌入 | 模型小很多 |
| **XLNet** | 基于排列的训练 | 某些基准上更好 |

---

## 3.4 ❗ 分类搞定了，但有一类更难的任务

BERT 做分类很擅长（整句话 → 一个标签），但很多实际场景需要**从文本中精确找到特定信息**。

比如：给一段维基百科文章和一个问题，要求指出答案在文章的**第几个词到第几个词**。

> 🔑 **故事转折点：** 分类只需要整句表示(CLS)，但问答需要精确定位每个词。这引出了本讲的第二大主题 —— Question Answering。

---

# 🏆 第四章：问答系统

## BERT 的杀手级应用

---

## 4.1 什么是问答系统？

三个维度分类：

| 维度 | 类型 |
|---|---|
| **信息源** | 结构化数据(DB)、非结构化文本(Web/Wiki)、对话数据(Forums) |
| **问题类型** | 事实型、开放域、封闭域、复杂叙事型 |
| **答案类型** | 抽取式(指出位置)、生成式(写出答案)、事实型(简短回答) |

---

## 4.2 抽取式问答（阅读理解）

最核心的形式化：

```
输入: 段落 P = (p₁, p₂, ..., pₙ)
      问题 Q = (q₁, q₂, ..., qₘ)
输出: 答案 A = P[start : end]  （段落中的一个连续片段）
```

> 💡 抽取式 QA = 拿荧光笔在文章里画出答案。答案必须是原文里已经写好的文字，你只需找到它。

---

## 4.3 SQuAD：阅读理解的标准考试

**SQuAD (Stanford Question Answering Dataset):**
- 10 万个（段落、问题、答案）三元组
- 段落来自英语 Wikipedia
- 问题由众包标注者生成
- 答案是段落中的一个 span

| 指标 | 含义 | 特点 |
|---|---|---|
| **EM (Exact Match)** | 预测答案 = 金标准答案？ | 严格：0 或 1 |
| **F1** | 预测和金标准的 token 重叠度 | 宽松：给部分分 |

---

## EM / F1 计算示例

```
Q: What did Tesla do in December 1878?
Gold: {left Graz, left Graz and severed all relations with his family}
Prediction: left Graz and severed

EM = max(0, 0) = 0  （不完全匹配任何一个金标准）
F1 = max(0.67, 0.61) = 0.67  （有部分重叠，给部分分）
```

---

## 4.4 BERT 如何做阅读理解

整个模型惊人地简单：

```
输入: [CLS] 问题 [SEP] 段落 [SEP]
       ↓ BERT 编码 ↓
每个段落 token 的隐藏状态
       ↓
两个线性层:
  Start 层: 预测每个 token 是答案起始位置的概率
  End 层:   预测每个 token 是答案结束位置的概率
       ↓
答案 = P[argmax(start_probs) : argmax(end_probs)]
```

> 💡 就像让 BERT 拿两支笔：一支画"从这里开始"，一支画"到这里结束"。中间的文字就是答案。

---

## 4.5 性能飞跃

| 模型 | F1 | EM | 关键特点 |
|---|:---:|:---:|---|
| BiDAF | 77.3 | 67.7 | 复杂的手工设计架构 |
| **BERT-base** | **88.5** | **80.8** | 预训练 + 简单微调 |
| BERT-large | 90.9 | 84.1 | 更大的预训练模型 |
| RoBERTa | 94.6 | 88.9 | 更好的预训练方案 |
| ALBERT | 94.8 | 89.3 | 高效参数共享 |

从 BiDAF 到 BERT-base 的跳跃是 **+11.2 F1** —— 这个巨大提升几乎完全来自预训练，而不是更复杂的架构设计。

---

## 4.6 处理长文本的滑动窗口

BERT 最多只能处理 512 个 token，但真实段落经常更长。解决方案：**滑动窗口**。

```
长段落 (2000 tokens)
    ↓ 切分 ↓
chunk1: tokens[0:500]     → BERT → 预测答案1
chunk2: tokens[475:975]   → BERT → 预测答案2  (stride=25, 有重叠)
chunk3: tokens[950:1450]  → BERT → 预测答案3
chunk4: tokens[1425:1925] → BERT → 预测答案4
    ↓
最终答案 = 所有 chunk 中得分最高的那个
```

> 💡 滑动窗口 = 拿放大镜看长文章，每次看500个字符，向前滑动时稍微重叠一点，确保不遗漏边缘的答案。

---

# 📖 第五章

## 从"给段落找答案"到"从整个互联网找答案"

---

## 5.1 问题升级

SQuAD 的设定是：**给你段落**，你来找答案。但真实世界的问题是：

> 我连应该看**哪篇文章**都不知道！

这就是**开放域问答 (Open-Domain QA)** —— 你需要先从百万文档中**找到正确的段落**，然后再从中抽取答案。

---

## 5.2 检索器-阅读器架构（Retriever-Reader）

这是整个问答系统的核心架构——也是 **RAG 的理论原型**：

```
用户问题
    ↓
┌─────────────────────────────┐
│ Retriever（检索器）           │
│ 从百万文档中找到 top-K 段落   │
│ 方法: BM25 / DPR             │
└─────────────┬───────────────┘
              ↓ top-K 段落
┌─────────────────────────────┐
│ Reader（阅读器）              │
│ 从每个段落中抽取答案跨度      │
│ 方法: BERT fine-tuned on SQuAD│
└─────────────┬───────────────┘
              ↓
最终答案 = 所有段落中得分最高的答案
```

---

## 5.3 稀疏检索 vs 密集检索

| 维度 | 稀疏检索 (BM25/TF-IDF) | 密集检索 (DPR) |
|---|:---:|:---:|
| 匹配方式 | 关键词重叠 | 语义嵌入相似度 |
| 速度 | 非常快 | 较慢（需 ANN 搜索）|
| 同义词处理 | ❌ 差 | ✅ 好 |
| 拼写错误容忍 | ❌ 差 | ✅ 好 |
| 需要训练数据 | 不需要 | 需要标注 QA 对 |
| 最适合 | 术语明确的领域 | 自然语言问题 |

---

## DPR (Dense Passage Retrieval)

用两个独立的 BERT 编码器：

```
问题 → Question Encoder → 问题向量 (768维)
段落 → Passage Encoder → 段落向量 (768维)

相关性 = cosine_similarity(问题向量, 段落向量)
```

> 💡 DPR 就是"双塔搜索引擎"——一塔编码问题，一塔编码段落，然后在向量空间中找最近的邻居。这正是你 RAG 项目检索模块的原理!

---

# 📹 第六章：超越抽取式

## RAG 的时代

---

## 6.1 抽取式 QA 的局限

抽取式 QA 只能回答文本中**字面存在**的内容：

| 能力 | 抽取式 QA | 生成式 QA / RAG |
|---|:---:|:---:|
| 从文中找答案 | ✅ | ✅ |
| 综合多段信息 | ❌ | ✅ |
| 自然语言回答 | ❌ | ✅ |
| 推理和计算 | ❌ | ✅ |
| 可能产生幻觉 | ❌ | ⚠️ 是 |

---

## 6.2 RAG = 检索 + 生成

现代 RAG 把检索器-阅读器架构升级了：

```
检索器-阅读器 (2019):
  Retriever (BM25/DPR) → Reader (BERT span extraction)

RAG (2020+):
  Retriever (DPR/hybrid) → Generator (GPT/Claude/Llama)
```

> 💡 技术演进比喻：阅读器从"荧光笔"(抽取式) 升级为了"带参考资料的专业作家"(生成式)。

---

# 🗺️ 全局回顾：技术演进路线图

```text
Transformer (2017) — 架构蓝图
  ✅ 自注意力 + 并行计算
  ❌ 空壳，没有语言知识
            │
            ▼
BERT Pre-training (2018) — 注入知识
  ✅ MLM + NSP 让模型学会语言
  ✅ 双向注意力 = 深度理解
  ❌ 只有通用能力，不知道具体任务
            │
            ▼
BERT Fine-tuning — 适应任务
  ✅ 一个模型适配所有 NLP 任务
  ✅ 少量数据 + 短时间训练
  ❌ 512 token 长度限制
            │
            ▼
Reading Comprehension (SQuAD) — 阅读理解
  ✅ 给定段落，精确找到答案
  ❌ 需要提前给定正确段落
            │
            ▼
Open-Domain QA — 开放域问答
  ✅ 检索器 + 阅读器架构
  ✅ 从百万文档中搜索答案
  ❌ 只能抽取原文，不能生成
            │
            ▼
RAG — 检索增强生成
  ✅ 检索 + LLM 生成
  ✅ 自然语言回答
  ⚠️ 可能产生幻觉 → 需要验证
```

---

## 转折总结表

| 从 | 到 | 解决的核心问题 |
|---|---|---|
| Transformer 空壳 | BERT 预训练 | 模型没有语言知识 → 用 MLM/NSP 注入 |
| 预训练模型 | 微调模型 | 通用能力 → 适配具体任务 |
| 手工设计架构 (BiDAF) | BERT 微调 | 复杂 → 简单，性能从 77 跳到 88 |
| 给定段落 QA | 开放域 QA | 不知道看哪篇文章 → 先检索再阅读 |
| 稀疏检索 (BM25) | 密集检索 (DPR) | 关键词匹配不够 → 语义匹配 |
| 抽取式 QA | RAG | 只能引用原文 → 能生成自然语言答案 |
