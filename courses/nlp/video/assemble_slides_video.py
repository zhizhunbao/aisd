"""
视频组装器（Marp PNG + TTS 版）
================================
输入：
  - narration/timestamps.json  (TTS 精确时间戳)
  - narration/full_narration_qwen.mp3  (TTS 音频)
  - slides/slide.001 ~ slide.NNN  (Marp PNG 图片)
  - narration/script.txt  (旁白稿)

输出：
  - output/final.mp4  (最终视频)
  - output/subtitles.srt  (字幕)

用法: python assemble_slides_video.py <project_dir>
"""
import subprocess
import json
import re
from pathlib import Path
import argparse
import shutil


RESOLUTION = (1920, 1080)


def main():
    parser = argparse.ArgumentParser(description="Marp PNG + TTS 视频组装器")
    parser.add_argument("project_dir")
    args = parser.parse_args()

    proj = Path(args.project_dir)
    narration_dir = proj / "narration"
    slides_dir = proj / "slides"
    output_dir = proj / "output"
    output_dir.mkdir(exist_ok=True)
    tmp_dir = output_dir / "tmp_build"
    tmp_dir.mkdir(exist_ok=True)

    # 1. 读取旁白
    script_path = narration_dir / "script.txt"
    lines = [l.strip().split("|")[0].strip() for l in script_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    n = len(lines)
    print(f"Narrations: {n} segments")

    # 2. 读取音频
    audio_path = find_audio(narration_dir)
    audio_dur = get_duration(audio_path)
    print(f"Audio: {audio_path.name} ({audio_dur:.1f}s)")

    # 3. 获取时间戳
    ts_path = narration_dir / "timestamps.json"
    if ts_path.exists():
        print("Time: Using TTS timestamps")
        segments = json.loads(ts_path.read_text(encoding="utf-8"))
    else:
        print("Time: Using proportional segments")
        segments = proportion_segments(lines, audio_dur)

    # 4. 查找 slides
    slide_files = sorted(slides_dir.glob("slide.*"))
    # 重命名确保 .png 扩展名
    for sf in slide_files:
        if not sf.suffix:
            new_name = sf.with_suffix(".png")
            sf.rename(new_name)
    slide_files = sorted(slides_dir.glob("slide.*.png")) or sorted(slides_dir.glob("slide.*"))
    print(f"Slides: Found {len(slide_files)} files")

    # 确保 segments 和 slides 数量匹配
    n_segs = min(len(segments), len(slide_files))
    segments = segments[:n_segs]

    # 5. 生成字幕
    srt_path = output_dir / "subtitles.srt"
    generate_srt(segments, srt_path)

    # 6. 生成幻灯片视频（不切割音频，避免 MP3 帧边界漂移）
    #    方案：先用 timestamps 生成纯图片视频轨，再与完整音频一次性合成
    w, h = RESOLUTION

    # 6a. 生成 ffmpeg concat demuxer 文件（每张 slide 按时间戳持续）
    concat_list = tmp_dir / "slides_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments):
            dur = seg["end"] - seg["start"]
            # 加上与下一段之间的间隔（静音期也显示当前 slide）
            if i + 1 < len(segments):
                gap = segments[i + 1]["start"] - seg["end"]
                dur += gap
            slide_path = slide_files[i] if i < len(slide_files) else None
            if slide_path and slide_path.exists():
                f.write(f"file '{slide_path.resolve()}'\n")
                f.write(f"duration {dur:.6f}\n")
            else:
                # 无 slide → 生成黑屏占位图
                black_img = tmp_dir / f"black_{i:02d}.png"
                subprocess.run([
                    "ffmpeg", "-y",
                    "-f", "lavfi", "-i", f"color=c=black:s={w}x{h}:d=1:r=1",
                    "-frames:v", "1", str(black_img)
                ], capture_output=True)
                f.write(f"file '{black_img.resolve()}'\n")
                f.write(f"duration {dur:.6f}\n")

            idx = seg.get("index", i + 1)
            slide_name = slide_path.name if slide_path else "black"
            print(f"  [{idx:2d}] {slide_name} -> {dur:.2f}s")

        # concat demuxer 需要最后一行再写一次最后的 file（否则最后一帧丢失）
        last_slide = slide_files[-1] if slide_files else None
        if last_slide and last_slide.exists():
            f.write(f"file '{last_slide.resolve()}'\n")

    # 6b. 合成纯视频轨（无音频）
    print(f"\n[Video] Generating slideshow track...")
    slideshow_path = tmp_dir / "slideshow.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,"
               f"pad={w}:{h}:-1:-1:color=black,"
               f"fps=30",
        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
        "-an",
        str(slideshow_path)
    ], capture_output=True)

    # 6c. 与完整音频一次性合成（零漂移）
    print(f"[Audio] Muxing audio and video...")
    concat_output = tmp_dir / "concat.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(slideshow_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(concat_output)
    ], capture_output=True)

    # 8. 烧入字幕
    print(f"\n[Subtitles] Burning subtitles...")
    srt_escaped = str(srt_path.resolve()).replace("\\", "/").replace(":", "\\:")

    subtitle_style = (
        f"subtitles='{srt_escaped}'"
        f":force_style='"
        f"FontName=Microsoft YaHei UI,"
        f"FontSize=26,"
        f"PrimaryColour=&HFFFFFF&,"
        f"OutlineColour=&H40000000&,"
        f"BackColour=&H40000000&,"
        f"BorderStyle=1,"
        f"Outline=3,"
        f"Shadow=1,"
        f"MarginV=20,"
        f"Alignment=2,"
        f"Bold=1"
        f"'"
    )

    final_path = output_dir / "final.mp4"
    result = subprocess.run([
        "ffmpeg", "-y", "-i", str(concat_output),
        "-vf", subtitle_style,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "copy",
        str(final_path)
    ], capture_output=True, text=True)

    if not final_path.exists():
        print(f"  Warning: Subtitle burn-in failed, creating version without subtitles")
        if result.stderr:
            print(f"  Error: {result.stderr[-300:]}")
        shutil.copy2(concat_output, final_path)

    # 清理
    shutil.rmtree(tmp_dir, ignore_errors=True)

    if final_path.exists():
        size_mb = final_path.stat().st_size / 1024 / 1024
        print(f"\nOK: {final_path} ({size_mb:.1f}MB)")
    else:
        print("\nERROR: Assembly failed")


