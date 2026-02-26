# Week 4: RNN & LSTM — 教科书教程

> **核心问题：** Slides 给了 RNN 和 LSTM 的公式和架构图，但没有推导——教科书怎么从第一原理推出这些公式的？
>
> **教科书来源：** Goodfellow et al., _Deep Learning_, Chapter 10: Sequence Modeling: Recurrent and Recursive Nets

---

## §0 前置知识 (Prerequisites)

本教程假设你已经理解以下概念（来自 Week 3 CNN 和前面的数学基础）。如果不熟悉，请先回顾。

### 0.1 贯穿例子：周温度预测

> 📌 **贯穿例子 (Running Example)：** 澳大利亚墨尔本的每日最低温度数据（Lab4 的数据集）。
>
> - 输入：过去 12 周的温度 $x_1, x_2, \ldots, x_{12}$
> - 目标：预测第 13 周的温度 $y_{13}$
> - 为什么需要"记忆"：第 13 周的温度不只取决于第 12 周——它还取决于整个季节走势（是在升温还是降温）。

### 0.2 需要复习的概念

| 概念                      | 一句话定义                                              | 哪里学的          |
| ------------------------- | ------------------------------------------------------- | ----------------- |
| **前馈网络 (FFN)**        | 信息只往前流，无循环                                    | Week 3 CNN slides |
| **链式法则 (Chain Rule)** | $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$     | Week 3 反向传播   |
| **梯度下降**              | $W \leftarrow W - \alpha \frac{\partial L}{\partial W}$ | Week 3            |
| **tanh 激活函数**         | 输出 (-1, 1)，以 0 为中心                               | Week 3 CNN        |
| **sigmoid 激活函数**      | 输出 (0, 1)，用于"门"                                   | Week 3 CNN        |

---

## §1 展开计算图：从循环到链 (Unfolding Computational Graphs)

> 📚 Ref: Goodfellow §10.1, Eq. 10.1–10.7

### 1.1 动力学系统的递归定义

教科书从最简单的**动力学系统** (dynamical system) 出发：

$$s^{(t)} = f(s^{(t-1)}; \theta) \tag{Goodfellow Eq. 10.1}$$

| 符号      | 含义                         | 温度例子中对应             |
| --------- | ---------------------------- | -------------------------- |
| $s^{(t)}$ | 时间 $t$ 的系统状态          | 第 $t$ 周的"记忆向量"      |
| $f$       | 转移函数（定义状态如何演化） | 如何从上周记忆生成本周记忆 |
| $\theta$  | 可学习参数                   | 权重矩阵                   |

**关键洞察：** Eq. 10.1 是**递归定义**——$s^{(t)}$ 引用了 $s^{(t-1)}$，而 $s^{(t-1)}$ 又引用了 $s^{(t-2)}$，形成无限链。

### 1.2 展开 (Unfolding)

教科书指出：对于有限长度 $\tau$ 的序列，可以把递归定义"展开"成一条链 (Goodfellow §10.1):

$$s^{(3)} = f(s^{(2)}; \theta) = f(f(s^{(1)}; \theta); \theta) \tag{Goodfellow Eq. 10.2–10.3}$$

> ⚠️ **Slides 未强调：** 展开后得到的是一个**有向无环图 (DAG)**——不再有循环。这意味着标准的反向传播算法可以直接使用。

**展开的两大好处** (Goodfellow §10.1):

1. **固定输入大小：** 无论序列多长，模型的"一步"始终是 $f(s^{(t-1)}, x^{(t)}; \theta)$——输入大小不变
2. **参数共享：** 同一个 $f$（同一套 $\theta$）在每个时间步重复使用

> 📐 **推导 (tutorial 补充)：** 为什么展开使反向传播成为可能？
>
> 在递归形式下，$s^{(t)}$ 是自身的函数——无法直接求导。展开后，每个 $s^{(t)}$ 成为独立的计算图节点，链式法则可以沿着时间轴逐步应用。

### 1.3 加入外部输入

现实中系统不仅有内部状态，还接收外部输入 $x^{(t)}$：

$$h^{(t)} = f(h^{(t-1)}, x^{(t)}; \theta) \tag{Goodfellow Eq. 10.5}$$

