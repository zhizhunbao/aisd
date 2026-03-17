# KNN 视频素材清单 (Assets Manifest)

> **来源**: `storyboard.md` (20 场景)
> **渲染引擎**: Remotion
> **配色**: 背景 #1a1a2e | 金色 #ffd700 | 蓝色 #4ea8de | 红色 #e74c3c | 灰色 #888 | 白色 #f0f0f0

---

## 场景 → 组件映射

| Scene | 分镜类型 | 模板组件 | 自定义数据 | 时长 |
|-------|---------|---------|-----------|------|
| 01 | text_animation | TextReveal | "1951" + 军事背景 | 8s |
| 02 | diagram | DiagramBuilder | 2D 散点 + 查询点 + 箭头 | 10s |
| 03 | formula | FormulaExpand | 勾股定理 → 欧氏距离 | 8s |
| 04 | text_animation | TextReveal | 文件淡出 + 问号 | 4s |
| 05 | timeline + formula | TimelineFly + FormulaExpand | 1951→1967 + Cover-Hart | 15s |
| 06 | diagram | DiagramBuilder | 教室投票动画 | 10s |
| 07 | comparison | ComparisonSplit | k=1 vs k=100 决策边界 | 15s |
| 08 | diagram | DiagramBuilder | 偏差-方差 U 形曲线 | 12s |
| 09 | step_by_step | StepByStep | 训练 0.1s vs 预测 600s | 15s |
| 10 | diagram | DiagramBuilder | 散点聚类 + 邻域搜索 | 15s |
| 11 | comparison | ComparisonSplit | 正确距离 vs 歪距离 | 15s |
| 12 | step_by_step | StepByStep | 5点→50点→500点 | 12s |
| 13 | diagram | DiagramBuilder | 三公理汇聚 | 15s |
| 14 | comparison + code | ComparisonSplit + CodeHighlight | ❌/✅ 归一化代码 | 20s |
| 15 | step_by_step | StepByStep | 2D→10D→100D 距离趋同 | 20s |
| 16 | diagram | DiagramBuilder | PCA + 余弦距离 | 12s |
| 17 | timeline + diagram | TimelineFly + DiagramBuilder | 暴力→KD-Tree | 10s |
| 18 | timeline | TimelineFly | LSH→FAISS 演进 | 12s |
| 19 | diagram | DiagramBuilder | RAG 架构图 | 12s |
| 20 | text_animation | TextReveal | "下期 LOF" + 关注 | 8s |

---

## 模板使用统计

| 模板 | 使用次数 | 场景 |
|------|---------|------|
| DiagramBuilder | 8 | 02,06,08,10,13,16,17,19 |
| TextReveal | 3 | 01,04,20 |
| ComparisonSplit | 4 | 07,11,14 (含 CodeHighlight) |
| StepByStep | 3 | 09,12,15 |
| TimelineFly | 3 | 05,17,18 |
| FormulaExpand | 2 | 03,05 |
| CodeHighlight | 1 | 14 (组合使用) |

---

## 静态素材需求

| 素材 | 类型 | 来源 | 用于 Scene |
|------|------|------|-----------|
| Fix & Hodges 人物卡片 | 文字卡片（无照片） | 自制 | 02 |
| Cover & Hart 人物卡片 | 文字卡片 | 自制 | 05 |
| Bentley 人物卡片 | 文字卡片 | 自制 | 17 |
| Cover-Hart 论文封面 | 截图 | Wikipedia/Google Scholar | 05 |

> ⚠️ 人物无公开照片可用，统一用文字卡片（姓名+年份+贡献），避免 AI 生成图片。

---

## Remotion 项目结构（待创建）

```
assets/
├── src/
│   ├── Root.tsx                    # Remotion 入口
│   ├── KnnVideo.tsx                # 主 Composition
│   ├── theme.ts                    # 配色方案 + 字体
│   ├── components/                 # 可复用模板
│   │   ├── TextReveal.tsx
│   │   ├── DiagramBuilder.tsx
│   │   ├── ComparisonSplit.tsx
│   │   ├── StepByStep.tsx
│   │   ├── TimelineFly.tsx
│   │   ├── FormulaExpand.tsx
│   │   └── CodeHighlight.tsx
│   └── scenes/                     # 每个场景实例
│       ├── Scene01_YearFlash.tsx
│       ├── Scene02_FindNearest.tsx
│       ├── Scene03_EuclideanDist.tsx
│       ├── ...
│       └── Scene20_NextEpisode.tsx
├── public/
│   └── photos/                     # 静态素材
└── remotion.config.ts              # 渲染配置
```

---

## 下一步操作

### 初始化 Remotion 项目
```bash
cd video-content/machine-learning/knn
npx create-video@latest ./assets
```

### 本地预览
```bash
cd assets
npx remotion preview src/Root.tsx
```

### 渲染单场景
```bash
npx remotion render src/Root.tsx Scene01 --output ../output/scene_01.mp4
```

### 渲染全部
```bash
npx remotion render src/Root.tsx KnnVideo --output ../output/knn_full.mp4
```
