---
name: textbook-vectorization
description: Vectorize PDF textbooks for semantic search. Use when (1) need to quickly find concepts in textbooks, (2) building personal knowledge base, (3) preparing study materials with searchable content, (4) want to query textbook semantically.
---

# Textbook Vectorization

## Objectives

- Extract text from PDF textbooks
- Generate vector embeddings for semantic search
- Enable fast concept lookup across large textbooks
- Support both local (free) and cloud-based embedding models

## Key Instructions

### 1. Choose Embedding Model

**Local Model (Free)**:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')  # ~80MB, runs locally
```

**Cloud Model (Paid)**:
```python
from openai import OpenAI
client = OpenAI()
# Use text-embedding-3-small (~$0.0001/1K tokens)
```

### 2. Extract and Chunk Text

```python
import pypdf
from pathlib import Path

def extract_text_from_pdf(pdf_path: Path) -> list:
    pages = []
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                pages.append({'page': page_num, 'text': text.strip()})
    return pages

def chunk_text(pages: list, chunk_size: int = 500, overlap: int = 50) -> list:
    chunks = []
    for page_data in pages:
        text = page_data['text']
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append({
                    'page': page_data['page'],
                    'text': chunk
                })
            start = end - overlap
    return chunks
```

### 3. Generate Embeddings

**Batch processing for efficiency**:
```python
def get_embeddings(texts: list, model) -> list:
    batch_size = 32
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings = model.encode(batch, show_progress_bar=False)
        all_embeddings.extend(embeddings.tolist())
    
    return all_embeddings
```

### 4. Save Vector Database

**Single JSON file format**:
```python
import json

data = {
    'metadata': {
        'total_chunks': len(chunks),
        'embedding_model': 'all-MiniLM-L6-v2',
        'embedding_dim': len(embeddings[0]),
        'chunk_size': 500,
        'chunk_overlap': 50
    },
    'chunks': [
        {
            'id': i,
            'page': chunk['page'],
            'text': chunk['text'],
            'embedding': embedding
        }
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]
}

with open('textbook_vectors.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 5. Query the Vectorized Textbook

```python
import numpy as np

def cosine_similarity(vec1: list, vec2: list) -> float:
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search(query: str, data: dict, model, top_k: int = 5):
    # Get query embedding
    query_embedding = model.encode([query])[0].tolist()
    
    # Calculate similarities
    results = []
    for chunk in data['chunks']:
        similarity = cosine_similarity(query_embedding, chunk['embedding'])
        results.append((chunk, similarity))
    
    # Sort and return top results
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]
```

## Workflow

### Initial Setup

1. Install dependencies:
   ```bash
   uv add pypdf sentence-transformers numpy
   ```

2. Prepare PDF textbook in accessible location

3. Run vectorization script (one-time, ~5-10 minutes for 500-page book)

### Query Usage

**Interactive mode**:
```python
while True:
    query = input("🔍 Query > ").strip()
    if query.lower() in ['quit', 'exit']:
        break
    
    results = search(query, data, model, top_k=3)
    for i, (chunk, score) in enumerate(results, 1):
        print(f"\n[Result {i}] Similarity: {score:.4f} | Page: {chunk['page']}")
        print(chunk['text'][:300] + "...")
```

**Single query**:
```bash
uv run python query_textbook.py "What is temporal difference learning?"
```

## Configuration

### Chunk Size Tuning

- **Small chunks (200-300 chars)**: More precise, more chunks, larger file
- **Medium chunks (500-700 chars)**: Balanced (recommended)
- **Large chunks (1000+ chars)**: Broader context, fewer chunks

### Overlap Strategy

- **No overlap (0)**: Faster, may miss boundary concepts
- **Small overlap (50-100)**: Recommended for most cases
- **Large overlap (200+)**: Better coverage, more redundancy

## Cost Estimation

### Local Model (Free)
- Model download: ~80MB (one-time)
- Processing time: ~5-10 min for 500 pages
- Storage: ~50-100MB JSON file

### Cloud Model (OpenAI)
- text-embedding-3-small: ~$0.0001/1K tokens
- 500-page textbook: ~$0.50-$2.00
- Faster processing, no local compute needed

## Validation

Before using the vectorized textbook:

- [ ] Verify JSON file size is reasonable (50-200MB for typical textbook)
- [ ] Test query with known concept from textbook
- [ ] Check that page numbers are preserved correctly
- [ ] Ensure embeddings dimension matches model output

## Common Issues

### Issue: PDF extraction returns gibberish

**Solution**: PDF may be scanned images. Use OCR first:
```bash
uv add pytesseract pdf2image
# Convert to images, then OCR
```

### Issue: Out of memory during embedding

**Solution**: Reduce batch size:
```python
batch_size = 16  # or even 8
```

### Issue: Query returns irrelevant results

**Solution**: 
- Try different query phrasing
- Reduce chunk size for more precision
- Increase top_k to see more results

## Best Practices

1. **Version control**: Save vectorization parameters in metadata
2. **Incremental updates**: Re-vectorize only changed chapters
3. **Multiple textbooks**: Use separate JSON files or add book_id field
4. **Query refinement**: Start broad, then narrow down with specific terms
5. **Backup**: Keep original PDF and vectors separately

## Reference Scripts

**通用脚本（推荐）:**
- `courses/self-study/vectorize_all.py` - 批量向量化所有 17 本教材（Ollama nomic-embed-text）
- `courses/self-study/query_books.py` - 跨教材语义搜索（CLI + 交互模式）

**旧版单本脚本:**
- `.shared/skills/learning-textbook_vectorization/scripts/vectorize_textbook.py`
- `.shared/skills/learning-textbook_vectorization/scripts/query_textbook.py`

## Integration with generate-study-material Workflow

本 skill 在工作流中的使用方式：

### Phase 1（笔记）中使用

遇到概念/公式时，除了查 `math-concept-library` 和 `concept-glossary`，还要搜教材：

```bash
# 搜索多本教材对同一概念的解释
uv run python courses/self-study/query_books.py "concept name" --top-k 5
```

用搜索结果中的多本书解释来丰富笔记内容，提供多角度理解。

### Phase 2（代码）中使用

遇到算法实现细节不确定时，搜教材找伪代码或推导：

```bash
uv run python courses/self-study/query_books.py "algorithm pseudocode" --top-k 3
```

### Python 代码中调用

```python
# 在笔记生成脚本中直接导入
import sys
sys.path.insert(0, "courses/self-study")
from query_books import load_vectors, search, get_query_embedding

chunks = load_vectors()  # 加载所有教材
results = search("SVM kernel trick", chunks, top_k=5)
for chunk, score in results:
    print(f"{score:.3f} | {chunk['book']} {chunk['chapter']} p.{chunk['page']}")
    print(chunk['text'][:200])
```

### 向量文件位置

```
courses/self-study/
├── ml/      → barber, bishop, esl, goodfellow, kelleher, murphy_pml1, murphy_pml2, shalev
├── math/    → mml, boyd, mackay, grinstead, downey
├── nlp/     → jurafsky
├── cv/      → szeliski
├── rl/      → sutton
└── graphs/  → hamilton
```