这里用 $h$（hidden）替代 $s$（state），因为它将成为 RNN 的**隐藏层**。

> 📌 **温度预测例子：** $h^{(t)}$ 编码了"过去 $t$ 周所有温度信息的摘要"。$x^{(t)}$ 是第 $t$ 周的新温度。网络将两者结合，产生包含所有 $t$ 周信息的新摘要 $h^{(t)}$。

Eq. 10.5 还可以写成展开形式 (Goodfellow Eq. 10.6):

$$h^{(t)} = g^{(t)}(x^{(t)}, x^{(t-1)}, x^{(t-2)}, \ldots, x^{(1)}) \tag{Goodfellow Eq. 10.6}$$

> ⚠️ **Slides 未强调：** $h^{(t)}$ 是整个过去序列的"有损摘要" (lossy summary)——它把任意长的序列压缩成固定长度的向量。信息必然有丢失。

**Eq. 10.5 → Eq. 10.6 之间的逻辑：** Eq. 10.5 说"当前状态由上一步状态+当前输入决定"；Eq. 10.6 说"如果把递归全展开，当前状态实际上是所有过去输入的函数"。这两个是同一件事的两种表达——一个是递归形式（实现），一个是展开形式（理解）。

---

## §2 标准 RNN 的前向传播 (Forward Propagation in Standard RNNs)

> 📚 Ref: Goodfellow §10.2, Eq. 10.8–10.14

### 2.1 从抽象到具体

§1 给出了抽象的 $h^{(t)} = f(h^{(t-1)}, x^{(t)}; \theta)$。现在教科书把 $f$ 具体化为：

$$a^{(t)} = b + W h^{(t-1)} + U x^{(t)} \tag{Goodfellow Eq. 10.8}$$

$$h^{(t)} = \tanh(a^{(t)}) \tag{Goodfellow Eq. 10.9}$$

$$o^{(t)} = c + V h^{(t)} \tag{Goodfellow Eq. 10.10}$$

$$\hat{y}^{(t)} = \text{softmax}(o^{(t)}) \tag{Goodfellow Eq. 10.11}$$

| 符号      | 含义                           | Slides 的写法 |
| --------- | ------------------------------ | ------------- |
| $U$       | 输入到隐藏层的权重             | $W_x$         |
| $W$       | 隐藏到隐藏的权重（递归）       | $W_h$         |
| $V$       | 隐藏到输出的权重               | —             |
| $b$       | 隐藏层偏置                     | —             |
| $c$       | 输出层偏置                     | —             |
| $a^{(t)}$ | 激活前的加和（pre-activation） | —             |

> ⚠️ **Slides 未覆盖：** 教科书明确区分了 $a^{(t)}$（激活前的线性组合）和 $h^{(t)}$（激活后的隐藏状态）。Slides 直接写 $h_t = f(W_x x_t + W_h h_{t-1})$，省略了偏置和 pre-activation 步骤。

> ⚠️ **符号差异：** 教科书用 $U, W, V$，Slides 用 $W_x, W_h$。考试以 Slides 为准。

### 2.2 损失函数

教科书定义总损失为所有时间步损失的求和 (Goodfellow Eq. 10.12–10.14):

$$L = \sum_t L^{(t)} = -\sum_t \log p_{\text{model}}(y^{(t)} \mid x^{(1)}, \ldots, x^{(t)}) \tag{Goodfellow Eq. 10.14}$$

> 📌 **温度预测对应：** 如果用 MSE 而非 NLL，则 $L^{(t)} = (y^{(t)} - \hat{y}^{(t)})^2$，总损失 = 所有时间步 MSE 的平均。

### 2.3 三种 RNN 架构模式

教科书描述了三种设计模式 (Goodfellow §10.2, Figures 10.3–10.5):

| 模式                                       | 结构                                     | 对应 Slides 的类型 |
| ------------------------------------------ | ---------------------------------------- | ------------------ |
| **Hidden-to-hidden recurrence** (Fig 10.3) | $h^{(t)}$ 连接到 $h^{(t+1)}$，每步有输出 | Many-to-Many       |
| **Output-to-hidden recurrence** (Fig 10.4) | $o^{(t)}$ 连接到 $h^{(t+1)}$             | — (Slides 未提)    |
| **Single output** (Fig 10.5)               | 只在最后一步输出                         | Many-to-One        |

