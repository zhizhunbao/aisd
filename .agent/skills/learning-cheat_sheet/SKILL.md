---
name: learning-cheat_sheet
description: Generate exam cheat sheets from slides, quizzes, and labs. Use when (1) user asks to create/update a cheat sheet, (2) mentions "cheat sheet" or "小抄", (3) needs to compile exam review material into printable format.
---

# Cheat Sheet Generator

## Objectives

- Extract ALL testable content from slides, quizzes, and labs into a printable cheat sheet
- Pipeline: source materials → `.md` → `.json` → `.html`
- Zero information loss — every concept, formula, trap, and example must be captured

## File Naming Convention

All cheat sheet files live in `courses/{course}/notes/` and follow this pattern:

```
courses/{course}/notes/
├── {exam}_cheat_sheet.md           # Step 1 output (human-readable)
├── {exam}_cheat_sheet.json         # Step 2 output (structured data)
├── {exam}_cheat_sheet.html         # Step 3 output (print-ready)
├── md_to_json_{exam}.py            # Convert script (MD → JSON)
└── build_{exam}_cheat_sheet.py     # Build script (JSON → HTML)
```

**Script templates in `references/`:**
- `md_to_json_template.py` — MD → JSON conversion
- `build_script_template.py` — JSON → HTML generation

Where `{exam}` = exam name in snake_case, e.g.:
- `midterm_cheat_sheet.md` — 期中
- `final_cheat_sheet.md` — 期末
- `quiz3_cheat_sheet.md` — 单次测验

## From-Zero Workflow

### Step 0: Identify Sources

Locate all source materials for the exam scope:

```
courses/{course}/notes/lecture*_slides.md   → slides (primary)
courses/{course}/quizzes/                   → quiz files (traps, key points)
courses/{course}/labs/                      → lab docs (practical knowledge)
```

Read ALL source files within the exam scope before writing anything.

### Step 1: Create `{exam}_cheat_sheet.md`

This is the master document. Read every slide, quiz, and lab file, then write a comprehensive markdown covering all weeks in scope.

#### Source Priority

1. **Slides** (`lecture*_slides.md`) — definitions, concepts, formulas, comparisons
2. **Quizzes** (`quizzes/*.md`) — trap questions (⚠️), correct/incorrect patterns
3. **Labs** (`labs/*.md`) — practical commands, code patterns, common mistakes

#### Content Rules

##### ⚠️⚠️⚠️ CRITICAL — Abbreviations (再三强调)

**EVERY abbreviation MUST include its full English form AND (中文) EVERY time it appears.** No exceptions. No "first use only" — EVERY occurrence.

Format: `ABBR (Full English Name, 中文名)`

Examples:
- `NLP (Natural Language Processing, 自然语言处理)`
- `LSTM (Long Short-Term Memory, 长短期记忆网络)`
- `BPTT (Backpropagation Through Time, 时序反向传播)`
- `SGNS (Skip-Gram with Negative Sampling, 跳字负采样)`
- `PPL (Perplexity, 困惑度)`
- `OOV (Out-of-Vocabulary, 未登录词)`
- `FFNN (Feed-Forward Neural Network, 前馈神经网络)`
- `POS (Part of Speech, 词性)`
- `NER (Named Entity Recognition, 命名实体识别)`
- `BOW (Bag of Words, 词袋模型)`
- `LM (Language Model, 语言模型)`

Even well-known abbreviations (AI, ML, DL, RNN, CNN, BERT, GPT) MUST have full form + 中文. **NEVER write a bare abbreviation without full form.**

##### ⚠️⚠️⚠️ CRITICAL — Technical Terms (再三强调)

**EVERY technical term MUST have (中文) annotation.** No exceptions.

Format: `English Term (中文)`

Examples:
- `Tokenization (分词)`
- `Vanishing Gradient (梯度消失)`
- `Cosine Similarity (余弦相似度)`
- `Attention Mechanism (注意力机制)`

##### ⚠️⚠️⚠️ CRITICAL — Math Formulas (再三强调)

**ALL math formulas MUST use LaTeX notation.** No plain text math. No ASCII approximations.

Format: `$LaTeX$` for inline, code block with LaTeX for display

Examples:
- ✅ `$P(w_t | w_{t-1}) = \frac{C(w_{t-1}, w_t)}{C(w_{t-1})}$`
- ✅ `$\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \times \|\vec{B}\|}$`
- ✅ `$IDF(t) = \log\frac{N}{df(t)}$`
- ❌ `cos(θ) = (A · B) / (‖A‖ × ‖B‖)` — FORBIDDEN plain text
- ❌ `IDF = log(N/df)` — FORBIDDEN ASCII math

