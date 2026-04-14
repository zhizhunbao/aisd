import asyncio
import json
import edge_tts
from pathlib import Path

# 设置路径（相对于仓库根目录）
LECTURE_DIR = Path("aisd/courses/nlp/video/lecture10")
SCRIPT_PATH = LECTURE_DIR / "narration/script.txt"
OUTPUT_DIR = LECTURE_DIR / "narration"
OUTPUT_AUDIO = OUTPUT_DIR / "full_narration.mp3"
TIMESTAMPS_PATH = OUTPUT_DIR / "timestamps.json"

async def generate_narration():
    # 1. 读取旁白稿
    if not SCRIPT_PATH.exists():
        print(f"Error: Script not found at {SCRIPT_PATH}")
        return

    raw_lines = SCRIPT_PATH.read_text(encoding="utf-8").splitlines()
    lines = []
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        text = line.split("|")[0].strip()
        lines.append(text)

    # 云希声音 (zh-CN-YunxiNeural) - 磁性男声
    voice = "zh-CN-YunxiNeural"
    
    print(f"Starting Edge-TTS ({voice}) for {len(lines)} lines...")
    
    # 2. 我们通过一次性合成并监听 Offset 来获取精确的时间戳
    #    为了让每一段之间有清晰的停顿，我们在合成时使用 [PAUSE] 标记（实际上加个句号和空格）
    #    或者更好的做法是分段合成并累加时长。
    
    full_audio_data = b""
    timestamps = []
    current_time = 0.0
    
    for i, line in enumerate(lines):
        print(f"  [{i+1}/{len(lines)}] Synthesizing...")
        
        # 每一段末尾加一点停顿
        communicate = edge_tts.Communicate(line, voice)
        
        # 获取该段的时长（通过 offset 估算并不精确，最准确是合成后看 duration）
        # 这里我们采用逐段保存并读取时长的方法，最后合并
        temp_file = OUTPUT_DIR / f"temp_{i}.mp3"
        await communicate.save(temp_file)
        
        # 使用 ffprobe 获取时长
        import subprocess
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(temp_file)],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip())
        
        start_time = current_time
        end_time = start_time + duration
        
        timestamps.append({
            "index": i + 1,
            "start": round(start_time, 3),
            "end": round(end_time, 3),
            "text": line
        })
        
        # 累加时长，同时预留 0.4s 的固定停顿间隔（与 script 中的 "... " 逻辑一致）
        pause_dur = 0.4
        current_time = end_time + pause_dur
    
    # 3. Merge audio files
    print("\nMerging audio files...")
    concat_list_path = OUTPUT_DIR / "temp_list.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for i in range(len(lines)):
            f.write(f"file 'temp_{i}.mp3'\n")
            # 插入静音
            # 注意：ffmpeg concat 直接插静音比较麻烦，简单做法是生成一个小静音文件
            silence_path = OUTPUT_DIR / "silence.mp3"
            if not silence_path.exists():
                subprocess.run([
                    "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", 
                    "-t", "0.4", str(silence_path)
                ], capture_output=True)
            f.write(f"file 'silence.mp3'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
        "-c", "copy", str(OUTPUT_AUDIO)
    ], capture_output=True)

    # 4. 保存时间戳
    TIMESTAMPS_PATH.write_text(json.dumps(timestamps, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # 5. 清理临时文件
    for i in range(len(lines)):
        (OUTPUT_DIR / f"temp_{i}.mp3").unlink(missing_ok=True)
    concat_list_path.unlink(missing_ok=True)
    (OUTPUT_DIR / "silence.mp3").unlink(missing_ok=True)

    print(f"\nSuccess!")
    print(f"Audio: {OUTPUT_AUDIO}")
    print(f"Timestamps: {TIMESTAMPS_PATH}")

if __name__ == "__main__":
    asyncio.run(generate_narration())
