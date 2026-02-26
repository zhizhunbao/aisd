---
name: learning-cheat_sheet
description: Generate exam cheat sheets from slides, quizzes, and labs. Use when (1) user asks to create/update a cheat sheet, (2) mentions "cheat sheet" or "小抄", (3) needs to compile exam review material into printable format.
---

# Cheat Sheet Generator

## Objectives

- Extract ALL testable content from slides, quizzes, and labs
- **Split into 3 focused files** per topic — cheatsheet, math, code
- Zero information loss — every concept, formula, trap, and example must be captured

## 3-File Split Architecture (三文件拆分)

Each topic produces **3 companion files**, each with a single focus:

| File           | Suffix           | Contains                                           | Does NOT contain                      |
| -------------- | ---------------- | -------------------------------------------------- | ------------------------------------- |
| **Cheatsheet** | `_cheatsheet.md` | Definitions, Key Points, Traps, Tables             | No formulas, no hand calc, no code    |
| **Math**       | `_math.md`       | Formulas, Hand Calculations                        | No definitions, no code               |
| **Code**       | `_code.md`       | Code patterns, imports, API usage                   | No definitions, no formulas           |

### Why Split?

- **Cheatsheet** = quick lookup during conceptual review → "what is X? what to watch out for?"
- **Math** = formula reference + exam hand-calc practice → "how to compute X step by step?"
- **Code** = lab/assignment reference → "how to implement X in Python?"
- Each file stays focused and small → AI can process one file at a time without context overflow
- Print-ready: bring only the files you need to the exam

### Cross-References

Each file's header links to the other two companion files:

```markdown
> **See also:** [\_cheatsheet.md](...) | [\_math.md](...) | [\_code.md](...)
```

## File Naming Convention

All files live in `courses/{course}/notes/` and use the topic prefix:

```
courses/{course}/notes/
├── {topic}_cheatsheet.md     # Definitions + Key Points + Traps + Tables
├── {topic}_math.md           # Formulas + Hand Calculations
├── {topic}_code.md           # Code patterns
├── {exam}_cheat_sheet.json   # (Optional) Structured data for HTML build
└── {exam}_cheat_sheet_final.html  # (Optional) Print-ready HTML
```

Where `{topic}` = `week{N}_{topicname}`, e.g.:

- `week5_naivebayes_cheatsheet.md` + `week5_naivebayes_math.md` + `week5_naivebayes_code.md`
- `week2_svm_cheatsheet.md` + `week2_svm_math.md` + `week2_svm_code.md`

## Design Principles

### Simplicity First

Each section contains **only two types of content**:

1. **Bullets** (`content[]`) — for concepts, formulas, warnings, examples, key points
2. **Tables** (`table{}`) — for comparisons, structured data

There are NO colored boxes, NO special formatting classes. Everything is a bullet or a table row.

### ⚠️⚠️⚠️ CRITICAL — Bullet Categories Per File (每个文件的 Bullet 分类)

**Each of the 3 files uses ONLY its designated categories:**

#### File 1: `_cheatsheet.md` — Concepts & Warnings

| Category                         | What goes here                         |
| -------------------------------- | -------------------------------------- |
| **Definitions (名词定义)**       | Term definitions with full name + 中文 |
| **Key Points (要点/记忆)**       | Core insights, memory aids, summaries  |
| **Traps & Warnings (陷阱/注意)** | Quiz traps, common mistakes, warnings  |

Plus: **Comparison tables** at section end.

#### File 2: `_math.md` — Formulas & Calculations (Bilingual 双语)

| Category                      | What goes here                                                  |
| ----------------------------- | --------------------------------------------------------------- |
| **Formulas (公式)**           | Formulas with parameter explanation                             |
| **Hand Calc (手写计算/例题)** | Step-by-step worked examples with concrete numbers (exam-style) |

**⚠️⚠️⚠️ CRITICAL — `_math.md` MUST be Bilingual (中文在上, English below):**

- ALL formula names, section headings, and explanations must be bilingual: **Chinese first, English second**
- Formula parameter tables should have both `含义（中文）` and `Meaning (English)` columns
- Hand calculation steps should have Chinese explanation first, then English
- LaTeX formulas themselves stay in standard math notation (no translation needed)
- Quick Reference Table at the end should have bilingual column headers

