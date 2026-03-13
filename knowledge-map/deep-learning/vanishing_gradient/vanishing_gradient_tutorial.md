---
topic: vanishing_gradient
dimension: tutorial
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Paper: [Hochreiter (1991)](https://www.bioinf.jku.at/publications/older/2304.pdf)"
  - "📖 Paper: [Hochreiter & Schmidhuber (1997)](https://www.bioinf.jku.at/publications/older/2604.pdf)"
  - "📖 Paper: [Pascanu et al. (2013)](https://arxiv.org/abs/1211.5063)"
  - "📖 Paper: [Vaswani et al. (2017)](https://arxiv.org/abs/1706.03762)"
expiry: 12m
status: current
---

# 梯度消失 (Vanishing Gradient) 教程

> **前置知识：** 反向传播（Backpropagation）、链式法则（Chain Rule）、RNN 基本结构
> **参考来源：** [Pascanu et al. (2013)](https://arxiv.org/abs/1211.5063) | [Hochreiter & Schmidhuber (1997)](https://www.bioinf.jku.at/publications/older/2604.pdf)

---


## Section 0: 前置知识速查

1. **反向传播**：从输出层向输入层逐层计算损失对每个参数的梯度
2. **链式法则**：复合函数的导数 = 各层导数的连乘
3. **RNN 结构**：同一组权重 $W_h$ 在每个时间步共享，$h_t = \sigma(W_h h_{t-1} + W_e e_t + b)$
4. **sigmoid 函数**：输出范围 (0,1)，导数最大值 0.25
5. **tanh 函数**：输出范围 (-1,1)，导数最大值 1（仅在 z=0）

> 📖 Paper: Rumelhart, Hinton & Williams, "Learning representations by back-propagating errors" (1986)

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

如果你对梯度消失一无所知，以下场景会让你崩溃：

- 🤯 **训练 RNN 时 loss 死活不下降** — 你以为是数据问题、学习率问题，其实是梯度传不回去
- 😱 **模型对长距离依赖完全无感** — "The cat, which sat on the mat, ___" 填不出 "sat"
- 🔥 **加深网络反而效果更差** — 违反直觉，更多层 = 更差，因为梯度消失更严重
- 💸 **浪费大量算力** — 训练几天发现模型什么也没学到

### 它的核心价值

1. **诊断能力**：知道 loss 停滞的真正原因，不再盲目调参
2. **架构选择**：理解为什么 LSTM/GRU 比 Vanilla RNN 好
3. **设计直觉**：在设计新网络时主动避免梯度消失
4. **理解历史**：明白 NLP 为什么从 RNN → LSTM → Transformer 的演进

> 📖 Paper: Hochreiter (1991) — 首次系统描述此问题

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 问题的产生：BPTT 的连乘灾难

```
RNN 展开图（以 "the students opened their" 为例）

时间步:    t=1          t=2           t=3           t=4
输入:     "the"      "students"    "opened"      "their"
          ↓            ↓             ↓             ↓
隐藏:    h1 ────→    h2 ────→     h3 ────→     h4
          │     Wh     │     Wh     │     Wh     │
          ↓            ↓             ↓             ↓
输出:    y1           y2            y3            y4
          ↓            ↓             ↓             ↓
损失:    J1           J2            J3            J4

         ◀── 梯度回传方向 ─────────────────────────
```

反向传播时，梯度从 J4 回传到 h1 的路径：

$$
\frac{\partial J_4}{\partial h_1} = \frac{\partial J_4}{\partial h_4} \cdot \frac{\partial h_4}{\partial h_3} \cdot \frac{\partial h_3}{\partial h_2} \cdot \frac{\partial h_2}{\partial h_1}
$$

**三个因子连乘**，每个因子 = $\text{diag}(\sigma') \cdot W_h$

> 📖 Paper: Pascanu et al. (2013), Section 2

### 2.2 为什么会消失：sigmoid 导数的"天花板"

```
Sigmoid 函数及其导数

σ(z) 曲线:                σ'(z) 曲线:
    1 ┤─────────────         0.25 ┤    ╭─╮
      │        ╱                  │   ╱   ╲
  0.5 ┤───╱───                   │  ╱     ╲
      │  ╱                       │ ╱       ╲
    0 ┤╱─────────────        0  ┤╱─────────╲──
     -4   0   4                 -4   0   4

  最大值 = 1                最大值 = 0.25 (在 z=0)
```

- sigmoid 导数 **最大只有 0.25**
- 连乘 T 步后：$0.25^T$ → 指数级衰减
- 即使用 tanh（最大导数 1），实际操作中 z 很少恰好为 0，通常 $\sigma'_{\text{tanh}} < 1$

### 2.3 直觉类比

> 想象你在玩**传话游戏**：
> - 第一个人说 "苹果" → 传 5 个人 → 最后一个人还能听到 "苹果"
> - 但如果每个人只传递 **25% 的音量**（sigmoid 导数 = 0.25）
> - 传 5 个人后：音量 = $0.25^5 = 0.001$ → **基本听不见了**
>
> 这就是梯度消失：信号在传递过程中被不断衰减，最终远端完全接收不到

### 2.4 LSTM 的解决方案：加法高速公路

```
LSTM 细胞状态流动（关键区别：加法而非乘法）

                  遗忘门ft    输入门it
                    ↓           ↓
  c(t-1) ─────→ [ ×f_t ] ─→ [ + ] ─→ c(t) ─────→ ...
                              ↑
                             i_t × c̃_t

  对比 RNN: h(t-1) ─→ [ σ(W_h × h + ...) ] ─→ h(t)
                        ↑
                     全部经过非线性变换（乘法）
```

**核心区别**：
1. RNN 隐藏状态更新 = **非线性乘法**（经过 σ/tanh × Wh）→ 梯度被压缩
2. LSTM 细胞状态更新 = **线性加法**（$c_t = f_t \cdot c_{t-1} + ...$）→ 梯度可以保持

当遗忘门 $f_t ≈ 1$ 时，$\frac{\partial c_t}{\partial c_{t-1}} ≈ 1$ → 梯度几乎无衰减

> 📖 Paper: Hochreiter & Schmidhuber (1997), Section 4

---


## Section 3: 局限性

1. **LSTM 并非完美解**：对于极长序列（>1000 步），LSTM 仍然会出现梯度退化
2. **计算开销**：LSTM 的参数量约为 Vanilla RNN 的 4 倍，训练更慢
3. **仍然是顺序处理**：无法并行化时间步，不适合超长文档
4. **Transformer 的出现**：通过自注意力机制完全绕开递归，彻底解决了长距离依赖和并行化问题

> 📖 Paper: Vaswani et al., "Attention Is All You Need" (2017)

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **LSTM** | 门控保持梯度；效果好 | 参数多；无法并行 | 中等长度序列（< 500 步）|
| **GRU** | 更少参数；训练更快 | 没有独立细胞状态 | 资源受限场景 |
| **残差连接** | 简单有效；可并行 | 需要深层网络架构配合 | CNN、Transformer |
| **梯度裁剪** | 简单；防止爆炸 | 只解决爆炸，不解决消失 | 配合其他方案使用 |
| **ReLU 激活** | 导数=1（正区间） | Dead neuron 问题 | 前馈网络 |
| **Transformer** | 无递归；长距离；可并行 | 内存 O(n²)；需要大数据 | 当前主流 NLP |
| **Xavier/He 初始化** | 保持方差稳定 | 仅缓解，不根治 | 所有网络的初始化 |

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| Hochreiter (1991), Diploma thesis | 📖 论文 | 首次系统描述梯度消失 |
| Hochreiter & Schmidhuber (1997), "Long Short-Term Memory" | 📖 论文 | LSTM 解决方案 |
| Pascanu et al. (2013), "On the difficulty of training RNNs" | 📖 论文 | 梯度消失/爆炸数学分析 |
| Cho et al. (2014), "GRU" | 📖 论文 | GRU 方案对比 |
| Vaswani et al. (2017), "Attention Is All You Need" | 📖 论文 | Transformer 替代方案 |
| Rumelhart, Hinton & Williams (1986), "Backpropagation" | 📖 论文 | 前置知识 |
