---
topic: naive_bayes
dimension: map
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Raschka, 'Naive Bayes and Text Classification I', arXiv 2014 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf"
  - "📖 Paper: Vidhya & Aghila, 'A Survey of Naive Bayes in Text Document Classification', arXiv 2010 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf"
  - "📚 Book: Murphy, 《Probabilistic Machine Learning: An Introduction》 Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.6.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Docs: scikit-learn Naive Bayes User Guide — https://scikit-learn.org/stable/modules/naive_bayes.html"
  - "💻 Source: scikit-learn/sklearn/naive_bayes.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/naive_bayes.py"
expiry: 12m
status: current
---

# Naive Bayes 知识地图

> 📖 Paper: Raschka, [Naive Bayes and Text Classification I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf)
> 📚 Book: Murphy, [《Probabilistic Machine Learning: An Introduction》](../../../textbooks/murphy_pml1.pdf), Ch.9

## 1. 核心问题

- **为什么朴素贝叶斯"朴素"？** → 它假设特征在给定类别下条件独立，这个假设在现实中几乎不成立，但大幅简化了计算
- **朴素贝叶斯如何做分类？** → 用贝叶斯定理从先验 P(y) 和似然 P(x|y) 推导后验 P(y|x)，取后验最大类别（MAP）
- **拉普拉斯平滑解决什么问题？** → 解决训练集中未出现的特征组合导致似然为零（零频率问题），令整个分类器崩溃
- **Gaussian NB 和 Multinomial NB 的根本区别？** → 似然建模方式不同：Gaussian 用正态分布建模连续特征；Multinomial 用多项分布建模离散计数
- **为什么朴素贝叶斯仍被广泛使用？** → 训练极快（O(nd)）、增量学习、高维稀疏数据效果好（文本分类）、输出概率可解释

> 📖 Paper: Raschka, [Naive Bayes and Text Classification I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf)
> 📖 Docs: [scikit-learn Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)

---

## 2. 全景位置

```
机器学习
├── 监督学习
│   ├── 分类
│   │   ├── 判别模型 (Discriminative)
│   │   │   ├── Logistic Regression  (直接建模 P(y|x))
│   │   │   └── SVM                  (找最大间隔超平面)
│   │   └── 生成模型 (Generative)  ← 你在这里
│   │       ├── 【Naive Bayes】      (条件独立假设 + 贝叶斯推断)
│   │       ├── LDA/QDA              (高斯判别分析，不做独立假设)
│   │       └── HMM                  (序列生成模型)
│   └── 回归
│       └── 线性回归, 岭回归...
└── 无监督学习
    └── K-Means, DBSCAN, LOF...
```

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.1 — 生成模型 vs 判别模型

---

## 3. 依赖地图

```
前置知识                      Naive Bayes                     后续方向
┌─────────────────┐          ┌──────────────────┐          ┌──────────────────────┐
│ 贝叶斯定理       │─────────→│                  │─────────→│ 文本分类/垃圾邮件过滤  │
│ 条件概率         │─────────→│   Naive Bayes    │─────────→│ 情感分析              │
│ 最大似然估计(MLE)│─────────→│  (生成式分类器)  │─────────→│ 贝叶斯网络（放宽独立） │
│ 概率分布         │─────────→│                  │─────────→│ LDA 主题模型          │
│  (正态/多项/     │          │ MAP 决策规则:     │          │ 朴素贝叶斯在线学习     │
│   伯努利)        │          │ argmax P(y|x)    │          └──────────────────────┘
└─────────────────┘          └──────────────────┘
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.6.6

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [naive_bayes_map.md](naive_bayes_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [naive_bayes_concepts.md](naive_bayes_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [naive_bayes_math.md](naive_bayes_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [naive_bayes_tutorial.md](naive_bayes_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [naive_bayes_code.md](naive_bayes_code.md) | ⑤ 代码 | 快速上手实现 |
| [naive_bayes_pitfalls.md](naive_bayes_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [naive_bayes_history.md](naive_bayes_history.md) | ⑦ 历史 | 了解技术演进 |
| [naive_bayes_bridge.md](naive_bayes_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [naive_bayes_first_principles.md](naive_bayes_first_principles.md) | ⑨ 第一性原理 | 理解算法必然性 |

> 📖 Docs: [scikit-learn Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [naive_bayes_map.md](naive_bayes_map.md) 了解全局位置
2. 读 [naive_bayes_tutorial.md](naive_bayes_tutorial.md) Section 1 理解动机
3. 读 [naive_bayes_concepts.md](naive_bayes_concepts.md) 掌握核心术语
4. 读 [naive_bayes_math.md](naive_bayes_math.md) 手算一次 MAP 分类
5. 跟 [naive_bayes_code.md](naive_bayes_code.md) 快速开始跑一个示例
6. 读 [naive_bayes_history.md](naive_bayes_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [naive_bayes_code.md](naive_bayes_code.md) API 速查表
2. 查 [naive_bayes_math.md](naive_bayes_math.md) 公式速查
3. 查 [naive_bayes_pitfalls.md](naive_bayes_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [naive_bayes_history.md](naive_bayes_history.md) 完整演进线
2. 读 [naive_bayes_bridge.md](naive_bayes_bridge.md) 探索下游任务
3. 读 [naive_bayes_first_principles.md](naive_bayes_first_principles.md) 理解公理假设

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-13 | 12m | ✅ current |
| Concepts | 2026-03-13 | 12m | ✅ current |
| Math | 2026-03-13 | 12m | ✅ current |
| Tutorial | 2026-03-13 | 12m | ✅ current |
| Code | 2026-03-13 | 6m | ✅ current |
| Pitfalls | 2026-03-13 | 6m | ✅ current |
| History | 2026-03-13 | never | ✅ current |
| Bridge | 2026-03-13 | 12m | ✅ current |
| First Principles | 2026-03-13 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [《PML1》Ch.9](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 全文核心参考（贝叶斯推断框架、各变体数学） |
| [《ESL》Ch.6.6](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 判别分析对比、LDA 关联 |
| [Raschka 2014](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf) | 📖 论文 | Tutorial、History（文本分类应用） |
| [Vidhya & Aghila 2010](../../../.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf) | 📖 论文 | Pitfalls、Bridge（综述对比） |
| [scikit-learn NB Guide](https://scikit-learn.org/stable/modules/naive_bayes.html) | 📖 官方文档 | Code、API 速查 |
| [sklearn/naive_bayes.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/naive_bayes.py) | 💻 源码 | GaussianNB/MultinomialNB/BernoulliNB 实现细节 |
