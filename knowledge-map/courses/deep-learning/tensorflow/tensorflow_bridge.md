---
topic: tensorflow
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: TensorFlow Ecosystem — https://www.tensorflow.org/resources/tools"
  - "📖 Docs: TensorFlow Guide — https://www.tensorflow.org/guide"
expiry: 6m
status: current
---

# TensorFlow 衔接与扩展

> 📖 Docs: [TensorFlow Ecosystem](https://www.tensorflow.org/resources/tools)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Python + NumPy | TF Tensor API 类似 NumPy | — |
| ← 前置 | 微分 | GradientTape 的数学基础 | [differentiation_map.md](../../math/differentiation/differentiation_map.md) |
| ← 前置 | DL 基础 (MLP/CNN) | TF 实现的模型架构 | [mlp](../mlp/), [cnn](../cnn/) |
| ← 前置 | PyTorch | 竞品对标，API 设计互相影响 | [pytorch](../pytorch/) |
| → 后续 | TF Serving | 服务端部署 | — |
| → 后续 | TF Lite | 移动端/嵌入式 | — |
| → 后续 | TF.js | 浏览器 AI | — |
| → 后续 | TFX | 端到端 MLOps | — |
| → 后续 | JAX | Google 下一代 DL 框架 | — |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在 TF 中如何使用 |
|---------|-----------|-----------------|
| NumPy | ndarray、广播 | `tf.Tensor` 设计灵感；`tensor.numpy()` 互转 |
| 微分 | 链式法则、自动微分 | `tf.GradientTape` 实现反向模式 AD |
| 线性代数 | 矩阵乘法 | `tf.matmul`、`Dense` 层核心运算 |
| MLP/CNN | 全连接、卷积 | `tf.keras.layers.Dense/Conv2D` |

---

## 下游影响

| 去向主题 | TF 提供的概念 | 在下游如何使用 |
|---------|-------------|-------------|
| TF Serving | SavedModel | REST/gRPC API 部署 |
| TF Lite | TFLiteConverter | 量化+优化→移动端推理 |
| TF.js | tfjs-converter | 浏览器端 DL |
| TFX | Pipeline 组件 | 端到端 ML 工作流（数据验证→训练→部署） |
| TF Hub | 预训练模型 | 迁移学习 |
| Keras 3.0 | 高级 API | 多后端（TF/PT/JAX）统一入口 |

---

## 概念演变追踪

| 概念 | TF 1.x | TF 2.x | 变化 |
|------|--------|--------|------|
| 执行模式 | 静态图 + Session | Eager 默认 + @tf.function | 从"先定义后执行"到"逐行执行" |
| 高级 API | tf.layers / tf.estimator / Keras | tf.keras（唯一） | 终结 API 碎片化 |
| 数据输入 | feed_dict / tf.queue | tf.data.Dataset | 高效流水线化 |
| 变量管理 | tf.get_variable / variable_scope | tf.Variable（简化） | 消除命名空间复杂性 |
| 模型保存 | checkpoint(.ckpt) + GraphDef(.pb) | SavedModel（统一） | 一个格式支持所有部署 |
| 分布式 | tf.train.ClusterSpec（手动） | tf.distribute.Strategy（自动） | 3 行代码多 GPU |

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [《Deep Learning》Ch.6,8](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | TF 模型的数学基础 | ⭐⭐⭐ |
| [TF 源码](../../../.github/tensorflow/) | 💻 源码 | 理解底层实现 | ⭐⭐⭐⭐⭐ |
| [Keras 源码](../../../.github/keras/) | 💻 源码 | Layer/Model 设计 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| PyTorch 知识库 [pytorch](../pytorch/) | TF vs PT 全面对比 | 框架选择时 |
| sklearn 知识库 [scikit_learn](../../ml/scikit_learn/) | 传统 ML vs DL 框架 | 决定是否需要 DL 时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| DL 架构 | 3 | [mlp](../mlp/), [cnn](../cnn/), [conv_layer](../conv_layer/) | TF/Keras 实现这些架构 |
| DL 框架 | 1 | [pytorch](../pytorch/) | 竞品对标 |
| DL 概念 | 2 | [tensor](../tensor/), [vanishing_gradient](../vanishing_gradient/) | TF 的基本数据类型 / 训练问题 |
| 数学基础 | 1 | [differentiation](../../math/differentiation/) | GradientTape 的数学基础 |
| ML 框架 | 1 | [scikit_learn](../../ml/scikit_learn/) | 传统 ML vs DL 框架 |
