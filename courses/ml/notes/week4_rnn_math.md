# Week 4: RNN & LSTM — 数学公式 + 手算

> **Source:** slides `04_CST8506_RNN.pdf` + lab4 code
> **Scope:** 数学基础 → RNN 公式 → LSTM 门公式 → BPTT 梯度 → 损失函数
> **See also:** [week4_rnn_cheatsheet.md](week4_rnn_cheatsheet.md) (概念速查) | [week4_rnn_code.md](week4_rnn_code.md) (代码)
> **阅读建议：** 先看本文件的"数学基础"部分，再看 [week4_rnn_tutorial.md](week4_rnn_tutorial.md) 的推导会更轻松

---

## ★ 数学基础 (Math Foundations)

> 📌 这一部分是理解 RNN/LSTM 的**前置知识**。如果你已经熟悉 sigmoid、tanh、链式法则，可以跳到"RNN 核心公式"。
>
> 📌 This section covers **prerequisites** for understanding RNN/LSTM. Skip to "RNN Core Formula" if you already know sigmoid, tanh, and chain rule.

### 📐 Sigmoid 函数 (Sigmoid Function)

$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

| 性质（中文） | Property (English) | 值 (Value)                              |
| ------------ | ------------------ | --------------------------------------- |
| 输出范围     | Output range       | **(0, 1)**                              |
| 导数公式     | Derivative formula | $\sigma'(x) = \sigma(x)(1 - \sigma(x))$ |
| 导数范围     | Derivative range   | **(0, 0.25]**                           |
| 最大导数位置 | Max derivative at  | $x=0$ 时, $\sigma'(0) = 0.25$           |

> 🔑 为什么 LSTM 的门用 sigmoid？因为输出 (0,1) 正好当"开关"——0 = 关，1 = 开。
>
> 🔑 Why do LSTM gates use sigmoid? Output (0,1) acts as a "switch" — 0 = off, 1 = on.

#### 📝 手算：计算 sigmoid 值 (Hand calc: compute sigmoid values)

$$\sigma(0) = \frac{1}{1 + e^0} = \frac{1}{2} = \mathbf{0.5}$$

$$\sigma(1.5) = \frac{1}{1 + e^{-1.5}} = \frac{1}{1 + 0.223} = \frac{1}{1.223} \approx \mathbf{0.818}$$

$$\sigma(-2) = \frac{1}{1 + e^{2}} = \frac{1}{1 + 7.389} = \frac{1}{8.389} \approx \mathbf{0.119}$$

> 💡 记忆技巧：$\sigma(0) = 0.5$，正数越大越接近 1，负数越大越接近 0。
>
> 💡 Memory tip: $\sigma(0) = 0.5$, larger positive → closer to 1, larger negative → closer to 0.

### 📐 Tanh 函数 (Tanh Function)

$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$$

| 性质（中文） | Property (English) | 值 (Value)                   |
| ------------ | ------------------ | ---------------------------- |
| 输出范围     | Output range       | **(-1, 1)**                  |
| 导数公式     | Derivative formula | $\tanh'(x) = 1 - \tanh^2(x)$ |
| 导数范围     | Derivative range   | **(0, 1]**                   |
| 最大导数位置 | Max derivative at  | $x=0$ 时, $\tanh'(0) = 1$    |
| 零中心       | Zero-centered      | ✅ 是 (Yes)                  |

> 🔑 为什么 RNN 隐藏状态用 tanh 而不是 sigmoid？
>
> | 对比（中文） | Comparison (English) | sigmoid       | tanh          |
> | ------------ | -------------------- | ------------- | ------------- |
> | 输出范围     | Output range         | (0, 1)        | (-1, 1)       |
> | 零中心       | Zero-centered        | ❌            | ✅            |
> | 最大导数     | Max derivative       | 0.25          | 1             |
> | 梯度消失速度 | Vanishing speed      | 更快 (faster) | 较慢 (slower) |
>
> tanh 以 0 为中心，梯度传播更稳定。但两者导数都 < 1，连乘必然消失。
>
> tanh is centered at 0, making gradient propagation more stable. But both have derivatives < 1, so the product inevitably vanishes.

