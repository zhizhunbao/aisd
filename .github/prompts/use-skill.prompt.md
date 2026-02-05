# Use Skill

加载并使用指定的 Skill。

## 使用方式

```
/use-skill [skill-category]-[skill-name]
```

## 可用 Skill 分类

### AI 学习类 (ai_learning-*)
- `ai_learning-ml`: 机器学习
- `ai_learning-dl`: 深度学习
- `ai_learning-cv`: 计算机视觉
- `ai_learning-nlp`: 自然语言处理
- `ai_learning-rl`: 强化学习

### 开发类 (dev-*)
- `dev-senior_architect`: 架构设计
- `dev-senior_backend`: 后端开发
- `dev-code_reviewer`: 代码审查
- `dev-git`: Git 操作
- `dev-documentation_standards`: 文档标准

### 学习类 (learning-*)
- `learning-brightspace_scraper`: Brightspace 抓取
- `learning-note_taking`: 笔记整理
- `learning-code_generation`: 代码生成
- `learning-quiz_generation`: 测验生成

## 执行步骤

1. 定位 Skill: `.shared/skills/{skill-name}/SKILL.md`
2. 读取 Skill 内容
3. 按照 Skill 指导执行任务

## 示例

```
/use-skill dev-code_reviewer
请审查这段代码...
```

```
/use-skill learning-note_taking
帮我整理这节课的笔记...
```
