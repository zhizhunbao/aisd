# Phase 2: DIM-1 Map（导航地图）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Navigator |
| **技能** | knowledge-map-format (DIM-1) |
| **前置条件** | Phase 1 通过 |
| **输出** | `{topic}_map.md` |
| **预计时间** | 15-30 分钟 |

## 设计理论依据

| 章节 | 格式设计 | 教科书依据 |
|------|---------|-----------| 
| `## 1. 核心问题` | 3-5 个问题，每行末尾 → 答案 | Wiggins & McTighe《Understanding by Design》Ch.5: "Essential Questions" — 学习应从核心问题出发，不是从内容大纲出发 |
| `## 2. 全景位置` | ASCII 树，标注 `← 你在这里` | Ausubel《Educational Psychology》Ch.14: "Advance Organizers" — 新知识必须先锚定在已有认知结构上，全景图就是 organizer |
| `## 3. 依赖地图` | 前置→本主题→后续 三栏图 | Gagné《The Conditions of Learning》Ch.3: "Learning Hierarchies" — 技能有前置依赖，不能跳过底层直接学上层 |
| `## 4. 文件地图` | 表格 + ① ② ③ 编号 | Norman《The Design of Everyday Things》Revised Ed. (2013), Ch.3: "Knowledge in the World" — 把记忆负担外化到文档，用编号降低查找成本 |
| `## 5. 学习路线` | 三小节：初学/日常/深度 | Bloom《Taxonomy of Educational Objectives》(1956) — 认知从低到高递进，不同阶段需要不同文件 |
| `## 6. 缺口检查` | ✅/⬜/~~删除线~~ | Gawande《The Checklist Manifesto》Ch.2 — 清单防遗漏，视觉化状态降低认知负荷 |
| `## 7. 新鲜度状态` | expiry + status 标注 | Hunt & Thomas《The Pragmatic Programmer》(1999), Tip 27 "Don't Outrun Your Headlights" — 知识有保鲜期，过期内容比没有内容更危险 |
| `## 8. 参考来源表` | 汇总所有维度的引用 | 学术规范 — 集中管理引用方便验证和审计 |

## 固定 8 章模板

