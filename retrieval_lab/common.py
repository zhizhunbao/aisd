from __future__ import annotations

import importlib.util
from pathlib import Path

from retrieval_lab.retrievers import BM25Retriever, EnsembleRetriever, TOCRetriever


ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = ROOT.parent
CONFIG_PATH = WORKSPACE_ROOT / ".shared" / "skills" / "learning-textbook_search" / "scripts" / "config.py"


def load_config_module():
    spec = importlib.util.spec_from_file_location("textbook_search_config", CONFIG_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load config from {CONFIG_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_retriever(book: str, method: str):
    config = load_config_module()
    data_dir = config.DATA_DIR

    bm25 = BM25Retriever(data_dir / "bm25" / f"{book}_bm25.pkl", book)
    toc = TOCRetriever(data_dir / "toc_index.json", book)

    if method == "bm25":
        return bm25
    if method == "toc":
        return toc
    if method == "ensemble":
        return EnsembleRetriever([bm25, toc], rrf_k=config.RRF_K)
    raise ValueError(f"Unsupported method: {method}")
