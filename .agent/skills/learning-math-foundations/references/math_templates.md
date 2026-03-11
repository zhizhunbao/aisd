# Math Foundations — Templates & Examples

## Document Template

Each file follows this structure:

```markdown
# [Discipline Name] | [中文名]

> **Purpose:** [What this file covers and why ML students need it]
> **Primary Source:** [Main textbook used]
> **See also:** [Links to other foundation files + relevant week*_math.md files]
> **Prerequisites:** [Which other foundation files to read first, if any]

---


## §1 Topic Title (中文标题)

> 📚 Source: MML §X.Y, pp. XX–XX — Deisenroth et al.

### 1.1 Definition / Theorem

> 📚 MML Def. X.Y

$$\text{formula in LaTeX}$$

| Symbol | Meaning (EN) | 含义 (中文) | Example   |
| ------ | ------------ | ----------- | --------- |
| $x$    | data point   | 数据点      | [1, 2, 3] |

### 1.2 Intuition (直觉理解)

> Why does this matter for ML? Connect to course concepts.

### 1.3 Worked Example (手算例题)

> 📚 Adapted from MML Example X.Y

**Problem:** [concrete numbers]
**Solution:**
$$\text{step-by-step}$$

### 1.4 Connection to Course (课程关联)

> This concept appears in:
>
> - **W2 SVM:** [how it's used]
> - **W3 CNN:** [how it's used]

### 1.5 Practice Problems (练习题)

> 📚 Problems from MML §X.Y Exercises X.1–X.3

#### 🟢 Easy | 基础题

**P1.** [problem statement in EN]
[题目中文描述]

<details><summary>💡 Hint / 提示</summary>

[hint without giving away the answer]

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Solution adapted from MML §X.Y

$$\text{step-by-step solution}$$

</details>

#### 🟡 Medium | 中等题

**P2.** [problem requiring multi-step reasoning]

<details><summary>💡 Hint / 提示</summary>

[partial approach hint]

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Source: ...

$$\text{detailed solution}$$

</details>

#### 🔴 Hard | 挑战题

**P3.** [problem connecting to ML application or requiring proof]

<details><summary>💡 Hint / 提示</summary>

[strategy hint]

</details>

<details><summary>✅ Solution / 解答</summary>

> 📚 Source: ...

$$\text{complete derivation}$$

</details>

---


## §2 Next Topic...

---


## Quick Reference (速查表)

| Concept | Formula | Source   | Used In |
| ------- | ------- | -------- | ------- |
| ...     | $...$   | MML §X.Y | W2 SVM  |

---


## Source Index (来源索引)

| Section | Textbook   | Chapter/Equation | Pages       |
| ------- | ---------- | ---------------- | ----------- |
| §1      | MML        | §6.3, Eq. 6.20   | pp. 189–191 |
| §2      | Goodfellow | §3.11            | p. 85       |
```

---


## Section Structure Rules

### Rule 1: Source First (来源优先)

Every section starts with a `> 📚 Source:` blockquote identifying the textbook reference.

```markdown

## §3 Chain Rule (链式法则)

> 📚 Source: MML §5.2–5.3, pp. 152–160 — Deisenroth et al.
> 📚 Also: Goodfellow §6.5, pp. 219–238 — Backpropagation derivation
```

### Rule 2: Symbol Legend BEFORE Formula (符号必须先解释再使用)

Every symbol **MUST** be explained in a legend table **BEFORE** it appears in any formula. Never write a formula first and explain symbols after — the reader will not understand.

每个符号**必须**在公式中使用**之前**用对照表解释。绝不能先写公式再解释符号 —— 读者看不懂。

**Ordering rule (顺序规则):**

1. **Plain-language explanation** of what the formula does (一两句人话说这个公式干嘛的)
2. **Symbol legend table** defining every symbol (符号对照表)
3. **Formula** using those symbols (公式)

**Sub-rule 2a: Notation Explainer (符号读法解释)**

When using unfamiliar math notation, add a `📖 Reading the notation` blockquote explaining how to read it in plain language. **Common symbols that MUST be explained on first use:**