#### 📝 手算：计算 tanh 值 (Hand calc: compute tanh values)

$$\tanh(0) = \frac{1 - 1}{1 + 1} = \mathbf{0}$$

$$\tanh(1.5) = \frac{e^{1.5} - e^{-1.5}}{e^{1.5} + e^{-1.5}} = \frac{4.482 - 0.223}{4.482 + 0.223} = \frac{4.259}{4.705} \approx \mathbf{0.905}$$

> 💡 记忆技巧：$\tanh(0) = 0$，$\tanh(\pm 2)$ 已经很接近 $\pm 1$ 了。
>
> 💡 Memory tip: $\tanh(0) = 0$, $\tanh(\pm 2)$ is already very close to $\pm 1$.

### 📐 链式法则 (Chain Rule)

反向传播的数学基础。理解 BPTT 必须先理解链式法则。

The mathematical foundation of backpropagation. Must understand chain rule before BPTT.

- **单层情况 (Single layer):** 如果 $y = f(g(x))$，则:

$$\frac{dy}{dx} = \frac{dy}{dg} \cdot \frac{dg}{dx}$$

- **多层情况（神经网络） (Multi-layer / Neural Network):**

$$x \to f_1 \to f_2 \to f_3 \to \cdots \to f_n \to \text{Loss}$$

$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial f_n} \cdot \frac{\partial f_n}{\partial f_{n-1}} \cdots \frac{\partial f_2}{\partial f_1} \cdot \frac{\partial f_1}{\partial x}$$

> 🔑 **关键观察：** 这是一长串**乘法**！如果每个 $\frac{\partial f_i}{\partial f_{i-1}}$ 都 < 1，乘积会**指数级衰减**。
>
> 🔑 **Key insight:** This is a long chain of **multiplications**! If each $\frac{\partial f_i}{\partial f_{i-1}} < 1$, the product **decays exponentially**.

#### 📝 手算：链式法则 (Hand calc: chain rule)

**题目 (Problem):** $y = (3x + 2)^2$，求 $\frac{dy}{dx}$ 在 $x = 1$ 时的值。

Find $\frac{dy}{dx}$ at $x = 1$.

**Step 1:** 令 $u = 3x + 2$，则 $y = u^2$。
Let $u = 3x + 2$, then $y = u^2$.

**Step 2:** 链式法则 / Chain rule:
$$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx} = 2u \cdot 3 = 6u = 6(3x+2)$$

**Step 3:** 代入 $x = 1$: $\frac{dy}{dx} = 6(3 \times 1 + 2) = 6 \times 5 = \mathbf{30}$

### 📐 加法 vs 乘法：梯度传播的命运 (Additive vs Multiplicative: Gradient Fate)

> 🔑 **这是理解"为什么梯度消失"和"LSTM 如何解决"的最关键数学基础！**
>
> 🔑 **This is THE most critical math foundation for understanding vanishing gradients and LSTM's solution!**

- **乘法路径 (Multiplicative path):** 信号经过 $n$ 步，每步乘以系数 $\alpha$:

$$s_n = \alpha^n \cdot s_0$$

| $\alpha$ 的值 (Value) | $\alpha^{100}$ 的结果 (Result) | 含义（中文） | Meaning (English)          |
| --------------------- | ------------------------------ | ------------ | -------------------------- |
| 0.9                   | $\approx 2.7 \times 10^{-5}$   | 信号几乎消失 | Signal nearly vanishes     |
| 1.0                   | $= 1$                          | 信号完美保持 | Signal perfectly preserved |
| 1.1                   | $\approx 13780$                | 信号爆炸     | Signal explodes            |

- **加法路径 (Additive path):** 信号经过 $n$ 步，每步**加上**增量 $\delta$:

$$s_n = s_0 + n \cdot \delta$$

无论传多少步，原始信号 $s_0$ **始终保留**！
Regardless of steps, original signal $s_0$ **is always preserved**!

- **梯度视角 (Gradient perspective):**

