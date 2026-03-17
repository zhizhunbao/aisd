# Phase 5: DIM-4 Tutorial（教程）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Tutorial Writer |
| **技能** | knowledge-map-format (DIM-4) |
| **前置条件** | Phase 4（Math）完成或跳过 |
| **输出** | `{topic}_tutorial.md` |
| **预计时间** | 30-60 分钟 |

## 设计理论依据

| 章节 | 格式设计 | 教科书依据 |
|------|---------|-----------|
| `## Section 0: 前置知识` | 一句话列出前置项 | Gagné《Conditions of Learning》Ch.3 — 学习必须在已有能力基础上建构，先确认前置 |
| `## Section 1: Why` | **痛点先行**，先讲没有它会怎样 | Keller "ARCS Model of Motivation" (1987) — **Attention + Relevance**: 先引起注意、建立关联，学生才有动力继续 |
| Why-First 顺序 | 痛点→价值→原理，不是原理→痛点 | Mayer《Multimedia Learning》Ch.17: "Motivation Principle" — 先激活动机再讲内容，学习效果显著提升 |
| `## Section 2: How` | 设计决策（为什么用 X 不用 Y） | Sweller "Cognitive Load Theory" (1988) — Worked Examples: 展示**为什么这样设计**比直接给结论认知负荷更低 |
| Section 2 流程图 | ASCII box-drawing 风格 | Mayer《Multimedia Learning》Ch.5: "Spatial Contiguity Principle" — 文字与图形邻近放置才有效 |
| `## Section 3: 局限性` | 列出局限 + 应对策略 | Popper《Conjectures and Refutations》(1963) — 可证伪性: 不讲局限的教程不是好教程 |
| `## Section 4: 方案对比` | 多方案对比表 | Bruner《The Process of Education》(1960) — 对比学习法: 横向对比加深对核心特征的理解 |
| 三层止挖 | 会用→知道为什么→看过底层原理 | Bloom《Taxonomy》— 到 Analysis 层即止，不追到 Creation 层 |

## 固定 5 Section（0-4）模板

```
---
topic: {topic}
dimension: tutorial
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📚 Book: ..."
  - "📖 Docs: ..."
expiry: 12m
status: current
---

# {Topic} 教程

> **前置知识：** 列出前置项
> **参考来源：** [来源](URL)

---

## Section 0: 前置知识速查

1. **前置项 A**：一句话说明
2. **前置项 B**：一句话说明

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **痛点 1**：具体描述
- 🔥 **痛点 2**：具体描述

### 它的核心价值

1. **价值 1**：说明
2. **价值 2**：说明

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图
（ASCII box-drawing 图）

### 2.2 核心机制
**为什么用 X 而不是 Y？**

---

## Section 3: 局限性

1. **局限 1**：描述 → 应对策略

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
```

## 格式规则

- ✅ Section 1 **必须先讲痛点**，不能上来就讲原理
- ✅ Section 2 解释**设计决策**
- ✅ Section 2 流程图用 ASCII `┌───┤` 风格
- ✅ Section 3 局限性列出应对策略
- ✅ 末尾有参考来源表

## 完成检查

- [ ] 5 Section（0-4）结构完整 + 参考来源表存在
- [ ] Section 1 有痛点 + 价值
- [ ] Section 2 有设计决策解释
- [ ] 参考来源表存在

## 教科书来源

- Mayer《Multimedia Learning》3rd Ed. (2020), Ch.5 "Spatial Contiguity", Ch.17 "Motivation"
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`
- Keller "ARCS Model of Motivational Design" (1987)
- Sweller "Cognitive Load Theory" (1988)
- Clark & Mayer《e-Learning》3rd Ed. (2011), Ch.10 "Segmenting + Pretraining", p.205-218
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Gagné《The Conditions of Learning》4th Ed. (1985), Ch.3 "Learning Hierarchies"
- Bruner《The Process of Education》(1960), Ch.2 — 对比学习法
- Popper《Conjectures and Refutations》(1963) — 可证伪性
- Bloom《Taxonomy of Educational Objectives》(1956) — 三层止挖
