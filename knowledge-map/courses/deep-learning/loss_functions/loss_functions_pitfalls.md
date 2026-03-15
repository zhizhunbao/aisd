---
topic: loss_functions
dimension: pitfalls
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: Keras Losses — https://keras.io/api/losses/"
  - "🧪 经验: 损失函数相关的常见训练问题"
expiry: 6m
status: current
---

# Loss Functions 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 分类任务用了 MSE 损失——Sigmoid 饱和梯度消失

**场景：** 二分类任务，Sigmoid 输出层 + `loss='mse'`

**症状：** 训练极慢，loss 下降缓慢，accuracy 远低于用 cross-entropy 时

**根因：** MSE 的梯度经过 Sigmoid 后包含 $\sigma'(z) = \hat{y}(1-\hat{y})$ 项。当预测自信（$\hat{y}\approx0$ 或 $\hat{y}\approx1$）时梯度 ≈ 0——模型明明"自信地"犯错却无法纠正

**解法：**

❌ 错误写法

```python
model.compile(loss='mse', optimizer='adam')  # ← 分类不要用 MSE！
```

✅ 正确写法

```python
# 二分类: Sigmoid + BCE
model.compile(loss='binary_crossentropy', optimizer='adam')

# 多分类: Softmax + Sparse CCE
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
```

**教训：** 分类任务**永远**用交叉熵。MSE 只用于回归。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2

---

## 坑 2: Categorical CE 用了整数标签——loss 异常高

**场景：** 标签是整数（如 `[0, 3, 2, 1]`），但 loss 设为 `'categorical_crossentropy'`

**症状：** 训练看起来正常，但 loss 值不合理地高或准确率很低

**根因：** Categorical CE 期望 one-hot 标签。整数标签 `3` 会被误当作一个浮点数而不是类别索引，计算出错误的 loss

**解法：**

❌ 错误写法 — 整数标签 + categorical CE

```python
model.compile(loss='categorical_crossentropy')
model.fit(X_train, y_train_integers)  # ← y=[0,3,2,1] → 错误！
```

✅ 正确写法 — 两种方案

```python
# 方案 1（推荐）: 整数标签 + sparse_categorical_crossentropy
model.compile(loss='sparse_categorical_crossentropy')
model.fit(X_train, y_train_integers)  # ← y=[0,3,2,1] ✅

# 方案 2: 转 one-hot + categorical_crossentropy
y_onehot = keras.utils.to_categorical(y_train_integers, num_classes=10)
model.compile(loss='categorical_crossentropy')
model.fit(X_train, y_onehot)           # ← y=[[1,0,0,...], ...] ✅
```

**教训：** 标签是整数→用 `sparse_categorical_crossentropy`；标签是 one-hot→用 `categorical_crossentropy`。

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---

## 坑 3: 输出层激活和 loss 不匹配——梯度异常

**场景：** 多分类用了 Sigmoid 而不是 Softmax，或回归用了 Softmax

**症状：** 模型可能"训练"但结果荒谬。多分类的概率和不为 1

**根因：** 激活函数和损失函数是配对设计的：Sigmoid+BCE 的梯度 = $\hat{y}-y$；Softmax+CCE 的梯度 = $\hat{y}-y$。配对错误时梯度公式不成立

**解法：**

❌ 错误写法 — 配对错误

```python
# 多分类用 Sigmoid → 概率和 ≠ 1
model.add(layers.Dense(10, activation='sigmoid'))
model.compile(loss='categorical_crossentropy')   # ← 配对错误

# 回归用 Softmax → 输出被压缩到 (0,1)
model.add(layers.Dense(1, activation='softmax'))
model.compile(loss='mse')                         # ← 配对错误
```

✅ 正确配对

```python
# 配对表：
# 二分类:  Dense(1, activation='sigmoid')  + loss='binary_crossentropy'
# 多分类:  Dense(K, activation='softmax')  + loss='sparse_categorical_crossentropy'
# 回归:    Dense(1)                        + loss='mse'
```

**教训：** 永远遵循配对表：Sigmoid+BCE, Softmax+CCE, Linear+MSE。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2

---

