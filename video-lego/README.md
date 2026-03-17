# 🎬 Video Lego — 教育视频积木管理系统

> 基于 Mayer 多媒体学习理论 + Snyder 故事节拍体系，将视频制作流水线拆解为原子化、解耦的管理模块。
> 每个知识点 = 一集视频 = 一组可复用的积木搭建而成。

---

## 架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Video Lego 管理系统                              │
│                                                                     │
│  ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌─────────────────┐   │
│  │ 内容层   │──▶│ 表现层   │──▶│ 组装层    │──▶│ 质量层           │   │
│  │ Content  │   │ Present │   │ Assembly │   │ Quality         │   │
│  │ M1,M4,M8│   │M2,M3,M5 │   │ M9, M10  │   │ M7              │   │
│  │         │   │ M6      │   │          │   │                 │   │
│  └─────────┘   └─────────┘   └──────────┘   └─────────────────┘   │
│                                                                     │
│  教科书: Mayer | Clark&Mayer | Snyder | McKee | Knaflic | Williams  │
└─────────────────────────────────────────────────────────────────────┘
```

**4 大层 · 10 模块 · 37 子模块 · 7 素材分类 · 6 积木分类**

---

## 🗂️ 完整目录树

```
video-lego/
│
├── 📄 README.md                          ← 本文件
├── 📄 package.json                       ← Vite + React + TypeScript
├── 📄 vite.config.ts                     ← 路径别名 @/ @blocks/
├── 📄 tsconfig.json                      ← 项目 TypeScript 配置
├── 📄 index.html                         ← SPA 入口
│
└── src/
    │
    ├── 📄 main.tsx                        ← 应用启动入口
    ├── 📄 App.tsx                         ← 路由 + 侧边栏导航
    ├── 📄 theme.ts                        ← 管理系统 UI 主题
    ├── 📄 index.css                       ← 全局样式（暗色系）
    │
    │
    │ ═══════════════════════════════════════════════════════════
    │ 📐 lib/ — 类型定义 & 运行时工具（0 副作用，纯数据层）
    │ ═══════════════════════════════════════════════════════════
    │
    ├── lib/
    │   │
    │   │ ── 素材系统 ──
    │   ├── 📄 asset-types.ts              ← 素材分类 & 数据结构（7大类 × 子类 × 数据接口）
    │   │   │
    │   │   │ ┌─ 7 大素材分类 (ASSET_CATEGORIES) ──────────────────────────────┐
    │   │   │ │                                                                 │
    │   │   │ │  🎙️ narration  旁白文稿    ── hook | explain | transition       │
    │   │   │ │  │                            | summary | aside                  │
    │   │   │ │  │                            └─ NarrationAssetData              │
    │   │   │ │  │                                                               │
    │   │   │ │  🎨 visual     视觉画面    ── animation | diagram | chart        │
    │   │   │ │  │                            | screencast | illustration | photo│
    │   │   │ │  │                            └─ VisualAssetData                 │
    │   │   │ │  │                                                               │
    │   │   │ │  ✏️ text_overlay 文字叠层   ── title | bullet | formula          │
    │   │   │ │  │                            | code | caption | quote            │
    │   │   │ │  │                            └─ TextOverlayAssetData            │
    │   │   │ │  │                                                               │
    │   │   │ │  🔊 audio      音频音效    ── bgm | sfx | alert | ambient       │
    │   │   │ │  │                            └─ AudioAssetData                  │
    │   │   │ │  │                                                               │
    │   │   │ │  📊 data       数据素材    ── dataset | timeline | comparison    │
    │   │   │ │  │                            | code_sample | table               │
    │   │   │ │  │                            └─ DataAssetData                   │
    │   │   │ │  │                                                               │
    │   │   │ │  📖 reference  引用来源    ── textbook | paper | docs | wiki     │
    │   │   │ │  │                            └─ ReferenceAssetData              │
    │   │   │ │  │                                                               │
    │   │   │ │  🔄 transition 转场衔接    ── chapter_card | progress            │
    │   │   │ │                               | recap | bridge_anim              │
    │   │   │ │                               └─ TransitionAssetData             │
    │   │   │ │                                                                  │
    │   │   │ │  🏷️ 知识维度标签 (KNOWLEDGE_DIMENSIONS)                          │
    │   │   │ │  map | concepts | math | tutorial | code                         │
    │   │   │ │  | pitfalls | history | bridge | first_principles                │
    │   │   │ │                                                                  │
    │   │   │ │  📦 14 种原子类型 (AtomType)                                     │
    │   │   │ │  narration_segment | formula | code_snippet | timeline_event     │
    │   │   │ │  | comparison | person_card | story | term_definition            │
    │   │   │ │  | bullet_points | chapter_card | diagram_spec | data_table     │
    │   │   │ │  | quote | audio_clip                                            │
    │   │   │ └──────────────────────────────────────────────────────────────────┘
    │   │
    │   │ ── 积木系统 ──
    │   ├── 📄 types.ts                    ← 积木数据类型（BlockData, SceneData...）
    │   ├── 📄 video-theme.ts              ← 视频渲染主题（Remotion 用）
    │   │
    │   │ ── 动画系统 ──
    │   ├── 📄 anim-types.ts               ← 动画原子类型定义
    │   └── 📄 animation-atoms.ts          ← 可复用动画原子库
    │
    │
    │ ═══════════════════════════════════════════════════════════
    │ 🧱 blocks/ — M6 动画引擎（积木组件库）
    │ ═══════════════════════════════════════════════════════════
    │
    ├── blocks/
    │   │
    │   ├── 📄 catalog.ts                  ← 积木注册表 SSOT（6 分类 × 20 积木）
    │   ├── 📄 index.ts                    ← 积木导出总入口
    │   │
    │   │ ┌─ 6 大积木分类 ──────────────────────────────────────────────────────┐
    │   │ │                                                                      │
    │   │ │  📐 formula/      公式类 ── LaTeX 公式展示 & 推导                     │
    │   ├── formula/
    │   │   ├── FormulaBlock.tsx            ←  .tsx  数据接口层
    │   │   ├── FormulaBlock.view.tsx       ← .view  纯视觉层（React 组件）
    │   │   ├── FormulaBlock.motion.tsx     ← .motion 动画层（Remotion 动画）
    │   │   ├── FormulaDerivation.tsx       ←  多步公式推导
    │   │   ├── FormulaDerivation.view.tsx
    │   │   └── FormulaDerivation.motion.tsx
    │   │   [待实现] FormulaComparison      ←  公式对比
    │   │ │                                                                      │
    │   │ │  ⚖️ structure/    对比+关系类 ── 对比面板、时间线、树图、流程图        │
    │   ├── structure/
    │   │   ├── ComparisonSplit.tsx         ←  A vs B 左右对比
    │   │   ├── ComparisonSplit.view.tsx
    │   │   ├── ComparisonSplit.motion.tsx
    │   │   ├── Timeline.tsx               ←  垂直时间线
    │   │   ├── Timeline.view.tsx
    │   │   └── Timeline.motion.tsx
    │   │   [待实现] TreeDiagram            ←  树状层级图
    │   │   [待实现] FlowDiagram            ←  流程图
    │   │   [待实现] NetworkDiagram         ←  网络关系图
    │   │ │                                                                      │
    │   │ │  📊 chart/        图表类 ── 数据可视化 SVG 图表                       │
    │   ├── chart/
    │   │   ├── UCurve.tsx                 ←  U 形曲线（偏差-方差）
    │   │   ├── UCurve.view.tsx
    │   │   └── UCurve.motion.tsx
    │   │   [待实现] ScatterPlot2D         ←  2D 散点图
    │   │   [待实现] BarChart              ←  柱状图
    │   │   [待实现] HeatMap               ←  热力图
    │   │ │                                                                      │
    │   │ │  🖼️ data/         展示类 ── 静态内容展示（卡片、代码、图片）           │
    │   ├── data/
    │   │   ├── StatCards.tsx               ←  统计卡片网格
    │   │   ├── StatCards.view.tsx
    │   │   ├── StatCards.motion.tsx
    │   │   ├── CodeBlock.tsx              ←  代码块（语法高亮）
    │   │   ├── CodeBlock.view.tsx
    │   │   ├── CodeBlock.motion.tsx
    │   │   ├── ImageDisplay.tsx           ←  图片展示
    │   │   ├── ImageDisplay.view.tsx
    │   │   ├── ImageDisplay.motion.tsx
    │   │   ├── ProgressBars.tsx           ←  进度条对比
    │   │   ├── ProgressBars.view.tsx
    │   │   └── ProgressBars.motion.tsx
    │   │ │                                                                      │
    │   │ │  🎬 process/      过程类 ── 算法/数据变换动画 [全部待实现]             │
    │   │   [待实现] MatrixAnimation       ←  矩阵运算动画
    │   │   [待实现] GradientDescent       ←  梯度下降动画
    │   │   [待实现] ConvolutionAnimation  ←  卷积核滑动
    │   │   [待实现] DataTransform         ←  数据变换过程
    │   │ │                                                                      │
    │   │ │  每个积木遵循三层架构:                                                │
    │   │ │    .tsx     数据接口层  ── props 类型 + 导出                          │
    │   │ │    .view    纯视觉层    ── React 组件，不含动画                        │
    │   │ │    .motion  动画层      ── Remotion 动画包装器                         │
    │   │ └──────────────────────────────────────────────────────────────────────┘
    │
    │
    │ ═══════════════════════════════════════════════════════════
    │ 📊 data/ — 示例数据（供管理界面开发用）
    │ ═══════════════════════════════════════════════════════════
    │
    ├── data/
    │   ├── 📄 demo-assets.ts              ← 18 个 KNN 示例素材（按视频制作维度分类）
    │   └── 📄 video-projects.ts           ← 视频项目列表 & 进度数据
    │
    │
    │ ═══════════════════════════════════════════════════════════
    │ 🖥️ pages/ — 管理界面页面
    │ ═══════════════════════════════════════════════════════════
    │
    ├── pages/
    │   │
    │   │ ── M0 总览 ──
    │   ├── 📄 Dashboard.tsx               ← 🏠 首页仪表盘（统计 + 分类概览 + 项目进度）
    │   │
    │   │ ── M1-M5, M8 素材管理 ──
    │   ├── 📄 AssetLibrary.tsx            ← 📦 素材库（分类侧栏 + 子分类 + 搜索筛选）
    │   ├── 📄 AssetDetail.tsx             ← 📋 素材详情（预览 + 元数据 + 来源引用）
    │   │
    │   │ ── M6 动画引擎 ──
    │   ├── 📄 BlockCatalog.tsx            ← 🧱 积木目录（分类浏览 + 评分 + 状态）
    │   ├── 📄 BlockDetail.tsx             ← 🔍 积木详情（实时预览 + 参数编辑 + 评审）
    │   │
    │   │ ── M9 + M10 视频制作 ──
    │   ├── 📄 VideoList.tsx               ← 🎬 视频项目列表
    │   └── 📄 VideoPipeline.tsx           ← ⚙️ 视频制作流水线（阶段进度）
    │
    │
    │ ═══════════════════════════════════════════════════════════
    │ 🧩 components/ — 可复用 UI 组件
    │ ═══════════════════════════════════════════════════════════
    │
    └── components/
        ├── 📄 ui.tsx                      ← 基础 UI（Card, SearchBar, FilterPills, ProgressBar...）
        ├── 📄 AssetPreview.tsx            ← 素材迷你预览（7 种分类各一个渲染器）
        └── 📄 BlockPreview.tsx            ← 积木实时预览渲染器
