# Phase 2: 脚本写作 (Script Writing)

## 概述

| 项 | 值 |
|----|---|
| **角色** | Script Writer |
| **技能** | ai-video-director |
| **前置条件** | Phase 1 完成，`content_brief.json` 存在 |
| **输出** | `script.json` + `script_tts.txt` |
| **预计时间** | 30-60 分钟 |

## 目标

将 `content_brief.json` 转化为分段视频脚本，遵循叙事结构理论，严格执行三条铁律。

## 🚨 三条铁律（违反任何一条 = 废稿重写）

### 铁律 1: 先定义后使用

- 每个专业名词必须**先用白话解释，再给专业名称**
- 使用 `content_brief.json` 的 `term_dependency_graph` 确定出场顺序
- 示例：✅ "一个小窗口在图片上滑动做加权求和——这叫**卷积核**"
- 反例：❌ "卷积核在特征图上做卷积运算" （三个名词都没定义）

### 铁律 2: 来源标注

- script.json 中每个 segment 必须标注 `source_file` 和 `source_section`
- 标注示例：`"source": "pitfalls.md § 痛点#5"`

### 铁律 3: 无未定义名词

- 脚本中出现的每个专业名词必须在 `term_dependency_graph` 中
- 运行检查脚本验证：扫描全文，找出不在依赖图中的名词

## 叙事结构

### 开场策略选择（Phase 1 决定）

> ⚠️ **先判断受众再定开场**。不是所有视频都适合痛点 Hook。

| 模式 | 适用场景 | 第一幕内容 | 理论依据 |
|------|---------|-----------|---------|
| **模式 A: 痛点 Hook** | 受众已知主题（课程学生、进阶者） | 说出挫败感 + Pitfalls 真实错误 | Heath《Made to Stick》Ch.2 "Unexpected" |
| **模式 B: 故事 Hook** | 受众不知主题（科普、入门） | 历史故事切入 + 一句话讲清是什么 | McKee《Story》Part 2 "Inciting Incident" |

**判断标准**：如果观众还不知道这个主题的名字，用模式 B；如果观众正在学这个主题且被困住了，用模式 A。

### 五幕结构（来源：McKee + Snyder）

| 幕 | 时间 | 模式 A（痛点开场） | 模式 B（故事开场） | 来源维度 |
|----|------|-------------------|-------------------|---------|
| **① 开场** | 0:00-1:00 | 痛点共鸣：说出挫败感 | 故事切入：历史+一句话定义 | A: pitfalls / B: history+concepts |
| **② 人话翻译** | 1:00-2:00 | 白话讲核心概念 | 白话讲核心概念 | concepts |
| **③ 核心逻辑** | 2:00-3:15 | 原理+公式口语化 | 原理+公式口语化 | first_principles+tutorial+math |
| **④ 避坑指南** | 3:15-4:15 | 常见错误+公理失效 | 常见错误+公理失效 | pitfalls+first_principles |
| **⑤ 收尾** | 4:15-5:00 | 历史演进+下集预告 | 技术演进+下集预告 | A: history+bridge / B: history(续)+bridge |

### SUCCESs 检查（来源：Heath《Made to Stick》）

每幕写完后检查：

- [ ] **S**imple: 核心信息能用一句话说清吗？
- [ ] **U**nexpected: 有没有打破预期的"啊哈时刻"？
- [ ] **C**oncrete: 用了具体例子而非抽象概念？
- [ ] **C**redible: 有教科书/论文来源支撑？
- [ ] **E**motional: 能引起观众情感共鸣（挫败感→成就感）？
- [ ] **S**tory: 有因果链而非单纯罗列？

## 输出格式

### script.json

```json
{
  "topic": "conv_layer",
  "course": "deep-learning",
  "total_duration_seconds": 300,
  "structure": "five_act",
  "segments": [
    {
      "id": "act1_pain",
      "act": 1,
      "act_name": "痛点共鸣",
      "start_time": "0:00",
      "end_time": "0:30",
      "narration": "学卷积层，最让人崩溃的是什么？名词太多了。...",
      "visual_cue": "大字'卷积层' → 名词雨动画 → 崩溃表情",
      "source": {
        "file": "pitfalls.md",
        "section": "§ 痛点 #5: 名词太多"
      },
      "terms_introduced": [],
      "terms_used": []
    },
    {
      "id": "act2_explain",
      "act": 2,
      "act_name": "人话翻译",
      "start_time": "0:30",
      "end_time": "1:30",
      "narration": "但我告诉你，卷积层的核心逻辑一句话就能说清...",
      "visual_cue": "小窗口滑动动画 → 加权求和可视化",
      "source": {
        "file": "concepts.md",
        "section": "§ 卷积操作"
      },
      "terms_introduced": ["卷积核", "卷积操作"],
      "terms_used": []
    }
  ]
}
```

### script_tts.txt（TTS 专用纯文本）

- 去掉所有注释行和视觉提示
- `3×3` → `3乘3`
- `$C_{in}$` → `输入通道数`
- 每行一个段落

## 完成检查

- [ ] `script.json` 合法 JSON
- [ ] 每个 segment 有 `source.file` 和 `source.section`
- [ ] `terms_introduced` 中每个名词在首次出现时已白话解释
- [ ] `terms_used` 中每个名词在之前的某个 segment 的 `terms_introduced` 中
- [ ] 五幕时长分配合理（痛点≤30s，人话≤60s，核心≤105s，避坑≤60s，历史≤45s）
- [ ] SUCCESs 六项检查全通过
- [ ] `script_tts.txt` 不含注释、LaTeX、乘号等 TTS 不友好字符

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- McKee《Story》Part 2: "The Elements of Story" — 五幕叙事结构、因果链
  - MinerU: `data/mineru_output/mckee_story/mckee_story/auto/mckee_story.md`
- Snyder《Save the Cat》Ch.2: "Give Me the Same Thing Only Different" — 15 Beat Sheet
  - MinerU: `data/mineru_output/snyder_save_the_cat/snyder_save_the_cat/auto/snyder_save_the_cat.md`
- Heath《Made to Stick》全书: SUCCESs 框架
  - MinerU: `data/mineru_output/heath_made_to_stick/heath_made_to_stick/hybrid_auto/heath_made_to_stick.md`
- Clark & Mayer《e-Learning and the Science of Instruction》3rd Ed., Ch.8 "Applying the Coherence Principle: Adding Material Can Hurt Learning", **p.151-172** — 删除无关内容（"Avoid e-Lessons with Extraneous Words", p.166）
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Clark & Mayer, Ch.10 "Applying the Segmenting and Pretraining Principles", **p.205-218** — 结构化提示与分段
- Mayer《Multimedia Learning》3rd Ed. — Coherence + Signaling Principle
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`


## 参考实现

- `ai-video-generation-workflow` 的 `generate-script.ts`: 结构化分段脚本生成
- 我们已有的 `generate-knowledge-map.md` 工作流 § 6.1: 旁白稿生成规则
