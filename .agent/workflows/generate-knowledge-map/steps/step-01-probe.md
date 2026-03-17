# Phase 1: 输入探测 (Probe)

## 概述

| 项 | 值 |
|----|---|
| **角色** | Source Researcher |
| **前置条件** | Phase 0 通过 |
| **输出** | 素材报告 + 生成计划 |
| **预计时间** | 5-15 分钟 |

## 执行步骤

### 1. 验证目标路径

- 课程类: `knowledge-map/courses/<课程>/` 必须存在 `_course.md` + `README.md`
- 工具类: `knowledge-map/tools/<领域>/` 必须存在
- 项目类: `knowledge-map/projects/<项目>/` 必须存在

### 2. 扫描可用素材

| 素材位置 | 用途 |
|---------|------|
| `textbooks/` + `data/mineru_output/` | 教科书 PDF + MinerU 解析 |
| `.github/` | 开源参考代码 |
| `knowledge-map/courses/<课程>/` | 同课程已有主题（用于 Bridge） |
| `knowledge-map/courses/<课程>/_course.md` | 课程名词总表 |

### 3. 主题粒度判断

满足任一则拆分: 核心概念 > 15 个 / 跨越多层次 / Tutorial 预估 > 3000 字

### 4. 来源充分性检查

| 维度 | 最低来源要求 |
|------|-------------|
| Concepts | 1 个权威来源 |
| Math | 必须有教科书/论文 |
| Tutorial | 1 官方文档 + 1 教科书 |
| Code | 1 个参考实现 |
| Pitfalls | 1 个来源 |

来源不足时按优先级补齐: ① `download_papers.py` → ② `search_web` → ③ 教科书兜底

### 5. 论文下载失败处理（不阻塞）

终止脚本 → 在 `source_versions` 标注占位符 → 创建 `papers_index.md` → 继续生成

### 6. 向用户确认

展示素材报告和生成计划。