```

---

## 🏗️ 10 大管理模块详解

### 4 层架构 × 10 模块 × 37 子模块

```
═══════════════════════════════════════════════════════════════════
  层               模块                  子模块                 教科书
═══════════════════════════════════════════════════════════════════

📝 内容层 Content Layer
│
├── M1 🎭 脚本工坊 Script Workshop ─────────── Snyder + McKee
│   ├── M1.1 故事结构      三幕/五幕 + Beat Sheet 15 拍
│   ├── M1.2 旁白文稿      每场景旁白 + 语气标注 (casual/serious/humorous)
│   ├── M1.3 节奏设计      每句时长预估 + 停顿标记
│   └── M1.4 冲突弧线      问题→紧张→解决 情感节奏
│
├── M4 📊 数据源 Data Sources ───────────── Knaflic + Mayer
│   ├── M4.1 时间线数据    {year, text, color, icon}[]
│   ├── M4.2 对比结构      {left, right} 两列结构
│   ├── M4.3 数值数据集    驱动图表的 JSON/CSV
│   ├── M4.4 代码示例      可运行的代码片段
│   └── M4.5 参数表        key-value 属性表
│
└── M8 📖 来源引用 References ──────────── 学术规范
    ├── M8.1 教科书库      已索引教科书 + 章节结构
    ├── M8.2 引用管理      每个素材绑定 citation
    ├── M8.3 版权检查      图片/代码 license 状态
    └── M8.4 片尾字幕      参考文献列表生成


