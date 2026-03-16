"""
视频组装器 v3 — 通用版
======================
输入：
  project_dir/
    narration/
      full_narration_myvoice.mp3  (或 full_narration_qwen.mp3)
      script.txt                   (旁白文本，用于生成字幕)
    visuals/
      scene_01.mp4 / scene_01.png  (Manim 动画或图片)
      scene_02.mp4 / scene_02.png
      ...

输出：
  project_dir/output/
    final.mp4                      (带字幕的成品)
    subtitles.srt                  (字幕文件)

用法:
  python assemble_video_v3.py <project_dir>
  python assemble_video_v3.py C:/workspace/video-content/machine-learning/knn

特性:
  - 自动从音频+文本生成 SRT 字幕（用 stable-ts 或音频时长均分）
  - Ken Burns 效果（图片自动添加缓慢推拉）
  - 字幕自动烧录到视频
  - 支持混合视频+图片素材
"""
import argparse
import subprocess
import json
import re
from pathlib import Path


def ffprobe_duration(file_path: Path) -> float:
    """获取音视频文件时长"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return float(r.stdout.strip())


def ffmpeg(args: list, desc: str = "") -> bool:
    """运行 ffmpeg，返回是否成功"""
    r = subprocess.run(
        ["ffmpeg", "-y"] + args,
        capture_output=True, text=True
    )
    if r.returncode != 0:
        stderr = (r.stderr or "")[-300:]
        print(f"  ❌ {desc}: {stderr}")
        return False
    return True


def find_audio(narr_dir: Path) -> Path | None:
    """按优先级查找音频文件"""
    priorities = [
        "full_narration_myvoice.mp3",
        "full_narration_qwen.mp3",
        "full_narration_continuous.mp3",
        "full_narration.mp3",
    ]
    for name in priorities:
        p = narr_dir / name
        if p.exists():
            return p
    # 找任何 mp3
    mp3s = list(narr_dir.glob("*.mp3"))
    return mp3s[0] if mp3s else None


def generate_srt_from_script(script_path: Path, audio_duration: float, output_path: Path):
    """
    从文本脚本生成 SRT 字幕。
    按字数均分时间，每行一段。
    """
    lines = [l.strip() for l in script_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    total_chars = sum(len(l) for l in lines)

    entries = []
    current_time = 0.0

    for i, line in enumerate(lines):
        # 按字数比例分配时间
        seg_duration = (len(line) / total_chars) * audio_duration
        start = current_time
        end = current_time + seg_duration
        current_time = end

        # 长段落拆成多条字幕（每条最多20字）
        chunks = []
        words = line
        while len(words) > 20:
            # 找标点断句
            cut = -1
            for punct in ['，', '。', '！', '？', '；', '、', ',', '.', '!', '?']:
                idx = words[:25].rfind(punct)
                if idx > 5:
                    cut = idx + 1
                    break
            if cut == -1:
                cut = 20
            chunks.append(words[:cut])
            words = words[cut:]
        if words:
            chunks.append(words)

        chunk_dur = seg_duration / len(chunks)
        for j, chunk in enumerate(chunks):
            cs = start + j * chunk_dur
            ce = start + (j + 1) * chunk_dur
            entries.append((cs, ce, chunk))

    # 写 SRT
    with open(output_path, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(entries):
            f.write(f"{i+1}\n")
            f.write(f"{_fmt_srt_time(start)} --> {_fmt_srt_time(end)}\n")
            f.write(f"{text}\n\n")

    print(f"  📝 生成 {len(entries)} 条字幕 → {output_path.name}")
    return output_path


def _fmt_srt_time(seconds: float) -> str:
    """格式化为 SRT 时间戳"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_visual_track(visuals_dir: Path, total_duration: float, tmp_dir: Path) -> Path:
    """
    从 visuals/ 目录构建视觉轨道。
    支持 .mp4（视频）和 .png/.jpg（图片，自动加 Ken Burns）。
    """
    files = sorted(visuals_dir.glob("scene_*"))
    if not files:
        # 没有视觉素材，生成纯黑视频
        print("  ⚠️ 无视觉素材，生成黑色背景")
        black = tmp_dir / "black.mp4"
        ffmpeg([
            "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:d={total_duration}:r=30",
            "-c:v", "libx264", "-preset", "fast",
            str(black)
        ], "black bg")
        return black

    # 均分时长
    seg_dur = total_duration / len(files)
    parts = []

    for i, f in enumerate(files):
        out = tmp_dir / f"visual_{i:03d}.mp4"

        if f.suffix in ('.mp4', '.mov', '.avi'):
            # 视频：拉伸/裁剪到目标时长
            vid_dur = ffprobe_duration(f)
            if vid_dur >= seg_dur:
                ffmpeg([
                    "-i", str(f), "-t", str(seg_dur),
                    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1",
                    "-c:v", "libx264", "-preset", "fast", "-an",
                    str(out)
                ], f"video {i}")
            else:
                # 冻结最后一帧
                ffmpeg([
                    "-i", str(f),
                    "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1,tpad=stop_mode=clone:stop_duration={seg_dur - vid_dur}",
                    "-c:v", "libx264", "-preset", "fast", "-an",
                    str(out)
                ], f"video {i}")

        elif f.suffix in ('.png', '.jpg', '.jpeg', '.webp'):
            # 图片：Ken Burns 推拉效果（平滑版）
            # 先用 lanczos 高质量缩放 + pad 到 2160x1216（保持比例），
            # 再用温和 zoompan（1% 缩放）避免小图抖动
            total_frames = int(seg_dur * 30)
            ffmpeg([
                "-loop", "1", "-i", str(f),
                "-vf", (
                    f"scale=2160:1216:force_original_aspect_ratio=decrease:flags=lanczos,"
                    f"pad=2160:1216:-1:-1:color=black,"
                    f"zoompan=z='1.02+0.01*on/{total_frames}'"
                    f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                    f":d={total_frames}:s=1920x1080:fps=30"
                ),
                "-t", str(seg_dur),
                "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                str(out)
            ], f"image {i}")

        if out.exists():
            parts.append(out)

    # 拼接
    concat_file = tmp_dir / "visual_concat.txt"
    with open(concat_file, "w", encoding="utf-8") as cf:
        for p in parts:
            cf.write(f"file '{p.resolve()}'\n")

    visual_track = tmp_dir / "visual_track.mp4"
    ffmpeg([
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", str(visual_track)
    ], "concat visuals")

    return visual_track


