---
name: ai-video-director
description: AI Video Director skill for creating educational videos from knowledge map files. Use when (1) creating video narration scripts in 4 styles (袁腾飞/老高/罗翔/精简), (2) generating TTS audio with voice cloning, (3) assembling videos with auto-subtitles, (4) user says "视频" or "video" with knowledge map topics.
---

# 🎬 AI 视频编导 Skill

> 角色定义见 `knowledge-map/README.md` 第 22 号角色。

## 定位

**一句话**：把知识地图的 9 维文件变成 3-5 分钟「痛点共鸣 + 人话翻译 + 避坑指南」教育视频。

**核心原则**：**知识地图 9 维文件 = 视频的多源素材库**，从 Concepts/Tutorial/Pitfalls/History/Bridge 中提取，重组为五幕结构。

**工具链**：Claude 五幕重组 → Qwen3-TTS 配音 → Remotion 动画 → FFmpeg 组装

**内容理念**：不搞玄学，不装逼，只讲人话、讲逻辑、讲避坑。

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

> 📚 详细分类见 Step 3（Clark & Mayer 四类体系）

### ✅ 允许使用（按优先级）
1. **Remotion 组件动画**（首选）— Organizational / Transformational / Interpretive 三类
2. **Wikimedia Commons 真实照片** — Representational 类（人物肖像、历史事件）
3. **论文封面/首页截图** — Representational 类（arXiv / 出版商）
4. **大学官网/档案馆照片** — Representational 类（机构、实验室）

### ❌ 禁止使用
1. ~~AI 生成图片~~（generate_image）— 违反 Mayer Coherence 原则
2. ~~Pexels/Pixabay 库存图片~~ — 与内容不匹配（Decorative）
3. ~~Emoji 图标~~ — Decorative，用设计手段替代
4. ~~Ken Burns / zoompan 效果~~ — 导致画面抖动
5. ~~无版权标注的图片~~ — 法律风险

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

## 完整工作流（7步出视频）

### Step 1: 创建项目
```bash
python generate_video_script.py <course> <topic> --style yuan
```
→ 创建 `video-content/<course>/<topic>/` 目录结构

### Step 2: 多维度提取 + 五幕重组旁白稿

> **内容忠于知识地图**，不捏造。从多个维度提取后，重组为五幕结构。

告诉 Claude：
> "用袁腾飞风格，根据 xxx 的 concepts/tutorial/pitfalls/history/bridge 文件，
> 按五幕结构（痛点共鸣 → 人话翻译 → 核心逻辑 → 避坑指南 → 来龙去脉）重组为旁白稿。
> 开场从通用痛点库选最匹配的痛点引发共鸣。
> 要求：口语化 + 降门槛 + 加风格 + 调节奏。每行一句话，每行附 [视觉提示]。"

Claude 直接输出 → 存为 `narration/script.txt`

### Step 3: 素材收集与整理（按需搜索）

> **原则：不囤素材，按旁白稿需求精准搜索。**
> 旁白稿确定后，从 `[视觉提示]` 中提取素材需求，一个个去找。

#### 3.1 素材分类（基于教科书理论）

> 📚 来源: Clark & Mayer《e-Learning and the Science of Instruction》(4th ed), Ch.4 "Applying the Multimedia Principle"
> 图形分六类，教育视频只用其中四类，**禁止 Decorative（装饰）**。

| 类别 | 教学功能 | 素材举例 | 文件前缀 | Remotion 实现 |
|------|---------|---------|---------|-------------|
| **Representational（再现）** | 展示真实外观 | 科学家肖像、论文封面、实验室照片 | `repr_` | `<Img>` / `<PersonCard photo={...}>` |
| **Organizational（组织）** | 展示关系和结构 | 时间线、技术演进路线图、对比表 | `org_` | `<TimelineFly>` / `<ComparisonSplit>` |
| **Transformational（变化）** | 展示过程和变化 | 算法步骤动画、数据流动、训练过程 | `trans_` | Remotion 动画组件（首选！） |
| **Interpretive（阐释）** | 让抽象可见 | 高维空间降维、决策边界可视化 | `interp_` | Remotion 动画 + react-katex 公式 |

