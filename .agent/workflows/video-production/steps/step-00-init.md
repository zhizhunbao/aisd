# Phase 0: 初始化 (Init)

## 概述

| 项 | 值 |
|----|---|
| **角色** | — (自动) |
| **技能** | — |
| **前置条件** | 知识地图 9 维文件存在 |
| **输出** | `.video-state.yaml` |
| **预计时间** | < 1 分钟 |

## 执行步骤

### 1. 验证知识地图

检查 `knowledge-map/courses/{course}/{topic}/` 目录：

- [ ] `{topic}_map.md` 存在
- [ ] `{topic}_concepts.md` 存在
- [ ] `{topic}_tutorial.md` 存在
- [ ] `{topic}_pitfalls.md` 存在
- [ ] `{topic}_history.md` 存在
- [ ] `{topic}_first_principles.md` 存在
- [ ] 至少 6/9 维文件存在

### 2. 创建工作目录

```
video-content/{course}/{topic}/
├── narration/
├── assets/
└── .video-state.yaml
```

### 3. 初始化状态文件

从 `state-template.yaml` 复制并填入项目信息：
- `topic`: 主题名
- `course`: 课程名
- `knowledge_map_path`: 知识地图路径
- `started_at`: 当前时间

### 4. 选择痛点

从 `{topic}_pitfalls.md` 中选择 1-2 个目标观众最可能遇到的痛点。
这决定了整个视频的切入角度。

## 完成检查

- [ ] `.video-state.yaml` 创建且字段完整
- [ ] 知识地图验证通过
- [ ] 痛点已选择并记录

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- Heath《Made to Stick》Ch.1: "Simple" — 找到核心信息（痛点选择方法论）
  - MinerU: `data/mineru_output/heath_made_to_stick/heath_made_to_stick/hybrid_auto/heath_made_to_stick.md`
