---
topic: model_evaluation_metrics
dimension: concepts
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Paper: Fawcett, 'An Introduction to ROC Analysis', Pattern Recognition Letters 2006 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf"
  - "📖 Paper: Grandini et al., 'Metrics for Multi-Class Classification', arXiv 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/grandini_2020_confusion_matrix.pdf"
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Docs: scikit-learn Model Evaluation Guide — https://scikit-learn.org/stable/modules/model_evaluation.html"
expiry: 12m
status: current
---

# Model Evaluation & Metrics 核心概念

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7
> 📖 Paper: Fawcett, [An Introduction to ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf)

---

## 术语定义

### 混淆矩阵 (Confusion Matrix)

一张 2×2 的表格（二分类时），把模型的每一个预测结果按"实际类别"和"预测类别"两个维度归类。它是几乎所有分类指标的**计算起点**。四格分别是：真正例 (TP)、假正例 (FP)、假负例 (FN)、真负例 (TN)。

> 易混淆：**误差矩阵 (Error Matrix)** — 同一个东西的另一个名字，常见于遥感和生态学文献

> 📖 Paper: Grandini et al., [Metrics for Multi-Class Classification](../../../.documents/papers/model_evaluation_metrics/grandini_2020_confusion_matrix.pdf)

### 准确率 (Accuracy)

所有预测中猜对的比例。公式：(TP + TN) / (TP + FP + FN + TN)。最直觉、最简单的指标，但在类别不平衡时**极其不可靠**——99% 负样本的数据集上，全部预测为负也能达到 99% 准确率。

> 易混淆：**精确率 (Precision)** — 准确率看的是"全部预测"，精确率看的是"预测为正的那些里有多少是对的"。中文翻译容易混

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.2

### 精确率 (Precision)

在所有被模型**预测为正**的样本中，确实是正例的比例。公式：TP / (TP + FP)。回答的问题是："模型说的'是'里面，有多少真的是？"。高 Precision 意味着误报少。

> 易混淆：**准确率 (Accuracy)** — Precision 只关注"预测为正"的子集，Accuracy 关注全部预测

> 📖 Docs: [scikit-learn precision_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)

### 召回率 (Recall / Sensitivity / True Positive Rate)

在所有**实际为正**的样本中，被模型正确识别出来的比例。公式：TP / (TP + FN)。回答的问题是："真正的正例里面，模型抓到了多少？"。高 Recall 意味着漏检少。

> 易混淆：**特异度 (Specificity)** — Recall 关注正例被正确识别的比例，Specificity 关注负例被正确识别的比例（TN / (TN + FP)）

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 2

### F1 分数 (F1 Score)

Precision 和 Recall 的调和平均数。公式：2 × Precision × Recall / (Precision + Recall)。用调和平均而不是算术平均，是因为调和平均对极端低值更敏感——如果 Precision 或 Recall 任一为 0，F1 也为 0。

> 易混淆：**Fβ 分数** — F1 是 β=1 的特例。β>1 更重视 Recall（如 F2），β<1 更重视 Precision（如 F0.5）

> 📖 Paper: Powers, [Evaluation: From Precision, Recall and F-Measure to ROC](../../../.documents/papers/model_evaluation_metrics/powers_2020_evaluation_precision_recall_fmeasure.pdf)

### Matthews 相关系数 (MCC — Matthews Correlation Coefficient)

考虑混淆矩阵全部四格 (TP, FP, FN, TN) 的单一指标，取值 [-1, +1]。+1 = 完美预测，0 = 随机预测，-1 = 完全反转。它本质上是预测与实际之间的 Pearson 相关系数，在不平衡数据上比 F1 更可靠。

> 易混淆：**F1 分数** — F1 忽略 TN，所以在负例远多于正例时可能给出误导性的高值；MCC 不会

> 📖 Paper: Chicco & Jurman, [MCC vs F1](../../../.documents/papers/model_evaluation_metrics/chicco_jurman_2020_mcc_vs_f1.pdf)

