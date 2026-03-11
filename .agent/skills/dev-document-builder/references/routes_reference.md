# Document Builder — Route Details

## Route 2: Markdown → DOCX Conversion (Pandoc)

**Best for:** Quick conversion of existing markdown notes to Word for submission.

### Script Usage

```bash
# Use the conversion script (recommended)
# 使用转换脚本（推荐）
python scripts/convert_md_to_docx.py Lab_Answer.md

# Specify output filename 指定输出文件名
python scripts/convert_md_to_docx.py Lab_Answer.md Lab1.docx

# Direct pandoc command 直接 pandoc 命令
pandoc input.md -o output.docx --resource-path="./images"

# With custom template 使用自定义模板
pandoc input.md -o output.docx --reference-doc=template.docx --toc --number-sections

# With metadata 带元数据
pandoc input.md -o output.docx \
  -M title="Lab 1: Title" \
  -M author="Student Name" \
  -M date="2026-01-20"
```

### What the Script Does Automatically

1. **Removes image alt text** — prevents `![Step 1 Code](path.png)` from becoming a caption in Word
2. **Removes horizontal rules** — `---` become ugly visible lines in Word
3. **Resolves relative image paths** — ensures images are found
4. **Inserts cover page + TOC** — post-processes with python-docx
5. **Adds page breaks** — after cover page and TOC

### Pre-processing Rules (if using pandoc directly)

```python
import re

def preprocess_markdown(md_content):
    """Clean markdown for better Word output. 清理 markdown 以获得更好的 Word 输出。"""
    # Separate YAML frontmatter 分离 YAML 前置信息
    frontmatter = ''
    body = md_content

    if md_content.startswith('---'):
        end_match = re.search(r'\n---\s*\n', md_content[3:])
        if end_match:
            split_pos = 3 + end_match.end()
            frontmatter = md_content[:split_pos]
            body = md_content[split_pos:]

    # Remove horizontal rules from body 从正文中移除水平线
    body = re.sub(r'^---\s*$\n?', '', body, flags=re.MULTILINE)

    # Remove image alt text 移除图片替代文本
    body = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', lambda m: f'![]({m.group(2)})', body)

    return frontmatter + body
```

### Common Issues

| Problem                    | Cause               | Fix                                         |
| -------------------------- | ------------------- | ------------------------------------------- |
| Unwanted text below images | Alt text as caption | Use `![](path)` not `![text](path)`         |
| Visible horizontal lines   | `---` in markdown   | Remove `---` separators                     |
| Chinese characters garbled | Encoding            | `pandoc -f markdown+east_asian_line_breaks` |
| Missing images             | Path resolution     | Use `--resource-path`                       |
| Large file size            | Uncompressed images | Compress before conversion                  |

---


## Route 3: DOCX → Markdown Conversion (Mammoth)

**Best for:** Extracting editable content from instructor-provided Word templates.

### Quick Usage

```bash
# Install 安装
uv add mammoth

# Convert using script 使用脚本转换
python scripts/convert_docx_mammoth.py input.docx output.md

# Batch convert 批量转换
python scripts/batch_convert.py input_dir/ output_dir/
```

### Python API

```python
import mammoth
from pathlib import Path

def docx_to_md(docx_path, md_path=None):
    """Convert DOCX to Markdown. CRITICAL: Only format, never modify content.
    将 DOCX 转换为 Markdown。关键：只转换格式，绝不修改内容。"""
    docx_path = Path(docx_path)
    if md_path is None:
        md_path = docx_path.with_suffix('.md')

    with open(docx_path, 'rb') as f:
        result = mammoth.convert_to_markdown(f)
        Path(md_path).write_text(result.value, encoding='utf-8')

    for msg in result.messages:
        print(f"Warning: {msg}")
    return md_path
```

### With Pandoc (for image extraction)

```python
import subprocess
from pathlib import Path

def docx_to_md_with_images(docx_path, output_dir):
    """Convert DOCX with image extraction. 转换 DOCX 并提取图片。"""
    md_path = output_dir / f"{Path(docx_path).stem}.md"
    images_dir = output_dir / 'images'

    subprocess.run([
        'pandoc', str(docx_path),
        '-o', str(md_path),
        '--extract-media', str(images_dir)
    ])

    # Fix image paths 修复图片路径
    content = md_path.read_text(encoding='utf-8')
    content = content.replace('](media/', '](images/')
    md_path.write_text(content, encoding='utf-8')
    return md_path
```

---


## Route 4: PDF Processing (PyMuPDF + Friends)

**Best for:** Extracting content from PDFs, splitting textbooks, creating study materials.

### Library Selection Guide

| Task             | Best Library                   | Why                                           |
| ---------------- | ------------------------------ | --------------------------------------------- |
| Extract text     | `pymupdf` (fitz)               | Fast, accurate, hybrid mode                   |
| Extract tables   | `pdfplumber`                   | Excellent table detection                     |
| Merge/split PDFs | `pypdf`                        | Fast and lightweight                          |
| **Split by TOC** | `scripts/pdf_section_split.py` | Auto-read bookmarks, fallback to page headers |
| **Batch to MD**  | `scripts/batch_pdf_to_md.py`   | Convert PDFs to .md with filters              |
| Create PDFs      | `reportlab`                    | Professional output                           |
| Fill forms       | `pypdf` or `pdf-lib` (JS)      | Form field support                            |
| Extract images   | `pymupdf` (fitz)               | Built-in, preserves quality                   |
| OCR scanned PDFs | `pytesseract` + `pdf2image`    | Industry standard                             |
| Convert to MD    | `pymupdf` (fitz)               | Best for slides and academic                  |

