---
topic: integration_summation
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5-6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Grinstead & Snell, Introduction to Probability, Ch.1-2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/grinstead_snell_probability.pdf"
  - "📚 Book: Bishop, PRML, Ch.1-2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: NumPy/SciPy Numerical Integration — https://docs.scipy.org/doc/scipy/reference/integrate.html"
expiry: 12m
status: current
---

# 积分与求和 知识地图

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5-6
> 📚 Book: Grinstead & Snell, [《Introduction to Probability》](../../../textbooks/grinstead_snell_probability.pdf), Ch.1-2

## 1. 核心问题

- **积分和求和的本质区别？** → 求和处理离散值的累加，积分处理连续函数在区间上的"面积"；积分是求和在连续极限下的推广
- **为什么 ML/DL 到处都要用积分？** → 概率分布的归一化、期望的计算、边缘化（marginalization）、损失函数的连续版本都依赖积分
- **求和在 ML 中扮演什么角色？** → 离散概率的期望、损失函数（如交叉熵）、级数展开（Taylor）、矩阵迹（trace）都是求和
- **遇到解析不可积怎么办？** → 数值积分（梯形法、Simpson 法）或蒙特卡洛近似（采样估计期望）
- **求和与积分可以交换顺序吗？** → 不总是可以；需要满足一致收敛或 Fubini 定理等条件

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1.2-1.3

---

## 2. 全景位置

```
数学基础 (Mathematics Foundations)
├── 线性代数 (Linear Algebra)
│   ├── 向量与矩阵
│   └── 特征分解 / SVD
├── 微积分 (Calculus) ← 你在这里
│   ├── 微分 (Differentiation)
│   ├── 【积分与求和】 (连续累加 + 离散累加，概率/期望/归一化的核心工具)
│   └── 卷积 (Convolution) — 积分的特殊应用
├── 概率论 (Probability)
│   ├── 概率分布 (积分→连续分布归一化)
│   ├── 期望 (积分/求和→E[f(x)])
│   └── 贝叶斯推断 (边缘化→高维积分)
└── 优化 (Optimization)
    ├── 梯度下降
    └── 凸优化
```

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Table of Contents

---

## 3. 依赖地图

```
前置知识                    本主题                      后续方向
┌──────────────────┐    ┌───────────────────┐    ┌──────────────────────────┐
│ 函数 (Function)  │───→│                   │───→│ 概率分布归一化           │
│ 极限 (Limit)     │───→│   积分与求和       │───→│ 期望计算 E[X]            │
│ 微分 (Derivative)│───→│ Integration &     │───→│ 贝叶斯边缘化             │
│ 级数 (Series)    │───→│ Summation         │───→│ 蒙特卡洛方法             │
│ 集合 (Set)       │───→│                   │───→│ 卷积 (Convolution)       │
└──────────────────┘    └───────────────────┘    └──────────────────────────┘
```

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [integration_summation_map.md](integration_summation_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [integration_summation_concepts.md](integration_summation_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [integration_summation_math.md](integration_summation_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [integration_summation_tutorial.md](integration_summation_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [integration_summation_code.md](integration_summation_code.md) | ⑤ 代码 | 快速上手实现 |
| [integration_summation_pitfalls.md](integration_summation_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [integration_summation_history.md](integration_summation_history.md) | ⑦ 历史 | 了解技术演进 |
| [integration_summation_bridge.md](integration_summation_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [integration_summation_first_principles.md](integration_summation_first_principles.md) | ⑨ 第一性原理 | 从公理推导积分为什么必须如此 |

> 📚 Book: 本文件汇总

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [integration_summation_map.md](integration_summation_map.md) 了解全局位置
2. 读 [integration_summation_tutorial.md](integration_summation_tutorial.md) Section 1 理解动机
3. 读 [integration_summation_concepts.md](integration_summation_concepts.md) 掌握核心术语
4. 读 [integration_summation_math.md](integration_summation_math.md) 手算一次核心公式
5. 跟 [integration_summation_code.md](integration_summation_code.md) 快速开始跑一个示例
6. 读 [integration_summation_history.md](integration_summation_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [integration_summation_code.md](integration_summation_code.md) API 速查表
2. 查 [integration_summation_math.md](integration_summation_math.md) 公式速查
3. 查 [integration_summation_pitfalls.md](integration_summation_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [integration_summation_history.md](integration_summation_history.md) 完整演进线
2. 读 [integration_summation_bridge.md](integration_summation_bridge.md) 探索下游任务
3. 读 [integration_summation_first_principles.md](integration_summation_first_principles.md) 从公理理解为什么

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
| [《MML》Ch.5-6](../../../textbooks/deisenroth_mml.pdf) | 📚 教科书 | 全文核心参考（积分定义、连续概率） |
| [《Probability》Ch.1-2](../../../textbooks/grinstead_snell_probability.pdf) | 📚 教科书 | 离散/连续期望、求和 |
| [《PRML》Ch.1-2](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 贝叶斯积分、边缘化 |
| [《Deep Learning》Ch.3](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | ML 中的积分应用 |
| [SciPy integrate](https://docs.scipy.org/doc/scipy/reference/integrate.html) | 📖 文档 | 数值积分 API |
| [NumPy sum/cumsum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html) | 📖 文档 | 求和 API |
