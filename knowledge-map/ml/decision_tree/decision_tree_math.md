---
topic: decision_tree
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Hastie et al., ESL Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., ISLR Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📚 Book: Bishop, PRML Ch.14.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, PML1 Ch.18 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
expiry: 12m
status: current
---

# Decision Tree 数学基础

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8.1

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------| 
| $N$ | 样本数 | number of samples | $N \geq 1$ |
| $p$ | 特征维度 | number of features | $p \geq 1$ |
| $K$ | 类别数 | number of classes | $K \geq 2$（分类） |
| $R_m$ | 第 $m$ 个区域/叶子 | region / leaf | $m = 1,...,|T|$ |
| $|T|$ | 叶子节点数 | number of terminal nodes | $|T| \geq 1$ |
| $N_m$ | 区域 $R_m$ 中的样本数 | samples in region $m$ | $N_m \leq N$ |
| $\hat{p}_{mk}$ | 区域 $m$ 中类别 $k$ 的比例 | class proportion | $\sum_k \hat{p}_{mk} = 1$ |
| $\hat{c}_m$ | 区域 $m$ 的预测值 | predicted value | 多数类（分类）/均值（回归） |
| $j$ | 分割特征索引 | splitting feature | $j \in \{1,...,p\}$ |
| $t$ | 分割阈值 | split threshold | $t \in \mathbb{R}$ |
| $\alpha$ | 代价复杂度参数 | complexity parameter | $\alpha \geq 0$ |
| $G(m)$ | 节点 $m$ 的 Gini 不纯度 | Gini impurity | $[0, 1-1/K]$ |
| $H(m)$ | 节点 $m$ 的信息熵 | entropy | $[0, \log_2 K]$ |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

---


## 核心公式

### 公式 1: Gini 不纯度

**直觉：** 从节点中随机取两个样本，它们属于不同类别的概率。Gini=0 表示完全纯净

$$
G(m) = 1 - \sum_{k=1}^K \hat{p}_{mk}^2 = \sum_{k=1}^K \hat{p}_{mk}(1 - \hat{p}_{mk})
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq.9.17

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $\hat{p}_{mk}$ | 节点 $m$ 中类别 $k$ 的占比 | 10 个样本 6 正 4 负 → $\hat{p}_1=0.6$ |

**关键性质：**
- 二分类时: $G = 2\hat{p}(1-\hat{p})$，最大值 0.5（当 $\hat{p}=0.5$）
- 等价于: 随机分配标签的期望误分类率
- 近似: $G \approx H$ 的二阶泰勒展开

---

### 公式 2: 信息熵

**直觉：** 描述一个节点中标签的"不确定性"。熵越大越"乱"，越小越"纯"

$$
H(m) = -\sum_{k=1}^K \hat{p}_{mk} \log_2 \hat{p}_{mk}
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq.9.18

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $\hat{p}_{mk}$ | 节点 $m$ 中类别 $k$ 的占比 | 全是正类 → $H=0$ |

**Gini vs Entropy 对比（二分类）：**

```
不纯度 ↑
  |    Entropy ___________
  |   /   \.  .  .  .  .\
  |  / Gini ·.  .  .  .  ·\
  | /  / Misclass     \   \
  |/ /                 \ \  \
  ──────────────────────────→ p
  0        0.5          1
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Fig.9.3

---

### 公式 3: 信息增益（分割准则）

**直觉：** 分割前后不纯度下降了多少——下降越多说明分割越好

$$
\Delta I(j, t) = I(\text{parent}) - \frac{N_L}{N}I(\text{left}) - \frac{N_R}{N}I(\text{right})
$$

其中 $I$ 可以是 Gini 或 Entropy。CART 的贪心策略：

$$
(j^*, t^*) = \arg\max_{j, t} \Delta I(j, t)
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq.9.13

**推导过程：**

$$
\text{Step 1: 遍历特征 } j \in \{1,...,p\}
$$
$$
\text{Step 2: 对特征 } j \text{, 将样本按 } x_j \text{ 排序}
$$
$$
\text{Step 3: 遍历相邻值之间的阈值 } t
$$
$$
\text{Step 4: 按 } x_j \leq t \text{ 拆分为左右子节点}
$$
$$
\text{Step 5: 计算 } \Delta I \text{, 取最大的 } (j^*, t^*)
$$

---

### 公式 4: 回归树分割准则 (MSE)

**直觉：** 找到使分割后两个区域内方差最小的特征和阈值

$$
\min_{j,t} \left[ \min_{c_L} \sum_{x_i \in R_L(j,t)} (y_i - c_L)^2 + \min_{c_R} \sum_{x_i \in R_R(j,t)} (y_i - c_R)^2 \right]
$$

最优预测值是区域均值：

$$
\hat{c}_L = \frac{1}{N_L}\sum_{x_i \in R_L} y_i, \quad \hat{c}_R = \frac{1}{N_R}\sum_{x_i \in R_R} y_i
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq.9.13

---

### 公式 5: 代价复杂度剪枝

**直觉：** 在树的预测准确性和复杂度之间做权衡——$\alpha$ 控制"每多一个叶子要付出多少代价"

$$
R_\alpha(T) = R(T) + \alpha |T|
$$

- $R(T)$: 树 $T$ 的训练误差（误分类率或 MSE）
- $|T|$: 叶子节点数（树的复杂度）
- $\alpha$: 复杂度参数（越大越鼓励简单的树）

对于每个 $\alpha$，存在唯一的最优子树 $T(\alpha)$：

$$
T(\alpha) = \arg\min_{T \preceq T_{\max}} R_\alpha(T)
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq.9.15-9.16

**推导过程：weakest link pruning**

$$
\text{Step 1: 从完全树 } T_{\max} \text{ 开始}
$$
$$
\text{Step 2: 对每个内部节点 } t \text{, 计算 }
$$
$$
g(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}
$$
$$
\text{Step 3: } g(t) \text{ 是删掉子树 } T_t \text{ 后每个叶子节点的平均误差增量}
$$
$$
\text{Step 4: 剪掉 } g(t) \text{ 最小的节点（"最弱"的分支）}
$$
$$
\text{Step 5: 重复直到只剩根节点 → 得到一系列嵌套子树}
$$
$$
\text{Step 6: 用交叉验证选择最优 } \alpha
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2.2

---

### 公式 6: 增益率 (C4.5)

**直觉：** 对信息增益做归一化，惩罚取值过多的特征

$$
GR(j) = \frac{IG(j)}{H_{\text{split}}(j)}
$$

其中分割信息量 (Split Information)：

$$
H_{\text{split}}(j) = -\sum_{v} \frac{N_v}{N}\log_2\frac{N_v}{N}
$$

$N_v$ 是特征 $j$ 取值为 $v$ 的样本数

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.18.1

---

### 公式 7: 特征重要性 (MDI)

**直觉：** 特征对降低不纯度的总贡献

$$
\text{Importance}(j) = \sum_{t: \text{node splits on } j} \frac{N_t}{N} \Delta I_t
$$

其中 $N_t$ 是节点 $t$ 的样本数，$\Delta I_t$ 是该节点的不纯度下降。最终归一化使所有特征重要性之和为 1。

> 📖 Docs: [scikit-learn Feature Importance](https://scikit-learn.org/stable/modules/tree.html#feature-importance-evaluation)

---


## 公式关系图

```
Gini 不纯度 (公式1) ──┐
                       ├──→ 分割准则 (公式3: 信息增益)
