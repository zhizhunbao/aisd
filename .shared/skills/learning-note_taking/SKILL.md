---
name: learning-note_taking
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

When a section contains a **math formula**, notes require special handling:

**⓪ Check `math-concept-library` first (先查公式库):**

Before writing any formula explanation, look up the concept in `.shared/skills/math-concept-library/resources/`:

- `signal_processing.md` — Filters, convolution, frequency domain
- `calculus.md` — Derivatives, gradients, optimization
- `linear_algebra.md` — Matrices, transformations, eigenvalues
- `statistics.md` — Distributions, probability, estimation
- `evaluation_metrics.md` — Precision, recall, F1, IoU, etc.
- `image_processing.md` — Image-specific formulas

If the concept **exists**: reuse its definition, intuition, and formula breakdown — adapt to the lecture context.
If the concept **does not exist**: write the explanation from scratch, then **add it to the library** after completing the notes (see step C below).

**A) Main text (BEFORE the notes block):**

- Write the formula with **full expansion** (compact → expanded)
- Below the formula, list a **symbol legend**: every variable's meaning, type, and range

```markdown
- **SSE** = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖² = Σᵢ Σₓ∈Cᵢ Σⱼ (xⱼ - mᵢⱼ)²
  - Cᵢ = the i-th cluster (set of data points)
  - x = a data point in cluster Cᵢ (d-dimensional vector)
  - mᵢ = centroid (mean) of cluster Cᵢ (d-dimensional vector)
  - ‖x - mᵢ‖² = squared Euclidean distance
  - Overall: total "spread" of all clusters — lower = tighter
```

**B) Inside the notes block, use these dedicated formula layers:**

| Layer       | Icon | Purpose                                               | NOT for                   |
| ----------- | ---- | ----------------------------------------------------- | ------------------------- |
| **Formula** | 📐   | Break down formula structure: what each part does     | Analogies or calculations |
| **Example** | 🔢   | Set up a clear problem, then walk through calculation | Exam questions            |
| **Exam**    | 📝   | Predict exam question types                           | Worked calculations       |

**Distinction between layers:**

|              | 💡 Intuition           | 📐 Formula                                              | 🔢 Example                   |
| ------------ | ---------------------- | ------------------------------------------------------- | ---------------------------- |
| **Approach** | Analogy / mental model | Structural reading of the formula                       | Plug in real numbers         |
| **Style**    | "It's like magnets..." | "Σᵢ means for each cluster, Σₓ means for each point..." | "Given {1,3,7,9}, SSE = ..." |
| **Goal**     | Build intuition        | Understand the math notation                            | Verify you can compute it    |

**Layer order:**

📌 → 🎯 → 💡 → ⚙️ → **📐** → **🔢** → ⚖️ → ⚠️ → 📝

**Rules:**

- **Symbol legend goes in main text** — not inside the notes block.
- **📐 Formula reads the formula piece by piece** — "Σᵢ iterates over all K clusters. For each cluster Cᵢ, Σₓ∈Cᵢ iterates over every data point in that cluster. ‖x - mᵢ‖² computes the squared distance from that point to the centroid."
- **🔢 Example MUST start with a clear problem setup** — describe the scenario BEFORE any computation: what data, how many points, how many clusters, what are the centroids. Then walk through step by step.
- **📝 Exam stays for exam predictions only** — "What question type might test this?" Not a worked example.

**C) After writing notes — add new concepts to the library (新概念入库):**

If you explained a formula that is **not yet in** `math-concept-library/resources/`, add it using the standard entry format defined in `.shared/skills/math-concept-library/SKILL.md`. This ensures future notes can reuse the explanation.

**Template:**

