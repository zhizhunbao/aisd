---
name: learning-bridge
description: Generate Chinese-first bridge files between topics. Use when the user wants to know how one lecture leads into the next, which concepts are reused, what changes in the next topic, and how to avoid knowledge discontinuity.
---

# Learning Bridge

## Purpose

Generate:

- `courses/{course}/notes/{topic}_bridge.md`

This file explains how the current topic connects backward and forward.

## Language

- Chinese first
- English only for term names

## Inputs

Use:

- current topic files
- previous topic files
- next topic files if available

## Required Structure

```markdown
# [Topic] 衔接桥

## 1. 它承接了什么
## 2. 它新增了什么
## 3. 它会通向什么
## 4. 最容易断层的地方
## 5. 过渡学习建议
```

## Rules

- Make transitions explicit
- Focus on reused concepts and changed assumptions
- Good bridge files should reduce “上一讲懂了，这一讲突然断掉”的感觉

