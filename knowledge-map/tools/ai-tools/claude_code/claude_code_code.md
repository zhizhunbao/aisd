---
topic: claude_code
dimension: code
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Docs: Anthropic Claude Code CLI Reference — https://docs.anthropic.com/en/docs/claude-code/cli-reference"
  - "📖 Docs: Anthropic Claude Code Getting Started — https://docs.anthropic.com/en/docs/claude-code/getting-started"
  - "📖 Docs: Anthropic Claude Code Memory — https://docs.anthropic.com/en/docs/claude-code/memory"
  - "📖 Docs: Anthropic Claude Code Hooks — https://docs.anthropic.com/en/docs/claude-code/hooks"
  - "📖 Docs: Anthropic Claude Code Skills — https://docs.anthropic.com/en/docs/claude-code/skills"
  - "📖 Docs: Anthropic Claude Code Common Workflows — https://docs.anthropic.com/en/docs/claude-code/common-workflows"
expiry: 3m
status: current
---

# Claude Code 代码参考

> 📖 Docs: Anthropic, [Claude Code CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

---

## 快速开始

### 最简示例 — 30 秒上手

```bash
# ============================================================
# 1. 安装 Claude Code / Install Claude Code
# ============================================================
npm install -g @anthropic-ai/claude-code

# ============================================================
# 2. 进入项目目录 / Navigate to project
# ============================================================
cd your-project/

# ============================================================
# 3. 启动交互式会话 / Start interactive session
# ============================================================
claude
```

**测试方法：** 输入 `claude` 后看到交互式提示符即表示安装成功。输入 `"summarize this project"` 验证项目上下文读取。

> 📖 Docs: Anthropic, [Getting Started](https://docs.anthropic.com/en/docs/claude-code/getting-started)

---

## 完整实现示例

### 示例 1: 创建项目记忆文件 (CLAUDE.md)

```markdown
# CLAUDE.md — 项目记忆 / Project Memory

## 项目概述 / Project Overview
这是一个 Next.js 14 + TypeScript 项目，使用 Tailwind CSS。

## 编码规范 / Coding Standards
- 使用 TypeScript strict mode
- 组件使用函数式写法 + React hooks
- 文件命名: kebab-case
- CSS: 使用 Tailwind utility classes

## 常用命令 / Common Commands
- `npm run dev` — 启动开发服务器
- `npm run test` — 运行测试
- `npm run lint` — 代码检查
- `npm run build` — 生产构建

## 架构决策 / Architecture Decisions
- 状态管理: Zustand (不用 Redux)
- API: tRPC (不用 REST)
- 数据库: PostgreSQL + Prisma ORM

## 注意事项 / Important Notes
- 不要修改 `src/generated/` 目录下的文件（自动生成）
- 环境变量在 `.env.local`，不要提交到 Git
```

### 示例 2: 创建自定义 Skill (斜杠命令)

```markdown
# .claude/commands/review-pr.md
# 用法 / Usage: 在 Claude Code 中输入 /review-pr

请对当前分支与 main 分支的差异进行代码审查。

审查要点:
1. **安全性**: 检查 SQL 注入、XSS、硬编码密钥
2. **性能**: 检查 N+1 查询、不必要的重渲染
3. **可读性**: 变量命名、函数长度、注释质量
4. **测试**: 是否有新增测试覆盖变更

输出格式:
- 🔴 必须修复 (安全/bug)
- 🟡 建议修复 (性能/可读性)
- 🟢 表现优秀

额外参数: $ARGUMENTS
```

### 示例 3: 配置 Hooks (自动格式化)

```json
// .claude/settings.json — Hooks 配置 / Hooks Configuration
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $CLAUDE_FILE_PATH"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[Hook] About to run: $CLAUDE_TOOL_INPUT'"
          }
        ]
      }
    ]
  }
}
```

### 示例 4: MCP Server 配置

```json
// .claude/mcp.json — MCP Server 配置 / MCP Server Configuration
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "/path/to/data"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    }
  }
}
```

> 📖 Docs: Anthropic, [MCP](https://docs.anthropic.com/en/docs/claude-code/mcp)

---

## API 速查

### 基本命令

| 命令 | 参数 | 说明 |
|------|------|------|
| `claude` | — | 启动交互式会话 / Start interactive session |
| `claude "prompt"` | 初始提示 | 带初始提示启动 / Start with initial prompt |
| `claude -p "prompt"` | `-p` / `--print` | 无头模式（非交互） / Headless mode |
| `claude -c` | `-c` / `--continue` | 恢复上次会话 / Resume last session |
| `claude -r "id"` | `-r` / `--resume` | 恢复指定会话 / Resume specific session |

### 模型与输出

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--model` | `sonnet` | 选择模型 / Select model (`sonnet`, `haiku`, `opus`) |
| `--output-format` | `text` | 输出格式 / Output format (`text`, `json`, `stream-json`) |
| `--max-turns` | 无限制 | 最大轮次 / Max agentic turns |
| `--verbose` | `false` | 详细日志 / Verbose logging |

### 交互式命令 (会话内)

| 命令 | 说明 |
|------|------|
| `/compact` | 压缩上下文 / Compact context window |
| `/clear` | 清空对话 / Clear conversation |
| `/cost` | 查看费用 / Show cost breakdown |
| `/doctor` | 诊断问题 / Diagnose installation issues |
| `/init` | 生成 CLAUDE.md / Generate CLAUDE.md |
| `/memory` | 编辑记忆 / Edit memory files |
| `/model` | 切换模型 / Switch model |
| `/permissions` | 查看权限 / View permission settings |
| `/schedule` | 创建定时任务 / Create scheduled task |
| `/teleport` | 远程传送会话 / Teleport session |
| `/desktop` | 移交桌面端 / Hand off to Desktop app |

### 管道与自动化

| 用法 | 示例 |
|------|------|
| 管道输入 | `cat error.log \| claude -p "explain this error"` |
| 批量处理 | `git diff --name-only \| claude -p "review these files"` |
| JSON 输出 | `claude -p "list TODOs" --output-format json` |
| 并行实例 | 多个终端窗口各自运行 `claude` |

> 📖 Docs: Anthropic, [Claude Code CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

---

## 目录结构模板

### 简单结构

```
project/
├── CLAUDE.md               ← 项目记忆
├── .claude/
│   └── settings.json       ← 权限 + Hooks 配置
└── src/
    └── ...
```

### 标准结构

```
project/
├── CLAUDE.md                   ← 项目级记忆
├── .claude/
│   ├── settings.json           ← 权限 + Hooks 配置
│   ├── mcp.json                ← MCP Server 配置
│   └── commands/               ← 自定义 Skills
│       ├── review-pr.md
│       └── deploy.md
├── src/
│   ├── CLAUDE.md               ← 目录级记忆（特殊规则）
│   └── ...
└── tests/
    └── ...
```

### 高级结构（团队协作）

```
project/
├── CLAUDE.md                   ← 项目共享记忆
├── .claude/
│   ├── settings.json           ← 共享权限配置
│   ├── mcp.json                ← 共享 MCP 配置
│   └── commands/               ← 团队共享 Skills
│       ├── review-pr.md
│       ├── deploy-staging.md
│       └── generate-migration.md
├── .github/
│   └── workflows/
│       └── claude-code.yml     ← CI/CD 集成
├── src/
│   ├── api/
│   │   └── CLAUDE.md           ← API 层特殊规则
│   ├── frontend/
│   │   └── CLAUDE.md           ← 前端特殊规则
│   └── ...
└── ~/ (全局)
    └── .claude/
        ├── CLAUDE.md            ← 个人全局偏好
        ├── settings.json        ← 个人权限
        └── commands/            ← 个人 Skills
            └── my-template.md
```

> 📖 Docs: Anthropic, [Claude Code Memory](https://docs.anthropic.com/en/docs/claude-code/memory) / [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
