# Phase 3: 分镜设计 (Storyboard)

## 概述

| 项 | 值 |
|----|---|
| **角色** | Visual Designer |
| **技能** | CRAP 设计原则, Mayer 空间/时间邻近原则 |
| **前置条件** | Phase 2 完成，`script.json` 存在 |
| **输出** | `storyboard.json` |
| **预计时间** | 30-45 分钟 |

## 目标

将 `script.json` 的每个 segment 转化为具体的视觉描述，定义每个场景的动画类型、布局和转场。

## 设计原则

### Mayer 多媒体原则（来源：Mayer《Multimedia Learning》）

| 原则 | 规则 | 分镜中如何体现 |
|------|------|---------------|
| **空间邻近** | 文字和对应的图形放在一起 | 标注文字紧贴对应元素 |
| **时间邻近** | 解说和动画同步呈现 | 动画时长 = 旁白时长 |
| **冗余** | 不要同时显示旁白文字+语音 | 只显示关键词，不显示整句旁白 |
| **连贯** | 删除无关装饰 | 每帧只有一个视觉焦点 |
| **信号** | 用高亮/箭头引导注意力 | 关键元素用色彩/动画突出 |
| **分段** | 复杂内容分成小步骤 | 每个 segment ≤ 15 秒一个概念 |
| **预训练** | 先介绍关键词再讲原理 | 名词卡片先出现 |
| **模态** | 动画+语音 > 动画+文字 | 用旁白而非屏幕文字解释 |

### CRAP 原则（来源：Williams《Non-Designer's Design Book》）

- **C**ontrast: 关键元素与背景有足够对比度
- **R**epetition: 同类元素用一致的颜色/形状
- **A**lignment: 所有元素对齐到网格
- **P**roximity: 相关元素放在一起，无关元素拉开距离

## 输出格式

### storyboard.json

```json
{
  "scenes": [
    {
      "id": "scene_01",
      "segment_id": "act1_pain",
      "duration_seconds": 5,
      "type": "text_animation",
      "description": "大字'卷积层'居中，然后名词雨从上方落下",
      "layout": {
        "canvas": "16:9",
        "safe_zone": { "subtitle_y_min": -2.3 },
        "elements": [
          {
            "type": "title",
            "text": "卷积层",
            "position": "center",
            "animation": "fade_in → scale_up"
          },
          {
            "type": "word_rain",
            "words": ["卷积核", "特征图", "步长", "填充", "感受野"],
            "animation": "rain_down",
            "delay": 1.5
          }
        ]
      },
      "transition_to_next": "dissolve",
      "design_notes": "Mayer 连贯原则: 背景纯色，不加装饰"
    }
  ]
}
```

## 场景类型库

| 类型 | 描述 | 适用场景 | 工具 |
|------|------|---------|------|
| `text_animation` | 文字出现/消失动画 | 标题、关键词 | Remotion |
| `diagram` | 结构图/流程图 | 概念关系 | Remotion |
| `step_by_step` | 逐步展示计算过程 | 卷积操作演示 | Remotion |
| `comparison` | 分屏对比 | ✅/❌ 避坑 | Remotion |
| `timeline` | 时间线动画 | 历史演进 | Remotion |
| `code_walkthrough` | 代码高亮+注释 | 代码演示 | Remotion |
| `formula` | 公式渐进展开 | 数学推导 | Remotion + LaTeX |

## 完成检查

- [ ] `storyboard.json` 合法 JSON
- [ ] 每个 scene 有 `segment_id` 关联到 `script.json`
- [ ] 每个 scene 有 `duration_seconds`
- [ ] 所有 scene 时长之和 ≈ `script.json` 总时长
- [ ] 每帧只有一个视觉焦点（Mayer 连贯原则）
- [ ] 文字标注与图形邻近（Mayer 空间邻近原则）
- [ ] 无全屏旁白文字（Mayer 冗余原则）

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- Clark & Mayer《e-Learning and the Science of Instruction》3rd Ed.:
  - Ch.5 "Applying the Contiguity Principle: Align Words to Corresponding Graphics", **p.91-110** — 空间邻近
  - Ch.6 "Applying the Modality Principle: Present Words as Audio Narration Rather Than On-Screen Text", **p.115-129** — 模态原则
  - Ch.7 "Applying the Redundancy Principle: Explain Visuals with Words in Audio OR Text: Not Both", **p.133-146** — 冗余原则
  - Ch.8 "Applying the Coherence Principle: Adding Material Can Hurt Learning", **p.151-172** — 连贯原则
  - Ch.10 "Applying the Segmenting and Pretraining Principles", **p.205-218** — 分段+预训练
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Williams《Non-Designer's Design Book》: CRAP 四原则
  - MinerU: `data/mineru_output/williams_non_designers_design_book/williams_non_designers_design_book/auto/williams_non_designers_design_book.md`
- Knaflic《Storytelling with Data》Ch.3: "Clutter is your enemy" — 去除视觉杂讯
  - MinerU: `data/mineru_output/knaflic_storytelling_with_data/knaflic_storytelling_with_data/auto/knaflic_storytelling_with_data.md`
- Williams《Animator's Survival Kit》Ch.1: "Timing" — 动画时长控制
  - MinerU: `data/mineru_output/williams_animators_survival_kit/williams_animators_survival_kit/auto/williams_animators_survival_kit.md`


## 参考实现

- `short-video-maker` 的 `Scene` 类型: 每个场景有 text + searchTerms + captions
- `ai-video-generation-workflow` 的 `plan.ts`: shot plan 结构化设计
