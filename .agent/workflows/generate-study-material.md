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
│ Phase 1: 双语翻译 (Bilingual Translation)                    │
│   ↓ learning-note_taking skill (§10 翻译模式)               │
│   ↓ slides 加中英文翻译，不加深度 Notes                    │
├─────────────────────────────────────────────────────────────┤
│ Phase 1.5: 故事线 (Storyline)                     ← NEW      │
│   ↓ learning-lecture_storyline skill                        │
│   ↓ 基于老师 slides，重组为因果叙事                         │
├─────────────────────────────────────────────────────────────┤
│ Phase 1.55: 历史线 (History Timeline)              ← NEW      │
│   ↓ learning-lecture_history skill                          │
│   ↓ 将技术概念按历史脉络排列，理解演进因果                 │
├─────────────────────────────────────────────────────────────┤
│ Phase 1.6: 数学基础 (Math Foundations)             ← NEW      │
│   ↓ learning-math_foundations skill                         │
│   ↓ 从教科书提取本主题需要的数学前置知识                   │
├─────────────────────────────────────────────────────────────┤
│ Phase 1.7: 教程 (Tutorial)                        ← NEW      │
│   ↓ dev-pdf_processing (batch_pdf_to_md.py)                 │
│   ↓ + learning-note_taking skill                            │
│   ↓ 基于自己的教科书，合成为独立教程文件                   │
├─────────────────────────────────────────────────────────────┤
│ Phase 1.9: 速查三件套 (Cheat Sheet Split)          ← NEW      │
│   ↓ learning-cheat_sheet skill                              │
│   ↓ 拆分为 3 个文件：概念速查 + 数学公式 + 代码参考       │
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

### 新阶段的设计逻辑

```
Phase 1 双语翻译    → 老师 slides 加中英文翻译（基础）
    ↓
Phase 1.5 故事线    → 把碎片化 slides 重组为因果叙事（宏观）
    ↓
Phase 1.55 历史线   → 将技术概念按年代排列，理解演进因果（纵深）
    ↓
Phase 1.6 数学基础  → 从教科书提取本主题的数学前置知识（补基础）
    ↓
Phase 1.7 教程      → 用自己教科书合成独立教程（加深）
    ↓
Phase 1.9 速查三件套 → 拆分为概念速查 + 数学公式 + 代码参考（压缩）
```

| 阶段                 | 输入来源             | 输出目的     | 类比                  |
| -------------------- | -------------------- | ------------ | --------------------- |
| **Translation**      | 老师 slides          | 读懂内容     | 双语课堂笔记          |
| **Storyline**        | 老师 slides + Notes  | 整体理解     | 故事书                |
| **History Timeline** | slides + 文献        | 技术演进脉络 | 年代大事记            |
| **Math Foundations** | 教科书（数学部分）   | 补数学前置   | 数学预习手册          |
| **Tutorial**         | 自己的教科书         | 深度理解     | 参考书 → 独立教程文件 |
| **Cheat Sheet**      | 老师 slides+quiz+lab | 考试速查     | 小抄（3件套）         |

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

## Phase 1: 双语翻译 🌐

**Skill**: `learning-note_taking` (§10 教师资料格式化模式)

在 Phase 0.5 格式化好的 `_slides.md` 上添加**中英文翻译**。不加深度 Notes 块（深度分析移到 Phase 1.7 教程）。

### 步骤

1. 读取 Phase 0.5 格式化后的 `[topic]_slides.md`
2. 所有英文文本加中文翻译：`English — 中文翻译`
3. 表格双语化
4. 公式保留原样，必要时加一行中文说明
5. 代码块原样保留
6. **不加** `📝 Notes:` 块（深度笔记移到 Phase 1.7）

### 命令

```
读取 skill: .shared/skills/learning-note_taking/SKILL.md (§10 翻译模式)
为 slides 添加中英文翻译
```

### 输出

- `courses/[course]/notes/[topic]_slides.md` (带翻译版本)

---

## Phase 1.5: 故事线 📖

**Skill**: `learning-lecture_storyline`

基于老师 slides 和 Phase 1 笔记，将碎片化的幻灯片重组为**因果叙事**（problem → motivation → solution → new problem → ...）。

### 与 Phase 1 的区别

