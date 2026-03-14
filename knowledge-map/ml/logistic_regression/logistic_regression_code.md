---
topic: logistic_regression
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: scikit-learn LogisticRegression — https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression"
  - "💻 Source: scikit-learn _logistic.py — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn/linear_model/_logistic.py"
  - "📚 Book: Hastie et al., ESL Ch.4.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., ISLR Ch.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
expiry: 6m
status: current
---

# Logistic Regression 代码参考

> 📖 Docs: [scikit-learn LogisticRegression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
> 💻 Source: [scikit-learn _logistic.py](../../../.github/scikit-learn/sklearn/linear_model/_logistic.py)


## 快速开始

### 最简示例 — 30 秒上手

```python
# === Logistic Regression 最简示例 ===
# === Logistic Regression Minimal Example ===

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# 加载数据（取前两类做二分类）
# Load data (take first two classes for binary)
X, y = load_iris(return_X_y=True)
X, y = X[y != 2], y[y != 2]

# 划分训练/测试集
# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 训练模型（一行搞定）
# Train model (one-liner)
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# 预测类别和概率
# Predict class and probability
y_pred = model.predict(X_test)           # 类别标签 / class labels
y_prob = model.predict_proba(X_test)     # 概率 / probabilities

# 评估
# Evaluate
print(f"准确率 / Accuracy: {model.score(X_test, y_test):.4f}")
print(f"系数 / Coefficients: {model.coef_}")
print(f"截距 / Intercept: {model.intercept_}")
```

**测试方法：** 运行后应输出 Accuracy ≈ 1.0（Iris 前两类线性可分）

> 📖 Docs: [scikit-learn LogisticRegression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

---

## 完整实现示例

### 示例 1: 从零实现 Logistic Regression（纯 NumPy）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 生成二分类数据集
# Generate binary classification dataset
X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=5,
    n_redundant=2, random_state=42
)

# 标准化特征（LR 对特征尺度敏感）
# Standardize features (LR is scale-sensitive)
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
class LogisticRegressionScratch:
    """从零实现的 Logistic Regression / Logistic Regression from scratch"""
    
    def __init__(self, lr=0.01, n_iters=1000, lambda_reg=0.01):
        self.lr = lr                # 学习率 / learning rate
        self.n_iters = n_iters      # 迭代次数 / number of iterations
        self.lambda_reg = lambda_reg # L2 正则化系数 / L2 regularization
        self.weights = None         # 权重 / weights
        self.bias = None            # 偏置 / bias
        self.losses = []            # 损失记录 / loss history
    
    def _sigmoid(self, z):
        """Sigmoid 函数（数值稳定版本）
        Sigmoid function (numerically stable version)"""
        return np.where(
            z >= 0,
            1 / (1 + np.exp(-z)),       # z >= 0 时直接计算 / direct for z >= 0
            np.exp(z) / (1 + np.exp(z)) # z < 0 时用等价形式避免溢出 / avoid overflow
        )
    
    def _cross_entropy(self, y, p):
        """交叉熵损失 + L2 正则化
        Cross-entropy loss with L2 regularization"""
        eps = 1e-15  # 数值稳定 / numerical stability
        p = np.clip(p, eps, 1 - eps)
        ce = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
        l2 = (self.lambda_reg / 2) * np.sum(self.weights ** 2)
        return ce + l2
    
    def fit(self, X, y):
        """训练模型（梯度下降法）
        Train model using gradient descent"""
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)  # 零初始化 / zero initialization
        self.bias = 0
        
        for i in range(self.n_iters):
            # 前向传播 / Forward pass
            z = X @ self.weights + self.bias  # 线性组合 / linear combination
            p = self._sigmoid(z)              # 概率 / probability
            
            # 计算梯度 / Compute gradients
            dw = (1/n_samples) * (X.T @ (p - y)) + self.lambda_reg * self.weights
            db = (1/n_samples) * np.sum(p - y)
            
            # 更新参数 / Update parameters
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
            
            # 记录损失 / Record loss
            loss = self._cross_entropy(y, p)
            self.losses.append(loss)
        
        return self
    
    def predict_proba(self, X):
        """预测概率 / Predict probabilities"""
        z = X @ self.weights + self.bias
        p1 = self._sigmoid(z)
        return np.column_stack([1 - p1, p1])  # [P(0), P(1)]
    
    def predict(self, X, threshold=0.5):
        """预测类别 / Predict class labels"""
        proba = self.predict_proba(X)[:, 1]
        return (proba >= threshold).astype(int)
    
    def score(self, X, y):
        """计算准确率 / Compute accuracy"""
        return np.mean(self.predict(X) == y)

