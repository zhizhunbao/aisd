---
topic: loss_functions
dimension: code
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📖 Docs: Keras Losses — https://keras.io/api/losses/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Loss Functions 代码参考

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)
> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
import numpy as np

# ============================================================
# 从零实现 4 种损失函数（不依赖框架）
# Implement 4 loss functions from scratch (no framework)
# ============================================================

# MSE: 回归任务的默认损失
# MSE: default loss for regression
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# MAE: 对异常值更鲁棒
# MAE: more robust to outliers
def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

# Binary Cross-Entropy: 二分类
# Binary CE: for binary classification
def binary_ce(y_true, y_pred):
    eps = 1e-15                                    # 防止 log(0)
    y_pred = np.clip(y_pred, eps, 1 - eps)         # 数值稳定
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# Categorical Cross-Entropy: 多分类
# Categorical CE: for multi-class classification
def categorical_ce(y_true_onehot, y_pred):
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1.0)
    return -np.mean(np.sum(y_true_onehot * np.log(y_pred), axis=1))

# 测试 / Test
print("=== 回归 ===")
y = np.array([3.0, 5.0, 7.0])
y_hat = np.array([2.5, 5.5, 6.0])
print(f"MSE: {mse(y, y_hat):.4f}")     # → 0.5000
print(f"MAE: {mae(y, y_hat):.4f}")     # → 0.6667

print("\n=== 二分类 ===")
y_bin = np.array([1, 0, 1, 1])
y_pred_bin = np.array([0.9, 0.1, 0.8, 0.7])
print(f"BCE: {binary_ce(y_bin, y_pred_bin):.4f}")

print("\n=== 多分类 ===")
y_onehot = np.array([[0,1,0], [1,0,0]])                  # 2 个样本, 3 个类
y_pred_multi = np.array([[0.1, 0.7, 0.2], [0.8, 0.1, 0.1]])
print(f"CCE: {categorical_ce(y_onehot, y_pred_multi):.4f}")
```

**测试方法：** 运行脚本。MSE 应为 0.5。BCE 和 CCE 值越小表示预测越准。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 完整实现示例

### 示例 1: Keras 分类任务 — loss 选择对比

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from tensorflow import keras
from tensorflow.keras import layers

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.reshape(-1, 784).astype('float32') / 255.0
X_test = X_test.reshape(-1, 784).astype('float32') / 255.0

# ============================================================
# 2. 对比不同 loss 函数 / Compare different losses
# ============================================================
def build_model(loss_name, output_activation, num_outputs):
    """构建模型，指定 loss 和输出层配置"""
    model = keras.Sequential([
        layers.Dense(128, activation='relu', input_shape=(784,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_outputs, activation=output_activation)
    ])
    model.compile(optimizer='adam', loss=loss_name, metrics=['accuracy'])
    return model

# --- 方式 1: Sparse Categorical CE (推荐，整数标签) ---
print("=== sparse_categorical_crossentropy ===")
model_sparse = build_model('sparse_categorical_crossentropy', 'softmax', 10)
model_sparse.fit(X_train, y_train, epochs=3, batch_size=128,
                 validation_split=0.1, verbose=0)
_, acc = model_sparse.evaluate(X_test, y_test, verbose=0)
print(f"  Test Accuracy: {acc:.4f}")

# --- 方式 2: Categorical CE (one-hot 标签) ---
print("\n=== categorical_crossentropy ===")
y_train_oh = keras.utils.to_categorical(y_train, 10)   # 转 one-hot
y_test_oh = keras.utils.to_categorical(y_test, 10)
model_cat = build_model('categorical_crossentropy', 'softmax', 10)
model_cat.fit(X_train, y_train_oh, epochs=3, batch_size=128,
              validation_split=0.1, verbose=0)
_, acc = model_cat.evaluate(X_test, y_test_oh, verbose=0)
print(f"  Test Accuracy: {acc:.4f}")

# --- 方式 3: MSE 做分类 (错误示范！) ---
print("\n=== mse (NOT recommended for classification) ===")
model_mse = build_model('mse', 'softmax', 10)
model_mse.fit(X_train, y_train_oh, epochs=3, batch_size=128,
              validation_split=0.1, verbose=0)
_, acc = model_mse.evaluate(X_test, y_test_oh, verbose=0)
print(f"  Test Accuracy: {acc:.4f}  ← 通常低于 CE")
```

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---

