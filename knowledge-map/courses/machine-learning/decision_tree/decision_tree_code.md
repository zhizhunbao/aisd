---
topic: decision_tree
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: scikit-learn DecisionTree — https://scikit-learn.org/stable/modules/tree.html"
  - "💻 Source: scikit-learn tree/_classes.py — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn/tree/_classes.py"
  - "📚 Book: Hastie et al., ESL Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
expiry: 6m
status: current
---

# Decision Tree 代码参考

> 📖 Docs: [scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html)
> 💻 Source: [scikit-learn tree/_classes.py](../../../.github/scikit-learn/sklearn/tree/_classes.py)


## 快速开始

### 最简示例 — 30 秒上手

```python
# === Decision Tree 最简示例 ===
# === Decision Tree Minimal Example ===

from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# 加载数据 / Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 一行训练 / One-liner training
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# 评估 / Evaluate
print(f"准确率 / Accuracy: {model.score(X_test, y_test):.4f}")

# 打印树规则 / Print tree rules
print(export_text(model, feature_names=load_iris().feature_names))
```

**测试方法：** 运行后应输出 Accuracy ≈ 0.96 + 可读的 if-else 规则

> 📖 Docs: [scikit-learn DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)

---

## 完整实现示例

### 示例 1: 从零实现 Decision Tree（纯 NumPy, CART 算法）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=200, n_features=4, n_informative=3,
    n_redundant=0, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
class Node:
    """树节点 / Tree node"""
    def __init__(self, feature=None, threshold=None, left=None,
                 right=None, value=None):
        self.feature = feature      # 分割特征索引 / split feature index
        self.threshold = threshold  # 分割阈值 / split threshold
        self.left = left            # 左子节点 / left child
        self.right = right          # 右子节点 / right child
        self.value = value          # 叶子预测值 / leaf prediction (None if internal)

class DecisionTreeScratch:
    """从零实现的 CART 分类器 / CART classifier from scratch"""

    def __init__(self, max_depth=10, min_samples_split=2, criterion='gini'):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.criterion = criterion
        self.root = None

    def _gini(self, y):
        """Gini 不纯度 / Gini impurity"""
        if len(y) == 0:
            return 0
        proportions = np.bincount(y) / len(y)
        return 1 - np.sum(proportions ** 2)

    def _entropy(self, y):
        """信息熵 / Information entropy"""
        if len(y) == 0:
            return 0
        proportions = np.bincount(y) / len(y)
        proportions = proportions[proportions > 0]  # 避免 log(0) / avoid log(0)
        return -np.sum(proportions * np.log2(proportions))

    def _impurity(self, y):
        """选择不纯度函数 / Select impurity function"""
        if self.criterion == 'gini':
            return self._gini(y)
        return self._entropy(y)

    def _best_split(self, X, y):
        """找到最优分割 / Find best split (greedy)"""
        best_gain = -1
        best_feature, best_threshold = None, None
        n_samples, n_features = X.shape
        parent_impurity = self._impurity(y)

        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask

                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                # 加权不纯度 / Weighted impurity
                n_l, n_r = np.sum(left_mask), np.sum(right_mask)
                child_impurity = (
                    (n_l / n_samples) * self._impurity(y[left_mask]) +
                    (n_r / n_samples) * self._impurity(y[right_mask])
                )
                gain = parent_impurity - child_impurity

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain

    def _build_tree(self, X, y, depth=0):
        """递归构建树 / Recursively build tree"""
        n_samples = len(y)
        n_classes = len(np.unique(y))

        # 停止条件 / Stopping conditions
        if (depth >= self.max_depth or
            n_classes == 1 or
            n_samples < self.min_samples_split):
            return Node(value=np.argmax(np.bincount(y)))

        # 找最优分割 / Find best split
        feature, threshold, gain = self._best_split(X, y)

        if gain <= 0:
            return Node(value=np.argmax(np.bincount(y)))

        # 递归建左右子树 / Recursively build subtrees
        left_mask = X[:, feature] <= threshold
        left = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right = self._build_tree(X[~left_mask], y[~left_mask], depth + 1)

        return Node(feature=feature, threshold=threshold,
                    left=left, right=right)

    def fit(self, X, y):
        """训练 / Train"""
        self.root = self._build_tree(X, y)
        return self

    def _predict_single(self, x, node):
        """单样本预测 / Predict single sample"""
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_single(x, node.left)
        return self._predict_single(x, node.right)

    def predict(self, X):
        """批量预测 / Batch predict"""
        return np.array([self._predict_single(x, self.root) for x in X])

    def score(self, X, y):
        """准确率 / Accuracy"""
        return np.mean(self.predict(X) == y)

