---
topic: claude_code
dimension: map
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Docs: Anthropic Claude Code Overview — https://docs.anthropic.com/en/docs/claude-code/overview"
  - "📖 Docs: Anthropic Claude Code CLI Reference — https://docs.anthropic.com/en/docs/claude-code/cli-reference"
  - "📖 Docs: Anthropic Claude Code Memory (CLAUDE.md) — https://docs.anthropic.com/en/docs/claude-code/memory"
  - "📖 Docs: Anthropic Claude Code Hooks — https://docs.anthropic.com/en/docs/claude-code/hooks"
  - "📖 Docs: Anthropic Claude Code Sub-agents — https://docs.anthropic.com/en/docs/claude-code/sub-agents"
  - "📖 Docs: Anthropic Claude Code Skills — https://docs.anthropic.com/en/docs/claude-code/skills"
  - "📖 Docs: Anthropic MCP — https://docs.anthropic.com/en/docs/claude-code/mcp"
expiry: 3m
status: current
---

# Claude Code 知识地图

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)
> 📖 Docs: Anthropic, [Claude Code CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

---

## 1. 核心问题

- **Claude Code 是什么？** → Anthropic 开发的 Agentic Coding 命令行工具，能读懂代码库、编辑文件、执行命令、集成开发工具
- **它和传统 AI 编程助手（如 Copilot Autocomplete）有什么本质区别？** → 它是自主 Agent，能规划多步骤任务、自动执行并验证，而非仅补全代码
- **CLAUDE.md、Skills、Hooks 三者分别解决什么问题？** → CLAUDE.md = 记忆/上下文持久化；Skills = 自定义斜杠命令；Hooks = 确定性 Shell 预/后处理
- **MCP (Model Context Protocol) 在 Claude Code 中扮演什么角色？** → 开放标准协议，连接外部工具和数据源（数据库、设计文档、Ticket 系统等）
- **Sub-agents 是什么？什么时候用？** → 隔离的子 Agent 实例，用于并行研究、代码探索、专项任务，避免污染主上下文

> 📖 Docs: Anthropic, [Claude Code Overview — What you can do](https://docs.anthropic.com/en/docs/claude-code/overview#what-you-can-do)

---

## 2. 全景位置

    AI 编程工具生态
    ├── 代码补全 (Code Completion)
    │   ├── GitHub Copilot Autocomplete (行级补全)
    │   ├── TabNine (本地模型)
    │   └── Codeium (免费替代)
    ├── AI IDE / 编辑器
    │   ├── Cursor (AI-native IDE，基于 VS Code)
    │   ├── Windsurf (Codeium IDE)
    │   └── Void (开源)
    ├── Agentic Coding 工具 ← 你在这里
    │   ├── 【Claude Code】 (终端优先、高自主性、1M token 上下文)
    │   ├── GitHub Copilot Agent Mode (GitHub 生态深度集成)
    │   ├── Devin (全自主 AI 工程师)
    │   └── OpenHands (开源 Agent)
    └── AI 辅助平台
        ├── Vercel v0 (UI 生成)
        ├── Bolt.new (全栈生成)
        └── Replit Agent (云端开发)

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## 3. 依赖地图

    前置知识                   本主题                     后续方向
    ┌─────────────────────┐   ┌────────────────────┐   ┌───────────────────────────┐
    │ 终端/Shell 基础      │──→│                    │──→│ CLAUDE.md 最佳实践         │
    │ Git 版本控制         │──→│   Claude Code      │──→│ Skills 开发 (自定义命令)    │
    │ Node.js 18+ 环境     │──→│   (Agentic CLI)    │──→│ Hooks 系统 (预/后处理)      │
    │ API Key / Max 订阅   │──→│                    │──→│ MCP Server 集成            │
    │ Markdown 基础        │──→│                    │──→│ Sub-agents 并行执行         │
    └─────────────────────┘   └────────────────────┘   │ CI/CD 集成 (GitHub Actions) │
                                                       │ Agent SDK 自定义 Agent      │
                                                       └───────────────────────────┘

> 📖 Docs: Anthropic, [Getting Started](https://docs.anthropic.com/en/docs/claude-code/getting-started)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [claude_code_map.md](claude_code_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [claude_code_concepts.md](claude_code_concepts.md) | ② 概念 | 理解术语定义、辨析 CLAUDE.md vs Skills vs Hooks |
| ~~claude_code_math.md~~ | ~~③ 公式~~ | ~~不适用（纯工程工具）~~ |
| [claude_code_tutorial.md](claude_code_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [claude_code_code.md](claude_code_code.md) | ⑤ 代码 | 快速上手实现、CLI 命令速查 |
| [claude_code_pitfalls.md](claude_code_pitfalls.md) | ⑥ 踩坑 | 调试问题、避坑指南 |
| [claude_code_history.md](claude_code_history.md) | ⑦ 历史 | 了解 AI Coding 工具演进 |
| [claude_code_bridge.md](claude_code_bridge.md) | ⑧ 衔接 | 找相关主题（Skills、MCP、Workflow） |
| ~~claude_code_first_principles.md~~ | ~~⑨ 第一性原理~~ | ~~不适用（纯工程工具）~~ |

> 📖 Docs: Anthropic, [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [claude_code_map.md](claude_code_map.md) 了解全局位置
2. 读 [claude_code_tutorial.md](claude_code_tutorial.md) Section 1 理解 Claude Code 解决什么问题
3. 读 [claude_code_concepts.md](claude_code_concepts.md) 掌握核心术语（Agentic Loop、CLAUDE.md、Hooks、MCP）
4. 跟 [claude_code_code.md](claude_code_code.md) 快速开始：安装 → 初始化 → 第一个任务
5. 读 [claude_code_history.md](claude_code_history.md) 了解 AI Coding 工具演进

### 日常参考 🔧

1. 查 [claude_code_code.md](claude_code_code.md) CLI 命令速查表
2. 查 [claude_code_pitfalls.md](claude_code_pitfalls.md) 排查常见问题
3. 查 [claude_code_concepts.md](claude_code_concepts.md) 辨析术语

### 深度研究 🔬

1. 读 [claude_code_history.md](claude_code_history.md) AI Coding 完整演进线
2. 读 [claude_code_bridge.md](claude_code_bridge.md) 探索 Skills 开发、MCP 集成
3. 阅读 Anthropic 官方文档和博客

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ~~不适用~~ |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ~~不适用~~ |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-23 | 3m | ✅ current |
| Concepts | 2026-03-23 | 3m | ✅ current |
| Math | — | — | ~~不适用~~ |
| Tutorial | 2026-03-23 | 3m | ✅ current |
| Code | 2026-03-23 | 3m | ✅ current |
| Pitfalls | 2026-03-23 | 3m | ✅ current |
| History | 2026-03-23 | never | ✅ current |
| Bridge | 2026-03-23 | 6m | ✅ current |
| First Principles | — | — | ~~不适用~~ |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview) | 📖 文档 | 全文核心参考 |
| [Claude Code CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference) | 📖 文档 | Code 维度 CLI 命令 |
| [Claude Code Memory (CLAUDE.md)](https://docs.anthropic.com/en/docs/claude-code/memory) | 📖 文档 | Concepts + Tutorial |
| [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) | 📖 文档 | Concepts + Tutorial |
| [Claude Code Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents) | 📖 文档 | Concepts + Tutorial |
| [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills) | 📖 文档 | Concepts + Bridge |
| [Model Context Protocol](https://docs.anthropic.com/en/docs/claude-code/mcp) | 📖 文档 | Concepts + Bridge |
| [Claude Code GitHub Actions](https://docs.anthropic.com/en/docs/claude-code/github-actions) | 📖 文档 | Code + Bridge |
| [claude_code_skill/](../claude_code_skill/) | 💻 知识库 | Bridge 维度内链参考 |
| [antigravity_workflow/](../antigravity_workflow/) | 💻 知识库 | Bridge 维度内链参考 |