### 真正率 (TPR — True Positive Rate)

在所有**实际为正**的样本中，被模型正确预测为正的比例。公式：TPR = TP / (TP + FN)。它和 Recall / Sensitivity 是**同一个东西的三个名字**。TPR 这个名字主要出现在 ROC 曲线的上下文中（作为 y 轴）。

> 易混淆：**FPR (False Positive Rate)** — TPR 看的是"正例多少被找到了"，FPR 看的是"负例有多少被误判了"。一个关注正例，一个关注负例

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 2

### 假正率 (FPR — False Positive Rate)

在所有**实际为负**的样本中，被模型错误预测为正的比例。公式：FPR = FP / (FP + TN) = 1 − Specificity。它是 ROC 曲线的 **x 轴**。FPR 越低越好——说明模型很少把负例误报为正例。

> 易混淆：**TPR (True Positive Rate)** — FPR 和 TPR 的分母不同：FPR 的分母是全部负例 (FP+TN)，TPR 的分母是全部正例 (TP+FN)

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 2

### 特异度 (Specificity / True Negative Rate)

在所有**实际为负**的样本中，被模型正确预测为负的比例。公式：Specificity = TN / (TN + FP) = 1 − FPR。它回答的问题是："健康人里面，模型判断为'没病'的比例是多少？"。高 Specificity 意味着误报率低。

> 易混淆：**Sensitivity (= Recall = TPR)** — Sensitivity 关注正例，Specificity 关注负例。两者互为"镜像"

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 2

### ROC 曲线 (Receiver Operating Characteristic Curve)

以假正率 (FPR = FP / (FP + TN)) 为 x 轴、真正率 (TPR = TP / (TP + FN)) 为 y 轴画的曲线。每个点对应一个分类阈值。起源于二战雷达信号检测——"接收方操作特性"就是雷达操作员区分敌机和噪声的能力。

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 3

### AUC (Area Under the Curve)

ROC 曲线下的面积。AUC = 1 表示完美分类，AUC = 0.5 表示随机猜测（对角线）。它的概率解释是：随机抽一个正例和一个负例，模型给正例打的分高于负例打的分的概率。

> 易混淆：**PR-AUC** — ROC-AUC 在类别严重不平衡时会过于乐观；PR-AUC（Precision-Recall 曲线下面积）在这种场景下更可靠

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 4

### 交叉验证 (Cross-Validation)

把数据反复切成训练集和验证集，在每一份上都训练+测试，最后取所有结果的均值作为模型性能估计。最常用的是 K-Fold CV（把数据切成 K 份，每次留一份做验证）。它解决的核心问题是：一次随机 train/test 划分的结果不稳定。

> 📖 Paper: Kohavi, [Cross-Validation and Bootstrap](../../../.documents/papers/model_evaluation_metrics/kohavi_1995_cross_validation_bootstrap.pdf)
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.5

### 均方误差 (MSE — Mean Squared Error)

回归问题中最标准的损失函数。公式：(1/n) × Σ(yᵢ - ŷᵢ)²。对大误差（离群值）非常敏感，因为误差被平方放大了。

> 易混淆：**MAE (Mean Absolute Error)** — MAE 对离群值更鲁棒（用绝对值而非平方），但梯度在零点不可导

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.2

### 学习曲线 (Learning Curve)

