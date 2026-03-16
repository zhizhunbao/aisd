---
description: generate 9-dim knowledge map + optional video content (Map / Concepts / Math / Tutorial / Code / Pitfalls / History / Bridge / First Principles + Video)
---

# 🧠 知识地图生成工作流 (Generate Knowledge Map)

为任意主题生成完整的 8 维知识库文档体系。适用于：研究主题、开发系统/模块、学习学科。

> ⚠️ **格式强制规则**: 每个维度文件必须 follow `knowledge-map-format` skill 的模板。

## 📁 目录结构

```
knowledge-map/
├── README.md                    ← 一人公司全角色技能树总览
├── courses/                     ← 按课程组织的知识地图
│   ├── deep-learning/           ← 研究生级 DL 课程
│   │   ├── README.md            ← 课程主题列表 + 进度
│   │   ├── _course.md           ← 课程名词总表
│   │   ├── conv_layer/          ← 主题文件夹
│   │   │   ├── conv_layer_map.md
│   │   │   ├── conv_layer_concepts.md
│   │   │   ├── conv_layer_math.md
│   │   │   ├── conv_layer_tutorial.md
│   │   │   ├── conv_layer_code.md
│   │   │   ├── conv_layer_pitfalls.md
│   │   │   ├── conv_layer_history.md
│   │   │   ├── conv_layer_bridge.md
│   │   │   └── conv_layer_first_principles.md
│   │   ├── dense_layer/
│   │   ├── transformer/
│   │   └── ...
│   ├── advanced-deep-learning/  ← 博士 PhD 级
│   ├── computer-vision/         ← 研究生级 CV 课程
│   ├── nlp/                     ← 研究生级 NLP 课程
│   ├── reinforcement-learning/  ← 研究生级 RL 课程
│   ├── machine-learning/
│   ├── machine-vision/          ← 本科/工业级
│   ├── linear-algebra/
│   ├── calculus/
│   ├── probability/
│   ├── statistics/
│   └── optimization/
├── tools/                       ← 工具知识地图
│   └── ai-tools/
│       ├── hugging_face/
│       ├── claude_code_skill/
│       └── antigravity_workflow/
├── projects/                    ← 项目知识地图
│   └── retrieval-lab/
├── roles/                       ← 21 个角色技能树
│   ├── ml-engineer/
│   ├── data-scientist/
│   └── ...
└── registry/
    └── progress.md
```

## 🎯 使用方式

```
/generate-knowledge-map <课程> <主题>

示例：
/generate-knowledge-map deep-learning conv_layer
/generate-knowledge-map nlp word_vectors
/generate-knowledge-map computer-vision epipolar_geometry
/generate-knowledge-map advanced-deep-learning energy_based_models

# 工具类（无课程归属）：
/generate-knowledge-map tools/ai-tools hugging_face

# 选择性生成 / 中断恢复：
/generate-knowledge-map deep-learning transformer --only=map,pitfalls
/generate-knowledge-map nlp llm --from=phase3
```

### 路径解析规则

| 输入 | 输出目录 |
|------|---------|
| `deep-learning conv_layer` | `knowledge-map/courses/deep-learning/conv_layer/` |
| `nlp word_vectors` | `knowledge-map/courses/nlp/word_vectors/` |
| `tools/ai-tools hugging_face` | `knowledge-map/tools/ai-tools/hugging_face/` |
| `projects/retrieval-lab bm25` | `knowledge-map/projects/retrieval-lab/bm25/` |

**默认路径**: 如果只提供 `<课程> <主题>`，自动映射到 `knowledge-map/courses/<课程>/<主题>/`

## 📋 9 维结构与生成顺序

```
Phase 0   输入探测 + 主题拆分
Phase 1   Map 骨架（核心问题 + 依赖关系）
Phase 2   理解层: ② Concepts → ③ Math → ④ Tutorial
Phase 3   实战层: ⑤ Code → ⑥ Pitfalls
Phase 4   脉络层: ⑦ History → ⑧ Bridge → ⑨ First Principles
Phase 5   收尾: 回填 Map + 更新课程 README + 缺口检查 + 新鲜度
Phase 6   视频创作（可选 --video）: History → 家长版脚本 → Veo 视频 → 发布
```

