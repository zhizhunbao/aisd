---
topic: svm
dimension: tutorial
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Cortes & Vapnik ML 1995 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/svm/cortes_vapnik_1995_svm.pdf"
  - "📖 Paper: Boser Guyon Vapnik COLT 1992 — https://doi.org/10.1145/130385.130401"
  - "📚 Book: Hastie et al., ESL Ch.12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md"
  - "📚 Book: Bishop, PRML Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md"
  - "📖 Docs: sklearn SVM Practical Tips — https://scikit-learn.org/stable/modules/svm.html#tips-on-practical-use"
expiry: 12m
status: current
---

# SVM 教程

> **前置知识：** 超平面几何、内积、拉格朗日乘子法、凸优化基础
> **参考来源：** [Cortes & Vapnik 1995](../../../.documents/papers/svm/cortes_vapnik_1995_svm.pdf) | [Hastie ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md) | [Bishop PRML Ch.7](../../../data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md)

---

## Section 0: 前置知识速查

1. **超平面**：$p$ 维空间中 $w^Tx + b = 0$ 的点集；法向量 $w$ 决定方向，$b$ 决定位置
2. **有符号距离**：点 $x_0$ 到超平面的有符号距离 = $f(x_0)/\|w\|$，正负对应两侧
3. **拉格朗日乘子法**：等式约束优化；KKT 条件推广到不等式约束（$\alpha_i \geq 0$，互补松弛）
4. **凸二次规划 (QP)**：目标函数是二次的，约束是线性的 → 有全局最优解，有高效求解器
5. **内积与正定核**：Mercer 定理：若 $K$ 是对称正半定函数，则存在隐式特征映射 $h$ 使 $K(x,x') = \langle h(x), h(x') \rangle$

> 📚 Book: Hastie ESL, Appendix A (矩阵/优化基础); Bishop PRML Appendix E (Lagrange Multipliers)

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

以感知机（Perceptron）为例——它能找到一条分离直线，但：

- 🔥 **问题 1：解不唯一**。对线性可分数据，无穷多条直线都能完美分类；感知机停在第一个它遇到的解，高度依赖训练顺序
- 🔥 **问题 2：泛化无保证**。一条"贴着"某个样本的边界，哪怕训练误差为 0，测试时一个微小扰动就误分类
- 🔥 **问题 3：无法量化置信度**。距离边界 0.001 和距离边界 10 的点，感知机完全等同对待
- 🔥 **问题 4：线性不可分的情况下完全失效**（感知机不收敛）

### 它的核心价值

1. **唯一性**：最大间隔超平面是唯一确定的（凸 QP 有全局唯一最优解）
2. **泛化理论支撑**：Vapnik-Chervonenkis 理论证明，最大化间隔 = 最小化 VC 维上界 = 更紧的泛化误差界
3. **稀疏性**：决策函数只由少量支持向量决定，预测高效，对非支持向量的噪声天然鲁棒
4. **核技巧**：通过核函数将线性 SVM 推广到非线性，且无需显式计算高维特征

> 📖 Paper: Cortes & Vapnik 1995, Sec.1 (Introduction); Vapnik 1998 (Statistical Learning Theory)
> 📚 Book: Hastie ESL, Sec.12.1 (Introduction) + Sec.7.9 (VC Dimension)

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 训练流程图

```
┌────────────────────────────────────────────────────────────────────┐
│                         SVM 训练流程                               │
├────────────────────────────────────────────────────────────────────┤
│  输入：(x_i, y_i), C, 核函数 K                                     │
│       │                                                            │
│       ▼                                                            │
│  ┌──────────────────────┐                                          │
│  │ Step 1: 标准化输入    │ StandardScaler / MinMaxScaler           │
│  └──────────────────────┘                                          │
│       │                                                            │
│       ▼                                                            │
│  ┌──────────────────────┐                                          │
│  │ Step 2: 构造核矩阵    │ K_ij = K(x_i, x_j)，N×N 矩阵           │
│  └──────────────────────┘                                          │
│       │                                                            │
│       ▼                                                            │
│  ┌──────────────────────┐                                          │
│  │ Step 3: 求解对偶 QP  │ libsvm SMO 算法求 α_i                   │
│  └──────────────────────┘                                          │
│       │                                                            │
│       ▼                                                            │
│  ┌──────────────────────┐                                          │
│  │ Step 4: 识别支持向量 │ α_i > 0 的点即支持向量                  │
│  └──────────────────────┘                                          │
│       │                                                            │
│       ▼                                                            │
│  ┌──────────────────────┐                                          │
│  │ Step 5: 计算 β_0     │ 对 margin 上的点：y_i f(x_i) = 1        │
│  └──────────────────────┘                                          │
│       │                                                            │
│       ▼                                                            │
│  输出：f(x) = Σ α_i y_i K(x, x_i) + β_0                           │
└────────────────────────────────────────────────────────────────────┘
```

> 📖 Paper: Platt 1999 (SMO算法); 💻 Source: sklearn svm/_libsvm.pyx

### 2.2 为什么最大化间隔能提升泛化？

**VC 维理论的关键结论**：对于决策函数类 $\{G(x) = \text{sign}(w^Tx+b) : \|w\| \leq A\}$，VC 维 $h \leq R^2A^2$（$R$ 为数据球半径）。测试误差以高概率满足：

