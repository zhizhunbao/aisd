---
topic: differentiation
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.4,6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML, Ch.4-5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Boyd & Vandenberghe, Convex Optimization, Ch.2-3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/boyd_convex_optimization.pdf"
  - "📖 Docs: PyTorch Autograd — https://pytorch.org/docs/stable/autograd.html"
expiry: 12m
status: current
---

# 微分 知识地图

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

## 1. 核心问题

- **微分的本质是什么？** → 测量函数在某一点的"瞬时变化率"；几何上是切线斜率，代数上是极限 $\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$
- **为什么 ML 必须用微分？** → 梯度下降是训练模型的核心：$\theta \leftarrow \theta - \eta \nabla_\theta L$，没有微分就无法计算梯度
- **偏导数、梯度、Jacobian、Hessian 有什么关系？** → 偏导数是多元函数对一个变量的导数；梯度是所有偏导组成的向量；Jacobian 是向量函数的梯度矩阵；Hessian 是二阶偏导矩阵
- **链式法则为什么是反向传播的数学基础？** → 深度网络是复合函数 $f \circ g \circ h$，链式法则让我们能逐层计算梯度
- **自动微分 vs 数值微分 vs 符号微分？** → 自动微分（PyTorch/JAX）精确且高效；数值微分简单但有舍入误差；符号微分精确但表达式膨胀

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---

## 2. 全景位置

```
数学基础 (Mathematics Foundations)
├── 线性代数 (Linear Algebra)
│   ├── 向量与矩阵
│   └── 特征分解 / SVD
├── 微积分 (Calculus) ← 你在这里
│   ├── 【微分】 (瞬时变化率, 梯度, 链式法则 — ML 训练的数学引擎)
│   ├── 积分与求和 (微分的逆运算)
│   └── 卷积 (积分的特殊应用)
├── 概率论 (Probability)
│   ├── 概率分布
│   ├── 期望 / 方差
│   └── 贝叶斯推断
└── 优化 (Optimization)
    ├── 梯度下降 (依赖微分!)
    └── 凸优化 (Hessian → 凸性判定)
```

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Table of Contents

---

## 3. 依赖地图

```
前置知识                      本主题                      后续方向
┌───────────────────┐    ┌────────────────────┐    ┌─────────────────────────┐
│ 函数 (Function)   │───→│                    │───→│ 梯度下降 (Gradient      │
│ 极限 (Limit)      │───→│     微分            │───→│   Descent)              │
│ 线性代数 (向量/   │───→│  Differentiation   │───→│ 反向传播 (Backprop)     │
│   矩阵)           │───→│                    │───→│ 优化 (Newton / LBFGS)   │
│                   │    │                    │───→│ 积分 (逆运算)           │
└───────────────────┘    └────────────────────┘    └─────────────────────────┘
```

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [differentiation_map.md](differentiation_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [differentiation_concepts.md](differentiation_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [differentiation_math.md](differentiation_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [differentiation_tutorial.md](differentiation_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [differentiation_code.md](differentiation_code.md) | ⑤ 代码 | 快速上手实现 |
| [differentiation_pitfalls.md](differentiation_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [differentiation_history.md](differentiation_history.md) | ⑦ 历史 | 了解技术演进 |
| [differentiation_bridge.md](differentiation_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [differentiation_first_principles.md](differentiation_first_principles.md) | ⑨ 第一性原理 | 从公理推导微分为什么必须如此 |

> 📚 Book: 本文件汇总

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [differentiation_map.md](differentiation_map.md) 了解全局位置
2. 读 [differentiation_tutorial.md](differentiation_tutorial.md) Section 1 理解动机
3. 读 [differentiation_concepts.md](differentiation_concepts.md) 掌握核心术语
4. 读 [differentiation_math.md](differentiation_math.md) 手算一次核心公式
5. 跟 [differentiation_code.md](differentiation_code.md) 快速开始跑一个示例
6. 读 [differentiation_history.md](differentiation_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [differentiation_code.md](differentiation_code.md) API 速查表
2. 查 [differentiation_math.md](differentiation_math.md) 公式速查
3. 查 [differentiation_pitfalls.md](differentiation_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [differentiation_history.md](differentiation_history.md) 完整演进线
2. 读 [differentiation_bridge.md](differentiation_bridge.md) 探索下游任务
3. 读 [differentiation_first_principles.md](differentiation_first_principles.md) 从公理理解为什么

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
| Map | 2026-03-14 | 12m | ✅ current |
| Concepts | 2026-03-14 | 12m | ✅ current |
| Math | 2026-03-14 | 12m | ✅ current |
| Tutorial | 2026-03-14 | 12m | ✅ current |
| Code | 2026-03-14 | 6m | ✅ current |
| Pitfalls | 2026-03-14 | 6m | ✅ current |
| History | 2026-03-14 | never | ✅ current |
| Bridge | 2026-03-14 | 12m | ✅ current |
| First Principles | 2026-03-14 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《MML》Ch.5](../../../textbooks/deisenroth_mml.pdf) | 📚 教科书 | 全文核心参考（导数、偏导、梯度、Jacobian） |
| [《Deep Learning》Ch.4,6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 反向传播、计算图 |
| [《PRML》Ch.4-5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 梯度在分类/回归中的应用 |
| [《Convex Optimization》Ch.2-3](../../../textbooks/boyd_convex_optimization.pdf) | 📚 教科书 | Hessian、凸性、二阶方法 |
| [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html) | 📖 文档 | 自动微分 API |
| [JAX autodiff](https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html) | 📖 文档 | 函数式自动微分 |
