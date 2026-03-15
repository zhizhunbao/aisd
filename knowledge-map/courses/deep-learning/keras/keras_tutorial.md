---
topic: keras
dimension: tutorial
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Chollet, 'Keras', 2015 — https://arxiv.org/abs/1508.01211"
  - "📖 Docs: Keras 3 Official Documentation — https://keras.io/api/"
  - "📖 Docs: Keras 3 Getting Started — https://keras.io/getting_started/"
  - "💻 Source: keras/keras GitHub — https://github.com/keras-team/keras"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.11 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Keras 教程

> **前置知识：** Python 基础 | NumPy 张量运算 | 神经网络基本原理 (前向传播、反向传播、损失函数)
> **参考来源：** [Keras 3 Docs](https://keras.io/api/) | [Chollet 2015](https://arxiv.org/abs/1508.01211) | [《Deep Learning》Ch.11](../../textbooks/goodfellow_deep_learning.pdf)

---


## Section 0: 前置知识速查

1. **Python 面向对象编程**：理解类继承、`__init__`、方法重写——Keras 的 Layer/Model 都基于 OOP
2. **NumPy 张量操作**：理解多维数组（ndarray）、shape、dtype、广播——Keras 的 `keras.ops` 与 NumPy API 高度一致
3. **神经网络基础**：理解前向传播（输入 → 层 → 输出）、反向传播（梯度 → 更新权重）、损失函数（量化预测误差）
4. **梯度下降优化**：理解 SGD、Adam 等优化器的基本原理——Keras 的 `compile()` 需要指定优化器

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../textbooks/goodfellow_deep_learning.pdf), Ch.6-8
> 📖 Docs: [Keras 3 — Getting Started](https://keras.io/getting_started/)

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **代码冗余爆炸**：直接用 PyTorch / TF 底层 API，一个简单的训练循环就需要 50+ 行代码（数据加载 → 前向 → 损失 → 反向 → 更新 → 日志 → 保存），每个项目都得重写
- 🔥 **后端锁定**：用 `tf.keras` 写的模型只能在 TensorFlow 上运行，想换 JAX 或 PyTorch 得重写全部代码
- 🔥 **认知负荷高**：初学者面对 `torch.nn.Module`, `torch.optim`, `torch.utils.data`, `torch.cuda` 等几十个模块，不知从何下手
- 🔥 **可复现性差**：每个研究者写自己的训练循环风格，导致代码难以阅读和复现
- 🔥 **部署碎片化**：不同后端的模型导出方式完全不同（SavedModel vs ONNX vs TorchScript），需要后端专有知识

### 它的核心价值

1. **极简 API 设计**：`compile → fit → evaluate → predict` 四步完成完整训练流程，5 行代码跑通 MNIST
2. **多后端统一**：同一份 `keras.Model` 代码可透明运行在 JAX / TensorFlow / PyTorch / OpenVINO 上——真正的 "Write once, run anywhere"
3. **渐进式复杂度**：从 Sequential（零门槛）→ Functional API（中级）→ Subclassing（高级）→ 自定义训练循环（专家），按需决定抽象层级
4. **生态系统完整**：Keras Hub（预训练模型）、Keras Tuner（超参搜索）、Keras CV/NLP（垂直领域工具包）

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015 — Section 1 "Design Principles"
> 📖 Docs: [Why Keras?](https://keras.io/why_keras/)

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 Keras 3 架构总览

```
┌───────────────────────────────────────────────────────────────┐
│                    Keras 3 运行时流程                          │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  用户代码                                                     │
│  model = keras.Sequential([Dense(32), Dense(10)])             │
│  model.compile(optimizer="adam", loss="mse")                  │
│  model.fit(x, y, epochs=5)                                   │
│      │                                                       │
│      ▼                                                       │
│  ┌──────────────────────────────────────────────────┐        │
│  │ Trainer (keras/src/trainers/trainer.py)           │        │
│  │  compile() → 存储 optimizer, loss, metrics        │        │
│  │  fit()     → 调用后端特定的 Trainer               │        │
│  └──────────────┬───────────────────────────────────┘        │
│                 │ 委托给后端 Trainer                           │
│                 ▼                                             │
│  ┌──────────────────────────────────────────────────┐        │
│  │ Backend Trainer                                   │        │
│  │  ├─ TensorFlowTrainer  (tf.GradientTape)         │        │
│  │  ├─ JAXTrainer         (jax.grad + jit)          │        │
│  │  ├─ TorchTrainer       (torch.autograd)          │        │
│  │  └─ NumpyTrainer       (推理 only, 无梯度)       │        │
│  └──────────────┬───────────────────────────────────┘        │
│                 │ 执行                                        │
│                 ▼                                             │
│  ┌──────────────────────────────────────────────────┐        │
│  │ Layer.call() + keras.ops (NumPy 兼容操作)        │        │
│  │  → 转换为后端原生操作                              │        │
│  │  → tf.matmul / jnp.dot / torch.mm                │        │
│  └──────────────────────────────────────────────────┘        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

> 💻 Source: [keras](../../.github/keras/) `keras/src/models/model.py:20-35` — 后端 Trainer 动态导入
> 💻 Source: [keras](../../.github/keras/) `keras/src/trainers/trainer.py:19-32` — Trainer 基类

### 2.2 多后端架构：为什么用抽象层而不是直接调用？

**为什么用统一 `keras.ops` 而不是直接用 `tf.nn` / `torch.nn.functional`？**

Keras 3 的核心创新是 **ops 抽象层**：`keras.ops` 提供了一套与 NumPy 兼容的操作接口（如 `keras.ops.matmul`, `keras.ops.relu`），在运行时根据当前后端自动分发到对应的原生操作。

这意味着：
- Layer 的 `call()` 方法中只使用 `keras.ops`，无需关心后端
- 后端切换对 Layer 代码完全透明
- 新增后端只需实现 ops 映射，不需要修改任何 Layer

```
用户代码:  keras.ops.matmul(a, b)
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 tf.matmul  jnp.dot  torch.mm
```

> 💻 Source: [keras](../../.github/keras/) `keras/src/ops/` — ops 抽象层实现
> 📖 Docs: [Keras 3 — Ops API](https://keras.io/api/ops/)

### 2.3 三种建模方式的内部实现

**Sequential 内部其实是 Functional**：当你 `add` 层并且已知输入形状时，Sequential 内部会自动构建一个 Functional 模型来追踪计算图。这就是为什么 Sequential 模型也能 `summary()` 和序列化。

**Functional API 的核心是 KerasTensor**：每次 `layer(input_tensor)` 调用，Keras 不会真正计算——它创建一个新的 KerasTensor，记录"这个张量是哪个层的输出"。最后 `Model(inputs, outputs)` 遍历 KerasTensor 链条，构建出完整的计算图。

**Subclassing 是纯命令式**：没有 KerasTensor 追踪，`call()` 中的代码在实际调用时才执行。因此无法自动获得计算图——这就是 Subclassing 不支持自动 `summary()` 的原因。

> 💻 Source: [keras](../../.github/keras/) `keras/src/models/sequential.py:190-216` — Sequential 构建 Functional
> 💻 Source: [keras](../../.github/keras/) `keras/src/backend/common/keras_tensor.py` — KerasTensor

### 2.4 训练流程详解

```
model.fit(x, y, epochs=N)
│
├── 每个 epoch:
│   ├── 数据 → DataAdapter → 批次化
│   ├── 每个 batch:
│   │   ├── train_step():
│   │   │   ├── y_pred = model(x, training=True)     # 前向
│   │   │   ├── loss = compute_loss(y, y_pred)         # 损失
│   │   │   ├── gradients = backend.grad(loss, params)  # 反向
│   │   │   ├── optimizer.apply(gradients, params)      # 更新
│   │   │   └── compute_metrics(y, y_pred)              # 指标
│   │   └── 触发 on_batch_end 回调
│   ├── 验证 (if validation_data)
│   └── 触发 on_epoch_end 回调
└── 返回 History 对象
```

> 💻 Source: [keras](../../.github/keras/) `keras/src/trainers/trainer.py:534-734` — fit() 方法
> 📖 Docs: [Keras 3 — Training API](https://keras.io/api/models/model_training_apis/)

---


## Section 3: 局限性

1. **抽象开销**：Keras 在后端之上增加了一层间接调用 → 对于极致性能要求（如大规模分布式训练），可能比直接用原生后端慢几个百分点 → **应对**: 性能敏感部分用自定义训练循环 + 原生后端操作
2. **后端差异泄漏**：尽管 Keras 3 力求统一，某些行为仍因后端而异（如 JAX 的纯函数约束、PyTorch 的 eager 特性） → **应对**: 测试时覆盖多后端，使用 `keras.ops` 而非后端原生操作
3. **Subclassing 功能受限**：子类化模型无法自动序列化、无法显示 `summary()`（除非先 build） → **应对**: 优先使用 Functional API，只在必须时使用 Subclassing
4. **生态碎片化**：Keras Hub / Keras CV / Keras NLP 仍在发展中，模型覆盖不如 Hugging Face 全面 → **应对**: 混合使用 Keras 和 Hugging Face

> 📖 Docs: [Keras 3 — Migration Guide](https://keras.io/guides/migrating_to_keras_3/)
> 📖 Docs: [Keras 3 — Known Limitations](https://keras.io/getting_started/faq/)

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **Keras 3** | 多后端统一、API 极简、渐进复杂度 | 抽象开销、部分功能受后端限制 | 快速原型、教学、多平台部署 |
| **PyTorch (原生)** | 灵活、社区庞大、CUDA 生态成熟 | 训练循环需手写、无 JIT 编译优势 | 研究、自定义 CUDA 操作 |
| **PyTorch Lightning** | 结构化训练、减少样板代码 | 仅 PyTorch 后端、学习曲线 | PyTorch 用户的生产级训练 |
| **JAX (原生)** | 函数式设计、极致性能(pjit) | 学习曲线陡、无内置训练循环 | 大规模分布式训练、TPU |
| **Hugging Face Transformers** | 最全预训练模型、社区活跃 | 仅 NLP/多模态、API 复杂 | 预训练模型微调、NLP 任务 |

> 📖 Docs: [Why Keras?](https://keras.io/why_keras/)
> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Chollet, Keras 2015](https://arxiv.org/abs/1508.01211) | 📖 论文 | Section 1 设计哲学 |
| [Keras 3 Official Docs](https://keras.io/api/) | 📖 文档 | 全文核心参考 |
| [《Deep Learning》Ch.11](../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | Section 0 前置知识 |
| [keras GitHub](../../.github/keras/) | 💻 源码 | Section 2 内部实现 |
| [keras-io GitHub](../../.github/keras-io/) | 💻 源码 | 示例代码参考 |
