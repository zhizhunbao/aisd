---
topic: loss_functions
dimension: map
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 §6.2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.4, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, 'PML1' Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: Keras Losses — https://keras.io/api/losses/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
expiry: 12m
status: current
---

# Loss Functions 知识地图

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4

## 1. 核心问题

- **什么是损失函数？** → 衡量模型预测值与真实值之间差距的标量函数，训练目标就是最小化它
- **主要有哪些损失函数？** → MSE, MAE, Binary Cross-Entropy, Categorical Cross-Entropy, Sparse CCE, Hinge Loss
- **如何选择损失函数？** → 回归→MSE/MAE；二分类→Binary CE；多分类→Categorical CE；任务决定损失
- **损失函数和激活函数如何配对？** → Sigmoid+BCE, Softmax+CCE, Linear+MSE——配对错误会导致梯度异常
- **compile 中 loss 参数的作用？** → 告诉 Keras 用什么标准来评估预测质量，优化器根据它计算梯度

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2

---

## 2. 全景位置

```
深度学习 (Deep Learning)
├── 网络架构 (Architecture)
│   ├── MLP / CNN / RNN / Transformer
├── 网络组件 (Components)
│   ├── Activation Functions / Dense / Conv / ...
├── 训练过程 (Training) ← 你在这里
│   ├── Optimizers (权重更新策略)
│   ├── 【Loss Functions】 (优化目标)
│   ├── Backpropagation (梯度计算)
│   ├── Metrics (评估指标)
│   └── Regularization (正则化)
└── 框架工具 (Frameworks)
    ├── Keras: model.compile(loss=...)
    └── Scikit-Learn: MLPClassifier（隐式使用 log-loss）
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 3. 依赖地图

```
前置知识                        本主题                          后续方向
┌────────────────────────┐    ┌─────────────────────┐    ┌──────────────────────────┐
│ 概率论 (MLE/KL散度)    │───→│                     │───→│ Optimizers (梯度来源)     │
│ 信息论 (交叉熵/熵)     │───→│   Loss Functions    │───→│ Backpropagation          │
│ 统计学 (回归/分类)     │───→│                     │───→│ Metrics vs Loss 的区别    │
│ 激活函数 (输出层)      │───→│                     │───→│ 正则化 (L1/L2 加在 loss)  │
└────────────────────────┘    └─────────────────────┘    └──────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [loss_functions_map.md](loss_functions_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [loss_functions_concepts.md](loss_functions_concepts.md) | ② 概念 | 理解各损失函数定义、辨析区别 |
| [loss_functions_math.md](loss_functions_math.md) | ③ 公式 | 推导公式、理解梯度计算 |
| [loss_functions_tutorial.md](loss_functions_tutorial.md) | ④ 教程 | Why-First 理解损失函数设计动机 |
| [loss_functions_code.md](loss_functions_code.md) | ⑤ 代码 | 快速上手各框架的 loss API |
| [loss_functions_pitfalls.md](loss_functions_pitfalls.md) | ⑥ 踩坑 | 调试问题（loss 选错、NaN等） |
| [loss_functions_history.md](loss_functions_history.md) | ⑦ 历史 | 从 MSE 到交叉熵的演进 |
| [loss_functions_bridge.md](loss_functions_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [loss_functions_first_principles.md](loss_functions_first_principles.md) | ⑨ 第一性原理 | 从 MLE 推导为什么用交叉熵 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [loss_functions_map.md](loss_functions_map.md) 了解全局位置
2. 读 [loss_functions_tutorial.md](loss_functions_tutorial.md) Section 1 理解为什么需要损失函数
3. 读 [loss_functions_concepts.md](loss_functions_concepts.md) 掌握 MSE/BCE/CCE 核心术语
4. 读 [loss_functions_math.md](loss_functions_math.md) 手算一次各损失函数的前向+梯度
5. 跟 [loss_functions_code.md](loss_functions_code.md) 在 Keras 中使用不同 loss
6. 读 [loss_functions_history.md](loss_functions_history.md) 了解从 MSE → 交叉熵的演进

### 日常参考 🔧

1. 查 [loss_functions_code.md](loss_functions_code.md) API 速查表
2. 查 [loss_functions_concepts.md](loss_functions_concepts.md) 任务-激活-损失配对表
3. 查 [loss_functions_pitfalls.md](loss_functions_pitfalls.md) 排查 loss 异常问题

### 深度研究 🔬

1. 读 [loss_functions_first_principles.md](loss_functions_first_principles.md) 从 MLE 推导交叉熵
2. 读 [loss_functions_history.md](loss_functions_history.md) 完整演进线
3. 读 [loss_functions_bridge.md](loss_functions_bridge.md) 探索 Focal Loss、Label Smoothing 等高级技术

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
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考，§6.2 Output Units & Cost Functions |
| [《PRML》Ch.4, Ch.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 分类损失函数、交叉熵推导 |
| [《PML1》Ch.5](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | Decision Theory, Loss Functions |
| [Keras Losses](https://keras.io/api/losses/) | 📖 文档 | API 参考 |
| [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html) | 📖 文档 | 隐式损失函数 |
| Shannon, Bell System Technical Journal 1948 | 📖 论文 | 信息论基础/熵 |
| Lin, ICML 2017 (Focal Loss) | 📖 论文 | 类别不平衡损失 |
