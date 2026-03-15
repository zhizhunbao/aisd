---
topic: logistic_regression
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Cox, 'The Regression Analysis of Binary Sequences', JRSS-B 1958 — https://doi.org/10.1111/j.2517-6161.1958.tb00292.x"
  - "📚 Book: Hastie et al., ESL Ch.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., ISLR Ch.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📚 Book: Bishop, PRML Ch.4.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, PML1 Ch.10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: scikit-learn LogisticRegression — https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression"
  - "💻 Source: scikit-learn _logistic.py — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn/linear_model/_logistic.py"
expiry: 12m
status: current
---

# Logistic Regression 知识地图

> 📖 Paper: Cox, [The Regression Analysis of Binary Sequences](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x), JRSS-B 1958
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.4

---

## 1. 核心问题

- **Logistic Regression 是什么？** → 一种广义线性模型，用 sigmoid 函数将线性组合映射到 [0,1] 概率，解决二分类（可扩展到多分类）问题
- **它和 Linear Regression 有什么区别？** → Linear Regression 输出连续值，Logistic Regression 通过 logit 链接函数输出类别概率，损失函数是交叉熵而非 MSE
- **为什么叫 "Regression" 但实际是分类器？** → 因为它回归的是**对数几率 (log-odds)**，是 GLM 框架下的回归模型，决策边界是线性的
- **什么时候该用 Logistic Regression？** → 需要概率输出、特征与 log-odds 近似线性、可解释性要求高、baseline 模型
- **多分类怎么办？** → 二分类用 sigmoid，多分类用 softmax（Multinomial LR），或 One-vs-Rest

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.4.3

---

## 2. 全景位置

```
机器学习 (Machine Learning)
├── 监督学习 (Supervised Learning)
│   ├── 回归 (Regression)
│   │   ├── Linear Regression (连续输出)
│   │   └── Polynomial Regression
│   ├── 分类 (Classification) ← 你在这里
│   │   ├── 线性分类器
│   │   │   ├── 【Logistic Regression】 (概率输出 + 线性决策边界)
│   │   │   ├── Linear Discriminant Analysis (生成式)
│   │   │   └── Perceptron (无概率输出)
│   │   ├── SVM (最大间隔)
│   │   ├── KNN (距离投票)
│   │   ├── Naive Bayes (生成式)
│   │   └── 决策树 / 随机森林 / 集成方法
│   └── 广义线性模型 (GLM)
│       ├── Logistic Regression (binomial + logit link)
│       ├── Poisson Regression (count + log link)
│       └── Probit Regression (binomial + probit link)
├── 无监督学习
└── 强化学习
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.1
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10.1

---

## 3. 依赖地图

```
前置知识                         本主题                            后续方向
┌──────────────────────────┐    ┌───────────────────────────┐    ┌────────────────────────────┐
│ Linear Regression        │───→│                           │───→│ Neural Networks (单层=LR)  │
│ 概率论 (Bayes 定理)       │───→│                           │───→│ Softmax Regression (多分类) │
│ 最大似然估计 (MLE)        │───→│   Logistic Regression     │───→│ GLM 家族 (Poisson等)       │
│ 梯度下降 / 优化理论       │───→│                           │───→│ SVM (对比理解)             │
│ 线性代数 (矩阵运算)       │───→│                           │───→│ 正则化 (L1/L2 → 特征选择)  │
└──────────────────────────┘    └───────────────────────────┘    └────────────────────────────┘
```

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.3
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.5.7

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [logistic_regression_map.md](logistic_regression_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [logistic_regression_concepts.md](logistic_regression_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [logistic_regression_math.md](logistic_regression_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [logistic_regression_tutorial.md](logistic_regression_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [logistic_regression_code.md](logistic_regression_code.md) | ⑤ 代码 | 快速上手实现 |
| [logistic_regression_pitfalls.md](logistic_regression_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [logistic_regression_history.md](logistic_regression_history.md) | ⑦ 历史 | 了解技术演进 |
| [logistic_regression_bridge.md](logistic_regression_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [logistic_regression_first_principles.md](logistic_regression_first_principles.md) | ⑨ 第一性原理 | 从公理推导技术必然性 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [logistic_regression_map.md](logistic_regression_map.md) 了解全局位置
2. 读 [logistic_regression_tutorial.md](logistic_regression_tutorial.md) Section 1 理解动机
3. 读 [logistic_regression_concepts.md](logistic_regression_concepts.md) 掌握核心术语
4. 读 [logistic_regression_math.md](logistic_regression_math.md) 手算一次核心公式
5. 跟 [logistic_regression_code.md](logistic_regression_code.md) 快速开始跑一个示例
6. 读 [logistic_regression_history.md](logistic_regression_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [logistic_regression_code.md](logistic_regression_code.md) API 速查表
2. 查 [logistic_regression_math.md](logistic_regression_math.md) 公式速查
3. 查 [logistic_regression_pitfalls.md](logistic_regression_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [logistic_regression_first_principles.md](logistic_regression_first_principles.md) 理解公理根基
2. 读 [logistic_regression_history.md](logistic_regression_history.md) 完整演进线
3. 读 [logistic_regression_bridge.md](logistic_regression_bridge.md) 探索下游任务
4. 阅读 Cox 1958 原始论文

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
| [《ESL》Ch.4](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 全文核心参考：理论推导、公式、方法对比 |
| [《ISLR》Ch.4](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | 概念入门、直觉解释、R 代码示例 |
| [《PRML》Ch.4.3](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 贝叶斯视角、IRLS 推导、概率框架 |
| [《PML1》Ch.10](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 现代视角、正则化、多分类 |
| [《Deep Learning》Ch.5.7](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | LR 作为最简单神经网络的理解 |
| [《MML》Ch.12.2](../../../textbooks/deisenroth_mml.pdf) | 📚 教科书 | 数学基础推导 |
| [Cox 1958](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x) | 📖 论文 | History（原始论文） |
| [scikit-learn docs](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression) | 📖 文档 | Code（API 参考）、Tutorial（使用指南） |
| [scikit-learn _logistic.py](../../../.github/scikit-learn/sklearn/linear_model/_logistic.py) | 💻 源码 | Code（实现细节）、Pitfalls（源码级理解） |
