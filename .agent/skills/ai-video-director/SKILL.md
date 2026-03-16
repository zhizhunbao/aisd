---
name: ai-video-director
description: AI Video Director skill for creating educational videos from knowledge map files. Use when (1) creating video narration scripts in 4 styles (袁腾飞/老高/罗翔/精简), (2) generating TTS audio with voice cloning, (3) assembling videos with auto-subtitles, (4) user says "视频" or "video" with knowledge map topics.
---

# 🎬 AI 视频编导 Skill

> 角色定义见 `knowledge-map/README.md` 第 22 号角色。

## 定位

**一句话**：把知识地图里的 History 文件变成 3-5 分钟教育视频。

**核心原则**：**History 文件 = 视频的 Single Source of Truth**，不重写内容，只做风格适配。

**工具链**：Claude 风格化润色 → Qwen3-TTS 配音 → Remotion 动画 → FFmpeg 组装

## 四种叙事风格

| 风格 | 命令参数 | 说明 | 适合 |
|------|---------|------|------|
| **袁腾飞** | `--style yuan` | 吐槽历史，段子连发 | 技术史、人物故事 |
| **老高** | `--style laogao` | 悬疑驱动，层层揭秘 | 前沿技术、神秘话题 |
| **罗翔** | `--style luoxiang` | "张三"式荒诞类比 | 算法原理、概念解释 |
| **精简** | `--style clean` | 纯干货，无废话 | 教程、技术讲解 |

## 工具链

| 工具 | 用途 | 依赖 |
|------|------|------|
| **Claude** | 基于 History 风格化润色旁白稿 | 已有 |
| **Qwen3-TTS** | 本地 TTS + 声音克隆（RTX 4060） | pip install qwen-tts |
| **Remotion** | React 组件式视频动画（替代 Manim） | npx create-video@latest |
| **react-katex** | 数学公式渲染（替代 MiKTeX） | npm install react-katex |
| **FFmpeg** | 视频组装 + 字幕烧录 | 已有 |

## Mayer 多媒体学习原则（设计最高准则）

> 📚 来源: Mayer, R.E. (2009). *Multimedia Learning* (2nd ed). Cambridge University Press.
> 📚 来源: Clark, R.C. & Mayer, R.E. (2016). *e-Learning and the Science of Instruction* (4th ed). Wiley.

以下 7 条原则经实验验证，**每条都必须在视频设计中遵守**：

| # | 原则 | 含义 | 对视频的要求 |
|---|------|------|------------|
| **1. Coherence** | 去掉无关装饰 | 不加 emoji、不加无意义动效、不加纯装饰图片 |
| **2. Signaling** | 高亮关键信息 | 用颜色/字号/边框区分层级(金色=结论,蓝色=概念,红色=转折) |
| **3. Redundancy** | 旁白 ≠ 屏幕文字 | 屏幕放关键词/图表/动画，旁白讲故事/类比。**绝不同步念屏幕上的字** |
| **4. Spatial Contiguity** | 相关内容放一起 | 板书布局：人物+论文在左，核心内容在中，关键词在右 |
| **5. Segmenting** | 分段消化 | 每行旁白 = 一个独立动画，层层递进 |
| **6. Personalization** | 口语化 | 风格化润色时用对话式语气，不用学术论述 |
| **7. Voice** | 友好人声 | 使用声音克隆或温暖的 TTS 声线，不用机器感强的声音 |

## 视觉素材规则

### ✅ 允许使用
1. **Remotion 组件动画**（首选）— 概念、算法、流程、时间线、对比
2. **Wikipedia 真实照片** — 人物肖像（如科学家、发明者）
3. **论文封面/首页截图** — 增加专业感，可做缓慢滑动动画
4. **历史老照片** — 增加故事感（公有领域）

### ❌ 禁止使用
1. ~~AI 生成图片~~（generate_image）— 质量不可控
2. ~~Pexels/Pixabay 库存图片~~ — 与内容不匹配
3. ~~Emoji 图标~~ — AI 感太重，用设计手段替代
4. ~~Ken Burns / zoompan 效果~~ — 导致画面抖动

## 板书式动画设计规范

> 📚 来源: Williams, R. (2002). *The Non-Designer's Design Book*. CRAP 四原则.
> 📚 来源: Knaflic, C.N. (2015). *Storytelling with Data*. 数据可视化叙事.

### 布局原则（CRAP — Contrast, Repetition, Alignment, Proximity）