```markdown
- **Formula** = compact = expanded
  - symbol₁ = meaning (type, range)
  - symbol₂ = meaning (type, range)
  - Overall: what it measures

> **📝 Notes:**
>
> **💡 Intuition:**
> Analogy: think of it like [real-world analogy].
>
> > 类比：就像[现实类比]。
>
> **📐 Formula:**
> Reading the formula piece by piece:
>
> - Σᵢ: iterate over all K clusters
> - Σₓ∈Cᵢ: for each point x in cluster i
> - ‖x - mᵢ‖²: squared distance from x to centroid mᵢ
> - Overall: sum up all these squared distances = total "spread"
>
> > 逐段读公式：
> >
> > - Σᵢ：遍历所有K个簇
> > - Σₓ∈Cᵢ：对簇i中的每个点x
> > - ‖x - mᵢ‖²：x到质心mᵢ的平方距离
> > - 整体：把所有平方距离加起来 = 总"散布程度"
>
> **🔢 Example:**
> **Problem:** We have 4 data points in 1D: {1, 3, 7, 9}. They've been assigned to 2 clusters: C₁={1,3} and C₂={7,9}.
> **Question:** What is the SSE?
> **Solution:**
>
> - Centroid m₁ = (1+3)/2 = 2, centroid m₂ = (7+9)/2 = 8
> - SSE = (1-2)² + (3-2)² + (7-8)² + (9-8)² = 1+1+1+1 = **4**
>
> > **题目：** 4个1维数据点：{1, 3, 7, 9}。分为2个簇：C₁={1,3}，C₂={7,9}。
> > **问：** SSE是多少？
> > **解：**
> >
> > - 质心 m₁ = (1+3)/2 = 2，m₂ = (7+9)/2 = 8
> > - SSE = (1-2)² + (3-2)² + (7-8)² + (9-8)² = 1+1+1+1 = **4**
>
> **📝 Exam:**
> "Given these clusters, compute SSE." Must show: formula → plug in each point → sum.
>
> > "给定这些簇，计算SSE。" 必须展示：公式 → 代入每个点 → 求和。
```

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

Patterns learned from effective note-taking:

**⚠️ MANDATORY Rule — EVERY layer MUST have numbered sub-items (每层必须有子分类):**

**No exceptions.** Every layer's content MUST be structured with **numbered sub-items `(1), (2), ...`** for categorization and scannability. Do NOT write monolithic paragraphs. Each sub-item should be self-contained — its own concept/point + bilingual explanation. This rule applies to ALL 9 layers equally.

**Per-layer structure:**

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

**Summary:** **ALL layers** must use `**(N) Name:**` numbered sub-items to force categorization. The only exceptions are when a layer has a highly specialized internal structure (e.g., a table inside a Compare sub-item, or a Problem/Solution block inside an Example sub-item), but the top-level categorization must still be numbered sub-items.

✅ **GOOD — sub-divided (clear, scannable):**

```markdown
> **📌 What:**
> **(1) Filter/Kernel (滤波器/核):**
>
> A small matrix (e.g., 3×3, 5×5) with pre-set or learned weights.
> Also called a convolution matrix. Each weight determines how much the corresponding pixel contributes.
>
> > 一个小矩阵（如3×3、5×5），具有预设或学习到的权重。
> > 也叫卷积矩阵。每个权重决定对应像素的贡献度。
>
> **(2) Convolution operation (卷积运算):**
>
> The kernel slides across the image; at each position it computes a weighted sum of the covered pixels, producing one output value. The full sliding process is called convolution.
>
> > 核在图像上滑动，每个位置对覆盖的像素做加权和，产生一个输出值。整个滑动过程称为卷积。
>
> **(3) Weighted sum vs weighted average (加权和 vs 加权平均):**
>
> Weighted sum = Σ(pixel × weight). Weighted average = Σ(pixel × weight) / Σ(weight).
> Blur kernels (all positive, sum=1) are true weighted averages. Sharpening/edge kernels (negative weights, sum≠1) are weighted sums but NOT averages.
>
> > 加权和 = Σ(像素 × 权重)。加权平均 = Σ(像素 × 权重) / Σ(权重)。
> > 模糊核（全正，和=1）是真正的加权平均。锐化/边缘核（有负权重，和≠1）是加权和但不是平均。
```

