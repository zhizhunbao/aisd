---
topic: decision_tree
dimension: tutorial
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

# Decision Tree 教程

> **前置知识：** 基础统计 | 信息论（熵）| 过拟合概念
> **参考来源：** [《ESL》Ch.9](../../../textbooks/hastie_esl.pdf) | [《ISLR》Ch.8](../../../textbooks/james_ISLR.pdf) | [scikit-learn docs](https://scikit-learn.org/stable/modules/tree.html)

---


## Section 0: 前置知识速查

1. **信息熵**：$H = -\sum p_k \log p_k$，衡量不确定性——Decision Tree 用它来评估分割质量
2. **过拟合**：模型在训练集上表现好但泛化差——DT 不加限制会完美拟合训练集
3. **偏差-方差权衡**：简单模型高偏差低方差，复杂模型低偏差高方差——DT 属于高方差模型
4. **递归算法**：函数调用自身——DT 构建的核心就是递归分割

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2.9, Ch.7

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **线性模型无法处理非线性**：Logistic Regression 只能画直线决策边界。如果"满足条件 A 且条件 B 时用规则 1，否则用规则 2"——线性模型需要人工构造交互特征
- 🔥 **黑箱模型无法解释**：神经网络能拟合复杂模式，但无法告诉你"为什么做出这个决策"。在医疗诊断、贷款审批中，监管机构要求模型**可解释**
- 🔥 **对特征类型有要求**：很多模型需要数值输入（标准化、独热编码）。Decision Tree 天然支持混合类型——数值直接比较阈值，类别直接分组

### 它的核心价值

1. **可解释性**：决策过程可以画成一棵树——每个分支是一个 if-else 规则，非技术人员也能理解
2. **自动特征交互**：树的层次结构天然捕捉特征交互（"如果年龄>50 且吸烟"自动出现在树中）
3. **无需预处理**：不需要标准化、不受异常值影响、能处理缺失值（sklearn ≥1.4）
4. **计算高效**：训练 $O(Np\log N)$，预测 $O(\log N)$ — 比 KNN 的 $O(Np)$ 快得多
5. **集成方法基石**：Random Forest 和 GBDT 的核心组件——理解 DT 是理解现代集成方法的前提

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8.1
> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Decision Tree 工作流程 (CART)                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  构建阶段 (Grow)                                                            │
│  ─────────────────                                                          │
│  Input: X (N×p), y (N×1)                                                   │
│      │                                                                      │
│      ▼                                                                      │
│  ┌─────────────────┐     ┌──────────────────────────────────────────────┐  │
│  │ 1. 当前节点     │     │ 2. 对所有特征 j 和阈值 t:                     │  │
│  │    包含样本集 S │────→│    计算 ΔI(j,t) = I(S) - weighted I(子节点)  │  │
│  └─────────────────┘     │    选择使 ΔI 最大的 (j*, t*)                 │  │
│                          └──────────────────────────────────────────────┘  │
│                                    │                                       │
│                                    ▼                                       │
│             ┌─────────────────────────────────────────────┐               │
│             │ 3. 按 x_{j*} ≤ t* 拆分为左右子节点            │               │
│             └─────────┬─────────────────┬─────────────────┘               │
│                       │                 │                                   │
│                   Left child        Right child                             │
│                       │                 │                                   │
│              ┌─────────────────┐  ┌─────────────────┐                     │
│              │ 4. 满足停止条件？│  │ 4. 满足停止条件？│                     │
│              │ · max_depth     │  │ · min_samples    │                     │
│              │ · 所有样本同类  │  │ · 不纯度=0       │                     │
│              └──┬──────┬──────┘  └──┬──────┬──────┘                     │
│             Yes ↓   No ↓         Yes ↓   No ↓                             │
│            标记叶子  回到 Step 1  标记叶子  回到 Step 1                       │
│                                                                            │
│  剪枝阶段 (Prune, 可选)                                                     │
│  ──────────────────────                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ 5. 代价复杂度剪枝: R_α(T) = R(T) + α|T|                            │  │
│  │    用交叉验证选择最优 α → 剪掉"最弱"分支                             │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  预测阶段                                                                   │
│  ──────────                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ 6. 新样本从根节点出发，按规则 x_j ≤ t ? 下行到叶子节点              │  │
│  │    分类: 输出叶子多数类 | 回归: 输出叶子均值                        │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### 2.2 为什么用贪心而不是全局最优？

**全局最优 DT 构建是 NP-hard 问题**——因为可能的树结构数量随特征数和样本数指数增长。Hyafil & Rivest (1976) 证明了：即使只考虑二叉树，找到最小的正确分类树也是 NP-complete 的。

贪心策略的代价就是**可能错过全局最优分割**。这就是为什么：
1. 单棵树不够好 → 用 **Random Forest**（多棵树投票抵消贪心偏差）
2. 单棵树误差大 → 用 **GBDT**（后续的树修正前面的错误）

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

### 2.3 为什么 Decision Tree 容易过拟合？

一棵不受限制的树会继续分割直到**每个叶子只有一个样本**——训练准确率 100%，但泛化极差。原因：

1. **高方差**：训练数据的微小变化可能导致完全不同的树结构（一个根节点的分割变了，整棵树都变了）
2. **无正则化先验**：不像 LR 有 L2 正则化限制参数大小，DT 的唯一内在限制是数据量
3. **噪声拟合**：树可以精确分割噪声点和异常值

**应对策略：**
- 预剪枝：`max_depth`, `min_samples_split`, `min_samples_leaf`
- 后剪枝：`ccp_alpha`（代价复杂度剪枝）
- 集成：RF（降方差）、GBDT（降偏差）

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8.1

### 2.4 决策边界的形状

Decision Tree 的决策边界是**轴对齐的矩形**——每个分割平行于某个坐标轴。这意味着：

```
线性模型的边界:          Decision Tree 的边界:
  ↑ x2                    ↑ x2
  │    /                   │ ┌────┐
  │   / A                  │ │ A  │
  │  / ──                  │ ├────┤
  │ / B                    │ │ B  │
  └──────→ x1              └──────→ x1
  (斜线)                   (轴对齐阶梯)
```

如果真实边界是斜线，DT 需要很多次分割才能近似——这时候 SVM 或 LR 可能更好。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

---


## Section 3: 局限性

1. **高方差/不稳定**：微小数据变化→完全不同的树 → **应对**：使用 RF/GBDT
2. **轴对齐边界**：只能做平行于坐标轴的分割 → **应对**：使用 oblique decision tree 或旋转特征
3. **贪心次优**：全局最优是 NP-hard → **应对**：集成多棵树
4. **不能外推**：回归树在训练范围外预测为常数 → **应对**：对数据做变换或使用线性模型
5. **对类别不平衡敏感**：少数类可能被多数类"淹没" → **应对**：`class_weight='balanced'`
6. **大特征空间效率低**：$O(Np\log N)$ 对高维数据较慢 → **应对**：特征选择后再建树

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.18

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------| 
| **Decision Tree** | 可解释、无需预处理、快 | 高方差、容易过拟合 | 可解释场景、EDA、集成基础 |
| **Logistic Regression** | 概率输出、低方差、凸优化 | 线性边界、需特征工程 | 线性关系、概率排序 |
| **Random Forest** | 低方差、鲁棒、并行 | 不如单棵树可解释 | 中大数据、需准确率 |
| **GBDT / XGBoost** | 高精度、处理异质数据 | 调参复杂、过拟合风险 | 竞赛、结构化数据 |
| **SVM** | 强泛化、核方法 | 慢、不直接概率 | 中小数据、非线性 |
| **KNN** | 简单、无假设 | 慢（预测时）、维度灾难 | 小数据探索 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9-10

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [《ESL》Ch.9](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 全文核心：CART 算法、剪枝理论 |
| [《ISLR》Ch.8](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | Section 0-1：直觉、入门 |
| [《PML1》Ch.18](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | Section 3：局限性分析 |
| [scikit-learn docs](https://scikit-learn.org/stable/modules/tree.html) | 📖 文档 | Section 2：实现细节 |
