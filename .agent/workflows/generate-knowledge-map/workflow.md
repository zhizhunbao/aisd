---
description: 9 维知识地图生成工作流 - 为任意主题构建完整知识库文档体系
# --- 以下字段供 Agent 上下文参考，不是系统配置 ---
# name: generate-knowledge-map
# version: 2.0.0
# trigger: /generate-knowledge-map
# state_file: 'knowledge-map/courses/{course}/{topic}/.km-state.yaml'
---

# Knowledge Map Generation Workflow

一个命令，为任意主题生成完整的 9 维知识库文档体系。自动跳过已完成的阶段。

## 使用方法

```bash
/generate-knowledge-map <课程> <主题>                      # 启动/继续
/generate-knowledge-map <课程> <主题> --only=map,pitfalls   # 选择性生成
/generate-knowledge-map <课程> <主题> --from=phase3         # 中断恢复
/generate-knowledge-map <课程> <主题> --video               # 含视频创作
/generate-knowledge-map status                              # 查看进度
/generate-knowledge-map reset                               # 重置
```

### 路径解析规则

| 输入 | 输出目录 |
|------|---------|
| `deep-learning conv_layer` | `knowledge-map/courses/deep-learning/conv_layer/` |
| `tools/ai-tools hugging_face` | `knowledge-map/tools/ai-tools/hugging_face/` |

## 设计理论基础

> **本工作流的 9 维结构和每个维度的模板格式都有教科书来源**，不是凭空设计。

### 全局理论框架

| 教科书 | 核心理论 | 如何指导本工作流 |
|--------|---------|-----------------|
| Bloom《Taxonomy of Educational Objectives》(1956) | 认知六层次：记忆→理解→应用→分析→评估→创造 | 9 维度按 Bloom 层次递进编排：Concepts(记忆) → Tutorial(理解) → Code(应用) → Pitfalls(分析) → First Principles(评估) |
| Ausubel《Educational Psychology: A Cognitive View》(1968) | 先行组织者(Advance Organizer)：新知识必须锚定在已有认知结构上 | DIM-1 Map 和 DIM-8 Bridge 的设计——先给全景定位，再建前后链接 |
| Wiggins & McTighe《Understanding by Design》(2005) | 逆向设计：从"核心问题"出发倒推学习路径 | DIM-1 Map 第一章"核心问题"放在最前面 |
| Mayer《Multimedia Learning》3rd Ed. (2020) | 12 条多媒体学习原则 | DIM-4 Tutorial 的 Why-First 结构 + Phase 7 视频创作 |
| Clark & Mayer《e-Learning and the Science of Instruction》3rd Ed. (2011) | 分段原则、预训练原则、worked examples | DIM-6 Pitfalls 的 ❌/✅ 对比格式 + DIM-3 Math 的逐步推导 |
| Pólya《How to Solve It》(1945) | 理解→规划→执行→回顾 四步解题法 | DIM-3 Math "直觉先于公式"的设计 |
| McKee《Story》(1997) | 叙事结构：序幕→冲突→转折→高潮→结局 | DIM-7 History 故事线叙事格式 |
| Heath《Made to Stick》(2007) | SUCCESs 粘性框架: Simple, Unexpected, Concrete, Credible, Emotional, Story | DIM-7 History 的 🔑转折点 + Phase 7 视频的 Hook 设计 |
| Gawande《The Checklist Manifesto》(2009) | 清单化降低复杂任务出错率 | DIM-6 Pitfalls 的调试清单 + DIM-1 Map 的缺口检查 |

### 教科书 Markdown 路径（MinerU 已转换）

| Key | Markdown 路径 |
|-----|---------------|
| `mayer_multimedia_learning` | `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md` |
| `clark_mayer_elearning` | `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md` |
| `mckee_story` | `data/mineru_output/mckee_story/mckee_story/auto/mckee_story.md` |
| `heath_made_to_stick` | `data/mineru_output/heath_made_to_stick/heath_made_to_stick/hybrid_auto/heath_made_to_stick.md` |
| `norman_design_everyday_things` | `data/mineru_output/norman_design_everyday_things/norman_design_everyday_things/auto/norman_design_everyday_things.md` |

## 工作流阶段

