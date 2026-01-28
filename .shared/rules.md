# Shared AI Agent Rules

> 这是所有 AI 编程助手平台的共享规则文件。
> 各平台配置文件应引用此文件以保持一致性。

## Project Context / 项目背景

This is a personal AI study and development workspace (AISD).

**主要目录结构:**

- `.shared/` - 共享配置（skills, prompts, commands）
- `.github/` - 参考仓库
- `courses/` - 课程材料

## Coding Standards / 代码规范

### 命名规范

- 使用描述性的变量和函数名
- Python: `snake_case`
- JavaScript/TypeScript: `camelCase`

### 注释规范

- 使用双语注释（中文为主，技术术语保留英文）
- 文件顶部添加块注释说明用途
- 复杂逻辑需要注释解释

### 格式规范

- Python: 4 空格缩进
- JavaScript/TypeScript: 2 空格缩进
- 每行最多 120 字符

## AI Behavior Guidelines / AI 行为准则

1. **语言**: 使用中文进行解释和说明
2. **技术术语**: 保留英文原文，如 "PCA"、"API"
3. **响应风格**: 简洁、可操作、结构化
4. **不确定时**: 主动询问而非假设
5. **修改文件**: 显示变更差异（diff）

## Common Commands / 常用命令

```bash
# Git 操作
git pull origin main
git add . && git commit -m "message" && git push

# Python 环境
uv sync
uv run python script.py
```

## Platform-Specific Notes / 平台特定说明

| 平台        | 配置入口            | 引用方式                    |
| ----------- | ------------------- | --------------------------- |
| Claude Code | `.claude/CLAUDE.md` | 直接引用此文件内容          |
| Antigravity | `.agent/`           | 通过 `.shared/skills/` 引用 |
| Kiro        | `.kiro/steering/`   | 复制核心规则                |
| Windsurf    | `.windsurfrules`    | 复制核心规则                |
