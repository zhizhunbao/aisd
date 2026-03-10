---
name: learning-map
description: Generate a Chinese-first learning map for a topic. Use when the user wants a navigation file that shows where the topic fits, what depends on what, which files to read, what is missing, and how to study without getting lost.
---

# Learning Map

## Purpose

Generate a topic-level navigation file:

- `courses/{course}/notes/{topic}_map.md`

This file is not for teaching every concept in detail. It is for answering:

- 我现在在学什么
- 这讲在整门课里的位置
- 先看什么，后看什么
- 已经有哪些材料
- 还缺什么材料

## Language

- Main body must be Chinese
- English only for term names or file names when necessary

## Inputs

Cross-check available files such as:

- `{topic}_slides.md`
- `{topic}_storyline.md`
- `{topic}_concepts.md`
- `{topic}_math.md`
- `{topic}_code.md`
- `{topic}_tutorial.md`

## Required Structure

```markdown
# [Topic] 学习地图

## 1. 核心问题
## 2. 全景位置
## 3. 依赖地图
## 4. 文件地图
## 5. 学习路线
## 6. 缺口检查
```

## Rules

- Optimize for navigation, not coverage
- Make dependencies explicit
- Explain file roles clearly
- Call out missing artifacts directly
- Prefer “第一次学习 / 复习 / 做作业” three study routes when useful

