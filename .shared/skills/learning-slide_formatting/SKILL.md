---
name: learning-slide_formatting
description: Format raw PDF-to-MD slide extractions into clean, structured lecture notes. Use after pdf_processing and before note_taking. Handles section numbering, bilingual headings, image references, and content cleanup.
---

# Slide Formatting

## Objectives

Transform raw PDF/PPT-to-Markdown output into clean, well-structured lecture notes suitable for study and note-taking.

## When to Use

This skill sits **between** `dev-pdf_processing` (Phase 0) and `learning-note_taking` (Phase 1) in the `generate-study-material` workflow:

```
PDF/PPT → [dev-pdf_processing] → raw .md → [THIS SKILL] → formatted .md → [learning-note_taking] → notes added
```

## Input → Output

| Input                              | Output                             |
| ---------------------------------- | ---------------------------------- |
| Raw `*_slides.md` from PDF extract | Clean, formatted `*_slides.md`     |
| Page-by-page dump with artifacts   | Logical sections with proper heads |
| Broken image refs, raw text        | Clean images, structured bullets   |

## Instructions

### 1. Document Header

Every formatted file MUST start with a metadata header:

```markdown
# Week N: 中文标题 (English Title)

> Source: `Original_Filename.pptx`
> Total slides: NN
> Instructor: Name | Date
```

Rules:
- Week number from filename or content
- Bilingual title: Chinese first, English in parentheses
- Source filename in backticks
- Slide count from the PDF page count
- Instructor name and date from first/last slide

### 2. Section Structure

Organize content into **logical sections** (NOT one-per-slide):

```markdown
---

## 1. 中文标题 (English Title)

- Bullet point content
- Key concepts in **bold**

![Alt text](images_folder/slideNN_imgN.ext)
```

Rules:
- **Numbered sections**: `## 1.`, `## 2.`, etc.
- **⚠️ Subsections are MANDATORY** when a `##` section groups **2 or more slides** that cover distinguishable sub-topics. Use `### N.1`, `### N.2`, etc. with bilingual titles.
  - **Trigger:** The section contains multiple slides, each with a different subtitle or focus (e.g., "Sigmoid", "Tanh", "ReLU" under "Activation Functions", or "Collection", "Preprocessing", "Augmentation" under "Dataset Preparation")
  - **Skip:** If the section has only 1 slide, or all slides cover the same single concept without sub-divisions, no `###` is needed
  - Example: `## 5. 激活函数 (Activation Functions)` → `### 5.1 概述 (Overview)` / `### 5.2 Sigmoid 函数` / `### 5.3 Tanh 函数` / `### 5.4 ReLU 函数`