信息熵 (公式2) ────────┘        │
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
           分类树分割                   回归树分割 (公式4: MSE)
                    │                       │
                    └───────────┬───────────┘
                                │
                    代价复杂度剪枝 (公式5)
                                │
                    增益率 (公式6, C4.5 专用)
                                │
                    特征重要性 (公式7: MDI)
```

---


## 手算练习

### 练习 1: 计算 Gini 不纯度

**题目：** 一个节点有 10 个样本：6 正 4 负。计算 Gini 不纯度。

**解答步骤：**

1. $\hat{p}_+ = 6/10 = 0.6$, $\hat{p}_- = 4/10 = 0.4$
2. $G = 1 - (0.6^2 + 0.4^2) = 1 - (0.36 + 0.16) = 1 - 0.52 = 0.48$
3. 也可用: $G = 2 \times 0.6 \times 0.4 = 0.48$ ✓

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### 练习 2: 选择最优分割

**题目：** 10 个样本，特征 $x$ 和标签 $y$ 如下。选择最优 Gini 分割。

| 样本 | x | y |
|------|---|---|
| 1-3 | 1 | + |
| 4-5 | 2 | + |
| 6-7 | 3 | - |
| 8 | 4 | + |
| 9-10 | 5 | - |

**解答步骤：**

1. 父节点 Gini: 6正4负 → $G_p = 0.48$
2. 阈值 $t=2.5$: 左5个(3正2负), 右5个(3正2负) → $G_L = G_R = 1-(9/25+4/25) = 0.48$, $\Delta G = 0.48 - 0.48 = 0$
3. 阈值 $t=1.5$: 左3个(3正0负), 右7个(3正4负) → $G_L = 0$, $G_R = 1-(9/49+16/49) = 0.490$, $\Delta G = 0.48 - 3/10 \times 0 - 7/10 \times 0.490 = 0.137$
4. 最优分割: $t = 1.5$, $\Delta G = 0.137$

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8.1

### 练习 3: 信息增益计算

**题目：** 父节点有 8 个样本 (4+4-)。分割后左子节点 3+1-，右子节点 1+3-。计算信息增益。

**解答步骤：**

1. $H_p = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1.0$
2. $H_L = -(3/4)\log_2(3/4) - (1/4)\log_2(1/4) = 0.811$
3. $H_R = -(1/4)\log_2(1/4) - (3/4)\log_2(3/4) = 0.811$
4. $IG = 1.0 - (4/8)\times 0.811 - (4/8)\times 0.811 = 1.0 - 0.811 = 0.189$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置 |
|------|------|------|---------| 
| Gini | $1 - \sum p_k^2$ | 分类分割准则 | 无 |
| Entropy | $-\sum p_k \log_2 p_k$ | 分类分割准则 | 无 |
| 信息增益 | $I_p - \frac{N_L}{N}I_L - \frac{N_R}{N}I_R$ | 选择最优分割 | Gini/Entropy |
| MSE 分割 | $\min_{j,t}[\sum(y-\bar{y}_L)^2 + \sum(y-\bar{y}_R)^2]$ | 回归分割 | 无 |
| 剪枝 | $R_\alpha(T) = R(T) + \alpha|T|$ | 防过拟合 | 信息增益 |
| 增益率 | $IG / H_{\text{split}}$ | C4.5 修正 | 信息增益 |
| 特征重要性 | $\sum (N_t/N)\Delta I_t$ | 特征排序 | 信息增益 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8.1
