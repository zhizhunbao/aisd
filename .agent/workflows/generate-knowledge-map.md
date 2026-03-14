---
description: 为任意主题生成 8 维知识库文档（Map / Concepts / Math / Tutorial / Code / Pitfalls / History / Bridge）
---

# 🧠 知识地图生成工作流 (Generate Knowledge Map)

为任意主题生成完整的 8 维知识库文档体系。适用于：研究主题、开发系统/模块、学习学科。

> ⚠️ **格式强制规则**: 每个维度文件必须 follow `knowledge-map-format` skill 的模板。

## 🎯 使用方式

```
/generate-knowledge-map <领域> <主题>

示例：
/generate-knowledge-map retrieval bm25
/generate-knowledge-map nlp tokenization
/generate-knowledge-map retrieval bm25 --only=map,pitfalls
/generate-knowledge-map retrieval bm25 --from=phase3
```

## 📋 9 维结构与生成顺序

```
Phase 0   输入探测 + 主题拆分
Phase 1   Map 骨架（核心问题 + 依赖关系）
Phase 2   理解层: ② Concepts → ③ Math → ④ Tutorial
Phase 3   实战层: ⑤ Code → ⑥ Pitfalls
Phase 4   脉络层: ⑦ History → ⑧ Bridge → ⑨ First Principles
Phase 5   收尾: 回填 Map + 缺口检查 + 新鲜度
```

### 与 generate-study-material 的区别

| | study-material | knowledge-map |
|---|---|---|
| 目的 | 学课程、备考 | 建个人知识库、指导开发 |
| 输入 | 必须有老师 Slides | 任意: 主题名、文档、代码 |
| 输出 | 15+ 文件 | 8 个文件 |
| 维护 | 学期结束归档 | 长期维护 |

---

## ⚖️ 执行协议

1. **Skill 优先**: 每个维度开始前**必须** follow `knowledge-map-format` skill
2. **来源引证**: follow `learning-source-citation` skill — 每个声明必须标注来源
3. **串行执行**: 按 Phase 顺序
4. **中断恢复**: `--from=<phase>` 继续

---

## 🚦 Pre-Flight 检查（每次启动工作流的第一步，不可跳过）

> ⛔ **无论是新会话还是中断恢复，都必须先执行以下步骤，否则不允许写任何文件。**

### 必须执行的 view_file 调用

```
// 步骤 A：读取完整维度模板（不可省略）
view_file(.agent/skills/knowledge-map-format/references/dimension_templates.md)

// 步骤 B：读取 SKILL.md 来源规则
view_file(.agent/skills/knowledge-map-format/SKILL.md)
```

### Pre-Flight 通过条件（必须在开始写文件之前确认）

- [ ] 已 `view_file` 读取 `dimension_templates.md` 全文
- [ ] 已确认 DIM-1 Map: 固定 **8 章**，章节编号格式 `## 1. 核心问题`
- [ ] 已确认 DIM-2 Concepts: 固定 **4 章**（含 **核心属性** = 信息架构 + 适用/不适用场景）
- [ ] 已确认 DIM-3 Math: 固定 **5 章**（含符号对照表 + 手算练习）
- [ ] 已确认 DIM-4 Tutorial: 固定 **6 Section + 参考来源表**
- [ ] 已确认 DIM-5 Code: 固定 **4 章**（含中英双语注释 + `# ====` 分隔符）
- [ ] 已确认 DIM-6 Pitfalls: **加粗关键词** + ❌/✅ 缩进代码 + 调试清单
- [ ] 已确认 DIM-7 History: **故事线叙事**（🎬序幕 + 📚第N章 + 🔑转折 + 🗺️全局回顾）
- [ ] 已确认 DIM-8 Bridge: 固定 **6 章**（含 ← 前置/→ 后续 + 概念演变追踪）
- [ ] 已确认 DIM-9 First Principles: 固定 **5 章**（核心问题链 + 公理 + 推导链 + 如果公理不成立 + 速查表）
- [ ] 已确认 `source_versions` Frontmatter 用**裸 URL**（不是 Markdown 链接）

### 中断恢复专项规则

> 若会话被截断（Checkpoint 重启），摘要信息**不可信任**，必须重新读取模板。
> 直接跳过 Pre-Flight 是上一次出错的根本原因。

---

## 🚨 来源白名单（最高优先级规则）

> **所有生成内容的来源严格限定为以下四类**，缺少时标注 `⚠️ 来源不足` 并等待用户选择，**绝不**用老师课件代替。