🎨 表现层 Presentation Layer
│
├── M2 🎨 视觉画面 Visual Assets ──────── Mayer Multimedia + Knaflic
│   ├── M2.1 动画规格      Manim/Motion 动画描述 + 参数
│   ├── M2.2 图表设计      柱状/散点/热力图/U曲线...
│   ├── M2.3 示意图        概念图、流程图、树图
│   ├── M2.4 屏幕录制      软件操作录屏规格
│   └── M2.5 插画/照片     静态图像素材
│
├── M3 ✏️ 文字叠层 Text Overlays ──────── Mayer Redundancy + Signaling
│   ├── M3.1 标题卡        场景标题 + 章节卡
│   ├── M3.2 要点列表      3-5 条 bullet points
│   ├── M3.3 公式渲染      LaTeX 公式 + 直觉注释
│   ├── M3.4 代码块        语法高亮代码片段
│   ├── M3.5 字幕          旁白字幕 + 时间戳
│   └── M3.6 标注/引用     画面内箭头/框/标注
│
├── M5 🔊 音频中心 Audio Center ──────── Mayer Modality + Voice
│   ├── M5.1 TTS 合成      文字→语音（声音克隆参数）
│   ├── M5.2 BGM           低调背景音乐
│   ├── M5.3 转场音效      whoosh/ding 转场音
│   ├── M5.4 提示音        强调关键点的提示音
│   └── M5.5 时间戳        每段旁白 start/end
│
└── M6 🧱 动画引擎 Animation Engine ──── Williams 动画原理
    ├── M6.1 积木注册表    catalog.ts（类型/参数/预览/评分）
    ├── M6.2 积木预览      管理界面实时预览
    ├── M6.3 积木评分      Mayer/CRAP/动画/灵活性/代码 5 维评分
    └── M6.4 Remotion桥接  积木组件 → Remotion Composition


