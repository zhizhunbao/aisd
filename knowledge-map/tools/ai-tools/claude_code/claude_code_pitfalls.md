---
topic: claude_code
dimension: pitfalls
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📖 Docs: Anthropic Claude Code Overview — https://docs.anthropic.com/en/docs/claude-code/overview"
  - "📖 Docs: Anthropic Claude Code Troubleshooting — https://docs.anthropic.com/en/docs/claude-code/troubleshooting"
  - "📖 Docs: Anthropic Claude Code Memory — https://docs.anthropic.com/en/docs/claude-code/memory"
  - "🧪 经验: 实际使用 Claude Code 过程中积累的踩坑记录"
expiry: 3m
status: current
---

# Claude Code 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: CLAUDE.md 写了但 Claude 不遵守

**痛点类别：** 概念误解——以为 CLAUDE.md 是"强制规则"

**场景：** 在 CLAUDE.md 中写了详细的编码规范（如"不要用 `any` 类型"），但 Claude Code 生成的代码仍然包含 `any`。

**症状：** Claude 看似"忽略"了 CLAUDE.md 中的指令

**根因：** CLAUDE.md 是**上下文提示**，不是**强制约束**。LLM 可能因为上下文过长、指令优先级竞争、或任务复杂度导致遗漏。此外，CLAUDE.md 太长（> 500 行）会降低遵守率。

**解法：**

❌ 错误做法 — 把所有规则塞进一个巨大的 CLAUDE.md

```markdown
# CLAUDE.md (500+ 行的规则清单)
- 不要用 any
- 不要用 var
- 函数不超过 30 行
- 必须有 JSDoc
- 必须用 camelCase
- ... (还有几百条)
```

✅ 正确做法 — 精简核心规则 + 分层 CLAUDE.md + 用 Hooks 做强制检查

```markdown
# CLAUDE.md (精简版，< 100 行)
## 铁律（必须遵守）
- TypeScript strict mode，禁止 any
- 每个函数必须有 JSDoc

## 偏好（尽量遵守）
- 函数 < 30 行
- 使用 React hooks 模式
```

```json
// .claude/settings.json — 用 Hook 强制 lint
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "npx eslint --fix $CLAUDE_FILE_PATH"
      }]
    }]
  }
}
```

**教训：** CLAUDE.md 越短越好，核心规则用 Hooks 强制保障，不要靠 LLM 记住所有规则。

