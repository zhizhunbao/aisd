---
name: learning-logic_consistency
description: Review learning materials for logical flow, conceptual continuity, and "Why-First" explanations. Use to ensure tutorials are beginner-accessible and free of "magic" leaps.
---

# Learning Logic Consistency

## Objectives

Ensure that learning materials (Notes, Tutorials, Notebooks) follow a linear, logical path where every concept is justified, explained before used, and flows naturally.

## Review Criteria

### 1. The "Zero Leap" Rule
- **Check**: Does the content introduce a technical term, acronym, or code library without a prior plain-English explanation?
- **Correction**: If "SVM" appears, ensure "Support Vector Machine" and the concept of "finding the widest path" were explained in the preceding paragraph.

### 2. The "IO & Parameter" Transparency Rule
- **Check (Input)**: Is it clear what data is being "fed" into the model? (e.g., "We are giving the model the X coordinates and the Y labels").
- **Check (Output)**: Is the result of the code explained? What does the return value actually mean in the physical world?
- **Check (Parameters)**: Is every "magic" parameter (like `C`, `gamma`, `random_state`) explained? 
    - *Bad*: `SVC(C=1.0)`
    - *Good*: "We set `C=1.0`. Think of C as a 'strictness' dial. 1.0 is the default balance."
- **Correction**: Add a "Parameter Table" or explicit "Input/Output" description for every major code block.

### 3. The "Why-First" Principle
- **Check**: Does the tutorial say "Do X" without explaining *why* we are doing X?
- **Check (Code)**: Is there a "Magic Number" or a parameter (like `C=1.0`) that isn't explained in terms of its impact on the result?
- **Correction**: Prepend every action with its motivation. "Because real-world data is messy, we need to allow some errors. We do this by adjusting the 'C' parameter..."

### 3. Conceptual Dependency Chain
- **Check**: Does Step B depend on a concept that was only introduced in Step C?
- **Correction**: Reorder content so that the "Foundation" always precedes the "Application".

### 4. Code-Theory Synchronization
- **Check**: Does the code use variable names or logic that contradict the terminology used in the text?
- **Correction**: Align names. If the text calls it "Safety Gap", the code comment shouldn't just call it "margin" without linking the two.

### 5. Transition Verification
- **Check**: Is there a "Cliffhanger" between sections where the reader might get lost? (e.g., jumping from simple lines to complex 3D math).
- **Correction**: Add "Bridge sentences". (e.g., "Now that we know how to handle straight lines, what happens when the data forms a circle? This is where the 'Kernel' comes in.")

## Implementation Workflow (Self-Review)

Before finalizing any learning package, perform this 3-point check:
1. **The "Newbie Test"**: If I didn't know the title of this page, would I understand the second paragraph?
2. **The "Why" Audit**: Search for every code block. Is the paragraph above it explaining the *problem* the code is solving?
3. **The Acronym Scan**: Search for all-caps words. Are they all defined at their first occurrence?

## Language Tone
- Encouraging, pedagogical, and clear.
- Use analogies (e.g., "修路", "魔法转换", "惩罚旋钮") to ground abstract math.
