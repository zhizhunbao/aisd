# Evaluation Metrics & Loss Functions (评估指标与损失函数)

> This file contains loss functions and evaluation metrics used in machine learning.

---

## Loss Functions (损失函数)

### Mean Squared Error, MSE (均方误差)

**Tags:** `#loss` `#regression` `#ml-week4`

**📐 Formula:**

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

- $y_i$ = actual value (target)
- $\hat{y}_i$ = predicted value
- $n$ = number of samples

**💡 Intuition (直觉理解):**
> Squaring penalizes large errors heavily. An error of 10 becomes 100, while an error of 2 becomes 4. The large error is penalized 25x more. This makes MSE sensitive to outliers.
>> 平方会重重惩罚大误差。误差10变成100，而误差2变成4。大误差被多惩罚25倍。这使得MSE对离群值敏感。

**⚖️ Also Known As:**
- Quadratic Loss
- L2 Loss

**📚 Appears In:**
- ML Week 4 §7.2 (Regression Loss Functions)

---

### Mean Absolute Error, MAE (平均绝对误差)

**Tags:** `#loss` `#regression` `#ml-week4`

**📐 Formula:**

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n}|y_i - \hat{y}_i|$$

- $y_i$ = actual value
- $\hat{y}_i$ = predicted value
- $n$ = number of samples

**💡 Intuition (直觉理解):**
> Takes absolute difference, not squared. More robust to outliers since large errors aren't amplified. Linear penalty instead of quadratic.
>> 取绝对差，不是平方。对离群值更鲁棒，因为大误差不会被放大。线性惩罚而不是二次惩罚。

**⚖️ Also Known As:**
- L1 Loss

**⚖️ Compare MSE vs MAE:**
| Feature | MSE | MAE |
|---|---|---|
| Outlier sensitivity | High (squared) | Low (linear) |
| Gradient at 0 | 0 (smooth) | Constant (non-smooth) |
| Optimization | Easier | Harder (non-differentiable at 0) |

**📚 Appears In:**
- ML Week 4 §7.2 (Regression Loss Functions)

---

### Cross Entropy Loss (交叉熵损失)

**Tags:** `#loss` `#classification` `#ml-week4`

**📐 Formula:**

Binary CE: $$L = -[y \cdot \log(\hat{y}) + (1-y) \cdot \log(1-\hat{y})]$$

Categorical CE: $$L = -\sum_i y_i \cdot \log(\hat{y}_i)$$

- $y$ = true distribution (one-hot for categorical)
- $\hat{y}$ = predicted probabilities

**💡 Intuition (直觉理解):**
> Cross Entropy heavily penalizes confident wrong predictions. If true label = 1 and you predict 0.01, the -log(0.01) ≈ 4.6 is huge. This forces the model to avoid confident mistakes.
>> 交叉熵严重惩罚自信的错误预测。如果真实标签=1而你预测0.01，-log(0.01) ≈ 4.6非常大。这迫使模型避免自信的错误。

**⚙️ Variants:**
- **Binary CE** — two classes (0 and 1)
- **Categorical CE** — one-hot encoded labels
- **Sparse Categorical CE** — integer labels (saves memory)

**📚 Appears In:**
- ML Week 4 §7.3 (Probabilistic Loss Functions)

---

### Hinge Loss (合页损失)

**Tags:** `#loss` `#classification` `#svm` `#ml-week4`

**📐 Formula:**

$$\text{Hinge} = \max(0, 1 - y \cdot \hat{y})$$

- $y \in \{-1, +1\}$ (NOT 0,1!)
- $\hat{y}$ = raw model output (NOT probability)

**💡 Intuition (直觉理解):**
> Loss is 0 when the correct class is confidently predicted (margin > 1). Penalizes predictions close to the decision boundary. Maximizes the margin between classes.
>> 当正确类别被自信预测（间隔 > 1）时损失为0。惩罚接近决策边界的预测。最大化类别之间的间隔。

**⚠️ Important:**
- Requires labels to be **-1 and +1**, not 0 and 1
- Primarily used with SVMs
- For multi-class: use Categorical Hinge Loss

**📚 Appears In:**
- ML Week 4 §7.4 (Hinge Loss)

---

## Evaluation Metrics (评估指标)

*Reserved for future metrics: Precision, Recall, F1, IoU, Accuracy, Confusion Matrix, etc.*
*Will be populated when CNN/classification course content is processed.*

---
