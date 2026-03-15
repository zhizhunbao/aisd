---
topic: keras
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Chollet, 'Keras', 2015 — https://arxiv.org/abs/1508.01211"
  - "📖 Docs: Keras 3 Official Documentation — https://keras.io/api/"
  - "💻 Source: keras/keras GitHub — https://github.com/keras-team/keras"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.11 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Keras 核心概念

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015
> 📖 Docs: [Keras 3 Official](https://keras.io/api/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/`

---


## 术语定义

### 后端 (Backend)

Keras 3 的「后端」是指底层执行张量计算的框架引擎。Keras 不自己做矩阵乘法——它把所有计算委托给后端（JAX、TensorFlow、PyTorch 或 OpenVINO）。用户通过环境变量 `KERAS_BACKEND` 或 `keras.config.set_backend()` 切换后端，同一份 Keras 代码可以在不同后端上运行。

> 易混淆：**后端 vs 框架** — 后端是 Keras 的「计算引擎插件」，框架（如 PyTorch）是独立的完整 DL 库；Keras 用框架作后端，但 Keras 本身不是框架的一部分

### 层 (Layer)

层是 Keras 的基本构建模块。每个 Layer 封装了一组**可训练权重（weights）** 和一个**前向计算（call）**。层接受张量输入、产生张量输出。所有 Keras 层继承自 `keras.Layer`。自定义层只需覆写 `__init__`（定义权重）和 `call`（定义计算）两个方法。

> 易混淆：**Layer vs Model** — Model 是特殊的 Layer，额外拥有 `compile/fit/evaluate/predict` 训练能力；普通 Layer 只负责计算

### 模型 (Model)

模型是层的组合体，代表一个完整的可训练神经网络。Keras 提供三种建模方式：Sequential（线性堆叠）、Functional API（有向无环图）、Subclassing（继承 Model 类）。Model 继承自 Layer，同时混入 Trainer，因此既能像 Layer 一样被嵌套使用，也能直接训练。

> 易混淆：**Model vs Sequential** — Sequential 是 Model 的子类，仅支持单输入单输出的线性堆叠；Model（Functional）支持任意 DAG 拓扑

### Sequential 模型 (Sequential Model)

Sequential 是最简单的模型类型——将层按顺序堆叠成一条直线。适合快速原型和简单网络。不支持多输入多输出、层共享或非线性拓扑。通过 `model.add(layer)` 逐层添加，或在构造函数中传入层列表。

### Functional API (函数式 API)

Functional API 是 Keras 最强大的建模方式。通过将层当作函数调用（`output = layer(input)`），然后用 `keras.Model(inputs, outputs)` 构建模型。支持多输入多输出、层共享、残差连接等复杂拓扑。模型的计算图在定义时就确定，便于可视化和调试。

> 易混淆：**Functional API vs Subclassing** — Functional 在定义时构建静态图（可序列化、可可视化），Subclassing 在调用时动态执行（灵活但牺牲部分功能）

### 子类化 (Subclassing)

通过继承 `keras.Model` 并覆写 `call()` 方法来定义模型的前向传播。这种方式最灵活，可以在 `call()` 中写任意 Python 逻辑（条件分支、循环等）。代价是丧失了 Functional API 的静态图特性——无法自动 `summary()`、无法直接序列化。

### 编译 (Compile)

`model.compile()` 是训练前的配置步骤。它指定**优化器** (optimizer)、**损失函数** (loss)、**评估指标** (metrics) 三大核心组件。编译不做任何实际计算，只是把这些配置存储在模型内部，供 `fit()` 调用时使用。

> 易混淆：**compile() vs build()** — `compile()` 配置训练策略（优化器/损失/指标），`build()` 创建权重（确定输入形状）；两者目的完全不同

### 训练循环 (Training Loop / fit)

`model.fit()` 是 Keras 内置的训练循环。它自动处理数据批次化、前向传播、损失计算、反向传播、权重更新、指标记录、回调触发等全部流程。用户只需提供数据和超参数（epochs, batch_size 等），无需手写训练循环。

### 回调 (Callback)

回调是训练过程中的「钩子函数」。在训练开始/结束、每个 epoch 开始/结束、每个 batch 开始/结束等时间点自动触发。常用回调包括 `ModelCheckpoint`（保存最优模型）、`EarlyStopping`（提前停止）、`TensorBoard`（可视化）。

### 优化器 (Optimizer)

优化器实现参数更新算法。Keras 内置 SGD、Adam、AdamW、RMSprop 等。通过字符串（`"adam"`）或实例（`keras.optimizers.Adam(lr=1e-3)`）指定。Keras 3 的优化器是后端无关的——同一个 Adam 可以在 JAX/TF/PyTorch 上运行。

### 损失函数 (Loss Function)

损失函数衡量模型预测与真实标签之间的差距。Keras 内置分类损失（`CategoricalCrossentropy`、`SparseCategoricalCrossentropy`）、回归损失（`MeanSquaredError`、`MeanAbsoluteError`）等。可用字符串或实例指定。

### 指标 (Metric)

指标用于评估模型性能，但不参与梯度计算。与损失函数的区别：损失用于优化（反向传播），指标只用于监控。指标支持有状态累积（如 `accuracy` 会跨 batch 累积统计）。

### KerasTensor

KerasTensor 是 Keras 内部的符号张量，用于在 Functional API 中追踪计算图。它不是真正的数值张量，而是形状、dtype、来源层的元数据容器。在实际执行时，KerasTensor 被替换为后端的真实张量。

> 易混淆：**KerasTensor vs 后端张量** — KerasTensor 是「符号占位符」（定义时用），后端张量是「真实数据」（执行时用）

### 模型保存与加载 (Saving / Loading)

Keras 3 的默认保存格式是 `.keras`（一个 zip 文件，包含模型配置 JSON + 权重 HDF5）。支持 `model.save()` / `keras.saving.load_model()` 完整保存，也支持 `model.save_weights()` / `model.load_weights()` 仅保存权重。还可导出为 SavedModel/ONNX/OpenVINO/LiteRT 格式用于部署。

### 量化 (Quantization)

Keras 3 内置模型量化功能——将 float32 权重压缩为 int8/int4/float8 等低精度表示。通过 `model.quantize("int8")` 一行代码即可完成。支持 PTQ（训练后量化）和 GPTQ/AWQ 等高级量化方法。显著减小模型体积和推理延迟。

> 📖 Docs: [Keras 3 API — Layers](https://keras.io/api/layers/)
> 📖 Docs: [Keras 3 API — Models](https://keras.io/api/models/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/models/model.py`, `keras/src/layers/layer.py`

---


## 概念辨析

### Sequential vs Functional API vs Subclassing

| 维度 | Sequential | Functional API | Subclassing |
|------|-----------|----------------|-------------|
| **拓扑** | 线性堆叠（单入单出） | 任意 DAG（多入多出） | 任意（含动态分支） |
| **定义方式** | `model.add(layer)` | `output = layer(input)` + `Model(in, out)` | 覆写 `call()` |
| **可序列化** | ✅ 完全支持 | ✅ 完全支持 | ⚠️ 需手动实现 `get_config()` |
| **`summary()`** | ✅ 完整 | ✅ 完整 | ⚠️ 需先 `build()` |
| **灵活度** | ⭐ 最低 | ⭐⭐⭐ 中高 | ⭐⭐⭐⭐⭐ 最高 |
| **适用场景** | 快速原型、简单分类 | 生产级模型、复杂架构 | 研究、自定义逻辑 |

> 📖 Docs: [Keras 3 — Sequential Model](https://keras.io/guides/sequential_model/)
> 📖 Docs: [Keras 3 — Functional API](https://keras.io/guides/functional_api/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/models/sequential.py`, `keras/src/models/functional.py`

### compile() vs build()

| 维度 | compile() | build() |
|------|-----------|---------|
| **目的** | 配置训练策略 | 创建模型权重 |
| **输入** | optimizer, loss, metrics | input shape |
| **何时调用** | 训练前必须 | 首次 `fit()` 时自动或手动 |
| **可重复调用** | ✅ 可重新编译 | ⚠️ 通常只构建一次 |
| **影响** | 改变优化器/损失/指标 | 改变权重形状和初始化 |

> 📖 Docs: [Keras 3 — Training API](https://keras.io/api/models/model_training_apis/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/trainers/trainer.py`

### Keras 3 vs tf.keras (Keras 2)

| 维度 | Keras 3 | tf.keras (Keras 2) |
|------|---------|-------------------|
| **后端** | JAX / TF / PyTorch / OpenVINO | 仅 TensorFlow |
| **安装** | `pip install keras` | `import tensorflow.keras` |
| **代码可移植性** | ✅ 跨后端 | ❌ 绑定 TF |
| **API 兼容性** | 98%+ 兼容 tf.keras | — |
| **性能** | 后端原生性能 | TF 原生 |
| **状态** | 活跃开发 | 维护模式 |

> 📖 Docs: [Migrating to Keras 3](https://keras.io/guides/migrating_to_keras_3/)

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────────┐
│                        Keras 3 架构                              │
├──────────────────────────────────────────────────────────────────┤
│ 用户 API 层                                                      │
│ ├─ keras.Sequential / keras.Model / keras.Layer                  │
│ ├─ keras.optimizers (Adam, SGD, AdamW ...)                       │
│ ├─ keras.losses (MSE, CrossEntropy ...)                          │
│ ├─ keras.metrics (Accuracy, AUC ...)                             │
│ ├─ keras.callbacks (EarlyStopping, ModelCheckpoint ...)           │
│ └─ keras.saving / keras.export                                   │
├──────────────────────────────────────────────────────────────────┤
│ 核心引擎层                                                       │
│ ├─ Trainer (compile/fit/evaluate/predict)                        │
│ ├─ Functional (计算图追踪)                                       │
│ ├─ KerasTensor (符号张量)                                        │
│ └─ ops (NumPy 兼容操作)                                          │
├──────────────────────────────────────────────────────────────────┤
│ 后端 适配层                                                      │
│ ├─ backend.tensorflow (TensorFlowTrainer)                        │
│ ├─ backend.jax (JAXTrainer)                                      │
│ ├─ backend.torch (TorchTrainer)                                  │
│ ├─ backend.numpy (NumpyTrainer)                                  │
│ └─ backend.openvino (OpenVINOTrainer)                            │
└──────────────────────────────────────────────────────────────────┘
```

> 💻 Source: [keras](../../.github/keras/) `keras/src/models/model.py:20-35`

### 适用场景 ✅

- 快速原型验证——从想法到可运行模型几分钟
- 多后端部署——同一模型需要在 JAX (训练) + TF (部署) 上运行
- 教学和学习——API 清晰、文档丰富，最佳入门深度学习框架
- 标准神经网络任务——分类、回归、生成、序列建模
- 预训练模型微调——Keras Hub 提供 200+ 预训练模型

### 不适用场景 ❌

- 需要后端特有功能（如 PyTorch 的自定义 CUDA kernel、JAX 的 pmap）
- 极致性能要求——Keras 在后端之上增加了一层抽象开销
- 非神经网络 ML——传统机器学习（SVM、决策树等用 scikit-learn）
- 底层张量操作研究——需要直接控制计算图和自动微分

> 📖 Docs: [Keras 3 — Why Keras?](https://keras.io/why_keras/)
> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 创建 Sequential | 线性堆叠层 | `keras.Sequential([Dense(32), Dense(10)])` |
| 创建 Functional | DAG 拓扑 | `Model(inputs=inp, outputs=out)` |
| 编译模型 | 配置训练 | `model.compile(optimizer="adam", loss="mse")` |
| 训练模型 | 内置循环 | `model.fit(x, y, epochs=10)` |
| 评估模型 | 测试性能 | `model.evaluate(x_test, y_test)` |
| 预测 | 推理 | `model.predict(x_new)` |
| 保存模型 | 完整保存 | `model.save("model.keras")` |
| 加载模型 | 恢复模型 | `keras.saving.load_model("model.keras")` |
| 切换后端 | 环境变量 | `os.environ["KERAS_BACKEND"] = "jax"` |
| 量化 | 压缩模型 | `model.quantize("int8")` |

> 📖 Docs: [Keras 3 API Reference](https://keras.io/api/)
