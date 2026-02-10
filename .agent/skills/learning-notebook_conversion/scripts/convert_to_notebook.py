"""
Convert Python script to Jupyter Notebook using # ==== section markers as cell boundaries.
将 Python 脚本转换为 Jupyter Notebook，使用 # ==== 分隔符作为 cell 边界。

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


def split_by_section_markers(content: str) -> list[str]:
    """按 # ==== 分隔符分割内容
    Split content by # ==== section markers"""

    # 匹配模式：# ===...=== 开头行 + 标题注释行 + # ===...=== 结尾行
    # Pattern: # ===...=== line + title comment lines + # ===...=== line
    pattern = r'(# ={40,}\r?\n(?:# .+?\r?\n)+# ={40,})'

    parts = re.split(pattern, content)
    return parts


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

    # 检测并处理 main() 函数结构
    # Detect and handle main() function structure
    header_code, main_body, has_main = extract_main_body(content)

    if has_main:
        print(f"Detected main() function structure, extracting body...")

        # 处理头部代码（imports、常量、辅助函数等）
        # Process header code (imports, constants, helper functions, etc.)
        header_parts = split_by_section_markers(header_code)

        # 添加第一部分（通常是 imports）
        # Add first part (usually imports)
        if header_parts[0].strip():
            nb.cells.append(nbformat.v4.new_code_cell(header_parts[0].strip()))

        # 处理头部中的其他段落
        # Process other sections in header
        i = 1
        while i < len(header_parts):
            if re.match(r'# ={40,}', header_parts[i]):
                step_header = header_parts[i]
                step_code = header_parts[i + 1].strip() if i + 1 < len(header_parts) else ''
                full_cell = step_header + '\n' + step_code
                nb.cells.append(nbformat.v4.new_code_cell(full_cell.strip()))
                i += 2
            else:
                if header_parts[i].strip():
                    nb.cells.append(nbformat.v4.new_code_cell(header_parts[i].strip()))
                i += 1

        # 处理 main() 函数体
        # Process main() function body
        main_parts = split_by_section_markers(main_body)

        # 添加 main 体的第一部分（如果有）
        # Add first part of main body (if any)
        if main_parts[0].strip():
            nb.cells.append(nbformat.v4.new_code_cell(main_parts[0].strip()))

        # 处理 main 体中的每个步骤
        # Process each step in main body
        i = 1
        while i < len(main_parts):
            if re.match(r'# ={40,}', main_parts[i]):
                step_header = main_parts[i]
                step_code = main_parts[i + 1].strip() if i + 1 < len(main_parts) else ''
                full_cell = step_header + '\n' + step_code
                nb.cells.append(nbformat.v4.new_code_cell(full_cell.strip()))
                i += 2
            else:
                if main_parts[i].strip():
                    nb.cells.append(nbformat.v4.new_code_cell(main_parts[i].strip()))
                i += 1

    else:
        # 原有逻辑：处理顶层代码
        # Original logic: process top-level code
        parts = split_by_section_markers(content)

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
                full_cell = step_header + '\n' + step_code
                nb.cells.append(nbformat.v4.new_code_cell(full_cell.strip()))
                i += 2
            else:
                if parts[i].strip():
                    nb.cells.append(nbformat.v4.new_code_cell(parts[i].strip()))
                i += 1

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
