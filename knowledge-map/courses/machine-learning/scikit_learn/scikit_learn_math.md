---
topic: scikit_learn
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Hastie et al., ESL, Ch.2-4,7,10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: Murphy, PML Vol.1, Ch.4-5,8-9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: scikit-learn User Guide — https://scikit-learn.org/stable/user_guide.html"
  - "💻 Source: scikit-learn/sklearn — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn"
expiry: 12m
status: current
---

# Scikit-Learn 数学基础

> 📚 Book: Hastie et al., [《Elements of Statistical Learning》](../../../textbooks/hastie_esl.pdf), Ch.2-4
> 📖 Docs: [sklearn User Guide – Mathematical formulation sections](https://scikit-learn.org/stable/user_guide.html)

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $X \in \mathbb{R}^{n \times p}$ | 特征矩阵 | Feature matrix | $n$ 样本 $\times$ $p$ 特征 |
| $\mathbf{y} \in \mathbb{R}^n$ | 目标向量 | Target vector | 回归: $\mathbb{R}$；分类: $\{0,1,\ldots,K-1\}$ |
| $\hat{y}$ | 预测值 | Prediction | — |
| $\mathbf{w} \in \mathbb{R}^p$ | 权重/系数向量 | Weights / `coef_` | — |
| $b$ | 截距 | Bias / `intercept_` | — |
| $\lambda$ / $\alpha$ | 正则化强度 | Regularization / `alpha` | $\geq 0$ |
| $C$ | SVM 正则化参数（$=1/\lambda$） | `C` parameter | $> 0$ |
| $K$ | 类别数 / 聚类数 | Number of classes/clusters | 正整数 |
| $k$ | 近邻数 | Number of neighbors | 正整数 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2

---


## 核心公式

### 公式 1: 线性回归的最小二乘解 (OLS)

**直觉：** 找到使预测值与真实值之间"距离平方和"最小的直线/超平面

$$
\hat{\mathbf{w}} = (X^\top X)^{-1} X^\top \mathbf{y}
$$

损失函数：$L(\mathbf{w}) = \|X\mathbf{w} - \mathbf{y}\|_2^2 = \sum_{i=1}^n (x_i^\top \mathbf{w} - y_i)^2$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq. 3.6
> 📖 Docs: [sklearn LinearRegression](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares)
> 💻 Source: `sklearn/linear_model/_base.py`

---

### 公式 2: Ridge 回归（L2 正则化）

**直觉：** 在 OLS 的基础上加"权重不能太大"的约束，防止过拟合

$$
\hat{\mathbf{w}} = (X^\top X + \alpha I)^{-1} X^\top \mathbf{y}
$$

损失函数：$L = \|X\mathbf{w} - \mathbf{y}\|_2^2 + \alpha \|\mathbf{w}\|_2^2$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq. 3.44
> 📖 Docs: [sklearn Ridge](https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression)

---

### 公式 3: Lasso 回归（L1 正则化）

**直觉：** L1 惩罚让某些权重精确为 0 → 自动特征选择

$$
L = \frac{1}{2n}\|X\mathbf{w} - \mathbf{y}\|_2^2 + \alpha \|\mathbf{w}\|_1
$$

无封闭解，用坐标下降法（Coordinate Descent）求解。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.3.4.2
> 📖 Docs: [sklearn Lasso](https://scikit-learn.org/stable/modules/linear_model.html#lasso)

---

### 公式 4: Logistic 回归

**直觉：** 线性模型 + Sigmoid → 输出概率；用交叉熵损失训练

$$
P(y=1|\mathbf{x}) = \sigma(\mathbf{w}^\top \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^\top \mathbf{x} + b)}}
$$

损失函数（交叉熵 + L2 正则化）：

