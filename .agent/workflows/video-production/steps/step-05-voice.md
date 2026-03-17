# Phase 5: 语音合成 (Voice Synthesis)

## 概述

| 项 | 值 |
|----|---|
| **角色** | Voice Engineer |
| **技能** | TTS (Qwen3 / Edge-TTS / 声音克隆) |
| **前置条件** | Phase 2 完成，`script.md` 和 `script_tts.txt` 存在 |
| **输出** | `narration/` (音频文件 + timestamps.json) |
| **预计时间** | 10-30 分钟 |
| **可并行** | 与 Phase 3-4 (分镜+素材) 并行 |

## 目标

将 `script_tts.txt` 转为高质量旁白音频，支持声音克隆。

## TTS 方案对比

| 方案 | 质量 | 速度 | 离线 | 克隆 | 推荐场景 |
|------|------|------|------|------|---------|
| **Qwen3-TTS** | ⭐⭐⭐⭐⭐ | 中 | ✅ | ✅ | 生产版本（需 GPU） |
| **Edge-TTS** | ⭐⭐⭐⭐ | 快 | ❌ | ❌ | 快速预览 |
| **Kokoro TTS** | ⭐⭐⭐⭐ | 快 | ✅ | ❌ | 英文内容 |
| **自己录制** | ⭐⭐⭐⭐⭐ | 慢 | ✅ | N/A | 最高质量 |

## 执行步骤

### 1. 准备 TTS 文本

从 `script_tts.txt` 读取（Phase 2 已清理过）：
- 无注释行
- 无视觉提示
- LaTeX/乘号已口语化
- 每行一段

### 2. 生成音频

#### 方式 A: Qwen3-TTS 声音克隆

```bash
python .agent/skills/ai-video-director/scripts/generate_narration_qwen.py \
  --script video-content/{course}/{topic}/script_tts.txt \
  --clone video-content/voice_sample.m4a \
  --output-dir video-content/{course}/{topic}/narration
```

#### 方式 B: Edge-TTS 快速预览

```bash
python .agent/skills/ai-video-director/scripts/generate_narration_edge.py \
  --script video-content/{course}/{topic}/script_tts.txt \
  --voice zh-CN-YunxiNeural \
  --output-dir video-content/{course}/{topic}/narration
```

### 3. 输出结构

```
narration/
├── segment_01.wav      # 每段独立音频
├── segment_02.wav
├── ...
├── full_narration.mp3  # 完整合并音频
└── timestamps.json     # 每段时间戳
```

### 4. timestamps.json 格式

```json
{
  "segments": [
    {
      "id": "act1_pain",
      "file": "segment_01.wav",
      "start_ms": 0,
      "end_ms": 8500,
      "duration_ms": 8500,
      "text": "学卷积层，最让人崩溃的是什么？"
    },
    {
      "id": "act1_pain_2",
      "file": "segment_02.wav",
      "start_ms": 8500,
      "end_ms": 15200,
      "duration_ms": 6700,
      "text": "名词太多了。"
    }
  ],
  "total_duration_ms": 300000
}
```

## Mayer 模态原则

> **来源**: Mayer《Multimedia Learning》Ch.20: "Modality Principle"
>
> "People learn better from graphics and narration than from graphics and on-screen text."
>
> → 用语音旁白而非屏幕文字来解释概念。屏幕只显示关键词和图形。

## 完成检查

- [ ] `narration/` 目录存在
- [ ] 每个 `script_tts.txt` 段落都有对应的 `segment_XX.wav`
- [ ] `timestamps.json` 存在且合法 JSON
- [ ] `full_narration.mp3` 可正常播放
- [ ] 音频无明显断句/停顿异常
- [ ] 总时长与 `script.md` 预期时长偏差 < 15%

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- Clark & Mayer《e-Learning and the Science of Instruction》3rd Ed., Ch.6 "Applying the Modality Principle: Present Words as Audio Narration Rather Than On-Screen Text", **p.115-129** — 语音 > 文字（"Present Words as Speech Rather Than On-Screen Text", p.117）
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Clark & Mayer, Ch.9 "Applying the Personalization Principle: Use Conversational Style and Virtual Coaches", **p.179-201** — 对话式语气（"Use Conversational Rather Than Formal Style", p.182）
- Mayer《Multimedia Learning》3rd Ed. — Modality + Personalization Principle
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`


## 参考实现

- `short-video-maker` 的 `Kokoro` 类: TTS 生成 + 音频时长获取
- `video-creator` 的 `AudioModel`: Coqui TTS 集成
- `ai-video-generation-workflow` 的 `generate_audio.py`: Edge/ElevenLabs 多后端
