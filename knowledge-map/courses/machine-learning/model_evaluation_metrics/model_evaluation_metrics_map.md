---
topic: model_evaluation_metrics
dimension: map
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Paper: Fawcett, 'An Introduction to ROC Analysis', Pattern Recognition Letters 2006 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf"
  - "📖 Paper: Kohavi, 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation', IJCAI 1995 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/kohavi_1995_cross_validation_bootstrap.pdf"
  - "📖 Paper: Raschka, 'Model Evaluation, Model Selection, and Algorithm Selection in ML', arXiv 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf"
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., 《An Introduction to Statistical Learning》 Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📖 Docs: scikit-learn Model Evaluation Guide — https://scikit-learn.org/stable/modules/model_evaluation.html"
  - "💻 Source: scikit-learn/sklearn/metrics/ — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/metrics/"
expiry: 12m
status: current
---

# Model Evaluation & Metrics 知识地图

> 📖 Paper: Fawcett, [An Introduction to ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf)
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7

## 1. 核心问题

- **准确率 (Accuracy) 为什么会骗人？** → 在类别不平衡数据上（如 99% 负样本），一个只预测"全负"的模型也能达到 99% 准确率，但它毫无用处
- **Precision 和 Recall 为什么不能兼得？** → 提高阈值可以减少假阳性（Precision↑）但也会漏掉更多正例（Recall↓），这是本质的 trade-off
- **ROC 曲线和 PR 曲线应该用哪个？** → 类别平衡时用 ROC-AUC；严重不平衡时用 PR-AUC，因为 ROC 会高估少数类的分类能力
- **交叉验证解决什么问题？** → 解决训练集和测试集的单次划分"运气好坏"问题，通过多次划分取均值来得到模型泛化能力的可靠估计
- **F1 分数够好吗？何时该用 MCC？** → F1 忽略 True Negatives，在不平衡数据上可能误导；MCC 考虑混淆矩阵全部四格，提供更全面的评价

> 📖 Paper: Fawcett, [An Introduction to ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf)
> 📖 Paper: Chicco & Jurman, [MCC vs F1](../../../.documents/papers/model_evaluation_metrics/chicco_jurman_2020_mcc_vs_f1.pdf)

---

## 2. 全景位置

```
机器学习
├── 数据预处理
│   └── 特征工程、数据清洗、编码
├── 模型训练
│   ├── 监督学习
│   │   ├── 分类 (SVM, NB, DT, KNN...)
│   │   └── 回归 (Linear, Ridge, Lasso...)
│   └── 无监督学习
│       └── 聚类 (K-Means, DBSCAN...)
├── 模型评估与度量 ← 你在这里
│   ├── 【分类指标】 (Accuracy, Precision, Recall, F1, ROC-AUC)
│   ├── 【回归指标】 (MSE, RMSE, MAE, R²)
│   ├── 【聚类指标】 (Silhouette, Davies-Bouldin)
│   ├── 【验证方法】 (K-Fold CV, Bootstrap, Hold-out)
│   └── 【诊断工具】 (学习曲线, 验证曲线, 校准曲线)
├── 超参数调优
│   └── Grid Search, Random Search, Bayesian Opt
└── 模型部署
    └── A/B Testing, Monitoring
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7

---

## 3. 依赖地图

```
前置知识                      本主题                        后续方向
┌─────────────────┐          ┌──────────────────┐          ┌──────────────────────┐
│ 概率论基础       │─────────→│                  │─────────→│ 超参数调优            │
│ (条件概率,       │          │ Model Evaluation │          │ (GridSearchCV 用 CV   │
│  贝叶斯定理)     │          │  & Metrics       │          │  做内层评估)           │
│                  │          │                  │          │                       │
│ 分类/回归模型    │─────────→│ • 混淆矩阵       │─────────→│ 不平衡学习            │
│ (至少了解一个    │          │ • ROC / PR 曲线  │          │ (用 F1/Recall 做      │
│  分类器如何工作) │          │ • 交叉验证       │          │  重采样的评价指标)     │
│                  │          │ • 学习曲线       │          │                       │
│ 线性代数基础     │─────────→│                  │─────────→│ 模型可解释性          │
│ (矩阵运算)      │          │                  │          │ (评估 SHAP 解释的     │
└─────────────────┘          └──────────────────┘          │  可靠性)              │
                                                           └──────────────────────┘
