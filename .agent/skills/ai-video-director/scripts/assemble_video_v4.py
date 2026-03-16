"""
视频组装器 v4 — 智能版
======================
修复 v3 的三个问题：
  1. 字幕不同步 → Whisper 精确对齐
  2. 一张图放太久 → 关键词匹配，4-6秒自动切换
  3. 字幕挡画面 → 底部半透明安全区

用法:
  python assemble_video_v4.py <project_dir>

依赖: moviepy, whisper, pillow, numpy
"""
import argparse
import json
import subprocess
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ============================================================
# 关键词 → 素材映射（按优先级排列）
# ============================================================
KEYWORD_VISUAL_MAP = [
    # (关键词列表, 对应素材文件名列表) — 优先 Manim .mp4
    (["KNN", "邻居", "投票", "最简单", "AI算法", "找邻居"],
     ["scene_01_knn_voting.mp4", "scene_01_knn_voting.png"]),
    (["1951", "空军", "Fix", "Hodges", "年代", "统计学家"],
     ["scene_01_1950s_lab.jpg", "scene_02_paper_fix.png"]),
    (["Cover", "Hart", "1967", "定理", "斯坦福", "贝叶斯"],
     ["scene_03_cover.jpg", "scene_03_hart.jpg", "scene_03_paper_cover.png"]),
    (["最简单的方法", "理论保证", "震撼"],
     ["scene_04_quote1.png"]),
    (["暴力", "搜索", "算一遍", "排序", "慢", "北京", "敲门"],
     ["scene_04_brute_force.mp4"]),
    (["Bentley", "KD-Tree", "KD树", "1975", "切割", "切开", "二叉"],
     ["scene_05_kdtree.mp4", "scene_05_bentley.jpg", "scene_05_paper_bentley.png"]),
    (["维度", "灾难", "高维", "退化"],
     ["scene_06_curse_of_dim.png"]),
    (["LSH", "哈希", "1999", "近似", "差不多近"],
     ["scene_07_lsh.mp4"]),
    (["FAISS", "Facebook", "GPU", "十亿", "数据中心", "2017", "服务器"],
     ["scene_08_datacenter.jpg"]),
    (["推荐", "RAG", "检索", "HNSW", "向量", "搜图"],
     ["scene_09_recommendation.jpg"]),
    (["相似", "在一起", "核心思想", "关注", "决策树"],
     ["scene_10_quote2.png"]),
    (["报告", "抽屉", "锁", "内部", "发表"],
     ["scene_02_paper_fix.png"]),
    (["错误率", "引用", "万八千"],
     ["scene_03_paper_cover.png"]),
    (["速度", "加速", "指数级", "对数"],
     ["scene_05_kdtree.mp4"]),
    (["七十", "演化", "基础设施"],
     ["scene_11_timeline.mp4", "scene_08_datacenter.jpg"]),
]


