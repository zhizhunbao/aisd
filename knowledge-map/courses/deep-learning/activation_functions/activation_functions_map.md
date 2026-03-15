---
topic: activation_functions
dimension: map
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, 'PML1' Ch.13 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: Keras Activations — https://keras.io/api/layers/activations/"
  - "📖 Docs: PyTorch Activations — https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity"
expiry: 12m
status: current
---

# Activation Functions 知识地图

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.13

## 1. 核心问题

- **什么是激活函数？** → 在神经元输出端施加的非线性变换，使网络能学习非线性映射
- **为什么需要激活函数？** → 没有非线性，多层线性变换等价于单层线性变换（矩阵乘法的结合律）
- **主要的激活函数有哪些？** → Sigmoid, Tanh, ReLU, Leaky ReLU, ELU, Softmax, Swish/SiLU, GELU
- **如何选择激活函数？** → 隐藏层默认 ReLU；输出层根据任务选（Sigmoid=二分类, Softmax=多分类, Linear=回归）
- **激活函数如何影响梯度传播？** → 饱和函数（Sigmoid/Tanh）导致梯度消失；ReLU 负区间梯度为零导致"死神经元"

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.3

---

## 2. 全景位置

```
深度学习 (Deep Learning)
├── 网络架构 (Architecture)
│   ├── MLP (全连接网络)
│   ├── CNN (卷积神经网络)
│   └── RNN / Transformer
├── 网络组件 (Components) ← 你在这里
│   ├── 【Activation Functions】 (引入非线性)
│   ├── Dense Layer (线性变换 + 激活)
│   ├── Conv Layer (局部连接 + 激活)
│   ├── Normalization (BatchNorm, LayerNorm)
│   └── Dropout (正则化)
├── 训练过程 (Training)
│   ├── Loss Functions (损失函数)
│   ├── Optimizers (优化器)
│   └── Backpropagation (反向传播)
└── 框架工具 (Frameworks)
    ├── Keras / TensorFlow
    ├── PyTorch
    └── Scikit-Learn (MLPClassifier)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 3. 依赖地图

```
前置知识                         本主题                           后续方向
┌─────────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│ 线性代数 (矩阵乘法) │───→│                      │───→│ MLP 隐藏层设计           │
│ 微积分 (链式法则)    │───→│  Activation          │───→│ CNN 特征提取             │
│ 概率论 (概率分布)    │───→│  Functions           │───→│ 梯度消失/爆炸问题        │
│ 感知机 (线性分类器)  │───→│                      │───→│ 网络初始化策略           │
└─────────────────────┘    └──────────────────────┘    └──────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [activation_functions_map.md](activation_functions_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [activation_functions_concepts.md](activation_functions_concepts.md) | ② 概念 | 理解各激活函数定义、辨析区别 |
| [activation_functions_math.md](activation_functions_math.md) | ③ 公式 | 推导公式、理解梯度计算 |
| [activation_functions_tutorial.md](activation_functions_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [activation_functions_code.md](activation_functions_code.md) | ⑤ 代码 | 快速上手实现和可视化 |
| [activation_functions_pitfalls.md](activation_functions_pitfalls.md) | ⑥ 踩坑 | 调试问题（梯度消失、死神经元等） |
| [activation_functions_history.md](activation_functions_history.md) | ⑦ 历史 | 了解技术演进（从 Sigmoid 到 GELU） |
| [activation_functions_bridge.md](activation_functions_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [activation_functions_first_principles.md](activation_functions_first_principles.md) | ⑨ 第一性原理 | 从公理推导为什么需要非线性 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [activation_functions_map.md](activation_functions_map.md) 了解全局位置
2. 读 [activation_functions_tutorial.md](activation_functions_tutorial.md) Section 1 理解动机
3. 读 [activation_functions_concepts.md](activation_functions_concepts.md) 掌握核心术语
4. 读 [activation_functions_math.md](activation_functions_math.md) 手算一次每个激活函数的前向+反向
5. 跟 [activation_functions_code.md](activation_functions_code.md) 快速开始可视化各函数
6. 读 [activation_functions_history.md](activation_functions_history.md) 了解从 Sigmoid → ReLU → GELU 的演进

### 日常参考 🔧

1. 查 [activation_functions_code.md](activation_functions_code.md) API 速查表
2. 查 [activation_functions_math.md](activation_functions_math.md) 公式速查
3. 查 [activation_functions_pitfalls.md](activation_functions_pitfalls.md) 排查梯度问题

### 深度研究 🔬

1. 读 [activation_functions_first_principles.md](activation_functions_first_principles.md) 理解非线性的数学必要性
2. 读 [activation_functions_history.md](activation_functions_history.md) 完整演进线
3. 读 [activation_functions_bridge.md](activation_functions_bridge.md) 探索初始化策略与归一化层的关系
4. 阅读原始论文（Nair & Hinton 2010, Glorot & Bengio 2010, Ramachandran et al. 2017）

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
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考，§6.3 Hidden Units |
| [《PRML》Ch.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 神经网络激活函数基础 |
| [《PML1》Ch.13](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | Neural Net Fundamentals |
| [Keras Activations](https://keras.io/api/layers/activations/) | 📖 文档 | API 参考、代码示例 |
| [PyTorch Activations](https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity) | 📖 文档 | API 参考、代码示例 |
| [Scikit-Learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html) | 📖 文档 | MLP 激活函数参数 |
| Nair & Hinton, ICML 2010 | 📖 论文 | ReLU 的提出 |
| Glorot & Bengio, AISTATS 2010 | 📖 论文 | 激活函数与初始化策略 |
| Ramachandran et al., arXiv 2017 | 📖 论文 | Swish 激活函数 |
| Hendrycks & Gimpel, arXiv 2016 | 📖 论文 | GELU 激活函数 |
