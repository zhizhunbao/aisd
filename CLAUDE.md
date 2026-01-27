# Claude Code Configuration

## Skills Directory

Skills are located in `.skills/` directory. Available skills:

- `dev-code_comment`: Bilingual code commenting (Chinese & English)

## Usage

To use a skill, reference it by name or invoke with `/skill-name`.

### Code Comment Skill

Use `/code-comment` or mention "add bilingual comments" to apply the code commenting rules:

- File docstring: English only
- Function docstring: Chinese block + `----` + English block
- Inline comments: Chinese first, `#`, then English
- Section dividers: English only

See `.skills/dev-code_comment/SKILL.md` for full documentation.
