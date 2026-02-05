# GitHub Copilot Instructions

> 这是 GitHub Copilot 的项目指令文件，整合了 `.shared/` 目录下的所有 skills、workflows 和 agents。

## 项目背景

这是一个个人 AI 学习和开发工作区 (AISD - AI Study & Development)。

**主要目录结构:**

- `.shared/` - 共享配置（skills, prompts, workflows, agents, templates）
- `.github/` - 参考仓库和 GitHub 配置
- `courses/` - 课程材料 (ml, mv, nlp, rl, pj)
- `data/` - 下载的课程数据

## 核心规则

### 语言和响应风格

- 使用**中文**进行解释和说明
- 技术术语保留英文（如 "PCA", "API", "SVM"）
- 响应要简洁、可操作、结构化
- 不确定时主动询问而非假设

### 代码规范

- Python: `snake_case`，4 空格缩进
- JavaScript/TypeScript: `camelCase`，2 空格缩进
- 每行最多 120 字符
- 使用双语注释（中文为主，技术术语保留英文）

## 可用的 Skills（130+）

### AI/学习类 Skills

| Skill 路径 | 用途 |
|------------|------|
| `.shared/skills/ai_learning-ml/` | 机器学习 |
| `.shared/skills/ai_learning-dl/` | 深度学习 |
| `.shared/skills/ai_learning-cv/` | 计算机视觉 |
| `.shared/skills/ai_learning-mv/` | 机器视觉 |
| `.shared/skills/ai_learning-nlp/` | 自然语言处理 |
| `.shared/skills/ai_learning-rl/` | 强化学习 |
| `.shared/skills/ai_learning-rag/` | RAG 技术 |
| `.shared/skills/ai_learning-llm/` | 大语言模型 |

### 开发类 Skills

| Skill 路径 | 用途 |
|------------|------|
| `.shared/skills/dev-senior_architect/` | 架构设计 |
| `.shared/skills/dev-senior_backend/` | 后端开发 |
| `.shared/skills/dev-senior_frontend/` | 前端开发 |
| `.shared/skills/dev-senior_fullstack/` | 全栈开发 |
| `.shared/skills/dev-code_reviewer/` | 代码审查 |
| `.shared/skills/dev-tdd_guide/` | TDD 指南 |
| `.shared/skills/dev-git/` | Git 操作 |
| `.shared/skills/dev-documentation_standards/` | 文档标准 |

### 学习类 Skills

| Skill 路径 | 用途 |
|------------|------|
| `.shared/skills/learning-brightspace_scraper/` | Brightspace 课程抓取 |
| `.shared/skills/learning-note_taking/` | 笔记整理 |
| `.shared/skills/learning-quiz_generation/` | 测验生成 |
| `.shared/skills/learning-code_generation/` | 代码生成 |
| `.shared/skills/learning-assignment_document/` | 作业文档 |
| `.shared/skills/learning-lab_submission/` | 实验提交 |
| `.shared/skills/learning-notebook_conversion/` | Notebook 转换 |
| `.shared/skills/learning-md_to_docx/` | Markdown 转 Word |

### 文档处理 Skills

| Skill 路径 | 用途 |
|------------|------|
| `.shared/skills/dev-docx_to_md/` | Word 转 Markdown |
| `.shared/skills/dev-pdf_processing/` | PDF 处理 |
| `.shared/skills/dev-translation/` | 翻译 |

## 可用的 Workflows

### 学习工作流

| 命令 | 文件 | 用途 |
|------|------|------|
| `/complete-lab [课程] [lab编号]` | `.shared/workflows/complete-lab.md` | 完成课程实验 |
| `/complete-lab-rl` | `.shared/workflows/complete-lab-rl.md` | 完成强化学习实验 |
| `/generate-study-material` | `.shared/workflows/generate-study-material.md` | 生成学习材料 |
| `/scrape-content` | `.shared/workflows/scrape-content.md` | 抓取课程内容 |
| `/explore-repo` | `.shared/workflows/explore-repo.md` | 探索代码仓库 |

### 开发工作流 (BMAD-METHOD)

| 阶段 | 目录 | 内容 |
|------|------|------|
| 1-分析 | `.shared/workflows/1-analysis/` | 创建产品简报、研究 |
| 2-规划 | `.shared/workflows/2-plan-workflows/` | PRD、UX 设计 |
| 3-方案 | `.shared/workflows/3-solutioning/` | 架构、用户故事 |
| 4-实现 | `.shared/workflows/4-implementation/` | 开发、代码审查 |
| 快速流程 | `.shared/workflows/bmad-quick-flow/` | 快速开发全流程 |

## 可用的 Agents

| Agent | 角色 | 文件 |
|-------|------|------|
| `analyst` | 需求分析师 | `.shared/agents/analyst.agent.yaml` |
| `pm` | 产品经理 | `.shared/agents/pm.agent.yaml` |
| `architect` | 架构师 | `.shared/agents/architect.agent.yaml` |
| `dev` | 开发者 | `.shared/agents/dev.agent.yaml` |
| `sm` | Scrum Master | `.shared/agents/sm.agent.yaml` |
| `tea` | 测试工程师 | `.shared/agents/tea.agent.yaml` |
| `ux-designer` | UX 设计师 | `.shared/agents/ux-designer.agent.yaml` |
| `quick-flow-solo-dev` | 独立开发者 | `.shared/agents/quick-flow-solo-dev.agent.yaml` |

## 常用命令

### 如何使用 Skill

```
读取 skill: .shared/skills/[skill-name]/SKILL.md
按照 skill 指导执行任务
```

### 如何执行 Workflow

```
读取 workflow: .shared/workflows/[workflow-name].md
按照步骤逐一执行
```

### 如何切换 Agent

```
切换到 [agent-name] 角色
读取 agent: .shared/agents/[agent-name].agent.yaml
以该角色身份工作
```

## 课程目录映射

| 课程代码 | 目录 | 全称 |
|----------|------|------|
| `ml` | `courses/ml/` | Machine Learning |
| `mv` | `courses/mv/` | Machine Vision |
| `nlp` | `courses/nlp/` | Natural Language Processing |
| `rl` | `courses/rl/` | Reinforcement Learning |
| `pj` | `courses/pj/` | Project |

## 模板

可用模板位于 `.shared/templates/`:

- `spec-template.md` - 规格文档模板
- `plan-template.md` - 技术方案模板
- `tasks-template.md` - 任务分解模板
- `checklist-template.md` - 检查清单模板
- `agent-file-template.md` - Agent 定义模板
- `spec-driven.md` - Spec-Driven 方法论

## Prompts

可用的 Prompt 模板位于 `.shared/prompts/`:

- `analysis-*` - 分析类
- `code-*` - 代码类
- `generation-*` - 生成类
- `learning-*` - 学习类
- `text_processing-*` - 文本处理类
- `format_conversion-*` - 格式转换类
- `test-*` - 测试类

---

**使用说明**: 当需要执行特定任务时，请参考对应的 skill 或 workflow 文件获取详细指导。
