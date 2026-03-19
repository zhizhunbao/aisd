---
topic: model_evaluation_metrics
dimension: math
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Paper: Fawcett, 'An Introduction to ROC Analysis', Pattern Recognition Letters 2006 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf"
  - "📖 Paper: Chicco & Jurman, 'The advantages of the MCC over F1', BMC Genomics 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/chicco_jurman_2020_mcc_vs_f1.pdf"
expiry: 12m
status: current
---

# Model Evaluation & Metrics 数学基础

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7
> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf)

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $n$ | 样本总数 | Total samples | 正整数 |
| $y_i$ | 第 i 个样本的真实标签 | True label | {0, 1}（二分类）|
| $\hat{y}_i$ | 第 i 个样本的预测标签 | Predicted label | {0, 1}（二分类）|
| $f(x_i)$ | 模型对第 i 个样本的预测分数 | Score / probability | [0, 1] 或 ℝ |
| $t$ | 分类阈值（Score ≥ t → 预测为正） | Threshold | [0, 1] |
| TP | 真正例数 | True Positives | {0, 1, ..., n} |
| FP | 假正例数 | False Positives | {0, 1, ..., n} |
| FN | 假负例数 | False Negatives | {0, 1, ..., n} |
| TN | 真负例数 | True Negatives | {0, 1, ..., n} |
| $K$ | 交叉验证折数 | Number of folds | 正整数，通常 5 或 10 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.2

---

## 核心公式

### 公式 1: 混淆矩阵 (Confusion Matrix)

**直觉：** 把每个预测按"猜对没有"和"实际是什么"放进一个 2×2 格子里

$$
\begin{bmatrix}
& \text{Predicted +} & \text{Predicted −} \\
\text{Actual +} & TP & FN \\
\text{Actual −} & FP & TN
\end{bmatrix}
$$

> 📖 Paper: Grandini et al., [Confusion Matrix](../../../.documents/papers/model_evaluation_metrics/grandini_2020_confusion_matrix.pdf), Section 2

**约束：** TP + FP + FN + TN = n（四格之和等于样本总数）

---

### 公式 2: Precision, Recall, F1

**直觉：** Precision = "模型说'是'的里面有多少对的"；Recall = "实际的正例里有多少被找到了"

$$
\text{Precision} = \frac{TP}{TP + FP}
$$

$$
\text{Recall} = \frac{TP}{TP + FN}
$$

$$
F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}
$$

> 📖 Paper: Powers, [Evaluation](../../../.documents/papers/model_evaluation_metrics/powers_2020_evaluation_precision_recall_fmeasure.pdf), Section 2

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| TP | 正确预测的正例 | 有病且检出 |
| FP | 错误预测的正例 | 没病但报了阳性 |
| FN | 遗漏的正例 | 有病但没检出 |

**推导 F1 等价形式：**

1. 从调和平均定义出发：$\frac{1}{F_1} = \frac{1}{2}\left(\frac{1}{P} + \frac{1}{R}\right)$
2. 代入 P 和 R：$\frac{1}{F_1} = \frac{1}{2}\left(\frac{TP+FP}{TP} + \frac{TP+FN}{TP}\right) = \frac{2 \cdot TP + FP + FN}{2 \cdot TP}$
3. 取倒数：$F_1 = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$

> 📖 Paper: Powers, [Evaluation](../../../.documents/papers/model_evaluation_metrics/powers_2020_evaluation_precision_recall_fmeasure.pdf)

---

### 公式 3: Fβ 广义 F 分数

**直觉：** F1 对 Precision 和 Recall 同等重视，但有时你更在意其中一个（比如看病不想漏诊 → 更重 Recall）

$$
F_\beta = (1 + \beta^2) \times \frac{\text{Precision} \times \text{Recall}}{\beta^2 \times \text{Precision} + \text{Recall}}
$$

> 📖 Paper: Powers, [Evaluation](../../../.documents/papers/model_evaluation_metrics/powers_2020_evaluation_precision_recall_fmeasure.pdf), Section 3

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| β = 1 | 同等重视 P 和 R | 标准 F1 |
| β = 2 | Recall 权重为 Precision 的 4 倍 | 癌症筛查（不想漏） |
| β = 0.5 | Precision 权重为 Recall 的 4 倍 | 垃圾邮件过滤（不想误杀） |

---

### 公式 4: Matthews 相关系数 (MCC)

**直觉：** 用混淆矩阵全部四格算出预测与实际之间的相关性，+1 完美，0 随机，-1 完全反转

$$
MCC = \frac{TP \times TN - FP \times FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}
$$

> 📖 Paper: Chicco & Jurman, [MCC vs F1](../../../.documents/papers/model_evaluation_metrics/chicco_jurman_2020_mcc_vs_f1.pdf), Eq. 1

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| 分子 TP×TN − FP×FN | 对角线乘积差（正确 vs 错误的"势"） | 类似于 Pearson r 的分子 |
| 分母 | 四个边缘频率的几何平均 | 归一化因子 |

---

### 公式 5: ROC 曲线坐标 (TPR 和 FPR)

**直觉：** 对每个阈值 t，算两个比率：正例被正确识别的比例（y 轴）和负例被错误识别的比例（x 轴）

$$
TPR(t) = \frac{TP(t)}{TP(t) + FN(t)} = \text{Recall}(t)
$$

$$
FPR(t) = \frac{FP(t)}{FP(t) + TN(t)} = 1 - \text{Specificity}(t)
$$

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 3, Fig. 1

**AUC 的概率解释：**