|          | Phase 1 翻译            | Phase 1.5 故事线       |
| -------- | ----------------------- | ---------------------- |
| **视角** | 逐 slide 翻译           | 宏观：全讲重组为故事   |
| **结构** | 保留原 slide 顺序       | 按因果逻辑重排         |
| **语言** | 中英双语对照            | 纯中文叙事             |
| **核心** | "这张 slide 说了什么？" | "为什么需要这个概念？" |

### 步骤

1. 读取 Phase 1 的 `[topic]_slides.md`（带笔记版本）
2. 识别核心问题：整讲在解决什么？
3. 找出技术演进链：方案A ❌→ 方案B ⚠️→ 方案C ✅
4. 按 storyline 标准模板写出因果叙事
5. 包含：ASCII 路线图 + 对比表格 + 考试 checklist
6. 末尾添加 **📚 参考资料** 链接（指向 Phase 1.7 的教程文件，如果已存在）

### 命令

```
读取 skill: .shared/skills/learning-lecture_storyline/SKILL.md
提取 slides 因果链
生成故事线
```

### 输出

- `courses/[course]/notes/[topic]_storyline.md`

---

## Phase 1.55: 历史线 🕰️

**Skill**: `learning-lecture_history`

将课程中涉及的技术概念按**历史年代**排列，帮助学生理解"为什么会有这个技术"——每个技术都是对前一个技术局限性的回应。

### 与 Phase 1.5 的区别

|          | Phase 1.5 故事线        | Phase 1.55 历史线        |
| -------- | ----------------------- | ------------------------ |
| **视角** | 一次课内部的逻辑线      | **跨越多年的演进线**     |
| **组织** | 按因果逻辑（问题→方案） | **按年代顺序**           |
| **范围** | 当前主题                | 当前主题 + 前身技术      |
| **核心** | "为什么需要这个概念？"  | **"这个技术从哪来的？"** |

### 步骤

1. 读取 Phase 1.5 Storyline，识别涉及的技术节点
2. 回溯每个技术的**直接前身**（不需要写领域综述，只覆盖课程涉及的）
3. 按 `learning-lecture_history` skill 模板写出历史线：
   - 📍 全景时间线（ASCII 时间轴图）
   - 每站：之前的问题 → 核心创新 → 关键人物 → 里程碑数据 → 遗留问题 → 课程关联
   - 📊 对比总结表
   - 🎯 考试相关知识点

### 跳过条件

- 主题是纯数学/纯理论，没有明确的技术演进关系
- 主题只涉及一个技术，没有前身也没有后续

### 命令

```
读取 skill: .agent/skills/learning-lecture_history/SKILL.md
识别 Storyline 中的技术节点
回溯前身技术
生成历史线
```

### 输出

- `courses/[course]/notes/[topic]_history.md`

---

## Phase 1.6: 数学基础 📐

**Skill**: `learning-math_foundations`

从教科书提取本主题需要的**数学前置知识**，生成独立的数学基础文件。在进入 Tutorial 推导之前，确保读者具备必要的数学工具。

### 与其他阶段的区别

|              | Phase 1.6 数学基础                 | Phase 1.7 教程                 | Phase 1.9 `_math.md` |
| ------------ | ---------------------------------- | ------------------------------ | -------------------- |
| **核心问题** | "这个主题需要哪些数学工具？"       | "教科书怎么推导/证明的？"      | "考试要用哪些公式？" |
| **内容**     | 纯数学定义 + 定理 + 手算练习       | ML 特定的推导过程              | Slides 公式速查      |
| **来源**     | 数学教科书（MML, Grinstead 等）    | ML 教科书（Murphy, Bishop 等） | 课程 Slides          |
| **复用性**   | 跨主题共享（多个主题复用同一文件） | 主题专属                       | 主题专属             |

### 步骤

1. **识别数学依赖**: 读取 Phase 1.5 Storyline，列出本主题用到的数学概念（如 SVM → 内积、拉格朗日乘子）
2. **检查已有文件**: 查看 `courses/math/` 下是否已有对应的数学基础文件
3. **生成缺失文件**: 对于尚未生成的数学基础文件，按 `learning-math_foundations` skill 的模板从教科书提取：
   - 定义 + 定理（带教科书方程编号）
   - 符号对照表（每个公式前）
   - 直觉理解 + 手算例题
   - 课程关联（标注哪些 week 用到）
   - 练习题（从教科书习题提取，分 🟢🟡🔴 三级）
