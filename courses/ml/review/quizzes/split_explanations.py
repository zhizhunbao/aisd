"""
Split mixed explanation fields into separate explanation (EN) and explanation_zh (ZH).

Current format:
  "explanation": "English explanation text.<br>💡 Chinese summary text."

Target format:
  "explanation": "English explanation text."
  "explanation_zh": "Chinese summary text."
"""

import json
import re
import glob
import os

def split_explanation(expl: str) -> tuple[str, str]:
    """Split a mixed EN+ZH explanation into (en, zh) parts."""
    if not expl:
        return ("", "")
    
    # Pattern: split on <br> or <br/> followed by 💡
    # Some may have multiple <br> tags
    parts = re.split(r'<br\s*/?>\s*💡\s*', expl, maxsplit=1)
    
    if len(parts) == 2:
        en_part = parts[0].strip()
        zh_part = parts[1].strip()
        return (en_part, zh_part)
    
    # Try splitting on just 💡 (no <br> tag)
    parts = re.split(r'\s*💡\s*', expl, maxsplit=1)
    if len(parts) == 2:
        en_part = parts[0].strip()
        zh_part = parts[1].strip()
        return (en_part, zh_part)
    
    # No Chinese part found - return original as EN, empty ZH
    return (expl.strip(), "")


def process_file(filepath: str):
    """Process a single quiz JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        quizzes = json.load(f)
    
    changes = 0
    for q in quizzes:
        if 'explanation' not in q:
            continue
        
        original = q['explanation']
        en_part, zh_part = split_explanation(original)
        
        if zh_part:  # Only split if we found a Chinese part
            q['explanation'] = en_part
            q['explanation_zh'] = zh_part
            changes += 1
        else:
            # Check if the explanation is purely Chinese (no English)
            # Keep as-is if no split point found
            print(f"  [WARN] No split found: {original[:60]}...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, ensure_ascii=False, indent=2)
    
    print(f"  [OK] {changes} explanations split")
    return changes


def main():
    quiz_dir = os.path.dirname(os.path.abspath(__file__))
    json_files = sorted(glob.glob(os.path.join(quiz_dir, '*.json')))
    
    total = 0
    for filepath in json_files:
        fname = os.path.basename(filepath)
        print(f"\nProcessing {fname}...")
        total += process_file(filepath)
    
    print(f"\nDone! Total explanations split: {total}")


if __name__ == '__main__':
    main()
