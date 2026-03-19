---
topic: model_evaluation_metrics
dimension: tutorial
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Paper: Fawcett, 'An Introduction to ROC Analysis', Pattern Recognition Letters 2006 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf"
  - "📖 Paper: Raschka, 'Model Evaluation, Model Selection, and Algorithm Selection in ML', arXiv 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf"
  - "📖 Docs: scikit-learn Model Evaluation — https://scikit-learn.org/stable/modules/model_evaluation.html"
expiry: 12m
status: current
---

# Model Evaluation & Metrics 教程

> **前置知识：** 至少训练过一个分类/回归模型（如 Logistic Regression、Decision Tree）
> **参考来源：** [scikit-learn Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

---

## Section 0: 前置知识速查

1. **监督学习基本流程**：数据 → 训练 → 预测 → ？（评估就是这个问号）
2. **训练集 vs 测试集**：用不同数据训练和评估，防止"做题和看答案用同一套卷子"
3. **概率基础**：条件概率 P(A|B)，因为大多数分类器输出的是概率而非硬标签

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **痛点 1：你不知道模型好不好** — 训练完一个分类器，Loss 下降了，但这只说明它在训练数据上"记住了"答案（可能过拟合），你完全不知道它面对新数据会怎样
- 🔥 **痛点 2：你不知道选哪个模型** — SVM 和 Random Forest 都跑了一遍，都有结果，但用什么数字来公平比较？光看 Accuracy？这在不平衡数据上会骗人
- 🔥 **痛点 3：你不知道什么时候该停** — 调超参数可以无限调下去，但怎么知道继续调还有没有收益？模型是欠拟合（该更复杂）还是过拟合（该更简单）？
- 🔥 **痛点 4：你不知道模型在哪类样本上犯错** — Accuracy 只给一个总分，不告诉你模型是漏了正例还是误报了负例——在医疗、金融等领域，这两种错误的代价完全不同

### 它的核心价值

1. **量化模型性能** — 用数字（Accuracy、F1、AUC 等）客观衡量模型好坏，替代主观感觉
2. **指导模型选择** — 在多个候选模型之间用同一把尺子公平比较
3. **诊断模型问题** — 学习曲线告诉你是欠拟合还是过拟合，混淆矩阵告诉你具体在哪犯错
4. **估计泛化能力** — 交叉验证给出模型在"没见过的数据"上的可靠性能估计

> 📖 Paper: Raschka, [Model Evaluation](../../../.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf), Section 1

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 评估流程全景图

```
原始数据
    │
    ├──→ Hold-out 划分                    ┌─→ 分类评估：混淆矩阵 → P/R/F1/MCC
    │    (train/test split)               │   ROC/PR 曲线 → AUC
    │    └──→ 训练 → 预测 → 评估 ────────→│
    │                                     │
    ├──→ K-Fold 交叉验证                   ├─→ 回归评估：MSE/RMSE/MAE/R²
    │    (更稳定)                          │
    │    ├── Fold 1: 训练 → 评估 ─┐       └─→ 诊断工具：学习曲线/验证曲线
    │    ├── Fold 2: 训练 → 评估 ─┤
    │    ├── ...                   ├──→ 取均值±标准差
    │    └── Fold K: 训练 → 评估 ─┘
    │
    └──→ 嵌套交叉验证 (Nested CV)
         外层: 评估泛化性能
         内层: 调超参数
```

### 2.2 核心机制

**为什么用 K-Fold 交叉验证而不是单次 Train/Test Split？**

单次划分有"运气"成分——恰好把简单的样本分到了测试集，或者把关键的少数类样本全分到了训练集。Kohavi (1995) 用大规模实验证明：10-fold 分层交叉验证在大多数情况下给出偏差和方差最平衡的估计。

**为什么用 F1 而不是 Accuracy？**

Accuracy 的分母是全部样本，当负例远多于正例时，TN 的数量"稀释"了错误。举例：1000 个样本中只有 10 个正例，一个全部预测为负的模型 Accuracy = 990/1000 = 99%，但 Recall = 0（一个正例都没找到）。F1 的分母只涉及 TP、FP、FN，不受 TN 数量影响。

**为什么 ROC-AUC 在不平衡数据上会过度乐观？**

因为 FPR = FP/(FP+TN)，当 TN 很大时（大量负例被正确分类），FPR 的值很低，ROC 曲线被压到左上角。这给人"模型很好"的错觉。PR 曲线避免了这个问题，因为它不涉及 TN。

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 6
> 📖 Paper: Kohavi, [Cross-Validation](../../../.documents/papers/model_evaluation_metrics/kohavi_1995_cross_validation_bootstrap.pdf)

---

## Section 3: 局限性

1. **评估指标无法替代业务理解** → Accuracy 0.95 不一定意味着模型"够好"——医疗场景下 Recall 0.90 可能都不够（10% 漏诊率）。应对：先明确业务可接受的指标阈值
2. **交叉验证假设数据是 i.i.d.** → 时间序列数据不能随机划分（未来数据不能出现在训练集中）。应对：使用 TimeSeriesSplit
3. **所有指标都是对测试集的估计** → 测试集太小时估计方差很大。应对：报告置信区间，使用重复交叉验证
4. **多指标可能矛盾** → Precision 高但 Recall 低，或者反过来。应对：根据业务场景选择主要指标，或用 F1/MCC 综合
5. **评估指标本身有偏差** → AUC 在严重不平衡数据上过于乐观。应对：改用 PR-AUC 或报告多个指标

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.10

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **Hold-out Split** | 简单快速，一次搞定 | 结果依赖划分运气，方差大 | 数据量 > 100k，快速实验 |
| **K-Fold CV (K=5,10)** | 偏差低，所有数据都参与评估 | 计算量是 Hold-out 的 K 倍 | 标准工作流，中等数据量 |
| **Stratified K-Fold** | 保持每折类别比例一致 | 比普通 K-Fold 略复杂 | 类别不平衡数据（应为默认） |
| **LOOCV (K=n)** | 偏差最低（训练集最大） | 方差高（各折高度相关），极慢 | 小数据集 (n < 100) |
| **Repeated K-Fold** | 进一步降低方差 | 计算量 = K × repeats | 需要高置信度的最终评估 |
| **Nested CV** | 同时调参+评估，无信息泄露 | 最复杂，计算量最大 | 严格的学术论文评估 |
| **Bootstrap** | 可计算置信区间 | 有偏（部分样本重复，部分从未见） | 统计推断，小样本 |

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.5
> 📖 Paper: Kohavi, [Cross-Validation and Bootstrap](../../../.documents/papers/model_evaluation_metrics/kohavi_1995_cross_validation_bootstrap.pdf)

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《ESL》Ch.7](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | Section 2-3（CV 理论、偏差-方差） |
| [《ISLR》Ch.5](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | Section 4（验证方法对比） |
| [Fawcett 2006](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf) | 📖 论文 | Section 2（ROC 设计决策） |
| [Kohavi 1995](../../../.documents/papers/model_evaluation_metrics/kohavi_1995_cross_validation_bootstrap.pdf) | 📖 论文 | Section 2（CV vs Bootstrap） |
| [Raschka 2020](../../../.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf) | 📖 论文 | Section 1（Why） |
| [scikit-learn Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) | 📖 文档 | 全文（API 参考） |