Example format:

```markdown
- **均方误差 (Mean Squared Error / MSE):**
  $$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$
  $y_i$ = 实际值 (actual value), $\hat{y}_i$ = 预测值 (predicted value)
```

#### File 3: `_code.md` — Code Patterns

| Category                        | What goes here                      |
| ------------------------------- | ----------------------------------- |
| **Code & Practice (代码/实践)** | Python code, lab patterns, commands |

**Rules (apply to all 3 files):**

- **Every bullet should be clearly categorized** — use descriptive bold labels
- Indented bullets inherit the parent's category
- Section headings use `## Section Name` + `### Category`

### ⚠️⚠️⚠️ CRITICAL — Section Internal Structure Per File

**`_cheatsheet.md` section structure:**

```
### Definition      ──► Noun definitions (名词解释)
### Key Points      ──► Core insights, memory aids
### Traps           ──► Quiz traps, common mistakes
### Compare         ──► Comparison table (对比表)
```

**`_math.md` section structure:**

```
## ★ 数学基础 (Math Foundations)   ──► FIRST section, prerequisite math
    ### Sigmoid / Tanh              ──► Function definition, properties, derivative, range table
    ### 链式法则 (Chain Rule)       ──► Single-layer & multi-layer, with hand calc
    ### 加法 vs 乘法 (Add vs Mul)  ──► Gradient fate comparison (the key to understanding vanishing gradient & LSTM)
    ### Hand Calc                   ──► Worked examples for each foundation topic
## [Topic sections]                 ──► Topic-specific formulas & hand calcs
    ### Formula                     ──► Formulas with parameter explanation
    ### Hand Calc                   ──► Step-by-step worked examples
## 速查公式表 (Quick Formula Ref)   ──► LAST section, summary table
```

> ⚠️ The ★ Math Foundations section MUST come FIRST. It covers prerequisite math that the topic formulas rely on (activation functions, derivatives, chain rule, gradient paths). Reading this section first makes the tutorial's derivations much easier to follow.

**`_code.md` section structure:**

```
## ★ 代码基础 (Code Foundations)    ──► FIRST section, prerequisite code patterns
    ### Numpy basics               ──► Array operations, matrix multiply, reshape, element-wise ops
    ### Matplotlib basics          ──► Plot patterns reused in all sections
    ### Framework building blocks  ──► Keras Sequential, compile, fit, predict pattern
## [Topic sections]                 ──► Topic-specific code patterns
    ### Code                       ──► Python code patterns, imports, API
## Key API Cheat Sheet              ──► LAST section, API reference table
```

> ⚠️ The ★ Code Foundations section MUST come FIRST. It covers numpy/matplotlib/Keras basics that all later code sections depend on. Reading this section first makes the lab code and demo script much easier to understand.

> Not every section needs all parts — only include the parts that have content. But the ORDER within each file is **FIXED**: Foundations → Topics → Reference Table.

### ⚠️⚠️⚠️ CRITICAL — Define Before Reference (再三强调)

**Terms MUST be defined in Definition BEFORE they are used in Formula/Hand Calc/Code.** Do NOT reference a term in formulas, examples, or code if it hasn't been defined in the SAME section's Definition group.

Examples:

- ❌ BAD: Core Concepts uses "MMC" in formula, but MMC is defined in a different section (SVM Types)
- ✅ GOOD: MMC formula appears in SVM Types section where MMC's definition exists

**If a term belongs to a different section, move the formula/example there.** Do NOT forward-reference undefined terms.

#### `_cheatsheet.md` Parts

**Definitions (名词解释):**

- **ALL nouns/terms that appear in this section** must have a definition here — including terms that ONLY appear in the table below
- **One term per line** — each definition is its own bullet
- Format: `- **TERM (Full English Name, 中文名):** definition`
- This block should be exhaustive — if a reader encounters ANY term in this section (bullet or table cell), its definition MUST be in this block

**Key Points (要点/记忆):**

- Core insights, goals, steps, memory aids
- Format: `- PCA goal: maximize variance along new axes`

**Traps & Warnings (陷阱/注意):**

- Quiz traps, common mistakes, warnings
- Format: `- Must standardize BEFORE PCA`

**Comparison Table (对比表):**