### 与 generate-study-material 的区别

| | study-material | knowledge-map |
|---|---|---|
| 目的 | 学课程、备考 | 建个人知识库、指导开发 |
| 输入 | 必须有老师 Slides | 任意: 主题名、文档、代码 |
| 输出 | 15+ 文件 | 9 个文件 |
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

// 步骤 C：确认目标课程存在（不可省略）
list_dir(knowledge-map/courses/<课程>/)
// 或 list_dir(knowledge-map/tools/<领域>/) 或 list_dir(knowledge-map/projects/<项目>/)
```

### Pre-Flight 通过条件（必须在开始写文件之前确认）

- [ ] 已 `view_file` 读取 `dimension_templates.md` 全文
- [ ] 已确认目标课程/工具目录存在，且有 `_course.md` 和 `README.md`
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

1. **验证目标路径**:
   - 课程类: `knowledge-map/courses/<课程>/` 必须存在 `_course.md` + `README.md`
   - 工具类: `knowledge-map/tools/<领域>/` 必须存在
   - 项目类: `knowledge-map/projects/<项目>/` 必须存在
   - 主题文件夹如不存在则自动创建

2. **扫描可用素材**:
   - `textbooks/` 教科书 PDF + `data/mineru_output/` MinerU 解析
   - `.github/` 开源项目参考代码
   - `official-docs/` 工具链官方文档
   - `knowledge-map/courses/<课程>/` 同课程已有主题（用于 Bridge）
   - `knowledge-map/courses/<课程>/_course.md` 课程名词总表（术语参照）
   - `search_web` 搜索在线文档（优先下载到 `.documents/`）

3. **主题粒度判断** — 满足任一则拆分:
   - 核心概念 > 15 个
   - 跨越多层次（理论+工具+实践）
   - Tutorial 预估 > 3000 字

4. **来源充分性检查**:

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

5. **论文下载失败处理（不阻塞流程）**:

   > ⚠️ **下载脚本无 open access 结果、网络超时、脚本卡在交互模式时，立即按以下步骤处理：**

   1. **终止脚本**，立即继续生成维度文件
   2. **在 source_versions 中标注占位符**：
      ```
      "📖 Paper: 作者, '标题', 刊物 年份 — ⚠️ 待下载 见 papers_index.md"
      ```
   3. **创建/追加 `papers_index.md`**（在主题文件夹下），记录：
      - 完整论文信息（标题/作者/年份/刊物）
      - 重要性评级（⭐1-5）
      - 手动搜索链接（IEEE Xplore / ACM DL / arXiv）
   4. 生成完成后提示用户手动下载，**不等待**

6. **向用户确认**: 展示素材报告和生成计划

---

## Phase 1: Map 骨架 🗺️

**Skill**: `knowledge-map-format` (DIM-1)

> ✅ 前提：Pre-Flight 已通过，dimension_templates.md 已读取

1. 对照 DIM-1 模板（**固定 8 章**）逐章生成：
   - `## 1. 核心问题`（3-5 个问题，每行末尾 → 答案）
   - `## 2. 全景位置`（ASCII 树，标注 `【你在这里】`，根节点为课程名）
   - `## 3. 依赖地图`（ASCII box-drawing 三栏图）
   - `## 4. 文件地图`（表格，文件名用 Markdown 相对链接）
   - `## 5. 学习/使用路线`（三小节：初学/日常/深度）
   - `## 6. 缺口检查`（✅/⬜/~~删除线~~）
   - `## 7. 新鲜度状态`（含 expiry + status）
   - `## 8. 参考来源表`（汇总所有 9 维度引用）
2. 每章结尾有 `> 📖/📚` 引证块

**输出**: `knowledge-map/courses/<课程>/<主题>/<主题>_map.md`

---

## Phase 2: 理解层 📖

### 2.1 Concepts

**Skill**: `knowledge-map-format` (DIM-2)

1. Follow skill 的 Concepts 模板
2. 每个术语: 一句话白话定义 + 英文标注
3. 至少一组辨析对比表
4. **参照** `_course.md` 名词总表确保术语一致

**输出**: `<主题>_concepts.md`

