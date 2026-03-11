"""
Vector Retriever (Standard RAG)
向量检索器 — 标准 RAG 语义搜索

Flow:
  1. Load pre-built vectors JSON (from textbook-vectorization or learning-textbook-search)
  2. Embed query via Ollama nomic-embed-text
  3. Compute cosine similarity
  4. Return top-k results

Data format (sutton_vectors.json):
  {
    "metadata": { "book": "sutton", "model": "nomic-embed-text", "dim": 768, ... },
    "chunks": [
      { "id": 0, "book": "sutton", "chapter": "...", "chapter_title": "...",
        "section": "...", "page": 2, "text": "...", "embedding": [...] },
      ...
    ]
  }
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .base import BaseRetriever, RetrievalResult


class VectorRetriever(BaseRetriever):
    """标准 RAG 语义向量检索：Ollama embed → cosine similarity → top-k。"""

    name = "vector"

    def __init__(
        self,
        vectors_path: Path,
        book: str,
        *,
        ollama_base: str = "http://localhost:11434",
        embed_model: str = "nomic-embed-text",
    ):
        self.book = book
        self.ollama_base = ollama_base
        self.embed_model = embed_model

        with open(vectors_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.chunks: list[dict] = []
        embeddings: list[list[float]] = []
        for c in data["chunks"]:
            self.chunks.append(
                {
                    "id": c["id"],
                    "book": c.get("book", book),
                    "chapter": c.get("chapter", ""),
                    "chapter_title": c.get("chapter_title", ""),
                    "section": c.get("section", ""),
                    "page": c.get("page"),
                    "text": c.get("text", ""),
                }
            )
            embeddings.append(c["embedding"])

        self.vecs = np.array(embeddings, dtype=np.float32) if embeddings else np.array([])

    # ── Embed query ──────────────────────────────────────

    def _get_query_embedding(self, query: str) -> np.ndarray:
        """Get query embedding via Ollama local API."""
        import httpx

        resp = httpx.post(
            f"{self.ollama_base}/api/embed",
            json={"model": self.embed_model, "input": [query]},
            timeout=30,
        )
        resp.raise_for_status()
        return np.array(resp.json()["embeddings"][0], dtype=np.float32)

    # ── Cosine similarity ────────────────────────────────

    @staticmethod
    def _cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Batch cosine similarity: a (D,), b (N, D) → (N,)"""
        a_norm = a / (np.linalg.norm(a) + 1e-10)
        b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
        return b_norm @ a_norm

    # ── Search ───────────────────────────────────────────

    def search(self, query: str, top_k: int = 10) -> list[RetrievalResult]:
        if len(self.chunks) == 0:
            return []

        q_emb = self._get_query_embedding(query)
        sims = self._cosine_sim(q_emb, self.vecs)
        top_idx = np.argsort(sims)[-top_k:][::-1]

        results: list[RetrievalResult] = []
        for i in top_idx:
            chunk = self.chunks[i]
            results.append(
                RetrievalResult(
                    doc_id=f"{self.book}:vector:{chunk['id']}",
                    score=float(sims[i]),
                    title=chunk.get("chapter_title") or chunk.get("chapter") or self.book,
                    book=chunk.get("book", self.book),
                    method=self.name,
                    text=chunk.get("text", ""),
                    page=chunk.get("page"),
                    meta={
                        "chapter": chunk.get("chapter"),
                        "section": chunk.get("section"),
                        "chunk_id": chunk["id"],
                    },
                )
            )
        return results
