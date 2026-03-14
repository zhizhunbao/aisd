---
topic: decision_tree
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Hastie et al., ESL Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., ISLR Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📚 Book: Murphy, PML1 Ch.18 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: scikit-learn DecisionTree — https://scikit-learn.org/stable/modules/tree.html"
expiry: 12m
status: current
---

# Decision Tree 核心概念

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8

---


## 术语定义

### 决策树 (Decision Tree)

一种通过递归地将特征空间分割为矩形区域，并在每个区域内做常数预测的非参数模型。树结构由内部节点（测试条件）、分支（条件结果）和叶子节点（预测值）组成。分类树预测类别，回归树预测连续值。

> 易混淆：**Decision Tree vs Decision Rule** — 树是嵌套的规则集合（有层次结构），规则列表是扁平的（无层次）

### 根节点 (Root Node)

树的最顶层节点，包含全部训练数据。第一次分割就发生在这里——选择使不纯度下降最大的特征和阈值。

### 内部节点 / 决策节点 (Internal Node / Decision Node)

树中间的节点，每个节点对应一个**测试条件**："特征 $x_j \leq t$？"。CART 算法中每个节点只做**二叉分割**（是/否），而 ID3/C4.5 可以做多路分割。

### 叶子节点 / 终端节点 (Leaf Node / Terminal Node)

树的末端节点，不再分割。分类树中叶子输出**多数类标签**，回归树中叶子输出**区域内样本均值**。

### 不纯度 (Impurity)

衡量一个节点中样本"混杂"程度的指标。不纯度为 0 意味着节点中所有样本属于同一类别（纯净）。常用的不纯度度量有 Gini 不纯度和信息熵。

> 易混淆：**Gini 不纯度 vs Gini 系数** — Decision Tree 中的 Gini 是 $1 - \sum p_k^2$（衡量分类纯度），经济学中的 Gini 系数衡量收入不平等，虽然名字相同但含义完全不同

### Gini 不纯度 (Gini Impurity)

$$G = 1 - \sum_{k=1}^K p_k^2$$

其中 $p_k$ 是节点中类别 $k$ 的比例。取值范围 $[0, 1-1/K]$，值越小越纯。Gini 是 sklearn 的默认分割准则——它近似信息熵但计算更快（不需要对数运算）。

### 信息熵 (Entropy)

$$H = -\sum_{k=1}^K p_k \log_2 p_k$$

信息论中的概念，衡量不确定性。最大值 $\log_2 K$（均匀分布时），最小值 0（纯净时）。ID3/C4.5 使用熵作为分割准则。

> 易混淆：**Entropy vs Gini** — 实际效果差异很小（~2%），Gini 计算更快，Entropy 倾向于产生更平衡的树

### 信息增益 (Information Gain)

$$IG = H(\text{parent}) - \sum_{\text{children}} \frac{N_{\text{child}}}{N_{\text{parent}}} H(\text{child})$$

分割前后熵的减少量。每次分割选择使信息增益最大的特征。ID3 用信息增益的一个问题是：它偏好取值多的特征（如 ID 字段）。

### 增益率 (Gain Ratio)

$$GR = \frac{IG}{H_{\text{split}}}$$

C4.5 引入的修正——用分割本身的熵（Split Information）归一化信息增益，惩罚取值过多的特征。

### 递归二分法 (Recursive Binary Splitting)

CART 的核心算法：贪心地选择最优特征和阈值进行二叉分割，然后对每个子节点递归执行。"贪心"意味着每一步只看当前最优，不考虑全局最优——因为全局最优是 NP-hard 问题。

> 易混淆：**贪心 vs 最优** — Decision Tree 构建是**贪心**的（局部最优），不保证全局最优。这是集成方法（RF/GBDT）用多棵树补偿的原因

### 剪枝 (Pruning)

通过删除树的某些子树来减小复杂度、防止过拟合。**预剪枝（Pre-pruning）** 在构建时限制（如 `max_depth`），**后剪枝（Post-pruning）** 先长完整棵树再回头修剪（如 Cost-Complexity Pruning / Minimal Cost-Complexity Pruning）。

### 代价复杂度剪枝 (Cost-Complexity Pruning / Minimal Cost-Complexity Pruning)

CART 的后剪枝方法。定义目标函数 $R_\alpha(T) = R(T) + \alpha|T|$，其中 $R(T)$ 是误差，$|T|$ 是叶子节点数，$\alpha$ 是惩罚参数。通过交叉验证选择最优 $\alpha$。sklearn 中用 `ccp_alpha` 参数实现。

### 特征重要性 (Feature Importance)

衡量每个特征对降低不纯度的贡献。计算方式：该特征在所有分割中带来的加权不纯度下降之和，除以总下降量。sklearn 的 `.feature_importances_` 属性直接输出。

> 易混淆：**MDI vs Permutation Importance** — MDI（Mean Decrease in Impurity）是树内部计算的，对高基数特征有偏；Permutation Importance 是模型无关的，更可靠

### CART (Classification and Regression Trees)

Breiman 等人 1984 年提出的决策树算法。特点：只做**二叉分割**（每个节点分成两个子节点），分类用 Gini 不纯度，回归用 MSE，并引入了代价复杂度剪枝。scikit-learn 实现的就是 CART。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8.1
> 📖 Docs: [scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html)

---


## 概念辨析

### ID3 vs C4.5 vs CART

