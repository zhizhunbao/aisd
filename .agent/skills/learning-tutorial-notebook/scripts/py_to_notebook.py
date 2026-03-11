"""
Convert tutorial-style .py scripts to Jupyter Notebooks (.ipynb).
将教程风格的 .py 脚本转换为 Jupyter Notebook。

Parses the jupytext percent format:
解析 jupytext percent 格式：
  - `# %% [markdown]` + triple-quoted string → Markdown cell
  - `# %%` → Code cell

Usage:
    python py_to_notebook.py <input.py> [output.ipynb]
"""

import json
import re
import sys
from pathlib import Path


def parse_cells(content: str) -> list[dict]:
    """Parse .py content into a list of cell dicts.
    解析 .py 内容为 cell 字典列表。

    Returns list of {'type': 'code'|'markdown', 'source': str}
    """
    cells = []
    lines = content.split('\n')
    i = 0
    n = len(lines)

    # Collect any content before the first # %% marker as a code cell
    # 将第一个 # %% 标记之前的内容收集为代码 cell
    preamble_lines = []
    while i < n and not re.match(r'^# %%', lines[i]):
        preamble_lines.append(lines[i])
        i += 1

    preamble = '\n'.join(preamble_lines).strip()
    if preamble:
        cells.append({'type': 'code', 'source': preamble})

    # Parse cells delimited by # %% markers
    # 解析由 # %% 标记分隔的 cells
    while i < n:
        line = lines[i]

        if re.match(r'^# %% \[markdown\]', line):
            # Markdown cell: extract content from triple-quoted string
            # Markdown cell：从三引号字符串中提取内容
            i += 1
            md_lines = []
            in_triple_quote = False
            quote_char = None

            while i < n:
                current = lines[i]

                if not in_triple_quote:
                    # Look for opening triple quotes
                    # 查找开始的三引号
                    stripped = current.strip()
                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        quote_char = stripped[:3]
                        # Check if it opens and closes on the same line
                        # 检查是否在同一行打开和关闭
                        rest = stripped[3:]
                        if quote_char in rest:
                            # Single-line: """content"""
                            md_content = rest[:rest.index(quote_char)]
                            md_lines.append(md_content)
                            i += 1
                            break
                        else:
                            in_triple_quote = True
                            # Content after opening quotes on same line
                            if rest:
                                md_lines.append(rest)
                            i += 1
                            continue
                    elif stripped == '' or stripped.startswith('#'):
                        # Skip empty lines and comments between marker and quotes
                        i += 1
                        continue
                    else:
                        # Not a triple-quoted string, treat as code
                        break
                else:
                    # Inside triple-quoted string
                    # 在三引号字符串内部
                    if quote_char in lines[i]:
                        # Closing triple quotes found
                        # 找到关闭的三引号
                        before_close = lines[i][:lines[i].index(quote_char)]
                        if before_close:
                            md_lines.append(before_close)
                        in_triple_quote = False
                        i += 1
                        break
                    else:
                        md_lines.append(lines[i])
                        i += 1

            md_source = '\n'.join(md_lines).strip()
            if md_source:
                cells.append({'type': 'markdown', 'source': md_source})

        elif re.match(r'^# %%', line):
            # Code cell: collect all lines until next # %% marker
            # 代码 cell：收集到下一个 # %% 标记之前的所有行
            # Extract optional cell title from comment after # %%
            i += 1
            code_lines = []

            while i < n and not re.match(r'^# %%', lines[i]):
                code_lines.append(lines[i])
                i += 1

            code_source = '\n'.join(code_lines).strip()
            if code_source:
                cells.append({'type': 'code', 'source': code_source})

        else:
            i += 1

    return cells


def cells_to_notebook(cells: list[dict]) -> dict:
    """Convert cell list to nbformat v4 notebook dict.
    将 cell 列表转换为 nbformat v4 notebook 字典。
    """
    nb = {
        "nbformat": 4,
        "nbformat_minor": 4,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "cells": []
    }

    for cell in cells:
        if cell['type'] == 'markdown':
            # Split source into lines for JSON array format
            # 将源代码分割为行用于 JSON 数组格式
            source_lines = cell['source'].split('\n')
            # Add \n to all lines except the last
            json_source = [line + '\n' for line in source_lines[:-1]]
            if source_lines:
                json_source.append(source_lines[-1])

            nb['cells'].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": json_source
            })
        else:
            source_lines = cell['source'].split('\n')
            json_source = [line + '\n' for line in source_lines[:-1]]
            if source_lines:
                json_source.append(source_lines[-1])

            nb['cells'].append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": json_source
            })

    return nb


def convert(input_path: str, output_path: str = None) -> str:
    """Main conversion: .py → .ipynb
    主转换函数：.py → .ipynb

    Args:
        input_path: Path to the .py file
        output_path: Optional path for output .ipynb (defaults to same name)

    Returns:
        Path to the generated .ipynb file
    """
    input_file = Path(input_path)

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    if output_path is None:
        output_file = input_file.with_suffix('.ipynb')
    else:
        output_file = Path(output_path)

    # Read .py source
    content = input_file.read_text(encoding='utf-8')

    # Parse into cells
    cells = parse_cells(content)

    if not cells:
        print("Warning: No cells parsed from input file.")
        print("Make sure the file uses # %% and # %% [markdown] markers.")
        sys.exit(1)

    # Build notebook
    nb = cells_to_notebook(cells)

    # Validate JSON before writing
    try:
        json_str = json.dumps(nb, ensure_ascii=False, indent=1)
        json.loads(json_str)  # Validate roundtrip
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: Generated notebook has invalid JSON: {e}")
        sys.exit(1)

    # Write notebook
    output_file.write_text(json_str + '\n', encoding='utf-8')

    # Summary
    md_count = sum(1 for c in cells if c['type'] == 'markdown')
    code_count = sum(1 for c in cells if c['type'] == 'code')
    print(f"✅ Converted: {input_file.name} → {output_file.name}")
    print(f"   Cells: {len(cells)} total ({md_count} markdown, {code_count} code)")

    return str(output_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python py_to_notebook.py <input.py> [output.ipynb]")
        print()
        print("Converts a tutorial-style .py file to .ipynb notebook.")
        print("The .py file should use # %% and # %% [markdown] markers.")
        print()
        print("Example:")
        print("  python py_to_notebook.py linear_algebra_demo.py")
        sys.exit(0)

    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    convert(in_file, out_file)