$$
L = -\frac{1}{n}\sum_{i=1}^n \left[y_i \log \hat{p}_i + (1-y_i)\log(1-\hat{p}_i)\right] + \frac{1}{2C}\|\mathbf{w}\|_2^2
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4
> 📖 Docs: [sklearn LogisticRegression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
> 💻 Source: `sklearn/linear_model/_logistic.py`

---

### 公式 5: SVM 对偶问题

**直觉：** 找到最大间隔的分类超平面

原问题：$\min_{\mathbf{w},b} \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_i \xi_i$，$\text{s.t. } y_i(\mathbf{w}^\top x_i + b) \geq 1 - \xi_i$

对偶问题：

$$
\max_{\alpha} \sum_{i=1}^n \alpha_i - \frac{1}{2}\sum_{i,j} \alpha_i \alpha_j y_i y_j K(x_i, x_j)
$$

$$
\text{s.t. } 0 \leq \alpha_i \leq C,\; \sum_i \alpha_i y_i = 0
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.12
> 📖 Docs: [sklearn SVM](https://scikit-learn.org/stable/modules/svm.html#mathematical-formulation)

---

### 公式 6: K-Means 目标函数

**直觉：** 把数据分成 $K$ 组，每组内的点尽量靠近组中心

$$
J = \sum_{k=1}^K \sum_{x_i \in C_k} \|x_i - \mu_k\|^2
$$

算法交替执行：(1) 固定 $\mu_k$，将每个 $x_i$ 分配到最近的 $\mu_k$；(2) 固定分配，更新 $\mu_k = \frac{1}{|C_k|}\sum_{x_i \in C_k} x_i$。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.14.3.6
> 📖 Docs: [sklearn KMeans](https://scikit-learn.org/stable/modules/clustering.html#k-means)

---

### 公式 7: PCA（主成分分析）

**直觉：** 找到数据方差最大的方向，用少数几个方向表示高维数据

$$
\text{maximize } \mathbf{w}_1^\top S \mathbf{w}_1 \quad \text{s.t. } \|\mathbf{w}_1\| = 1
$$

其中 $S = \frac{1}{n}X_c^\top X_c$ 是中心化数据的协方差矩阵。解 = $S$ 的最大特征值对应的特征向量。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.14.5
> 📖 Docs: [sklearn PCA](https://scikit-learn.org/stable/modules/decomposition.html#pca)

---

### 公式 8: 交叉验证分数

**直觉：** 用 $K$ 折轮流验证估计泛化错误，比单次 train/test 分割更可靠

$$
\text{CV}(K) = \frac{1}{K} \sum_{k=1}^K \text{Score}(f_{-k}, \mathcal{D}_k)
$$

其中 $f_{-k}$ 是在排除第 $k$ 折后训练的模型，$\mathcal{D}_k$ 是第 $k$ 折数据。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.10
> 📖 Docs: [sklearn Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

---


## 公式关系图

```
线性回归 (OLS)
    │
    ├──→ + L2 正则化 ──→ Ridge
    │
    ├──→ + L1 正则化 ──→ Lasso (稀疏特征选择)
    │
    └──→ + Sigmoid 输出 ──→ Logistic 回归 (分类)
                                │
                                ├──→ 多类扩展 ──→ Softmax / OvR
                                │
                                └──→ 核化 ──→ SVM

KMeans (聚类)         PCA (降维)
    │                     │
    └──→ 交替优化          └──→ 特征分解

        交叉验证 (CV)
            │
            └──→ GridSearchCV ──→ 最优超参数
```

---


## 手算练习

### 练习 1: 2D 线性回归

**题目：** 数据 $\{(1,2), (2,3), (3,5)\}$，求线性回归系数 $\hat{w}, \hat{b}$

**解答：** $X = [1,2,3]^\top, y = [2,3,5]^\top$。加截距列 $X' = [[1,1],[1,2],[1,3]]$。$\hat{\theta} = (X'^\top X')^{-1} X'^\top y$。$X'^\top X' = [[3,6],[6,14]]$，$X'^\top y = [10, 23]$。逆矩阵 × 右边 → $\hat{b} = 1/3, \hat{w} = 3/2$。$\hat{y} = 1/3 + 1.5x$。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.3

### 练习 2: K-Means 一轮迭代

**题目：** 数据 $\{1, 2, 8, 9\}$，初始中心 $\mu_1=1, \mu_2=8$。执行一轮 K-Means。

**解答：** 分配：$1 \to C_1, 2 \to C_1, 8 \to C_2, 9 \to C_2$。更新：$\mu_1 = (1+2)/2 = 1.5, \mu_2 = (8+9)/2 = 8.5$。

> 📖 Docs: [sklearn KMeans](https://scikit-learn.org/stable/modules/clustering.html#k-means)

### 练习 3: 5-折 CV 计算

**题目：** 5 折 CV 得分分别为 $[0.85, 0.82, 0.88, 0.84, 0.86]$，求平均分和标准差

**解答：** 平均 = $0.85$，标准差 = $\sqrt{\frac{(0.85-0.85)^2 + \ldots}{5}} = 0.02$

> 📖 Docs: [sklearn Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

---


## 公式速查表

| 名称 | 公式 | sklearn 类 | 前置 |
|------|------|-----------|-------|
| OLS | $\hat{w} = (X^\top X)^{-1} X^\top y$ | `LinearRegression` | 线性代数 |
| Ridge | $+ \alpha\|w\|_2^2$ | `Ridge(alpha=)` | OLS |
| Lasso | $+ \alpha\|w\|_1$ | `Lasso(alpha=)` | OLS |
| Logistic | $\sigma(w^\top x + b)$ | `LogisticRegression(C=)` | OLS + Sigmoid |
| SVM | 最大间隔 + 核技巧 | `SVC(C=, kernel=)` | Logistic |
| KMeans | $\min \sum\|x_i - \mu_k\|^2$ | `KMeans(n_clusters=)` | 距离 |
| PCA | 特征分解 $S$ | `PCA(n_components=)` | 协方差 |
| CV | $\frac{1}{K}\sum \text{Score}_k$ | `cross_val_score(cv=)` | — |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf)
> 📖 Docs: [sklearn API](https://scikit-learn.org/stable/modules/classes.html)
