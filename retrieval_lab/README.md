# Retrieval Lab

Minimal retrieval experiment harness for textbook search.

Current status:
- Lives at workspace root
- Uses `retrieval_lab/data/search_data/` for reusable search indexes
- Uses `retrieval_lab/data/benchmarks/` for query sets
- Starts with one test book: `barber`
- Supports:
  - `bm25`
  - `toc`
  - `ensemble` (RRF over all enabled retrievers)

Planned extension points:
- `vector`
- `pageindex`
- `sirchmunk`

Data layout:
- `retrieval_lab/data/search_data/`
  - reusable indexes and method-specific assets
- `retrieval_lab/data/benchmarks/`
  - query sets, raw runs, and reports

Run examples:

```bash
uv run python retrieval_lab/scripts/run_query.py --book barber --method bm25 "kernel trick"
uv run python retrieval_lab/scripts/run_query.py --book barber --method toc "graphical models"
uv run python retrieval_lab/scripts/run_query.py --book barber --method ensemble "graphical models"
uv run python retrieval_lab/scripts/benchmark.py --book barber
```
