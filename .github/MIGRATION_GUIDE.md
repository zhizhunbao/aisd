# 工作流与 Skills 迁移指南

根据你的项目结构和需求（需求 → 设计 → 前端 → 后端 → 数据库 → 运维），以下是推荐迁移的内容。

---

## 一、推荐迁移的工作流 (Workflows)

### 来源：BMAD-METHOD

#### 1. 分析阶段 (1-analysis)
| 工作流 | 用途 | 迁移优先级 |
|--------|------|-----------|
| `create-product-brief` | 创建产品简介 | ⭐⭐⭐ |
| `research` | 需求调研 | ⭐⭐⭐ |

#### 2. 规划阶段 (2-plan-workflows)
| 工作流 | 用途 | 迁移优先级 |
|--------|------|-----------|
| `create-prd` | 创建产品需求文档 | ⭐⭐⭐ |
| `create-ux-design` | UX 设计 | ⭐⭐ |

#### 3. 方案阶段 (3-solutioning)
| 工作流 | 用途 | 迁移优先级 |
|--------|------|-----------|
| `create-architecture` | 系统架构设计 | ⭐⭐⭐ |
| `create-epics-and-stories` | 创建 Epic 和 Story | ⭐⭐⭐ |
| `check-implementation-readiness` | 实现准备检查 | ⭐⭐ |

#### 4. 实现阶段 (4-implementation)
| 工作流 | 用途 | 迁移优先级 |
|--------|------|-----------|
| `dev-story` | 开发 Story | ⭐⭐⭐ |
| `code-review` | 代码审查 | ⭐⭐⭐ |
| `create-story` | 创建开发任务 | ⭐⭐⭐ |
| `sprint-planning` | Sprint 规划 | ⭐⭐ |
| `correct-course` | 问题修正 | ⭐⭐ |
| `retrospective` | 回顾总结 | ⭐ |
| `sprint-status` | Sprint 状态 | ⭐ |

#### 5. 其他工作流
| 工作流 | 用途 | 迁移优先级 |
|--------|------|-----------|
| `bmad-quick-flow` | 快速开发流程 | ⭐⭐⭐ |
| `document-project` | 项目文档生成 | ⭐⭐ |
| `testarch` | 测试架构 | ⭐⭐ |

### 来源：spec-kit

| 模板/工作流 | 用途 | 迁移优先级 |
|-------------|------|-----------|
| `spec-template.md` | 规格文档模板 | ⭐⭐⭐ |
| `plan-template.md` | 技术方案模板 | ⭐⭐⭐ |
| `tasks-template.md` | 任务分解模板 | ⭐⭐⭐ |
| `checklist-template.md` | 检查清单模板 | ⭐⭐ |
| `agent-file-template.md` | Agent 定义模板 | ⭐⭐ |

---

## 二、推荐迁移的 Agents

### 来源：BMAD-METHOD/src/bmm/agents/

| Agent | 角色 | 职责 | 迁移优先级 |
|-------|------|------|-----------|
| `analyst` | 需求分析师 | 需求收集、分析、文档 | ⭐⭐⭐ |
| `pm` | 产品经理 | PRD、用户故事、验收标准 | ⭐⭐⭐ |
| `architect` | 架构师 | 系统设计、技术选型 | ⭐⭐⭐ |
| `dev` | 开发者 | 代码实现、单元测试 | ⭐⭐⭐ |
| `sm` | Scrum Master | Sprint 管理、进度跟踪 | ⭐⭐ |
| `tech-writer` | 技术作者 | 文档编写 | ⭐⭐ |
| `ux-designer` | UX 设计师 | 界面设计、交互设计 | ⭐⭐ |
| `tea` | 测试工程师 | 测试设计、自动化测试 | ⭐⭐ |
| `quick-flow-solo-dev` | 独立开发者 | 快速全栈开发 | ⭐⭐⭐ |

---

## 三、推荐迁移的 Skills

### 来源：claude-skills/engineering-team/ ⭐⭐⭐

