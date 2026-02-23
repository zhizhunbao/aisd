# ML Self-Study | 机器学习自学

基于经典教材的自学资料库。

---

## Books (8)

| Book | Key | Chapters | Sections |
|------|-----|----------|----------|
| Understanding Machine Learning | shalev | 31 | 189 |
| Pattern Recognition and ML | bishop | 14 | 81 |
| Elements of Statistical Learning | esl | 18 | 134 |
| Deep Learning | goodfellow | 20 | 164 |
| Fundamentals of ML | kelleher | 18 | 112 |
| Bayesian Reasoning and ML | barber | 28 | 214 |
| Probabilistic ML: Introduction | murphy_pml1 | 23 | 146 |
| Probabilistic ML: Advanced | murphy_pml2 | 36 | 215 |

### Reading Path

```
Beginner:    Kelleher -> Shalev-Shwartz (theory)
Intermediate: Bishop (Bayesian) or ESL (Statistical)
Advanced:    Murphy PML 1 & 2, Barber
Deep Learning: Goodfellow
```

---

## 目录结构

```
ml/
├── _sources/                              # 原始 PDF + 拆分脚本
│   ├── shalev-shwartz_uml.pdf            → shalev_sections/
│   ├── bishop_prml.pdf                   → bishop_sections/
│   ├── hastie_esl.pdf                    → esl_sections/
│   ├── goodfellow_deep_learning.pdf      → goodfellow_sections/
│   ├── kelleher_ml_fundamentals.pdf      → kelleher_sections/
│   ├── barber_brml.pdf                   → barber_sections/
│   ├── murphy_pml1.pdf                   → murphy_pml1_sections/
│   └── murphy_pml2.pdf                   → murphy_pml2_sections/
```

每个 `*_sections/` 包含 `toc.json` + `chXX/sec_*.pdf`。
