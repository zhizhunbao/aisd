"""
Cheat Sheet HTML Builder Template
==================================
Reads a structured JSON file and produces a print-ready HTML cheat sheet.

Layout: 8.5in x 11in (US Letter), 3 columns per page, 3 weeks per page.
Top-left 5cm x 5cm signature/proctor box on each page.

Usage:
    uv run python build_cheatsheet.py

Customize:
    - INPUT_JSON: path to the structured JSON data file
    - OUTPUT_HTML: path for the generated HTML file
    - WEEKS_PER_PAGE: how many weeks to group per page (default: 3)
    - QUIZ_TO_WEEK: mapping from quiz names to week IDs
"""

import json
import sys
from pathlib import Path

# ============================================================
# Configuration — customize these for each course/exam
# ============================================================
INPUT_JSON = "cheat_sheet.json"       # 输入 JSON 文件路径
OUTPUT_HTML = "cheat_sheet_final.html" # 输出 HTML 文件路径
WEEKS_PER_PAGE = 3                     # 每页显示的周数

# Quiz → Week mapping (根据课程调整)
# Map quiz titles to week IDs for merging key points
QUIZ_TO_WEEK = {
    # "Quiz 1 — Topic": "W1",
    # "Quiz 2 — Topic": "W2",
}

# ============================================================
# CSS — print-optimized layout
# ============================================================
CSS = r"""
@page { size: 8.5in 11in; margin: 4mm; }
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: 'Consolas','Courier New',monospace;
  font-size: 5pt;
  line-height: 1.18;
  color: #000;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.page {
  width: 20.4cm;
  height: 27.1cm;
  overflow: hidden;
  position: relative;
  page-break-after: always;
  column-count: 3;
  column-gap: 4px;
  column-rule: 0.3px solid #ccc;
}
.page:last-child { page-break-after: avoid; }
.sig {
  width: 5cm;
  height: 5cm;
  border: 1.5px dashed #999;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 7pt;
  color: #bbb;
  background: #fff;
  margin-bottom: 4px;
  break-inside: avoid;
}
.hdr {
  column-span: all;
  text-align: center;
  font-size: 6.5pt;
  font-weight: bold;
  border-bottom: 0.8px solid #000;
  padding-bottom: 1px;
  margin-bottom: 2px;
}
.wk {
  break-inside: avoid;
  border: 0.3px solid #ddd;
  padding: 1.5px 2px;
  margin-bottom: 2px;
}
.wt {
  font-size: 5.5pt;
  font-weight: bold;
  background: #222;
  color: #fff;
  padding: 0.5px 3px;
  margin: -1.5px -2px 1px -2px;
}
.st {
  font-size: 5.2pt;
  font-weight: bold;
  border-bottom: 0.3px solid #888;
  margin: 1.5px 0 0.5px 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.5px 0;
  font-size: 4.8pt;
}
th, td {
  border: 0.3px solid #ccc;
  padding: 0.3px 1.5px;
  text-align: left;
  vertical-align: top;
}
th { background: #eee; font-weight: bold; }
ul { padding-left: 7px; margin: 0.3px 0; }
li { margin: 0; font-size: 4.8pt; }
code { background:#eee; padding:0 1px; font-size:4.5pt; }
.f { background:#f5f5e0; padding:0.5px 2px; margin:0.5px 0; font-size:4.8pt; }
.w { background:#fff1f1; padding:0.5px 2px; margin:0.5px 0; border-left:1.5px solid #d33; font-size:4.7pt; }
.g { background:#f0f7f0; padding:0.5px 2px; margin:0.5px 0; border-left:1.5px solid #3a3; font-size:4.7pt; }
.kp { background:#f0f0ff; padding:0.5px 2px; margin:1px 0; border-left:1.5px solid #33a; font-size:4.7pt; }
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
    """Render a single section within a week block."""
    h = f'<div class="st">{esc(sec["title"])}</div>'
    if "content" in sec:
        h += "<ul>" + "".join(f"<li>{c}</li>" for c in sec["content"]) + "</ul>"
    if "table" in sec:
        h += render_table(sec["table"])
    if "formulas" in sec:
        h += '<div class="f">' + "<br>".join(sec["formulas"]) + "</div>"
    if "examples" in sec:
        for ex in sec["examples"]:
            h += f'<div class="g"><b>{esc(ex["label"])}</b><br>'
            h += "<br>".join(ex["steps"]) + "</div>"
    if "content_extra" in sec:
        h += "<ul>" + "".join(f"<li>{c}</li>" for c in sec["content_extra"]) + "</ul>"
    if "traps" in sec:
        h += '<div class="w">' + "<br>".join("⚠️ " + t for t in sec["traps"]) + "</div>"
    return h


def render_week(wk: dict, keypoints: list | None = None) -> str:
    """Render a full week block with optional quiz key points."""
    h = f'<div class="wk"><div class="wt">{wk["id"]}: {esc(wk["title"])}</div>'
    for sec in wk["sections"]:
        h += render_section(sec)
    if keypoints:
        h += '<div class="kp"><b>📌 Key Points</b><ul>'
        for kp in keypoints:
            h += f"<li>{kp}</li>"
        h += "</ul></div>"
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
def build(input_path: str = INPUT_JSON, output_path: str = OUTPUT_HTML):
    data = json.loads(Path(input_path).read_text(encoding="utf-8"))

    # Build quiz key points per week
    week_keypoints: dict[str, list[str]] = {}
    for quiz in data.get("quiz_answers", []):
        wk = QUIZ_TO_WEEK.get(quiz["quiz"], "")
        if wk:
            if wk not in week_keypoints:
                week_keypoints[wk] = []
            for q in quiz["questions"]:
                week_keypoints[wk].append(q.get("topic", q.get("key_point", "")))

    # Collect all weeks
    all_weeks: list[dict] = []
    for page in data.get("pages", data.get("sides", [])):
        for wk in page["weeks"]:
            all_weeks.append(wk)

    weeks_by_id = {wk["id"]: wk for wk in all_weeks}
    week_ids = [wk["id"] for wk in all_weeks]

    # Group weeks into pages
    pages_content: list[str] = []
    for i in range(0, len(week_ids), WEEKS_PER_PAGE):
        chunk = week_ids[i:i + WEEKS_PER_PAGE]
        content = ""
        for wid in chunk:
            wk = weeks_by_id[wid]
            kp = week_keypoints.get(wid)
            content += render_week(wk, kp)
        pages_content.append((chunk, content))

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
  <div class="sig">Proctor<br>Signature<br><span style="font-size:5pt">(5cm × 5cm)</span></div>
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


if __name__ == "__main__":
    # Allow overriding paths via command line args
    inp = sys.argv[1] if len(sys.argv) > 1 else INPUT_JSON
    out = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_HTML
    build(inp, out)
