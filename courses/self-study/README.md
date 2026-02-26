# Self-Study: AI/ML Classic Textbooks

Personal collection of foundational textbooks for AI/ML self-study.

## Collection Overview

| Domain | Books | Topics |
|--------|-------|--------|
| [ML](#machine-learning) | 8 | Theory, Deep Learning, Probabilistic ML |
| [Math](#mathematics) | 5 | Linear Algebra, Optimization, Probability, Information Theory |
| [NLP](#natural-language-processing) | 1 | Speech & Language Processing |
| [CV](#computer-vision) | 1 | Computer Vision Algorithms |
| [RL](#reinforcement-learning) | 1 | Reinforcement Learning |
| [Graphs](#graph-learning) | 1 | Graph Neural Networks |

**Total: 17 books**

---

## Machine Learning

| Book | Author | Focus | Pages |
|------|--------|-------|-------|
| **Understanding Machine Learning** | Shalev-Shwartz & Ben-David | PAC Learning, VC-Dimension, Theory | ~450 |
| **Pattern Recognition and Machine Learning** | Bishop | Bayesian ML, Graphical Models | ~740 |
| **The Elements of Statistical Learning** | Hastie, Tibshirani, Friedman | Statistical Learning | ~750 |
| **Deep Learning** | Goodfellow, Bengio, Courville | Neural Networks, DL Theory | ~800 |
| **Fundamentals of ML** | Kelleher | Practical ML, CRISP-DM | ~850 |
| **Bayesian Reasoning and ML** | Barber | Bayesian Inference, PGMs | ~700 |
| **Probabilistic ML: An Introduction** | Murphy | Modern Probabilistic ML | ~850 |
| **Probabilistic ML: Advanced Topics** | Murphy | Advanced PML, Deep Generative Models | ~1200 |

### Reading Path
```
Beginner:    Kelleher -> Shalev-Shwartz (theory)
Intermediate: Bishop (Bayesian) or ESL (Statistical)
Advanced:    Murphy PML 1 & 2, Barber
Deep Learning: Goodfellow
```

---

## Mathematics

| Book | Author | Focus |
|------|--------|-------|
| **Mathematics for Machine Learning** | Deisenroth et al. | Linear Algebra, Calculus, Probability |
| **Convex Optimization** | Boyd & Vandenberghe | Optimization Theory |
| **Introduction to Probability** | Grinstead & Snell | Probability Foundations |
| **Think Stats** | Downey | Statistics with Python |
| **Information Theory, Inference, and Learning** | MacKay | Information Theory, Bayesian |

### Reading Path
```
Foundations: MML -> Grinstead (probability)
Statistics:  Think Stats
Optimization: Boyd (essential for DL)
Advanced:    MacKay
```

---

## Natural Language Processing

| Book | Author | Focus |
|------|--------|-------|
| **Speech and Language Processing (3rd ed)** | Jurafsky & Martin | NLP, Computational Linguistics |

---

## Computer Vision

| Book | Author | Focus |
|------|--------|-------|
| **Computer Vision: Algorithms and Applications** | Szeliski | Classical CV, Deep Learning for Vision |

---

## Reinforcement Learning

| Book | Author | Focus |
|------|--------|-------|
| **Reinforcement Learning: An Introduction (2nd ed)** | Sutton & Barto | RL Theory, TD Learning, Policy Gradient |

### Lecture Slides

| Course | Lectures | Source |
|--------|----------|--------|
| **David Silver RL Course (UCL)** | 10 | [YouTube Playlist](https://www.youtube.com/watch?v=2pWv7GOvuf0&list=PLMZdRRhAoLnKFxZlmFoFp0uHVvN2PSE9T) |

---

## Graph Learning

| Book | Author | Focus |
|------|--------|-------|
| **Graph Representation Learning** | Hamilton | GNN, Node Embeddings, Graph Generation |

---

## Directory Structure

```
self-study/
├── ml/_sources/
│   ├── bishop_prml.pdf          → bishop_sections/
│   ├── murphy_pml1.pdf          → murphy_pml1_sections/
│   ├── murphy_pml2.pdf          → murphy_pml2_sections/
│   ├── goodfellow_deep_learning.pdf → goodfellow_sections/
│   ├── kelleher_ml_fundamentals.pdf → kelleher_sections/
│   ├── shalev-shwartz_uml.pdf   → shalev_sections/
│   ├── barber_brml.pdf          → barber_sections/
│   └── hastie_esl.pdf           → esl_sections/
├── math/_sources/
│   ├── deisenroth_mml.pdf       → mml_sections/
│   ├── boyd_convex_optimization.pdf → boyd_sections/
│   ├── mackay_information_theory.pdf → mackay_sections/
│   ├── grinstead_snell_probability.pdf → grinstead_sections/
│   └── downey_think_stats_2e.pdf → downey_sections/
├── nlp/_sources/
│   └── jurafsky_slp3.pdf        → jurafsky_sections/
├── cv/_sources/
│   └── szeliski_cv.pdf          → szeliski_sections/
├── rl/_sources/
│   └── sutton_barto_rl_intro.pdf → sutton_sections/
│   david_silver_lectures/
│   ├── L1-intro_RL.pdf ... L10-games.pdf
└── graphs/_sources/
    └── hamilton_grl.pdf         → hamilton_sections/
```

---

## Split Status

All 17 books have been split into chapters and sections for easier reading:

| Subject | Book | Chapters | Sections |
|---------|------|----------|----------|
| ML | bishop | 14 | 81 |
| ML | murphy_pml1 | 23 | 146 |
| ML | murphy_pml2 | 36 | 215 |
| ML | goodfellow | 20 | 164 |
| ML | kelleher | 18 | 112 |
| ML | shalev | 31 | 189 |
| ML | barber | 28 | 214 |
| ML | esl | 18 | 134 |
| Math | mml | 11 | 78 |
| Math | boyd | 14 | 109 |
| Math | mackay | 50 | 297 |
| Math | grinstead | 12 | 33 |
| Math | downey | 14 | 141 |
| NLP | jurafsky | 26 | 235 |
| CV | szeliski | 18 | 113 |
| RL | sutton | 17 | 155 |
| Graphs | hamilton | 10 | 35 |

**Total: 17 books, 360 chapters, 2,451 sections**

Each `*_sections/` folder contains:
- `toc.json` - Table of contents with page ranges
- `ch*/` - Chapter folders with section PDFs

---

## Topic Index

`topic_index.json` provides keyword→section mapping for quick topic lookup:

| Stat | Value |
|------|-------|
| Topics | 43 |
| References | 327 |

**Top topics by reference count:**
- `inference` (34 refs) - Barber, Bishop, Goodfellow, Murphy...
- `probability` (24 refs) - across 10 books
- `bayesian` (22 refs) - Bishop, Barber, Murphy, MacKay...
- `neural_networks` (16 refs) - Goodfellow, Murphy, Kelleher...
- `optimization` (14 refs) - Boyd, Murphy, Goodfellow...

**Usage in generate-study-material workflow:**
```python
import json
with open('courses/self-study/topic_index.json') as f:
    idx = json.load(f)

# Find all sections about "inference"
refs = idx['topics']['inference']['references']
for r in refs:
    print(f"{r['book']}/{r['chapter']}: {r['title']}")
```

---

## Sources

All books are from official free/open-access sources:

| Book | Source |
|------|--------|
| Bishop PRML | Microsoft Research |
| ESL | Stanford (Hastie) |
| Boyd Convex Optimization | Stanford |
| Murphy PML | GitHub (probml) |
| Barber BRML | UCL |
| Hamilton GRL | McGill |
| MML | mml-book.github.io |
| Jurafsky SLP3 | Stanford |
| Sutton & Barto | incompleteideas.net |
| Szeliski CV | szeliski.org |
