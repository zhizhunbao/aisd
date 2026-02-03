---
description: Transform raw course materials (PPT/PDF) into an interactive Jupyter Notebook learning package
---

# 📖 自学材料生成工作流 (Generate Study Material)

将课程原始 PPT/PDF 转换为可交互的 Jupyter Notebook 教程。

## 使用方式

```
/generate-study-material [课程] [主题]

示例:
/generate-study-material ml svm
/generate-study-material ml decision_tree --from=phase2
/generate-study-material nlp transformer --phase=0
```

## 5 阶段流程

| Phase | 阶段         | 使用的 Skills                            |
| ----- | ------------ | ---------------------------------------- |
| 0     | 📄 转换      | dev-pptx_to_pdf, dev-pdf_processing      |
| 1     | 🧠 提取笔记  | learning-note_taking                     |
| 2     | 💻 生成 Demo | learning-code_generation                 |
| 3     | 📓 合成 NB   | learning-notebook_conversion             |
| 4     | ✅ 审查验证   | learning-logic_consistency, learning-code_consistency |

## 快捷选项

| 选项             | 说明                             |
| ---------------- | -------------------------------- |
| `--from=phase0`  | 从 PPTX/PDF 转换开始 (Phase 0)  |
| `--from=phase1`  | 从笔记提取开始 (Phase 1)        |
| `--from=phase2`  | 从 Demo 脚本开始 (Phase 2)      |
| `--from=phase3`  | 从 Notebook 合成开始 (Phase 3)  |
| `--phase=N`      | 只运行指定 Phase                 |

## 支持的课程

ml, nlp, mv, cv, dl, rl

详细说明请参考: `.shared/skills/learning-automated_study_material/SKILL.md`
