---
name: learning-source_citation
description: Cross-cutting rule for all learning materials. Every claim must cite a textbook source, every conclusion must have a proof or derivation. No unsourced content allowed. 跨所有学习资料的通用规则：所有资料必须注明来源教科书，结论必须附带证明，不能拍脑袋。
---

# 📚 Source Citation & Proof Rule | 来源引证与证明规则

> **This rule applies to ALL learning material files.**
> **此规则适用于所有学习资料文件。**

## ⚠️ Absolute Rule: No Unsourced Content | 绝对规则：不允许无来源内容

Every formula, definition, theorem, conclusion, and non-trivial claim in any learning material **MUST** cite its source:

所有学习资料中的每个公式、定义、定理、结论和重要论述**必须**标明来源：

```markdown
> 📚 Source: Murphy §9.3, Eq. 9.46 — Murphy, Kevin P. "Probabilistic Machine Learning"
> 📚 来源：Murphy §9.3, 公式 9.46 — Murphy, Kevin P. "Probabilistic Machine Learning"
```

---

## Rule 1: Source First (来源优先)

Every section/subsection that introduces a formula or concept starts with a `> 📚 Source:` blockquote.

每个引入公式或概念的章节/小节必须以 `> 📚 Source:` 引用块开头。

### Citation Format (引用格式)

```markdown
> 📚 Source: [Book Key] §[Chapter.Section], Eq. [Number] — [Author]
> 📚 来源：[教科书缩写] §[章.节], 公式 [编号] — [作者]
```

### Precision Level (精确度要求)

| Level        | Example                 | When to Use                    |
| ------------ | ----------------------- | ------------------------------ |
| **Equation** | `Murphy Eq. 9.46`       | Specific formula — 具体公式    |
| **Section**  | `MML §6.3, pp. 189–191` | Definition/theorem — 定义/定理 |
| **Chapter**  | `Goodfellow Ch. 3`      | General concept — 一般概念     |

**Minimum requirement: Section level.**
**最低要求：精确到节。**

---

## Rule 2: Conclusion Must Have Proof (结论必须有证明)

Every conclusion/formula must satisfy **one** of the following:

每个结论/公式必须满足以下**之一**：

### Option A: Textbook Proof (教科书证明)

Cite the textbook's original derivation and reproduce the key steps:

引用教科书原文证明并复现关键步骤：

```markdown
> 📚 Proof: MML §6.3, Theorem 6.12

**Step 1:** Start from the product rule...
$$P(A, B) = P(A|B) \cdot P(B)$$

**Step 2:** By symmetry, also...
$$P(A, B) = P(B|A) \cdot P(A)$$

**Step 3:** Therefore...
$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$
```

### Option B: Supplementary Derivation (补充推导)

When the textbook doesn't provide a proof but the tutorial needs one, derive it yourself and **clearly mark** it:

当教科书未提供证明但教程需要时，自行推导并**明确标注**：

```markdown
> 📐 Supplementary derivation (tutorial supplement, not from textbook)
> 📐 补充推导（tutorial 补充，非教科书原文）

The number of parameters without the naive assumption:
未加朴素假设时的参数数量：

- Each feature $x_j$ has $v$ possible values → 每个特征 $x_j$ 有 $v$ 个可能值
- With $D$ features, total combinations = $v^D$ → $D$ 个特征的总组合数 = $v^D$
- Minus 1 for the sum-to-one constraint → 减1（因为概率之和为1的约束）
- Therefore: parameters = $v^D - 1$ → 所以参数数 = $v^D - 1$
```

### What is NOT Allowed (不允许的做法)

❌ **Bare conclusion without proof or source:**
❌ **无证明或来源的裸结论：**

```markdown
<!-- BAD — 拍脑袋！ -->

The number of parameters is $v^D - 1$.
```

❌ **"It is well known that..." without citation:**
❌ **"众所周知..."但不给引用：**

```markdown
<!-- BAD — 谁说的？哪本书？ -->

It is well known that naive Bayes is equivalent to logistic regression.
```

---

## Rule 3: Bilingual Requirement (双语要求)

All source citations and proofs must be bilingual (Chinese + English):

所有来源引用和证明必须双语（中英文）：

- **Citation line:** Both languages on the same line or consecutive lines
  引用行：两种语言在同一行或连续行
- **Proof steps:** English first, Chinese second (matching the note-taking convention)
  证明步骤：英文在前，中文在后（与笔记规范一致）
- **Symbol legends:** Both `Meaning` and `含义` columns
  符号对照表：同时包含 `Meaning` 和 `含义` 列

---

## Rule 4: Symbol Legend Before Each Formula (公式前符号对照表)

Every formula's **first appearance** must have a symbol legend table:

每个公式**首次出现**时必须附带符号对照表：