$$\frac{\partial s_n}{\partial s_0} = \begin{cases} \alpha^n & \text{乘法路径 (multiplicative) → 指数衰减 (exponential decay)} \\ 1 & \text{加法路径 (additive) → 完美传递 (perfect transfer)} \end{cases}$$

> 🔑 **RNN 的悲剧：** $h_t = \tanh(W_h \cdot h_{t-1} + W_x \cdot x_t)$ 是**乘法路径**（$W_h$ 矩阵乘法 + tanh 导数 < 1）→ 梯度**必然消失**。
>
> 🔑 **LSTM 的解决：** $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$ 是**加法路径**（逐元素乘+加法）→ 当 $f_t \approx 1$ 时，梯度**恒为 1**。
>
> 🔑 **RNN's tragedy:** The hidden state update is a **multiplicative path** → gradients **inevitably vanish**.
>
> 🔑 **LSTM's solution:** Cell state update is an **additive path** → when $f_t \approx 1$, gradients **stay at 1**.

---

## RNN 核心公式 (RNN Core Formula)

### 📐 公式 (Formula)

- **RNN 隐藏状态更新 (Hidden State Update):**

$$h_t = f(W_x \cdot x_t + W_h \cdot h_{t-1})$$

| 符号      | 含义（中文）                   | Meaning (English)                    | 温度预测例子 |
| --------- | ------------------------------ | ------------------------------------ | ------------ |
| $h_t$     | 当前时间步的隐藏状态（"记忆"） | Hidden state at time $t$             | 本周记忆     |
| $x_t$     | 当前时间步的输入               | Input at time $t$                    | 本周温度     |
| $h_{t-1}$ | 上一时间步的隐藏状态           | Previous hidden state                | 上周记忆     |
| $W_x$     | 输入权重矩阵                   | Weight matrix for input              | —            |
| $W_h$     | 隐藏状态权重矩阵               | Weight matrix for hidden state       | —            |
| $f$       | 激活函数（通常 tanh）          | Activation function (typically tanh) | —            |

> 🔑 **关键：** $W_x$ 和 $W_h$ 在**所有时间步共享**——不管序列多长，参数量固定。
>
> 🔑 **Key:** $W_x$ and $W_h$ are **shared across ALL time steps** — parameter count is fixed regardless of sequence length.

---

## BPTT 梯度公式 (BPTT Gradient Formulas)

### 📐 公式 (Formula)

- **梯度下降权重更新 (Gradient Descent Weight Update):**

$$W = W - \alpha \cdot \frac{\partial L}{\partial W}$$

$\alpha$ = 学习率 (learning rate), $L$ = 损失函数 (loss function)

- **链式法则（多层情况） (Chain Rule — Multi-layer):**

$$\frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial \hat{y}_2} \cdot \frac{\partial \hat{y}_2}{\partial \hat{y}_1} \cdot \frac{\partial \hat{y}_1}{\partial W_1}$$

- **BPTT 总梯度（权重共享导致求和） (BPTT Total Gradient — Sum Due to Weight Sharing):**

$$\frac{\partial L}{\partial W} = \sum_t \frac{\partial L_t}{\partial W}$$

> 所有时间步的梯度贡献**求和**，因为同一个 $W$ 影响所有时间步。
>
> Gradient contributions from all time steps are **summed** because the same $W$ affects all time steps.

- **梯度消失的数学原因 (Mathematical Cause of Vanishing Gradient):**

从 $h_{100}$ 传回 $h_1$ 的梯度 (gradient from $h_{100}$ back to $h_1$):

$$\frac{\partial L}{\partial h_1} = \frac{\partial L}{\partial h_{100}} \cdot \prod_{t=2}^{100} \frac{\partial h_t}{\partial h_{t-1}}$$

每一步 $\frac{\partial h_t}{\partial h_{t-1}}$ 涉及 $\tanh'$，而 $\tanh' \in (0, 1]$。
Each step involves $\tanh'$, and $\tanh' \in (0, 1]$.

$$0.5^{100} \approx 10^{-30} \quad \leftarrow \text{梯度消失！(Gradient vanished!)}$$

### 📝 手算 (Hand Calc)

