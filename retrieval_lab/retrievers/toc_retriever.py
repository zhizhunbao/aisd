from __future__ import annotations

import json
import re
from pathlib import Path

from .base import BaseRetriever, RetrievalResult


class TOCRetriever(BaseRetriever):
    name = "toc"

    def __init__(self, toc_path: Path, book: str):
        self.toc_path = toc_path
        self.book = book
        with open(toc_path, "r", encoding="utf-8") as f:
            toc = json.load(f)
        self.headings = toc.get(book, {}).get("headings", [])

    def search(self, query: str, top_k: int = 10) -> list[RetrievalResult]:
        q = query.lower().strip()
        q_terms = set(re.findall(r"[a-z0-9]+", q))
        if not q_terms:
            return []

        scored: list[RetrievalResult] = []
        for idx, heading in enumerate(self.headings):
            title = heading.get("title", "")
            title_lower = title.lower()
            title_terms = set(re.findall(r"[a-z0-9]+", title_lower))
            overlap = len(q_terms & title_terms)
            if overlap == 0 and q not in title_lower:
                continue

            score = 0.0
            if overlap:
                score += overlap / max(len(q_terms), 1)
            if q in title_lower:
                score += 2.0

            scored.append(
                RetrievalResult(
                    doc_id=f"{self.book}:toc:{idx}",
                    score=score,
                    title=title,
                    book=self.book,
                    method=self.name,
                    text=title,
                    page=heading.get("page"),
                    meta={"heading_index": idx},
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]
