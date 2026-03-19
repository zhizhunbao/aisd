---
topic: overfitting
dimension: code
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Docs: scikit-learn Model Selection — https://scikit-learn.org/stable/modules/cross_validation.html"
  - "📖 Docs: scikit-learn learning_curve — https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.learning_curve.html"
  - "📖 Docs: scikit-learn validation_curve — https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.validation_curve.html"
  - "📚 Book: James, Witten, Hastie & Tibshirani, 《An Introduction to Statistical Learning》 Ch.5 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
expiry: 6m
status: current
---

# Overfitting 代码参考

> 📖 Docs: [scikit-learn Model Selection](https://scikit-learn.org/stable/modules/cross_validation.html)

## 快速开始

### 最简示例 — 30 秒看到 overfitting

```python
# ============================================================
# 最简 overfitting 演示 / Minimal overfitting demo
# 用多项式回归展示 underfitting vs optimal vs overfitting
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 生成数据: 真实函数 f(x) = sin(πx) + 噪声 / Generate data: true f(x) = sin(πx) + noise
np.random.seed(42)
n = 20  # 样本数 / number of samples
X = np.sort(np.random.uniform(0, 1, n)).reshape(-1, 1)
y = np.sin(np.pi * X).ravel() + np.random.normal(0, 0.2, n)

# 测试集 / Test set
X_test = np.linspace(0, 1, 200).reshape(-1, 1)
y_test_true = np.sin(np.pi * X_test).ravel()

# 三种复杂度对比 / Compare three complexity levels
for d, label in [(1, "d=1 欠拟合/Underfit"), (3, "d=3 最优/Optimal"), (15, "d=15 过拟合/Overfit")]:
    poly = PolynomialFeatures(d)
    X_poly = poly.fit_transform(X)
    X_test_poly = poly.transform(X_test)

    model = LinearRegression().fit(X_poly, y)
    y_pred = model.predict(X_test_poly)

    train_err = mean_squared_error(y, model.predict(X_poly))
    # 用真实函数作为参考 / Use true function as reference
    test_err = mean_squared_error(y_test_true, y_pred)

    print(f"{label}: 训练MSE={train_err:.4f}, 测试MSE={test_err:.4f}")
```

**测试方法：** 运行后应看到 d=1 训练/测试误差都较高（欠拟合），d=3 两者都较低（最优），d=15 训练误差极低但测试误差极高（过拟合）

---

## 完整实现示例

### 示例 1: Learning Curve — 诊断 overfitting vs underfitting

```python
# ============================================================
# 1. 导入依赖 / Import dependencies
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.datasets import make_regression

# ============================================================
# 2. 生成数据 / Generate data
# ============================================================
# 生成非线性数据 / Generate nonlinear data
np.random.seed(42)
n_samples = 200
X = np.sort(np.random.uniform(0, 1, n_samples)).reshape(-1, 1)
y = np.sin(4 * np.pi * X).ravel() + np.random.normal(0, 0.3, n_samples)

# ============================================================
# 3. 定义不同复杂度的模型 / Define models of different complexity
# ============================================================
models = {
    "d=1 线性/Linear (Underfit)": make_pipeline(PolynomialFeatures(1), LinearRegression()),
    "d=4 四阶/Quartic (Good)": make_pipeline(PolynomialFeatures(4), LinearRegression()),
    "d=15 高阶/High-deg (Overfit)": make_pipeline(PolynomialFeatures(15), LinearRegression()),
}

# ============================================================
# 4. 绘制 Learning Curve / Plot learning curves
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for ax, (name, model) in zip(axes, models.items()):
    # learning_curve 返回训练集大小、训练分数、验证分数
    # Returns train sizes, train scores, validation scores
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y,
        train_sizes=np.linspace(0.1, 1.0, 10),  # 训练集从10%到100% / Train set from 10% to 100%
        cv=5,                                     # 5折交叉验证 / 5-fold CV
        scoring='neg_mean_squared_error',          # 负MSE（sklearn约定越高越好） / Neg MSE (sklearn convention)
        n_jobs=-1                                  # 并行计算 / Parallel
    )

    # 转换为正MSE / Convert to positive MSE
    train_mean = -train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = -val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)

    # 绘图 / Plot
    ax.plot(train_sizes, train_mean, 'o-', label='训练误差/Train Error')
    ax.plot(train_sizes, val_mean, 'o-', label='验证误差/Val Error')
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1)
    ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1)
    ax.set_title(name)
    ax.set_xlabel('训练集大小 / Training Set Size')
    ax.set_ylabel('MSE')
    ax.legend()
    ax.set_ylim(0, 1.5)

plt.tight_layout()
plt.savefig('learning_curve_comparison.png', dpi=150)
plt.show()
```

### 示例 2: Validation Curve — 找最优超参数

```python
# ============================================================
# 1. 导入依赖 / Import dependencies
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import validation_curve
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline

# ============================================================
# 2. 生成数据 / Generate data
# ============================================================
np.random.seed(42)
n_samples = 100
X = np.sort(np.random.uniform(0, 1, n_samples)).reshape(-1, 1)
y = np.sin(2 * np.pi * X).ravel() + np.random.normal(0, 0.3, n_samples)

# ============================================================
# 3. Validation Curve: 多项式阶数 vs 误差
# Polynomial degree as the hyperparameter to tune
# ============================================================
degrees = np.arange(1, 20)
train_scores_list = []
val_scores_list = []

for d in degrees:
    model = make_pipeline(PolynomialFeatures(d), Ridge(alpha=0.01))
    # 手动做 5-fold CV / Manual 5-fold CV
    from sklearn.model_selection import cross_validate
    cv_results = cross_validate(model, X, y, cv=5,
                                 scoring='neg_mean_squared_error',
                                 return_train_score=True)
    train_scores_list.append(-cv_results['train_score'].mean())
    val_scores_list.append(-cv_results['test_score'].mean())

# ============================================================
# 4. 绘制 Validation Curve / Plot validation curve
# ============================================================
plt.figure(figsize=(10, 6))
plt.plot(degrees, train_scores_list, 'o-', label='训练误差/Train Error')
plt.plot(degrees, val_scores_list, 'o-', label='验证误差/Val Error')
plt.xlabel('多项式阶数 / Polynomial Degree')
plt.ylabel('MSE')
plt.title('Validation Curve: 多项式阶数 vs 误差 / Degree vs Error')
plt.legend()
plt.axvline(x=degrees[np.argmin(val_scores_list)], color='r', linestyle='--',
            label=f'最优阶数/Best d={degrees[np.argmin(val_scores_list)]}')
plt.legend()
plt.savefig('validation_curve.png', dpi=150)
plt.show()

print(f"最优多项式阶数 / Best polynomial degree: {degrees[np.argmin(val_scores_list)]}")
```

### 示例 3: Bias-Variance 分解可视化

```python
# ============================================================
# 1. Bias-Variance 分解实验 / Bias-Variance decomposition experiment
# 对同一个 x₀ 点，用 100 个不同训练集分别训练，计算 bias 和 variance
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

np.random.seed(42)

# 真实函数 / True function
f_true = lambda x: np.sin(np.pi * x)

# 实验参数 / Experiment parameters
n_experiments = 200  # 重复实验次数 / Number of repeated experiments
n_train = 20         # 每次训练样本数 / Training samples per experiment
noise_std = 0.3      # 噪声标准差 / Noise std
x0 = 0.5             # 测试点 / Test point

degrees = range(1, 16)
bias_squared = []
variance = []
total_error = []

for d in degrees:
    predictions = []

    for _ in range(n_experiments):
        # 生成新训练集 / Generate new training set
        X_train = np.random.uniform(0, 1, n_train).reshape(-1, 1)
        y_train = f_true(X_train).ravel() + np.random.normal(0, noise_std, n_train)

        # 训练多项式回归 / Train polynomial regression
        poly = PolynomialFeatures(d)
        X_poly = poly.fit_transform(X_train)
        model = LinearRegression().fit(X_poly, y_train)

        # 预测测试点 / Predict test point
        x0_poly = poly.transform([[x0]])
        predictions.append(model.predict(x0_poly)[0])

    predictions = np.array(predictions)
    f_x0 = f_true(x0)  # 真实值 / True value

    # 计算 Bias² 和 Variance / Compute Bias² and Variance
    bias_sq = (predictions.mean() - f_x0) ** 2
    var = predictions.var()

    bias_squared.append(bias_sq)
    variance.append(var)
    total_error.append(bias_sq + var + noise_std**2)

# ============================================================
# 2. 绘制 Bias²-Variance-Total Error 曲线 / Plot decomposition
# ============================================================
plt.figure(figsize=(10, 6))
plt.plot(list(degrees), bias_squared, 'b-o', label='Bias²')
plt.plot(list(degrees), variance, 'r-o', label='Variance')
plt.plot(list(degrees), total_error, 'k-o', label='Total Error (Bias²+Var+σ²)')
plt.axhline(y=noise_std**2, color='gray', linestyle='--', label=f'σ²={noise_std**2}')
plt.xlabel('多项式阶数 / Polynomial Degree')
plt.ylabel('Error')
plt.title('Bias-Variance Tradeoff 可视化 / Visualization')
plt.legend()
plt.savefig('bias_variance_tradeoff.png', dpi=150)
plt.show()
```

---

## API 速查

### sklearn.model_selection

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `learning_curve()` | `estimator` | — | 模型对象 / Model object |
| ↳ | `X, y` | — | 数据 / Data |
| ↳ | `train_sizes` | `[0.1,0.33,0.55,0.78,1.0]` | 训练集比例 / Train set fractions |
| ↳ | `cv` | `5` | 交叉验证折数 / CV folds |
| ↳ | `scoring` | `None` | 评分函数 / Scoring function |
| ↳ | `n_jobs` | `None` | 并行数（-1=全部） / Parallel jobs |
| `validation_curve()` | `estimator` | — | 模型对象 / Model object |
| ↳ | `X, y` | — | 数据 / Data |
| ↳ | `param_name` | — | 超参数名 / Hyperparameter name |
| ↳ | `param_range` | — | 超参数范围 / Parameter range |
| ↳ | `cv` | `5` | 交叉验证折数 / CV folds |
| `cross_val_score()` | `estimator` | — | 模型对象 / Model object |
| ↳ | `X, y` | — | 数据 / Data |
| ↳ | `cv` | `5` | 交叉验证折数 / CV folds |
| ↳ | `scoring` | `None` | 评分函数 / Scoring function |
| `cross_validate()` | `return_train_score` | `False` | 是否返回训练分数 / Return train scores |
| `KFold()` | `n_splits` | `5` | 折数 / Number of folds |
| ↳ | `shuffle` | `False` | 是否打乱 / Shuffle before split |
| ↳ | `random_state` | `None` | 随机种子 / Random seed |

### sklearn.linear_model

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `Ridge()` | `alpha` | `1.0` | L2 正则化强度 / L2 regularization strength |
| `Lasso()` | `alpha` | `1.0` | L1 正则化强度 / L1 regularization strength |
| `ElasticNet()` | `alpha` | `1.0` | 正则化强度 / Regularization strength |
| ↳ | `l1_ratio` | `0.5` | L1 权重占比 / L1 ratio (0=Ridge, 1=Lasso) |

---

## 目录结构模板

### 简单结构

```
overfitting_demo/
├── demo.py               ← 快速开始：多项式过拟合演示
├── learning_curve.py     ← 学习曲线可视化
└── validation_curve.py   ← 验证曲线可视化
```

### 标准结构

```
overfitting_analysis/
├── config.py             ← 实验参数配置
├── data_generator.py     ← 数据生成（真实函数 + 噪声）
├── models.py             ← 不同复杂度的模型定义
├── bias_variance.py      ← Bias-Variance 分解实验
├── diagnostics.py        ← Learning curve + Validation curve
├── regularization.py     ← Ridge/Lasso/ElasticNet 对比
├── results/              ← 图片输出
└── README.md             ← 实验说明
```
