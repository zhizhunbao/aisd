---
name: math-concept-library
description: Reusable math/formula reference library. Use when (1) explaining a math concept in notes, (2) user says "没概念" or "不理解公式", (3) need formula breakdown for any course material.
---

# Math Concept Library (数学概念库)

## Purpose

A **reusable reference library** of mathematical concepts, formulas, and intuitive explanations. When writing course notes or explaining a concept, look up the relevant entry here first — don't reinvent explanations from scratch.

## When to Use

- Writing notes that involve a math formula → look up the concept here for standard explanation
- User says they don't understand a concept → pull the entry and adapt it
- Adding a new math concept encountered in course material → add it to the library

## Library Structure

Concepts are stored in `resources/` as markdown files, organized by category:

```
resources/
├── signal_processing.md    — Filters, convolution, frequency domain
├── calculus.md              — Derivatives, gradients, optimization
├── linear_algebra.md        — Matrices, transformations, eigenvalues
├── statistics.md            — Distributions, probability, estimation
└── evaluation_metrics.md    — Precision, recall, F1, IoU, etc.
```

## Concept Entry Format

Every concept entry follows this fixed structure:

```markdown
---

### Concept Name (中文名)

**Tags:** `#category` `#subcategory` `#course-week`

**📌 One-line Definition:**
> English definition in one sentence.
>> 中文一句话定义。

**📐 Formula:**
```
formula here
```
- symbol₁ = meaning (type, range)
- symbol₂ = meaning (type, range)

**💡 Intuition (直觉理解):**
> Analogy or mental model — make it concrete.
>> 类比或心理模型 — 要具体。

**🔢 Worked Example:**
> Step-by-step with real numbers.
>> 用真实数字逐步演示。

**⚙️ In Practice (实际使用):**
> How it's used in code (OpenCV, NumPy, etc.)
>> 在代码中如何使用。

**🔗 Related Concepts:**
> Links to other entries in this library.

**📚 Appears In:**
> Which course weeks/sections use this concept.
```

## Rules

### Content Rules

1. **One concept = one entry.** Don't merge related but distinct concepts.
2. **Always bilingual.** English first, Chinese second.
3. **Intuition is mandatory.** Every concept MUST have a real-world analogy.
4. **Keep formulas simple.** Use ASCII math notation. Only use LaTeX if absolutely necessary.
5. **Add `Appears In`** to track which course materials reference this concept.
6. **Cross-reference** related concepts using `→ see: Concept Name` links.
7. **When adding new concepts,** check if related concepts already exist and add cross-references.
8. **Link to `concept-glossary`** when a formula's parent concept has an entry there (e.g., formula "Convolution" → concept "CNN" in `concept-glossary`).

### Auto-Organization Rules (自动组织规则)

9. **Alphabetical within category:** Entries within each file should be in alphabetical order.
10. **Merge check:** Before adding, scan for existing entries covering the same formula (possibly under a different name). Update instead of duplicating.
11. **Tag evolution:** When a formula appears in a new course, update `Appears In` and tags.
12. **Bidirectional cross-references:** When adding `→ see: X`, also add `→ see: [this]` to X.

### Growth Workflow (滚雪球式积累)

Every time notes are written:

```
┌─────────────────────────────────┐
│ 1. BEFORE writing notes:       │
│    Check library for existing   │
│    formula entries → reuse      │
├─────────────────────────────────┤
│ 2. WHILE writing notes:        │
│    Flag new formulas            │
├─────────────────────────────────┤
│ 3. AFTER writing notes:        │
│    Add new formulas to library  │
│    Update cross-references      │
│    Update "Appears In" for      │
│    existing formulas reused     │
└─────────────────────────────────┘
```

## How to Add a New Concept

1. Identify which category file it belongs to (or create a new one)
2. Check for existing entries — update if found, create if not
3. Follow the entry format exactly
4. Add cross-references to related existing concepts (bidirectional)
5. If the concept has a non-formula counterpart, add `→ concept:` link to `concept-glossary`
6. Add `Appears In` to link back to course materials

## How to Use in Notes

When writing course notes and encountering a formula:

1. **Check this library** for the concept
2. **Copy the relevant parts** (definition, intuition, formula breakdown) into the notes
3. **Adapt** the explanation to the specific context of the lecture
4. If the concept is **not in the library**, add it after writing the notes

## Related Skill

- **`concept-glossary`** (`.shared/skills/concept-glossary/SKILL.md`): For non-formula concepts, terminology, and historical context. Both skills follow the same snowball growth pattern and should cross-reference each other.
