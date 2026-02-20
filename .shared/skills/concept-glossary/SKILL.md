---
name: concept-glossary
description: Reusable glossary of concepts, terminology, and historical development. Use when (1) explaining a concept/term in notes, (2) user says "这个是什么" or "不理解概念", (3) need standard definition for any course material. Grows automatically with each note-taking session.
---

# Concept Glossary (概念术语库)

## Purpose

A **living, growing glossary** of concepts, terminology, and historical context across all courses. Every time you write notes and encounter a concept, check here first — don't reinvent definitions from scratch. After writing notes, add any new concepts back to the library.

**Core philosophy: 滚雪球 (Snowball Effect)** — each note-taking session makes the library richer, which makes the next session faster and more consistent.

## When to Use

- Writing notes that introduce a concept or term → look it up here first
- User asks "what is X?" → pull the entry and adapt it
- Encountering a new term in course material → add it after writing notes
- Need to compare related concepts → check cross-references here
- Need historical context for a technique → check the `📜 History` field

## Library Structure

Concepts are stored in `resources/` as markdown files, organized by domain:

```
resources/
├── ml_fundamentals.md       — Core ML concepts (overfitting, bias-variance, etc.)
├── deep_learning.md         — Neural networks, architectures, training techniques
├── computer_vision.md       — Vision-specific concepts (edge detection, segmentation, etc.)
├── nlp.md                   — NLP-specific concepts (tokenization, attention, etc.)
├── optimization.md          — Optimization methods (SGD, Adam, learning rate, etc.)
├── data_processing.md       — Data handling (normalization, augmentation, etc.)
└── historical_milestones.md — Key papers, breakthroughs, and evolution timelines
```

## Concept Entry Format

Every concept entry follows this fixed structure:

```markdown
---

### Concept Name (中文名)

**Tags:** `#domain` `#subdomain` `#course-week`

**📌 Definition (定义):**
> One-line English definition — precise and self-contained.
>> 中文一句话定义 — 精确且自包含。

**📜 History (历史背景):**
> Who introduced it, when, and why it mattered.
> Key paper or milestone (if applicable).
>> 谁提出的，什么时候，为什么重要。

**💡 Analogy (类比):**
> Real-world analogy — make it concrete and memorable.
>> 现实世界类比 — 具体且易记。

**🔗 Related Concepts (关联概念):**
> → see: [Related Concept 1] — how they relate
> → see: [Related Concept 2] — how they differ
> → formula: [Math Concept] in math-concept-library — if there's a formula counterpart

**⚖️ Contrast (易混淆对比):**
> | Feature     | This Concept | Easily Confused With |
> |-------------|--------------|----------------------|
> | Key diff 1  | ...          | ...                  |
> | Key diff 2  | ...          | ...                  |

