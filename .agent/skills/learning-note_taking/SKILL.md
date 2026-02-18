---
name: learning-note_taking
description: Add deep, bilingual (Chinese+English) study notes to lecture materials. Use when (1) user asks to add notes to extracted PDFs/slides, (2) mentions "笔记" or "notes", (3) organizing course content.
---

# Learning Note-Taking

## Objectives

Add deep, insightful bilingual (Chinese + English) study notes to lecture materials. Notes must go beyond restating slide content — they should explain **why**, build **intuitive understanding**, reveal **connections**, and flag **pitfalls**.

## Core Principle: Notes ≠ Translation

Slides already cover **What** and **How**. Notes must add the layers that slides miss.

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

### 1. The 7-Layer Note Framework

Based on Bloom's Taxonomy. **Only show layers with content** — omit layers with nothing to say. Layer order is fixed when shown.

| #   | Layer         | Icon | Core Question                                    | Depth Guidance                                |
| --- | ------------- | ---- | ------------------------------------------------ | --------------------------------------------- |
| 1   | **What**      | 📌   | Definition, core concept                         | Brief 1-2 sentences; only if slide is unclear |
| 2   | **Why**       | 🎯   | Why does this exist? What problem does it solve? | ⭐ Key layer — must have real insight         |
| 3   | **Intuition** | 💡   | Analogy, geometric meaning, mental model         | ⭐ Abstract concepts need strong analogies    |
| 4   | **How**       | ⚙️   | Why this formula? Derivation motivation          | Explain reasoning, not just repeat formula    |
| 5   | **Compare**   | ⚖️   | Differences and connections to related concepts  | Connect to other concepts in this course      |
| 6   | **Pitfall**   | ⚠️   | Common mistakes, confusions                      | ⭐ Key layer — must have real insight         |
| 7   | **Exam**      | 📝   | Typical question types, calculation patterns     | Predict how this could be tested              |

### 2. Workflow

1. **Analyze Structure**: Identify every concept, step, or section in the material.
2. **Assess Depth Need**: For each concept, decide which layers are most valuable (slides already cover What + How at surface level).
3. **Write Deep Notes**: For each selected layer, write bilingual content that adds genuine insight.
4. **Self-Check**: Re-read each note and ask "Does this add something the slide doesn't already say?" If not, rewrite or remove.

### 3. Note Format (Bilingual, Compact)

Rules:

- **Only show layers with content** — no empty layers, no "—" placeholders
- **Layer order is fixed** when shown: 📌 → 🎯 → 💡 → ⚙️ → ⚖️ → ⚠️ → 📝
- **Layer headers: English only** with icon (no Chinese in headers)
- **Content: English first** in `>`, then Chinese in `>>` nested blockquote
- **At least 3 layers** must have content per note block

```markdown
> **📝 Notes:**
>
> **🎯 Why:**
> English explanation with depth — answer WHY, not just WHAT.
>
> > 中文解释 — 回答"为什么"，而不是重复"是什么"。
>
> **💡 Intuition:**
> Think of it like [analogy]...
>
> > 类比：就像[类比]...
>
> **⚖️ Compare:**
> X vs Y: key difference is...
>
> > X vs Y：关键区别在于...
>
> **⚠️ Pitfall:**
> Don't confuse X with Y — they look similar but...
>
> > 不要混淆 X 和 Y — 它们看起来相似但...
>
> **📝 Exam:**
> Likely question: given [input], calculate [output].
>
> > 可能考法：给定[输入]，计算[输出]。
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
- [ ] Layer order is correct when shown: 📌 → 🎯 → 💡 → ⚙️ → ⚖️ → ⚠️ → 📝
- [ ] Why and Pitfall layers have real insight (not restating slides)
- [ ] English in `>`, Chinese in `>>`
- [ ] Both languages read naturally (not word-for-word translation)
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

## Examples

### Example 1: Math/Algorithm Concept (Eigenvalues)

```markdown
> **📝 Notes:**
>
> **🎯 Why:**
> Why find eigenvectors? They reveal the "natural axes" of a transformation.
> A complex matrix transformation, viewed along eigenvector directions, becomes simple scaling.
> This is why PCA uses eigenvectors for dimensionality reduction — finding directions of maximum variance.
>
> > 为什么要找特征向量？因为它揭示了变换的"本质方向"。
> > 复杂的矩阵变换，沿特征向量方向看就变成了简单的缩放。
> > 这就是 PCA 用特征向量降维的原因 — 找到数据方差最大的方向。
>
> **💡 Intuition:**
> Imagine pushing a revolving door. Most directions make it spin.
> But one direction only pushes it forward/backward without rotation —
> that direction is the "eigenvector", the displacement magnitude is the "eigenvalue".
>
> > 想象推旋转门。大部分方向推会让门转动。
> > 但有一个方向推只会让门前后移动不转 —
> > 那个方向就是"特征向量"，移动幅度就是"特征值"。
>
> **⚙️ How:**
> Why det(A-λI) = 0? Because Av = λv rearranges to (A-λI)v = 0.
> For non-zero v to exist, (A-λI) must be singular, meaning its determinant is 0.
>
> > 为什么 det(A-λI) = 0？因为 Av = λv 移项得 (A-λI)v = 0。
> > 要有非零解 v，(A-λI) 必须不可逆，即行列式为 0。
>
> **⚖️ Compare:**
> Eigendecomposition vs SVD: Eigen requires square matrices; SVD works for any matrix.
> SVD is essentially eigendecomposition applied to AᵀA.
>
> > 特征分解 vs SVD：特征分解要求方阵，SVD 对任意矩阵都有效。
> > SVD 本质是对 AᵀA 做特征分解。
>
> **⚠️ Pitfall:**
> Not all matrices have real eigenvalues. Rotation matrices have complex eigenvalues —
> because no direction stays unchanged after rotation.
>
> > 不是所有矩阵都有实数特征值。旋转矩阵的特征值是复数 —
> > 因为旋转后没有方向保持不变。
```

### Example 2: CV/ML Concept (Max Pooling)

```markdown
> **📝 Notes:**
>
> **🎯 Why:**
> After convolution, feature maps are too large — expensive to compute.
> More importantly, we care about WHETHER a feature exists, not its exact pixel location.
> Pooling achieves both: reduces size and adds positional tolerance.
>
> > 卷积后特征图太大，计算成本高。
> > 更重要的是，我们关心特征"有没有"，而不是"在哪个精确像素"。
> > 池化同时实现两个目标：减小尺寸 + 增加位置容忍度。
>
> **💡 Intuition:**
> Like zooming out on a map — you lose street-level detail but still see city shapes.
> Max pooling keeps the strongest signal in each region.
>
> > 像缩小地图 — 丢失街道细节但保留城市轮廓。
> > 最大池化保留每个区域中最强的信号。
>
> **⚠️ Pitfall:**
> Pooling has NO learnable parameters — don't confuse it with convolution.
> Convolution learns filters; pooling just applies a fixed rule (max or average).
>
> > 池化没有可学习参数 — 不要跟卷积层混淆。
> > 卷积学习滤波器；池化只是应用固定规则（取最大值或平均值）。
>
> **📝 Exam:**
> Given input size 4x4 with 2x2 pooling and stride 2, output is 2x2.
> Formula: output = (input - pool_size) / stride + 1.
>
> > 给定 4x4 输入，2x2 池化，stride=2，输出为 2x2。
> > 公式：output = (input - pool_size) / stride + 1。
```
