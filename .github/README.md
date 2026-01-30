# .github 参考项目集合

本目录包含用于 Skill 和 Workflow 开发的参考项目，支持迁移到 Claude Code、Cursor、Kiro、Windsurf 等多种 AI 编程工具。

---

## 工作流规范 (Workflow Specification)

### 1. BMAD-METHOD ⭐⭐⭐

> **Breakthrough Method of Agile AI Driven Development**

**最完整的工作流规范框架**，包含 21 个专业 Agent 和 50+ 个工作流。

- **GitHub**: https://github.com/bmad-code-org/BMAD-METHOD
- **文档**: https://docs.bmad-method.org

**核心特性：**
- YAML 格式的 Agent 和 Workflow 定义
- 支持 Claude Code、Cursor、Windsurf、Roo 等多 IDE
- 完整的软件开发生命周期覆盖

**关键目录：**
```
BMAD-METHOD/
├── src/modules/          # Agent 和 Workflow 模块
├── docs/                 # 完整文档
│   ├── agent-customization-guide.md
│   └── workflow-reference.md
└── tools/                # 辅助工具
```

**Workflow YAML 格式示例：**
```yaml
config_source: _bmad/bmm/config.yaml
discover_inputs:
  - name: discover_inputs
    load_strategy: FULL_LOAD
outputFile: "{planning_artifacts}/prd/index.md"
nextStepFile: steps/step-02-vision.md
```

**Agent YAML 格式示例：**
```yaml
name: analyst
persona: Requirements Analyst
menu:
  - trigger: prd
    workflow_path: "_bmad/workflows/create-prd"
  - trigger: architecture
    workflow_path: "_bmad/workflows/create-architecture"
```

**标准工作流：**
```
/product-brief → /create-prd → /create-architecture → /create-epics-and-stories → /dev-story → /code-review
```

---

### 2. spec-kit ⭐⭐⭐

> **GitHub 官方 Spec-Driven Development 工具包**

- **GitHub**: https://github.com/github/spec-kit
- **博客**: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/

**四阶段工作流：**
```
/specify → /plan → /tasks → /implement
```

**核心理念：**
- Specification 作为"真相来源"
- 代码是规格的实现产物
- 支持 GitHub Copilot、Claude Code、Gemini CLI

**关键目录：**
```
spec-kit/
├── docs/                 # 方法论文档
├── templates/            # 项目模板
├── src/specify_cli/      # CLI 工具
├── scripts/              # 辅助脚本
├── spec-driven.md        # 核心方法论
└── AGENTS.md             # Agent 配置
```

**初始化命令：**
```bash
pip install specify-cli
specify init
```

---

### 3. claude-code-spec-workflow ⭐⭐

> **Claude Code 专用 Spec 工作流**

- **GitHub**: https://github.com/Pimzino/claude-code-spec-workflow

**两种工作流模式：**

1. **新功能开发**：Requirements → Design → Tasks → Implementation
2. **Bug 修复**：Report → Analyze → Fix → Verify

**关键目录：**
```
claude-code-spec-workflow/
├── src/                  # 核心逻辑
├── examples/             # 使用示例
└── docs/                 # 文档
```

---

## Agent Skills 规范

### 4. skills (Anthropic 官方) ⭐⭐⭐

> **Agent Skills 开放标准规范**

- **GitHub**: https://github.com/anthropics/skills
- **规范**: https://agentskills.io/specification

**已采用平台：** Claude Code、Cursor、VS Code、GitHub Copilot、OpenAI Codex、Windsurf、Amp、Goose

**Skill 最小结构：**
```
my-skill/
├── SKILL.md              # 必需，包含 YAML frontmatter
├── scripts/              # 可选，脚本
├── templates/            # 可选，模板
└── references/           # 可选，参考资料
```

**SKILL.md 格式：**
```markdown
---
name: my-skill
description: Skill description
---

# My Skill

## Instructions
...
```

**关键目录：**
```
skills/
├── spec/                 # Agent Skills 规范定义
├── skills/               # 示例 Skills
└── template/             # Skill 模板
```

