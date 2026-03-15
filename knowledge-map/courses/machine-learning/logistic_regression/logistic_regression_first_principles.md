---
topic: logistic_regression
dimension: first_principles
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Cox, 'The Regression Analysis of Binary Sequences', JRSS-B 1958 — https://doi.org/10.1111/j.2517-6161.1958.tb00292.x"
  - "📚 Book: Bishop, PRML Ch.4.2-4.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Hastie et al., ESL Ch.4.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: Murphy, PML1 Ch.10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Deisenroth et al., MML Ch.12.2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
expiry: 12m
status: current
---

# Logistic Regression 第一性原理

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.2-4.3
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4

---


## 核心问题链

> 用"5 个为什么"式的递归追问，从表面功能一路追到不可再分的基本事实。

### 问题链

1. **Logistic Regression 在做什么？** → 给定输入特征，输出样本属于各类别的概率
2. **为什么要输出概率而不是直接给类别？** → 因为现实决策需要不确定性信息——概率量化了"我有多确定"，可用于风险评估和排序
3. **为什么用 sigmoid 函数来产生概率？** → 因为当类条件分布属于指数族时，贝叶斯后验概率的函数形式恰好是 sigmoid（这不是人为选择，而是数学必然）
4. **指数族导出 sigmoid 的根基是什么？** → 贝叶斯定理 + 指数族分布的标准形式 $p(\mathbf{x}|\mathcal{C}_k) = h(\mathbf{x})\exp(\boldsymbol{\eta}^T\mathbf{T}(\mathbf{x}) - A(\boldsymbol{\eta}))$ → log-odds 是特征的线性函数
5. **这个根基能否继续拆分？** → 不能：贝叶斯定理是概率论基本公理的直接推论，指数族是满足充分统计量条件的最大分布族 → **到达公理**

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.2

---


## 公理与基本假设

> 列出本技术赖以成立的**不可再分的基本事实**。这些是"如果它们不成立，整个技术就崩塌"的根基。

### 公理 1: 贝叶斯定理

**陈述：** 后验概率 = 似然 × 先验 / 证据，即 $P(Y|X) = \frac{P(X|Y)P(Y)}{P(X)}$

**白话：** 看到数据之后，我对类别的信念 = 数据在该类别下出现的可能性 × 我原来的信念 / 数据出现的总可能性

**来源：** 概率论基本公理（Kolmogorov 公理 + 条件概率定义）的直接推论。这不是假设，是**数学定理**。

**可验证性：** 始终成立——只要概率的定义符合 Kolmogorov 公理。只有在概率定义不明确时（如主观概率解释争议）才有哲学层面的讨论。

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2.3

### 公理 2: 对数几率线性性假设 (Log-Odds Linearity)

**陈述：** 类别后验概率的 log-odds 是特征的线性函数：$\log\frac{P(Y=1|\mathbf{x})}{P(Y=0|\mathbf{x})} = \mathbf{w}^T\mathbf{x} + b$

**白话：** 每个特征对"正类 vs 负类的对数几率"的贡献是相加的、等比的——特征之间没有交互效应，每个特征独立地"投票"

**来源：** 当类条件分布 $P(\mathbf{x}|Y=k)$ 属于指数族分布时，这个线性性是**数学推导**的结论（Bishop PRML Ch.4.2 定理）。但在实际使用中，它被当作**模型假设**——我们假设 log-odds 近似线性

**可验证性：** 
- **成立条件**：类条件分布是高斯（等协方差）、二项式、多项式等指数族分布
- **不成立条件**：当真实决策边界是非线性的（如 XOR 问题、图像分类）；当特征间存在强交互效应

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.2, Eq.4.57-4.58
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4

### 公理 3: 最大似然原理 (Maximum Likelihood Principle)

**陈述：** 最好的参数是使观测数据出现概率最大的参数：$\hat{\boldsymbol{\theta}} = \arg\max_{\boldsymbol{\theta}} P(\mathcal{D}|\boldsymbol{\theta})$

**白话：** 在所有可能的参数中，选择让"已经发生的数据"看起来"最不意外"的那组参数