| 阶段 | 名称 | 维度 | 产出物 | 教科书依据 |
|------|------|------|--------|-----------|
| 0 | Pre-Flight | — | 模板确认 | — |
| 1 | 输入探测 | — | 素材报告 | — |
| 2 | Map 骨架 | DIM-1 | `{topic}_map.md` | Wiggins, Ausubel |
| 3 | 概念定义 | DIM-2 | `{topic}_concepts.md` | Bloom (记忆层), Bruner |
| 4 | 数学基础 | DIM-3 | `{topic}_math.md` | Pólya, Knuth |
| 5 | 教程 | DIM-4 | `{topic}_tutorial.md` | Mayer, Keller ARCS |
| 6 | 代码参考 | DIM-5 | `{topic}_code.md` | Carroll, Bloom (应用层) |
| 7 | 踩坑记录 | DIM-6 | `{topic}_pitfalls.md` | Clark & Mayer, Gawande |
| 8 | 历史演进 | DIM-7 | `{topic}_history.md` | McKee, Heath |
| 9 | 跨主题衔接 | DIM-8 | `{topic}_bridge.md` | Ausubel, Kuhn |
| 10 | 第一性原理 | DIM-9 | `{topic}_first_principles.md` | Euclid, Lakatos |
| 11 | 收尾 | — | Map 回填 + README | — |
| 12 | 视频创作 | — | `script.json` + `narration/` | Mayer, McKee, Heath |

## 来源白名单（最高优先级）

| ✅ 允许 | ❌ 严禁 |
|--------|---------|
| 📖 原始论文 / 预印本 | 教师 PPT / 课件 |
| 📚 出版教科书 (`textbooks/`) | 百度百科 / CSDN / 知乎 |
| 📖 官方文档 | 自己生成的内容 |
| 💻 开源代码 (`.github/`) | — |

## 两条铁律

1. **先定义后使用** — 每个名词必须先白话解释再给专业名称
2. **来源标注** — 每个声明必须标注引自哪个教科书/论文/文档的哪个章节

## 跳过规则

| 维度 | 跳过条件 | **永远不能跳过** |
|------|---------|----------------|
| Math | 无数学内容 | Map |
| History | 太新/无脉络 | Concepts |
| Bridge | 完全孤立 | Tutorial |
| First Principles | 纯工程工具 | Code, Pitfalls |

## 与 generate-study-material 的区别

| | study-material | knowledge-map |
|---|---|---|
| **目的** | 学课程、备考 | 建个人知识库、指导开发 |
| **输入** | 必须有老师 Slides | 任意: 主题名、文档、代码 |
| **输出** | 15+ 文件 | 9 个维度文件 |
| **维护** | 学期结束归档 | 长期维护 |

## 输出结构

```
knowledge-map/courses/<课程>/<主题>/
├── <主题>_map.md               ← ① 导航（DIM-1）
├── <主题>_concepts.md          ← ② 概念（DIM-2）
├── <主题>_math.md              ← ③ 公式（DIM-3，可跳过）
├── <主题>_tutorial.md          ← ④ 教程（DIM-4）
├── <主题>_code.md              ← ⑤ 代码（DIM-5）
├── <主题>_pitfalls.md          ← ⑥ 踩坑（DIM-6）
├── <主题>_history.md           ← ⑦ 历史（DIM-7，可跳过）
├── <主题>_bridge.md            ← ⑧ 衔接（DIM-8）
├── <主题>_first_principles.md  ← ⑨ 第一性原理（DIM-9，可跳过）
└── .km-state.yaml              ← 工作流状态文件
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
├── conv_layer_first_principles.md
└── .km-state.yaml
```

## 各阶段设计文档

| 文件 | 阶段 |
|------|------|
| [step-00-preflight.md](steps/step-00-preflight.md) | Pre-Flight 检查 |
| [step-01-probe.md](steps/step-01-probe.md) | 输入探测 |
| [step-02-map.md](steps/step-02-map.md) | DIM-1 Map 骨架 |
| [step-03-concepts.md](steps/step-03-concepts.md) | DIM-2 概念定义 |
| [step-04-math.md](steps/step-04-math.md) | DIM-3 数学基础 |
| [step-05-tutorial.md](steps/step-05-tutorial.md) | DIM-4 教程 |
| [step-06-code.md](steps/step-06-code.md) | DIM-5 代码参考 |
| [step-07-pitfalls.md](steps/step-07-pitfalls.md) | DIM-6 踩坑记录 |
| [step-08-history.md](steps/step-08-history.md) | DIM-7 历史演进 |
| [step-09-bridge.md](steps/step-09-bridge.md) | DIM-8 跨主题衔接 |
| [step-10-first-principles.md](steps/step-10-first-principles.md) | DIM-9 第一性原理 |
| [step-11-finalize.md](steps/step-11-finalize.md) | 收尾 |
| [step-12-video.md](steps/step-12-video.md) | 视频创作（可选） |