❌ **BAD — monolithic paragraph (hard to parse):**

```markdown
> **📌 What:**
> A filter (also called a kernel or convolution matrix) is a small matrix (e.g., 3×3, 5×5) that slides across the image. At each position, it computes a weighted sum of the pixel neighborhood — i.e., multiply each pixel by the corresponding kernel weight and sum all products — producing a new output pixel. This sliding weighted-sum operation is called convolution. Note: weighted sum ≠ weighted average. A weighted average divides by the sum of weights (normalizes to 1). Only blur kernels are true weighted averages. Sharpening/edge kernels have negative weights or sum ≠ 1, so they are weighted sums but NOT averages.
```

**Rules:**

1. Use `**(N) Concept Name (中文名):**` format — bold number, bold concept, colon
2. Each sub-point has its own English block + Chinese `>>` block
3. Order sub-points logically: foundational concept first, derived/comparative concepts later
4. If a sub-point itself is long, it can have bullet points inside
5. Minimum 2 sub-items per layer (if only 1 point, still number it as `(1)` for consistency)

---

**⚖️ Compare — use tables:**

When comparing 2+ concepts/methods, always use a markdown table inside the blockquote. Tables make differences immediately scannable.

```markdown
> **⚖️ Compare:**
> | Feature | Method A | Method B |
> |---|---|---|
> | Shape | Spherical | Any shape |
> | Noise | No handling | Built-in |
>
> > | 特性 | 方法A  | 方法B    |
> > | ---- | ------ | -------- |
> > | 形状 | 仅球形 | 任意形状 |
> > | 噪声 | 无处理 | 内置     |
```

**⚠️ Pitfall — number multiple items:**

When there are multiple pitfalls, use **(1), (2), (3)** numbering with bold keywords. Don't bury multiple issues in one paragraph.

```markdown
> **⚠️ Pitfall:**
> (1) **Chaining effect:** MIN linkage can merge distant clusters through noise bridges.
> (2) **"Including itself"** in core point count is a classic exam trap.
> (3) **Varying density:** single ε can't handle clusters with different densities.
>
> > (1) **链接效应：** MIN方法可能通过噪声桥连接远距离簇。
> > (2) 核心点计数中**"包括自身"**是经典考试陷阱。
> > (3) **密度不均：** 单一ε无法处理不同密度的簇。
```

**📝 Exam — include expected answers and question types:**

Don't just state the question — also include the expected answer pattern so students know what to write. When ≥ 2 distinct question types exist, use numbered sub-items with **bold type labels**.

✅ **GOOD — sub-divided by question type (when ≥ 2 types):**

```markdown
> **📝 Exam:**
> (1) **定义题 (Definition):**
> "What does image sharpening do?" → Enhances edges and details by amplifying the difference between a pixel and its neighbors.
>
> > "图像锐化做什么？" → 通过放大像素与邻居的差异来增强边缘和细节。
>
> (2) **公式解释题 (Formula explanation):**
> "Explain unsharp masking." → `sharpened = original + α × (original − blurred)`.
>
> > "解释反锐化掩模。" → `锐化 = 原始 + α × (原始 − 模糊)`。
>
> (3) **推理题 (Reasoning):**
> "Why should you blur before sharpening?" → Sharpening amplifies ALL high-frequency content, including noise.
>
> > "为什么应该先模糊再锐化？" → 锐化放大所有高频内容，包括噪声。
```

✅ **GOOD — simple (single question type, or short list):**

```markdown
> **📝 Exam:**
> "Which method is prone to chaining?" → MIN.
> "Which method tends to produce compact clusters?" → MAX or Ward.
>
> > "哪种方法容易产生链接效应？" → MIN。
> > "哪种方法倾向产生紧凑簇？" → MAX 或 Ward。
```

**Main text bullets — Fidelity Rule (原文保真规则):**

Bullet points in the main text (outside Notes block) must **preserve the original PPT/PDF text verbatim** in English, then append a Chinese translation with `—`.

