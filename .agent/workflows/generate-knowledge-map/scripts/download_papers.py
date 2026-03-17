#!/usr/bin/env python3
"""
download_papers.py — Knowledge Map Paper Downloader
=====================================================
Downloads academic papers to .documents/papers/{topic}/ for local reference.

Supports THREE modes:
  1. --url       Direct download from a PDF/arXiv/DOI URL
  2. --search    Search Semantic Scholar by title/keyword → auto-find open access PDF
  3. --from-km   Extract Paper URLs from a knowledge map frontmatter and batch download

Key APIs used (all free, no API key required for basic use):
  - Semantic Scholar: https://api.semanticscholar.org/graph/v1/
    * Search paper by title/keyword, returns openAccessPdf field
    * 100 req/5min unauthenticated; 1 req/sec with API key
  - Papers With Code: https://paperswithcode.com/api/v1/
    * Find papers by query, get associated GitHub code repos
  - arXiv API: https://export.arxiv.org/api/query
    * arXiv paper metadata + PDF links

Usage:
    # Mode 1: Direct URL download
    python download_papers.py --url "https://arxiv.org/abs/1705.07321" --topic dbscan

    # Mode 2: Search by title keyword (auto-finds open access PDF)
    python download_papers.py --search "DBSCAN density based clustering noise" --topic dbscan
    python download_papers.py --search "HDBSCAN" --topic dbscan --top 3

    # Mode 3: Batch from knowledge map frontmatter
    python download_papers.py --from-km knowledge-map/ml/dbscan/dbscan_map.md

    # Search + show Papers With Code links
    python download_papers.py --search "DBSCAN" --topic dbscan --pwc

Output:
    Downloads to: .documents/papers/{topic}/{author_year_keyword}.pdf
    Prints the file:/// path to paste into source_versions
    Creates/updates .documents/papers/{topic}/index.md
"""

import os
import re
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime

# Semantic Scholar API Key (optional, but strongly recommended to avoid 429 rate limits)
# Set via environment variable:  set S2_API_KEY=your_key_here
# Or pass via CLI:                --api-key your_key_here
S2_API_KEY: str | None = os.environ.get("S2_API_KEY")

# ── Configuration ──────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parents[3]  # scripts→generate-knowledge-map→workflows→.agent→workspace
PAPERS_ROOT = WORKSPACE_ROOT / ".documents" / "papers"

HEADERS = {
    "User-Agent": (
        "KnowledgeMapDownloader/2.0 (academic research tool; "
        "contact: knowledge-map-bot)"
    )
}


def build_headers(extra_api_key: str | None = None) -> dict:
    """Build request headers, injecting x-api-key if available."""
    h = dict(HEADERS)
    key = extra_api_key or S2_API_KEY
    if key:
        h["x-api-key"] = key
    return h

# Semantic Scholar Graph API
S2_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_PAPER_URL  = "https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
S2_FIELDS = "title,authors,year,venue,externalIds,openAccessPdf,abstract"

# Papers With Code API
PWC_SEARCH_URL = "https://paperswithcode.com/api/v1/papers/"

# arXiv API
ARXIV_API_URL  = "https://export.arxiv.org/api/query"

# ── Helpers ────────────────────────────────────────────────────────────────────

def api_get(url: str, params: dict = None, _retry: bool = True) -> dict | None:
    """HTTP GET with JSON response, basic rate-limit handling."""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers=build_headers())
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 429:
            wait = 10 if S2_API_KEY else 30  # with key: shorter wait
            key_hint = "(加 API Key 后限速更宽松)" if not S2_API_KEY else ""
            print(f"  ⚠️  Rate limited (429). Waiting {wait}s... {key_hint}")
            time.sleep(wait)
            if _retry:
                return api_get(url, _retry=False)  # one retry
            return None
        print(f"  ❌ HTTP {e.code}: {e.reason} — {url}")
    except Exception as e:
        print(f"  ❌ Request error: {e}")
    return None


def normalize_to_pdf_url(url: str) -> str:
    """Convert arXiv abstract/various URLs to direct PDF URL."""
    # arXiv abstract → PDF
    m = re.match(r"https?://arxiv\.org/abs/([\w.]+)", url)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}.pdf"
    # arXiv PDF (ensure .pdf)
    m = re.match(r"https?://arxiv\.org/pdf/([\w.]+?)(?:\.pdf)?$", url)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}.pdf"
    return url