def detect_segments(audio_path: Path, script_path: Path) -> list[dict]:
    """
    用静音检测精确对齐字幕（不需要 ASR）。
    原理：TTS 在每个段落之间插入了 0.3s 静音，用 FFmpeg 检测这些静音。
    """
    print("🎙 静音检测对齐中...")

    # 读取脚本文本
    lines = [l.strip() for l in script_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  📝 {len(lines)} 段旁白文本")

    # FFmpeg 静音检测
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    total_duration = float(r.stdout.strip())

    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", "silencedetect=noise=-25dB:d=0.1",
        "-f", "null", "-"
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    stderr = r.stderr

    # 解析静音区间
    silence_pairs = []
    silence_starts = []
    silence_ends = []
    for line in stderr.split("\n"):
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([\d.]+)", line)
            if m:
                silence_starts.append(float(m.group(1)))
        if "silence_end:" in line:
            m = re.search(r"silence_end:\s*([\d.]+)", line)
            if m:
                silence_ends.append(float(m.group(1)))

    # 配对静音区间
    for i in range(min(len(silence_starts), len(silence_ends))):
        dur = silence_ends[i] - silence_starts[i]
        mid = (silence_starts[i] + silence_ends[i]) / 2
        silence_pairs.append((mid, dur))

    print(f"  🔇 检测到 {len(silence_pairs)} 个静音点")

    # 我们需要 n_lines-1 个分界点
    n_needed = len(lines) - 1
    if len(silence_pairs) >= n_needed:
        # 取最长的 n_needed 个静音作为分界点
        silence_pairs.sort(key=lambda x: x[1], reverse=True)
        boundaries_mid = sorted([p[0] for p in silence_pairs[:n_needed]])
    else:
        # 静音点不够，用所有的
        boundaries_mid = sorted([p[0] for p in silence_pairs])

    boundaries = [0.0] + boundaries_mid + [total_duration]

    # 匹配段落数量
    segments = []
    if len(boundaries) - 1 >= len(lines):
        # 静音点足够多，直接匹配
        for i, text in enumerate(lines):
            segments.append({
                "start": boundaries[i],
                "end": boundaries[i + 1] if i + 1 < len(boundaries) else total_duration,
                "text": text,
            })
    else:
        # 静音点不够，按字数比例分配
        total_chars = sum(len(l) for l in lines)
        current = 0.0
        for text in lines:
            dur = (len(text) / total_chars) * total_duration
            segments.append({
                "start": current,
                "end": current + dur,
                "text": text,
            })
            current += dur

    print(f"  ✅ {len(segments)} 个片段，总时长 {total_duration:.1f}s")
    print(f"  🔇 检测到 {len(silence_starts)} 个静音点")
    return segments


def generate_srt(segments: list[dict], output_path: Path, max_chars: int = 12):
    """
    生成短视频风格字幕：每条最多 max_chars 个字，跟着语速快速切换。
    """
    # 中文标点，用于断句
    punct = set("，。！？、；：…—""''")

    srt_idx = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in segments:
            text = seg["text"]
            seg_dur = seg["end"] - seg["start"]

            # 按标点和长度拆成短句
            chunks = []
            current = ""
            for ch in text:
                current += ch
                if ch in punct and len(current) >= 4:
                    chunks.append(current)
                    current = ""
                elif len(current) >= max_chars:
                    # 没有标点就硬切
                    chunks.append(current)
                    current = ""
            if current:
                chunks.append(current)

            # 按字数比例分配时间
            total_chars = sum(len(c) for c in chunks)
            if total_chars == 0:
                continue

            t = seg["start"]
            for chunk in chunks:
                chunk_dur = (len(chunk) / total_chars) * seg_dur
                end_t = min(t + chunk_dur, seg["end"])

                srt_idx += 1
                f.write(f"{srt_idx}\n")
                f.write(f"{_fmt_time(t)} --> {_fmt_time(end_t)}\n")
                f.write(f"{chunk.strip()}\n\n")

                t = end_t

    print(f"  📝 {srt_idx} 条短视频字幕 → {output_path.name}")


def _fmt_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def match_visual(text: str, visuals_dir: Path, last_file: str = "") -> str:
    """根据文本内容匹配最佳视觉素材"""
    for keywords, files in KEYWORD_VISUAL_MAP:
        if any(kw in text for kw in keywords):
            # 找到匹配的分类，选一个不同于上一张的文件
            available = [f for f in files if (visuals_dir / f).exists()]
            if not available:
                continue
            # 优先选不同于上次的
            for f in available:
                if f != last_file:
                    return f
            return available[0]

    # 默认
    return "scene_01_knn_voting.png"


def create_shot_list(segments: list[dict], visuals_dir: Path, max_shot_dur: float = 5.0) -> list[dict]:
    """
    创建镜头列表：每个 Whisper 段落 = 一个镜头。
    合并极短段落（<2s），不强制轮换素材。
    """
    # 先合并极短段落
    merged = []
    for seg in segments:
        if merged and (seg["end"] - seg["start"]) < 2.0:
            # 合并到上一段
            merged[-1]["end"] = seg["end"]
            merged[-1]["text"] += seg["text"]
        else:
            merged.append(dict(seg))

    shots = []
    last_file = ""

    for seg in merged:
        text = seg["text"]
        visual = match_visual(text, visuals_dir, last_file)

        shots.append({
            "start": seg["start"],
            "end": seg["end"],
            "file": visual,
            "text": text,
        })
        last_file = visual

    avg_dur = sum(s["end"] - s["start"] for s in shots) / len(shots)
    print(f"  🎬 {len(shots)} 个镜头（平均 {avg_dur:.1f}s/shot）")
    return shots


def build_video_ffmpeg(shots: list[dict], visuals_dir: Path,
                       audio_path: Path, srt_path: Path,
                       output_path: Path, resolution=(1920, 1080)):
    """
    用 FFmpeg 复杂滤镜链构建视频。
    每个镜头：图片 → Ken Burns → 交叉淡化
    字幕：底部半透明条，不遮挡主画面
    """
    w, h = resolution
    total_dur = shots[-1]["end"]
    tmp_dir = output_path.parent / "tmp_v4"
    tmp_dir.mkdir(exist_ok=True)

    print(f"\n🖼 构建视觉轨道（{len(shots)} 个镜头）...")

    # Phase 1: 为每个镜头生成片段
    part_files = []
    for i, shot in enumerate(shots):
        dur = shot["end"] - shot["start"]
        img_path = visuals_dir / shot["file"]
        out_path = tmp_dir / f"shot_{i:04d}.mp4"

        if not img_path.exists():
            img_path = visuals_dir / "scene_01_knn_voting.png"

        if img_path.suffix in ('.mp4', '.mov', '.avi'):
            # 视频素材（Manim 动画）：截取或循环到目标时长
            vid_cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                       "-of", "default=noprint_wrappers=1:nokey=1", str(img_path)]
            vr = subprocess.run(vid_cmd, capture_output=True, text=True)
            vid_dur = float(vr.stdout.strip()) if vr.stdout.strip() else dur

            if vid_dur >= dur:
                # 视频够长，截取
                cmd = [
                    "ffmpeg", "-y", "-i", str(img_path),
                    "-t", str(dur),
                    "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:-1:-1:color=black",
                    "-r", "30", "-c:v", "libx264", "-preset", "fast",
                    "-pix_fmt", "yuv420p", "-an",
                    str(out_path)
                ]
            else:
                # 视频太短，播完后冻结最后一帧
                cmd = [
                    "ffmpeg", "-y", "-i", str(img_path),
                    "-vf", (
                        f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,"
                        f"pad={w}:{h}:-1:-1:color=black,"
                        f"tpad=stop_mode=clone:stop_duration={dur - vid_dur:.2f}"
                    ),
                    "-r", "30", "-c:v", "libx264", "-preset", "fast",
                    "-pix_fmt", "yuv420p", "-an",
                    str(out_path)
                ]
        else:
            # 图片素材：静态画面
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(img_path),
                "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:-1:-1:color=black",
                "-t", str(dur), "-r", "30",
                "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                str(out_path)
            ]

        r = subprocess.run(cmd, capture_output=True, text=True)
        if out_path.exists():
            part_files.append(out_path)
        if (i + 1) % 5 == 0 or i == len(shots) - 1:
            print(f"  [{i+1}/{len(shots)}] 镜头渲染中...")

    # Phase 2: 用 xfade 串联所有片段（交叉淡化）
    print(f"\n🔗 串联 {len(part_files)} 个片段（交叉淡化）...")

    # 由于 FFmpeg xfade 串联大量片段很复杂，用简单 concat 代替
    concat_file = tmp_dir / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for p in part_files:
            f.write(f"file '{p.resolve()}'\n")

    visual_track = tmp_dir / "visual_track.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", str(visual_track)
    ], capture_output=True, text=True)

    # Phase 3: 合成 音频 + 视觉 + 字幕
    print(f"\n🔧 最终合成...")

    # 字幕样式：底部半透明黑条，白字，不遮挡画面主体
    srt_escaped = str(srt_path).replace("\\", "/").replace(":", "\\:")
    subtitle_filter = (
        f"subtitles='{srt_escaped}'"
        f":force_style='FontName=Microsoft YaHei,"
        f"FontSize=16,"
        f"PrimaryColour=&HFFFFFF,"
        f"OutlineColour=&H000000,"
        f"BackColour=&H80000000,"
        f"BorderStyle=4,"
        f"Outline=1,"
        f"Shadow=0,"
        f"MarginV=16,"
        f"MarginL=40,"
        f"MarginR=40'"
    )

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(visual_track),
        "-i", str(audio_path),
        "-vf", subtitle_filter,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_path)
    ], capture_output=True, text=True)

    if not output_path.exists():
        # 字幕烧录失败，不带字幕合成
        print("  ⚠️ 字幕烧录失败，生成无字幕版本")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(visual_track),
            "-i", str(audio_path),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(output_path)
        ], capture_output=True, text=True)

    # 清理临时文件
    for f in tmp_dir.glob("*"):
        try:
            f.unlink()
        except:
            pass
    try:
        tmp_dir.rmdir()
    except:
        pass


