---
description: Transform raw course materials (PPT/PDF) into an interactive Jupyter Notebook learning package
---

# 📖 自学材料生成工作流 (Generate Study Material)

将课程原始 PPT/PDF 转换为可交互的 Jupyter Notebook 自学教程。

## 🎯 使用方式

```
/generate-study-material [课程] [主题]

示例:
/generate-study-material ml svm
/generate-study-material ml decision_tree --from=phase2
/generate-study-material nlp lab3          ← Lab 格式化模式
```

## 📋 流程概览

```
Phase -1  抓取       → brightspace-scraper skill
Phase 0   转换       → dev-pptx-to-pdf, dev-pdf-processing skills
Phase 0.5 格式化     → learning-slide-formatting skill
Phase 1   双语翻译   → learning-note-taking skill (§10)
Phase 1.5 故事线     → learning-lecture-storyline skill
Phase 1.55 历史线    → learning-lecture-history skill
Phase 1.52 学习地图  → learning-map skill
Phase 1.53 前置知识  → learning-prerequisite skill
Phase 1.6  数学基础  → learning-math-foundations skill
Phase 1.7  教程      → dev-pdf-processing + learning-note-taking skill
Phase 1.9  概念三件套 → learning-concept-coverage skill
Phase 1.91 术语表    → learning-glossary skill
Phase 1.92 常见问题  → learning-faq skill
Phase 1.95 衔接桥    → learning-bridge skill
Phase 2   演示代码   → learning-code-generation + dev-code-comment skills
Phase 2.5 转 Notebook → learning-notebook-conversion skill
Phase 3   合成 NB    → learning-notebook-conversion skill
Phase 4   审查       → learning-logic-consistency + learning-code-consistency skills
Phase 5   测验       → learning-quiz-generation skill
Phase 5.5 练习       → learning-exercise skill
Phase L   Lab格式化  → dev-pdf-processing + learning-note-taking §10
```

---

## ⚖️ 执行协议

1. **串行执行**: 按 Phase 顺序，禁止跨阶段
2. **检查点验证**: 每 Phase 末尾验证后才进入下一阶段
3. **中断恢复**: `--from=<phase>` 从指定阶段继续
4. **Skill 优先**: 每个 Phase 开始前**必须先读取对应 skill 的 SKILL.md**

---

## Phase -1: 远程抓取 🌐

**Skill**: `brightspace-scraper`

1. 检查配置: Course ID 在 `scraper/config.py` 中
2. 执行抓取: 下载指定课程 Slides
3. 同步文件: 移动到 `courses/[course]/slides/`
4. 跳过条件: 本地已有最新材料 或 `--from=phase0`

**输出**: `courses/[course]/slides/[topic].pdf`

---

## Phase 0: 材料转换 📄

**Skills**: `dev-pptx-to-pdf`, `dev-pdf-processing`

1. PPTX → PDF (如需要): follow `dev-pptx-to-pdf` skill
2. PDF → Markdown: follow `dev-pdf-processing` skill (`pdf_to_md_hybrid.py`)
3. 提取图片到 `[topic]_slides_images/`
4. 验证 Markdown 完整性

**输出**: `courses/[course]/notes/[topic]_slides.md` + images/

---

## Phase 0.5: 格式化 📐

**Skill**: `learning-slide-formatting`

1. Follow `learning-slide-formatting` skill 完整指令
2. 双语章节标题、清理残留、整理图片引用

**输出**: `courses/[course]/notes/[topic]_slides.md` (格式化后)

---

## Phase 1: 双语翻译 🌐

**Skill**: `learning-note-taking` (§10 教师资料格式化模式)

1. Follow `learning-note-taking` skill §10 模式
2. 所有英文加中文翻译，表格双语化
3. **不加** `📝 Notes:` 块（深度笔记移到 Phase 1.7）

**输出**: `courses/[course]/notes/[topic]_slides.md` (带翻译)

---

## Phase 1.5: 故事线 📖

**Skill**: `learning-lecture-storyline`

1. Follow `learning-lecture-storyline` skill
2. 将碎片化 slides 重组为因果叙事
3. 末尾添加 📚 参考资料链接

**输出**: `courses/[course]/notes/[topic]_storyline.md`

---

## Phase 1.55: 历史线 🕰️

**Skill**: `learning-lecture-history`

1. Follow `learning-lecture-history` skill
2. 技术概念按历史年代排列
3. 跳过条件: 纯数学/纯理论主题，无技术演进

**输出**: `courses/[course]/notes/[topic]_history.md`

---

## Phase 1.52: 学习地图 🗺️

**Skill**: `learning-map`

1. Follow `learning-map` skill
2. 生成导航文件：位置、文件作用、学习路线

**输出**: `courses/[course]/notes/[topic]_map.md`

---

## Phase 1.53: 前置知识 📚

**Skill**: `learning-prerequisite`

1. Follow `learning-prerequisite` skill
2. 列出必须掌握的背景知识和前置缺口

**输出**: `courses/[course]/notes/[topic]_prerequisite.md`

---

## Phase 1.6: 数学基础 📐

**Skill**: `learning-math-foundations`

1. Follow `learning-math-foundations` skill
2. 从教科书提取数学前置知识
3. 更新 `courses/math/README.md`
4. 在 Storyline/Tutorial 头部添加数学前置链接
5. 跳过条件: 本主题不涉及新数学前置

**输出**: `courses/math/{discipline}/{topic}.md`

---