def find_audio(narration_dir: Path) -> Path:
    for name in ["full_narration_myvoice.mp3", "full_narration_qwen.mp3", "full_narration.mp3"]:
        p = narration_dir / name
        if p.exists():
            return p
    mp3s = list(narration_dir.glob("*.mp3"))
    if mp3s:
        return mp3s[0]
    raise FileNotFoundError(f"在 {narration_dir} 中未找到 mp3 文件")


def get_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return float(r.stdout.strip())


def proportion_segments(lines, total_dur):
    char_counts = [len(line) for line in lines]
    total_chars = sum(char_counts)
    segments = []
    t = 0.0
    for i, line in enumerate(lines):
        dur = (char_counts[i] / total_chars) * total_dur
        segments.append({
            "index": i + 1,
            "start": round(t, 3),
            "end": round(t + dur, 3),
            "text": line,
        })
        t += dur
    return segments


def strip_punctuation(text: str) -> str:
    return re.sub(r'[，。！？、；：…——""''《》（）【】,.!?;:"\'\(\)\-]', '', text)


def generate_srt(segments, output_path, max_chars=28):
    cn_punct = set("，。！？、；：…—")
    en_punct = set(",!?;:.")

    srt_idx = 0
    with open(output_path, "w", encoding="utf-8-sig") as f:
        for seg in segments:
            text = seg.get("text", "")
            # 去掉视觉提示部分
            if "|" in text:
                text = text.split("|")[0].strip()
            seg_start = seg["start"]
            seg_end = seg["end"]
            seg_dur = seg_end - seg_start

            # 按标点分句
            sentences = split_by_punct(text, cn_punct | en_punct)
            merged = merge_short(sentences, 6)
            if not merged:
                continue

            # 长句拆分
            final_chunks = []
            for s in merged:
                if len(s) <= max_chars:
                    final_chunks.append(s)
                else:
                    final_chunks.extend(split_long(s, max_chars))

            # 去标点（短视频风格）
            final_chunks = [strip_punctuation(c).strip() for c in final_chunks]
            final_chunks = [c for c in final_chunks if c]

            total_chars = sum(len(c) for c in final_chunks)
            if total_chars == 0:
                continue

            t = seg_start
            for chunk in final_chunks:
                chunk_dur = (len(chunk) / total_chars) * seg_dur
                end_t = min(t + chunk_dur, seg_end)
                srt_idx += 1
                f.write(f"{srt_idx}\n")
                f.write(f"{fmt_time(t)} --> {fmt_time(end_t)}\n")
                f.write(f"{chunk}\n\n")
                t = end_t

    print(f"  SRT: {srt_idx} lines -> {output_path.name}")


def split_by_punct(text, punct):
    sentences = []
    current = ""
    for ch in text:
        current += ch
        if ch in punct:
            sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())
    return sentences


def merge_short(sentences, min_len=6):
    if not sentences:
        return []
    merged = []
    buf = ""
    for s in sentences:
        buf += s
        if len(buf) >= min_len:
            merged.append(buf)
            buf = ""
    if buf:
        if merged:
            merged[-1] += buf
        else:
            merged.append(buf)
    return merged


def split_long(text, max_chars):
    """拆分长句，不劈开英文单词/数字/引号内容。"""
    chunks = []
    current = ""
    i = 0
    while i < len(text):
        ch = text[i]
        # 英文单词保护（含连字符）
        if ch.isascii() and ch.isalpha():
            word = ""
            while i < len(text) and (text[i].isascii() and (text[i].isalpha() or text[i] in '-_')):
                word += text[i]
                i += 1
            if len(current) + len(word) > max_chars and current:
                chunks.append(current.strip())
                current = ""
            current += word
        # 数字保护（含后续量词）
        elif ch.isdigit():
            word = ""
            while i < len(text) and (text[i].isdigit() or text[i] in '.%'):
                word += text[i]
                i += 1
            if i < len(text) and text[i] in '年分倍次个级维亿万千百层':
                word += text[i]
                i += 1
            if len(current) + len(word) > max_chars and current:
                chunks.append(current.strip())
                current = ""
            current += word
        else:
            current += ch
            i += 1
            if len(current) >= max_chars:
                chunks.append(current.strip())
                current = ""
    if current.strip():
        chunks.append(current.strip())
    return chunks


def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


if __name__ == "__main__":
    main()
