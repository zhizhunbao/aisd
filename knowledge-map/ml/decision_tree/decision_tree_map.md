---
topic: decision_tree
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Hastie et al., ESL Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., ISLR Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📚 Book: Bishop, PRML Ch.14.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, PML1 Ch.18 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: scikit-learn DecisionTree — https://scikit-learn.org/stable/modules/tree.html"
  - "💻 Source: scikit-learn tree/_classes.py — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn/tree/_classes.py"
expiry: 12m
status: current
---

# Decision Tree 知识地图

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8

---

## 1. 核心问题

- **Decision Tree 是什么？** → 一种非参数监督学习模型，通过递归分割特征空间来构建树形决策规则，既可分类也可回归
- **它怎么决定在哪里"切"？** → 遍历所有特征和阈值，选择使不纯度下降最大的分割点（Gini/信息增益/MSE）
- **为什么 Decision Tree 容易过拟合？** → 不加限制时会长到每个叶子只有一个样本（完美拟合训练集），需要剪枝或参数限制
- **CART, ID3, C4.5 有什么区别？** → ID3 用信息增益（偏好多值特征），C4.5 用增益率修正，CART 用 Gini 且只做二叉分割
- **它和 Random Forest / GBDT 是什么关系？** → Decision Tree 是集成方法的基学习器：RF 用 bagging + 随机特征子集，GBDT 用 boosting 逐步修正残差

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8.1

---

## 2. 全景位置

```
机器学习 (Machine Learning)
├── 监督学习 (Supervised Learning)
│   ├── 线性模型
│   │   ├── Linear / Logistic Regression
│   │   └── SVM (线性核)
│   ├── 基于树的模型 ← 你在这里
│   │   ├── 【Decision Tree】 (单棵树，可解释，易过拟合)
│   │   ├── Random Forest (Bagging + 随机特征)
│   │   ├── Gradient Boosting / XGBoost / LightGBM (Boosting)
│   │   └── AdaBoost (加权 Boosting)
│   ├── 概率模型
│   │   ├── Naive Bayes
│   │   └── Logistic Regression (GLM)
│   ├── 距离模型
│   │   ├── KNN
│   │   └── SVM (核方法)
│   └── 神经网络
├── 无监督学习
│   ├── 聚类 (K-Means, DBSCAN)
│   └── 异常检测 (LOF, ISF)
└── 强化学习
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9

---

## 3. 依赖地图

```
前置知识                         本主题                            后续方向
┌──────────────────────────┐    ┌───────────────────────────┐    ┌────────────────────────────┐
│ 信息论 (熵, 信息增益)     │───→│                           │───→│ Random Forest (Bagging)    │
│ 基础统计 (Gini 不纯度)    │───→│                           │───→│ Gradient Boosting (GBDT)   │
│ 递归算法                  │───→│     Decision Tree          │───→│ XGBoost / LightGBM        │
│ 过拟合 / 偏差-方差权衡    │───→│                           │───→│ AdaBoost                  │
│                           │    │                           │───→│ 模型可解释性 (SHAP/LIME)   │
└──────────────────────────┘    └───────────────────────────┘    └────────────────────────────┘
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9-10

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [decision_tree_map.md](decision_tree_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [decision_tree_concepts.md](decision_tree_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [decision_tree_math.md](decision_tree_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [decision_tree_tutorial.md](decision_tree_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [decision_tree_code.md](decision_tree_code.md) | ⑤ 代码 | 快速上手实现 |
| [decision_tree_pitfalls.md](decision_tree_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [decision_tree_history.md](decision_tree_history.md) | ⑦ 历史 | 了解技术演进 |
| [decision_tree_bridge.md](decision_tree_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [decision_tree_first_principles.md](decision_tree_first_principles.md) | ⑨ 第一性原理 | 从公理推导技术必然性 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [decision_tree_map.md](decision_tree_map.md) 了解全局位置
2. 读 [decision_tree_tutorial.md](decision_tree_tutorial.md) Section 1 理解动机
3. 读 [decision_tree_concepts.md](decision_tree_concepts.md) 掌握核心术语
4. 读 [decision_tree_math.md](decision_tree_math.md) 手算一次信息增益
5. 跟 [decision_tree_code.md](decision_tree_code.md) 快速开始跑一个示例
6. 读 [decision_tree_history.md](decision_tree_history.md) 了解 ID3→C4.5→CART 演进

### 日常参考 🔧

1. 查 [decision_tree_code.md](decision_tree_code.md) API 速查表
2. 查 [decision_tree_math.md](decision_tree_math.md) 公式速查
3. 查 [decision_tree_pitfalls.md](decision_tree_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [decision_tree_first_principles.md](decision_tree_first_principles.md) 理解公理根基
2. 读 [decision_tree_history.md](decision_tree_history.md) 完整演进线
3. 读 [decision_tree_bridge.md](decision_tree_bridge.md) 探索 RF/GBDT

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
| Map | 2026-03-14 | 12m | ✅ current |
| Concepts | 2026-03-14 | 12m | ✅ current |
| Math | 2026-03-14 | 12m | ✅ current |
| Tutorial | 2026-03-14 | 12m | ✅ current |
| Code | 2026-03-14 | 6m | ✅ current |
| Pitfalls | 2026-03-14 | 6m | ✅ current |
| History | 2026-03-14 | never | ✅ current |
| Bridge | 2026-03-14 | 12m | ✅ current |
| First Principles | 2026-03-14 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《ESL》Ch.9](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 全文核心：CART 算法、剪枝、不纯度度量 |
| [《ISLR》Ch.8](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | 概念入门、直觉解释、R 代码 |
| [《PRML》Ch.14.4](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 贝叶斯视角、CART 理论 |
| [《PML1》Ch.18](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 现代视角、变量重要性 |
| [Breiman et al. CART 1984](https://doi.org/10.1201/9781315139470) | 📖 论文/书 | History（CART 原始文献） |
| [Quinlan ID3 1986 / C4.5 1993](https://link.springer.com/article/10.1007/BF00116251) | 📖 论文 | History（ID3/C4.5 原始文献） |
| [scikit-learn Decision Tree docs](https://scikit-learn.org/stable/modules/tree.html) | 📖 文档 | Code（API 参考）、Tutorial |
| [scikit-learn tree/_classes.py](../../../.github/scikit-learn/sklearn/tree/_classes.py) | 💻 源码 | Code（实现细节） |
