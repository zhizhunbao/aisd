---
topic: knn
dimension: tutorial
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Cover & Hart, IEEE Trans. Inform. Theory 1967 — ⚠️ 待下载 见 papers_index.md"
  - "📚 Book: Hastie, Tibshirani, Friedman, 《ESL》 Ch.2 §2.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., 《ISLR》 Ch.2 §2.2.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📖 Docs: scikit-learn Neighbors User Guide — https://scikit-learn.org/stable/modules/neighbors.html"
expiry: 12m
status: current
---

# KNN 教程

> **前置知识：** 距离度量基础、偏差-方差权衡、交叉验证、特征缩放
> **参考来源：** [scikit-learn Neighbors](https://scikit-learn.org/stable/modules/neighbors.html) | [《ESL》Ch.2](../../../textbooks/hastie_esl.pdf) | [《ISLR》Ch.2](../../../textbooks/james_ISLR.pdf)

---

## Section 0: 前置知识速查

1. **距离度量**：欧氏距离 $\sqrt{\sum_j (x_j - x'_j)^2}$，需要特征量纲一致
2. **特征缩放**：必须先 StandardScaler 或 MinMaxScaler，否则量级大的特征主导距离
3. **偏差-方差权衡**：k 小→低偏差高方差，k 大→高偏差低方差
4. **交叉验证**：通过 k-fold CV 选择最优超参数 k
5. **非参数模型**：不假设数据服从特定分布

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.2 §2.2

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **问题1：复杂决策边界无法用线性模型拟合** — 现实数据经常有非线性、弯曲的类别边界，逻辑回归等线性模型无能为力（需要复杂特征工程）
- 🔥 **问题2：需要一个快速可用的基线方法** — 在没有领域知识时，需要一个不做任何假设就能运行的方法
- 🔥 **问题3：小数据集下参数模型受限** — 数据量少时，参数模型难以可靠估计参数；KNN 直接利用数据本身

### 它的核心价值

1. **零假设**：不假设数据分布，天然适应任何形状的决策边界
2. **直觉透明**：预测逻辑"找最像的邻居问他们"，任何人都能理解
3. **Cover-Hart 理论保证**：渐近误差率不超过贝叶斯最优错误率的 2 倍——这是严格的数学保证
4. **多任务**：同一框架支持分类、回归、异常检测

> 📖 Paper: Cover & Hart (1967) ⚠️ 待下载
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

```
┌───────────────────────────────────────────────────────────────────────┐
│                          KNN 完整流程                                  │
├───────────────────────────────────────────────────────────────────────┤
│  训练阶段（惰性）                                                       │
│  输入: (X_train, y_train)                                              │
│  └──→ 仅存储数据，构建索引结构（KD-Tree / Ball Tree）                    │
│                                                                       │
│  预测阶段（每次查询）                                                    │
│  输入: x_query                                                        │
│         │                                                             │
│         ▼                                                             │
│  ┌─────────────────────────────┐                                      │
│  │ Step 1: 计算距离             │  D(x_query, x_i) for all i          │
│  └──────────────┬──────────────┘                                      │
│                 ▼                                                     │
│  ┌─────────────────────────────┐                                      │
│  │ Step 2: 排序，取前 k 名     │  argsort → N_k(x)                   │
│  └──────────────┬──────────────┘                                      │
│                 ▼                                                     │
│     ┌───────────┴───────────┐                                         │
│     ▼                       ▼                                         │
│  分类: 多数投票          回归: 取均值                                    │
│  y_hat = mode(y[N_k])   y_hat = mean(y[N_k])                         │
└───────────────────────────────────────────────────────────────────────┘
```

> 💻 Source: [sklearn/neighbors/_classification.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_classification.py)

### 2.2 核心机制：为什么"惰性"有意义？

**为什么不预先构建判别函数？**

参数模型（如逻辑回归）在训练时将数据"压缩"进固定参数——一旦训练完成，决策边界就固定了。但 KNN 保留全部训练数据：

- 局部适应性：每个查询点都有自己的"局部邻域"，决策边界自动随数据分布弯曲
- 代价：预测时必须访问训练数据（内存+时间开销）

这是一种**空间换时间的反向权衡**——训练极快，但预测慢。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3（与最近质心分类的对比）

### 2.3 索引加速：KD-Tree 与 Ball Tree

暴力搜索 Brute Force 对每个查询需要 $O(n \cdot d)$ 时间。当 $n$ 大时无法接受。

**KD-Tree（k-d 树）**：按维度递归将空间切成两半，建成二叉树。查询时利用三角不等式剪枝，跳过不可能包含最近邻的分支。
- 适合：$d \leq 20$，效果 $O(d \log n)$
- 缺点：高维下剪枝效果消失（几乎每个分支都得检查）

**Ball Tree（球树）**：用超球体而非超矩形划分空间。高维下比 KD-Tree 更有效。
- 适合：$d > 20$ 时优于 KD-Tree

```
KD-Tree 二维示意：
  
  D=中线
  ┌───┬───┐
  │ A │ B │  按 x₁ 切割：左子树 A，右子树 B
  ├───┼───┤  再按 x₂ 切割各子树
  │ C │ D │
  └───┴───┘
```

> 📖 Docs: [scikit-learn Algorithm Choice](https://scikit-learn.org/stable/modules/neighbors.html#choice-of-nearest-neighbors-algorithm)

### 2.4 k 的选择：偏差-方差权衡

```
高方差（过拟合）      最优 k              高偏差（欠拟合）
     k=1    ──────────────────────────→ k=N
   ↑误差     Best k via CV               ↑误差
   边界锯齿状                           边界平滑/退化为全局预测
```

规则：
- **k 为奇数**（二分类）：避免投票平局
- **k ≈ √n**：经验起始点，再用 CV 微调
- **加权 KNN**（`weights='distance'`）：距离加权可部分缓解大 k 的平滑过度问题

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.2 §2.2.3

---

## Section 3: 局限性

1. **维度灾难** → 高维时距离失去意义；应对：PCA降维、特征选择、改用余弦相似度
2. **预测慢** → 每次查询 O(n·d)；应对：使用 KD-Tree/Ball Tree 加速，或近似最近邻（ANN）库（faiss, annoy）
3. **内存消耗大** → 必须存全部训练数据；应对：原型方法（Condensed NN）选代表子集
4. **特征敏感** → 无关/噪声特征严重干扰距离；应对：特征选择或学习距离度量（Metric Learning）
5. **类不平衡** → 多数类邻居更多，少数类被压制；应对：`class_weight='balanced'` 或 SMOTE 过采样

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.5（维度灾难专节）

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **KNN (k=1)** | 完美拟合训练集，零假设 | 高方差，预测慢 | 噪声少的小数据集 |
| **KNN (最优 k)** | 理论保证，非线性边界 | 预测 O(n·d) | 中小数据集，非线性问题 |
| **逻辑回归** | 预测极快 O(d)，可解释 | 只能线性边界 | 线性可分，大数据集 |
| **SVM** | 高维有效，最大间隔 | 训练慢，核选择难 | 高维，中等数据集 |
| **决策树** | 可解释，处理类别特征 | 不稳定，容易过拟合 | 需要可解释性 |
| **随机森林** | 精度高，抗过拟合 | 黑盒，慢 | 通用基线 |

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.2-8（各算法对比）

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《ESL》Ch.2 §2.3](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | Section 1 核心价值、Section 2.2 原理 |
| [《ESL》Ch.2 §2.5](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | Section 3 维度灾难 |
| [《ISLR》Ch.2 §2.2.3](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | Section 2.4 k 选择、Section 4 对比 |
| Cover & Hart (1967) ⚠️ 待下载 | 📖 论文 | Section 1 理论保证 |
| [scikit-learn Neighbors](https://scikit-learn.org/stable/modules/neighbors.html) | 📖 文档 | Section 2.3 算法选择 |
| [sklearn/neighbors/_classification.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_classification.py) | 💻 源码 | Section 2.1 流程图 |
