"""
Convert Python script to Jupyter Notebook using # ==== section markers as cell boundaries.
Uses the existing step section markers instead of requiring explicit # %% markers.
"""

import nbformat
import re
import sys
from pathlib import Path


def py_to_notebook(py_file: str, output_file: str = None):
    """将Python脚本转换为Jupyter Notebook
    Convert Python script to Jupyter Notebook"""
    
    # 读取Python文件
    # Read Python file
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建notebook
    # Create notebook
    nb = nbformat.v4.new_notebook()
    
    # 使用 # ==== 分隔符分割内容
    # Split content using # ==== separators
    # 匹配模式：# ===...=== 开头行 + 标题注释行 + # ===...=== 结尾行
    pattern = r'(# ={40,}\r?\n(?:# .+?\r?\n)+# ={40,})'
    
    parts = re.split(pattern, content)
    
    # 第一部分是文件头（imports和配置）
    # First part is file header (imports and configuration)
    if parts[0].strip():
        nb.cells.append(nbformat.v4.new_code_cell(parts[0].strip()))
    
    # 处理每个步骤
    # Process each step
    i = 1
    while i < len(parts):
        if re.match(r'# ={60,}', parts[i]):
            # 这是一个步骤分隔符
            # This is a step separator
            step_header = parts[i]
            step_code = parts[i + 1].strip() if i + 1 < len(parts) else ''
            
            # 合并分隔符和代码
            # Combine separator and code
            full_cell = step_header + '\n' + step_code
            nb.cells.append(nbformat.v4.new_code_cell(full_cell.strip()))
            
            i += 2
        else:
            # 不应该发生，但以防万一
            # Shouldn't happen, but just in case
            if parts[i].strip():
                nb.cells.append(nbformat.v4.new_code_cell(parts[i].strip()))
            i += 1
    
    # 确定输出文件名
    # Determine output filename
    if output_file is None:
        output_file = Path(py_file).with_suffix('.ipynb')
    
    # 保存notebook
    # Save notebook
    with open(output_file, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    print(f"Converted: {py_file} -> {output_file}")
    print(f"Total cells: {len(nb.cells)}")
    
    return output_file


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_to_notebook.py <python_file> [output_file]")
        sys.exit(1)
    
    py_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    py_to_notebook(py_file, output_file)
