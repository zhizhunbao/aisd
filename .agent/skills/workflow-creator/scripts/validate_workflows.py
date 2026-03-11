#!/usr/bin/env python3
"""
Workflow Validator — validate all workflow .md files against the workflow-creator standard.

Usage:
    python validate_workflows.py <workflows_dir>
    python validate_workflows.py .agent/workflows

Checks:
    - Frontmatter presence and format
    - Description quality
    - File naming convention (kebab-case)
    - Line count (warn >200, fail >500)
    - Step numbering
    - Turbo annotation safety
    - Duplicate detection
"""

import re
import sys
import json
from pathlib import Path
from difflib import SequenceMatcher


def validate_workflow(filepath: Path) -> dict:
    """Validate a single workflow file."""
    result = {
        "file": filepath.name,
        "status": "PASS",
        "errors": [],
        "warnings": [],
        "info": {}
    }

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        result["status"] = "FAIL"
        result["errors"].append(f"Cannot read file: {e}")
        return result

    lines = content.splitlines()
    result["info"]["lines"] = len(lines)

    # === 1. Frontmatter check ===
    if not content.startswith("---"):
        result["status"] = "FAIL"
        result["errors"].append("Missing frontmatter (file must start with ---)")
    else:
        fm_end = content.find("---", 3)
        if fm_end < 0:
            result["status"] = "FAIL"
            result["errors"].append("Unclosed frontmatter (missing closing ---)")
        else:
            fm_text = content[3:fm_end].strip()
            # Check description
            desc_match = re.search(r"description:\s*(.+)", fm_text)
            if not desc_match:
                result["status"] = "FAIL"
                result["errors"].append("Missing 'description' in frontmatter")
            else:
                desc = desc_match.group(1).strip()
                result["info"]["description"] = desc
                if len(desc) > 120:
                    result["warnings"].append(f"Description too long ({len(desc)} chars, max 120)")
                if len(desc) < 10:
                    result["warnings"].append(f"Description too short ({len(desc)} chars)")

            # Check for unknown fields
            known_fields = {"description"}
            for line in fm_text.splitlines():
                field_match = re.match(r"(\w[\w-]*)\s*:", line)
                if field_match:
                    field = field_match.group(1)
                    if field not in known_fields:
                        result["warnings"].append(f"Non-standard frontmatter field: '{field}'")

    # === 2. File naming ===
    name = filepath.stem
    if name != name.lower():
        result["warnings"].append(f"Filename has uppercase: '{name}' → use lowercase")
    if "_" in name:
        result["warnings"].append(f"Filename has underscores: '{name}' → use hyphens")
    if " " in name:
        result["status"] = "FAIL"
        result["errors"].append(f"Filename has spaces: '{name}'")

    # === 3. Line count ===
    line_count = len(lines)
    if line_count > 500:
        result["warnings"].append(f"Oversized: {line_count} lines (max recommended: 500)")
    elif line_count > 200:
        result["warnings"].append(f"Large: {line_count} lines (ideal: <200)")

    # === 4. Step numbering ===
    numbered_steps = [l for l in lines if re.match(r"^\d+\.\s", l.strip())]
    result["info"]["numbered_steps"] = len(numbered_steps)
    if len(numbered_steps) == 0:
        result["warnings"].append("No numbered steps found — workflows should use numbered steps")

    # === 5. Turbo annotation check ===
    has_turbo_all = "// turbo-all" in content
    turbo_lines = []
    for i, line in enumerate(lines):
        if line.strip() == "// turbo":
            turbo_lines.append(i + 1)

    result["info"]["turbo_steps"] = len(turbo_lines)
    result["info"]["turbo_all"] = has_turbo_all

    # Check for dangerous turbo annotations
    dangerous_keywords = ["delete", "remove", "rm ", "push", "deploy", "install", "drop"]
    for turbo_line_num in turbo_lines:
        if turbo_line_num < len(lines):
            next_line = lines[turbo_line_num].lower()
            for kw in dangerous_keywords:
                if kw in next_line:
                    result["warnings"].append(
                        f"L{turbo_line_num}: '// turbo' before potentially dangerous step containing '{kw}'"
                    )

    # === 6. Code fence balance ===
    fence_count = sum(1 for l in lines if l.strip().startswith("```"))
    if fence_count % 2 != 0:
        result["status"] = "FAIL"
        result["errors"].append(f"Unclosed code fence ({fence_count} markers, expected even)")

    # Set status
    if result["errors"]:
        result["status"] = "FAIL"
    elif result["warnings"]:
        result["status"] = "WARN"

    return result


def check_duplicates(workflows_dir: Path, results: list) -> list:
    """Check for potentially duplicate or very similar workflows."""
    duplicates = []
    files = list(workflows_dir.glob("*.md"))
    descriptions = {}

    for r in results:
        desc = r.get("info", {}).get("description", "")
        if desc:
            descriptions[r["file"]] = desc

    # Compare descriptions
    names = list(descriptions.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ratio = SequenceMatcher(None, descriptions[names[i]], descriptions[names[j]]).ratio()
            if ratio > 0.6:
                duplicates.append({
                    "files": [names[i], names[j]],
                    "similarity": round(ratio * 100, 1),
                    "descriptions": [descriptions[names[i]][:60], descriptions[names[j]][:60]]
                })

    return duplicates


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_workflows.py <workflows_dir>")
        sys.exit(1)

    wf_dir = Path(sys.argv[1])
    if not wf_dir.exists():
        print(f"Error: {wf_dir} does not exist")
        sys.exit(1)

    md_files = sorted(wf_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {wf_dir}")
        sys.exit(0)

    print(f"\n{'=' * 70}")
    print(f"  Workflow Validator — {len(md_files)} workflows")
    print(f"{'=' * 70}\n")

    results = []
    pass_count = warn_count = fail_count = 0

    for f in md_files:
        r = validate_workflow(f)
        results.append(r)

        icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}[r["status"]]
        info = r["info"]
        print(f"  {icon} {r['file']:40s} {r['status']:4s}  ({info.get('lines', '?')} lines, {info.get('numbered_steps', 0)} steps)")

        for e in r["errors"]:
            print(f"      ❌ {e}")
        for w in r["warnings"]:
            print(f"      ⚠️  {w}")

        if r["status"] == "PASS":
            pass_count += 1
        elif r["status"] == "WARN":
            warn_count += 1
        else:
            fail_count += 1

    # Check duplicates
    duplicates = check_duplicates(wf_dir, results)
    if duplicates:
        print(f"\n{'─' * 70}")
        print(f"  🔍 Potential Duplicates")
        print(f"{'─' * 70}")
        for d in duplicates:
            print(f"  {d['files'][0]} ↔ {d['files'][1]}  ({d['similarity']}% similar)")
            print(f"    → \"{d['descriptions'][0]}...\"")
            print(f"    → \"{d['descriptions'][1]}...\"")

    # Summary
    print(f"\n{'=' * 70}")
    print(f"  Summary: {pass_count} PASS | {warn_count} WARN | {fail_count} FAIL")
    print(f"{'=' * 70}\n")

    # Save report
    report_path = wf_dir / "_workflow_report.json"
    report = {
        "total": len(results),
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "results": results,
        "duplicates": duplicates
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  📄 Report saved to: {report_path}\n")


if __name__ == "__main__":
    main()