### 2.2 Math

**Skill**: `knowledge-map-format` (DIM-3)

1. Follow skill 的 Math 模板
2. 每个公式: 符号表 → 公式 → 直觉解释 → 推导
3. 跳过条件: 主题无数学内容

**输出**: `<主题>_math.md`

### 2.3 Tutorial

**Skill**: `knowledge-map-format` (DIM-4)

1. Follow skill 的 Tutorial 模板
2. **Why-First**: Section 1 先讲动机，Section 2 再讲底层原理
3. 衔接性规则: follow `learning-source-citation` skill
4. 三层止挖: 会用 → 知道为什么 → 看过底层原理（到此为止）

**输出**: `<主题>_tutorial.md`

---

## Phase 3: 实战层 🔧

### 3.1 Code

**Skills**: `knowledge-map-format` (DIM-5), `learning-code-generation`, `dev-code-comment`

1. Follow skill 的 Code 模板
2. 快速开始 → 完整实现 → API 速查
3. 代码必须可直接运行，双语注释

**输出**: `<主题>_code.md`

### 3.2 Pitfalls ⚠️

**Skill**: `knowledge-map-format` (DIM-6)

1. Follow skill 的 Pitfalls 模板
2. 每个坑: 场景 → 症状 → 根因 → ❌/✅ 代码对比 → 教训
3. 末尾加调试清单
4. **活文档**: 每次踩坑后追加

**输出**: `<主题>_pitfalls.md`

---

## Phase 4: 脉络层 🔗

### 4.1 History

**Skill**: `knowledge-map-format` (DIM-7)

1. Follow skill 的 History 模板
2. Station 叙事: 前身 → 创新 → 局限 → 引出下一站
3. 跳过条件: 主题太新/无历史脉络

**输出**: `<主题>_history.md`

### 4.2 Bridge

**Skill**: `knowledge-map-format` (DIM-8)

1. Follow skill 的 Bridge 模板
2. 前后导航 + 上下游依赖 + 概念演变追踪
3. **同课程内链接**: 用相对路径链接同课程下已有主题
   - 示例: `[conv_layer](../conv_layer/conv_layer_map.md)`
4. **跨课程链接**: 用相对路径链接相关课程主题
   - 示例: `[CNN](../../deep-learning/cnn/cnn_map.md)`
5. 扩展阅读分三层: 纵深 → 同层 → 全景
6. 双向更新: 如相关主题已存在，更新其 Bridge

**输出**: `<主题>_bridge.md`

### 4.3 First Principles

**Skill**: `knowledge-map-format` (DIM-9)

1. Follow skill 的 First Principles 模板（固定 5 章）
2. 核心问题链: 5 个为什么式递归追问，从表层功能到不可再分公理
3. 每个公理必须有: **陈述 + 白话 + 来源 + 可验证性**（四要素缺一不可）
4. 推导链每步标注"用了哪个公理"，末尾附全景图（ASCII box-drawing）
5. "如果公理不成立"用表格逐一分析边界和替代方案
6. 跳过条件: 主题是纯工程工具（如 Git、Docker），无数学/理论公理

**输出**: `<主题>_first_principles.md`

---

## Phase 5: 收尾 ✅

1. **回填 Map**: 文件地图 + 缺口检查 + 新鲜度状态
2. **更新 Bridge**: 双向更新相关主题
3. **更新课程 README**: `knowledge-map/courses/<课程>/README.md`
   - 在主题列表中更新该主题的状态从 `🔲 planned` 到 `✅ current`
   - 更新文件数和描述
4. **质量检查**:
   - [ ] 每个声明有来源？
   - [ ] Tutorial Why-First？
   - [ ] Code 30 秒可跑？
   - [ ] Pitfalls 有 ❌/✅ 对比？
   - [ ] 交叉引用链接有效？（同课程用 `../`，跨课程用 `../../`）

---

## Phase 6: 视频创作 🎬（可选）

**Skill**: `ai-video-director`

> **触发条件**: 用户传入 `--video` 参数，或主题的 History 文件具有强故事性。
> **前置要求**: Phase 4 的 History 文件已生成 + 已 `view_file` 读取 `ai-video-director/SKILL.md`。
> **核心原则**: **History 文件 = 视频的 Single Source of Truth**，不重写内容，只做风格适配。

