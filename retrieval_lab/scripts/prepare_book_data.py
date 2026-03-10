from __future__ import annotations

import argparse
import importlib.util
import json
import pickle
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
LAB_ROOT = SCRIPT_DIR.parent
WORKSPACE_ROOT = LAB_ROOT.parent
CONFIG_PATH = WORKSPACE_ROOT / ".shared" / "skills" / "learning-textbook_search" / "scripts" / "config.py"


def load_config_module():
    spec = importlib.util.spec_from_file_location("textbook_search_config", CONFIG_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load config from {CONFIG_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_bm25_docs(bm25_path: Path) -> list[dict]:
    with open(bm25_path, "rb") as f:
        data = pickle.load(f)
    return data["docs"]


def load_toc_book(toc_path: Path, book: str) -> dict:
    with open(toc_path, "r", encoding="utf-8") as f:
        toc = json.load(f)
    return toc.get(book, {})


def write_manifest(book: str, docs: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in docs:
            row = {
                "doc_id": f"{book}:{doc['id']}",
                "book": doc.get("book", book),
                "title": doc.get("chapter_title") or doc.get("chapter") or book,
                "chapter": doc.get("chapter", ""),
                "section": doc.get("section", ""),
                "page": doc.get("page"),
                "text": doc.get("text", ""),
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_pageindex_seed(book: str, toc_book: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    headings = toc_book.get("headings", [])
    tree = {
        "title": book,
        "node_id": book,
        "summary": f"Seed tree for {book}, derived from TOC headings.",
        "nodes": [],
    }
    for idx, heading in enumerate(headings, start=1):
        title = heading.get("title", "").strip()
        if not title:
            continue
        tree["nodes"].append(
            {
                "title": title,
                "node_id": f"{book}-{idx:04d}",
                "start_page": heading.get("page"),
                "end_page": heading.get("page"),
            }
        )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)


def copy_sirchmunk_source(src_md: Path, book: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{book}.md"
    shutil.copy2(src_md, target)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare retrieval_lab data assets for one textbook.")
    parser.add_argument("--book", default="sutton")
    args = parser.parse_args()

    config = load_config_module()
    data_dir = config.DATA_DIR
    book = args.book

    bm25_path = data_dir / "bm25" / f"{book}_bm25.pkl"
    toc_path = data_dir / "toc_index.json"
    src_md = config.get_mineru_md(book)

    if not bm25_path.exists():
        raise FileNotFoundError(f"BM25 index not found: {bm25_path}")
    if not toc_path.exists():
        raise FileNotFoundError(f"TOC index not found: {toc_path}")
    if not src_md.exists():
        raise FileNotFoundError(f"Source markdown not found: {src_md}")

    docs = load_bm25_docs(bm25_path)
    toc_book = load_toc_book(toc_path, book)

    manifest_path = data_dir / "manifests" / f"{book}_manifest.jsonl"
    pageindex_seed_path = data_dir / "pageindex" / f"{book}_structure_seed.json"
    sirchmunk_dir = data_dir / "sirchmunk" / "books"

    write_manifest(book, docs, manifest_path)
    write_pageindex_seed(book, toc_book, pageindex_seed_path)
    copied_path = copy_sirchmunk_source(src_md, book, sirchmunk_dir)

    summary = {
        "book": book,
        "manifest": str(manifest_path.relative_to(WORKSPACE_ROOT)),
        "pageindex_seed": str(pageindex_seed_path.relative_to(WORKSPACE_ROOT)),
        "sirchmunk_source": str(copied_path.relative_to(WORKSPACE_ROOT)),
        "docs": len(docs),
        "headings": len(toc_book.get("headings", [])),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