| Skill | 用途 | 对应阶段 |
|-------|------|----------|
| `senior-architect` | 架构设计 | 设计 |
| `senior-backend` | 后端开发 | 后端 |
| `senior-frontend` | 前端开发 | 前端 |
| `senior-fullstack` | 全栈开发 | 前端+后端 |
| `senior-data-engineer` | 数据工程 | 数据库 |
| `senior-devops` | DevOps | 运维 |
| `senior-qa` | 质量保证 | 测试 |
| `senior-security` | 安全 | 全流程 |
| `code-reviewer` | 代码审查 | 实现 |
| `tdd-guide` | TDD 指南 | 实现 |
| `tech-stack-evaluator` | 技术栈评估 | 设计 |

### 来源：claude-skills/product-team/ ⭐⭐

| Skill | 用途 | 对应阶段 |
|-------|------|----------|
| `product-manager-toolkit` | 产品管理工具 | 需求 |
| `product-strategist` | 产品策略 | 需求 |
| `agile-product-owner` | 敏捷产品负责人 | 需求+管理 |
| `ux-researcher-designer` | UX 研究设计 | 设计 |
| `ui-design-system` | UI 设计系统 | 前端 |

### 来源：claude-skills/standards/ ⭐⭐⭐

| Skill | 用途 | 说明 |
|-------|------|------|
| `documentation` | 文档标准 | 代码和项目文档规范 |
| `git` | Git 标准 | 提交、分支、PR 规范 |
| `quality` | 质量标准 | 代码质量检查规范 |
| `security` | 安全标准 | 安全开发规范 |
| `communication` | 沟通标准 | 团队沟通规范 |

### 来源：skills (Anthropic 官方) ⭐⭐

| Skill | 用途 |
|-------|------|
| `frontend-design` | 前端设计 |
| `webapp-testing` | Web 应用测试 |
| `mcp-builder` | MCP 构建 |
| `skill-creator` | Skill 创建指南 |
| `doc-coauthoring` | 文档协作 |

---

## 四、与你现有 Skills 的整合

你已有的开发相关 Skills：
```
.shared/skills/
├── dev-code_comment      # 代码注释
├── dev-code_standards    # 代码标准
├── dev-code_style        # 代码风格
├── dev-git               # Git 规范
├── dev-markdown_check    # Markdown 检查
└── ...
```

### 建议的目标结构

```
.shared/skills/
├── # === 需求阶段 ===
├── dev-requirements/           # 新增：需求分析
├── dev-product-brief/          # 新增：产品简介
│
├── # === 设计阶段 ===
├── dev-architecture/           # 新增：系统架构
├── dev-api-design/             # 新增：API 设计
├── dev-ux-design/              # 新增：UX 设计
│
├── # === 数据库阶段 ===
├── dev-database/               # 新增：数据库设计
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── check-naming.py     # 命名检查
│   │   ├── check-schema.py     # 表结构检查
│   │   ├── check-fields.py     # 字段检查
│   │   └── check-indexes.py    # 索引检查
│   └── templates/
│       ├── migration.sql.j2
│       └── model.py.j2
│
├── # === 后端阶段 ===
├── dev-backend/                # 新增：后端开发
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── check-model.py      # Model 检查
│   │   ├── check-router.py     # Router 检查
│   │   ├── check-service.py    # Service 检查
│   │   ├── check-enum.py       # 枚举检查
│   │   └── check-api.py        # API 检查
│   └── templates/
│       ├── model.py.j2
│       ├── router.py.j2
│       ├── service.py.j2
│       └── schema.py.j2
│
├── # === 前端阶段 ===
├── dev-frontend/               # 新增：前端开发
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── check-component.py
│   │   ├── check-style.py
│   │   └── check-a11y.py       # 无障碍检查
│   └── templates/
│
├── # === 测试阶段 ===
├── dev-testing/                # 新增：测试
│   ├── SKILL.md
│   └── scripts/
│
├── # === 运维阶段 ===
├── dev-devops/                 # 新增：DevOps
│   ├── SKILL.md
│   └── scripts/
│
├── # === 通用/已有 ===
├── dev-code_comment/           # 已有
├── dev-code_standards/         # 已有
├── dev-code_style/             # 已有
├── dev-git/                    # 已有
├── dev-code_review/            # 新增：代码审查
└── ...
```

