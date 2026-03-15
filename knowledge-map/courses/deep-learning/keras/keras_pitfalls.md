---
topic: keras
dimension: pitfalls
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: Keras 3 Official Documentation — https://keras.io/api/"
  - "📖 Docs: Keras 3 Migration Guide — https://keras.io/guides/migrating_to_keras_3/"
  - "💻 Source: keras/keras GitHub Issues — https://github.com/keras-team/keras/issues"
  - "🧪 经验: Keras 3 多后端迁移和日常使用中踩坑"
expiry: 3m
status: current
---

# Keras 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 后端未正确设置导致 import 失败

**场景：** 安装了 `keras` 但没有安装对应后端包，或环境变量未设置

**症状：** `ImportError: Unable to import backend 'jax'` 或模型在错误的后端上运行

**根因：** Keras 3 在 `import keras` 时会读取 `KERAS_BACKEND` 环境变量（默认 `tensorflow`），如果对应后端包未安装则报错

**解法：**

❌ 错误写法 — 没有设置后端就直接导入

```python
import keras  # 默认 tensorflow，但可能没装 tf
```

✅ 正确写法 — 在导入前设置环境变量

```python
import os
os.environ["KERAS_BACKEND"] = "jax"  # 在 import keras 之前设置
import keras
```

✅ 备选方案 — 使用 `~/.keras/keras.json` 配置

```json
{
    "backend": "jax"
}
```

**教训：** 始终在脚本最开头、`import keras` 之前设置 `KERAS_BACKEND`

