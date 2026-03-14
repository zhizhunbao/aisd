---
topic: decision_tree
dimension: first_principles
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Hastie et al., ESL Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: Bishop, PRML Ch.14.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, PML1 Ch.18 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
expiry: 12m
status: current
---

# Decision Tree 第一性原理

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.14.4

---


## 核心问题链

> 用"5 个为什么"式的递归追问，从表面功能一路追到不可再分的基本事实。

### 问题链

1. **Decision Tree 在做什么？** → 通过递归分割特征空间来构建预测规则
2. **为什么要分割特征空间？** → 因为在每个局部区域内，用常数（多数类/均值）近似目标函数比用全局模型更灵活——这是**非参数回归**的核心思想
3. **为什么选不纯度下降最大的分割？** → 因为这等价于最大限度地减少预测不确定性——等价于信息论中的最大信息增益
4. **为什么信息增益率是好的准则？** → 因为 Shannon 信息论证明了**熵是衡量不确定性的唯一合理度量**（满足连续性、对称性、可加性公理）
5. **这个根基能否继续拆分？** → 不能：Shannon 的信息论公理是概率论和信息度量的基础 → **到达公理**

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.6

---


## 公理与基本假设

### 公理 1: Shannon 信息熵公理

**陈述：** 在满足以下条件 (1)连续性 (2)对称性 (3)可分解性 的前提下，衡量不确定性的唯一函数形式是 $H = -\sum p_k \log p_k$

**白话：** 信息熵是唯一一个"合理的"不确定性度量——如果你接受"不确定性应该光滑、对称、可分解"这三个常识性要求

**来源：** Shannon, "A Mathematical Theory of Communication", 1948。这是信息论的基石定理

**可验证性：** 始终成立——这是公理化信息论的定理，只要接受三个公理就必须接受熵作为度量

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.6

### 公理 2: 分段常数近似假设

**陈述：** 目标函数 $f(\mathbf{x})$ 可以用分段常数函数很好地近似：$\hat{f}(\mathbf{x}) = \sum_m c_m \cdot \mathbf{1}[\mathbf{x} \in R_m]$

**白话：** 对于任何目标函数，只要区域划分得足够细，在每个小区域内用一个常数就能逼近真实值

**来源：** 数学分析中简单函数逼近定理的离散化版本。在实变分析中，任何可测函数都可以用简单函数一致逼近

**可验证性：**
- **成立条件**：$f$ 连续或分段连续时，区域足够细就能逼近
- **不成立条件**：如果 $f$ 极其不规则（如处处不连续），需要指数级区域数

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### 公理 3: 贪心近似可行假设

**陈述：** 每步选择局部最优分割（贪心策略）可以得到接近全局最优的树

**白话：** 虽然全局最优 DT 是 NP-hard，但贪心策略在实践中足够好——因为好的局部分割通常也是好的全局分割

**来源：** 这是一个**实践假设**而非数学定理。Hyafil & Rivest (1976) 证明了最优 DT 构建是 NP-complete，贪心只是一个启发式妥协

**可验证性：**
- **成立条件**：特征之间不存在复杂的全局交互时（如 XOR 问题需要多步配合）
- **不成立条件**：当最优分割需要"先分一个看似无用的特征，才能让第二步分割有效"时（如 XOR），贪心策略失败

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### 公理 4: 轴对齐分割假设

**陈述：** 每次分割只基于一个特征的一个阈值：$x_j \leq t$

**白话：** 我们只用"某个特征是否超过某个值"这种最简单的问题来分割数据——不考虑多个特征的线性组合

**来源：** CART 算法的设计选择（Breiman 1984），不是数学必然性。Oblique Decision Tree 就放弃了此假设

**可验证性：**
- **成立条件**：真实决策边界近似轴对齐时
- **不成立条件**：真实边界是斜线（如 $x_1 + x_2 > 5$），需要很多次轴对齐分割来近似

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

---


## 从公理到技术的推导链

### Step 1: {从公理 1} → {分割准则}

**推理：** 
由 Shannon 公理，衡量节点不确定性的唯一合理度量是信息熵 $H = -\sum p_k \log p_k$。分割的目标是最大化不确定性的减少：

$$
\Delta H = H(\text{parent}) - \sum_{\text{children}} \frac{N_{\text{child}}}{N} H(\text{child})
$$

**结果：** 信息增益作为分割准则是 Shannon 公理的**必然推论**。Gini 不纯度是 $H$ 的二阶泰勒近似，因此也是合理的替代

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.6

### Step 2: {结合 Step 1 + 公理 2} → {递归分割算法}

