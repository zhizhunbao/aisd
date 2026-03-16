"""
视频组装器 v6（精确对齐版）
=============================
核心改进：
  1. 字幕精确同步 — 优先读 timestamps.json（TTS 生成时导出），
     回退到 Whisper ASR，最后才用字数比例估算
  2. 不断词 — 中文按标点断句，英文按空格/标点断，绝不劈开单词
  3. 字体美观 — 思源黑体/微软雅黑 大号字，底部居中，半透明描边
  4. 场景映射 — 自动在 visuals/ 及 media/videos/ 子目录下查找

管线：timestamps.json / Whisper → 精确时间 → scene_N + audio_N → subtitle_N → 合并

用法: python assemble_video_v6.py <project_dir>
"""
import subprocess
import json
import re
from pathlib import Path
import argparse

RESOLUTION = (1920, 1080)


def main():
    parser = argparse.ArgumentParser(description="视频组装器 v6（精确对齐版）")
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
    audio_path = find_audio(narration_dir)
    audio_dur = get_duration(audio_path)
    print(f"🎙 音频: {audio_path.name} ({audio_dur:.1f}s)")

    # ============================================================
    # 获取精确时间戳（三级回退）
    # ============================================================
    ts_path = narration_dir / "timestamps.json"
    if ts_path.exists():
        # 🥇 最优：TTS 导出的精确时间戳
        print("⏱ 使用 TTS 时间戳 (timestamps.json)")
        segments = json.loads(ts_path.read_text(encoding="utf-8"))
    else:
        # 🥈 次优：Whisper ASR
        print("⏱ 未找到 timestamps.json, 尝试 Whisper...")
        segments = try_whisper(audio_path, lines)
        if segments is None:
            # 🥉 保底：静音检测 + 字数比例
            print("⏱ Whisper 不可用, 使用静音检测 + 字数比例")
            segments = detect_by_silence_or_proportion(audio_path, lines, audio_dur)

    print(f"✂️ {len(segments)} 个分段")
    for s in segments:
        dur = s["end"] - s["start"]
        print(f"  段{s['index']:2d}: {s['start']:6.1f}s ~ {s['end']:6.1f}s ({dur:5.1f}s) {s['text'][:30]}...")

    # 查找视频场景文件
    scene_map = build_scene_map(visuals_dir, n)

    # 生成字幕（不断词版）
    srt_path = output_dir / "subtitles.srt"
    generate_srt(segments, srt_path)

    # 保存分段信息
    with open(output_dir / "segments.json", "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    # 组装视频
    final_path = output_dir / "final_v6.mp4"
    assemble(segments, scene_map, visuals_dir, audio_path, srt_path, final_path)

    if final_path.exists():
        size_mb = final_path.stat().st_size / 1024 / 1024
        print(f"\n✅ 完成: {final_path} ({size_mb:.1f}MB)")
    else:
        print("\n❌ 组装失败")


# ==============================================================
# 音频工具
# ==============================================================

def find_audio(narration_dir: Path) -> Path:
    """按优先级查找音频文"""
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


# ==============================================================
# 时间戳获取（三级回退）
# ==============================================================

def try_whisper(audio_path: Path, lines: list[str]) -> list[dict] | None:
    """尝试用 faster-whisper 获取逐句时间戳"""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("  ⚠️ faster-whisper 未安装 (pip install faster-whisper)")
        return None

    try:
        print("  ⏳ 加载 Whisper large-v3...")
        model = WhisperModel("large-v3", device="cuda", compute_type="float16")
        whisper_segments, info = model.transcribe(
            str(audio_path), language="zh", word_timestamps=True,
            vad_filter=True,
        )
        whisper_segments = list(whisper_segments)
        print(f"  ✅ Whisper 识别到 {len(whisper_segments)} 段")

        # 匹配 Whisper 段落到脚本行
        # 策略：按时间顺序,将 Whisper 段落合并到脚本行
        if len(whisper_segments) == len(lines):
            # 完美匹配
            return [
                {
                    "index": i + 1,
                    "start": round(ws.start, 3),
                    "end": round(ws.end, 3),
                    "text": lines[i],
                    "scene": f"scene_{i+1:02d}.mp4",
                }
                for i, ws in enumerate(whisper_segments)
            ]
        else:
            # Whisper 段数 ≠ 脚本行数，需要合并
            return merge_whisper_to_script(whisper_segments, lines)
    except Exception as e:
        print(f"  ⚠️ Whisper 失败: {e}")
        return None


def merge_whisper_to_script(whisper_segs, lines: list[str]) -> list[dict]:
    """将数量不匹配的 Whisper 段落合并到脚本行"""
    n = len(lines)
    total_dur = whisper_segs[-1].end if whisper_segs else 0

    # 简单策略：按时间均分边界，每段脚本对应一个时间区间
    segments = []
    # 收集所有 Whisper 分段的开始时间作为候选边界
    all_starts = [ws.start for ws in whisper_segs]
    all_ends = [ws.end for ws in whisper_segs]

    # 按字数比例分配预期边界
    char_counts = [len(line) for line in lines]
    total_chars = sum(char_counts)
    boundaries = [0.0]
    t = 0.0
    for cc in char_counts[:-1]:
        t += (cc / total_chars) * total_dur
        # 找最近的 Whisper 边界
        best = min(all_ends, key=lambda x: abs(x - t))
        boundaries.append(best)
    boundaries.append(total_dur)

    for i, text in enumerate(lines):
        segments.append({
            "index": i + 1,
            "start": round(boundaries[i], 3),
            "end": round(boundaries[i + 1], 3),
            "text": text,
            "scene": f"scene_{i+1:02d}.mp4",
        })
    return segments


def detect_by_silence_or_proportion(audio_path: Path, lines: list[str],
                                     total_dur: float) -> list[dict]:
    """静音检测分段；静音点不够时按字数比例"""
    # FFmpeg 静音检测
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", "silencedetect=noise=-30dB:d=0.15",
        "-f", "null", "-"
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    stderr = r.stderr

    silence_mids = []
    starts, ends = [], []
    for line in stderr.split("\n"):
        m = re.search(r"silence_start:\s*([\d.]+)", line)
        if m:
            starts.append(float(m.group(1)))
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m:
            ends.append(float(m.group(1)))

    for i in range(min(len(starts), len(ends))):
        mid = (starts[i] + ends[i]) / 2
        silence_mids.append(mid)

    print(f"  🔇 检测到 {len(silence_mids)} 个静音点")

    n = len(lines)
    n_needed = n - 1

    if len(silence_mids) >= n_needed:
        # 取间隔最大的 n_needed 个静音作为边界
        # 策略：按字数比例预测边界，然后找最近的静音点
        char_counts = [len(line) for line in lines]
        total_chars = sum(char_counts)
        boundaries = [0.0]
        t = 0.0
        used = set()
        for cc in char_counts[:-1]:
            t += (cc / total_chars) * total_dur
            # 找最近的未使用静音点
            best_idx = min(
                [j for j in range(len(silence_mids)) if j not in used],
                key=lambda j: abs(silence_mids[j] - t)
            )
            used.add(best_idx)
            boundaries.append(silence_mids[best_idx])
        boundaries.append(total_dur)
    else:
        # 静音点不够，纯字数比例
        char_counts = [len(line) for line in lines]
        total_chars = sum(char_counts)
        boundaries = [0.0]
        t = 0.0
        for cc in char_counts[:-1]:
            t += (cc / total_chars) * total_dur
            boundaries.append(t)
        boundaries.append(total_dur)

    segments = []
    for i, text in enumerate(lines):
        segments.append({
            "index": i + 1,
            "start": round(boundaries[i], 3),
            "end": round(boundaries[i + 1], 3),
            "text": text,
            "scene": f"scene_{i+1:02d}.mp4",
        })
    return segments


# ==============================================================
# 场景文件映射
# ==============================================================

def build_scene_map(visuals_dir: Path, n: int) -> dict[int, Path]:
    """
    构建场景编号 → 视频文件路径 的映射。
    搜索顺序：
      1. visuals/scene_01.mp4
      2. visuals/media/videos/*/1080p60/Scene01*.mp4
      3. visuals/media/videos/*/720p30/Scene01*.mp4
    """
    scene_map = {}

    for i in range(1, n + 1):
        # 优先: visuals/scene_XX.mp4
        direct = visuals_dir / f"scene_{i:02d}.mp4"
        if direct.exists():
            scene_map[i] = direct
            continue

        # 次优: Manim 输出目录
        found = False
        for res in ["1080p60", "720p30", "480p15"]:
            pattern = f"Scene{i:02d}*.mp4"
            matches = list(visuals_dir.rglob(f"*/{res}/{pattern}"))
            if matches:
                scene_map[i] = matches[0]
                found = True
                break

        if not found:
            # 最后: 任何 SceneXX*.mp4
            pattern = f"Scene{i:02d}*.mp4"
            matches = list(visuals_dir.rglob(pattern))
            if matches:
                scene_map[i] = matches[0]
            else:
                print(f"  ⚠️ 缺少场景 {i}: scene_{i:02d}.mp4")

    for i, path in scene_map.items():
        print(f"  🎬 场景{i:2d} → {path.name}")

    return scene_map


# ==============================================================
# 字幕生成（不断词版）
# ==============================================================

def strip_punctuation(text: str) -> str:
    """去掉所有中英文标点，短视频字幕风格"""
    import re
    return re.sub(r'[，。！？、；：…——""''《》（）【】,.!?;:"\'\(\)\-]', '', text)


def generate_srt(segments: list[dict], output_path: Path, max_chars: int = 18):
    """
    短视频风格字幕：按标点断句，绝不劈开词，输出无标点。
    规则：
      1. 优先在中文标点处断开（利用标点做断句依据）
      2. 英文单词不拆分（保持完整 word）
      3. 每条字幕 ≤ max_chars 字
      4. 过短分句（< 4字）与前句合并
      5. 最终输出去掉所有标点（短视频风格）
    """
    # 中英文标点
    cn_punct = set("，。！？、；：…—")
    en_punct = set(",!?;:.")

    srt_idx = 0
    with open(output_path, "w", encoding="utf-8-sig") as f:
        for seg in segments:
            text = seg["text"]
            seg_start = seg["start"]
            seg_end = seg["end"]
            seg_dur = seg_end - seg_start

            # Step 1: 按标点分句（标点仍用于断句逻辑）
            sentences = split_by_punctuation(text, cn_punct | en_punct)

            # Step 2: 合并过短的句子
            merged = merge_short(sentences, min_len=6)
            if not merged:
                continue

            # Step 3: 长句再拆（按 max_chars，不断英文词）
            final_chunks = []
            for s in merged:
                if len(s) <= max_chars:
                    final_chunks.append(s)
                else:
                    final_chunks.extend(split_long_sentence(s, max_chars))

            # Step 4: 去掉标点（短视频风格，字幕不带标点）
            final_chunks = [strip_punctuation(c).strip() for c in final_chunks]
            final_chunks = [c for c in final_chunks if c]  # 去空

            # Step 5: 按字数比例分配时间
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

    print(f"  📝 {srt_idx} 条字幕 → {output_path.name}")


def split_by_punctuation(text: str, punct: set) -> list[str]:
    """按标点位置将文本分成句子（保留标点在句尾）"""
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


def merge_short(sentences: list[str], min_len: int = 6) -> list[str]:
    """合并过短的句子"""
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


def split_long_sentence(text: str, max_chars: int) -> list[str]:
    """
    拆分长句，不劈开英文单词。
    策略：逐字符扫描，保护以下原子单元不被拆开：
      - 英文单词（含连字符如 KD-Tree）
      - 数字+后缀（如 1951年、100分、50%）
      - 引号内容（如 "找邻居"）
    """
    chunks = []
    current = ""
    i = 0
    while i < len(text):
        ch = text[i]

        # 引号保护："xxx" 或 \"xxx\" 整体不拆
        if ch in '""\\"':
            word = ch
            i += 1
            # 找到匹配的关闭引号
            close_chars = {'"': '"', '"': '"', '\\"': '\\"'}
            close = close_chars.get(ch, '"')
            while i < len(text) and text[i] != close:
                word += text[i]
                i += 1
            if i < len(text):
                word += text[i]
                i += 1
            if len(current) + len(word) > max_chars and current:
                chunks.append(current.strip())
                current = ""
            current += word

        # 英文单词保护（含连字符）
        elif ch.isascii() and ch.isalpha():
            word = ""
            while i < len(text) and (text[i].isascii() and (text[i].isalpha() or text[i] in '-_')):
                word += text[i]
                i += 1
            if len(current) + len(word) > max_chars and current:
                chunks.append(current.strip())
                current = ""
            current += word

        # 数字保护（含后续 中文量词/单位）
        elif ch.isdigit():
            word = ""
            while i < len(text) and (text[i].isdigit() or text[i] in '.%'):
                word += text[i]
                i += 1
            # 后接中文量词（年/分/倍/次/个/级/维 等）一起保护
            if i < len(text) and text[i] in '年分倍次个级维亿万千百':
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


def fmt_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ==============================================================
# 视频组装
# ==============================================================

def assemble(segments: list[dict], scene_map: dict[int, Path],
             visuals_dir: Path, audio_path: Path,
             srt_path: Path, output_path: Path):
    """1:1 组装：每段音频 + 对应 Manim 视频 → 拼接 → 字幕"""
    w, h = RESOLUTION
    tmp_dir = output_path.parent / "tmp_v6"
    tmp_dir.mkdir(exist_ok=True)

    print(f"\n🎬 组装 {len(segments)} 段...")

    # Phase 1: 为每段生成 视频+音频 片段
    part_files = []
    for seg in segments:
        i = seg["index"]
        dur = seg["end"] - seg["start"]
        scene_path = scene_map.get(i)
        out_part = tmp_dir / f"part_{i:02d}.mp4"

        # 提取音频段
        audio_seg = tmp_dir / f"audio_{i:02d}.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(audio_path),
            "-ss", str(seg["start"]), "-t", str(dur),
            "-c", "copy", str(audio_seg)
        ], capture_output=True)

        vf = f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:-1:-1:color=black"

        if scene_path and scene_path.exists():
            vid_dur = get_duration(scene_path)

            if vid_dur >= dur:
                # 视频够长，截取
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(scene_path), "-i", str(audio_seg),
                    "-t", str(dur), "-vf", vf,
                    "-r", "30", "-c:v", "libx264", "-preset", "fast",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                    str(out_part)
                ], capture_output=True)
            else:
                # 视频太短，冻结最后一帧
                vf_ext = (f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,"
                          f"pad={w}:{h}:-1:-1:color=black,"
                          f"tpad=stop_mode=clone:stop_duration={dur - vid_dur + 0.5:.2f}")
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(scene_path), "-i", str(audio_seg),
                    "-t", str(dur), "-vf", vf_ext,
                    "-r", "30", "-c:v", "libx264", "-preset", "fast",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                    str(out_part)
                ], capture_output=True)
        else:
            # 无场景 → 黑屏 + 音频
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
            print(f"  [{i:2d}/{len(segments)}] {scene_path.name if scene_path else 'black'} ({dur:.1f}s)")

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

    # 字体优先级: 思源黑体 > 微软雅黑 > Noto Sans CJK
    subtitle_style = (
        f"subtitles='{srt_escaped}'"
        f":force_style='"
        f"FontName=Microsoft YaHei UI,"  # Windows 自带的雅黑
        f"FontSize=24,"                   # 大号字，短视频标准
        f"PrimaryColour=&HFFFFFF&,"       # 纯白
        f"OutlineColour=&H40000000&,"     # 半透明黑描边
        f"BackColour=&H40000000&,"        # 半透明背景
        f"BorderStyle=1,"                 # 描边 + 阴影
        f"Outline=3,"                     # 描边粗细
        f"Shadow=1,"                      # 阴影
        f"MarginV=15,"                    # 紧贴底部，不挡画面
        f"Alignment=2,"                   # 底部居中
        f"Bold=1"                         # 加粗
        f"'"
    )

    result = subprocess.run([
        "ffmpeg", "-y", "-i", str(concat_output),
        "-vf", subtitle_style,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "copy",
        str(output_path)
    ], capture_output=True, text=True)

    if not output_path.exists():
        print(f"  ⚠️ 字幕烧入失败: {result.stderr[-500:]}")
        # 不带字幕版
        print(f"  🔄 生成无字幕版...")
        subprocess.run([
            "ffmpeg", "-y", "-i", str(concat_output),
            "-c", "copy", str(output_path)
        ], capture_output=True)

    # 清理
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