$$
\text{Error}_\text{Test} \leq \text{Error}_\text{Train} + O\left(\sqrt{\frac{h \log(N/h)}{N}}\right)
$$

最大化间隔 = 最小化 $\|w\|$ = 最小化 $h$ = **最紧泛化误差界**。

**直觉**：宽间隔相当于给预测留了"安全余量"——训练样本上的小扰动不会让测试样本越过边界。

> 📚 Book: Hastie ESL, Sec.12.3.8 Eq.(12.50–12.51) + Sec.7.9 (SRM)

### 2.3 为什么核技巧有效？

**核心洞察**：SVM 的对偶问题和预测函数中，$x$ 只以内积 $\langle x_i, x_j \rangle$ 出现。因此：将所有内积替换为 $K(x_i, x_j)$，等价于在映射后的高维空间中做线性 SVM。

```
低维原始空间（线性不可分）   →   高维特征空间（线性可分）
         x ∈ R^p                        h(x) ∈ R^M (M >> p)
         
   核函数直接给出高维内积：K(x,x') = h(x)^T h(x')
   永远不需要显式计算 h(x)
```

**为什么不直接做特征展开？** d 次多项式展开后维度是 $\binom{p+d}{d}$（如 $p=100, d=3$ 时超过 17 万维）。核函数 $K(x,x') = (1+x^Tx')^3$ 只需 $O(p)$ 计算即可得到这 17 万维空间的内积。

> 📖 Paper: Boser, Guyon & Vapnik 1992; 📚 Hastie ESL, Sec.12.3 Eq.(12.19–12.22)

### 2.4 参数 C 和 γ 的直觉

```
C 小（容忍误分类）          C 大（严格分类）
宽间隔 ──────────────────────────────── 窄间隔
平滑边界                              复杂边界（过拟合）

γ 小（高斯核宽）            γ 大（高斯核窄）
全局影响（欠拟合）──────────────────── 局部影响（过拟合）
```

- **C 的调参策略**：以对数尺度搜索（如 $10^{-3}, 10^{-2}, ..., 10^3$），用交叉验证
- **γ 的调参策略**：`gamma='scale'`（$= 1/(p \cdot \text{Var}(X))$）是好起点；再对数尺度搜索

> 📖 Docs: [sklearn SVM Practical Tips](https://scikit-learn.org/stable/modules/svm.html#tips-on-practical-use)
> 📚 Book: Hastie ESL, Sec.12.3.5 + Fig.12.6 (C 对决策边界的影响)

---

## Section 3: 局限性

1. **训练慢** → 核矩阵 $O(N^2)$，QP 求解 $O(N^{2..3})$；N > 50k 时极慢 → 改用 `LinearSVC` 或逻辑回归
2. **核的选择依赖先验** → 没有"一个核适合所有问题"；RBF 是通用起点但不一定最优 → 用交叉验证选核
3. **参数敏感** → C 和 γ 相互影响，需要二维网格搜索 → `GridSearchCV` 或 `RandomizedSearchCV`
4. **不输出概率** → 铰链损失的极值是类别符号，不是概率；需要 Platt scaling（`probability=True`）但使训练慢 5 倍 → 需要概率时优先逻辑回归
5. **不适合高维 + 少样本的核 SVM** → 核矩阵退化，特征数 >> 样本数时用线性 SVM 更合适

> 📚 Book: Hastie ESL, Sec.12.3.4 (SVM and Curse of Dimensionality) + Sec.12.3.8 (Discussion)
> 📖 Docs: [sklearn SVM 常见问题](https://scikit-learn.org/stable/modules/svm.html#complexity)

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 最适合场景 |
|------|------|------|-----------|
| **SVM (RBF 核)** | 泛化理论强；处理非线性；对高维有效 | 训练慢 O(N²⁻³)；参数需调 | 中小规模，边界非线性 |
| **逻辑回归** | 输出概率；训练快 O(N)；可在线学习 | 仅线性边界（无核时）| 大规模，需要概率校准 |
| **随机森林** | 无需标准化；自动特征选择；并行 | 不产生间隔；预测慢 | 表格数据，混合类型特征 |
| **神经网络** | 超强非线性表达；端到端特征学习 | 需要大量数据；调参复杂 | 图像/文本/大规模数据 |
| **线性SVM (LinearSVC)** | liblinear 优化，大规模可用 | 仅线性边界 | 高维稀疏（文本/NLP）|

> 📚 Book: Hastie ESL, Sec.12.3.8 + Table 12.2 (Skin of Orange 实验对比)

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [Cortes & Vapnik 1995](../../../.documents/papers/svm/cortes_vapnik_1995_svm.pdf) | 📖 论文 | Section 1（动机）, Section 2（训练流程）|
| [Boser, Guyon & Vapnik 1992](https://doi.org/10.1145/130385.130401) | 📖 论文 | Section 2.3（核技巧）|
| [Hastie ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md) | 📚 教科书 | 全文，Section 2.2/2.4/3/4 |
| [Bishop PRML Ch.7](../../../data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md) | 📚 教科书 | Section 0（前置）|
| [sklearn SVM Docs](https://scikit-learn.org/stable/modules/svm.html) | 📖 文档 | Section 2.4（参数调节）, Section 3（局限性）|
