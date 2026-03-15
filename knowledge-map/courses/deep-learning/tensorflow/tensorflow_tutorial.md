---
topic: tensorflow
dimension: tutorial
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: TensorFlow Guide — https://www.tensorflow.org/guide"
  - "📖 Docs: Keras Getting Started — https://keras.io/getting_started/"
  - "💻 Source: tensorflow — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/tensorflow"
expiry: 6m
status: current
---

# TensorFlow 教程

> **前置知识：** Python、NumPy、ML 基础、DL 基础（反向传播）
> **参考来源：** [TF Guide](https://www.tensorflow.org/guide) | [Keras](https://keras.io/)

---

## Section 0: 前置知识速查

1. **NumPy ndarray**：TF Tensor 的设计灵感来源，API 类似
2. **反向传播**：`GradientTape` 的数学基础（链式法则）
3. **梯度下降**：`optimizer.apply_gradients()` 的核心操作
4. **sklearn 工作流**：TF 的 `model.compile/fit/evaluate` 类似 sklearn 的 `fit/predict/score`

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **手写梯度+CUDA 内核：** 没有自动微分框架，每个新层/新损失都需要手推梯度并写 C++/CUDA 实现
- 🔥 **无法部署到端侧：** 训练好的模型导出到手机、浏览器、嵌入式设备需要不同格式和运行时——全部自己写
- 🔥 **分布式训练从零做起：** 多 GPU/多机训练需要手动管理通信、梯度同步、数据分片
- 🔥 **训练-部署割裂：** 用 Python 训练，用 C++ 部署，两端不一致容易出 bug

### 它的核心价值

1. **自动微分 + 计算图优化：** `GradientTape` 自动求导，`@tf.function` 编译优化
2. **端到端一条龙：** 训练 (tf.keras) → 导出 (SavedModel) → 部署 (TF Serving/Lite/JS)
3. **Keras 高级 API：** `model.fit()` 一行训练，降低入门门槛
4. **分布式策略抽象：** `MirroredStrategy` 让多 GPU 训练只需 3 行改动
5. **TPU 原生支持：** Google TPU 只能用 TF（或 JAX），不能用 PyTorch

> 📖 Docs: [Why TensorFlow](https://www.tensorflow.org/about)

---

## Section 2: 它怎么工作的（How）

### 2.1 两种训练方式

```
方式 1: Keras 高级 API（推荐入门）
    model = Sequential([Dense(128, 'relu'), Dense(10, 'softmax')])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    model.fit(X_train, y_train, epochs=10, validation_split=0.2)

方式 2: 自定义训练循环（GradientTape）
    for epoch in range(10):
        for x_batch, y_batch in dataset:
            with tf.GradientTape() as tape:
                y_pred = model(x_batch, training=True)
                loss = loss_fn(y_batch, y_pred)
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))
```

**何时用哪种？** 标准任务用 `model.fit()`（省代码 + 内置 callbacks）；自定义损失/多步训练/GAN 用 GradientTape。

> 📖 Docs: [Custom Training](https://www.tensorflow.org/guide/keras/writing_a_training_loop_from_scratch)

### 2.2 Eager vs Graph 模式

```
Eager（默认）:          @tf.function（Graph 模式）:
  逐行执行                  首次调用时"追踪"函数
  可以 print() 调试          生成优化后的计算图
  速度较慢                   后续调用跳过 Python 直接执行
  适合开发/调试               适合训练/部署
```

**最佳实践：** 开发时 Eager，训练时 `@tf.function` 装饰训练步骤。

> 📖 Docs: [tf.function Guide](https://www.tensorflow.org/guide/function)

### 2.3 tf.data 数据管线

```
dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(10000)        # 打乱
              .batch(32)                 # 分批
              .map(preprocess_fn,        # 数据增强
                   num_parallel_calls=AUTO)
              .prefetch(AUTO)            # CPU 预取 + GPU 训练并行

    CPU: ──[Batch 1]──[Batch 2]──[Batch 3]──
    GPU:           ──[Train 1]──[Train 2]──
                   ↑ prefetch 让 CPU/GPU 流水线化
```

> 📖 Docs: [tf.data Performance](https://www.tensorflow.org/guide/data_performance)

### 2.4 部署全链路

```
训练完成
    │
    ▼
model.save('saved_model/')          ← SavedModel 格式
    │
    ├──→ TF Serving (Docker)         ← REST API / gRPC 服务
    │     docker run -p 8501:8501 ...
    │
    ├──→ TF Lite                     ← 移动端/嵌入式
    │     converter = tf.lite.TFLiteConverter.from_saved_model(path)
    │     tflite_model = converter.convert()
    │
    └──→ TF.js                      ← 浏览器
          tensorflowjs_converter --input_format=tf_saved_model
```

> 📖 Docs: [TF Deployment](https://www.tensorflow.org/tfx/guide/serving)

---

## Section 3: 局限性

1. **API 变动频繁：** TF 1.x→2.x 是破坏性更新，社区旧代码大量失效
2. **调试仍比 PyTorch 难：** `@tf.function` 中的错误栈难读；Eager 模式调试方便但慢
3. **社区/论文偏向 PyTorch：** 2020 年后学术论文大多使用 PyTorch
4. **Keras 3.0 独立化：** Keras 3.0 支持多后端（TF/PyTorch/JAX），模糊了 TF 的 Keras 垄断
5. **启动开销大：** `import tensorflow` 耗时数秒（比 PyTorch 慢）

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **TensorFlow/Keras** | 全栈部署、TPU、`model.fit` | 调试难、社区偏 PyTorch | 工业部署、移动端 |
| **PyTorch** | 灵活、社区大、调试友好 | 部署工具弱于 TF | 研究、教学 |
| **JAX** | 函数式、可组合变换、XLA | 生态小、无内置训练循环 | 科学计算、研究前沿 |
| **Keras 3.0** | 多后端（TF/PT/JAX） | 新项目、生态仍在建设 | 想要后端灵活性 |

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [TF Guide](https://www.tensorflow.org/guide) | 📖 文档 | 全文 |
| [Keras API](https://keras.io/api/) | 📖 文档 | Section 2 |
| [tensorflow 源码](../../../.github/tensorflow/) | 💻 源码 | 底层理解 |
