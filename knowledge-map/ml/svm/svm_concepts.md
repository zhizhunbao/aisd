---
topic: svm
dimension: concepts
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📚 Book: Hastie et al., ESL Ch.12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md"
  - "📚 Book: Bishop, PRML Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md"
  - "📖 Docs: scikit-learn SVM — https://scikit-learn.org/stable/modules/svm.html"
expiry: 12m
status: current
---

# SVM 核心概念

> 📚 Book: Hastie et al., [ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md), Sec.12.1–12.3
> 📚 Book: Bishop, [PRML Ch.7](../../../data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md), Sec.7.1–7.2

---

## 术语定义

### 超平面 (Hyperplane)

$p$ 维空间中满足 $\{x : f(x) = x^T\beta + \beta_0 = 0\}$ 的点集。在 2D 是一条直线，在 3D 是一个平面。SVM 寻找的决策边界就是一个超平面，分类规则为 $G(x) = \text{sign}[x^T\beta + \beta_0]$。超平面将空间一分为二，SVM 找的是"最居中"的那一个。

> 易混淆：**超平面 vs 决策边界** — 对线性 SVM 两者等价；对核 SVM，原始输入空间的决策边界是非线性的，但映射后的高维特征空间里仍是超平面

> 📚 Book: Hastie ESL, Sec.12.2 Eq.(12.1–12.2)

### 间隔 (Margin)

超平面到最近训练样本的最小距离之两倍，宽度为 $2M = 2/\|\beta\|$。SVM 通过最小化 $\|\beta\|$（即最大化 $M$）来找最优超平面。间隔越宽，模型的 VC 维上界越小，泛化误差上界越紧。

直觉：间隔是超平面两侧的"禁区"——SVM 找宽度最大的禁区，使两类样本离边界尽可能远。

> 易混淆：**间隔 $M$ vs 总宽度** — $M = 1/\|\beta\|$ 是超平面到单侧支持向量的距离，总宽度是 $2M$

> 📚 Book: Hastie ESL, Sec.12.2 Eq.(12.3–12.4); Bishop PRML Sec.7.1 Fig.7.1

### 支持向量 (Support Vectors)

对偶解中 $\hat{\alpha}_i > 0$ 的训练样本。超平面 $\hat{\beta} = \sum_i \hat{\alpha}_i y_i x_i$ 完全由支持向量表示——其他样本点删除或移动不影响解。支持向量通常只占训练集的一小部分，这带来了预测时的效率优势。

直觉：支持向量是"撑起边界的桥墩"，普通样本是"旁观者"，只有桥墩影响桥的位置。

> 易混淆：**支持向量 vs 所有样本** — 只有 $\hat{\alpha}_i > 0$ 的点才是支持向量；软间隔中分为 margin 上（$0 < \hat{\alpha}_i < C$）和违反 margin（$\hat{\alpha}_i = C$）两类

> 📚 Book: Hastie ESL, Sec.12.2.1 Eq.(12.17); Bishop PRML Sec.7.1.1

### 松弛变量 (Slack Variables)

软间隔 SVM 引入 $\xi_i \geq 0$ 允许样本"违反"间隔约束：$\xi_i = 0$ 表示在间隔正确侧；$\xi_i \in (0,1]$ 表示在间隔带内但分类正确；$\xi_i > 1$ 表示误分类。通过 $\sum \xi_i \leq \text{const}$ 约束控制总违反量。

直觉：松弛变量是"违规罚款额度"——每个样本可以越界，但需要"买单"，总预算由参数 C 控制。

> 易混淆：**松弛变量 vs 误差** — $\xi_i > 1$ 才是真正的误分类；$\xi_i \leq 1$ 只是"进入禁区"但分类正确

> 📚 Book: Hastie ESL, Sec.12.2 Eq.(12.7); Bishop PRML Sec.7.1.1 Eq.(7.19–7.21)

### 参数 C (正则化参数)

