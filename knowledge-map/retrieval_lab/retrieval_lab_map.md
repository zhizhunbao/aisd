---
topic: retrieval_lab
dimension: map
created: 2026-03-11
last_verified: 2026-03-11
source_versions:
  - "📚 Book: [manning_intro_to_ir.pdf](../../textbooks/manning_intro_to_ir.pdf) — Ch.1-11"
  - "📚 MinerU: [manning_intro_to_ir.md](../../data/mineru_output/manning_intro_to_ir/manning_intro_to_ir/auto/manning_intro_to_ir.md)"
  - "📖 Docs: [rank_bm25](https://github.com/dorianbrown/rank_bm25)"
  - "📖 Docs: [RRF Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)"
  - "💻 Source: [retrieval_lab](../../retrieval_lab/) — retrievers/*.py"
expiry: 6m
status: current
---

# Retrieval Lab 知识地图

> 📚 Book: Manning et al., [《Introduction to IR》](../../textbooks/manning_intro_to_ir.pdf)

## 1. 核心问题

- **Retrieval Lab 是什么？** → 一个极简的教科书全文检索实验平台，支持 5 种独立检索方法（BM25 词法检索、TOC 目录匹配、PageIndex 结构树匹配、Vector 语义向量检索、Sirchmunk ripgrep-all 全文搜索）+ 1 种融合策略（Ensemble/RRF），可对比评测检索质量
- **为什么不直接用 Elasticsearch / Whoosh？** → 目的是**学习检索原理**而非生产部署；极简代码让每个算法一眼看懂
- **5 种检索方法各有什么特点？** → BM25（概率词法）、TOC（标题匹配）、PageIndex（结构树节点匹配）、Vector（Ollama 嵌入 + 余弦相似度）、Sirchmunk（ripgrep-all 全文 grep）
- **Ensemble 怎么融合多路结果？** → 使用 Reciprocal Rank Fusion (RRF)，无需训练权重，仅依赖排序名次
- **如何衡量检索质量？** → `benchmark.py` 用 Recall@K + P50 延迟评测，支持选择性纳入 Vector 和 Sirchmunk

> 💻 Source: [retrieval_lab](../../retrieval_lab/) `README.md` + `common.py`

---

## 2. 全景位置

```
信息检索 (Information Retrieval)
├── 词法检索 (Lexical Retrieval)
│   ├── 倒排索引 (Inverted Index)
│   │   └── BM25                       ← BM25Retriever
│   ├── 目录匹配 (TOC Matching)         ← TOCRetriever
│   ├── 结构树匹配 (Structure Tree)     ← PageIndexRetriever
│   └── 全文搜索工具 (ripgrep-all)      ← SirchmunkRetriever
├── 语义检索 (Semantic Retrieval)
│   └── 向量检索 (Vector Search)        ← VectorRetriever
├── 混合检索 (Hybrid Retrieval)
│   └── RRF 融合                        ← EnsembleRetriever 【你在这里】
└── 评测 (Evaluation)
    ├── Recall@K
    └── Latency Benchmark               ← benchmark.py
```

> 💻 Source: [retrieval_lab](../../retrieval_lab/) 代码结构 + `README.md`

---

## 3. 依赖地图

```
前置知识                   本主题                      后续方向
┌──────────────────┐  ┌────────────────────────┐  ┌──────────────────────┐
│ Python 基础       │──│                        │──│ RAG Pipeline         │
│ 数据结构          │  │  Retrieval Lab         │  │ (检索增强生成)        │
└──────────────────┘  │                        │  └──────────────────────┘
                      │  独立检索器:            │  ┌──────────────────────┐
┌──────────────────┐  │   BM25 (词法)          │──│ Reranker             │
│ 概率论基础        │──│   TOC  (目录)          │  │ (Neural 重排序)       │
│ (TF-IDF/BM25)    │  │   PageIndex (结构)     │  └──────────────────────┘
└──────────────────┘  │   Vector (语义)        │  ┌──────────────────────┐
                      │   Sirchmunk (grep)     │──│ 生产检索系统         │
┌──────────────────┐  │                        │  │ (Elasticsearch等)    │
│ 教科书 PDF        │──│  融合策略:             │  └──────────────────────┘
│ (MinerU 解析)     │  │   Ensemble (RRF)      │
└──────────────────┘  │                        │
                      │  评测:                  │
┌──────────────────┐  │   Recall@K + P50 延迟  │
│ Ollama 本地推理   │──│                        │
│ (nomic-embed-text)│  └────────────────────────┘
└──────────────────┘
```

> 💻 Source: [retrieval_lab](../../retrieval_lab/) `README.md` + `common.py`

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [retrieval_lab_map.md](retrieval_lab_map.md) | ① 导航 | 首次了解全局 |
| [retrieval_lab_concepts.md](retrieval_lab_concepts.md) | ② 概念 | 查术语定义 |
| [retrieval_lab_math.md](retrieval_lab_math.md) | ③ 公式 | 理解 BM25/RRF/余弦相似度数学 |
| [retrieval_lab_tutorial.md](retrieval_lab_tutorial.md) | ④ 教程 | 第一次使用 |
| [retrieval_lab_code.md](retrieval_lab_code.md) | ⑤ 代码 | 开发参考 |
| [retrieval_lab_pitfalls.md](retrieval_lab_pitfalls.md) | ⑥ 踩坑 | 遇到问题时查 |
| [retrieval_lab_history.md](retrieval_lab_history.md) | ⑦ 历史 | 理解演进脉络 |
| [retrieval_lab_bridge.md](retrieval_lab_bridge.md) | ⑧ 衔接 | 扩展学习 |

> 💻 Source: 本知识库生成结构

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读本文件 `retrieval_lab_map.md` — 了解全局
2. 读 `retrieval_lab_concepts.md` — 掌握核心术语（6 种方法 + 评测指标）
3. 读 `retrieval_lab_math.md` — 理解 BM25、RRF、余弦相似度公式
4. 读 `retrieval_lab_tutorial.md` — 跟着教程跑一遍所有方法
5. 读 `retrieval_lab_code.md` — 看完整代码实现

### 日常参考 🔧

1. 查 `retrieval_lab_code.md` → API 速查表
2. 遇到问题查 `retrieval_lab_pitfalls.md`
3. 忘记公式查 `retrieval_lab_math.md` → 公式速查表

### 深度研究 🔬

1. 查 `retrieval_lab_history.md` — 理解检索技术演进
2. 查 `retrieval_lab_bridge.md` — 找到扩展方向
3. 对比 BM25/TF-IDF/BM25+ 等变体
4. 研究 Vector + BM25 混合检索的效果

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成（含 5 独立方法 + 1 融合策略） |
| Concepts | ✅ 已完成（含 PageIndex/Vector/Sirchmunk） |
| Math | ✅ 已完成（含余弦相似度公式） |
| Tutorial | ✅ 已完成（含 5 种方法 + 融合） |
| Code | ✅ 已完成（8 示例 + API 速查） |
| Pitfalls | ✅ 已完成（10 坑 + 调试清单） |
| History | ✅ 已完成（6 Station） |
| Bridge | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-11 | 6m | ✅ current |
| Concepts | 2026-03-11 | 6m | ✅ current |
| Math | 2026-03-11 | 12m | ✅ current |
| Tutorial | 2026-03-11 | 6m | ✅ current |
| Code | 2026-03-11 | 6m | ✅ current |
| Pitfalls | 2026-03-11 | 6m | ✅ current |
| History | 2026-03-11 | 12m | ✅ current |
| Bridge | 2026-03-11 | 6m | ✅ current |
