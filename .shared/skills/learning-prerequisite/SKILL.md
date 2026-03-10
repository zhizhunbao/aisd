---
name: learning-prerequisite
description: Generate Chinese-first prerequisite files for a topic. Use when the user needs to know what must be understood before learning the current topic, what missing background will block progress, and how to fill those gaps.
---

# Learning Prerequisite

## Purpose

Generate:

- `courses/{course}/notes/{topic_key}_prerequisite.md`

Naming convention:

- `topic_key` should use `讲次_主题`, for example `lecture9_transformer`

This file identifies the minimum background required to learn the topic successfully.

## Language

- Chinese first
- English only for technical term names

## Inputs

Use:

- `{topic_key}_slides.md`
- `{topic_key}_storyline.md`
- `{topic_key}_concepts.md`
- related earlier lecture files if needed

## Required Structure

```markdown
# [Topic] 前置知识

## 1. 为什么需要这些前置
## 2. 必要前置概念
## 3. 最小会用清单
## 4. 常见卡点
## 5. 补课顺序
```

## Rules

- Separate “必须会” from “最好会”
- Explain each prerequisite in one short Chinese paragraph
- State what breaks if the prerequisite is missing
- Prefer ordering prerequisites from foundational to topic-specific
