"""
Merge all cheat_sheet_w*.md files and convert to cheat_sheet_unified.html
Produces a 4-column, 2-page print-ready cheat sheet with MathJax support.
"""
import re, os, glob

def escape(text):
    """Escape HTML special chars but preserve intentional HTML entities."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('&amp;amp;', '&amp;')
    return text

def process_inline(text):
    """Process inline markdown: bold, italic, code, math.
    Math ($...$) and code (`...`) content is preserved verbatim."""
    result = []
    i = 0
    n = len(text)

    while i < n:
        # Code span
        if text[i] == '`':
            j = text.find('`', i + 1)
            if j == -1:
                j = n
            inner = text[i+1:j]
            result.append(f'<code>{escape(inner)}</code>')
            i = j + 1
            continue

        # Math span $...$
        if text[i] == '$':
            j = text.find('$', i + 1)
            if j == -1:
                j = n
            math_content = text[i:j+1]
            result.append(math_content)
            i = j + 1
            continue

        # Normal text — collect until next $ or `
        j = i
        while j < n and text[j] != '$' and text[j] != '`':
            j += 1
        segment = text[i:j]
        s = escape(segment)
        # Bold **...**
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        # Italic *...*
        s = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', s)
        # Strikethrough ~~...~~
        s = re.sub(r'~~(.+?)~~', r'<del>\1</del>', s)
        result.append(s)
        i = j

    return ''.join(result)

def smart_split_pipe(line, expected_cols=0):
    """Split a markdown table row by |, respecting $...$, `...`, (...) and \\|."""
    PLACEHOLDER = '\x00'
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]

    protected = []
    in_math = False
    in_code = False
    paren_depth = 0
    i = 0

    while i < len(s):
        ch = s[i]
        if ch == '\\' and i + 1 < len(s):
            protected.append(ch)
            protected.append(s[i + 1])
            i += 2
            continue
        if ch == '`' and not in_math:
            in_code = not in_code
        elif ch == '$' and not in_code:
            in_math = not in_math
        elif ch == '(' and not in_math and not in_code:
            paren_depth += 1
        elif ch == ')' and not in_math and not in_code:
            paren_depth = max(0, paren_depth - 1)
        if ch == '|' and (in_math or in_code or paren_depth > 0):
            protected.append(PLACEHOLDER)
        else:
            protected.append(ch)
        i += 1

    text = ''.join(protected)
    cells = text.split('|')
    if expected_cols > 0 and len(cells) > expected_cols:
        first_cells = cells[:expected_cols - 1]
        last_cell = '|'.join(cells[expected_cols - 1:])
        cells = first_cells + [last_cell]
    cells = [c.strip().replace(PLACEHOLDER, '|') for c in cells]
    return cells

def parse_table(lines):
    """Parse markdown table lines into HTML table."""
    if len(lines) < 2:
        return ''
    sep_cols = len([c for c in lines[1].strip().strip('|').split('|') if c.strip()])
    header = smart_split_pipe(lines[0], sep_cols)
    num_cols = len(header)
    rows = []
    for line in lines[2:]:
        cols = smart_split_pipe(line, num_cols)
        rows.append(cols)

    html_parts = ['<table>', '<thead>', '<tr>']
    for h in header:
        html_parts.append(f'<th>{process_inline(h)}</th>')
    html_parts.append('</tr></thead><tbody>')
    for row in rows:
        html_parts.append('<tr>')
        for cell in row:
            html_parts.append(f'<td>{process_inline(cell)}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody></table>')
    return '\n'.join(html_parts)

def convert_md_to_html(md_text):
    """Convert markdown content to HTML body content."""
    lines = md_text.split('\n')
    html_parts = []
    i = 0
    in_code_block = False
    code_block_lines = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code blocks
        if stripped.startswith('```'):
            if in_code_block:
                code_content = '\n'.join(code_block_lines)
                html_parts.append(f'<pre><code>{escape(code_content)}</code></pre>')
                code_block_lines = []
                in_code_block = False
            else:
                in_code_block = True
            i += 1
            continue
        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if stripped == '---':
            html_parts.append('<hr>')
            i += 1
            continue

        # H1 = Week title
        if stripped.startswith('# ') and not stripped.startswith('## '):
            title = stripped[2:]
            if html_parts and any('<div class="week-block">' in p for p in html_parts):
                html_parts.append('</div>')
            html_parts.append(f'<div class="week-block"><h1>{process_inline(title)}</h1>')
            i += 1
            continue

        # H2 = Section
        if stripped.startswith('## ') and not stripped.startswith('### '):
            title = stripped[3:]
            section_map = {'1.': '一.', '2.': '二.', '3.': '三.', '4.': '四.', '5.': '五.'}
            display_title = title
            for num, cn in section_map.items():
                if title.startswith(num):
                    display_title = cn + title[2:]
                    break
            html_parts.append(f'<h2>{process_inline(display_title)}</h2>')
            i += 1
            continue

        # H3 = Sub-topic
        if stripped.startswith('### '):
            title = stripped[4:]
            html_parts.append(f'<h3>{process_inline(title)}</h3>')
            i += 1
            continue

        # Table detection
        if '|' in stripped and not stripped.startswith('>'):
            next_i = i + 1
            if next_i < len(lines) and re.match(r'^\s*\|?[\s\-:|]+\|[\s\-:|]+\|?\s*$', lines[next_i].strip()):
                table_lines = []
                while i < len(lines) and '|' in lines[i].strip() and lines[i].strip():
                    table_lines.append(lines[i])
                    i += 1
                html_parts.append(parse_table(table_lines))
                continue

        # Blockquote
        if stripped.startswith('> '):
            text = process_inline(stripped[2:])
            html_parts.append(f'<p style="border-left:1.5px solid #1a1a2e; padding-left:3px; margin:1px 0; background:#f8f8ff;">{text}</p>')
            i += 1
            continue

        # Italic-only line
        if stripped.startswith('_') and stripped.endswith('_'):
            html_parts.append(f'<p><em>{escape(stripped[1:-1])}</em></p>')
            i += 1
            continue

        # Bullet list
        if stripped.startswith('- '):
            list_items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                item = lines[i].strip()[2:]
                list_items.append(f'<li>{process_inline(item)}</li>')
                i += 1
            html_parts.append('<ul>' + ''.join(list_items) + '</ul>')
            continue

        # Numbered list
        if re.match(r'^\d+\.', stripped):
            list_items = []
            while i < len(lines) and re.match(r'^\d+\.', lines[i].strip()):
                item = re.sub(r'^\d+\.\s*', '', lines[i].strip())
                list_items.append(f'<li>{process_inline(item)}</li>')
                i += 1
            html_parts.append('<ol>' + ''.join(list_items) + '</ol>')
            continue

        # Regular paragraph
        html_parts.append(f'<p>{process_inline(stripped)}</p>')
        i += 1

    # Close last week-block
    if any('<div class="week-block">' in p for p in html_parts):
        html_parts.append('</div>')

    return '\n'.join(html_parts)


# ─────────────────── CSS ───────────────────
CSS = """
@page {
  size: 8.5in 11in;
  margin: 0;
}
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Microsoft YaHei', 'Segoe UI', 'Noto Sans SC', Arial, sans-serif;
  font-size: 4.4pt;
  line-height: 1.15;
  color: #000;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page {
  column-count: 4;
  column-gap: 3px;
  column-rule: 0.3px solid #ccc;
  column-fill: auto;
  padding: 3mm;
  width: 8.5in;
  height: 11in;
  overflow: hidden;
  page-break-after: always;
}