> **关键决策规则：**
> - 🔍 **Representational** → 需要**搜索下载**（照片、论文截图）
> - 🎨 **Organizational / Transformational / Interpretive** → 用 **Remotion 组件制作**（不需要外部素材）
> - ❌ **Decorative**（纯装饰） → **禁止**（Mayer Coherence 原则）

#### 3.2 提取素材清单

从 `narration/script.txt` 的 `[视觉提示]` 中，按上述四类分类每个素材需求：

```
需要搜索下载的（Representational）：
- 👤 person: 人物肖像（科学家、发明者）
- 📄 paper: 论文封面/首页截图
- 📸 event: 历史事件照片
- 🏛️ place: 机构/实验室照片

用 Remotion 制作的（不需要搜索）：
- 📊 org: 时间线、路线图、对比表 → TimelineFly / ComparisonSplit
- 🔄 trans: 算法演示、步骤动画 → 自定义动画组件
- 💡 interp: 概念可视化、公式推导 → 动画 + react-katex
```

#### 3.3 搜索素材（仅 Representational 类）

| 优先级 | 来源 | 适合 | 搜索方式 |
|-------|------|------|---------|
| 1️⃣ | **知识地图 History 文件** | 已有 `🎥 视觉素材` 表 | 直接读取 `{topic}_history.md` 中的链接 |
| 2️⃣ | **Wikimedia Commons** | 科学家肖像、历史照片 | `commons.wikimedia.org/w/index.php?search=XXX` |
| 3️⃣ | **大学官网/档案馆** | 本校教授照片 | Google: `"XXX" site:stanford.edu` |
| 4️⃣ | **arXiv / Google Scholar** | 论文首页截图 | 下载 PDF 第一页截图 |
| 5️⃣ | **Smithsonian Open Access** | 博物馆藏品 | `si.edu/openaccess` |
| 6️⃣ | **Library of Congress** | 美国历史照片 | `loc.gov/free-to-use` |

#### 3.4 下载并整理

下载到 `visuals/photos/` 目录，命名规则 `{类别前缀}_{名称}.{ext}`：

```
visuals/photos/
├── repr_person_fix_hodges.jpg     # Representational: 人物肖像
├── repr_person_cover_hart.jpg
├── repr_paper_fix_hodges_1951.png # Representational: 论文封面
├── repr_event_rand_corp.jpg       # Representational: 事件照片
└── asset_manifest.json            # 素材清单（含分类信息）
```

#### 3.5 生成素材清单

创建 `visuals/photos/asset_manifest.json`：

```json
{
  "topic": "knn",
  "collected_at": "2026-03-17",
  "classification_source": "Clark & Mayer, e-Learning, Ch.4",
  "assets": [
    {
      "id": "repr_person_fix_hodges",
      "category": "representational",
      "type": "portrait",
      "file": "repr_person_fix_hodges.jpg",
      "source": "Wikimedia Commons",
      "url": "https://commons.wikimedia.org/wiki/File:XXX.jpg",
      "license": "Public Domain",
      "used_in_scenes": ["Scene01"]
    }
  ],
  "remotion_only": [
    {
      "id": "org_knn_timeline",
      "category": "organizational",
      "description": "KNN 技术演进时间线 1951-2020",
      "component": "TimelineFly",
      "used_in_scenes": ["Scene02"]
    },
    {
      "id": "trans_brute_force_search",
      "category": "transformational",
      "description": "暴力搜索逐个比较动画",
      "component": "Custom animation",
      "used_in_scenes": ["Scene03"]
    }
  ],
  "missing": [
    {
      "id": "repr_person_cover",
      "category": "representational",
      "type": "portrait",
      "reason": "No public domain portrait found",
      "fallback": "Use text-only PersonCard component (organizational)"
    }
  ]
}
```

> ⚠️ **找不到素材时的降级策略：**
> - Representational 人物无肖像 → 降级为 Organizational（用 `PersonCard` 文字卡片）
> - Representational 论文无 PDF → 降级为 Organizational（用引用块展示标题和出处）
> - ❌ 绝不用 AI 生成替代（违反 Mayer Coherence 原则）

### Step 4: 生成音频
```bash
# 用自己的声音
python generate_narration_qwen.py --script narration/script.txt --clone voice.mp3 --output-dir narration

# 或用预设声音
python generate_narration_qwen.py --script narration/script.txt --speaker uncle_fu --output-dir narration
```

