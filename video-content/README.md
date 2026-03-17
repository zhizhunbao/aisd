# 🧱 Video Lego — 教科书驱动 × 乐高积木视频生产系统

> **一句话**：写一个数据文件 → 自动出教育视频。  
> **核心理念**：视频 = 积木 + 布局 + 旁白。三者解耦，任意组合。

---

## 目录

- [系统全景](#系统全景)
- [架构设计](#架构设计)
- [三层解耦](#三层解耦)
- [积木目录](#积木目录)
- [布局系统](#布局系统)
- [引擎系统](#引擎系统)
- [数据驱动](#数据驱动)
- [做一个新视频](#做一个新视频)
- [新增积木规范](#新增积木规范)
- [设计原则](#设计原则)
- [目录结构](#目录结构)

---

## 系统全景

```
┌─────────────────────────────────────────────────────────┐
│                    video.data.ts                        │
│              （唯一需要写的文件）                          │
│                                                         │
│  meta:      { topic, course, title, sources }           │
│  narration: { audioFile, timestamps[], subtitles[] }    │
│  scenes:    [ { layout, visuals[], points[] } ... ]     │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│               VideoEngine (引擎)                        │
│                                                         │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │  Audio    │   │  Series +    │   │  Subtitle    │    │
│  │ (旁白)   │   │  SceneRenderer│   │  (字幕)     │    │
│  └──────────┘   └──────┬───────┘   └──────────────┘    │
│                        │                                │
│                        ▼                                │
│            ┌───────────────────────┐                    │
│            │    Layout (布局)      │                    │
│            │  SplitLayout 55/45   │                    │
│            │  FullScreenLayout    │ (TODO)              │
│            │  ThreeColumnLayout   │ (TODO)              │
│            └───────┬──────────────┘                    │
│                    │                                    │
│                    ▼                                    │
│          ┌─────────────────────┐                        │
│          │  Block Registry     │                        │
│          │  (积木注册表)        │                        │
│          │                     │                        │
│          │  FormulaBlock       │  ┌──────────────────┐  │
│          │  UCurve             │  │  BLOCK_REGISTRY  │  │
│          │  ComparisonSplit    │  │  name → Component │  │
│          │  StatCards          │  └──────────────────┘  │
│          │  ...                │                        │
│          └─────────────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

---

## 架构设计

### 核心思想：ECS 模式

借鉴游戏引擎的 Entity-Component-System 思想：

| 概念 | 对应 | 说明 |
|------|------|------|
| **Entity** | `SceneData` | 一个场景，是积木和要点的容器 |
| **Component** | `Block` | 可视化积木，如 `StatCards`、`UCurve` |
| **System** | `VideoEngine` | 引擎，读数据自动编排 |

### 数据流

```
video.data.ts  →  VideoEngine  →  SceneRenderer  →  Layout + Blocks  →  视频帧
                      ↓
                   Audio + Subtitle（同步叠加）
```

---

## 三层解耦

| 层 | 职责 | 文件 | 改动频率 |
|----|------|------|---------|
| **积木层** | 一个可视化组件 | `src/lib/blocks/*/` | 低 — 写好复用 |
| **布局层** | 画面排版方式 | `src/lib/layouts/` | 极低 — 极少新增 |
| **数据层** | 某个视频的全部内容 | `src/videos/*/video.data.ts` | 高 — 每个视频一份 |

> **做新视频** = 只写数据层文件，积木和布局自动复用。

---

## 积木目录

### 📐 公式类 Formula

> 教科书核心竞争力 — 公式展示与推导动画

| 积木 | 状态 | 说明 | Props |
|------|------|------|-------|
| **FormulaBlock** | ✅ READY | 单个 LaTeX 公式展示 | `latex`, `label?`, `color?` |
| **FormulaDerivation** | ✅ READY | 逐步公式推导动画 | `steps: { latex, annotation?, highlight? }[]`, `source?` |
| **FormulaComparison** | ⬜ TODO | 两公式并排对比（Ridge vs Lasso） | `left: { latex, label }`, `right: { latex, label }` |

### 📊 图表类 Chart

> 教科书图表可视化 — 曲线、散点、柱状、热力

| 积木 | 状态 | 说明 | Props |
|------|------|------|-------|
| **UCurve** | ✅ READY | U/J/L 形曲线，区域标注+最优点 | `points[]`, `xLabel`, `yLabel`, `zones?`, `bestPoint?` |
| **ScatterPlot2D** | ⬜ TODO | 2D 散点图 + 决策边界 + 查询点动画 | `points[]`, `queryPoint?`, `boundaries?` |
| **BarChart** | ⬜ TODO | 柱状图/直方图 | `bars: { label, value, color }[]` |
| **HeatMap** | ⬜ TODO | 热力图/混淆矩阵 | `matrix[][]`, `xLabels`, `yLabels` |

### 🏗️ 结构类 Structure

> 概念关系 — 对比、时间线、树形、流程

| 积木 | 状态 | 说明 | Props |
|------|------|------|-------|
| **ComparisonSplit** | ✅ READY | A vs B 左右滑入对比 | `left: { label, value, icon?, color, subItems? }`, `right` |
| **Timeline** | ✅ READY | 垂直/水平时间线 | `events: { year, text, icon?, color? }[]` |
| **TreeDiagram** | ⬜ TODO | 树形结构图（KD-Tree / 决策树） | `root: TreeNode` |
| **FlowDiagram** | ⬜ TODO | 流程图（RAG / 训练流程） | `steps: { label, icon?, color? }[]` |
| **NetworkDiagram** | ⬜ TODO | 神经网络层级图 | `layers: { type, units, label? }[]` |

### 📋 数据展示 Data

> 数据卡片、进度条、代码块、图片展示

| 积木 | 状态 | 说明 | Props |
|------|------|------|-------|
| **StatCards** | ✅ READY | 数据卡片网格，弹簧动画 | `cards: { label, value, icon?, color, desc? }[]` |
| **ProgressBars** | ✅ READY | 动画填充进度条 | `bars: { label, value(0-100), color }[]` |
| **CodeBlock** | ✅ READY | 深色代码展示块 | `code`, `language?`, `label?`, `color?` |
| **ImageDisplay** | ✅ READY | 教科书图片/人物照片 | `src`, `caption?`, `maxHeight?` |

### 🎬 动画类 Animation

> ML 专用动画 — 矩阵运算、梯度下降、卷积操作

| 积木 | 状态 | 说明 | Props |
|------|------|------|-------|
| **MatrixAnimation** | ⬜ TODO | 矩阵乘法/加法/卷积逐元素动画 | `left[][]`, `right[][]`, `result[][]`, `operation` |
| **GradientDescent** | ⬜ TODO | 梯度下降路径可视化 | `path[]`, `learningRate`, `surfacePoints?` |
| **ConvolutionAnimation** | ⬜ TODO | 卷积核滑动窗口 | `input[][]`, `kernel[][]`, `stride?`, `padding?` |
| **DataTransform** | ⬜ TODO | 数据变换前后对比（PCA/归一化） | `before[]`, `after[]`, `transformLabel` |

### 进度概览

```
总计: 19 积木
├── ✅ READY:  9 积木 (47%)
└── ⬜ TODO:  10 积木 (53%)
```

---

## 布局系统

布局定义一帧画面的空间分区方式。积木填入布局的插槽中。

### SplitLayout（✅ 已实现）

```
┌────────────────────────────────────────────────────────┐
│  幕名标签                 场景标题                       │
├──────────────────────────────┬─────────────────────────┤
│                              │                         │
│     左侧 55%                │    右侧 45%              │
│     可视化积木               │    要点列表               │
│                              │    · icon + text         │
│     FormulaBlock             │    · icon + text         │
│     StatCards                │    · (highlight)         │
│     ComparisonSplit          │    · (formula + latex)   │
│     ...                      │    · (warning)           │
│                              │                         │
│                              │    ┌──────────────────┐ │
│                              │    │ 💡 结论横幅      │ │
│                              │    └──────────────────┘ │
├──────────────────────────────┴─────────────────────────┤
│                    字幕安全区 (140px)                    │
└────────────────────────────────────────────────────────┘
```

**Props**:
- `act: string` — 幕名（第一幕 · 起源）
- `title: string` — 场景标题
- `titleColor?: string`
- `points: KeyPoint[]` — 右侧要点
- `conclusion?: { text, icon? }` — 结论横幅
- `children` — 左侧可视化积木

**KeyPoint 类型**:
```typescript
interface KeyPoint {
  icon?: string;          // emoji 图标
  text: string;           // 要点文字
  color?: string;         // 自定义颜色
  bold?: boolean;         // 加粗
  variant?: 'normal' | 'highlight' | 'warning' | 'formula';
  latex?: string;         // variant='formula' 时用
}
```

### FullScreenLayout（⬜ TODO）

全画面布局，用于全屏动画或大型可视化。

### ThreeColumnLayout（⬜ TODO）

三列布局：左-人物 / 中-核心内容 / 右-关键词。

---

## 引擎系统

### VideoEngine

读取 `VideoData` 数据对象，自动编排：

1. **Audio** — 挂载旁白 MP3
2. **Series** — 按 `timestamps[]` 顺序编排场景序列
3. **SceneRenderer** — 每个场景根据 `layout` 选布局，根据 `visuals[]` 选积木
4. **Subtitle** — 叠加字幕层

```
VideoEngine
├── <Audio>
├── <Series>
│   ├── <Series.Sequence durationInFrames={...}>
│   │   └── <SceneRenderer scene={scenes[0]} />
│   ├── <Series.Sequence durationInFrames={...}>
│   │   └── <SceneRenderer scene={scenes[1]} />
│   └── ...
└── <Subtitle entries={subtitles} />
```

### SceneRenderer

根据场景的 `layout` 字段选布局组件，根据 `visuals[]` 从 `BLOCK_REGISTRY` 查找积木组件：

```typescript
// 伪代码
scene.visuals.map(v => {
  const Block = BLOCK_REGISTRY[v.block];  // 查注册表
  return <Block {...v.data} />;           // 传数据渲染
});
```

如果积木不在注册表中，显示红色占位提示 `⚠️ Block "XXX" not found`。

---

## 数据驱动

### video.data.ts — 做视频唯一需要写的文件

```typescript
import type { VideoData } from '../../lib/types';

export const MY_VIDEO: VideoData = {
  // 1. 元数据
  meta: {
    topic: 'knn',
    course: 'machine-learning',
    title: 'KNN — 从抄作业到 AI 基础设施',
    textbookSource: 'ISL Ch.2, PRML Ch.2.5.2',
    totalDurationSec: 395.3,
  },

  // 2. 旁白
  narration: {
    audioFile: 'narration/knn/full_narration.mp3',
    timestamps: [
      { start: 0.0, end: 13.52 },
      { start: 13.82, end: 24.94 },
      // ...每个 scene 一个时间段
    ],
    subtitles: [
      { start: 0.0, end: 13.52, text: '1951年美国空军出了个难题...' },
      // ...
    ],
  },

  // 3. 场景列表 — 选积木 + 填数据
  scenes: [
    {
      layout: 'split',
      act: '第一幕 · 起源',
      title: '1951 · 分类问题的诞生',
      visuals: [
        {
          block: 'ImageDisplay',                        // ← 选积木
          data: { src: 'photos/knn/fix.jpg' },          // ← 填数据
        },
        {
          block: 'StatCards',                            // ← 选积木
          data: {                                       // ← 填数据
            cards: [
              { label: '提出者', value: 'Fix & Hodges', icon: '👤', color: '#4ea8de' },
            ],
          },
        },
      ],
      points: [
        { icon: '✈️', text: '美国空军 · 统计分类问题', bold: true },
        { icon: '💡', text: '找最像的人 → 直接抄答案', variant: 'highlight' },
      ],
      conclusion: { text: '思路极其简单 — 找最近 → 抄标签', icon: '⭐' },
    },
    // ... 更多 scenes
  ],
};
```

### 核心原则：数据 ≠ 代码

| 做视频的人 | 需要写 | 不需要碰 |
|-----------|-------|---------|
| **内容创作者** | `video.data.ts` | 任何 React 组件 |
| **积木开发者** | `src/lib/blocks/*/` | 任何视频数据文件 |
| **布局设计者** | `src/lib/layouts/` | 任何视频数据文件 |

---

## 做一个新视频

### 三步出视频

```bash
# 1. 创建数据文件
#    src/videos/{course}/{topic}/video.data.ts

# 2. 注册到 Root.tsx
#    import { MY_VIDEO } from './videos/...';
#    <Composition id="my-video" component={VideoEngine} defaultProps={{ data: MY_VIDEO }} ... />

# 3. 预览 / 渲染
npm run preview                                       # 预览
npx remotion render src/index.tsx my-video --output output/my-video.mp4  # 渲染
```

### 场景 ← 积木映射表（以 KNN 为例）

| Segment | 旁白摘要 | 积木 | 状态 |
|---------|---------|------|------|
| S1 | 1951 美国空军 | `ImageDisplay` + `StatCards` | ✅ |
| S2 | Fix & Hodges 抄答案 | `StatCards` + `ScatterPlot2D` | ⬜ |
| S3 | 勾股定理→距离 | `FormulaDerivation` | ✅ |
| S4 | 石沉大海 | `ImageDisplay` + `Timeline` | ✅ |
| S5 | Cover-Hart 定理 | `ImageDisplay` + `FormulaBlock` | ✅ |
| S6 | KNN = 抄邻居作业 | `ComparisonSplit` | ✅ |
| S7 | K 值两个极端 | `ComparisonSplit` | ✅ |
| S8 | 偏差-方差曲线 | `UCurve` | ✅ |
| S9 | 惰性学习 | `ComparisonSplit` | ✅ |
| S10 | 公理1 局部连续 | `StatCards` | ✅ |
| S11 | 公理2 距离管用 | `ComparisonSplit` | ✅ |
| S12 | 公理3 数据够多 | `ProgressBars` | ✅ |
| S13 | 三公理总结 | `StatCards` + `FormulaBlock` | ✅ |
| S14 | 坑1 归一化 | `ComparisonSplit` + `CodeBlock` | ✅ |
| S15 | 维度灾难 | `ProgressBars` | ✅ |
| S16 | 维度灾难解法 | `ComparisonSplit` + `FormulaBlock` | ✅ |
| S17 | KD-Tree | `ImageDisplay` + `ComparisonSplit` | ✅ |
| S18 | ANN 演进 | `Timeline` + `StatCards` | ✅ |
| S19 | ChatGPT = KNN | `Timeline` | ✅ |
| S20 | 下期预告 | `StatCards` | ✅ |

---

## 新增积木规范

### 1. 定义接口（types.ts）

```typescript
/** 我的新积木数据 */
export interface MyBlockData {
  // 必填 props
  items: { label: string; value: number }[];
  // 可选 props
  source?: string;  // 教科书来源标注
}
```

并在 `BlockDataMap` 中注册：

```typescript
export interface BlockDataMap {
  // ... 已有积木
  MyBlock: MyBlockData;
}
```

### 2. 实现组件（blocks/category/MyBlock.tsx）

```typescript
import React from 'react';
import { useCurrentFrame, spring, useVideoConfig } from 'remotion';
import { THEME } from '../../theme';
import type { MyBlockData } from '../../types';

export const MyBlock: React.FC<MyBlockData> = ({ items, source }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 弹簧动画示例
  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 80 } });

  return (
    <div style={{ transform: `scale(${Math.max(0.01, scale)})` }}>
      {/* 积木内容 */}
    </div>
  );
};
```

### 3. 注册（blocks/index.ts）

```typescript
import { MyBlock } from './category/MyBlock';

export const BLOCK_REGISTRY = {
  // ... 已有积木
  MyBlock,
};
```

### 积木编写规则

| 规则 | 说明 |
|------|------|
| **纯 props 驱动** | 不读外部文件，不 fetch，所有数据从 props 来 |
| **用 THEME 常量** | 颜色用 `THEME.gold` 不用 `'#ffd700'`，字号用 `THEME.fontSize.body` |
| **动画用 Remotion API** | `spring()`, `interpolate()`, `useCurrentFrame()` |
| **字幕安全区** | 底部 140px 不放内容（`THEME.subtitleSafeY`） |
| **宽度自适应** | 积木宽度用 `%` 或 `width: '95%'`，不用固定 px |
| **source 标注** | 如果积木展示教科书来源，加 `source?: string` prop |

---

## 设计原则

### Mayer 多媒体学习原则

> 📚 Mayer (2009). *Multimedia Learning*. Cambridge University Press.

| 原则 | 在系统中的体现 |
|------|--------------|
| **Coherence** | 积木只做一件事，不加装饰 |
| **Signaling** | `THEME` 统一颜色层级：金=结论、蓝=概念、红=警告 |
| **Redundancy** | 旁白讲故事，画面放积木（不在画面上重复旁白文字） |
| **Spatial Contiguity** | SplitLayout 左视觉右要点，相关内容紧邻 |
| **Segmenting** | 1 段旁白 = 1 个场景 = 1 组积木 |
| **Personalization** | 旁白用口语化（袁腾飞/老高/罗翔风格） |
| **Voice** | TTS 声音克隆（Qwen3-TTS） |

### CRAP 设计原则

> 📚 Williams (2002). *The Non-Designer's Design Book*.

| 原则 | 在系统中的体现 |
|------|--------------|
| **Contrast** | `THEME.fontSize` 四级字号层级 |
| **Repetition** | 所有积木共用 `THEME` 配色和圆角 |
| **Alignment** | SplitLayout CSS 对齐，左栏居中，右栏左对齐 |
| **Proximity** | 同场景积木紧邻，不同场景 Series.Sequence 分隔 |

### Clark & Mayer 素材分类原则

> 📚 Clark & Mayer (2016). *e-Learning and the Science of Instruction*, Ch.4.

| 素材类型 | 对应积木 | 来源 |
|---------|---------|------|
| **Representational（再现）** | `ImageDisplay` | Wikimedia Commons / 论文 |
| **Organizational（组织）** | `Timeline`, `ComparisonSplit`, `StatCards` | Remotion 组件 |
| **Transformational（变化）** | `ScatterPlot2D`, `DataTransform`, 动画类 | Remotion 组件 |
| **Interpretive（阐释）** | `FormulaBlock`, `UCurve` | Remotion + react-katex |
| **Decorative（装饰）** | ❌ 禁止 | — |

---

## 目录结构

```
video-content/
├── README.md                            ← 你在这里
├── package.json                         # video-lego 包配置
├── remotion.config.ts                   # Remotion 配置
├── catalog.html                         # 积木可视化目录（独立页面）
│
├── src/
│   ├── index.tsx                        # Remotion 入口
│   ├── Root.tsx                         # Composition 注册（加新视频在这里）
│   ├── react-katex.d.ts                 # LaTeX 类型声明
│   │
│   ├── lib/                             # 核心库 — 积木开发者工作区
│   │   ├── types.ts                     # 🔑 所有积木/场景/视频的 TypeScript 接口
│   │   ├── theme.ts                     # 🎨 全局主题（颜色、字号、安全区）
│   │   │
│   │   ├── blocks/                      # 🧱 积木组件
│   │   │   ├── index.ts                 # 积木注册表 BLOCK_REGISTRY
│   │   │   ├── formula/                 # 📐 公式类
│   │   │   │   ├── FormulaBlock.tsx
│   │   │   │   └── FormulaDerivation.tsx
│   │   │   ├── chart/                   # 📊 图表类
│   │   │   │   └── UCurve.tsx
│   │   │   ├── structure/               # 🏗️ 结构类
│   │   │   │   ├── ComparisonSplit.tsx
│   │   │   │   └── Timeline.tsx
│   │   │   └── data/                    # 📋 数据展示类
│   │   │       ├── StatCards.tsx
│   │   │       ├── ProgressBars.tsx
│   │   │       ├── CodeBlock.tsx
│   │   │       └── ImageDisplay.tsx
│   │   │
│   │   ├── layouts/                     # 📐 布局模板
│   │   │   └── SplitLayout.tsx          # 55/45 左右分栏
│   │   │
│   │   └── engine/                      # ⚙️ 引擎
│   │       ├── VideoEngine.tsx          # 视频编排引擎
│   │       ├── SceneRenderer.tsx        # 场景渲染器
│   │       └── Subtitle.tsx             # 字幕组件
│   │
│   ├── videos/                          # 📹 视频数据 — 内容创作者工作区
│   │   └── machine-learning/
│   │       └── knn/
│   │           └── video.data.ts        # KNN 视频数据文件
│   │
│   └── catalog/                         # 📖 积木目录预览
│       └── BlockCatalog.tsx
│
├── public/                              # 静态资源
│   ├── narration/                       # 旁白音频
│   └── photos/                          # 人物照片/论文截图
│
└── machine-learning/                    # 素材源文件
    └── knn/
        ├── script.md                    # 脚本（旁白+积木映射）
        └── script_tts.txt               # TTS 纯文本
```

---

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Remotion** | 4.0 | React 视频框架 |
| **React** | 19 | UI 组件 |
| **TypeScript** | 5.9 | 类型安全 |
| **react-katex** | 3.1 | LaTeX 公式渲染 |
| **remotion-animated** | 2.2 | 额外动画工具 |

```bash
# 预览
npm run preview

# 渲染某个视频
npx remotion render src/index.tsx knn --output output/knn.mp4

# 积木目录预览（独立 Composition）
# 访问 http://localhost:3000/block-catalog
```
