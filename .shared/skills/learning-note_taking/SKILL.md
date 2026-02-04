---
name: learning-note_taking
description: Add concise study notes to lecture materials. Use when (1) user asks to add notes to extracted PDFs/slides, (2) mentions "笔记" or "notes", (3) organizing course content.
---

# Learning Note-Taking

## Objectives

Add brief, practical notes in Chinese to lecture materials with minimal code examples.

## Instructions

### 1. Workflow

Before adding notes, follow these steps to ensure logical placement:

1. **Analyze Structure**: Identify every individual step, sub-section, or task (even small ones).
2. **Determine Locations**: Identify the end of *every* logical step or task.
3. **Insert Placeholders**: Add `> [Add your notes here]` after *every single task or sub-step*.
4. **Final Fill**: Review the content around each placeholder and replace it with notes following the structure below.

### 2. Keep Notes Concise

- Focus on key concepts only
- **Line-by-Line Correspondence**: 必须依序解释 `Text Content` 中的每一项内容（每一行、每一个 bullet point、每一个公式）。
- **Image Interpretation**: 解释 `Page Image` 中的关键视觉元素（如图表、流程图、逻辑框图），确保笔记覆盖图片中传达的逻辑。
- 2-4 bullet points per concept
- Short code snippets (5-10 lines max)
- Avoid lengthy explanations
- **Use Chinese only** (no English/bilingual)
- **Only summarize existing content** - do not add external knowledge or examples

### 3. Note Structure

For each section requiring notes, wrap the entire content in a blockquote (`>`) to distinguish it from the original material:

```markdown
> **📝 笔记:**
> 
> **概念名称:**
> 
> - 简短定义（1-2句）
> - 关键点（2-3个要点）
> - 简单示例（如适用）
> 
> **💡 提示:** 实用技巧或注意事项
```

### 3. Language Rules

- All text in Chinese
- Technical terms: keep English in parentheses, e.g., "主成分分析 (PCA)"
- Code comments in Chinese
- Keep code variable names in English

### 4. What to Include

- ✅ 核心定义（基于原文）
- ✅ **逐行/逐项解释**（覆盖所有文本要点）
- ✅ **图片内容解析**（覆盖视觉图表逻辑）
- ✅ 关键区别/对比（如原文提到）
- ✅ 实用技巧（原文中的提示）
- ✅ 常见错误（原文中的注意事项）
- ✅ **作业提交要求**（如截图、文件命名、提交格式等）
- ❌ 避免：冗长教程、额外示例、原文没有的内容、拓展知识

### 5. Submission Requirements (Important!)

When original content mentions submission requirements, ALWAYS include them in notes:

- Screenshot instructions (e.g., "截图保存到Lab1.docx")
- File naming conventions (e.g., "命名为lab1_zipf_law.ipynb")
- Folder structure (e.g., "创建lab1文件夹")
- Submission format (e.g., "压缩为lab1.zip上传")
- Due dates and platforms (e.g., "上传到Brightspace")

**Format:**

```markdown
**提交要求:**

- 截图：运行结果截图保存到Word文档
- 文件命名：lab1_zipf_law.ipynb
- 文件夹：创建lab1文件夹，包含代码和文档
- 提交：压缩为lab1.zip上传到Brightspace
```

## Examples

**Example 1: Basic Concept**

```markdown
**📝 笔记:**

**Conda环境:**

- 独立的Python运行空间，避免依赖冲突
- 建议为每个项目创建独立环境
- 常用命令: `conda create -n name`, `conda activate name`

**💡 提示:** 避免在base环境安装过多库
```

**Example 2: With Submission Requirements**

```markdown
**📝 笔记:**

**测试代码:**

- 运行`brown.words()`查看语料库
- 退出Python：输入`exit()`

**提交要求:**

- 截图：运行结果截图保存到Lab1.docx
- 每个测试步骤都需要截图
```
