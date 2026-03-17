"""从 timestamps.json 直接生成字幕（无需 Whisper）"""
import json, re
from pathlib import Path

BASE = Path(r"c:\Users\40270\OneDrive\Desktop\workspace\aisd\video-content\machine-learning\knn")
ts = json.loads((BASE / "narration" / "timestamps.json").read_text("utf-8"))

srt_lines = []
caption_data = []
sub_idx = 1

for seg in ts:
    text = seg["text"]
    start = seg["start"]
    end = seg["end"]
    duration = end - start

    # 去标点（短视频风格）
    clean = re.sub(r'[，。！？：；、""''——……（）《》\-]', '', text)

    # 按 18 字分割
    chunks = []
    while len(clean) > 18:
        chunks.append(clean[:18])
        clean = clean[18:]
    if clean:
        chunks.append(clean)

    total_chars = sum(len(c) for c in chunks)
    t = start
    for chunk in chunks:
        chunk_dur = duration * len(chunk) / total_chars
        chunk_end = t + chunk_dur

        def fmt(s):
            h = int(s // 3600)
            m = int((s % 3600) // 60)
            sec = int(s % 60)
            ms = int((s % 1) * 1000)
            return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

        srt_lines.append(str(sub_idx))
        srt_lines.append(f"{fmt(t)} --> {fmt(chunk_end)}")
        srt_lines.append(chunk)
        srt_lines.append("")

        caption_data.append({
            "index": sub_idx,
            "text": chunk,
            "start": round(t, 3),
            "end": round(chunk_end, 3),
            "segment_index": seg["index"]
        })
        sub_idx += 1
        t = chunk_end

# 写 SRT
srt_path = BASE / "output" / "subtitles.srt"
srt_path.parent.mkdir(parents=True, exist_ok=True)
srt_path.write_text("\n".join(srt_lines), encoding="utf-8")

# 写 captions.json
cap_path = BASE / "captions.json"
with open(cap_path, "w", encoding="utf-8") as f:
    json.dump({
        "total_subtitles": len(caption_data),
        "total_duration_sec": round(ts[-1]["end"], 3),
        "style": "short_video_no_punctuation",
        "max_chars_per_line": 18,
        "captions": caption_data
    }, f, ensure_ascii=False, indent=2)

print(f"OK subtitles.srt: {len(caption_data)} lines")
print(f"OK captions.json: {cap_path}")
print(f"   duration: {ts[-1]['end']:.1f}s")
