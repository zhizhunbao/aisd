---
name: learning-tutorial-notebook
description: Write tutorial/demo .py scripts and convert to .ipynb notebooks. Use when (1) user wants to create a visual tutorial notebook, (2) user mentions "教程" or "tutorial" with notebook, (3) needs to fix or regenerate a broken .ipynb from .py source, (4) user says "格式不对" on a .ipynb file.
---

# Tutorial Notebook Skill

## Purpose

Write tutorials as **plain `.py` files** (the source of truth), then convert to `.ipynb` notebooks.
This avoids JSON formatting issues that plague direct `.ipynb` editing (unescaped quotes, etc.).

## .py Tutorial Format Convention

Use the **jupytext percent format** — a well-established standard recognized by VS Code, Jupyter, and jupytext:

```python
# %% [markdown]
"""
# 📐 Tutorial Title

> Description here.

**Dependencies**: `pip install numpy matplotlib`
"""

# %%
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (8, 6)
print('✅ Setup complete!')

# %% [markdown]
"""
---

## 1. Section Title

**Key insight**: Explanation with **bold**, *italic*, and math: $Ax = b$

| Column A | Column B |
|----------|----------|
| value1   | value2   |
"""

# %%
# Code for section 1
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_title('Section 1 Demo')
plt.show()

# %%
# Numerical verification
print('Result:', 2 + 2)

# %% [markdown]
"""
---

## 2. Next Section

More explanation here.
"""

# %%
# Code for section 2
print('Hello from section 2!')
```

### Format Rules

1. **`# %% [markdown]`** followed by a `"""..."""` block → becomes a **Markdown cell**
2. **`# %%`** (without `[markdown]`) → starts a new **Code cell**
3. Everything between cell markers belongs to that cell
4. The file is valid Python and can be run directly with `python tutorial.py`
5. **DO NOT** put unescaped special characters in markdown — this is Python, so `"""` strings must not contain unmatched `"""`
6. Use `「」` or `'...'` instead of `"..."` inside markdown strings to avoid quote issues
7. Keep `%matplotlib inline` out — use `plt.show()` instead (works in both .py and .ipynb)

### Template

A minimal template:

```python
# %% [markdown]
"""
# Tutorial Title

> Brief description.

**Dependencies**: `pip install numpy matplotlib`
"""

# %%
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
"""
---

## 1. First Concept

Explanation here.
"""

# %%
# Demo code
print('Hello!')
```

## How to Convert .py → .ipynb

### Method 1: Custom Script (Recommended — No extra dependencies)

```bash
python .agent/skills/learning-tutorial_notebook/scripts/py_to_notebook.py <input.py> [output.ipynb]
```

This script:
- Parses `# %%` and `# %% [markdown]` markers
- Creates proper markdown and code cells
- Validates JSON output
- Handles Chinese characters correctly
- No dependencies beyond Python stdlib + nbformat

### Method 2: jupytext (If installed)

```bash
pip install jupytext
jupytext --to notebook tutorial.py
```

## Workflow

### Creating a new tutorial

1. **Plan** the tutorial structure (sections, concepts, demos)
2. **Create** the `.py` file using the format convention above
3. **Test** by running `python tutorial.py` to verify all code works
4. **Convert** to `.ipynb` using the conversion script
5. **Verify** the notebook opens correctly in VS Code / Jupyter

### Fixing a broken .ipynb

1. **Check** if a `.py` source file exists alongside the `.ipynb`
2. If yes: fix issues in the `.py` file, then re-convert
3. If no: the `.ipynb` likely has JSON issues (unescaped quotes, etc.)
   - Create a `.py` version manually or extract from the broken `.ipynb`
   - Then convert back to `.ipynb`

### Common .ipynb JSON Issues

| Problem | Cause | Prevention |
|---------|-------|------------|
| `Expected ',' or ']'` | Unescaped `"` in JSON string | Write in .py, convert |
| Chinese garbled | Wrong encoding | Always use UTF-8 |
| Notebook won't open | Malformed JSON | Validate with `python -m json.tool` |

## Generating Tutorial Content Guidelines

When generating tutorial `.py` content:

1. **Structure**: Title → Setup → Section 1 → Section 2 → ... → Summary
2. **Each section**: Markdown explanation → Code demo → Optional verification
3. **Markdown cells**: Use tables, math, blockquotes, emoji for rich content
4. **Code cells**: Keep focused, one concept per cell, always `plt.show()`
5. **Bilingual**: Support Chinese + English headers when appropriate
6. **Quotes in markdown**: Use `「」` for Chinese quotes, avoid bare `"` inside `"""`

## Validation

After conversion, verify:

- [ ] `.ipynb` opens without errors in VS Code
- [ ] All markdown cells render correctly
- [ ] All code cells execute without errors
- [ ] Plots display inline
- [ ] Chinese characters display correctly
- [ ] JSON is valid: `python -c "import json; json.load(open('file.ipynb'))"`