> 📖 Docs: [Keras 3 — Installation](https://keras.io/getting_started/)

---

## 坑 2: compile() 后修改 layer.trainable 不生效

**场景：** 迁移学习中先 `compile()` 然后冻结/解冻层，期望 `fit()` 时生效

**症状：** 冻结的层仍然被更新，或解冻后的层没有被训练

**根因：** Keras 在 `compile()` 时确定可训练变量列表。之后修改 `layer.trainable` 不会自动刷新这个列表

**解法：**

❌ 错误写法 — compile 后才修改 trainable

```python
model.compile(optimizer="adam", loss="mse")
model.layers[0].trainable = False  # ❌ compile 后修改不生效
model.fit(x, y, epochs=5)
```

✅ 正确写法 — 修改 trainable 后重新 compile

```python
model.layers[0].trainable = False  # 先修改
model.compile(optimizer="adam", loss="mse")  # 再 compile
model.fit(x, y, epochs=5)
```

**教训：** 修改 `trainable` 属性后必须重新 `compile()`

> 💻 Source: [keras](../../.github/keras/) `keras/src/trainers/trainer.py:142-163`
> 📖 Docs: [Keras 3 — Transfer Learning Guide](https://keras.io/guides/transfer_learning/)

---

## 坑 3: 在 keras.ops 和后端原生操作之间混用

**场景：** 自定义层的 `call()` 中同时使用 `keras.ops.relu()` 和 `torch.nn.functional.relu()`

**症状：** 后端切换后代码崩溃，或出现 `Tensor type mismatch` 错误

**根因：** `keras.ops` 返回 Keras 管理的张量，后端原生操作返回后端张量。混用可能导致张量类型不兼容

**解法：**

❌ 错误写法 — 混用后端原生操作

```python
import torch
class MyLayer(keras.layers.Layer):
    def call(self, x):
        x = keras.ops.relu(x)
        x = torch.nn.functional.dropout(x, p=0.5)  # ❌ 混用 torch
        return x
```

✅ 正确写法 — 全部使用 keras.ops

```python
class MyLayer(keras.layers.Layer):
    def call(self, x):
        x = keras.ops.relu(x)
        x = keras.layers.Dropout(0.5)(x)  # ✅ 使用 Keras 层
        return x
```

**教训：** 在 Layer/Model 代码中**只用** `keras.ops` 和 `keras.layers`，确保多后端兼容

> 📖 Docs: [Keras 3 — Ops API](https://keras.io/api/ops/)

---

## 坑 4: Subclassing 模型无法 summary() 或序列化

**场景：** 创建了一个 `keras.Model` 子类，调用 `model.summary()` 报错

**症状：** `ValueError: This model has not yet been built` 或序列化时丢失结构

**根因：** Subclassing 模型没有静态计算图，Keras 不知道输入形状直到第一次 `call()`

**解法：**

❌ 错误写法 — 子类模型直接 summary

```python
class MyModel(keras.Model):
    def __init__(self):
        super().__init__()
        self.dense = keras.layers.Dense(10)
    def call(self, x):
        return self.dense(x)

model = MyModel()
model.summary()  # ❌ RuntimeError: model not built
```

✅ 正确写法 — 先 build 再 summary

```python
model = MyModel()
model.build(input_shape=(None, 784))  # 手动 build
model.summary()  # ✅ 正常输出
```

✅ 更好的方案 — 优先使用 Functional API

```python
inputs = keras.Input(shape=(784,))
outputs = keras.layers.Dense(10)(inputs)
model = keras.Model(inputs, outputs)
model.summary()  # ✅ 自动工作
```

**教训：** 除非需要动态控制流，否则优先用 Functional API；子类模型记得手动 `build()`

> 📖 Docs: [Keras 3 — Subclassing Guide](https://keras.io/guides/making_new_layers_and_models_via_subclassing/)

---

## 坑 5: 从 tf.keras 迁移到 Keras 3 时的 import 路径

**场景：** 将旧项目从 `tf.keras` 迁移到独立的 `keras` 包

**症状：** `ModuleNotFoundError` 或行为不一致

**根因：** Keras 3 是独立包 `keras`，不再是 `tensorflow.keras` 的别名。部分 API 路径有变化

**解法：**

❌ 错误写法 — 使用旧的 tf.keras 路径

```python
from tensorflow.keras.layers import Dense       # ❌ Keras 2 路径
from tensorflow.keras.callbacks import EarlyStopping
```

✅ 正确写法 — 使用新的 keras 路径

```python
from keras.layers import Dense                   # ✅ Keras 3 路径
from keras.callbacks import EarlyStopping
# 或
import keras
keras.layers.Dense(...)
```

**教训：** 全局搜索替换 `tensorflow.keras` → `keras`，参考官方迁移指南

> 📖 Docs: [Migrating to Keras 3](https://keras.io/guides/migrating_to_keras_3/)

---

## 坑 6: validation_split 在非 NumPy 数据上不支持

**场景：** 用 `tf.data.Dataset` 或 `torch.utils.data.DataLoader` 调用 `fit()` 并设置 `validation_split`

**症状：** `ValueError: validation_split is only supported for NumPy arrays or tensors`

**根因：** `validation_split` 需要对整个数据集随机分割，但迭代器/生成器类数据源不支持索引

**解法：**

❌ 错误写法 — Dataset + validation_split

```python
dataset = tf.data.Dataset.from_tensor_slices((x, y)).batch(32)
model.fit(dataset, epochs=5, validation_split=0.2)  # ❌ 报错
```

✅ 正确写法 — 手动创建验证集

```python
val_dataset = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(32)
model.fit(dataset, epochs=5, validation_data=val_dataset)  # ✅
```

**教训：** 使用 Dataset/DataLoader 时，用 `validation_data` 显式传入验证集

> 📖 Docs: [Keras 3 — model.fit()](https://keras.io/api/models/model_training_apis/#fit-method)

---

## 坑 7: 保存模型时 `.keras` 后缀遗漏

**场景：** 调用 `model.save("my_model")` 没有加 `.keras` 后缀

**症状：** `ValueError: Invalid filepath. Must end in .keras` 或保存为错误格式

**根因：** Keras 3 强制要求 `.keras` 后缀（或配合 `zipped=False` 保存为目录）

**解法：**

❌ 错误写法 — 没有 .keras 后缀

```python
model.save("my_model")     # ❌ 报错
model.save("my_model.h5")  # ❌ Keras 3 不再默认支持 .h5
```

✅ 正确写法 — 使用 .keras 后缀

```python
model.save("my_model.keras")                # ✅ 标准格式
loaded = keras.saving.load_model("my_model.keras")
```

**教训：** Keras 3 的标准保存格式是 `.keras`，旧的 `.h5` 格式已弃用

> 📖 Docs: [Keras 3 — Saving API](https://keras.io/api/models/model_saving_apis/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/models/model.py:274-317`

---

## 调试清单

1. [ ] **后端正确？** → 检查 `keras.backend.backend()` 返回值，确认 `KERAS_BACKEND` 环境变量
2. [ ] **版本兼容？** → `keras.__version__` 是否为 3.x，后端包版本是否匹配
3. [ ] **import 路径正确？** → 使用 `import keras` 而不是 `from tensorflow import keras`
4. [ ] **模型已 build？** → Subclassing 模型调用 `summary()` 前需要 `build()` 或先 `fit()`
5. [ ] **compile 后修改了 trainable？** → 修改 `trainable` 后必须重新 `compile()`
6. [ ] **使用了 keras.ops？** → 自定义 Layer 中不要混用后端原生操作
7. [ ] **保存格式正确？** → 使用 `.keras` 后缀，不要用 `.h5`
8. [ ] **validation_data 方式正确？** → Dataset/DataLoader 用 `validation_data` 而不是 `validation_split`
9. [ ] **GPU 可用？** → 检查 `keras.backend` 对应后端的 GPU 配置
10. [ ] **数据类型正确？** → 输入数据 dtype 应为 `float32`，标签类型应匹配损失函数期望