```
---
topic: {topic}
dimension: map
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📚 Book: 书名 — Ch.X"
  - "📖 Paper: 作者 年份"
  - "📖 Docs: 名称"
expiry: 12m
status: current
---

# {Topic} 知识地图

> 📚 Book: 作者, [《书名》](../../../textbooks/书名.pdf), Ch.X
> 📖 Paper: 作者, [论文名](URL)

## 1. 核心问题

- **问题1？** → 一句话回答
- **问题2？** → 一句话回答
- **问题3？** → 一句话回答
（3-5 个问题）

> 📖 来源引证

---

## 2. 全景位置

（ASCII 树状图，用 `├──` `└──` 风格，**在父级行末尾标注 `← 你在这里`**）

    大领域
    ├── 分类 A
    │   ├── 子类 X
    │   └── 子类 Y
    ├── 分类 B ← 你在这里
    │   ├── 【{Topic}】 ({核心特点})
    │   ├── 相关算法 A (说明)
    │   └── 相关算法 B (说明)
    └── 分类 C
        └── 其他

> ✅ 格式要求：
> - `← 你在这里` 标注在**当前所属分类的行末**（父节点），不是主题本身
> - 当前主题用 `【{Topic}】` 加粗标注，后跟括号说明其核心特点
> - 每个兄弟项也标注括号说明，便于横向对比

> 📚 来源引证

---

## 3. 依赖地图

（ASCII box-drawing 图：前置知识 → 本主题 → 后续方向）

    前置知识                 本主题                   后续方向
    ┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────┐
    │ 前置概念 A       │────→│                  │────→│ 后续方向 1            │
    │ 前置概念 B       │────→│   {Topic}        │────→│ 后续方向 2            │
    │ 前置概念 C       │────→│                  │────→│ 后续方向 3            │
    └─────────────────┘     └──────────────────┘     └──────────────────────┘

> 📚 来源引证

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [{topic}_map.md]({topic}_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [{topic}_concepts.md]({topic}_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [{topic}_math.md]({topic}_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [{topic}_tutorial.md]({topic}_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [{topic}_code.md]({topic}_code.md) | ⑤ 代码 | 快速上手实现 |
| [{topic}_pitfalls.md]({topic}_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [{topic}_history.md]({topic}_history.md) | ⑦ 历史 | 了解技术演进 |
| [{topic}_bridge.md]({topic}_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [{topic}_first_principles.md]({topic}_first_principles.md) | ⑨ 第一性原理 | 追问底层公理、理解边界 |

（不存在的维度用 ~~删除线~~ + "不适用" 标注）

> 📖 来源引证

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [{topic}_map.md]({topic}_map.md) 了解全局位置
2. 读 [{topic}_tutorial.md]({topic}_tutorial.md) Section 1 理解动机
3. 读 [{topic}_concepts.md]({topic}_concepts.md) 掌握核心术语
4. 读 [{topic}_math.md]({topic}_math.md) 手算一次核心公式
5. 跟 [{topic}_code.md]({topic}_code.md) 快速开始跑一个示例
6. 读 [{topic}_history.md]({topic}_history.md) 了解技术演进
7. 读 [{topic}_first_principles.md]({topic}_first_principles.md) 追问底层公理

### 日常参考 🔧

1. 查 [{topic}_code.md]({topic}_code.md) API 速查表
2. 查 [{topic}_math.md]({topic}_math.md) 公式速查
3. 查 [{topic}_pitfalls.md]({topic}_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [{topic}_history.md]({topic}_history.md) 完整演进线
2. 读 [{topic}_first_principles.md]({topic}_first_principles.md) 追问底层公理
3. 读 [{topic}_bridge.md]({topic}_bridge.md) 探索下游任务
4. 阅读原始论文

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 / ⬜ 待生成 |
| Concepts | ✅ 已完成 / ⬜ 待生成 |
| Math | ✅ 已完成 / ⬜ 待生成 / ~~不适用~~ |
| Tutorial | ✅ 已完成 / ⬜ 待生成 |
| Code | ✅ 已完成 / ⬜ 待生成 |
| Pitfalls | ✅ 已完成 / ⬜ 待生成 |
| History | ✅ 已完成 / ⬜ 待生成 |
| Bridge | ✅ 已完成 / ⬜ 待生成 |
| First Principles | ✅ 已完成 / ⬜ 待生成 / ~~不适用~~ |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | YYYY-MM-DD | 12m | ✅ current |
| Concepts | YYYY-MM-DD | 12m | ✅ current |
| Math | YYYY-MM-DD | 12m | ✅ current |
| Tutorial | YYYY-MM-DD | 12m | ✅ current |
| Code | YYYY-MM-DD | 6m | ✅ current |
| Pitfalls | YYYY-MM-DD | 6m | ✅ current |
| History | YYYY-MM-DD | never | ✅ current |
| Bridge | YYYY-MM-DD | 12m | ✅ current |
| First Principles | YYYY-MM-DD | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [《书名》Ch.X](../../../textbooks/书名.pdf) | 📚 教科书 | 全文核心参考 |
| [作者 年份](URL) | 📖 论文 | Section X（说明） |
| [名称](URL) | 📖 文档 | Section X（说明） |
| [仓库名](URL) | 💻 源码 | 代码实现参考 |
```

## 格式规则

- ✅ 每个 `##` 章节结尾都有 `> 📖/📚` 引证块
- ✅ 文件地图用 ① ② ③ 编号标注定位
- ✅ 学习路线每步链接一个具体文件
- ✅ 缺口检查标注 ✅/⬜/~~删除线~~
- ✅ 新鲜度状态标注 expiry 和 status
- ✅ 参考来源表汇总所有维度引用的全部来源

## 完成检查

- [ ] `{topic}_map.md` 存在且 8 章结构完整
- [ ] 核心问题 3-5 个
- [ ] 全景位置有 `← 你在这里` 标注
- [ ] 依赖地图有三栏

## 教科书来源

- Wiggins & McTighe《Understanding by Design》2nd Ed. (2005), Ch.5 "Essential Questions"
- Ausubel《Educational Psychology: A Cognitive View》(1968), Ch.14 "Advance Organizers"
- Gagné《The Conditions of Learning》4th Ed. (1985), Ch.3 "Learning Hierarchies"
- Norman《The Design of Everyday Things》Revised Ed. (2013), Ch.3 "Knowledge in the World"
  - MinerU: `data/mineru_output/norman_design_everyday_things/norman_design_everyday_things/auto/norman_design_everyday_things.md`
- Bloom《Taxonomy of Educational Objectives》(1956)
- Gawande《The Checklist Manifesto》(2009), Ch.2
- Hunt & Thomas《The Pragmatic Programmer》(1999), Tip 27
  - MinerU: `data/mineru_output/hunt_pragmatic_programmer/hunt_pragmatic_programmer/auto/hunt_pragmatic_programmer.md`

