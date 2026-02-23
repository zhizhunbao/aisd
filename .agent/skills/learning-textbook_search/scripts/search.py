"""
三路混合搜索引擎 (Vector + BM25 + TOC)

支持模式：
  vector  - 语义向量搜索 (Ollama nomic-embed-text)
  bm25    - 关键词搜索 (BM25Okapi)
  toc     - 目录导航 (模糊匹配章节标题)
  hybrid  - 三路融合 (RRF 排序)

用法:
    uv run python .shared/skills/learning-textbook_search/scripts/search.py "SVM kernel trick"
    uv run python .shared/skills/learning-textbook_search/scripts/search.py --mode bm25 "gradient descent"
    uv run python .shared/skills/learning-textbook_search/scripts/search.py --mode toc "reinforcement"
    uv run python .shared/skills/learning-textbook_search/scripts/search.py --interactive
"""

import argparse
import json
import pickle
import sys
import time
from pathlib import Path

import numpy as np

from config import (
    DATA_DIR, BOOKS, OLLAMA_BASE, EMBED_MODEL, RRF_K,
)

VECTORS_DIR = DATA_DIR / "vectors"
BM25_DIR = DATA_DIR / "bm25"
TOC_INDEX_PATH = DATA_DIR / "toc_index.json"


# ══════════════════════════════════════════════════════
# Vector Search
# ══════════════════════════════════════════════════════

