# Phase 7: DIM-6 Pitfalls（踩坑记录）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Debug Expert |
| **技能** | knowledge-map-format (DIM-6) |
| **前置条件** | Phase 6（Code）完成 |
| **输出** | `{topic}_pitfalls.md` |
| **预计时间** | 20-40 分钟 |
| **活文档** | 每次踩坑后追加条目 |

## 设计理论依据

| 章节 | 格式设计 | 教科书依据 |
|------|---------|------------|
| 全局组织方式 | **围绕学习痛点组织**，不是围绕技术 bug | Heath《Made to Stick》Ch.1 "Simple" — 找到核心痛点才能引发共鸣；学生的痛点不是"报错信息"而是"不知道为什么" |
| `## 坑 N` 解法 | ❌/✅ 错误vs正确对比（代码块 + 语法高亮） | Clark & Mayer《e-Learning》Ch.10, p.208 — "Worked Examples with Contrasting Cases": 看到错误和正确的对比，学习效果远优于只看正确答案 |
| `## 坑 N` 结构 | **场景→症状→根因→解法→教训** 五步 | Jonassen《Learning to Solve Problems》(2010) — Case-Based Reasoning: 完整案例（情境+问题+推理+结果）才能迁移到新问题 |
| `## 超级避坑指南` | 调试清单 | Gawande《The Checklist Manifesto》(2009), Ch.2 — 清单化降低复杂任务出错率，尤其在高压力/高疲劳场景 |
| 坑内关键词 | **加粗关键词**而非三级标题 | Mayer《Multimedia Learning》Ch.9: "Signaling Principle" — 用视觉信号引导注意力，加粗比层级标题更轻量 |

## 核心定位：围绕学习痛点

> ⚠️ Pitfalls 不是技术 debug 日志，而是**学生真实痛点的解决方案库**。

### 通用痛点库 + 坑分类

> **完整痛点库和坑分类见** [`references/pain_points.md`](../references/pain_points.md)
>
> 每个坑应能映射到至少一个通用痛点，按学生需求（概念/代码/作业/考试/心态）分类组织。

## 固定格式模板

```
---
topic: {topic}
dimension: pitfalls
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📚 Book: ..."
  - "🧪 经验: ..."
expiry: 6m
status: current
---

# {Topic} 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: {坑标题}

**痛点类别：** {对应上表痛点编号和名称}

**场景：** {什么情况下会遇到这个坑}

**症状：** {学生看到的现象——可以是报错，也可以是"完全不理解"}

**根因：** {为什么会发生——通常是教学缺失或概念误导}

**解法：**

❌ 错误做法 — 原因

```python
# 错误的代码
bad_code()
```

✅ 正确做法 — 原因

```python
# 正确的代码
good_code()
```

**教训：** {一句话总结，用人话}

> 📖 来源引证

---

## 坑 2: {坑标题}

（同上格式，编号连续）

---

## 超级避坑指南

### 学习避坑

1. [ ] **别死记硬背** → 先理解逻辑，再记关键词
2. [ ] **别只抄代码** → 每一行都要知道在干嘛
3. [ ] **别被名词吓住** → 90% 都是包装
4. [ ] **别一上来啃理论** → 先从用途 + 流程入手
5. [ ] **少而精 > 多而乱** → 别盲目堆内容

### 作业/项目避坑

1. [ ] **先看要求再动手** → 不要瞎做
2. [ ] **先搭结构再填内容** → 框架比细节重要
3. [ ] **能简单就不复杂** → 不搞炫技
4. [ ] **注释写人话** → 不写空话
5. [ ] **遇到问题查根源** → 不是盲目改参数

### 考试/答辩避坑

1. [ ] **被问住不要慌** → 很多老师自己也不清楚
2. [ ] **被问细节回到大逻辑** → 不要被带偏
3. [ ] **一句话讲清原理** → 别堆砌名词

### 调试清单（技术类）

1. [ ] **检查项 1？** → 操作建议
2. [ ] **检查项 2？** → 操作建议
...
```

## 格式规则

- ✅ 每个坑标注**痛点类别**（映射到通用痛点表）
- ✅ 用 **加粗关键词**（场景/症状/根因/解法/教训），不用 `###`
- ✅ 解法用 ❌/✅ + 4 空格缩进代码
- ✅ 每个坑结尾有 `> 📖` 引证
- ✅ 超级避坑指南按 学习/作业/考试/调试 分类
- ❌ 不要嵌套代码块

## 完成检查

- [ ] 每个坑有痛点类别标注
- [ ] 每个坑有 ❌/✅ 对比
- [ ] 超级避坑指南存在
- [ ] 调试清单存在（技术类主题）

## 教科书来源

- Heath《Made to Stick》(2007), Ch.1 "Simple" — 找到核心痛点
  - MinerU: `data/mineru_output/heath_made_to_stick/heath_made_to_stick/hybrid_auto/heath_made_to_stick.md`
- Clark & Mayer《e-Learning》3rd Ed. (2011), Ch.10 "Worked Examples", p.205-218
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Jonassen《Learning to Solve Problems》(2010) — Case-Based Reasoning
- Gawande《The Checklist Manifesto》(2009), Ch.2
- Mayer《Multimedia Learning》3rd Ed. (2020), Ch.9 "Signaling Principle"
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`