- Side-by-side comparison of related concepts
- Terms used in the table MUST already be defined in Definition above

#### `_math.md` Parts

**⚠️⚠️⚠️ CRITICAL — LaTeX Formatting (再三强调):**

- **ALL formulas MUST use LaTeX syntax** — `$...$` for inline, `$$...$$` for display blocks
- Do NOT use plain-text formulas — use proper LaTeX
- Parameter explanations go as plain text AFTER the LaTeX block, using `$var$` for variable names

Example:

```markdown
- **Bayes Theorem:**

$$P(Y|X) = \frac{P(X|Y) \cdot P(Y)}{P(X)}$$

$Y$ = class, $X$ = features, $P(X|Y)$ = likelihood, $P(Y)$ = prior
```

**Formulas (公式):**

- Every formula MUST include: LaTeX display block `$$...$$` + parameter definitions below
- Each step in a hand calc gets its own `$$...$$` block

**Hand Calculation (手写计算/例题):**

- **Step-by-step worked examples** with concrete numbers using LaTeX
- Label each step clearly (Step 1, Step 2, ...)
- Show problem setup, each calculation step, and final result

**Quick Formula Reference Table:**

- At the end of the math file, include a summary table of ALL formulas
- Table cells use inline LaTeX `$...$` for formulas
- Format: `| Name | Formula | Key Params |`

#### `_code.md` Parts

**⚠️⚠️⚠️ CRITICAL — Code Block Formatting (再三强调):**

- **ALL code MUST use fenced code blocks** with language tag ` ```python `
- Code blocks include **bilingual comments** (English first, Chinese below)
- Each code block should be a **complete, runnable snippet** — no broken fragments
- Group code by **task/workflow step**, not by individual function

**Code & Practice (代码/实践) — MANDATORY for weeks with labs:**

- **Every week that has a corresponding lab MUST have a `_code.md` file** — no exceptions
- **Formula-as-comment pattern**: show the formula being implemented as a comment above the code

Example:

````markdown
### Code

- **Gaussian PDF (scipy):** `scipy.stats.norm.pdf(x, μ, σ)`

- **Complete NB pipeline:**

  ```python
  # Naive Bayes classification pipeline
  # 朴素贝叶斯分类流程
  from sklearn.naive_bayes import GaussianNB

  gnb = GaussianNB()
  gnb.fit(X_train, y_train)       # Estimate μ, σ² per class
  y_pred = gnb.predict(X_test)    # argmax P(Y) × ∏ P(Xᵢ|Y)
  ```
````

````

**What to include per lab:**

- Key `sklearn` / `keras` / `tensorflow` imports
- Data loading & preprocessing calls
- Model instantiation with key parameters
- `.fit()` / `.predict()` / `.transform()` patterns
- **fit on train, transform on both** — prevent data leakage
- Evaluation metrics (`accuracy_score`, `confusion_matrix`, etc.)
- Visualization patterns (`plt.scatter`, `Axes3D`, etc.)

#### Example — `_cheatsheet.md` section

```markdown
## Kernel Functions

### Definition

- **Kernel (核函数):** compute similarity in high-dim WITHOUT explicitly mapping data there
- **Kernel Trick (核技巧):** use kernel function to implicitly work in high-dim space
- **RBF (Radial Basis Function, 径向基函数):** most common non-linear kernel

### Traps

- Most common non-linear kernel? → RBF, NOT polynomial

| Kernel       | Boundary Shape    | When to Use                  |
| ------------ | ----------------- | ---------------------------- |
| Linear       | Straight line     | Linearly separable data      |
| RBF/Gaussian | Complex, flexible | MOST COMMON — default choice |
````

❌ BAD: table mentions "RBF" but no definition for RBF in Definition above
✅ GOOD: every term in the table is defined in Definition section

### Why This Design?

- **Denser** — no padding/margins from colored boxes = more content per page
- **Faster scanning** — clear category headers let eyes jump to the right section instantly
- **Easier maintenance** — simpler JSON, fewer things to break
- **Print-friendly** — consistent rendering across browsers and printers
- **Predictable layout** — reader always knows: definitions → formulas → traps → table

## From-Zero Workflow

### Step 0: Identify Sources

Locate all source materials for the exam scope:

