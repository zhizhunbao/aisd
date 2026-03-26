---
topic: claude_code
dimension: bridge
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Docs: Anthropic Claude Code Overview — https://docs.anthropic.com/en/docs/claude-code/overview"
  - "📖 Docs: Anthropic Claude Code Skills — https://docs.anthropic.com/en/docs/claude-code/skills"
  - "📖 Docs: Anthropic MCP — https://docs.anthropic.com/en/docs/claude-code/mcp"
  - "📖 Docs: Anthropic Claude Code GitHub Actions — https://docs.anthropic.com/en/docs/claude-code/github-actions"
expiry: 6m
status: current
---

# Claude Code 衔接与扩展

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Claude Code Skill 开发 | Skill 是 Claude Code 的扩展机制 | [claude_code_skill/](../claude_code_skill/) |
| ← 前置 | Antigravity Workflow | Workflow 是 Skill 的更高层编排 | [antigravity_workflow/](../antigravity_workflow/) |
| → 后续 | Claude Code Hooks | 确定性预/后处理系统 | — |
| → 后续 | Claude Code Sub-agents | 并行执行和任务分解 | — |
| → 后续 | MCP Server 开发 | 自定义外部工具集成 | — |
| → 后续 | CI/CD 集成 | GitHub Actions / GitLab CI 自动化 | — |
| → 后续 | Agent SDK | 构建自定义 Agent 应用 | — |

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| Git 版本控制 | commit、branch、diff、merge | Claude Code 的核心操作之一是自动化 Git 工作流 |
| Shell / 终端 | bash 命令执行、管道、环境变量 | Claude Code 是终端原生工具，所有操作基于 Shell |
| Markdown | 文件格式、YAML frontmatter | CLAUDE.md 和 Skills 都是 Markdown 文件 |
| Node.js | npm 安装、包管理 | Claude Code 基于 Node.js 运行 |
| Claude Code Skill | Skill 模板格式、`$ARGUMENTS` 占位符 | 掌握 Skill 开发才能扩展 Claude Code 功能 |
| Antigravity Workflow | 多步骤编排、状态管理 | Workflow 是更高层的任务编排框架 |

> 📖 Docs: Anthropic, [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills) / [Workflows](../antigravity_workflow/)

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| Hooks 开发 | Hook 触发点（PreToolUse/PostToolUse） | 深入学习如何编写复杂的 Hook 规则 |
| Sub-agents | Agent spawn/report 机制 | 学习如何设计并行任务分解策略 |
| MCP Server 开发 | MCP 协议理解、Server 配置 | 学习如何开发自定义 MCP Server 连接外部工具 |
| GitHub Actions 集成 | Headless mode (`-p`)、JSON 输出 | 在 CI/CD 中自动化代码审查/测试生成/文档更新 |
| Agent SDK | Agentic Loop 概念、工具调用模式 | 理解 Claude Code 的底层 Agent 架构，构建自定义 Agent |

> 📖 Docs: Anthropic, [Claude Code GitHub Actions](https://docs.anthropic.com/en/docs/claude-code/github-actions)

---

## 概念演变追踪

| 概念 | 在早期 (2021-2023) | 在现代 (2024-2025) | 变化原因 |
|------|-------------------|--------------------|---------|
| AI 编程助手 | 行内代码补全（被动） | Agentic Coding（主动） | 模型能力提升 + Agent 架构成熟 |
| 上下文范围 | 当前文件 + 几个相关文件 | 整个项目目录 + 1M token | 上下文窗口大幅扩展 |
| 交互模式 | 编辑器内嵌入 | 终端 CLI + IDE + 桌面 + Web | 多平台覆盖需求 |
| 定制化 | 有限的设置选项 | CLAUDE.md + Skills + Hooks + MCP | 开发者对可定制性的需求 |
| 安全模型 | 沙箱或无安全控制 | 分层权限系统 + 用户审批 | AI 直操文件系统的风险意识增强 |

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code/overview) | 📖 文档 | 最权威的功能和 API 参考 | ⭐⭐ |
| [Anthropic Engineering Blog](https://www.anthropic.com/engineering) | 📖 博客 | Claude Code 的设计思考和技术决策 | ⭐⭐⭐ |
| [MCP Specification](https://modelcontextprotocol.io/) | 📖 规范 | 理解 MCP 协议的完整设计 | ⭐⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Cursor Docs](https://docs.cursor.com/) | AI IDE vs Agentic CLI | 选择工具时 |
| [GitHub Copilot Docs](https://docs.github.com/en/copilot) | Copilot Agent Mode 对比 | 评估团队工具时 |
| [Devin](https://devin.ai/) | 全自主 vs 人在循环 | 了解行业极端路线 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [AI-Assisted Software Engineering (IEEE)](https://www.computer.org/csdl/magazine/so) | 学术视角看 AI 编程 | 研究行业趋势 |
| [The State of AI Coding Tools 2025](https://www.google.com/search?q=state+of+ai+coding+tools+2025) | 年度行业报告 | 全局视角 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| AI 工具知识库 | 4 | [claude_code_skill](../claude_code_skill/)、[antigravity_workflow](../antigravity_workflow/)、[hugging_face](../hugging_face/)、[mineru](../mineru/) | Skill 开发模式、Workflow 编排、模型使用 |
| 课程知识库 | 16 | deep-learning、nlp、reinforcement-learning 等 | Claude Code 可用于加速课程知识库的生成 |

> 📖 Docs: 工作区内部知识库索引
