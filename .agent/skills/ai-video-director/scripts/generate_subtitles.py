"""
精准字幕生成器 — FunASR SenseVoice（阿里开源，中文识别最强）
===========================================================
从音频生成精准 SRT 字幕，带时间戳对齐。

Usage:
    python generate_subtitles.py <audio_file> [--output subtitles.srt]

示例:
    python generate_subtitles.py narration/full_narration_myvoice.mp3
    python generate_subtitles.py narration/full_narration_myvoice.mp3 --output output/subtitles.srt

依赖:
    pip install -U funasr modelscope
    首次运行自动下载模型（~1GB）

输出:
    SRT 字幕文件，每条 ≤20 字，精准时间戳
"""
import argparse
from pathlib import Path


def fmt_srt_time(ms: int) -> str:
    """毫秒 → SRT 时间格式"""
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    ms_r = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms_r:03d}"


def split_text(text: str, max_len: int = 20) -> list[str]:
    """长文本按标点拆分，每条不超过 max_len 字"""
    if len(text) <= max_len:
        return [text]

    chunks = []
    remaining = text
    while len(remaining) > max_len:
        cut = -1
        for punct in ['，', '。', '！', '？', '；', '、', ',', '.', '!', '?', ' ']:
            idx = remaining[:max_len + 5].rfind(punct)
            if 5 < idx <= max_len + 2:
                cut = idx + 1
                break
        if cut == -1:
            cut = max_len
        chunks.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    if remaining:
        chunks.append(remaining)
    return chunks


def generate_with_funasr(audio_path: Path, output_path: Path):
    """用 FunASR SenseVoice 生成精准字幕"""
    from funasr import AutoModel

    print("⏳ 加载 SenseVoice 模型...")
    # paraformer-zh: 中文语音识别，带时间戳
    model = AutoModel(
        model="paraformer-zh",
        vad_model="fsmn-vad",
        punc_model="ct-punc",
        device="cuda:0",
    )

    print(f"🎙 识别: {audio_path.name}")
    result = model.generate(
        input=str(audio_path),
        batch_size_s=300,
    )

    entries = []
    idx = 1

    for item in result:
        if "sentence_info" in item:
            # 有句级时间戳
            for sent in item["sentence_info"]:
                text = sent.get("text", "").strip()
                start_ms = sent.get("start", 0)
                end_ms = sent.get("end", 0)

                if not text:
                    continue

                # 拆分长句
                chunks = split_text(text)
                chunk_dur = (end_ms - start_ms) / len(chunks) if chunks else 0

                for j, chunk in enumerate(chunks):
                    cs = int(start_ms + j * chunk_dur)
                    ce = int(start_ms + (j + 1) * chunk_dur)
                    entries.append((idx, cs, ce, chunk))
                    idx += 1
        elif "text" in item:
            # 无句级时间戳，用整体时间戳
            text = item["text"].strip()
            if "timestamp" in item:
                timestamps = item["timestamp"]
                for ts in timestamps:
                    word = ts[0] if isinstance(ts[0], str) else ""
                    start_ms = ts[1] if len(ts) > 1 else 0
                    end_ms = ts[2] if len(ts) > 2 else start_ms + 500
                    if word.strip():
                        entries.append((idx, start_ms, end_ms, word))
                        idx += 1
            else:
                # 完全没有时间戳，写一条
                entries.append((idx, 0, 10000, text))
                idx += 1

    # 写 SRT
    with open(output_path, "w", encoding="utf-8") as f:
        for seq, start, end, text in entries:
            f.write(f"{seq}\n")
            f.write(f"{fmt_srt_time(start)} --> {fmt_srt_time(end)}\n")
            f.write(f"{text}\n\n")

    print(f"✅ 生成 {len(entries)} 条字幕 → {output_path}")
    return output_path


def generate_from_script(script_path: Path, audio_duration_sec: float, output_path: Path):
    """备用：从脚本文本按字数均分生成字幕（不需要模型）"""
    lines = [l.strip() for l in script_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    total_chars = sum(len(l) for l in lines)

    entries = []
    current_ms = 0
    idx = 1

    for line in lines:
        seg_ms = int((len(line) / total_chars) * audio_duration_sec * 1000)
        start = current_ms

        chunks = split_text(line)
        chunk_ms = seg_ms // len(chunks) if chunks else 0

        for j, chunk in enumerate(chunks):
            cs = start + j * chunk_ms
            ce = start + (j + 1) * chunk_ms
            entries.append((idx, cs, ce, chunk))
            idx += 1

        current_ms += seg_ms

    with open(output_path, "w", encoding="utf-8") as f:
        for seq, start, end, text in entries:
            f.write(f"{seq}\n")
            f.write(f"{fmt_srt_time(start)} --> {fmt_srt_time(end)}\n")
            f.write(f"{text}\n\n")

    print(f"✅ 生成 {len(entries)} 条字幕（均分法） → {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="精准字幕生成器")
    parser.add_argument("audio", type=str, help="音频文件路径")
    parser.add_argument("--output", type=str, default=None, help="输出 SRT 路径")
    parser.add_argument("--fallback-script", type=str, default=None,
                        help="备用：用脚本文本均分（不用模型）")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"❌ 音频不存在: {audio_path}")
        return

    output_path = Path(args.output) if args.output else audio_path.parent / "subtitles.srt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.fallback_script:
        import subprocess
        dur_cmd = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
            capture_output=True, text=True
        )
        duration = float(dur_cmd.stdout.strip())
        generate_from_script(Path(args.fallback_script), duration, output_path)
    else:
        generate_with_funasr(audio_path, output_path)


if __name__ == "__main__":
    main()
