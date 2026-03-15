---
topic: tensorflow
dimension: pitfalls
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: TensorFlow Guide — https://www.tensorflow.org/guide"
  - "📖 Docs: tf.function caveats — https://www.tensorflow.org/guide/function#limitations"
  - "🧪 经验: TF 训练常见陷阱"
expiry: 6m
status: current
---

# TensorFlow 踩坑记录

> ⚠️ **每次踩坑后请追加条目。**

---

## 坑 1: @tf.function 中使用 Python 副作用

**场景：** 在 `@tf.function` 装饰的函数中使用 `print()`、`list.append()`、全局变量修改

**症状：** `print()` 只在第一次追踪时执行，后续调用不再打印；`list.append()` 只在追踪时添加一次

**根因：** `@tf.function` 首次调用时"追踪"Python 代码转为计算图。Python 副作用（print、list 操作）只在追踪阶段执行，之后图执行时这些 Python 代码不再运行。

**解法：**

❌ 错误写法

```python
@tf.function
def train_step(x, y):
    loss = compute_loss(x, y)
    print(f"loss = {loss}")       # 只在第一次追踪时执行！
    my_list.append(loss)           # 只追踪时添加一次！
    return loss
```

✅ 正确写法 — 用 tf.print 和 TF 操作

```python
@tf.function
def train_step(x, y):
    loss = compute_loss(x, y)
    tf.print("loss =", loss)       # 每次执行都打印 ✅
    return loss

# 收集数据在函数外部做
losses = []
for x, y in dataset:
    loss = train_step(x, y)
    losses.append(loss.numpy())    # 在 Python 层面收集
```

