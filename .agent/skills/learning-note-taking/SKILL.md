---
name: learning-note-taking
description: Add deep, bilingual (Chinese+English) study notes to lecture materials. Use when (1) user asks to add notes to extracted PDFs/slides, (2) mentions "笔记" or "notes", (3) organizing course content.
---

# Learning Note-Taking

## Objectives

Add deep, insightful bilingual (Chinese + English) study notes to lecture materials. Notes must go beyond restating slide content — they should explain **why**, build **intuitive understanding**, reveal **connections**, and flag **pitfalls**.

## Core Principle: Notes ≠ Translation

Slides already cover **What** and **How**. Notes must add the layers that slides miss.

> ⚠️ **Cross-cutting Rule:** When notes include formulas, conclusions, or non-trivial claims, follow the **Source Citation & Proof Rule** (`learning-source_citation` SKILL.md). Every claim must cite a textbook source; every conclusion must have a proof or derivation. No unsourced content (不能拍脑袋).
> ⚠️ **通用规则：** 当笔记中包含公式、结论或重要论述时，必须遵守**来源引证与证明规则**（`learning-source_citation` SKILL.md）。所有论述必须注明教科书来源，结论必须附带证明或推导。

❌ **BAD (shallow):** Restating slide content in another language

```
> Canny edge detection step 1 is noise reduction using Gaussian filter.
> Canny 边缘检测第1步是降噪，使用高斯滤波器平滑图像。
```

✅ **GOOD (deep):** Explaining WHY with bilingual nested format

```
> **🎯 Why:**
> Gradient calculation is essentially differentiation, which amplifies noise.
> Without smoothing, noise pixels produce large gradients and get misidentified as edges.
>> 梯度计算本质是求导，求导会放大噪声。
>> 不先平滑的话，噪声点也会产生大梯度，被误判为边缘。
```

## Instructions

### 1. The 9-Layer Note Framework

Based on Bloom's Taxonomy. **Only show layers with content** — omit layers with nothing to say. Layer order is fixed when shown.

| #   | Layer         | Icon | Core Question                                    | Depth Guidance                                |
| --- | ------------- | ---- | ------------------------------------------------ | --------------------------------------------- |
| 1   | **What**      | 📌   | Definition, core concept                         | Brief 1-2 sentences; only if slide is unclear |
| 2   | **Why**       | 🎯   | Why does this exist? What problem does it solve? | ⭐ Key layer — must have real insight         |
| 3   | **Intuition** | 💡   | Analogy, geometric meaning, mental model         | ⭐ Abstract concepts need strong analogies    |
| 4   | **How**       | ⚙️   | Why this formula? Derivation motivation          | Explain reasoning, not just repeat formula    |
| 5   | **Formula**   | 📐   | Break down formula structure piece by piece      | Only for sections WITH formulas (see §7)      |
| 6   | **Example**   | 🔢   | Worked calculation with concrete numbers         | Only for sections WITH formulas (see §7)      |
| 7   | **Compare**   | ⚖️   | Differences and connections to related concepts  | Connect to other concepts in this course      |
| 8   | **Pitfall**   | ⚠️   | Common mistakes, confusions                      | ⭐ Key layer — must have real insight         |
| 9   | **Exam**      | 📝   | Typical question types, NOT worked examples      | Predict how this could be tested              |

### 2. Workflow

1. **Analyze Structure**: Identify every concept, step, or section in the material.
2. **Check Knowledge Libraries** (查库): Before writing, look up encountered concepts in reusable libraries:
   - Math formulas → `.shared/skills/math-concept-library/resources/` (reuse definitions, intuitions, breakdowns)
   - Concepts/terms → `.shared/skills/concept-glossary/resources/` (reuse definitions, analogies, history)
3. **Assess Depth Need**: For each concept, decide which layers are most valuable (slides already cover What + How at surface level).
4. **Write Deep Notes**: For each selected layer, write bilingual content that adds genuine insight. Adapt library entries to the lecture context.
5. **Self-Check**: Re-read each note and ask "Does this add something the slide doesn't already say?" If not, rewrite or remove.
6. **Update Libraries** (入库): After completing notes, add new concepts/formulas back to the libraries (see §7 step C for formulas, and `concept-glossary` SKILL.md for concepts). Update `Appears In` for any reused entries.

