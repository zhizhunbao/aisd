---
topic: claude_code
dimension: tutorial
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Docs: Anthropic Claude Code Overview — https://docs.anthropic.com/en/docs/claude-code/overview"
  - "📖 Docs: Anthropic Claude Code Getting Started — https://docs.anthropic.com/en/docs/claude-code/getting-started"
  - "📖 Docs: Anthropic Claude Code Memory — https://docs.anthropic.com/en/docs/claude-code/memory"
  - "📖 Docs: Anthropic Claude Code Hooks — https://docs.anthropic.com/en/docs/claude-code/hooks"
  - "📖 Docs: Anthropic Claude Code Sub-agents — https://docs.anthropic.com/en/docs/claude-code/sub-agents"
  - "📖 Docs: Anthropic Claude Code CLI Reference — https://docs.anthropic.com/en/docs/claude-code/cli-reference"
  - "📖 Docs: Anthropic Claude Code Common Workflows — https://docs.anthropic.com/en/docs/claude-code/common-workflows"
expiry: 3m
status: current
---

# Claude Code 教程

> **前置知识：** 终端/Shell 基础、Git 版本控制、Node.js 18+ 已安装
> **参考来源：** [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## Section 0: 前置知识速查

1. **终端基础**：能在 Terminal/PowerShell 中运行命令（`cd`、`ls`/`dir`、`npm`）
2. **Git 基础**：理解 `commit`、`push`、`branch`、`merge`
3. **Node.js 18+**：Claude Code 基于 Node.js 运行，需要 18 或更高版本
4. **认证方式**（二选一）：
   - Anthropic API Key（按量付费）
   - Claude Pro/Max 订阅（月费包含使用额度）

> 📖 Docs: Anthropic, [Getting Started](https://docs.anthropic.com/en/docs/claude-code/getting-started)

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **上下文切换成本高**：在编辑器、终端、浏览器、文档之间来回跳转，每次切换都丢失思路
- 🔥 **大项目改不动**：跨 10 个文件的重构，手动追踪每个引用点极易遗漏
- 🔥 **重复劳动多**：写测试、修 lint、解冲突、更新文档——每次都是机械性操作
- 🔥 **AI 助手不够聪明**：传统 AI 补全只看当前文件，不理解项目架构，给出的建议经常不能直接用
- 🔥 **调试黑洞**：一个 bug 可能涉及 5 个文件的交互，逐个排查耗费大量时间

### 它的核心价值

1. **全项目上下文理解**：Claude Code 读取整个项目目录，理解文件间的依赖关系，不是只看当前打开的文件
2. **自主多步骤执行**：一条指令可以触发"读代码→分析→修改→测试→提交"的完整链路
3. **终端原生**：不需要离开你的开发环境，一个终端搞定一切
4. **可定制记忆**：通过 CLAUDE.md 告诉 Claude 你的项目规范，它会持续遵守
5. **安全可控**：所有操作需要用户批准，你始终是最终决策者

> 📖 Docs: Anthropic, [Claude Code Overview — What you can do](https://docs.anthropic.com/en/docs/claude-code/overview#what-you-can-do)

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 Agentic Loop 生命周期

    用户输入自然语言指令
         │
         ▼
    ┌─────────────────────────────────────┐
    │          初始化 (Initialize)         │
    │  • 读取 CLAUDE.md（项目记忆）        │
    │  • 加载 MCP Server 连接             │
    │  • 扫描项目结构                      │
    └────────────┬────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │           规划 (Plan)               │
    │  • 分解任务为子步骤                  │
    │  • 确定需要读/写哪些文件             │
    │  • 判断需要执行哪些命令              │
    └────────────┬────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │         工具调用 (Execute)           │◄──┐
    │  • Read: 读取代码文件               │   │
    │  • Write: 编辑/创建文件             │   │
    │  • Bash: 执行终端命令               │   │
    │  • MCP: 调用外部工具                │   │
    │                                     │   │
    │  ⚡ Hooks 在此处触发               │   │
    │    PreToolUse → 执行 → PostToolUse  │   │
    └────────────┬────────────────────────┘   │
                 │                            │
                 ▼                            │
    ┌─────────────────────────────────────┐   │
    │          验证 (Verify)              │   │
    │  • 检查执行结果                      │   │
    │  • 如果失败 → 修正方案 ─────────────┼───┘
    │  • 如果成功 → 继续下一步或结束       │
    └────────────┬────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │        输出结果 (Report)            │
    │  • 向用户报告完成情况               │
    │  • 等待下一条指令                   │
    └─────────────────────────────────────┘

### 2.2 核心机制

**为什么用"循环"而不是"一次性响应"？**

传统 AI 助手（如 ChatGPT）的工作方式是一问一答。但真实的编程任务往往需要：
1. 先读代码理解上下文
2. 再制定修改方案
3. 然后执行修改
4. 最后验证修改是否正确

这不是一步能完成的。所以 Claude Code 采用 Agentic Loop——循环执行直到任务完成。

**为什么需要权限系统？**

AI 直接操作你的文件系统是有风险的。Claude Code 的设计哲学是"**信任但验证**"：
- 默认每次文件修改、命令执行都需要你确认
- 你可以通过 `allowedTools` 配置自动批准你信任的操作
- Web 端会话在隔离沙箱中运行，限制网络和文件系统访问

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## Section 3: 局限性

1. **网络依赖**：每次交互都需要调用 Anthropic API，离线环境不可用 → **应对策略：** 关键操作前确保网络稳定
2. **上下文窗口限制**：超大代码库单次无法全部载入 → **应对策略：** 使用 `/compact` 压缩上下文，或让 Claude 分批处理
3. **非确定性**：同样的指令可能产生不同结果（LLM 本质） → **应对策略：** 用 Hooks 保证关键操作的确定性
4. **不适合实时补全**：终端模式没有行内自动补全 → **应对策略：** 配合 Cursor 或 Copilot 使用
5. **成本控制**：长对话消耗大量 token → **应对策略：** 使用 `--model haiku` 降低成本，或用 Max 订阅

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **Claude Code (终端)** | 全项目上下文、高自主性、可脚本化 | 无可视化 diff、学习曲线 | 终端爱好者、大代码库、CI/CD |
| **Claude Code (IDE 扩展)** | IDE 内使用、可视化 diff | 功能可能比终端版略少 | VS Code/JetBrains 用户 |
| **Cursor** | AI-native IDE、可视化编辑、多模型 | 非终端、需要付费 | 日常编码、快速迭代 |
| **GitHub Copilot** | 深度 GitHub 集成、团队协作 | 上下文较小、自主性中等 | GitHub 重度用户、团队项目 |
| **Devin** | 全自主 AI 工程师 | 成本高、控制力弱 | 完全委托的简单任务 |

> 📖 Docs: 综合对比来源

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview) | 📖 文档 | 全文核心参考 |
| [Claude Code Getting Started](https://docs.anthropic.com/en/docs/claude-code/getting-started) | 📖 文档 | Section 0 前置知识 |
| [Claude Code Memory](https://docs.anthropic.com/en/docs/claude-code/memory) | 📖 文档 | Section 2 核心机制 |
| [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) | 📖 文档 | Section 2 Hooks 触发点 |
| [Claude Code CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference) | 📖 文档 | Section 4 CLI 用法 |
| [Claude Code Common Workflows](https://docs.anthropic.com/en/docs/claude-code/common-workflows) | 📖 文档 | Section 1 核心价值 |