```markdown
| Symbol | Meaning (EN) | 含义 (中文)           | Example  |
| ------ | ------------ | --------------------- | -------- | ----------------- | ---------------- |
| $P(A   | B)$          | Posterior probability | 后验概率 | P(tax_evasion=yes | income=high)     |
| $P(B   | A)$          | Likelihood            | 似然     | P(income=high     | tax_evasion=yes) |
```

---

## Applicability Matrix (适用范围)

| File Type                  | Source Required?    | Proof Required?             | Bilingual?  |
| -------------------------- | ------------------- | --------------------------- | ----------- |
| `*_tutorial.md`            | ✅ Every formula    | ✅ Every conclusion         | ✅          |
| `*_math.md` (foundation)   | ✅ Every formula    | ✅ Every theorem            | ✅          |
| `*_math.md` (cheat sheet)  | ✅ Section-level    | ⚠️ Reference only           | ✅          |
| `*_storyline.md`           | ✅ Key claims       | ⚠️ Reference to tutorial    | ✅ (主中文) |
| `*_concepts.md`            | ✅ Section-level    | ❌ Definitions only         | ✅          |
| `*_cheatsheet.md`          | ✅ Section-level    | ❌ Definitions only         | ✅          |
| `*_code.md`                | ⚠️ Algorithm source | ❌ Not applicable           | ✅          |
| `*_slides.md`              | ❌ Teacher's slides | ❌ Teacher's content        | ✅          |
| `*_notes.md` (note-taking) | ✅ Key claims       | ⚠️ When presenting formulas | ✅          |

---

## Quality Checklist (质量检查清单)

Before completing any learning material file, verify:

完成任何学习材料文件前，验证：

- [ ] **Every formula has a `📚 Source:` citation** — 每个公式都有来源引用
- [ ] **Every conclusion has a proof or derivation** — 每个结论都有证明或推导
- [ ] **No bare claims** — supplementary derivations are clearly marked — 无裸论述，补充推导有明确标注
- [ ] **Bilingual** — all citations and proofs in both EN and CN — 双语
- [ ] **Symbol legends** present for all formulas on first appearance — 符号对照表
- [ ] **Precision** — citations include equation numbers where applicable — 引用精确到公式编号

---

## Available Textbook Sources (可用教科书来源)

See `learning-math_foundations` SKILL.md §Available Textbook Sources for the complete list.

Key references:

| Key            | Book                             | Path                                                   |
| -------------- | -------------------------------- | ------------------------------------------------------ |
| **MML**        | Mathematics for Machine Learning | `textbooks/math/_sources/mml_sections/`       |
| **Murphy**     | Probabilistic ML (PML1)          | `textbooks/ml/_sources/murphy_pml1_sections/` |
| **Goodfellow** | Deep Learning                    | `textbooks/ml/_sources/goodfellow_sections/`  |
| **Bishop**     | Pattern Recognition and ML       | `textbooks/ml/_sources/bishop_sections/`      |

---

## How to Search for Sources (如何查找来源)

### Step 1 — BM25 优先（必须先做）

**Always use BM25 retrieval first** before grep or manual lookup.
BM25 定位到章节，再用 grep 验证内容。

```bash
# BM25 keyword search — 关键词检索定位章节
uv run python retrieval_lab/scripts/run_query.py --book goodfellow --method bm25 "pooling translation invariance" --top-k 5
uv run python retrieval_lab/scripts/run_query.py --book murphy_pml1 --method bm25 "multiclass logistic regression maximum likelihood" --top-k 5
uv run python retrieval_lab/scripts/run_query.py --book manning_ir --method bm25 "precision recall F1" --top-k 5
```

**Available book keys (available BM25 indexes):**

| Key | Book |
|-----|------|
| `goodfellow` | Goodfellow *Deep Learning* |
| `murphy_pml1` | Murphy *PML1* |
| `murphy_pml2` | Murphy *PML2* |
| `mml` | Deisenroth *MML* |
| `bishop` | Bishop *PRML* |
| `esl` | Hastie *ESL* |
| `isl` | James *ISLR* |
| `eisenstein` | Eisenstein *NLP* |
| `jurafsky` | Jurafsky *SLP3* |
| `hamilton` | Hamilton *GRL* |
| `sutton` | Sutton *RL* |
| `grinstead` | Grinstead *Probability* |
| `mackay` | MacKay *Information Theory* |

### Step 2 — grep 验证（BM25 定位后）

After BM25 returns candidate section numbers, use grep to confirm the exact heading and content:

BM25 返回候选章节号后，用 grep 确认标题和内容：

```bash
# Verify section heading — 验证章节标题（在 data/mineru_output/ 下）
# Example: confirm §9.3 is "Pooling" in Goodfellow
grep_search pattern="^# 9\.3" in goodfellow_deep_learning .md
```

### Step 3 — Fallback（BM25 无结果时）

Only if BM25 returns nothing relevant:

```bash
# Topic index fallback — 主题索引备选
cat textbooks/topic_index.json | python -m json.tool | Select-String "bayes"
```
