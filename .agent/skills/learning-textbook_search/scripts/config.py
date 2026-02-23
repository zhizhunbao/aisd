"""
共享配置：教材注册表、路径、模型参数

所有脚本 import 这个文件获取统一配置
"""

import sys
import os
import re
from pathlib import Path

# ── Windows UTF-8 ─────────────────────────────────────
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── 路径 ──────────────────────────────────────────────
# 脚本在 .shared/skills/learning-textbook_search/scripts/
# 数据在 courses/self-study/
WORKSPACE_ROOT = Path(__file__).resolve().parents[4]  # aisd/
SELF_STUDY_ROOT = WORKSPACE_ROOT / "courses" / "self-study"
DATA_DIR = SELF_STUDY_ROOT / "_search_data"  # 统一存储搜索索引

# ── Ollama 配置 ───────────────────────────────────────
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIM = 768

# ── 分块参数 ──────────────────────────────────────────
CHUNK_SIZE = 1500         # 目标块大小（字符）
CHUNK_OVERLAP = 200       # 重叠大小（字符）
MIN_CHUNK_SIZE = 100      # 太短的并入前一块
BATCH_SIZE = 32           # Ollama 批量请求

# ── RRF 融合参数 ──────────────────────────────────────
RRF_K = 60                # Reciprocal Rank Fusion 常数

# ── 噪声清洗 regex ────────────────────────────────────
NOISE_RE = re.compile(
    r"^\s*\d{1,4}\s*$"             # 纯页码行
    r"|^.{0,5}Draft.{0,15}$"       # Draft 水印
    r"|^\s*©.*$"                    # 版权行
    r"|^\s*Downloaded from.*$"      # 下载声明
    r"|^\s*https?://\S+\s*$",      # 纯 URL 行
    re.MULTILINE | re.IGNORECASE,
)

# 句子分割 regex
SENTENCE_RE = re.compile(r"(?<=[.!?。！？\n])\s+")

# ── 教材注册表 ────────────────────────────────────────
# book_key -> (subject, pdf_name, sections_dir)
BOOKS = {
    # ML (8 books)
    "barber":      ("ml", "barber_brml.pdf",              "barber_sections"),
    "bishop":      ("ml", "bishop_prml.pdf",              "bishop_sections"),
    "esl":         ("ml", "hastie_esl.pdf",               "esl_sections"),
    "goodfellow":  ("ml", "goodfellow_deep_learning.pdf", "goodfellow_sections"),
    "kelleher":    ("ml", "kelleher_ml_fundamentals.pdf", "kelleher_sections"),
    "murphy_pml1": ("ml", "murphy_pml1.pdf",              "murphy_pml1_sections"),
    "murphy_pml2": ("ml", "murphy_pml2.pdf",              "murphy_pml2_sections"),
    "shalev":      ("ml", "shalev-shwartz_uml.pdf",       "shalev_sections"),
    # Math (5 books)
    "mml":         ("math", "deisenroth_mml.pdf",               "mml_sections"),
    "boyd":        ("math", "boyd_convex_optimization.pdf",     "boyd_sections"),
    "mackay":      ("math", "mackay_information_theory.pdf",    "mackay_sections"),
    "grinstead":   ("math", "grinstead_snell_probability.pdf",  "grinstead_sections"),
    "downey":      ("math", "downey_think_stats_2e.pdf",        "downey_sections"),
    # NLP (1 book)
    "jurafsky":    ("nlp", "jurafsky_slp3.pdf",           "jurafsky_sections"),
    # CV (1 book)
    "szeliski":    ("cv",  "szeliski_cv.pdf",             "szeliski_sections"),
    # RL (1 book)
    "sutton":      ("rl",  "sutton_barto_rl_intro.pdf",   "sutton_sections"),
    # Graphs (1 book)
    "hamilton":    ("graphs", "hamilton_grl.pdf",          "hamilton_sections"),
}


def get_sources_dir(book_key: str) -> Path:
    """获取书籍的 _sources 目录"""
    subject = BOOKS[book_key][0]
    return SELF_STUDY_ROOT / subject / "_sources"


def get_sections_dir(book_key: str) -> Path:
    """获取书籍的 sections 目录"""
    subject, _, sections_dir_name = BOOKS[book_key]
    return SELF_STUDY_ROOT / subject / "_sources" / sections_dir_name


def get_pdf_path(book_key: str) -> Path:
    """获取书籍的 PDF 路径"""
    subject, pdf_name, _ = BOOKS[book_key]
    return SELF_STUDY_ROOT / subject / "_sources" / pdf_name