# ============================================================
# 3. 训练 / Training
# ============================================================
model = LogisticRegressionScratch(lr=0.1, n_iters=500, lambda_reg=0.01)
model.fit(X_train, y_train)

# ============================================================
# 4. 评估 / Evaluation
# ============================================================
print(f"训练准确率 / Train Accuracy: {model.score(X_train, y_train):.4f}")
print(f"测试准确率 / Test Accuracy:  {model.score(X_test, y_test):.4f}")
print(f"最终损失 / Final Loss: {model.losses[-1]:.4f}")
print(f"权重 / Weights: {model.weights}")

# 可视化损失曲线 / Visualize loss curve
import matplotlib.pyplot as plt
plt.plot(model.losses)
plt.xlabel("Iteration")
plt.ylabel("Cross-Entropy Loss")
plt.title("Training Loss Curve")
plt.grid(True)
plt.show()
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4 — 梯度推导
> 📖 Docs: [scikit-learn LogisticRegression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

---

### 示例 2: scikit-learn 完整工程实践（二分类 + 评估 + 可视化）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_curve, auc, precision_recall_curve
)

# 乳腺癌数据集（真实医疗数据，569 样本，30 特征）
# Breast cancer dataset (real medical data, 569 samples, 30 features)
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = data.feature_names

# 标准化 / Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# 2. 模型训练（含超参调优）/ Model Training with Hyperparameter Tuning
# ============================================================
# 尝试不同的 C 值（正则化强度的倒数）
# Try different C values (inverse regularization strength)
C_values = [0.001, 0.01, 0.1, 1, 10, 100]
results = {}

for C in C_values:
    model = LogisticRegression(C=C, penalty='l2', solver='lbfgs', max_iter=1000)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    results[C] = scores.mean()
    print(f"C={C:>6}: CV Accuracy = {scores.mean():.4f} ± {scores.std():.4f}")

# 选择最佳 C / Select best C
best_C = max(results, key=results.get)
print(f"\n最佳 C / Best C: {best_C}")

# ============================================================
# 3. 最终模型训练 / Final Model Training
# ============================================================
final_model = LogisticRegression(
    C=best_C, penalty='l2', solver='lbfgs', max_iter=1000, random_state=42
)
final_model.fit(X_train, y_train)

# ============================================================
# 4. 评估 / Evaluation
# ============================================================
y_pred = final_model.predict(X_test)
y_prob = final_model.predict_proba(X_test)[:, 1]

# 分类报告 / Classification report
print("\n分类报告 / Classification Report:")
print(classification_report(y_test, y_pred, target_names=data.target_names))

# 混淆矩阵 / Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(f"混淆矩阵 / Confusion Matrix:\n{cm}")

# 特征重要性（系数的绝对值）/ Feature importance (absolute coefficients)
coef_importance = np.abs(final_model.coef_[0])
top_features = np.argsort(coef_importance)[::-1][:10]
print("\nTop 10 特征 / Top 10 Features:")
for i, idx in enumerate(top_features):
    print(f"  {i+1}. {feature_names[idx]:>25s}: "
          f"coef={final_model.coef_[0][idx]:+.4f}, "
          f"OR={np.exp(final_model.coef_[0][idx]):.4f}")

