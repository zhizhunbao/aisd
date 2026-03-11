#!/usr/bin/env python3
"""
MD → JSON Converter for Cheat Sheet
将 6-layer 结构的 markdown 转换为 JSON

Usage:
    uv run python md_to_json_{exam}.py

Input:  {exam}_cheat_sheet.md
Output: {exam}_cheat_sheet.json
"""

import json
import re
from pathlib import Path

# ============== CONFIG ==============
INPUT_MD = "midterm_cheat_sheet.md"      # 修改为实际文件名
OUTPUT_JSON = "midterm_cheat_sheet.json"  # 修改为实际文件名
# ====================================


def parse_markdown(md_content: str) -> dict:
    """
    Parse 6-layer markdown structure into JSON
    解析 6 层 markdown 结构为 JSON
    """
    result = {
        "title": "",
        "description": "",
        "weeks": [],
        "milestones": [],
        "flash_cards": [],
        "quiz_answers": []
    }

    lines = md_content.split('\n')

    current_week = None
    current_section = None
    current_content_type = None
    code_block = []
    in_code_block = False
    code_lang = ""

    i = 0
    while i < len(lines):
        line = lines[i]

        # === Level 1: Title (# ...) ===
        if line.startswith('# ') and not line.startswith('## '):
            result["title"] = line[2:].strip()
            i += 1
            continue

        # === Description (> ...) ===
        if line.startswith('> ') and not result["description"]:
            result["description"] = line[2:].strip()
            i += 1
            continue

        # === Level 2: Week (## W1: ...) ===
        week_match = re.match(r'^## (W\d+):\s*(.+)', line)
        if week_match:
            # Save previous week if exists
            if current_week and current_section:
                current_week["sections"].append(current_section)
            if current_week:
                result["weeks"].append(current_week)

            current_week = {
                "id": week_match.group(1),
                "title": week_match.group(2).strip(),
                "sections": []
            }
            current_section = None
            current_content_type = None
            i += 1
            continue

        # === Special sections: Milestones, Quiz Quick Review ===
        if line.startswith('## Milestones'):
            # Save current state
            if current_week and current_section:
                current_week["sections"].append(current_section)
            if current_week:
                result["weeks"].append(current_week)
                current_week = None

            # Parse milestones table
            i += 1
            while i < len(lines) and not lines[i].startswith('## '):
                table_line = lines[i].strip()
                if table_line.startswith('|') and '---' not in table_line:
                    cols = [c.strip() for c in table_line.split('|')[1:-1]]
                    if len(cols) >= 2 and cols[0] and cols[0] != 'Year':
                        result["milestones"].append({
                            "year": cols[0],
                            "event": cols[1]
                        })
                i += 1
            continue

        if line.startswith('## Quiz Quick Review'):
            i += 1
            while i < len(lines) and not lines[i].startswith('## '):
                review_line = lines[i].strip()
                if review_line.startswith('✅'):
                    result["flash_cards"].append(review_line[1:].strip())
                i += 1
            continue

        # === Level 3: Section (### ...) ===
        if line.startswith('### ') and not line.startswith('#### '):
            # Save previous section
            if current_week and current_section:
                current_week["sections"].append(current_section)

            current_section = {
                "title": line[4:].strip(),
                "content": [],
                "table": {"headers": [], "rows": []},
                "formulas": [],
                "examples": [],
                "traps": [],
                "code": []
            }
            current_content_type = None
            i += 1
            continue

        # === Level 4: Content Type (#### ...) ===
        if line.startswith('#### '):
            heading = line[5:].strip().lower()
            if 'definition' in heading:
                current_content_type = 'content'
            elif 'comparison' in heading:
                current_content_type = 'table'
            elif 'formula' in heading:
                current_content_type = 'formulas'
            elif 'example' in heading:
                current_content_type = 'examples'
            elif 'trap' in heading:
                current_content_type = 'traps'
            elif 'code' in heading:
                current_content_type = 'code'
            else:
                current_content_type = 'content'  # default
            i += 1
            continue

        # === Handle code blocks ===
        if line.startswith('```'):
            if in_code_block:
                # End of code block
                if current_section and current_content_type == 'code':
                    current_section["code"].append({
                        "lang": code_lang,
                        "snippet": '\n'.join(code_block)
                    })
                code_block = []
                in_code_block = False
                code_lang = ""
            else:
                # Start of code block
                in_code_block = True
                code_lang = line[3:].strip() or "python"
            i += 1
            continue

        if in_code_block:
            code_block.append(line)
            i += 1
            continue

        # === Level 5: Items (- ...) ===
        if line.strip().startswith('- ') and current_section and current_content_type:
            item = line.strip()[2:]  # Remove "- "

            if current_content_type == 'content':
                current_section["content"].append(item)

            elif current_content_type == 'formulas':
                # Extract LaTeX formula
                current_section["formulas"].append(item)

            elif current_content_type == 'examples':
                # Parse example: **Label**: content
                ex_match = re.match(r'\*\*(.+?)\*\*:\s*(.+)', item)
                if ex_match:
                    current_section["examples"].append({
                        "label": ex_match.group(1),
                        "steps": [ex_match.group(2)]
                    })
                else:
                    current_section["examples"].append({
                        "label": "Example",
                        "steps": [item]
                    })

            elif current_content_type == 'traps':
                current_section["traps"].append(item)

            i += 1
            continue

        # === Handle tables (for Comparisons) ===
        if line.strip().startswith('|') and current_section and current_content_type == 'table':
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if '---' in line:
                pass  # Skip separator line
            elif not current_section["table"]["headers"]:
                current_section["table"]["headers"] = cols
            else:
                current_section["table"]["rows"].append(cols)
            i += 1
            continue

        i += 1

    # Save final state
    if current_week and current_section:
        current_week["sections"].append(current_section)
    if current_week:
        result["weeks"].append(current_week)

    return result


def clean_empty_fields(data: dict) -> dict:
    """
    Remove empty lists and dicts for cleaner JSON
    清理空字段
    """
    if isinstance(data, dict):
        return {
            k: clean_empty_fields(v)
            for k, v in data.items()
            if v and (not isinstance(v, (list, dict)) or v)
        }
    elif isinstance(data, list):
        return [clean_empty_fields(item) for item in data if item]
    return data


def main():
    # Read input markdown
    # 读取输入 markdown
    md_path = Path(__file__).parent / INPUT_MD
    if not md_path.exists():
        print(f"Error: {INPUT_MD} not found")
        return

    md_content = md_path.read_text(encoding='utf-8')

    # Parse markdown to JSON structure
    # 解析 markdown 为 JSON 结构
    result = parse_markdown(md_content)

    # Optional: clean empty fields
    # 可选：清理空字段
    # result = clean_empty_fields(result)

    # Write output JSON
    # 写入输出 JSON
    json_path = Path(__file__).parent / OUTPUT_JSON
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    print(f"✅ Converted {INPUT_MD} → {OUTPUT_JSON}")
    print(f"   Weeks: {len(result['weeks'])}")
    total_sections = sum(len(w.get('sections', [])) for w in result['weeks'])
    print(f"   Sections: {total_sections}")


if __name__ == "__main__":
    main()
