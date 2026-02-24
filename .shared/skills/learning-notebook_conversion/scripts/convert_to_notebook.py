"""
Convert Python script to Jupyter Notebook using step markers as cell boundaries.
将 Python 脚本转换为 Jupyter Notebook，使用步骤标记作为 cell 边界。

Key behavior:
关键行为：
- Only split on STEP markers (# 步骤 X or # Step X)
  只在步骤标记处分割
- Keep concept/classifier blocks together with their step code
  概念/分类器解释块与步骤代码保持在同一 cell
- Do NOT split on concept markers (# 概念 or # Concept)
  不在概念标记处分割

Supports two code structures:
支持两种代码结构：
1. Top-level code with section markers (original behavior)
   顶层代码带分隔符（原有行为）
2. Code inside main() function with section markers
   main() 函数内的代码带分隔符
"""

import nbformat
import re
import sys
from pathlib import Path


def extract_step_title(step_header: str) -> str | None:
    """从步骤标记块中提取标题，用于生成 Markdown cell
    Extract title from step marker block for Markdown cell generation

    示例输入 / Example input:
        # ============================================================
        # 步骤 1：数据加载
        # Step 1: Data Loading
        # ============================================================

    返回 / Returns: "## Step 1: Data Loading" 或 None
    """

    lines = step_header.strip().split('\n')

    # 跳过分隔线，提取标题行
    # Skip separator lines, extract title lines
    title_lines = [
        line.lstrip('# ').strip()
        for line in lines
        if line.strip() and not re.match(r'^# ={10,}$', line.strip())
    ]

    if not title_lines:
        return None

    # 优先使用英文标题行（Step X: ... 或纯英文行）
    # Prefer English title line (Step X: ... or pure English line)
    for line in title_lines:
        if re.match(r'Step \d', line):
            return f"## {line}"

    # 查找纯英文行（不含中文字符和 @ 符号）
    # Find pure English line (no Chinese characters or @ symbols)
    for line in title_lines:
        if not re.search(r'[\u4e00-\u9fff@]', line) and line.strip():
            return f"## {line}"

    # 回退到第一行
    # Fallback to first line
    return f"## {title_lines[0]}"


def extract_main_body(content: str) -> tuple[str, str, bool]:
    """提取 main() 函数体内容，返回 (头部代码, main体代码, 是否有main函数)
    Extract main() function body, returns (header_code, main_body_code, has_main)"""

    # 检查是否有 main() 函数
    # Check if there's a main() function
    main_match = re.search(r'^def main\(\):\s*$', content, re.MULTILINE)

    if not main_match:
        return content, '', False

    # 找到 main() 函数的位置
    # Find main() function position
    main_start = main_match.start()
    main_def_end = main_match.end()

    # 提取头部代码（main() 之前的所有内容）
    # Extract header code (everything before main())
    header_code = content[:main_start].strip()

    # 提取 main() 函数体
    # Extract main() function body
    # 找到下一个顶层定义（def 或 class 在行首，或 if __name__）
    remaining = content[main_def_end:]

    # 寻找 main() 函数体的结束位置
    # Find end of main() function body
    lines = remaining.split('\n')
    main_body_lines = []

    for line in lines:
        # 检查是否是顶层代码（非空行且不以空格开头）
        # Check if it's top-level code (non-empty line not starting with space)
        if line and not line.startswith(' ') and not line.startswith('\t'):
            # 跳过空行和文档字符串的起始
            if line.strip() and not line.strip().startswith('"""') and not line.strip().startswith("'''"):
                break
        main_body_lines.append(line)

    main_body = '\n'.join(main_body_lines)

    # 移除函数体的缩进（通常是4个空格）
    # Remove function body indentation (usually 4 spaces)
    dedented_lines = []
    for line in main_body.split('\n'):
        if line.startswith('    '):
            dedented_lines.append(line[4:])
        elif line.startswith('\t'):
            dedented_lines.append(line[1:])
        else:
            dedented_lines.append(line)

    main_body_dedented = '\n'.join(dedented_lines)

    return header_code, main_body_dedented, True


def split_by_step_markers(content: str) -> list[str]:
    """按顶层分隔符块分割内容（匹配所有 # ====...==== 包裹的标题块）
    Split content by top-level separator blocks (match all # ====...==== header blocks)

    不在概念/分类器解释块处分割，保持它们与步骤代码在同一 cell
    Do NOT split on concept/classifier blocks, keep them with step code
    """

    # 匹配模式：任何被 # ====...==== 包裹的标题块
    # Pattern: any header block wrapped by # ====...====
    # 排除：概念 / Concept / 分类器 / Classifier / 评估指标 / Metric / 超参数 / Hyperparameter / 特征提取
    # Exclude: concept, classifier, metric, hyperparameter, feature extraction blocks
    exclude_prefixes = (
        '概念', 'Concept',
        '分类器', 'Classifier',
        '评估指标', 'Metric',
        '超参数', 'Hyperparameter',
        '特征提取', 'Feature Extraction',
    )

    # 匹配所有 # ====...==== 块
    # Match all # ====...==== blocks
    pattern = r'(# ={40,}\r?\n(?:# [^\n]*\r?\n)*# ={40,})'

    parts = re.split(pattern, content)

    # 合并被排除的块到前一个 part
    # Merge excluded blocks back into previous part
    merged = []
    i = 0
    while i < len(parts):
        part = parts[i]

        # 检查是否是被排除的标题块
        # Check if this is an excluded header block
        if re.match(r'# ={40,}', part):
            # 提取标题行（跳过分隔线）
            # Extract title lines (skip separator lines)
            title_lines = [
                line.lstrip('# ').strip()
                for line in part.strip().split('\n')
                if line.strip() and not re.match(r'^# ={10,}$', line.strip())
            ]

            # 检查是否以排除前缀开头
            # Check if starts with excluded prefix
            is_excluded = any(
                any(tl.startswith(prefix) for prefix in exclude_prefixes)
                for tl in title_lines
            )

            if is_excluded and merged:
                # 合并到前一个 part
                # Merge into previous part
                next_code = parts[i + 1] if i + 1 < len(parts) else ''
                merged[-1] = merged[-1] + part + next_code
                i += 2
                continue

        merged.append(part)
        i += 1

    return merged


