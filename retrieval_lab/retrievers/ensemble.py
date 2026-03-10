from __future__ import annotations

from collections import defaultdict

from .base import BaseRetriever, RetrievalResult


class EnsembleRetriever(BaseRetriever):
    name = "ensemble"

    def __init__(self, retrievers: list[BaseRetriever], rrf_k: int = 60):
        self.retrievers = retrievers
        self.rrf_k = rrf_k

    def search(self, query: str, top_k: int = 10) -> list[RetrievalResult]:
        score_map: dict[str, float] = defaultdict(float)
        doc_map: dict[str, RetrievalResult] = {}
        methods_map: dict[str, set[str]] = defaultdict(set)

        for retriever in self.retrievers:
            results = retriever.search(query, top_k=top_k * 2)
            for rank, result in enumerate(results, start=1):
                score_map[result.doc_id] += 1.0 / (self.rrf_k + rank)
                doc_map.setdefault(result.doc_id, result)
                methods_map[result.doc_id].add(retriever.name)

        merged: list[RetrievalResult] = []
        for doc_id in sorted(score_map, key=score_map.get, reverse=True):
            base = doc_map[doc_id]
            merged.append(
                RetrievalResult(
                    doc_id=base.doc_id,
                    score=score_map[doc_id],
                    title=base.title,
                    book=base.book,
                    method=self.name,
                    text=base.text,
                    page=base.page,
                    meta={**base.meta, "methods": sorted(methods_map[doc_id])},
                )
            )
        return merged[:top_k]
