---
topic: forward_propagation
dimension: map
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow, Bengio & Courville, Deep Learning, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Rumelhart, Hinton & Williams, 'Learning representations by back-propagating errors', Nature 1986 — https://doi.org/10.1038/323533a0"
  - "📖 Docs: PyTorch nn.Module — https://pytorch.org/docs/stable/generated/torch.nn.Module.html"
expiry: 12m
status: current
---

# Forward Propagation 知识地图

> 📚 Book: Goodfellow, Bengio & Courville, [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 "Deep Feedforward Networks"
> 📖 Paper: Rumelhart, Hinton & Williams, [Learning representations by back-propagating errors](https://doi.org/10.1038/323533a0), Nature 1986

## 1. 核心问题

- **前向传播到底在做什么？** → 把输入数据从第一层逐层变换到输出层，每一层做一次"线性变换 + 非线性激活"，最终产生预测结果
- **为什么不能一步直接算出结果？** → 单层线性变换只能表达线性函数；多层叠加 + 非线性激活才能逼近任意连续函数（通用近似定理）
- **前向传播和反向传播是什么关系？** → 前向传播计算输出和损失值，反向传播利用前向传播保存的中间结果计算梯度
- **矩阵乘法在前向传播中的角色是什么？** → 权重矩阵左乘输入向量实现仿射变换，这是每层计算的核心运算

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1-6.3

---

## 2. 全景位置

    深度学习 Deep Learning
    ├── 张量与计算 (数据表示)
    ├── 神经网络基础 ← 你在这里
    │   ├── 【Forward Propagation】 (输入→输出的计算流)
    │   ├── 激活函数 (引入非线性)
    │   ├── 损失函数 (衡量预测误差)
    │   └── 反向传播 (计算梯度)
    ├── 优化器 (更新权重)
    ├── 正则化 (防止过拟合)
    ├── CNN / RNN / Transformer (网络架构)
    └── 框架工具 (PyTorch/TensorFlow)

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 "Deep Feedforward Networks"

---

## 3. 依赖地图

    前置知识                 本主题                   后续方向
    ┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────┐
    │ 矩阵乘法        │────→│                  │────→│ 反向传播             │
    │ 激活函数        │────→│  Forward          │────→│ 计算图构建           │
    │ 全连接层        │────→│  Propagation      │────→│ 模型推理/部署        │
    │ 张量/向量       │────→│                  │────→│ 特征可视化           │
    └─────────────────┘     └──────────────────┘     └──────────────────────┘

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5 "Back-Propagation and Other Differentiation Algorithms"

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [forward_propagation_map.md](forward_propagation_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [forward_propagation_concepts.md](forward_propagation_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [forward_propagation_math.md](forward_propagation_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [forward_propagation_tutorial.md](forward_propagation_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [forward_propagation_code.md](forward_propagation_code.md) | ⑤ 代码 | 快速上手实现 |
| [forward_propagation_pitfalls.md](forward_propagation_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [forward_propagation_history.md](forward_propagation_history.md) | ⑦ 历史 | 了解技术演进 |
| [forward_propagation_bridge.md](forward_propagation_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [forward_propagation_first_principles.md](forward_propagation_first_principles.md) | ⑨ 第一性原理 | 追问底层公理、理解边界 |

> 📚 Book: Norman, [《The Design of Everyday Things》](../../../textbooks/norman_design_everyday_things.pdf), Ch.3 "Knowledge in the World"

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [forward_propagation_map.md](forward_propagation_map.md) 了解全局位置
2. 读 [forward_propagation_tutorial.md](forward_propagation_tutorial.md) Section 1 理解动机
3. 读 [forward_propagation_concepts.md](forward_propagation_concepts.md) 掌握核心术语
4. 读 [forward_propagation_math.md](forward_propagation_math.md) 手算一次核心公式
5. 跟 [forward_propagation_code.md](forward_propagation_code.md) 快速开始跑一个示例
6. 读 [forward_propagation_history.md](forward_propagation_history.md) 了解技术演进
7. 读 [forward_propagation_first_principles.md](forward_propagation_first_principles.md) 追问底层公理

### 日常参考 🔧

1. 查 [forward_propagation_code.md](forward_propagation_code.md) API 速查表
2. 查 [forward_propagation_math.md](forward_propagation_math.md) 公式速查
3. 查 [forward_propagation_pitfalls.md](forward_propagation_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [forward_propagation_history.md](forward_propagation_history.md) 完整演进线
2. 读 [forward_propagation_first_principles.md](forward_propagation_first_principles.md) 追问底层公理
3. 读 [forward_propagation_bridge.md](forward_propagation_bridge.md) 探索下游任务
4. 阅读原始论文

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
| Map | 2026-03-23 | 12m | ✅ current |
| Concepts | 2026-03-23 | 12m | ✅ current |
| Math | 2026-03-23 | 12m | ✅ current |
| Tutorial | 2026-03-23 | 12m | ✅ current |
| Code | 2026-03-23 | 6m | ✅ current |
| Pitfalls | 2026-03-23 | 6m | ✅ current |
| History | 2026-03-23 | never | ✅ current |
| Bridge | 2026-03-23 | 12m | ✅ current |
| First Principles | 2026-03-23 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考 |
| [Rumelhart et al. 1986](https://doi.org/10.1038/323533a0) | 📖 论文 | 历史演进、公式推导 |
| [PyTorch nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html) | 📖 文档 | 代码参考 |
| [PyTorch nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html) | 📖 文档 | 代码参考 |