> ⚠️ **Slides 未覆盖的洞察：** Output-to-hidden 架构（Fig 10.4）更弱——因为 $o^{(t)}$ 是为匹配目标而训练的，不一定包含最佳的历史信息。但它的优势是**可以并行化训练**（每个时间步独立）。

**§1 到 §2 的过渡：** §1 告诉我们"RNN 可以展开成链"，但没说链里的每个节点具体做什么计算。§2 回答了这个问题：每个节点做线性变换 + tanh 激活 + softmax 输出。

---

## §3 BPTT 梯度推导 (Backpropagation Through Time)

> 📚 Ref: Goodfellow §10.2.2, Eq. 10.17–10.25

### 3.1 为什么需要 BPTT？

标准反向传播是"逐层"传梯度。RNN 展开后变成一条**时间链**——反向传播就变成"逐时间步"传梯度。教科书称之为 BPTT (Backpropagation Through Time)。

> ⚠️ **Slides 未强调：** BPTT **不是**一种新算法——它就是标准反向传播，只是应用在展开后的 RNN 上 (Goodfellow §10.2.2: "No specialized algorithms are necessary")。

### 3.2 逐步推导

教科书从损失对输出的梯度开始 (Goodfellow Eq. 10.18):

$$(\nabla_{o^{(t)}} L)_i = \hat{y}_i^{(t)} - \mathbf{1}_{i, y^{(t)}} \tag{Goodfellow Eq. 10.18}$$

这是 softmax + 交叉熵的标准结果：预测概率减去真实标签的 one-hot。

**在最后一个时间步 $\tau$：**

$$\nabla_{h^{(\tau)}} L = V^\top \nabla_{o^{(\tau)}} L \tag{Goodfellow Eq. 10.19}$$

$h^{(\tau)}$ 只影响 $o^{(\tau)}$，所以梯度很简单。

**在中间时间步 $t < \tau$：**

$h^{(t)}$ 同时影响 $o^{(t)}$（当前输出）和 $h^{(t+1)}$（下一步隐藏状态），所以梯度有两个来源：

$$\nabla_{h^{(t)}} L = W^\top (\nabla_{h^{(t+1)}} L) \cdot \text{diag}(1 - (h^{(t+1)})^2) + V^\top (\nabla_{o^{(t)}} L) \tag{Goodfellow Eq. 10.21}$$

| 项                                                                   | 含义                    | 来源                          |
| -------------------------------------------------------------------- | ----------------------- | ----------------------------- |
| $W^\top (\nabla_{h^{(t+1)}} L) \cdot \text{diag}(1 - (h^{(t+1)})^2)$ | 来自未来时间步的梯度    | $h^{(t)} \to h^{(t+1)} \to L$ |
| $V^\top (\nabla_{o^{(t)}} L)$                                        | 来自当前输出的梯度      | $h^{(t)} \to o^{(t)} \to L$   |
| $\text{diag}(1 - (h^{(t+1)})^2)$                                     | tanh 的导数（Jacobian） | $\tanh'(x) = 1 - \tanh^2(x)$  |

> 🔑 **关键洞察：** 每回退一步，梯度都要乘以 $W^\top$ 和 $\text{diag}(1 - h^2)$。这两个因子决定了梯度是消失还是爆炸。

### 3.3 参数梯度

因为权重共享，参数梯度是所有时间步贡献的总和 (Goodfellow Eq. 10.22–10.25):

$$\nabla_W L = \sum_t \text{diag}(1 - (h^{(t)})^2) (\nabla_{h^{(t)}} L) h^{(t-1)\top} \tag{Goodfellow Eq. 10.25}$$

> ⚠️ **Slides 给了 $\frac{\partial L}{\partial W} = \sum_t \frac{\partial L_t}{\partial W}$，但没展开。** 教科书告诉我们：每个 $\frac{\partial L_t}{\partial W}$ 的具体计算涉及 $h^{(t)}$、$h^{(t-1)}$、和 tanh 的 Jacobian。