# ============================================================
# 5. 可视化 / Visualization
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# ROC 曲线 / ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
axes[0].plot(fpr, tpr, 'b-', label=f'AUC = {roc_auc:.4f}')
axes[0].plot([0, 1], [0, 1], 'r--')
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].set_title('ROC Curve')
axes[0].legend()

# PR 曲线 / Precision-Recall Curve
precision, recall, _ = precision_recall_curve(y_test, y_prob)
axes[1].plot(recall, precision, 'g-')
axes[1].set_xlabel('Recall')
axes[1].set_ylabel('Precision')
axes[1].set_title('Precision-Recall Curve')

# Top 10 特征系数 / Top 10 Feature Coefficients
axes[2].barh(range(10), coef_importance[top_features])
axes[2].set_yticks(range(10))
axes[2].set_yticklabels([feature_names[i] for i in top_features])
axes[2].set_xlabel('|Coefficient|')
axes[2].set_title('Feature Importance (|coef|)')

plt.tight_layout()
plt.show()
```

> 📖 Docs: [scikit-learn LogisticRegression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
> 📖 Docs: [scikit-learn classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)

---

### 示例 3: 多分类 + L1 正则化特征选择（Multinomial + Lasso）

```python
# ============================================================
# 多分类 LR + L1 特征选择 / Multinomial LR with L1 Feature Selection
# ============================================================
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# 加载 Iris 全部三类 / Load all 3 classes of Iris
X, y = load_iris(return_X_y=True)
feature_names = load_iris().feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Multinomial + L1 (需要 saga solver)
# Multinomial + L1 (requires saga solver)
model = LogisticRegression(
    multi_class='multinomial',  # 多分类用 softmax / use softmax for multiclass
    penalty='l1',               # L1 正则化 → 稀疏系数 / L1 → sparse coefficients
    solver='saga',              # 唯一支持 L1+multinomial 的 solver
    C=0.5,                      # 正则化强度 / regularization strength
    max_iter=5000,
    random_state=42,
)
model.fit(X_train, y_train)

print(f"测试准确率 / Test Accuracy: {model.score(X_test, y_test):.4f}")
print(f"\n系数矩阵 / Coefficient Matrix (K×p):")
print(f"Shape: {model.coef_.shape}")  # (3, 4) = 3 classes × 4 features

# 显示哪些特征被 L1 选中（非零系数）
# Show which features are selected by L1 (non-zero coefficients)
for k in range(model.coef_.shape[0]):
    selected = [f for f, c in zip(feature_names, model.coef_[k]) if abs(c) > 1e-6]
    print(f"  Class {k}: 选中特征 = {selected}")
    print(f"           系数 = {model.coef_[k]}")
