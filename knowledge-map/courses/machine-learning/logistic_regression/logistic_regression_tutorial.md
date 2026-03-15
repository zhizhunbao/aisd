---
topic: logistic_regression
dimension: tutorial
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Hastie et al., ESL Ch.4.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., ISLR Ch.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📚 Book: Bishop, PRML Ch.4.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, PML1 Ch.10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning Ch.5.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: scikit-learn LogisticRegression — https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression"
expiry: 12m
status: current
---

# Logistic Regression 教程

> **前置知识：** 线性代数 | 概率论基础 | 梯度下降 | Linear Regression
> **参考来源：** [《ESL》Ch.4](../../../textbooks/hastie_esl.pdf) | [《ISLR》Ch.4](../../../textbooks/james_ISLR.pdf) | [scikit-learn docs](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

---


## Section 0: 前置知识速查

1. **Linear Regression**：$\hat{y} = \mathbf{w}^T\mathbf{x} + b$，用 MSE 损失拟合连续值——LR 的线性组合部分完全相同
2. **概率论基础**：贝叶斯定理、条件概率、MLE——理解 LR 的概率输出和参数估计
3. **梯度下降**：沿负梯度方向更新参数——LR 没有闭合解，必须用迭代优化
4. **线性代数**：矩阵乘法、转置、逆矩阵——理解向量化梯度和 IRLS

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2-3

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **Linear Regression 做分类不合理**：LR 输出连续值，可能预测出 $P < 0$ 或 $P > 1$，无法解释为概率。例如用 LR 预测糖尿病概率，对某些特征组合可能输出 -0.3 或 1.5——完全没有物理意义
- 🔥 **硬分类器缺少概率校准**：Perceptron、SVM 等只给出类别标签，不给出"有多确定"。在医疗诊断、金融风控等场景，知道"有 85% 概率是恶性"比知道"是恶性"有用得多
- 🔥 **复杂模型缺少可解释性**：决策树和随机森林虽然能分类，但难以给出"每个特征对结果的影响有多大"的定量解释。在受监管行业（银行、保险），模型必须可解释

### 它的核心价值

1. **概率输出**：输出的是真概率 $P(Y=1|\mathbf{x}) \in [0,1]$，可以直接用于风险评估、排序、阈值调整
2. **可解释性**：每个系数 $w_j$ 的 $e^{w_j}$ 就是 odds ratio——"特征增加一个单位，事件几率变为原来的几倍"
3. **理论优雅**：作为 GLM 家族的一员，有完备的统计推断框架（置信区间、假设检验、似然比检验）
4. **计算高效**：损失函数是凸的，保证收敛到全局最优；预测时只需一次矩阵乘法 + sigmoid
5. **万能 baseline**：在任何分类任务中，LR 都应该是第一个尝试的模型——如果 LR 就够用，没必要上复杂模型

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.4.1-4.2
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Logistic Regression 工作流程                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  训练阶段                                                                   │
│  ─────────                                                                  │
│  Input: X (N×p), y (N×1, 二值)                                              │
│      │                                                                      │
│      ▼                                                                      │
│  ┌─────────────────┐     ┌─────────────────┐     ┌──────────────────────┐  │
│  │ 1. 线性组合       │────→│ 2. Sigmoid 变换  │────→│ 3. 计算交叉熵损失     │  │
│  │ z = Xw + b       │     │ p̂ = σ(z)        │     │ L = -Σ[ylog(p̂)+...]  │  │
│  └─────────────────┘     └─────────────────┘     └──────────────────────┘  │
│                                                           │                 │
│                                                           ▼                 │
│                                                   ┌──────────────────┐     │
│  ┌─────────────────┐     ┌─────────────────┐     │ 4. 计算梯度        │     │
│  │ 6. 收敛？        │←────│ 5. 更新参数       │←────│ g = X'(p̂ - y)/N   │     │
│  │ |g| < tol?       │     │ w ← w - H⁻¹g    │     │ (+正则化梯度)      │     │
│  └──────┬───────────┘     └─────────────────┘     └──────────────────┘     │
│         │                                                                   │
│    Yes ─┤─ No → 回到 Step 1                                                │
│         ▼                                                                   │
│  ┌─────────────────┐                                                       │
│  │ 7. 输出 w*, b*   │                                                       │
│  └─────────────────┘                                                       │
│                                                                            │
│  预测阶段                                                                   │
│  ─────────                                                                  │
│  ┌─────────────────┐     ┌─────────────────┐     ┌──────────────────────┐  │
│  │ X_new            │────→│ z = X_new·w* + b*│────→│ p̂ = σ(z)            │  │
│  └─────────────────┘     └─────────────────┘     │ ŷ = 1 if p̂>0.5       │  │
│                                                   └──────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.3.3

### 2.2 为什么用 Sigmoid 而不是其他函数？

**为什么用 Sigmoid 而不是直接截断？**

硬截断（如 $f(z) = 1 \text{ if } z > 0$）不可导，无法用梯度优化。Sigmoid 是可微的，而且有以下特殊地位：

1. **最大熵原理**：在只知道特征的线性组合的约束下，Sigmoid 是满足最大熵原则的唯一函数（来自指数族分布的自然链接函数）
2. **贝叶斯视角**：如果类条件分布属于指数族（如高斯），则后验概率 $P(Y=1|X)$ 恰好是 sigmoid 形式
3. **梯度性质**：$\sigma'(z) = \sigma(z)(1-\sigma(z))$，使得梯度计算极为简洁

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.2（证明指数族导出 sigmoid）
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10.1

### 2.3 交叉熵损失为什么是凸的？

凸性保证了**全局最优解的存在**（梯度下降不会陷入局部最优）。证明路径：

1. 单样本损失 $\ell_i = -y_i\log\sigma(z_i) - (1-y_i)\log(1-\sigma(z_i))$
2. $\frac{\partial^2 \ell_i}{\partial z_i^2} = \sigma(z_i)(1-\sigma(z_i)) > 0$（因为 $\sigma \in (0,1)$）
3. 关于 $\mathbf{w}$ 的 Hessian：$\mathbf{H} = \mathbf{X}^T\mathbf{W}\mathbf{X} \succeq 0$（正半定）
4. 非负凸函数的和仍然是凸的 → 总损失是凸的

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4

### 2.4 优化算法选择

```
小数据集 (<10K 样本)           中等数据集 (10K-100K)          大数据集 (>100K)
┌───────────────────┐         ┌───────────────────┐         ┌───────────────────┐
│ Newton-Cholesky   │         │ L-BFGS (默认)      │         │ SAG / SAGA        │
│ · 二次收敛         │         │ · 拟牛顿法          │         │ · 随机梯度          │
│ · 精确 Hessian     │         │ · 近似 Hessian      │         │ · 线性收敛          │
│ · O(p³) per iter  │         │ · O(p) per iter     │         │ · O(1) per iter    │
└───────────────────┘         └───────────────────┘         └───────────────────┘

需要 L1 正则化？ → liblinear (小数据) 或 SAGA (大数据)
稀疏数据？ → liblinear
```

> 📖 Docs: [scikit-learn LogisticRegression Solvers](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

### 2.5 正则化的直觉

```
无正则化                      L2 正则化 (Ridge)                L1 正则化 (Lasso)
┌──────────────┐             ┌──────────────┐                ┌──────────────┐
│ 权重可能很大   │             │ 权重被压缩      │                │ 部分权重为 0    │
│ 过拟合风险     │             │ 所有特征保留     │                │ 自动特征选择    │
│               │             │ 圆形约束        │                │ 菱形约束        │
└──────────────┘             └──────────────┘                └──────────────┘
    min L(w)                     min L(w)                        min L(w)
                                 s.t. Σw²≤t                     s.t. Σ|w|≤t
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.3.4 + Ch.4.4

---


## Section 3: 局限性

1. **线性决策边界**：LR 本身只能学习线性决策边界。如果真实边界是非线性的（如 XOR 问题），LR 无法拟合 → **应对策略**：手动添加多项式/交互特征，或用核化 LR
2. **特征独立性假设较弱**：虽然不像 Naive Bayes 那样假设完全独立，但多重共线性会导致系数不稳定、标准误膨胀 → **应对策略**：使用 L2 正则化消除多重共线性影响
3. **对异常值敏感**：sigmoid 在极端值处梯度很小（接近饱和），但极端离群点仍会影响决策边界 → **应对策略**：异常值检测 + 数据预处理
4. **完全分离问题 (Complete Separation)**：当数据可以被完美分离时，MLE 不收敛（权重 → ∞）→ **应对策略**：添加正则化（scikit-learn 默认 L2, C=1.0）
5. **不适合高维稀疏**：当 $p \gg N$ 时容易过拟合 → **应对策略**：L1 正则化 + 降维

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10.2

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------| 
| **Logistic Regression** | 概率输出、可解释、凸优化、快速推理 | 线性边界、需特征工程 | baseline、可解释场景、概率排序 |
| **LDA** | 闭合解、小样本稳定 | 需高斯+等协方差假设 | 满足分布假设时 |
| **SVM** | 非线性核、最大间隔 | 无天然概率、大规模慢 | 高维、非线性、小中数据 |
| **Naive Bayes** | 极快训练、小样本好 | 独立性假设、概率校准差 | 文本分类、极高维 |
| **决策树** | 非线性、可解释 | 过拟合、不稳定 | 混合特征类型 |
| **Neural Network** | 任意非线性、自动特征 | 黑箱、需大数据 | 大规模复杂任务 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [《ESL》Ch.4.4](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 全文核心：公式推导、IRLS、理论分析 |
| [《ISLR》Ch.4](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | Section 0-1：直觉解释、入门动机 |
| [《PRML》Ch.4.3](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | Section 2：贝叶斯视角、指数族推导 |
| [《PML1》Ch.10](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | Section 3-4：正则化、多分类、现代视角 |
| [《Deep Learning》Ch.5.7](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | Section 2：LR 作为最简单神经网络 |
| [scikit-learn docs](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression) | 📖 文档 | Section 2.4：优化算法选择 |
