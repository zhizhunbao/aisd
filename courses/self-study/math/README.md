# Math Self-Study | 数学自学

基于经典教材的数学自学资料库。

---

## Books (5)

| Book | Key | Chapters | Sections |
|------|-----|----------|----------|
| Mathematics for Machine Learning | mml | 11 | 78 |
| Convex Optimization | boyd | 14 | 109 |
| Introduction to Probability | grinstead | 12 | 33 |
| Think Stats 2e | downey | 14 | 141 |
| Information Theory, Inference, and Learning | mackay | 50 | 297 |

### Reading Path

```
Foundations: MML -> Grinstead (probability)
Statistics:  Think Stats (Downey)
Optimization: Boyd (essential for DL)
Advanced:    MacKay (information theory)
```

---

## 目录结构

```
math/
├── _sources/
│   ├── deisenroth_mml.pdf                → mml_sections/
│   ├── boyd_convex_optimization.pdf      → boyd_sections/
│   ├── grinstead_snell_probability.pdf   → grinstead_sections/
│   ├── downey_think_stats_2e.pdf         → downey_sections/
│   └── mackay_information_theory.pdf     → mackay_sections/
```

每个 `*_sections/` 包含 `toc.json` + `chXX/sec_*.pdf`。

---

## 参考

- [MML Book](https://mml-book.github.io/)
- [Boyd Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/)
- [MacKay Info Theory](https://www.inference.org.uk/mackay/itila/)
- [Think Stats 2e](https://greenteapress.com/thinkstats2/)
- [Grinstead & Snell](https://math.dartmouth.edu/~prob/prob/prob.pdf)