4. **更新 README**: 在 `courses/math/README.md` 中添加新文件条目和依赖关系
5. **添加前置链接**: 在 Storyline 和后续 Tutorial 的头部添加数学前置链接：
   ```markdown
   > **数学前置：** [内积](../../math/linear-algebra/inner_product.md) | [拉格朗日乘子](../../math/optimization/lagrange_multipliers.md)
   ```

### 跳过条件

- 如果 `courses/math/` 下已有本主题所需的所有数学基础文件，跳过生成，只添加前置链接
- 如果主题不涉及新的数学前置（如纯应用型主题），跳过整个 Phase

### 命令

```
读取 skill: .agent/skills/learning-math_foundations/SKILL.md
识别 Storyline 中的数学依赖
检查 courses/math/ 已有文件
生成缺失的数学基础文件
更新 README 和前置链接
```

### 输出

- `courses/math/{discipline}/{topic}.md` — 数学基础文件（可能多个，跨学科）
- `courses/math/README.md` — 更新索引和依赖图

---

## Phase 1.7: 教科书教程 📚

**Skills**: `dev-pdf_processing` (`batch_pdf_to_md.py`), `learning-note_taking`

基于**教科书**（`courses/self-study/`），提供 Slides **未覆盖的数学推导和定理证明**。

### ⚠️ 核心原则：与 Storyline 不重复

Tutorial ≠ "另一个 Storyline"。两者的区分必须严格：

|                      | Phase 1.5 故事线   | **Phase 1.7 教程**                 |
| -------------------- | ------------------ | ---------------------------------- |
| **核心问题**         | "为什么需要？"     | **"教科书怎么推导/证明的？"**      |
| **风格**             | 因果叙事           | **定义 → 定理 → 推导 → 意义**      |
| **内容**             | 概念 + 直觉 + 类比 | **数学公式 + 证明步骤 + 方程编号** |
| **LaTeX**            | 可选               | **必须 — 所有公式用 `$$...$$`**    |
| **与 Slides 的关系** | 重组 Slides 内容   | **补充 Slides 没讲的推导**         |

**每节必须回答：** "_Slides 没讲什么？教科书补充了什么？_"

### 教程结构模版

每节按以下结构组织（不是 Storyline 的叙事结构）：

```
## §N 章节标题
> 📚 Ref: [Book §X.Y](relative_link) — Eq. X.Y–X.Z

### N.1 推导/证明
$$...LaTeX 公式...$$     ← 带教科书方程编号 (Book Eq. X.Y)

### N.2 意义 / Slides 未覆盖的洞察
> ⚠️ **Slides 未强调：** ...
```

末尾添加参考索引表：

```
| 教程章节 | 教科书来源 | 核心内容 | Slides 覆盖？ |
```

### ⚠️ 衔接性规则（Coherence Rules）

生成教程时必须遵守以下规则，避免读者遇到"突然冒出来"的概念：

#### 规则1: 前置概念检查（Prerequisite Check）

每节开始前，检查该节用到的所有概念是否在**前面的章节已经解释过**。如果没有，必须先加一个 §0 前置知识节。

> 📎 **Phase 1.6 衔接：** 纯数学前置（如条件概率、内积、梯度）应已在 `courses/math/` 中由 Phase 1.6 生成。Tutorial 的 §0 只需**链接**到对应的数学基础文件，不需要重新推导。只有 ML 特定的前置概念（如 Phase 1.5 Storyline 中的概念）才需要在 Tutorial 内部解释。

**实例：** Bayes 定理推导（§1）依赖条件概率、联合概率、边缘概率 → 链接到 `courses/math/probability/conditional_probability.md`，不在 Tutorial 内重写。

#### 规则2: 术语首次使用必须解释（Zero-Jargon-Drop Rule）

任何术语（如"似然"、"先验"、"MAP"、"MLE"、"共轭先验"）在文档中**首次出现时**，必须：

1. 给出白话解释（一句话说清楚"这是什么"）
2. 用具体例子对应（最好复用 §0 的贯穿例子）
3. 标注教科书出处（如 "MML §6.3 的术语标注"）

**反面示例：** ❌ "…$p(y \mid x)$（似然）和 $p(x)$（先验）可以直接数出来…" — "似然"和"先验"没有解释就使用了。

#### 规则3: 章节间过渡句（Transition Bridge）

每两个小节之间，必须有一句话解释"**为什么从 A 到 B**"。避免读者产生"怎么突然跳到这个话题"的困惑。

