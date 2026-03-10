"""
构建 BM25 关键词索引 + TOC 目录索引

从已有的向量 JSON 文件中提取文本，构建：
1. BM25 倒排索引（关键词搜索）— 存为 pickle
2. TOC 目录索引（章节导航）— 从 toc.json 汇总

不需要 Ollama，不需要 embedding，秒级完成。

用法:
    uv run python .shared/skills/learning-textbook_search/scripts/build_index.py
    uv run python .shared/skills/learning-textbook_search/scripts/build_index.py --book barber
"""

import json
import pickle
import re
import time
import argparse
from pathlib import Path

from config import (
    DATA_DIR, BOOKS, get_mineru_content_list,
)

VECTORS_DIR = DATA_DIR / "vectors"
BM25_DIR = DATA_DIR / "bm25"
TOC_INDEX_PATH = DATA_DIR / "toc_index.json"


# ══════════════════════════════════════════════════════
# BM25 索引
# ══════════════════════════════════════════════════════

def tokenize(text: str) -> list[str]:
    """简单分词：小写 + 按非字母数字分割，统一 Unicode 连字符为 ASCII"""
    # 将各种 Unicode 连字符/破折号统一为 ASCII hyphen
    text = text.replace("\u2010", "-").replace("\u2011", "-").replace(
        "\u2012", "-").replace("\u2013", "-").replace("\u2014", "-").replace(
        "\u2015", "-").replace("\uff0d", "-").replace("\u02d7", "-")
    # 替换 PDF 常见乱码（如 o↵ = off, ↵ 是换行符 U+21B5）
    text = text.replace("\u21b5", "").replace("\ufb01", "fi").replace(
        "\ufb02", "fl").replace("\ufb00", "ff").replace("\ufb03", "ffi")
    return re.findall(r"[a-z0-9]+", text.lower())


def build_bm25_from_mineru(book_key: str) -> bool:
    """
    直接从 mineru content_list.json 构建 BM25 索引。
    无需 Ollama，无需向量文件，秒级完成。
    按 heading 分组，每个 heading 节作为一个 BM25 文档。
    """
    cl_path = get_mineru_content_list(book_key)
    if not cl_path.exists():
        print(f"  !! 找不到 content_list: {cl_path}")
        return False

    with open(cl_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    docs: list[dict] = []
    tokenized: list[list[str]] = []
    current_heading = ""
    heading_page = 1
    buffer: list[str] = []

    def flush(heading: str, page: int) -> None:
        text = " ".join(buffer).strip()
        if not text or len(text) < 50:
            return
        tok = tokenize(text)
        if tok:
            tokenized.append(tok)
            docs.append({
                "id": len(docs), "book": book_key,
                "chapter": heading, "chapter_title": heading,
                "section": "", "page": page,
                "text": text[:3000],  # BM25 不需要保存全文
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
                buffer.append(cap)
        elif t == "equation":
            eq = item.get("text", "").strip()
            if eq:
                buffer.append(eq)

    flush(current_heading, heading_page)

    if not docs:
        print(f"  !! {book_key}: 无文本内容")
        return False

    from rank_bm25 import BM25Okapi
    bm25 = BM25Okapi(tokenized)
    BM25_DIR.mkdir(parents=True, exist_ok=True)
    out_path = BM25_DIR / f"{book_key}_bm25.pkl"
    with open(out_path, "wb") as f:
        pickle.dump({"bm25": bm25, "docs": docs, "tokenized": tokenized}, f)
    size_kb = out_path.stat().st_size / 1024
    print(f"  [{book_key}] {len(docs)} sections, {size_kb:.0f}KB")
    return True


def build_bm25_for_book(book_key: str) -> bool:
    """构建 BM25：优先用 mineru content_list，若已有向量文件则从向量文件同步"""
    vec_path = VECTORS_DIR / f"{book_key}_vectors.json"
    if vec_path.exists():
        # 向量文件已有 → 从向量 JSON 同步（保持 chunk 粒度一致）
        with open(vec_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        chunks = data["chunks"]
        if not chunks:
            return False
        docs, tokenized = [], []
        for c in chunks:
            tok = tokenize(c["text"])
            tokenized.append(tok)
            docs.append({
                "id": c["id"], "book": c["book"],
                "chapter": c["chapter"], "chapter_title": c["chapter_title"],
                "section": c["section"], "page": c["page"],
                "text": c["text"],
            })
        from rank_bm25 import BM25Okapi
        bm25 = BM25Okapi(tokenized)
        BM25_DIR.mkdir(parents=True, exist_ok=True)
        out_path = BM25_DIR / f"{book_key}_bm25.pkl"
        with open(out_path, "wb") as f:
            pickle.dump({"bm25": bm25, "docs": docs, "tokenized": tokenized}, f)
        size_kb = out_path.stat().st_size / 1024
        print(f"  [{book_key}] {len(docs)} chunks (from vectors), {size_kb:.0f}KB")
        return True
    else:
        # 无向量文件 → 直接从 mineru 构建（无需 Ollama）
        return build_bm25_from_mineru(book_key)


# ══════════════════════════════════════════════════════
# TOC 目录索引
# ══════════════════════════════════════════════════════

def build_toc_index() -> dict:
    """从 mineru content_list.json 的 text_level 标题提取目录结构"""
    toc_all = {}

    for book_key, (subject, _) in BOOKS.items():
        cl_path = get_mineru_content_list(book_key)
        if not cl_path.exists():
            continue

        with open(cl_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        headings = [
            {"title": d["text"].strip(), "page": d.get("page_idx", 0) + 1}
            for d in items
            if d.get("type") == "text" and "text_level" in d and d.get("text", "").strip()
        ]

        if headings:
            toc_all[book_key] = {"subject": subject, "headings": headings}

    return toc_all


# ══════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="构建 BM25 + TOC 索引")
    parser.add_argument("--book", type=str, help="只处理指定书籍")
    parser.add_argument("--subject", type=str, help="只处理指定学科")
    args = parser.parse_args()

    t0 = time.time()

    # 1. BM25 索引
    print("\n  === BM25 索引 ===")
    if args.book:
        books = [args.book]
    elif args.subject:
        books = [k for k, (s, _) in BOOKS.items() if s == args.subject]
    else:
        books = list(BOOKS.keys())

    ok = 0
    for bk in books:
        if build_bm25_for_book(bk):
            ok += 1
    print(f"  BM25: {ok}/{len(books)} books")

    # 2. TOC 索引
    print("\n  === TOC 索引 ===")
    toc = build_toc_index()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(TOC_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(toc, f, ensure_ascii=False, indent=2)
    total_headings = sum(len(b["headings"]) for b in toc.values())
    print(f"  TOC: {len(toc)} books, {total_headings} headings")
    print(f"  saved: {TOC_INDEX_PATH.relative_to(DATA_DIR.parent.parent.parent.parent)}")

    print(f"\n  done: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
