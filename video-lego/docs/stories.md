# Blackboard Flash Video — 任务分解

## Epic 1: 类型扩展（video-lego/src/lib/types.ts）

### Story 1.1: 新增 KnowledgeUnitData 类型
- 新增 `KnowledgeUnitData` 接口
- 扩展 `BlockDataMap` 注册 `KnowledgeUnit`
- 扩展 `LayoutType` 增加 `'blackboard'`
- **文件**: `video-lego/src/lib/types.ts`
- **工时**: 5 分钟

---

## Epic 2: BlackboardLayout 布局（video-lego/src/lib/layouts/）

### Story 2.1: 创建 BlackboardLayout 组件
- 全屏深色背景 + 噪点纹理
- 顶部课程标题栏（act + title + progress）
- 底部字幕安全区（140px）
- 居中渲染 children
- **文件**: `video-lego/src/lib/layouts/BlackboardLayout.tsx`
- **工时**: 30 分钟

---

## Epic 3: KnowledgeUnit 积木（video-lego/src/blocks/knowledge/）

### Story 3.1: KnowledgeUnit.view.tsx — 静态预览
- 排版：zhName(72px) → enName(36px) → aliases(24px) → diagram → formula → explanation
- 纯 CSS，无 Remotion 依赖
- **工时**: 20 分钟

### Story 3.2: KnowledgeUnit.motion.tsx — Remotion 动画
- 逐元素入场：6 步 stagger 动画
- 使用 useCurrentFrame + interpolate
- **工时**: 30 分钟

### Story 3.3: 桶导出 KnowledgeUnit.tsx
- **工时**: 2 分钟

---

## Epic 4: 图解组件（video-lego/src/blocks/knowledge/diagrams/）

### Story 4.1: 图解注册表 + 基础组件
- `DIAGRAM_REGISTRY`: 图解名 → React 组件映射
- 通用 SVG 容器
- **工时**: 10 分钟

### Story 4.2: 线性代数图解（6-8 个）
- MatrixDiagram: 网格数组
- LinearTransformDiagram: 网格变形
- EigenvalueDiagram: 向量拉伸
- DeterminantDiagram: 面积缩放
- OrthogonalDiagram: 90° 向量
- SVDDiagram: 旋转→缩放→旋转
- **工时**: 60 分钟

---

## Epic 5: 引擎集成（video-content）

### Story 5.1: SceneRenderer 新增 blackboard 分支
- `case 'blackboard': return <BlackboardLayout>...</BlackboardLayout>`
- **文件**: `video-content/src/lib/engine/SceneRenderer.tsx`
- **工时**: 10 分钟

### Story 5.2: 积木注册表更新
- 在 `BLOCK_REGISTRY` 中注册 `KnowledgeUnit`
- **文件**: `video-lego/src/blocks/index.ts`
- **工时**: 5 分钟

---

## Epic 6: 示例视频数据

### Story 6.1: MIT 线性代数 60s video.data.ts
- 12 个知识单元
- 60 秒时间轴
- 字幕文本
- **文件**: `video-content/src/videos/linear-algebra/flash/video.data.ts`
- **工时**: 30 分钟

### Story 6.2: Root.tsx 注册 Composition
- 注册 `linear-algebra-flash` composition
- **文件**: `video-content/src/Root.tsx`
- **工时**: 5 分钟

---

## 执行顺序

```
Story 1.1 (类型) → Story 2.1 (布局) → Story 3.1/3.2/3.3 (积木)
                                          ↓
                                    Story 4.1/4.2 (图解)
                                          ↓
                                    Story 5.1/5.2 (集成)
                                          ↓
                                    Story 6.1/6.2 (数据+注册)
                                          ↓
                                    预览验证
```

总工时估算：~3.5 小时
