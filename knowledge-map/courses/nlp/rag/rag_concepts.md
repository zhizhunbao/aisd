---
topic: rag
dimension: concepts
created: 2026-04-13
last_verified: 2026-04-13
source_versions:
  - "📚 Book: Jurafsky & Martin, Speech and Language Processing (3rd), 2025 — file:///c:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📖 Paper: Lewis et al., 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks', NeurIPS 2020 — https://arxiv.org/abs/2005.11401"
expiry: 12m
status: current
---

# RAG (检索增强生成) 核心概念

> 📚 Book: Jurafsky & Martin, [《Speech and Language Processing (3rd Ed.)》](../../../textbooks/jurafsky_slp3.pdf), Ch.22.4

---

## 术语定义

### 幻觉 (Hallucination)

指大语言模型生成了看起来很专业但事实上错误、毫无根据的信息。这通常是因为模型在训练时“死记硬背”了知识，但在提取时发生了记忆漂移。RAG 的初衷就是为了通过“翻书”来治愈幻觉。

> 📚 来源引证：Jurafsky & Martin (2025), Ch.22.4

### 向量数据库 (Vector Database)

RAG 的“外挂大脑”。它将海量文档切成小块，并转化为数学向量存储。当用户提问时，数据库计算问题与文档之间的相似度，从而定位相关内容。

> 别名：**向量索引 (Vector Index)**

> 📚 来源引证：Lewis et al. (2020), Section 2.1

### 生成器 (Generator)

RAG 流程中的最后一个环节，通常由强大的 LLM（如 GPT-4）充当。它的任务是阅读检索回来的参考资料，并根据这些资料“组织语言”回答用户。

> 易混淆：**阅读器 (Reader)** — 在传统抽取式 QA 中叫 Reader，在 RAG 中它不再只是“画重点”，而是生成新文本。

> 📚 来源引证：Lewis et al. (2020), Section 2.3

### 提示词注入 (Prompt Injection)

RAG 实现的关键技巧：将检索到的文档内容“塞进”给 AI 的提示词里。此时 AI 的任务变成了“请参考以下资料回答问题...”。

---

## 概念辨析

### 预训练知识 (Parametric Knowledge) vs RAG 知识 (Non-parametric Knowledge)

| 维度 | 预训练知识 (参数) | RAG 知识 (非参数) |
|------|---|---|
| **存储位置** | 模型权重中 (离线存储) | 外部数据库中 (实时链接) |
| **更新成本** | 极高 (需要重新训练) | 极低 (删除/增加文档即可) |
| **时效性** | 受限于训练截止期 | 理论上可以是实时动态的 |
| **事实准确性** | 容易发生幻觉 | 有据可查，准确性高 |

> 📚 来源引证：Lewis et al. (2020), Section 1

---

## 核心属性

### RAG 经典三步走 (Naive RAG Workflow)

```
用户提问 ──→ [检索 (Retrieve)] ──→ [增强 (Augment)] ──→ [生成 (Generate)]
```

1.  **检索 (Retrieve)**: 用问题去海量向量库里找 Top-K 段落。
2.  **增强 (Augment)**: 把段落和原始问题拼在一起，告诉 AI：“这些是参考资料，请回答”。
3.  **生成 (Generate)**: AI 综合参考资料，写出有逻辑的答案。

### 适用场景 ✅
- 每日更新的知识库（如新闻、新闻综述）
- 私有领域的知识问答（如企业内网文档）
- 需要附带来源引证的严肃任务（如学术、医疗、法律辅助）

### 不适用场景 ❌
- 纯逻辑推理或数学证明（这种任务不需要外挂知识库）
- 对延迟要求极高的实时交互（检索过程会增加响应时间）

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| **Embedding** | 将文字转为向量的过程 | `Hello World` → `[0.12, -0.45, ...]` |
| **Cosine Similarity** | 衡量两个向量“像不像”的常用方法 | 常用于检索排序 |
| **Chunking** | 把大文档切成小块的策略 | 按 500 字一块切，允许重叠 |
| **Top-K** | 检索时返回的最相关的文档段落数量 | 典型值为 K=3 或 K=5 |