def make_filename(authors: list[str], year: int | None, title: str, topic: str) -> str:
    """
    Build a readable filename: firstauthor_year_keyword.pdf
    e.g. ester_1996_dbscan.pdf
    """
    first_author = ""
    if authors:
        # Take last name of first author
        first_author = authors[0].split()[-1].lower()
        first_author = re.sub(r"[^a-z0-9]", "", first_author)

    yr = str(year) if year else "xxxx"

    # Keyword from title: first 2 non-stopword words
    stopwords = {"a", "an", "the", "of", "on", "in", "for", "with", "and",
                 "or", "is", "are", "to", "by", "from", "based", "using",
                 "large", "spatial", "applications"}
    words = [w.lower() for w in re.split(r'\W+', title) if w.lower() not in stopwords]
    keyword = "_".join(words[:2]) if words else topic
    keyword = re.sub(r"[^a-z0-9_]", "", keyword)[:30]

    return f"{first_author}_{yr}_{keyword}.pdf"


def path_to_file_uri(path: Path) -> str:
    """Convert Path to file:/// URI (handles Windows backslashes)."""
    return path.resolve().as_uri()


# ── Semantic Scholar ───────────────────────────────────────────────────────────

def s2_search(query: str, top_n: int = 5) -> list[dict]:
    """
    Search Semantic Scholar for papers matching query.
    Returns list of paper dicts with title, authors, year, openAccessPdf.

    API docs: https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_get_paper_search
    """
    print(f"\n🔍 Searching Semantic Scholar: '{query}'")
    data = api_get(S2_SEARCH_URL, {
        "query": query,
        "fields": S2_FIELDS,
        "limit": top_n,
    })
    if not data or "data" not in data:
        print("  ⚠️  No results from Semantic Scholar")
        return []

    results = []
    for p in data["data"]:
        authors = [a.get("name", "") for a in p.get("authors", [])]
        open_pdf = p.get("openAccessPdf")
        arxiv_id = (p.get("externalIds") or {}).get("ArXiv")

        # Build best available PDF URL
        pdf_url = None
        if open_pdf:
            pdf_url = open_pdf.get("url")
        if not pdf_url and arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        results.append({
            "s2_id":   p.get("paperId"),
            "title":   p.get("title", "Unknown"),
            "authors": authors,
            "year":    p.get("year"),
            "venue":   p.get("venue", ""),
            "abstract": (p.get("abstract") or "")[:200],
            "pdf_url": pdf_url,
            "arxiv_id": arxiv_id,
        })

    return results


def print_s2_results(results: list[dict]) -> None:
    """Pretty-print Semantic Scholar search results."""
    print(f"\n{'─'*60}")
    for i, p in enumerate(results):
        authors_str = ", ".join(p["authors"][:3])
        if len(p["authors"]) > 3:
            authors_str += " et al."
        pdf_status = "✅ Open Access" if p["pdf_url"] else "❌ No open access PDF"
        venue = f" ({p['venue']})" if p["venue"] else ""
        print(f"\n[{i+1}] {p['title']}")
        print(f"     {authors_str}{venue} {p['year'] or ''}")
        print(f"     {pdf_status}")
        if p["pdf_url"]:
            print(f"     PDF: {p['pdf_url']}")
        if p["abstract"]:
            print(f"     Abstract: {p['abstract']}...")
    print(f"{'─'*60}\n")


# ── Papers With Code ───────────────────────────────────────────────────────────

def pwc_search(query: str, top_n: int = 5) -> list[dict]:
    """
    Search Papers With Code for papers + associated GitHub code repos.
    API docs: https://paperswithcode.com/api/v1/docs/

    Returns list with paper info + code_url.
    """
    print(f"\n🔍 Searching Papers With Code: '{query}'")
    data = api_get(PWC_SEARCH_URL, {
        "q": query,
        "page_size": top_n,
    })
    if not data or "results" not in data:
        print("  ⚠️  No results from Papers With Code")
        return []

    results = []
    for p in data["results"]:
        results.append({
            "title":    p.get("title", ""),
            "arxiv_id": p.get("arxiv_id", ""),
            "url_pdf":  p.get("url_pdf", ""),
            "url_abs":  p.get("url_abs", ""),
            "github_urls": [r.get("url") for r in p.get("repositories", []) if r.get("url")],
        })

    return results


