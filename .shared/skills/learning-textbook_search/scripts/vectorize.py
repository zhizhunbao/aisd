"""
向量化所有 self-study 教材（17 本）
使用 Ollama nomic-embed-text 本地模型

改进点（v2）:
用法:
    uv run python .shared/skills/learning-textbook_search/scripts/vectorize.py
    uv run python .shared/skills/learning-textbook_search/scripts/vectorize.py --book barber
    uv run python .shared/skills/learning-textbook_search/scripts/vectorize.py --force
    uv run python .shared/skills/learning-textbook_search/scripts/vectorize.py --list
"""
# 数据存储在 textbooks/_search_data/vectors/
import json
import re
import time
import argparse
import httpx
from pathlib import Path
from typing import Optional

from config import (
    DATA_DIR, OLLAMA_URL, EMBED_MODEL, EMBED_DIM,
    CHUNK_SIZE, CHUNK_OVERLAP, MIN_CHUNK_SIZE, BATCH_SIZE,
    SENTENCE_RE, BOOKS, get_mineru_content_list,
)

VECTORS_DIR = DATA_DIR / "vectors"


# ══════════════════════════════════════════════════════
# 文本处理
# ══════════════════════════════════════════════════════

def check_ollama() -> bool:
    """检查 Ollama 服务和 embedding 模型"""
    try:
        resp = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = [m["name"] for m in resp.json().get("models", [])]
        if not any(EMBED_MODEL in m for m in models):
            print(f"  !! 模型 {EMBED_MODEL} 未安装。运行: ollama pull {EMBED_MODEL}")
            return False
        return True
    except Exception:
        print("  !! Ollama 服务未运行。请先启动 Ollama Desktop。")
        return False


