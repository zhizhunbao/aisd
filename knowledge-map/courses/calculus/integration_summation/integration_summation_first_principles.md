---
topic: integration_summation
dimension: first_principles
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Bishop, PRML, Ch.1-2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Grinstead & Snell, Introduction to Probability — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/grinstead_snell_probability.pdf"
expiry: 12m
status: current
---

# 积分与求和 第一性原理

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2

---


## 核心问题链

> 用"5 个为什么"式的递归追问，从表面功能一路追到不可再分的基本事实。

### 问题链

1. **积分/求和在做什么？** → 计算离散值的累加（求和）或连续函数在区间上的"累积量"（积分）
2. **为什么要做累积？** → 因为很多量（面积、概率、期望）不是"点"上的值，而是区间/区域上的"总效果"
3. **为什么"总效果"不能直接测量？** → 因为连续量有无穷多个点，不能逐个测量；离散量可能有大量项，需要系统化方法
4. **处理无穷多个无穷小量的根基是什么？** → **极限的存在性**——$\lim_{n\to\infty} \sum_{i=1}^n f(x_i) \Delta x_i$ 必须收敛到确定的值
5. **极限为什么能给出确定值？** → 因为实数系的**完备性公理 (Completeness Axiom)**——每个有界单调序列必有极限。这是**不可再分的公理**

> 📚 Book: 实分析基础（实数完备性公理）

---


## 公理与基本假设

> 列出本技术赖以成立的**不可再分的基本事实**。这些是"如果它们不成立，整个技术就崩塌"的根基。

### 公理 1: 实数完备性 (Completeness of Real Numbers)

**陈述：** 实数系中，每个非空有上界的子集必有上确界（最小上界）。等价表述：每个柯西序列都收敛。

**白话：** 实数轴上"没有空隙"。无论你怎么无限逼近一个位置，那个位置上一定有一个实数等着你。

**来源：** 实数完备性公理（Dedekind 完备性 / Cauchy 完备性），是实分析的基础公理。

**可验证性：** 在实数系 $\mathbb{R}$ 中永远成立。在有理数 $\mathbb{Q}$ 中不成立（例如 $\sqrt{2}$ 的逼近序列在 $\mathbb{Q}$ 中不收敛）。

> 📚 Book: 实分析教材（Rudin, *Principles of Mathematical Analysis*, Ch.1）

### 公理 2: 可加性 (Additivity of Measure)

**陈述：** 如果区间 $[a, c]$ 被分为 $[a, b]$ 和 $[b, c]$，则面积（积分）满足 $\int_a^c f = \int_a^b f + \int_b^c f$。

**白话：** 把一块区域切成两半，两半的面积加起来等于原来的面积。面积不会因为你怎么切而改变。

**来源：** 测度论的有限可加性公理。对于黎曼积分，这直接从求和的性质推出。

**可验证性：** 对所有黎曼可积函数成立。对于"面积无法定义"的病态集合（如 Vitali 集），需要勒贝格测度理论的 σ-可加性。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5 (积分性质)

### 公理 3: 大数定律 (Law of Large Numbers)

**陈述：** 对独立同分布 (i.i.d.) 随机变量 $X_1, X_2, \ldots$，样本均值收敛到期望：$\frac{1}{N}\sum_{i=1}^N X_i \xrightarrow{N\to\infty} E[X]$。

**白话：** 你抛硬币的次数越多，正面的比例就越接近 50%。用"多次采样取平均"可以逼近理论期望值。

**来源：** 概率论基本定理，基于独立性和有限方差假设。

**可验证性：** 需要 i.i.d. 假设和有限期望/方差。如果样本不独立（如 MCMC 的马尔可夫链），需要额外的遍历性条件。如果方差无穷（如柯西分布），强大数定律不成立。

> 📚 Book: Grinstead & Snell, [《Probability》](../../../textbooks/grinstead_snell_probability.pdf), Ch.8 (大数定律)
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11.1 (MC 理论基础)

### 公理 4: 概率归一化 (Probability Normalization Axiom)

**陈述：** 概率分布必须满足 $\int p(x)\,dx = 1$（连续）或 $\sum_x P(x) = 1$（离散）。

**白话：** "所有可能的结果加起来的概率必须等于 100%"。这是概率论的基本约束。

**来源：** Kolmogorov 概率公理（1933）。

**可验证性：** 所有合法的概率分布都满足。如果积分≠1，则不是有效的概率分布（例如，非归一化的后验需要除以归一化常数）。

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2

---


## 从公理到技术的推导链

> 展示如何**仅从上述公理出发**，一步步逻辑推导出完整的技术方案。
> 每一步必须标注"用了哪个公理"，不允许跳步或引入未声明的假设。

### Step 1: {从公理 1 (完备性)} → {黎曼积分的定义}

**推理：** 因为实数的完备性，黎曼和 $S_n = \sum_{i=1}^n f(x_i^*) \Delta x_i$ 在 $\max \Delta x_i \to 0$ 时形成柯西序列（对连续/分段连续函数），因此必须收敛到一个确定的极限值。这个极限就定义为 $\int_a^b f(x)\,dx$。

**结果：** 定积分有了严格的定义——"求面积"变成了一个有明确数学含义的操作。

> 📚 Book: 实分析（黎曼积分存在定理）

### Step 2: {从 Step 1 + 公理 2 (可加性)} → {微积分基本定理}