# ============================================================
# 3. 训练与评估 / Training & Evaluation
# ============================================================
tree = DecisionTreeScratch(max_depth=5, criterion='gini')
tree.fit(X_train, y_train)

print(f"训练准确率 / Train Acc: {tree.score(X_train, y_train):.4f}")
print(f"测试准确率 / Test Acc:  {tree.score(X_test, y_test):.4f}")
```

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9.2

---

### 示例 2: scikit-learn 完整工程实践（分类 + 可视化 + 剪枝）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import (
    DecisionTreeClassifier, plot_tree, export_text
)
from sklearn.metrics import classification_report, confusion_matrix

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# 2. 不剪枝 vs 剪枝对比 / Unpruned vs Pruned Comparison
# ============================================================
# 不剪枝（过拟合）/ Unpruned (overfitting)
tree_full = DecisionTreeClassifier(random_state=42)
tree_full.fit(X_train, y_train)
print(f"不剪枝 - 训练: {tree_full.score(X_train, y_train):.4f}")
print(f"不剪枝 - 测试: {tree_full.score(X_test, y_test):.4f}")
print(f"不剪枝 - 叶子数: {tree_full.get_n_leaves()}")
print(f"不剪枝 - 深度: {tree_full.get_depth()}")

# 预剪枝 / Pre-pruning
tree_pruned = DecisionTreeClassifier(
    max_depth=4, min_samples_leaf=5, random_state=42
)
tree_pruned.fit(X_train, y_train)
print(f"\n预剪枝 - 训练: {tree_pruned.score(X_train, y_train):.4f}")
print(f"预剪枝 - 测试: {tree_pruned.score(X_test, y_test):.4f}")
print(f"预剪枝 - 叶子数: {tree_pruned.get_n_leaves()}")

# ============================================================
# 3. 代价复杂度剪枝 (CCP) / Cost-Complexity Pruning
# ============================================================
# 获取 alpha 路径 / Get alpha path
path = tree_full.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas
impurities = path.impurities

# 对每个 alpha 训练一棵树 / Train a tree for each alpha
trees = []
for alpha in ccp_alphas:
    t = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42)
    t.fit(X_train, y_train)
    trees.append(t)

# 绘制 alpha vs 准确率 / Plot alpha vs accuracy
train_scores = [t.score(X_train, y_train) for t in trees]
test_scores = [t.score(X_test, y_test) for t in trees]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(ccp_alphas, train_scores, 'b-o', label='Train', markersize=2)
axes[0].plot(ccp_alphas, test_scores, 'r-o', label='Test', markersize=2)
axes[0].set_xlabel('ccp_alpha')
axes[0].set_ylabel('Accuracy')
axes[0].set_title('CCP: Accuracy vs Alpha')
axes[0].legend()

# 叶子数 vs alpha / Leaves vs alpha
n_leaves = [t.get_n_leaves() for t in trees]
axes[1].plot(ccp_alphas, n_leaves, 'g-o', markersize=2)
axes[1].set_xlabel('ccp_alpha')
axes[1].set_ylabel('Number of Leaves')
axes[1].set_title('CCP: Tree Complexity vs Alpha')

plt.tight_layout()
plt.show()

# ============================================================
# 4. 最优树可视化 / Visualize Best Tree
# ============================================================
# 选最佳 alpha (测试准确率最高)
best_idx = np.argmax(test_scores)
best_tree = trees[best_idx]
print(f"\n最佳 alpha: {ccp_alphas[best_idx]:.4f}")
print(f"最佳树准确率: {best_tree.score(X_test, y_test):.4f}")
print(f"叶子数: {best_tree.get_n_leaves()}, 深度: {best_tree.get_depth()}")

fig, ax = plt.subplots(figsize=(20, 10))
plot_tree(best_tree, feature_names=data.feature_names,
          class_names=data.target_names, filled=True,
          rounded=True, fontsize=8, ax=ax)
plt.title(f"Best Pruned Tree (alpha={ccp_alphas[best_idx]:.4f})")
plt.show()

# ============================================================
# 5. 特征重要性 / Feature Importance
# ============================================================
importances = best_tree.feature_importances_
indices = np.argsort(importances)[::-1][:10]

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(range(10), importances[indices])
ax.set_yticks(range(10))
ax.set_yticklabels([data.feature_names[i] for i in indices])
ax.set_xlabel('Feature Importance (MDI)')
ax.set_title('Top 10 Features')
plt.tight_layout()
plt.show()
```