| 维度 | ID3 | C4.5 | CART |
|------|-----|------|------|
| **作者** | Quinlan 1986 | Quinlan 1993 | Breiman et al. 1984 |
| **分割方式** | 多路分割 | 多路分割 | **二叉分割** |
| **分类准则** | 信息增益 | 增益率 | Gini 不纯度 |
| **回归** | ❌ 不支持 | ❌ 不支持 | ✅ 支持（MSE） |
| **缺失值** | ❌ | ✅ 概率权重 | ✅ 代理分割 |
| **连续特征** | ❌ | ✅ 二分阈值 | ✅ 二分阈值 |
| **剪枝** | 无 | 基于 MDL | 代价复杂度剪枝 |
| **sklearn** | ❌ | ❌ | ✅ 默认实现 |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.18.1

### Decision Tree vs Logistic Regression

| 维度 | Decision Tree | Logistic Regression |
|------|--------------|-------------------|
| **决策边界** | 轴对齐矩形（非线性） | 线性超平面 |
| **假设** | 无参数假设 | log-odds 线性 |
| **可解释性** | 可视化树结构 | 系数 → odds ratio |
| **概率输出** | 叶子频率（粗粒度） | sigmoid 概率（细粒度） |
| **特征交互** | 自动捕捉 | 需手动添加交互项 |
| **过拟合** | 高（需剪枝） | 低（凸优化 + 正则化） |
| **训练速度** | 快 | 快 |
| **集成** | RF/GBDT 的基学习器 | 通常不做集成 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4 vs Ch.9

### Classification Tree vs Regression Tree

| 维度 | Classification Tree | Regression Tree |
|------|-------------------|-----------------|
| **输出** | 类别标签 | 连续值 |
| **叶子预测** | 多数类投票 | 区域均值 |
| **分割准则** | Gini / Entropy | MSE / MAE |
| **评估指标** | Accuracy / F1 | MSE / R² |
| **sklearn 类** | `DecisionTreeClassifier` | `DecisionTreeRegressor` |

> 📖 Docs: [scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html)

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────┐
│                    Decision Tree 架构                          │
├──────────────────────────────────────────────────────────────┤
│  输入                                                         │
│  └─ 特征矩阵 X (N×p) + 标签 y (N×1)                          │
├──────────────────────────────────────────────────────────────┤
│  训练：递归二分法                                              │
│  ├─ 对每个节点：                                              │
│  │   ├─ 遍历所有特征 j ∈ {1,...,p}                           │
│  │   ├─ 遍历所有阈值 t (排序后的 unique 值)                   │
│  │   ├─ 计算分割后不纯度下降 ΔI                               │
│  │   └─ 选择使 ΔI 最大的 (j*, t*)                            │
│  ├─ 停止条件: max_depth / min_samples / 纯净                 │
│  └─ 剪枝: ccp_alpha (后剪枝)                                 │
├──────────────────────────────────────────────────────────────┤
│  预测                                                         │
│  ├─ 从根节点开始，按规则下行到叶子                             │
│  ├─ 分类: 叶子多数类                                          │
│  └─ 回归: 叶子区域均值                                        │
├──────────────────────────────────────────────────────────────┤
│  输出                                                         │
│  ├─ 树结构 (可视化)                                           │
│  ├─ 类别 / 回归值                                             │
│  └─ 特征重要性 feature_importances_                           │
└──────────────────────────────────────────────────────────────┘
```

> 📖 Docs: [scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html)

### 适用场景 ✅

- 需要**高可解释性**（医疗、法律、合规）——树可以直接画出决策规则
- 特征包含**混合类型**（数值 + 类别）——不需要标准化或独热编码
- 数据中有**非线性关系和特征交互**——树自动捕捉
- 作为 Random Forest / GBDT 的**基学习器**
- 需要**快速训练和预测**——$O(Np\log N)$ 训练，$O(\log N)$ 预测
- 探索性数据分析（快速发现重要特征和规则）

### 不适用场景 ❌

- 需要平滑的决策边界（树的边界是阶梯形的轴对齐矩形）
- 数据存在**线性关系**时——Linear/Logistic Regression 更简洁高效
- 要求**稳定性**时——训练数据微小变化可能导致完全不同的树
- 高维稀疏数据（如文本 TF-IDF）——线性模型通常更好
- 需要**外推**（extrapolation）时——回归树在训练范围外预测为常数

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8.1

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 模型类型 | 非参数监督学习 | `DecisionTreeClassifier()` |
| 分割准则（分类） | Gini / Entropy / Log-loss | `criterion='gini'` |
| 分割准则（回归） | MSE / MAE / Friedman MSE | `criterion='squared_error'` |
| 分割方式 | CART: 二叉分割 | $x_j \leq t$ ? |
| 剪枝 | 预剪枝 + 后剪枝 | `max_depth`, `ccp_alpha` |
| 训练复杂度 | $O(Np\log^2 N)$ | 排序特征 + 遍历分割点 |
| 预测复杂度 | $O(\text{depth})$ ≈ $O(\log N)$ | 从根到叶 |
| 特征重要性 | MDI (不纯度下降) | `.feature_importances_` |
| 过拟合风险 | 高（需限制树深度或剪枝） | `max_depth=5` |
| 缺失值 | sklearn ≥1.4 支持原生缺失值 | 自动处理 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📖 Docs: [scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html)
