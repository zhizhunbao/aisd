from __future__ import annotations

import pickle
import re
from pathlib import Path

from .base import BaseRetriever, RetrievalResult


class BM25Retriever(BaseRetriever):
    name = "bm25"

    def __init__(self, index_path: Path, book: str):
        self.index_path = index_path
        self.book = book
        with open(index_path, "rb") as f:
            data = pickle.load(f)
        self.bm25 = data["bm25"]
        self.docs = data["docs"]

    def search(self, query: str, top_k: int = 10) -> list[RetrievalResult]:
        tokens = re.findall(r"[a-z0-9]+", query.lower())
        if not tokens:
            return []

        scores = self.bm25.get_scores(tokens)
        ranked_idx = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )

        results: list[RetrievalResult] = []
        for i in ranked_idx:
            score = float(scores[i])
            if score <= 0:
                continue
            doc = self.docs[i]
            results.append(
                RetrievalResult(
                    doc_id=f"{self.book}:bm25:{doc['id']}",
                    score=score,
                    title=doc.get("chapter_title") or doc.get("chapter") or self.book,
                    book=doc.get("book", self.book),
                    method=self.name,
                    text=doc.get("text", ""),
                    page=doc.get("page"),
                    meta={
                        "chapter": doc.get("chapter"),
                        "section": doc.get("section"),
                        "source_id": doc.get("id"),
                    },
                )
            )
            if len(results) >= top_k:
                break
        return results
