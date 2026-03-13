---
topic: svm
dimension: math
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Cortes & Vapnik ML 1995 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/svm/cortes_vapnik_1995_svm.pdf"
  - "📖 Paper: Boser Guyon Vapnik COLT 1992 — https://doi.org/10.1145/130385.130401"
  - "📚 Book: Hastie et al., ESL Ch.12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md"
  - "📚 Book: Bishop, PRML Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/data/mineru_output/bishop_prml/bishop_prml/auto/bishop_prml.md"
expiry: 12m
status: current
---

# SVM 数学基础

> 📖 Paper: Cortes & Vapnik, [Support-Vector Networks](../../../.documents/papers/svm/cortes_vapnik_1995_svm.pdf), ML 1995
> 📚 Book: Hastie et al., [ESL Ch.12](../../../data/mineru_output/hastie_esl/hastie_esl/auto/hastie_esl.md), Sec.12.2–12.3

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|------------|------|---------|
| $N$ | 训练样本数 | number of training samples | $N \geq 1$ |
| $p$ | 特征维度 | feature dimensionality | $p \geq 1$ |
| $x_i \in \mathbb{R}^p$ | 第 $i$ 个训练样本的特征向量 | feature vector | — |
| $y_i$ | 第 $i$ 个样本的类别标签 | class label | $\{-1, +1\}$ |
| $\beta \in \mathbb{R}^p$ | 超平面法向量（决定超平面方向）| weight vector | $\|\beta\| \neq 0$ |
| $\beta_0$ | 超平面截距（偏置项）| bias / intercept | $\mathbb{R}$ |
| $M$ | 间隔（超平面到最近样本点的距离）| margin | $M = 1/\|\beta\|$ |
| $\xi_i$ | 第 $i$ 个样本的松弛变量 | slack variable | $\xi_i \geq 0$ |
| $C$ | 正则化参数（惩罚误分类强度）| cost parameter | $C > 0$ |
| $\alpha_i$ | 对偶问题的第 $i$ 个拉格朗日乘子 | dual variable | $0 \leq \alpha_i \leq C$ |
| $K(x, x')$ | 核函数（高维内积的紧凑计算）| kernel function | $K: \mathbb{R}^p \times \mathbb{R}^p \to \mathbb{R}$ |
| $\gamma$ | RBF 核参数（控制高斯曲线宽度）| gamma | $\gamma > 0$ |
| $\epsilon$ | SVR 的不敏感区间宽度 | epsilon | $\epsilon \geq 0$ |

> 📚 Book: Hastie ESL, Sec.12.2 (符号定义); Bishop PRML Sec.7.1 (Eq.7.1–7.8)

---

## 核心公式

### 公式 1: 硬间隔 SVM 原始问题 (Primal — Separable Case)

**直觉：** 找一个超平面使两类样本最远离边界——最大化"安全区宽度" $2M = 2/\|\beta\|$，等价于最小化 $\|\beta\|$

$$
\min_{\beta, \beta_0} \frac{1}{2}\|\beta\|^2 \quad \text{s.t.} \quad y_i(x_i^T\beta + \beta_0) \geq 1, \quad i = 1, \ldots, N
$$

> 📖 Paper: Cortes & Vapnik 1995, Eq.(1–2); 📚 Hastie ESL, Sec.12.2 Eq.(12.4)

**参数解释：**
| 参数 | 含义 |
|------|------|
| $\frac{1}{2}\|\beta\|^2$ | 间隔宽度的倒数平方（最小化 = 最大化间隔）|
| $y_i(x_i^T\beta + \beta_0) \geq 1$ | 所有样本都在正确侧且离边界 ≥ 1 个单位 |

**推导过程：**

$$
\text{Step 1: 间隔定义} \quad M = \min_i \frac{y_i f(x_i)}{\|\beta\|}, \quad f(x) = x^T\beta + \beta_0
$$

$$
\text{Step 2: 令 } \|\beta\| = 1 \text{，约束变为 } y_i f(x_i) \geq M
$$

$$
\text{Step 3: 规范化（令 M·\|\beta\| = 1）} \Rightarrow \text{max } M = \text{min } \|\beta\|^2/2
$$

> 📚 Book: Hastie ESL, Sec.12.2 Eq.(12.3–12.4)

---

### 公式 2: 软间隔 SVM 原始问题 (Primal — Non-Separable)

**直觉：** 引入松弛变量 $\xi_i$ 允许样本越过边界，但要付出代价 $C\sum\xi_i$——C 越大越不允许越界

$$
\min_{\beta, \beta_0, \xi} \frac{1}{2}\|\beta\|^2 + C\sum_{i=1}^N \xi_i \quad \text{s.t.} \quad y_i(x_i^T\beta + \beta_0) \geq 1 - \xi_i, \quad \xi_i \geq 0
$$

> 📖 Paper: Cortes & Vapnik 1995, Sec.2; 📚 Hastie ESL, Sec.12.2.1 Eq.(12.8)

---

### 公式 3: 对偶问题 (Wolfe Dual)

**直觉：** 通过拉格朗日乘子法将原始问题转化为只包含 $\alpha_i$ 的最大化问题——计算只依赖内积 $x_i^Tx_{i'}$，为核技巧铺路

$$
\max_{\alpha} L_D = \sum_{i=1}^N \alpha_i - \frac{1}{2}\sum_{i=1}^N\sum_{i'=1}^N \alpha_i \alpha_{i'} y_i y_{i'} x_i^T x_{i'}
$$

$$
\text{s.t.} \quad 0 \leq \alpha_i \leq C, \quad \sum_{i=1}^N \alpha_i y_i = 0
$$

> 📚 Book: Hastie ESL, Sec.12.2.1 Eq.(12.13); Bishop PRML Sec.7.1.1 Eq.(7.10)

**推导过程（拉格朗日函数求极值）：**

$$
\text{Step 1: 构造 Lagrangian} \quad \mathcal{L}_P = \frac{1}{2}\|\beta\|^2 + C\sum_i\xi_i - \sum_i\alpha_i[y_i(x_i^T\beta+\beta_0)-(1-\xi_i)] - \sum_i\mu_i\xi_i
$$

$$
\text{Step 2: } \frac{\partial \mathcal{L}_P}{\partial \beta} = 0 \Rightarrow \hat{\beta} = \sum_{i=1}^N \alpha_i y_i x_i
$$

$$
\text{Step 3: }\frac{\partial \mathcal{L}_P}{\partial \beta_0} = 0 \Rightarrow \sum_{i=1}^N \alpha_i y_i = 0
$$

$$
\text{Step 4: 代入消去 } \beta, \xi_i \Rightarrow \text{得对偶目标函数 } L_D
$$

> 📚 Book: Hastie ESL, Sec.12.2.1 Eq.(12.9–12.13)

---

### 公式 4: KKT 条件与支持向量识别

**直觉：** KKT 互补松弛条件唯一确定哪些点是支持向量——$\alpha_i > 0$ 的点才对 $\hat{\beta}$ 有贡献

$$
\alpha_i[y_i(x_i^T\hat{\beta} + \hat{\beta}_0) - (1-\xi_i)] = 0, \quad \mu_i\xi_i = 0, \quad \forall i
$$

由此可知：
- $\alpha_i = 0$：非支持向量，$y_i f(x_i) > 1$，不参与计算 $\hat{\beta}$
- $0 < \alpha_i < C$：margin 上的支持向量，$\xi_i = 0$，用于求 $\hat{\beta}_0$
- $\alpha_i = C$：违反 margin 的支持向量，$\xi_i > 0$（可能误分类）

> 📚 Book: Hastie ESL, Sec.12.2.1 Eq.(12.14–12.16)

---

### 公式 5: 核技巧 (Kernel Trick)

**直觉：** 将对偶问题中所有内积 $x_i^Tx_{i'}$ 替换为核函数 $K(x_i, x_{i'})$——等价于在高维（甚至无限维）特征空间中做 SVM，无需显式计算映射

$$
K(x, x') = \langle h(x), h(x') \rangle \implies L_D = \sum_i\alpha_i - \frac{1}{2}\sum_{i,i'}\alpha_i\alpha_{i'}y_iy_{i'}K(x_i,x_{i'})
$$