### 示例 2: Keras 回归任务 — MSE vs MAE vs Huber

```python
# ============================================================
# 回归损失函数对比 / Regression loss comparison
# ============================================================
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# 生成回归数据（含异常值）
np.random.seed(42)
X = np.random.randn(1000, 1).astype('float32')
y = 3 * X.squeeze() + 2 + np.random.randn(1000) * 0.5  # 正常数据
y[::50] += 20                                             # 每 50 个加一个异常值

losses = {
    'mse': 'mse',
    'mae': 'mae',
    'huber': keras.losses.Huber(delta=1.0),
}

for name, loss_fn in losses.items():
    model = keras.Sequential([
        layers.Dense(32, activation='relu', input_shape=(1,)),
        layers.Dense(1)                                    # 回归：无激活
    ])
    model.compile(optimizer='adam', loss=loss_fn)
    model.fit(X, y, epochs=20, verbose=0)

    # 预测测试点
    test_x = np.array([[0.0], [1.0]])
    preds = model.predict(test_x, verbose=0)
    print(f"Loss: {name:6s} | f(0)={preds[0][0]:.2f} (期望~2) | f(1)={preds[1][0]:.2f} (期望~5)")
```

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---

### 示例 3: scikit-learn 的隐式损失函数

```python
# ============================================================
# scikit-learn MLPClassifier 使用隐式的 log-loss
# scikit-learn uses log-loss (cross-entropy) implicitly
# ============================================================
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# MLPClassifier 内部自动使用 log-loss (= binary cross-entropy)
# 不需要手动指定 loss！
mlp = MLPClassifier(
    hidden_layer_sizes=(100, 50),
    activation='relu',
    solver='adam',
    max_iter=500,
    random_state=42
)
mlp.fit(X_train, y_train)

# loss_curve_ 记录了每个 epoch 的 loss 值
print(f"Final loss: {mlp.loss_curve_[-1]:.4f}")
print(f"Accuracy:   {mlp.score(X_test, y_test):.4f}")
print(f"Loss type:  log-loss (binary cross-entropy, 自动选择)")
```

> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

## API 速查

### Keras Losses

| 名称 | Keras 字符串 | 适用任务 | 配套激活 |
|------|-------------|---------|---------|
| MSE | `'mse'` 或 `'mean_squared_error'` | 回归 | Linear |
| MAE | `'mae'` 或 `'mean_absolute_error'` | 回归 | Linear |
| Huber | `keras.losses.Huber(delta=1.0)` | 回归（抗异常值）| Linear |
| BCE | `'binary_crossentropy'` | 二分类/多标签 | Sigmoid |
| CCE | `'categorical_crossentropy'` | 多分类(one-hot) | Softmax |
| Sparse CCE | `'sparse_categorical_crossentropy'` | **多分类(整数)** | Softmax |
| Hinge | `'hinge'` | SVM 分类 | Linear |

### Keras compile 用法

| 用法 | 说明 |
|------|------|
| `model.compile(loss='mse')` | 字符串形式（简洁） |
| `model.compile(loss=keras.losses.Huber(delta=1.0))` | 对象形式（可调参数） |
| `model.compile(loss={'out1': 'mse', 'out2': 'bce'})` | 多输出模型指定不同 loss |

### scikit-learn

| 方面 | 说明 |
|------|------|
| 分类 loss | `MLPClassifier` 自动使用 log-loss (= cross-entropy) |
| 回归 loss | `MLPRegressor` 自动使用 MSE |
| 查看 loss 曲线 | `mlp.loss_curve_`（训练后可访问） |
| **不能手动指定 loss** | sklearn MLP 没有 loss 参数 |

> 📖 Docs: [Keras Losses API](https://keras.io/api/losses/)
> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
