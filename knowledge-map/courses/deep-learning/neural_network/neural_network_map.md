---
topic: neural_network
dimension: map
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: McCulloch & Pitts, 'A logical calculus of the ideas immanent in nervous activity', Bulletin of Mathematical Biophysics 1943 — https://doi.org/10.1007/BF02478259"
  - "📖 Paper: Rosenblatt, 'The Perceptron: A probabilistic model for information storage and organization in the brain', Psychological Review 1958 — https://doi.org/10.1037/h0042519"
  - "📖 Paper: Rumelhart et al., 'Learning representations by back-propagating errors', Nature 1986 — https://www.nature.com/articles/323533a0"
  - "📖 Paper: Hornik et al., 'Multilayer feedforward networks are universal approximators', Neural Networks 1989 — https://doi.org/10.1016/0893-6080(89)90020-8"
  - "📖 Docs: PyTorch nn Module — https://pytorch.org/docs/stable/generated/torch.nn.Module.html"
  - "📖 Docs: Keras Sequential — https://keras.io/guides/sequential_model/"
expiry: 12m
status: current
---

# Neural Network (神经网络) 知识地图

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5
> 📖 Paper: McCulloch & Pitts, [A logical calculus of the ideas immanent in nervous activity](https://doi.org/10.1007/BF02478259), 1943

## 1. 核心问题

- **神经网络是什么？** → 由大量互连的计算单元（人工神经元）按层组织构成的计算模型，通过学习参数来逼近输入与输出之间的映射关系
- **为什么需要神经网络？** → 传统线性模型无法捕捉复杂的非线性关系，神经网络通过层层非线性变换自动提取特征表示
- **神经网络与大脑的关系？** → 受生物神经元启发但本质是数学函数复合，现代设计早已偏离生物学，更侧重工程效率
- **Neural Network 和 Deep Learning 有什么区别？** → Neural Network 是计算模型的总称；Deep Learning 特指使用深层（多隐藏层）神经网络的机器学习子领域
- **神经网络的理论保证是什么？** → 万能近似定理 (UAT)：一个足够宽的单隐藏层前馈网络可以逼近任意连续函数

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.1–6.4
> 📖 Paper: Hornik et al., [Universal Approximation Theorem](https://doi.org/10.1016/0893-6080(89)90020-8), 1989

---

## 2. 全景位置

```
人工智能 (Artificial Intelligence)
├── 机器学习 (Machine Learning) ← 你在这里
│   ├── 监督学习 (Supervised Learning)
│   │   ├── 线性模型 (Linear/Logistic Regression)
│   │   └── 【Neural Network (神经网络)】 (通过层层非线性变换学习特征表示)
│   │       ├── 前馈网络: MLP, Dense Layer
│   │       ├── 卷积网络: CNN, Conv Layer, Pool Layer
│   │       ├── 循环网络: RNN, LSTM, GRU
│   │       ├── 注意力网络: Transformer
│   │       └── 生成模型: VAE, GAN, Diffusion
│   ├── 无监督学习 (Unsupervised Learning)
│   └── 强化学习 (Reinforcement Learning)
└── 符号 AI (Symbolic AI)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.1, Ch.5, Ch.6

---

## 3. 依赖地图

```
前置知识                          本主题                          后续方向
┌──────────────────────┐    ┌──────────────────────┐    ┌─────────────────────────────┐
│ 线性代数 (矩阵乘法)   │───→│                      │───→│ MLP (多层感知机)             │
│ 微积分 (链式法则)      │───→│                      │───→│ CNN (卷积神经网络)           │
│ 概率论 (MLE/贝叶斯)    │───→│   Neural Network     │───→│ RNN / LSTM / GRU            │
│ 优化理论 (梯度下降)    │───→│   (神经网络)          │───→│ Transformer                 │
│ 生物神经元 (启发)      │───→│                      │───→│ 生成模型 (VAE/GAN/Diffusion)│
│ 线性/逻辑回归          │───→│                      │───→│ 正则化/优化/初始化 技术      │
└──────────────────────┘    └──────────────────────┘    └─────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.5.1

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [neural_network_map.md](neural_network_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [neural_network_concepts.md](neural_network_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [neural_network_math.md](neural_network_math.md) | ③ 公式 | 推导前向传播/反向传播公式 |
| [neural_network_tutorial.md](neural_network_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [neural_network_code.md](neural_network_code.md) | ⑤ 代码 | 快速上手实现 |
| [neural_network_pitfalls.md](neural_network_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [neural_network_history.md](neural_network_history.md) | ⑦ 历史 | 了解从 McCulloch-Pitts 到现代深度学习的技术演进 |
| [neural_network_bridge.md](neural_network_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [neural_network_first_principles.md](neural_network_first_principles.md) | ⑨ 第一性原理 | 从公理出发理解神经网络为什么有效 |

> 📖 本文件地图覆盖全部 9 个维度

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [neural_network_map.md](neural_network_map.md) 了解全局位置
2. 读 [neural_network_tutorial.md](neural_network_tutorial.md) Section 1 理解动机
3. 读 [neural_network_concepts.md](neural_network_concepts.md) 掌握核心术语
4. 读 [neural_network_math.md](neural_network_math.md) 手算一次前向传播 + 反向传播
5. 跟 [neural_network_code.md](neural_network_code.md) 快速跑一个 XOR / MNIST 示例
6. 读 [neural_network_history.md](neural_network_history.md) 了解 80 年技术演进
7. 读 [neural_network_first_principles.md](neural_network_first_principles.md) 追问底层公理

### 日常参考 🔧

1. 查 [neural_network_code.md](neural_network_code.md) API 速查表
2. 查 [neural_network_math.md](neural_network_math.md) 公式速查
3. 查 [neural_network_pitfalls.md](neural_network_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [neural_network_first_principles.md](neural_network_first_principles.md) 理解公理基础
2. 读 [neural_network_history.md](neural_network_history.md) 完整演进线
3. 读 [neural_network_bridge.md](neural_network_bridge.md) 探索下游架构
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
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考：神经网络架构、前向传播、反向传播、激活函数 |
| [《PRML》Ch.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | Concepts / Math：网络训练、误差反向传播、正则化 |
| [McCulloch & Pitts 1943](https://doi.org/10.1007/BF02478259) | 📖 论文 | History：人工神经元的开创性论文 |
| [Rosenblatt 1958](https://doi.org/10.1037/h0042519) | 📖 论文 | History：感知机原始论文 |
| [Rumelhart et al. 1986](https://www.nature.com/articles/323533a0) | 📖 论文 | History / Math：反向传播算法的经典论文 |
| [Hornik et al. 1989](https://doi.org/10.1016/0893-6080(89)90020-8) | 📖 论文 | Math / First Principles：万能近似定理 |
| [Hinton et al. 2006](https://doi.org/10.1162/neco.2006.18.7.1527) | 📖 论文 | History：深度信念网络，引发深度学习复兴 |
| [Krizhevsky et al. 2012](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) | 📖 论文 | History：AlexNet，深度学习在 ImageNet 上的突破 |
| [PyTorch nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html) | 📖 文档 | Code：PyTorch 神经网络基类 |
| [Keras Sequential](https://keras.io/guides/sequential_model/) | 📖 文档 | Code：Keras 序贯模型 |