| ✅ 允许 | 示例 |
|--------|------|
| 📖 **原始论文 / 预印本** | Ester et al. KDD 1996, arXiv, ACL Anthology |
| 📚 **出版教科书** | `textbooks/` 目录下 — ESL, PRML, PML, ISLR, CLRS… |
| 📖 **官方文档** | scikit-learn docs, PyTorch docs, RFC, W3C… |
| 💻 **开源代码仓库** | `.github/` 目录下 — GitHub: sklearn, numpy, huggingface… |

| ❌ 严禁 | 后果 |
|---------|------|
| 教师 PPT / 课件 / 授课讲义 | 直接拒绝引用，标 `⚠️ 来源不足` |
| 课程作业题 / 考试题 | 同上 |
| 百度百科 / CSDN / 知乎博客等非权威内容 | 不引用 |
| 自己生成的内容 | 循环引证，无意义 |



## Phase 0: 输入探测 🔍

1. **扫描可用素材**:
   - `textbooks/` 教科书 PDF + `data/mineru_output/` MinerU 解析
   - `.github/` 开源项目参考代码
   - `.documents/` 本地官方文档
   - `knowledge-map/` 已有相关主题
   - `search_web` 搜索在线文档（优先下载到 `.documents/`）

2. **主题粒度判断** — 满足任一则拆分:
   - 核心概念 > 15 个
   - 跨越多层次（理论+工具+实践）
   - Tutorial 预估 > 3000 字

3. **来源充分性检查**:

   | 维度 | 最低来源要求 |
   |------|-------------|
   | Concepts | 1 个权威来源 |
   | Math | 必须有教科书/论文 |
   | Tutorial | 1 官方文档 + 1 教科书 |
   | Code | 1 个参考实现 |
   | Pitfalls | 1 个来源 (Issues/SO/经验) |

   来源不足时**优先用以下顺序补齐，不暂停等待**:
   - [首选] 尝试 `download_papers.py` 自动下载论文
   - [次选] 用 `search_web` 查找官方文档/arXiv 链接补齐
   - [兜底] 有教科书时直接用教科书章节作为来源

4. **论文下载失败处理（不阻塞流程）**:

   > ⚠️ **下载脚本无 open access 结果、网络超时、脚本卡在交互模式时，立即按以下步骤处理：**

   1. **终止脚本**，立即继续生成维度文件
   2. **在 source_versions 中标注占位符**：
      ```
      "📖 Paper: 作者, '标题', 刊物 年份 — ⚠️ 待下载 见 papers_index.md"
      ```
   3. **创建/追加 `papers_index.md`**（在知识地图目录下），记录：
      - 完整论文信息（标题/作者/年份/刊物）
      - 重要性评级（⭐1-5）
      - 手动搜索链接（IEEE Xplore / ACM DL / arXiv）
   4. 生成完成后提示用户手动下载，**不等待**

5. **向用户确认**: 展示素材报告和生成计划

---

## Phase 1: Map 骨架 🗺️

**Skill**: `knowledge-map-format` (DIM-1)

> ✅ 前提：Pre-Flight 已通过，dimension_templates.md 已读取

1. 对照 DIM-1 模板（**固定 8 章**）逐章生成：
   - `## 1. 核心问题`（3-5 个问题，每行末尾 → 答案）
   - `## 2. 全景位置`（ASCII 树，标注 `【你在这里】`）
   - `## 3. 依赖地图`（ASCII box-drawing 三栏图）
   - `## 4. 文件地图`（表格，文件名用 Markdown 链接）
   - `## 5. 学习/使用路线`（三小节：初学/日常/深度）
   - `## 6. 缺口检查`（✅/⬜/~~删除线~~）
   - `## 7. 新鲜度状态`（含 expiry + status）
   - `## 8. 参考来源表`（汇总所有 8 维度引用）
2. 每章结尾有 `> 📖/📚` 引证块

**输出**: `{output_dir}/{topic}/{topic}_map.md`

---

## Phase 2: 理解层 📖

### 2.1 Concepts

**Skill**: `knowledge-map-format` (DIM-2)

1. Follow skill 的 Concepts 模板
2. 每个术语: 一句话白话定义 + 英文标注
3. 至少一组辨析对比表

**输出**: `{topic}_concepts.md`

### 2.2 Math

**Skill**: `knowledge-map-format` (DIM-3)

1. Follow skill 的 Math 模板
2. 每个公式: 符号表 → 公式 → 直觉解释 → 推导
3. 跳过条件: 主题无数学内容

