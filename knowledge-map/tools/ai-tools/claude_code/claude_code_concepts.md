---
topic: claude_code
dimension: concepts
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Docs: Anthropic Claude Code Overview — https://docs.anthropic.com/en/docs/claude-code/overview"
  - "📖 Docs: Anthropic Claude Code Memory — https://docs.anthropic.com/en/docs/claude-code/memory"
  - "📖 Docs: Anthropic Claude Code Hooks — https://docs.anthropic.com/en/docs/claude-code/hooks"
  - "📖 Docs: Anthropic Claude Code Sub-agents — https://docs.anthropic.com/en/docs/claude-code/sub-agents"
  - "📖 Docs: Anthropic Claude Code Skills — https://docs.anthropic.com/en/docs/claude-code/skills"
  - "📖 Docs: Anthropic MCP — https://docs.anthropic.com/en/docs/claude-code/mcp"
  - "📖 Docs: Anthropic Claude Code CLI Reference — https://docs.anthropic.com/en/docs/claude-code/cli-reference"
expiry: 3m
status: current
---

# Claude Code 核心概念

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## 术语定义

### Agentic Coding (代理式编程)

一种 AI 辅助编程范式，AI 不只是补全代码或回答问题，而是像一个开发者一样**自主规划、执行多步骤任务、验证结果**。它能读取代码库、编辑文件、运行测试、提交 Git，形成完整的"感知→规划→执行→验证"循环。

> 易混淆：**Code Completion (代码补全)** — 代码补全只做单行/多行的被动预测，不理解项目全局上下文，也不会主动执行命令。Agentic Coding 是主动的、多步骤的、有上下文的。

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

### Agentic Loop (代理循环)

Claude Code 的核心运行机制。每次收到用户指令后，Claude 会进入一个循环：**初始化 → 规划 → 工具调用（读文件/写文件/执行命令）→ 验证 → 反馈**。这个循环会持续运行直到任务完成或需要用户确认。

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

### CLAUDE.md (记忆文件)

Claude Code 的"项目记忆"文件。它是一个 Markdown 文件，放在项目根目录（或 `~/.claude/` 全局目录），告诉 Claude 项目的编码规范、架构决策、常用命令、注意事项等。Claude Code 在每次启动时自动读取。

层级结构：
- **全局** `~/.claude/CLAUDE.md` — 跨项目的个人偏好
- **项目** `./CLAUDE.md` — 项目级别的规范
- **本地** `./src/CLAUDE.md` — 目录级别的特殊规则

> 别名：**Memory File**（官方文档中的叫法）/ **Project Instructions**（概念上等同）

> 易混淆：**Skills (技能文件)** — CLAUDE.md 是被动的上下文记忆，每次会话自动加载；Skills 是主动的命令定义，只在用户调用 `/slash-command` 时触发。