```

> 📖 Docs: [scikit-learn LogisticRegression solver comparison](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

---

## API 速查

### 模型类

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `LogisticRegression()` | — | — | 主分类器 |
| ↳ `penalty` | `str` | `'l2'` | 正则化类型: `'l1'`, `'l2'`, `'elasticnet'`, `None` |
| ↳ `C` | `float` | `1.0` | 正则化强度的倒数，越大正则化越弱 |
| ↳ `solver` | `str` | `'lbfgs'` | 优化器: `'lbfgs'`, `'liblinear'`, `'newton-cg'`, `'newton-cholesky'`, `'sag'`, `'saga'` |
| ↳ `max_iter` | `int` | `100` | 最大迭代次数 |
| ↳ `multi_class` | `str` | `'auto'` | `'ovr'` (One-vs-Rest), `'multinomial'` |
| ↳ `class_weight` | `dict/'balanced'` | `None` | 类别权重，`'balanced'` 自动按频率倒数加权 |
| ↳ `l1_ratio` | `float` | `None` | ElasticNet 混合比例 (仅 `penalty='elasticnet'`) |
| ↳ `fit_intercept` | `bool` | `True` | 是否拟合截距 |
| ↳ `tol` | `float` | `1e-4` | 收敛容差 |
| `LogisticRegressionCV()` | — | — | 带交叉验证自动选 C |
| ↳ `Cs` | `int/list` | `10` | 待搜索的 C 值数量或列表 |
| ↳ `cv` | `int` | `5` | 交叉验证折数 |

### 方法

| 函数 | 参数 | 说明 |
|------|------|------|
| `.fit(X, y)` | 训练数据 | 训练模型 |
| `.predict(X)` | 测试数据 | 预测类别标签 |
| `.predict_proba(X)` | 测试数据 | 预测各类概率 |
| `.predict_log_proba(X)` | 测试数据 | 预测各类对数概率 |
| `.score(X, y)` | 测试数据+标签 | 返回准确率 |
| `.decision_function(X)` | 测试数据 | 返回决策值 (距超平面距离) |

### 属性

| 属性 | 说明 |
|------|------|
| `.coef_` | 系数矩阵 (n_classes × n_features)，二分类时 shape=(1, n_features) |
| `.intercept_` | 截距 |
| `.classes_` | 类别标签 |
| `.n_iter_` | 实际迭代次数 |
| `.n_features_in_` | 训练时特征数 |

### Solver 选择指南

| Solver | L1 | L2 | ElasticNet | multinomial | 大数据 | 稀疏 |
|--------|----|----|------------|-------------|--------|------|
| `lbfgs` | ❌ | ✅ | ❌ | ✅ | 中等 | ✅ |
| `liblinear` | ✅ | ✅ | ❌ | ❌(OvR only) | ❌ | ✅ |
| `newton-cg` | ❌ | ✅ | ❌ | ✅ | 中等 | ✅ |
| `newton-cholesky` | ❌ | ✅ | ❌ | ✅ | ❌(密集) | ❌ |
| `sag` | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ |
| `saga` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### 常用工具

| 函数 | 说明 |
|------|------|
| `sklearn.metrics.log_loss(y, p)` | 计算交叉熵损失 |
| `sklearn.metrics.roc_auc_score(y, p)` | 计算 AUC |
| `sklearn.metrics.classification_report(y, ŷ)` | 完整分类报告 |
| `sklearn.preprocessing.StandardScaler()` | 特征标准化（LR 前必做） |

> 📖 Docs: [scikit-learn LogisticRegression API](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
> 💻 Source: [scikit-learn _logistic.py](../../../.github/scikit-learn/sklearn/linear_model/_logistic.py)

---

## 目录结构模板

### 简单结构

```
project/
├── train.py              ← 训练 + 评估脚本
├── data/
│   ├── train.csv         ← 训练数据
│   └── test.csv          ← 测试数据
└── requirements.txt      ← scikit-learn, numpy, pandas
```

### 标准结构

```
project/
├── config.py             ← 超参配置 (C, penalty, solver...)
├── preprocess.py         ← 数据清洗 + 标准化
├── train.py              ← 训练 + 交叉验证
├── evaluate.py           ← 评估 + 可视化
├── predict.py            ← 部署推理
├── data/
│   ├── raw/              ← 原始数据
│   └── processed/        ← 预处理后数据
├── models/               ← 保存的模型 (joblib/pickle)
├── reports/              ← 评估报告 + 图表
└── requirements.txt
```

### 高级结构

```
project/
├── configs/              ← YAML 配置文件
├── src/
│   ├── data/             ← 数据加载 + 预处理
│   ├── features/         ← 特征工程
│   ├── models/           ← 模型定义
│   ├── training/         ← 训练流程
│   └── evaluation/       ← 评估 + 报告
├── notebooks/            ← 探索性分析
├── tests/                ← 单元测试
├── models/               ← 序列化模型
├── logs/                 ← 训练日志
└── requirements.txt
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4