```
courses/{course}/notes/lecture*_slides.md   → slides (primary)
courses/{course}/quizzes/                   → quiz files (traps, key points)
courses/{course}/labs/                      → lab docs (practical knowledge)
```

Read ALL source files within the exam scope before writing anything.

### Step 1: Create `{exam}_cheat_sheet.json`

This is the single structured data file. Read every slide, quiz, and lab file, then build the JSON directly.

#### Source Priority

1. **Slides** (`lecture*_slides.md`) — definitions, concepts, formulas, comparisons
2. **Quizzes** (`quizzes/*.md`) — trap questions (⚠️), correct/incorrect patterns
3. **Labs** (`labs/*.md`) — practical commands, code patterns, common mistakes

#### JSON Schema

```json
{
  "title": "Course Exam Cheat Sheet (W1-WN)",
  "pages": [
    {
      "label": "PAGE 1 (W1–W3)",
      "weeks": [
        {
          "id": "W1",
          "title": "Topic (中文)",
          "sections": [
            {
              "title": "Section Name",
              "content": [
                "── Part 1: Noun Definitions (名词解释) ──",
                "Term A (Full Name, 中文): definition of A",
                "Term B (Full Name, 中文): definition of B",
                "Term C (Full Name, 中文): definition of C",
                "",
                "── Part 2: Key Notes (注意事项) ──",
                "Formula: x' = (x − min) / (max − min) → [0,1]",
                "⚠️ Common trap — correct answer here"
              ],
              "table": {
                "headers": ["Col A", "Col B", "Col C"],
                "rows": [
                  ["val1", "val2", "val3"],
                  ["val4", "val5", "val6"]
                ]
              }
            }
          ]
        }
      ]
    }
  ],
  "milestones": [{ "year": "1997", "event": "Description" }],
  "flash_cards": ["Key review item 1", "Key review item 2"]
}
```

> **Note:** The `── Part 1 ──` and `── Part 2 ──` comment lines are for illustration only — do NOT include them in actual JSON. The visual separation comes naturally from the ordering: definitions first, then notes.

**Section fields:**

| Field     | Required? | Description                            |
| --------- | --------- | -------------------------------------- |
| `title`   | ✅ Yes    | Section heading text                   |
| `content` | Optional  | Array of bullet strings                |
| `table`   | Optional  | Object with `headers[]` and `rows[][]` |

That's it. **No other fields.** Formulas, warnings, examples — all go into `content[]` as regular bullets.

#### Content Encoding Rules

##### ⚠️⚠️⚠️ CRITICAL — Terms Must Include Definition (再三强调)

**Every technical term or concept MUST include its definition inline.** Don't just name a term — explain what it IS.

**ALL nouns from the section must be defined** — including terms that only appear in the table. If a table mentions "RBF", "Polynomial", etc., each must have a definition bullet in `content[]`. **One term per line, each on a separate bullet.**

```json
"content": [
  "Support Vectors (支持向量): closest data points to the hyperplane — they define the margin width",
  "Kernel Trick (核技巧): compute similarity in high-dim space WITHOUT explicitly mapping data there",
  "Overfitting (过拟合): model memorizes training data, performs poorly on new data",
  "",
  "key note goes here after all definitions"
]
```

❌ BAD: `"Support Vectors"` — no definition, reader doesn't know what it means
❌ BAD: `"Kernel Trick: ..."` — missing definition
✅ GOOD: `"Support Vectors (支持向量): closest points to hyperplane — define margin width"`
✅ GOOD: every term that appears anywhere in the section has a definition bullet

##### ⚠️⚠️⚠️ CRITICAL — Formulas Must Include Explanation + Example (再三强调)

**Every formula MUST include: (1) a label, (2) parameter definitions, and (3) at least one concrete example.**

```json
"content": [
  "Normalization (Min-Max): x' = (x−x_min)/(x_max−x_min) → [0,1]. x=value, x_min/x_max=feature min/max",
  "  Ex: x=50, min=0, max=100 → (50−0)/(100−0) = 0.5",
  "Z-score: z = (x−μ)/σ → mean=0, SD=1. x=value, μ=mean, σ=std dev",
  "  Ex: x=50, μ=40, σ=10 → (50−40)/10 = 1.0"
]
```

