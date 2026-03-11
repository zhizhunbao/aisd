from __future__ import annotations

import importlib.util
from pathlib import Path

from retrieval_lab.retrievers import (
    BM25Retriever,
    EnsembleRetriever,
    PageIndexRetriever,
    SirchmunkRetriever,
    TOCRetriever,
    VectorRetriever,
)


ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = ROOT.parent
CONFIG_PATH = WORKSPACE_ROOT / ".agent" / "skills" / "learning-textbook-search" / "scripts" / "config.py"


def load_config_module():
    spec = importlib.util.spec_from_file_location("textbook_search_config", CONFIG_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load config from {CONFIG_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_retriever(book: str, method: str):
    config = load_config_module()
    data_dir: Path = config.DATA_DIR
    lab_data = ROOT / "data" / "search_data"

    bm25 = BM25Retriever(data_dir / "bm25" / f"{book}_bm25.pkl", book)
    toc = TOCRetriever(data_dir / "toc_index.json", book)

    if method == "bm25":
        return bm25
    if method == "toc":
        return toc
    if method == "ensemble":
        return EnsembleRetriever([bm25, toc], rrf_k=config.RRF_K)

    # ── PageIndex ─────────────────────────────────────
    if method == "pageindex":
        structure_path = lab_data / "pageindex" / f"{book}_structure.json"
        if not structure_path.exists():
            raise FileNotFoundError(f"PageIndex structure not found: {structure_path}")
        return PageIndexRetriever(structure_path, book)

    # ── Vector (standard RAG) ─────────────────────────
    if method == "vector":
        vectors_path = lab_data / "vectors" / f"{book}_vectors.json"
        if not vectors_path.exists():
            raise FileNotFoundError(f"Vectors file not found: {vectors_path}")
        return VectorRetriever(
            vectors_path,
            book,
            ollama_base=getattr(config, "OLLAMA_URL", "http://localhost:11434"),
            embed_model=getattr(config, "EMBED_MODEL", "nomic-embed-text"),
        )

    # ── Sirchmunk (rga grep) ──────────────────────────
    if method == "sirchmunk":
        books_dir = lab_data / "sirchmunk" / "books"
        cache_dir = lab_data / "sirchmunk" / "work" / ".cache" / "rga"
        return SirchmunkRetriever(
            books_dir,
            book,
            cache_dir=cache_dir if cache_dir.exists() else None,
        )

    raise ValueError(f"Unsupported method: {method}")

