# Blackboard Flash Video — 系统架构

## 1. 设计原则

- **复用优先**：不新建引擎，复用现有 `VideoEngine` + `SceneRenderer` + `Subtitle`
- **积木扩展**：新增积木 + 布局，不修改已有积木逻辑
- **类型安全**：扩展现有 TypeScript 类型系统

---

## 2. 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    video-content (消费侧)                    │
│                                                              │
│  Root.tsx                                                    │
│    └─ Composition id="linear-algebra-flash"                  │
│         └─ VideoEngine  ← 复用，不改                         │
│              ├─ Audio (旁白，可选)                            │
│              ├─ Series (场景序列)                             │
│              │   ├─ Scene 1 → SceneRenderer                  │
│              │   │              └─ layout='blackboard'        │
│              │   │                   └─ BlackboardLayout ★新  │
│              │   │                        └─ KnowledgeUnit ★新│
│              │   ├─ Scene 2 → ...                            │
│              │   └─ Scene 12 → ...                           │
│              └─ Subtitle (字幕，复用)                        │
│                                                              │
│  videos/linear-algebra/flash/video.data.ts  ★新              │
│                                                              │
└───────────────────────────────┬──────────────────────────────┘
                                │ imports
┌───────────────────────────────▼──────────────────────────────┐
│                    video-lego (积木侧)                       │
│                                                              │
│  lib/types.ts         ← 扩展 KnowledgeUnitData, LayoutType  │
│  lib/layouts/                                                │
│    ├─ SplitLayout.tsx          ← 已有，不改                  │
│    └─ BlackboardLayout.tsx     ★新                           │
│  blocks/                                                     │
│    ├─ formula/  chart/  data/  structure/  ← 已有            │
│    └─ knowledge/               ★新目录                       │
│        ├─ KnowledgeUnit.tsx                                  │
│        ├─ KnowledgeUnit.motion.tsx                           │
│        ├─ KnowledgeUnit.view.tsx                             │
│        └─ diagrams/            ★新: 2D 图解 SVG 组件库      │
│            ├─ EigenvalueDiagram.tsx                           │
│            ├─ MatrixMultiplyDiagram.tsx                       │
│            ├─ LinearTransformDiagram.tsx                      │
│            ├─ DeterminantDiagram.tsx                          │
│            └─ ...                                            │
│  blocks/index.ts      ← 注册新积木                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. 变更清单

### 3.1 video-lego 变更（积木侧）

| 文件 | 操作 | 描述 |
|------|------|------|
| `src/lib/types.ts` | 修改 | 新增 `KnowledgeUnitData`，扩展 `BlockDataMap`，扩展 `LayoutType` |
| `src/lib/layouts/BlackboardLayout.tsx` | 新增 | 全屏黑板布局组件 |
| `src/blocks/knowledge/KnowledgeUnit.tsx` | 新增 | 桶导出 |
| `src/blocks/knowledge/KnowledgeUnit.motion.tsx` | 新增 | Remotion 动画层 |
| `src/blocks/knowledge/KnowledgeUnit.view.tsx` | 新增 | 管理 UI 预览层 |
| `src/blocks/knowledge/diagrams/*.tsx` | 新增 | 2D 图解 SVG 组件 |
| `src/blocks/index.ts` | 修改 | 注册 KnowledgeUnit 到 BLOCK_REGISTRY |

### 3.2 video-content 变更（消费侧）

| 文件 | 操作 | 描述 |
|------|------|------|
| `src/lib/engine/SceneRenderer.tsx` | 修改 | 新增 `case 'blackboard'` 分支 |
| `src/videos/linear-algebra/flash/video.data.ts` | 新增 | MIT 线性代数 60s 数据文件 |
| `src/Root.tsx` | 修改 | 注册 `linear-algebra-flash` Composition |

---

## 4. 类型设计

### 4.1 KnowledgeUnitData（新增到 types.ts）

```typescript
/** 知识单元数据 — 一屏黑板上的完整内容 */
export interface KnowledgeUnitData {
  /** 中文核心术语 */
  zhName: string;
  /** 英文对照 */
  enName: string;
  /** 同义词/别名列表 */
  aliases?: string[];
  /** LaTeX 核心公式 */
  formula?: string;
  /** 公式标注文字 */
  formulaLabel?: string;
  /** 2D 图解组件名（在 DIAGRAM_REGISTRY 中查找） */
  diagram?: string;
  /** 一句话白话释义 */
  explanation: string;
  /** 中文名颜色（默认 white） */
  color?: string;
}
```