---

### 5. claude-skills (社区集合) ⭐⭐

> **社区收集的 Claude Code Skills**

- **GitHub**: https://github.com/alirezarezvani/claude-skills

**包含的 Skills 分类：**
- `agents/` - 子 Agent 定义
- `commands/` - 命令脚本
- `engineering-team/` - 工程团队相关
- `product-team/` - 产品团队相关
- `project-management/` - 项目管理
- `documentation/` - 文档相关
- `standards/` - 标准规范
- `templates/` - 模板

---

## Agent 编排框架

### 6. claude-flow ⭐⭐

> **多 Agent 编排平台**

- **GitHub**: https://github.com/ruvnet/claude-flow

**特性：**
- 108 个专业 AI Agent
- 15 个多 Agent 工作流编排器
- 129 个 Agent Skills
- 支持 MCP 协议

**关键目录：**
```
claude-flow/
├── agents/               # Agent 定义
├── plugin/               # 插件系统
├── v2/                   # V2 版本
├── v3/                   # V3 版本
└── docs/                 # 文档
```

---

## 其他参考资源

### 7. anthropic-cookbook

> **Anthropic 官方示例代码库**

- **GitHub**: https://github.com/anthropics/anthropic-cookbook

### 8. claude-code-action

> **GitHub Actions 中使用 Claude Code**

- **GitHub**: https://github.com/anthropics/claude-code-action

### 9. awesome-claude-prompts

> **Claude 提示词集合**

### 10. prompt-eng-interactive-tutorial

> **Anthropic 提示工程交互教程**

### 11. courses

> **课程相关资料**

---

## 迁移指南

### 从本项目 Skills 迁移到其他平台

本项目的 Skills 位于 `.shared/skills/`，遵循 Agent Skills 规范，可直接用于：

| 平台 | 配置方式 |
|------|----------|
| Claude Code | 在 `CLAUDE.md` 或 `.claude/settings.json` 中引用 |
| Cursor | 在 `.cursorrules` 或 `.cursor/rules/` 中引用 |
| Windsurf | 在 `.windsurfrules` 中引用 |
| Kiro | 在 `.kiro/` 目录中配置 |
| VS Code Copilot | 在 `.github/copilot-instructions.md` 中引用 |

### 创建跨平台 Workflow

推荐参考 **BMAD-METHOD** 的 workflow.yaml 格式：

```yaml
# .agent/workflows/feature-development/workflow.yaml
name: feature-development
description: 新功能开发完整流程
phases:
  - name: requirements
    agent: analyst
    skill: dev-requirements
    output: "{artifacts}/requirements.md"

  - name: design
    agent: architect
    skill: dev-design
    input: "{artifacts}/requirements.md"
    output: "{artifacts}/design.md"

  - name: implementation
    agent: developer
    skills:
      - dev-backend
      - dev-frontend
      - dev-database
    input: "{artifacts}/design.md"

  - name: review
    agent: reviewer
    skill: code-review
    checks:
      - scripts/check-naming.py
      - scripts/check-schema.py
```

---

## 快速开始

### 1. 学习工作流规范
```bash
# 阅读 BMAD-METHOD 文档
cat .github/BMAD-METHOD/docs/workflow-reference.md

# 阅读 spec-kit 方法论
cat .github/spec-kit/spec-driven.md
```

### 2. 学习 Skill 规范
```bash
# 阅读 Agent Skills 规范
cat .github/skills/spec/

# 查看示例 Skills
ls .github/skills/skills/
```

### 3. 创建自己的 Workflow
```bash
# 参考 BMAD 创建 workflow
mkdir -p .agent/workflows/my-workflow
# 编写 workflow.yaml 和相关 steps
```

---

## 相关链接

- [Agent Skills 规范](https://agentskills.io/specification)
- [BMAD-METHOD 文档](https://docs.bmad-method.org)
- [GitHub Spec-Kit 博客](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Anthropic Agent Skills 介绍](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