**模版：**

```
[§N 的结论]. 但要实际使用这个结果，还需要解决一个问题：[§N+1 要回答的问题]。
```

**实例：** "Bayes 公式推出来了。但要真的用它算数字，右边三项中 P(y) 不能直接数出来 — 怎么算？"

#### 规则4: 贯穿例子（Running Example）

§0 建立的具体例子（如"班级30个学生"）应在后续章节中**反复复用**，让新公式有具体的数字可以代入验证。

#### 规则5: 教科书引用精确到方程编号（Precise Citation）

每个公式不仅要标注章节（如 "Murphy §9.3"），还要标注**具体的方程编号**（如 "Murphy Eq. 9.46"），让读者能直接翻到原文。

#### 规则6: 命名来源与历史（Name Origin & History）

当教程中出现**以人名命名的概念**（如 "Bayes 定理"、"Laplace 平滑"、"Dirichlet 分布"）或**专门术语**（如 "Prior"、"Likelihood"）时，必须注明：

1. **谁起的名** — 哪位数学家/统计学家提出或命名的
2. **什么时候** — 大致年代
3. **为什么这么叫** — 名字背后的直觉（如 "Prior = '先'于观察的信念"）

**实例：** "数学家给公式里的四个位置起了专门的名字（MML §6.3 的标注，这些名字源自 Laplace 1812 和 Fisher 1921）"

**目的：** 帮助读者建立**元知识** — 不只是记住公式，还知道这些公式和术语从何而来，形成知识的历史脉络。

#### 规则7: 结论必须有证明或出处（Claim-Proof Rule）

教程中**每个结论/公式**都必须满足以下之一：

1. **引用教科书原文证明** — 标注"📚 Book §X.Y"并给出原文的推导步骤
2. **tutorial 自行推导** — 明确标注"📐 推导（tutorial 补充，非教科书原文）"，给出推导过程

**绝不允许：** 给出一个结论（如"参数数 = $v^D - 1$"）但不解释它是怎么来的。

**实例：** Murphy 只说"the model has $O(CD)$ parameters"，但没推导未加朴素假设时需要多少参数。Tutorial 需要补充推导时，必须标注为"tutorial 补充"并给出推导步骤。

> 📎 **Complete Rule:** See `learning-source_citation` SKILL.md for the full citation & proof standard (applies to all learning materials).
> 📎 **完整规则：** 详见 `learning-source_citation` SKILL.md 了解完整的来源引证与证明标准（适用于所有学习资料）。

#### 规则8: 公式前符号对照表（Symbol Legend Rule）

每个公式**首次出现新符号**时，必须在公式前放一个对照表，列出：

1. 符号
2. 含义（白话）
3. 具体例子中对应什么

**模版：**

```
| 符号 | 含义 | 逃税例子中对应 |
|------|------|---------------|
| $y$  | 类别标签 | 逃税？（Yes/No）|
```

**目的：** 读者看到公式时，每个字母都能立刻对到具体的东西，不需要回翻前面找定义。

### 步骤

1. **找出 Slides 的推导缺口**: 对比 Storyline 和 Slides，找出"给了结论但没推导"的公式
2. **识别教科书中的对应推导**: 在 `courses/self-study/` 中找到对应 PDF sections
   - **RL 课程额外资源**: `courses/self-study/rl/david_silver_lectures/` 包含 David Silver 的 10 讲 UCL RL 课程 PDF（L1-L10），可作为 Sutton & Barto 教科书的补充参考
3. **批量转换**: 用 `batch_pdf_to_md.py` 将相关 PDF 转为 .md
   ```bash
   python .agent/skills/dev-pdf_processing/scripts/batch_pdf_to_md.py \
     --root courses/self-study --book murphy_pml1_sections --chapter ch09
   ```
4. **合成教程**: 从 ref 文件提取推导，合成为独立教程文件
   - 按知识依赖排序（基础 → 进阶）
   - 每节引用教科书方程编号（如 Murphy Eq. 9.46）
   - 所有公式用 LaTeX（`$$...$$`）
   - 末尾添加参考索引表（标注"Slides 覆盖？"列）
   - **遵守衔接性规则**（规则1-6）
5. **更新链接**: Storyline 末尾添加 📚 参考资料链接

### 选择资料的原则（三层止挖）

