---
topic: tensorflow
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: TensorFlow Guide — https://www.tensorflow.org/guide"
  - "📖 Docs: Keras API — https://keras.io/api/"
  - "💻 Source: tensorflow/tensorflow — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/tensorflow"
expiry: 6m
status: current
---

# TensorFlow 核心概念

> 📖 Docs: [TensorFlow Guide](https://www.tensorflow.org/guide)
> 📖 Docs: [Keras API](https://keras.io/api/)

---

## 术语定义

### 张量 (Tensor / tf.Tensor)

TF 的基本数据单元——多维数组。`tf.constant([1,2,3])` 创建 1D 张量，`tf.zeros([3,4])` 创建 3×4 零矩阵。张量有形状 (shape)、数据类型 (dtype) 和设备 (device)。张量默认不可变（immutable）；可变版本用 `tf.Variable`。

> 易混淆：**tf.Tensor vs tf.Variable** — Tensor 不可变、不跟踪梯度；Variable 可变、参与梯度计算（模型参数用 Variable）

### 变量 (tf.Variable)

可变的、持久化的张量，用于存储模型参数（权重和偏置）。`tf.Variable(initial_value)` 创建，`var.assign(new_val)` 更新。Variable 的变化会被 `GradientTape` 自动追踪。所有 Keras 层的 `weights` 属性返回的都是 Variable。

### 计算图 (Computational Graph / tf.Graph)

将数学运算表示为有向无环图 (DAG)。TF 1.x 是纯静态图（先构建图、再 Session.run 执行）；TF 2.x 默认 Eager Execution（立即执行），但可以用 `@tf.function` 将函数转为图模式以获得性能优化。

> 易混淆：**Eager vs Graph 模式** — Eager = Python 般逐行执行（方便调试）；Graph = 编译优化后执行（高性能）。TF 2.x 默认 Eager，用 `@tf.function` 切换到 Graph

### Eager Execution

TF 2.x 的默认执行模式——运算立即执行并返回结果，像普通 Python 代码。不需要 `Session`，可以用 `print()` 调试。大幅降低了 TF 的学习曲线。

### @tf.function

装饰器，将 Python 函数编译为 TF 计算图（AutoGraph）。首次调用时"追踪"（trace）函数，生成图；后续调用直接执行图。能获得 XLA 编译加速、跨平台部署、并行优化等好处。

### GradientTape (tf.GradientTape)

TF 2.x 的自动微分机制。在 `with tf.GradientTape() as tape:` 上下文中，所有涉及 `tf.Variable` 的运算会被记录。调用 `tape.gradient(loss, variables)` 计算梯度。默认只能调用一次（单次使用），设 `persistent=True` 可重复调用。

### Keras Sequential / Functional / Subclassing

三种构建模型的方式：
1. **Sequential**：`tf.keras.Sequential([Dense(64), ReLU(), Dense(10)])`——线性堆叠层，最简单
2. **Functional API**：`inputs = Input(); x = Dense(64)(inputs); model = Model(inputs, x)`——支持多输入多输出、共享层
3. **Subclassing**：继承 `tf.keras.Model`，重写 `call()`——最灵活，类似 PyTorch

### 层 (tf.keras.layers.Layer)

神经网络的基本构建单元。每个 Layer 有 `build()` (创建权重)、`call()` (前向计算) 两个核心方法。常用层：`Dense`（全连接）、`Conv2D`（卷积）、`BatchNormalization`、`Dropout`、`LSTM` 等。

### 回调 (tf.keras.callbacks.Callback)

训练过程中自动执行的钩子函数。常用回调：`ModelCheckpoint`（保存最优模型）、`EarlyStopping`（验证损失不降则停止）、`TensorBoard`（可视化训练）、`ReduceLROnPlateau`（自动降低学习率）。

### tf.data.Dataset

高效数据输入管线。`tf.data.Dataset.from_tensor_slices(data)` 创建，支持 `.batch()`, `.shuffle()`, `.map()`, `.prefetch()` 等链式变换。`prefetch(tf.data.AUTOTUNE)` 实现 CPU 数据预处理和 GPU 训练的流水线并行。

### 分布式策略 (tf.distribute.Strategy)

多 GPU / 多机训练的抽象层。`MirroredStrategy`（单机多 GPU）、`MultiWorkerMirroredStrategy`（多机多 GPU）、`TPUStrategy`（TPU）。用 `with strategy.scope():` 包裹模型创建代码即可。

### SavedModel

TF 的标准模型序列化格式。`model.save('path/')` 保存为 SavedModel 目录，包含计算图 + 权重 + 签名。可被 TF Serving、TF Lite、TF.js 直接加载部署。

> 📖 Docs: [TensorFlow Guide](https://www.tensorflow.org/guide)
> 📖 Docs: [Keras API](https://keras.io/api/)

---

## 概念辨析

### TensorFlow vs PyTorch

| 维度 | TensorFlow 2.x | PyTorch |
|------|---|---|
| **默认模式** | Eager（可 @tf.function 转图） | 动态图（可 torch.compile） |
| **高级 API** | tf.keras（内置） | torch.nn（需额外写训练循环） |
| **部署** | TF Serving / TF Lite / TF.js | TorchServe / ONNX |
| **TPU** | 原生支持 | 需 torch_xla |
| **研究社区** | 工业偏好 | 学术偏好 |
| **训练循环** | `model.fit()` 一行搞定 | 手写循环（灵活） |

### Sequential vs Functional vs Subclassing

| 维度 | Sequential | Functional API | Subclassing |
|------|---|---|---|
| **复杂度** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **多输入/输出** | ❌ | ✅ | ✅ |
| **共享层** | ❌ | ✅ | ✅ |
| **动态控制流** | ❌ | ❌ | ✅ |
| **可序列化** | ✅ 容易 | ✅ 容易 | ⚠️ 需额外代码 |
| **推荐场景** | 简单线性堆叠 | 大多数场景 | 研究/自定义 |

> 📖 Docs: [Keras Functional API](https://keras.io/guides/functional_api/)

---

## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────┐
│                 TensorFlow 核心模块                        │
├──────────────────────────────────────────────────────────┤
│  数据 (tf.data)                                           │
│  ├─ Dataset: from_tensor_slices / from_generator          │
│  └─ 变换: batch / shuffle / map / prefetch                │
├──────────────────────────────────────────────────────────┤
│  模型构建 (tf.keras)                                       │
│  ├─ layers: Dense / Conv2D / LSTM / Dropout / BN          │
│  ├─ Model: Sequential / Functional / Subclassing          │
│  └─ losses / metrics / optimizers                         │
├──────────────────────────────────────────────────────────┤
│  训练 (tf.keras + tf.GradientTape)                        │
│  ├─ model.compile() + model.fit()  (高级)                 │
│  └─ GradientTape 自定义训练循环 (底层)                      │
├──────────────────────────────────────────────────────────┤
│  部署                                                      │
│  ├─ SavedModel (标准格式)                                  │
│  ├─ TF Serving (服务端 REST/gRPC)                          │
│  ├─ TF Lite (移动/嵌入式)                                  │
│  └─ TF.js (浏览器)                                        │
├──────────────────────────────────────────────────────────┤
│  分布式 (tf.distribute)                                    │
│  ├─ MirroredStrategy (单机多 GPU)                          │
│  └─ TPUStrategy (Google TPU)                               │
└──────────────────────────────────────────────────────────┘
```

### 适用场景 ✅

- 端到端 DL 项目（训练→部署一条龙）
- 移动端/嵌入式部署（TF Lite）
- 浏览器 AI 应用（TF.js）
- Google Cloud TPU 训练
- 工业级 serving（TF Serving 成熟稳定）
- Keras 快速原型（`model.fit()` 一行训练）

### 不适用场景 ❌

- 传统 ML（用 sklearn）
- 纯研究/灵活实验（PyTorch 更灵活）
- 函数式 / 科学计算（用 JAX）
- 小规模脚本（TF 启动开销大）

---

## 速查表

| 项 | 说明 | 示例 |
|----|------|------|
| `tf.constant(val)` | 创建不可变张量 | `tf.constant([1,2,3])` |
| `tf.Variable(val)` | 创建可变变量 | `tf.Variable(0.0)` |
| `tf.GradientTape()` | 自动微分上下文 | `tape.gradient(loss, vars)` |
| `@tf.function` | 编译为计算图 | 装饰训练步骤函数 |
| `model.compile()` | 配置优化器+损失 | `compile(optimizer='adam', loss='mse')` |
| `model.fit()` | 训练 | `fit(X, y, epochs=10)` |
| `model.predict()` | 推理 | `predict(X_test)` |
| `model.save()` | 保存 SavedModel | `save('model_dir/')` |
| `tf.data.Dataset` | 数据管线 | `.batch(32).prefetch(AUTO)` |

> 📖 Docs: [TensorFlow API](https://www.tensorflow.org/api_docs/python/tf)