**⚠️ CRITICAL: Do NOT paraphrase, shorten, restructure, or reword the original English text.** The English portion is a direct transcription of the slide — it must match the source material exactly. Only the Chinese translation after `—` is added by the note-taker.

❌ **BAD (paraphrased):**

```markdown
- Filtering manipulates or enhances an image by altering its pixels — 滤波通过改变像素来操作或增强图像
```

✅ **GOOD (verbatim from PPT):**

```markdown
- Filtering in image processing is a technique used to manipulate or enhance an image by **altering its pixels**. It's a fundamental tool that can either **amplify certain features** or **suppress unwanted distortions** — 图像处理中的滤波是一种通过**改变像素**来操作或增强图像的技术。它是一种基本工具，可以**放大某些特征**或**抑制不需要的失真**
```

**Rules:**

1. **English = exact copy** from the original slide (preserve full sentences, highlighted keywords, punctuation)
2. **Bold keywords** should match what the slide visually emphasizes (colored text, underlined, bold)
3. **Chinese = natural translation** appended after `—` (not word-for-word translation)
4. **Do NOT split** one slide bullet into multiple bullets — keep the original structure
5. **When in doubt**, view the slide image (`page_NNN.png`) to verify the original text

```markdown
- **Core point:** has ≥ MinPts within ε (**including itself**) — 核心点：ε内有≥MinPts个点（**包括自身**）
- **Border point:** not core, but within ε of a core — 边界点：不是核心但在核心点ε内
```

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

**结构模板：**

```markdown
## Page N

![Page N](path/page_NNN.png)

**Document Title — 文档标题**

**Section Heading — 章节标题**

- Original text from PDF — 中文翻译
- Another point from PDF — 另一个要点的中文翻译
  1. Sub-step from PDF — 子步骤翻译
  2. Another sub-step — 另一个子步骤

| Column — 列名 | Description — 描述                |
| ------------- | --------------------------------- |
| value1        | Meaning of value1 — value1 的含义 |
```

**示例（Lab PDF）：**

```markdown
## Page 1

![Page 1](CST8507_Lab_3_W26_pages/page_001.png)

**CST8507: Natural Language Processing — CST8507：自然语言处理**

**Lab 3: Word Embedding — 实验 3：词嵌入**

**Objective — 目标**

- Load pre-trained word vectors. — 加载预训练词向量。
- Evaluate embeddings using intrinsic metrics — 使用内在评价指标评估词嵌入
```

## Examples

### Example 1: Math/Algorithm Concept (Eigenvalues)

