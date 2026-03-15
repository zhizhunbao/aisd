---
topic: integration_summation
dimension: tutorial
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5-6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Bishop, PRML, Ch.1-2,11 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Grinstead & Snell, Introduction to Probability, Ch.1-2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/grinstead_snell_probability.pdf"
  - "📖 Docs: SciPy integrate — https://docs.scipy.org/doc/scipy/reference/integrate.html"
expiry: 12m
status: current
---

# 积分与求和 教程

> **前置知识：** 函数、极限、微分（导数）
> **参考来源：** [《MML》Ch.5-6](../../../textbooks/deisenroth_mml.pdf) | [《PRML》Ch.1-2](../../../textbooks/bishop_prml.pdf) | [《Deep Learning》Ch.3](../../../textbooks/goodfellow_deep_learning.pdf)

---


## Section 0: 前置知识速查

1. **函数 (Function)**：$y = f(x)$，给定输入 $x$ 返回唯一输出 $y$
2. **极限 (Limit)**：$\lim_{n\to\infty} a_n = L$ 表示序列 $a_n$ 无限趋近于 $L$
3. **导数 (Derivative)**：$f'(x) = \lim_{h\to 0} \frac{f(x+h)-f(x)}{h}$，函数的瞬时变化率
4. **级数 (Series)**：无穷多项的求和 $\sum_{n=0}^{\infty} a_n$，需要讨论收敛性

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.1

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **无法计算连续概率：** 连续随机变量的概率 $P(a \le X \le b)$ 无法定义——没有积分，就没有 $\int_a^b p(x)\,dx$，概率论就局限在离散世界
- 🔥 **无法计算期望和方差：** 损失函数的期望风险 $E[L]$、高斯分布的方差 $\text{Var}[X]$ 都依赖积分/求和。没有这些工具，模型的理论分析完全不可能
- 🔥 **贝叶斯推断寸步难行：** 贝叶斯公式的分母 $p(\mathcal{D}) = \int p(\mathcal{D}|\theta)p(\theta)\,d\theta$ 是一个积分。没有积分（或其近似），就无法做贝叶斯预测
- 🔥 **无法处理"累加到连续"的场景：** 从离散的柱状图到连续的曲线面积，从求和到积分的推广是数学的核心跳跃

### 它的核心价值

1. **统一离散与连续：** 求和处理离散值，积分处理连续值，两者在概率/期望框架下形成完美对应——$\sum \leftrightarrow \int$
2. **精确量化"累积效果"：** 无论是面积、体积、概率质量还是期望值，积分/求和提供了严格的数学工具
3. **ML 的数学语言：** 损失函数、概率分布、梯度计算、变分推断——ML 的核心数学几乎全部建立在积分与求和之上

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2 (概率中的积分角色)
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3.4 (期望)

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 从求和到积分的演进

```
┌───────────────────────────────────────────────────────────────┐
│              从离散到连续的演进路径                              │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  离散求和                连续积分                               │
│  ┌─────────────┐        ┌─────────────────────┐              │
│  │ Σ_{i=1}^N   │  Δx→0  │ ∫_a^b f(x) dx      │              │
│  │ f(x_i)·Δx_i │  ───→  │ = lim Σ f(x_i)·Δx_i│              │
│  └─────────────┘        └─────────────────────┘              │
│        │                         │                            │
│        ▼                         ▼                            │
│  ┌─────────────┐        ┌─────────────────────┐              │
│  │ 离散期望     │        │ 连续期望              │             │
│  │ E[X]=Σ x·P  │   ↔    │ E[X]=∫ x·p(x)dx    │              │
│  └─────────────┘        └─────────────────────┘              │
│        │                         │                            │
│        ▼                         ▼                            │
│  ┌─────────────┐        ┌─────────────────────┐              │
│  │ PMF: P(x)   │        │ PDF: p(x)            │             │
│  │ Σ P(x) = 1  │   ↔    │ ∫ p(x) dx = 1       │              │
│  └─────────────┘        └─────────────────────┘              │
└───────────────────────────────────────────────────────────────┘
```

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.6.2

### 2.2 黎曼积分：求和的极限

**为什么用"切细长条再加起来"？** 因为直线（矩形）的面积是最容易计算的：宽 × 高。如果我们把曲线下方的区域切成无穷多个无穷窄的矩形，每个矩形面积 $f(x_i) \cdot \Delta x_i$，然后全部加起来，就得到精确的面积。

