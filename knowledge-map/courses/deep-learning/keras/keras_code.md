---
topic: keras
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: Keras 3 Official Documentation — https://keras.io/api/"
  - "📖 Docs: Keras 3 Getting Started — https://keras.io/getting_started/"
  - "💻 Source: keras/keras GitHub — https://github.com/keras-team/keras"
  - "💻 Source: keras-io GitHub — https://github.com/keras-team/keras-io"
expiry: 3m
status: current
---

# Keras 代码参考

> 📖 Docs: [Keras 3 API Reference](https://keras.io/api/)
> 💻 Source: [keras](../../.github/keras/) | [keras-io](../../.github/keras-io/)


## 快速开始

### 最简示例 — 30 秒上手

```python
import keras
from keras import layers

# ============================================================
# 1. 构建模型 / Build Model
# ============================================================
# 用 Sequential 创建一个简单的两层 MLP
# Create a simple 2-layer MLP using Sequential
model = keras.Sequential([
    layers.Dense(64, activation="relu"),   # 隐藏层 / Hidden layer
    layers.Dense(10, activation="softmax") # 输出层 / Output layer (10 classes)
])

# ============================================================
# 2. 编译模型 / Compile Model
# ============================================================
# 指定优化器、损失函数、评估指标
# Specify optimizer, loss function, and evaluation metrics
model.compile(
    optimizer="adam",                              # 优化器 / Optimizer
    loss="sparse_categorical_crossentropy",        # 损失函数 / Loss function
    metrics=["accuracy"]                           # 指标 / Metrics
)

# ============================================================
# 3. 造假数据训练 / Train with dummy data
# ============================================================
import numpy as np
x_train = np.random.random((1000, 784))            # 1000 个样本, 784 维 / 1000 samples, 784-dim
y_train = np.random.randint(0, 10, (1000,))         # 10 分类标签 / 10-class labels

model.fit(x_train, y_train, epochs=5, batch_size=32)

# ============================================================
# 4. 评估与预测 / Evaluate & Predict
# ============================================================
x_test = np.random.random((200, 784))
y_test = np.random.randint(0, 10, (200,))
loss, acc = model.evaluate(x_test, y_test)          # 评估 / Evaluate
print(f"Test accuracy: {acc:.4f}")

predictions = model.predict(x_test[:5])              # 预测 / Predict
print(f"Predictions shape: {predictions.shape}")     # (5, 10)
```

**测试方法：** 运行脚本，应看到 5 个 epoch 的训练日志和最终测试准确率（约 10% 因为是随机数据）

> 📖 Docs: [Keras 3 — Quick Start](https://keras.io/getting_started/)
> 💻 Source: [keras-io](../../.github/keras-io/) `quickstarts/keras_quickstart.ipynb`

---

## 完整实现示例

### 示例 1: MNIST 手写数字分类（Sequential）

```python
import keras
from keras import layers
import numpy as np

# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
# 加载 MNIST 数据集 / Load MNIST dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 归一化到 [0, 1] / Normalize to [0, 1]
x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
model = keras.Sequential([
    keras.Input(shape=(784,)),                      # 输入形状声明 / Input shape declaration
    layers.Dense(256, activation="relu"),            # 隐藏层 1 / Hidden layer 1
    layers.Dropout(0.3),                             # Dropout 防过拟合 / Dropout for regularization
    layers.Dense(128, activation="relu"),            # 隐藏层 2 / Hidden layer 2
    layers.Dropout(0.3),                             # Dropout
    layers.Dense(10, activation="softmax"),          # 输出层 / Output layer
])

model.summary()                                      # 打印模型结构 / Print model summary

# ============================================================
# 3. 训练 / Training
# ============================================================
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1,                            # 10% 验证集 / 10% validation split
    callbacks=[
        keras.callbacks.EarlyStopping(               # 提前停止 / Early stopping
            monitor="val_loss", patience=3, restore_best_weights=True
        ),
    ]
)

# ============================================================
# 4. 评估 / Evaluation
# ============================================================
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_acc:.4f}")

# 保存模型 / Save model
model.save("mnist_model.keras")
```

> 📖 Docs: [Keras 3 — Sequential Model Guide](https://keras.io/guides/sequential_model/)
> 📖 Docs: [Keras 3 — Training API](https://keras.io/api/models/model_training_apis/)

---

### 示例 2: 多输入多输出模型（Functional API）

```python
import keras
from keras import layers

# ============================================================
# 1. 定义输入 / Define Inputs
# ============================================================
# 数值特征输入 / Numerical features input
num_input = keras.Input(shape=(10,), name="numerical")
# 文本嵌入输入 / Text embedding input
text_input = keras.Input(shape=(128,), name="text_embedding")

# ============================================================
# 2. 分支处理 / Branch Processing
# ============================================================
# 数值分支 / Numerical branch
x_num = layers.Dense(64, activation="relu")(num_input)
x_num = layers.Dense(32, activation="relu")(x_num)

# 文本分支 / Text branch
x_text = layers.Dense(128, activation="relu")(text_input)
x_text = layers.Dense(32, activation="relu")(x_text)

# ============================================================
# 3. 合并 + 多输出 / Merge + Multiple Outputs
# ============================================================
# 拼接两个分支 / Concatenate both branches
merged = layers.Concatenate()([x_num, x_text])
merged = layers.Dense(64, activation="relu")(merged)

# 分类输出 / Classification output
class_output = layers.Dense(5, activation="softmax", name="class_output")(merged)
# 回归输出 / Regression output
score_output = layers.Dense(1, name="score_output")(merged)

# ============================================================
# 4. 构建 + 训练 / Build + Train
# ============================================================
model = keras.Model(
    inputs=[num_input, text_input],
    outputs=[class_output, score_output]
)
model.summary()

model.compile(
    optimizer="adam",
    loss={
        "class_output": "sparse_categorical_crossentropy",  # 分类损失
        "score_output": "mse",                               # 回归损失
    },
    loss_weights={"class_output": 1.0, "score_output": 0.5}, # 损失权重
    metrics={
        "class_output": ["accuracy"],
        "score_output": ["mae"],
    }
)

# model.fit({"numerical": x_num_data, "text_embedding": x_text_data},
#           {"class_output": y_class, "score_output": y_score},
#           epochs=10)
```

> 📖 Docs: [Keras 3 — Functional API Guide](https://keras.io/guides/functional_api/)

---

### 示例 3: 自定义模型 + 自定义训练步（Subclassing）

```python
import keras
from keras import layers, ops

# ============================================================
# 1. 自定义层 / Custom Layer
# ============================================================
class ResidualBlock(layers.Layer):
    """残差块 / Residual Block"""
    def __init__(self, units, **kwargs):
        super().__init__(**kwargs)
        self.dense1 = layers.Dense(units, activation="relu")
        self.dense2 = layers.Dense(units)
        self.add = layers.Add()
        self.relu = layers.Activation("relu")

    def call(self, inputs):
        x = self.dense1(inputs)                      # 第一层 / First layer
        x = self.dense2(x)                           # 第二层 / Second layer
        x = self.add([x, inputs])                    # 残差连接 / Residual connection
        return self.relu(x)                          # 激活 / Activation

# ============================================================
# 2. 自定义模型 + 自定义训练步 / Custom Model + Custom train_step
# ============================================================
class MyModel(keras.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dense_in = layers.Dense(64, activation="relu")
        self.res_block = ResidualBlock(64)
        self.dense_out = layers.Dense(10, activation="softmax")

    def call(self, inputs, training=False):
        x = self.dense_in(inputs)                    # 输入投影 / Input projection
        x = self.res_block(x)                        # 残差块 / Residual block
        return self.dense_out(x)                     # 输出 / Output

    def train_step(self, data):
        """自定义训练步 / Custom training step"""
        x, y = data

        # 前向 + 梯度 / Forward + Gradients
        with keras.backend.GradientTape() if hasattr(keras.backend, 'GradientTape') else None:
            pass
        # 使用默认实现 / Use default implementation
        return super().train_step(data)

# ============================================================
# 3. 使用 / Usage
# ============================================================
model = MyModel()
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
# model.fit(x_train, y_train, epochs=10)
```

> 📖 Docs: [Keras 3 — Custom Layers and Models](https://keras.io/guides/making_new_layers_and_models_via_subclassing/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/layers/layer.py`

---

## API 速查

### 模型构建

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `keras.Sequential(layers)` | `layers` | `None` | 线性堆叠模型 |
| ↳ `.add(layer)` | `layer` | — | 添加一层 |
| ↳ `.pop()` | — | — | 移除最后一层 |
| `keras.Model(inputs, outputs)` | `inputs, outputs` | — | Functional API 构建 |
| `keras.Input(shape)` | `shape` | — | 创建输入占位符 |
| ↳ `dtype` | str | `"float32"` | 输入数据类型 |
| ↳ `name` | str | `None` | 输入名称 |

### 训练与评估

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `.compile(optimizer, loss, metrics)` | `optimizer` | `"rmsprop"` | 配置训练 |
| ↳ `loss` | str/Loss | `None` | 损失函数 |
| ↳ `metrics` | list | `None` | 评估指标 |
| ↳ `jit_compile` | bool | `"auto"` | JIT 编译 |
| `.fit(x, y, epochs, batch_size)` | `epochs` | `1` | 训练模型 |
| ↳ `batch_size` | int | `32` | 批大小 |
| ↳ `validation_split` | float | `0.0` | 验证集比例 |
| ↳ `callbacks` | list | `None` | 回调列表 |
| `.evaluate(x, y)` | `batch_size` | `32` | 评估模型 |
| `.predict(x)` | `batch_size` | `32` | 批量预测 |

### 保存与加载

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `.save(filepath)` | `"model.keras"` | 保存完整模型 |
| `keras.saving.load_model(filepath)` | `"model.keras"` | 加载完整模型 |
| `.save_weights(filepath)` | `"model.weights.h5"` | 仅保存权重 |
| `.load_weights(filepath)` | `"model.weights.h5"` | 仅加载权重 |
| `.export(filepath, format)` | `format="tf_saved_model"` | 导出部署格式 |

### 常用层

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `layers.Dense(units)` | `activation` | 全连接层 |
| `layers.Conv2D(filters, kernel_size)` | `strides, padding` | 2D 卷积层 |
| `layers.LSTM(units)` | `return_sequences` | 长短期记忆层 |
| `layers.Dropout(rate)` | `rate` | 随机丢弃层 |
| `layers.BatchNormalization()` | `axis` | 批归一化层 |
| `layers.Embedding(input_dim, output_dim)` | — | 嵌入层 |
| `layers.GlobalAveragePooling2D()` | — | 全局平均池化 |

### 常用工具

| 函数 | 说明 |
|------|------|
| `keras.ops.matmul(a, b)` | 矩阵乘法 (跨后端) |
| `keras.ops.softmax(x)` | Softmax 激活 |
| `keras.ops.relu(x)` | ReLU 激活 |
| `keras.config.set_backend("jax")` | 切换后端 |
| `keras.utils.plot_model(model)` | 可视化模型 |
| `keras.applications.ResNet50()` | 预训练 ResNet50 |

> 📖 Docs: [Keras 3 API Reference](https://keras.io/api/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/layers/`, `keras/src/ops/`

---

## 目录结构模板

### 简单结构

```
project/
├── train.py              ← 训练脚本 (compile + fit)
├── model.py              ← 模型定义 (Sequential/Functional)
└── data/
    ├── train/
    └── test/
```

### 标准结构

```
project/
├── config.py             ← 超参数配置
├── dataset.py            ← 数据加载和预处理
├── model.py              ← 模型定义
├── train.py              ← 训练脚本
├── evaluate.py           ← 评估脚本
├── callbacks.py          ← 自定义回调
├── data/
├── checkpoints/          ← 模型检查点
└── logs/                 ← TensorBoard 日志
```

### 高级结构

```
project/
├── configs/              ← 多套配置 (yaml/json)
├── models/               ← 多个模型定义
│   ├── __init__.py
│   ├── resnet.py
│   └── transformer.py
├── layers/               ← 自定义层
│   ├── __init__.py
│   └── attention.py
├── datasets/             ← 数据管道
├── trainers/             ← 自定义训练逻辑
├── utils/                ← 工具函数
├── train.py
├── evaluate.py
├── predict.py
├── checkpoints/
├── logs/
└── requirements.txt
```

> 📖 Docs: [Keras 3 — Project Templates](https://keras.io/getting_started/)
> 💻 Source: [keras-io](../../.github/keras-io/) `examples/`
