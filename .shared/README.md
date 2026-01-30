# Shared Configuration Hub

This directory is the **single source of truth** for AI agent configurations across all platforms.

## Directory Structure

```
.shared/
├── rules.md          # 共享规则（核心配置）
├── skills/           # Skills 库（130+ skills）
├── agents/           # Agent 定义（9 agents）
├── workflows/        # 工作流（10+ workflows）
├── templates/        # 模板文件
├── prompts/          # Prompt 模板
└── commands/         # 共享命令
```

## Agents (来自 BMAD-METHOD)

| Agent | 角色 | 文件 |
|-------|------|------|
| `analyst` | 需求分析师 | `analyst.agent.yaml` |
| `pm` | 产品经理 | `pm.agent.yaml` |
| `architect` | 架构师 | `architect.agent.yaml` |
| `dev` | 开发者 | `dev.agent.yaml` |
| `sm` | Scrum Master | `sm.agent.yaml` |
| `tea` | 测试工程师 | `tea.agent.yaml` |
| `ux-designer` | UX 设计师 | `ux-designer.agent.yaml` |
| `tech-writer` | 技术作者 | `tech-writer/` |
| `quick-flow-solo-dev` | 独立开发者 | `quick-flow-solo-dev.agent.yaml` |

## Workflows (来自 BMAD-METHOD)

| 阶段 | 工作流目录 | 包含内容 |
|------|-----------|----------|
| 1-分析 | `1-analysis/` | create-product-brief, research |
| 2-规划 | `2-plan-workflows/` | create-prd, create-ux-design |
| 3-方案 | `3-solutioning/` | create-architecture, create-epics-and-stories |
| 4-实现 | `4-implementation/` | dev-story, code-review, sprint-planning |
| 快速流程 | `bmad-quick-flow/` | 快速开发全流程 |
| 文档 | `document-project/` | 项目文档生成 |
| 测试 | `testarch/` | 测试架构 |

## New Dev Skills (来自 claude-skills)

### 工程团队 Skills
| Skill | 用途 |
|-------|------|
| `dev-senior_architect` | 架构设计 |
| `dev-senior_backend` | 后端开发 |
| `dev-senior_frontend` | 前端开发 |
| `dev-senior_fullstack` | 全栈开发 |
| `dev-senior_data_engineer` | 数据工程 |
| `dev-senior_devops` | DevOps |
| `dev-senior_qa` | 质量保证 |
| `dev-senior_security` | 安全 |
| `dev-code_reviewer` | 代码审查 |
| `dev-tdd_guide` | TDD 指南 |
| `dev-tech_stack_evaluator` | 技术栈评估 |

### 标准 Skills
| Skill | 用途 |
|-------|------|
| `dev-quality_standards` | 质量标准 |
| `dev-security_standards` | 安全标准 |
| `dev-documentation_standards` | 文档标准 |
| `dev-communication_standards` | 沟通标准 |

### 产品团队 Skills
| Skill | 用途 |
|-------|------|
| `dev-product_manager` | 产品管理 |
| `dev-ux_designer` | UX 设计 |

## Templates (来自 spec-kit)

| 模板 | 用途 |
|------|------|
| `spec-template.md` | 规格文档模板 |
| `plan-template.md` | 技术方案模板 |
| `tasks-template.md` | 任务分解模板 |
| `checklist-template.md` | 检查清单模板 |
| `agent-file-template.md` | Agent 定义模板 |
| `spec-driven.md` | Spec-Driven 方法论 |

## Supported Platforms

| Platform        | Config Location  | How It References .shared/         |
| --------------- | ---------------- | ---------------------------------- |
| **Claude Code** | `.claude/`       | `CLAUDE.md` includes rules         |
| **Antigravity** | `.agent/`        | Symlinks to `.shared/*`            |
| **Kiro**        | `.kiro/`         | `steering/` copies from `rules.md` |
| **Windsurf**    | `.windsurfrules` | Copies from `rules.md`             |
| **Cursor**      | `.cursorrules`   | Copies from `rules.md`             |

## .agent Symlinks

`.agent/` 目录通过 symlinks 指向 `.shared/`：

```
.agent/
├── skills -> .shared/skills
├── agents -> .shared/agents
├── workflows -> .shared/workflows
└── templates -> .shared/templates
```

## How to Use Workflows

### 完整开发流程
```
/product-brief → /create-prd → /create-architecture → /create-epics-and-stories → /dev-story → /code-review
```

### 快速开发流程
```
/quick-flow
```

## How to Add New Skills

1. Create skill directory in `.shared/skills/[category]-[name]/`
2. Add `SKILL.md` with frontmatter (name, description)
3. Add supporting files as needed

## How to Add New Workflows

1. Create workflow directory in `.shared/workflows/[name]/`
2. Add `workflow.yaml` or `workflow.md`
3. Add step files in `steps/` subdirectory

## Syncing Across Platforms

When you update `.shared/rules.md`, manually update:

- `.claude/CLAUDE.md`
- `.kiro/steering/project.md`
- `.windsurfrules`
- `.cursorrules`

Or use the `/sync-config` command (if available).