> 📖 Docs: [tf.function Limitations](https://www.tensorflow.org/guide/function#limitations)

---

## 坑 2: 忘记 from_logits=True 导致数值不稳定

**场景：** 模型最后一层输出 logits（无 softmax），但损失函数没设 `from_logits=True`

**症状：** 训练损失 NaN/Inf，或收敛极慢

**根因：** `CategoricalCrossentropy()` 默认 `from_logits=False`，期望输入是概率（经过 softmax）。如果你的模型输出 logits（未经 softmax），它会对 logits 取 log，得到错误结果。设 `from_logits=True` 会内部用 log-softmax 做数值稳定计算。

**解法：**

❌ 错误写法

```python
model.add(Dense(10))                                    # 输出 logits
model.compile(loss='sparse_categorical_crossentropy')    # 默认 from_logits=False → 错！
```

✅ 正确写法

```python
# 方案 1: 设 from_logits=True（推荐，数值更稳定）
model.add(Dense(10))     # logits
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))

# 方案 2: 模型加 softmax（不推荐，数值精度差）
model.add(Dense(10, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy')
```

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---

## 坑 3: BatchNorm 在推理时行为异常

**场景：** 训练时效果好，推理/部署时准确率骤降

**症状：** `model.predict()` 结果与 `model(x, training=True)` 差异巨大

**根因：** `BatchNormalization` 训练时用 mini-batch 均值/方差，推理时用移动平均。如果 (1) 训练 epochs 太少导致移动平均不准确，或 (2) 自定义循环中忘记设 `training=True/False`，会导致不一致。

**解法：**

❌ 错误写法 — 推理时忘记设 training=False

```python
# 自定义训练循环中
y_pred = model(x_batch)               # 默认 training=False，但 BN 统计量未更新完
```

✅ 正确写法

```python
# 训练时
y_pred = model(x_batch, training=True)     # BN 用 batch 统计量 + 更新移动平均

# 推理时
y_pred = model(x_batch, training=False)    # BN 用移动平均

# 或用 model.fit() — 自动处理 training 标志
```

> 📖 Docs: [BatchNormalization](https://www.tensorflow.org/api_docs/python/tf/keras/layers/BatchNormalization)

---

## 坑 4: GradientTape 默认只能用一次

**场景：** 需要计算两次梯度（如 GAN 的 D 和 G），但第二次 `tape.gradient()` 返回 None

**症状：** 第二次调用 `tape.gradient()` 返回全部 None

**根因：** `GradientTape` 为了节省内存，默认在第一次 `gradient()` 后释放资源。

**解法：**

❌ 错误写法

```python
with tf.GradientTape() as tape:
    loss_d = discriminator_loss(...)
    loss_g = generator_loss(...)
grads_d = tape.gradient(loss_d, d_vars)    # ✅ 第一次 OK
grads_g = tape.gradient(loss_g, g_vars)    # ❌ 返回 None！
```

✅ 正确写法 — persistent=True

```python
with tf.GradientTape(persistent=True) as tape:
    loss_d = discriminator_loss(...)
    loss_g = generator_loss(...)
grads_d = tape.gradient(loss_d, d_vars)    # ✅
grads_g = tape.gradient(loss_g, g_vars)    # ✅
del tape                                     # 手动释放

# 或分开两个 tape（更清晰）
with tf.GradientTape() as tape_d:
    loss_d = ...
with tf.GradientTape() as tape_g:
    loss_g = ...
```

> 📖 Docs: [GradientTape](https://www.tensorflow.org/api_docs/python/tf/GradientTape)

---

## 坑 5: tf.data 忘记 prefetch 导致 GPU 空闲

**场景：** 数据预处理在 CPU 上，GPU 等 CPU 处理完才开始下一批

**症状：** GPU 利用率很低（<50%），训练比预期慢很多

**根因：** 没有 `prefetch`，CPU 和 GPU 是串行工作——CPU 处理一批 → GPU 训练一批 → CPU 处理下一批...

**解法：**

❌ 错误写法

```python
dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(10000).batch(64)
# 没有 prefetch → CPU/GPU 串行
```

✅ 正确写法

```python
dataset = dataset.shuffle(10000).batch(64).prefetch(tf.data.AUTOTUNE)
# prefetch 让 CPU 在 GPU 训练时提前准备下一批
```

> 📖 Docs: [tf.data Performance](https://www.tensorflow.org/guide/data_performance)

---

## 坑 6: 模型保存后加载失败（自定义层/损失）

**场景：** 模型有自定义 Layer 或 loss function，save 后 `load_model` 报错

**症状：** `ValueError: Unknown layer: CustomLayer` 或 `Unknown loss function`

**根因：** Keras 的序列化只保存层的名字和配置，不保存 Python 类定义。加载时需要注册自定义对象。

**解法：**

✅ 正确写法

```python
# 方案 1: 注册自定义对象
@tf.keras.utils.register_keras_serializable()
class CustomLayer(tf.keras.layers.Layer):
    ...

# 方案 2: 加载时传 custom_objects
model = tf.keras.models.load_model(
    'my_model', custom_objects={'CustomLayer': CustomLayer}
)

# 方案 3: 只保存权重（避免序列化问题）
model.save_weights('weights.h5')
new_model = build_model()
new_model.load_weights('weights.h5')
```

> 📖 Docs: [Model Serialization](https://keras.io/guides/serialization_and_saving/)

---

## 调试清单

1. [ ] **训练 loss=NaN？** → 检查 `from_logits=True`；检查学习率是否太大
2. [ ] **@tf.function 里 print 不执行？** → 用 `tf.print()`
3. [ ] **推理精度差（训练好）？** → BN 的 `training=True/False` 是否正确
4. [ ] **tape.gradient() 返回 None？** → 设 `persistent=True`；或变量未被 tape 监控
5. [ ] **GPU 利用率低？** → `dataset.prefetch(AUTOTUNE)`
6. [ ] **load_model 报错？** → 注册 `@register_keras_serializable` 或传 `custom_objects`
7. [ ] **内存不够 (OOM)？** → 减小 `batch_size`；用 `tf.data` 而非全加载
8. [ ] **@tf.function 重新追踪 (retracing)？** → 输入 shape/dtype 变化触发；用 `input_signature` 固定
9. [ ] **TF 1.x 代码不兼容？** → 运行 `tf_upgrade_v2` 工具
10. [ ] **多 GPU 训练不加速？** → 检查 `MirroredStrategy`；batch_size 需 × GPU 数
