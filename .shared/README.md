# Shared Configuration Hub

This directory is the **single source of truth** for AI agent configurations across all platforms.

## Directory Structure

```
.shared/
├── rules.md          # 共享规则（核心配置）
├── skills/           # Skills 库（112+ skills）
├── prompts/          # Prompt 模板
└── commands/         # 共享命令/工作流
```

## Supported Platforms

| Platform        | Config Location  | How It References .shared/         |
| --------------- | ---------------- | ---------------------------------- |
| **Claude Code** | `.claude/`       | `CLAUDE.md` includes rules         |
| **Antigravity** | `.agent/`        | Symlink to `.shared/skills/`       |
| **Kiro**        | `.kiro/`         | `steering/` copies from `rules.md` |
| **Windsurf**    | `.windsurfrules` | Copies from `rules.md`             |

## How to Add New Skills

1. Create skill directory in `.shared/skills/[category]-[name]/`
2. Add `SKILL.md` with frontmatter (name, description)
3. Add supporting files as needed

## How to Add New Commands

1. Create command file in `.shared/commands/[name].md`
2. Follow platform-specific format:
   - **Claude Code**: `$ARGUMENTS` for parameters
   - **Antigravity**: YAML frontmatter with `description`
   - **Kiro**: Agent hooks format
   - **Windsurf**: Rules format

## Syncing Across Platforms

When you update `.shared/rules.md`, manually update:

- `.claude/CLAUDE.md`
- `.kiro/steering/project.md`
- `.windsurfrules`

Or use the `/sync-config` command (if available).
