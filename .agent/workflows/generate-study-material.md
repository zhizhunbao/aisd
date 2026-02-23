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
/generate-study-material nlp transformer --phase=0
```

## 📋 完整流程概览

```
┌─────────────────────────────────────────────────────────────┐
│ Phase -1: 抓取 (Scrape)                                       │
│   ↓ learning-brightspace_scraper skill                      │
├─────────────────────────────────────────────────────────────┤
│ Phase 0: 转换 (Convert)                                      │
│   ↓ dev-pptx_to_pdf, dev-pdf_processing skills              │
├─────────────────────────────────────────────────────────────┤
│ Phase 0.5: 格式化 (Format)                                    │
│   ↓ learning-slide_formatting skill                         │
├─────────────────────────────────────────────────────────────┤
│ Phase 1: 笔记 (Notes)                                        │
│   ↓ learning-note_taking skill                              │
│   ↓ + math-concept-library (公式库, 滋雪球式积累)           │
│   ↓ + concept-glossary (术语库, 滋雪球式积累)              │
│   ↓ + textbook-vectorization (教材语义搜索, 多书交叉参考) │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: 演示 (Demo)                                         │
│   ↓ learning-code_generation + dev-code_comment skills      │
│   ↓ + math-concept-library / concept-glossary (复用注释)    │
│   ↓ + textbook-vectorization (搜索伪代码/推导细节)       │
├─────────────────────────────────────────────────────────────┤
│ Phase 2.5: 转换 (Convert .py → .ipynb)                       │
│   ↓ learning-notebook_conversion skill                      │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: 合成 (Synthesize)                                   │
│   ↓ learning-notebook_conversion skill                      │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: 审查 (Review)                                       │
│   ↓ learning-logic_consistency, learning-code_consistency   │
├─────────────────────────────────────────────────────────────┤
│ Phase 5: 测验 (Quiz)                                         │
│   ↓ learning-quiz_generation skill                          │
├─────────────────────────────────────────────────────────────┤
│ Phase L: 实验格式化 (Lab Formatting) ← 独立流程             │
│   ↓ Lab PDF → 格式化 + 中文翻译（不加 Notes）              │
│   ↓ dev-pdf_processing + learning-note_taking §10           │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase -1: 远程抓取 🌐

**Skill**: `learning-brightspace_scraper`

从 Brightspace LMS 自动下载最新的课程材料。

### 步骤

1. **检查配置**: 确保主题对应的 Course ID 在 `scraper/config.py` 中。
2. **执行抓取**: 运行 scraper 下载指定课程的 Slides 或相关模块。
3. **同步文件**: 将下载的 `data/[course]/.../Slides/*.pdf` 移动到 `courses/[course]/slides/`。
4. **跳过判断**: 如果本地已有最新材料或明确指定 `--from=phase0`，则跳过。

### 命令

```bash
# 启动时会自动检查
/generate-study-material ml svm --scrape
```

### 输出

- `courses/[course]/slides/[topic].pdf` (或 .pptx)

---

## Phase 0: 材料转换 📄

**Skills**: `dev-pptx_to_pdf`, `dev-pdf_processing`

将原始 PPTX/PDF 转为可处理的 Markdown。

### 步骤

1. **如果是 PPTX**: 先用 `dev-pptx_to_pdf` 转为 PDF
2. **如果是 PDF**: 用 `dev-pdf_processing` 的 `pdf_to_md_hybrid.py` 转为 Markdown
3. 提取嵌入图片到 `[topic]_slides_images/`
4. 验证提取的 Markdown 包含所有文本、公式和图表描述
5. 如果源材料已经是可读格式，跳过此阶段

### 命令

```
读取 skill: .shared/skills/dev-pptx_to_pdf/SKILL.md
读取 skill: .shared/skills/dev-pdf_processing/SKILL.md
执行转换
```

### 输出

- `courses/[course]/notes/[topic]_slides.md`
- `courses/[course]/notes/[topic]_slides_images/`

---

## Phase 0.5: 格式化 📐

**Skill**: `learning-slide_formatting`

将 Phase 0 输出的原始 Markdown 整理为结构清晰的课堂笔记格式。

### 步骤

1. 添加文档头（标题、来源、讲师、日期）
2. 将 `## Page N` / `## Slide N` 替换为按主题编号的逻辑章节
3. 双语章节标题（中文在前，英文括号）
4. 清理 PDF 提取残留（页码、重复标题、空行）
5. 整理图片引用，去除重复
6. 在每个主要概念后添加 `📝 Notes:` 占位符
7. 合并相关 slides 到同一章节

### 命令

```
读取 skill: .shared/skills/learning-slide_formatting/SKILL.md
格式化 Markdown 结构
```

### 输出