**输出**: `{topic}_math.md`

### 2.3 Tutorial

**Skill**: `knowledge-map-format` (DIM-4)

1. Follow skill 的 Tutorial 模板
2. **Why-First**: Section 1 先讲动机，Section 2 再讲底层原理
3. 衔接性规则: follow `learning-source-citation` skill
4. 三层止挖: 会用 → 知道为什么 → 看过底层原理（到此为止）

**输出**: `{topic}_tutorial.md`

---

## Phase 3: 实战层 🔧

### 3.1 Code

**Skills**: `knowledge-map-format` (DIM-5), `learning-code-generation`, `dev-code-comment`

1. Follow skill 的 Code 模板
2. 快速开始 → 完整实现 → API 速查
3. 代码必须可直接运行，双语注释

**输出**: `{topic}_code.md`

### 3.2 Pitfalls ⚠️

**Skill**: `knowledge-map-format` (DIM-6)

1. Follow skill 的 Pitfalls 模板
2. 每个坑: 场景 → 症状 → 根因 → ❌/✅ 代码对比 → 教训
3. 末尾加调试清单
4. **活文档**: 每次踩坑后追加

**输出**: `{topic}_pitfalls.md`

---

## Phase 4: 脉络层 🔗

### 4.1 History

**Skill**: `knowledge-map-format` (DIM-7)

1. Follow skill 的 History 模板
2. Station 叙事: 前身 → 创新 → 局限 → 引出下一站
3. 跳过条件: 主题太新/无历史脉络

**输出**: `{topic}_history.md`

### 4.2 Bridge

**Skill**: `knowledge-map-format` (DIM-8)

1. Follow skill 的 Bridge 模板
2. 前后导航 + 上下游依赖 + 概念演变追踪
3. 扩展阅读分三层: 纵深 → 同层 → 全景
4. 双向更新: 如相关主题已存在，更新其 Bridge

**输出**: `{topic}_bridge.md`

### 4.3 First Principles

**Skill**: `knowledge-map-format` (DIM-9)

1. Follow skill 的 First Principles 模板（固定 5 章）
2. 核心问题链: 5 个为什么式递归追问，从表层功能到不可再分公理
3. 每个公理必须有: **陈述 + 白话 + 来源 + 可验证性**（四要素缺一不可）
4. 推导链每步标注"用了哪个公理"，末尾附全景图（ASCII box-drawing）
5. "如果公理不成立"用表格逐一分析边界和替代方案
6. 跳过条件: 主题是纯工程工具（如 Git、Docker），无数学/理论公理

**输出**: `{topic}_first_principles.md`

---

## Phase 5: 收尾 ✅

1. **回填 Map**: 文件地图 + 缺口检查 + 新鲜度状态
2. **更新 Bridge**: 双向更新相关主题
3. **更新 README**: `knowledge-map/{领域}/README.md`
4. **质量检查**:
   - [ ] 每个声明有来源？
   - [ ] Tutorial Why-First？
   - [ ] Code 30 秒可跑？
   - [ ] Pitfalls 有 ❌/✅ 对比？
   - [ ] 交叉引用链接有效？

---

## 元数据标准

每个文件顶部必须有:

```yaml
---
topic: bm25
dimension: tutorial
created: 2026-03-11
last_verified: 2026-03-11
source_versions:
  - "SQLite FTS5 docs (2025-12)"
  - "rank_bm25 v0.2.2"
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

---

## 跳过规则

| 维度 | 跳过条件 | Map 标注 |
|------|---------|---------|
| Math | 无数学内容 | ⬜ 不适用 |
| History | 太新/无脉络 | ⬜ 不适用 |
| Bridge | 完全孤立 | ⬜ 简化 |
| First Principles | 纯工程工具（无数学/理论公理） | ⬜ 不适用 |

**永远不能跳过**: Map, Concepts, Tutorial, Code, Pitfalls

---

## 输出结构

```
{output_dir}/{topic}/
├── {topic}_map.md               ← ① 导航
├── {topic}_concepts.md          ← ② 概念
├── {topic}_math.md              ← ③ 公式
├── {topic}_tutorial.md          ← ④ 教程
├── {topic}_code.md              ← ⑤ 代码
├── {topic}_pitfalls.md          ← ⑥ 踩坑
├── {topic}_history.md           ← ⑦ 历史
├── {topic}_bridge.md            ← ⑧ 衔接
└── {topic}_first_principles.md  ← ⑨ 第一性原理
```
