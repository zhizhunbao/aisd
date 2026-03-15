---
topic: keras
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Chollet, 'Keras', 2015 — https://arxiv.org/abs/1508.01211"
  - "📖 Docs: Keras 3 Official Documentation — https://keras.io/api/"
  - "💻 Source: keras/keras GitHub — https://github.com/keras-team/keras"
  - "💻 Source: keras-io GitHub — https://github.com/keras-team/keras-io"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.11 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 6m
status: current
---

# Keras 知识地图

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015
> 📖 Docs: [Keras 3 Official](https://keras.io/api/)
> 💻 Source: [keras](../../.github/keras/) | [keras-io](../../.github/keras-io/)

---

## 1. 核心问题

- **Keras 是什么？** → 一个多后端深度学习高层 API，可在 JAX/TensorFlow/PyTorch/OpenVINO 上运行
- **为什么不直接用 PyTorch/TF？** → Keras 提供统一接口 + 极简 API + 后端可切换，降低认知负荷和代码迁移成本
- **Keras 3 vs tf.keras？** → Keras 3 是独立包（`pip install keras`），解耦了 TensorFlow 依赖，支持多后端
- **三种建模方式？** → Sequential（线性堆叠）、Functional API（DAG 图）、Subclassing（完全自定义）
- **如何训练模型？** → `compile()` 配置 → `fit()` 训练 → `evaluate()` 评估 → `predict()` 推理

> 📖 Docs: [Keras 3 Overview](https://keras.io/getting_started/)
> 💻 Source: [keras](../../.github/keras/) `keras/src/models/model.py`

---

## 2. 全景位置

```
深度学习生态
├── 底层计算引擎
│   ├── JAX (Google, 函数式 + JIT)
│   ├── TensorFlow (Google, 工业部署)
│   ├── PyTorch (Meta, 研究灵活)
│   └── OpenVINO (Intel, 推理优化)
├── 高层 API 框架 ← 你在这里
│   ├── 【Keras 3】 (多后端统一 API, 极简设计)
│   ├── PyTorch Lightning (PyTorch 的高层封装)
│   ├── Hugging Face Transformers (NLP/多模态专用)
│   └── FastAI (教学友好, PyTorch 封装)
├── 模型库 / Hub
│   ├── Keras Hub (Keras 生态预训练模型)
│   ├── TF Hub / torch.hub
│   └── Hugging Face Hub
└── 部署工具
    ├── TF Serving / TF Lite / LiteRT
    ├── TorchServe / ONNX Runtime
    └── Keras Export (SavedModel/ONNX/OpenVINO/LiteRT)
```

> 📖 Docs: [Keras 3 About](https://keras.io/about/)
> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015

---

## 3. 依赖地图

```
前置知识                    本主题                    后续方向
┌─────────────────────┐    ┌──────────────────┐    ┌──────────────────────────┐
│ Python 基础          │───→│                  │───→│ Keras Hub 预训练模型      │
│ 张量 / NumPy         │───→│                  │───→│ 自定义训练循环             │
│ 神经网络基础 (MLP)   │───→│     Keras 3      │───→│ 分布式训练                │
│ 损失函数 / 优化器    │───→│                  │───→│ 量化 / 剪枝 / 部署        │
│ 至少一个后端基础     │───→│                  │───→│ 模型导出 (ONNX/SavedModel)│
└─────────────────────┘    └──────────────────┘    └──────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../textbooks/goodfellow_deep_learning.pdf), Ch.11
> 📖 Docs: [Keras 3 Getting Started](https://keras.io/getting_started/)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [keras_map.md](keras_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [keras_concepts.md](keras_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| ~~keras_math.md~~ | ~~③ 公式~~ | ~~不适用~~ — Keras 是工程框架，无数学公式 |
| [keras_tutorial.md](keras_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [keras_code.md](keras_code.md) | ⑤ 代码 | 快速上手实现 |
| [keras_pitfalls.md](keras_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [keras_history.md](keras_history.md) | ⑦ 历史 | 了解技术演进 |
| [keras_bridge.md](keras_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [keras_first_principles.md](keras_first_principles.md) | ⑨ 第一性原理 | 理解 Keras 设计哲学的根基 |

> 📖 Docs: [Keras 3 API Reference](https://keras.io/api/)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [keras_map.md](keras_map.md) 了解全局位置
2. 读 [keras_tutorial.md](keras_tutorial.md) Section 1 理解动机
3. 读 [keras_concepts.md](keras_concepts.md) 掌握核心术语
4. 跟 [keras_code.md](keras_code.md) 快速开始跑一个 MNIST 示例
5. 读 [keras_history.md](keras_history.md) 了解从 Keras 1 到 Keras 3 的演进
6. 读 [keras_first_principles.md](keras_first_principles.md) 理解设计哲学

### 日常参考 🔧

1. 查 [keras_code.md](keras_code.md) API 速查表
2. 查 [keras_pitfalls.md](keras_pitfalls.md) 排查问题
3. 查 [Keras 官方文档](https://keras.io/api/) 最新 API

### 深度研究 🔬

1. 读 [keras_history.md](keras_history.md) 完整演进线
2. 读 [keras_bridge.md](keras_bridge.md) 探索下游任务
3. 阅读 Keras 源码 `.github/keras/` 理解内部实现

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ~~不适用~~ |
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
| Math | — | — | ~~不适用~~ |
| Tutorial | 2026-03-14 | 6m | ✅ current |
| Code | 2026-03-14 | 3m | ✅ current |
| Pitfalls | 2026-03-14 | 3m | ✅ current |
| History | 2026-03-14 | never | ✅ current |
| Bridge | 2026-03-14 | 6m | ✅ current |
| First Principles | 2026-03-14 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Chollet, Keras 2015](https://arxiv.org/abs/1508.01211) | 📖 论文 | 历史、设计哲学 |
| [Keras 3 Official Docs](https://keras.io/api/) | 📖 文档 | 全文核心参考 |
| [《Deep Learning》Ch.11](../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 背景知识 |
| [keras GitHub](../../.github/keras/) | 💻 源码 | 代码实现参考 |
| [keras-io GitHub](../../.github/keras-io/) | 💻 源码 | 文档和示例参考 |
