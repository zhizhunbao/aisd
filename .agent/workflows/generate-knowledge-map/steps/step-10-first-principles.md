# Phase 10: DIM-9 First Principles（第一性原理）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Philosopher |
| **技能** | knowledge-map-format (DIM-9) |
| **前置条件** | Phase 9（Bridge）完成 |
| **输出** | `{topic}_first_principles.md` |
| **预计时间** | 20-40 分钟 |
| **跳过条件** | 纯工程工具，无数学/理论公理 |

## 设计理论依据

| 章节 | 格式设计 | 教科书依据 |
|------|---------|-----------|
| `## 核心问题链` | "5 个为什么"递归追问 | Toyota Production System "5 Whys" (Ohno, 1988) — 从表象追到根因的标准方法 + Descartes《Discourse on the Method》(1637) — 只接受不可怀疑的公理 |
| `## 公理与基本假设` | 陈述+白话+来源+可验证性 四要素 | Euclid《Elements》(~300 BC) — 公理化方法：先声明公设(axioms)，再从公设推导一切定理 |
| 四要素中的"可验证性" | 什么条件下成立/不成立 | Popper《The Logic of Scientific Discovery》(1959) — 可证伪性: 不能被证伪的命题没有科学价值 |
| `## 推导链` | 每步标注"用了哪个公理" | Euclid — 每个定理的证明必须引用具体公设编号，不允许隐含假设 |
| 推导链全景图 | ASCII box-drawing | Mayer《Multimedia Learning》Ch.5 "Spatial Contiguity" — 文字关系用图形外化 |
| `## 如果公理不成立？` | 逐个拔掉公理分析崩塌 | Lakatos《Proofs and Refutations》(1976) — 数学不是绝对真理，通过"反例攻击公理"理解边界比理解证明更深刻 |
| 速查表 | 公理+条件+后果 一览 | 外化记忆，快速定位适用边界 |

## 固定 5 章模板

````
---
topic: {topic}
dimension: first_principles
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📖 Paper: ..."
  - "📚 Book: ..."
expiry: 12m
status: current
---

# {Topic} 第一性原理

> 📖 Paper: 作者, 论文名
> 📚 Book: 作者, 《书名》, Ch.X

---

## 核心问题链

> 用"5 个为什么"递归追问，从表层功能到不可再分公理。

1. **{Topic} 在做什么？** → 一句话（表层）
2. **为什么要这样做？** → 一句话（动机）
3. **为什么这个动机重要？** → 一句话（更深层）
4. **这个原因的根基是什么？** → 一句话（基本事实）
5. **能否继续拆分？** → 不能 → **到达公理**

---

## 公理与基本假设

### 公理 1: {名称}

**陈述：** 严格陈述
**白话：** 日常语言
**来源：** 数学定理/物理定律/统计性质/经验观察
**可验证性：** 什么条件下成立？什么条件下不成立？

> 📖 来源引证

---

## 从公理到技术的推导链

### Step 1: {从公理 X 出发} → {推论}

**推理：** 因为公理 X 成立，所以……
**结果：** 第一个中间结论

### Step N: → {完整的 {Topic} 技术}

### 推导链全景图

```
公理 1 ─────┐
            ├──→ 推论 A ──→ {Topic}
公理 2 ─────┘
```

---

## 如果公理不成立？

### 公理 1 失效：{场景}

**如果不成立：** {具体场景}
**技术后果：** {如何失效}
**替代方案：** {替代方法}

---

## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
````

## 格式规则

- ✅ 问题链用递归追问，从表层到公理
- ✅ 每个公理有**陈述+白话+来源+可验证性**四要素
- ✅ 推导链每步标注**用了哪个公理**
- ✅ 末尾有全景图
- ❌ 不允许引入未声明的隐含假设
- ❌ 不允许用类比代替推理

## 完成检查

- [ ] 5 章结构完整
- [ ] 问题链从表层追到公理
- [ ] 每个公理有四要素
- [ ] 推导链无跳步
- [ ] 公理失效分析覆盖所有公理

## 教科书来源

- Euclid《Elements》(~300 BC) — 公理化方法
- Descartes《Discourse on the Method》(1637) — 方法论怀疑
- Popper《The Logic of Scientific Discovery》(1959) — 可证伪性
- Lakatos《Proofs and Refutations》(1976) — 反例攻击公理
- Ohno, Toyota Production System "5 Whys" (1988)
- Mayer《Multimedia Learning》3rd Ed. (2020), Ch.5 "Spatial Contiguity"
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`