def assemble_final(visual_track: Path, audio_file: Path, srt_file: Path, output_path: Path):
    """合并视觉+音频+字幕 → 成品"""
    # 字幕样式：底部居中，白字黑边，微软雅黑
    srt_escaped = str(srt_file).replace("\\", "/").replace(":", "\\:")
    subtitle_filter = (
        f"subtitles='{srt_escaped}'"
        f":force_style='FontName=Microsoft YaHei,"
        f"FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,"
        f"BorderStyle=3,Outline=2,Shadow=0,MarginV=40'"
    )

    success = ffmpeg([
        "-i", str(visual_track),
        "-i", str(audio_file),
        "-vf", subtitle_filter,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_path)
    ], "final assembly with subtitles")

    if not success:
        # 字幕烧录失败，不带字幕合成
        print("  ⚠️ 字幕烧录失败，生成无字幕版本")
        ffmpeg([
            "-i", str(visual_track),
            "-i", str(audio_file),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(output_path)
        ], "final without subtitles")


def main():
    parser = argparse.ArgumentParser(description="视频组装器 v3")
    parser.add_argument("project_dir", type=str, help="项目目录")
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()

    print("=" * 60)
    print("🎬 视频组装器 v3")
    print(f"   项目: {project.name}")
    print("=" * 60)

    narr_dir = project / "narration"
    visuals_dir = project / "visuals"
    output_dir = project / "output"
    tmp_dir = output_dir / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # 1. 找音频
    audio_file = find_audio(narr_dir)
    if not audio_file:
        print("❌ 没找到旁白音频")
        return
    audio_dur = ffprobe_duration(audio_file)
    print(f"\n🎙 音频: {audio_file.name} ({audio_dur:.1f}s)")

    # 2. 生成字幕
    script_file = narr_dir / "script.txt"
    if not script_file.exists():
        script_file = narr_dir / "script_clean.txt"
    srt_file = output_dir / "subtitles.srt"

    if script_file.exists():
        generate_srt_from_script(script_file, audio_dur, srt_file)
    else:
        print("  ⚠️ 没找到脚本文件，将不含字幕")
        srt_file = None

    # 3. 构建视觉轨道
    print(f"\n🖼 构建视觉轨道...")
    if visuals_dir.exists():
        visual_track = build_visual_track(visuals_dir, audio_dur, tmp_dir)
    else:
        print("  ⚠️ 无 visuals/ 目录，生成黑色背景")
        visual_track = tmp_dir / "black.mp4"
        ffmpeg([
            "-f", "lavfi", "-i", f"color=c=#1a1a2e:s=1920x1080:d={audio_dur}:r=30",
            "-c:v", "libx264", "-preset", "fast",
            str(visual_track)
        ], "dark bg")

    # 4. 最终合成
    print(f"\n🔧 合成最终视频...")
    final_path = output_dir / "final.mp4"
    assemble_final(visual_track, audio_file, srt_file, final_path)

    # 5. 清理
    for f in tmp_dir.glob("*"):
        try:
            f.unlink()
        except:
            pass
    try:
        tmp_dir.rmdir()
    except:
        pass

    # 6. 结果
    if final_path.exists():
        dur = ffprobe_duration(final_path)
        size_mb = final_path.stat().st_size / 1024 / 1024
        print(f"\n{'=' * 60}")
        print(f"  ✅ 成品: {final_path}")
        print(f"  ⏱  时长: {dur:.0f}s ({dur/60:.1f}分钟)")
        print(f"  📦 大小: {size_mb:.1f} MB")
        if srt_file and srt_file.exists():
            print(f"  📝 字幕: {srt_file}")
        print(f"{'=' * 60}")
    else:
        print("  ❌ 合成失败")


if __name__ == "__main__":
    main()