/* Week block */
.week-block {
  border: 0.3px solid #ddd;
  padding: 1px 2px;
  margin-bottom: 2px;
}

/* H1 = Week title */
h1 {
  font-size: 5.25pt;
  font-weight: bold;
  background: #1a1a2e;
  color: #fff;
  padding: 0.5px 3px;
  margin: -1px -2px 1px -2px;
  break-after: avoid;
  letter-spacing: -0.2px;
}

/* H2 = Section */
h2 {
  font-size: 4.7pt;
  font-weight: bold;
  color: #1a1a2e;
  border-bottom: 0.5px solid #1a1a2e;
  margin: 1px 0 0.5px 0;
  break-after: avoid;
}

/* H3 = Sub-topic */
h3 {
  font-size: 4.4pt;
  font-weight: bold;
  color: #333;
  margin: 1px 0 0.3px 0;
  border-bottom: 0.2px solid #aaa;
  break-after: avoid;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.5px 0 1px 0;
  font-size: 4pt;
}
th, td {
  border: 0.2px solid #bbb;
  padding: 0.2px 1.5px;
  text-align: left;
  vertical-align: top;
  word-wrap: break-word;
}
th {
  background: #e8e8f0;
  font-weight: bold;
  font-size: 4pt;
}
td { font-size: 3.6pt; }

