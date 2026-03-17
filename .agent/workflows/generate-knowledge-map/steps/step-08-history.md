# Phase 8: DIM-7 History（历史演进）

## 概述

| 项 | 值 |
|----|---|
| **角色** | Historian |
| **技能** | knowledge-map-format (DIM-7) |
| **前置条件** | Phase 7（Pitfalls）完成 |
| **输出** | `{topic}_history.md` |
| **预计时间** | 20-40 分钟 |
| **跳过条件** | 主题太新/无历史脉络 |

## 设计理论依据

| 格式设计 | 教科书依据 |
|---------|-----------|
| **故事线叙事**（🎬序幕 + 📚章节 + 🔑转折） | McKee《Story》(1997), Part 2 "The Elements of Story" — 故事=因果链，不是时间线。每章有冲突→解决→新冲突 |
| 每章三个固定小节 | McKee: 每个叙事单元有 "Inciting Incident"(发生了什么) → "Progressive Complication"(为什么重要) → "Crisis"(但还有问题) |
| `🔑 转折点` 引出下一章 | Heath《Made to Stick》Ch.2 "Unexpected" — 人记住的是**意料之外**的转折，不是平铺直叙的年表 |
| `> **关键人物** + **关键论文**` | Heath Ch.4 "Credible" — 有人物和来源的故事比抽象叙述可信度高 |
| `🗺️ 全局回顾` 路线图 | Bruner《The Process of Education》(1960), Ch.4 — "Spiral Curriculum": 学完细节后回到全局，加深结构性理解 |
| `expiry: never` | 历史已发生，不会过期 |

## 固定格式模板

````
---
topic: {topic}
dimension: history
created: {YYYY-MM-DD}
last_verified: {YYYY-MM-DD}
source_versions:
  - "📖 Paper: ..."
  - "📚 Book: ..."
expiry: never
status: current
---

# {Topic} 的故事线：从 {起点} 到 {终点}

> **核心主题：** 一句话概括技术演进核心线索
> **故事线：** 一个不断"打怪升级"的问题解决历程

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 用引用块写出核心问题

（交代背景）

> 🔑 **问题提出：** 引出第一章

---

## 📚 第一章：{章节标题}（年代）

> **关键人物：** 姓名
> **关键论文：** 引用

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| {人物}肖像 | Wikimedia Commons | `https://commons.wikimedia.org/wiki/File:XXX.jpg` | CC BY-SA / 公有领域 |
| {论文}封面 | arXiv / 出版商 | `https://...` | 学术引用 |

### 发生了什么？

（叙事语言讲故事）

### 为什么这很重要？

（解释影响）

### 但还有一个问题……

（局限性，引出下一章）

> 🔑 **故事转折点：** 一句话引出下一章

---

## 📚 第二章：{章节标题}（年代）

（同上格式）

---

## 🗺️ 全局回顾：技术演进路线图

（ASCII box-drawing 总结）

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|

### 🎥 视觉素材总表（视频制作用）

| 章节 | 人物 | 肖像来源 | 论文/事件图片 | 版权 |
|------|------|---------|-------------|------|
| 第一章 | {人物} | Wikimedia Commons: `File:XXX.jpg` | arXiv: `XXXX.XXXXX` | CC BY-SA |
| 第二章 | {人物} | ... | ... | ... |

> ⚠️ **素材查找优先级：**
> 1. **Wikimedia Commons** — 首选，多数科学家有公有领域肖像
> 2. **大学官网/档案馆** — 本校教授的官方照片
> 3. **Smithsonian Open Access** (`si.edu/openaccess`) — CC0 博物馆藏品
> 4. **Library of Congress** (`loc.gov/free-to-use`) — 美国历史公有领域
> 5. **Internet Archive** (`archive.org`) — 老书、老照片
> 6. **论文首页截图** — arXiv / Google Scholar
>
> ❌ **禁止：** AI 生成肖像、库存图片网站、无版权标注的图片
````

## 格式规则

- ✅ 用 `🎬 序幕` + `📚 第N章` 作为章节标题
- ✅ 每章有三个 `###`：发生了什么 / 为什么重要 / 但还有问题
- ✅ 每章结尾用 `🔑 **故事转折点**` 引出下一章
- ✅ 每章有关键人物 + 关键论文
- ✅ 每章有 `🎥 视觉素材` 表格（肖像 + 论文封面 + 版权）
- ✅ 叙事口吻讲故事，不是干巴巴列事实
- ✅ 末尾有 `🗺️ 全局回顾`，包含视觉素材总表
- ❌ 不用 Station 格式
- ❌ 不用 AI 生成肖像或无来源图片

## 完成检查

- [ ] 有 🎬 序幕 + 至少 2 个 📚 章节 + 🗺️ 全局回顾
- [ ] 每章有转折点
- [ ] 每章有 🎥 视觉素材表格（至少有肖像来源 + 版权标注）
- [ ] 全局回顾有升级表
- [ ] 全局回顾有视觉素材总表
- [ ] 所有素材链接可访问（Wikimedia Commons 链接格式正确）

## 教科书来源

- McKee《Story》(1997), Part 2 "The Elements of Story"
  - MinerU: `data/mineru_output/mckee_story/mckee_story/auto/mckee_story.md`
- Heath《Made to Stick》(2007), Ch.2 "Unexpected", Ch.4 "Credible"
  - MinerU: `data/mineru_output/heath_made_to_stick/heath_made_to_stick/hybrid_auto/heath_made_to_stick.md`
- Bruner《The Process of Education》(1960), Ch.4 "Spiral Curriculum"
