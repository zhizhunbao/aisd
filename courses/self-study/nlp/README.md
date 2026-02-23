# NLP Self-Study | 自然语言处理自学

---

## Books (1)

| Book | Key | Chapters | Sections |
|------|-----|----------|----------|
| Speech and Language Processing (3rd) | jurafsky | 26 | 235 |

---

## 目录结构

```
nlp/
├── _sources/
│   └── jurafsky_slp3.pdf → jurafsky_sections/
```

每个 `*_sections/` 包含 `toc.json` + `chXX/sec_*.pdf`。

---

## 源文件

### Speech and Language Processing (SLP3)

> **Jurafsky & Martin - NLP 领域"圣经"级教材**

- **版本**: 3rd Edition Draft (2024)
- **官网**: https://web.stanford.edu/~jurafsky/slp3/
- **特点**: 从传统 NLP 到 Transformer/LLM 全覆盖

**主要章节**:

| Part | Topic | Content |
|------|-------|---------|
| I | Large Language Models | Tokenization, N-gram, Neural LM, Transformer |
| II | NLP Applications | NER, Parsing, Sentiment, QA, MT |

---

## 工作流

```bash
# 拆分章节（如需要）
uv run python .shared/skills/dev-pdf_processing/scripts/pdf_split.py \
    _sources/slp3_speech_language_processing.pdf --list-toc

# 生成学习资料
/generate-study-material _sources/slp3_chapter.pdf
```

---

## 参考

- [SLP3 Official](https://web.stanford.edu/~jurafsky/slp3/) — Speech and Language Processing
- [Stanford CS224N](https://web.stanford.edu/class/cs224n/) — NLP with Deep Learning