```markdown
> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Reveal natural axes (揭示本质方向):**
>
> Eigenvectors reveal the "natural axes" of a transformation.
> A complex matrix transformation, viewed along eigenvector directions, becomes simple scaling.
>
> > 特征向量揭示了变换的"本质方向"。
> > 复杂的矩阵变换，沿特征向量方向看就变成了简单的缩放。
>
> **(2) Foundation for PCA (PCA的基础):**
>
> PCA uses eigenvectors for dimensionality reduction — finding directions of maximum variance.
> Without eigenvectors, there's no principled way to choose which dimensions to keep.
>
> > PCA 用特征向量降维 — 找到数据方差最大的方向。
> > 没有特征向量，就无法有原则地选择保留哪些维度。
>
> **💡 Intuition:**
> **(1) Revolving door analogy (旋转门类比):**
>
> Imagine pushing a revolving door. Most directions make it spin.
> But one direction only pushes it forward/backward without rotation —
> that direction is the "eigenvector", the displacement magnitude is the "eigenvalue".
>
> > 想象推旋转门。大部分方向推会让门转动。
> > 但有一个方向推只会让门前后移动不转 —
> > 那个方向就是"特征向量"，移动幅度就是"特征值"。
>
> **(2) Stretching rubber sheet (拉伸橡胶布):**
>
> A matrix is like stretching a rubber sheet. Most points move in complex ways.
> Eigenvectors are the directions that only get stretched (or compressed), never rotated.
>
> > 矩阵就像拉伸橡胶布。大部分点移动方式复杂。
> > 特征向量是只被拉伸（或压缩）而不被旋转的方向。
>
> **⚙️ How:**
> **(1) Derivation of characteristic equation (特征方程推导):**
>
> Why det(A-λI) = 0? Because Av = λv rearranges to (A-λI)v = 0.
> For non-zero v to exist, (A-λI) must be singular, meaning its determinant is 0.
>
> > 为什么 det(A-λI) = 0？因为 Av = λv 移项得 (A-λI)v = 0。
> > 要有非零解 v，(A-λI) 必须不可逆，即行列式为 0。
>
> **⚖️ Compare:**
> **(1) Eigendecomposition vs SVD:**
>
> Eigen requires square matrices; SVD works for any matrix.
> SVD is essentially eigendecomposition applied to AᵀA.
>
> > 特征分解要求方阵，SVD 对任意矩阵都有效。
> > SVD 本质是对 AᵀA 做特征分解。
>
> **⚠️ Pitfall:**
> **(1) Complex eigenvalues (复数特征值):**
>
> Not all matrices have real eigenvalues. Rotation matrices have complex eigenvalues —
> because no direction stays unchanged after rotation.
>
> > 不是所有矩阵都有实数特征值。旋转矩阵的特征值是复数 —
> > 因为旋转后没有方向保持不变。
>
> **(2) Confusing eigenvalue with eigenvector (混淆特征值和特征向量):**
>
> The eigenvalue λ is the scaling factor; the eigenvector v is the direction.
> Students often swap which is which in exam answers.
>
> > 特征值 λ 是缩放因子；特征向量 v 是方向。
> > 学生在考试中经常搞混哪个是哪个。
```

### Example 2: CV/ML Concept (Max Pooling)

```markdown
> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Reduce computational cost (降低计算成本):**
>
> After convolution, feature maps are too large — expensive to compute and store.
>
> > 卷积后特征图太大，计算和存储成本高。
>
> **(2) Add positional tolerance (增加位置容忍度):**
>
> We care about WHETHER a feature exists, not its exact pixel location.
> Pooling adds spatial invariance — a cat shifted by 2 pixels still gets detected.
>
> > 我们关心特征"有没有"，而不是"在哪个精确像素"。
> > 池化增加空间不变性 — 猫移动2像素仍然能被检测到。
>
> **💡 Intuition:**
> **(1) Map zoom analogy (地图缩放类比):**
>
> Like zooming out on a map — you lose street-level detail but still see city shapes.
>
> > 像缩小地图 — 丢失街道细节但保留城市轮廓。
>
> **(2) Strongest signal wins (最强信号胜出):**
>
> Max pooling keeps the strongest signal in each region, like picking the loudest voice in each room.
>
> > 最大池化保留每个区域中最强的信号，像从每个房间里挑出最大声的声音。
>
> **⚠️ Pitfall:**
> **(1) No learnable parameters (无可学习参数):**
>
> Pooling has NO learnable parameters — don't confuse it with convolution.
> Convolution learns filters; pooling just applies a fixed rule (max or average).
>
> > 池化没有可学习参数 — 不要跟卷积层混淆。
> > 卷积学习滤波器；池化只是应用固定规则（取最大值或平均值）。
>
> **(2) Information loss (信息损失):**
>
> Aggressive pooling (large kernel or stride) can destroy fine-grained spatial details needed for tasks like segmentation.
>
> > 激进的池化（大核或大步长）会破坏分割等任务需要的精细空间细节。
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> Given input size 4×4 with 2×2 pooling and stride 2, output is 2×2.
> Formula: output = (input - pool_size) / stride + 1.
>
> > 给定 4×4 输入，2×2 池化，stride=2，输出为 2×2。
> > 公式：output = (input - pool_size) / stride + 1。
>
> **(2) 对比题 (Comparison):**
>
> "Max pooling vs average pooling — when to use which?" → Max for feature detection (keep strongest), average for smooth downsampling.
>
> > "最大池化 vs 平均池化 — 什么时候用哪个？" → 最大用于特征检测（保留最强），平均用于平滑下采样。
```