控制间隔宽度和误分类惩罚的权衡。优化目标为 $\min \frac{1}{2}\|\beta\|^2 + C\sum_i \xi_i$：**C 大 → 惩罚误分类重 → 间隔窄 → 过拟合风险**；**C 小 → 容忍更多误分类 → 间隔宽 → 欠拟合风险**。C 等价于铰链损失写法中的 $\lambda = 1/C$。

> 易混淆：**C 越大越好？** — 不是，C 太大会过拟合；应用交叉验证在对数尺度（$10^{-3}$ 到 $10^3$）搜索

> 📚 Book: Hastie ESL, Sec.12.2.1 Eq.(12.8); Sec.12.3.2 Eq.(12.25)

### 核技巧 (Kernel Trick)

核函数 $K(x, x') = \langle h(x), h(x') \rangle$ 隐式计算高维特征空间的内积，无需显式构造映射 $h(x)$。只要 $K$ 是对称正定函数（满足 Mercer 条件），SVM 的对偶问题可以将所有 $\langle x_i, x_j \rangle$ 替换为 $K(x_i, x_j)$，从而在任意高维（甚至无限维）空间中操作。

直觉：核函数是"魔法翻译器"——不用飞到高维空间，只要知道两点在那里的"相似度"（内积）。

> 易混淆：**核函数 vs 特征映射** — 核 $K(x,x')$ 是标量函数（两点间的相似度）；特征映射 $h(x)$ 是向量函数（单点的高维表示）。Kernel SVM 只需要 $K$，永远不显式计算 $h$

> 📚 Book: Hastie ESL, Sec.12.3 Eq.(12.21–12.22); Bishop PRML Ch.6 (Kernel Methods)

### 铰链损失 (Hinge Loss)

$L(y, f) = [1 - yf]_+ = \max(0, 1 - yf)$。当预测正确且离边界足够远（$yf \geq 1$）时损失为 0；越过边界则线性增加。SVM 可等价地写为 $\min_{\beta_0, \beta} \sum_i [1-y_i f(x_i)]_+ + \frac{\lambda}{2}\|\beta\|^2$（$\lambda = 1/C$）。

> 易混淆：**铰链损失 vs 逻辑损失** — 铰链损失估计的是分类器符号（模）；对数损失估计的是类别概率的对数几率。铰链损失在 $yf \geq 1$ 时完全为 0，有稀疏性；逻辑损失永远非零

> 📚 Book: Hastie ESL, Sec.12.3.2 Eq.(12.25) + Fig.12.4 + Table 12.1

---

## 概念辨析

### 硬间隔 SVM vs 软间隔 SVM

| 维度 | 硬间隔 (Hard Margin) | 软间隔 (Soft Margin) |
|------|---------------------|---------------------|
| **适用条件** | 数据线性可分 | 数据可不可分均适用 |
| **松弛变量** | 无 | $\xi_i \geq 0$ |
| **参数 C** | C → ∞ | C > 0，需调参 |
| **允许误分类** | ❌ 不允许 | ✅ 受 C 控制 |
| **实用性** | 理论理想，实际罕见 | **工业主流** |
| **对应公式** | $\min \|\beta\|$ s.t. $y_i f(x_i) \geq 1$ | $\min \frac{1}{2}\|\beta\|^2 + C\sum\xi_i$ |

> 📚 Book: Hastie ESL, Sec.12.2 Eq.(12.4) vs Eq.(12.8)

### SVM 铰链损失 vs 各类损失函数

| 损失函数 | 公式 | 稀疏性 | 估计目标 | 对离群点 |
|---------|------|-------|---------|---------|
| **铰链 (SVM)** | $[1-yf]_+$ | ✅ 高 | 类别符号 $G(x)$ | 线性惩罚，较鲁棒 |
| **逻辑损失** | $\log(1+e^{-yf})$ | ❌ 无 | 对数几率 | 渐近线性，鲁棒 |
| **平方损失** | $[y-f]^2$ | ❌ 无 | $2P(y=1|x)-1$ | 二次惩罚，**不鲁棒** |
| **Huberized 铰链** | 分段 | ✅ 有 | $2P(y=1|x)-1$ | 光滑，兼具优点 |

> 📚 Book: Hastie ESL, Sec.12.3.2 Fig.12.4 + Table 12.1

---

## 核心属性

### 信息架构

```
┌────────────────────────────────────────────────────────────────┐
│  SVM 系统架构                                                   │
├────────────────────────────────────────────────────────────────┤
│ 输入                                                            │
│  ├─ 训练数据 (x_i, y_i)，y_i ∈ {-1, +1}                       │
│  ├─ 核函数 K（linear / poly / rbf / sigmoid）                  │
│  ├─ 参数 C（惩罚强度）                                          │
│  └─ 核参数（gamma γ、degree d 等）                             │
├────────────────────────────────────────────────────────────────┤
│ 训练流程                                                        │
│  ├─ Step 1: 构造对偶 QP 问题（N×N 核矩阵）                     │
│  ├─ Step 2: 求解 α_i（libsvm: SMO 或类似算法）                │
│  ├─ Step 3: 找支持向量（α_i > 0），计算 β_0                   │
│  └─ 决策函数 f(x) = Σ α_i y_i K(x, x_i) + β_0               │
├────────────────────────────────────────────────────────────────┤
│ 输出                                                            │
│  ├─ support_vectors_：支持向量特征矩阵                          │
│  ├─ dual_coef_：α_i × y_i                                     │
│  ├─ intercept_：β_0（偏置项）                                  │
│  └─ n_support_：每类的支持向量数                               │
└────────────────────────────────────────────────────────────────┘
```

> 💻 Source: [sklearn svm/_classes.py](../../../.github/scikit-learn/sklearn/svm/_classes.py) `SVC.fit()`

### 适用场景 ✅

- 中小规模数据集（样本 N < 50,000），特征维度中等
- 高维稀疏特征（文本分类、基因组数据）——使用线性核
- 数据有明显间隔，或希望得到稀疏支持向量解
- 需要非概率的硬分类边界（SVM 不直接输出概率）
- 二分类问题（多分类需用 OvO 或 OvR 策略）

### 不适用场景 ❌

- 大规模数据集（N > 100,000）：O(N²~N³) 训练时间和 O(N²) 内存不可接受，改用 `LinearSVC` 或逻辑回归
- 需要校准概率输出：SVM 不直接输出概率，需额外 Platt scaling（`probability=True` 训练慢 5 倍）
- 特征维度 >> 样本数时核 SVM 核矩阵意义不大，优先线性模型
- 实时在线学习（SVM 不支持增量更新，改用 SGD）

> 📚 Book: Hastie ESL, Sec.12.3.4 (SVMs and Curse of Dimensionality) + Sec.12.3.8 (Discussion)
> 📖 Docs: [sklearn SVM 用户指南](https://scikit-learn.org/stable/modules/svm.html#tips-on-practical-use)

---

## 速查表

| 项 | 说明 | 典型值/示例 |
|-----|------|-----------|
| `SVC(C=1.0, kernel='rbf')` | 默认软间隔 RBF 核 | 分类任务起点 |
| `SVR(C=1.0, epsilon=0.1)` | 回归，ε-不敏感损失 | ε 是忽略残差的区间 |
| `LinearSVC(C=1.0)` | 线性核，liblinear 优化 | 大数据集、高维稀疏特征 |
| `kernel` | `'linear'/'poly'/'rbf'/'sigmoid'` | 默认 `'rbf'` |
| `gamma` | RBF/poly/sigmoid 核参数 | `'scale'`=1/(n_feat·var(X)) |
| `support_vectors_` | 支持向量特征矩阵 | shape: (n_sv, n_features) |
| `dual_coef_` | $\alpha_i y_i$ 系数 | shape: (n_class-1, n_sv) |
| 训练复杂度 | $O(N^{2..3})$（libsvm） | N > 50k 请用 LinearSVC |
| 预测复杂度 | $O(N_{sv} \cdot d)$ | $N_{sv}$ = 支持向量数，d = 特征维 |

> 📖 Docs: [sklearn SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
> 💻 Source: [sklearn svm/_libsvm.pyx](../../../.github/scikit-learn/sklearn/svm/_libsvm.pyx)