## Phase 1.7: 教科书教程 📚

**Skills**: `dev-pdf-processing`, `learning-note-taking`, `learning-source-citation`

1. 找出 Slides 的推导缺口（给了结论但没推导的公式）
2. 在 `courses/self-study/` 中找对应教科书 PDF
3. 用 `batch_pdf_to_md.py` 转换相关 PDF
4. 合成教程: follow `learning-note-taking` skill 的教程规则
   - 遵守来源引证标准: follow `learning-source-citation` skill
   - LaTeX 公式必须、教科书方程编号必须
   - 末尾添加参考索引表
5. 更新 Storyline 的 📚 参考资料链接

**教程 ≠ 另一个 Storyline**:

| Storyline | Tutorial |
|-----------|----------|
| 为什么需要？因果叙事 | 教科书怎么推导/证明？ |
| 概念 + 直觉 + 类比 | 公式 + 证明步骤 + 方程编号 |

**输出**: `courses/[course]/notes/[topic]_tutorial.md`

---

## Phase 1.9: 概念三件套 📋

**Skill**: `learning-concept-coverage`

1. Follow `learning-concept-coverage` skill
2. 交叉检查 slides + quiz + lab
3. 生成 3 个文件:
   - `_concepts.md` — 定义+动机+关联+⚠️陷阱+对比表
   - `_math.md` — 公式+手算练习
   - `_code.md` — 代码模式+API用法

**输出**: `[topic]_concepts.md`, `[topic]_math.md`, `[topic]_code.md`

---

## Phase 1.91–1.95: 辅助文件

| Phase | Skill | 输出 |
|-------|-------|------|
| 1.91 术语表 | `learning-glossary` | `[topic]_glossary.md` |
| 1.92 FAQ | `learning-faq` | `[topic]_faq.md` |
| 1.95 衔接桥 | `learning-bridge` | `[topic]_bridge.md` |

每个 Phase: follow 对应 skill 的完整指令。

---

## Phase 2: 实现演示 💻

**Skills**: `learning-code-generation`, `dev-code-comment`, `textbook-vectorization`

1. Follow `learning-code-generation` skill
2. 双语注释: follow `dev-code-comment` skill
3. 搜索教材伪代码: `uv run python courses/self-study/query_books.py "算法名 pseudocode"`
4. 运行脚本验证

**输出**: `[topic]_complete_demo.py` + `[topic]_complete_demo_pages/`

---

## Phase 2.5: 转 Notebook 📒

**Skill**: `learning-notebook-conversion`

1. Follow `learning-notebook-conversion` skill
2. `.py` → `.ipynb`，替换 `plt.close()` → `plt.show()`
3. 执行所有 cells

**输出**: `[topic]_complete_demo.ipynb`

---

## Phase 3: 交互合成 📓

**Skill**: `learning-notebook-conversion`

1. 合并 Phase 1 理论 + Phase 2 代码为交互式 Notebook
2. 每个概念: Markdown简介 → 理论 → Code → 可视化 → "试一试"
3. Zero Acronym Policy: 先解释概念再使用术语

**输出**: `[topic]_interactive_tutorial.ipynb`

---

## Phase 4: 审查 ✅

**Skills**: `learning-logic-consistency`, `learning-code-consistency`

1. Follow `learning-logic-consistency` skill (Zero Leap, Why-First, IO Transparency)
2. Follow `learning-code-consistency` skill (代码/资产一致性)
3. 从头运行 Notebook 确认无错误
4. 检查: 无 magic numbers / 无未定义缩写 / 无 TODO

---

## Phase 5: 测验 ✍️

**Skill**: `learning-quiz-generation`

1. Follow `learning-quiz-generation` skill
2. 生成 MCQ + T/F + 简答题

**输出**: `courses/[course]/quizzes/[topic]_quiz.md`

---

## Phase 5.5: 理解型练习 📝

**Skill**: `learning-exercise`

1. Follow `learning-exercise` skill
2. 概念题、对比题、推理题、公式题、代码理解题

**输出**: `courses/[course]/notes/[topic]_exercise.md`

---

## Phase L: Lab 格式化 🧪

**Skills**: `dev-pdf-processing`, `learning-note-taking` (§10)

1. PDF → MD: follow `dev-pdf-processing` skill
2. 格式化: follow `learning-note-taking` §10 (仅翻译，不加 Notes)

**输出**: `courses/[course]/labs/Lab_X.md`

---

## 💡 快捷子命令

| 命令 | Phase |
|------|-------|
| `/generate-study-material ml svm` | 完整 (Phase -1) |
| `--from=phase0` | 从转换开始 |
| `--from=phase1` | 从双语翻译 |
| `--from=phase1.5` | 从故事线 |
| `--from=phase1.7` | 从教程 |
| `--from=phase1.9` | 从概念整理 |
| `--from=phase2` | 从 Demo |
| `--phase=4` | 只审查 |
| `--phase=5` | 只测验 |
| `nlp lab3` | Lab 格式化 |

## 📊 支持的课程

| 代码 | 课程 | Skill |
|------|------|-------|
| `ml` | Machine Learning | `ai-learning-ml` |
| `nlp` | NLP | `ai-learning-nlp` |
| `mv` | Machine Vision | `ai-learning-mv` |
| `cv` | Computer Vision | `ai-learning-cv` |
| `dl` | Deep Learning | `ai-learning-dl` |
| `rl` | Reinforcement Learning | `ai-learning-rl` |