### 3. Note Format (Bilingual, Compact)

Rules:

- **Only show layers with content** — no empty layers, no "—" placeholders
- **Layer order is fixed** when shown: 📌 → 🎯 → 💡 → ⚙️ → 📐 → 🔢 → ⚖️ → ⚠️ → 📝
- **Layer headers: English only** with icon (no Chinese in headers)
- **Content: English first** in `>`, then Chinese in `>>` nested blockquote
- **At least 3 layers** must have content per note block
- **`>>` block termination:** Every Chinese `>>` block MUST end with an empty `>>` line to properly close the nested blockquote. Without this, the next `>` line may render incorrectly.
- **⚠️ Mandatory sub-division:** EVERY layer MUST use **`(N) Name:`** numbered sub-items to categorize its content. Do NOT write monolithic paragraphs. Each sub-item is self-contained with its own English + Chinese bilingual block. Minimum 2 sub-items per layer; if only 1 point exists, still number it as `(1)` for consistency. See §9 for per-layer formatting details.
- **Sub-layer spacing:** After a `**(N) Concept Name:**` heading, add an empty `>` line before the content begins

```markdown
> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Reason A (原因A):**
>
> English explanation with depth — answer WHY, not just WHAT.
>
> > 中文解释 — 回答"为什么"，而不是重复"是什么"。
>
> **(2) Reason B (原因B):**
>
> Another insight about why this matters.
>
> > 另一个关于为什么重要的洞察。
>
> **💡 Intuition:**
> **(1) Analogy A (类比A):**
>
> Think of it like [analogy]...
>
> > 类比：就像[类比]...
>
> **(2) Analogy B (类比B):**
>
> Another way to think about it...
>
> > 另一种理解方式...
>
> **⚖️ Compare:**
> **(1) X vs Y:**
>
> Key difference is...
>
> > 关键区别在于...
>
> **(2) X vs Z:**
>
> Another comparison...
>
> > 另一个对比...
>
> **⚠️ Pitfall:**
> **(1) Confusion trap (混淆陷阱):**
>
> Don't confuse X with Y — they look similar but...
>
> > 不要混淆 X 和 Y — 它们看起来相似但...
>
> **(2) Common mistake (常见错误):**
>
> Students often forget that...
>
> > 学生经常忘记...
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> Given [input], calculate [output]. → Show formula → plug in → result.
>
> > 给定[输入]，计算[输出]。→ 列公式 → 代入 → 结果。
>
> **(2) 概念题 (Conceptual):**
>
> "Explain why X is needed." → Because [reason].
>
> > "解释为什么需要X。" → 因为[原因]。
```

### 4. Language Rules

- **English** in `>` single blockquote, **Chinese** in `>>` nested blockquote
- Each language should read naturally — NOT word-for-word translation
- Technical terms: use English naturally in both languages (e.g., "CNN", "ReLU", "eigenvalue")
- Code comments: bilingual
- Code variable names: English

### 5. Quality Checklist

Before finalizing each note, verify:

- [ ] At least 3 layers have substantial content
- [ ] Empty layers are omitted (NOT shown with "—")
- [ ] Layer order is correct when shown: 📌 → 🎯 → 💡 → ⚙️ → 📐 → 🔢 → ⚖️ → ⚠️ → 📝
- [ ] Why and Pitfall layers have real insight (not restating slides)
- [ ] English in `>`, Chinese in `>>`
- [ ] Every `>>` Chinese block ends with an empty `>>` line (blockquote termination)
- [ ] Sub-layer `**(N)**` headings have an empty `>` line after them before content
- [ ] Both languages read naturally (not word-for-word translation)
- [ ] Multi-concept layers are sub-divided with **(1), (2), ...** numbering
- [ ] Exam layer with ≥ 2 question types uses numbered sub-items with bold type labels
- [ ] Would a student actually benefit from reading this?