> 📖 Docs: Anthropic, [Claude Code Memory](https://docs.anthropic.com/en/docs/claude-code/memory)

---

## 坑 2: 上下文爆了，Claude 开始"忘事"

**痛点类别：** 概念误解——不理解上下文窗口限制

**场景：** 在一个长对话中做了很多操作，到后期 Claude 开始"忘记"之前的讨论，重复问已经回答过的问题，或修改了不该改的文件。

**症状：** Claude 的回复质量明显下降，或与之前的讨论不一致

**根因：** Claude 的上下文窗口有限（约 200K tokens），长对话会导致早期上下文被截断。Claude Code 有自动压缩机制，但压缩过程中会丢失细节。

**解法：**

❌ 错误做法 — 所有事情在一个会话里做完

```bash
# 一个会话干 2 小时，做了 20 个不同的任务
claude
> fix bug in auth
> now add payment feature
> also refactor the database
> and update all tests
> ...
```

✅ 正确做法 — 一任务一会话 + 主动压缩

```bash
# 任务 1: 修 bug
claude "fix the auth token expiry bug"

# 任务 2: 新功能（新会话）
claude "add Stripe payment integration"

# 长任务中主动压缩
# 在 Claude Code 中输入:
/compact
```

**教训：** 把大任务拆成小会话，每个会话只做一件事。长会话用 `/compact` 主动压缩。

> 📖 Docs: Anthropic, [Claude Code CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

---

## 坑 3: 权限弹窗太多，效率低

**痛点类别：** 工具配置——不知道如何优化权限

**场景：** Claude 每次读文件、写文件、运行测试都弹出确认框，需要一直点"Allow"，感觉比手动还慢。

**症状：** 频繁的权限确认打断工作流

**根因：** Claude Code 默认采用最严格的权限模式。这是出于安全考虑，但对于受信任的操作（如运行测试、格式化代码），可以配置自动批准。

**解法：**

❌ 错误做法 — 忍受每次确认 或 直接关闭所有权限检查

✅ 正确做法 — 精细化配置 allowedTools

```json
// .claude/settings.json
{
  "permissions": {
    "allowedTools": [
      "Read",
      "Grep",
      "Glob",
      "bash(npm run test*)",
      "bash(npm run lint*)",
      "bash(npx prettier*)",
      "bash(git status)",
      "bash(git diff*)"
    ]
  }
}
```

**教训：** 用 `allowedTools` 白名单批准你信任的操作，但不要批准 `bash(*)` 这种过于宽泛的规则。

> 📖 Docs: Anthropic, [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

---

## 坑 4: Claude 在错误的目录下运行

**痛点类别：** 代码执行——目录上下文错误

**场景：** 在 monorepo 中运行 Claude Code，它把前端的修改写到了后端目录，或在根目录运行了只在子包目录才有效的命令。

**症状：** 文件被写入错误位置 / 命令执行失败

**根因：** Claude Code 以当前工作目录为项目根。在 monorepo 中，如果从根目录启动，Claude 可能不清楚每个子包的边界。

**解法：**

❌ 错误做法 — 在 monorepo 根目录启动并处理所有子包

```bash
cd ~/my-monorepo
claude "fix the auth bug in the frontend"
# Claude 可能在根目录找 package.json，找不到
```

✅ 正确做法 — 在正确的子包目录启动 + CLAUDE.md 标注结构

```bash
# 方法 1: 在子包目录启动
cd ~/my-monorepo/packages/frontend
claude "fix the auth bug"

# 方法 2: 在根目录 CLAUDE.md 说明结构
```

```markdown
# CLAUDE.md (monorepo 根目录)
## 项目结构
- packages/frontend/ — React 前端 (npm run dev)
- packages/backend/ — Node.js 后端 (npm run start)
- packages/shared/ — 共享类型和工具
注意：每个子包有独立的 package.json 和 tsconfig.json
```

**教训：** Monorepo 用户要么在子包目录启动，要么用 CLAUDE.md 明确标注项目结构。

> 🧪 经验: Monorepo 项目中的实际踩坑

---

## 坑 5: 用 Claude Code 改代码但没有 Git，改坏了回不去

**痛点类别：** 安全意识——不做备份就让 AI 改代码

**场景：** 在一个没有 Git 初始化的临时项目中使用 Claude Code，Claude 改错了代码但没有版本记录可以回滚。

**症状：** 代码被改坏，无法恢复

**根因：** Claude Code 直接操作文件系统，它的修改是**不可逆的**（除非有 Git）。

**解法：**

❌ 错误做法 — 在没有 Git 的目录里直接让 Claude 修改

```bash
cd ~/random-scripts/  # 没有 git init
claude "refactor everything"
# 改坏了，无法回滚
```

✅ 正确做法 — 先 Git 提交，再让 Claude 修改

```bash
git init && git add -A && git commit -m "checkpoint before Claude"
claude "refactor the auth module"
# 如果改坏了:
git diff          # 查看修改
git checkout .    # 一键回滚
```

**教训：** 永远在有 Git 的环境下使用 Claude Code。让 Claude 改代码前先 commit 一个 checkpoint。

> 🧪 经验: 新手常见失误

---

## 坑 6: 费用失控——不知不觉花了很多钱

**痛点类别：** 成本管理——不了解 token 消耗

**场景：** 使用 API Key 模式，一个下午做了很多复杂任务，月底发现账单远超预期。

**症状：** Anthropic 账单异常高

**根因：** Claude Code 的 Agentic Loop 会自动多轮工具调用，每轮都消耗 token。复杂任务可能执行 10-20 轮，每轮都有大量代码上下文。

**解法：**

❌ 错误做法 — 不关注费用，用 Opus 做简单任务

✅ 正确做法 — 监控费用 + 选对模型

```bash
# 查看当前会话费用
# 在 Claude Code 中输入:
/cost

# 简单任务用 Haiku（便宜 10x）
claude --model haiku "fix this typo"

# 复杂任务用 Sonnet
claude --model sonnet "refactor the entire auth module"

# 限制最大轮次
claude -p "fix lint errors" --max-turns 5
```

**教训：** 用 `/cost` 监控费用，简单任务用 Haiku，限制 `--max-turns` 防止无限循环消耗。或直接用 Max 订阅（月费封顶）。

> 📖 Docs: Anthropic, [Claude Code CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

---

## 超级避坑指南

### 学习避坑

1. [ ] **别把 CLAUDE.md 当万能** → 核心规则用 Hooks 强制，CLAUDE.md 只放最重要的
2. [ ] **别在一个会话做太多事** → 一任务一会话，用 `/compact` 管理上下文
3. [ ] **别忽视权限配置** → 花 5 分钟配置 `allowedTools`，节省几小时的确认点击
4. [ ] **别跳过 Git** → 让 Claude 改代码前必须先 commit

### 作业/项目避坑

1. [ ] **先在小项目练手** → 不要上来就在生产代码上用
2. [ ] **先看 Claude 的修改再批准** → 特别是删除操作
3. [ ] **Monorepo 用户在子包目录启动** → 避免上下文混乱
4. [ ] **用 `/init` 生成 CLAUDE.md** → 比自己从头写更靠谱

### 调试清单（技术类）

1. [ ] **Claude Code 启动失败？** → 运行 `/doctor` 诊断，检查 Node.js 版本 >= 18
2. [ ] **Claude 读不到文件？** → 检查是否在正确的项目目录，检查 `.gitignore` 是否排除了目标文件
3. [ ] **MCP Server 连不上？** → 检查 `.claude/mcp.json` 配置，确认 Server 进程正常运行
4. [ ] **Hooks 不触发？** → 检查 `settings.json` 中 matcher 是否正确（区分大小写）
5. [ ] **费用异常？** → 输入 `/cost` 查看，考虑切换 `--model haiku` 或加 `--max-turns`

> 📖 Docs: Anthropic, [Claude Code Troubleshooting](https://docs.anthropic.com/en/docs/claude-code/troubleshooting)
