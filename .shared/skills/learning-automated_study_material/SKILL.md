---
name: learning-automated_study_material
description: Transform raw course materials (PPT/PDF) into an interactive Jupyter Notebook learning package. Orchestrates note extraction, demo scripting, notebook synthesis, and quality review.
---

# Learning Automated Study Material

## Objectives

Create a seamlessly integrated learning experience from raw lecture materials (PPT/PDF) to an executed, result-rich interactive tutorial that is accessible to beginners.

## Workflow (6 Phases)

### Phase -1: Material Scraping (Brightspace -> Local)

**Uses:** `learning-brightspace_scraper`

Automate downloading of slides and resources from Brightspace LMS.

- Check `scraper/config.py` for correct `course_id`.
- Run scraper to fetch `slides` module for the target topic.
- Move downloaded files from `data/` to `courses/[course]/slides/`.

**Output:** `courses/[course]/slides/[topic].pdf`

### Phase 0: Material Conversion (PPTX/PDF -> Markdown)

**Uses:** `dev-pptx_to_pdf` + `dev-pdf_processing`

Raw course materials (PPTX/PDF) must be converted to readable markdown before note-taking.

- **If PPTX**: Convert to PDF first using `dev-pptx_to_pdf`, then proceed as PDF.
- **If PDF**: Convert to markdown using `dev-pdf_processing` (`pdf_to_md_hybrid.py` recommended for slides).
- Extract embedded images into `courses/[course]/notes/[topic]_slides_images/`.
- Verify the extracted markdown captures all text, formulas, and diagram descriptions.
- If the source is already readable (e.g., plain text, existing markdown), skip this phase.

**Output:** `[topic]_slides.md` + `[topic]_slides_images/`

### Phase 1: Conceptual Extraction (`*_slides.md` -> `*_notes.md`)

**Uses:** `learning-note_taking`

- Summarize the extracted markdown (from Phase 0) into `courses/[course]/notes/[topic]_notes.md`.
- Use beginner-friendly language and define all acronyms at first occurrence.
- Focus on definitions, formulas, and key logic. Use bilingual headers but Chinese notes.
- Cross-reference with original slides images to ensure diagrams and visual concepts are described.

**Output:** `[topic]_notes.md`

### Phase 2: Implementation Demo (`*_notes.md` -> `*_complete_demo.py`)

**Uses:** `learning-code_generation`

- Create a standalone Python script `courses/[course]/notes/[topic]_complete_demo.py`.
- Implement the core algorithms using synthetic data (`sklearn.datasets`, `numpy`) so it runs without external dependencies.
- Save all visualizations to a dedicated folder `[topic]_complete_demo_pages/`.
- Use `os.path.join(os.path.dirname(os.path.abspath(__file__)), ...)` for path safety.
- Verify the script runs end-to-end and the logic matches the theory from Phase 1.

**Output:** `[topic]_complete_demo.py` + `[topic]_complete_demo_pages/`

### Phase 3: Interactive Synthesis (`*_complete_demo.py` -> `*_interactive_tutorial.ipynb`)

**Uses:** `learning-notebook_conversion`

- Merge theory (Phase 1) and code (Phase 2) into an interactive Jupyter Notebook.
- Cell structure for each concept:
  1. **Markdown Cell**: Brief introduction + simple explanation of the problem.
  2. **Markdown Cell**: Theory (from Phase 1) + defined terms.
  3. **Code Cell**: Implementation code (from Phase 2).
  4. **Code Cell**: Visualization code to show results inline.
  5. **Markdown Cell**: "What to try" section (encourage changing parameters like `C`, `gamma`, etc.).
- Apply the **Zero Acronym Policy**: explain the concept in plain language before using technical terms.
- Ensure all plots display inline (`%matplotlib inline` or `plt.show()`).

**Output:** `[topic]_interactive_tutorial.ipynb`

### Phase 4: Execution, Verification & Review

**Uses:** `learning-logic_consistency` + `learning-code_consistency`

This phase combines execution verification and quality review into a single pass.

#### 4a. Execution Verification

- Run all notebook cells from top to bottom to ensure outputs are pre-populated.
- Confirm the notebook is self-contained (no missing imports, no external file dependencies).

#### 4b. Logic Consistency Review (`learning-logic_consistency`)

- **Zero Leap Rule**: No technical term, acronym, or library appears without a prior plain-English explanation.
- **IO & Parameter Transparency**: Every code block has clear Input/Output descriptions; every "magic" parameter (like `C=1.0`) is explained.
- **Why-First Principle**: Every action is preceded by its motivation.
- **Conceptual Dependency Chain**: Foundation always precedes application.
- **Code-Theory Synchronization**: Variable names and logic align with terminology in the text.
- **Transition Verification**: No "cliffhanger" jumps between sections; bridge sentences connect topics.

#### 4c. Code & Asset Consistency Review (`learning-code_consistency`)

- Code logic in the notebook matches the demo script from Phase 2.
- All image references are valid (relative paths, no broken links).
- Statistical values and outputs are consistent across files.

#### 4d. Final Checklist

- [ ] No "magic numbers" in code without "Why" in text.
- [ ] No acronyms (MMC, SVC, RBF, etc.) without full names and analogies.
- [ ] Every code block has a "Motivation" paragraph above it.
- [ ] Input and Output of each code block are clearly identifiable.
- [ ] Zero Acronym Policy: explain before naming.
- [ ] Notebook runs from top to bottom without errors.
- [ ] No `TODO`s, placeholders, or generic summaries remain.

### Phase 5: Quiz Generation (`*_notes.md` + `*_complete_demo.py` -> `*_quiz.md`)

**Uses:** `learning-quiz_generation`

- Analyze the generated notes and demo code to create a comprehensive self-assessment.
- Generate at least 5 MCQ and 5 T/F questions.
- Include 1-2 coding-related short answer questions.
- Format based on the standard `courses/[course]/quizzes/` template.
- Include an Answer Key at the end of the file.

**Output:** `courses/[course]/quizzes/[topic]_quiz.md`

## Key Principles

1. **Accessibility First**: Write for a student seeing the topic for the first time. Avoid "leaps of logic".
2. **Visual Evidence**: Every theoretical claim should be backed by a generated plot in the notebook.
3. **Clean House**: No scattered files. Keep binaries/images in subfolders.
4. **No Placeholders**: The result should be "distribution-ready".

## Output File Structure

```text
courses/[course]/
├── slides/
│   └── [topic].pdf                      # Phase -1: Downloaded source
└── notes/
    ├── [topic]_slides.md                   # Phase 0: Raw extraction from PPTX/PDF
├── [topic]_slides_images/              # Phase 0: Extracted slide images
│   ├── slide1_img1.png
│   └── slide2_img1.png
├── [topic]_notes.md                    # Phase 1: Theory (Summarized)
├── [topic]_complete_demo.py            # Phase 2: Code (Validation Script)
├── [topic]_complete_demo_pages/        # Phase 2: Assets (Reference Images)
│   ├── [topic]_demo_plot1.png
│   └── [topic]_demo_plot2.png
├── [topic]_interactive_tutorial.ipynb   # Phase 3: The Final Experience
└── ../quizzes/
    └── [topic]_quiz.md                 # Phase 5: Knowledge Assessment
```