```

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.5
> 📖 Paper: Raschka, [Model Evaluation](../../../.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [model_evaluation_metrics_map.md](model_evaluation_metrics_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [model_evaluation_metrics_concepts.md](model_evaluation_metrics_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [model_evaluation_metrics_math.md](model_evaluation_metrics_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [model_evaluation_metrics_tutorial.md](model_evaluation_metrics_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [model_evaluation_metrics_code.md](model_evaluation_metrics_code.md) | ⑤ 代码 | 快速上手实现 |
| [model_evaluation_metrics_pitfalls.md](model_evaluation_metrics_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [model_evaluation_metrics_history.md](model_evaluation_metrics_history.md) | ⑦ 历史 | 了解技术演进 |
| [model_evaluation_metrics_bridge.md](model_evaluation_metrics_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [model_evaluation_metrics_first_principles.md](model_evaluation_metrics_first_principles.md) | ⑨ 第一性原理 | 追问底层公理、理解边界 |

> 📖 Docs: [scikit-learn Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [model_evaluation_metrics_map.md](model_evaluation_metrics_map.md) 了解全局位置
2. 读 [model_evaluation_metrics_tutorial.md](model_evaluation_metrics_tutorial.md) Section 1 理解动机
3. 读 [model_evaluation_metrics_concepts.md](model_evaluation_metrics_concepts.md) 掌握核心术语
4. 读 [model_evaluation_metrics_math.md](model_evaluation_metrics_math.md) 手算一次混淆矩阵指标
5. 跟 [model_evaluation_metrics_code.md](model_evaluation_metrics_code.md) 快速开始跑一个分类评估
6. 读 [model_evaluation_metrics_history.md](model_evaluation_metrics_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [model_evaluation_metrics_code.md](model_evaluation_metrics_code.md) API 速查表
2. 查 [model_evaluation_metrics_math.md](model_evaluation_metrics_math.md) 公式速查
3. 查 [model_evaluation_metrics_pitfalls.md](model_evaluation_metrics_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [model_evaluation_metrics_history.md](model_evaluation_metrics_history.md) 完整演进线
2. 读 [model_evaluation_metrics_first_principles.md](model_evaluation_metrics_first_principles.md) 追问底层公理
3. 读 [model_evaluation_metrics_bridge.md](model_evaluation_metrics_bridge.md) 探索下游任务
4. 阅读原始论文

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
| Map | 2026-03-18 | 12m | ✅ current |
| Concepts | 2026-03-18 | 12m | ✅ current |
| Math | 2026-03-18 | 12m | ✅ current |
| Tutorial | 2026-03-18 | 12m | ✅ current |
| Code | 2026-03-18 | 6m | ✅ current |
| Pitfalls | 2026-03-18 | 6m | ✅ current |
| History | 2026-03-18 | never | ✅ current |
| Bridge | 2026-03-18 | 12m | ✅ current |
| First Principles | 2026-03-18 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《ESL》Ch.7](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 全文核心参考（偏差-方差分解、CV 理论） |
| [《ISLR》Ch.5](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | 交叉验证、Bootstrap（入门级） |
| [《PML1》Ch.5](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 决策论、损失函数 |
| [《PRML》Ch.1.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 贝叶斯决策论 |
| [Fawcett 2006](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf) | 📖 论文 | ROC 曲线入门（经典） |
| [Kohavi 1995](../../../.documents/papers/model_evaluation_metrics/kohavi_1995_cross_validation_bootstrap.pdf) | 📖 论文 | 交叉验证 vs Bootstrap（经典） |
| [Raschka 2020](../../../.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf) | 📖 论文 | 综合综述（评估、选择、比较） |
| [Chicco & Jurman 2020](../../../.documents/papers/model_evaluation_metrics/chicco_jurman_2020_mcc_vs_f1.pdf) | 📖 论文 | MCC vs F1 对比 |
| [Grandini et al. 2020](../../../.documents/papers/model_evaluation_metrics/grandini_2020_confusion_matrix.pdf) | 📖 论文 | 混淆矩阵完整教程 |
| [Powers 2020](../../../.documents/papers/model_evaluation_metrics/powers_2020_evaluation_precision_recall_fmeasure.pdf) | 📖 论文 | Precision/Recall/F-measure 深度分析 |
| [Flach 2020](../../../.documents/papers/model_evaluation_metrics/flach_2020_precision_recall.pdf) | 📖 论文 | Precision-Recall 曲线分析 |
| [Arlot & Celisse 2010](../../../.documents/papers/model_evaluation_metrics/arlot_celisse_2010_cross_validation.pdf) | 📖 论文 | 交叉验证方法综述 |
| [scikit-learn Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) | 📖 文档 | API 参考、代码实现 |
| [sklearn/metrics/](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/metrics/) | 💻 源码 | 指标实现细节 |
