# Phase 7: 组装渲染 (Assembly & Render)

## 概述

| 项 | 值 |
|----|---|
| **角色** | Editor |
| **技能** | Remotion / FFmpeg |
| **前置条件** | Phase 4 + Phase 6 完成 |
| **输出** | `final.mp4` |
| **预计时间** | 5-15 分钟 |

## 目标

将素材、语音、字幕、BGM 组装成最终视频，确保时间轴同步。

## 同步策略

> **来源**: ai-video-generation-workflow ARCHITECTURE.md
>
> "Subtitle cue timing is derived from audio-manifest.json segment durations.
>  Slide switching uses the same duration timeline to avoid drift.
>  Rendering applies fixed 16:9 canvas and normalized scaling."

### 时间轴主轴 = 音频

```
音频时间轴 (主轴)
|--- segment_01 ---|--- segment_02 ---|--- segment_03 ---|

动画时间轴 (从属)
|--- scene_01 ----|--- scene_02 ----|--- scene_03 ----|

字幕时间轴 (从属)
|-- word1 -- word2 -- word3 --|-- word4 -- word5 ---|

BGM 时间轴 (独立)
|=============== fade in → sustain → fade out ===============|
```

所有时间轴都以 `timestamps.json` 为基准对齐。

## 执行步骤

### 方式 A: Remotion 渲染（推荐）

#### 1. 构建 Composition

```tsx
// composition.tsx
import { Composition } from 'remotion';
import { VideoComposition } from './VideoComposition';
import timestamps from './narration/timestamps.json';
import captions from './captions.json';

export const RemotionRoot = () => (
  <Composition
    id="EducationalVideo"
    component={VideoComposition}
    durationInFrames={Math.ceil(timestamps.total_duration_ms / 1000 * 30)}
    fps={30}
    width={1920}
    height={1080}
    defaultProps={{ timestamps, captions }}
  />
);
```

#### 2. 渲染

```bash
npx remotion render composition.tsx EducationalVideo final.mp4
```

### 方式 B: FFmpeg 组装（备选）

```bash
# 合并所有场景 + 音频 + 字幕
ffmpeg -i narration/full_narration.mp3 \
       -i assets/scenes_concat.mp4 \
       -i bgm/ambient.mp3 \
       -filter_complex "[1:v][0:a][2:a]..." \
       -c:v libx264 -preset fast \
       final.mp4
```

## BGM 处理

| 参数 | 值 | 来源 |
|------|---|------|
| BGM 音量 | 旁白的 10-15% | Clark & Mayer: 不干扰认知通道 |
| Fade in | 前 2 秒渐入 | — |
| Fade out | 末 3 秒渐出 | — |
| 类型 | 无歌词环境音乐 | Mayer: 避免 seductive details |

## 输出规格

| 参数 | 值 |
|------|---|
| 分辨率 | 1920×1080 (16:9) |
| 帧率 | 30 fps |
| 编码 | H.264 (libx264) |
| 音频 | AAC 128kbps |
| 格式 | MP4 |
| 目标大小 | < 100 MB/5min |

## 完成检查

- [ ] `final.mp4` 存在且可播放
- [ ] 视频时长与 `timestamps.json` 总时长匹配（误差 < 1 秒）
- [ ] 旁白与动画同步（无明显延迟/提前）
- [ ] 字幕与语音同步
- [ ] BGM 不干扰旁白
- [ ] 无黑屏/空白帧
- [ ] 分辨率和帧率达标

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- Clark & Mayer《e-Learning and the Science of Instruction》3rd Ed., Ch.5 "Applying the Contiguity Principle", **p.91-110** — 音画同步（"Synchronize Spoken Words with Corresponding Graphics", p.102）
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Clark & Mayer, Ch.8 "Applying the Coherence Principle", **p.151-172** — BGM 不干扰（"Avoid e-Lessons with Extraneous Audio", p.153）
- Mayer《Multimedia Learning》3rd Ed. — Temporal Contiguity + Coherence Principle
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`


## 参考实现

- `short-video-maker` 的 `Remotion.render()`: Remotion 渲染管道
- `ai-video-generation-workflow` 的 `render_video.py`: FFmpeg 渲染 + 字幕同步
- `video-creator` 的 `VideoModel.generate_video()`: 音频+图片+字幕组装