/* Code */
code {
  background: #f0f0f0;
  padding: 0 1px;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 3.6pt;
  border-radius: 1px;
}
pre {
  background: #f5f5f5;
  padding: 2px 3px;
  margin: 1px 0;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 3.4pt;
  line-height: 1.2;
  white-space: pre;
  border: 0.2px solid #ddd;
  border-radius: 1px;
}

em { font-style: italic; color: #666; }
p { margin: 0.3px 0; font-size: 4pt; }
ul, ol { padding-left: 6px; margin: 0.3px 0; }
li { font-size: 3.8pt; margin: 0; }

/* Section 5 (Exam Traps) highlight */
h2:last-of-type ~ table td:first-child,
.trap-cell { color: #c0392b; }

hr {
  border: none;
  border-top: 0.3px solid #999;
  margin: 1px 0;
}

@media print {
  body { margin: 0; }
  .no-print { display: none; }
  .page { overflow: hidden; }
}

@media screen {
  body {
    background: #555;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    padding: 20px;
  }
  .page {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
  }
}
"""


def build_html(pages_content):
    """Build full HTML with N pages."""
    pages_html = []
    for idx, content in enumerate(pages_content):
        pages_html.append(f'''<div class="page">
{content}
</div>''')

    num_pages = len(pages_content)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AISD Final Cheat Sheet</title>
<style>
{CSS}
</style>

<script>
MathJax = {{
  tex: {{
    inlineMath: [['$', '$']],
    displayMath: [['$$', '$$']],
  }},
  svg: {{
    fontCache: 'global',
    scale: 0.7
  }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>

</head>
<body>
<div class="no-print" style="text-align:center; padding:10px; font-family:sans-serif; font-size:14px; color:#fff;">
  AISD Final Cheat Sheet | {num_pages} pages | Ctrl+P to print
</div>
{''.join(pages_html)}
</body>
</html>"""


def main():
    review_dir = os.path.dirname(os.path.abspath(__file__))

    # Ordered list of cheat sheet files
    md_files = [
        'cheat_sheet_w1w2.md',
        'cheat_sheet_w3.md',
        'cheat_sheet_w4.md',
        'cheat_sheet_w6.md',
        'cheat_sheet_w7w9.md',
        'cheat_sheet_w11.md',
        'cheat_sheet_w12.md',
    ]

    # Read and merge all markdown files
    merged_parts = []
    for fname in md_files:
        fpath = os.path.join(review_dir, fname)
        if not os.path.exists(fpath):
            print(f"[WARN] Missing: {fname}")
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        merged_parts.append(content)
        print(f"  [OK] {fname} ({len(content)} bytes)")

    merged_md = '\n\n'.join(merged_parts)

    # Save merged markdown
    merged_md_path = os.path.join(review_dir, 'cheat_sheet_unified.md')
    with open(merged_md_path, 'w', encoding='utf-8') as f:
        f.write(merged_md)
    print(f"\n[OK] Merged markdown: {merged_md_path} ({len(merged_md)} bytes)")

    # Convert to HTML
    body = convert_md_to_html(merged_md)

    # Split into 2 pages:
    # Page 1: W1-W2, W3, W4, W6  (with sig box)
    # Page 2: W7/W9, W11, W12
    block_starts = [m.start() for m in re.finditer(r'<div class="week-block">', body)]
    print(f"  Found {len(block_starts)} week-blocks")

    # Split before W7/W9 (index 4)
    if len(block_starts) >= 5:
        split_idx = block_starts[4]  # Before W7/W9
        page1 = body[:split_idx].rstrip()
        page2 = body[split_idx:].rstrip()
        pages = [page1, page2]
    elif len(block_starts) >= 3:
        mid = len(block_starts) // 2
        idx = block_starts[mid]
        page1 = body[:idx].rstrip()
        page2 = body[idx:].rstrip()
        pages = [page1, page2]
    else:
        pages = [body]

    html_output = build_html(pages)

    out_path = os.path.join(review_dir, 'cheat_sheet_unified.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"[OK] HTML output: {out_path} ({len(html_output)} bytes)")
    for i, p in enumerate(pages):
        print(f"   Page {i+1}: {len(p)} chars")


if __name__ == '__main__':
    main()
