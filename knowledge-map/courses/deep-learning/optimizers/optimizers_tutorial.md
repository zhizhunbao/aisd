---
topic: optimizers
dimension: tutorial
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: Keras Optimizers — https://keras.io/api/optimizers/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
expiry: 12m
status: current
---

# Optimizers 教程

> **前置知识：** 微积分（梯度/偏导数）| 损失函数 | 反向传播
> **参考来源：** [《Deep Learning》Ch.8](../../../textbooks/goodfellow_deep_learning.pdf) | [Keras Optimizers](https://keras.io/api/optimizers/) | [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)

---


## Section 0: 前置知识速查

1. **梯度**：$\nabla L = [\frac{\partial L}{\partial w_1}, \frac{\partial L}{\partial w_2}, ...]$，指向损失增大最快的方向
2. **损失函数**：衡量预测与真实值的差距（如 MSE、交叉熵），训练目标是最小化它
3. **反向传播**：利用链式法则从输出层到输入层逐层计算梯度
4. **Mini-batch**：每次用一小批样本（如 32 个）来估计梯度，平衡计算效率和梯度准确性

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.5

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **无法训练**：神经网络有百万甚至数十亿个参数，没有优化器，权重就是随机初始值，模型完全无用
- 🔥 **手动调参不可能**：不可能手动找到让损失最小的数百万个参数值组合
- 🔥 **简单 SGD 太慢**：在复杂的损失地表上，vanilla SGD 在"窄长谷"中疯狂震荡，在"高原"上几乎不动

### 它的核心价值

1. **自动化权重更新**：给定梯度和学习率，优化器自动决定每个参数的更新方向和幅度
2. **加速收敛**：Momentum, Adam 等通过累积历史信息加速训练，比纯 SGD 快几倍到几十倍
3. **自适应学习率**：Adam, RMSprop 等为每个参数自动调整学习率，减少超参数调优负担
4. **在 compile 中配置训练过程**：`model.compile(optimizer=...)` 将优化策略与模型架构解耦

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.1

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 优化器在训练循环中的位置

```
┌────────────────────────────────────────────────────────────────────┐
│                    训练循环 (Training Loop)                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  for each epoch:                                                   │
│    for each mini-batch (X_batch, y_batch):                        │
│                                                                    │
│      ① 前向传播:  ŷ = model(X_batch)                              │
│                         ▼                                          │
│      ② 计算损失:  L = loss(ŷ, y_batch)                            │
│                         ▼                                          │
│      ③ 反向传播:  ∂L/∂W = backprop(L)                             │
│                         ▼                                          │
│      ④ 优化器更新: W = optimizer.step(W, ∂L/∂W)  ← 【这里】      │
│                                                                    │
│  Keras fit() 自动执行上述循环                                       │
│  scikit-learn fit() 也是如此（solver 参数选择优化器）               │
└────────────────────────────────────────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

### 2.2 为什么简单 SGD 不够好？

**为什么需要 Momentum/Adam 而不是只用 SGD？**

想象你在一个"窄长谷"中优化（损失沿一个方向平坦、沿另一个方向陡峭）：
- **SGD**：在平坦方向移动很小，在陡峭方向来回震荡 → 极慢
- **Momentum**：累积平坦方向的小梯度为大速度，陡峭方向的正负梯度相互抵消 → 沿谷底快速前进
- **Adam**：不仅有动量，还自动为每个方向调整学习率（陡峭方向用小 lr，平坦方向用大 lr）→ 最优

```
损失地表 (等高线图)

SGD 的路径:           Momentum 的路径:       Adam 的路径:
┌──────────────┐    ┌──────────────┐      ┌──────────────┐
│  ╱╲╱╲╱╲╱╲   │    │  ──────→     │      │  ─→           │
│   ╲╱╲╱╲╱    │    │    ──────→   │      │   ─→ ★        │
│    ★ (最优) │    │      ★       │      │               │
└──────────────┘    └──────────────┘      └──────────────┘
  震荡严重              平滑加速              最短路径
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.3

### 2.3 Adam 的三步计算过程

每一步 Adam 做三件事：

1. **更新动量（一阶矩）**：$m_t = 0.9 \cdot m_{t-1} + 0.1 \cdot g_t$ — "我一直在往哪个方向走？"
2. **更新方差（二阶矩）**：$v_t = 0.999 \cdot v_{t-1} + 0.001 \cdot g_t^2$ — "每个参数的梯度波动有多大？"
3. **自适应更新**：大波动参数用小学习率，小波动参数用大学习率

> 📖 Paper: Kingma & Ba, [Adam](https://arxiv.org/abs/1412.6980), ICLR 2015

### 2.4 compile 和 fit 的角色

```
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
│              │                 │                                │
│              │                 │                                └─ 监控什么指标
│              │                 └─ 优化什么目标（损失函数）
│              └─ 用什么方法优化（优化器）
└─ 配置训练过程（不执行训练）

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)
│         │        │         │          │               │
│         │        │         │          │               └─ 留 10% 做验证
│         │        │         │          └─ 每次用 32 个样本计算梯度
│         │        │         └─ 遍历数据 10 次
│         │        └─ 训练标签
│         └─ 训练特征
└─ 执行实际训练（反复调用 compile 中配置的 optimizer）
```

> 📖 Docs: [Keras Model Training APIs](https://keras.io/api/models/model_training_apis/)

---


## Section 3: 局限性

1. **Adam 泛化可能不如 SGD**：在某些 CV 任务中，SGD + LR schedule 的最终测试精度略优于 Adam → 大型 CV 比赛常用 SGD
2. **学习率仍需要调**：虽然 Adam 对 lr 不太敏感，但极端的 lr 仍会导致失败。lr=0.1 对 Adam 通常太大
3. **内存开销**：Adam 需要为每个参数维护 $m$ 和 $v$ 两个状态 → 内存是 SGD 的 3 倍
4. **L-BFGS 无法扩展**：只适合小规模问题（几千个参数），深度学习主流不使用
5. **所有优化器都可能卡在鞍点**：高维空间中鞍点远多于局部最优 → Momentum/Adam 的动量有助于逃离

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **SGD** | 内存最少，可达最佳泛化 | 收敛慢，需精细调 lr | CV 研究/比赛 |
| **Momentum SGD** | 加速收敛，抑制震荡 | 仍需调 lr + β | 大规模 CV 训练 |
| **Adam** | 自适应 lr，对超参数鲁棒 | 内存 3×，泛化有时略逊 | **通用默认** |
| **AdamW** | 解耦权重衰减 | 同 Adam | Transformer 训练 |
| **RMSprop** | 自适应 lr，无偏差修正开销 | 无动量 | RNN/LSTM |
| **L-BFGS** | 二阶信息，收敛快，无需调 lr | 内存大，不适合大数据 | sklearn MLP, 小数据 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📖 Docs: [Keras Optimizers](https://keras.io/api/optimizers/)

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.8](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考 |
| [Kingma & Ba, ICLR 2015](https://arxiv.org/abs/1412.6980) | 📖 论文 | Adam 公式推导 |
| [Keras Optimizers](https://keras.io/api/optimizers/) | 📖 文档 | API 参考 |
| [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html) | 📖 文档 | solver 参数 |
