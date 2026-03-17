# Phase 12: 视频创作 (Video) — 可选

## 概述

| 项 | 值 |
|----|---|
| **角色** | Video Director |
| **前置条件** | Phase 11（Finalize）完成 + `--video` 参数 |
| **输出** | `video-content/{course}/{topic}/` 完整项目 |
| **执行方式** | **委托给 `video-production` 工作流** |
| **跳过条件** | 无 `--video` 参数 / 素材不足（至少需 3 个维度） |

## 本阶段的职责

> ⚠️ **本阶段不直接制作视频。** 它的职责是：
> 1. 从知识地图 9 维文件中确定素材映射关系
> 2. 启动 `video-production` 工作流（`/video-prod`）
> 3. 完成后回填标注到 `{topic}_map.md`

## 设计理论依据

| 章节 | 设计决策 | 教科书依据 |
|------|---------|-----------|
| 全局 | 知识地图 9 维 = 视频多源素材库 | 不重新写内容，只从已有维度提取+重组+风格化 |
| 开场策略 | **受众已知主题 → 痛点 Hook；受众不知主题 → 故事 Hook** | Heath Ch.2 "Unexpected"（痛点）/ McKee Part 2（故事） |
| 五幕结构 | 开场→人话→逻辑→避坑→收尾 | McKee《Story》Part 2 — 叙事结构：冲突→对抗→高潮 |
| 多媒体原则 | 语音 > 屏幕文字 | Mayer《Multimedia Learning》Ch.20 "Modality Principle" |
| 分段原则 | 1 段旁白 = 1 个场景 | Clark & Mayer《e-Learning》Ch.10 "Segmenting Principle" |

---

## 知识地图 → 视频的素材映射

> 这是本阶段的核心产出：告诉 `video-production` 从哪里取素材。

| 视频幕 | 内容来源（知识地图维度） | 提取什么 |
|--------|-----------------------|---------|
| 🎣 Hook（痛点共鸣） | `references/pain_points.md` + `{topic}_pitfalls.md` | 学这个最崩溃的是什么？ |
| 🗣️ 人话翻译 | `{topic}_concepts.md` | 核心术语的白话定义 + 生活类比 |
| 🧠 核心逻辑 | `{topic}_tutorial.md` + `{topic}_math.md` + `{topic}_first_principles.md` | 为什么要这样？公理→推导 |
| ⚠️ 避坑指南 | `{topic}_pitfalls.md` + `{topic}_first_principles.md`（公理失效） | ❌/✅ 对比 + "公理不成立会怎样" |
| 📜 来龙去脉 | `{topic}_history.md` | 谁发明？为什么？解决什么？ |
| 🔗 一句话收尾 | `{topic}_map.md` + `{topic}_bridge.md` | 和什么有关？下一步学什么？ |

---

## 执行步骤

### Step 1: 确认知识地图完整度

检查 `{topic}_map.md` 的缺口检查表，确保至少有 3 个维度已完成（至少需要 Concepts + Tutorial + Pitfalls）。

### Step 2: 启动 video-production 工作流

```
/video-prod --course {course} --topic {topic}
```

> 📋 **完整流程见**：[`.agent/workflows/video-production/workflow.md`](../../video-production/workflow.md)
>
> video-production 工作流包含 9 个阶段：
> 1. Phase 0: 初始化 → `.video-state.yaml`
> 2. Phase 1: 内容提取 → `content_brief.json`（从知识地图维度提取）
> 3. Phase 2: 脚本写作 → `script.json`（五幕结构 + 铁律检查）
> 4. Phase 3: 分镜设计 → `storyboard.json`
> 5. Phase 4: 素材制作 → `assets/`（Remotion 动画）
> 6. Phase 5: 语音合成 → `narration/`（Qwen3-TTS）
> 7. Phase 6: 字幕生成 → `captions.json`
> 8. Phase 7: 组装渲染 → `final.mp4`
> 9. Phase 8: 质量审查 → `review_report.md`

### Step 3: 回填标注

video-production 完成后，回填到知识地图：

1. 在 `{topic}_map.md` 的文件地图表中追加：`🎬 已生成视频`
2. 在课程 `README.md` 中标注主题已有视频内容

---

## 两条铁律（由 video-production 执行检查）

**铁律 1: 先定义后使用**
> 使用未定义名词 = 和那些只甩名词不讲逻辑的烂老师犯一模一样的错。

**铁律 2: 每段旁白必须有来源**
> 格式：`# 来源: <主题>_<维度>.md — Section <名称>`

---

## 完成检查

- [ ] 知识地图至少 3 个维度已完成
- [ ] `video-production` 工作流 Phase 8 (review) 通过
- [ ] `{topic}_map.md` 已标注 `🎬 已生成视频`
- [ ] 课程 `README.md` 已更新

---

## 教科书来源

> 详细引用和 MinerU 路径见 [`video-production/workflow.md`](../../video-production/workflow.md) 的教科书表。

- McKee《Story》(1997), Part 2
- Heath《Made to Stick》(2007), Ch.1 "Simple", Ch.2 "Unexpected"
- Mayer《Multimedia Learning》3rd Ed. (2020), Ch.5, Ch.12, Ch.20
- Clark & Mayer《e-Learning》3rd Ed. (2011), Ch.6, Ch.8, Ch.10
- Snyder《Save the Cat》(2005), Ch.2 "15 Beat Sheet"