### 6.1 旁白稿生成（基于 History 风格化润色）

> ⚠️ **不允许重写内容**。History 文件的故事线、人物、年份、转折点全部保留。

1. **读取 History 文件**: `<主题>_history.md`
2. **风格化润色**（Claude 直接完成，做四件事）:
   - **口语化**: 去掉 markdown 语法、LaTeX 公式、引用标记、链接
   - **降门槛**: 专业术语换成生活类比（如 "O(n)" → "一个一个找"），保留人物和年份但简化理论细节
   - **加风格**: 按 `--style` 参数（袁腾飞/老高/罗翔/精简）润色语气
   - **调节奏**: 标注停顿位置，每段一行，确保每段 ≤ 30 秒
   - **加视觉提示**: 每行末尾加 `| [视觉提示]`，简述对应动画内容
3. **输出**: `narration/script.txt`（每行格式: `旁白文本 | [视觉提示]`）

### 6.2 TTS + Remotion + 组装

> 工具链：Qwen3-TTS 配音 → Remotion 动画 → FFmpeg 组装
> 设计准则：Mayer 多媒体学习原则 + CRAP 布局原则（详见 `ai-video-director` skill）

1. **Qwen3-TTS 生成旁白音频**: `generate_narration_qwen.py`
2. **Remotion 制作动画**: 板书式 React 组件，每段旁白 = 一个 `<Series.Sequence>`
3. **素材补充**: Wikipedia 人物肖像 + 论文封面截图（增加故事感和专业感）
4. **FFmpeg 组装**: `assemble_video_v6.py` 自动对齐 + 字幕烧录

### 6.3 反馈回填

1. 在 `_map.md` 的文件地图中标注 `🎬 已生成视频`
2. 在课程 `README.md` 中标注主题已有视频内容

### 6.4 跳过条件

| 条件 | 说明 |
|------|------|
| 无 `--video` 参数 | 默认不生成 |
| History 无故事性 | 纯数学概念、纯工程配置 |
| 主题太窄 | 无法撑起 3 分钟视频 |

### 6.5 单视频生产时间预估

| 环节 | 耗时 |
|------|------|
| 读 History + 风格化润色 | 10 min |
| TTS 生成音频 | 5 min |
| Manim 动画制作 | 30-60 min |
| FFmpeg 组装 + 字幕 | 10 min |
| **合计** | **约 1-1.5 小时/个** |

---

## 元数据标准

每个文件顶部必须有:

```yaml
---
topic: conv_layer
course: deep-learning
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
knowledge-map/courses/<课程>/<主题>/
├── <主题>_map.md               ← ① 导航
├── <主题>_concepts.md          ← ② 概念
├── <主题>_math.md              ← ③ 公式
├── <主题>_tutorial.md          ← ④ 教程
├── <主题>_code.md              ← ⑤ 代码
├── <主题>_pitfalls.md          ← ⑥ 踩坑
├── <主题>_history.md           ← ⑦ 历史
├── <主题>_bridge.md            ← ⑧ 衔接
├── <主题>_first_principles.md  ← ⑨ 第一性原理
├── <主题>_video_script.md      ← ⑩ 视频脚本（Phase 6·可选）
└── <主题>_video_article.md     ← ⑪ 家长版文章（Phase 6·可选）
```

### 实际示例

```
knowledge-map/courses/deep-learning/conv_layer/
├── conv_layer_map.md
├── conv_layer_concepts.md
├── conv_layer_math.md
├── conv_layer_tutorial.md
├── conv_layer_code.md
├── conv_layer_pitfalls.md
├── conv_layer_history.md
├── conv_layer_bridge.md
└── conv_layer_first_principles.md
```

---

## 课程级文件说明

每个课程目录下有两个课程级文件（不属于任何主题）：

| 文件 | 作用 | 何时更新 |
|------|------|---------|
| `_course.md` | 课程名词总表（分类 + 中英对照） | 课程创建时 |
| `README.md` | 主题列表 + 进度追踪 + 课程定位 | 每次主题完成时 (Phase 5) |
