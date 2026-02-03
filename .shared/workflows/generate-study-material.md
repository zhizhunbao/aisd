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
│ Phase 0: 转换 (Convert)                                      │
│   ↓ dev-pptx_to_pdf, dev-pdf_processing skills              │
├─────────────────────────────────────────────────────────────┤
│ Phase 1: 提取 (Extract)                                      │
│   ↓ learning-note_taking skill                              │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: 演示 (Demo)                                         │
│   ↓ learning-code_generation skill                          │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: 合成 (Synthesize)                                   │
│   ↓ learning-notebook_conversion skill                      │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: 审查 (Review)                                       │
│   ↓ learning-logic_consistency, learning-code_consistency   │
└─────────────────────────────────────────────────────────────┘
```

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

## Phase 1: 概念提取 🧠

**Skill**: `learning-note_taking`

将提取的 Markdown 总结为结构化学习笔记。

### 步骤

1. 读取 Phase 0 输出的 `[topic]_slides.md`
2. 总结为 `[topic]_notes.md`
3. 用初学者友好的语言，所有首字母缩写在首次出现时定义
4. 双语标题，中文笔记
5. 对照原始 slides 图片确保图表和视觉概念被描述

### 命令

```
读取 skill: .shared/skills/learning-note_taking/SKILL.md
总结为笔记
```

### 输出

- `courses/[course]/notes/[topic]_notes.md`

---

## Phase 2: 实现演示 💻

**Skill**: `learning-code_generation`

基于笔记生成独立可运行的 Python 演示脚本。

### 步骤

1. 创建 `courses/[course]/notes/[topic]_complete_demo.py`
2. 用合成数据实现核心算法（`sklearn.datasets`, `numpy`）
3. 可视化保存到 `[topic]_complete_demo_pages/`
4. 使用 `os.path.join(os.path.dirname(os.path.abspath(__file__)), ...)` 确保路径安全
5. 运行脚本，验证逻辑与 Phase 1 理论一致

### 命令

```
读取 skill: .shared/skills/learning-code_generation/SKILL.md
生成演示脚本
运行验证
```

### 输出

- `courses/[course]/notes/[topic]_complete_demo.py`
- `courses/[course]/notes/[topic]_complete_demo_pages/`

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

## 🗂️ 目录结构示例

```
courses/
└── ml/
    └── notes/
        ├── svm_slides.md                   # Phase 0: 原始提取
        ├── svm_slides_images/              # Phase 0: 提取的图片
        │   ├── slide1_img1.png
        │   └── slide2_img1.png
        ├── svm_notes.md                    # Phase 1: 理论笔记
        ├── svm_complete_demo.py            # Phase 2: 演示脚本
        ├── svm_complete_demo_pages/        # Phase 2: 参考图片
        │   ├── svm_demo_plot1.png
        │   └── svm_demo_plot2.png
        └── svm_interactive_tutorial.ipynb   # Phase 3: 最终成品
```

---

## 💡 快捷子命令

| 命令                                         | 说明              | 从哪个 Phase 开始 |
| -------------------------------------------- | ----------------- | ----------------- |
| `/generate-study-material ml svm`            | 完整流程          | Phase 0           |
| `/generate-study-material ml svm --from=phase1` | 从笔记提取开始 | Phase 1           |
| `/generate-study-material ml svm --from=phase2` | 从 Demo 开始   | Phase 2           |
| `/generate-study-material ml svm --from=phase3` | 从 NB 合成开始 | Phase 3           |
| `/generate-study-material ml svm --phase=4`  | 只运行审查        | Phase 4           |

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

详细规范请参考: `.shared/skills/learning-automated_study_material/SKILL.md`