- `courses/[course]/notes/[topic]_slides.md` (格式化后，覆盖原文件)

---

## Phase 1: 添加笔记 🧠

**Skills**: `learning-note_taking`, `math-concept-library`, `concept-glossary`, `textbook-vectorization`

在 Phase 0.5 格式化好的 `_slides.md` 上直接添加深度双语笔记。同时滋雪球式完善两个知识库，并利用教材语义搜索获取多书交叉参考。

### 步骤

1. 读取 Phase 0.5 格式化后的 `[topic]_slides.md`
2. **查库 (先查再写)**:
   - 遇到数学公式 → 查阅 `math-concept-library/resources/`，复用已有的定义、直觉类比和分步解读
   - 遇到概念/术语 → 查阅 `concept-glossary/resources/`，复用已有的定义、类比、历史背景
   - 遇到核心概念 → 用 `query_books.py` 搜索多本教材的解释，获取多角度理解
3. 将 `📝 Notes:` 占位符替换为深度双语笔记（7 层框架）
4. 每个笔记块至少 3 层有内容
5. 英文在 `>` 引用块，中文在 `>>` 嵌套引用块
6. 层标题用英文 + 图标（📌📎🎯💡⚙️⚖️⚠️📝）
7. **入库 (写完回填)**:
   - 新数学公式 → 按 `math-concept-library` 条目格式添加到 `resources/*.md`
   - 新概念/术语 → 按 `concept-glossary` 条目格式添加到 `resources/*.md`
   - 已有条目 → 更新其 `Appears In` 字段，补充交叉引用

### 两种输出模式

**模式 A（默认）：直接在 slides 上加笔记**
- 笔记直接添加到 `[topic]_slides.md` 中每个概念后面
- 适合快速复习，slides 和 notes 在一个文件中

**模式 B：生成独立笔记文件**
- 总结为独立的 `[topic]_notes.md`
- 适合深度学习，笔记可以独立展开

### 命令

```
读取 skill: .shared/skills/learning-note_taking/SKILL.md
读取 skill: .shared/skills/math-concept-library/SKILL.md
读取 skill: .shared/skills/concept-glossary/SKILL.md
查阅两个库的 resources/ 中的已有条目
搜索教材: uv run python courses/self-study/query_books.py "核心概念" --top-k 5
在格式化的 slides 上添加笔记（模式 A）
或 总结为独立笔记文件（模式 B）
新公式写回 math-concept-library/resources/
新概念写回 concept-glossary/resources/
```

### 输出

- 模式 A: `courses/[course]/notes/[topic]_slides.md` (带笔记版本)
- 模式 B: `courses/[course]/notes/[topic]_notes.md` (独立笔记)

---

## Phase 2: 实现演示 💻

**Skills**: `learning-code_generation`, `dev-code_comment`, `math-concept-library`, `concept-glossary`, `textbook-vectorization`

基于笔记生成独立可运行的 Python 演示脚本。代码注释中的算法/概念解释从知识库复用。遇到实现细节不确定时，用 `query_books.py` 搜索教材中的伪代码或推导过程。

### 步骤

1. 创建 `courses/[course]/notes/[topic]_complete_demo.py`
2. 用合成数据实现核心算法（`sklearn.datasets`, `numpy`）
3. 可视化保存到 `[topic]_complete_demo_pages/`
4. 使用 `os.path.join(os.path.dirname(os.path.abspath(__file__)), ...)` 确保路径安全
5. **代码注释**: 按 `dev-code_comment` 规范添加双语注释，算法/概念注释模板中的术语解释和公式从 `math-concept-library` 和 `concept-glossary` 复用
6. 运行脚本，验证逻辑与 Phase 1 理论一致

### 命令

```
读取 skill: .shared/skills/learning-code_generation/SKILL.md
读取 skill: .shared/skills/dev-code_comment/SKILL.md
查阅 math-concept-library + concept-glossary 复用注释素材
搜索教材: uv run python courses/self-study/query_books.py "算法名 pseudocode" --top-k 3
生成演示脚本
运行验证
```

### 输出

- `courses/[course]/notes/[topic]_complete_demo.py`
- `courses/[course]/notes/[topic]_complete_demo_pages/`

---

## Phase 2.5: 脚本转 Notebook 📒

**Skill**: `learning-notebook_conversion`

将 Phase 2 的 `.py` 演示脚本转换为 Jupyter Notebook，方便交互式学习。

### 步骤

1. 使用 `convert_to_notebook.py` 将 `[topic]_complete_demo.py` 转换为 `.ipynb`

```bash
uv run python .shared/skills/learning-notebook_conversion/scripts/convert_to_notebook.py courses/[course]/notes/[topic]_complete_demo.py
```

