"""
Convert cheat_sheet_unified.md to cheat_sheet_unified.html
Preserves the existing CSS styling and 2-page 4-column layout.
"""
import re, html

def escape(text):
    """Escape HTML special chars but preserve intentional HTML entities."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # Restore common entities
    text = text.replace('&amp;amp;', '&amp;')
    return text

def process_inline(text):
    """Process inline markdown: bold, italic, code, math.
    Math ($...$) and code (`...`) content is preserved verbatim."""
    # Split into segments: math, code, and normal text
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
            # Keep the entire $...$ verbatim for MathJax
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
        result.append(s)
        i = j
    
    return ''.join(result)

def smart_split_pipe(line, expected_cols=0):
    """Split a markdown table row by |, respecting $...$, `...`, (...) and \\|.
    If expected_cols > 0, merge extra splits into the last column."""
    PLACEHOLDER = '\x00'
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    
    # Pass 1: protect | inside $...$, `...`, (...), and after backslash
    protected = []
    in_math = False
    in_code = False
    paren_depth = 0
    i = 0
    
    while i < len(s):
        ch = s[i]
        
        # Escaped char (backslash + next) — protect and skip
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
    
    # Pass 2: if we still have too many columns, merge extras into last cell
    if expected_cols > 0 and len(cells) > expected_cols:
        first_cells = cells[:expected_cols - 1]
        last_cell = '|'.join(cells[expected_cols - 1:])
        cells = first_cells + [last_cell]
    
    # Restore placeholders and strip
    cells = [c.strip().replace(PLACEHOLDER, '|') for c in cells]
    return cells

def parse_table(lines):
    """Parse markdown table lines into HTML table."""
    if len(lines) < 2:
        return ''
    
    # Count columns from separator line (line index 1)
    sep_cols = len([c for c in lines[1].strip().strip('|').split('|') if c.strip()])
    
    # Parse header
    header = smart_split_pipe(lines[0], sep_cols)
    num_cols = len(header)
    
    # Skip separator line (lines[1])
    rows = []
    for line in lines[2:]:
        cols = smart_split_pipe(line, num_cols)
        rows.append(cols)
    
    html_parts = ['<table>', '<thead>', '<tr>']
    for h in header:
        html_parts.append(f'<th>{process_inline(h)}</th>')
    html_parts.append('</tr>')
    html_parts.append('</thead>')
    html_parts.append('<tbody>')
    for row in rows:
        html_parts.append('<tr>')
        for cell in row:
            html_parts.append(f'<td>{process_inline(cell)}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody>')
    html_parts.append('</table>')
    
    return '\n'.join(html_parts)

def convert_md_to_html(md_text):
    """Convert markdown content to HTML body content."""
    lines = md_text.split('\n')
    html_parts = []
    i = 0
    in_sa_mark = False  # Track short-answer marked sections
    in_code_block = False
    code_block_lines = []
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Code blocks
        if stripped.startswith('```'):
            if in_code_block:
                # End code block
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
        
        # Skip empty lines
        if not stripped:
            i += 1
            continue
        
        # Horizontal rule
        if stripped == '---':
            html_parts.append('<hr>')
            i += 1
            continue
        
        # H1 = Week title (starts new week-block)
        if stripped.startswith('# ') and not stripped.startswith('## '):
            title = stripped[2:]
            # Close previous week-block if any
            if html_parts and any('<div class="week-block">' in p for p in html_parts):
                html_parts.append('</div>')
            html_parts.append(f'<div class="week-block"><h1>{process_inline(title)}</h1>')
            i += 1
            continue
        
        # H2 = Section
        if stripped.startswith('## ') and not stripped.startswith('### '):
            title = stripped[3:]
            # Map section numbers
            section_map = {
                '1.': '一.',
                '2.': '二.',
                '3.': '三.',
                '4.': '四.',
                '5.': '五.',
            }
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
            # Check if this is a short-answer section (SA-1, SA-2, etc.)
            if re.match(r'SA-\d+:', title) or re.match(r'B-\d+:', title):
                if in_sa_mark:
                    html_parts.append('</div>')
                html_parts.append(f'<div class="sa-mark"><h3>{process_inline(title)}</h3>')
                in_sa_mark = True
            else:
                if in_sa_mark:
                    html_parts.append('</div>')
                    in_sa_mark = False
                html_parts.append(f'<h3>{process_inline(title)}</h3>')
            i += 1
            continue
        
        # Table detection — requires a separator row (|---|) as line 2
        if '|' in stripped and not stripped.startswith('>'):
            # Peek ahead: a real table needs a separator row (|---|...) as the next line
            next_i = i + 1
            if next_i < len(lines) and re.match(r'^\s*\|?[\s\-:|]+\|[\s\-:|]+\|?\s*$', lines[next_i].strip()):
                table_lines = []
                while i < len(lines) and '|' in lines[i].strip() and lines[i].strip():
                    table_lines.append(lines[i])
                    i += 1
                html_parts.append(parse_table(table_lines))
                continue
            # Not a table — fall through to paragraph handling
        
        # Blockquote
        if stripped.startswith('> '):
            text = stripped[2:]
            # Check for bold prefix
            text = process_inline(text)
            html_parts.append(f'<p style="border-left:1.5px solid #1a1a2e; padding-left:3px; margin:1px 0; background:#f8f8ff;">{text}</p>')
            i += 1
            continue
        
        # Italic only line
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
    
    # Close any open sa-mark or week-block
    if in_sa_mark:
        html_parts.append('</div>')
    # Close last week-block
    if any('<div class="week-block">' in p for p in html_parts):
        html_parts.append('</div>')
    
    return '\n'.join(html_parts)


# CSS from original HTML
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

/* Signature box - 5cm x 5cm top-left of each page (exam requirement) */
.sig {
  width: 5cm;
  height: 5cm;
  border: 0.5px dashed #999;
  margin-bottom: 1px;
  break-inside: avoid;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #bbb;
  font-size: 4pt;
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

/* Italic */
em { font-style: italic; color: #666; }

/* Paragraphs */
p { margin: 0.3px 0; font-size: 4pt; }

/* Lists */
ul, ol { padding-left: 6px; margin: 0.3px 0; }
li { font-size: 3.8pt; margin: 0; }

/* Short-answer highlight */
.sa-mark {
  border-left: 1.5px solid #e63946;
  background: linear-gradient(90deg, #fff0f0 0%, transparent 60%);
  padding-left: 2px;
  margin-left: -3px;
}
.sa-mark > h3::before {
  content: '📝简答 ';
  color: #e63946;
  font-weight: bold;
}

/* Horizontal Rule */
hr {
  border: none;
  border-top: 0.3px solid #999;
  margin: 1px 0;
}

/* Print */
@media print {
  body { margin: 0; }
  .no-print { display: none; }
  .page { overflow: hidden; }
}

/* Screen preview */
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

def build_html(page1_content, page2_content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cheat Sheet</title>
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
  NLP Final Cheat Sheet | 2 pages | Ctrl+P to print
</div>
<div class="page">
<div class="sig">Signature / 签名</div>
{page1_content}
</div>
<div class="page">
<div class="sig">Signature / 签名</div>
{page2_content}
</div>
</body>
</html>"""


# Page break marker - split at this H1 heading
PAGE_BREAK_AT = 'W9:'

def main():
    with open(r'cheat_sheet_unified.md', 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    body = convert_md_to_html(md_text)
    
    # Split into two pages at the W9 week-block
    # Find the week-block div that contains W9
    split_marker = None
    for marker in ['W9:', 'W10:']:
        pattern = f'<div class="week-block"><h1>{marker}'
        if pattern in body:
            split_marker = pattern
            break
    
    if split_marker:
        idx = body.index(split_marker)
        # Close any open week-block before the split
        page1 = body[:idx].rstrip()
        page2 = body[idx:].rstrip()
        # Make sure page1 doesn't have a dangling open week-block div
        # (The converter already closes each week-block when a new one starts)
    else:
        # Fallback: put everything on one page
        print("[WARN] Could not find page break marker, using single page")
        page1 = body
        page2 = ''
    
    html_output = build_html(page1, page2)
    
    with open(r'cheat_sheet_unified.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print("[OK] cheat_sheet_unified.html has been updated from cheat_sheet_unified.md")
    print(f"   Output: {len(html_output)} bytes")
    print(f"   Page 1: {len(page1)} chars | Page 2: {len(page2)} chars")

if __name__ == '__main__':
    main()