- **Bilingual section headers**: Chinese first, English in parentheses
- **Horizontal rule** `---` before each `##` section (NOT before `###`)
- **Group related slides** into one section (don't create a section per slide)
- **Last section**: Always include "下周预告 (Next Week Preview)" if present

### 3. Content Formatting

#### Bullet Points
- Convert slide text into clean bullet points
- **⚠️ Fidelity Rule: Preserve original PPT/PDF text verbatim** — do NOT paraphrase, shorten, or restructure the slide text. The English content must be an exact transcription of what appears on the slide
- Highlight key terms with **bold** (matching any colored/emphasized text on the slide)
- Use numbered lists for sequential steps or processes
- Remove slide artifacts (page numbers, headers/footers, repeated titles)

#### Images

**⚠️ RULE: Image First (图片在前)**

- **Images (PPT screenshots) MUST appear BEFORE their explanatory text**
- Reading flow: See the slide → Read the explanation → See notes
- **NEVER stack multiple images together** without text in between
- Each image should have its own brief description or explanation below it
- Keep ALL images from the extraction (these are teacher's PPT slides — do not delete)
- Reference format: `![Description](folder/slideNN_imgN.ext)` or `![Page N](folder/page_NNN.png)`

**✅ GOOD — image before text, each image has its own explanation:**

```markdown
![Page 10](week6_slides_pages/page_010.png)

**Well-separated:** Every point closer to its cluster than to any other cluster

![Page 11](week6_slides_pages/page_011.png)

**Prototype-based:** Each point closer to the centroid of its cluster than to any other centroid
```

**❌ BAD — images stacked together, text summarized separately:**

```markdown
- Well-separated: ...
- Prototype-based: ...

![Page 10](week6_slides_pages/page_010.png)
![Page 11](week6_slides_pages/page_011.png)
```

#### Tables
- Preserve tables in Markdown format
- Align columns for readability

#### Code/Formulas
- Wrap code in fenced code blocks with language tag
- Display formulas in inline code or LaTeX when appropriate

### 4. Content Cleanup

Remove or fix these common PDF extraction artifacts:

| Artifact                    | Action                              |
| --------------------------- | ----------------------------------- |
| Repeated slide titles       | Keep first occurrence only          |
| Page numbers                | Remove entirely                     |
| `## Page N` / `## Slide N`  | Replace with logical section heads  |
| Empty lines / extra spaces  | Normalize to single blank lines     |
| Broken bullet points        | Merge into proper list items        |
| Raw text dumps              | Structure into bullets or paragraphs|
| Duplicate images            | Keep one, remove duplicates         |
| Header/footer text          | Remove unless it's content          |

### 5. Note Placeholders

After formatting, add empty `📝 Notes:` blocks where notes should go. These serve as insertion points for the `learning-note_taking` skill.

```markdown
> **📝 Notes:**
>
> _(To be added by note_taking skill)_
```

Place one note block after each **major concept or section** — typically:
- After each `##` section's content (before the next `---`)
- After significant subsections with enough depth
- NOT after every minor bullet point or trivial slide

**Guideline:** Aim for 6-12 note blocks per file, matching the number of distinct concepts.

### 6. Reference Links

If the slide mentions references or URLs:

```markdown
Ref: https://example.com/docs
```

Place reference links near the related content, not at the end.

## Quality Checklist

Before finalizing formatting:

- [ ] Document has proper header (title, source, slides, instructor)
- [ ] Sections are numbered and have bilingual headers
- [ ] All meaningful images are referenced and paths are correct
- [ ] **Images appear BEFORE their explanatory text** (Image First rule)
- [ ] **No stacked images** — each image has its own description text below
- [ ] No raw PDF artifacts remain (page numbers, slide headers)
- [ ] Related slides are grouped into logical sections
- [ ] Bullet points are clean and properly structured
- [ ] Tables are properly formatted in Markdown
- [ ] `📝 Notes:` placeholders are positioned at major concepts
- [ ] Horizontal rules separate major sections
- [ ] File reads as a coherent study document, not a slide dump

## Example: Before and After

### Before (raw PDF extraction)

```markdown
## Page 3

Fundamentals of Image Processing
Image Processing is the building block of Machine Vision

## Page 4

Why Image Processing in Machine Vision:
Enhancement: Reduces noise
Feature Extraction: Identifies edges
Segmentation: Divides image

![Image](images/slide03_img1.jpg)
![Image](images/slide04_img1.jpg)

---

## Page 5

Key Stages of Digital Image Processing
Nine stages (not all required):
```

### After (formatted)

```markdown
# Week 2: 图像处理基础 (Fundamentals of Image Processing)

> Source: `Week 2 - Fundamentals of Image Processing.pptx`
> Total slides: 24
> Instructor: Stephin Rachel Thomas | 22-01-2026

---

## 1. 图像处理简介 (Introduction to Image Processing)

![Picture 4](week2_image_processing_slides_images/slide03_img1.jpg)

- Image Processing is the building block of Machine Vision
- Involves manipulation and analysis of images

![Picture 5](week2_image_processing_slides_images/slide04_img1.jpg)

**Why Image Processing in Machine Vision:**

- **Enhancement:** Reduces noise, enhances contrast, sharpens details
- **Feature Extraction:** Identifies edges, corners, textures
- **Segmentation:** Divides image into meaningful regions

> **📝 Notes:**
>
> _(To be added by note_taking skill)_

---

## 2. 图像处理阶段 (Key Stages)

Nine stages (not all required for every task):

1. **Acquisition** — Camera/sensor capture
2. **Enhancement** — Improve quality, reveal hidden details
3. **Restoration** — Remove noise/degradation
...
```

## File Naming Convention

| Type                | Pattern                          | Example                              |
| ------------------- | -------------------------------- | ------------------------------------ |
| Formatted slides    | `week{N}_{topic}_slides.md`      | `week2_image_processing_slides.md`   |
| Image folder        | `week{N}_{topic}_slides_images/` | `week2_image_processing_slides_images/` |
| Separate notes file | `week{N}_{topic}_notes.md`       | `week2_image_processing_notes.md`    |