**推理：** 
由分段常数假设，目标是将特征空间分成多个区域 $\{R_m\}$。每个区域用常数 $c_m$ 预测。为了找到好的分割，在每个节点用 Step 1 的信息增益准则选择最优分割特征和阈值

**结果：** 递归二分法——对当前节点选最优分割 → 对子节点递归 → 直到停止条件

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### Step 3: {结合 Step 2 + 公理 3} → {贪心 CART 算法}

**推理：** 
全局最优分割方案是 NP-hard（Hyafil & Rivest 1976），因此在每个节点只看当前最优（贪心），而非搜索所有可能的树

**结果：** CART 的贪心构建：每步 $O(Np)$ 计算所有可能分割，选最优

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### Step 4: {从 Step 3 + 过拟合观察} → {剪枝}

**推理：** 
贪心构建的完全树完美拟合训练集但过拟合。需要在"准确性"和"复杂度"之间做权衡 → 代价复杂度目标 $R_\alpha(T) = R(T) + \alpha|T|$

**结果：** CCP 剪枝 + 交叉验证选择最优 $\alpha$ → 完整的 CART 算法

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2.2

### 推导链全景图

```
公理 1 (Shannon 熵公理) ──→ Step 1: 信息增益分割准则 ──┐
                                                        │
公理 2 (分段常数近似) ───────────────────────────────────┼──→ Step 2: 递归分割算法
                                                        │
公理 3 (贪心近似可行) ─────────────────────────────────────→ Step 3: CART 贪心构建
                                                               │
公理 4 (轴对齐分割) ────────────────── 约束分割形式             │
                                                               │
                                               过拟合观察 ──→ Step 4: CCP 剪枝
                                                               │
                                                        完整 CART 算法
```

---


## 如果公理不成立？

### 公理 1 失效：信息熵不是唯一的不确定性度量

**如果不成立：** 如果不接受 Shannon 的三条公理（如放松对称性），可以有其他不确定性度量（如 Rényi 熵 $H_\alpha = \frac{1}{1-\alpha}\log\sum p_k^\alpha$）

**技术后果：** Gini 不纯度就是 Rényi 熵在 $\alpha=2$ 时的特例。实际上 Gini 和 Entropy 在决策树中效果差异很小（~2%），说明分割准则对精确形式不太敏感

**替代方案：** Gini, Misclassification Error, Tsallis Entropy 等——在实践中差异极小

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### 公理 2 失效：分段常数近似不够好

**如果不成立：** 目标函数在每个区域内不是常数，而是线性或非线性变化的

**技术后果：** 需要极细的分割才能近似——导致树极深、过拟合严重

**替代方案：**
- **M5 Model Tree**：叶子节点不是常数，而是线性回归模型
- **体制混合模型**：每个区域用一个完整的参数模型
- **Neural Networks**：用连续可微函数替代分段常数

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.18

### 公理 3 失效：贪心策略找不到好的树

**如果不成立：** 需要全局配合的复杂交互（如 XOR 问题：$x_1$ 和 $x_2$ 单独看都无关，但 $x_1 \oplus x_2$ 有预测力）

**技术后果：** 贪心策略在第一步看不到 $x_1$ 或 $x_2$ 的价值（信息增益=0），无法构建有效的树

**替代方案：**
- **集成方法**：Random Forest 通过多棵树覆盖不同分割路径
- **特征工程**：手动添加交互特征 $x_1 \cdot x_2$
- **Look-Ahead 方法**：搜索深度>1 的分割组合（计算量指数增长）

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### 公理 4 失效：真实边界不是轴对齐的

**如果不成立：** 真实决策边界是斜线 $w_1 x_1 + w_2 x_2 > t$（如线性判别或旋转过的类别）

**技术后果：** 需要非常多次的轴对齐分割才能近似一条斜线——树变得很深很复杂

**替代方案：**
- **Oblique Decision Tree**：允许多特征线性组合分割 $\mathbf{w}^T\mathbf{x} \leq t$
- **SVM / Logistic Regression**：天然支持斜线边界
- **旋转森林 (Rotation Forest)**：先 PCA 旋转特征再建树

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
| Shannon 熵公理 | 熵是唯一满足连续+对称+可加的不确定性度量 | 始终成立 | 换准则影响小 |
| 分段常数近似 | 足够细的区域内用常数能逼近任何函数 | 连续函数 | 树极深过拟合 → M5/NN |
| 贪心近似可行 | 局部最优分割接近全局最优 | 无复杂全局交互 | XOR 问题失败 → 集成/特征工程 |
| 轴对齐分割 | 每次只看一个特征 $x_j \leq t$ | 边界近似轴对齐 | 斜线边界低效 → ObliqueDT/SVM |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.14.4