**推理：** 定义 $G(x) = \int_a^x f(t)\,dt$（用公理 2 保证区间的分割-合并一致性）。由 Step 1 的极限定义，$G'(x) = \lim_{h\to 0} \frac{G(x+h)-G(x)}{h} = \lim_{h\to 0} \frac{1}{h}\int_x^{x+h} f(t)\,dt = f(x)$。所以 $G$ 是 $f$ 的原函数，$\int_a^b f = G(b) - G(a)$。

**结果：** 微积分基本定理——将"求面积"归结为"找反导数"，积分与微分统一。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2

### Step 3: {从 Step 2 + 公理 4 (归一化)} → {概率分布的积分性质}

**推理：** 概率密度函数 $p(x) \geq 0$ 的定积分 $\int_{-\infty}^{+\infty} p(x)\,dx = 1$（公理 4）。利用 Step 2 的积分工具，可以定义连续概率 $P(a \le X \le b) = \int_a^b p(x)\,dx$，以及期望 $E[g(X)] = \int g(x)p(x)\,dx$。

**结果：** 积分是连续概率论的数学基础——归一化、概率计算、期望、方差全部依赖积分。

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2

### Step 4: {从 Step 3 + 公理 3 (大数定律)} → {蒙特卡洛积分}

**推理：** 当 $\int g(x)p(x)\,dx$ 无法解析求解时，由公理 3（大数定律），从 $p(x)$ 中抽 $N$ 个独立样本 $x_i$，则 $\frac{1}{N}\sum_{i=1}^N g(x_i) \xrightarrow{N\to\infty} \int g(x)p(x)\,dx$。

**结果：** 蒙特卡洛积分——用求和（离散采样平均）近似积分（连续期望），完成了"积分→求和"的闭环。

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11.1

### 推导链全景图

```
公理 1 (完备性) ────┐
                    ├──→ 黎曼积分定义 ──┐
公理 2 (可加性) ────┘                   ├──→ 概率分布积分性质 ──┐
                                        │                       │
                    微积分基本定理 ──────┘                       │
                                                                ├──→ 蒙特卡洛积分
公理 4 (归一化) ──→ 概率密度约束 ────────────────────────────────┘        │
                                                                        │
公理 3 (大数定律) ──────────────────────────────────────────────────────┘
```

---


## 如果公理不成立？

> 逐个"拔掉"公理，分析技术会如何崩塌。这揭示了技术的**真正边界**。

### 公理 1 失效：完备性不成立（在有理数系中）

**如果不成立：** 在有理数 $\mathbb{Q}$ 上工作（没有无理数如 $\sqrt{2}, \pi, e$）

**技术后果：** 黎曼和不一定收敛——某些函数的"面积"无法定义。例如 $\int_0^1 x\,dx$ 的极限值 $1/2$ 在 $\mathbb{Q}$ 中存在，但 $\int_0^{\sqrt{2}} 1\,dx = \sqrt{2}$ 不在 $\mathbb{Q}$ 中。高斯积分 $\sqrt{\pi}$ 也不在 $\mathbb{Q}$ 中。

**替代方案：** 使用实数系（标准做法）或 $p$-进数系（数论应用），或只处理积分值在 $\mathbb{Q}$ 中的特殊情况。

> 📚 Book: 实分析基础

### 公理 2 失效：可加性不成立

**如果不成立：** 面积的分割性 $\int_a^c = \int_a^b + \int_b^c$ 不成立

**技术后果：** 整个积分理论崩塌——面积取决于你怎么切分区间，没有确定值。微积分基本定理也不再成立。

**替代方案：** 实际上，可加性在标准积分理论中总是成立的。失效场景是人造的（如 Banach-Tarski 悖论中的不可测集），但那需要选择公理，超出了一般 ML 应用范围。

> 📚 Book: 测度论（σ-可加性）

### 公理 3 失效：大数定律不成立

**如果不成立：** 样本不独立（如有强相关性），或方差无穷（如柯西分布 $p(x) = \frac{1}{\pi(1+x^2)}$）

**技术后果：** 蒙特卡洛积分不收敛——样本平均不再趋近期望。MC 估计的方差不随 $N$ 减小。

**替代方案：**
- 不独立：使用 MCMC（马尔可夫链满足遍历性时，大数定律仍成立，但收敛速度降低）
- 方差无穷：使用截断估计、中位数估计、或选择方差有限的替代分布做重要性采样

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11 (MCMC 遍历性条件)

### 公理 4 失效：概率不归一化

**如果不成立：** $\int p(x)\,dx \neq 1$

**技术后果：** $p(x)$ 不是合法的概率密度。期望 $E[X] = \int xp(x)\,dx$ 的值没有概率解释。贝叶斯推断中，非归一化后验 $p(\theta|\mathcal{D}) \propto p(\mathcal{D}|\theta)p(\theta)$ 是常见情况——它只定义了相对大小，不是概率。

**替代方案：**
- 计算归一化常数 $Z = \int p(x)\,dx$，除以 $Z$ 得到合法分布
- 使用不需要精确归一化的方法：MCMC（只需比值 $p(x')/p(x)$）、对比学习
- 变分推断（ELBO 不需要计算 $Z$）

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.2 (归一化常数), Ch.10 (ELBO)

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|----------|---------|---------|
| 实数完备性 | 有界单调序列必收敛 | 在 $\mathbb{R}$ 中 | 积分定义崩塌 |
| 可加性 | 分割区间，面积相加不变 | 黎曼可积函数 | 面积不确定 |
| 大数定律 | 样本均值→期望 | i.i.d. + 有限方差 | MC 不收敛 |
| 概率归一化 | $\int p = 1$ | 合法概率分布 | 期望无概率解释 |

> 📚 Book: 综合以上来源
