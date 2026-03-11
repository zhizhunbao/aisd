---
name: workflow-creator
description: Create, validate, and optimize agent workflows. Use when (1) creating new workflows, (2) validating existing workflow format and quality, (3) optimizing workflow size/structure, (4) auditing all workflows for consistency, (5) user mentions "workflow" with "check", "validate", "optimize", or "create".
---

# Workflow Creator

Create, validate, and optimize agent workflows (`.md` files in `.agent/workflows/`).

## Workflow Specification

### Required Format

Every workflow file MUST follow this structure:

```markdown
---
description: Short, clear description of what this workflow does
---

[Step-by-step instructions in markdown]
```

### Frontmatter Rules

| Field | Required | Format | Max Length |
|-------|----------|--------|-----------|
| `description` | ✅ Yes | Plain text, one line | 120 chars |

- `description` is the **only** recognized frontmatter field
- Must clearly state **what** the workflow does AND **when** to use it
- Keep it concise — this is shown in the UI slash-command list

### File Naming

- **kebab-case** only: `my-workflow-name.md`
- No underscores, spaces, or uppercase
- Name should match the slash command: `/my-workflow-name`
- Maximum 3-4 words

### Size Limits

| Level | Lines | Recommendation |
|-------|-------|----------------|
| ✅ Ideal | < 200 | Simple, focused workflow |
| ⚠️ Large | 200–500 | Consider splitting into phases |
| 🔴 Oversized | > 500 | Must split or use references |

Oversized workflows should extract detailed content to:
- Other files referenced via `See [reference](path)` links
- Sub-workflows invoked as separate steps
- Skills (for reusable instruction blocks)

### Step Structure

1. **Use numbered steps** — every major action gets a number
2. **One action per step** — don't bundle multiple actions
3. **Be specific** — "Run `npm test`" not "test the code"
4. **Include success criteria** — how to know a step is done
5. **Mark auto-runnable steps** with `// turbo` annotation

### Turbo Annotations

```markdown
// turbo
3. Run the test suite
```

- `// turbo` above a step = safe to auto-run without user approval
- `// turbo-all` anywhere = ALL steps auto-run
- Only use for **non-destructive** steps (read, build, test)
- **Never** turbo: delete, deploy, push, install system deps

### Quality Checklist

A good workflow:

- [ ] Has a clear, concise `description` in frontmatter
- [ ] Uses numbered steps throughout
- [ ] Each step has a single clear action
- [ ] Includes success criteria or expected output
- [ ] Is under 500 lines (or properly split)
- [ ] Uses `// turbo` for safe, repeatable steps
- [ ] References skills where appropriate instead of inlining instructions
- [ ] Has no duplicate logic with other workflows

---

## Creating a New Workflow

### Step 1: Define the scope

Ask: "What repetitive multi-step task does this automate?"

A workflow is NOT:
- A single command → just run it
- Reusable knowledge → make a skill instead
- A one-time task → just do it

A workflow IS:
- A repeatable sequence of 3+ steps
- Something you'd otherwise forget the order of
- Combinable with skills for detailed instructions

### Step 2: Write the workflow

```markdown
---
description: [what it does] - [when to use it]
---

# [Workflow Title]

## Prerequisites
- [What must be true before starting]

## Steps

1. [First action]
   - Expected output: [what success looks like]

// turbo
2. [Safe automated step]

3. [Step requiring judgment]
   - Option A: [if condition X]
   - Option B: [if condition Y]

## Verification
- [ ] [Final check 1]
- [ ] [Final check 2]
```

### Step 3: Validate

Run the validation script:

```bash
python .agent/skills/workflow-creator/scripts/validate_workflows.py .agent/workflows
```

---

## Validating Workflows

Run `scripts/validate_workflows.py` to check all workflows for:

- Frontmatter presence and format
- Description quality (length, clarity)
- File naming convention
- Line count warnings
- Step numbering consistency
- Turbo annotation safety
- Duplicate/similar workflow detection

---

## Optimizing Oversized Workflows

For workflows > 500 lines:

1. **Extract skill references** — if a workflow contains detailed "how to" instructions, move them to a skill and reference it: `Follow the [skill-name] skill for this step`
2. **Split into phases** — break into `phase-1-setup.md`, `phase-2-execute.md`, etc.
3. **Use sub-workflows** — "Run `/sub-workflow` to complete this section"
4. **Remove redundancy** — if two workflows share steps, extract shared steps into a common workflow or skill
