---
name: learning-math-foundations
description: Generate math foundation documents from textbooks. Use when (1) user asks to create math prerequisite materials, (2) mentions "数学基础" or "math foundations", (3) needs to understand the math behind ML/DL/NLP concepts. All content must have textbook source citations.
---

# Math Foundations Generator

## Objectives

Generate **math foundation documents** from textbooks in `courses/self-study/`. These are standalone reference files covering the mathematical prerequisites that ML/DL/NLP/RL courses assume you already know.

**Core Principle: Every claim has a source.**

Unlike course-specific `_math.md` files (which summarize slides formulas), these foundations are **extracted from textbooks** with precise citations.

## ⚠️ Absolute Rule: No Unsourced Content

Every formula, definition, theorem, and example in a math foundation file **MUST** cite its textbook source:

```markdown
> 📚 Source: MML §6.3, Eq. 6.20 — Deisenroth et al.
```

If you cannot find a source in the available textbooks, you **MUST**:

1. Mark it as `📐 补充推导 (Supplementary — not from textbook)`
2. Explain the derivation yourself step by step

**NO** bare formulas. **NO** "it is well known that..." without a citation.

> 📎 **Shared Rule:** This principle is part of the cross-cutting **Source Citation & Proof Rule** (`learning-source_citation` SKILL.md), which applies to all learning materials.
> 📎 **共享规则：** 此原则属于跨所有学习资料的通用**来源引证与证明规则**（`learning-source_citation` SKILL.md）。

---

## File Organization

### Directory

Each **math topic** gets its own file, organized under discipline subdirectories:

```
courses/math/
├── README.md                            ← Index + reading order + dependency map
│
├── linear-algebra/                      ← 线性代数
│   ├── vectors_matrices.md              ← 向量与矩阵运算
│   ├── inner_product.md                 ← 内积
│   ├── norms_distances.md               ← 范数与距离度量
│   └── eigenvalues_svd.md               ← 特征值与 SVD
│
├── calculus/                            ← 微积分
│   ├── derivatives.md                   ← 导数与偏导数
│   └── chain_rule_gradients.md          ← 链式法则与梯度
│
├── probability/                         ← 概率论
│   ├── conditional_probability.md       ← 条件概率与全概率公式
│   └── bayes_theorem.md                 ← 贝叶斯定理
│
├── statistics/                          ← 统计学
│   ├── mean_variance.md                 ← 均值、方差、标准差
│   ├── gaussian_distribution.md         ← 高斯分布 PDF
│   └── mle.md                           ← 最大似然估计
│
└── optimization/                        ← 最优化
    ├── gradient_descent.md              ← 梯度下降
    └── lagrange_multipliers.md          ← 拉格朗日乘子与 KKT
```

### File Count: ~13

Split by **math topic** (one concept per file), grouped by discipline subdirectory:

| #   | Subdirectory      | File                         | Topic (中文)       | Course Dependencies      |
| --- | ----------------- | ---------------------------- | ------------------ | ------------------------ |
| 1   | `linear-algebra/` | `vectors_matrices.md`        | 向量与矩阵运算     | CNN(W3), RNN(W4)         |
| 2   | `linear-algebra/` | `inner_product.md`           | 内积               | SVM hyperplane(W2)       |
| 3   | `linear-algebra/` | `norms_distances.md`         | 范数与距离度量     | K-Means(W6), KNN         |
| 4   | `linear-algebra/` | `eigenvalues_svd.md`         | 特征值与 SVD       | PCA                      |
| 5   | `calculus/`       | `derivatives.md`             | 导数与偏导数       | All training             |
| 6   | `calculus/`       | `chain_rule_gradients.md`    | 链式法则与梯度     | CNN-BP(W3), RNN-BPTT(W4) |
| 7   | `probability/`    | `conditional_probability.md` | 条件概率与全概率   | NB(W5)                   |
| 8   | `probability/`    | `bayes_theorem.md`           | 贝叶斯定理         | NB(W5), BBN(W5)          |
| 9   | `statistics/`     | `mean_variance.md`           | 均值/方差/标准差   | Preprocessing(W1), all   |
| 10  | `statistics/`     | `gaussian_distribution.md`   | 高斯分布 PDF       | NB-Gaussian(W5), EM(W6)  |
| 11  | `statistics/`     | `mle.md`                     | 最大似然估计       | NB(W5), EM(W6)           |
| 12  | `optimization/`   | `gradient_descent.md`        | 梯度下降           | CNN(W3), RNN(W4)         |
| 13  | `optimization/`   | `lagrange_multipliers.md`    | 拉格朗日乘子与 KKT | SVM(W2)                  |

> **Note:** This is the initial list. New files can be added when a course introduces a new math prerequisite (e.g., `information_theory.md` if entropy/KL-divergence is needed).

### Design Principles

- **One concept per file** — "inner_product.md" not "linear_algebra.md containing everything"
- **Subdirectories by discipline** — keeps related files together without a flat naming mess
- **~13 not 30** — don't over-split; closely coupled concepts stay together (e.g., chain rule + gradients)
- **ML concepts are excluded** — activation functions, loss functions, regularization belong in `week*_math.md`

### Length Target

Each file: **80–200 lines**. Short enough to read in one sitting, focused on one concept.

---

## Available Textbook Sources

### Priority 1: Dedicated Math Books (`courses/self-study/math/`)

