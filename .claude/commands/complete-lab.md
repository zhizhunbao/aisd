Complete course lab/assignment from start to submission.

$ARGUMENTS: [course] [lab_number] [--from=phase] [--check]

Examples:

- /complete-lab ml lab2
- /complete-lab nlp assignment1
- /complete-lab ml lab2 --from=code
- /complete-lab mv lab3 --check

## 8-Phase Workflow

| Phase | Name       | Skills Used                                      |
| ----- | ---------- | ------------------------------------------------ |
| 1     | Scrape     | brightspace_scraper                              |
| 2     | Convert    | docx_to_md, pdf_processing                       |
| 3     | Understand | note_taking, ai_learning-\*                      |
| 4     | Develop    | code_generation, notebook_conversion             |
| 5     | Verify     | code_consistency                                 |
| 6     | Document   | code_screenshot, assignment_document, md_to_docx |
| 7     | Check      | lab_submission                                   |
| 8     | Submit     | git                                              |

## Shortcuts

- `--from=scrape` → Start from Phase 1
- `--from=convert` → Start from Phase 2
- `--from=code` → Start from Phase 4
- `--from=doc` → Start from Phase 6
- `--check` → Only run Phase 7

## Supported Courses

ml, nlp, mv, cv, dl, rl
