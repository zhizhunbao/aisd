---
name: learning-lecture-storyline
description: Reorganize lecture slides into a coherent storyline narrative for deeper understanding. Use when (1) user asks to create a "storyline" from slides, (2) user wants to understand the logical progression of a lecture, (3) user mentions reorganizing or restructuring lecture content for better comprehension.
---

# Learning Lecture Storyline

## Objectives

Transform fragmented lecture slides into a **coherent narrative story** that reveals the logical progression of ideas, making technical concepts easier to understand by showing _why_ each new concept was needed (problem → motivation → solution → new problem → ...).

## Core Philosophy

> **Slides tell you WHAT to learn. A storyline tells you WHY each idea exists.**

Traditional slides present topics in blocks (A, B, C, D). A storyline connects them causally:

- A has a problem → which motivates B
- B improves on A but still has a flaw → which motivates C
- C solves B's flaw but introduces a new challenge → which motivates D

This "打怪升级" (boss-fight progression) structure maps naturally to how technology evolves.

> ⚠️ **Cross-cutting Rule:** Follow the **Source Citation & Proof Rule** (`learning-source_citation` SKILL.md). Key technical claims must cite textbook sources; formulas embedded in the storyline must reference their derivation (e.g., "详见 tutorial §N").
> ⚠️ **通用规则：** 遵守**来源引用与证明规则**（`learning-source_citation` SKILL.md）。关键技术断言须注明教科书来源，嵌入的公式须指向推导出处（如"详见 tutorial §N"）。

## Instructions

### Phase 1: Extract & Analyze Source Material

1. **Read the PDF/slides** using `dev-pdf_processing` or PyMuPDF (`fitz`).
2. **Check for existing notes**: Look for `*_slides.md` or `*_notes.md` in the same `notes/` directory — these contain valuable Chinese annotations.
3. **Identify the overarching question**: What central problem is the entire lecture trying to solve? (e.g., "How to predict the next word?")
4. **Map the technology evolution chain**: List each approach in order and identify:
   - What problem it solves
   - What new problem it introduces (its limitation)
   - How it transitions to the next approach

### Phase 2: Design the Storyline Structure

Use this **standard narrative template**:

```markdown
# Lecture N 故事线：[一句话主题]

> **Source:** `[filename].pdf`
> **核心主题：** [用一句通俗的话概括整个讲在解决什么问题]
> **故事线：** [用一个比喻描述进化过程]

---

## 🎬 序幕：我们在解决什么问题？

[定义核心问题，给出直观例子，说明为什么重要]

## 📚 第一章：[数学/理论基础]

[为后续方案铺垫必要的知识]

## 🎭 第二章：方案一——[名称]（✗ 失败/部分成功）

[介绍方案 → 展示效果 → 暴露致命问题 → 🔑 故事转折点]

## 📖 第三章：方案二——[名称]（⚡ 有缺陷）

[由上一章的问题引出 → 介绍方案 → 暴露新问题 → 🔑 故事转折点]

## 🏆 第四章：方案三——[名称]（✅ 解决！）

[由上一章的问题引出 → 介绍方案 → 解释为什么能解决前面的问题]

## 📹 [评估/应用章节]（如适用）

## 🗺️ 全局回顾：技术演进路线图

[ASCII 路线图 + 对比表格]

## 📝 考试/复习重点检查清单

[Checklist 格式]
```

### Phase 3: Write Each Chapter

For each chapter, follow these writing guidelines:

#### 3.1 Chapter Opening — Motivation First

每章开头**必须**回答：「为什么我们需要这个？」 从上一章的 ❗ 问题自然引出。

```markdown
> 🔑 **故事转折点：** [上一个方案]的[具体问题]使得我们不得不寻找新方法 → [新方案]登场！
```

#### 3.2 Concept Explanation — 四层递进法

对每个核心概念，按以下四层递进解释：

| 层次                | 内容                 | 示例                            |
| ------------------- | -------------------- | ------------------------------- |
| **① 一句话定义**    | 用最通俗的语言       | "RNN = 一个神经元 + 一根回忆线" |
| **② 公式/原理**     | 精确的数学描述       | `h₁ = W₁·x₁ + W₂·h₀ + b`      |
| **③ 具体例子**      | 用课程中的例子走一遍 | "the students opened their..."  |
| **④ 类比/记忆技巧** | 生活化比喻           | "h₁ 就像不断更新的笔记"         |

