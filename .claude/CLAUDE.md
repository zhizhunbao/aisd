# AISD Project

> 📌 完整规则请参考: `.shared/rules.md`

## Project Context

Personal AI study and development workspace.

## Directory Structure

```
.shared/          → 共享配置（skills, prompts, commands）
.github/          → 参考仓库
courses/          → 课程材料
```

## Quick Reference

**语言**: 中文解释，技术术语保留英文
**代码风格**: Python 4空格，JS/TS 2空格
**注释**: 双语注释（中+英）

## Common Commands

```bash
git pull origin main
git add . && git commit -m "message" && git push
uv sync && uv run python script.py
```

## Skills Location

All skills are in `.shared/skills/` directory.
Use `find_by_name` to discover available skills.
