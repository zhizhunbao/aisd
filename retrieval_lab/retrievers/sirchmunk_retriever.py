"""
Sirchmunk Retriever
Sirchmunk 检索器 — 基于 ripgrep-all (rga) 在 markdown 源文件中进行全文搜索

Requirements:
  - rga (ripgrep-all) installed and accessible
  - On Windows, the WSL setup script provides binaries at:
      retrieval_lab/data/search_data/sirchmunk/work/bin/rga
  - Source markdown files placed in:
      retrieval_lab/data/search_data/sirchmunk/books/{book}.md

Search strategy:
  1. Build rga command with query pattern
  2. Parse JSON-lines output (with --json flag)
  3. Deduplicate + rank by match frequency
  4. Return top-k results with line numbers and matched text
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .base import BaseRetriever, RetrievalResult


class SirchmunkRetriever(BaseRetriever):
    """基于 ripgrep-all (rga) 的全文 grep 检索。"""

    name = "sirchmunk"

    def __init__(
        self,
        books_dir: Path,
        book: str,
        *,
        rga_bin: str | None = None,
        cache_dir: Path | None = None,
    ):
        self.book = book
        self.source_md = books_dir / f"{book}.md"
        self.rga_bin = rga_bin or "rga"
        self.cache_dir = cache_dir

        if not self.source_md.exists():
            raise FileNotFoundError(
                f"Sirchmunk source markdown not found: {self.source_md}"
            )

    # ── Internal: run rga ────────────────────────────────

    def _run_rga(self, pattern: str, *, case_sensitive: bool = False) -> list[dict]:
        """Run rga and return parsed JSON matches."""
        cmd = [self.rga_bin, "--no-config", "--json"]

        if not case_sensitive:
            cmd.append("-i")

        if self.cache_dir:
            cmd.append(f"--rga-cache-path={self.cache_dir}")

        cmd.extend([pattern, str(self.source_md)])

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
                timeout=30,
            )
        except FileNotFoundError:
            raise RuntimeError(
                f"rga binary not found at '{self.rga_bin}'. "
                "Install ripgrep-all or run setup_sirchmunk_wsl.sh."
            )

        if result.returncode > 1 and not result.stdout.strip():
            raise RuntimeError(f"rga failed (exit {result.returncode}): {result.stderr.strip()}")

        if not result.stdout.strip():
            return []

        matches = []
        for line in result.stdout.strip().splitlines():
            try:
                obj = json.loads(line)
                if obj.get("type") == "match":
                    matches.append(obj)
            except json.JSONDecodeError:
                continue

        return matches

    # ── Search ───────────────────────────────────────────

    def search(self, query: str, top_k: int = 10) -> list[RetrievalResult]:
        # Build a regex-safe OR pattern from query terms
        terms = re.findall(r"[a-zA-Z0-9]+", query)
        if not terms:
            return []

        # Use alternation so rga matches any term
        pattern = "|".join(re.escape(t) for t in terms)

        raw_matches = self._run_rga(pattern)
        if not raw_matches:
            return []

        # Group matches and score by number of matched terms
        results: list[RetrievalResult] = []

        for idx, match in enumerate(raw_matches):
            data = match.get("data", {})
            lines_data = data.get("lines", {})
            text = lines_data.get("text", "").strip()

            line_number = data.get("line_number")
            path_text = data.get("path", {}).get("text", "")

            # Score: count how many query terms appear in the matched line
            text_lower = text.lower()
            term_hits = sum(1 for t in terms if t.lower() in text_lower)
            score = term_hits / max(len(terms), 1)

            results.append(
                RetrievalResult(
                    doc_id=f"{self.book}:sirchmunk:{idx}",
                    score=score,
                    title=self.book,
                    book=self.book,
                    method=self.name,
                    text=text[:500],  # Truncate long lines
                    page=None,
                    meta={
                        "line_number": line_number,
                        "source_path": path_text,
                        "term_hits": term_hits,
                    },
                )
            )

        # Sort by score descending, then by line_number ascending for ties
        results.sort(
            key=lambda r: (-r.score, r.meta.get("line_number", float("inf")))
        )
        return results[:top_k]
