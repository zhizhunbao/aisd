---
topic: scikit_learn
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: scikit-learn 1.6 User Guide — https://scikit-learn.org/stable/user_guide.html"
  - "📖 Docs: scikit-learn API Reference — https://scikit-learn.org/stable/modules/classes.html"
  - "💻 Source: scikit-learn/sklearn — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn"
  - "📚 Book: Hastie et al., Elements of Statistical Learning — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., ISLR — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📚 Book: Murphy, PML Vol.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
expiry: 6m
status: current
---

# Scikit-Learn 知识地图

> 📖 Docs: [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
> 💻 Source: [scikit-learn/sklearn](../../../.github/scikit-learn/sklearn/)

## 1. 核心问题

- **Scikit-Learn 在 ML 生态中扮演什么角色？** → Python 机器学习的标准工具库，覆盖分类/回归/聚类/降维/预处理/模型选择，统一 API 设计
- **为什么 sklearn 的 API 设计如此受推崇？** → Estimator 模式：所有模型统一 `fit()` / `predict()` / `transform()` 接口，Pipeline 组合可复用，一学百通
- **sklearn 适合什么场景？不适合什么？** → 适合传统 ML（表格数据、中小规模）；不适合深度学习、大规模在线学习、GPU 计算（用 PyTorch/TF）
- **如何选择正确的算法？** → sklearn 官方提供算法选择流程图（cheat sheet），基于数据量、特征类型、任务类型决策
- **sklearn 的核心模块有哪些？** → 预处理 `preprocessing` → 特征选择 `feature_selection` → 模型 `linear_model/svm/ensemble/...` → 评估 `metrics` → 调参 `model_selection`

> 📖 Docs: [sklearn User Guide](https://scikit-learn.org/stable/user_guide.html)
> 💻 Source: [scikit-learn/sklearn](../../../.github/scikit-learn/sklearn/)

---

## 2. 全景位置

```
Python ML/AI 生态
├── 数据处理 (Data Processing)
│   ├── NumPy (数值计算基础)
│   ├── Pandas (表格数据)
│   └── SciPy (科学计算)
├── 传统机器学习 (Traditional ML) ← 你在这里
│   ├── 【Scikit-Learn】 (统一 API, 分类/回归/聚类/降维/评估/调参)
│   ├── XGBoost / LightGBM (梯度提升树, 竞赛/工业首选)
│   └── statsmodels (统计建模)
├── 深度学习 (Deep Learning)
│   ├── PyTorch (研究导向)
│   ├── TensorFlow / Keras (工业部署)
│   └── JAX (函数式/科学计算)
├── NLP / CV / RL (领域应用)
│   ├── Hugging Face Transformers
│   └── OpenCV
└── 部署 (Deployment)
    ├── ONNX / TorchServe
    └── MLflow / BentoML
```

> 📖 Docs: [sklearn vs Other Tools](https://scikit-learn.org/stable/related_projects.html)

---

## 3. 依赖地图

```
前置知识                     本主题                      后续方向
┌──────────────────┐    ┌────────────────────┐    ┌───────────────────────┐
│ Python 基础      │───→│                    │───→│ XGBoost / LightGBM   │
│ NumPy / Pandas   │───→│   Scikit-Learn     │───→│ 模型部署 (ONNX)      │
│ 线性代数 / 统计  │───→│                    │───→│ 特征工程 (高级)      │
│ ML 基础概念      │───→│                    │───→│ 深度学习 (PyTorch)   │
│ (分类/回归/聚类) │    │                    │───→│ AutoML (H2O, TPOT)   │
└──────────────────┘    └────────────────────┘    └───────────────────────┘
```

> 📖 Docs: [sklearn User Guide](https://scikit-learn.org/stable/user_guide.html)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [scikit_learn_map.md](scikit_learn_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [scikit_learn_concepts.md](scikit_learn_concepts.md) | ② 概念 | 理解 Estimator/Transformer/Pipeline 等核心术语 |
| [scikit_learn_math.md](scikit_learn_math.md) | ③ 公式 | 理解 sklearn 内部算法的数学基础 |
| [scikit_learn_tutorial.md](scikit_learn_tutorial.md) | ④ 教程 | Why-First 理解设计哲学与工作流 |
| [scikit_learn_code.md](scikit_learn_code.md) | ⑤ 代码 | 快速上手实现 |
| [scikit_learn_pitfalls.md](scikit_learn_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [scikit_learn_history.md](scikit_learn_history.md) | ⑦ 历史 | 了解演进 |
| [scikit_learn_bridge.md](scikit_learn_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [scikit_learn_first_principles.md](scikit_learn_first_principles.md) | ⑨ 第一性原理 | 从统计学习理论理解设计决策 |

> 📖 Docs: 本文件汇总

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [scikit_learn_map.md](scikit_learn_map.md) 了解全局位置
2. 读 [scikit_learn_tutorial.md](scikit_learn_tutorial.md) Section 1 理解 sklearn 的设计哲学
3. 读 [scikit_learn_concepts.md](scikit_learn_concepts.md) 掌握 Estimator/Pipeline 等核心术语
4. 跟 [scikit_learn_code.md](scikit_learn_code.md) 快速开始跑一个完整示例
5. 读 [scikit_learn_math.md](scikit_learn_math.md) 理解背后的数学
6. 读 [scikit_learn_history.md](scikit_learn_history.md) 了解演进

### 日常参考 🔧

1. 查 [scikit_learn_code.md](scikit_learn_code.md) API 速查表
2. 查 [scikit_learn_pitfalls.md](scikit_learn_pitfalls.md) 排查问题
3. 查 [scikit_learn_math.md](scikit_learn_math.md) 公式速查

### 深度研究 🔬

1. 读 [scikit_learn_first_principles.md](scikit_learn_first_principles.md) 统计学习理论
2. 读 [scikit_learn_bridge.md](scikit_learn_bridge.md) 探索 XGBoost/PyTorch 等后续
3. 读源码 [sklearn/](../../../.github/scikit-learn/sklearn/)

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
| Map | 2026-03-14 | 6m | ✅ current |
| Concepts | 2026-03-14 | 6m | ✅ current |
| Math | 2026-03-14 | 12m | ✅ current |
| Tutorial | 2026-03-14 | 6m | ✅ current |
| Code | 2026-03-14 | 3m | ✅ current |
| Pitfalls | 2026-03-14 | 6m | ✅ current |
| History | 2026-03-14 | never | ✅ current |
| Bridge | 2026-03-14 | 6m | ✅ current |
| First Principles | 2026-03-14 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [sklearn User Guide](https://scikit-learn.org/stable/user_guide.html) | 📖 文档 | 全文核心参考 |
| [sklearn API Reference](https://scikit-learn.org/stable/modules/classes.html) | 📖 文档 | Code 维度 API 速查 |
| [scikit-learn/sklearn 源码](../../../.github/scikit-learn/sklearn/) | 💻 源码 | Code + Pitfalls |
| [《ESL》](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | Math 维度（算法理论） |
| [《ISLR》](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | Tutorial（入门参考） |
| [《PML》Vol.1](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | Math + First Principles |
