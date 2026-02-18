---
name: learning-code_generation
description: Generate Python code and Jupyter notebooks for course assignments. Use when (1) user asks to generate code for lab/assignment, (2) mentions "生成代码" or "generate code", (3) needs to create .py or .ipynb files for coursework.
---

# Learning Code Generation

## Objectives

Generate well-structured, self-documenting Python code for course assignments that meets academic requirements.

## Instructions

### 1. Understand Requirements

Before generating code:

- Read assignment document thoroughly
- Identify all required steps and their order
- Note submission requirements (file format, naming, structure)
- Check for instructor-specific code style requirements

### 2. Code Structure

**Student Information:**

Read student information from `.env.local` in workspace root:

- `NAME` - Student name
- `NUMBER` - Student number
- `EMAIL` - Student email (optional)

Use `python-dotenv` to load environment variables at the start of the script.

**For Python scripts (.py):**

**⚠️ RULE: Flat Sequential Style (No `main()` function)**

All lab code MUST be written as flat, sequential ("spaghetti") code that runs top-to-bottom. Do NOT wrap code in a `main()` function or `if __name__ == "__main__"` block. Do NOT create an `initialize_lab()` function. This produces code that looks more natural and student-written.

```python
"""
CST8508 Lab 4: Streaming Live Webcam Video with Timestamp Overlay
Author: Peng Wang
Student Number: 041107730

[Lab description]
"""

# 导入OpenCV库
# Import OpenCV library
import cv2

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

RANDOM_STATE = 42
OUTPUT_DIR = 'lab4_images'

# ============================================================
# 步骤 1：数据加载
# Step 1: Data Loading
# ============================================================

# [Bilingual comments + code here]
df = pd.read_csv('data.csv')

# ============================================================
# 步骤 2：数据预处理
# Step 2: Data Preprocessing
# ============================================================

# [Bilingual comments + code here]
X = df.drop('target', axis=1)
```

**⚠️ RULE: Step Dividers**

Every step MUST use 60-char `=` dividers with bilingual titles at the top level — **not** plain inline comments.

❌ **BAD** — plain comments without dividers:

```python
# 步骤 1：数据加载
# Step 1: Data loading
df = load_data("data.csv")
```

❌ **BAD** — wrapping in `main()`:

```python
def main():
    df = load_data("data.csv")

if __name__ == "__main__":
    main()
```

### 3. Output Formatting Requirements

**⚠️ PRINCIPLE 1: Raw Data Integrity**

When printing datasets or statistics, **always show the original form of the data**.

- **No Internal Mapping**: Never map numeric labels (e.g., `0, 1`) to string names (e.g., `class_0`) inside the script for the "Statistics" step.
- **Show Objects As-Is**: Display data exactly as it looks after loading. Do not "beautify" or alter original values.
- **Raw Means Clean**: The most professional output is one that accurately reflects the raw state of the dataset.

**⚠️ PRINCIPLE 2: Concise and Aligned Output**

- **Header Format**: Use exactly 60 '=' characters above and below the step title.
  ```python
  # ============================================================
  # Step N: Step Title
  # ============================================================
  ```
- **Avoid Truncation**: Use `pd.set_option('display.max_columns', None)`, `pd.set_option('display.width', 1000)`, and `pd.set_option('display.expand_frame_repr', False)` to ensure all data columns are visible in a single block.
- **Overwrite Policy**: All operations (executing scripts, capturing output, generating screenshots) should **directly overwrite** existing files. Do not use temporary or numbered filenames.
- **Verification First**: Always run the script and verify the console output (saved to `output.txt`) BEFORE generating screenshots.

**Example of Precise Output:**

```python
# ✅ GOOD - Precision for "Step 2: Dataset Statistics"
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)

print("=" * 60)
print("Step 2: Print dataset statistics")
print("=" * 60)
print(f"Number of instances: {X.shape[0]}")
print(f"Number of attributes: {X.shape[1]}")
print(df.head())
```

**Do NOT include:**

- Over-design: No complex tables if simple DataFrame print is enough.
- Redundant info: Don't print stats in the "Load" step.
- Truncated output: Ensure all columns are shown.
- Mismatched headers: Always 60 '='.

```python
# ❌ BAD - Results as raw arrays
print(f"Accuracy: {accuracy}")
print(f"Confusion Matrix: {cm}")

# ✅ GOOD - Formatted results table
from tabulate import tabulate

print("Step 10: Results table with accuracies and confusion matrices")
print("-" * 40)
results_table = []
for name, acc, cm in results:
    results_table.append([name, f"{acc:.4f}", str(cm.tolist())])

headers = ["Model", "Accuracy", "Confusion Matrix"]
print(tabulate(results_table, headers=headers, tablefmt="simple"))
```

**Required Dependencies for Formatted Output:**

```python
from tabulate import tabulate  # For formatted tables
import pandas as pd            # For DataFrame display
```

**⚠️ PRINCIPLE 3: Environment Setup at Top**

All environment-related setup (dotenv, pandas options, directory creation) should be placed at the top of the script, right after imports and constants. Do NOT wrap them in a function.