### 6. Submission Requirements

When original content mentions submission requirements, ALWAYS include:

```markdown
> **📋 Submission:**
>
> - Screenshots: Save to Lab1.docx
> - File naming: lab1_code.py
> - Submit: Upload zip to Brightspace
>   > - 截图保存到 Lab1.docx
>   > - 文件命名: lab1_code.py
>   > - 压缩上传到 Brightspace
```

### 7. Formula Explanation Protocol (公式解读规范)

When a section contains a **math formula**, notes require special handling with 3 steps:

1. **⓪ Check library first**: Look up `.shared/skills/math-concept-library/resources/` — reuse if exists, add after if new
2. **A) Main text**: Write formula with full expansion + symbol legend (BEFORE notes block)
3. **B) Notes block**: Use dedicated layers — 📐 Formula (structure), 🔢 Example (calculation), 📝 Exam (predictions)
4. **C) After writing**: Add new concepts back to the library

> 📖 See [references/formula_protocol.md](references/formula_protocol.md) for detailed templates, layer distinction tables, and complete worked examples.

### 8. Image Description Protocol (图片描述规范)

**EVERY image** in the notes gets a single-line bilingual title — placed directly below the image.

**Rules:**

1. **Each image gets ONE line:** `**Slide Title:** — 中文翻译` — plain text (NOT inside `>` blockquote), placed directly below the image
2. **Single line format:** `**English Title:** — 中文翻译` — English title from the slide followed by `—` and a direct Chinese translation of the title. NO separate English/Chinese paragraphs.
3. **NO image visual descriptions** — do NOT write paragraphs describing what the image shows (e.g., "Diagram showing...", "Slide showing..."). The title is just a translation of the slide title, NOT a description of the image content.
4. **NO duplicate titles** — if the slide title and the image description are the same text, keep only ONE line with the `— 中文` format. Do NOT have both a description line and a separate slide text line.
5. The **`📝 Notes` block** still appears **once** at the end of the entire section (after all images), providing deeper analysis
6. **Main text bullet points** under an image must follow the **Fidelity Rule** (see §10 below): `English verbatim from slide — 中文翻译` on the same line
7. **Per-slide bullet placement:** Each slide's bullet points MUST appear **directly after that slide's image + title** — NEVER grouped together after multiple slides. The order is always: `image → title → that slide's bullet points → next image → ...`
8. **No cross-slide merging:** Do NOT combine, rewrite, or reorganize bullet points from multiple slides into one unified list. Each slide's text is transcribed **separately** where it belongs. The Notes block at the end is where you synthesize and analyze across slides.
9. **Do NOT touch `📝 Notes` blocks** — they already have bilingual content and follow a different format.

**Applies to:** ALL images — step-by-step algorithm walkthroughs, concept definition slides, comparison diagrams, before/after examples, formula illustration slides.

**Structure:**

```markdown
### X.X Section Title

![Page N](path/to/image.png)

**Slide Title:** — 幻灯片标题中文翻译

- Verbatim bullet point from THIS slide — 中文翻译
- Another bullet point from THIS slide — 另一个要点的中文翻译

![Page N+1](path/to/next_image.png)

**Next Slide Title:** — 下一张幻灯片标题

- Bullet points from THIS slide (Page N+1) — 中文翻译

> **📝 Notes:**
> (deep analysis of the entire section — 7-layer framework)
```

**Example 1** (concept slide):

```markdown
![Page 38](lecture1_slides_pages/page_038.png)

**Language is Ambiguous: Words Have Many Meanings:** — 语言是歧义的：词有多种含义

- word "bass" can refer to a type of fish or a low-frequency sound. — 词"bass"可以指一种鱼或低频声音。
- The word "bank" can refer to a financial institution or the edge of a river. — 词"bank"可以指金融机构或河岸。
```

**Example 2** (title-only slide with reference):

```markdown
![Page 25](lecture1_slides_pages/page_025.png)

**History of NLP:** — NLP历史

Ref: https://example.com/nlp-history
```

### 9. Layer-Specific Best Practices (各层最佳实践)

