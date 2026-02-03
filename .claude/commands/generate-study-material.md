Transform raw course materials (PPT/PDF) into an interactive Jupyter Notebook learning package.

$ARGUMENTS: [course] [topic] [--from=phaseN] [--phase=N]

Examples:

- /generate-study-material ml svm
- /generate-study-material ml decision_tree --from=phase2
- /generate-study-material nlp transformer --phase=0

## 5-Phase Workflow

| Phase | Name      | Skills Used                                        |
| ----- | --------- | -------------------------------------------------- |
| 0     | Convert   | dev-pptx_to_pdf, dev-pdf_processing               |
| 1     | Extract   | learning-note_taking                               |
| 2     | Demo      | learning-code_generation                           |
| 3     | Synthesize| learning-notebook_conversion                       |
| 4     | Review    | learning-logic_consistency, learning-code_consistency |

## Shortcuts

- `--from=phase0` → Start from PPTX/PDF conversion (Phase 0)
- `--from=phase1` → Start from note extraction (Phase 1)
- `--from=phase2` → Start from demo script (Phase 2)
- `--from=phase3` → Start from notebook synthesis (Phase 3)
- `--phase=N` → Only run specified phase

## Supported Courses

ml, nlp, mv, cv, dl, rl

## Execution

Read and follow the detailed workflow: `.agent/workflows/generate-study-material.md`
Read skill specifications: `.shared/skills/learning-automated_study_material/SKILL.md`
