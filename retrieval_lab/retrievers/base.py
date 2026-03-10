from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class RetrievalResult:
    doc_id: str
    score: float
    title: str
    book: str
    method: str
    text: str = ""
    page: int | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BaseRetriever:
    name = "base"

    def search(self, query: str, top_k: int = 10) -> list[RetrievalResult]:
        raise NotImplementedError