##### ⚠️⚠️⚠️ CRITICAL — Define Before Reference (再三强调)

**Terms MUST be defined BEFORE they are referenced.** Do NOT use a term in formulas, examples, or code before its definition appears in `#### 📖 Definitions`.

**Structure order matters:**
1. `#### 📖 Definitions` — define ALL terms used in this section first
2. `#### 📐 Formulas` — only use terms already defined above
3. `#### 📝 Examples` — only use terms already defined above
4. Other sections follow...

Examples:
- ❌ BAD: Core Concepts formula mentions "MMC Goal" but MMC is defined in SVM Types section below
- ✅ GOOD: MMC formula appears in SVM Types section where MMC is defined

**If a term belongs to a different section, move the formula/example to that section.** Do NOT forward-reference undefined terms.

##### ⚠️⚠️⚠️ CRITICAL — Completeness / Zero Omission (再三强调)

**EVERY piece of testable knowledge from slides, quizzes, and labs MUST be included.** Do NOT summarize. Do NOT condense. Do NOT skip "obvious" content.

**EXCLUDE non-testable administrative content:** grading breakdown, evaluation percentages, submission deadlines, attendance policies, contact info, office hours, textbook lists, tool setup instructions, demo announcements, Q&A slides. These are course logistics, NOT exam content.

Checklist per source file:
- Every definition → included
- Every formula → included in LaTeX
- Every comparison table → included
- Every example/worked problem → included
- Every ⚠️ trap question from quizzes → included
- Every code pattern from labs → included
- Every diagram description → included as text

If the cheat sheet feels "too short", you MISSED content. Go back and re-read every source file line by line.

##### ⚠️⚠️⚠️ CRITICAL — Worked Examples / Hand Calculations (再三强调)

**EVERY worked example and hand calculation from slides MUST be included with FULL step-by-step details.** Exams often require students to perform calculations by hand — these examples are the most testable content.

Must-include worked examples (non-exhaustive):
- **PCA**: Eigenvalue → Variance ratio calculation (e.g., λ=[2.94, 0.92] → 73%, 23%)
- **CNN**: Output size calculation with padding/stride (e.g., 6×6 * 3×3 → 4×4)
- **Naive Bayes**: Full classification with P(X|Y) decomposition and Gaussian PDF
- **Conditional Probability**: Dice/card examples with P(A|B) = P(A∩B)/P(B)
- **Clustering**: SSE/SSB calculation for K=1 vs K=2
- **Silhouette Coefficient**: a, b, s calculation for a specific point
- **SVM**: Margin width calculation (2/||w||)
- **LSTM**: Gate output calculation (forget, input, output)

Format in `#### Examples`:
```markdown
#### Examples
- **PCA Variance Calculation**:
  - Eigenvalues: λ = [2.94, 0.92, 0.15, 0.02]
  - Total = 4.03
  - PC1 = 2.94/4.03 = **0.73 (73%)**
  - PC1 + PC2 = 0.96 → **96% information retained**
```

**If slides show a calculation with numbers, the cheat sheet MUST show the same calculation with all intermediate steps.**

##### ⚠️⚠️⚠️ CRITICAL — Comparison Tables (再三强调)

**ALL related/comparable technologies MUST have a side-by-side comparison table.** Whenever two or more concepts can be contrasted, add a markdown table. Do NOT describe differences in prose — use tables.

Must-have comparison tables (non-exhaustive):
- Stemming vs Lemmatization
- SpaCy vs NLTK
- One-Hot vs BOW vs N-Gram vs TF-IDF
- TF-IDF vs Word Embeddings
- CBOW vs Skip-gram
- Word2Vec vs GloVe vs FastText
- RNN vs FFNN
- RNN vs LSTM
- Vanishing Gradient vs Exploding Gradient
- Unidirectional LSTM vs Bi-LSTM
- Seq2Seq vs Seq2Seq+Attention
- RNN Attention vs Self-Attention (Transformer)
- Teacher Forcing vs Autoregressive decoding
- Intrinsic vs Extrinsic evaluation
- Low learning rate vs High learning rate

Format:
```markdown
| Dimension | A | B |
|---|---|---|
| Speed | Fast | Slow |
| Accuracy | Low | High |
```

If a comparison exists in slides but is missing from the cheat sheet, you MISSED content. Go back and add it.

##### ⚠️⚠️⚠️ CRITICAL — Code-Formula Correspondence (再三强调)

**Code in `#### Code` MUST correspond to formulas in `#### Formulas`.** Every formula should have matching sklearn/library code, and every code block should reference its formula in comments.