### Quick Text Extraction

```python
import pymupdf  # or: import fitz

doc = pymupdf.open("document.pdf")
text = ""
for page in doc:
    text += page.get_text()
doc.close()
```

### Extract Tables

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)
```

### PDF → Markdown (Academic Materials)

```python
import pymupdf
from pathlib import Path

def pdf_to_markdown(pdf_path, output_path=None):
    """Convert PDF to markdown. PDF 转 Markdown。"""
    pdf_path = Path(pdf_path)
    if output_path is None:
        output_path = pdf_path.with_suffix('.md')

    doc = pymupdf.open(pdf_path)
    md = []
    for page_num, page in enumerate(doc, 1):
        md.append(f"## Page {page_num}\n")
        md.append(page.get_text("text"))
        md.append("\n---\n")
    doc.close()

    Path(output_path).write_text("\n".join(md), encoding='utf-8')
    print(f"✓ {pdf_path.name} → {output_path}")
```

### PDF Slides → Markdown (with images)

```python
def pdf_slides_to_markdown(pdf_path, output_path=None):
    """Convert PDF slides to markdown, extracting images.
    将 PDF 幻灯片转换为 Markdown，同时提取图片。"""
    pdf_path = Path(pdf_path)
    if output_path is None:
        output_path = pdf_path.with_suffix('.md')

    img_dir = output_path.parent / f"{output_path.stem}_images"
    img_dir.mkdir(exist_ok=True)

    doc = pymupdf.open(pdf_path)
    md = []
    for page_num, page in enumerate(doc, 1):
        md.append(f"## Slide {page_num}\n")
        text = page.get_text()
        if text.strip():
            md.append(text)
        for img_idx, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_path = img_dir / f"slide{page_num}_img{img_idx}.{base_image['ext']}"
            img_path.write_bytes(base_image["image"])
            md.append(f"\n![Image]({img_path.relative_to(output_path.parent)})\n")
        md.append("\n---\n")
    doc.close()

    Path(output_path).write_text("\n".join(md), encoding='utf-8')
```

### Split PDF by TOC (Textbooks)

```bash
# Preview structure 预览结构
python scripts/pdf_section_split.py textbook.pdf --stats

# Split all chapters 拆分所有章节
python scripts/pdf_section_split.py textbook.pdf

# Split one chapter 拆分单个章节
python scripts/pdf_section_split.py textbook.pdf --chapter 2
```

For PDFs without bookmarks, the script automatically scans running page headers.

### Merge / Split PDFs

```python
from pypdf import PdfWriter, PdfReader

# Merge 合并
writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
with open("merged.pdf", "wb") as f:
    writer.write(f)

# Split by page 按页拆分
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        writer.write(f)
```

### Create New PDFs

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=letter)
width, height = letter
c.drawString(100, height - 100, "Hello World!")
c.save()
```

### OCR for Scanned PDFs

```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
text = ""
for image in images:
    text += pytesseract.image_to_string(image)
```

### Book Splitters (Custom Scripts)

For academic textbooks with non-standard TOC:

| Script                | Book               | Strategy                                    |
| --------------------- | ------------------ | ------------------------------------------- |
| `split_bishop.py`     | Bishop PRML        | L1 numbered chapters, skip non-numbered     |
| `split_murphy.py`     | Murphy PML1/PML2   | Parts + Chapters, find same-level end pages |
| `split_esl.py`        | ESL                | No TOC, scan running headers at y=90        |
| `split_barber.py`     | Barber BRML        | No TOC, scan running headers at y=16        |
| `split_goodfellow.py` | Goodfellow DL      | Standard TOC structure                      |
| `split_kelleher.py`   | Kelleher ML        | Appendices as separate chapters             |
| `split_shalev.py`     | Shalev-Shwartz UML | Extract sections from TOC pages             |

---


## Route 5: Assignment Document Generation

**Best for:** Creating lab/assignment submission documents with screenshots, discussions, and proper formatting.

### Workflow

1. Load student info from `.env.local` (NAME, NUMBER)
2. Generate Python script (if not exists)
3. Run script to produce outputs/plots
4. Generate code + output screenshots
5. Create markdown template with image paths
6. Write descriptions for each step
7. Convert to .docx using Route 2

### Document Structure

```
Assignment Title
Student Information (from .env.local)
├── Name: {NAME}
├── Student Number: {NUMBER}
├── Section/Class
└── Date: {Current date}

Step-by-Step Content
├── Step X: Title
│   ├── Screenshots (with captions)
│   ├── Code snippets
│   ├── Output/Results
│   └── Discussion/Analysis
└── Repeat for each step

Conclusion/Summary
References
```

### Discussion Format

```
Step N: Title

The results show that... (observation)
As seen in Figure X, ... (evidence)
This occurs because... (explanation)
Therefore, we can conclude... (conclusion)
```

### Anti-Patterns ❌

- Creating template before generating screenshots
- Image paths don't match generated filenames
- Missing explanations (no marks given!)
- Blurry screenshots
- Copy-pasting entire code files

---