$$
\hat{f}(x) = \sum_{i=1}^N \hat{\alpha}_i y_i K(x, x_i) + \hat{\beta}_0
$$

**三种常用核：**

| 核 | 公式 | 参数 |
|----|------|------|
| 多项式核 | $K(x,x') = (1 + x^Tx')^d$ | $d$（次数）|
| RBF/Gaussian 核 | $K(x,x') = \exp(-\gamma\|x-x'\|^2)$ | $\gamma$ |
| Sigmoid 核（类神经网络）| $K(x,x') = \tanh(\kappa_1 x^Tx'+\kappa_2)$ | $\kappa_1, \kappa_2$ |

> 📖 Paper: Boser, Guyon & Vapnik 1992; 📚 Hastie ESL, Sec.12.3 Eq.(12.21–12.22)

---

### 公式 6: 铰链损失等价形式 (Hinge Loss)

**直觉：** SVM 原始问题等价于最小化"铰链损失 + L2 正则"，$\lambda = 1/C$ — 这与逻辑回归的"对数损失 + L2 正则"形式完全平行

$$
\min_{\beta_0,\beta} \sum_{i=1}^N [1 - y_i f(x_i)]_+ + \frac{\lambda}{2}\|\beta\|^2, \quad [z]_+ = \max(0, z)
$$

