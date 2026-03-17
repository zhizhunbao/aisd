# Phase 6: 字幕生成 (Caption Generation)

## 概述

| 项 | 值 |
|----|---|
| **角色** | (自动) |
| **技能** | timestamps.json 解析 (首选) / Whisper (备选) |
| **前置条件** | Phase 5 完成，`narration/timestamps.json` 或 `narration/*.wav` 存在 |
| **输出** | `captions.json` + `output/subtitles.srt` |
| **预计时间** | < 1 分钟 (方式 A) / 2-5 分钟 (方式 B) |

## 目标

从 TTS 时间戳或音频生成精确字幕，确保字幕和语音同步。

## 字幕来源选择

| 方式 | 适用场景 | 精度 | 成本 |
|------|---------|------|------|
| **方式 A: 直接用 `timestamps.json`** | TTS 生成的音频（Qwen3/Edge） | ✅ 精确到段 | 零成本 |
| **方式 B: Whisper 重新转录** | 手动录制的音频（无时间戳） | ✅ 精确到词 | 需要 GPU |

> ⚠️ **优先用方式 A**。TTS 已经输出了每段的精确起止时间，
> 无需 Whisper 重新转录。只有手动录制（无 timestamps.json）时才用方式 B。

## 执行步骤

### 方式 A: 从 timestamps.json 生成（推荐）

`timestamps.json` 由 Phase 5 的 TTS 引擎自动输出，包含每段精确的 start/end 时间。
直接将每段文本去标点、按 ≤18 字分行、按字数比例分配时间：

```python
# 去标点 → 按18字切 → 按比例分时间 → 输出 SRT + captions.json
python generate_captions.py
```

### 方式 B: Whisper 转录（仅手动录制时使用）

```bash
python -c "
import whisper
model = whisper.load_model('base')
for wav in sorted(Path('narration').glob('segment_*.wav')):
    result = model.transcribe(str(wav), language='zh', word_timestamps=True)
    # 输出 word-level timestamps
"
```

### 2. 生成 captions.json

```json
{
  "segments": [
    {
      "segment_id": "act1_pain",
      "words": [
        { "text": "学", "start": 0.0, "end": 0.2 },
        { "text": "卷积层", "start": 0.2, "end": 0.8 },
        { "text": "最让人崩溃的", "start": 0.9, "end": 1.6 },
        { "text": "是", "start": 1.6, "end": 1.8 },
        { "text": "什么", "start": 1.8, "end": 2.3 }
      ],
      "full_text": "学卷积层最让人崩溃的是什么",
      "start": 0.0,
      "end": 2.3
    }
  ]
}
```

### 3. 字幕显示策略

| 策略 | 描述 | 适用场景 |
|------|------|---------|
| **逐词高亮** | 当前读到的词高亮显示 | 关键定义段 |
| **整句出现** | 整句一起显示 | 短句/感叹 |
| **关键词弹出** | 只显示专业名词 | 概念讲解段 |

## 完成检查

- [ ] `captions.json` 存在且合法 JSON
- [ ] 每个 narration segment 都有对应的 caption segment
- [ ] word-level timestamps 合理（无重叠、无大间隙）
- [ ] 中文分词正确（无乱切词）

## 教科书来源

> 以下引用已从 MinerU 解析的教科书原文验证

- Clark & Mayer《e-Learning and the Science of Instruction》3rd Ed., Ch.7 "Applying the Redundancy Principle: Explain Visuals with Words in Audio OR Text: Not Both", **p.133-146** — 字幕不应重复完整旁白（"Do Not Add On-Screen Text to Narrated Graphics", p.135）
  - MinerU: `data/mineru_output/clark_mayer_elearning/clark_mayer_elearning/hybrid_auto/clark_mayer_elearning.md`
- Mayer《Multimedia Learning》3rd Ed. — Redundancy Principle
  - MinerU: `data/mineru_output/mayer_multimedia_learning/mayer_multimedia_learning/hybrid_auto/mayer_multimedia_learning.md`


## 参考实现

- `short-video-maker` 的 `Whisper.CreateCaption()`: Whisper 字幕生成
- `video-creator` 的 `SubtitleModel.generate_subtitle()`: Whisper 对齐
- `ai-video-generation-workflow` 的 `render_video.py`: 基于音频时长的字幕生成
