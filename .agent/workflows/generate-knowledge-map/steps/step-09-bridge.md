# Phase 9: DIM-8 Bridge（跨主题衔接）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Connector |
| **技能** | knowledge-map-format (DIM-8) |
| **前置条件** | Phase 8（History）完成或跳过 |
| **输出** | `{topic}_bridge.md` |
| **预计时间** | 15-30 分钟 |

## 设计理论依据

| 章节 | 格式设计 | 教科书依据 |
|------|---------|-----------|
| `## ← 上一个 / 下一个 →` | 前后导航表 | Ausubel《Educational Psychology》(1968), Ch.14 "Advance Organizers" — 新旧知识必须有明确的锚定连接 |
| `## 上游依赖` + `## 下游影响` | 概念复用追踪 | Gagné《Conditions of Learning》Ch.3 "Learning Hierarchies" — 每个技能建立在前置技能上，必须明确依赖关系 |
| `## 概念演变追踪` | 早期 vs 现代做法 | Kuhn《The Structure of Scientific Revolutions》(1962) — 概念不是静态的，会随范式转换而演变 |
| `## 扩展阅读` 分三层 | 深入/横向/上层 | Bloom《Taxonomy》— 对应 Analysis(深入) → Synthesis(横向对比) → Evaluation(上层应用) 三个认知层次 |
| 同课程相对链接 | `../` 路径内链 | 知识网络化 — 孤立的知识点不是知识，关联起来才是 |

## 固定 6 章模板

```
---
topic: {topic}
dimension: bridge
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📚 Book: ..."
expiry: 12m
status: current
---

# {Topic} 衔接与扩展

> 📚 Book: 作者, 《书名》, Ch.X

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 前置主题 A | 关系说明 | [链接](相对路径) |
| → 后续 | 后续方向 A | 关系说明 | — |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [论文名](URL) | 📖 论文 | 原因 | ⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
```

## 格式规则

- ✅ `← 前置` / `→ 后续` 标注方向
- ✅ 有链接用 `[链接](路径)`，无链接用 `—`
- ✅ 同课程用 `../`，跨课程用 `../../`
- ✅ 扩展阅读分三层 + 难度星级

## 完成检查

- [ ] 6 章结构完整
- [ ] 双向更新：相关主题的 Bridge 也已更新
- [ ] 相对链接路径正确

## 教科书来源

- Ausubel《Educational Psychology: A Cognitive View》(1968), Ch.14 "Advance Organizers"
- Gagné《The Conditions of Learning》4th Ed. (1985), Ch.3 "Learning Hierarchies"
- Kuhn《The Structure of Scientific Revolutions》(1962)
- Bloom《Taxonomy of Educational Objectives》(1956)
