"""
Cheat Sheet HTML Builder (v2 — Simplified)
============================================
Reads a structured JSON file and produces a print-ready HTML cheat sheet.

Layout: 11in x 8.5in (US Letter Landscape), 4 columns per page.
Each section = bullets + optional table. No colored boxes.

Usage (run directly from skill directory, no need to copy):
    uv run python build_script_template.py <input.json> [output.html]

    If output.html is not specified, it defaults to the same name as
    the input JSON with '_final.html' suffix (e.g. midterm_cheat_sheet.json
    → midterm_cheat_sheet_final.html).

Examples:
    uv run python .agent/skills/learning-cheat_sheet/references/build_script_template.py courses/ml/notes/midterm_cheat_sheet.json
    uv run python .agent/skills/learning-cheat_sheet/references/build_script_template.py courses/nlp/notes/midterm_cheat_sheet.json courses/nlp/notes/output.html
"""

import json
import sys
from pathlib import Path

# ============================================================
# CSS — print-optimized, simplified layout
# ============================================================
CSS = r"""
@page { size: 11in 8.5in; margin: 4mm; }
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: 'Consolas','Courier New',monospace;
  font-size: 5pt;
  line-height: 1.2;
  color: #111;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.page {
  width: 27.1cm;
  height: 20.4cm;
  overflow: hidden;
  position: relative;
  page-break-after: always;
  column-count: 3;
  column-gap: 4px;
  column-rule: 0.3px solid #ddd;
}
.page:last-child { page-break-after: avoid; }

.hdr {
  column-span: all;
  text-align: center;
  font-size: 6pt;
  font-weight: bold;
  border-bottom: 0.6px solid #333;
  padding-bottom: 1px;
  margin-bottom: 2px;
}
/* ── Week block ── */
.wk {
  break-inside: avoid;
  border: 0.3px solid #ddd;
  padding: 1.5px 2px;
  margin-bottom: 2px;
}
.wt {
  font-size: 5.5pt;
  font-weight: bold;
  background: #1a1a2e;
  color: #fff;
  padding: 0.8px 3px;
  margin: -1.5px -2px 1.5px -2px;
  letter-spacing: 0.2px;
}
/* ── Section title ── */
.st {
  font-size: 5pt;
  font-weight: bold;
  border-bottom: 0.4px solid #999;
  margin: 2px 0 0.5px 0;
  padding-bottom: 0.3px;
}
/* ── Bullets ── */
ul { padding-left: 7px; margin: 0.3px 0; }
li { margin: 0; font-size: 4.8pt; line-height: 1.18; }
/* ── Tables ── */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.5px 0;
  font-size: 4.7pt;
}
th, td {
  border: 0.3px solid #ccc;
  padding: 0.3px 1.5px;
  text-align: left;
  vertical-align: top;
}
th { background: #eee; font-weight: bold; }
tr:nth-child(even) td { background: #fafafa; }
/* ── Inline code ── */
code { background:#eee; padding:0 1px; font-size:4.5pt; }
/* ── Code blocks ── */
.code { background:#f5f5f5; padding:1px 2px; font-size:4.5pt; white-space:pre-wrap; border-left:1.5px solid #1a1a2e; margin:0.5px 0; }
"""


# ============================================================
# Rendering helpers
# ============================================================
def esc(s: str) -> str:
    """Escape HTML special characters."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_table(t: dict) -> str:
    """Render a table dict with headers and rows."""
    h = "<table><tr>" + "".join(f"<th>{c}</th>" for c in t["headers"]) + "</tr>"
    for row in t["rows"]:
        h += "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
    return h + "</table>"


def render_section(sec: dict) -> str:
    """Render a single section: title + bullets + optional table."""
    h = f'<div class="st">{esc(sec["title"])}</div>'
    # Bullets (content)
    if "content" in sec and sec["content"]:
        h += "<ul>" + "".join(f"<li>{c}</li>" for c in sec["content"]) + "</ul>"
    # Table
    if "table" in sec:
        h += render_table(sec["table"])
    return h


def render_week(wk: dict) -> str:
    """Render a full week block."""
    h = f'<div class="wk"><div class="wt">{wk["id"]}: {esc(wk["title"])}</div>'
    for sec in wk["sections"]:
        h += render_section(sec)
    return h + "</div>"


def render_milestones(ms: list) -> str:
    """Render milestones timeline block."""
    h = '<div class="wk"><div class="wt">Milestones</div>'
    h += '<table><tr><th>Year</th><th>Event</th></tr>'
    for m in ms:
        h += f'<tr><td><b>{m["year"]}</b></td><td>{m["event"]}</td></tr>'
    return h + "</table></div>"


def render_flash(cards: list) -> str:
    """Render quick review flash cards block."""
    h = '<div class="wk"><div class="wt">⚡ Quick Review</div><ul>'
    for c in cards:
        h += f"<li>✅ {c}</li>"
    return h + "</ul></div>"


# ============================================================
# Main build logic
# ============================================================
def build(input_path: str, output_path: str):
    data = json.loads(Path(input_path).read_text(encoding="utf-8"))

    # Collect pages from JSON
    json_pages = data.get("pages", [])

    pages_content: list[tuple] = []
    all_weeks: list[dict] = []

    for page_def in json_pages:
        page_week_ids = []
        page_html = ""
        for wk in page_def["weeks"]:
            all_weeks.append(wk)
            wid = wk["id"]
            page_week_ids.append(wid)
            page_html += render_week(wk)
        pages_content.append((page_week_ids, page_html))

    # Add milestones and flash cards to last page
    if data.get("milestones"):
        last_idx = len(pages_content) - 1
        chunk, content = pages_content[last_idx]
        content += render_milestones(data["milestones"])
        if data.get("flash_cards"):
            content += render_flash(data["flash_cards"])
        pages_content[last_idx] = (chunk, content)

    # Build HTML pages
    title = data.get("title", "Cheat Sheet")
    pages_html = ""
    for idx, (chunk, content) in enumerate(pages_content):
        page_num = idx + 1
        range_label = f"{chunk[0]}–{chunk[-1]}" if len(chunk) > 1 else chunk[0]
        pages_html += f"""
<div class="page">
  <div class="hdr">{esc(title)} — PAGE {page_num} ({range_label})</div>

  {content}
</div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
{pages_html}
</body>
</html>"""

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"✅ Built {output_path} ({len(html):,} bytes)")
    print(f"   {len(pages_content)} page(s), {len(all_weeks)} week(s)")
    for idx, (chunk, _) in enumerate(pages_content):
        print(f"   Page {idx+1}: {'+'.join(chunk)}")


# ============================================================
# CLI entry point
# ============================================================
def main():
    if len(sys.argv) < 2:
        print("Usage: python build_script_template.py <input.json> [output.html]")
        print()
        print("  input.json   Path to the structured cheat sheet JSON file")
        print("  output.html  (optional) Path for generated HTML file")
        print("               Defaults to <input_stem>_final.html")
        sys.exit(1)

    input_json = Path(sys.argv[1]).resolve()
    if not input_json.exists():
        print(f"❌ Input file not found: {input_json}")
        sys.exit(1)

    if len(sys.argv) > 2:
        output_html = Path(sys.argv[2]).resolve()
    else:
        # Default: same directory as input, with _final.html suffix
        output_html = input_json.parent / (input_json.stem + "_final.html")

    print(f"📄 Input:  {input_json}")
    print(f"📝 Output: {output_html}")
    build(str(input_json), str(output_html))


if __name__ == "__main__":
    main()