❌ BAD: `"(x−min)/(max−min)"` — no label, no parameter explanation, no example
✅ GOOD: formula label + what each variable means + concrete numbers

##### Other Content Encoding

**Warnings/traps:**

```json
"content": [
  "⚠️ Must standardize BEFORE PCA — large-scale features dominate",
  "⚠️ PCA is Feature EXTRACTION, NOT Feature Selection"
]
```

**Comparisons → always use tables:**

```json
"table": {
  "headers": ["", "PCA", "LDA"],
  "rows": [
    ["Type", "Unsupervised", "Supervised"],
    ["Objective", "Max variance", "Max class separation"]
  ]
}
```

#### Content Rules

##### ⚠️⚠️⚠️ CRITICAL — Abbreviations & Chinese (再三强调)

**Chinese (中文) ONLY appears in `content[]` bullets, alongside abbreviation + full English name.** Tables, section titles, and other places use English only.

Format in bullets: `ABBR (Full English Name, 中文名): definition`

Examples:

- `PCA (Principal Component Analysis, 主成分分析): unsupervised DR method that maximizes variance`
- `LSTM (Long Short-Term Memory, 长短期记忆网络): RNN variant with 3 gates + cell state`
- `BPTT (Backpropagation Through Time, 时序反向传播): backprop unrolled over time steps`

Where Chinese does NOT go:

- ❌ Table cells — English only
- ❌ Section titles — English only
- ❌ Week titles — English only (except the parenthetical one in `.wt`)

##### ⚠️⚠️⚠️ CRITICAL — Completeness / Zero Omission (再三强调)

**EVERY piece of testable knowledge from slides, quizzes, and labs MUST be included.** Do NOT summarize. Do NOT condense. Do NOT skip "obvious" content.

**EXCLUDE non-testable administrative content:** grading breakdown, evaluation percentages, submission deadlines, attendance policies, contact info, office hours, textbook lists, tool setup instructions, demo announcements, Q&A slides. These are course logistics, NOT exam content.

Checklist per source file:

- Every definition → included as bullet
- Every formula → included as bullet
- Every comparison table → included as table
- Every example/worked problem → included as bullets
- Every ⚠️ trap question from quizzes → included as bullet with ⚠️ prefix
- Every code pattern from labs → included as bullet
- Every diagram description → included as bullet

If the cheat sheet feels "too short", you MISSED content. Go back and re-read every source file line by line.

##### ⚠️⚠️⚠️ CRITICAL — Atomicity (再三强调)

**One bullet = one fact. One table row = one item. One table column = one dimension.** Do NOT combine multiple ideas into a single bullet or cell.

❌ BAD bullet (two things crammed together):

```
"PCA: unsupervised, ignores class labels. Goal: max variance. 5 Steps: standardize → covariance → eigenvalues → sort → transform"
```

✅ GOOD bullets (one thing each):

```
"PCA (Principal Component Analysis, 主成分分析): unsupervised DR, ignores class labels"
"PCA goal: maximize variance along new axes"
"PCA steps: 1) Standardize → 2) Covariance matrix → 3) Eigenvalues & Eigenvectors → 4) Sort → 5) Transform"
```

❌ BAD table (multiple dimensions in one column):

```
headers: ["Algorithm", "Pros & Cons"]
rows: [["SVM", "High accuracy, fast prediction / Not for large datasets, sensitive to kernel"]]
```

✅ GOOD table (one dimension per column):

```
headers: ["Algorithm", "Advantage", "Disadvantage"]
rows: [
  ["SVM", "High accuracy", "Not for large datasets"],
  ["SVM", "Fast prediction", "Sensitive to kernel choice"]
]
```

##### ⚠️⚠️⚠️ CRITICAL — Instant Readability / Zero Confusion (再三强调)

**EVERY item on the cheat sheet MUST be instantly understandable by the reader during an exam.** If a reader sees a line and thinks "what does this mean?", you have FAILED.

Rules:

