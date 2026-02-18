---
description: Prepare comprehensive midterm review materials from course slides, notes, labs, and quizzes
---

# 📝 期中复习准备工作流 (Midterm Review Preparation)

系统化地将课程的 slides、笔记、labs、quiz 整合为一套完整的期中复习材料。

## 🎯 使用方式

```
/midterm-review [课程] [选项]

示例:
/midterm-review mv                          # 完整流程
/midterm-review mv --weeks=1-5              # 指定复习范围
/midterm-review mv --from=phase2            # 从题库生成开始
/midterm-review mv --phase=4               # 只生成速查表
/midterm-review mv --phase=5               # 只做模拟测试
```

## 📋 完整流程概览

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: 范围分析 (Scope Analysis)                            │
│   ↓ 确定考试范围、收集所有材料                                   │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: 笔记整合 (Note Consolidation)                        │
│   ↓ learning-note_taking, dev-pdf_processing skills          │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: 题库构建 (Quiz Bank)                                 │
│   ↓ learning-quiz_generation, learning-quiz_note_taking      │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: 代码复习 (Code Review)                               │
│   ↓ learning-code_generation skill                           │
├─────────────────────────────────────────────────────────────┤
│ Phase 5: 速查表 (Cheat Sheet)                                 │
│   ↓ 综合 Phase 2-4 生成精简速查表                               │
├─────────────────────────────────────────────────────────────┤
│ Phase 6: 模拟测试 (Mock Exam)                                 │
│   ↓ learning-quiz_generation skill                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: 范围分析 📋

**目标**: 确定期中考试覆盖范围，盘点已有材料和缺失内容。

### 步骤

1. **检查课程计划**:
   - 读取 `courses/[course]/schedule/` 中的课程安排文件
   - 确定期中考试覆盖的周次/主题范围
   - 如果没有 schedule 文件，询问用户确认范围

2. **盘点已有材料**:
   ```
   检查以下目录的内容:
   courses/[course]/slides/         → 有哪些周的 PPT/PDF?
   courses/[course]/notes/          → 有哪些已生成的笔记?
   courses/[course]/quizzes/        → 有哪些已有的 quiz?
   courses/[course]/labs/           → 有哪些 lab 说明?
   courses/[course]/code/           → 有哪些已完成的代码?
   courses/[course]/textbook/       → 有哪些参考教材章节?
   courses/[course]/resources/      → 有哪些额外资源? (论文、补充笔记等)
   ```

   **⚠️ resources/ 目录特别注意**:
   - 可能包含老师提供的**补充阅读论文** (PDF)
   - 可能包含**额外的学习笔记** (.md)，如按周整理的补充材料
   - 这些内容可能出现在考试中，必须纳入复习范围
   - 论文需要提取摘要和核心概念，不必全文精读

3. **生成材料清单**:
   - 列出每个周次的材料完整度
   - 标注需要补充的内容（缺少笔记、缺少 quiz 等）
   - 输出为 `courses/[course]/notes/midterm_review_plan.md`

### 输出

- `courses/[course]/notes/midterm_review_plan.md` (复习计划和材料清单)

### 清单模板

```markdown
# [Course] Midterm Review Plan

## 考试范围: Week 1 - Week N

| Week | 主题 | Slides | Notes | Quiz | Lab | Code | Resources | 状态 |
|------|------|--------|-------|------|-----|------|-----------|------|
| 1    | ...  | ✅     | ❌    | ❌   | ✅  | ✅   | —         | 需补笔记 |
| 2    | ...  | ✅     | ✅    | ✅   | ✅  | ✅   | week2.md  | 完整 |
| ...  |      |        |       |      |     |      |           |      |

## 待补充项
- [ ] Week 1 笔记
- [ ] Week 3 Quiz
- ...
```

---

## Phase 2: 笔记整合 🧠

**Skills**: `learning-note_taking`, `dev-pdf_processing`, `dev-pptx_to_pdf`

