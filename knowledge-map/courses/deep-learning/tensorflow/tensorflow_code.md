---
topic: tensorflow
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: TensorFlow API — https://www.tensorflow.org/api_docs/python/tf"
  - "📖 Docs: Keras API — https://keras.io/api/"
  - "💻 Source: keras — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/keras"
expiry: 3m
status: current
---

# TensorFlow 代码参考

> 📖 Docs: [TensorFlow API](https://www.tensorflow.org/api_docs/python/tf)
> 📖 Docs: [Keras API](https://keras.io/api/)

## 快速开始

### 最简示例 — 30 秒上手

```python
import tensorflow as tf

# ============================================================
# MNIST 分类 / MNIST Classification
# ============================================================
# 1. 加载数据 / Load data
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
X_train, X_test = X_train / 255.0, X_test / 255.0   # 归一化 / Normalize

# 2. 构建模型 / Build model
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),    # 展平 / Flatten
    tf.keras.layers.Dense(128, activation='relu'),     # 全连接 / Dense
    tf.keras.layers.Dropout(0.2),                      # 正则化 / Regularize
    tf.keras.layers.Dense(10, activation='softmax')    # 输出层 / Output
])

# 3. 编译+训练 / Compile + Train
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=5, validation_split=0.1)

# 4. 评估 / Evaluate
model.evaluate(X_test, y_test)
```

**测试方法：** 运行后 test accuracy ≈ 97-98%

> 📖 Docs: [Keras Getting Started](https://keras.io/getting_started/)

---

## 完整实现示例

### 示例 1: 自定义训练循环 (GradientTape)

```python
import tensorflow as tf

# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0

train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train))
train_ds = train_ds.shuffle(10000).batch(64).prefetch(tf.data.AUTOTUNE)
test_ds = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(64)

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)                          # logits, 不加 softmax
])

# ============================================================
# 3. 优化器+损失 / Optimizer + Loss
# ============================================================
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
train_acc = tf.keras.metrics.SparseCategoricalAccuracy()

# ============================================================
# 4. 自定义训练步骤 / Custom Training Step
# ============================================================
@tf.function                                           # 编译为图模式 / Graph mode
def train_step(x, y):
    with tf.GradientTape() as tape:                    # 记录梯度 / Record gradients
        logits = model(x, training=True)               # 前向 / Forward
        loss = loss_fn(y, logits)                      # 损失 / Loss
    grads = tape.gradient(loss, model.trainable_variables)  # 反向 / Backward
    optimizer.apply_gradients(zip(grads, model.trainable_variables))  # 更新 / Update
    train_acc.update_state(y, logits)
    return loss

# ============================================================
# 5. 训练循环 / Training Loop
# ============================================================
for epoch in range(10):
    train_acc.reset_state()
    for x_batch, y_batch in train_ds:
        loss = train_step(x_batch, y_batch)
    print(f"Epoch {epoch+1}: loss={loss:.4f}, acc={train_acc.result():.4f}")

# ============================================================
# 6. 评估 / Evaluation
# ============================================================
test_acc = tf.keras.metrics.SparseCategoricalAccuracy()
for x_batch, y_batch in test_ds:
    logits = model(x_batch, training=False)
    test_acc.update_state(y_batch, logits)
print(f"Test accuracy: {test_acc.result():.4f}")
```

> 📖 Docs: [Custom Training](https://www.tensorflow.org/guide/keras/writing_a_training_loop_from_scratch)

---

### 示例 2: CNN 图像分类 (Functional API + Callbacks)

```python
import tensorflow as tf
from tensorflow.keras import layers, Model, callbacks

# ============================================================
# 1. 数据 / Data
# ============================================================
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()
X_train, X_test = X_train / 255.0, X_test / 255.0

# ============================================================
# 2. Functional API 模型 / Functional API Model
# ============================================================
inputs = layers.Input(shape=(32, 32, 3))
x = layers.Conv2D(32, 3, padding='same', activation='relu')(inputs)
x = layers.BatchNormalization()(x)
x = layers.MaxPooling2D()(x)
x = layers.Conv2D(64, 3, padding='same', activation='relu')(x)
x = layers.BatchNormalization()(x)
x = layers.MaxPooling2D()(x)
x = layers.Conv2D(128, 3, padding='same', activation='relu')(x)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(10, activation='softmax')(x)

model = Model(inputs, outputs)
model.summary()

# ============================================================
# 3. 编译 / Compile
# ============================================================
model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ============================================================
# 4. Callbacks
# ============================================================
cbs = [
    callbacks.EarlyStopping(patience=5, restore_best_weights=True),
    callbacks.ReduceLROnPlateau(factor=0.5, patience=3),
    callbacks.ModelCheckpoint('best_model.keras', save_best_only=True),
]

# ============================================================
# 5. 训练 / Train
# ============================================================
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=64,
    validation_split=0.1,
    callbacks=cbs
)

# ============================================================
# 6. 保存+部署 / Save + Deploy
# ============================================================
model.save('cifar10_saved_model')     # SavedModel 格式
```

> 📖 Docs: [Keras Functional API](https://keras.io/guides/functional_api/)

---

### 示例 3: 分布式训练 (MirroredStrategy)

```python
import tensorflow as tf

# ============================================================
# 多 GPU 训练 / Multi-GPU Training
# ============================================================
strategy = tf.distribute.MirroredStrategy()               # 自动检测 GPU
print(f"Number of devices: {strategy.num_replicas_in_sync}")

with strategy.scope():                                      # 在策略作用域内
    model = tf.keras.Sequential([                           # 构建模型
        tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

# 正常训练 — 框架自动处理数据分片和梯度同步
model.fit(X_train, y_train, epochs=10, batch_size=64 * strategy.num_replicas_in_sync)
```

> 📖 Docs: [tf.distribute](https://www.tensorflow.org/guide/distributed_training)

---

## API 速查

### 模型构建

| 层/类 | 参数 | 说明 |
|-------|------|------|
| `Dense(units, activation)` | `units, activation` | 全连接层 |
| `Conv2D(filters, kernel_size)` | `filters, kernel_size, strides, padding` | 2D 卷积 |
| `MaxPooling2D(pool_size)` | `pool_size` | 最大池化 |
| `GlobalAveragePooling2D()` | — | 全局平均池化 |
| `BatchNormalization()` | — | 批归一化 |
| `Dropout(rate)` | `rate` | 随机丢弃 |
| `Flatten()` | — | 展平 |
| `LSTM(units)` | `units, return_sequences` | LSTM 循环层 |
| `Embedding(input_dim, output_dim)` | `input_dim, output_dim` | 词嵌入 |

### 训练

| API | 说明 |
|-----|------|
| `model.compile(optimizer, loss, metrics)` | 配置训练 |
| `model.fit(X, y, epochs, batch_size, callbacks)` | 训练 |
| `model.evaluate(X, y)` | 评估 |
| `model.predict(X)` | 推理 |
| `tf.GradientTape()` | 自动微分 |
| `tape.gradient(loss, vars)` | 计算梯度 |
| `optimizer.apply_gradients(grads_and_vars)` | 更新参数 |

### 数据

| API | 说明 |
|-----|------|
| `tf.data.Dataset.from_tensor_slices(data)` | 创建 Dataset |
| `.shuffle(buffer_size)` | 打乱 |
| `.batch(batch_size)` | 分批 |
| `.map(fn, num_parallel_calls=AUTO)` | 并行变换 |
| `.prefetch(AUTO)` | CPU/GPU 流水线 |

### 保存/加载

| API | 说明 |
|-----|------|
| `model.save('path/')` | 保存 SavedModel |
| `tf.keras.models.load_model('path/')` | 加载模型 |
| `tf.saved_model.load('path/')` | 底层加载 |
| `model.save_weights('path')` | 只保存权重 |

> 📖 Docs: [TensorFlow API](https://www.tensorflow.org/api_docs/python/tf)