def append_step_cells(nb, step_header: str, step_code: str):
    """为一个步骤添加 Markdown 标题 cell + 代码 cell
    Add a Markdown header cell + code cell for one step"""

    # 提取标题，生成 Markdown cell
    # Extract title, generate Markdown cell
    title = extract_step_title(step_header)
    if title:
        nb.cells.append(nbformat.v4.new_markdown_cell(title))

    # 添加代码 cell（保留原始步骤标记注释）
    # Add code cell (keep original step marker comments)
    full_cell = step_header + '\n' + step_code
    nb.cells.append(nbformat.v4.new_code_cell(full_cell.strip()))


def process_parts(nb, parts: list[str]):
    """处理分割后的代码段列表，统一添加到 notebook
    Process split code parts and add them to notebook"""

    # 第一部分是文件头（imports 和配置）
    # First part is file header (imports and configuration)
    if parts[0].strip():
        nb.cells.append(nbformat.v4.new_code_cell(parts[0].strip()))

    # 处理每个步骤
    # Process each step
    i = 1
    while i < len(parts):
        if re.match(r'# ={40,}', parts[i]):
            step_header = parts[i]
            step_code = parts[i + 1].strip() if i + 1 < len(parts) else ''
            append_step_cells(nb, step_header, step_code)
            i += 2
        else:
            if parts[i].strip():
                nb.cells.append(nbformat.v4.new_code_cell(parts[i].strip()))
            i += 1


def extract_docstring_title(content: str) -> tuple[str, str | None]:
    """从文件开头的 docstring 提取一级标题 Markdown cell
    Extract top-level title Markdown cell from leading docstring

    返回 (去掉 docstring 的内容, Markdown 标题文本 或 None)
    Returns (content without docstring, Markdown title text or None)
    """

    # 匹配文件开头的 triple-quote docstring
    # Match leading triple-quote docstring at file start
    match = re.match(r'^("""(.*?)"""|\'\'\'(.*?)\'\'\')\s*\n', content, re.DOTALL)
    if not match:
        return content, None

    docstring_text = match.group(2) or match.group(3)
    lines = [l.strip() for l in docstring_text.strip().split('\n') if l.strip()]

    if not lines:
        return content, None

    # 第一行作为一级标题
    # First line as top-level title
    title = f"# {lines[0]}"

    # 剩余行作为描述（如果有）
    # Remaining lines as description (if any)
    if len(lines) > 1:
        # 跳过 Author/Student Number 行，只保留描述性内容
        # Skip Author/Student Number lines, keep descriptive content only
        desc_lines = [
            l for l in lines[1:]
            if not l.lower().startswith(('author:', 'student number:'))
        ]
        if desc_lines:
            title += '\n\n' + '\n'.join(desc_lines)

    # 从原始内容中移除 docstring
    # Remove docstring from original content
    remaining = content[match.end():]

    return remaining, title


def py_to_notebook(py_file: str, output_file: str = None):
    """将 Python 脚本转换为 Jupyter Notebook
    Convert Python script to Jupyter Notebook"""

    # 读取 Python 文件
    # Read Python file
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建 notebook
    # Create notebook
    nb = nbformat.v4.new_notebook()

    # 提取文件开头的 docstring 作为一级标题 Markdown cell
    # Extract leading docstring as top-level (#) Markdown title cell
    content, title_cell = extract_docstring_title(content)
    if title_cell:
        nb.cells.append(nbformat.v4.new_markdown_cell(title_cell))

    # 检测并处理 main() 函数结构
    # Detect and handle main() function structure
    header_code, main_body, has_main = extract_main_body(content)

    if has_main:
        print(f"Detected main() function structure, extracting body...")

        # 处理头部代码（imports、常量、辅助函数等）
        # Process header code (imports, constants, helper functions, etc.)
        header_parts = split_by_step_markers(header_code)
        process_parts(nb, header_parts)

        # 处理 main() 函数体
        # Process main() function body
        main_parts = split_by_step_markers(main_body)
        process_parts(nb, main_parts)

    else:
        # 原有逻辑：处理顶层代码
        # Original logic: process top-level code
        parts = split_by_step_markers(content)
        process_parts(nb, parts)

    # 确定输出文件名
    # Determine output filename
    if output_file is None:
        output_file = Path(py_file).with_suffix('.ipynb')

    # 保存 notebook
    # Save notebook
    with open(output_file, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Converted: {py_file} -> {output_file}")
    print(f"Total cells: {len(nb.cells)}")

    return output_file


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_to_notebook.py <python_file> [output_file]")
        print()
        print("Supports:")
        print("  - Top-level code with # ==== section markers")
        print("  - Code inside main() function with # ==== section markers")
        sys.exit(1)

    py_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    py_to_notebook(py_file, output_file)
