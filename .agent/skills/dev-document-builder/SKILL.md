---
name: dev-document-builder
description: "Unified document builder: create, convert, and process documents across all formats (MD ↔ DOCX ↔ PDF). Use when (1) creating formatted reports/proposals with python-docx, (2) converting MD→DOCX or DOCX→MD, (3) processing PDFs (extract/split/merge/OCR), (4) creating assignment submission documents, (5) mentions '文档生成' or 'document builder'."
---

# Document Builder — Unified Document Skill

> One skill for all document creation, conversion, and processing needs.
> 文档创建、转换、处理一站式技能。

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Document Builder                          │
├──────────┬──────────┬──────────┬──────────┬─────────────────────┤
│ Route 1  │ Route 2  │ Route 3  │ Route 4  │ Route 5            │
│ Programm │ MD→DOCX  │ DOCX→MD  │ PDF Proc │ Assignment Doc     │
│ atic Gen │ (Pandoc) │(Mammoth) │ (PyMuPDF)│ (Templates)        │
├──────────┼──────────┼──────────┼──────────┼─────────────────────┤
│python-   │pypandoc  │mammoth   │pymupdf   │python-docx +       │
│docx      │python-   │          │pdfplumber│screenshot skills    │
│          │docx      │          │pypdf     │                     │
│          │          │          │reportlab │                     │
└──────────┴──────────┴──────────┴──────────┴─────────────────────┘
```

## Quick Decision Matrix

| You want to...                        | Use Route | Key Tech               | Quality    |
| ------------------------------------- | --------- | ---------------------- | ---------- |
| Create a **polished** report/proposal | **1**     | `python-docx`          | ⭐⭐⭐⭐⭐ |
| Quickly convert MD notes → DOCX       | **2**     | Pandoc + python-docx   | ⭐⭐⭐     |
| Extract DOCX content → editable MD    | **3**     | Mammoth                | ⭐⭐⭐     |
| Extract text/tables from PDF          | **4**     | PyMuPDF / pdfplumber   | ⭐⭐⭐⭐   |
| Split textbook PDF by chapter         | **4**     | `pdf_section_split.py` | ⭐⭐⭐⭐   |
| Create lab/assignment submission doc  | **5**     | python-docx + pandoc   | ⭐⭐⭐⭐   |
| Convert PDF slides → study notes      | **4→2**   | PyMuPDF → Pandoc       | ⭐⭐⭐     |

---

## Route 1: Programmatic Document Generation (python-docx)

**Best for:** Professional reports, proposals, formatted tables, precise typography control.

**Why it looks best:** No "conversion" step — every paragraph, table, font, color is code-controlled. Like writing HTML/CSS vs using a WYSIWYG.

### Core Pattern

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

doc = Document()

# ── Page Setup ──
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ── Default Style ──
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# ── Title ──
title = doc.add_heading('Report Title', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ── Styled Subtitle ──
subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Subtitle text')
run.bold = True
run.font.size = Pt(13)
run.font.color.rgb = RGBColor(47, 84, 150)  # Professional blue

# ── Bold Label + Normal Description ──
p = doc.add_paragraph()
r = p.add_run('Key Point: ')
r.bold = True
r.font.size = Pt(11)
p.add_run('Description text here.').font.size = Pt(11)

doc.save('output.docx')
```

### Table with Styling (Dark Header + Alternating Rows)