- **梯度消失量化例题 (Vanishing Gradient Quantification):**

  **题目设置 (Problem Setup):** 假设 tanh 导数平均值 = 0.5，序列长度 = 10 步。
  Suppose average tanh derivative = 0.5, sequence length = 10 steps.

  **Step 1: 计算梯度缩放因子 (Compute gradient scaling factor)**

  $$\prod_{t=1}^{10} 0.5 = 0.5^{10} = \frac{1}{1024} \approx 9.77 \times 10^{-4}$$

  **Step 2: 解释 (Interpretation)**

  梯度只剩原来的 **0.1%**——权重几乎无法更新，网络学不到长距离依赖。

  Only **0.1%** of the gradient remains — weights barely update, network cannot learn long-range dependencies.

---

## LSTM 门公式 (LSTM Gate Formulas)

### 📐 公式 (Formula)

- **Step 1: 遗忘门——决定丢弃什么 (Forget Gate — What to Discard):**

$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

| 符号             | 含义（中文）                            | Meaning (English)                                        |
| ---------------- | --------------------------------------- | -------------------------------------------------------- |
| $f_t$            | 遗忘门输出（0 到 1 之间，每个维度独立） | Forget gate output (0 to 1, per dimension)               |
| $\sigma$         | Sigmoid 激活函数                        | Sigmoid activation                                       |
| $[h_{t-1}, x_t]$ | 上一隐藏状态和当前输入的拼接            | Concatenation of previous hidden state and current input |
| $b_f$            | 遗忘门的偏置                            | Forget gate bias                                         |

> ⚠️ $f_t = 0$ 表示**完全丢弃**，$f_t = 1$ 表示**完全保留**。
>
> ⚠️ $f_t = 0$ means **completely forget**, $f_t = 1$ means **completely keep**.

- **Step 2: 输入门 + 候选值——决定写入什么 (Input Gate + Candidate — What to Write):**

$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$

$$\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$$

| 符号          | 含义（中文）               | Meaning (English)                         |
| ------------- | -------------------------- | ----------------------------------------- |
| $i_t$         | 输入门（哪些维度需要更新） | Input gate (which dimensions to update)   |
| $\tilde{C}_t$ | 候选值（新信息的内容）     | Candidate values (the actual new content) |

> 输入门用 sigmoid（控制"写多少"），候选值用 tanh（生成"写什么内容"，范围 -1 到 1）。
>
> Input gate uses sigmoid (controls "how much to write"), candidate uses tanh (generates "what content", range -1 to 1).

- **Step 3: 更新细胞状态 (Update Cell State):**

$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

| 符号                    | 含义（中文）                    | Meaning (English)                              |
| ----------------------- | ------------------------------- | ---------------------------------------------- |
| $f_t \odot C_{t-1}$     | 保留的旧记忆（旧状态 × 遗忘门） | Retained old memory (old state × forget gate)  |
| $i_t \odot \tilde{C}_t$ | 写入的新信息（候选值 × 输入门） | Written new info (candidate × input gate)      |
| $\odot$                 | 逐元素乘法（Hadamard 积）       | Element-wise multiplication (Hadamard product) |

> 🔑 **这就是 LSTM 解决梯度消失的关键！** 细胞状态更新只有逐元素乘法和**加法**——没有矩阵乘法。当 $f_t \approx 1$ 时，信息几乎无损地穿越多个时间步。
>
> 🔑 **This is how LSTM solves vanishing gradient!** Cell state update uses only element-wise multiply and **addition** — no matrix multiplication. When $f_t \approx 1$, information passes through nearly losslessly across many time steps.

- **Step 4: 输出门 (Output Gate):**

$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$

$$h_t = o_t \odot \tanh(C_t)$$

| 符号  | 含义（中文）               | Meaning (English)                     |
| ----- | -------------------------- | ------------------------------------- |
| $o_t$ | 输出门（控制输出哪些信息） | Output gate (controls what to output) |
| $h_t$ | 最终隐藏状态输出           | Final hidden state output             |