🎬 组装层 Assembly Layer
│
├── M9 🎞️ 场景编排 Scene Composer ────── Snyder BS2 + Mayer Segmenting
│   ├── M9.1 场景列表      全部场景顺序 + 归属幕（Act）
│   ├── M9.2 布局选择      split / fullscreen / three-column
│   ├── M9.3 素材绑定      每场景 ← visual + overlay + data
│   └── M9.4 转场设计      场景间过渡效果 + 章节卡
│
└── M10 ⏱️ 时间线 Timeline Editor ────── Mayer Temporal Contiguity
    ├── M10.1 场景时序     每场景 start / end / duration
    ├── M10.2 旁白对齐     timestamps → 场景映射
    ├── M10.3 字幕时序     字幕 start/end/text
    └── M10.4 总时长计算   所有场景 + 间隙 = 总帧数


🔍 质量层 Quality Layer
│
└── M7 📋 质量审查 Quality Review ────── Clark & Mayer Ch.17 Checklist
    ├── M7.1 冗余检查      旁白+画面+文字 三重冗余？    [🔴 严重]
    ├── M7.2 时间同步      画面和旁白同步吗？            [🔴 严重]
    ├── M7.3 空间邻近      文字离图片太远？              [🟡 中等]
    ├── M7.4 相干性        不相关的装饰图/BGM？          [🟡 中等]
    ├── M7.5 分段检查      连续播放 > 3 分钟无交互？     [🟡 中等]
    ├── M7.6 声音质量      机器声 vs 人声？              [🟢 建议]
    └── M7.7 人格化        正式语气 vs 对话语气？        [🟢 建议]