2. 替换 `plt.close()` 为 `plt.show()`（使图片在 notebook 内联显示）

```python
import nbformat
with open('notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)
for cell in nb.cells:
    if cell.cell_type == 'code':
        cell.source = cell.source.replace('plt.close()', 'plt.show()')
with open('notebook.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
```

3. 执行所有 cells 生成内联输出

```bash
jupyter nbconvert --to notebook --execute [topic]_complete_demo.ipynb --output [topic]_complete_demo.ipynb
```

### 命令

```
读取 skill: .shared/skills/learning-notebook_conversion/SKILL.md
转换 .py → .ipynb
替换 plt.close() → plt.show()
执行所有 cells
```

### 输出

- `courses/[course]/notes/[topic]_complete_demo.ipynb`

---

## Phase 3: 交互合成 📓

**Skill**: `learning-notebook_conversion`

将理论和代码合并为交互式 Jupyter Notebook。

### 步骤

1. 合并 Phase 1 理论和 Phase 2 代码
2. 每个概念的 Cell 结构：
   - **Markdown**: 简介 + 问题的简单解释
   - **Markdown**: 理论 + 术语定义
   - **Code**: 实现代码
   - **Code**: 可视化代码（inline 显示）
   - **Markdown**: "试一试" 部分（鼓励修改参数）
3. 执行 **Zero Acronym Policy**：先解释概念，再使用术语
4. 确保所有图表 inline 显示

### 命令

```
读取 skill: .shared/skills/learning-notebook_conversion/SKILL.md
合成 Notebook
运行所有 cells
```

### 输出

- `courses/[course]/notes/[topic]_interactive_tutorial.ipynb`

---

## Phase 4: 执行与审查 ✅

**Skills**: `learning-logic_consistency`, `learning-code_consistency`

验证 + 逻辑审查 + 代码一致性审查，一次性完成。

### 4a. 执行验证

- 从头到尾运行所有 Notebook cells
- 确认 Notebook 自包含（无缺失依赖）

### 4b. 逻辑一致性审查

```
读取 skill: .shared/skills/learning-logic_consistency/SKILL.md
```

- **Zero Leap Rule**: 技术术语使用前必须有解释
- **IO & Parameter Transparency**: 每个代码块有清晰的输入/输出描述
- **Why-First Principle**: 每个动作前有动机说明
- **Conceptual Dependency Chain**: 基础在前，应用在后
- **Code-Theory Synchronization**: 变量名与文本术语一致
- **Transition Verification**: 章节间有过渡句，无"悬崖"跳跃

### 4c. 代码与资产一致性审查

```
读取 skill: .shared/skills/learning-code_consistency/SKILL.md
```

- Notebook 代码逻辑与 Phase 2 demo 脚本一致
- 所有图片引用有效（相对路径，无损坏链接）
- 统计值和输出在各文件间一致

### 4d. 最终检查清单

- [ ] 代码中无未解释的 "magic numbers"
- [ ] 无未定义的首字母缩写
- [ ] 每个代码块上方有 "Motivation" 段落
- [ ] 每个代码块的 Input/Output 可识别
- [ ] Zero Acronym Policy 通过
- [ ] Notebook 从头到尾无错误运行
- [ ] 无 `TODO`、占位符或泛泛总结

---

## Phase 5: 知识测验 ✍️

**Skill**: `learning-quiz_generation`

根据笔记和演示代码生成测验题，以巩固学习效果。

### 步骤

1. 读取 Phase 1 的 `[topic]_notes.md` 和 Phase 2 的 `[topic]_complete_demo.py`
2. 生成 5-10 道选择题 (MCQ) 和 5 道判断题 (T/F)
3. 包含 1-2 道关于代码参数或输出的简答题
4. 生成 `courses/[course]/quizzes/[topic]_quiz.md`
5. 在文件末尾附上标准答案

### 命令

```
读取 skill: .shared/skills/learning-quiz_generation/SKILL.md
生成测验题
```

### 输出

- `courses/[course]/quizzes/[topic]_quiz.md`

---

## 🗂️ 目录结构示例

```
courses/
└── ml/
    └── notes/
        ├── svm_slides.md                   # Phase 0 + 0.5: 格式化的幻灯片
        ├── svm_slides_images/              # Phase 0: 提取的图片
        │   ├── slide1_img1.png
        │   └── slide2_img1.png
        ├── svm_notes.md                    # Phase 1: 理论笔记
        ├── svm_complete_demo.py            # Phase 2: 演示脚本
        ├── svm_complete_demo.ipynb          # Phase 2.5: 演示 Notebook
        ├── svm_complete_demo_pages/        # Phase 2: 参考图片
        │   ├── svm_demo_plot1.png
        │   └── svm_demo_plot2.png
        ├── svm_interactive_tutorial.ipynb   # Phase 3: 最终成品
        └── ../quizzes/
            └── svm_quiz.md                 # Phase 5: 测验题
```

