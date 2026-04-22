"""
Storyline → Marp Slides 自动生成器
===================================
读取 storyline.md，按 ## 分节，每节 = 一页 Marp slide。
内容原封不动，不做任何改写。

用法:
  python generate_slides.py <storyline.md> -o <slides.md>
"""
import argparse
import re
from pathlib import Path

MARP_HEADER = """---
marp: true
theme: uncover
class: invert
paginate: true
style: |
  section {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    font-family: 'Microsoft YaHei UI', 'Segoe UI', sans-serif;
    padding: 40px 60px;
  }
  h1 { color: #ffd700; font-size: 42px; }
  h2 { color: #64b5f6; font-size: 32px; }
  h3 { color: #81c784; font-size: 26px; }
  strong { color: #ffd700; }
  code { color: #80cbc4; background: rgba(128,203,196,0.1); }
  pre { font-size: 18px; }
  blockquote { border-left: 4px solid #ffd700; background: rgba(255,215,0,0.08); padding: 8px 16px; font-size: 20px; }
  table { font-size: 18px; width: 100%; }
  th { background: rgba(100,181,246,0.2); color: #64b5f6; }
  td { border-color: rgba(255,255,255,0.1); }
  li { font-size: 20px; line-height: 1.5; }
  p { font-size: 20px; line-height: 1.6; }
---
"""


def _find_code_fence_regions(md_text: str) -> list[tuple[int, int]]:
    """找出所有 ``` 围栏代码块的 (start, end) 字符偏移区间。"""
    regions = []
    fence_re = re.compile(r'^(`{3,})', re.MULTILINE)
    open_pos = None
    for m in fence_re.finditer(md_text):
        if open_pos is None:
            open_pos = m.start()
        else:
            regions.append((open_pos, m.end()))
            open_pos = None
    # 如果有未闭合的围栏，视为延伸到文件末尾
    if open_pos is not None:
        regions.append((open_pos, len(md_text)))
    return regions


def _inside_code_fence(pos: int, regions: list[tuple[int, int]]) -> bool:
    """判断字符位置 pos 是否位于任何代码围栏区间内。"""
    for start, end in regions:
        if start <= pos < end:
            return True
    return False


def split_sections(md_text: str) -> list[dict]:
    """按 ## 标题拆分 storyline 为多个 section。
    
    返回 [{"title": "...", "body": "..."}]
    跳过位于 ``` 围栏代码块内部的 # 行（避免把代码注释当作标题）。
    """
    sections = []
    # 匹配 #, ##, ### 开头的行（不匹配 #### 或更深层级）
    pattern = re.compile(r'^(#{1,3})\s+(.+)$', re.MULTILINE)
    
    # 先标记所有代码围栏区间
    code_regions = _find_code_fence_regions(md_text)
    
    # 过滤掉落在代码块内的 "假标题"
    matches = [
        m for m in pattern.finditer(md_text)
        if not _inside_code_fence(m.start(), code_regions)
    ]
    
    if not matches:
        # 没有 ## 标题，整个文件当作一页
        return [{"title": "", "body": md_text.strip()}]
    
    for i, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()
        
        # 获取 body：从当前标题末尾 到 下一个标题之前（扁平切分，不做层级嵌套）
        start = match.end()
        
        # 每个 heading 的 body 截止到下一个 heading（无论层级）
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(md_text)
        
        body = md_text[start:end].strip()
        
        # #, ##, ### 都作为 slide 分割点
        if level <= 3:
            sections.append({"title": title, "body": body, "level": level})
    
    # 合并空 body 的父级标题到下一个子级 slide
    # 例如 ## 第一章（无 body）+ ### 1.1（有 body）→ 合并为一页，标题带章节前缀
    merged = []
    i = 0
    while i < len(sections):
        sec = sections[i]
        # 如果当前节 body 为空，且下一节层级更深，合并
        if (not sec["body"].strip()
                and i + 1 < len(sections)
                and sections[i + 1]["level"] > sec["level"]):
            next_sec = sections[i + 1]
            next_sec["parent_title"] = sec["title"]
            next_sec["parent_level"] = sec["level"]
            merged.append(next_sec)
            i += 2  # 跳过已合并的两个
        else:
            merged.append(sec)
            i += 1
    
    return merged


def section_to_slide(section: dict) -> str:
    """将一个 section 转为 Marp slide 内容。"""
    title = section["title"]
    body = section["body"]
    level = section.get("level", 2)
    
    # 清理 body：去掉首尾的 --- 分隔线（storyline 自带的），
    # 避免和 Marp 的 slide 分隔符重复产生空白页
    body_clean = body.strip()
    while body_clean.startswith('---'):
        body_clean = body_clean[3:].strip()
    while body_clean.endswith('---'):
        body_clean = body_clean[:-3].strip()
    
    # 按原始层级输出标题
    prefix = '#' * level
    header = f"{prefix} {title}"
    
    # 如果有合并的父级标题，在子标题上方显示
    if "parent_title" in section:
        parent_prefix = '#' * section["parent_level"]
        header = f"{parent_prefix} {section['parent_title']}\n\n{header}"
    
    slide = f"{header}\n\n{body_clean}" if body_clean else header
    
    return slide


def generate_marp(storyline_path: str, output_path: str, max_lines: int = 0):
    """主函数：读取 storyline，生成 Marp slides。"""
    md_text = Path(storyline_path).read_text(encoding='utf-8')
    
    # 移除 YAML frontmatter（如果有）
    if md_text.startswith('---'):
        end = md_text.find('---', 3)
        if end > 0:
            md_text = md_text[end + 3:].strip()
    
    sections = split_sections(md_text)
    
    slides = []
    for sec in sections:
        slide_content = section_to_slide(sec)
        if slide_content.strip():
            slides.append(slide_content)
    
    # 组装最终 Marp 文件
    marp_content = MARP_HEADER.strip() + '\n\n'
    marp_content += '\n\n---\n\n'.join(slides)
    marp_content += '\n'
    
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(marp_content, encoding='utf-8')
    
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print(f"Generated {len(slides)} slides -> {output_path}")
    print(f"Slide titles:")
    for i, sec in enumerate(sections):
        if sec['title']:
            print(f"  [{i+1:2d}] {sec['title']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Storyline → Marp Slides 自动生成')
    parser.add_argument('storyline', help='输入的 storyline.md 文件路径')
    parser.add_argument('-o', '--output', default='slides/slides.md', help='输出的 Marp slides 路径')
    args = parser.parse_args()
    
    generate_marp(args.storyline, args.output)