> $h_t$ 同时用于：(1) 当前时间步的预测输出，(2) 传递给下一个时间步。
>
> $h_t$ is used for both: (1) prediction at current time step, (2) passed to next time step.

### 📝 手算 (Hand Calc)

- **LSTM 单步计算例题 (LSTM Single Step Example):**

  **题目设置 (Problem Setup):** 1 维 LSTM，$h_{t-1} = 0.5$, $x_t = 1.0$, $C_{t-1} = 0.8$。假设所有权重 = 1，偏置 = 0。

  1-dimensional LSTM, $h_{t-1} = 0.5$, $x_t = 1.0$, $C_{t-1} = 0.8$. Assume all weights = 1, biases = 0.

  **Step 1: 遗忘门 (Forget Gate)**

  $$f_t = \sigma(1 \times 0.5 + 1 \times 1.0 + 0) = \sigma(1.5) \approx \mathbf{0.818}$$

  **Step 2: 输入门 + 候选 (Input Gate + Candidate)**

  $$i_t = \sigma(1 \times 0.5 + 1 \times 1.0 + 0) = \sigma(1.5) \approx \mathbf{0.818}$$

  $$\tilde{C}_t = \tanh(1 \times 0.5 + 1 \times 1.0 + 0) = \tanh(1.5) \approx \mathbf{0.905}$$

  **Step 3: 更新细胞状态 (Update Cell State)**

  $$C_t = 0.818 \times 0.8 + 0.818 \times 0.905 = 0.654 + 0.740 = \mathbf{1.394}$$

  **Step 4: 输出门 (Output Gate)**

  $$o_t = \sigma(1.5) \approx 0.818$$

  $$h_t = 0.818 \times \tanh(1.394) = 0.818 \times 0.884 = \mathbf{0.723}$$

  **结果 (Result):** 细胞状态从 0.8 增长到 1.394（积累了新信息），隐藏状态输出 0.723。

  Cell state grew from 0.8 to 1.394 (accumulated new info), hidden state output is 0.723.

---

## 损失函数 (Loss Functions)

### 📐 公式 (Formula)

- **均方误差 (Mean Squared Error / MSE):**

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

$y_i$ = 实际值 (actual value), $\hat{y}_i$ = 预测值 (predicted value), $n$ = 样本数 (sample count)

- **平均绝对误差 (Mean Absolute Error / MAE):**

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n}|y_i - \hat{y}_i|$$

取绝对值，不取平方——对离群值更鲁棒。
Takes absolute difference, not squared — more robust to outliers.

- **平均偏差误差 (Mean Bias Error / MBE):**

$$\text{MBE} = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)$$

不取绝对值也不取平方——正负可能抵消，用于检测偏差方向。
No absolute value or square — positives and negatives may cancel out, used to detect bias direction.

- **交叉熵 (Cross Entropy):**

$$\text{CE} = -\sum_{i} y_i \cdot \log(\hat{y}_i)$$

$y_i$ = 真实分布（通常是 one-hot）(true distribution, usually one-hot), $\hat{y}_i$ = 预测概率 (predicted probabilities)

- **Hinge 损失 (Hinge Loss):**

$$\text{Hinge} = \max(0, 1 - y \cdot \hat{y})$$

$y \in \{-1, +1\}$（不是 0 和 1！）(NOT 0 and 1!), $\hat{y}$ = 模型原始输出（不是概率）(raw model output, NOT probability)

### 📝 手算 (Hand Calc)

- **MSE 计算例题 (MSE Calculation Example):**

  **题目设置 (Problem Setup):** 3 个样本，实际值 = [10, 12, 15]，预测值 = [11, 11, 14]

  3 samples, actual = [10, 12, 15], predicted = [11, 11, 14]

  **Step 1: 计算各差值的平方 (Compute squared differences)**

  $$(10-11)^2 = 1, \quad (12-11)^2 = 1, \quad (15-14)^2 = 1$$

  **Step 2: 求平均 (Average)**

  $$\text{MSE} = \frac{1 + 1 + 1}{3} = \mathbf{1.0}$$

