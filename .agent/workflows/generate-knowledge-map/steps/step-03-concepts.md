# Phase 3: DIM-2 Concepts（核心概念）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Concept Builder |
| **技能** | knowledge-map-format (DIM-2) |
| **前置条件** | Phase 2（Map）完成 |
| **输出** | `{topic}_concepts.md` |
| **预计时间** | 20-40 分钟 |

## 设计理论依据

| 章节 | 格式设计 | 教科书依据 |
|------|---------|-----------|
| `## 术语定义` | 用 `###` 段落定义，**不用表格** | Mayer《Multimedia Learning》Ch.12: "Coherence Principle" — 连贯叙事优于碎片化表格，段落能承载上下文和因果关系 |
| 术语标题格式 | `### 中文名 (English Name)` 中英并列 | Cummins《Language, Power and Pedagogy》(2000) — 双语标注降低 L2 学习者术语歧义 |
| `> 易混淆` 标注 | 术语末尾标注易混淆项 | Bruner《The Process of Education》(1960), Ch.2 — 对比分析 (contrastive analysis) 是概念形成的核心方法 |
| `## 概念辨析` | A vs B 对比表 | Clark & Mayer《e-Learning》Ch.10, p.205 — "Pretraining Principle": 先辨析易混概念再进入正题 |
| `## 核心属性` | 信息架构 + 适用✅/不适用❌ | Kahneman《Thinking, Fast and Slow》(2011) — 明确适用边界防止过度泛化（System 1 错误） |
| `## 速查表` | 一行一项，快速查阅 | Norman《The Design of Everyday Things》(2013), Ch.3 — "Knowledge in the World": 把记忆负担外化到文档 |

## 固定 4 章模板

```
---
topic: {topic}
dimension: concepts
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📚 Book: ..."
  - "📖 Paper: ..."
expiry: 12m
status: current
---

# {Topic} 核心概念

> 📚 Book: 作者, 《书名》, Ch.X

---

## 术语定义

### 术语名 (English Term)

白话定义段落。用自然语言解释。

> 易混淆：**另一个术语** — 区别说明

> 📚 来源引证

---

## 概念辨析

### A vs B

| 维度 | A | B |
|------|---|---|
| **本质** | ... | ... |
| **典型应用** | ... | ... |

> 📖 来源引证

---

## 核心属性

### 信息架构
（ASCII box-drawing 图）

### 适用场景 ✅
### 不适用场景 ❌

> 📚 来源引证

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
```

## 格式规则

- ✅ 术语定义用 `###` 三级标题 + 段落，**不用表格**
- ✅ 标题格式：`### 中文名 (English Name)`
- ✅ 概念辨析用对比表格
- ✅ 核心属性有 信息架构 + 适用✅ + 不适用❌
- ❌ 不要用表格列术语定义

## 完成检查

- [ ] 4 章结构完整
- [ ] 每个术语有白话定义段落
- [ ] 至少一组辨析对比表
- [ ] 参照 `_course.md` 名词总表确保术语一致

## 教科书来源

- Mayer《Multimedia Learning》3rd Ed. (2020), Ch.12 "Coherence Principle"
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`
- Clark & Mayer《e-Learning》3rd Ed. (2011), Ch.10 "Pretraining Principle", p.205-218
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Bruner《The Process of Education》(1960), Ch.2
- Kahneman《Thinking, Fast and Slow》(2011) — System 1 过度泛化
- Norman《The Design of Everyday Things》Revised Ed. (2013), Ch.3
  - MinerU: `data/mineru_output/norman_design_everyday_things/norman_design_everyday_things/auto/norman_design_everyday_things.md`