**目标**: 确保每个考试范围内的主题都有完整的学习笔记。

### 步骤

1. **补充缺失笔记**: 对 Phase 1 中标记为缺失的周次，依次执行:

   a. **PPTX → PDF → Markdown 转换**:
   ```
   读取 skill: .shared/skills/dev-pptx_to_pdf/SKILL.md
   读取 skill: .shared/skills/dev-pdf_processing/SKILL.md
   将 slides/[topic].pptx → notes/[topic]_slides.md
   ```

   b. **生成结构化笔记**:
   ```
   读取 skill: .shared/skills/learning-note_taking/SKILL.md
   将 notes/[topic]_slides.md → notes/[topic]_notes.md
   ```

   c. **整合 resources/ 补充材料**:
   - 读取 `resources/` 中的 `.md` 补充笔记（如 `week2.md`），合并到对应周次的笔记中
   - 读取 `resources/` 中的 PDF 论文，提取摘要、核心概念和关键结论
   - 使用 `dev-pdf_processing` 处理论文 PDF
   - 标注哪些内容来自补充材料（区分于主 slides）

2. **整合为复习笔记**: 将所有周次的笔记合并为一份完整的复习文档:
   - 按主题/周次顺序组织
   - 每个主题包含: 核心概念、关键公式、重要术语
   - 添加跨主题的关联说明（如前续知识的联系）
   - 标注重点和难点

3. **审查笔记质量**:
   - 确保覆盖所有 slides 内容
   - 确保术语一致性
   - 确保公式完整且变量有解释

### 命令

// turbo

```
对每个缺失周次:
  读取 skill: .shared/skills/dev-pptx_to_pdf/SKILL.md       (如果是 PPTX)
  读取 skill: .shared/skills/dev-pdf_processing/SKILL.md     (转 Markdown)
  读取 skill: .shared/skills/learning-note_taking/SKILL.md   (生成笔记)
```

### 输出

- `courses/[course]/notes/[topic]_slides.md` (各周 slides 文本)
- `courses/[course]/notes/[topic]_notes.md` (各周笔记)
- `courses/[course]/notes/midterm_review_notes.md` (整合复习笔记)

---

## Phase 3: 题库构建 📚

**Skills**: `learning-quiz_generation`, `learning-quiz_note_taking`

**目标**: 汇总所有已有 quiz，补充笔记解释，生成额外练习题。

### 步骤

1. **整理已有 Quiz**:
   - 扫描 `courses/[course]/quizzes/` 中所有 quiz 文件
   - 检查每道题是否有 Answer + Explanation
   - 使用 `learning-quiz_note_taking` 补充缺少解释的题目

   ```
   读取 skill: .shared/skills/learning-quiz_note_taking/SKILL.md
   为已有 quiz 补充答案和解释
   ```

2. **生成新练习题**:
   - 基于 Phase 2 的笔记为每个主题生成额外练习题
   - 每个主题: 5-8 道 MCQ + 3-5 道 T/F + 1-2 道简答
   - 注重考察易混淆概念和跨主题联系

   ```
   读取 skill: .shared/skills/learning-quiz_generation/SKILL.md
   为每个主题生成练习题
   ```

3. **合并题库**:
   - 将老师的原始 quiz 和生成的练习题合并
   - 按主题分类整理
   - 标注题目来源（老师出题 vs 自生成）
   - 标注难度等级（基础 / 进阶 / 挑战）

### 输出

- `courses/[course]/quizzes/[topic]_quiz.md` (各主题练习题)
- `courses/[course]/quizzes/midterm_quiz_bank.md` (合并题库)

---

## Phase 4: 代码复习 💻

**Skill**: `learning-code_generation`

**目标**: 整理所有已完成的 lab 代码，提取核心概念的代码模式。

### 步骤

1. **盘点 Lab 代码**:
   - 扫描 `courses/[course]/code/` 和 `courses/[course]/labs/` 中的代码
   - 列出每个 lab 涉及的核心概念和 API

