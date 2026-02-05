# Commit Message 生成指令

## 格式
使用 Conventional Commits 格式:
```
type(scope): description

[optional body]

[optional footer]
```

## 类型 (type)
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（不新增功能或修复 bug）
- `test`: 测试相关
- `chore`: 构建/工具相关

## 作用域 (scope)
基于项目目录:
- `ml`: 机器学习课程
- `mv`: 机器视觉课程
- `nlp`: 自然语言处理课程
- `rl`: 强化学习课程
- `skills`: .shared/skills
- `workflows`: .shared/workflows
- `config`: 配置文件

## 示例
```
feat(ml): add lab3 CNN implementation
fix(nlp): correct tokenization bug in lab2
docs(skills): update brightspace scraper usage
chore(config): update copilot instructions
```
