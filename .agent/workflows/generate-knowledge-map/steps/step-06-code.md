# Phase 6: DIM-5 Code（代码参考）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Code Engineer |
| **技能** | knowledge-map-format (DIM-5), learning-code-generation, code-comment |
| **前置条件** | Phase 5（Tutorial）完成 |
| **输出** | `{topic}_code.md` |
| **预计时间** | 20-40 分钟 |

## 设计理论依据

| 章节 | 格式设计 | 教科书依据 |
|------|---------|-----------|
| `## 快速开始` | **最简示例先行**，N 秒可跑 | Carroll《The Nurnberg Funnel: Designing Minimalist Instruction》(1990) — Minimalist Instruction: 用户想先跑起来再理解，不是先读完理论再动手 |
| 中英双语注释 | 每行注释中英并排 | Cummins (2000) — 双语标注降低 L2 切换成本；针对非英语母语学生 |
| `# ====` 分隔符 | 代码区块用 `# ============` 分隔 | Norman《Design of Everyday Things》Ch.1 — "Signifiers": 视觉分隔符告诉用户这里是新段落 |
| `## API 速查` | 子参数用 `↳` 缩进 | 速查表设计 = 外化记忆：不需要记住 API，翻一下就行 |
| `## 目录结构` | 简单/标准/高级三级模板 | Bloom《Taxonomy》— 不同熟练度用不同复杂度的结构 |

## 固定 4 章模板

````
---
topic: {topic}
dimension: code
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📖 Docs: ..."
expiry: 6m
status: current
---

# {Topic} 代码参考

> 📖 Docs: [主要来源](URL)

## 快速开始

### 最简示例 — N 秒上手

```python
# 最简示例代码 / Minimal example
...
```

**测试方法：** 如何验证

---

## 完整实现示例

### 示例 1: {名称}

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
...

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
...
```

---

## API 速查

### {分类}

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `函数名()` | `参数名` | 默认值 | 说明 |
| ↳ `子参数` | 类型 | 默认值 | 说明 |

---

## 目录结构模板

### 简单结构

```
project/
├── train.py              ← 训练脚本
├── model.py              ← 模型定义
└── data/
    ├── train/
    └── val/
```

### 标准结构

```
project/
├── config.py
├── dataset.py
├── model.py
├── train.py
├── evaluate.py
├── utils.py
├── data/
├── checkpoints/
└── logs/
```
````

## 格式规则

- ✅ 快速开始可直接复制运行
- ✅ 完整示例用 `# ===========` 分隔
- ✅ 所有代码有中英双语注释
- ✅ API 速查用 `↳` 缩进子参数

## 完成检查

- [ ] 快速开始代码可直接运行
- [ ] 至少 2 个完整实现示例
- [ ] API 速查表存在

## 教科书来源

- Carroll《The Nurnberg Funnel: Designing Minimalist Instruction》(1990)
- Norman《The Design of Everyday Things》Revised Ed. (2013), Ch.1 "Signifiers"
- Bloom《Taxonomy of Educational Objectives》(1956)
