---
topic: mlp
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Rumelhart et al., 'Learning representations by back-propagating errors', Nature 1986 — https://www.nature.com/articles/323533a0"
  - "📖 Paper: Cybenko, 'Approximation by superpositions of a sigmoidal function', Mathematics of Control, Signals and Systems 1989 — https://doi.org/10.1007/BF02551274"
  - "📖 Paper: Hornik et al., 'Multilayer feedforward networks are universal approximators', Neural Networks 1989 — https://doi.org/10.1016/0893-6080(89)90020-8"
  - "📖 Docs: PyTorch nn.Linear — https://pytorch.org/docs/stable/generated/torch.nn.Linear.html"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
expiry: 12m
status: current
---

# MLP (Multi-Layer Perceptron) 知识地图

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5
> 📖 Paper: Rumelhart et al., [Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0), Nature 1986

## 1. 核心问题

- **MLP 是什么？** → 由多层全连接层 + 非线性激活函数组成的前馈神经网络，是深度学习最基础的模型架构
- **MLP 解决什么问题？** → 克服线性模型的局限，能学习输入特征之间的非线性交互关系
- **为什么需要隐藏层？** → 单层线性变换无法解决 XOR 等非线性可分问题，隐藏层 + 激活函数提供非线性表示能力
- **MLP 的理论保证是什么？** → 万能近似定理 (Universal Approximation Theorem)：一个具有足够宽隐藏层的 MLP 可以逼近任意连续函数
- **MLP 如何训练？** → 通过反向传播 (Backpropagation) 计算梯度，使用随机梯度下降 (SGD) 等优化算法更新参数

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1–6.4
> 📖 Paper: Cybenko, [Universal Approximation Theorem](https://doi.org/10.1007/BF02551274), 1989

---

## 2. 全景位置

```
深度学习 (Deep Learning)
├── 前馈网络 (Feedforward Networks) ← 你在这里
│   ├── 【MLP (Multi-Layer Perceptron)】 (最基础的前馈网络，全连接层堆叠)
│   ├── CNN (Convolutional Neural Network) (引入局部连接+权值共享，擅长空间数据)
│   └── ResNet / DenseNet (引入跳跃连接，解决深层训练问题)
├── 序列模型 (Sequence Models)
│   ├── RNN (Recurrent Neural Network) (引入循环连接，处理时序数据)
│   ├── LSTM / GRU (门控机制解决梯度消失)
│   └── Transformer (自注意力机制，并行处理序列)
├── 生成模型 (Generative Models)
│   ├── VAE (变分自编码器)
│   └── GAN (生成对抗网络)
└── 图神经网络 (Graph Neural Networks)
    └── GCN / GAT (图结构数据处理)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, Ch.9, Ch.10

---

## 3. 依赖地图

```
前置知识                          本主题                          后续方向
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│ 线性代数 (矩阵乘法)   │───→│                      │───→│ CNN (卷积神经网络)        │
│ 微积分 (链式法则)      │───→│                      │───→│ RNN (循环神经网络)        │
│ 概率论 (极大似然)      │───→│   MLP                │───→│ Transformer              │
│ 线性回归 / 逻辑回归    │───→│   (Multi-Layer       │───→│ 正则化技术 (Dropout等)    │
│ 梯度下降优化           │───→│    Perceptron)       │───→│ 高级优化器 (Adam等)       │
│ 感知机 (Perceptron)    │───→│                      │───→│ Batch Normalization      │
└──────────────────────┘    └──────────────────────┘    └──────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.1

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [mlp_map.md](mlp_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [mlp_concepts.md](mlp_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [mlp_math.md](mlp_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [mlp_tutorial.md](mlp_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [mlp_code.md](mlp_code.md) | ⑤ 代码 | 快速上手实现 |
| [mlp_pitfalls.md](mlp_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [mlp_history.md](mlp_history.md) | ⑦ 历史 | 了解技术演进 |
| [mlp_bridge.md](mlp_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [mlp_first_principles.md](mlp_first_principles.md) | ⑨ 第一性原理 | 从公理出发理解 MLP 为什么必须是这样 |

> 📖 本文件地图覆盖全部 9 个维度

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [mlp_map.md](mlp_map.md) 了解全局位置
2. 读 [mlp_tutorial.md](mlp_tutorial.md) Section 1 理解动机
3. 读 [mlp_concepts.md](mlp_concepts.md) 掌握核心术语
4. 读 [mlp_math.md](mlp_math.md) 手算一次前向传播 + 反向传播
5. 跟 [mlp_code.md](mlp_code.md) 快速开始跑一个 XOR / MNIST 示例
6. 读 [mlp_history.md](mlp_history.md) 了解从感知机到现代 MLP 的技术演进

### 日常参考 🔧

1. 查 [mlp_code.md](mlp_code.md) API 速查表
2. 查 [mlp_math.md](mlp_math.md) 公式速查
3. 查 [mlp_pitfalls.md](mlp_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [mlp_first_principles.md](mlp_first_principles.md) 理解 MLP 的公理基础
2. 读 [mlp_history.md](mlp_history.md) 完整演进线
3. 读 [mlp_bridge.md](mlp_bridge.md) 探索下游架构
4. 阅读 Rumelhart et al. 1986 原始论文

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
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考：前馈网络架构、激活函数、万能近似定理、反向传播 |
| [《PRML》Ch.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | Concepts / Math：网络训练、误差反向传播、正则化 |
| [Rumelhart et al. 1986](https://www.nature.com/articles/323533a0) | 📖 论文 | History：反向传播算法的经典论文 |
| [Cybenko 1989](https://doi.org/10.1007/BF02551274) | 📖 论文 | Math / First Principles：万能近似定理 (sigmoid) |
| [Hornik et al. 1989](https://doi.org/10.1016/0893-6080(89)90020-8) | 📖 论文 | Math / First Principles：万能近似定理 (通用) |
| [PyTorch nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html) | 📖 文档 | Code：PyTorch 实现参考 |
| [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html) | 📖 文档 | Code：scikit-learn 实现参考 |
| [Rosenblatt 1958](https://doi.org/10.1037/h0042519) | 📖 论文 | History：感知机原始论文 |
| [Glorot & Bengio 2010](http://proceedings.mlr.press/v9/glorot10a.html) | 📖 论文 | Pitfalls / Code：Xavier 初始化 |
| [He et al. 2015](https://arxiv.org/abs/1502.01852) | 📖 论文 | Pitfalls / Code：He 初始化 / PReLU |
| [Srivastava et al. 2014](https://jmlr.org/papers/v15/srivastava14a.html) | 📖 论文 | Tutorial / Pitfalls：Dropout 正则化 |
