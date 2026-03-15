---
topic: keras
dimension: bridge
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

# Keras 衔接与扩展

> 📖 Docs: [Keras 3 Official](https://keras.io/api/)
> 💻 Source: [keras](../../.github/keras/) | [keras-io](../../.github/keras-io/)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Tensor (张量) | Keras 的所有计算都基于张量操作 | [tensor_map.md](../tensor/tensor_map.md) |
| ← 前置 | MLP (多层感知机) | Keras 最基本的层 (Dense) 就是 MLP 的一层 | [mlp_map.md](../mlp/mlp_map.md) |
| ← 前置 | CNN (卷积神经网络) | Keras 内置 Conv2D 等卷积层 | [cnn_map.md](../cnn/cnn_map.md) |
| ← 前置 | TensorFlow / PyTorch | Keras 的计算后端 | [tensorflow_map.md](../tensorflow/tensorflow_map.md) / [pytorch_map.md](../pytorch/pytorch_map.md) |
| → 后续 | Keras Hub | 预训练模型库，基于 Keras 3 API | — |
| → 后续 | 分布式训练 | 多 GPU/TPU 训练，用 `keras.distribution` | — |
| → 后续 | 模型量化与部署 | `model.quantize()` + `model.export()` | — |
| → 后续 | 自定义训练循环 | 覆写 `train_step()` 或完全手写循环 | — |

> 📖 Docs: [Keras 3 — Getting Started](https://keras.io/getting_started/)

---

## 上游依赖

| 来自主题 | 复用的概念 | 在 Keras 中如何使用 |
|---------|-----------|-------------------|
| Tensor (张量) | 多维数组、shape、dtype、广播 | `keras.ops` 提供 NumPy 兼容的张量操作 API |
| MLP | 全连接层、激活函数、前向传播 | `keras.layers.Dense` — Keras 最基础的层 |
| CNN | 卷积、池化、特征图 | `keras.layers.Conv2D`, `MaxPooling2D` 等 |
| 反向传播 | 梯度计算、链式法则 | 后端自动微分 (tf.GradientTape / jax.grad / torch.autograd) |
| 优化器 | SGD、Adam、学习率调度 | `keras.optimizers` — 统一的优化器 API |
| 损失函数 | 交叉熵、MSE 等 | `keras.losses` — 统一的损失 API |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../textbooks/goodfellow_deep_learning.pdf), Ch.6-8, 11

---

## 下游影响

| 去向主题 | Keras 提供的概念 | 在下游如何被使用 |
|---------|-----------------|----------------|
| Keras Hub | Model + Layer API | Hub 的所有模型都是 Keras Model 子类 |
| 迁移学习 | `layer.trainable` + `compile()` | 冻结骨干网络 → 微调头部层 |
| 分布式训练 | `keras.distribution.DataParallel` | 多 GPU 数据并行训练 |
| 模型压缩 | `model.quantize("int8")` | 训练后量化用于边缘部署 |
| AutoML | Keras Tuner + Sequential/Functional | 自动搜索模型结构和超参数 |
| 部署 | `model.export(format="tf_saved_model")` | 导出为 SavedModel/ONNX/LiteRT |

> 📖 Docs: [Keras Hub](https://keras.io/keras_hub/)
> 📖 Docs: [Keras Tuner](https://keras.io/keras_tuner/)

---

## 概念演变追踪

| 概念 | 在 Keras 1/2 (tf.keras) 中 | 在 Keras 3 中 | 变化原因 |
|------|---------------------------|---------------|---------|
| 后端 | Theano (已废) → TF only | JAX / TF / PyTorch / OpenVINO | 解耦框架绑定 |
| 保存格式 | `.h5` (HDF5) | `.keras` (zip: JSON + H5) | 更好的可移植性和元数据 |
| 张量操作 | `tf.nn.*` / `K.backend()` | `keras.ops.*` (NumPy 兼容) | 后端无关 |
| JIT 编译 | `tf.function` | `jit_compile="auto"` (自动选择) | 简化跨后端 JIT |
| 数据管道 | `tf.data` only | `tf.data` / `torch.DataLoader` / `PyDataset` | 后端原生数据管道 |
| 分布式 | `tf.distribute.Strategy` | `keras.distribution` | 统一多后端分布式 |
| 模型导出 | `tf.saved_model.save()` | `model.export(format=...)` | SavedModel+ONNX+OpenVINO+LiteRT |

> 📖 Docs: [Migrating to Keras 3](https://keras.io/guides/migrating_to_keras_3/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/models/model.py`

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Chollet, Keras 2015](https://arxiv.org/abs/1508.01211) | 📖 论文 | Keras 设计哲学的第一手来源 | ⭐⭐ |
| [Keras 3 源码 — Model 类](../../.github/keras/keras/src/models/model.py) | 💻 源码 | 理解 Model/Trainer/Layer 继承链 | ⭐⭐⭐ |
| [Keras 3 源码 — Trainer](../../.github/keras/keras/src/trainers/trainer.py) | 💻 源码 | 理解 compile/fit/evaluate 内部实现 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|-------|
| [PyTorch Lightning Docs](https://lightning.ai/docs/) | PyTorch 的高层 API vs Keras | 评估 Keras vs Lightning 选型时 |
| [JAX Documentation](https://jax.readthedocs.io/) | JAX 底层 vs Keras 高层 | 需要直接用 JAX 时 |
| [Hugging Face Transformers](https://huggingface.co/docs/transformers/) | NLP 生态 vs Keras Hub | NLP/LLM 项目选型时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|-------|
| [Keras Hub 文档](https://keras.io/keras_hub/) | 200+ 预训练模型 | 需要预训练模型微调时 |
| [Keras Tuner 文档](https://keras.io/keras_tuner/) | 超参数自动搜索 | AutoML 场景 |
| [Keras Examples](../../.github/keras-io/examples/) | 官方代码示例集 | 学习特定任务的实现方式 |

> 📖 Docs: [Keras 3 Official](https://keras.io/)

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 深度学习基础 | 3 | [CNN](../cnn/cnn_map.md), [MLP](../mlp/mlp_map.md), [Tensor](../tensor/tensor_map.md) | Keras 实现这些概念的具体层 |
| 深度学习框架 | 2 | [TensorFlow](../tensorflow/tensorflow_map.md), [PyTorch](../pytorch/pytorch_map.md) | Keras 的计算后端 |
| 深度学习问题 | 1 | [梯度消失](../vanishing_gradient/vanishing_gradient_map.md) | Keras 中 BatchNorm、残差连接的实现 |
| 卷积层 | 1 | [Conv Layer](../conv_layer/conv_layer_map.md) | `keras.layers.Conv2D` 的数学和实现细节 |