> 📖 Docs: [scikit-learn CCP Pruning](https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html)

---

### 示例 3: 回归树（Regression Tree）

```python
# ============================================================
# 回归树示例 / Regression Tree Example
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor

# 生成非线性数据 / Generate nonlinear data
np.random.seed(42)
X = np.sort(5 * np.random.rand(200, 1), axis=0)
y = np.sin(X).ravel() + np.random.normal(0, 0.1, X.shape[0])

# 不同深度的树 / Trees with different depths
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for i, depth in enumerate([2, 5, 20]):
    model = DecisionTreeRegressor(max_depth=depth, random_state=42)
    model.fit(X, y)

    X_test = np.arange(0, 5, 0.01)[:, np.newaxis]
    y_pred = model.predict(X_test)

    axes[i].scatter(X, y, s=10, alpha=0.5, label='Data')
    axes[i].plot(X_test, y_pred, 'r-', linewidth=2, label=f'depth={depth}')
    axes[i].set_title(f'Depth={depth}, R²={model.score(X, y):.4f}')
    axes[i].legend()

plt.suptitle('Regression Tree: Effect of max_depth')
plt.tight_layout()
plt.show()
```

> 📖 Docs: [scikit-learn DecisionTreeRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html)

---

## API 速查

### 分类器

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `criterion` | str | `'gini'` | `'gini'`, `'entropy'`, `'log_loss'` |
| `max_depth` | int | `None` | 最大深度 (None=不限) |
| `min_samples_split` | int/float | `2` | 分割所需最小样本数 |
| `min_samples_leaf` | int/float | `1` | 叶子最小样本数 |
| `max_features` | int/float/str | `None` | 每次分割考虑的最大特征数 |
| `max_leaf_nodes` | int | `None` | 最大叶子节点数 |
| `ccp_alpha` | float | `0.0` | 代价复杂度剪枝参数 |
| `class_weight` | dict/`'balanced'` | `None` | 类别权重 |
| `random_state` | int | `None` | 随机种子 |

### 回归器

| 参数差异 | 说明 |
|---------|------|
| `criterion` | `'squared_error'`(默认), `'absolute_error'`, `'friedman_mse'`, `'poisson'` |

### 方法

| 方法 | 说明 |
|------|------|
| `.fit(X, y)` | 训练 |
| `.predict(X)` | 预测类别/值 |
| `.predict_proba(X)` | 预测概率（分类） |
| `.score(X, y)` | 准确率/R² |
| `.apply(X)` | 返回叶子节点索引 |
| `.decision_path(X)` | 返回从根到叶子的路径 |
| `.get_depth()` | 树的最大深度 |
| `.get_n_leaves()` | 叶子节点数 |
| `.cost_complexity_pruning_path(X, y)` | CCP alpha 路径 |

### 属性

| 属性 | 说明 |
|------|------|
| `.feature_importances_` | 特征重要性 (MDI) |
| `.tree_` | 底层树结构对象 |
| `.classes_` | 类别标签 |
| `.n_features_in_` | 训练特征数 |

### 可视化工具

| 函数 | 说明 |
|------|------|
| `sklearn.tree.plot_tree(model)` | matplotlib 可视化树 |
| `sklearn.tree.export_text(model)` | 文本形式打印规则 |
| `sklearn.tree.export_graphviz(model)` | 导出 DOT 格式（Graphviz） |

> 📖 Docs: [scikit-learn DecisionTreeClassifier API](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
> 💻 Source: [tree/_classes.py](../../../.github/scikit-learn/sklearn/tree/_classes.py)
