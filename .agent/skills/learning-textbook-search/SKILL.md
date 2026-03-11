---
name: learning-textbook-search
description: "Textbook Search - 三路混合检索系统，用于从课程教材 PDF 中搜索相关内容。Use when (1) need to quickly find concepts in textbooks, (2) building personal knowledge base, (3) preparing study materials with searchable content, (4) want to query textbook semantically."
---

# SKILL: Textbook Search (教材搜索)

> 三路混合检索系统，用于从课程教材 PDF 中搜索相关内容。

## 概述

本 skill 提供完整的教材搜索流水线，支持三种检索方式和 RRF 融合排序：

| 检索方式 | 原理 | 适合场景 |
|---------|------|---------|
| **Vector** | 语义向量相似度 (Ollama nomic-embed-text, 768d) | 概念性问题、跨语言 |
| **BM25** | 关键词倒排索引 (BM25Okapi) | 精确术语、公式名称 |
| **TOC** | 目录标题模糊匹配 | 章节导航、浏览大纲 |
| **Hybrid** | RRF 融合 (K=60) | 默认模式，综合最优 |

## 架构

```
courses/self-study/
├── {subject}/
│   ├── toc.json                    # 目录结构
│   └── sections/
│       ├── ch01_intro.pdf          # 拆分的章节 PDF
│       └── ...
├── _search_data/                   # 所有索引数据
│   ├── vectors/
│   │   └── {book}_vectors.json     # 向量 + chunk 元数据
│   ├── bm25/
│   │   └── {book}_bm25.pkl        # BM25 倒排索引
│   └── toc_index.json             # 汇总 TOC
```

## 脚本

### 1. `scripts/config.py` — 共享配置

所有脚本共用的配置：路径、参数、书籍注册表。

**关键参数：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `CHUNK_SIZE` | 1500 | 分块大小（字符） |
| `CHUNK_OVERLAP` | 200 | 分块重叠 |
| `CHUNK_MIN` | 100 | 最小分块长度 |
| `EMBED_MODEL` | nomic-embed-text | Ollama 嵌入模型 |
| `RRF_K` | 60 | RRF 融合常数 |

**BOOKS 注册表：** 17 本教材，涵盖 ml / rl / nlp / cv / math 五个学科。

### 2. `scripts/vectorize.py` — 向量化

从教材章节 PDF 提取文本 → 智能分块 → Ollama 嵌入 → 保存向量 JSON。

```bash
# 全部向量化
uv run python .shared/skills/learning-textbook_search/scripts/vectorize.py

# 只处理一本书
uv run python .shared/skills/learning-textbook_search/scripts/vectorize.py --book bishop

# 只处理一个学科
uv run python .shared/skills/learning-textbook_search/scripts/vectorize.py --subject ml
```

**智能分块策略（3 级递归）：**

```
原始文本
  ├─ Level 1: 按段落分割 (\n\n)
  │   ├─ 段落 < chunk_size → 直接使用
  │   └─ 段落 > chunk_size
  │       ├─ Level 2: 按句子分割 ([.!?]\s+)
  │       │   ├─ 合并短句至 chunk_size
  │       │   └─ 单句 > chunk_size
  │       │       └─ Level 3: 按词边界硬切 + 重叠
  │       └─ 相邻段落不足 min_size 时合并
  └─ 添加语义前缀: "[Book | Chapter] "
```

### 3. `scripts/build_index.py` — 构建 BM25 + TOC 索引

从向量 JSON 中提取文本构建 BM25 索引，从 toc.json 汇总目录索引。

```bash
# 构建全部索引
uv run python .shared/skills/learning-textbook_search/scripts/build_index.py

# 只处理一本书
uv run python .shared/skills/learning-textbook_search/scripts/build_index.py --book sutton
```

**前提：** 需要先运行 `vectorize.py` 生成向量 JSON。

### 4. `scripts/search.py` — 混合搜索

三路混合搜索引擎，支持单次查询和交互模式。

```bash
# 默认 hybrid 搜索
uv run python .shared/skills/learning-textbook_search/scripts/search.py "SVM kernel trick"

# 指定模式
uv run python .shared/skills/learning-textbook_search/scripts/search.py --mode bm25 "gradient descent"
uv run python .shared/skills/learning-textbook_search/scripts/search.py --mode toc "reinforcement"

# 限定书籍
uv run python .shared/skills/learning-textbook_search/scripts/search.py --book bishop "Bayesian"

# 交互模式
uv run python .shared/skills/learning-textbook_search/scripts/search.py -i
```

**交互模式命令：**

| 命令 | 说明 |
|------|------|
| `/mode vector\|bm25\|toc\|hybrid` | 切换搜索模式 |
| `/book <key>\|all` | 限定/取消限定书籍 |
| `/quit` | 退出 |

## RRF 融合原理

Reciprocal Rank Fusion 将多路检索结果合并排序：

$$score(d) = \sum_{i=1}^{n} \frac{1}{K + rank_i(d)}$$

- $K = 60$（常数，降低高排名的权重集中度）
- 每路检索独立排名后融合
- 多路命中的文档分数叠加，排名更高

## 依赖

```
pymupdf     # PDF 文本提取
httpx       # Ollama API 调用
numpy       # 向量计算
rank-bm25   # BM25 关键词搜索
```

**外部依赖：** Ollama + nomic-embed-text 模型

```bash
# 安装依赖
uv add rank-bm25

# 确保 Ollama 模型可用
ollama pull nomic-embed-text
```

## 完整流水线

```bash
# Step 1: 向量化所有教材（首次，耗时较长）
uv run python .shared/skills/learning-textbook_search/scripts/vectorize.py

# Step 2: 构建 BM25 + TOC 索引（秒级）
uv run python .shared/skills/learning-textbook_search/scripts/build_index.py

# Step 3: 搜索
uv run python .shared/skills/learning-textbook_search/scripts/search.py -i
```

## Copilot 集成

在生成学习材料时，Copilot 可以调用搜索脚本获取教材参考：

```bash
# 搜索相关内容
uv run python .shared/skills/learning-textbook_search/scripts/search.py "topic keywords"
```

将搜索结果整合到笔记的 `📖 教材深入` 部分，提供：
- 具体教材名称和章节
- 核心概念的深入解释
- 与课件内容的关联说明

## 已注册教材 (17 本)

| Key | 学科 | 教材 |
|-----|------|------|
| bishop | ml | Pattern Recognition & ML (Bishop) |
| esl | ml | Elements of Statistical Learning |
| isl | ml | Intro to Statistical Learning |
| murphy | ml | Probabilistic ML (Murphy) |
| sutton | rl | Reinforcement Learning (Sutton & Barto) |
| bertsekas | rl | Reinforcement Learning & Optimal Control |
| jurafsky | nlp | Speech & Language Processing |
| eisenstein | nlp | Intro to NLP |
| tunstall | nlp | NLP with Transformers |
| prince | cv | Computer Vision (Prince) |
| szeliski | cv | Computer Vision: Algorithms & Applications |
| goodfellow | ml | Deep Learning (Goodfellow) |
| mackay | ml | Info Theory, Inference & Learning |
| barber | ml | Bayesian Reasoning & ML |
| strang_la | math | Linear Algebra (Strang) |
| strang_calc | math | Calculus (Strang) |
| boyd | math | Convex Optimization (Boyd) |
