---
name: full-dev
description: 完整软件开发流程 - 从需求到上线
trigger: /full-dev
arguments:
  - name: action
    description: 操作类型 (status/reset/skip/goto)
    required: false
  - name: phase
    description: 目标阶段 (用于 goto)
    required: false
---

# /full-dev - 完整开发工作流

启动或继续完整的软件开发流程。

## 使用方法

```bash
/full-dev                      # 启动或继续工作流
/full-dev status               # 查看当前进度
/full-dev reset                # 重置，从头开始
/full-dev skip                 # 跳过当前阶段
/full-dev goto architecture    # 跳转到指定阶段
```

## 工作流阶段

1. **requirements** - 需求分析
2. **prd** - 产品需求文档
3. **architecture** - 系统架构
4. **stories** - 任务分解
5. **database** - 数据库设计
6. **backend** - 后端开发
7. **frontend** - 前端开发
8. **testing** - 测试
9. **review** - 代码审查
10. **deployment** - 部署

## 执行指令

当用户调用此命令时：

1. 读取工作流定义：`.shared/workflows/full-development/workflow.md`
2. 检查状态文件：`.dev-state.yaml`
3. 根据参数执行相应操作
4. 加载并执行对应的 step 文件

### 无参数调用

```
读取 .dev-state.yaml
如果不存在：
    从 state-template.yaml 创建
    询问项目信息
    执行 step-00-init.md

如果存在：
    显示当前进度
    确定下一个待执行阶段
    检查是否可自动跳过
    执行对应 step 文件
```

### status 参数

```
读取 .dev-state.yaml
显示：
    - 项目名称
    - 开始时间
    - 各阶段状态
    - 预计完成度
```

### reset 参数

```
确认重置？[y/N]
如果确认：
    删除 .dev-state.yaml
    显示 "状态已重置，使用 /full-dev 重新开始"
```

### skip 参数

```
当前阶段：{current_phase}
确认跳过？[y/N]
如果确认：
    标记当前阶段为 skipped
    进入下一阶段
```

### goto 参数

```
/full-dev goto {phase_name}

验证 phase_name 有效
检查依赖是否满足
如果满足：
    更新 current_phase
    执行该阶段
如果不满足：
    显示 "需要先完成: {missing_deps}"
```

## 自动跳过逻辑

对于每个阶段，检查产出物：

| 阶段 | 检查文件 |
|------|----------|
| requirements | `docs/requirements.md` |
| prd | `docs/prd.md` |
| architecture | `docs/architecture.md` |
| stories | `docs/stories.md` |
| database | `docs/database.md` |
| backend | 运行检查脚本 |
| frontend | 运行检查脚本 |
| testing | 测试通过 |
| review | `docs/review-report.md` |
| deployment | 部署状态 |

如果产出物存在且有效，自动标记为完成并跳过。

## 相关文件

- 工作流定义：`.shared/workflows/full-development/workflow.md`
- 状态模板：`.shared/workflows/full-development/state-template.yaml`
- Step 文件：`.shared/workflows/full-development/steps/`