- **Top-level Constants**: `RANDOM_STATE`, `OUTPUT_DIR`, `LINE_WIDTH`, etc. as `UPPER_SNAKE_CASE` constants.
- **Top-level Setup**: `load_dotenv()`, `pd.set_option()`, `os.makedirs()` etc. placed inline after constants.

**⚠️ PRINCIPLE 4: Parameter Documentation (Critical for ML Assignments)**

Professors require explicit explanation of EVERY parameter — even defaults. For each classifier/algorithm parameter set, document:

1. **What the parameter controls** (e.g., "C controls regularization strength")
2. **Why this value was chosen** (e.g., "default balance between bias and variance")
3. **Effect of changing it** (e.g., "higher C = tighter margins, risk of overfitting")

This applies to BOTH the code comments AND the Answer Document's Discussion sections.

**In Code Comments:**

```python
# 三组kNN参数配置
# Three sets of kNN parameter configurations
knn_configs = [
    # k=3: 小k捕捉局部模式，可能对噪声敏感
    # k=3: Small k captures local patterns, may be sensitive to noise
    (KNeighborsClassifier(n_neighbors=3, weights='uniform', metric='euclidean'),
     "k=3, weights=uniform, metric=euclidean"),
]
```

**In Answer Document Discussion:**

```markdown
- **Set 1: k=3, weights=uniform, metric=euclidean** — Uses 3 nearest neighbors
  with equal voting weight and Euclidean distance. Small k captures local
  patterns but may be sensitive to noise.
```

**When using defaults, still explain them:**

```python
# ✅ GOOD - Document default parameters
print(f"SVM with Linear kernel")
print(f"  C (regularization): 1.0 (default)")
print(f"  - Higher C = less regularization, may overfit")
print(f"  - Lower C = more regularization, may underfit")
```

**For Jupyter Notebooks (.ipynb):**

- First cell: Code to load student info from `.env.local` and print header
- Second cell: Markdown with title, author info (using variables), date
- Each step: Markdown cell + Code cell
- Final cell: Submission reminder (if needed)

**For detailed structure examples:** See `.agent/skills/learning-code_generation/references/structure-examples.md`

### 3. Core Principles

**Self-Documenting Code:**

- Use clear, descriptive variable names
  **Absolutely No Magic Numbers:**
- All numeric literals with domain meaning (thresholds, sizes, ratios, limits) MUST be extracted to named constants.
- Constants should be defined in the `Configuration Constants` section using `UPPER_SNAKE_CASE`.
- Only trivially obvious values (0, 1, -1, 2 for halving/doubling) may remain inline.
- Structure code to reveal intent.
- **Scientific Notation**: Use decimal forms (e.g., `0.001`, `0.0003`) instead of scientific notation (e.g., `1e-3`, `3e-4`). Add a comment explaining the value and its role (e.g., "controls the step size of weight updates").

**Function Usage:**

- **No `main()` function** — all code runs top-to-bottom at module level
- **No `initialize_lab()`** — setup code placed inline at the top
- Only create functions when code is genuinely repeated (DRY principle)
- Don't create functions for one-time operations
- Keep program flow flat, readable, and sequential

**Comments (Bilingual):**

Follow `dev-code_comment` skill for bilingual comments:

- File docstring: English only
- Inline comments: Chinese line + English line above code
- Complex logic: Add reason (原因/Reason)
- API parameters: Explain what each value **does**, not just restate parameter names. For complex APIs (e.g., Stable-Baselines3, PyGame, OpenCV), define how each argument affects the algorithm or visualization.

Example:

```python
# 使用StandardScaler标准化数据
# Use StandardScaler to standardize data
# 原因：SVM对特征尺度敏感
# Reason: SVM is sensitive to feature scales
scaler = StandardScaler()

# 参数：127 是明暗分界线（亮度 > 127 的像素变白，≤ 127 的变黑），
#       255 是"变白"后赋予的像素值（纯白），
#       THRESH_BINARY 表示输出只有纯黑(0)和纯白(255)两种结果
# Parameters: 127 is the brightness cutoff (pixels > 127 become white, ≤ 127 become black),
#       255 is the value assigned to "white" pixels (pure white),
#       THRESH_BINARY means output has only two values: black(0) and white(255)
# 原因：二值化处理有助于提取目标轮廓
# Reason: Binarization helps extract object contours
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```

**Class Documentation:**

Always include a 60-character box header ABOVE class definitions:

```python
# ============================================================
# QLearningAgent: 封装有 Q-Table 及其更新法则的强化学习类
#                 Reinforcement learning class encapsulating Q-Table and its update rules
# ============================================================
class QLearningAgent:
    """封装有 Q-Table 及其更新法则的强化学习类
    Reinforcement learning class encapsulating Q-Table and its update rules"""
    ...
```

**Avoid AI Appearance:**

- No summary/conclusion sections at end
- No "Lab completed successfully!" messages
- No structured final summaries with statistics
- End with last required step + simple submission reminder

**For detailed principles and examples:** See `.agent/skills/learning-code_generation/references/code-principles.md`

### 4. Common Patterns

