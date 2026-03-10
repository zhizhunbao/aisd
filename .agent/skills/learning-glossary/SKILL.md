---
name: learning-glossary
description: Generate Chinese-first topic glossaries. Use when the user wants unified term definitions for a topic, consistent wording across files, or a dedicated glossary file for fast term lookup.
---

# Learning Glossary

## Purpose

Generate:

- `courses/{course}/notes/{topic}_glossary.md`

This is a topic-level glossary, not the global reusable library.

## Language

- Chinese definition first
- English term in parentheses

## Inputs

Use:

- `{topic}_slides.md`
- `{topic}_storyline.md`
- `{topic}_concepts.md`
- `concept-glossary` resources when useful

## Required Structure

```markdown
# [Topic] 术语表

## A-Z / 按主题分组

### 术语名 (English Term)
- **定义：**
- **本讲里的作用：**
- **不要和什么混淆：**
- **出现在哪些文件：**
```

## Rules

- Keep definitions short and consistent
- Prefer one canonical Chinese translation per term
- Explicitly mark near-synonyms and common confusions
- Link each term to the files where it appears