**§2 到 §3 的过渡：** §2 定义了前向传播——数据从左到右流过展开的 RNN。但我们还没说如何更新权重。§3 回答了这个问题：梯度从右到左（从未来到过去）流过同一条链——这就是 BPTT。

---

## §4 长期依赖的挑战——梯度消失的数学证明 (The Challenge of Long-Term Dependencies)

> 📚 Ref: Goodfellow §10.7, Eq. 10.36–10.39

### 4.1 简化模型：线性 RNN

教科书用一个**无激活函数、无输入**的简化 RNN 来揭示梯度消失的本质：

$$h^{(t)} = W h^{(t-1)} \tag{Goodfellow Eq. 10.36}$$

递归展开 $t$ 步：

$$h^{(t)} = W^t h^{(0)} \tag{Goodfellow Eq. 10.37}$$

### 4.2 特征值分解

如果 $W$ 可以特征值分解 (Goodfellow Eq. 10.38–10.39)：

$$W = Q \Lambda Q^\top \tag{Goodfellow Eq. 10.38}$$

则：

$$h^{(t)} = Q \Lambda^t Q^\top h^{(0)} \tag{Goodfellow Eq. 10.39}$$

| 符号        | 含义                                              |
| ----------- | ------------------------------------------------- |
| $Q$         | 正交矩阵（特征向量）                              |
| $\Lambda$   | 对角矩阵（特征值 $\lambda_1, \lambda_2, \ldots$） |
| $\Lambda^t$ | 每个特征值取 $t$ 次方                             |

**数学结论：**

- 如果 $|\lambda_i| < 1$：$\lambda_i^t \to 0$（指数衰减）→ 该方向的信息**消失**
- 如果 $|\lambda_i| > 1$：$\lambda_i^t \to \infty$（指数爆炸）→ 该方向的信息**爆炸**
- 如果 $|\lambda_i| = 1$：$\lambda_i^t = 1$（完美保持）→ 该方向信息**稳定**

> 🔑 **这就是梯度消失/爆炸的数学本质！**
>
> Slides 用 "$0.5^{100} \approx 10^{-30}$" 的例子说明了标量情况。教科书推广到矩阵情况——**特征值的模**决定了该方向的梯度命运。

> ⚠️ **Slides 未覆盖的重要结论 (Goodfellow §10.7)：**
>
> Bengio et al. (1993, 1994) 证明了：为了让 RNN 能够稳定地存储记忆（不对小扰动敏感），参数必须处于梯度消失的区域。换句话说，**稳定记忆和有效训练是矛盾的**——这是 vanilla RNN 的根本困难。

### 4.3 非递归网络为什么没这么严重？

> 📐 **推导 (tutorial 补充)：** 在非递归网络中，每一层有**不同的**权重 $w^{(t)}$。如果这些权重独立随机（均值 0，方差 $v$），则乘积的方差为 $O(v^n)$。可以通过选择 $v = \sqrt[n]{v^*}$ 来控制方差——这就是 Xavier/He 初始化的原理。而 RNN 的权重是**共享的**（同一个 $W$），无法用这种方式控制。

**§3 到 §4 的过渡：** §3 给出了 BPTT 的梯度公式。但公式中有一个 $W^\top$ 被反复相乘——§4 证明了这种反复相乘在数学上必然导致指数级衰减或爆炸。

---

## §5 LSTM：加法路径的设计哲学 (LSTM: The Design Philosophy of Additive Paths)

> 📚 Ref: Goodfellow §10.10, Eq. 10.40–10.44, Figure 10.16

### 5.1 从乘法困境到加法解决方案

§4 证明了乘法链必然导致梯度消失。解决方案的直觉是：

$$\text{如果能设计一条"加法路径"，梯度就能绕开乘法链的指数衰减。}$$

LSTM (Hochreiter & Schmidhuber, 1997) 的核心创新就是引入了这样的加法路径——**细胞状态** (cell state)。

### 5.2 LSTM 的数学定义

教科书给出了 LSTM 的完整公式 (Goodfellow Eq. 10.40–10.44)：

**遗忘门 (Forget Gate):**