```python
def set_cell_shading(cell, color_hex):
    """Set cell background color. 设置单元格背景颜色。"""
    shading = cell._element.get_or_add_tcPr()
    shading_elm = shading.makeelement(qn('w:shd'), {
        qn('w:val'): 'clear',
        qn('w:color'): 'auto',
        qn('w:fill'): color_hex,
    })
    shading.append(shading_elm)


def add_styled_table(doc, headers, rows, col_widths=None):
    """Add a table with dark blue header and alternating row colors.
    添加深蓝表头+隔行变色的美化表格。"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row: dark blue bg, white text
    # 表头行：深蓝背景，白色文字
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
                run.font.name = 'Calibri'
        set_cell_shading(cell, '2F5496')
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)

    # Data rows: alternating light blue
    # 数据行：隔行浅蓝
    for r_idx, row_data in enumerate(rows):
        for c_idx, cell_text in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = cell_text
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
                    run.font.name = 'Calibri'
        if r_idx % 2 == 1:
            for c_idx in range(len(headers)):
                set_cell_shading(table.rows[r_idx + 1].cells[c_idx], 'D6E4F0')

    if col_widths:
        for row in table.rows:
            for i, width in enumerate(col_widths):
                row.cells[i].width = Cm(width)

    doc.add_paragraph()  # spacing after table
    return table
```

### Design Constants

```python
# Professional color palette 专业配色方案
COLORS = {
    'header_bg': '2F5496',       # Dark blue table header
    'header_text': RGBColor(255, 255, 255),  # White
    'alt_row': 'D6E4F0',         # Light blue alternating rows
    'accent': RGBColor(47, 84, 150),  # Blue accent text
    'body': RGBColor(0, 0, 0),   # Black body text
}

# Typography 排版规范
FONTS = {
    'body': ('Calibri', Pt(11)),
    'heading': ('Calibri', Pt(14)),
    'title': ('Calibri', Pt(16)),
    'subtitle': ('Calibri', Pt(13)),
    'code': ('Courier New', Pt(10)),
    'table': ('Calibri', Pt(10)),
}

# Page margins 页边距
MARGINS = Cm(2.54)  # 1 inch standard
```

---

<!-- Detailed content moved to references/routes_reference.md -->

> 📖 See [references/routes_reference.md](references/routes_reference.md) for detailed content on the following topics:
> - ## Route 2: Markdown
> - ## Route 3: DOCX
> - ## Route 4: PDF Processing
> - ## Route 5: Assignment

## Installation

```bash
# Core dependencies 核心依赖
uv add python-docx    # Route 1: programmatic generation
uv add pypandoc       # Route 2: MD → DOCX
uv add mammoth        # Route 3: DOCX → MD
uv add pymupdf        # Route 4: PDF processing
uv add pdfplumber     # Route 4: table extraction
uv add pypdf          # Route 4: merge/split PDFs
uv add reportlab      # Route 4: create PDFs

# Optional 可选
uv add pytesseract pdf2image  # OCR
```

## Scripts Reference

| Script                    | Location                  | Purpose                      |
| ------------------------- | ------------------------- | ---------------------------- |
| `convert_md_to_docx.py`   | `scripts/`                | MD → DOCX with preprocessing |
| `convert_docx_mammoth.py` | `scripts/`                | DOCX → MD (mammoth)          |
| `batch_convert.py`        | `scripts/`                | Batch DOCX → MD              |
| `pdf_section_split.py`    | `scripts/`                | Split PDF by TOC             |
| `batch_pdf_to_md.py`      | `scripts/`                | Batch PDF → MD               |
| `pdf_converter.py`        | `scripts/`                | Advanced PDF conversion      |
| `pdf_to_md_hybrid.py`     | `scripts/`                | Hybrid PDF → MD              |
| `pdf_to_image_md.py`      | `scripts/`                | PDF → image-based MD         |
| `formula_mapper.py`       | `scripts/`                | Map PDF formulas             |
| `book_splitters/*.py`     | `scripts/book_splitters/` | Textbook-specific splitters  |

## Quality Checklist

- [ ] All images display correctly
- [ ] Headings are properly formatted
- [ ] Tables have styled headers (Route 1)
- [ ] Code blocks are readable
- [ ] Page layout is appropriate
- [ ] File size reasonable (<10MB)
- [ ] Chinese characters render correctly (UTF-8)

## References

- `references/advanced_techniques.md` — Password protection, watermarks, batch processing
- `references/cli_tools.md` — Command-line tools (qpdf, pdftotext, pdftoppm)
- `references/ml-lab-patterns.md` — ML course lab document patterns
