---
topic: qa_system
dimension: map
created: 2026-04-13
last_verified: 2026-04-13
source_versions:
  - "📚 Book: Jurafsky & Martin, Speech and Language Processing (3rd), 2025 — file:///c:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📖 Paper: Rajpurkar et al., 'SQuAD: 100,000+ Questions for Machine Comprehension of Text', 2016 — https://arxiv.org/abs/1606.05250"
expiry: 12m
status: current
---

# 问答系统 (QA System) 知识地图

> 📚 Book: Jurafsky & Martin, [《Speech and Language Processing (3rd Ed.)》](../../../textbooks/jurafsky_slp3.pdf), Ch.22
> 📖 Paper: Rajpurkar et al., [SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250)

## 1. 核心问题

- **为什么说“阅读理解”是问答系统的基础？** → 因为大多数 QA 都可以简化为：从一段给定的文字中精准抽取（Extract）那个最相关的片段。
- **如何判断 AI 是真的懂了，还是在乱猜？** → 通过精确匹配 (EM) 和词级重叠 (F1) 这两把尺子，严丝合缝地衡量模型找的位置对不对。
- **当 AI 面对整个互联网时，它该如何“翻书”？** → 采用“检索-阅读”二级跳架构：先在大海捞针出几段话，再在那几段话里细找答案。
- **如果答案不在原文里怎么办？** → 这就是从“抽取式”到“生成式（RAG）”的巨大飞跃，也是现代大模型的强项。

> 📚 Book: Jurafsky & Martin (2025), Ch.22.1 & 22.2

---

## 2. 全景位置

```
自然语言处理 (NLP) 应用层
├── 文本分类 (情感、垃圾邮件)
├── 翻译与摘要 (T5, BART)
└── 问答系统 (QA) ← 你在这里
    ├── 抽取式问答 (Extractive QA/Reading Comprehension)
    │   └── 【SQuAD / BERT-based】 (核心：找 Start/End 位置)
    ├── 检索式问答 (Information Retrieval QA)
    │   └── 【DPR / Retriever-Reader】 (核心：大规模搜索 + 局部精读)
    └── 生成式问答 (Generative QA / RAG)
        └── 【Retrieval-Augmented Generation】 (核心：参考资料 + 生成)
```

> 📚 Book: Jurafsky & Martin (2025), Ch.22.1

---

## 3. 依赖地图

```
前置知识                 本主题                   后续方向
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────┐
│ BERT / Transformer│────→│                  │────→│ 智能客服/虚拟助手      │
│ 词嵌入 (Embedding) │────→│    问答系统      │────→│ 检索增强生成 (RAG)    │
│ 文本检索 (BM25)    │────→│                  │────→│ 多模态问答 (Visual QA) │
└─────────────────┘     └──────────────────┘     └──────────────────────┘
```

> 📚 Book: Jurafsky & Martin (2025), Ch.22.2

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [qa_system_map.md](qa_system_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [qa_system_concepts.md](qa_system_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| ~~qa_system_math.md~~ | ③ 公式 | ⬜ 待生成 (v1 扩展) |
| ~~qa_system_tutorial.md~~ | ④ 教程 | ⬜ 待生成 (v1 扩展) |
| ~~qa_system_code.md~~ | ⑤ 代码 | ⬜ 待生成 (v1 扩展) |
| ~~qa_system_pitfalls.md~~ | ⑥ 踩坑 | ⬜ 待生成 (v1 扩展) |
| ~~qa_system_history.md~~ | ⑦ 历史 | ⬜ 待生成 (v1 扩展) |
| ~~qa_system_bridge.md~~ | ⑧ 衔接 | ⬜ 待生成 (v1 扩展) |
| ~~qa_system_first_principles.md~~ | ⑨ 第一性原理 | ⬜ 待生成 (v1 扩展) |

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [qa_system_map.md](qa_system_map.md) 了解问答系统的三种主流范式。
2. 读 [qa_system_concepts.md](qa_system_concepts.md) 搞清楚 EM 和 F1 分数怎么算。
3. 重点理解“抽取式问答”的数学本质——找起止索引。

### 日常参考 🔧

1. 查 [qa_system_concepts.md](qa_system_concepts.md) 确认 Retriever 和 Reader 的分工。
2. 确认 SQuAD 2.0 对“不可回答问题”的处理逻辑。

### 深度研究 🔬

1. 阅读原始论文：[SQuAD (2016)](https://arxiv.org/abs/1606.05250)。
2. 查看 [Haystack](https://haystack.deepset.ai/) 等问答框架的工业化实现。

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ⬜ 待生成 |
| Math | ⬜ v1 扩展 |
| Tutorial | ⬜ v1 扩展 |
| Code | ⬜ v1 扩展 |
| Pitfalls | ⬜ v1 扩展 |
| History | ⬜ v1 扩展 |
| Bridge | ⬜ v1 扩展 |
| First Principles | ⬜ v1 扩展 |

---

## 7. 新新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-04-13 | 12m | ✅ current |
| Concepts | 2026-04-13 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [Jurafsky & Martin (2025) SLP3 Ch.22](../../../textbooks/jurafsky_slp3.pdf) | 📚 教科书 | 全文范式分类参考 |
| [Rajpurkar et al. (2016) SQuAD Paper](https://arxiv.org/abs/1606.05250) | 📖 论文 | 1.核心问题 / 评价指标说明 |
| [Karpukhin et al. (2020) DPR Paper](https://arxiv.org/abs/2004.04906) | 📖 论文 | 开放域问答检索架构参考 |
