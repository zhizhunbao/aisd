import os
import re
import subprocess
from pathlib import Path

notes_dir = Path(r"C:\Users\40270\Desktop\workspace\aisd\courses\mv\notes")
output_dir = Path(r"C:\Users\40270\Desktop\workspace\aisd\courses\mv\storyline_audio")
output_dir.mkdir(exist_ok=True)
voice_sample = Path(r"c:\Users\40270\Desktop\workspace\aisd\video-lego\src\data\voice\voice-sample-original.wav")

def clean_markdown(text):
    lines = []
    # Skip table separator lines
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'): continue
        if line.startswith('---'): continue
        if re.match(r'^\|[-:]+\|', line): continue
        if line.startswith('>'): 
            line = line.replace('>', '').strip()
        
        # Filter out metadata lines like "Source:", "核心主题：", "故事线："
        if line.lower().startswith('source:') or line.startswith('核心主题：') or line.startswith('故事线：'):
            continue
            
        # Remove bold, italics, links, images
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
        line = re.sub(r'\*(.*?)\*', r'\1', line)
        line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line)
        line = re.sub(r'!\[(.*?)\]\(.*?\)', '', line)
        line = re.sub(r'`(.*?)`', r'\1', line)
        
        # strip table pipes
        if line.startswith('|'):
            line = line.replace('|', ' ').strip()
        
        # remove | [xx] format if present
        if '|' in line:
            line = line.split('|')[0].strip()
        if line:
            lines.append(line)
    return "\n".join(lines)

# For testing, we just do week1
file = notes_dir / "week1_intro_storyline.md"
print(f"Processing {file.name}")
content = file.read_text(encoding='utf-8')
clean_text = clean_markdown(content)

script_path = output_dir / f"{file.stem}_script.txt"
script_path.write_text(clean_text, encoding='utf-8')

out_folder = output_dir / file.stem
out_folder.mkdir(exist_ok=True)

# Run TTS
cmd = [
    "uv", "run", "python",
    r"C:\Users\40270\Desktop\workspace\.agent\skills\ai-video-director\scripts\generate_narration_qwen.py",
    "--script", str(script_path),
    "--clone", str(voice_sample),
    "--output-dir", str(out_folder)
]
print("Running:", " ".join(cmd))
subprocess.run(cmd, cwd=r"C:\Users\40270\Desktop\workspace\aisd", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
