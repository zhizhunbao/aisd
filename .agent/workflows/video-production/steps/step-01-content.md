# Phase 1: 内容提取 (Content Extraction)

## 概述

| 项 | 值 |
|----|---|
| **角色** | Content Researcher |
| **技能** | knowledge-map-format, learning-source-citation |
| **前置条件** | Phase 0 完成，知识地图验证通过 |
| **输出** | `content_brief.json` |
| **预计时间** | 15-30 分钟 |

## 目标

从 9 维知识地图中提取视频所需的核心内容，进行**压缩和筛选**——不是全部搬运，而是根据目标痛点选择最有效的内容子集。

## 执行步骤

### 1. 读取知识地图

加载以下维度文件并标记每段来源：

| 维度 | 文件 | 提取内容 |
|------|------|---------|
| ① Map | `{topic}_map.md` | 主题在知识体系中的位置、前置/后续关系 |
| ② Concepts | `{topic}_concepts.md` | 核心概念定义（白话版 + 术语） |
| ③ Math | `{topic}_math.md` | 关键公式（需口语化） |
| ④ Tutorial | `{topic}_tutorial.md` | 操作步骤、代码示例 |
| ⑤ Code | `{topic}_code.md` | 实现细节 |
| ⑥ Pitfalls | `{topic}_pitfalls.md` | 常见错误+为什么错 |
| ⑦ History | `{topic}_history.md` | 发明故事、演进时间线 |
| ⑧ Bridge | `{topic}_bridge.md` | 与前后主题的衔接 |
| ⑨ First Principles | `{topic}_first_principles.md` | 公理、为什么必须这样设计 |

### 2. 开场模式选择

在痛点聚焦之前，先判断受众：

| 问题 | 回答 | 模式 |
|------|------|------|
| 目标观众是否已知道本主题的名字和基本概念？ | 是（课程学生、进阶者） | **模式 A: 痛点 Hook** |
| 目标观众是否可能第一次接触本主题？ | 是（科普、入门） | **模式 B: 故事 Hook** |

将选择记入 `.video-state.yaml` 的 `config.opening_mode: A` 或 `B`。

### 3. 痛点聚焦

根据 Phase 0 选定的痛点，筛选内容：

- **痛点相关内容** → 保留，标记为 `priority: high`
- **理解痛点需要的前置知识** → 保留，标记为 `priority: medium`
- **与痛点无关的高级内容** → 排除

### 4. 构建名词依赖图

提取所有专业名词，构建**依赖关系**：

```json
{
  "terms": {
    "卷积核": {
      "depends_on": [],
      "definition": "一个小窗口，在图片上滑动做加权求和",
      "source": "concepts.md § 核心概念"
    },
    "特征图": {
      "depends_on": ["卷积核"],
      "definition": "卷积核扫完整张图后输出的新图",
      "source": "concepts.md § 输出"
    },
    "感受野": {
      "depends_on": ["卷积核", "特征图"],
      "definition": "输出上一个点能'看到'的输入区域大小",
      "source": "concepts.md § 感受野"
    }
  }
}
```

> 🚨 **铁律检查**: 如果名词 A 依赖名词 B，B 必须在 A 之前出现。
> 这是脚本写作的硬约束，在此阶段提前建好。

### 5. 生成 content_brief.md

```json
{
  "topic": "conv_layer",
  "course": "deep-learning",
  "target_pain_points": ["#5 名词太多", "#7 越学越怀疑自己"],
  "target_duration_minutes": 5,
  "term_dependency_graph": { ... },
  "content_blocks": [
    {
      "id": "pain_hook",
      "type": "pain_point",
      "source_file": "pitfalls.md",
      "source_section": "§ 痛点 #5",
      "content": "学卷积层最崩溃的是名词太多...",
      "priority": "high"
    },
    {
      "id": "core_concept",
      "type": "concept",
      "source_file": "concepts.md",
      "source_section": "§ 卷积操作",
      "content": "一个小窗口在图片上滑动...",
      "priority": "high"
    }
  ]
}
```

## 完成检查

- [ ] `content_brief.json` 存在且合法 JSON
- [ ] 每个 `content_block` 都有 `source_file` 和 `source_section`
- [ ] 名词依赖图完整，无循环依赖
- [ ] 核心概念不超过 7±2 个 (Miller's Law)

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- Clark & Mayer《e-Learning and the Science of Instruction》3rd Ed., Ch.4 "Applying the Multimedia Principle: Use Words and Graphics Rather Than Words Alone", **p.67-86** — 内容选择与压缩（"Include Both Words and Graphics", p.70）
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Clark & Mayer, Ch.10 "Applying the Segmenting and Pretraining Principles: Managing Complexity by Breaking a Lesson into Parts", **p.205-218** — 分段策略与预训练（"Ensure That Learners Know the Names and Characteristics of Key Concepts", p.212）
- Heath《Made to Stick》Ch.1: "Simple" — 找到核心信息
  - MinerU: `data/mineru_output/heath_made_to_stick/heath_made_to_stick/hybrid_auto/heath_made_to_stick.md`
- Mayer《Multimedia Learning》3rd Ed. — 认知负荷限制 → 内容量控制
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`


## 参考实现

- `ai-video-generation-workflow` 的 `plan.ts`: 从 topic 文件生成 shot plan
- `video-creator` 的 `TextModel.generate_content()`: 内容生成步骤
