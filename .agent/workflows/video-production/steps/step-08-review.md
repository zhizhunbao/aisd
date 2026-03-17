# Phase 8: 质量审查 (Quality Review)

## 概述

| 项 | 值 |
|----|---|
| **角色** | QA Reviewer |
| **技能** | Mayer 原则, CRAP 原则 |
| **前置条件** | Phase 7 完成，`final.mp4` 存在 |
| **输出** | `review_report.md` |
| **预计时间** | 15-30 分钟 |

## 目标

系统性审查成片，确保符合教学设计理论和铁律要求。这不是"感觉审"，而是逐条对照检查清单打分。

## 审查清单

### 一、铁律检查（一票否决）

| # | 检查项 | 通过/不通过 |
|---|--------|-----------|
| 1 | 所有专业名词在首次使用前已有白话解释 | |
| 2 | 每段旁白可以追溯到知识地图的具体维度和 section | |
| 3 | 无未定义名词出现 | |

> ❌ 任何一项不通过 → 回到 Phase 2 重写脚本

### 二、Mayer 多媒体学习原则检查（来源：Mayer《Multimedia Learning》）

| # | 原则 | 检查内容 | 分数 (1-5) |
|---|------|---------|-----------|
| 1 | **多媒体** | 同时用图形+语音解释，而非纯语音 | |
| 2 | **连贯** | 无无关装饰/音效/动画 | |
| 3 | **信号** | 关键概念有视觉高亮/箭头指引 | |
| 4 | **冗余** | 不同时显示完整旁白文字+播放语音 | |
| 5 | **空间邻近** | 文字标注紧贴对应图形 | |
| 6 | **时间邻近** | 旁白与对应动画同步播放 | |
| 7 | **分段** | 复杂内容被分成小步骤 | |
| 8 | **预训练** | 关键名词先单独介绍再用 | |
| 9 | **模态** | 用语音而非屏幕文字解释图形 | |
| 10 | **个性化** | 用对话式语气而非学术语气 | |

> 评分标准: 1=完全违反, 3=基本符合, 5=优秀示范
> 平均分 < 3 → 需要修改

### 三、SUCCESs 粘性检查（来源：Heath《Made to Stick》）

| 维度 | 问题 | 是/否 |
|------|------|------|
| **Simple** | 核心信息能用一句话说清？ | |
| **Unexpected** | 有打破预期的"啊哈时刻"？ | |
| **Concrete** | 用了具体例子而非抽象概念？ | |
| **Credible** | 内容有教科书/论文来源？ | |
| **Emotional** | 能引起观众情感共鸣？ | |
| **Story** | 有因果链而非单纯罗列？ | |

### 四、技术质量检查

| # | 检查项 | 通过/不通过 |
|---|--------|-----------|
| 1 | 视频分辨率 = 1920×1080 | |
| 2 | 帧率 = 30fps, 无掉帧 | |
| 3 | 音频清晰, BGM 不干扰旁白 | |
| 4 | 字幕与语音同步 (误差 < 0.3s) | |
| 5 | 无黑屏/空白帧/渲染错误 | |
| 6 | 总时长在目标范围 ±15% 内 | |

### 五、CRAP 视觉设计检查（来源：Williams《Non-Designer's Design Book》）

| 原则 | 检查内容 | 分数 (1-5) |
|------|---------|-----------|
| **Contrast** | 关键元素与背景对比度足够 | |
| **Repetition** | 同类元素样式一致 | |
| **Alignment** | 所有元素对齐到网格 | |
| **Proximity** | 相关元素靠近、无关元素分开 | |

## 输出格式

### review_report.md

```markdown
# 视频质量审查报告

## 基本信息
- 主题: {topic}
- 课程: {course}
- 审查日期: {date}
- 审查人: {reviewer}

## 铁律检查: ✅ 全部通过 / ❌ 需要修改

## Mayer 原则评分
| 原则 | 分数 |
|------|------|
| 多媒体 | 4/5 |
| 连贯 | 5/5 |
| ... | ... |
| **平均** | **4.2/5** |

## SUCCESs 检查: 5/6 通过
- ❌ Unexpected: 缺少"啊哈时刻"，建议在第三幕加入...

## 技术质量: ✅ 全部通过

## CRAP 评分: 4.0/5

## 修改建议
1. ...
2. ...

## 最终结论: ✅ 可发布 / ⚠️ 需修改后重审
```

## 审查流程

```
观看完整视频
    ↓
铁律检查（一票否决）
    ↓ 通过
Mayer 原则逐条打分
    ↓
SUCCESs 粘性检查
    ↓
技术质量检查
    ↓
CRAP 视觉检查
    ↓
生成 review_report.md
    ↓
结论: 可发布 / 需修改
```

## 完成检查

- [ ] `review_report.md` 存在且完整
- [ ] 铁律检查全部通过（否则不继续）
- [ ] Mayer 原则平均分 ≥ 3.0
- [ ] SUCCESs 检查 ≥ 4/6 通过
- [ ] 技术质量全部通过
- [ ] CRAP 评分 ≥ 3.0
- [ ] 最终结论为"可发布"或已完成修改

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- Clark & Mayer《e-Learning and the Science of Instruction》3rd Ed.:
  - Ch.1 "e-Learning: Promise and Pitfalls", **p.7-27** — 有效 e-Learning 概述
  - Ch.4 "Applying the Multimedia Principle", **p.67-86** — 多媒体原则
  - Ch.5 "Applying the Contiguity Principle", **p.91-110** — 空间/时间邻近
  - Ch.6 "Applying the Modality Principle", **p.115-129** — 模态原则
  - Ch.7 "Applying the Redundancy Principle", **p.133-146** — 冗余原则
  - Ch.8 "Applying the Coherence Principle", **p.151-172** — 连贯原则
  - Ch.9 "Applying the Personalization Principle", **p.179-201** — 个性化原则
  - Ch.10 "Applying the Segmenting and Pretraining Principles", **p.205-218** — 分段+预训练
  - Ch.17 "Applying the Guidelines", **p.401-424** — 综合检查清单
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Mayer《Multimedia Learning》3rd Ed. — 12 条多媒体学习原则
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`
- Heath《Made to Stick》全书: SUCCESs 粘性框架
  - MinerU: `data/mineru_output/heath_made_to_stick/heath_made_to_stick/hybrid_auto/heath_made_to_stick.md`
- Williams《Non-Designer's Design Book》全书: CRAP 四原则
  - MinerU: `data/mineru_output/williams_non_designers_design_book/williams_non_designers_design_book/auto/williams_non_designers_design_book.md`

