---
topic: qa_system
dimension: concepts
created: 2026-04-13
last_verified: 2026-04-13
source_versions:
  - "📚 Book: Jurafsky & Martin, Speech and Language Processing (3rd), 2025 — file:///c:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📖 Paper: Rajpurkar et al., 'SQuAD: 100,000+ Questions for Machine Comprehension of Text', 2016 — https://arxiv.org/abs/1606.05250"
expiry: 12m
status: current
---

# 问答系统 (QA System) 核心概念

> 📚 Book: Jurafsky & Martin, [《Speech and Language Processing (3rd Ed.)》](../../../textbooks/jurafsky_slp3.pdf), Ch.22

---

## 术语定义

### 抽取式问答 (Extractive QA)

最常见的问答形式。模型被给定一段参考文本和一个问题，它的任务是在原文中找到包含答案的那一小段文字（Span）。它的本质不是在“写写画画”，而是在“做标记”。

> 别名：**阅读理解 (Reading Comprehension)**（在学术测试中更常用此名）

> 📚 来源引证：Book: Jurafsky & Martin (2025), Ch.22.1

### 精确匹配 (Exact Match, EM)

针对问答系统最严苛的打分标准。只有当模型预测的答案与标准答案**每一个字符都完全一致**时，才得 1 分，否则得 0 分。这通常用于衡量模型对数字、日期、地名等事实的捕捉能力。

> 📚 来源引证：Paper: Rajpurkar et al. (2016), Section 4

### F1 分数 (F1 Score)

比 EM 更“通情达理”的打分标准。它计算模型答案和标准答案之间 **Token 级别的重叠程度**（精确率与召回率的平衡）。如果模型多写了一个冠词（比如 A 或 The），F1 仍会给很高的分值，而 EM 会直接归零。

> 📚 来源引证：Paper: Rajpurkar et al. (2016), Section 4

### 检索器 (Retriever)

开放域问答系统的“第一棒”。它的任务是在数百万甚至数十亿的文档库中，快速捞出前几个（Top-K）最可能包含答案的候选段落。它的核心目标是**召回率（Recall）**——只要答案在这些段落里就行，哪怕多捞了也没关系。

> 📚 来源引证：Book: Jurafsky & Martin (2025), Ch.22.2

### 阅读器 (Reader)

开放域问答系统的“第二棒”。它通常是一个像 BERT 这样强大的理解模型。它的任务是精读检索器捞回来的那几个段落，从中**精确定位（Extract）**出具体的答案。

> 📚 来源引证：Book: Jurafsky & Martin (2025), Ch.22.2

### 滑动窗口 (Sliding Window)

当 BERT 遇到超长文本（超过 512 token）时的处理策略。将长文切成重叠的小块，分别送入模型处理，通过重叠部分（Stride）确保答案不会因为恰好被切断而丢失。

> 📚 来源引证：Book: Jurafsky & Martin (2025), Ch.22.1.3

---

## 概念辨析

### 抽取式 (Extractive) vs 生成式 (Generative)

| 维度 | 抽取式 (Extractive) | 生成式 (Generative) |
|------|---|---|
| **答案来源** | 必须来自原文的子串 | 根据理解重新组织语言生成 |
| **可解释性** | 极高（能告诉你答案在第几行） | 较低（可能产生幻觉） |
| **比喻** | 拿着荧光笔在书里画重点 | 根据参考资料写一篇小论文 |
| **局限性** | 无法回答需要推理总结的问题 | 可能产生内容漂移（不准） |

> 📚 来源引证：Book: Jurafsky & Martin (2025), Ch.22.1 & 22.4

---

## 核心属性

### 检索-阅读架构 (Retriever-Reader)

```
[问题] ──→ [Retriever] ──→ [Top-K 相关段落] ──→ [Reader] ──→ [最终答案]
```

*   **Retriever**: 负责“广度”，利用索引快速过滤海量内容。
*   **Reader**: 负责“深度”，利用注意力机制深度解析文本。

### 适用场景 ✅
- 智能客服（根据知识库回答产品手册问题）
- 搜索引擎（搜索结果顶部的“精选片段”）
- 医疗/法律咨询（基于具体条文的解答）

### 不适用场景 ❌
- 情感陪聊（它会死板地引用原文，不适合感性交流）
- 创意写作（它只会“抽取”，不会“创造”）

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| **SQuAD 1.1** | 只有能回答的问题 | 标准阅读理解 |
| **SQuAD 2.0** | 增加了“无法从文中回答”的问题 | 考查模型是否会“不懂装懂” |
| **BM25** | 最经典的统计检索算法 | 基于词频匹配关键词 |
| **DPR** | 现代神经网络检索算法 | 基于向量空间语义匹配 |
| **Stride** | 滑动窗口的重叠步长 | 典型值 128 或 256 |
