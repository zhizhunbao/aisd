---
topic: optimizers
dimension: pitfalls
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: Keras Optimizers — https://keras.io/api/optimizers/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
  - "🧪 经验: 优化器相关的常见训练问题"
expiry: 6m
status: current
---

# Optimizers 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 学习率过大——Loss 震荡或 NaN

**场景：** 使用 Adam 但设置 `learning_rate=0.1`，或 SGD 设置 `learning_rate=1.0`

**症状：** Loss 不下降反而上升，或直接变成 `NaN`。训练曲线剧烈震荡

**根因：** 学习率过大导致每步更新幅度过大，权重"跳过"最优点，在最优点两侧来回震荡甚至发散

**解法：**

❌ 错误写法 — 学习率过大

```python
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.1))  # ← 太大
```

✅ 正确写法 — 使用合理默认值

```python
# Adam 的默认 lr=0.001 通常就是最佳起点
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001))

# 或者更保守地从小开始
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001))
```

**教训：** Adam 用 0.001，SGD 用 0.01 作为起点。出现 NaN 时首先将学习率减小 10 倍。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 坑 2: 学习率过小——训练极慢，看似不收敛

**场景：** 为求"安全"设置 `learning_rate=0.0000001`

**症状：** Loss 在数十个 epoch 后几乎没有变化，看起来模型没有学到任何东西

**根因：** 学习率太小，每步更新量微乎其微，需要海量 epoch 才能看到进展

**解法：**

❌ 错误写法 — 学习率过小

```python
model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-7))  # ← 太小
```

✅ 正确写法 — 使用学习率搜索

```python
# 方法 1: 用合理默认值
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001))

# 方法 2: 学习率范围搜索
for lr in [0.0001, 0.0005, 0.001, 0.005, 0.01]:
    # 各训练几个 epoch，选 loss 下降最快的
    pass
```

**教训：** 学习率是最有影响的超参数。太大→震荡，太小→不动。先用默认值，再做简单搜索。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 坑 3: sklearn 中 solver='lbfgs' 对大数据集崩溃

**场景：** 数据集有 10 万+ 样本，使用 `MLPClassifier(solver='lbfgs')`

**症状：** 内存暴涨 (`MemoryError`) 或训练时间极长（卡住不动）

**根因：** L-BFGS 是批量方法，每次用全部数据计算梯度 + 近似 Hessian，O(n) 内存和计算时间

**解法：**

❌ 错误写法 — 大数据用 L-BFGS

```python
mlp = MLPClassifier(solver='lbfgs')  # ← 大数据会崩
mlp.fit(X_train_100k, y_train_100k)
```

✅ 正确写法 — 大数据用 Adam

```python
# Adam 使用 mini-batch，内存和计算与数据量无关
mlp = MLPClassifier(solver='adam', batch_size=256)
mlp.fit(X_train_100k, y_train_100k)
```

**教训：** L-BFGS 只适合小数据集（<1 万样本，<1 万参数）。大数据永远用 Adam 或 SGD。

> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

## 坑 4: SGD 不收敛——忘了加 Momentum

**场景：** 使用 `keras.optimizers.SGD()` 不加任何参数

**症状：** 训练非常慢，loss 震荡，最终精度远低于 Adam

**根因：** Vanilla SGD（无动量）在"窄长谷"损失地表上疯狂震荡。momentum=0 是默认值

**解法：**

❌ 错误写法 — 裸 SGD

```python
model.compile(optimizer=keras.optimizers.SGD())  # ← momentum=0, 震荡
```

✅ 正确写法 — SGD + Momentum + 较大 lr

```python
model.compile(optimizer=keras.optimizers.SGD(
    learning_rate=0.01,
    momentum=0.9,        # ← 加动量
    nesterov=True         # ← Nesterov 更好
))
```

**教训：** 如果非要用 SGD，至少要加 `momentum=0.9`。否则用 Adam。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 坑 5: 混淆 sklearn solver 名和 Keras optimizer 名

**场景：** 在 sklearn 中写 `solver='Adam'`（大写），或在 Keras 中写 `optimizer='lbfgs'`

**症状：** `ValueError`

**根因：** sklearn 用小写 `'adam'`/`'sgd'`/`'lbfgs'`；Keras 用字符串 `'adam'`/`'sgd'`/`'rmsprop'` 或类对象。L-BFGS 在 Keras 中没有

**解法：**

❌ 错误写法

```python
# sklearn: 大写会报错
MLPClassifier(solver='Adam')             # ← ValueError

# Keras: L-BFGS 不存在
model.compile(optimizer='lbfgs')         # ← 不支持
```

✅ 正确写法

```python
# sklearn: 全小写
MLPClassifier(solver='adam')

# Keras: 字符串或对象
model.compile(optimizer='adam')
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001))
```

**教训：** sklearn solver: `'adam'`, `'sgd'`, `'lbfgs'`。Keras optimizer: `'adam'`, `'sgd'`, `'rmsprop'`, `'adagrad'`。大小写均区分。

> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---

## 坑 6: batch_size 设太大——泛化变差

**场景：** 使用 `batch_size=10000` 或 `batch_size=len(X_train)` 做全批量训练

**症状：** 训练 loss 下降很快，但测试 accuracy 反而比小 batch 差

**根因：** 大 batch 梯度估计太"准确"，缺少噪声，容易收敛到"尖锐"的极小值（泛化差）。小 batch 的噪声反而帮助跳出尖锐极小值，找到"平坦"极小值（泛化好）

**解法：**

❌ 错误写法 — 过大 batch

```python
model.fit(X_train, y_train, batch_size=len(X_train))  # ← 全批量
```

✅ 正确写法 — 使用常见 batch size

```python
# 常用 batch size: 32, 64, 128, 256
model.fit(X_train, y_train, batch_size=128)
```

**教训：** batch_size 32-256 是安全范围。越大训练越快但泛化可能变差。大 batch 需要线性增大学习率。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 调试清单

1. [ ] **Loss 变成 NaN？** → 学习率太大，减小 10 倍
2. [ ] **Loss 不下降？** → 学习率太小，增大 10 倍；或换用 Adam
3. [ ] **训练快但测试差？** → batch_size 太大，减小到 64-128
4. [ ] **SGD 震荡不收敛？** → 加 `momentum=0.9`
5. [ ] **内存不足？** → 减小 batch_size；不要用 L-BFGS
6. [ ] **sklearn solver 报错？** → 检查拼写（全小写）：`'adam'`, `'sgd'`, `'lbfgs'`
7. [ ] **不知道用哪个 optimizer？** → 先用 Adam (lr=0.001)，不行再试 SGD+Momentum
8. [ ] **训练后期 loss 不再下降？** → 使用学习率衰减调度（如 ReduceLROnPlateau）
9. [ ] **收敛到次优解？** → 尝试 warm restart 或 cosine annealing 学习率调度
10. [ ] **Adam 泛化不如 SGD？** → 对于 CV 任务，试 SGD+Momentum+CosineAnnealing