def print_pwc_results(results: list[dict]) -> None:
    """Pretty-print Papers With Code results."""
    print(f"\n{'─'*60}")
    print("📄 Papers With Code results:")
    for i, p in enumerate(results):
        print(f"\n[{i+1}] {p['title']}")
        if p["url_pdf"]:
            print(f"     PDF:    {p['url_pdf']}")
        if p["arxiv_id"]:
            print(f"     arXiv:  https://arxiv.org/abs/{p['arxiv_id']}")
        if p["github_urls"]:
            print(f"     Code:   {', '.join(p['github_urls'][:3])}")
    print(f"{'─'*60}\n")


# ── Downloader ─────────────────────────────────────────────────────────────────

def download_paper(url: str, topic: str, filename: str | None = None,
                   dry_run: bool = False) -> Path | None:
    """Download PDF to PAPERS_ROOT/{topic}/{filename}. Returns local Path."""
    pdf_url = normalize_to_pdf_url(url)
    out_dir = PAPERS_ROOT / topic
    out_dir.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = re.sub(r"[^a-zA-Z0-9._-]", "_", pdf_url.split("/")[-1])
        if not filename.endswith(".pdf"):
            filename += ".pdf"

    dest = out_dir / filename

    if dest.exists():
        print(f"  ✅ Already exists: {dest.name}")
        return dest

    if dry_run:
        print(f"  [dry-run] Would download:\n    {pdf_url}\n    → {dest}")
        return None

    print(f"  ⬇️  {pdf_url}")
    print(f"      → {dest}")
    try:
        req = urllib.request.Request(pdf_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest, "wb") as f:
            f.write(data)
        print(f"  ✅ Done ({len(data)//1024} KB)")
        return dest
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"  ❌ URL Error: {e.reason}")
    except Exception as e:
        print(f"  ❌ {e}")
    return None


def update_index(topic: str, paper_meta: dict, local_path: Path) -> None:
    """Append entry to .documents/papers/{topic}/index.md"""
    index_path = PAPERS_ROOT / topic / "index.md"
    if not index_path.exists():
        index_path.write_text(
            f"# Papers — {topic}\n\n"
            f"| 文件 | 标题 | 作者 | 年份 | 来源 URL |\n"
            f"|------|------|------|------|----------|\n",
            encoding="utf-8"
        )
    file_uri = path_to_file_uri(local_path)
    authors = ", ".join(paper_meta.get("authors", [])[:3])
    if len(paper_meta.get("authors", [])) > 3:
        authors += " et al."
    title = paper_meta.get("title", local_path.stem)
    year  = paper_meta.get("year", "")
    src   = paper_meta.get("pdf_url") or paper_meta.get("url", "")
    with open(index_path, "a", encoding="utf-8") as f:
        f.write(f"| [{local_path.name}]({file_uri}) | {title} | {authors} | {year} | {src} |\n")


