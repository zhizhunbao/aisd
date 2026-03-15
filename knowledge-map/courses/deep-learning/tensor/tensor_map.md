---
topic: tensor
dimension: map
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.3"
  - "📖 Docs: [PyTorch Tensor](https://pytorch.org/docs/stable/tensors.html)"
  - "📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)"
expiry: 12m
status: current
---

# Tensor 知识地图

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3
> 📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)

## 1. 核心问题

- **Tensor 到底是什么？** → 多维数组（n-dimensional array），是深度学习中数据和参数的统一表示形式。
- **Tensor 和 NumPy ndarray 有什么不同？** → Tensor 支持 GPU 加速、自动微分（autograd），并能与 ndarray 共享内存。
- **Tensor 的三大属性是什么？** → `shape`（维度形状）、`dtype`（数据类型）、`device`（存储设备 CPU/GPU）。
- **为什么深度学习需要 Tensor？** → Tensor 将标量、向量、矩阵统一为一种数据结构，使得批量数据处理和 GPU 并行计算成为可能。
- **Tensor 和数学中的张量是什么关系？** → 深度学习的 Tensor 借用了数学张量的名字，但更接近于"多维数组"的工程抽象，而非严格的张量分析。

> 📖 Docs: [PyTorch Tensor Tutorial](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

---

## 2. 全景位置

```
深度学习技术栈
├── 数据表示
│   ├── 标量 (Scalar)
│   ├── 向量 (Vector)
│   ├── 矩阵 (Matrix)
│   └── 【你在这里】Tensor（多维数组）
├── 计算引擎
│   ├── Autograd（自动微分）
│   └── GPU 加速（CUDA）
├── 神经网络构建
│   ├── nn.Module
│   ├── Layers（Linear, Conv2d...）
│   └── Loss Functions
└── 训练循环
    ├── Optimizer
    ├── DataLoader
    └── Train/Eval Loop
```

> 📖 Docs: [PyTorch Tensor](https://pytorch.org/docs/stable/tensors.html)

---

## 3. 依赖地图

```
前置知识                 本主题                 后续方向
─────────              ──────                ──────────
Python 基础 ─────────→                    ┌→ Autograd（自动微分）
NumPy ndarray ───────→   Tensor           ├→ nn.Module（模型构建）
线性代数基础 ────────→  （多维数组）       ├→ DataLoader（数据管道）
                                          ├→ GPU 并行计算
                                          └→ 模型训练与推理
```

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.3

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [tensor_map.md](tensor_map.md) | ① 导航 | 初次了解 Tensor 全貌 |
| [tensor_concepts.md](tensor_concepts.md) | ② 概念 | 查术语定义、辨析对比 |
| [tensor_math.md](tensor_math.md) | ③ 公式 | 理解 Tensor 运算的数学基础 |
| [tensor_tutorial.md](tensor_tutorial.md) | ④ 教程 | Why-First 系统学习 |
| [tensor_code.md](tensor_code.md) | ⑤ 代码 | 可运行示例、API 速查 |
| [tensor_pitfalls.md](tensor_pitfalls.md) | ⑥ 踩坑 | 排查常见问题 |
| [tensor_history.md](tensor_history.md) | ⑦ 历史 | 了解 Tensor 的演进脉络 |
| [tensor_bridge.md](tensor_bridge.md) | ⑧ 衔接 | 与 PyTorch/Autograd 等主题关联 |

> 📖 Docs: [PyTorch Tensor](https://pytorch.org/docs/stable/tensors.html)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 阅读 [tensor_concepts.md](tensor_concepts.md) — 搞清楚术语
2. 阅读 [tensor_tutorial.md](tensor_tutorial.md) — 理解为什么需要 Tensor
3. 动手跑 [tensor_code.md](tensor_code.md) — 30 秒跑起来
4. 浏览 [tensor_math.md](tensor_math.md) — 了解运算背后的数学

### 日常参考 🔧

1. 查 [tensor_code.md](tensor_code.md) API 速查表
2. 查 [tensor_pitfalls.md](tensor_pitfalls.md) 排错清单
3. 查 [tensor_concepts.md](tensor_concepts.md) 速查表

### 深度研究 🔬

1. 阅读 [tensor_history.md](tensor_history.md) — 张量的演进故事
2. 阅读 [tensor_math.md](tensor_math.md) — 完整推导
3. 查 [tensor_bridge.md](tensor_bridge.md) — 探索上下游主题

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| ① Map | ✅ 完成 |
| ② Concepts | ✅ 完成 |
| ③ Math | ✅ 完成 |
| ④ Tutorial | ✅ 完成 |
| ⑤ Code | ✅ 完成 |
| ⑥ Pitfalls | ✅ 完成 |
| ⑦ History | ✅ 完成 |
| ⑧ Bridge | ✅ 完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-12 | 12m | ✅ current |
| Concepts | 2026-03-12 | 12m | ✅ current |
| Math | 2026-03-12 | 12m | ✅ current |
| Tutorial | 2026-03-12 | 12m | ✅ current |
| Code | 2026-03-12 | 6m | ✅ current |
| Pitfalls | 2026-03-12 | 6m | ✅ current |
| History | 2026-03-12 | never | ✅ current |
| Bridge | 2026-03-12 | 6m | ✅ current |