| 原则 | 要求 |
|------|------|
| **Contrast** | 用字号/颜色/粗细区分层级，不用 emoji |
| **Repetition** | 每个场景用相同的配色方案和组件样式 |
| **Alignment** | CSS Grid 2-3 列布局，内容对齐 |
| **Proximity** | 相关元素紧挨，无关元素拉开间距 |

### 板书展示方式

- **从左到右逐步铺满**：先出左列（人物），再出中列（核心内容），最后右列（关键词）
- **从上到下逐行出现**：每行旁白对应一行板书内容
- **层层递进**：Setup → Tension → Turn → Payoff
- **铺满画面**：尽量填满可用空间，不留大面积空白
- **底部留白**：底部 15% 留给字幕区

### 视觉层级标记（替代 emoji）

| 标记方式 | 用于 |
|---------|------|
| 金色渐变文字 | 关键结论 |
| 蓝色左边框高亮块 | 核心概念 |
| 红色虚线框 | 转折/悬念 |
| 大号粗体年份 | 时间节点 |
| 灰色小字标签 | 分类/标注 |

### 旁白稿格式

```
旁白文本 | [视觉提示]
```

示例：
```
1951年，两个统计学家写了一份报告，结果没人看到。 | [年份闪入 + 两个人物卡片 + 文件淡出]
他们的想法很简单：找到跟你最像的邻居，抄他的答案。 | [查询点出现 → 箭头指向最近点 → 标签复制]
但问题是，一个一个比过去，数据多了就太慢了。 | [暴力搜索：逐个比较 → 进度条越来越慢]
```

## 完整工作流（5步出视频）

### Step 1: 创建项目
```bash
python generate_video_script.py <course> <topic> --style yuan
```
→ 创建 `video-content/<course>/<topic>/` 目录结构

### Step 2: 风格化润色旁白稿

> **不允许重写内容**。History 文件的故事线、人物、年份、转折点全部保留。

告诉 Claude：
> "用袁腾飞风格，根据 xxx_history.md，风格化润色为旁白稿。
> 要求：口语化 + 降门槛 + 加风格 + 调节奏。每行一句话，每行附 [视觉提示]。"

Claude 直接输出 → 存为 `narration/script.txt`

### Step 3: 生成音频
```bash
# 用自己的声音
python generate_narration_qwen.py --script narration/script.txt --clone voice.mp3 --output-dir narration

# 或用预设声音
python generate_narration_qwen.py --script narration/script.txt --speaker uncle_fu --output-dir narration
```

### Step 4: 制作 Remotion 动画

Remotion 项目中，为每段旁白创建一个 React 组件：

```tsx
// 板书式三列布局
<Series>
  <Series.Sequence durationInFrames={90}>
    <BlackboardScene layout="three-column">
      <PersonCard name="Fix & Hodges" year={1951} />
      <CoreInsight text="找到最像的邻居，抄答案" />
      <KeywordTag label="方法" value="非参数分类" />
    </BlackboardScene>
  </Series.Sequence>
</Series>
```

渲染为 mp4：
```bash
npx remotion render src/index.ts MainVideo --output visuals/scene_01.mp4
```

### Step 5: 组装视频
```bash
python assemble_video_v6.py <project_dir>
```
→ 自动：TTS时间戳对齐 + 场景自动映射 + 无标点字幕 → `output/final_v6.mp4`

## 组装器 v6 特性

| 特性 | 说明 |
|------|------|
| **时间对齐** | 三级回退：TTS timestamps.json → Whisper ASR → 静音检测+字数比例 |
| **字幕风格** | 短视频风格：无标点、不断词、每条 ≤18字、底部紧贴 |
| **不断词保护** | 英文单词、KD-Tree、1951年、"引号词" 等原子单元不拆开 |
| **场景映射** | 自动搜索 visuals/scene_XX.mp4 → Remotion 输出 → 按名匹配 |
| **冻结补帧** | 动画短于旁白时，自动冻结最后一帧补足时长 |
| **镜头节奏** | 1 段旁白 = 1 个场景，精确到毫秒级对齐 |

## 叙事规则

### 三幕结构（每个视频必须遵守）

```
第一幕：钩子（0-15秒）
└── 反直觉事实、惊人数字、或悬念

第二幕：故事（15秒-4分钟）
├── 起源：谁，在什么困境下，想到了这个方法？
├── 困境：第一次尝试失败了，为什么？
├── 突破：关键的那一步是什么？
└── 留尾：解决了问题，但制造了新问题

第三幕：收尾（最后30秒）
├── 一句话总结
├── 今天的回响
└── 预告 + 关注引导
```

