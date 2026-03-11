"""
PageIndex Retriever
页码索引检索器 — 基于文档结构树（structure JSON）进行标题匹配

Data format (sutton_structure.json):
  {
    "doc_name": "sutton",
    "structure": [
      {"title": "...", "node_id": "0036", "line_num": 448},
      ...
    ]
  }

Search strategy:
  1. Tokenize query into lowercase terms
  2. Score each node by term-overlap + substring-match (same logic as TOC)
  3. Return top-k nodes with line_num as the primary locator
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .base import BaseRetriever, RetrievalResult


class PageIndexRetriever(BaseRetriever):
    """基于文档结构树（PageIndex structure JSON）的章节标题检索。"""

    name = "pageindex"

    def __init__(self, structure_path: Path, book: str):
        self.structure_path = structure_path
        self.book = book

        with open(structure_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.doc_name: str = data.get("doc_name", book)
        self.nodes: list[dict] = data.get("structure", [])

    def search(self, query: str, top_k: int = 10) -> list[RetrievalResult]:
        q = query.lower().strip()
        q_terms = set(re.findall(r"[a-z0-9]+", q))
        if not q_terms:
            return []

        scored: list[RetrievalResult] = []

        for node in self.nodes:
            title = node.get("title", "")
            title_lower = title.lower()
            title_terms = set(re.findall(r"[a-z0-9]+", title_lower))

            # Score: term overlap + substring bonus
            overlap = len(q_terms & title_terms)
            if overlap == 0 and q not in title_lower:
                continue

            score = 0.0
            if overlap:
                score += overlap / max(len(q_terms), 1)
            if q in title_lower:
                score += 2.0

            node_id = node.get("node_id", "")
            line_num = node.get("line_num")

            scored.append(
                RetrievalResult(
                    doc_id=f"{self.book}:pageindex:{node_id}",
                    score=score,
                    title=title,
                    book=self.book,
                    method=self.name,
                    text=title,
                    page=None,  # pageindex uses line_num, not page
                    meta={
                        "node_id": node_id,
                        "line_num": line_num,
                    },
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]
