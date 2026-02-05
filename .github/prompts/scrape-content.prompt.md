# Scrape Content

从 Brightspace 或网页抓取内容。

## 使用方式

指定来源和目标:
- 来源: brightspace | web
- 课程/URL
- 模块类型 (可选): slides | labs | assignments

## 执行步骤

1. **读取工作流**: `.shared/workflows/scrape-content.md`
2. **读取 Skill**: `.shared/skills/learning-brightspace_scraper/SKILL.md`
3. **执行抓取**: 运行抓取脚本
4. **组织文件**: 保存到正确目录

## 前置要求

需要先完成 Brightspace 登录:
```bash
cd .shared/skills/learning-brightspace_scraper/scripts
uv run python run.py --login-only
```

## 示例

```
/scrape-content brightspace ml slides
```

```
/scrape-content brightspace nlp labs
```