| Symbol                     | Meaning                                                      | 中文                                     |
| -------------------------- | ------------------------------------------------------------ | ---------------------------------------- |
| $:=$                       | "is defined as" (left side is a NEW name for the right side) | "定义为"（左边是新符号，右边是它的定义） |
| $\|\cdot\|$                | "norm of whatever is inside" (double bars = length)          | "里面那个东西的范数"（双竖线 = 长度）    |
| $\in$                      | "belongs to" / "is a member of"                              | "属于"                                   |
| $\mathbb{R}^n$             | "the set of all n-dimensional real vectors"                  | "n 维实数向量的集合"                     |
| $V \to \mathbb{R}$         | "a function from space V to a real number"                   | "从空间 V 到实数的函数"                  |
| $\forall$                  | "for all"                                                    | "对所有"                                 |
| $\iff$                     | "if and only if" (both directions)                           | "当且仅当"（双向成立）                   |
| $\implies$ / $\Rightarrow$ | "implies" (one direction)                                    | "推出"（单向）                           |
| $\sum_{i=1}^{n}$           | "add up from i=1 to i=n"                                     | "从 i=1 加到 i=n"                        |
| $\arg\min_x$               | "the value of x that makes this smallest"                    | "让这个值最小的那个 x"                   |

```markdown
> 📖 **Reading the notation:** "$\|\cdot\|: V \to \mathbb{R}$" means "a function
> that takes a vector and returns a number (the length)."
```

**Example of correct order (正确顺序示例):**

```markdown
The Euclidean norm measures the straight-line length of a vector (勾股定理算直线长度):

| Symbol             | Meaning        | 含义         | Type           |
| ------------------ | -------------- | ------------ | -------------- |
| $\mathbf{x}$       | input vector   | 输入向量     | $\mathbb{R}^n$ |
| $x_i$              | i-th element   | 第 i 个分量  | $\mathbb{R}$   |
| $\|\mathbf{x}\|_2$ | Euclidean norm | 欧几里得范数 | $\geq 0$       |

$$\|\mathbf{x}\|_2 = \sqrt{\sum_{i=1}^{n} x_i^2}$$
```

### Rule 3: Course Connection (课程关联)

Each topic must explicitly state which course weeks use it:

```markdown
> 🔗 **Course Connection:**
>
> - **ML W2 SVM:** Inner product defines the hyperplane $\mathbf{w}^T\mathbf{x} + b = 0$
> - **ML W6 Clustering:** Euclidean distance $\|\mathbf{x} - \mathbf{m}\|^2$ is the K-Means objective
```

### Rule 4: Bilingual (双语)

- Section headings: `## §N English Title (中文标题)`
- Formula explanations: English first, then Chinese
- Symbol legends: both `Meaning` and `含义` columns
- Worked examples: bilingual step labels

### Rule 5: Only What Courses Need (只写课程用到的)

Do NOT comprehensively cover the entire textbook chapter. Only extract math that appears in your courses:

- ✅ Inner product → used in SVM hyperplane
- ✅ Eigenvalues → used in PCA
- ❌ Jordan normal form → not used in any course
- ❌ Abstract vector spaces → not needed

### Rule 6: Cross-Reference Between Files (文件间交叉引用)

When one foundation file depends on another:

```markdown
> 📎 **Prerequisite:** See [calculus.md §2 Chain Rule](calculus.md#§2) before reading this section.
```

### Rule 7: Practice Problems from Textbooks (教科书练习题)

Each topic section **MUST** include practice problems extracted or adapted from textbook exercises.

#### 7a. Placement Rule: Practice Immediately After Each Section (练习紧跟小节)

Practice problems **MUST** appear **immediately after** the section they test — NOT consolidated at the end of the file. This ensures "learn → practice → learn → practice" flow.

练习题**必须**紧跟在对应小节后面 —— **不能**堆在文件末尾。确保"学一节→练一节"的节奏。

```markdown

## §1 Topic A

### 1.1 Definition ...

### 1.2 Intuition ...

### 1.3 Practice Problems (练习题) ← immediately after §1 content

#### 🟢 Easy | 基础题


## ...


## §2 Topic B

### 2.1 Definition ...

### 2.2 Practice Problems (练习题) ← immediately after §2 content

...
```