═══════════════════════════════════════════════════════════════════
```

---

## 🔄 视频制作工作流 — 完整流水线

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  📂 knowledge-map/                    知识源文件（.md）                   │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────┐                                                    │
│  │ Phase 1: 拆解    │  knowledge-map → 分解为 7 类素材                    │
│  │ M1 脚本          │  ① 旁白文稿 (narration)                            │
│  │ M4 数据源        │  ② 视觉画面描述 (visual)                           │
│  │ M8 引用          │  ③ 要点/公式/代码 (text_overlay)                    │
│  │                  │  ④ 结构化数据 (data)                               │
│  └────────┬─────────┘  ⑤ 来源引用 (reference)                           │
│           │             ⑥ 转场卡片 (transition)                          │
│           ▼             ⑦ 音效规格 (audio)                               │
│  ┌─────────────────┐                                                    │
│  │ Phase 2: 脚本    │  旁白文稿 → Beat Sheet 节拍结构                     │
│  │ M1.1 故事结构    │  OpenImage → Theme → Setup → Catalyst → ...        │
│  │ M1.4 冲突弧线    │  标注每段旁白的语气 + 停顿 + 时长                     │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │ Phase 3: 音频    │  旁白文稿 → TTS 合成 → timestamps.json              │
│  │ M5.1 TTS 合成    │  选择 BGM + 配置音效                                │
│  │ M5.5 时间戳      │  输出: .mp3 + timestamps.json + subtitles.json     │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │ Phase 4: 视觉    │  为每个场景选择/制作视觉素材                         │
│  │ M2 视觉画面      │  Manim 动画 / 图表 / 插画 / 屏幕录制                 │
│  │ M6 动画引擎      │  选择积木组件 + 绑定数据                             │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │ Phase 5: 叠层    │  为每个场景配置文字叠层                              │
│  │ M3 文字叠层      │  标题 + 要点 + 公式/代码                             │
│  │                  │  ⚠️ 遵守 Mayer Redundancy 原则                     │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │ Phase 6: 编排    │  场景 = 布局 + 视觉 + 叠层 + 旁白                   │
│  │ M9 场景编排      │  SplitSlide: 55% visual + 45% keypoints             │
│  │ M9.2 布局选择    │  或 Fullscreen / Three-column                       │
│  │ M9.3 素材绑定    │  每场景绑定所有素材                                  │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │ Phase 7: 时间线  │  timestamps × 场景 → 精确帧数                       │
│  │ M10 时间线       │  旁白时间戳 → 场景时间戳                             │
│  │ M10.2 旁白对齐   │  字幕时间戳同步                                      │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │ Phase 8: 审查    │  Mayer 12 原则自动检查                              │
│  │ M7 质量审查      │  冗余? 同步? 邻近? 相干?                             │
│  │                  │  输出 review_report.md                              │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐                                                    │
│  │ Phase 9: 渲染    │  Remotion 渲染最终视频                              │
│  │ video-content/   │  npx remotion render                                │
│  │                  │  1920×1080 / 30fps                                  │
│  └─────────────────┘                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 统计概要

| 维度 | 数量 | 说明 |
|------|------|------|
| **大层** | 4 | 内容 → 表现 → 组装 → 质量 |
| **管理模块** | 10 | M1 ~ M10 |
| **子模块** | 37 | 见上方详细列表 |
| **素材分类** | 7 | narration / visual / text_overlay / audio / data / reference / transition |
| **素材子分类** | 32 | 5 + 6 + 6 + 4 + 5 + 4 + 4 (不含 audio 实际只 4) |
| **原子类型** | 14 | 跨分类的数据形态描述 |
| **知识维度标签** | 9 | map / concepts / math / tutorial / code / pitfalls / history / bridge / first_principles |
| **积木分类** | 6 | formula / compare / chart / relation / display / process |
| **已实现积木** | 8 | FormulaBlock, FormulaDerivation, ComparisonSplit, Timeline, UCurve, StatCards, CodeBlock, ImageDisplay |
| **待实现积木** | 12 | FormulaComparison, ProgressBars(✅), ScatterPlot2D, BarChart, HeatMap, TreeDiagram, FlowDiagram, NetworkDiagram, MatrixAnimation, GradientDescent, ConvolutionAnimation, DataTransform |
| **积木三层架构** | 3 | .tsx(数据) + .view.tsx(视觉) + .motion.tsx(动画) |
| **页面** | 7 | Dashboard, AssetLibrary, AssetDetail, BlockCatalog, BlockDetail, VideoList, VideoPipeline |

---

## 🎓 理论基础

| 教科书 | 作者 | 核心贡献 | 对应模块 |
|--------|------|---------|---------|
| Multimedia Learning | Mayer | Dual-Channel 理论 + 12 设计原则 | M1, M2, M3, M5, M7 |
| e-Learning & Science of Instruction | Clark & Mayer | 12 原则实践指南 + 检查清单 | M3, M7 |
| Save the Cat | Snyder | Blake Snyder Beat Sheet (15 拍) | M1, M9 |
| Story | McKee | 三幕结构 · Scene → Beat → Story | M1 |
| Storytelling with Data | Knaflic | 数据可视化叙事 | M2, M4 |
| Animator's Survival Kit | Williams | 动画 12 原则: Timing, Spacing, Ease | M6, M10 |

---

## 🚀 快速启动

```bash
# 管理界面（Vite）
cd video-lego
npm install
npm run dev           # → http://localhost:5173

# 视频渲染（Remotion）— 另一个项目
cd ../video-content
npm install
npx remotion preview  # → http://localhost:3001
```

---

## 📁 关联项目

```
aisd/
├── video-lego/        ← 本项目：管理系统 (Vite + React)
├── video-content/     ← 视频渲染引擎 (Remotion)
│   └── 使用 video-lego/src/blocks/ 的积木组件
└── data/
    ├── knowledge-maps/  ← 知识源文件
    └── mineru_output/   ← 教科书 PDF → Markdown
        ├── mayer_multimedia_learning/
        ├── clark_mayer_elearning/
        ├── snyder_save_the_cat/
        └── ...
```