### Example 3: Math Formula (SSE in K-Means)

```markdown
- **SSE** = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖² = Σᵢ Σₓ∈Cᵢ Σⱼ (xⱼ - mᵢⱼ)²
  - Cᵢ = the i-th cluster (a set of data points)
  - x = a data point in cluster Cᵢ (a d-dimensional vector)
  - mᵢ = centroid (mean) of cluster Cᵢ (a d-dimensional vector)
  - ‖x - mᵢ‖² = squared Euclidean distance between x and its centroid
  - Overall: total "spread" of all clusters — lower SSE = tighter clusters

> **📝 Notes:**
>
> **💡 Intuition:**
> **(1) Iron filings analogy (铁屑类比):**
>
> Like measuring how "scattered" iron filings are around magnets. Each filing's distance to its magnet is squared and summed. Tighter clusters = lower total.
>
> > 像测量铁屑围绕磁铁的"散布程度"。每个铁屑到磁铁的距离平方后求和。越紧凑 = 总和越小。
>
> **(2) Why squared? (为什么平方？):**
>
> Squaring penalizes outliers more heavily — a point 10 units away contributes 100, not 10. This makes SSE sensitive to distant points.
>
> > 平方会更重地惩罚离群点 — 距离10的点贡献100而不是10。这使SSE对远距离点敏感。
>
> **📐 Formula:**
> **(1) SSE breakdown (SSE逐段拆解):**
>
> Reading SSE = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖² piece by piece:
>
> - Σᵢ: iterate over all K clusters (i = 1, 2, ..., K)
> - Σₓ∈Cᵢ: for each data point x that belongs to cluster i
> - ‖x - mᵢ‖²: compute the squared Euclidean distance from x to its centroid mᵢ
> - Overall: sum up ALL these squared distances across ALL clusters = total "spread"
>
> > 逐段读 SSE = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖²：
> >
> > - Σᵢ：遍历所有K个簇（i = 1, 2, ..., K）
> > - Σₓ∈Cᵢ：对属于簇i的每个数据点x
> > - ‖x - mᵢ‖²：算x到它的质心mᵢ的平方欧氏距离
> > - 整体：把所有簇中所有点的平方距离加起来 = 总"散布程度"
>
> **🔢 Example:**
> **(1) 1D SSE calculation (一维SSE计算):**
>
> **Problem:** We have 4 data points in 1D: {1, 3, 7, 9}. They've been assigned to 2 clusters: C₁={1,3} and C₂={7,9}.
> **Question:** What is the SSE?
> **Solution:**
>
> - Centroid m₁ = (1+3)/2 = 2, centroid m₂ = (7+9)/2 = 8
> - Cluster 1: (1-2)² + (3-2)² = 1 + 1 = 2
> - Cluster 2: (7-8)² + (9-8)² = 1 + 1 = 2
> - SSE = 2 + 2 = **4**
>
> > **题目：** 4个1维数据点：{1, 3, 7, 9}。分为2个簇：C₁={1,3}，C₂={7,9}。
> > **问：** SSE是多少？
> > **解：**
> >
> > - 质心 m₁ = (1+3)/2 = 2，m₂ = (7+9)/2 = 8
> > - 簇1：(1-2)² + (3-2)² = 1 + 1 = 2
> > - 簇2：(7-8)² + (9-8)² = 1 + 1 = 2
> > - SSE = 2 + 2 = **4**
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> "Given these clusters, compute SSE." Must show: formula → plug in each point → sum.
>
> > "给定这些簇，计算SSE。" 必须展示：公式 → 代入每个点 → 求和。
>
> **(2) 概念题 (Conceptual):**
>
> "What happens to SSE as K increases?" → SSE always decreases (more clusters = tighter fit), but eventually overfits.
>
> > "K增大时SSE会怎样？" → SSE总是下降（更多簇 = 更紧密），但最终过拟合。
```

