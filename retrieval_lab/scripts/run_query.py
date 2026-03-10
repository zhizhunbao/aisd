from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
LAB_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(LAB_ROOT.parent))

from retrieval_lab.common import build_retriever


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one retrieval query against a textbook.")
    parser.add_argument("query", help="Query text")
    parser.add_argument("--book", default="barber", help="Book key to test")
    parser.add_argument(
        "--method",
        default="ensemble",
        choices=["bm25", "toc", "ensemble"],
        help="Retrieval method",
    )
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    retriever = build_retriever(args.book, args.method)
    results = retriever.search(args.query, top_k=args.top_k)
    print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
