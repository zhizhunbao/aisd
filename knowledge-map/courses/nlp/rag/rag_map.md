---
topic: rag
dimension: map
created: 2026-04-13
last_verified: 2026-04-13
source_versions:
  - "📚 Book: Jurafsky & Martin, Speech and Language Processing (3rd), 2025 — file:///c:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📖 Paper: Lewis et al., 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks', NeurIPS 2020 — https://arxiv.org/abs/2005.11401"
expiry: 12m
status: current
---

# RAG (检索增强生成) 知识地图

> 📚 Book: Jurafsky & Martin, [《Speech and Language Processing (3rd Ed.)》](../../../textbooks/jurafsky_slp3.pdf), Ch.22.4
> 📖 Paper: Lewis et al., [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)

## 1. 核心问题

- **既然模型已经能背下维基百科，为什么还容易一本正经胡说八道？** → 因为模型的参数知识是静态且由于压缩而易发生“幻觉”的，它需要一份实时的“参考手册”。
- **如何让模型在不重新训练的情况下学会昨天的头条新闻？** → 将外挂数据库作为模型的“外部存储”，通过检索最新信息直接喂给模型。
- **为什么说 RAG 是对“抽取式 QA”的终结？** → 抽取式只能“抄原文”，而 RAG 让模型能像人类一样参考资料后写出更自然、有逻辑的回答。
- **RAG 如何解决 AI 的“信任危机”？** → 通过附带来源引证（Citations），让用户可以核实 AI 的回答是否有据可依。

---

## 2. 全景位置

```
深度学习与大模型应用
├── 纯参数模型训练 (Pre-training / Fine-tuning)
└── 检索增强系统 (Retrieval-Augmented Systems) ← 你在这里
    ├── 【RAG】 (最广泛的范式：检索向量库 -> LLM 生成答案)
    ├── 代理系统 (AI Agents) (自主决定何时去检索)
    └── 事实校验系统 (Fact-checking Systems)
```

---

## 3. 依赖地图

```
前置知识                 本主题                   后续方向
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────┐
│ 词嵌入 & 分词    │────→│                  │────→│ 企业化知识库应用      │
│ 向量数据库       │────→│      RAG         │────→│ 复杂推理 Agent         │
│ LLM 推理         │────→│                  │────→│ 在线实时对话系统      │
└─────────────────┘     └──────────────────┘     └──────────────────────┘
```

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [rag_map.md](rag_map.md) | ① 导航 | 了解 RAG 的全貌及与传统 QA 的区别 |
| [rag_concepts.md](rag_concepts.md) | ② 概念 | 掌握向量库、幻觉、生成器等核心术语 |
| ~~rag_math.md~~ | ③ 公式 | ⬜ 待生成 (v1 扩展) |
| ~~rag_tutorial.md~~ | ④ 教程 | ⬜ 待生成 (v1 扩展) |
| ~~rag_code.md~~ | ⑤ 代码 | ⬜ 待生成 (v1 扩展) |
| ~~rag_pitfalls.md~~ | ⑥ 踩坑 | ⬜ 待生成 (v1 扩展) |
| ~~rag_history.md~~ | ⑦ 历史 | ⬜ 待生成 (v1 扩展) |
| ~~rag_bridge.md~~ | ⑧ 衔接 | ⬜ 待生成 (v1 扩展) |
| ~~rag_first_principles.md~~ | ⑨ 第一性原理 | ⬜ 待生成 (v1 扩展) |

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [rag_map.md](rag_map.md) 了解“外挂数据库”比“死记硬背”强在哪里。
2. 读 [rag_concepts.md](rag_concepts.md) 理解 Vector Database 和 Generator 的协作。
3. 对比传统搜索与 RAG 的交互差异。

### 日常参考 🔧

1. 查 [rag_concepts.md](rag_concepts.md) 确认 Top-K 对答案质量的影响。

### 深度研究 🔬

1. 阅读原始论文：[Lewis et al. (2020)](https://arxiv.org/abs/2005.11401)。
2. 探索 LangChain 或 LlamaIndex 的工程实现。

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
| [Lewis et al. (2020)](https://arxiv.org/abs/2005.11401) | 📖 论文 | 核心范式定义与流程参考 |
| [SLP3 Ch.22.4](../../../textbooks/jurafsky_slp3.pdf) | 📚 教科书 | 生成式模型与检索结合的理论背景 |
