"""
视频组装器 v5（语义对齐版）
=============================
管线：script.txt 第N行 → scene_N.mp4 + audio segment N → subtitle N
不再使用关键词匹配，全部 1:1 语义对齐。

用法: python assemble_video_v5.py <project_dir>
"""
import subprocess
import json
import re
from pathlib import Path
import argparse

RESOLUTION = (1920, 1080)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    args = parser.parse_args()

    proj = Path(args.project_dir)
    narration_dir = proj / "narration"
    visuals_dir = proj / "visuals"
    output_dir = proj / "output"
    output_dir.mkdir(exist_ok=True)

    # 读取旁白
    script_path = narration_dir / "script.txt"
    lines = [l.strip() for l in script_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    n = len(lines)
    print(f"📝 {n} 段旁白")

    # 读取音频
    audio_path = next(narration_dir.glob("*.mp3"))
    audio_dur = get_duration(audio_path)
    print(f"🎙 音频: {audio_path.name} ({audio_dur:.1f}s)")

    # 静音检测 → 分段
    segments = detect_segments(audio_path, lines, audio_dur)
    print(f"✂️ {len(segments)} 个音频段")

    # 检查视觉素材
    for i in range(1, n + 1):
        fp = visuals_dir / f"scene_{i:02d}.mp4"
        if not fp.exists():
            print(f"⚠️ 缺少 {fp.name}")

    # 生成字幕（短视频风格）
    srt_path = output_dir / "subtitles.srt"
    generate_srt(segments, srt_path)

    # 保存段落信息
    with open(output_dir / "segments.json", "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    # 组装视频
    final_path = output_dir / "final_v5.mp4"
    assemble(segments, visuals_dir, audio_path, srt_path, final_path)

    size_mb = final_path.stat().st_size / 1024 / 1024
    print(f"\n✅ 完成: {final_path} ({size_mb:.1f}MB)")


def get_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return float(r.stdout.strip())


def detect_segments(audio_path: Path, lines: list[str], total_dur: float) -> list[dict]:
    """按字数比例切分音频（TTS 语速均匀，比静音检测更可靠）"""
    char_counts = [len(line) for line in lines]
    total_chars = sum(char_counts)

    # 按字数比例分配时间
    segments = []
    t = 0.0
    for i, (line, cc) in enumerate(zip(lines, char_counts)):
        seg_dur = (cc / total_chars) * total_dur
        segments.append({
            "index": i + 1,
            "start": t,
            "end": t + seg_dur,
            "text": line,
            "scene": f"scene_{i+1:02d}.mp4",
        })
        t += seg_dur

    # 打印时长分布
    for s in segments:
        dur = s["end"] - s["start"]
        print(f"  段{s['index']:2d}: {dur:5.1f}s ({len(s['text']):3d}字)")

    return segments


def generate_srt(segments: list[dict], output_path: Path, max_chars: int = 20):
    """短视频风格字幕：按标点断句，不断词"""
    # 中英文标点集
    punct = set("，。！？、；：…—,!?;:")
    srt_idx = 0

    with open(output_path, "w", encoding="utf-8-sig") as f:  # UTF-8 BOM
        for seg in segments:
            text = seg["text"]
            seg_start = seg["start"]
            seg_dur = seg["end"] - seg["start"]

            # 按标点分句（保证不断词）
            sentences = []
            current = ""
            for ch in text:
                current += ch
                if ch in punct:
                    sentences.append(current.strip())
                    current = ""
            if current.strip():
                sentences.append(current.strip())

            # 合并过短的句子（< 6 字与下句合并）
            merged = []
            buf = ""
            for s in sentences:
                buf += s
                if len(buf) >= 6:
                    merged.append(buf)
                    buf = ""
            if buf:
                if merged:
                    merged[-1] += buf
                else:
                    merged.append(buf)

            total_chars = sum(len(s) for s in merged)
            if total_chars == 0:
                continue

            t = seg_start
            for chunk in merged:
                chunk_dur = (len(chunk) / total_chars) * seg_dur
                end_t = min(t + chunk_dur, seg["end"])
                srt_idx += 1
                f.write(f"{srt_idx}\n")
                f.write(f"{fmt_time(t)} --> {fmt_time(end_t)}\n")
                f.write(f"{chunk}\n\n")
                t = end_t

    print(f"  📝 {srt_idx} 条字幕（按标点断句）")


def fmt_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def assemble(segments: list[dict], visuals_dir: Path, audio_path: Path,
             srt_path: Path, output_path: Path):
    """1:1 组装：每段音频 + 对应 Manim 视频 → 拼接 → 字幕"""
    w, h = RESOLUTION
    tmp_dir = output_path.parent / "tmp_v5"
    tmp_dir.mkdir(exist_ok=True)

    print(f"\n🎬 组装 {len(segments)} 段...")

    # Phase 1: 为每段生成 视频+音频 片段
    part_files = []
    for seg in segments:
        i = seg["index"]
        dur = seg["end"] - seg["start"]
        scene_path = visuals_dir / seg["scene"]
        out_part = tmp_dir / f"part_{i:02d}.mp4"

        if not scene_path.exists():
            # 如果缺场景，用黑屏
            scene_path = None

        # 提取音频段
        audio_seg = tmp_dir / f"audio_{i:02d}.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(audio_path),
            "-ss", str(seg["start"]), "-t", str(dur),
            "-c", "copy", str(audio_seg)
        ], capture_output=True)

        if scene_path:
            # 获取视频时长
            vid_dur = get_duration(scene_path)

            if vid_dur >= dur:
                # 视频够长，截取
                vf = f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:-1:-1:color=black"
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(scene_path), "-i", str(audio_seg),
                    "-t", str(dur), "-vf", vf,
                    "-r", "30", "-c:v", "libx264", "-preset", "fast",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                    str(out_part)
                ], capture_output=True)
            else:
                # 视频太短，冻结最后一帧补足
                vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,"
                      f"pad={w}:{h}:-1:-1:color=black,"
                      f"tpad=stop_mode=clone:stop_duration={dur - vid_dur + 0.5:.2f}")
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(scene_path), "-i", str(audio_seg),
                    "-t", str(dur), "-vf", vf,
                    "-r", "30", "-c:v", "libx264", "-preset", "fast",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                    str(out_part)
                ], capture_output=True)
        else:
            # 黑屏 + 音频
            subprocess.run([
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", f"color=c=black:s={w}x{h}:d={dur}:r=30",
                "-i", str(audio_seg),
                "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-shortest",
                str(out_part)
            ], capture_output=True)

        if out_part.exists():
            part_files.append(out_part)
            print(f"  [{i:2d}/{len(segments)}] {seg['scene']} ({dur:.1f}s)")

    # Phase 2: 拼接所有片段
    concat_list = tmp_dir / "concat.txt"
    with open(concat_list, "w") as f:
        for p in part_files:
            f.write(f"file '{p.resolve()}'\n")

    concat_output = tmp_dir / "concat.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(concat_output)
    ], capture_output=True)

    # Phase 3: 烧入字幕
    print(f"\n🔤 烧入字幕...")
    srt_escaped = str(srt_path.resolve()).replace("\\", "/").replace(":", "\\:")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(concat_output),
        "-vf", (
            f"subtitles='{srt_escaped}'"
            f":force_style='FontName=Microsoft YaHei,"
            f"FontSize=20,PrimaryColour=&HFFFFFF&,"
            f"OutlineColour=&H40000000&,BorderStyle=1,Outline=2,"
            f"Shadow=1,BackColour=&H40000000&,"
            f"MarginV=30,Alignment=2'"
        ),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "copy",
        str(output_path)
    ], capture_output=True)

    # 清理
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