| Key           | Book                                          | Best For                              | Sections Dir                        |
| ------------- | --------------------------------------------- | ------------------------------------- | ----------------------------------- |
| **MML**       | Mathematics for Machine Learning (Deisenroth) | ⭐ Primary — covers all 5 disciplines | `math/_sources/mml_sections/`       |
| **Grinstead** | Introduction to Probability                   | Deep probability foundations          | `math/_sources/grinstead_sections/` |
| **Boyd**      | Convex Optimization                           | Optimization theory, Lagrange, KKT    | `math/_sources/boyd_sections/`      |
| **Downey**    | Think Stats 2e                                | Statistics with Python                | `math/_sources/downey_sections/`    |
| **MacKay**    | Information Theory, Inference, and Learning   | Entropy, KL divergence                | `math/_sources/mackay_sections/`    |

### Priority 2: ML Books with Math Chapters (`courses/self-study/ml/`)

| Key            | Book                       | Math Chapters                                                                            |
| -------------- | -------------------------- | ---------------------------------------------------------------------------------------- |
| **Goodfellow** | Deep Learning              | Ch2 Linear Algebra, Ch3 Probability, Ch4 Numerical Computation                           |
| **Murphy**     | Probabilistic ML (PML1)    | Ch2-3 Probability, Ch4 Statistics, Ch6 Info Theory, Ch7 Linear Algebra, Ch8 Optimization |
| **Bishop**     | Pattern Recognition and ML | Ch1.2 Probability Theory, Ch2 Probability Distributions                                  |

### How to Find Source Sections

1. **Use `topic_index.json`** for keyword→section mapping:

```python
import json
with open('courses/self-study/topic_index.json') as f:
    idx = json.load(f)
refs = idx['topics']['probability']['references']
for r in refs:
    print(f"{r['book']}/{r['chapter']}: {r['title']}")
```

2. **Use `toc.json`** in each book's sections directory:

```bash
# Find Bayes theorem in MML
cat courses/self-study/math/_sources/mml_sections/toc.json | grep -i "bayes"
```

3. **Use `batch_pdf_to_md.py`** to convert relevant sections to markdown:

```bash
python .agent/skills/dev-pdf_processing/scripts/batch_pdf_to_md.py \
  --root courses/self-study --book mml_sections --chapter ch06
```

---

## Generation Workflow

### Step 1: Identify What to Cover

For each math discipline file:

1. Read ALL `week*_math.md` files to find which math concepts courses use
2. Read `week*_tutorial.md` files to find which derivations need prerequisites
3. List the required math topics

### Step 2: Find Textbook Sources

For each required topic:

1. Search `topic_index.json` for relevant book sections
2. Check `toc.json` of prioritized books (MML first, then Goodfellow/Murphy)
3. Note the exact chapter, section, equation numbers

### Step 3: Convert Source PDFs

```bash
# Convert relevant textbook sections to markdown
python .agent/skills/dev-pdf_processing/scripts/batch_pdf_to_md.py \
  --root courses/self-study --book mml_sections --chapter ch06
```

### Step 4: Write the Foundation Document

1. Follow the Document Template above
2. Extract definitions, theorems, and proofs from converted markdown
3. Add symbol legends for every formula
4. Write worked examples (adapt from textbook or create exam-style)
5. Add course connections for every topic
6. **Extract practice problems from textbook exercises** (see Rule 7)
   - Locate the Exercises section of the relevant chapter
   - Select 2–4 problems per topic, covering Easy/Medium/Hard tiers
   - Write hints and step-by-step solutions with source citations
7. Build the Quick Reference table at the end
8. Build the Source Index table at the end

### Step 5: Update Cross-References

1. Update `courses/math/README.md` with the new file
2. Add prerequisite links in `week*_math.md` headers:

```markdown
> **数学前置：** [概率论](../../math/probability/conditional_probability.md) | [统计学](../../math/statistics/mean_variance.md)
```

---

## Quality Checklist

Before completing a foundation file, verify:

- [ ] **Every formula has a `📚 Source:` citation** with book, section, and equation number
- [ ] **Every formula has a symbol legend table** on first appearance
- [ ] **Every section has a Course Connection** listing which weeks use it
- [ ] **No unsourced claims** — supplementary derivations are marked as such
- [ ] **Length is 80–250 lines** — focused on one concept (practice problems may add ~50 lines)
- [ ] **Only course-relevant content** — no textbook topics unused by courses
- [ ] **Bilingual** — headings, explanations, and symbol legends in both EN and CN
- [ ] **Practice problems included** — at least 1 per section, immediately after section content (NOT at end of file)
- [ ] **Practice placement** — "learn → practice" flow: every §N ends with §N.X Practice Problems
- [ ] **All problems have source citations** — textbook exercise number or `📐 Original` tag
- [ ] **Direct display** — NO `<details>` collapsible blocks; hints and solutions directly visible
- [ ] **Each problem has Hint and Solution** — shown inline, not hidden
- [ ] **Quick Reference table** at the end summarizes all formulas
- [ ] **Source Index table** at the end lists all textbook references
- [ ] **README.md** is updated with the new file and dependency arrows

---

<!-- Detailed content moved to references/math_templates.md -->

> 📖 See [references/math_templates.md](references/math_templates.md) for detailed content on the following topics:
> - ## Document Template
> - ## §1 Topic Title
> - ## §2 Next Topic
> - ## Quick Reference
> - ## Source Index
> - ## Section Structure Rules
> - ## §3 Chain Rule
> - ## §1 Topic A
> - ## ...
> - ## §2 Topic B
> - ## README.md Template
> - ## 📚 Files
> - ## 📐 Dependency Map
> - ## 🔗 Course Reading
> - ## 📖 Primary Sources
> - ## Relationship to
