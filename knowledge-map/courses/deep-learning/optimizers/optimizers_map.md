---
topic: optimizers
dimension: map
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, 'PML1' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: Keras Optimizers — https://keras.io/api/optimizers/"
  - "📖 Docs: scikit-learn MLPClassifier solver — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
expiry: 12m
status: current
---

# Optimizers 知识地图

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.8

## 1. 核心问题

- **什么是优化器？** → 根据损失函数的梯度更新网络权重的算法，是训练神经网络的"引擎"
- **主要有哪些优化器？** → SGD, Momentum SGD, RMSprop, Adam, AdaGrad, L-BFGS
- **Adam 为什么是默认选择？** → 结合了 Momentum（动量）和 RMSprop（自适应学习率），对超参数不敏感
- **学习率为什么关键？** → 太大→震荡/发散，太小→收敛慢/卡在局部最优
- **compile 中 optimizer 参数的作用？** → 告诉 Keras 用哪种算法、以什么配置来更新权重

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 2. 全景位置

```
深度学习 (Deep Learning)
├── 网络架构 (Architecture)
│   ├── MLP / CNN / RNN / Transformer
├── 网络组件 (Components)
│   ├── Activation Functions / Dense / Conv / ...
├── 训练过程 (Training) ← 你在这里
│   ├── 【Optimizers】 (权重更新策略)
│   ├── Loss Functions (损失函数)
│   ├── Backpropagation (梯度计算)
│   ├── Learning Rate Schedules (学习率调度)
│   └── Regularization (正则化)
└── 框架工具 (Frameworks)
    ├── Keras: model.compile(optimizer=...)
    ├── PyTorch: torch.optim.Adam(...)
    └── Scikit-Learn: MLPClassifier(solver=...)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 3. 依赖地图

```
前置知识                       本主题                         后续方向
┌───────────────────────┐    ┌────────────────────┐    ┌─────────────────────────┐
│ 微积分 (梯度/偏导数)  │───→│                    │───→│ 学习率调度策略           │
│ 线性代数 (向量运算)   │───→│    Optimizers      │───→│ 模型训练流程 (fit)       │
│ 反向传播 (链式法则)   │───→│                    │───→│ 超参数调优               │
│ 损失函数 (Loss)       │───→│                    │───→│ 分布式训练               │
└───────────────────────┘    └────────────────────┘    └─────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [optimizers_map.md](optimizers_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [optimizers_concepts.md](optimizers_concepts.md) | ② 概念 | 理解各优化器定义、辨析区别 |
| [optimizers_math.md](optimizers_math.md) | ③ 公式 | 推导更新规则、理解动量和自适应学习率 |
| [optimizers_tutorial.md](optimizers_tutorial.md) | ④ 教程 | Why-First 理解优化器设计动机 |
| [optimizers_code.md](optimizers_code.md) | ⑤ 代码 | 快速上手各框架的优化器 API |
| [optimizers_pitfalls.md](optimizers_pitfalls.md) | ⑥ 踩坑 | 调试训练问题（不收敛、震荡等） |
| [optimizers_history.md](optimizers_history.md) | ⑦ 历史 | 从 SGD 到 Adam 的演进 |
| [optimizers_bridge.md](optimizers_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [optimizers_first_principles.md](optimizers_first_principles.md) | ⑨ 第一性原理 | 从公理推导为什么需要自适应优化 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [optimizers_map.md](optimizers_map.md) 了解全局位置
2. 读 [optimizers_tutorial.md](optimizers_tutorial.md) Section 1 理解为什么需要优化器
3. 读 [optimizers_concepts.md](optimizers_concepts.md) 掌握 SGD/Momentum/Adam 核心术语
4. 读 [optimizers_math.md](optimizers_math.md) 手算一次 SGD 和 Adam 的更新步骤
5. 跟 [optimizers_code.md](optimizers_code.md) 在 Keras/sklearn 中使用不同 optimizer
6. 读 [optimizers_history.md](optimizers_history.md) 了解从 SGD → Adam 的演进

### 日常参考 🔧

1. 查 [optimizers_code.md](optimizers_code.md) API 速查表
2. 查 [optimizers_math.md](optimizers_math.md) 公式速查
3. 查 [optimizers_pitfalls.md](optimizers_pitfalls.md) 排查训练问题

### 深度研究 🔬

1. 读 [optimizers_first_principles.md](optimizers_first_principles.md) 理解优化的数学基础
2. 读 [optimizers_history.md](optimizers_history.md) 完整演进线
3. 读 [optimizers_bridge.md](optimizers_bridge.md) 探索学习率调度和二阶方法
4. 阅读原始论文 (Kingma & Ba 2015 Adam, Ruder 2016 overview)

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
| Map | 2026-03-15 | 12m | ✅ current |
| Concepts | 2026-03-15 | 12m | ✅ current |
| Math | 2026-03-15 | 12m | ✅ current |
| Tutorial | 2026-03-15 | 12m | ✅ current |
| Code | 2026-03-15 | 6m | ✅ current |
| Pitfalls | 2026-03-15 | 6m | ✅ current |
| History | 2026-03-15 | never | ✅ current |
| Bridge | 2026-03-15 | 12m | ✅ current |
| First Principles | 2026-03-15 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.8](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考，Optimization for Training Deep Models |
| [《PRML》Ch.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 梯度下降基础 |
| [《PML1》Ch.8](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | Optimization Algorithms |
| [Keras Optimizers](https://keras.io/api/optimizers/) | 📖 文档 | API 参考 |
| [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html) | 📖 文档 | solver 参数 |
| Kingma & Ba, ICLR 2015 | 📖 论文 | Adam 优化器 |
| Ruder, arXiv 2016 | 📖 论文 | 梯度下降优化方法综述 |
| Duchi et al., JMLR 2011 | 📖 论文 | AdaGrad |
| Tieleman & Hinton, Coursera 2012 | 📖 论文 | RMSprop |
