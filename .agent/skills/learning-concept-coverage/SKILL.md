---
name: learning-concept-coverage
description: Generate complete concept coverage files from slides, quizzes, and labs. Default output language is Chinese. Use when the user asks for all related concepts, concept整理, concept list, concept map, or when a workflow should produce comprehensive concepts instead of a compressed cheat sheet.
---

# Concept Coverage Generator

## Purpose

This skill generates a **complete concept file** for a topic.

Default writing language:

- Chinese first
- English only for term names, paper names, API names, or necessary terminology
- Do not write the document as an English outline with Chinese translation appended

Primary output:

- `courses/{course}/notes/{topic}_concepts.md`

Optional companion outputs when the workflow asks for them:

- `courses/{course}/notes/{topic}_math.md`
- `courses/{course}/notes/{topic}_code.md`

## Core Rule

This is **not** a cheat sheet.

Optimize for:

- coverage
- concept dependency clarity
- distinctions between similar terms
- links between concepts, formulas, and code

Do not optimize for printability or extreme compression.

## Inputs

Cross-check:

- `courses/{course}/notes/{topic}_slides.md`
- `courses/{course}/notes/{topic}_storyline.md` if available
- relevant quiz files
- relevant lab files

Priority:

1. slides
2. storyline
3. quizzes
4. labs

## Language Rules

- Main body must be in Chinese
- Section titles should be Chinese-first
- English terms may appear in parentheses
- Prefer “概念地图 / 依赖关系 / 易混点 / 应用出现位置” style organization

## Required Output Structure

```markdown
# [Topic] 概念全集

> 来源: slides + storyline + quizzes + labs
> 目标: 完整概念覆盖

---

## 1. 核心问题

## 2. 概念地图

## 3. 概念项

### 3.1 概念名 (English Term)
- **定义：**
- **为什么重要：**
- **和谁关联：**
- **常见混淆：**
- **相关公式/代码：**

## 4. 对比

## 5. 易混点与考点区分

## 6. 实际出现位置
```

## Coverage Rules

Include:

- core concepts
- supporting concepts
- prerequisites explicitly used in the lecture
- comparisons
- traps
- formula links
- code links

Exclude:

- admin/logistics
- deadlines
- grading policy

## Naming Rules

- create `{topic}_concepts.md`
- do not create `{topic}_cheatsheet.md` from this skill