$$
AUC = P(\hat{f}(x^+) > \hat{f}(x^-))
$$

即随机抽一对 (正例, 负例)，模型给正例的分 > 给负例的分的概率。

> 📖 Paper: Fawcett, [ROC Analysis](../../../.documents/papers/model_evaluation_metrics/fawcett_2006_roc_introduction.pdf), Section 4

---

### 公式 6: 交叉验证估计 (K-Fold CV)

**直觉：** 把数据切 K 份，每次留 1 份做测试、其余 K-1 份训练，重复 K 次取平均，得到更稳定的性能估计

$$
\text{CV}_{(K)} = \frac{1}{K} \sum_{k=1}^{K} L(y^{(k)},\ \hat{f}^{(-k)}(x^{(k)}))
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq. 7.48

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $K$ | 折数 | 通常 5 或 10 |
| $\hat{f}^{(-k)}$ | 在去掉第 k 折后训练的模型 | 用 K-1 份数据训练 |
| $L(\cdot)$ | 损失函数（如误分类率、MSE） | 选择取决于任务类型 |
| $(x^{(k)}, y^{(k)})$ | 第 k 折的数据 | 留出的验证集 |

**推导 K-Fold CV 方差来源：**

1. 不同折数据分布不同 → 每折估计有波动
2. K 越大（极端: K=n, LOOCV）→ 训练集越大、偏差越低，但方差越高（各折高度相关）
3. K=5 或 K=10 经验上在偏差和方差之间取得好的平衡

> 📖 Paper: Kohavi, [Cross-Validation and Bootstrap](../../../.documents/papers/model_evaluation_metrics/kohavi_1995_cross_validation_bootstrap.pdf), Section 4

---

### 公式 7: MSE、RMSE、MAE、R²

**直觉：** 衡量回归预测值和真实值之间的"距离"，用不同方式聚合

$$
MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

$$
RMSE = \sqrt{MSE}
$$

$$
MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|
$$

$$
R^2 = 1 - \frac{RSS}{TSS} = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}
$$

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.3 Eq. 3.17

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| RSS | 残差平方和 | 模型没解释掉的变异 |
| TSS | 总平方和 | 数据本身的总变异 |
| $\bar{y}$ | 真实值均值 | 最简单的"预测"基线 |

---

## 公式关系图

```
              混淆矩阵
        ┌───────┼───────┐
        │       │       │
     TP, FP   FN, TN   全部四格
        │       │       │
        ↓       ↓       ↓
    Precision  Recall   MCC
        │       │
        └───┬───┘
            ↓
     F1 (调和平均)
            │
            ↓
     Fβ (广义 F)

    阈值 t 滑动
        │
    ┌───┴───┐
    TPR(t)  FPR(t)
    │       │
    └───┬───┘
        ↓
    ROC 曲线
        ↓
      AUC

    训练/测试划分
        ↓
    K-Fold CV → CV 误差均值 ± 标准差
```

---

## 手算练习

### 练习 1: 从混淆矩阵算全部指标

**题目：** 一个垃圾邮件分类器在 100 封邮件上的混淆矩阵如下：

| | 预测: 垃圾 | 预测: 正常 |
|---|---|---|
| **实际: 垃圾** | TP = 8 | FN = 2 |
| **实际: 正常** | FP = 5 | TN = 85 |

计算 Accuracy, Precision, Recall, F1, MCC。

**解答步骤：**

1. Accuracy = (8 + 85) / 100 = **0.93**
2. Precision = 8 / (8 + 5) = 8/13 ≈ **0.615**
3. Recall = 8 / (8 + 2) = 8/10 = **0.80**
4. F1 = 2 × 0.615 × 0.80 / (0.615 + 0.80) = 0.984 / 1.415 ≈ **0.696**
5. MCC = (8×85 − 5×2) / √((8+5)(8+2)(85+5)(85+2))
   = (680 − 10) / √(13 × 10 × 90 × 87)
   = 670 / √(1,017,900)
   = 670 / 1008.9 ≈ **0.664**

**观察：** Accuracy 高达 93%，但 Precision 只有 61.5%——因为正常邮件（负例）占 90%，Accuracy 被 TN 撑高了。F1 和 MCC 更真实地反映了模型在垃圾邮件识别上的性能。

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| Accuracy | (TP+TN)/(TP+FP+FN+TN) | 总体正确率 | 混淆矩阵 |
| Precision | TP/(TP+FP) | 预测为正的可靠性 | 混淆矩阵 |
| Recall | TP/(TP+FN) | 正例的覆盖率 | 混淆矩阵 |
| F1 | 2TP/(2TP+FP+FN) | P-R 调和均值 | Precision, Recall |
| Fβ | (1+β²)PR/(β²P+R) | 加权 P-R | Precision, Recall |
| MCC | (TP·TN−FP·FN)/√(…) | 全面相关性 | 混淆矩阵四格 |
| TPR | TP/(TP+FN) | ROC y 轴 | = Recall |
| FPR | FP/(FP+TN) | ROC x 轴 | 混淆矩阵 |
| AUC | ∫ TPR d(FPR) | 排序能力 | ROC 曲线 |
| MSE | Σ(y−ŷ)²/n | 回归损失 | — |
| RMSE | √MSE | 同单位损失 | MSE |
| MAE | Σ|y−ŷ|/n | 鲁棒损失 | — |
| R² | 1−RSS/TSS | 解释变异比 | MSE |
| CV(K) | (1/K)ΣL_k | 泛化估计 | 数据划分 |