**📚 Appears In (出现课程):**
> - [Course] Week N: context of use
> - [Course] Week M: another context
```

## Rules

### Content Rules

1. **One concept = one entry.** Don't merge related but distinct concepts (e.g., "Precision" and "Recall" are separate entries).
2. **Always bilingual.** English first, Chinese second.
3. **Analogy is mandatory.** Every concept MUST have a real-world analogy that a beginner can understand.
4. **History when available.** Not every concept needs deep history, but key breakthroughs (AlexNet, Transformer, etc.) MUST have it.
5. **Cross-reference aggressively.** Use `→ see:` links to connect related concepts. If a concept has a math formula, link to the corresponding entry in `math-concept-library`.

### Auto-Organization Rules (自动组织规则)

These rules ensure the library stays organized as it grows:

6. **Category placement:** When adding a new concept, choose the most specific category file. If unsure, prefer the domain where the concept is MOST frequently used.
7. **Alphabetical within category:** Entries within each file should be in alphabetical order by English concept name.
8. **Merge check:** Before adding a new entry, scan the category file for existing entries that cover the same concept (possibly under a different name or alias). If found, update the existing entry instead of creating a duplicate.
9. **Tag evolution:** When a concept appears in a new course/week, update its `Appears In` section and add the new course tag.
10. **Cross-reference backlinks:** When adding `→ see: X` to concept A, also add `→ see: A` to concept X (bidirectional linking).
11. **Analogy consistency:** If two related concepts use analogies from the same domain (e.g., both use "kitchen" analogies), note this connection — it helps students see the relationship.

### Growth Workflow (持续完善流程)

Every time notes are written:

```
┌─────────────────────────────────┐
│ 1. BEFORE writing notes:       │
│    Check glossary for existing  │
│    definitions → reuse & adapt  │
├─────────────────────────────────┤
│ 2. WHILE writing notes:        │
│    Flag new terms encountered   │
│    (mental list or comments)    │
├─────────────────────────────────┤
│ 3. AFTER writing notes:        │
│    Add new concepts to glossary │
│    Update cross-references      │
│    Update "Appears In" for      │
│    existing concepts reused     │
└─────────────────────────────────┘
```

## How to Add a New Concept

1. Identify which category file it belongs to (or create a new one if none fits)
2. Check for existing entries — update if found, create if not
3. Follow the entry format exactly
4. Add cross-references to related existing concepts (bidirectional)
5. If the concept has a math formula, add `→ formula:` link to `math-concept-library`
6. Add `Appears In` to link back to course materials

## How to Use in Notes

When writing course notes and encountering a concept:

1. **Check this glossary** for the concept
2. **Copy the relevant parts** (definition, analogy, history) into the notes
3. **Adapt** the explanation to the specific lecture context
4. If the concept is **not in the glossary**, add it after writing the notes

## Example Entry

```markdown
---

### Convolutional Neural Network (卷积神经网络)

**Tags:** `#deep_learning` `#architecture` `#mv-week4` `#ml-week8`

**📌 Definition (定义):**
> A neural network that uses learnable convolutional filters to automatically extract spatial features from input data (typically images), using weight sharing and local connectivity to reduce parameters.
>> 一种使用可学习卷积滤波器从输入数据（通常是图像）中自动提取空间特征的神经网络，通过权重共享和局部连接来减少参数量。

**📜 History (历史背景):**
> Inspired by Hubel & Wiesel's 1962 discovery of simple/complex cells in cat visual cortex.
> LeCun et al. (1998) created LeNet-5 for handwritten digit recognition — first practical CNN.
> Krizhevsky et al. (2012) AlexNet won ImageNet by a large margin → triggered the deep learning revolution.
>> 灵感来自 Hubel & Wiesel 1962年发现的猫视觉皮层简单/复杂细胞。
>> LeCun 等 (1998) 创建 LeNet-5 用于手写数字识别 — 第一个实用 CNN。
>> Krizhevsky 等 (2012) AlexNet 大幅赢得 ImageNet → 引发深度学习革命。

**💡 Analogy (类比):**
> Like a security guard scanning a room with a flashlight (the filter): they check each small area one at a time, looking for specific patterns (edges, textures). They don't need to see the whole room at once — they slide the flashlight across and note where they find something interesting.
>> 像保安用手电筒扫描房间（滤波器）：逐个小区域检查，寻找特定模式（边缘、纹理）。不需要一次看整个房间 — 滑动手电筒并记录发现有趣东西的位置。

**🔗 Related Concepts (关联概念):**
> → see: Pooling (池化) — downsampling after convolution
> → see: ReLU (激活函数) — non-linearity between conv layers
> → see: Backpropagation (反向传播) — how CNNs learn
> → formula: Convolution Operation in math-concept-library/signal_processing.md

**⚖️ Contrast (易混淆对比):**
> | Feature        | CNN                    | Fully Connected NN     |
> |----------------|------------------------|------------------------|
> | Connectivity   | Local (kernel size)    | Every neuron to every  |
> | Weight sharing | Yes (same filter)      | No                     |
> | Parameters     | Few (kernel weights)   | Many (all connections) |
> | Spatial aware  | Yes                    | No                     |

**📚 Appears In (出现课程):**
> - MV Week 4: Introduction to CNNs
> - ML Week 8: Deep Learning overview
```
