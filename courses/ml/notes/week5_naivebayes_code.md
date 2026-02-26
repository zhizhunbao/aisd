# Week 5: Naive Bayes & BBN — 代码参考

> **Source:** slides `Week5_NaiveBayes.pdf` + lab4 code
> **Scope:** Naive Bayes implementation, Gaussian PDF, Laplace smoothing
> **See also:** [week5_naivebayes_cheatsheet.md](week5_naivebayes_cheatsheet.md) (概念速查) | [week5_naivebayes_math.md](week5_naivebayes_math.md) (公式+手算)

---

## Gaussian PDF Computation

**scipy one-liner:** $\frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$

```python
from scipy.stats import norm

# Gaussian PDF: P(x | μ, σ) — note: σ is std dev, NOT variance
# 高斯概率密度：注意参数是标准差 σ，不是方差 σ²
p = norm.pdf(x, loc=mu, scale=sigma)  # scale = √(variance)
```

**manual numpy:**

```python
import numpy as np

# Manual Gaussian PDF: (1/√(2πσ²)) × exp(-(x-μ)²/(2σ²))
# 手动计算高斯概率密度
coeff = 1 / np.sqrt(2 * np.pi * var)
exponent = -(x - mean)**2 / (2 * var)
pdf = coeff * np.exp(exponent)
```

---

## Statistics Computation

```python
import numpy as np

# Mean per feature / 每个特征的均值
mean = data.mean(axis=0)

# Sample variance (ddof=1) — Bessel's correction: divide by (n-1)
# 样本方差 (ddof=1) — 贝塞尔校正：除以 (n-1)，不是 n
var = data.var(axis=0, ddof=1)  # ⚠️ MUST use ddof=1

# Sample covariance matrix / 样本协方差矩阵
cov = np.cov(data.T, ddof=1)   # ⚠️ ddof=1 for sample covariance
```

---

## sklearn GaussianNB Pipeline

```python
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Split data / 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train: estimate μ, σ² per class per feature
# 训练：估计每个类别每个特征的 μ 和 σ²
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# Predict: argmax P(Y) × ∏ P(Xᵢ|Y)
# 预测：选择使后验最大的类别
y_pred = gnb.predict(X_test)
acc = accuracy_score(y_test, y_pred)
```

**Learned parameters:**

```python
gnb.class_prior_   # Prior probabilities P(Y)          — 先验概率
gnb.theta_         # Per-class mean (μ) for each feature — 每类每特征的均值
gnb.var_           # Per-class variance (σ²)            — 每类每特征的方差
```

---

## Manual Naive Bayes (Lab4 Pattern)

```python
import numpy as np
from scipy.stats import norm

# Step 1: Organize data by class / 按类别组织数据
male_data = np.array([
    [6.00, 75, 9.0],   # [Height, Weight, Foot Size]
    [5.92, 80, 9.5],
    [5.58, 67, 8.0],
    [5.92, 70, 9.0],
])
female_data = np.array([
    [5.00, 55, 5.0],
    [5.50, 60, 7.0],
    [5.42, 58, 6.5],
    [5.75, 63, 8.0],
])

# Step 2: Compute priors P(Y) / 计算先验概率
n_total = len(male_data) + len(female_data)
p_male = len(male_data) / n_total     # P(Male)  = 0.5
p_female = len(female_data) / n_total  # P(Female) = 0.5

# Step 3: Compute per-class μ and σ² (ddof=1!) / 每类的均值和样本方差
male_mean = male_data.mean(axis=0)
male_var = male_data.var(axis=0, ddof=1)   # ⚠️ sample variance
female_mean = female_data.mean(axis=0)
female_var = female_data.var(axis=0, ddof=1)

# Step 4: Classify test sample / 对测试样本分类
test = np.array([5.0, 80, 5.0])

# Gaussian likelihood: ∏ P(Xᵢ | class) / 高斯似然
lik_male = np.prod(norm.pdf(test, male_mean, np.sqrt(male_var)))
lik_female = np.prod(norm.pdf(test, female_mean, np.sqrt(female_var)))

# Posterior ∝ Prior × Likelihood / 后验 ∝ 先验 × 似然
post_male = p_male * lik_male
post_female = p_female * lik_female

# Step 5: Compare and classify / 比较后验，选择最大的类别
prediction = "Male" if post_male > post_female else "Female"
```

---

## Laplace Smoothing

```python
# Original:  P(c|Y) = count / total         → can be ZERO!
# Smoothed:  P(c|Y) = (count + 1) / (total + v)
# v = number of possible values for this attribute

count = 0       # P(Married|Evade=Yes): 0 married evaders
total = 3       # Total evaders in class Yes
v = 3           # Marital Status: {Single, Married, Divorced}

p_original = count / total               # = 0     ← KILLS product!
p_smoothed = (count + 1) / (total + v)   # = 1/6   ← product survives
```

**m-estimate generalization:**

```python
# m-estimate: P(c|Y) = (count + m×p) / (total + m)
# m=0 → MLE | m=v,p=1/v → Laplace | m→∞ → prior only

m = 3
p = 1/v  # = 1/3
p_m_estimate = (count + m * p) / (total + m)  # = 1/6
```
