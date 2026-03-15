---
topic: tensorflow
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: TensorFlow Guide — https://www.tensorflow.org/guide"
  - "📖 Docs: Keras API — https://keras.io/api/"
  - "💻 Source: tensorflow/tensorflow — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/tensorflow"
  - "💻 Source: keras — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/keras"
  - "📚 Book: Goodfellow et al., Deep Learning — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# TensorFlow 知识地图

> 📖 Docs: [TensorFlow Guide](https://www.tensorflow.org/guide)
> 📖 Docs: [Keras API](https://keras.io/api/)

## 1. 核心问题

- **TensorFlow 在 DL 生态中扮演什么角色？** → Google 开源的端到端深度学习平台，覆盖训练→部署→移动端/服务端推理的全栈能力
- **TensorFlow vs Keras 是什么关系？** → Keras 是 TensorFlow 的高级 API（tf.keras），提供用户友好的模型构建接口；TF 提供底层计算引擎
- **TensorFlow vs PyTorch 怎么选？** → TF 强在部署生态（TF Serving/TF Lite/TF.js）和 TPU 支持；PyTorch 强在研究灵活性和动态图。TF 2.x 已采纳 Eager Execution 缩小差距
- **TensorFlow 的核心抽象是什么？** → Tensor（多维数组）+ 计算图（Graph）+ 自动微分（GradientTape）+ 分布式策略（tf.distribute）
- **什么时候不该用 TensorFlow？** → 传统 ML（用 sklearn）、小规模实验偏好灵活性（用 PyTorch）、纯 NumPy 科学计算（用 JAX）

> 📖 Docs: [TensorFlow Guide](https://www.tensorflow.org/guide)

---

## 2. 全景位置

```
Python DL/AI 生态
├── 数据处理
│   ├── NumPy / Pandas / SciPy
│   └── tf.data (TF 数据管线)
├── 传统 ML
│   └── Scikit-Learn
├── 深度学习框架 ← 你在这里
│   ├── 【TensorFlow / Keras】 (Google, 全栈: 训练+部署+移动端)
│   ├── PyTorch (Meta, 研究为主)
│   └── JAX (Google, 函数式+科学计算)
├── 模型库
│   ├── TensorFlow Hub / TF Model Garden
│   ├── Hugging Face Transformers
│   └── Keras Applications (预训练模型)
└── 部署
    ├── TF Serving (服务端推理)
    ├── TF Lite (移动/嵌入式)
    ├── TF.js (浏览器)
    └── ONNX / TorchServe (PyTorch 侧)
```

> 📖 Docs: [TensorFlow Ecosystem](https://www.tensorflow.org/resources/tools)

---

## 3. 依赖地图

```
前置知识                      本主题                       后续方向
┌───────────────────┐    ┌─────────────────────┐    ┌─────────────────────────┐
│ Python 基础       │───→│                     │───→│ TF Serving (部署)       │
│ NumPy             │───→│    TensorFlow       │───→│ TF Lite (移动端)        │
│ 线性代数 / 微积分 │───→│    + Keras           │───→│ TF.js (浏览器)          │
│ ML 基础 (sklearn) │───→│                     │───→│ TFX (端到端 MLOps)      │
│ DL 基础 (反向传播)│───→│                     │───→│ TPU 训练                │
└───────────────────┘    └─────────────────────┘    └─────────────────────────┘
```

> 📖 Docs: [TensorFlow Guide](https://www.tensorflow.org/guide)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [tensorflow_map.md](tensorflow_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [tensorflow_concepts.md](tensorflow_concepts.md) | ② 概念 | 理解 Tensor/Graph/Eager/Keras Layer 等 |
| [tensorflow_math.md](tensorflow_math.md) | ③ 公式 | TF 内部的数学运算与训练循环 |
| [tensorflow_tutorial.md](tensorflow_tutorial.md) | ④ 教程 | Why-First 理解 TF 的设计决策 |
| [tensorflow_code.md](tensorflow_code.md) | ⑤ 代码 | 快速上手实现 |
| [tensorflow_pitfalls.md](tensorflow_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [tensorflow_history.md](tensorflow_history.md) | ⑦ 历史 | 了解演进 |
| [tensorflow_bridge.md](tensorflow_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [tensorflow_first_principles.md](tensorflow_first_principles.md) | ⑨ 第一性原理 | 从计算图理论理解设计 |

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [tensorflow_map.md](tensorflow_map.md) 了解全局位置
2. 读 [tensorflow_tutorial.md](tensorflow_tutorial.md) Section 1 理解为什么选 TF
3. 读 [tensorflow_concepts.md](tensorflow_concepts.md) 掌握核心术语
4. 跟 [tensorflow_code.md](tensorflow_code.md) 跑一个完整示例
5. 读 [tensorflow_history.md](tensorflow_history.md) 了解 TF 1.x→2.x 演进

### 日常参考 🔧

1. 查 [tensorflow_code.md](tensorflow_code.md) API 速查表
2. 查 [tensorflow_pitfalls.md](tensorflow_pitfalls.md) 排查问题
3. 查 [tensorflow_math.md](tensorflow_math.md) 训练公式

### 深度研究 🔬

1. 读 [tensorflow_first_principles.md](tensorflow_first_principles.md)
2. 读 [tensorflow_bridge.md](tensorflow_bridge.md) 探索 TF Serving/TFX/TPU
3. 读源码 [tensorflow/](../../../.github/tensorflow/)

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-14 | 6m | ✅ current |
| Concepts | 2026-03-14 | 6m | ✅ current |
| Math | 2026-03-14 | 12m | ✅ current |
| Tutorial | 2026-03-14 | 6m | ✅ current |
| Code | 2026-03-14 | 3m | ✅ current |
| Pitfalls | 2026-03-14 | 6m | ✅ current |
| History | 2026-03-14 | never | ✅ current |
| Bridge | 2026-03-14 | 6m | ✅ current |
| First Principles | 2026-03-14 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [TensorFlow Guide](https://www.tensorflow.org/guide) | 📖 文档 | 全文核心 |
| [Keras API](https://keras.io/api/) | 📖 文档 | Code 维度 |
| [tensorflow 源码](../../../.github/tensorflow/) | 💻 源码 | Code + Tutorial |
| [keras 源码](../../../.github/keras/) | 💻 源码 | Code 层设计 |
| [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | Math + First Principles |
