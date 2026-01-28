---
description: Complete course lab/assignment from start to submission - universal workflow for all courses
---

# 📚 课程作业完成工作流 (Universal Lab Workflow)

通用的课程作业完成工作流，适用于所有课程。

## 使用方式

```
/complete-lab [课程] [作业编号] [选项]

示例:
/complete-lab ml lab2
/complete-lab nlp assignment1 --from=code
/complete-lab mv lab3 --check
```

## 8 阶段流程

| Phase | 阶段    | 使用的 Skills                                    |
| ----- | ------- | ------------------------------------------------ |
| 1     | 📥 抓取 | brightspace_scraper                              |
| 2     | 📄 转换 | docx_to_md, pdf_processing                       |
| 3     | 🧠 理解 | note_taking, ai_learning-\*                      |
| 4     | 💻 开发 | code_generation, notebook_conversion             |
| 5     | ✅ 验证 | code_consistency                                 |
| 6     | 📝 文档 | code_screenshot, assignment_document, md_to_docx |
| 7     | 🔍 检查 | lab_submission                                   |
| 8     | 📤 提交 | git                                              |

## 快捷选项

| 选项             | 说明                     |
| ---------------- | ------------------------ |
| `--from=scrape`  | 从抓取开始 (Phase 1)     |
| `--from=convert` | 从转换开始 (Phase 2)     |
| `--from=code`    | 从代码开发开始 (Phase 4) |
| `--from=doc`     | 从文档生成开始 (Phase 6) |
| `--check`        | 只运行检查 (Phase 7)     |

## 支持的课程

ml, nlp, mv, cv, dl, rl

详细说明请参考: `.agent/workflows/complete-lab.md`