- **No bare variable names without context** — `f_t` alone is meaningless. Write `Forget Gate: f_t=σ(…)` so the reader knows which gate, which formula.
- **Every formula must have a label** — `(1/n)Σ(y−ŷ)²` alone is useless. Write `MSE: (1/n)Σ(y−ŷ)²`.
- **Every comparison must state WHAT is being compared** — use descriptive column headers.
- **Every trap must be self-contained** — include the question AND the answer: `⚠️ Most common non-linear kernel → RBF, NOT polynomial`.
- **Every worked example must state the PROBLEM** — include the setup: `Tax Evasion: X=(Refund=No, Divorced, Income=120K)`.

##### ⚠️⚠️⚠️ CRITICAL — Comparison Tables (再三强调)

**ALL related/comparable technologies MUST have a side-by-side comparison table.** Whenever two or more concepts can be contrasted, add a table. Do NOT describe differences in prose — use tables.

### Step 2: Build `{exam}_cheat_sheet_final.html`

Run the build script **directly from the skill directory** — no need to copy:

```bash
uv run python .agent/skills/learning-cheat_sheet/references/build_script_template.py courses/{course}/notes/{exam}_cheat_sheet.json
```

The script accepts:

- **Arg 1** (required): path to the `{exam}_cheat_sheet.json`
- **Arg 2** (optional): output HTML path. Defaults to `{exam}_cheat_sheet_final.html` in the same directory as the input JSON.

#### Layout Specifications

| Property       | Value                                            |
| -------------- | ------------------------------------------------ |
| Page size      | **11in wide × 8.5in tall (US Letter Landscape)** |
| Margins        | 4mm all sides                                    |
| Columns        | **3 per page**                                   |
| Weeks per page | **2 per page** (recommended, split if overflow)  |
| Font           | Consolas/monospace, 5pt base                     |

> **Why landscape?** With 2 weeks per page, landscape orientation provides ~40% more horizontal space. 3 columns keep text wide enough for Python code readability.

⚠️ **Overflow Prevention**: If a page's content overflows (columns overlap, content gets clipped), split that page into two pages in the JSON. NEVER cram too much content into one page — readability beats compactness.

#### CSS Class Reference

| Class   | Purpose                             |
| ------- | ----------------------------------- |
| `.page` | One printed page, `column-count: 3` |
| `.wk`   | Week block with dark header         |
| `.wt`   | Week title (dark background)        |
| `.st`   | Section title with bottom border    |
| `.code` | Code block with mono font + bg      |

That's it — **5 classes total**. Bullets are `<ul><li>`, tables are `<table>`. No colored boxes.

**For the build script template:** See `references/build_script_template.py`

## Validation

After each step, verify:

### Step 1 (.json)

- [ ] Valid JSON (no trailing commas, proper escaping)
- [ ] Every slide section from every lecture in scope is covered — **no omissions**
- [ ] Every quiz question/trap is included — **no omissions**
- [ ] Lab practical points are captured — **no omissions**
- [ ] **EVERY abbreviation has full form + (中文) on EVERY occurrence**
- [ ] **EVERY technical term has (中文) annotation**
- [ ] **ALL comparable technologies have side-by-side comparison tables**
- [ ] Each section has ONLY `title`, `content`, and/or `table` — no other fields
- [ ] Content length is proportional to source material

### Step 2 (.html)

- [ ] Open in browser → Ctrl+P → **11×8.5 landscape** layout correct
- [ ] **3 columns** per page, content does NOT overlap
- [ ] No content overflow/truncation — if overflow, split page in JSON
- [ ] **🔧 Python code bullets present** for every week that has labs
- [ ] **Readability self-test**: read every line as if stressed during exam — every item must be instantly understandable

## Common Issues

- Content overflows page → reduce font size in CSS (min 4pt) or split sections across pages in JSON
- JSON parse error → check for unescaped quotes in formulas
- Table too wide → reduce column count or abbreviate cell content
- Too dense → increase `line-height` in CSS (current: 1.2)

## Migration from v1

If converting an existing v1 JSON (with `formulas`, `traps`, `examples`, `content_extra`, `keypoints`):

1. Move all `formulas[]` items into `content[]`
2. Move all `traps[]` items into `content[]` with `⚠️` prefix
3. Move all `examples[]` → flatten `label` + `steps` into `content[]` bullets
4. Move all `content_extra[]` items into `content[]`
5. Remove `keypoints`, `quiz_answers` → move to `flash_cards` or inline as bullets
6. Delete the old fields — section should only have `title`, `content`, `table`