### 4.2 LayoutType 扩展

```typescript
// 原有
export type LayoutType = 'split';
// 新增
export type LayoutType = 'split' | 'blackboard';
```

### 4.3 BlockDataMap 扩展

```typescript
export interface BlockDataMap {
  // ... 已有积木 ...
  KnowledgeUnit: KnowledgeUnitData;
}
```

---

## 5. 组件设计

### 5.1 BlackboardLayout

**职责**：全屏黑板背景 + 顶部课程标题 + 渲染子组件

```
┌──────────────────────────────────────────┐
│  ▎MIT 线性代数              3/12         │ ← 课程名 + 进度
│                                          │
│                                          │
│            [ KnowledgeUnit ]             │ ← 子组件（知识单元）
│                                          │
│                                          │
│                                          │
│  ████████████ 字幕安全区 ████████████████ │ ← 底部 15%
└──────────────────────────────────────────┘
```

Props：
- `act`: 课程/幕名
- `title`: 当前概念名
- `children`: KnowledgeUnit 组件
- `progress?`: `{current: 3, total: 12}`

### 5.2 KnowledgeUnit

**职责**：在黑板上整体呈现一个概念的 6 个维度

```
┌──────────────────────────────────────────┐
│                                          │
│              矩 阵                       │ ← zhName (72px, bold)
│              Matrix                      │ ← enName (36px, dim)
│                                          │
│     ┌──────────────┐   ┌─────────┐       │
│     │              │   │ A_{m×n} │       │ ← formula (KaTeX)
│     │  ┌─┬─┬─┐     │   │         │       │
│     │  │1│2│3│     │   │ 矩阵定义│       │ ← formulaLabel
│     │  ├─┼─┼─┤     │   └─────────┘       │
│     │  │4│5│6│     │                     │
│     │  └─┴─┴─┘     │                     │ ← diagram (SVG)
│     └──────────────┘                     │
│                                          │
│    按行列排列的矩形数组                    │ ← explanation
│                                          │
└──────────────────────────────────────────┘
```

**动画时间线**（使用 Remotion `useCurrentFrame` + `interpolate`）：

| 阶段 | 相对时间 | 动画 |
|------|---------|------|
| ① zhName | 0-8f | 淡入 + scale(0.8→1) |
| ② enName | 5-13f | 从下方滑入 |
| ③ aliases | 10-18f | 淡入 |
| ④ diagram | 15-28f | scale(0→1) + 淡入 |
| ⑤ formula | 22-32f | 淡入 + scale(0.9→1) |
| ⑥ explanation | 28-36f | 从底部滑入 |
| ⑦ 全部停留 | 36-末 | 静止 |

（每帧 = 1/30 秒，所以 30f = 1 秒）

### 5.3 图解组件（diagrams/）

每个图解是一个纯 React SVG 组件，接收 `frame` 参数做动画。

设计原则：
- 纯 SVG，不依赖外部图片
- 200×200 到 300×300 视口
- 使用 THEME 颜色
- 可选内部动画（如向量延伸）

---

## 6. 数据流

```
knowledge-map/courses/linear-algebra/
    ├── _math.md          → 提取公式 (formula, formulaLabel)
    └── _concepts.md      → 提取术语 (zhName, enName, aliases, explanation)
            │
            ▼
video.data.ts (手写 or 脚本生成)
    {
      scenes: [
        { layout: 'blackboard', visuals: [{ block: 'KnowledgeUnit', data: {...} }] }
      ]
    }
            │
            ▼
VideoEngine → SceneRenderer → BlackboardLayout → KnowledgeUnit
            │
            ▼
        final.mp4
```

---

## 7. 不需要变更的组件

| 组件 | 原因 |
|------|------|
| `VideoEngine` | 已支持 Series 场景序列，不需要改 |
| `Subtitle` | 已有字幕组件，直接复用 |
| `SplitLayout` | 不改，KNN 等视频不受影响 |
| `video-theme.ts` | 配色复用 THEME，可能加一个 blackboard 色 |
| 现有所有积木 | 不改 |
