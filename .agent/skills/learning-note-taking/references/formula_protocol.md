# Formula Explanation Protocol — Detailed Templates

> Extracted from learning-note-taking SKILL.md §7

## Check `math-concept-library` first (先查公式库)

Before writing any formula explanation, look up the concept in `.shared/skills/math-concept-library/resources/`:

- `signal_processing.md` — Filters, convolution, frequency domain
- `calculus.md` — Derivatives, gradients, optimization
- `linear_algebra.md` — Matrices, transformations, eigenvalues
- `statistics.md` — Distributions, probability, estimation
- `evaluation_metrics.md` — Precision, recall, F1, IoU, etc.
- `image_processing.md` — Image-specific formulas

If the concept **exists**: reuse its definition, intuition, and formula breakdown — adapt to the lecture context.
If the concept **does not exist**: write the explanation from scratch, then **add it to the library** after completing the notes.

## A) Main text (BEFORE the notes block)

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

## B) Inside the notes block — formula layers

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

**Layer order:** 📌 → 🎯 → 💡 → ⚙️ → **📐** → **🔢** → ⚖️ → ⚠️ → 📝

**Rules:**

- **Symbol legend goes in main text** — not inside the notes block.
- **📐 Formula reads the formula piece by piece** — "Σᵢ iterates over all K clusters. For each cluster Cᵢ, Σₓ∈Cᵢ iterates over every data point in that cluster. ‖x - mᵢ‖² computes the squared distance from that point to the centroid."
- **🔢 Example MUST start with a clear problem setup** — describe the scenario BEFORE any computation.
- **📝 Exam stays for exam predictions only** — "What question type might test this?" Not a worked example.

## C) After writing — add new concepts to the library (新概念入库)

If you explained a formula that is **not yet in** `math-concept-library/resources/`, add it using the standard entry format.

**Complete Template:**

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
> **Problem:** We have 4 data points in 1D: {1, 3, 7, 9}. Assigned to 2 clusters: C₁={1,3}, C₂={7,9}.
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