**Minimum per section:** 1 Easy + 1 Medium (or 1 conceptual). Overall file should have at least 1 Hard problem.

#### 7b. Source Requirement (来源要求)

- **Priority 1:** Directly use textbook exercises (cite exercise number)
- **Priority 2:** Adapt textbook examples by changing numbers/context
- **Priority 3:** Create original problems in textbook style — mark as `📐 Original Problem`
- **NO** problems without a source or `📐 Original` tag

#### 7c. Difficulty Tiers (难度分级)

| Tier | Label           | Target                          | Problem Type                    |
| ---- | --------------- | ------------------------------- | ------------------------------- |
| 🟢   | Easy / 基础题   | Direct formula application      | "Compute X given Y"             |
| 🟡   | Medium / 中等题 | Multi-step reasoning or proof   | "Show that... / Derive..."      |
| 🔴   | Hard / 挑战题   | ML application or cross-concept | "Why does this matter for SVM?" |

#### 7d. Problem Format (题目格式)

Practice problems are displayed **directly** — NO collapsible `<details>` blocks. Hint and Solution are shown inline for immediate readability.

练习题**直接显示** —— 不用折叠块。提示和解答直接可见。

```markdown
#### 🟢 Easy | 基础题

**P1.** [Problem in English]
[题目中文描述]

> 📚 From: MML Exercise 6.3

> 💡 **Hint:** [Hint without giving away the answer]

**Solution:**

> 📚 Method: MML §6.3, adapted from Example 6.5

**Step 1:** ...
**Step 2:** ...
$$\text{final answer}$$
```

#### 7e. Display Rules (显示规则)

- **NO** `<details>` collapsible blocks — everything is directly visible
- Each problem has: problem statement → source tag → hint → solution
- Solutions include **step-by-step** work with source citation

#### 7f. How to Find Textbook Exercises (如何找教科书习题)

1. **Check the Exercises section** at the end of each textbook chapter
2. Use `toc.json` to locate exercise pages:
   ```bash
   cat courses/self-study/math/_sources/mml_sections/toc.json | grep -i "exercise"
   ```
3. Convert exercise pages to markdown:
   ```bash
   python .agent/skills/dev-pdf_processing/scripts/batch_pdf_to_md.py \
     --root courses/self-study --book mml_sections --chapter ch06 --pages 195-200
   ```
4. Select problems that match the topic and cover different difficulty levels

---


## README.md Template

```markdown
# Math Foundations | 数学基础

> 跨课程共享的数学前置知识，从教科书提取，每个公式都有出处。
> Shared math prerequisites across all courses. Every formula has a textbook citation.


## 📚 Files

### Linear Algebra (线性代数)

| File                                                      | Topic          | Lines | Course Dependencies |
| --------------------------------------------------------- | -------------- | ----- | ------------------- |
| [vectors_matrices.md](linear-algebra/vectors_matrices.md) | 向量与矩阵运算 | ~120  | CNN(W3), RNN(W4)    |
| [inner_product.md](linear-algebra/inner_product.md)       | 内积           | ~100  | SVM(W2)             |
| [norms_distances.md](linear-algebra/norms_distances.md)   | 范数与距离度量 | ~120  | K-Means(W6)         |
| [eigenvalues_svd.md](linear-algebra/eigenvalues_svd.md)   | 特征值与 SVD   | ~150  | PCA                 |

### Calculus (微积分)

| File                                                        | Topic          | Lines | Course Dependencies  |
| ----------------------------------------------------------- | -------------- | ----- | -------------------- |
| [derivatives.md](calculus/derivatives.md)                   | 导数与偏导数   | ~120  | All training         |
| [chain_rule_gradients.md](calculus/chain_rule_gradients.md) | 链式法则与梯度 | ~150  | CNN-BP(W3), BPTT(W4) |

### Probability (概率论)

| File                                                                 | Topic      | Lines | Course Dependencies |
| -------------------------------------------------------------------- | ---------- | ----- | ------------------- |
| [conditional_probability.md](probability/conditional_probability.md) | 条件概率   | ~100  | NB(W5)              |
| [bayes_theorem.md](probability/bayes_theorem.md)                     | 贝叶斯定理 | ~120  | NB(W5), BBN(W5)     |

### Statistics (统计学)

| File                                                            | Topic            | Lines | Course Dependencies     |
| --------------------------------------------------------------- | ---------------- | ----- | ----------------------- |
| [mean_variance.md](statistics/mean_variance.md)                 | 均值/方差/标准差 | ~100  | Preprocessing(W1)       |
| [gaussian_distribution.md](statistics/gaussian_distribution.md) | 高斯分布 PDF     | ~120  | NB-Gaussian(W5), EM(W6) |
| [mle.md](statistics/mle.md)                                     | 最大似然估计     | ~120  | NB(W5), EM(W6)          |

### Optimization (最优化)

| File                                                            | Topic        | Lines | Course Dependencies |
| --------------------------------------------------------------- | ------------ | ----- | ------------------- |
| [gradient_descent.md](optimization/gradient_descent.md)         | 梯度下降     | ~120  | CNN(W3), RNN(W4)    |
| [lagrange_multipliers.md](optimization/lagrange_multipliers.md) | 拉格朗日乘子 | ~150  | SVM(W2)             |


## 📐 Dependency Map (依赖关系)

`` `
vectors_matrices ──→ inner_product ──→ norms_distances
│
eigenvalues_svd ◀────┘