```
第0层：会用公式     ← 必须（考试最低要求，Slides + Cheatsheet 覆盖）
第1层：知道为什么    ← 必须（Storyline 已覆盖）
第2层：看过推导      ← 推荐（Tutorial 覆盖 — 到此为止！）
第3层：理解公理基础  ← 可选（ref 文件自行阅读）
```

### 输出

- **主产出**: `courses/[course]/notes/[topic]_tutorial.md` — 数学推导教程
- **中间产物**: `courses/self-study/.../_sources/[book]_sections/[ch]/[section].md` — ref 文件
- **链接更新**: Storyline 末尾的 📚 参考资料链接表

---

## Phase 1.9: 速查三件套 📋

**Skill**: `learning-cheat_sheet`

基于**老师的资料**（slides + quiz + lab），将所有考试要点拆分为 **3 个聚焦文件**。

### 3-文件拆分架构

| 文件         | 后缀             | 包含                                 | 不包含                    |
| ------------ | ---------------- | ------------------------------------ | ------------------------- |
| **概念速查** | `_cheatsheet.md` | 📖 定义、💡 要点、⚠️ 陷阱、📊 对比表 | ❌ 无公式、无手算、无代码 |
| **数学公式** | `_math.md`       | 📐 公式（带参数解释）、📝 手算题目   | ❌ 无定义、无代码         |
| **代码参考** | `_code.md`       | 🔧 代码模式、imports、API 用法       | ❌ 无定义、无公式         |

### 为什么拆分？

- **概念速查** = 快速查概念 → "什么是X？注意什么？"
- **数学公式** = 公式参考 + 考试手算练习 → "X怎么算？一步步来"
- **代码参考** = lab/作业参考 → "X在Python里怎么实现？"
- 每个文件保持聚焦和小巧 → AI 一次处理一个文件不会溢出
- 考试时只带需要的文件

### 与前面阶段的区别

|              | Storyline  | Tutorial | Cheat Sheet (3件套)       |
| ------------ | ---------- | -------- | ------------------------- |
| **目的**     | 理解       | 深入     | **速查**                  |
| **详细度**   | 叙事展开   | 推导展开 | 极致压缩                  |
| **使用场景** | 课后复习   | 深挖概念 | **考前速查**              |
| **每个概念** | 一段话解释 | 完整推导 | 定义+公式+代码 各一个文件 |

### 步骤

1. 读取 Phase 1 笔记和 Phase 1.5 故事线
2. 交叉检查所有老师资料（slides + quiz + lab）确保覆盖
3. 生成 3 个文件：
   - `[topic]_cheatsheet.md` — 📖 Definition → 💡 Key Points → ⚠️ Traps → 📊 Compare
   - `[topic]_math.md` — 📐 Formula → 📝 Hand Calc → Quick Reference Table
   - `[topic]_code.md` — 🔧 Code patterns
4. 每个文件头部互相链接（See also）
5. 每个 trap 来源标注（slide/quiz/lab）

### 命令

```
读取 skill: .shared/skills/learning-cheat_sheet/SKILL.md
交叉检查: slides + quiz + lab
生成 3 个速查文件
```

### 输出

- `courses/[course]/notes/[topic]_cheatsheet.md` (概念速查)
- `courses/[course]/notes/[topic]_math.md` (数学公式+手算)
- `courses/[course]/notes/[topic]_code.md` (代码参考)

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
├── math/                                        # Phase 1.6: 数学基础（跨主题共享）
│   ├── README.md                                #   索引 + 阅读顺序 + 依赖图
│   ├── linear-algebra/
│   │   └── inner_product.md                     #   内积（SVM W2 前置）
│   └── optimization/
│       └── lagrange_multipliers.md              #   拉格朗日乘子（SVM W2 前置）
│
├── ml/
│   └── notes/
│       ├── week2_svm_slides.md              # Phase 0 + 0.5: 格式化的幻灯片
│       ├── week2_svm_slides_pages/          # Phase 0: 提取的图片
│       ├── week2_svm_storyline.md           # Phase 1.5: 故事线叙事
│       ├── week2_svm_tutorial.md            # Phase 1.7: 教科书教程（独立文件）
│       ├── week2_svm_cheatsheet.md          # Phase 1.9: 概念速查（定义+要点+陷阱+表）
│       ├── week2_svm_math.md               # Phase 1.9: 数学公式+手算
│       ├── week2_svm_code.md               # Phase 1.9: 代码参考
│       ├── week2_svm_complete_demo.py       # Phase 2: 演示脚本
│       ├── week2_svm_complete_demo.ipynb    # Phase 2.5: 演示 Notebook
│       ├── week2_svm_interactive_tutorial.ipynb  # Phase 3: 最终成品
│       └── ../quizzes/
│           └── week2_svm_quiz.md            # Phase 5: 测验题
│
└── self-study/
    └── math/_sources/
        └── mml_sections/ch12/
            ├── sec_12.2_svm.pdf             # 教科书原始 PDF
            └── sec_12.2_svm.md              # Phase 1.7: 教科书笔记（与 PDF 并排）
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

