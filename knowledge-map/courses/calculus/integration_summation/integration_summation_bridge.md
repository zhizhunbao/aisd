---
topic: integration_summation
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5-6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Bishop, PRML, Ch.1-2,10-11 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# 积分与求和 衔接与扩展

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5-6

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 微分 (Differentiation) | 积分是微分的逆运算；微积分基本定理连接两者 | [differentiation_map.md](../differentiation/differentiation_map.md) |
| ← 前置 | 极限 (Limits) | 积分定义依赖极限（黎曼和 → 极限） | — |
| ← 前置 | 级数 (Series) | 无穷级数的收敛性是理解积分近似的基础 | — |
| → 后续 | 卷积 (Convolution) | 卷积是积分的特殊应用 $f*g = \int f(\tau)g(t-\tau)\,d\tau$ | [convolution_map.md](../convolution/convolution_map.md) |
| → 后续 | 概率分布 (Probability Distributions) | 归一化、CDF、期望都依赖积分 | — |
| → 后续 | 贝叶斯推断 (Bayesian Inference) | 边缘化 $p(\mathcal{D}) = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta$ | — |
| → 后续 | 蒙特卡洛方法 (Monte Carlo Methods) | 当积分不可解析时的近似方法 | — |
| → 后续 | 变分推断 (Variational Inference) | 把积分转化为优化问题 | — |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5-6

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| 微分 (Differentiation) | 导数 $f'(x)$ | 微积分基本定理：$\int_a^b f(x)\,dx = F(b)-F(a)$，其中 $F'=f$ |
| 极限 (Limits) | $\lim_{n\to\infty}$ | 黎曼积分定义为黎曼和的极限 |
| 集合论 (Set Theory) | 可数/不可数集 | 求和用于可数集，积分用于不可数集 |
| 线性代数 | 矩阵迹 $\text{tr}(A)$ | 迹是对角元素的求和 $\sum_i a_{ii}$ |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.2 (线性代数), Ch.5 (微积分)

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|----------------|
| 概率论 | 定积分 $\int_a^b p(x)\,dx$ | PDF 归一化、CDF 定义、概率计算 |
| 期望与方差 | $E[X] = \int xp(x)\,dx$ | 损失函数的期望风险、模型评估 |
| 贝叶斯推断 | 边缘化 $\int p(\mathcal{D}|\theta)p(\theta)\,d\theta$ | 模型证据、后验预测分布 |
| 卷积 | 积分 $\int f(\tau)g(t-\tau)\,d\tau$ | CNN 中的卷积层、信号处理 |
| 信息论 | $H(X) = -\int p(x)\log p(x)\,dx$ | 熵、KL 散度、互信息 |
| 蒙特卡洛方法 | 积分→求和近似 | MCMC、变分推断、策略梯度 |
| 损失函数 | $L = \sum_{i=1}^N \ell_i$ | 交叉熵、MSE 的计算 |
| Taylor 展开 | 无穷级数 $\sum a_n x^n$ | 函数近似、激活函数分析 |

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1-2, 10-11
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化 |
|------|-------------|-------------|------|
| 面积计算 | 穷竭法（逐案设计多边形逼近） | 微积分（通用框架 $F(b)-F(a)$） | 从特殊到通用 |
| 积分计算 | 解析求原函数 | 数值积分 + MC 近似 | 从精确到近似（为了可计算性） |
| 高维积分 | 确定性网格（维度诅咒） | 蒙特卡洛采样 | 用随机性打破维度壁垒 |
| 贝叶斯积分 | 共轭先验（保证解析积分） | 变分推断（把积分变优化） | 从数学约束到计算自由 |
| 求和符号 | 手动逐项累加 | 向量化 `np.sum()`，GPU 并行 | 从串行到并行 |

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.2 (共轭先验), Ch.10 (变分推断)

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [《PRML》Ch.10-11](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 变分推断 + MCMC 的经典讲解 | ⭐⭐⭐⭐ |
| [《Information Theory》](../../../textbooks/mackay_information_theory.pdf) | 📚 教科书 | 积分在信息论中的角色 | ⭐⭐⭐⭐ |
| [《MML》Ch.6](../../../textbooks/deisenroth_mml.pdf) | 📚 教科书 | 概率分布中积分的系统讲解 | ⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| 卷积知识库 [convolution_map.md](../convolution/convolution_map.md) | 积分的特殊应用 vs 一般积分 | 学完积分基础后 |
| 勒贝格积分 (Lebesgue) vs 黎曼积分 | 积分定义的推广 | 需要处理更"病态"的函数时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [《Deep Learning》Ch.17-20](../../../textbooks/goodfellow_deep_learning.pdf) | MC 方法在深度生成模型中的应用 | 学贝叶斯深度学习时 |
| [《PRML》Ch.13](../../../textbooks/bishop_prml.pdf) | 顺序蒙特卡洛 / 粒子滤波 | 学时间序列贝叶斯推断时 |

> 📚 Book: 综合以上教科书

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 数学基础 | 2 | [convolution](../convolution/), [differentiation](../differentiation/) | 卷积是积分的特殊形式 / 微分是积分的逆运算 |
| 深度学习 | 3 | [cnn_map.md](../../deep-learning/cnn/cnn_map.md) | 卷积层依赖积分/求和概念 |
| 机器学习 | 4 | [naive_bayes](../../ml/naive_bayes/), [svm](../../ml/svm/) | 概率模型中的积分/求和应用 |