> 📚 Book: Hastie ESL, Sec.12.3.2 Eq.(12.25)

---

## 公式关系图

```
硬间隔原始问题 (公式 1)
        │ 加入松弛变量 ξ_i
        ▼
软间隔原始问题 (公式 2) ─────────────→ 铰链损失等价形式 (公式 6)
        │ 拉格朗日 + 求偏导
        ▼
对偶问题 (公式 3)
        │ KKT 互补松弛
        ▼
KKT 条件 → 识别支持向量 (公式 4)
        │ 替换内积为核函数
        ▼
核技巧 (公式 5) → f(x) = Σ α_i y_i K(x,x_i) + β_0
```

> 📚 Book: Hastie ESL, Sec.12.2–12.3 (完整推导链)

---

## 手算练习

### 练习 1: 硬间隔 SVM — 找最优超平面

**题目：** 2D 中有 3 个训练点：$(1,1,+1)$, $(2,1,+1)$, $(0,0,-1)$（格式 $(x_1,x_2,y)$）。求最优超平面 $w_1 x_1 + w_2 x_2 + b = 0$。

**解答步骤：**

1. 正类支持向量 $(1,1)$ 和负类支持向量 $(0,0)$，由对称性猜测 $w_1=w_2=w$
2. 由约束 $w(1+1)+b \geq 1$ 和 $-(w\cdot0+b) \geq 1$ → $b \leq -1$，取 $b = -1$
3. $2w - 1 = 1 \Rightarrow w = 1$
4. 超平面：$x_1 + x_2 - 1 = 0$，间隔 $M = 1/\sqrt{2}$

> 📚 Book: Hastie ESL, Sec.4.5.2 (Optimal Separating Hyperplane 示例)

### 练习 2: 核函数展开 — 多项式核

**题目：** 设 $x = (X_1, X_2)$，验证 $K(x,x') = (1 + x^Tx')^2$ 对应的隐式特征映射。

**解答步骤：**

1. 展开：$K(x,x') = (1 + X_1X_1' + X_2X_2')^2$
2. $= 1 + 2X_1X_1' + 2X_2X_2' + X_1^2X_1'^2 + X_2^2X_2'^2 + 2X_1X_2X_1'X_2'$
3. 对应 $h(x) = (1, \sqrt{2}X_1, \sqrt{2}X_2, X_1^2, X_2^2, \sqrt{2}X_1X_2)^T$（6维）
4. 验证：$h(x)^Th(x') = K(x,x')$ ✓

> 📚 Book: Hastie ESL, Sec.12.3 Eq.(12.23–12.24)

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 硬间隔原始 | $\min \frac{1}{2}\|\beta\|^2$，s.t. $y_if(x_i)\geq1$ | 线性可分 SVM | 无 |
| 软间隔原始 | $\min \frac{1}{2}\|\beta\|^2 + C\sum\xi_i$ | 线性不可分 SVM | 公式 1 |
| 对偶目标 | $\max \sum\alpha_i - \frac{1}{2}\sum\sum\alpha_i\alpha_{i'}y_iy_{i'}x_i^Tx_{i'}$ | 实际求解 | 公式 2 |
| 解的表示 | $\hat{\beta} = \sum\alpha_iy_ix_i$ | 找超平面 | 公式 3 |
| 核替换 | $x_i^Tx_{i'} \to K(x_i,x_{i'})$ | 非线性 SVM | 公式 3 |
| 决策函数 | $\hat{f}(x) = \sum\hat{\alpha}_iy_iK(x,x_i)+\hat{\beta}_0$ | 预测 | 公式 5 |
| 铰链损失 | $\sum[1-y_if(x_i)]_+ + \frac{\lambda}{2}\|\beta\|^2$ | 损失函数视角 | 公式 2 |
| RBF 核 | $K(x,x')=\exp(-\gamma\|x-x'\|^2)$ | 最常用核 | 公式 5 |

> 📖 Paper: Cortes & Vapnik 1995; 📚 Hastie ESL Sec.12.2–12.3