- **MAE 计算例题 (MAE Calculation Example):**

  **使用相同数据 (Same data as above):**

  $$|10-11| = 1, \quad |12-11| = 1, \quad |15-14| = 1$$

  $$\text{MAE} = \frac{1 + 1 + 1}{3} = \mathbf{1.0}$$

  > 💡 这个例子中 MSE = MAE，因为所有误差都是 1。如果有一个大误差（如差值=5），MSE 会变成 $25/3 \approx 8.3$，而 MAE 只有 $5/3 \approx 1.67$——MSE 对大误差更敏感。
  >
  > In this case MSE = MAE because all errors are 1. With a large error (e.g., diff=5), MSE would be $25/3 \approx 8.3$ while MAE would be $5/3 \approx 1.67$ — MSE is more sensitive to large errors.

---

## 激活函数导数 (Activation Function Derivatives)

### 📐 公式 (Formula)

- **Sigmoid 导数 (Sigmoid Derivative):**

$$\sigma(x) = \frac{1}{1 + e^{-x}}, \quad \sigma'(x) = \sigma(x)(1 - \sigma(x))$$

最大导数 = 0.25（当 $x = 0$ 时）。
Maximum derivative = 0.25 (when $x = 0$).

- **Tanh 导数 (Tanh Derivative):**

$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}, \quad \tanh'(x) = 1 - \tanh^2(x)$$

最大导数 = 1（当 $x = 0$ 时）。
Maximum derivative = 1 (when $x = 0$).

> 🔑 这就是 RNN 用 tanh 而不用 sigmoid 的原因：tanh 的最大导数是 1（sigmoid 是 0.25），梯度衰减更慢。但只要导数 < 1，连乘必然消失。
>
> 🔑 This is why RNN uses tanh over sigmoid: tanh's max derivative is 1 (sigmoid is 0.25), gradient decays slower. But as long as derivative < 1, the product inevitably vanishes.

---

## 速查公式表 (Quick Formula Reference)

| 公式名称 (Name)                 | 公式 (Formula)                                                           | 关键参数 (Key Params)             |
| ------------------------------- | ------------------------------------------------------------------------ | --------------------------------- | --- | ---------------------- |
| RNN 隐藏状态 (RNN Hidden State) | $h_t = \tanh(W_x x_t + W_h h_{t-1})$                                     | $W_x$=输入权重, $W_h$=递归权重    |
| BPTT 总梯度 (BPTT Gradient)     | $\frac{\partial L}{\partial W} = \sum_t \frac{\partial L_t}{\partial W}$ | 所有时间步求和 (sum over all $t$) |
| LSTM 遗忘门 (Forget Gate)       | $f_t = \sigma(W_f[h_{t-1}, x_t] + b_f)$                                  | 输出 0–1，控制丢弃                |
| LSTM 输入门 (Input Gate)        | $i_t = \sigma(W_i[h_{t-1}, x_t] + b_i)$                                  | 输出 0–1，控制写入                |
| LSTM 候选值 (Candidate)         | $\tilde{C}_t = \tanh(W_C[h_{t-1}, x_t] + b_C)$                           | 输出 -1 到 1                      |
| LSTM 细胞状态 (Cell State)      | $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$                        | **加法路径**——梯度不消失          |
| LSTM 输出 (Output)              | $h_t = o_t \odot \tanh(C_t)$                                             | 同时用于预测和传递                |
| MSE                             | $\frac{1}{n}\sum(y-\hat{y})^2$                                           | 回归任务，对离群值敏感            |
| MAE                             | $\frac{1}{n}\sum                                                         | y-\hat{y}                         | $   | 回归任务，对离群值鲁棒 |
| Cross Entropy                   | $-\sum y_i\log(\hat{y}_i)$                                               | 分类任务                          |
| Hinge Loss                      | $\max(0, 1-y\hat{y})$                                                    | SVM，标签必须 ±1                  |
| Sigmoid                         | $\frac{1}{1+e^{-x}}$                                                     | 输出 (0,1)，最大导数 0.25         |
| Tanh                            | $\frac{e^x-e^{-x}}{e^x+e^{-x}}$                                          | 输出 (-1,1)，最大导数 1           |
