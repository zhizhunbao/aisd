# Phase 0: Pre-Flight 检查

## 概述

| 项 | 值 |
|----|---|
| **前置条件** | 无 |
| **输出** | 模板已加载到上下文 |
| **预计时间** | < 1 分钟 |

## 目标

确保格式模板和规则已加载到上下文。

> ⛔ **无论是新会话还是中断恢复，都必须先执行本步骤，否则不允许写任何文件。**

## 执行步骤

### 1. 必须执行的读取操作

按顺序读取以下文件：

1. **格式规则**（R1-R8 + 来源白名单 + 论文下载）：
   - 路径：`.agent/workflows/generate-knowledge-map/references/format_rules.md`

2. **当前要执行的 step 文件**（包含教科书依据 + 完整模板 + 检查清单）：
   - 根据 `.km-state.yaml` 中的 `current_phase` 确定阶段编号
   - 路径：`.agent/workflows/generate-knowledge-map/steps/step-{阶段编号}-{阶段名}.md`
   - 例如：Phase 2 → `steps/step-02-map.md`，Phase 7 → `steps/step-07-pitfalls.md`

3. **目标课程/工具目录**（确认已存在）：
   - 课程类：`knowledge-map/courses/<课程>/`
   - 工具类：`knowledge-map/tools/<领域>/`

### 2. 模板确认

> **唯一权威来源是各 step 文件**（每个 step 文件包含：教科书依据 + 完整模板 + 格式规则 + 检查清单）。
> 格式规则 R1-R8 在 `format_rules.md`。

- [ ] 已读取 `format_rules.md` 来源白名单 + 格式规则
- [ ] 已读取当前维度的 step 文件（如 `step-02-map.md`）
- [ ] 已确认目标课程/工具目录存在
- [ ] 已确认 `source_versions` Frontmatter 格式

### 3. 中断恢复规则

> 若会话被截断，摘要信息**不可信任**，必须重新执行步骤 1 读取模板。

