from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


SUFFIX_ORDER = {
    "map": 10,
    "slides": 20,
    "storyline": 30,
    "concepts": 40,
    "math": 50,
    "code": 60,
    "tutorial": 70,
    "history": 80,
    "quiz": 90,
    "cheatsheet": 100,
}

GROUP_ORDER = {
    "week": 1,
    "lab": 2,
    "assignment": 3,
}


def split_stem(stem: str) -> tuple[str, str]:
    for suffix in sorted(SUFFIX_ORDER, key=len, reverse=True):
        marker = f"_{suffix}"
        if stem.endswith(marker):
            return stem[: -len(marker)], suffix
    return stem, ""


def natural_parts(text: str) -> list[object]:
    parts: list[object] = []
    for part in re.split(r"(\d+)", text):
        if not part:
            continue
        parts.append(int(part) if part.isdigit() else part.lower())
    return parts


def file_sort_key(path: Path) -> tuple[object, ...]:
    prefix, suffix = split_stem(path.stem)
    match = re.match(r"^(week|lab|assignment)(\d+)(?:_|$)", prefix)
    if match:
        group_name = match.group(1)
        group_number = int(match.group(2))
        remainder = prefix[match.end() :].strip("_")
        return (
            GROUP_ORDER[group_name],
            group_number,
            natural_parts(remainder),
            SUFFIX_ORDER.get(suffix, 999),
            natural_parts(suffix),
        )
    return (999, natural_parts(prefix), SUFFIX_ORDER.get(suffix, 999), natural_parts(suffix))


def find_markdown_files(notes_dir: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in notes_dir.rglob("*.md")
            if path.is_file()
            and "__pdf__" not in path.parts
            and "__html__" not in path.parts
            and path.name != "merged_rl_notes.md"
            and path.name != Path(__file__).name
        ),
        key=file_sort_key,
    )


def normalize_markdown_for_typora(text: str) -> str:
    lines = text.splitlines()
    normalized: list[str] = []
    in_fenced_code = False
    fence_pattern = re.compile(r"^\s*(```|~~~)")
    single_line_math_pattern = re.compile(r"^(\s*(?:>\s*)*)\$\$(.+)\$\$\s*$")

    for line in lines:
        if fence_pattern.match(line):
            in_fenced_code = not in_fenced_code
            normalized.append(line)
            continue

        if in_fenced_code:
            normalized.append(line)
            continue

        math_match = single_line_math_pattern.match(line)
        if math_match:
            prefix = math_match.group(1)
            expr = math_match.group(2).strip()
            normalized.append(f"{prefix}$$")
            normalized.append(f"{prefix}{expr}")
            normalized.append(f"{prefix}$$")
            continue

        normalized.append(line)

    return "\n".join(normalized)


def main() -> int:
    notes_dir = Path(__file__).resolve().parent
    output_path = notes_dir / "merged_rl_notes.md"
    markdown_files = find_markdown_files(notes_dir)

    parts: list[str] = []
    parts.append("# RL Notes Merged")
    parts.append("")
    parts.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    parts.append(f"- Source folder: `{notes_dir}`")
    parts.append(f"- Total files: {len(markdown_files)}")
    parts.append("")
    parts.append("## Contents")
    parts.append("")

    for index, path in enumerate(markdown_files, start=1):
        parts.append(f"{index}. `{path.name}`")

    for index, path in enumerate(markdown_files, start=1):
        text = normalize_markdown_for_typora(path.read_text(encoding="utf-8"))
        relative_path = path.relative_to(notes_dir).as_posix()
        parts.append("")
        parts.append("")
        parts.append("---")
        parts.append("")
        parts.append(f"## {index:02d}. {path.stem}")
        parts.append("")
        parts.append(f"Source: `{relative_path}`")
        parts.append("")
        parts.append(text.rstrip())
        parts.append("")

    output_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Merged {len(markdown_files)} files into {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