以训练集大小为 x 轴，训练/验证误差为 y 轴的图。用来诊断模型是**欠拟合**（两条线都高且收敛）还是**过拟合**（训练误差低但验证误差高，两线间距大）。

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.3
> 📖 Docs: [scikit-learn Learning Curve](https://scikit-learn.org/stable/modules/learning_curve.html)

---

## 概念辨析

### Precision vs Recall

| 维度 | Precision (精确率) | Recall (召回率) |
|------|-------------------|----------------|
| **本质** | 预测为正中真正为正的比例 | 实际为正中被正确识别的比例 |
| **公式** | TP / (TP + FP) | TP / (TP + FN) |
| **敏感对象** | False Positives (误报) | False Negatives (漏报) |
| **高值意味着** | 模型说"是"的时候很靠谱 | 模型不会漏掉正例 |
| **典型重视场景** | 垃圾邮件过滤（不想误杀正常邮件） | 癌症检测（不想漏诊） |

> 📖 Paper: Powers, [Evaluation](../../../.documents/papers/model_evaluation_metrics/powers_2020_evaluation_precision_recall_fmeasure.pdf)

### ROC-AUC vs PR-AUC

| 维度 | ROC-AUC | PR-AUC |
|------|---------|--------|
| **坐标轴** | FPR vs TPR | Precision vs Recall |
| **基线** | 对角线 (AUC=0.5) | 水平线 = 正例比例 |
| **不平衡数据** | 过于乐观（FPR 分母含大量 TN） | 更真实（不涉及 TN） |
| **适用场景** | 类别大致平衡 | 正例稀少（欺诈检测、疾病筛查） |

> 📖 Paper: Flach, [Precision-Recall](../../../.documents/papers/model_evaluation_metrics/flach_2020_precision_recall.pdf)
> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf)

### MSE vs MAE

| 维度 | MSE (均方误差) | MAE (平均绝对误差) |
|------|---------------|-------------------|
| **公式** | (1/n) Σ(y-ŷ)² | (1/n) Σ|y-ŷ| |
| **对离群值** | 非常敏感（平方放大） | 较鲁棒（线性惩罚） |
| **数学性质** | 处处可导 | 零点不可导 |
| **对应损失** | L2 Loss | L1 Loss |
| **单位** | 原始单位的平方 | 与原始单位一致 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.2

---

## 核心属性

### 信息架构

```
                    模型评估与度量
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    分类指标          回归指标         验证方法
    ┌────┴────┐      ┌───┴───┐      ┌───┴───┐
    │         │      │       │      │       │
  单值指标  曲线指标  MSE    R²    K-Fold  Bootstrap
  ┌──┴──┐   ┌─┴─┐   RMSE   Adj R²  LOOCV
  │     │   │   │   MAE           Stratified
  Acc  F1  ROC  PR
  Prec MCC AUC  AUC
  Rec
```

### 适用场景 ✅

- 训练完任何监督学习模型后的性能评估
- 多个模型之间的公平比较
- 超参数调优过程中的内层评分
- 检查模型是否过拟合/欠拟合

### 不适用场景 ❌

- 无监督学习的聚类质量评估（需要 Silhouette、Davies-Bouldin 等专用指标）
- 生成模型的评估（如 LLM 的文本质量——需要 BLEU、ROUGE、人工评价）
- 因果推断（模型评估只告诉你预测准不准，不告诉你因果关系）

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7
> 📖 Docs: [scikit-learn Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| TP | 实际正 → 预测正 | 病人有病，检测为阳性 |
| FP | 实际负 → 预测正（Type I Error） | 健康人，检测为阳性（误报） |
| FN | 实际正 → 预测负（Type II Error） | 病人有病，检测为阴性（漏报） |
| TN | 实际负 → 预测负 | 健康人，检测为阴性 |
| Accuracy | (TP+TN) / All | 不平衡时不可靠 |
| Precision | TP / (TP+FP) | 垃圾邮件过滤重视 |
| Recall | TP / (TP+FN) | 癌症筛查重视 |
| F1 | 2×P×R / (P+R) | Precision 和 Recall 的调和均值 |
| MCC | 综合四格 | [-1, +1]，不平衡数据更可靠 |
| AUC | ROC 曲线下面积 | [0, 1]，0.5 = 随机 |
| MSE | Σ(y-ŷ)²/n | 回归标准损失 |
| R² | 1 - RSS/TSS | [−∞, 1]，越接近 1 越好 |
| K-Fold CV | 切 K 份轮流验证 | 通常 K=5 或 K=10 |

> 📖 Paper: Raschka, [Model Evaluation](../../../.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf)