#### 3.3 Transitions — Problem → Solution Arc

每章结尾**必须**包含一个失败/问题展示，用来无缝过渡到下一章：

```markdown
### X.N ❗ [方案名]的致命问题——[问题名]

[用具体例子展示失败场景]

> 🔑 **故事转折点：** [问题总结] → 我们需要[下一个方案的核心能力]！
```

#### 3.4 Comparisons — Use Tables

在新方案引入后，用对比表格清晰展示进步：

```markdown
| 维度   | 旧方案 | 新方案  |
| ------ | :----: | :-----: |
| 能力1  |   ❌   |   ✅    |
| 能力2  |   ❌   |   ✅    |
| 新问题 |  N/A   | ⚠️ 描述 |
```

### Phase 4: Write the Global Review

#### 4.1 ASCII Evolution Roadmap

必须包含一个 ASCII 路线图，展示完整技术演进链：

```
┌──────────────────────────────────────────┐
│ 技术演进路线图                            │
│                                          │
│ 方案1                                    │
│ ✅ 优点                                  │
│ ❌ 致命问题                              │
│         │                                │
│         ▼                                │
│ 方案2                                    │
│ ✅ 解决了方案1的问题                     │
│ ❌ 新的致命问题                          │
│         │                                │
│         ▼                                │
│ 方案3                                    │
│ ✅ 解决了方案2的问题                     │
│         │                                │
│         ▼                                │
│ 下一站：...                              │
└──────────────────────────────────────────┘
```

#### 4.2 Transition Summary Table

```markdown
| 从 → 到 | 解决了什么核心问题？ |
| ------- | -------------------- |
| A → B   | [一句话]             |
| B → C   | [一句话]             |
```

#### 4.3 Review Checklist

用 `- [ ]` 格式列出所有需要掌握的考点，对应各章核心内容。

### Phase 5: Quality Checks

在完成故事线后，执行以下检查：

- [ ] **因果完整性**: 每个新方案的引入都有明确的"因为前面的方案有X问题"的动机
- [ ] **零跳跃原则**: 没有突然冒出来的概念——每个术语在使用前都已被解释
- [ ] **例子一致性**: 尽量全篇使用同一个累积例子（如 "the students opened their..."）
- [ ] **公式覆盖**: 所有关键公式都有"一句话直觉 + 数学表达 + 例子"三层解释
- [ ] **转折标记**: 每个章节过渡处都有 `🔑 故事转折点` 标记
- [ ] **路线图**: 文末包含完整的 ASCII 技术演进路线图
- [ ] **复习清单**: 文末包含 checklist 格式的考试要点

## Formatting Rules

### Language

- **主体语言**: 中文
- **术语处理**: 首次出现时用 "中文 (English)" 格式，之后可只用中英文任一
- **公式**: 用 code block 或 inline code 展示，确保可读性
- **Emoji**: 章节标题使用 emoji 增加视觉区分（🎬🎭📚📖🏆🗺️📝）

### Structure

- 用 `---` 分隔符隔开主要章节
- 每章内用 `###` 级别标题划分小节
- 对比用表格，流程用代码块缩进，重点用加粗
- 类比和记忆技巧用 `> 💡` blockquote 高亮

### Naming Convention

- 输出文件名: `[topic_key]_storyline.md`
- 存放位置: `courses/[course]/notes/`

## Output File Structure

```text
courses/[course]/
├── slides/
│   └── [topic].pdf                      # Source slides
└── notes/
    ├── [topic_key]_slides.md            # Raw extraction (if exists)
    ├── [topic_key]_notes.md             # Detailed notes (if exists)
    └── [topic_key]_storyline.md         # ⭐ This skill's output
```

## Example Reference

See `courses/nlp/notes/lecture5_storyline.md` for a complete example that transforms a 63-page NLP lecture (covering N-gram → FFNN → RNN → LSTM) into a coherent storyline narrative.