Format: `# MethodName (LibraryClass): formula → output_range`

Examples:
- ✅ `# Normalization (MinMaxScaler): x' = (x - min) / (max - min) → [0,1]`
- ✅ `# Standardization (StandardScaler): z = (x - μ) / σ → mean=0, std=1`
- ❌ Standalone sklearn code without formula reference
- ❌ Formula in `#### Formulas` with no matching code

Code section must show:
1. **Import statements** — all required libraries
2. **Train/test split** — proper data preparation workflow
3. **fit() on train only** — prevent data leakage
4. **transform() on both** — apply learned parameters
5. **Common mistakes** — comment what NOT to do

##### Other Rules

- **Language**: primarily English; Chinese only for `(中文)` annotations
- **Trap questions**: prefix with `⚠️`, include false statement + correction

#### Markdown Template (6-Layer Structure)

Use `####` headings to separate 6 content types within each section. This enables reliable parsing by `md_to_json.py`.

**Layer Structure:**
```
# Title                    ← Level 1: Root
## W1: Topic               ← Level 2: Week
### Section Name           ← Level 3: Section
#### Definitions           ← Level 4: Content Type (1 of 6)
- bullet                   ← Level 5: Items
```

**6 Content Types (must use exact `####` headings):**

| # | `####` Heading | JSON Field | Purpose |
|---|----------------|------------|---------|
| 1 | `#### Definitions` | `content` | 定义、概念、要点 |
| 2 | `#### Comparisons` | `table` | 对比表格 |
| 3 | `#### Formulas` | `formulas` | LaTeX 公式 |
| 4 | `#### Examples` | `examples` | 示例、步骤 |
| 5 | `#### Traps` | `traps` | ⚠️ 易错点 |
| 6 | `#### Code` | `code` | Python 代码 |

**Template:**

```markdown
# [Course Code] [Exam] Cheat Sheet (W1–WN)

> Merged from slides + quizzes + labs. ⚠️ = common trap questions.

---

## W1: [Topic] (中文)

### Section Name (中文)

#### Definitions
- **Term (Full Name, 中文)** = definition
- **Another Term (中文)** = definition

#### Comparisons
| Dimension | A | B |
|---|---|---|
| Speed | Fast | Slow |
| Accuracy | Low | High |

#### Formulas
- $P(w_t | w_{t-1}) = \frac{C(w_{t-1}, w_t)}{C(w_{t-1})}$
- $\text{TF-IDF} = TF \times IDF$

#### Examples
- **Example 1**: Input "Hello World" → Output ["Hello", "World"]
- **Example 2**: Step 1 → Step 2 → Step 3

#### Traps
- ⚠️ "false statement" → **False** (correction)
- ⚠️ "another trap" → **False** (why)

#### Code
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Normalization (MinMaxScaler): x' = (x - min) / (max - min) → [0,1]
minmax = MinMaxScaler()
minmax.fit(X_train)                    # learn min, max from train
X_train_norm = minmax.transform(X_train)
X_test_norm = minmax.transform(X_test)  # use train's min, max

# Standardization (StandardScaler): z = (x - μ) / σ → mean=0, std=1
scaler = StandardScaler()
scaler.fit(X_train)                    # learn μ, σ from train
X_train_std = scaler.transform(X_train)
X_test_std = scaler.transform(X_test)  # use train's μ, σ

# WRONG: fit_transform on test = data leakage!
```

**Code Section Rules:**
- **Formula in comment**: Each sklearn method MUST have its formula as inline comment
- **Format**: `# MethodName (SklearnClass): formula → output_range`
- **Match Formulas section**: Code must correspond to formulas defined in `#### Formulas`
- **Show workflow**: Include train/test split, fit on train, transform on both
- **Highlight pitfalls**: Comment common mistakes (e.g., data leakage)

### Another Section
...

---

## W2: [Topic] (中文)
...

---

## Milestones

| Year | Event |
|---|---|

## Quiz Quick Review

✅ Key point 1
✅ Key point 2
```

**Notes:**
- Not all 6 content types are required in every section — only include what's relevant
- Order of `####` headings within a section doesn't matter
- Empty sections can be omitted entirely

### Step 2: Convert to `{exam}_cheat_sheet.json`

1. Copy the conversion script template from `references/md_to_json_template.py` to `courses/{course}/notes/md_to_json_{exam}.py`
2. Update the config variables at the top:
   - `INPUT_MD` = `"{exam}_cheat_sheet.md"`
   - `OUTPUT_JSON` = `"{exam}_cheat_sheet.json"`
