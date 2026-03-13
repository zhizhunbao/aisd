---
topic: svm
dimension: map
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Cortes & Vapnik ML 1995 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/svm/cortes_vapnik_1995_svm.pdf"
  - "📖 Paper: Boser Guyon Vapnik COLT 1992 — https://doi.org/10.1145/130385.130401"
  - "📚 Book: Hastie et al., ESL Ch.12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md"
  - "📚 Book: Bishop, PRML Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md"
  - "📖 Docs: scikit-learn SVM User Guide — https://scikit-learn.org/stable/modules/svm.html"
  - "💻 Source: sklearn svm/_classes.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/svm/_classes.py"
expiry: 12m
status: current
---

# SVM 知识地图

> 📚 Book: Hastie et al., [ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md), Springer 2009
> 📚 Book: Bishop, [PRML Ch.7](../../../data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md), Springer 2006

---

## 1. 核心问题

- **SVM 解决什么问题？** → 在高维特征空间中找到**最大间隔超平面**，将两类样本以最大安全边距分开
- **为什么最大化间隔？** → 间隔越大 VC 维上界越小 → 泛化误差上界更紧 → 更不容易过拟合
- **线性不可分怎么办？** → 引入松弛变量 $\xi_i$ 允许误分，用参数 C 控制惩罚力度（软间隔 SVM）
- **如何做非线性分类？** → **核技巧**：用 $K(x,x')=\langle h(x),h(x')\rangle$ 隐式映射到高维空间，无需显式计算映射
- **什么是支持向量？** → 对偶解中 $\hat{\alpha}_i > 0$ 的样本点，唯一决定超平面，其他点删除不影响结果

> 📚 Book: Hastie ESL, Sec.12.1 (Introduction) + Sec.12.2 (Support Vector Classifier)

---

## 2. 全景位置

```
监督学习
├── 线性分类
│   ├── 感知机 (Perceptron)         (任意分离超平面，不唯一)
│   ├── 逻辑回归 (Logistic Reg.)    (最大化对数似然，输出概率)
│   ├── LDA                         (类条件高斯假设，Bayes 最优)
│   └── SVM 线性                    ← 你在这里
│       ├── 【SVM 线性】             (最大间隔超平面，稀疏支持向量)
│       └── Kernel SVM              (核技巧：RBF / Poly / Sigmoid)
├── 回归
│   └── SVR                         (ε-不敏感损失，SVM 回归版本)
└── 异常检测
    └── One-Class SVM               (无监督，仅用正样本估计边界)
```

> 📖 Paper: Cortes & Vapnik, [Support-Vector Networks](../../../.documents/papers/svm/cortes_vapnik_1995_svm.pdf), ML 1995



---

## 3. 依赖地图

```
前置知识                              SVM                           后续方向
┌─────────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│ 超平面几何           │──────→│                      │──────→│ Kernel 方法          │
│ 拉格朗日乘子法       │──────→│   SVM                │──────→│ 高斯过程 (GP)        │
│ 凸二次规划 (QP)     │──────→│   ├─ 硬间隔（可分）  │──────→│ SVR（回归）          │
│ KKT 条件            │──────→│   ├─ 软间隔 + C      │──────→│ One-Class SVM        │
│ 内积与核函数         │──────→│   └─ Kernel Trick    │──────→│ 结构风险最小化 (SRM) │
└─────────────────────┘       └──────────────────────┘       └──────────────────────┘
```

> 📚 Book: Hastie ESL Sec.4.5.2 (Optimal Separating Hyperplane) → Sec.12.2 → Sec.12.3

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [svm_map.md](svm_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [svm_concepts.md](svm_concepts.md) | ② 概念 | 理解超平面/间隔/支持向量/核函数/软间隔等术语 |
| [svm_math.md](svm_math.md) | ③ 公式 | 原始问题→对偶推导→KKT→核技巧→SVR 完整公式 |
| [svm_tutorial.md](svm_tutorial.md) | ④ 教程 | Why-First：为什么最大间隔？核怎么选？C/γ 怎么调 |
| [svm_code.md](svm_code.md) | ⑤ 代码 | sklearn SVC/SVR 上手示例，C/γ 搜索，决策边界可视化 |
| [svm_pitfalls.md](svm_pitfalls.md) | ⑥ 踩坑 | 忘记标准化、C/γ 混淆、核选错、大数据集慢 |
| [svm_history.md](svm_history.md) | ⑦ 历史 | 感知机→VC理论→硬间隔→软间隔→核SVM→现代应用 |
| [svm_bridge.md](svm_bridge.md) | ⑧ 衔接 | 上游逻辑回归，下游核方法/深度学习，与 DBSCAN 对比 |

> 📚 Book: Hastie ESL Ch.12; Bishop PRML Ch.7

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [svm_map.md](svm_map.md) 了解全局位置
2. 读 [svm_tutorial.md](svm_tutorial.md) Section 1 理解动机（为什么最大化间隔）
3. 读 [svm_concepts.md](svm_concepts.md) 掌握核心术语（超平面/间隔/支持向量/核/松弛变量）
4. 读 [svm_math.md](svm_math.md) 手算一次：原始 QP → 对偶推导 → 核替换
5. 跟 [svm_code.md](svm_code.md) 快速开始：sklearn SVC 分类 + 可视化决策边界
6. 读 [svm_history.md](svm_history.md) 了解 SVM 在 ML 历史中的地位

### 日常参考 🔧

1. 查 [svm_code.md](svm_code.md) API 速查（SVC/SVR/LinearSVC 参数表）
2. 查 [svm_math.md](svm_math.md) 公式速查（对偶、核函数、铰链损失）
3. 查 [svm_pitfalls.md](svm_pitfalls.md) 排查问题（标准化、C/γ 调参、内存问题）

### 深度研究 🔬

1. 读 [svm_history.md](svm_history.md) 完整演进线（Vapnik 1963 → 现代 libsvm）
2. 读 [svm_bridge.md](svm_bridge.md) 探索 Kernel 方法、高斯过程、现代对比
3. 阅读原始文献：[Hastie ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md) + [Boser et al. 1992 (kernel SVM)](https://doi.org/10.1145/130385.130401)

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

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [Hastie ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md) | 📚 教科书 | 全文核心：SVC, Kernel SVM, SVR, 铰链损失, SRM 关系 |
| [Bishop PRML Ch.7](../../../data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md) | 📚 教科书 | Concepts + Math：对偶推导, 概率输出, RVM 对比 |
| [sklearn SVM Docs](https://scikit-learn.org/stable/modules/svm.html) | 📖 文档 | Code + Pitfalls：API 用法，参数说明 |
| [sklearn svm/_classes.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/svm/_classes.py) | 💻 源码 | Code：SVC/SVR 实现细节，libsvm 封装 |
| [Chang & Lin 2011 LIBSVM](../../../.documents/papers/svm/chang_lin_2011_libsvm.pdf) | 📖 论文 | Code + History：libsvm 实现 |
| [Boser et al. COLT 1992](https://doi.org/10.1145/130385.130401) | 📖 论文 | History：核 SVM 原始论文 |