**来源：** 统计学基本原理，由 R.A. Fisher 在 1920 年代系统化。MLE 在大样本下具有一致性、渐近正态性和渐近有效性

**可验证性：**
- **成立条件**：数据量足够大时 MLE 近似最优；模型正确指定时
- **不成立条件**：小样本时可能过拟合（→ 加正则化 = MAP 估计）；模型严重错误指定时

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.4.2

### 公理 4: 样本独立同分布 (i.i.d.)

**陈述：** 训练样本 $\{(\mathbf{x}_i, y_i)\}_{i=1}^N$ 是独立同分布的：$P(\mathcal{D}) = \prod_{i=1}^N P(\mathbf{x}_i, y_i)$

**白话：** 每个样本是独立抽到的，没有一个样本的出现会影响另一个；而且所有样本来自同一个数据生成过程

**来源：** 统计学建模的标准假设。独立性让似然函数可以分解为乘积形式，对数似然变成求和形式——这是用梯度优化的前提

**可验证性：**
- **成立条件**：随机抽样、无时间依赖、无空间相关性
- **不成立条件**：时间序列数据（自相关）、家族/聚类数据（组内相关）、因果反馈数据

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.4.1

---


## 从公理到技术的推导链

> 展示如何**仅从上述公理出发**，一步步逻辑推导出完整的技术方案。
> 每一步必须标注"用了哪个公理"，不允许跳步或引入未声明的假设。

### Step 1: {从公理 1 + 公理 2} → {模型函数形式}

**推理：** 
由贝叶斯定理（公理 1），后验概率为 $P(Y=1|\mathbf{x}) = \frac{P(\mathbf{x}|Y=1)P(Y=1)}{P(\mathbf{x})}$。

由 log-odds 线性性假设（公理 2），$\log\frac{P(Y=1|\mathbf{x})}{P(Y=0|\mathbf{x})} = \mathbf{w}^T\mathbf{x} + b$。

**结果：** 解出 $P(Y=1|\mathbf{x}) = \sigma(\mathbf{w}^T\mathbf{x} + b) = \frac{1}{1+\exp(-\mathbf{w}^T\mathbf{x}-b)}$

→ Sigmoid 函数形式不是人为选择的，而是从公理 1 + 公理 2 推导出来的**唯一解**

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.2

### Step 2: {结合 Step 1 + 公理 3 + 公理 4} → {交叉熵损失函数}

**推理：** 
由 i.i.d. 假设（公理 4），似然函数分解为乘积：$L(\mathbf{w}) = \prod_{i=1}^N P(y_i|\mathbf{x}_i;\mathbf{w})$

由 Step 1 的模型形式 + Bernoulli 分布：$P(y_i|\mathbf{x}_i) = \hat{p}_i^{y_i}(1-\hat{p}_i)^{1-y_i}$

由 MLE 原理（公理 3），最大化对数似然 = 最小化负对数似然

**结果：** $\mathcal{L}(\mathbf{w}) = -\frac{1}{N}\sum_{i=1}^N[y_i\log\hat{p}_i + (1-y_i)\log(1-\hat{p}_i)]$ = 交叉熵损失

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10.2

### Step 3: {从 Step 2} → {梯度和 Hessian}

**推理：** 
对交叉熵损失求 $\mathbf{w}$ 的偏导，利用 sigmoid 导数性质 $\sigma'(z) = \sigma(z)(1-\sigma(z))$（公理 2 的推论）

**结果：** 
- 梯度：$\nabla\mathcal{L} = \frac{1}{N}\mathbf{X}^T(\hat{\mathbf{p}} - \mathbf{y})$
- Hessian：$\mathbf{H} = \frac{1}{N}\mathbf{X}^T\mathbf{W}\mathbf{X} \succeq 0$ → **损失是凸函数**

凸性 → 任何梯度方法都能找到全局最优解

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4

### Step 4: {从 Step 3} → {IRLS / 梯度下降优化}

