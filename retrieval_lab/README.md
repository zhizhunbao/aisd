# Retrieval Lab

Minimal retrieval experiment harness for textbook search.

Current status:
- Lives at workspace root
- Uses `retrieval_lab/data/search_data/` for reusable search indexes
- Uses `retrieval_lab/data/benchmarks/` for query sets
- Starts with one test book: `sutton`

## Retrieval Methods

Independent retrievers:
- `bm25` — BM25 keyword search (pickled index)
- `toc` — TOC heading fuzzy match (toc_index.json)
- `pageindex` — Document structure tree node matching (structure JSON from sirchmunk)
- `vector` — Standard RAG semantic search (Ollama nomic-embed-text + cosine similarity)
- `sirchmunk` — Full-text grep via ripgrep-all (rga) on source markdown

Fusion strategies:
- `ensemble` — Reciprocal Rank Fusion (RRF) over multiple retrievers

## Prerequisites

| Method     | Requires                                      |
|------------|-----------------------------------------------|
| bm25       | `{book}_bm25.pkl` in `_search_data/bm25/`    |
| toc        | `toc_index.json` in `_search_data/`           |
| pageindex  | `{book}_structure.json` in `data/search_data/pageindex/` |
| vector     | `{book}_vectors.json` in `data/search_data/vectors/` + Ollama running |
| sirchmunk  | `{book}.md` in `data/search_data/sirchmunk/books/` + rga installed |
| ensemble   | Same as bm25 + toc                            |

## Data Layout

- `retrieval_lab/data/search_data/`
  - reusable indexes and method-specific assets
- `retrieval_lab/data/benchmarks/`
  - query sets, raw runs, and reports

## Run Examples

```bash
# Keyword search
uv run python retrieval_lab/scripts/run_query.py --book sutton --method bm25 "kernel trick"

# TOC heading match
uv run python retrieval_lab/scripts/run_query.py --book sutton --method toc "graphical models"

# PageIndex structure search
uv run python retrieval_lab/scripts/run_query.py --book sutton --method pageindex "Monte Carlo"

# Standard RAG (requires Ollama)
uv run python retrieval_lab/scripts/run_query.py --book sutton --method vector "temporal difference learning"

# Sirchmunk grep (requires rga)
uv run python retrieval_lab/scripts/run_query.py --book sutton --method sirchmunk "policy gradient"

# RRF Fusion
uv run python retrieval_lab/scripts/run_query.py --book sutton --method ensemble "graphical models"

# Benchmark
uv run python retrieval_lab/scripts/benchmark.py --book sutton
```
