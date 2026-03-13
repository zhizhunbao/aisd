---
name: learning-history
description: Generate Chinese-first topic history files. Use when the user wants the evolution path behind a concept, how older methods led to newer ones, and why a topic appeared historically.
---

# Learning History

## Purpose

Generate:

- `courses/{course}/notes/{topic}_history.md`

This skill is generic topic history. If the repo already has a narrower skill such as `learning-lecture-history`, that more specific skill can still be used when appropriate.

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

## 🎬 序幕：一切从什么问题开始？

[定义核心问题，为什么这个问题值得几十年努力]

## 1. 历史问题起点

[第一个被提出的问题/需求，以及当时的背景]

## 2. 旧方法及其局限

[每一个旧方法，都必须以"但还有一个问题……"结尾，暴露其局限]

> 🔑 **故事转折点：** [旧方法局限] → 我们需要[新方法的核心能力]

## 3. 新方法如何出现

[新方法怎么解决了旧方法的问题，以及它又带来什么新问题]

## 4. 关键节点时间线

[ASCII 路线图 + 过渡对比表]

## 5. 今天为什么还要学它

[现代系统哪里还在用它，理解此历史对学习后续内容有何帮助]

## 📝 复习重点检查清单

- [ ] 能解释为什么需要[技术X]，它解决了[技术Y]的什么问题？
- [ ] 知道[关键人物]的贡献？
- [ ] 能说出每个技术演进步骤的核心动机？
- [ ] 今天的系统在哪里用到了这段历史遗产？
```

## Rules

- Focus on "为什么会出现这个概念"
- Organize by historical evolution, not slide order
- **每个技术节点必须以"但还有一个问题……"结尾，暴露局限，引出下一步**
- **每两个相邻节点之间必须有 `🔑 故事转折点` 标记**
- **文末必须包含 `## 📝 复习重点检查清单`，`- [ ]` 格式**
- 文末 `## 4. 关键节点时间线` 必须包含 ASCII 路线图

## 因果链写作模板（P→S Arc）

每个技术节点的写法：

```markdown
### [技术名]（[年份]）

[介绍这个技术做了什么，解决了什么问题]

**但还有一个问题……**

[暴露这个技术的局限，越具体越好]

> 🔑 **故事转折点：** [局限一句话总结] → 需要[下一步核心能力]
```

## 四层递进解释（用于解释核心概念）

对每个关键技术/概念，使用四层递进：

| 层次 | 说明 | 示例 |
|------|------|------|
| ① 一句话定义 | 最通俗的描述 | "LeNet = 卷积 + 反向传播的结合" |
| ② 原理/公式 | 精确的技术描述 | 结构图或核心公式 |
| ③ 具体例子 | 课程/现实中的案例 | "被美国邮政用于读取支票" |
| ④ 类比/记忆技巧 | 生活化比喻 | "卷积核就像放大镜，扫过图像找模式" |

> 💡 详细写法参考 `learning-lecture-storyline` skill §3.2 四层递进法
