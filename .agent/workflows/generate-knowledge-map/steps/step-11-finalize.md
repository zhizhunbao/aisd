# Phase 11: 收尾 (Finalize)

## 概述

| 项 | 值 |
|----|---|
| **角色** | QA |
| **前置条件** | Phase 10（First Principles）完成或跳过 |
| **输出** | Map 回填 + README 更新 |
| **预计时间** | 10-15 分钟 |

## 执行步骤

### 1. 回填 Map

- 更新文件地图（`## 4`）：标注实际生成的文件
- 更新缺口检查（`## 6`）：标注 ✅/⬜/~~不适用~~
- 更新新鲜度状态（`## 7`）
- 更新参考来源表（`## 8`）：汇总所有维度的引用

### 2. 双向更新 Bridge

如果相关主题已存在，更新其 Bridge 文件中的相关引用。

### 3. 更新课程 README

`knowledge-map/courses/<课程>/README.md`:
- 主题状态从 `🔲 planned` → `✅ current`
- 更新文件数和描述

### 4. 质量检查

- [ ] 每个声明有来源？
- [ ] Tutorial Why-First？
- [ ] Code 30 秒可跑？
- [ ] Pitfalls 有 ❌/✅ 对比？
- [ ] 交叉引用链接有效？

### 5. 格式检查清单

- [ ] **R1 Frontmatter** — 每个文件都有完整 frontmatter
- [ ] **R2 引证** — 每个 `##` 章节结尾都有 `>` 引证块
- [ ] **R3 无嵌套** — 没有嵌套代码块
- [ ] **R4 对比格式** — ❌/✅ 用缩进
- [ ] **R5 分隔线** — `##` 之间有 `---`
- [ ] **R6 标题引证** — `# 标题` 下紧跟全局引证行
- [ ] **R7 来源白名单** — 仅允许 📖论文/📚教科书/📖文档/💻源码
- [ ] **R8 素材目录** — 教科书/论文/文档/源码存放路径正确

## 元数据标准

```yaml
---
topic: conv_layer
course: deep-learning
dimension: tutorial
created: 2026-03-11
last_verified: 2026-03-11
source_versions:
  - "Goodfellow et al., Deep Learning, Ch.9 (2016)"
expiry: 6m
status: current
---
```

| 主题类型 | expiry |
|---------|--------|
| 快速迭代工具 | 3m |
| 稳定基础设施 | 6m |
| 数学/理论 | 12m |
| 教科书 | never |
