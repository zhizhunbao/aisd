---
name: code-comment
description: 中英文双语代码注释规范。Use when (1) 为代码添加注释, (2) 需要中英双语文档, (3) 规范化代码注释格式, (4) 学习类项目代码注释
---

# Code Comment (Bilingual)

## Objectives

- Add bilingual (Chinese & English) comments to code
- Follow consistent comment formatting rules
- Explain complex logic with reasons
- Maintain clear code documentation

## Comment Rules Overview

| Location                      | Language          | Format                                      |
| ----------------------------- | ----------------- | ------------------------------------------- |
| File-level docstring          | English only      | Standard docstring                          |
| Code block divider            | Chinese + English | 60 '=' separator with bilingual title       |
| Function docstring            | Chinese + English | Two-line format: Chinese line, English line |
| Method/Function Documentation | Bilingual         | Box-style Header ABOVE definition           |
| Inline comments               | Chinese + English | Chinese line, English line, above code      |
| Algorithm/Concept comments    | Chinese + English | Structured template: 定义/公式/举例/优点    |
| Step Output                   | English           | print_step usage for formatted I/O          |

## 1. File-level Docstring (English Only)

```python
"""
Lab 2: Q-Learning Agent for Cliff Walking
Student ID: 041107730
Implements Q-Learning using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
Modified from Hybrid Activity 1 to solve the Cliff Walking problem.
"""
```

## 2. Code Block Dividers (60 Characters)

Use exactly 60 '=' characters to separate major logical sections (Steps, Phases, Modules). Includes a bilingual title.

```python
# ============================================================
# 步骤 1：数据加载与预处理
# Step 1: Data Loading and Preprocessing
# ============================================================
```

**Rules:**

- Exactly 60 '=' characters.
- Chinese title first, then English title.
- Placed between major logical blocks.
- One blank line before and after the divider (except at the very start of file).
- All step dividers are at the **top level** of the script (no `main()` wrapper).

**Flat sequential example:**

```python
# ============================================================
# 步骤 1：数据加载
# Step 1: Data Loading
# ============================================================

# [Bilingual comments + code]
df = pd.read_csv('data.csv')

# ============================================================
# 步骤 2：数据预处理
# Step 2: Data Preprocessing
# ============================================================

# [Bilingual comments + code]
df = preprocess(df)
```

## Comment Checklist

Before finishing:

- [ ] File-level docstring is English only
- [ ] All function docstrings use two-line format: Chinese first line, English second line
- [ ] All inline comments have Chinese line immediately followed by English line
- [ ] Comments are placed ABOVE code, not beside it
- [ ] No blank line between Chinese and English lines (in both docstrings and comments)
- [ ] Blank line between each code block
- [ ] Complex logic has explanation and reason
- [ ] API parameters explain what each value does, not just its name
- [ ] EVERY single line of code has a bilingual comment above it
- [ ] Import statements have bilingual comments
- [ ] **Box-style class headers ABOVE all class definitions**
- [ ] **Dividers are exactly 60 characters long**
- [ ] **Every step uses 60-char `=` dividers at top level (not plain comments)**
- [ ] **No scientific notation (use decimal 0.001 instead)**
- [ ] No magic numbers — all meaningful numeric literals are named constants
- [ ] **Algorithm/Concept comments use structured template** (定义/公式/举例/优点)

## Quick Reference

```python
# File docstring (English only)
"""
Lab 2: Q-Learning Agent
Implements Q-Learning algorithm
"""

# Function docstring (two-line bilingual)
def train(env):
    """训练Q-Learning智能体
    Train Q-Learning agent"""

# Inline comment (line-by-line bilingual, above code)
# 初始化Q表，使用随机值
# Initialize Q-table with random values
qtable = [[random.random() for _ in range(env.actions())] for _ in range(env.states())]

# 增加步数计数
# Increment step count
steps += 1
```

## Key Rules Summary

1. **Function docstrings**: Two lines - Chinese first line, English second line (NO blank line between)
2. **Inline comments**: Chinese line, English line, then code (NO blank line between Chinese/English)
3. **Comment placement**: Always ABOVE code, never beside it
4. **Code spacing**: Blank line after each code block
5. **No blank line**: Between Chinese and English lines (both in docstrings and comments)
6. **API parameters**: Explain what each value DOES and WHY, not just restate parameter names
7. **No magic numbers**: All meaningful numeric literals must be named constants (UPPER_SNAKE_CASE)
8. **Flat sequential style**: All code runs top-to-bottom, no `main()` wrapper — step dividers are at the top level

<!-- Detailed content moved to references/comment_templates.md -->

> 📖 See [references/comment_templates.md](references/comment_templates.md) for detailed content on the following topics:
> - ## 2.1 Algorithm/Concept/Math
> - ## 2. Function Docstring
> - ## 3. Inline Comments
> - ## 4. Code Spacing
> - ## 5. Complex Logic
> - ## 6. API Parameter
> - ## 7. Import Comments
> - ## 10. Environment Setup
> - ## 9. No Magic Numbers
> - ## Complete Example
