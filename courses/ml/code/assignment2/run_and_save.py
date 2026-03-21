"""
Run assignment2_cifar10.py and capture output to file with proper UTF-8 encoding.
Bypasses PowerShell's encoding issues with Keras box-drawing characters.
Also cleans up \r carriage returns and Keras training progress bars.
"""
import subprocess
import sys
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(script_dir, 'assignment2_cifar10.py')
output_path = os.path.join(script_dir, 'assignment2_images', 'output.txt')

print(f"Running: {script_path}")
print(f"Output:  {output_path}")

result = subprocess.run(
    [sys.executable, script_path],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='replace',
    cwd=script_dir,
    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
)

# Clean up the output:
# 1. Handle \r carriage returns (Keras progress bars overwrite lines)
# 2. Remove intermediate progress bar lines, keep only the final one per epoch
# 3. Remove trailing whitespace
lines = result.stdout.split('\n')
cleaned_lines = []
for line in lines:
    if '\r' in line:
        # Keep only the last \r segment (the final overwrite)
        parts = line.split('\r')
        non_empty = [p for p in parts if p.strip()]
        line = non_empty[-1] if non_empty else ''

    # Skip intermediate Keras progress bar lines (partial progress like "137/704 ━━...")
    # Keep only completed epoch lines (e.g. "704/704 ━━━━━━━━━━━━━━━━━━━━ ")
    progress_match = re.match(r'^\s*(\d+)/(\d+)\s+━', line)
    if progress_match:
        current, total = int(progress_match.group(1)), int(progress_match.group(2))
        if current < total:
            continue  # Skip intermediate progress, keep only final

    cleaned_lines.append(line.rstrip())

output = '\n'.join(cleaned_lines)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(output)

line_count = len(cleaned_lines)
if result.returncode == 0:
    print(f"Done! Output saved successfully. ({line_count} lines)")
else:
    print(f"Script exited with code {result.returncode}")
    if result.stderr:
        print("STDERR (last 500 chars):")
        print(result.stderr[-500:])