---

## Phase L: 实验资料格式化 🧪 (Lab Material Formatting)

**Skills**: `learning-note_taking` (§10 教师资料格式化模式), `dev-pdf_processing`

对实验（Lab）PDF 进行格式化和中文翻译。**不生成 Notes 块**，只做格式整理 + 双语翻译。

### 适用场景

- 收到新的 Lab PDF，需要格式化为可读的 Markdown
- 需要中英双语版本方便理解
- Lab 内容与 slides 主题不完全对应

### 步骤

1. **转换 Lab PDF**（如果没有 markdown 版）:
   ```bash
   uv run python .shared/skills/dev-pdf_processing/scripts/pdf_to_md_hybrid.py "courses/[course]/labs/Lab_X.pdf" -o "courses/[course]/labs/Lab_X.md"
   ```

2. **格式化 Lab MD**:
   - 使用 `learning-note_taking` §10 教师资料格式化模式
   - 移除 PDF 转换工具生成的模板标记（`### 📷`、`### 📝`、`### ✍️`）
   - 保留页面截图 `![Page N](...)`
   - 所有文本加中文翻译：`English — 中文翻译`
   - 表格双语化
   - 代码块原样保留
   - **不加 📝 Notes 块**

3. **输出**: `courses/[course]/labs/Lab_X.md`（原地格式化）

### 命令

```
/generate-study-material [course] lab[N]

示例:
/generate-study-material nlp lab3
/generate-study-material ml lab2
```

### 输出

- `courses/[course]/labs/Lab_X.md`（格式化 + 中文翻译的 Lab 文档）

### 与 Slides 流程的区别

| 维度 | Slides 流程 (Phase 0-5) | Lab 流程 (Phase L) |
|------|------------------------|-------------------|
| 输入 | PPT/PDF slides | Lab PDF |
| 处理方式 | 格式化 + 深度 Notes | **仅格式化 + 翻译** |
| 📝 Notes | ✅ 9 层框架 | ❌ 不加 |
| 产出 | 多文件（slides+notes+demo+quiz） | 单文件（格式化的 Lab MD） |
| 何时使用 | 课前预习/课后复习 | 收到 Lab PDF 时 |

---

## 💡 快捷子命令

| 命令                                         | 说明              | 从哪个 Phase 开始 |
| -------------------------------------------- | ----------------- | ----------------- |
| `/generate-study-material ml svm`            | 完整流程 (含抓取) | Phase -1          |
| `/generate-study-material ml svm --no-scrape`| 完整流程 (跳过抓取)| Phase 0           |
| `/generate-study-material ml svm --from=phase1` | 从笔记提取开始 | Phase 1           |
| `/generate-study-material ml svm --from=phase2` | 从 Demo 开始   | Phase 2           |
| `/generate-study-material ml svm --from=phase2.5` | 从 .py→.ipynb 开始 | Phase 2.5     |
| `/generate-study-material ml svm --from=phase3` | 从 NB 合成开始 | Phase 3           |
| `/generate-study-material ml svm --phase=4`  | 只运行审查        | Phase 4           |
| `/generate-study-material ml svm --phase=5`  | 只生成测验题      | Phase 5           |
| `/generate-study-material nlp lab3`          | Lab 格式化+翻译   | Phase L           |

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

## 📎 关联 Skill 文档

- 整体规范: `.shared/skills/learning-automated_study_material/SKILL.md`
- 📱 数学公式库: `.shared/skills/math-concept-library/SKILL.md` — 公式的标准解读、直觉类比、分步解读复用库
- 📖 概念术语库: `.shared/skills/concept-glossary/SKILL.md` — 术语定义、历史背景、类比、交叉引用复用库
- 💬 代码注释: `.shared/skills/dev-code_comment/SKILL.md` — 双语代码注释规范，算法/概念注释模板
- 📚 教材搜索: `.shared/skills/learning-textbook_vectorization/SKILL.md` — 17 本教材向量化语义搜索
  - 向量化: `uv run python courses/self-study/vectorize_all.py`
  - 搜索: `uv run python courses/self-study/query_books.py "查询内容"`

> 💡 两个知识库都是**滚雪球式积累**：每次写笔记时查库复用 → 写完后新条目入库 → 下次写笔记时可复用的素材更多
> 💡 `dev-code_comment` 的算法注释模板（术语解释 + 定义/公式/举例/优点）与知识库条目格式互通，确保笔记和代码中的解释一致
> 💡 教材语义搜索提供**多书交叉参考**：遇到概念时搜索多本教材的解释，获取不同角度的理解