3. Run: `uv run python md_to_json_{exam}.py`

**JSON Schema:**

```json
{
  "title": "Course Exam Cheat Sheet (W1-WN)",
  "description": "Merged from slides + quizzes + labs.",
  "weeks": [
    {
      "id": "W1",
      "title": "Topic (中文)",
      "sections": [
        {
          "title": "Section Name",
          "content": ["bullet points"],
          "table": { "headers": [], "rows": [[]] },
          "formulas": ["LaTeX strings"],
          "examples": [{ "label": "str", "steps": ["str"] }],
          "traps": ["trap descriptions"],
          "code": [{ "lang": "python", "snippet": "code here" }]
        }
      ]
    }
  ],
  "milestones": [{ "year": "str", "event": "str" }],
  "flash_cards": ["quick review items"],
  "quiz_answers": [
    {
      "quiz": "Quiz N — Topic",
      "questions": [{ "topic": "str", "key_point": "str" }]
    }
  ]
}
```

**Mapping rules (#### heading → JSON field):**

| Markdown `####` | JSON Field | Parsing Rule |
|-----------------|------------|--------------|
| `#### Definitions` | `content[]` | Each `- bullet` → string |
| `#### Comparisons` | `table` | Parse markdown table → `{headers, rows}` |
| `#### Formulas` | `formulas[]` | Each `- $...$` → LaTeX string |
| `#### Examples` | `examples[]` | Each `- **Label**: ...` → `{label, steps}` |
| `#### Traps` | `traps[]` | Each `- ⚠️ ...` → string |
| `#### Code` | `code[]` | Each ` ```python ``` ` → `{lang, snippet}` |

- `## Milestones` table → `milestones[]`
- `## Quiz Quick Review` → `quiz_answers[]`

### Step 3: Build `{exam}_cheat_sheet.html`

1. Copy the build script template from `references/build_script_template.py` to `courses/{course}/notes/build_{exam}_cheat_sheet.py`
2. Update the config variables at the top:
   - `INPUT_JSON` = `"{exam}_cheat_sheet.json"`
   - `OUTPUT_HTML` = `"{exam}_cheat_sheet.html"`
   - `QUIZ_TO_WEEK` = mapping for this exam's quizzes
3. Run: `uv run python build_{exam}_cheat_sheet.py`

#### Layout Specifications

| Property | Value |
|---|---|
| Page size | 8.5in wide × 11in tall (US Letter) |
| Margins | 4mm all sides |
| Columns | 3 per page |
| Weeks per page | 3 |
| Signature box | 5cm × 5cm, top-left corner, dashed border |
| Font | Consolas/monospace, 5pt base |

#### CSS Class Reference

| Class | Purpose |
|---|---|
| `.page` | One printed page, `column-count: 3` |
| `.sig` | 5cm × 5cm signature box, dashed border |
| `.wk` | Week block with dark header |
| `.st` | Section title with bottom border |
| `.f` | Formula block (yellow background) |
| `.w` | Trap/warning block (red left border) |
| `.g` | Example block (green left border) |
| `.kp` | Quiz key points (blue left border) |

**For the build script template:** See `references/build_script_template.py`

## Validation

After each step, verify:

### Step 1 (.md)
- [ ] Every slide section from every lecture in scope is covered — **no omissions**
- [ ] Every quiz question/trap is included — **no omissions**
- [ ] Lab practical points are captured — **no omissions**
- [ ] **EVERY abbreviation has full form + (中文) on EVERY occurrence** (grep for bare abbreviations)
- [ ] **EVERY technical term has (中文) annotation**
- [ ] **ALL formulas use LaTeX notation** (no plain text math anywhere)
- [ ] Content length is proportional to source material — if sources have 300+ slides, cheat sheet should be 500+ lines
- [ ] **ALL comparable technologies have side-by-side comparison tables** (no prose-only comparisons)

### Step 2 (.json)
- [ ] Valid JSON (no trailing commas, proper escaping)
- [ ] All markdown content mapped to correct fields
- [ ] `quiz_answers` properly linked to weeks

### Step 3 (.html)
- [ ] Open in browser → Ctrl+P → 8.5×11 layout correct
- [ ] Signature box is 5×5cm in top-left
- [ ] 3 weeks per page, 3 columns
- [ ] No content overflow/truncation

## Common Issues

- Content overflows page → reduce font size (min 4pt) or split sections
- JSON parse error → check for unescaped quotes in formulas
- Signature box misaligned → ensure `.sig` is first child in `.page`
- Missing quiz points → verify `QUIZ_TO_WEEK` mapping in build script
