from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
LAB_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(LAB_ROOT.parent))

from retrieval_lab.common import build_retriever


def load_queries(book: str) -> list[dict]:
    path = LAB_ROOT / "data" / "benchmarks" / f"{book}_queries.jsonl"
    queries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                queries.append(json.loads(line))
    return queries


def recall_at_k(results: list[dict], expected_terms: list[str]) -> float:
    for result in results:
        haystacks = [
            result.get("title", "").lower(),
            result.get("text", "").lower(),
        ]
        if any(term.lower() in " ".join(haystacks) for term in expected_terms):
            return 1.0
    return 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark textbook retrieval methods.")
    parser.add_argument("--book", default="barber")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--include-vector", action="store_true", help="Include vector (RAG) method (requires Ollama)")
    parser.add_argument("--include-sirchmunk", action="store_true", help="Include sirchmunk method (requires rga)")
    args = parser.parse_args()

    queries = load_queries(args.book)
    methods = ["bm25", "toc", "pageindex", "ensemble"]
    if args.include_vector:
        methods.append("vector")
    if args.include_sirchmunk:
        methods.append("sirchmunk")

    for method in methods:
        try:
            retriever = build_retriever(args.book, method)
        except (FileNotFoundError, RuntimeError) as exc:
            print(json.dumps({"book": args.book, "method": method, "skipped": str(exc)}))
            continue

        recalls = []
        latencies = []
        for item in queries:
            started = time.perf_counter()
            results = retriever.search(item["query"], top_k=args.top_k)
            latencies.append((time.perf_counter() - started) * 1000)
            recalls.append(
                recall_at_k(
                    [r.to_dict() for r in results],
                    item["expected_terms"],
                )
            )

        avg_recall = sum(recalls) / len(recalls) if recalls else 0.0
        p50 = statistics.median(latencies) if latencies else 0.0
        print(
            json.dumps(
                {
                    "book": args.book,
                    "method": method,
                    "queries": len(queries),
                    "recall_at_k": round(avg_recall, 3),
                    "p50_latency_ms": round(p50, 2),
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