**⚠️ MANDATORY Rule — EVERY layer MUST have numbered sub-items (每层必须有子分类):**

Use `**(N) Concept Name (中文名):**` format. Minimum 2 sub-items per layer.

| Layer            | Sub-layer format                          | Example                                                  |
| ---------------- | ----------------------------------------- | -------------------------------------------------------- |
| 📌 **What**      | `(1) Concept A:` / `(2) Concept B:`       | (1) Filter/Kernel / (2) Convolution operation            |
| 🎯 **Why**       | `(1) Reason A:` / `(2) Reason B:`         | (1) Why learnable filters? / (2) Why padding matters?    |
| 💡 **Intuition** | `(1) Analogy A:` / `(2) Analogy B:`       | (1) Convolution as a question / (2) Stride as zoom level |
| ⚙️ **How**       | `(1) Step/mechanism A:` / `(2) Step B:`   | (1) Forward pass / (2) Backward pass                     |
| 📐 **Formula**   | `(1) Formula A:` / `(2) Formula B:`       | (1) SSE breakdown / (2) Entropy breakdown                |
| 🔢 **Example**   | `(1) Scenario A:` / `(2) Scenario B:`     | (1) Predict with max pool / (2) Predict with avg pool    |
| ⚖️ **Compare**   | `(1) Comparison A:` / `(2) Comparison B:` | (1) CNN vs RNN / (2) Max vs Avg Pooling                  |
| ⚠️ **Pitfall**   | `(1) Mistake A:` / `(2) Mistake B:`       | (1) Chaining effect / (2) "Including itself" trap        |
| 📝 **Exam**      | `(1) 题型A (Type A):` / `(2) 题型B:`      | (1) 计算题 / (2) 概念题 / (3) 对比题                     |

Key layer-specific rules:
- **⚖️ Compare**: Always use markdown **tables** inside blockquotes
- **⚠️ Pitfall**: Use **(1), (2), (3)** with bold keywords
- **📝 Exam**: Include expected answers; use numbered sub-items when ≥ 2 question types
- **Fidelity Rule**: Main text bullets must preserve original PPT text verbatim in English

> 📖 See [references/layer_best_practices.md](references/layer_best_practices.md) for detailed ✅/❌ examples of each layer format and the Fidelity Rule.

### 10. Teacher Material Formatting Mode (教师资料格式化模式)

当处理**教师原始资料**（Lab PDF、Assignment 文档等）时，使用 **纯格式化 + 翻译** 模式，**不添加 📝 Notes 块**。

**适用场景：**

- Lab 实验指导文档（如 `CST8507 Lab 3_W26.pdf`）
- Assignment 作业说明文档
- 任何教师分发的操作/说明性 PDF

**与 Slides 笔记的区别：**

| 维度        | Slides 笔记模式 (§1-§9) | 教师资料格式化模式 (§10) |
| ----------- | ----------------------- | ------------------------ |
| 📝 Notes 块 | ✅ 必须，9 层框架       | ❌ **不加**              |
| 中文翻译    | 在 `>>` 嵌套引用块中    | 在同一行 ` — 中文翻译`   |
| 内容深度    | 深度分析、类比、陷阱    | 仅翻译，不额外分析       |
| 页面截图    | 保留                    | 保留                     |
| 原文保真    | ✅ Fidelity Rule        | ✅ Fidelity Rule         |

**格式规则：**

1. **保留页面截图**：`![Page N](path/page_NNN.png)` 直接放在页面开头
2. **标题格式**：`**English Title — 中文标题**`
3. **正文要点**：`- English verbatim from PDF — 中文翻译`（同一行，`—` 分隔）
4. **表格**：表头和内容都加双语 `English — 中文`
5. **代码块**：原样保留，不翻译
6. **移除模板结构**：去掉 `### 📷 Page Image`、`### 📝 Text Content`、`### ✍️ Notes` 等 PDF 转换工具生成的模板标记
7. **Fidelity Rule 适用**：英文部分忠实还原原文，中文部分自然翻译

> 📖 See [references/note_templates.md](references/note_templates.md) for page layout templates and complete examples.

