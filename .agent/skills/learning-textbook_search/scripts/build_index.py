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
    SELF_STUDY_ROOT, DATA_DIR, BOOKS, get_sections_dir,
)

VECTORS_DIR = DATA_DIR / "vectors"
BM25_DIR = DATA_DIR / "bm25"
TOC_INDEX_PATH = DATA_DIR / "toc_index.json"


# ══════════════════════════════════════════════════════
# BM25 索引
# ══════════════════════════════════════════════════════

def tokenize(text: str) -> list[str]:
    """简单分词：小写 + 按非字母数字分割"""
    return re.findall(r"[a-z0-9]+", text.lower())


def build_bm25_for_book(book_key: str) -> bool:
    """从向量 JSON 中提取文本，构建 BM25 索引"""
    vec_path = VECTORS_DIR / f"{book_key}_vectors.json"
    if not vec_path.exists():
        print(f"  >> 跳过 {book_key} (无向量文件，先运行 vectorize.py)")
        return False

    with open(vec_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data["chunks"]
    if not chunks:
        return False

    # 为 BM25 准备: 保存 tokenized docs + metadata（不含 embedding）
    docs = []
    tokenized = []
    for c in chunks:
        tokens = tokenize(c["text"])
        tokenized.append(tokens)
        docs.append({
            "id": c["id"], "book": c["book"],
            "chapter": c["chapter"], "chapter_title": c["chapter_title"],
            "section": c["section"], "page": c["page"],
            "text": c["text"],
        })

    # 用 rank_bm25 构建索引
    from rank_bm25 import BM25Okapi
    bm25 = BM25Okapi(tokenized)

    # 保存
    BM25_DIR.mkdir(parents=True, exist_ok=True)
    out_path = BM25_DIR / f"{book_key}_bm25.pkl"
    with open(out_path, "wb") as f:
        pickle.dump({"bm25": bm25, "docs": docs, "tokenized": tokenized}, f)

    size_kb = out_path.stat().st_size / 1024
    print(f"  [{book_key}] {len(docs)} docs, {size_kb:.0f}KB")
    return True


# ══════════════════════════════════════════════════════
# TOC 目录索引
# ══════════════════════════════════════════════════════

def build_toc_index() -> dict:
    """汇总所有教材的 toc.json → 统一目录索引"""
    toc_all = {}

    for book_key, (subject, _, sections_dir_name) in BOOKS.items():
        sections_dir = get_sections_dir(book_key)
        toc_path = sections_dir / "toc.json"
        if not toc_path.exists():
            continue

        with open(toc_path, "r", encoding="utf-8") as f:
            toc = json.load(f)

        book_toc = {
            "subject": subject,
            "chapters": {},
        }

        for ch_key, ch_data in toc.items():
            if not isinstance(ch_data, dict):
                continue
            ch_entry = {
                "title": ch_data.get("title", ch_key),
                "start_page": ch_data.get("start_page"),
                "end_page": ch_data.get("end_page"),
                "sections": [],
            }
            for sec in ch_data.get("sections", []):
                ch_entry["sections"].append({
                    "id": sec.get("id", ""),
                    "title": sec.get("title", ""),
                    "start_page": sec.get("start_page"),
                    "end_page": sec.get("end_page"),
                })
            book_toc["chapters"][ch_key] = ch_entry

        if book_toc["chapters"]:
            toc_all[book_key] = book_toc

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
        books = [k for k, (s, _, _) in BOOKS.items() if s == args.subject]
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
    total_chapters = sum(len(b["chapters"]) for b in toc.values())
    print(f"  TOC: {len(toc)} books, {total_chapters} chapters")
    print(f"  saved: {TOC_INDEX_PATH.relative_to(DATA_DIR.parent.parent.parent.parent)}")

    print(f"\n  done: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