### 叙事节拍（替代雅思写作结构）

每段旁白遵循叙事节拍（Not 论证结构）：

```
Setup    → "1951年，两个统计学家……"
Tension  → "但这份报告从来没有正式发表"
Turn     → "直到16年后，另一个人证明了……"
Payoff   → "原来最笨的方法，也有数学保证"
```

### SUCCESs 自检（Made to Stick 框架）

- **S — Simple**: 能一句话说清吗？
- **U — Unexpected**: 钩子反直觉吗？
- **C — Concrete**: 类比到位吗？
- **C — Credible**: 有具体人名/年份吗？
- **E — Emotional**: 有情感触发吗？
- **S — Stories**: 是故事还是论述？

## 文件结构

### Skill 脚本
```
scripts/
├── generate_video_script.py     # 项目脚手架
├── generate_narration_qwen.py   # Qwen3-TTS 旁白（导出 timestamps.json）
├── assemble_video_v6.py         # 视频组装 v6（精确对齐+无标点字幕）
└── download_visuals.py          # 已弃用（不再使用库存图片）
```

### 项目输出
```
video-content/<course>/<topic>/
├── narration/
│   ├── script.txt                # 旁白稿（每行一句 + [视觉提示]）
│   ├── full_narration_myvoice.mp3
│   └── timestamps.json           # TTS 精确时间戳
├── visuals/
│   ├── src/                      # Remotion React 源码
│   ├── photos/                   # Wikipedia 肖像 + 论文封面
│   └── scene_XX.mp4              # Remotion 渲染输出
├── output/
│   ├── final_v6.mp4              # 最终成品
│   ├── subtitles.srt             # 无标点短视频字幕
│   └── segments.json             # 分段信息（调试用）
└── EDITING_GUIDE.md              # 剪辑指南
```

## 参考教材

### 教育视频设计（科学依据）
| 书名 | 作者 | 本地文件 | 核心价值 |
|------|------|---------|---------|
| **Multimedia Learning** (2nd ed) | Richard Mayer | `textbooks/mayer_multimedia_learning.pdf` | 12 条实验验证的多媒体学习原则 |
| **e-Learning and the Science of Instruction** (4th ed) | Clark & Mayer | `textbooks/clark_mayer_elearning.pdf` | 上面那本的实践版 |

### 视觉设计
| 书名 | 作者 | 本地文件 | 核心价值 |
|------|------|---------|---------|
| **The Non-Designer's Design Book** (4th ed) | Robin Williams | `textbooks/williams_non_designers_design_book.pdf` | CRAP 四原则 |
| **Storytelling with Data** | Cole Nussbaumer Knaflic | `textbooks/knaflic_storytelling_with_data.pdf` | 数据可视化叙事 |
| **Don't Make Me Think** | Steve Krug | `textbooks/krug_dont_make_me_think.pdf` | 用户体验直觉设计 |

### 叙事与编剧
| 书名 | 作者 | 本地文件 | 核心价值 |
|------|------|---------|---------|
| **Story** | Robert McKee | `textbooks/mckee_story.pdf` | 编剧圣经——结构、节奏、冲突 |
| **Save the Cat!** | Blake Snyder | `textbooks/snyder_save_the_cat.pdf` | Beat Sheet 节拍表 |
| **Made to Stick** | Chip & Dan Heath | `textbooks/heath_made_to_stick.pdf` | SUCCESs 传播模型 |

### 动画制作
| 书名/资源 | 作者 | 本地文件 | 核心价值 |
|----------|------|---------|---------|
| **The Animator's Survival Kit** | Richard Williams | `textbooks/williams_animators_survival_kit.pdf` | 动画节奏与时间控制 |
| **Remotion 官方文档** | — | [remotion.dev/docs](https://remotion.dev/docs) | React 视频制作框架 |
| **3Blue1Brown 源码** | Grant Sanderson | [github.com/3b1b/manim](https://github.com/3b1b/manim) | 数学可视化参考 |

### 风格参考
| 创作者 | 为什么参考 |
|--------|-----------|
| **袁腾飞** | 吐槽式讲史 |
| **老高与小茉** | 悬疑驱动叙事 |
| **罗翔** | 荒诞类比教学 |
| **3Blue1Brown** | 数学可视化动画 |
| **Ali Abdaal** | A-Cut + B-Roll 剪辑法 |
