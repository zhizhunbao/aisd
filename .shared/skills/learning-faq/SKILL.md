---
name: learning-faq
description: Generate Chinese-first FAQ files for a topic. Use when the user wants common confusions, short clarifications, practical distinctions, or a compact Q&A style explanation layer.
---

# Learning FAQ

## Purpose

Generate:

- `courses/{course}/notes/{topic_key}_faq.md`

Naming convention:

- `topic_key` should use `讲次_主题`, for example `lecture9_transformer`

This file collects high-frequency confusion points in Q&A form.

## Language

- Chinese first
- English only for term names

## Inputs

Use:

- `{topic_key}_slides.md`
- `{topic_key}_storyline.md`
- `{topic_key}_concepts.md`
- quizzes and labs when relevant

## Required Structure

```markdown
# [Topic] 常见问题

## 1. 概念区别
## 2. 为什么需要它
## 3. 公式/机制相关疑问
## 4. 实现与应用疑问
```

Each entry should look like:

```markdown
### Q: 为什么 X 不是 Y？
A: ...
```

## Rules

- Questions must reflect real confusion, not textbook headings
- Answers should be short, direct, and Chinese-first
- Prefer contrastive explanations
- Good FAQ entries should reduce repeated future explanation work