def extract_paper_urls_from_km(km_path: Path) -> list[tuple[str, str]]:
    """Parse Paper URLs from knowledge map YAML frontmatter."""
    content = km_path.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not fm:
        return []
    results = []
    for line in fm.group(1).splitlines():
        m = re.search(r"📖 Paper:\s*(.+?)\s*—\s*(https?://\S+)", line)
        if m:
            results.append((m.group(2).rstrip('"'), m.group(1).strip()))
    return results


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Knowledge Map Paper Downloader — supports direct URL, Semantic Scholar search, and batch from KM"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url",     help="Direct paper URL (PDF / arXiv / DOI)")
    group.add_argument("--search",  help="Search Semantic Scholar by title/keyword")
    group.add_argument("--from-km", help="Extract Paper URLs from a knowledge map .md file")

    parser.add_argument("--topic",    default="general", help="Topic subfolder name")
    parser.add_argument("--top",      type=int, default=5, help="Max results to show (--search mode)")
    parser.add_argument("--pwc",      action="store_true", help="Also show Papers With Code results (--search mode)")
    parser.add_argument("--filename", help="Custom output filename (--url mode only)")
    parser.add_argument("--dry-run",  action="store_true", help="Preview without downloading")
    parser.add_argument("--delay",    type=float, default=1.5, help="Delay between downloads (sec)")
    parser.add_argument("--api-key",  help="Semantic Scholar API Key (overrides S2_API_KEY env var)")

    args = parser.parse_args()

    # Inject API key from CLI arg (overrides env var)
    global S2_API_KEY
    if args.api_key:
        S2_API_KEY = args.api_key
        print(f"   🔑 Using API Key: {S2_API_KEY[:8]}...")
    elif S2_API_KEY:
        print(f"   🔑 Using API Key from env: {S2_API_KEY[:8]}...")
    else:
        print("   ⚠️  No API Key — using anonymous access (rate limit: 100 req/5min shared)")
        print("      Tip: Get a free key at https://www.semanticscholar.org/product/api#api-key")

    print(f"\n📚 Knowledge Map Paper Downloader v2")
    print(f"   Topic: {args.topic} | Output: {PAPERS_ROOT / args.topic}\n")

    downloaded = []

    # ── Mode 1: Direct URL ─────────────────────────────────────────────────────
    if args.url:
        meta = {"title": args.url, "authors": [], "year": None, "pdf_url": args.url}
        local = download_paper(args.url, args.topic, args.filename, args.dry_run)
        if local:
            update_index(args.topic, meta, local)
            downloaded.append((args.url, local))

    # ── Mode 2: Semantic Scholar Search ───────────────────────────────────────
    elif args.search:
        results = s2_search(args.search, top_n=args.top)
        if not results:
            sys.exit(1)
        print_s2_results(results)

        if args.pwc:
            pwc_results = pwc_search(args.search, top_n=args.top)
            if pwc_results:
                print_pwc_results(pwc_results)

        # Download the ones with open access PDFs
        downloadable = [r for r in results if r.get("pdf_url")]
        if not downloadable:
            print("⚠️  None of the results have open access PDFs.")
            print("   Try arXiv directly or check Unpaywall: https://unpaywall.org")
            sys.exit(0)

        print(f"Found {len(downloadable)} paper(s) with open access PDFs.")
        if len(downloadable) > 1:
            print("Enter numbers to download (e.g. 1 3), or 'all', or 'q' to quit:")
            choice = input("> ").strip().lower()
            if choice == "q":
                sys.exit(0)
            elif choice == "all":
                to_download = downloadable
            else:
                indices = []
                for c in choice.split():
                    try:
                        idx = int(c) - 1
                        if 0 <= idx < len(results) and results[idx].get("pdf_url"):
                            indices.append(results[idx])
                    except ValueError:
                        pass
                to_download = indices if indices else downloadable[:1]
        else:
            to_download = downloadable

        for i, paper in enumerate(to_download):
            filename = make_filename(
                paper["authors"], paper["year"], paper["title"], args.topic
            )
            local = download_paper(paper["pdf_url"], args.topic, filename, args.dry_run)
            if local:
                update_index(args.topic, paper, local)
                downloaded.append((paper["pdf_url"], local))
            if i < len(to_download) - 1:
                time.sleep(args.delay)

    # ── Mode 3: Batch from Knowledge Map ──────────────────────────────────────
    elif args.from_km:
        km_path = Path(args.from_km)
        if not km_path.exists():
            print(f"❌ File not found: {args.from_km}")
            sys.exit(1)
        urls = extract_paper_urls_from_km(km_path)
        if not urls:
            print("ℹ️  No Paper URLs found in frontmatter.")
            sys.exit(0)
        print(f"Found {len(urls)} Paper URL(s) in {km_path.name}:\n")
        for url, hint in urls:
            print(f"  • {hint}")
            print(f"    {url}")

        # For each URL, try Semantic Scholar to get metadata + better filename
        for i, (url, hint) in enumerate(urls):
            print(f"\n[{i+1}/{len(urls)}] {hint}")
            # Try to get metadata from Semantic Scholar
            arxiv_m = re.search(r"arxiv\.org/(?:abs|pdf)/([\w.]+)", url)
            meta = {"title": hint, "authors": [], "year": None, "pdf_url": url}
            if arxiv_m:
                arxiv_id = arxiv_m.group(1)
                s2_data = api_get(
                    f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}",
                    {"fields": S2_FIELDS}
                )
                if s2_data:
                    meta["title"]   = s2_data.get("title", hint)
                    meta["authors"] = [a.get("name","") for a in s2_data.get("authors",[])]
                    meta["year"]    = s2_data.get("year")

            filename = make_filename(meta["authors"], meta["year"], meta["title"], args.topic)
            local = download_paper(url, args.topic, filename, args.dry_run)
            if local:
                update_index(args.topic, meta, local)
                downloaded.append((url, local))
            if i < len(urls) - 1:
                time.sleep(args.delay)

    # ── Summary ────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"✅ Downloaded {len(downloaded)} paper(s)")
    if downloaded:
        print(f"\n📋 Paste into source_versions frontmatter (YAML bare URL format):")
        for url, path in downloaded:
            uri = path_to_file_uri(path)
            stem = path.stem
            print(f'  - "📖 Paper: {stem} — {uri}"')
    print()


if __name__ == "__main__":
    main()