def read_from_mineru(book_key: str) -> list[dict]:
    """
    从 mineru content_list.json 读取书籍内容，按 heading 分组为自然章节块。
    - text_level 字段标志新章节标题，触发 flush
    - image caption / equation / table 文本并入当前块
    - 比 PDF 重新提取快得多，且保留章节结构信息
    """
    cl_path = get_mineru_content_list(book_key)
    if not cl_path.exists():
        print(f"  !! 找不到 content_list: {cl_path}")
        return []

    with open(cl_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    chunks: list[dict] = []
    current_heading = ""
    heading_page = 1
    buffer: list[str] = []

    def flush(heading: str, page: int) -> None:
        text = "\n\n".join(buffer).strip()
        if len(text) < MIN_CHUNK_SIZE:
            return
        prefix = make_prefix(book_key, heading, heading, "")
        for sub in smart_chunk(text):
            chunks.append({
                "book": book_key, "chapter": heading,
                "chapter_title": heading, "section": "",
                "page": page, "text": sub,
                "text_for_embed": prefix + sub,
            })

    for item in items:
        t = item.get("type", "")
        page = item.get("page_idx", 0) + 1
        if t == "text" and "text_level" in item:
            flush(current_heading, heading_page)
            buffer.clear()
            current_heading = item["text"].strip()
            heading_page = page
        elif t == "text":
            txt = item.get("text", "").strip()
            if txt:
                buffer.append(txt)
        elif t == "image":
            caps = item.get("image_caption", []) + item.get("image_footnote", [])
            cap = " ".join(str(c) for c in caps).strip()
            if cap:
                buffer.append(f"[Figure] {cap}")
        elif t == "equation":
            eq = item.get("text", "").strip()
            if eq:
                buffer.append(f"[Equation] {eq}")
        elif t == "table":
            tbl = item.get("text", "").strip()
            if tbl:
                buffer.append(f"[Table] {tbl}")

    flush(current_heading, heading_page)
    return chunks


# ══════════════════════════════════════════════════════
# 智能分块（段落 → 句子 → 硬切）
# ══════════════════════════════════════════════════════

def smart_chunk(text: str, chunk_size: int = CHUNK_SIZE,
                overlap: int = CHUNK_OVERLAP,
                min_size: int = MIN_CHUNK_SIZE) -> list[str]:
    """
    递归三级分块：段落 → 句子 → 硬切
    1. 按双换行分段落，贪心合并短段落
    2. 超长段落按句子边界拆
    3. 超长句子按词边界硬切
    4. 块间保持 overlap 重叠
    5. 末尾短块并入前一块
    """
    if not text or not text.strip():
        return []

    # 按段落分割
    paragraphs = re.split(r"\n\s*\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # 贪心合并短段落
    raw_chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current = f"{current}\n\n{para}" if current else para
        else:
            if current:
                raw_chunks.append(current)
            if len(para) > chunk_size:
                raw_chunks.extend(_split_by_sentences(para, chunk_size))
                current = ""
            else:
                current = para
    if current:
        raw_chunks.append(current)

    # 合并末尾短块
    if len(raw_chunks) > 1 and len(raw_chunks[-1]) < min_size:
        raw_chunks[-2] += "\n\n" + raw_chunks[-1]
        raw_chunks.pop()

    # 添加 overlap
    if overlap <= 0 or len(raw_chunks) <= 1:
        return raw_chunks

    overlapped = [raw_chunks[0]]
    for i in range(1, len(raw_chunks)):
        overlap_text = _get_overlap_text(raw_chunks[i - 1], overlap)
        overlapped.append(overlap_text + "\n" + raw_chunks[i])
    return overlapped


def _split_by_sentences(text: str, max_size: int) -> list[str]:
    """按句子边界拆分超长段落"""
    sentences = SENTENCE_RE.split(text)
    chunks, current = [], ""
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        if len(current) + len(sent) + 1 <= max_size:
            current = f"{current} {sent}" if current else sent
        else:
            if current:
                chunks.append(current)
            if len(sent) > max_size:
                chunks.extend(_hard_split(sent, max_size))
                current = ""
            else:
                current = sent
    if current:
        chunks.append(current)
    return chunks


def _hard_split(text: str, max_size: int) -> list[str]:
    """硬切兜底：尽量在词边界切"""
    chunks = []
    while len(text) > max_size:
        cut = text.rfind(" ", 0, max_size)
        if cut == -1:
            cut = max_size
        chunks.append(text[:cut].strip())
        text = text[cut:].strip()
    if text:
        chunks.append(text)
    return chunks


def _get_overlap_text(text: str, overlap_size: int) -> str:
    """从文本末尾取 overlap 字符，在句子/词边界断开"""
    if len(text) <= overlap_size:
        return text
    candidate = text[-overlap_size:]
    match = re.search(r"[.!?。！？]\s+", candidate)
    if match:
        return candidate[match.end():]
    space_pos = candidate.find(" ")
    if space_pos != -1 and space_pos < len(candidate) // 2:
        return candidate[space_pos + 1:]
    return candidate


# ══════════════════════════════════════════════════════
# 语义前缀 + Embedding
# ══════════════════════════════════════════════════════

def make_prefix(book: str, chapter: str, ch_title: str, section: str) -> str:
    """生成语义前缀 [book > chapter > section]"""
    parts = [book]
    if ch_title and ch_title != chapter:
        parts.append(ch_title)
    elif chapter:
        parts.append(chapter)
    if section:
        sec_clean = section.replace("sec_", "").replace("_", " ").strip()
        parts.append(sec_clean)
    return "[" + " > ".join(parts) + "] "


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """通过 Ollama 批量获取 embedding"""
    all_embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        resp = httpx.post(
            f"{OLLAMA_URL}/api/embed",
            json={"model": EMBED_MODEL, "input": batch},
            timeout=120,
        )
        resp.raise_for_status()
        all_embeddings.extend(resp.json()["embeddings"])
        done = min(i + BATCH_SIZE, len(texts))
        if done % 128 == 0 or done >= len(texts):
            print(f"    embedding: {done}/{len(texts)}")
    return all_embeddings


# ══════════════════════════════════════════════════════
# 处理流程
# ══════════════════════════════════════════════════════

def process_book(book_key: str) -> list[dict]:
    """处理一本书 → 所有 chunks（从 mineru content_list.json 读取）"""
    return read_from_mineru(book_key)


def vectorize_book(book_key: str, force: bool = False) -> Optional[Path]:
    """向量化一本书 → JSON 文件"""
    if book_key not in BOOKS:
        print(f"  !! 未知: {book_key}")
        return None

    subject = BOOKS[book_key][0]
    output_path = VECTORS_DIR / f"{book_key}_vectors.json"

    if output_path.exists() and not force:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  >> 跳过 {book_key} ({size_mb:.1f}MB)。用 --force 重新生成")
        return output_path

    print(f"\n{'='*60}")
    print(f"  [{book_key}] ({subject})")
    print(f"{'='*60}")
    t0 = time.time()

    chunks = process_book(book_key)
    if not chunks:
        print(f"  !! 无文本块")
        return None
    print(f"  chunks: {len(chunks)}")

    print(f"  embedding: {EMBED_MODEL}...")
    embed_texts = [c["text_for_embed"] for c in chunks]
    embeddings = get_embeddings(embed_texts)

    data = {
        "metadata": {
            "book": book_key, "subject": subject,
            "model": EMBED_MODEL, "dim": EMBED_DIM,
            "chunk_size": CHUNK_SIZE, "chunk_overlap": CHUNK_OVERLAP,
            "total_chunks": len(chunks), "version": 2,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "chunks": [
            {
                "id": i, "book": c["book"], "chapter": c["chapter"],
                "chapter_title": c["chapter_title"], "section": c["section"],
                "page": c["page"], "text": c["text"], "embedding": emb,
            }
            for i, (c, emb) in enumerate(zip(chunks, embeddings))
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    elapsed = time.time() - t0
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  done: {len(chunks)} chunks, {size_mb:.1f}MB, {elapsed:.0f}s")
    return output_path


# ══════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="向量化教材 (v2)")
    parser.add_argument("--book", type=str, help="只处理指定书籍")
    parser.add_argument("--subject", type=str, help="只处理指定学科")
    parser.add_argument("--force", action="store_true", help="强制重新向量化")
    parser.add_argument("--list", action="store_true", help="列出所有书籍")
    args = parser.parse_args()

    if args.list:
        print("\n  书籍列表:")
        for key, (subj, mdir) in sorted(BOOKS.items()):
            vec_path = VECTORS_DIR / f"{key}_vectors.json"
            cl_path = get_mineru_content_list(key)
            vec_status = "vec" if vec_path.exists() else "   "
            src_status = "src" if cl_path.exists() else "   "
            print(f"  [{vec_status}|{src_status}] {key:15s}  {subj:6s}  {mdir}")
        return

    if not check_ollama():
        import sys; sys.exit(1)

    books = [args.book] if args.book else \
            [k for k, (s, _) in BOOKS.items() if s == args.subject] if args.subject else \
            list(BOOKS.keys())

    print(f"\n  plan: {len(books)} books, model={EMBED_MODEL}")
    print(f"  params: chunk={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}")
    print(f"  output: {VECTORS_DIR}/")

    ok, fail = [], []
    t0 = time.time()
    for bk in books:
        try:
            out = vectorize_book(bk, force=args.force)
            (ok if out else fail).append(bk)
        except Exception as e:
            print(f"  !! {bk}: {e}")
            fail.append(bk)

    print(f"\n{'='*60}")
    print(f"  ok: {len(ok)}, fail: {len(fail)}, time: {time.time()-t0:.0f}s")
    if fail:
        print(f"  failed: {', '.join(fail)}")


if __name__ == "__main__":
    main()
