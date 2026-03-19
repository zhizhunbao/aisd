# 🎙️ 声音资产 Voice Assets

## 目录结构

```
assets/voice/
├── voice-sample-original.m4a   # 原始声音样本（用于声音克隆训练）
├── README.md                    # 本文件
```

## 声音样本信息

| 字段       | 值                          |
|----------|-----------------------------|
| 文件名     | voice-sample-original.m4a   |
| 用途       | TTS 声音克隆训练样本          |
| 来源       | 用户本人录音                 |

## 使用方式

### 1. 声音克隆服务

将 `voice-sample-original.m4a` 上传到以下任一服务进行声音克隆：

| 服务            | 中文效果 | 克隆质量 | 价格     |
|----------------|---------|---------|----------|
| Fish Audio      | ⭐⭐⭐⭐⭐ | 优秀     | 免费额度  |
| ElevenLabs      | ⭐⭐⭐   | 优秀     | $5/月起   |
| Azure Custom    | ⭐⭐⭐⭐  | 企业级   | 按量付费  |
| Edge TTS (免费) | ⭐⭐⭐⭐  | 无克隆   | 免费      |

### 2. 生成旁白脚本

克隆完成后，使用 `scripts/generate-narration.py` 生成视频旁白：

```bash
python scripts/generate-narration.py \
  --voice-id <克隆后的voice_id> \
  --data video-lego/data/linear-algebra/flash/video.data.ts \
  --output video-content/public/narration/
```

### 3. 在视频数据中引用

```typescript
narration: {
  audioFile: 'narration/linear-algebra-flash/full_narration.mp3',
  // ...
}
```

## 注意事项

- 声音样本包含个人隐私，请勿上传到公开仓库
- 建议在 `.gitignore` 中忽略 `assets/voice/*.m4a`