$$f_i^{(t)} = \sigma\left(b_i^f + \sum_j U_{i,j}^f x_j^{(t)} + \sum_j W_{i,j}^f h_j^{(t-1)}\right) \tag{Goodfellow Eq. 10.40}$$

**细胞状态更新 (Cell State Update):**

$$s_i^{(t)} = f_i^{(t)} s_i^{(t-1)} + g_i^{(t)} \sigma\left(b_i + \sum_j U_{i,j} x_j^{(t)} + \sum_j W_{i,j} h_j^{(t-1)}\right) \tag{Goodfellow Eq. 10.41}$$

**输入门 (Input/External Gate):**

$$g_i^{(t)} = \sigma\left(b_i^g + \sum_j U_{i,j}^g x_j^{(t)} + \sum_j W_{i,j}^g h_j^{(t-1)}\right) \tag{Goodfellow Eq. 10.42}$$

**输出门和隐藏状态 (Output Gate and Hidden State):**

$$h_i^{(t)} = \tanh(s_i^{(t)}) \cdot q_i^{(t)} \tag{Goodfellow Eq. 10.43}$$

$$q_i^{(t)} = \sigma\left(b_i^o + \sum_j U_{i,j}^o x_j^{(t)} + \sum_j W_{i,j}^o h_j^{(t-1)}\right) \tag{Goodfellow Eq. 10.44}$$

| 教科书符号  | Slides 符号 | 含义                                |
| ----------- | ----------- | ----------------------------------- |
| $s_i^{(t)}$ | $C_t$       | 细胞状态 (cell state)               |
| $f_i^{(t)}$ | $f_t$       | 遗忘门 (forget gate)                |
| $g_i^{(t)}$ | $i_t$       | 输入门/外部门 (input/external gate) |
| $q_i^{(t)}$ | $o_t$       | 输出门 (output gate)                |
| $h_i^{(t)}$ | $h_t$       | 隐藏状态输出 (hidden state)         |

> ⚠️ **符号差异：** 教科书用 $s$ 表示细胞状态，$g$ 表示输入门。Slides 用 $C$ 表示细胞状态，$i$ 表示输入门。考试以 Slides 为准。

### 5.3 为什么加法路径有效？

细胞状态更新关键公式 (对应 Slides 的 $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$):

$$s_i^{(t)} = f_i^{(t)} s_i^{(t-1)} + g_i^{(t)} (\text{new input})$$

计算梯度 $\frac{\partial s_i^{(t)}}{\partial s_i^{(t-1)}}$：

$$\frac{\partial s_i^{(t)}}{\partial s_i^{(t-1)}} = f_i^{(t)}$$

