# KNN 视频剪辑指南 (Editing Guide)

> 本文件是 KNN 视频项目的总指南。后续 Phase 4-8 只需按此文件执行。

---

## 当前进度

| Phase | 名称 | 状态 | 产出物 |
|-------|------|------|--------|
| 0 | 初始化 | ✅ | `.video-state.yaml` |
| 1 | 内容提取 | ✅ | `content_brief.md` |
| 2 | 脚本写作 | ✅ | `script.md` + `script_tts.txt` |
| 3 | 分镜设计 | ✅ | `storyboard.md` |
| 4 | 素材制作 | 📋 就绪 | `assets_manifest.md`（需要 Remotion 渲染） |
| 5 | 语音合成 | 📋 就绪 | `voice_guide.md`（需要 GPU / 手动录制） |
| 6 | 字幕生成 | ⏳ | 依赖 Phase 5 |
| 7 | 组装渲染 | ⏳ | 依赖 Phase 4 + 6 |
| 8 | 质量审查 | ⏳ | 依赖 Phase 7 |

---

## 快速执行指南

### Step 1: 语音合成（Phase 5）

```bash
# 方式 A: Qwen3-TTS + 声音克隆（GPU 环境）
python .agent/skills/ai-video-director/scripts/generate_narration_qwen.py \
  --script video-content/machine-learning/knn/script_tts.txt \
  --clone video-content/voice_sample.m4a \
  --output-dir video-content/machine-learning/knn/narration

# 方式 B: Edge-TTS 快速预览（无需 GPU）
python .agent/skills/ai-video-director/scripts/generate_narration_edge.py \
  --script video-content/machine-learning/knn/script_tts.txt \
  --voice zh-CN-YunxiNeural \
  --output-dir video-content/machine-learning/knn/narration
```

### Step 2: 素材制作（Phase 4，可与 Step 1 并行）

```bash
cd video-content/machine-learning/knn

# 初始化 Remotion 项目
npx -y create-video@latest ./assets

# 按 assets_manifest.md 创建 20 个场景组件
# 参考 storyboard.md 的视觉描述

# 预览
cd assets && npx remotion preview src/Root.tsx
```

### Step 3: 字幕生成（Phase 6）

```bash
# 依赖 narration/*.wav 存在
python -c "
import whisper, json
from pathlib import Path
model = whisper.load_model('base')
segments = []
t = 0
for wav in sorted(Path('narration').glob('segment_*.wav')):
    r = model.transcribe(str(wav), language='zh', word_timestamps=True)
    words = [{'text': w['word'], 'start': t + w['start'], 'end': t + w['end']} 
             for s in r['segments'] for w in s.get('words', [])]
    dur = r['segments'][-1]['end'] if r['segments'] else 0
    segments.append({'words': words, 'start': t, 'end': t + dur})
    t += dur
json.dump({'segments': segments, 'total_duration_s': t}, 
          open('captions.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'✅ captions.json 生成完成，总时长 {t:.1f}s')
"
```

### Step 4: 组装渲染（Phase 7）

```bash
# Remotion 方式
cd assets
npx remotion render src/Root.tsx KnnVideo --output ../output/knn_full.mp4

# 或 FFmpeg 方式
ffmpeg -i narration/full_narration.mp3 \
       -i output/scenes_concat.mp4 \
       -c:v libx264 -preset medium -crf 18 \
       -c:a aac -b:a 128k \
       output/final.mp4
```

### Step 5: 质量审查（Phase 8）

按以下清单逐项检查:

- [ ] 视频可播放，无黑屏
- [ ] 旁白与动画同步（误差 < 0.5s）
- [ ] 字幕与语音同步
- [ ] 无未定义名词（铁律 1）
- [ ] 每段有来源（铁律 2）
- [ ] 每帧一个视觉焦点（Mayer 连贯）
- [ ] 屏幕无大段文字（Mayer 冗余）
- [ ] 配色一致（金=结论 蓝=概念 红=转折）
- [ ] 底部 15% 字幕安全区无遮挡
- [ ] 总时长 4:00-5:30

---

## 文件清单

```
video-content/machine-learning/knn/
├── .video-state.yaml       # 状态文件
├── content_brief.md        # Phase 1: 内容提要
├── script.md               # Phase 2: 结构化脚本（带来源+视觉提示）
├── script_tts.txt           # Phase 2: TTS 纯文本
├── storyboard.md            # Phase 3: 分镜设计（20 场景）
├── assets_manifest.md       # Phase 4: 素材清单
├── voice_guide.md           # Phase 5: 语音生成指南
├── EDITING_GUIDE.md         # 本文件
├── narration/               # Phase 5 输出（待生成）
├── assets/                  # Phase 4 输出（待创建 Remotion 项目）
├── captions.json            # Phase 6 输出（待生成）
└── output/
    └── final.mp4            # Phase 7 输出（最终成品）
```

---

## 视频信息

| 项 | 值 |
|----|---|
| 主题 | KNN (K-Nearest Neighbors) |
| 风格 | 袁腾飞 |
| 开场模式 | B — 故事 Hook（1951 年历史故事） |
| 总时长 | ~5 分钟（20 段 Segment） |
| 分辨率 | 1920×1080 16:9 |
| 帧率 | 30 fps |
| 下期预告 | LOF 异常检测 |
