"""
Qwen3-TTS 通用旁白生成器（本地 GPU）
=====================================
支持两种模式：
  1. 预设声音: python generate_narration_qwen.py --script script.txt
  2. 声音克隆: python generate_narration_qwen.py --script script.txt --clone voice.mp3

脚本格式：
  纯文本文件，每行一个段落。空行忽略。

输出：
  narration/full_narration_qwen.mp3   (预设声音)
  narration/full_narration_myvoice.mp3 (克隆声音)
  narration/timestamps.json           (每段精确起止时间)

硬件要求：
  RTX 4060 (8GB VRAM) 或更高
  模型大小：~1.8GB，首次下载后自动缓存到 ~/.cache/huggingface/
"""
import argparse
import json
import numpy as np
import soundfile as sf
import subprocess
from pathlib import Path


def load_script(script_path: Path) -> list[str]:
    """从文本文件读取旁白稿，每行一段"""
    text = script_path.read_text(encoding="utf-8")
    segments = [line.strip() for line in text.splitlines() if line.strip()]
    return segments


def synthesize_segments(model, segments: list[str], gen_func, gen_kwargs: dict) -> tuple:
    """逐段合成语音，返回 (all_wavs, sample_rate)"""
    all_wavs = []
    sample_rate = None

    for i, text in enumerate(segments):
        print(f"  [{i+1}/{len(segments)}] {text[:40]}...")
        wavs, sr = gen_func(text=text, **gen_kwargs)
        all_wavs.append(wavs[0])
        sample_rate = sr

    return all_wavs, sample_rate


def concat_and_save(all_wavs: list, segments_text: list[str], sample_rate: int,
                    output_path: Path, gap_sec: float = 0.3):
    """拼接音频段落，段间插入静默，保存为 mp3 + timestamps.json"""
    silence_samples = int(sample_rate * gap_sec)
    silence = np.zeros(silence_samples, dtype=np.float32)

    combined = []
    timestamps = []  # 记录每段精确起止时间
    cursor = 0  # 当前采样点位置

    for i, wav in enumerate(all_wavs):
        start_sec = cursor / sample_rate
        cursor += len(wav)
        end_sec = cursor / sample_rate

        timestamps.append({
            "index": i + 1,
            "start": round(start_sec, 3),
            "end": round(end_sec, 3),
            "text": segments_text[i],
            "scene": f"scene_{i+1:02d}.mp4",
        })

        combined.append(wav)
        if i < len(all_wavs) - 1:
            combined.append(silence)
            cursor += silence_samples

    full_audio = np.concatenate(combined)

    # wav -> mp3
    wav_temp = output_path.with_suffix(".wav")
    sf.write(str(wav_temp), full_audio, sample_rate)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(wav_temp),
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(output_path)
    ], capture_output=True)
    wav_temp.unlink(missing_ok=True)

    # 导出时间戳
    ts_path = output_path.parent / "timestamps.json"
    with open(ts_path, "w", encoding="utf-8") as f:
        json.dump(timestamps, f, ensure_ascii=False, indent=2)

    dur = len(full_audio) / sample_rate
    print(f"\n✅ 完成: {output_path}")
    print(f"   时长: {dur:.1f}s | 采样率: {sample_rate}Hz")
    print(f"   时间戳: {ts_path} ({len(timestamps)} 段)")
    return output_path


def generate_preset(segments: list[str], output_dir: Path, speaker: str = "uncle_fu"):
    """用 CustomVoice 预设声音生成"""
    from qwen_tts.inference.qwen3_tts_model import Qwen3TTSModel

    print(f"⏳ 加载 CustomVoice 模型...")
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        device_map="cuda:0",
        torch_dtype="auto",
    )

    all_wavs, sr = synthesize_segments(
        model, segments,
        gen_func=model.generate_custom_voice,
        gen_kwargs={"speaker": speaker, "language": "Chinese"}
    )
    return concat_and_save(all_wavs, segments, sr, output_dir / "full_narration_qwen.mp3")


def generate_clone(segments: list[str], output_dir: Path, voice_sample: Path):
    """用 Base 模型克隆声音"""
    from qwen_tts.inference.qwen3_tts_model import Qwen3TTSModel

    if not voice_sample.exists():
        print(f"❌ 声音样本不存在: {voice_sample}")
        return None

    print(f"⏳ 加载 Base 模型...")
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
        device_map="cuda:0",
        torch_dtype="auto",
    )

    print("🔊 提取声音特征...")
    voice_prompt = model.create_voice_clone_prompt(
        ref_audio=str(voice_sample),
        x_vector_only_mode=True,
    )

    all_wavs, sr = synthesize_segments(
        model, segments,
        gen_func=model.generate_voice_clone,
        gen_kwargs={"language": "Chinese", "voice_clone_prompt": voice_prompt}
    )
    return concat_and_save(all_wavs, segments, sr, output_dir / "full_narration_myvoice.mp3")


def main():
    parser = argparse.ArgumentParser(description="Qwen3-TTS 通用旁白生成器")
    parser.add_argument("--script", type=str, required=True,
                        help="旁白稿文件路径（每行一段）")
    parser.add_argument("--clone", type=str, default=None,
                        help="声音样本路径（mp3/wav/m4a），用于声音克隆")
    parser.add_argument("--speaker", type=str, default="uncle_fu",
                        help="预设声音 (aiden/uncle_fu/serena/ryan/...)")
    parser.add_argument("--output-dir", type=str, default="narration",
                        help="输出目录")
    args = parser.parse_args()

    script_path = Path(args.script)
    if not script_path.exists():
        print(f"❌ 脚本文件不存在: {script_path}")
        return

    segments = load_script(script_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"📝 {len(segments)} 段旁白")

    if args.clone:
        generate_clone(segments, output_dir, Path(args.clone))
    else:
        generate_preset(segments, output_dir, speaker=args.speaker)


if __name__ == "__main__":
    main()