derivatives ──→ chain_rule_gradients ──→ gradient_descent
│
lagrange_multipliers ◀┘

conditional_probability ──→ bayes_theorem
│
mean_variance ──→ gaussian_distribution ──→ mle
`` `


## 🔗 Course Reading Lists (课程阅读清单)

| Course Week         | Read These First                                                              |
| ------------------- | ----------------------------------------------------------------------------- |
| ML W1 Preprocessing | `mean_variance`                                                               |
| ML W2 SVM           | `inner_product` → `lagrange_multipliers`                                      |
| ML W3 CNN           | `vectors_matrices` → `derivatives` → `chain_rule_gradients`                   |
| ML W4 RNN           | `chain_rule_gradients` → `gradient_descent`                                   |
| ML W5 Naive Bayes   | `conditional_probability` → `bayes_theorem` → `gaussian_distribution` → `mle` |
| ML W6 Clustering    | `norms_distances` → `gaussian_distribution` → `mle` → `gradient_descent`      |


## 📖 Primary Sources

| Book                             | Key        | Chapters Used |
| -------------------------------- | ---------- | ------------- |
| Mathematics for Machine Learning | MML        | Ch2–7         |
| Deep Learning                    | Goodfellow | Ch2–4         |
| Probabilistic ML                 | Murphy     | Ch2–8         |
| Introduction to Probability      | Grinstead  | Ch1, 4, 6     |
| Convex Optimization              | Boyd       | Ch5, 9        |
```

---


## Relationship to Other Files

### Math Foundations vs `week*_math.md`

|              | Math Foundations                   | `week*_math.md`                            |
| ------------ | ---------------------------------- | ------------------------------------------ |
| **Location** | `courses/math/{discipline}/`       | `courses/{course}/notes/`                  |
| **Scope**    | One math concept                   | One course week's formulas                 |
| **Content**  | Textbook definitions + proofs      | Slide formulas + hand calc                 |
| **Source**   | Textbooks (with citations)         | Course slides                              |
| **Audience** | "I don't understand the math"      | "I need the exam formula"                  |
| **Example**  | "What IS conditional probability?" | "How to compute P(A\|B) for this dataset?" |
| **Length**   | 80–200 lines                       | 150–400 lines                              |

### Math Foundations vs `week*_tutorial.md`

|                  | Math Foundations        | `week*_tutorial.md`              |
| ---------------- | ----------------------- | -------------------------------- |
| **Level**        | Pure math prerequisites | ML-specific derivations          |
| **Content**      | "What is chain rule?"   | "How chain rule applies to BPTT" |
| **Dependencies** | None (self-contained)   | Depends on math foundations      |

**Flow:** Math Foundations → Tutorial → Math (exam formulas)