- Data Analysis: Import → Load → Preprocess → Analyze → Visualize
- Algorithm: Import → Define helpers → Implement → Test → Analyze
- Machine Learning: Import → Load → Engineer → Train → Evaluate → Visualize

**For pattern details:** See `.agent/skills/learning-code_generation/references/common-patterns.md`

### 5. Environment Setup

**Required Package:**

Ensure `python-dotenv` is available for loading `.env.local`:

```python
from dotenv import load_dotenv
import os

load_dotenv('.env.local')
STUDENT_NAME = os.getenv('NAME', '[Your Name]')
STUDENT_NUMBER = os.getenv('NUMBER', '[Your Student Number]')
```

**Date Formatting:**

Use `datetime` for current date:

```python
from datetime import datetime
current_date = datetime.now().strftime('%Y-%m-%d')
```

### 6. Language Requirements

**Bilingual Comments (Chinese + English):**

- Variable names: English
- Function names: English
- Comments: Chinese line first, then English line
- Docstrings: English only
- Print outputs: English

### 7. Screenshot Separation

**CRITICAL: Do NOT include internal logging or screenshot code in scripts.**

- **No Logger Classes**: Avoid defining `Logger` or `OutputCapture` classes in the coursework script.
- **Manual Redirection**: Use terminal redirection to capture `output.txt` for verification and screenshots.
  ```bash
  uv run python lab[n]_*.py > lab[n]_images/output.txt 2>&1
  ```

**Never include:**

- `OutputCapture` or `Logger` classes
- `save_code_screenshot()` functions
- `StringIO` or screenshot-related imports
- Any code that captures or redirects `stdout` internally

**Keep assignment code focused on:**

- Core analysis logic
- Data processing
- Visualization (using `plt.savefig()` for plots)
- Results output to terminal

**For screenshot generation:** Use the `learning-code_screenshot` skill separately.

### 8. Submission Reminder

**⚠️ IMPORTANT: Submission reminders are for debugging purposes ONLY.**

The reminder section should:

- Be placed at the very END of the script
- Be separated from the last step's output
- **NOT appear in output screenshots** (use `generate_output_screenshots.py` which captures step-by-step output, not the entire run)

```python
# Only print reminder after all steps are complete (debugging only)
print()
print("=" * 60)
print("Reminder:")
print("1. Take screenshots of code from Google Colab")
print("2. Paste screenshots into Lab1AnswerTemplate.md")
print("3. Fill in descriptions for each step")
print("4. Convert markdown to .docx for submission")
print("=" * 60)
```

**Note:** When generating output screenshots with `learning-code_screenshot` skill, each step's output is captured separately, so submission reminders won't appear in the screenshots.

## Validation

After generating code, check:

**Documentation:**

- [ ] File-level docstring with author info (English only)
- [ ] **No `main()` function** — code runs flat, top-to-bottom
- [ ] **No `initialize_lab()`** — setup code placed inline at top
- [ ] Concise function docstrings (two-line bilingual) for any helper functions
- [ ] Box-style function headers ABOVE definitions for parameters/returns (if functions exist)
- [ ] **Box-style class headers ABOVE class definitions** (if classes exist)
- [ ] **Dividers are exactly 60 characters long**
- [ ] **Every step uses 60-char `=` dividers at top level (not plain comments)**
- [ ] **No scientific notation (e.g., 1e-3 used); all replaced with 0.001 decimal style**

**Code Quality:**

- [ ] Meaningful, self-explanatory variable names
- [ ] **Absolutely NO magic numbers** (all meaningful numeric literals extracted to constants)
- [ ] All constants defined at top level as `UPPER_SNAKE_CASE`
- [ ] Minimal "why" comments above every single line of code

**Requirements:**

- [ ] Follows assignment step order exactly
- [ ] All required steps implemented
- [ ] No AI-generated appearance (summaries, conclusions)
- [ ] English language throughout
- [ ] **All algorithm parameters explained** (what it controls, why chosen, effect of changing)

**For detailed validation checklist:** See `.agent/skills/learning-code_generation/references/validation-guide.md`

## Workflow

1. Read assignment document
2. Identify all steps
3. Generate code following step order
4. Use self-documenting code practices
5. Add functions only for repeated operations
6. Include docstrings for functions
7. Add minimal "why" comments if needed
8. Add submission reminder (if appropriate)
9. Validate against checklist
10. Save to appropriate location

## Anti-Patterns

- ❌ Generating code without reading requirements
- ❌ **Wrapping code in `main()` or `initialize_lab()`** — use flat sequential style
- ❌ **Using `if __name__ == "__main__"`** — not needed for flat scripts
- ❌ Using Chinese comments or variable names
- ❌ Over-commenting obvious operations
- ❌ Creating functions for one-time operations
- ❌ Adding AI-generated summaries/conclusions
- ❌ Using meaningless variable names (x, y, data1)
- ❌ Not following assignment step order
- ❌ Hardcoding values that should be constants
- ❌ Including screenshot generation code (use `learning-code_screenshot` skill)
- ❌ Using ML algorithms without explaining parameter choices (what, why, effect)

**For more examples:** See `.agent/skills/learning-code_generation/references/code-principles.md`
