# Phase 4: 素材制作 (Asset Creation)

## 概述

| 项 | 值 |
|----|---|
| **角色** | Animator |
| **技能** | Remotion, 动画原则 |
| **前置条件** | Phase 3 完成，`storyboard.md` 存在 |
| **输出** | `assets/` 目录（Remotion 组件 + 静态资源） |
| **预计时间** | 1-3 小时 |
| **可并行** | 与 Phase 5 (语音合成) 并行 |

## 目标

根据 `storyboard.md` 的视觉描述，为每个场景创建 Remotion 动画组件或静态素材。

## 动画设计原则

### 来源：Williams《Animator's Survival Kit》

| 原则 | 解释 | 在教育视频中的应用 |
|------|------|-------------------|
| **Timing** | 动画时长决定感受 | 快 = 轻快简单，慢 = 重要强调 |
| **Ease In/Out** | 缓入缓出比匀速自然 | 所有出现/消失动画用 easing |
| **Staging** | 一次只呈现一个重点 | 每帧一个视觉焦点 |
| **Anticipation** | 大动作前先有小暗示 | 关键概念出现前先闪烁/高亮 |

### Remotion 组件模板

为常见场景类型维护可复用模板：

```
assets/templates/
├── TextReveal.tsx        # 文字逐字/逐行出现
├── DiagramBuilder.tsx    # 结构图逐步构建
├── StepByStep.tsx        # 计算过程分步展示
├── ComparisonSplit.tsx   # ✅/❌ 分屏对比
├── TimelineFly.tsx       # 时间线推进动画
├── CodeHighlight.tsx     # 代码逐行高亮
├── FormulaExpand.tsx     # 公式渐进展开
└── TransitionWipe.tsx    # 场景切换过渡
```

## 执行步骤

### 1. 解析 storyboard.md

读取每个场景的视觉描述和动画类型。

### 2. 选择或创建组件

- 匹配已有模板 → 直接复用，传入数据参数
- 无匹配模板 → 创建新组件，完成后归入模板库

### 3. 构建场景数据

每个场景一个子目录：

```
assets/
├── scene_01/
│   ├── Scene01.tsx       # Remotion 组件
│   ├── data.json         # 场景数据（文字、颜色、位置）
│   └── images/           # 静态图片素材（如有）
├── scene_02/
│   └── ...
└── composition.tsx       # 总组合文件
```

### 4. 本地预览

```bash
npx remotion preview assets/composition.tsx
```

验证每个场景动画效果。

## 完成检查

- [ ] 每个 `storyboard.md` 中的场景都有对应的 `assets/scene_XX/` 目录
- [ ] 每个组件可独立预览无报错
- [ ] 动画时长与 `storyboard.md` 标注的 `duration_seconds` 匹配
- [ ] 每帧只有一个视觉焦点（Staging 原则）
- [ ] 文字与图形邻近（Mayer 空间邻近）
- [ ] 无无关装饰元素（Mayer 连贯原则）

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- Williams《Animator's Survival Kit》: Timing, Ease In/Out, Staging, Anticipation
  - MinerU: `data/mineru_output/williams_animators_survival_kit/williams_animators_survival_kit/auto/williams_animators_survival_kit.md`
- Williams《Non-Designer's Design Book》: CRAP 原则应用于每帧布局
  - MinerU: `data/mineru_output/williams_non_designers_design_book/williams_non_designers_design_book/auto/williams_non_designers_design_book.md`
- Mayer《Multimedia Learning》Ch.13: "Coherence Principle" — 删除装饰性视觉
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`
- Knaflic《Storytelling with Data》Ch.4: "Focus your audience's attention"
  - MinerU: `data/mineru_output/knaflic_storytelling_with_data/knaflic_storytelling_with_data/auto/knaflic_storytelling_with_data.md`


## 参考实现

- `short-video-maker` 的 `src/components/`: Remotion 组件架构
- `short-video-maker` 的 `remotion.config.ts`: Remotion 项目配置