具体步骤：
1. 将 $[a,b]$ 分成 $n$ 个小段：$a = x_0 < x_1 < \cdots < x_n = b$
2. 在每段 $[x_{i-1}, x_i]$ 中取一点 $x_i^*$
3. 做黎曼和：$S_n = \sum_{i=1}^{n} f(x_i^*) \cdot (x_i - x_{i-1})$
4. 令最大段宽 $\max_i (x_i - x_{i-1}) \to 0$，$S_n \to \int_a^b f(x)\,dx$

**关键洞察：** 积分就是"求和的连续极限"。这也是为什么积分符号 $\int$ 实际上是字母 S（Sum）的变体——莱布尼茨的设计。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2

### 2.3 微积分基本定理：连接微分与积分

**为什么"求面积"可以用"找反导数"？** 因为如果 $G(x) = \int_a^x f(t)\,dt$ 定义了面积随 $x$ 增长的函数，那么面积的增长率 $G'(x)$ 就是当前的函数值 $f(x)$。所以 $G$ 就是 $f$ 的一个原函数。

这个定理将两个看似不同的问题——"求面积"（积分）和"求变化率"（微分）——优雅地统一了起来。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2, Theorem 5.2

### 2.4 ML 中的三种积分场景

```
     解析可积？
         │
    ┌────┴────┐
    YES       NO
    │         │
    ▼         ▼
 使用公式   维度？
 F(b)-F(a)    │
         ┌────┴────┐
         低维       高维
         │         │
         ▼         ▼
      数值积分   蒙特卡洛
      (quad)    (采样平均)
```

1. **解析可积**：高斯分布归一化、指数分布期望 — 直接用公式
2. **低维不可积**：用 SciPy `quad` 做数值积分（梯形法/Simpson）
3. **高维不可积**：用蒙特卡洛采样 $\frac{1}{N}\sum f(x_i)$ 近似（变分推断、MCMC）

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.10.1 (变分推断), Ch.11.1 (蒙特卡洛)

---


## Section 3: 局限性

1. **高维积分的维度诅咒：** 传统数值积分方法的计算量随维度指数增长。10 维空间中每轴 10 个点需要 $10^{10}$ 个采样点 → 只能用蒙特卡洛近似
2. **不是所有函数都可积：** 黎曼积分要求函数"足够规则"（不连续点是零测集）。极端不规则函数需要勒贝格积分理论
3. **蒙特卡洛的收敛速度慢：** $O(1/\sqrt{N})$ 意味着精度提高 10 倍需要 100 倍的样本量。对精度要求高的场景代价大
4. **求和-积分交换有条件：** 随意交换 $\sum$ 和 $\int$ 的顺序可能导致错误结果（需 Fubini 定理 / 一致收敛 / Dominated Convergence）

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.11.1 (MC 限制)
> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.6.6 (高维问题)

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------| 
| **解析积分** | 精确、无误差 | 很多函数无封闭解 | 标准分布（高斯、指数、Beta） |
| **数值积分 (Quadrature)** | 低维高精度、确定性 | 维度诅咒、需要光滑函数 | 1D-3D 的定积分 |
| **蒙特卡洛 (MC)** | 不受维度影响、$O(1/\sqrt{N})$ | 收敛慢、需要能采样 | 高维贝叶斯推断 |
| **变分推断 (VI)** | 快速、可扩展 | 近似质量受分布族限制 | 大规模贝叶斯模型 |
| **Laplace 近似** | 简单、快速 | 仅在后验近似高斯时可靠 | 后验近似单峰场景 |

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.4 (Laplace), Ch.10 (VI), Ch.11 (MC)

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《MML》Ch.5-6](../../../textbooks/deisenroth_mml.pdf) | 📚 教科书 | 全文核心参考（积分定义、连续概率） |
| [《PRML》Ch.1-2, 10-11](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 期望、边缘化、MC、变分推断 |
| [《Deep Learning》Ch.3](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | Section 1 (期望在 ML 中的角色) |
| [《Probability》Ch.1-2](../../../textbooks/grinstead_snell_probability.pdf) | 📚 教科书 | 离散/连续期望对比 |
| [SciPy integrate](https://docs.scipy.org/doc/scipy/reference/integrate.html) | 📖 文档 | Section 4 (数值积分工具) |