2. **提取代码速查**:
   - 从每个 lab 中提取关键代码片段
   - 为每个片段添加注释说明其作用和关键参数
   - 按主题组织代码速查

3. **生成核心概念代码总结**:
   按主题汇总关键代码模式:

   ```markdown
   ## [主题名] - 核心代码

   ### 关键 API
   - `cv2.GaussianBlur(src, ksize, sigmaX)`: 高斯模糊
   - `cv2.Canny(image, threshold1, threshold2)`: Canny 边缘检测
   - ...

   ### 代码片段
   ```python
   # [描述]
   [精简代码]
   ```

   ### 常见陷阱
   - [陷阱1]
   - [陷阱2]
   ```

4. **验证代码可运行**: 确保提取的关键代码片段独立可运行

### 命令

```
读取 skill: .shared/skills/learning-code_generation/SKILL.md
从 lab 代码提取核心模式
生成代码速查
```

### 输出

- `courses/[course]/notes/midterm_code_review.md` (代码复习文档)
- `courses/[course]/notes/midterm_code_snippets.py` (可运行的精简代码合集，可选)

---

## Phase 5: 速查表生成 📄

**目标**: 将 Phase 2-4 的内容精炼为 1-2 页的速查表。

### 步骤

1. **提取核心内容**:
   - 从每个主题的笔记中提取: 核心定义 + 关键公式 + 重要对比
   - 从题库中提取: 高频考点 + 易错点
   - 从代码复习中提取: 关键 API 和常见模式

2. **组织速查表结构**:

   ```markdown
   # [Course] Midterm Cheat Sheet

   ## 1. [主题1]
   **定义**: ...
   **公式**: $...$
   **vs [相关概念]**: [区别]
   **代码**: `api_call(param1, param2)`

   ## 2. [主题2]
   ...

   ## 关键对比
   | 概念A | 概念B | 区别 |
   |-------|-------|------|
   | ...   | ...   | ...  |

   ## 易错点
   - ⚠️ [易错点1]
   - ⚠️ [易错点2]

   ## 关键 API 速查
   | API | 用途 | 关键参数 |
   |-----|------|----------|
   | ... | ...  | ...      |
   ```

3. **精简和排版**:
   - 确保每个主题不超过 5-8 行
   - 使用表格和缩写提高信息密度
   - 公式使用标准 LaTeX 格式
   - 中英对照术语

### 输出

- `courses/[course]/notes/midterm_cheat_sheet.md` (速查表)

---

## Phase 6: 模拟测试 🎯

**Skill**: `learning-quiz_generation`

**目标**: 生成一套模拟期中考试，帮助自我评估。

### 步骤

1. **设计考试结构**:
   - 参考已有 quiz 的题型比例（MCQ / T/F / 简答）
   - 按主题权重分配题目数量
   - 确保覆盖所有考试范围内的主题

2. **生成模拟试卷**:
   - **选择题 (MCQ)**: 15-20 道，覆盖所有主题
   - **判断题 (T/F)**: 8-10 道，侧重易混淆概念
   - **简答/代码题**: 3-5 道，涵盖代码理解和概念解释
   - 难度分布: 基础 40% + 进阶 40% + 挑战 20%
   - **不重复**: 不得与 Phase 3 题库中的题目重复

3. **生成答案与评分标准**:
   - 每题附标准答案
   - MCQ/T/F 附解释（使用 `learning-quiz_note_taking` 格式）
   - 简答题附评分要点和示例答案

4. **导出两个版本**:
   - **试卷版**: 只有题目，无答案（用于自测）
   - **答案版**: 含完整答案和解释（用于对答案）

### 输出

- `courses/[course]/quizzes/midterm_mock_exam.md` (模拟试卷 - 无答案)
- `courses/[course]/quizzes/midterm_mock_exam_answers.md` (模拟试卷 - 含答案)

---

## 🗂️ 最终目录结构