| 维度     | Slides 流程 (Phase 0-5)          | Lab 流程 (Phase L)        |
| -------- | -------------------------------- | ------------------------- |
| 输入     | PPT/PDF slides                   | Lab PDF                   |
| 处理方式 | 格式化 + 深度 Notes              | **仅格式化 + 翻译**       |
| 📝 Notes | ✅ 9 层框架                      | ❌ 不加                   |
| 产出     | 多文件（slides+notes+demo+quiz） | 单文件（格式化的 Lab MD） |
| 何时使用 | 课前预习/课后复习                | 收到 Lab PDF 时           |

---

## 💡 快捷子命令

| 命令                                               | 说明                | 从哪个 Phase 开始 |
| -------------------------------------------------- | ------------------- | ----------------- |
| `/generate-study-material ml svm`                  | 完整流程 (含抓取)   | Phase -1          |
| `/generate-study-material ml svm --no-scrape`      | 完整流程 (跳过抓取) | Phase 0           |
| `/generate-study-material ml svm --from=phase1`    | 从笔记提取开始      | Phase 1           |
| `/generate-study-material ml svm --from=phase1.5`  | 从故事线开始        | Phase 1.5         |
| `/generate-study-material ml svm --from=phase1.55` | 从历史线开始        | Phase 1.55        |
| `/generate-study-material ml svm --from=phase1.6`  | 从数学基础开始      | Phase 1.6         |
| `/generate-study-material ml svm --from=phase1.7`  | 从教科书教程开始    | Phase 1.7         |
| `/generate-study-material ml svm --from=phase1.9`  | 从速查表开始        | Phase 1.9         |
| `/generate-study-material ml svm --from=phase2`    | 从 Demo 开始        | Phase 2           |
| `/generate-study-material ml svm --from=phase2.5`  | 从 .py→.ipynb 开始  | Phase 2.5         |
| `/generate-study-material ml svm --from=phase3`    | 从 NB 合成开始      | Phase 3           |
| `/generate-study-material ml svm --phase=4`        | 只运行审查          | Phase 4           |
| `/generate-study-material ml svm --phase=5`        | 只生成测验题        | Phase 5           |
| `/generate-study-material nlp lab3`                | Lab 格式化+翻译     | Phase L           |

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
- 🕰️ 历史线: `.agent/skills/learning-lecture_history/SKILL.md` — 将技术概念按年代排列，理解演进因果
- 📐 数学基础: `.agent/skills/learning-math_foundations/SKILL.md` — 从教科书提取数学前置知识，每个公式有出处
- 📱 数学公式库: `.shared/skills/math-concept-library/SKILL.md` — 公式的标准解读、直觉类比、分步解读复用库
- 📖 概念术语库: `.shared/skills/concept-glossary/SKILL.md` — 术语定义、历史背景、类比、交叉引用复用库
- 💬 代码注释: `.shared/skills/dev-code_comment/SKILL.md` — 双语代码注释规范，算法/概念注释模板
- 📚 教材搜索: `.shared/skills/learning-textbook_vectorization/SKILL.md` — 17 本教材向量化语义搜索
  - 向量化: `uv run python courses/self-study/vectorize_all.py`
  - 搜索: `uv run python courses/self-study/query_books.py "查询内容"`

> 💡 两个知识库都是**滚雪球式积累**：每次写笔记时查库复用 → 写完后新条目入库 → 下次写笔记时可复用的素材更多
> 💡 `dev-code_comment` 的算法注释模板（术语解释 + 定义/公式/举例/优点）与知识库条目格式互通，确保笔记和代码中的解释一致
> 💡 教材语义搜索提供**多书交叉参考**：遇到概念时搜索多本教材的解释，获取不同角度的理解
