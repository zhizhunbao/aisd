# Phase 4: DIM-3 Math（数学基础）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Math Writer |
| **技能** | knowledge-map-format (DIM-3) |
| **前置条件** | Phase 3（Concepts）完成 |
| **输出** | `{topic}_math.md` |
| **预计时间** | 20-40 分钟 |
| **跳过条件** | 主题无数学内容（如 Docker、Git） |

## 设计理论依据

| 章节 | 格式设计 | 教科书依据 |
|------|---------|-----------|
| `## 符号对照表` | 全局符号定义放最前 | Knuth《The Art of Computer Programming》Vol.1 (1968) — Knuth 在每章开头先定义全部符号，后续公式不再重复解释 |
| 公式前加"直觉" | **一句话直觉先于公式** | Pólya《How to Solve It》(1945), "Understanding the Problem" — 必须先理解问题在问什么，再看形式化表达 |
| `## 核心公式` | 直觉→公式→参数→推导 四步 | Pólya 四步法：理解→规划→执行→回顾；对应 直觉→公式→参数→推导 |
| 推导逐步展开 | 不跳步，每步有中间注释 | Clark & Mayer《e-Learning》Ch.10, p.208 — "Segmenting Principle": 复杂过程必须分成小步骤，否则认知过载 |
| `## 手算练习` | 用**具体数字**，不是抽象变量 | Bloom《Taxonomy》Application 层 — 只有用具体数字实际算一次，才能从"理解"跃升到"应用" |
| `## 公式速查表` | 一行一公式，方便查阅 | Norman《The Design of Everyday Things》Ch.3 — 外化记忆，降低考试/写代码时的回忆负担 |

## 固定 5 章模板

```
---
topic: {topic}
dimension: math
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📚 Book: ..."
  - "📖 Paper: ..."
expiry: 12m
status: current
---

# {Topic} 数学基础

> 📚 Book: 作者, 《书名》, Ch.X

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|

> 📚 来源引证

---

## 核心公式

### 公式 1: {名称}

**直觉：** 一句话说清在干什么

$$
... LaTeX ...
$$

> 📚 Book: 作者, Eq. X.Y

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 

**推导过程：**（逐步，不跳步）

> 📖 来源引证

---

## 公式关系图

（ASCII 图展示公式间推导/依赖关系）

---

## 手算练习

### 练习 1: {名称}

**题目：** （给具体数字）

**解答步骤：**
1. 代入公式 X: ...
2. 计算: ...
3. 结果: ...

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
```

## 格式规则

- ✅ 每个公式前有**一句话直觉**（不是公式后）
- ✅ 每个公式后有**教科书方程编号引证**
- ✅ 推导逐步展开，不跳步
- ✅ 符号对照表在最前面
- ✅ 手算练习用**具体数字**
- ❌ 不能只给公式不给直觉
- ❌ 不能公式没有出处

## 完成检查

- [ ] 5 章结构完整
- [ ] 符号表覆盖所有公式中出现的符号
- [ ] 每个公式有直觉 + 引证
- [ ] 手算练习有具体数字

## 教科书来源

- Pólya《How to Solve It》(1945), "Understanding the Problem"
- Knuth《The Art of Computer Programming》Vol.1 (1968), Notation Conventions
- Clark & Mayer《e-Learning》3rd Ed. (2011), Ch.10 "Segmenting Principle", p.205-218
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Bloom《Taxonomy of Educational Objectives》(1956), Application Level
