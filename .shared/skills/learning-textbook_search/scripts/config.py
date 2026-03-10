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
WORKSPACE_ROOT = Path(__file__).resolve().parents[4]  # aisd/
SELF_STUDY_ROOT = WORKSPACE_ROOT / "textbooks"
DATA_DIR = WORKSPACE_ROOT / "retrieval_lab" / "data" / "search_data"  # 搜索索引输出
# MinerU 转换输出目录（每本书已提取文本 + 图片 + 结构索引）
MINERU_ROOT = WORKSPACE_ROOT / "data" / "mineru_output"

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
# book_key -> (subject, mineru_dir_name)
# mineru_dir_name 对应 data/mineru_output/{mineru_dir}/{mineru_dir}/auto/ 中的内容
BOOKS = {
    # ── ML (9 books) ──────────────────────────────────
    "barber":      ("ml",     "barber_brml"),
    "bishop":      ("ml",     "bishop_prml"),
    "esl":         ("ml",     "hastie_esl"),
    "goodfellow":  ("ml",     "goodfellow_deep_learning"),
    "isl":         ("ml",     "james_ISLR"),
    "kelleher":    ("ml",     "kelleher_ml_fundamentals"),
    "murphy_pml1": ("ml",     "murphy_pml1"),
    "murphy_pml2": ("ml",     "murphy_pml2"),
    "shalev":      ("ml",     "shalev-shwartz_uml"),
    # ── Math (6 books) ────────────────────────────────
    "mml":         ("math",   "deisenroth_mml"),
    "boyd":        ("math",   "boyd_convex_optimization"),
    "mackay":      ("math",   "mackay_information_theory"),
    "grinstead":   ("math",   "grinstead_snell_probability"),
    "downey_stats":("math",   "downey_think_stats_2e"),
    "downey_cs":   ("math",   "downey_how_to_think_like_cs"),
    # ── NLP (3 books) ─────────────────────────────────
    "jurafsky":    ("nlp",    "jurafsky_slp3"),
    "eisenstein":  ("nlp",    "eisenstein_nlp"),
    "manning_ir":  ("nlp",    "manning_intro_to_ir"),
    # ── CV (1 book) ───────────────────────────────────
    "szeliski":    ("cv",     "szeliski_cv"),
    # ── RL (1 book) ───────────────────────────────────
    "sutton":      ("rl",     "sutton_barto_rl_intro"),
    # ── Graphs (1 book) ───────────────────────────────
    "hamilton":    ("graphs", "hamilton_grl"),
    # ── Python (7 books) ──────────────────────────────
    "beazley":     ("python", "beazley_python_cookbook"),
    "downey_py":   ("python", "downey_think_python_2e"),
    "fluent_py":   ("python", "ramalho_fluent_python"),
    "okken":       ("python", "okken_python_testing_pytest"),
    "percival":    ("python", "percival_cosmic_python"),
    "fastapi":     ("python", "lubanovic_fastapi_modern_web"),
    "black_hat":   ("python", "seitz_black_hat_python"),
    # ── JavaScript (8 books) ──────────────────────────
    "flanagan_js": ("js",     "flanagan_js_definitive_guide"),
    "haverbeke":   ("js",     "haverbeke_eloquent_javascript"),
    "ydkjs_up":    ("js",     "simpson_ydkjs_up_going"),
    "ydkjs_scope": ("js",     "simpson_ydkjs_scope_closures"),
    "ydkjs_this":  ("js",     "simpson_ydkjs_this_object_prototypes"),
    "ydkjs_types": ("js",     "simpson_ydkjs_types_grammar"),
    "ydkjs_async": ("js",     "simpson_ydkjs_async_performance"),
    "ydkjs_es6":   ("js",     "simpson_ydkjs_es6_beyond"),
    # ── TypeScript (1 book) ───────────────────────────
    "basarat_ts":  ("ts",     "basarat_typescript_deep_dive"),
    # ── Algorithms (1 book) ───────────────────────────
    "clrs":        ("algo",   "cormen_CLRS"),
    # ── Software Engineering (9 books) ────────────────
    "clean_code":  ("se",     "martin_clean_code"),
    "clean_arch":  ("se",     "martin_clean_architecture"),
    "ddia":        ("se",     "kleppmann_ddia"),
    "gof":         ("se",     "gof_design_patterns"),
    "refactoring": ("se",     "fowler_refactoring"),
    "pragmatic":   ("se",     "hunt_pragmatic_programmer"),
    "web_scale":   ("se",     "ejsmont_web_scalability"),
    "release_it":  ("se",     "nygard_release_it"),
    # ── DevOps (3 books) ──────────────────────────────
    "pro_git":     ("devops", "chacon_pro_git"),
    "sre":         ("devops", "google_sre"),
    "swe":         ("devops", "google_swe"),
    # ── Security (4 books) ────────────────────────────
    "binary":      ("sec",    "andriesse_practical_binary_analysis"),
    "cryptography":("sec",    "aumasson_serious_cryptography"),
    "tangled_web": ("sec",    "zalewski_tangled_web"),
    # ── Networking (2 books) ──────────────────────────
    "http":        ("net",    "gourley_http_definitive_guide"),
    "ssh":         ("net",    "barrett_ssh_definitive_guide"),
    # ── Database / Frameworks (2 books) ───────────────
    "sqlite":      ("db",     "kreibich_using_sqlite"),
    "postgresql":  ("db",     "fontaine_art_of_postgresql"),
    # ── UX / Design (2 books) ─────────────────────────
    "dont_think":  ("ux",     "krug_dont_make_me_think"),
    "design_things":("ux",    "norman_design_everyday_things"),
}


def get_mineru_auto_dir(book_key: str) -> Path:
    """获取 mineru auto 输出目录：data/mineru_output/{dir}/{dir}/auto/"""
    d = BOOKS[book_key][1]
    return MINERU_ROOT / d / d / "auto"


def get_mineru_content_list(book_key: str) -> Path:
    """获取 mineru 结构化索引 JSON（含 text/image/equation/table 条目 + 页码）"""
    d = BOOKS[book_key][1]
    return get_mineru_auto_dir(book_key) / f"{d}_content_list.json"


def get_mineru_md(book_key: str) -> Path:
    """获取 mineru 转换的完整 Markdown 文件"""
    d = BOOKS[book_key][1]
    return get_mineru_auto_dir(book_key) / f"{d}.md"


def get_mineru_images_dir(book_key: str) -> Path:
    """获取 mineru 提取的图片目录（图片名为内容 hash）"""
    return get_mineru_auto_dir(book_key) / "images"


# search.py 兼容别名
OLLAMA_BASE = OLLAMA_URL