## 坑 4: Loss 变成 NaN——log(0) 数值爆炸

**场景：** 模型预测值出现 0 或 1，交叉熵中 $\log(0)$ 导致 NaN

**症状：** 训练几个 epoch 后 loss 突然变成 `nan`

**根因：** $\log(0) = -\infty$。当模型极端自信时（某类 Softmax 输出 = 0），交叉熵中的 $-\log(\hat{y}_k)$ 爆炸

**解法：**

```python
# Keras 内部已经处理了 clip，但自己实现时要注意：

# ❌ 不安全
loss = -np.log(y_pred)                     # ← y_pred=0 时爆炸

# ✅ 安全
loss = -np.log(np.clip(y_pred, 1e-7, 1))   # ← clip 到极小正数

# Keras 中用 from_logits=True 更安全：
model.compile(loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True))
# 此时输出层不要加 softmax！让 Keras 在 loss 内部做 log-softmax（数值更稳定）
```

**教训：** 尽可能使用 `from_logits=True`——让框架在 loss 内部处理 softmax，数值稳定性更好。

> 📖 Docs: [Keras SparseCategoricalCrossentropy](https://keras.io/api/losses/probabilistic_losses/#sparsecategoricalcrossentropy-class)

---

## 坑 5: sklearn 中想指定自定义 loss——不支持

**场景：** 在 `MLPClassifier` 中想换 loss 函数

**症状：** 找不到 `loss` 参数

**根因：** scikit-learn 的 MLP 不暴露 loss 参数。`MLPClassifier` 固定使用 log-loss（交叉熵）；`MLPRegressor` 固定使用 MSE

**解法：**

```python
# sklearn MLP 没有 loss 参数，这些是固定的：
# MLPClassifier → log-loss (cross-entropy)
# MLPRegressor  → squared-error (MSE)

# 如果需要自定义 loss → 使用 Keras
model.compile(loss=keras.losses.Huber(delta=1.0))
```

**教训：** 需要灵活的 loss → 用 Keras/PyTorch。sklearn MLP 只适合快速原型验证。

> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

## 坑 6: 多标签分类用了 Softmax + CCE

**场景：** 一张图可以同时属于多个类别（如"猫"和"室内"），用了 Softmax 输出

**症状：** 每张图只能预测一个类别，其他类别被压到接近 0

**根因：** Softmax 强制所有概率和为 1（互斥竞争）。多标签分类中各标签是独立的，需要每个标签独立的 Sigmoid

**解法：**

❌ 错误写法

```python
# 多标签用 Softmax → 强制互斥
model.add(layers.Dense(num_labels, activation='softmax'))
model.compile(loss='categorical_crossentropy')
```

✅ 正确写法

```python
# 多标签：每个标签独立的 Sigmoid
model.add(layers.Dense(num_labels, activation='sigmoid'))
model.compile(loss='binary_crossentropy')  # ← 每个标签独立的 BCE
```

**教训：** 多分类（互斥）= Softmax + CCE；多标签（可共存）= Sigmoid + BCE。

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---

## 调试清单

1. [ ] **分类 loss 下降慢？** → 检查是否用了 MSE（应该用交叉熵）
2. [ ] **loss 值异常高？** → 检查标签格式是否与 loss 匹配（整数 vs one-hot）
3. [ ] **loss 变 NaN？** → 使用 `from_logits=True` 让框架内部处理数值稳定
4. [ ] **预测概率和 ≠ 1？** → 检查多分类是否用了 Sigmoid（应该用 Softmax）
5. [ ] **多标签分类效果差？** → 检查是否用了 Softmax（应该用多个 Sigmoid + BCE）
6. [ ] **输出层激活对了吗？** → Sigmoid+BCE, Softmax+CCE, Linear+MSE
7. [ ] **回归受异常值干扰？** → 换 Huber Loss 或 MAE
8. [ ] **sklearn 想自定义 loss？** → 不支持，换 Keras
9. [ ] **training loss 降但 val loss 升？** → 过拟合，不是 loss 的问题，加正则化
10. [ ] **loss 不下降且很大？** → 检查学习率是否合理（见 optimizers_pitfalls）
