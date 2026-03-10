---
name: learning-history
description: Generate Chinese-first topic history files. Use when the user wants the evolution path behind a concept, how older methods led to newer ones, and why a topic appeared historically.
---

# Learning History

## Purpose

Generate:

- `courses/{course}/notes/{topic}_history.md`

This skill is generic topic history. If the repo already has a narrower skill such as `learning-lecture_history`, that more specific skill can still be used when appropriate.

## Language

- Chinese first
- English only for paper names, method names, and dates when useful

## Inputs

Use:

- current topic files
- earlier related lecture/topic files
- references when needed

## Required Structure

```markdown
# [Topic] 历史线

## 1. 历史问题起点
## 2. 旧方法及其局限
## 3. 新方法如何出现
## 4. 关键节点时间线
## 5. 今天为什么还要学它
```

## Rules

- Focus on “为什么会出现这个概念”
- Organize by historical evolution, not slide order
- Make each step answer which limitation triggered the next step

