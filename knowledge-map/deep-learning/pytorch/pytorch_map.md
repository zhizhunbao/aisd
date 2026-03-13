---
topic: pytorch
dimension: map
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Docs: [PyTorch Documentation](https://pytorch.org/docs/stable/) — v2.10"
  - "📖 Paper: [Paszke et al. 2019](https://arxiv.org/abs/1912.01703)"
  - "📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf)"
expiry: 6m
status: current
---

# PyTorch 知识地图

> 📖 Docs: [PyTorch Official Documentation](https://pytorch.org/docs/stable/) — v2.10
> 📖 Paper: Paszke et al., [PyTorch: An Imperative Style, High-Performance Deep Learning Library](https://arxiv.org/abs/1912.01703), NeurIPS 2019

---

## 1. 核心问题

- **PyTorch 是什么？** → 基于 Python 的开源深度学习框架，提供张量计算（GPU 加速）和自动微分两大核心能力，以**命令式（Imperative / Eager mode）**编程风格著称。
- **PyTorch 和 TensorFlow 最本质的区别？** → PyTorch 默认动态计算图（define-by-run），TensorFlow 1.x 是静态图（define-and-run）；TF2 也默认 Eager mode 但底层仍有静态图优化。
- **Autograd 如何实现自动求导？** → 前向传播时动态构建 DAG 计算图，反向传播时沿图应用链式法则自动计算梯度。
- **`torch.nn` 和 `torch.Tensor` 是什么关系？** → `Tensor` 是基本数据结构（多维数组 + 梯度追踪），`nn.Module` 是神经网络层的抽象，内部持有 `Parameter`（可训练的 Tensor）。
- **什么时候用 PyTorch？** → 研究原型（灵活性高）、需要自定义训练循环、动态网络结构（如 NLP/RL 中变长输入）。

> 📖 Docs: [PyTorch Documentation](https://pytorch.org/docs/stable/)
> 📖 Paper: Paszke et al., [NeurIPS 2019](https://arxiv.org/abs/1912.01703)

---

## 2. 全景位置

```
科学计算 & 深度学习生态
├── 数值计算库
│   ├── NumPy（CPU 多维数组）
│   └── CuPy（GPU 加速 NumPy）
├── 深度学习框架
│   ├── 【你在这里 → PyTorch】
│   │   ├── torch（张量 + 自动微分）
│   │   ├── torch.nn（神经网络模块）
│   │   ├── torch.optim（优化器）
│   │   ├── torch.utils.data（数据加载）
│   │   ├── torchvision / torchaudio / torchtext
│   │   └── torch.distributed（分布式训练）
│   ├── TensorFlow / Keras
│   ├── JAX（函数式 + XLA 编译）
│   └── MXNet / PaddlePaddle
├── 高层框架
│   ├── PyTorch Lightning（训练工程化）
│   ├── Hugging Face Transformers
│   └── fastai
└── 部署 & 推理
    ├── TorchScript / torch.export
    ├── ONNX Runtime
    └── TensorRT
```

> 📖 Docs: [PyTorch Ecosystem](https://pytorch.org/ecosystem/)

---

## 3. 依赖地图

```
前置知识                    本主题                      后续方向
┌──────────────────────┐    ┌───────────────┐    ┌───────────────────────┐
│ Python 基础           │───→│               │───→│ torchvision / CV      │
│ NumPy 多维数组        │───→│               │───→│ torchaudio / NLP      │
│ 线性代数基础          │───→│   PyTorch     │───→│ PyTorch Lightning     │
│ 微积分（链式法则）    │───→│               │───→│ Hugging Face          │
│ 概率统计基础          │───→│               │───→│ 分布式训练            │
│ GPU 计算概念(可选)    │───→│               │───→│ 模型部署 (ONNX/TRT)   │
└──────────────────────┘    └───────────────┘    └───────────────────────┘
```

> 📖 Docs: [Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [pytorch_map.md](pytorch_map.md) | 导航地图 | 第一次接触，需要全景概览 |
| [pytorch_concepts.md](pytorch_concepts.md) | 核心概念 | 查术语定义、辨析混淆概念 |
| [pytorch_math.md](pytorch_math.md) | 数学公式 | 理解自动微分、反向传播数学原理 |
| [pytorch_tutorial.md](pytorch_tutorial.md) | 教程 | 系统学习 Why + How |
| [pytorch_code.md](pytorch_code.md) | 代码参考 | 查代码模板、快速上手 |
| [pytorch_pitfalls.md](pytorch_pitfalls.md) | 踩坑记录 | Debug 时查常见问题 |
| [pytorch_history.md](pytorch_history.md) | 历史演进 | 了解技术演进脉络 |
| [pytorch_bridge.md](pytorch_bridge.md) | 跨主题衔接 | 找相关主题、扩展阅读 |

---

## 5. 学习/使用路线

### 第一次学习 🎒
1. 读 [pytorch_concepts.md](pytorch_concepts.md) — 建立术语体系
2. 读 [pytorch_tutorial.md](pytorch_tutorial.md) — 理解 Why + How
3. 跑 [pytorch_code.md](pytorch_code.md) 的快速开始 — 30 秒上手
4. 读 [pytorch_math.md](pytorch_math.md) — 理解自动微分原理
5. 浏览 [pytorch_pitfalls.md](pytorch_pitfalls.md) — 提前避坑

### 日常参考 🔧
1. 查 [pytorch_code.md](pytorch_code.md) API 速查表
2. 遇到 Bug 查 [pytorch_pitfalls.md](pytorch_pitfalls.md)
3. 查术语回 [pytorch_concepts.md](pytorch_concepts.md)

### 深度研究 🔬
1. 读 [pytorch_history.md](pytorch_history.md) — 理解设计哲学演进
2. 读 [pytorch_bridge.md](pytorch_bridge.md) — 横向对比与扩展
3. 读原论文 [Paszke et al. 2019](https://arxiv.org/abs/1912.01703)

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

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-12 | 2026-09-12 | ✅ current |
| Concepts | 2026-03-12 | 2026-09-12 | ✅ current |
| Math | 2026-03-12 | 2027-03-12 | ✅ current |
| Tutorial | 2026-03-12 | 2026-09-12 | ✅ current |
| Code | 2026-03-12 | 2026-09-12 | ✅ current |
| Pitfalls | 2026-03-12 | 2026-09-12 | ✅ current |
| History | 2026-03-12 | 2027-03-12 | ✅ current |
| Bridge | 2026-03-12 | 2026-09-12 | ✅ current |
