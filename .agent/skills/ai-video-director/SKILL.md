---
name: ai-video-director
description: AI Video Director skill for creating educational videos from knowledge map files. Use when (1) creating video narration scripts in 4 styles (袁腾飞/老高/罗翔/精简), (2) generating TTS audio with voice cloning, (3) assembling videos with auto-subtitles, (4) user says "视频" or "video" with knowledge map topics.
---

# 🎬 AI 视频编导 Skill

> 角色定义见 `knowledge-map/README.md` 第 22 号角色。

## 定位

**一句话**：把知识地图里的 History 文件变成 3 分钟教育视频。

**工具链**：Claude 写稿 → Qwen3-TTS 配音 → FFmpeg 组装 → 自动字幕

## 四种叙事风格

| 风格 | 命令参数 | 说明 | 适合 |
|------|---------|------|------|
| **袁腾飞** | `--style yuan` | 吐槽历史，段子连发 | 技术史、人物故事 |
| **老高** | `--style laogao` | 悬疑驱动，层层揭秘 | 前沿技术、神秘话题 |
| **罗翔** | `--style luoxiang` | "张三"式荒诞类比 | 算法原理、概念解释 |
| **精简** | `--style clean` | 纯干货，无废话 | 教程、技术讲解 |

## 工具链

| 工具 | 用途 | 费用 |
|------|------|------|
| **Claude** | 写旁白稿（4种风格） | 已有 |
| **Qwen3-TTS** | 本地 TTS + 声音克隆（RTX 4060） | 免费 |
| **FFmpeg** | 视频组装 + 字幕烧录 | 免费 |
| **Manim** | 算法/公式动画 | 免费 |
| **Pexels/Pixabay** | 免费图片/视频素材 | 免费 |
| **CapCut（可选）** | 精调字幕、BGM | 免费 |

## 完整工作流（5步出视频）

### Step 1: 创建项目
```bash
python generate_video_script.py <course> <topic> --style clean
```
→ 创建 `video-content/<course>/<topic>/` 目录结构

### Step 2: 写旁白稿
告诉 Claude：
> "用精简风格，根据 xxx_history.md，写一个 3 分钟旁白稿，每段一行"

Claude 直接输出 → 存为 `narration/script.txt`

### Step 3: 生成音频
```bash
# 用自己的声音
python generate_narration_qwen.py --script narration/script.txt --clone voice.mp3 --output-dir narration

# 或用预设声音
python generate_narration_qwen.py --script narration/script.txt --speaker uncle_fu --output-dir narration
```

### Step 4: 准备视觉素材
把图片/视频放到 `visuals/` 目录，命名为 `scene_01.png`, `scene_02.mp4` 等。

**素材规则**：
- 讲人物历史 → 老照片、人物肖像、论文截图
- 讲算法原理 → Manim 动画
- 讲现代应用 → 产品截图、科技素材
- 金句/感悟 → 大字文字卡

### Step 5: 组装视频
```bash
python assemble_video_v3.py <project_dir>
```
→ 自动：视觉轨道 + 音频 + SRT 字幕 → `output/final.mp4`

## 叙事规则

### 三幕结构（每个视频必须遵守）

```
第一幕：钩子（0-15秒）
└── 反直觉事实、惊人数字、或悬念

第二幕：故事（15秒-2分30秒）
├── 起源：谁，在什么困境下，想到了这个方法？
├── 困境：第一次尝试失败了，为什么？
├── 突破：关键的那一步是什么？
└── 留尾：解决了问题，但制造了新问题

第三幕：收尾（2分30秒-3分钟）
├── 一句话总结
├── 今天的回响
└── 预告 + 关注引导
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
├── generate_narration_qwen.py   # Qwen3-TTS 旁白
├── assemble_video_v3.py         # 视频组装 v3
└── assemble_video.py            # 旧版（备用）
```

### 项目输出
```
video-content/<course>/<topic>/
├── narration/
│   ├── script.txt                # 旁白稿
│   └── full_narration_myvoice.mp3
├── visuals/
│   ├── scene_01.png
│   └── scene_02.mp4
└── output/
    ├── final.mp4
    └── subtitles.srt
```

## 参考教材

### 叙事与编剧
| 书名 | 作者 | 为什么必读 |
|------|------|-----------|
| **Story** | Robert McKee | 编剧圣经——结构、节奏、冲突 |
| **Save the Cat!** | Blake Snyder | Beat Sheet 节拍表 |
| **Made to Stick** | Chip & Dan Heath | SUCCESs 传播模型 |

### 视觉叙事
| 书名 | 作者 | 为什么必读 |
|------|------|-----------|
| **In the Blink of an Eye** | Walter Murch | 剪辑理论 |
| **The Visual Story** | Bruce Block | 画面构图服务叙事 |

### 风格参考
| 创作者 | 为什么参考 |
|--------|-----------|
| **袁腾飞** | 吐槽式讲史 |
| **老高与小茉** | 悬疑驱动叙事 |
| **罗翔** | 荒诞类比教学 |
| **3Blue1Brown** | 数学可视化 |
| **Ali Abdaal** | A-Cut + B-Roll 剪辑法 |
