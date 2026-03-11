# Layer-Specific Best Practices — Detailed Examples

> Extracted from learning-note-taking SKILL.md §9

## ALL layers MUST have numbered sub-items

**Rules:**

1. Use `**(N) Concept Name (中文名):**` format — bold number, bold concept, colon
2. Each sub-point has its own English block + Chinese `>>` block
3. Order sub-points logically: foundational concept first, derived/comparative concepts later
4. If a sub-point itself is long, it can have bullet points inside
5. Minimum 2 sub-items per layer (if only 1 point, still number it as `(1)` for consistency)

---

## ✅ GOOD — sub-divided (clear, scannable)

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
> The kernel slides across the image; at each position it computes a weighted sum of the covered pixels, producing one output value.
>
> > 核在图像上滑动，每个位置对覆盖的像素做加权和，产生一个输出值。
>
> **(3) Weighted sum vs weighted average (加权和 vs 加权平均):**
>
> Weighted sum = Σ(pixel × weight). Weighted average = Σ(pixel × weight) / Σ(weight).
> Blur kernels (all positive, sum=1) are true weighted averages. Sharpening/edge kernels (negative weights, sum≠1) are weighted sums but NOT averages.
>
> > 加权和 = Σ(像素 × 权重)。加权平均 = Σ(像素 × 权重) / Σ(权重)。
> > 模糊核（全正，和=1）是真正的加权平均。锐化/边缘核（有负权重，和≠1）是加权和但不是平均。
```

## ❌ BAD — monolithic paragraph (hard to parse)

```markdown
> **📌 What:**
> A filter (also called a kernel or convolution matrix) is a small matrix (e.g., 3×3, 5×5) that slides across the image. At each position, it computes a weighted sum of the pixel neighborhood — i.e., multiply each pixel by the corresponding kernel weight and sum all products — producing a new output pixel. This sliding weighted-sum operation is called convolution. Note: weighted sum ≠ weighted average. A weighted average divides by the sum of weights (normalizes to 1). Only blur kernels are true weighted averages. Sharpening/edge kernels have negative weights or sum ≠ 1, so they are weighted sums but NOT averages.
```

---

## ⚖️ Compare — use tables

When comparing 2+ concepts/methods, always use a markdown table inside the blockquote.

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

---

## ⚠️ Pitfall — number multiple items

Use **(1), (2), (3)** numbering with bold keywords.

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

---

## 📝 Exam — include expected answers

### Sub-divided by question type (when ≥ 2 types)

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

### Simple (single question type)

```markdown
> **📝 Exam:**
> "Which method is prone to chaining?" → MIN.
> "Which method tends to produce compact clusters?" → MAX or Ward.
>
> > "哪种方法容易产生链接效应？" → MIN。
> > "哪种方法倾向产生紧凑簇？" → MAX 或 Ward。
```

---

## Fidelity Rule (原文保真规则)

Bullet points in the main text (outside Notes block) must **preserve the original PPT/PDF text verbatim** in English, then append a Chinese translation with `—`.

**⚠️ CRITICAL: Do NOT paraphrase, shorten, restructure, or reword the original English text.**

### ❌ BAD (paraphrased)

```markdown
- Filtering manipulates or enhances an image by altering its pixels — 滤波通过改变像素来操作或增强图像
```

### ✅ GOOD (verbatim from PPT)

```markdown
- Filtering in image processing is a technique used to manipulate or enhance an image by **altering its pixels**. It's a fundamental tool that can either **amplify certain features** or **suppress unwanted distortions** — 图像处理中的滤波是一种通过**改变像素**来操作或增强图像的技术。它是一种基本工具，可以**放大某些特征**或**抑制不需要的失真**
```

**Rules:**

1. **English = exact copy** from the original slide
2. **Bold keywords** should match what the slide visually emphasizes
3. **Chinese = natural translation** appended after `—`
4. **Do NOT split** one slide bullet into multiple bullets
5. **When in doubt**, view the slide image (`page_NNN.png`) to verify
