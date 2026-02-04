---
name: learning-quiz_generation
description: Generate comprehensive quizzes (MCQ, True/False, Short Answer) based on study notes and demo code to test student understanding.
---

# Learning Quiz Generation

## Objectives

Create a high-quality assessment tool that covers both theoretical concepts and practical code implementation from the study materials.

## Workflow

1.  **Analyze Source Material**: Read `[topic]_notes.md` and `[topic]_complete_demo.py`.
2.  **Search for Teacher Quizzes**: Check `courses/[course]/quizzes/` for existing files that might contain teacher-provided questions for the same topic (e.g., `quizzes1.md`, `quize2.md`).
3.  **Identify Key Concepts**: Compare existing teacher questions with the new study material. Identify gaps where code-related or deeper conceptual questions are needed.
4.  **Generate/Incorporate Questions**:
    -   **Incorporate**: Start with the teacher-provided questions if valid.
    -   **Generate MCQ**: Add questions to reach at least 5-10 MCQ total. Focus on bridging the gap between theory and the implementation in `complete_demo.py`.
    -   **Generate T/F**: Add at least 5 T/F questions testing common misconceptions found in the notes.
    -   **Generate Short Answer/Coding**: 1-2 questions asking about specific parameter changes in the demo code.
5.  **Format Output**:
    -   Use the format observed in existing quiz files (Question number, options).
    -   Include an **Answer Key** section at the bottom (hidden or in a separate block).
5.  **Save File**: `courses/[course]/quizzes/[topic]_quiz.md`.

## Quality Standards

- **Alignment**: Questions must be directly answerable using the generated notes, demo, or referenced teacher material.
- **Teacher-First**: If teacher-provided questions exist, they MUST be included and prioritized.
- **Clarity**: Questions must be unambiguous and use the terms defined in the notes.
-   **Bilingual**: Questions should be in English (matching the course format) but can include Chinese hints if the topic is complex.
-   **Zero Leap**: No questions on topics not covered in the provided notes.

## Example Format

```markdown
Question 1 (1 point)
[Question Text]

Question 1 options:
A) ...
B) ...
C) ...
D) ...

Question 2 (1 point)
[Statement for True/False]

Question 2 options:
True
False

...

## Answer Key
1. C
2. True
...
```