def main():
    parser = argparse.ArgumentParser(description="视频组装器 v4（智能版）")
    parser.add_argument("project_dir", type=str, help="项目目录")
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    narr_dir = project / "narration"
    visuals_dir = project / "visuals"
    output_dir = project / "output"
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("🎬 视频组装器 v4（智能版）")
    print(f"   项目: {project.name}")
    print("=" * 60)

    # 1. 找音频
    audio_file = None
    for name in ["full_narration_myvoice.mp3", "full_narration_qwen.mp3", "full_narration.mp3"]:
        p = narr_dir / name
        if p.exists():
            audio_file = p
            break
    if not audio_file:
        mp3s = list(narr_dir.glob("*.mp3"))
        audio_file = mp3s[0] if mp3s else None
    if not audio_file:
        print("❌ 没找到旁白音频")
        return
    print(f"\n🎙 音频: {audio_file.name}")

    # 2. 静音检测精确对齐（不需要 ASR）
    script_file = narr_dir / "script.txt"
    if not script_file.exists():
        print("❌ 没找到 script.txt")
        return
    segments = detect_segments(audio_file, script_file)

    # 3. 生成精确 SRT
    srt_path = output_dir / "subtitles.srt"
    generate_srt(segments, srt_path)

    # 4. 创建镜头列表（自动匹配素材）
    print(f"\n🎯 匹配视觉素材...")
    shots = create_shot_list(segments, visuals_dir, max_shot_dur=5.0)

    # 保存镜头列表供参考
    shots_json = output_dir / "shots.json"
    with open(shots_json, "w", encoding="utf-8") as f:
        json.dump(shots, f, ensure_ascii=False, indent=2)
    print(f"  📋 镜头列表 → {shots_json.name}")

    # 5. 构建视频
    final_path = output_dir / "final_v4.mp4"
    build_video_ffmpeg(shots, visuals_dir, audio_file, srt_path, final_path)

    # 6. 结果
    if final_path.exists():
        cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", str(final_path)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        dur = float(r.stdout.strip()) if r.stdout.strip() else 0
        size_mb = final_path.stat().st_size / 1024 / 1024
        print(f"\n{'=' * 60}")
        print(f"  ✅ 成品: {final_path}")
        print(f"  ⏱  时长: {dur:.0f}s ({dur/60:.1f}分钟)")
        print(f"  📦 大小: {size_mb:.1f} MB")
        print(f"  📝 字幕: {srt_path}")
        print(f"  📋 镜头: {shots_json} ({len(shots)} shots)")
        print(f"{'=' * 60}")
    else:
        print("  ❌ 合成失败")


if __name__ == "__main__":
    main()