> 📐 **推导 (tutorial 补充)：**
>
> 如果遗忘门 $f_i^{(t)} \approx 1$（"完全保留"），则:
>
> $$\frac{\partial s_i^{(T)}}{\partial s_i^{(1)}} = \prod_{t=2}^{T} f_i^{(t)} \approx 1^{T-1} = 1$$
>
> 梯度**恒为 1**——完美传递！
>
> 对比 vanilla RNN（§4）：
>
> $$\frac{\partial h^{(T)}}{\partial h^{(1)}} = \prod_{t=2}^{T} W^\top \cdot \text{diag}(\tanh') \quad \to \quad \text{指数衰减}$$
>
> 这就是 LSTM 解决梯度消失的数学原理：用**逐元素乘法+加法**替代了**矩阵乘法+非线性激活**。

> 🔑 **Greff et al. (2015) 实验发现：遗忘门是 LSTM 中最关键的组件。** Jozefowicz et al. (2015) 发现将遗忘门偏置初始化为 1（让初始 $f_t \approx 1$），LSTM 性能等同于最佳变体。
>
> 📚 Ref: Goodfellow §10.10, 最后一段

### 5.4 自循环权重的上下文化

> ⚠️ **Slides 未覆盖的洞察 (Goodfellow §10.10.1)：**
>
> LSTM 的核心贡献不仅是引入自循环 (self-loop)——leaky units 也有自循环。**关键区别**是：LSTM 的自循环权重（遗忘门 $f_t$）是**上下文相关的**——它由当前输入和上一隐藏状态动态计算，而非固定常数。
>
> 这意味着：即使 LSTM 的参数固定，积分的时间尺度 (time scale of integration) 也会根据输入序列**动态变化** (Gers et al., 2000)。

**§4 到 §5 的过渡：** §4 证明了乘法链导致梯度消失是不可避免的。LSTM 的回答是：**不要试图修复乘法链——绕开它！** 引入一条平行的加法路径（细胞状态），让梯度可以"走高速公路"。

---

## §6 GRU：LSTM 的简化变体 (GRU: A Simpler Alternative)

> 📚 Ref: Goodfellow §10.10.2, Eq. 10.45–10.47

### 6.1 设计动机

LSTM 有 3 个门 + 2 个状态，参数量较大。Cho et al. (2014) 提出的 GRU 简化了这个设计：

**GRU 更新方程 (Goodfellow Eq. 10.45):**

$$h_i^{(t)} = u_i^{(t-1)} h_i^{(t-1)} + (1 - u_i^{(t-1)}) \sigma\left(b_i + \sum_j U_{i,j} x_j^{(t-1)} + \sum_j W_{i,j} r_j^{(t-1)} h_j^{(t-1)}\right) \tag{Goodfellow Eq. 10.45}$$

其中 $u$ 是**更新门** (update gate)，$r$ 是**重置门** (reset gate)。

### 6.2 与 LSTM 的关键差异

| 方面            | LSTM                                | GRU                                                            |
| --------------- | ----------------------------------- | -------------------------------------------------------------- |
| 门数量          | 3（遗忘、输入、输出）               | 2（更新、重置）                                                |
| 状态            | $C_t$（细胞）+ $h_t$（隐藏）        | 只有 $h_t$                                                     |
| 遗忘/输入的关系 | **独立**（$f_t$ 和 $i_t$ 各自计算） | **耦合**（$u_t$ 同时控制保留和更新：保留 $u_t$，更新 $1-u_t$） |
| 参数量          | 约 $4 \times n^2$（4 组权重）       | 约 $3 \times n^2$（3 组权重）                                  |

> 🔑 **GRU 的核心简化：** 用一个更新门 $u_t$ 同时控制"遗忘多少"和"更新多少"——$u_t$ 越大越保留旧状态，$1 - u_t$ 越大越使用新信息。LSTM 中这两个功能是**独立控制**的。

> ⚠️ **Slides 未覆盖的实验结论 (Goodfellow §10.10.2)：** Greff et al. (2015) 和 Jozefowicz et al. (2015) 发现，**没有一种变体能在所有任务上同时超越 LSTM 和 GRU**——选择取决于具体任务。

---

## 📚 参考索引

| 教程章节         | 教科书来源                          | 核心内容                   | Slides 覆盖？                    |
| ---------------- | ----------------------------------- | -------------------------- | -------------------------------- |
| §1 展开计算图    | Goodfellow §10.1 Eq. 10.1–10.7      | 递归→链，参数共享          | ⚠️ 部分（提到展开但未推导）      |
| §2 前向传播      | Goodfellow §10.2 Eq. 10.8–10.14     | RNN 具体公式 ($U$,$W$,$V$) | ⚠️ 简化版（只写了 $W_x$, $W_h$） |
| §3 BPTT 推导     | Goodfellow §10.2.2 Eq. 10.17–10.25  | 梯度逐时间步传播           | ❌ 只给了结论                    |
| §4 梯度消失证明  | Goodfellow §10.7 Eq. 10.36–10.39    | 特征值分解→指数衰减        | ❌ 只给了直觉                    |
| §5 LSTM 设计哲学 | Goodfellow §10.10.1 Eq. 10.40–10.44 | 加法路径+动态时间尺度      | ⚠️ 给了公式但未解释设计原因      |
| §6 GRU           | Goodfellow §10.10.2 Eq. 10.45–10.47 | 简化 LSTM，耦合门          | ⚠️ 只提到了对比表                |

---

> 📖 **Storyline 链接：** 本教程的宏观故事线见 [week4_rnn_storyline.md](week4_rnn_storyline.md)——从"金鱼"(FFN) 到"大象"(LSTM) 的记忆进化。
