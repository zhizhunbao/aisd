# Switch Agent

切换到指定的 Agent 角色。

## 使用方式

```
/switch-agent [agent-name]
```

## 可用 Agents

| Agent | 角色 | 适用场景 |
|-------|------|----------|
| `analyst` | 需求分析师 | 分析需求、研究问题 |
| `pm` | 产品经理 | 定义产品、编写 PRD |
| `architect` | 架构师 | 系统设计、技术选型 |
| `dev` | 开发者 | 编写代码、实现功能 |
| `sm` | Scrum Master | 项目管理、迭代规划 |
| `tea` | 测试工程师 | 测试设计、质量保证 |
| `ux-designer` | UX 设计师 | 用户体验设计 |
| `quick-flow-solo-dev` | 独立开发者 | 快速开发全流程 |

## 执行步骤

1. 读取 Agent 定义: `.shared/agents/{agent}.agent.yaml`
2. 理解角色职责和工作方式
3. 以该角色身份回答问题

## 示例

```
/switch-agent architect
请帮我设计这个系统的架构...
```

```
/switch-agent dev
请帮我实现这个功能...
```