def load_vectors(book_filter: str | None = None) -> tuple[list[dict], np.ndarray]:
    """加载所有（或指定）向量"""
    all_chunks = []
    all_vecs = []

    for bk in BOOKS:
        if book_filter and bk != book_filter:
            continue
        vpath = VECTORS_DIR / f"{bk}_vectors.json"
        if not vpath.exists():
            continue
        with open(vpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for c in data["chunks"]:
            all_chunks.append({
                "id": c["id"], "book": c["book"],
                "chapter": c["chapter"], "chapter_title": c["chapter_title"],
                "section": c["section"], "page": c["page"],
                "text": c["text"],
            })
            all_vecs.append(c["embedding"])

    return all_chunks, np.array(all_vecs, dtype=np.float32) if all_vecs else np.array([])


def get_query_embedding(query: str) -> np.ndarray:
    """通过 Ollama 获取查询向量"""
    import httpx
    resp = httpx.post(
        f"{OLLAMA_BASE}/api/embed",
        json={"model": EMBED_MODEL, "input": [query]},
        timeout=30,
    )
    resp.raise_for_status()
    return np.array(resp.json()["embeddings"][0], dtype=np.float32)


def cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """批量 cosine similarity"""
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return b_norm @ a_norm


def search_vector(query: str, chunks: list, vecs: np.ndarray, top_k: int = 10) -> list[dict]:
    """语义向量搜索"""
    if len(chunks) == 0:
        return []
    q_emb = get_query_embedding(query)
    sims = cosine_sim(q_emb, vecs)
    top_idx = np.argsort(sims)[-top_k:][::-1]
    results = []
    for i in top_idx:
        r = dict(chunks[i])
        r["score"] = float(sims[i])
        r["method"] = "vector"
        results.append(r)
    return results


# ══════════════════════════════════════════════════════
# BM25 Search
# ══════════════════════════════════════════════════════

def load_bm25(book_filter: str | None = None):
    """加载所有 BM25 索引"""
    import re
    all_bm25 = []
    for bk in BOOKS:
        if book_filter and bk != book_filter:
            continue
        bpath = BM25_DIR / f"{bk}_bm25.pkl"
        if not bpath.exists():
            continue
        with open(bpath, "rb") as f:
            data = pickle.load(f)
        all_bm25.append(data)
    return all_bm25


def search_bm25(query: str, bm25_data: list, top_k: int = 10) -> list[dict]:
    """BM25 关键词搜索"""
    import re
    tokens = re.findall(r"[a-z0-9]+", query.lower())
    if not tokens:
        return []

    scored = []
    for data in bm25_data:
        bm25 = data["bm25"]
        docs = data["docs"]
        scores = bm25.get_scores(tokens)
        for i, s in enumerate(scores):
            if s > 0:
                r = dict(docs[i])
                r["score"] = float(s)
                r["method"] = "bm25"
                scored.append(r)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


# ══════════════════════════════════════════════════════
# TOC Search
# ══════════════════════════════════════════════════════

def load_toc() -> dict:
    """加载 TOC 索引"""
    if not TOC_INDEX_PATH.exists():
        return {}
    with open(TOC_INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search_toc(query: str, toc: dict, top_k: int = 10) -> list[dict]:
    """模糊匹配章节标题"""
    query_lower = query.lower()
    query_words = set(query_lower.split())
    results = []

    for book_key, book_data in toc.items():
        for ch_key, ch_data in book_data.get("chapters", {}).items():
            title = ch_data.get("title", "")
            title_lower = title.lower()

            # 打分：关键词匹配 + 子串匹配
            score = 0.0
            title_words = set(title_lower.split())
            word_overlap = len(query_words & title_words)
            if word_overlap > 0:
                score += word_overlap / max(len(query_words), 1)
            if query_lower in title_lower:
                score += 2.0

            # 检查子节标题
            matching_sections = []
            for sec in ch_data.get("sections", []):
                sec_title = sec.get("title", "").lower()
                sec_score = 0.0
                sec_words = set(sec_title.split())
                sw_overlap = len(query_words & sec_words)
                if sw_overlap > 0:
                    sec_score += sw_overlap / max(len(query_words), 1)
                if query_lower in sec_title:
                    sec_score += 2.0
                if sec_score > 0:
                    matching_sections.append(sec)
                    score = max(score, sec_score)

            if score > 0:
                results.append({
                    "book": book_key,
                    "chapter": ch_key,
                    "chapter_title": title,
                    "subject": book_data.get("subject", ""),
                    "sections": matching_sections,
                    "start_page": ch_data.get("start_page"),
                    "end_page": ch_data.get("end_page"),
                    "score": score,
                    "method": "toc",
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ══════════════════════════════════════════════════════
# Hybrid (RRF Fusion)
# ══════════════════════════════════════════════════════

def rrf_merge(result_lists: list[list[dict]], k: int = RRF_K) -> list[dict]:
    """
    Reciprocal Rank Fusion (RRF) 排序融合

    score(doc) = Σ 1 / (k + rank_i)  对每个结果列表 i
    """
    doc_scores: dict[str, float] = {}
    doc_data: dict[str, dict] = {}
    doc_methods: dict[str, set] = {}

    for results in result_lists:
        for rank, r in enumerate(results):
            # 用 book+text[:50] 做近似 dedup key
            doc_id = f"{r.get('book', '')}:{r.get('text', '')[:80]}"
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
            if doc_id not in doc_data:
                doc_data[doc_id] = r
            doc_methods.setdefault(doc_id, set()).add(r.get("method", ""))

    # 按 RRF 分数排序
    merged = []
    for doc_id in sorted(doc_scores, key=doc_scores.get, reverse=True):
        entry = dict(doc_data[doc_id])
        entry["rrf_score"] = doc_scores[doc_id]
        entry["methods"] = sorted(doc_methods[doc_id])
        merged.append(entry)

    return merged


def search_hybrid(query: str, chunks, vecs, bm25_data, toc, top_k: int = 10) -> list[dict]:
    """三路混合搜索"""
    results_lists = []

    # Vector
    if len(chunks) > 0:
        vec_results = search_vector(query, chunks, vecs, top_k=top_k * 2)
        results_lists.append(vec_results)

    # BM25
    if bm25_data:
        bm25_results = search_bm25(query, bm25_data, top_k=top_k * 2)
        results_lists.append(bm25_results)

    # TOC
    if toc:
        toc_results = search_toc(query, toc, top_k=top_k)
        results_lists.append(toc_results)

    if not results_lists:
        return []

    merged = rrf_merge(results_lists)
    return merged[:top_k]


# ══════════════════════════════════════════════════════
# Display
# ══════════════════════════════════════════════════════

def display_results(results: list[dict], query: str):
    """格式化输出搜索结果"""
    print(f"\n  Query: \"{query}\"")
    print(f"  Results: {len(results)}")
    print("  " + "=" * 72)

    for i, r in enumerate(results):
        method = r.get("method", ",".join(r.get("methods", [])))
        book = r.get("book", "?")
        chapter = r.get("chapter_title") or r.get("chapter", "?")

        # RRF 结果显示
        if "rrf_score" in r:
            methods_str = "+".join(r.get("methods", []))
            score_str = f"RRF={r['rrf_score']:.4f} [{methods_str}]"
        else:
            score_str = f"{method}={r.get('score', 0):.4f}"

        print(f"\n  [{i+1}] {score_str}")
        print(f"      Book: {book} | Ch: {chapter}")

        if r.get("page"):
            print(f"      Page: {r['page']}")

        # TOC 结果显示子节
        if r.get("sections"):
            for sec in r["sections"][:3]:
                print(f"      >> {sec.get('id', '')} {sec.get('title', '')}")
                if sec.get("start_page"):
                    print(f"         p.{sec['start_page']}-{sec.get('end_page', '?')}")

        # 文本片段
        if r.get("text"):
            text = r["text"][:200].replace("\n", " ")
            print(f"      \"{text}...\"")

    print("\n  " + "=" * 72)


# ══════════════════════════════════════════════════════
# Interactive Mode
# ══════════════════════════════════════════════════════

def interactive_mode():
    """交互式搜索循环"""
    print("\n  === Textbook Hybrid Search ===")
    print("  Loading indices...")

    t0 = time.time()
    chunks, vecs = load_vectors()
    bm25_data = load_bm25()
    toc = load_toc()
    print(f"  Loaded: {len(chunks)} vectors, {len(bm25_data)} BM25, {len(toc)} TOC books ({time.time()-t0:.1f}s)")
    print("  Commands: /mode [vector|bm25|toc|hybrid], /book <key>, /quit")

    mode = "hybrid"
    book_filter = None

    while True:
        try:
            query = input(f"\n  [{mode}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query:
            continue
        if query in ("/quit", "/q", "/exit"):
            break

        if query.startswith("/mode "):
            mode = query.split()[1]
            print(f"  Mode: {mode}")
            continue

        if query.startswith("/book "):
            book_filter = query.split()[1] if query.split()[1] != "all" else None
            print(f"  Book filter: {book_filter or 'all'}")
            # 重新加载对应数据
            chunks, vecs = load_vectors(book_filter)
            bm25_data = load_bm25(book_filter)
            continue

        t0 = time.time()
        if mode == "vector":
            results = search_vector(query, chunks, vecs)
        elif mode == "bm25":
            results = search_bm25(query, bm25_data)
        elif mode == "toc":
            results = search_toc(query, toc)
        else:  # hybrid
            results = search_hybrid(query, chunks, vecs, bm25_data, toc)

        display_results(results, query)
        print(f"  ({time.time()-t0:.2f}s)")


# ══════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════

def main():
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="教材三路混合搜索")
    parser.add_argument("query", nargs="?", help="搜索查询")
    parser.add_argument("--mode", choices=["vector", "bm25", "toc", "hybrid"],
                        default="hybrid", help="搜索模式")
    parser.add_argument("--book", type=str, help="限定书籍")
    parser.add_argument("--top", type=int, default=10, help="返回结果数")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        return

    if not args.query:
        parser.print_help()
        return

    # 单次查询
    t0 = time.time()

    if args.mode in ("vector", "hybrid"):
        chunks, vecs = load_vectors(args.book)
    else:
        chunks, vecs = [], np.array([])

    if args.mode in ("bm25", "hybrid"):
        bm25_data = load_bm25(args.book)
    else:
        bm25_data = []

    if args.mode in ("toc", "hybrid"):
        toc = load_toc()
    else:
        toc = {}

    if args.mode == "vector":
        results = search_vector(args.query, chunks, vecs, args.top)
    elif args.mode == "bm25":
        results = search_bm25(args.query, bm25_data, args.top)
    elif args.mode == "toc":
        results = search_toc(args.query, toc, args.top)
    else:
        results = search_hybrid(args.query, chunks, vecs, bm25_data, toc, args.top)

    display_results(results, args.query)
    print(f"  ({time.time()-t0:.2f}s)")


if __name__ == "__main__":
    main()