**推理：** 
将 Newton 更新 $\mathbf{w}^+ = \mathbf{w} - \mathbf{H}^{-1}\nabla\mathcal{L}$ 代入到 Step 3 的梯度和 Hessian 中

**结果：** 
得到 IRLS 算法：$\mathbf{w}^{(t+1)} = (\mathbf{X}^T\mathbf{W}\mathbf{X})^{-1}\mathbf{X}^T\mathbf{W}\mathbf{z}$ — 每一步是一个**加权最小二乘**问题

这就是完整的 Logistic Regression 技术方案

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq.4.99-4.100

### 推导链全景图

```
公理 1 (贝叶斯定理) ────┐
                        ├──→ Step 1: sigmoid 模型形式 ──┐
公理 2 (log-odds 线性) ──┘                              │
                                                        ├──→ Step 2: 交叉熵损失
公理 3 (MLE) ────────────────────────────────────────────┤
                                                        │
公理 4 (i.i.d.) ─────────────────────────────────────────┘
                                                           │
                                            Step 3: 梯度 + Hessian (凸性证明)
                                                           │
                                            Step 4: IRLS / 梯度下降 → 完整 LR
```

---


## 如果公理不成立？

> 逐个"拔掉"公理，分析技术会如何崩塌。这揭示了技术的**真正边界**。

### 公理 1 失效：贝叶斯定理不适用

**如果不成立：** 贝叶斯定理是概率论的定理，只有在放弃概率框架时才"不成立"——例如用 Dempster-Shafer 证据理论或模糊逻辑

**技术后果：** LR 的概率解释失去基础。输出值不再有"属于正类的概率"的含义——但作为一个**评分函数**仍然可用（就像 SVM 的决策值）

**替代方案：** SVM（不依赖概率框架）、证据理论方法、模糊分类器

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2

### 公理 2 失效：log-odds 与特征非线性

**如果不成立：** 真实决策边界是非线性的（如图像分类、XOR 问题）

**技术后果：** LR 的线性模型无法捕捉真实模式，训练损失无法降低，欠拟合。这是 LR 最常见的失效模式

**替代方案：**
- 特征工程：手动添加多项式特征、交互项 → $\mathbf{x}' = [x_1, x_2, x_1^2, x_1 x_2, ...]$
- 核化 LR：隐式映射到高维空间
- 神经网络：自动学习非线性特征 → 本质上是多层非线性变换后接 LR
- 决策树/随机森林：天然处理非线性

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4 — "linear boundary limitation"
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.5.7

### 公理 3 失效：MLE 不是好的估计方法

**如果不成立：** 小样本时 MLE 过拟合；完全分离时 MLE 不收敛（参数 → ∞）

**技术后果：** 模型系数不稳定、方差大、泛化性能差

**替代方案：**
- MAP 估计 = MLE + 正则化（L2 对应高斯先验，L1 对应拉普拉斯先验）
- 完全贝叶斯方法：对参数积分而非点估计（计算密集但最完备）
- Firth 惩罚似然：专门解决完全分离问题

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10.2

### 公理 4 失效：样本不是 i.i.d.

**如果不成立：** 时间序列数据（自相关）、聚类数据（组内相关）、在线学习（分布漂移）

**技术后果：** 似然函数分解为乘积的前提不成立 → 参数估计有偏/标准误失效 → 置信区间和假设检验不可信

**替代方案：**
- 时间序列：GEE（广义估计方程）、混合效应模型
- 聚类数据：多层 LR（随机效应模型）
- 分布漂移：在线学习 + 滑动窗口 LR

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
| 贝叶斯定理 | 后验 = 似然×先验/证据 | 概率论框架内始终成立 | 概率解释失效（但评分仍可用） |
| Log-odds 线性性 | logit(P) 是 X 的线性函数 | 指数族类条件分布 / 近似线性 | 欠拟合，需非线性方法 |
| MLE | 选择使数据最可能的参数 | 大样本、模型正确指定 | 过拟合/不收敛 → 加正则化 |
| i.i.d. | 样本独立且来自同一分布 | 随机抽样、无时间/空间相关 | 参数估计有偏、推断失效 |

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.2-4.3
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4