> 📖 Docs: Anthropic, [Claude Code Memory](https://docs.anthropic.com/en/docs/claude-code/memory)

### Skills (技能 / 自定义命令)

用户自定义的斜杠命令（如 `/review-pr`、`/deploy-staging`），存放在 `.claude/commands/` 或项目的 `.agent/workflows/` 目录中。每个 Skill 是一个 Markdown 文件，包含指令模板和参数占位符 `$ARGUMENTS`。

两种类型：
- **项目命令** `.claude/commands/` — 所有项目成员共享
- **个人命令** `~/.claude/commands/` — 仅自己使用

> 别名：**Custom Commands**（官方文档中的叫法）/ **Custom Slash Commands**

> 易混淆：**Hooks** — Skills 是 AI Agent 执行的高级指令（Markdown 模板），Hooks 是确定性的 Shell 脚本（在 Agent 动作前后执行）。Skills 由 LLM 解释执行，Hooks 由系统确定性执行。

> 📖 Docs: Anthropic, [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills)

### Hooks (钩子)

确定性的预/后处理规则，在 Claude Code 执行特定动作（如编辑文件、执行命令、发送消息）的前后自动触发。与 Skills 不同，Hooks 是 **Shell 脚本**，不经过 LLM 推理，保证执行结果可预测。

触发点：
- `PreToolUse` — 工具调用前（如编辑文件前自动备份）
- `PostToolUse` — 工具调用后（如编辑后自动格式化）
- `Notification` — 通知用户时
- `Stop` — Agent 停止时

> 易混淆：**Skills** — Hooks 是确定性 Shell 脚本（不经 LLM），Skills 是 Markdown 指令（由 LLM 解释执行）。

> 📖 Docs: Anthropic, [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)

### MCP (Model Context Protocol / 模型上下文协议)

一个开放标准协议，让 Claude Code 连接外部工具和数据源。通过 MCP Server，Claude Code 可以访问数据库、设计文档、Ticket 系统（Jira/Linear）、Slack 等。MCP 是 Anthropic 推出的通用协议，不限于 Claude Code。

> 别名：**Model Context Protocol** — 唯一官方名称

> 📖 Docs: Anthropic, [MCP](https://docs.anthropic.com/en/docs/claude-code/mcp)

### Sub-agents (子代理)

隔离的 Claude Code Agent 实例，由主 Agent 生成（spawn），用于并行执行研究、代码探索等任务。每个 Sub-agent 有独立的上下文窗口，完成后向主 Agent 报告结果，不会污染主上下文。

主要用途：
- 并行研究多个文件/代码路径
- 独立评估不同方案
- 执行耗时的分析任务

> 📖 Docs: Anthropic, [Claude Code Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

### Permission System (权限系统)

Claude Code 的安全控制机制。默认情况下，Claude Code 对**所有文件编辑、命令执行、网络请求**都需要用户显式批准。用户可以通过 `settings.json` 或 CLAUDE.md 中的 `allowedTools` 配置白名单以自动批准某些操作。

权限层级：
- **Ask** (默认) — 每次请求用户确认
- **Allow** — 自动批准（可配置范围）
- **Deny** — 明确禁止

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

### Headless Mode (无头模式)

Claude Code 的非交互式运行模式，用 `claude -p "prompt"` 调用。适用于 CI/CD 管线、自动化脚本、批量处理。输出可以是纯文本或 JSON（`--output-format json`）。

> 别名：**Print Mode** / **Non-interactive Mode**

> 📖 Docs: Anthropic, [Claude Code CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

### Context Window (上下文窗口)

Claude Code 使用的 Claude 模型的输入容量上限。当前支持最大 **200K token** 的上下文窗口（Claude 3.5 Sonnet/Haiku），Opus 支持更大。Claude Code 会自动管理上下文，在接近上限时进行 Context Compaction（压缩）。

> 易混淆：**Token Limit vs Context Window** — Token Limit 是模型的硬限制，Context Window 是 Claude Code 实际使用的有效上下文大小。

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## 概念辨析

### CLAUDE.md vs Skills vs Hooks

| 维度 | CLAUDE.md | Skills | Hooks |
|------|-----------|--------|-------|
| **本质** | 被动上下文记忆（Markdown） | 主动命令模板（Markdown） | 确定性 Shell 脚本 |
| **触发方式** | 会话启动时自动加载 | 用户输入 `/command` | Agent 动作前/后自动触发 |
| **执行者** | LLM 读取并遵循 | LLM 解释并执行 | 系统直接执行（不经 LLM） |
| **存放位置** | 项目根目录 / `~/.claude/` | `.claude/commands/` | `settings.json` |
| **典型用途** | 编码规范、架构决策、常用命令 | 代码审查、部署、自定义流程 | 自动格式化、备份、lint 检查 |
| **可预测性** | LLM 可能忽略或理解偏差 | LLM 可能执行偏差 | 100% 确定性执行 |

> 📖 Docs: Anthropic, [Memory](https://docs.anthropic.com/en/docs/claude-code/memory) / [Skills](https://docs.anthropic.com/en/docs/claude-code/skills) / [Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)

### Claude Code vs Cursor vs GitHub Copilot

| 维度 | Claude Code | Cursor | GitHub Copilot |
|------|-------------|--------|----------------|
| **界面** | 终端 CLI（也有 IDE/桌面端） | AI-native IDE（基于 VS Code） | IDE 插件 + GitHub 平台 |
| **自主程度** | 高自主——自动规划、执行、验证 | 中等——需要更多用户指引 | 中等——Coding Agent 自主但范围受限 |
| **上下文范围** | 整个项目目录 + 1M token | 索引整个代码库 | 打开的文件 + 仓库 |
| **模型灵活性** | 仅 Anthropic 模型 | 多模型（Claude/GPT/Gemini） | 主要 OpenAI 模型 |
| **最强场景** | 终端爱好者、大代码库、复杂调试 | 日常编码、可视化多文件编辑 | GitHub 深度集成、团队协作 |

> 📖 Docs: 综合对比来源

---

## 核心属性

### 信息架构

    用户输入 (自然语言)
         │
         ▼
    ┌──────────────────────────────┐
    │      Claude Code CLI         │
    │  ┌────────────────────────┐  │
    │  │     Agentic Loop       │  │
    │  │  ┌───────┐ ┌────────┐ │  │
    │  │  │ Plan  │→│ Execute│ │  │
    │  │  └───────┘ └────┬───┘ │  │
    │  │       ▲         │     │  │
    │  │       └─Verify──┘     │  │
    │  └────────────────────────┘  │
    │                              │
    │  ┌──────┐ ┌──────┐ ┌─────┐  │
    │  │CLAUDE│ │Skills│ │Hooks│  │
    │  │ .md  │ │      │ │     │  │
    │  └──────┘ └──────┘ └─────┘  │
    │                              │
    │  ┌────────────────────────┐  │
    │  │   MCP Servers          │  │
    │  │  (外部工具连接)         │  │
    │  └────────────────────────┘  │
    └──────────────────────────────┘
         │
         ▼
    文件编辑 / 命令执行 / Git 操作

### 适用场景 ✅

- 大代码库的跨文件重构
- 自动化测试编写和修复
- Git 工作流（commit、PR、merge conflict）
- CI/CD 管线中的自动化任务
- 代码审查和文档生成
- 复杂 bug 调试（需要理解全局上下文）

### 不适用场景 ❌

- 需要实时代码补全的场景（用 Cursor/Copilot）
- 需要可视化 diff 审查的场景（用 IDE 工具）
- 对网络隔离有严格要求的环境（需要 API 调用）
- 非常简单的单行代码修改（手动更快）

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 安装 | npm 全局安装 | `npm install -g @anthropic-ai/claude-code` |
| 启动 | 在项目目录运行 | `claude` |
| 无头模式 | 非交互式执行 | `claude -p "fix all lint errors"` |
| 恢复会话 | 继续上次对话 | `claude --continue` |
| 记忆文件 | 项目规范 | 项目根目录 `CLAUDE.md` |
| 自定义命令 | 斜杠命令 | `.claude/commands/review.md` |
| 权限配置 | 自动批准 | `settings.json` → `allowedTools` |
| MCP 集成 | 外部工具 | `.claude/mcp.json` 配置 Server |
| 上下文管理 | 压缩长对话 | `/compact` 命令 |
| 多模型 | 切换模型 | `claude --model sonnet` |