```
courses/
└── [course]/
    ├── slides/                                # 原始课件
    │   ├── Week 1 - [topic].pptx
    │   └── ...
    ├── notes/
    │   ├── [topic]_slides.md                  # Phase 2: 各周 slides 提取
    │   ├── [topic]_notes.md                   # Phase 2: 各周笔记
    │   ├── midterm_review_plan.md             # Phase 1: 复习计划
    │   ├── midterm_review_notes.md            # Phase 2: 整合复习笔记
    │   ├── midterm_code_review.md             # Phase 4: 代码复习
    │   ├── midterm_code_snippets.py           # Phase 4: 代码片段 (可选)
    │   └── midterm_cheat_sheet.md             # Phase 5: 速查表
    ├── quizzes/
    │   ├── quizes1.md                         # 老师原始 quiz (保持原命名)
    │   ├── [topic]_quiz.md                    # Phase 3: 各主题练习题
    │   ├── midterm_quiz_bank.md               # Phase 3: 合并题库
    │   ├── midterm_mock_exam.md               # Phase 6: 模拟试卷
    │   └── midterm_mock_exam_answers.md       # Phase 6: 试卷答案
    ├── code/                                  # 已完成的 lab 代码
    │   └── ...
    └── labs/                                  # Lab 说明
        └── ...
```

---

## 💡 快捷子命令

| 命令                                          | 说明             | 从哪个 Phase 开始 |
| --------------------------------------------- | ---------------- | ----------------- |
| `/midterm-review mv`                          | 完整流程         | Phase 1           |
| `/midterm-review mv --weeks=1-5`              | 指定范围         | Phase 1           |
| `/midterm-review mv --from=phase2`            | 从笔记整合开始   | Phase 2           |
| `/midterm-review mv --from=phase3`            | 从题库构建开始   | Phase 3           |
| `/midterm-review mv --phase=4`                | 只做代码复习     | Phase 4           |
| `/midterm-review mv --phase=5`                | 只生成速查表     | Phase 5           |
| `/midterm-review mv --phase=6`                | 只做模拟测试     | Phase 6           |

---

## 📊 支持的课程

| 课程代码 | 课程名称                    | 对应 Skill        |
| -------- | --------------------------- | ----------------- |
| `ml`     | Machine Learning            | `ai_learning-ml`  |
| `nlp`    | Natural Language Processing | `ai_learning-nlp` |
| `mv`     | Machine Vision              | `ai_learning-mv`  |
| `cv`     | Computer Vision             | `ai_learning-cv`  |
| `dl`     | Deep Learning               | `ai_learning-dl`  |
| `rl`     | Reinforcement Learning      | `ai_learning-rl`  |

---

## 📎 关联 Skill 文档

| Skill                              | 用途                     |
| ---------------------------------- | ------------------------ |
| `learning-note_taking`             | 生成结构化笔记           |
| `learning-quiz_generation`         | 生成练习题和模拟试卷     |
| `learning-quiz_note_taking`        | 为 quiz 补充答案解释     |
| `learning-code_generation`         | 整理代码和生成演示       |
| `dev-pdf_processing`               | PDF 转 Markdown          |
| `dev-pptx_to_pdf`                  | PPTX 转 PDF              |
| `learning-bilingual_content`       | 双语内容生成             |
| `learning-logic_consistency`       | 逻辑一致性审查           |

---

## 🚨 注意事项

1. **不改原始文件**: 不修改 `slides/` 和 `labs/` 中的源文件
2. **保持拼写一致**: 已有文件如 `quizes1.md`（拼写错误）保持原名不改
3. **笔记语言**: 笔记以中文为主，技术术语保留英文
4. **Quiz 格式**: 检测已有 quiz 的格式风格（Inline / Checkbox），新题匹配该格式
5. **代码可运行**: Phase 4 提取的代码片段必须独立可运行
6. **速查表精简**: Phase 5 速查表控制在 2 页以内（打印友好）
7. **模拟试卷不重复**: Phase 6 的题目不得与 Phase 3 题库重复