### Example 4: Concept Comparison Section (Inter-Cluster Distance Methods)

```markdown
### 4.4 簇间距离定义 (Inter-Cluster Distance Methods)

![Page 29](week6_clustering_slides_pages/page_029.png)

**MIN (Single Linkage):** Same two-cluster diagram, but now a single yellow line connects the two closest points (one from each cluster) — this shortest cross-cluster distance is used. "MIN" is highlighted. Intuition: only the nearest pair matters.

**MIN（单链接）：** 同样的两个簇图，但现在一条黄色线连接了两个最近的点（每个簇各一个）— 使用最短跨簇距离。"MIN"被高亮。直觉：只有最近的那一对点有关系。

| Method  | Definition                          | Also Called       |
| ------- | ----------------------------------- | ----------------- |
| **MIN** | Min distance between any two points | Nearest neighbor  |
| **MAX** | Max distance between any two points | Farthest neighbor |

> **📝 Notes:**
>
> **📌 What:**
> **(1) Five linkage methods (五种链接方法):**
>
> Five methods to compute d(AB, C) after merging A and B: MIN, MAX, Average, Centroid, Ward.
>
> > 合并A和B后计算d(AB, C)的五种方法：MIN、MAX、Average、Centroid、Ward。
>
> **(2) Shape determinism (形状决定性):**
>
> The choice of linkage method completely determines the dendrogram shape — same data, different method → completely different tree.
>
> > 链接方法的选择完全决定树状图形状 — 同一数据、不同方法 → 完全不同的树。
>
> **💡 Intuition:**
> **(1) Country distance analogy (国家距离类比):**
>
> Measuring "distance" between two countries: MIN = nearest border crossing, MAX = farthest cities, Average = all city pairs, Centroid = capitals, Ward = population spread increase.
>
> > 测量两国"距离"：MIN = 最近边境，MAX = 最远城市，Average = 所有城市对，质心 = 首都，Ward = 人口扩散增量。
>
> **⚖️ Compare:**
> **(1) Method comparison table (方法对比表):**
>
> | Method | Tendency         | Weakness              |
> | ------ | ---------------- | --------------------- |
> | MIN    | Chain-like       | Chaining from noise   |
> | MAX    | Compact          | Breaks large clusters |
> | Ward   | Compact, min SSE | Biased to equal sizes |
>
> > | 方法 | 倾向          | 弱点         |
> > | ---- | ------------- | ------------ |
> > | MIN  | 链状          | 噪声导致链接 |
> > | MAX  | 紧凑          | 拆分大簇     |
> > | Ward | 紧凑、最小SSE | 偏向等大小   |
>
> **⚠️ Pitfall:**
> **(1) Chaining effect (链接效应):**
>
> MIN merges through noise bridges — a few stray points between distant clusters can chain them together.
>
> > MIN通过噪声桥合并 — 远距离簇之间的几个散点可以把它们串联起来。
>
> **(2) Dendrogram inversions (树状图反转):**
>
> Centroid method can produce later merges at lower distances — the dendrogram "goes backward", which is confusing.
>
> > 质心方法可能后续合并距离反而更低 — 树状图"倒退"，令人困惑。
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> "Compute inter-cluster distance using MIN/MAX/Average." → MIN = smallest entry, MAX = largest, Average = sum ÷ count.
>
> > "用MIN/MAX/Average计算簇间距离。" → MIN = 最小值，MAX = 最大值，Average = 总和 ÷ 个数。
>
> **(2) 推理题 (Reasoning):**
>
> "Which method is most sensitive to outliers?" → MIN, because a single outlier point can bridge two clusters.
>
> > "哪种方法对离群值最敏感？" → MIN，因为一个离群点就能桥接两个簇。
```