### Step 5: 制作 Remotion 动画

Remotion 项目中，为每段旁白创建一个 React 组件。
**使用 Step 3 收集的素材**：通过 `asset_manifest.json` 查找可用素材。

```tsx
// 板书式三列布局，引用收集的素材
<Series>
  <Series.Sequence durationInFrames={90}>
    <BlackboardScene layout="three-column">
      <PersonCard
        name="Fix & Hodges"
        year={1951}
        photo={staticFile("photos/person_fix_hodges.jpg")}  // Step 3 收集的肖像
      />
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

### Step 6: 组装视频
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

### 五幕结构（每个视频必须遵守）

> ⚠️ **先判断受众，再定开场模式**。

| 模式 | 适用场景 | 第一幕 |
|------|---------|-------|
| **模式 A: 痛点 Hook** | 受众已知主题（课程学生） | "学 [主题]，最让人崩溃的是……" |
| **模式 B: 故事 Hook** | 受众不知主题（科普、入门） | 历史故事切入 → 一句话定义 |

**判断标准**：观众还不知道主题名字 → 模式 B；观众正在学且被困住 → 模式 A。

```
第一幕：开场（0:00 - 1:00）
├── 模式 A：痛点共鸣 Hook
│   └── 从通用痛点库选最匹配的 + 用 Pitfalls 中真实错误举例
│       "学 [主题]，最让人崩溃的是……"
└── 模式 B：故事 Hook
    └── 从 History 提取起源故事 + Concepts 一句话定义
        "[年份]，[人物] 发明了一个蠢到不可思议的方法……"

第二幕：人话翻译（1:00 - 2:00）
└── 从 Concepts 提取核心术语 → 换成生活类比
    "说人话，[术语] 就是 [类比]"

第三幕：核心逻辑（2:00 - 3:15）
└── 从 Tutorial + Math + First Principles 提取
    用 First Principles 的"5个为什么"追问链讲清底层逻辑
    "这东西的公理是什么？→ 从公理怎么推出来的？→ 为什么必须这样？"

第四幕：避坑指南（3:15 - 4:15）
└── 从 Pitfalls + First Principles（公理失效）提取
    "这里 90% 的人会踩坑：……"
    "如果 [公理] 不成立，整个方法就废了：……"

第五幕：收尾（4:15 - 5:00）
├── 模式 A：从 History 提取关键故事线 + Bridge 关联
└── 模式 B：从 History 提取技术演进线 + Bridge 关联
    "下期讲 [Bridge 后续主题]，关注不迷路"
```

### 叙事节拍（每幕内部遵循）

每段旁白遵循叙事节拍（Not 论证结构）：

```
Setup    → "学卷积层，最让人崩溃的是……"
Tension  → "你看教科书上三页公式，完全不知道在干嘛"
Turn     → "但说人话，卷积就是一个小窗口在图片上滑动"
Payoff   → "就这么简单。三页公式，一句话讲完"
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
├── generate_video_script.py     # Step 1: 项目脚手架
├── generate_narration_qwen.py   # Step 4: Qwen3-TTS 旁白（导出 timestamps.json）
└── assemble_video_v6.py         # Step 6: 视频组装 v6（精确对齐+无标点字幕）
```

### 项目输出
```
video-content/<course>/<topic>/
├── narration/
│   ├── script.txt                # Step 2: 旁白稿（每行一句 + [视觉提示]）
│   ├── full_narration_myvoice.mp3
│   └── timestamps.json           # Step 4: TTS 精确时间戳
├── visuals/
│   ├── photos/                   # Step 3: 按需搜索的素材
│   │   ├── person_*.jpg           #   人物肖像（Wikimedia Commons）
│   │   ├── paper_*.png            #   论文封面（arXiv）
│   │   ├── event_*.jpg            #   事件照片（公有领域）
│   │   └── asset_manifest.json    #   素材清单（来源+版权+降级策略）
│   ├── src/                      # Step 5: Remotion React 源码
│   └── scene_XX.mp4              # Step 5: Remotion 渲染输出
├── output/
│   ├── final_v6.mp4              # Step 6: 最终成品
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