---

## 五、工作流目录结构

```
.agent/workflows/
├── # === 完整开发流程 ===
├── full-development/
│   ├── workflow.yaml
│   └── steps/
│       ├── 01-requirements.md
│       ├── 02-design.md
│       ├── 03-database.md
│       ├── 04-backend.md
│       ├── 05-frontend.md
│       ├── 06-testing.md
│       └── 07-deployment.md
│
├── # === 快速开发流程 ===
├── quick-flow/
│   ├── workflow.yaml
│   └── steps/
│
├── # === 单阶段流程 ===
├── feature-development/
├── bug-fix/
├── code-review/
├── sprint-planning/
└── retrospective/
```

---

## 六、迁移步骤

### 第一步：复制 Agent 定义
```bash
# 复制 BMAD 的 agent 定义
cp .github/BMAD-METHOD/src/bmm/agents/*.yaml .agent/agents/
```

### 第二步：复制工作流
```bash
# 复制核心工作流
cp -r .github/BMAD-METHOD/src/bmm/workflows/1-analysis/* .agent/workflows/
cp -r .github/BMAD-METHOD/src/bmm/workflows/2-plan-workflows/* .agent/workflows/
cp -r .github/BMAD-METHOD/src/bmm/workflows/3-solutioning/* .agent/workflows/
cp -r .github/BMAD-METHOD/src/bmm/workflows/4-implementation/* .agent/workflows/
```

### 第三步：复制 Skills
```bash
# 复制工程团队 skills
cp -r .github/claude-skills/engineering-team/senior-backend .shared/skills/dev-backend-ref
cp -r .github/claude-skills/engineering-team/senior-frontend .shared/skills/dev-frontend-ref
cp -r .github/claude-skills/engineering-team/code-reviewer .shared/skills/dev-code_review-ref

# 复制标准 skills
cp -r .github/claude-skills/standards/* .shared/skills/
```

### 第四步：创建检查脚本
根据需要在各 skill 的 `scripts/` 目录下创建检查脚本。

---

## 七、快速开始命令

复制以下最重要的内容：

```bash
# 1. Agent 定义
mkdir -p .agent/agents
cp .github/BMAD-METHOD/src/bmm/agents/analyst.agent.yaml .agent/agents/
cp .github/BMAD-METHOD/src/bmm/agents/architect.agent.yaml .agent/agents/
cp .github/BMAD-METHOD/src/bmm/agents/dev.agent.yaml .agent/agents/
cp .github/BMAD-METHOD/src/bmm/agents/pm.agent.yaml .agent/agents/

# 2. 核心工作流
cp -r .github/BMAD-METHOD/src/bmm/workflows/bmad-quick-flow .agent/workflows/

# 3. 工程 Skills
cp -r .github/claude-skills/engineering-team/senior-backend .shared/skills/
cp -r .github/claude-skills/engineering-team/senior-frontend .shared/skills/
cp -r .github/claude-skills/engineering-team/senior-architect .shared/skills/
cp -r .github/claude-skills/engineering-team/code-reviewer .shared/skills/

# 4. 标准 Skills
cp -r .github/claude-skills/standards/quality .shared/skills/dev-quality
cp -r .github/claude-skills/standards/security .shared/skills/dev-security
```

---

## 八、参考文件

- BMAD Agent 格式：`.github/BMAD-METHOD/src/bmm/agents/analyst.agent.yaml`
- BMAD Workflow 格式：`.github/BMAD-METHOD/src/bmm/workflows/`
- Spec-Kit 模板：`.github/spec-kit/templates/`
- Agent Skills 规范：`.github/skills/spec/`
- Claude Skills 示例：`.github/claude-skills/engineering-team/`
