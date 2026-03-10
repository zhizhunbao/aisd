---
name: learning-exercise
description: Generate Chinese-first exercise files for a topic. Use when the user wants understanding-oriented practice, not just quiz items, including reasoning questions, concept application, derivation prompts, and small implementation tasks.
---

# Learning Exercise

## Purpose

Generate:

- `courses/{course}/notes/{topic}_exercise.md`

This file is for practice and consolidation, not just quick testing.

## Language

- Chinese first
- English only for term names, formulas, and code identifiers

## Inputs

Use:

- slides
- storyline
- concepts
- math
- code

## Required Structure

```markdown
# [Topic] 练习

## 1. 概念题
## 2. 对比题
## 3. 推理题
## 4. 公式/推导题
## 5. 代码理解题
## 6. 开放延伸题
```

## Rules

- Prefer questions that reveal understanding gaps
- Include answer outlines or key points when requested
- Separate “会背” from “会用”
- Good exercises should map back to concepts, formulas, and code

