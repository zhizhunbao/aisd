# Week 4: RNN & LSTM — 概念速查

> **Source:** slides `04_CST8506_RNN.pdf` + quizzes3 + lab4 code
> **Scope:** FFN Review, Time Series, RNN, BPTT, Vanishing Gradient, LSTM, Loss Functions
> **See also:** [week4_rnn_math.md](week4_rnn_math.md) (公式+手算) | [week4_rnn_code.md](week4_rnn_code.md) (代码)

---

## FFN vs RNN

### 📖 Definition

- **FFN (Feed Forward Network, 前馈网络):** neural network where information flows only in one direction (input → hidden → output), no loops or cycles
- **RNN (Recurrent Neural Network, 循环神经网络):** neural network that uses previous hidden states as part of current input, enabling memory of past inputs
- **Sequential Data (序列数据):** data where order matters — each data point depends on prior context (text, audio, time series)

### 💡 Key Points

- 💡 FFN treats each input independently — no memory of past inputs ("goldfish brain")
- 💡 RNN introduces feedback loop: hidden state $h_{t-1}$ feeds into next step as additional input
- 💡 RNN processes inputs **one at a time** (not all at once), building memory incrementally

### ⚠️ Traps

- ⚠️ FFN CANNOT process sequential data — it has NO memory mechanism
- ⚠️ RNN is NOT just "a deeper FFN" — the key difference is the **recurrent loop** (hidden state feeds back)

### 📊 Compare

| Feature          | FFN                     | RNN                                |
| ---------------- | ----------------------- | ---------------------------------- |
| Information Flow | Forward only            | Forward + recurrent loop           |
| Memory           | None                    | Hidden state carries history       |
| Input Processing | All at once             | One at a time (sequential)         |
| Weight Sharing   | No (each layer has own) | Yes (same W across all time steps) |
| Use Case         | Image classification    | Text, speech, time series          |

---

## Sequence Data Applications

### 📖 Definition

- **Speech Recognition (语音识别):** converting audio clips to text
- **Sentiment Analysis (情感分析):** mapping text sequence to a rating/label
- **Machine Translation (机器翻译):** converting text from one language to another
- **Image Captioning (图像描述):** generating a text description from an image (CNN → RNN)
- **Time Series Forecasting (时间序列预测):** predicting future values based on historical trends

### 💡 Key Points

- 💡 All sequence tasks share one property: **current output depends on past inputs**
- 💡 Image captioning combines CNN (feature extraction) with RNN (sequence generation)

---

## RNN Input-Output Types

### 📖 Definition

- **One-to-One (单对单):** single input → single output — standard classification (same as FFN)
- **One-to-Many (单对多):** single input → sequence output — image captioning
- **Many-to-One (多对单):** sequence input → single output — sentiment analysis
- **Many-to-Many (多对多):** sequence input → sequence output — machine translation, video captioning

### ⚠️ Traps

- ⚠️ One-to-One is essentially a feed-forward network — no sequential processing needed
- ⚠️ Know the example for each type (exam favorite): captioning=1-to-N, sentiment=N-to-1, translation=N-to-M

### 📊 Compare

| Type         | Input    | Output   | Example             |
| ------------ | -------- | -------- | ------------------- |
| One-to-One   | Single   | Single   | Classification      |
| One-to-Many  | Single   | Sequence | Image Captioning    |
| Many-to-One  | Sequence | Single   | Sentiment Analysis  |
| Many-to-Many | Sequence | Sequence | Machine Translation |

---

## Time Series

### 📖 Definition

- **Time Series (时间序列):** sequence of data points collected at specific time intervals — X-axis = time, Y-axis = measured variable
- **Trend (趋势):** long-term direction — generally going up, down, or staying flat
- **Seasonal (季节性):** patterns that repeat over a **fixed, known** period (e.g., 12 months)
- **Cycle (周期):** long-term fluctuations that repeat but at **irregular, unknown** intervals
- **Noise/Residual (噪声/残差):** random fluctuations that cannot be explained by trend, seasonal, or cycle
- **Stationarity (平稳性):** statistical properties (mean, variance) do NOT change over time
- **Non-Stationary (非平稳):** statistical properties change over time — needs preprocessing before modeling

### 💡 Key Points

- 💡 Time series decomposition: Original = Trend + Seasonal + Cycle + Noise
- 💡 RNN assumes patterns exist in the data — non-stationary data needs differencing/detrending first

### ⚠️ Traps

- ⚠️ **Seasonal ≠ Cycle!** Seasonal = fixed period (every December). Cycle = variable period (economic cycle 3–7 years)
- ⚠️ Air Passengers dataset is **non-stationary** — mean and variance change with time
- ⚠️ "Additive" decomposition when seasonal amplitude stays constant; "Multiplicative" when it grows with trend

---

## RNN Architecture

### 📖 Definition

- **Hidden State (隐藏状态):** $h_t$ — the "memory" vector that carries information from past time steps
- **Weight Sharing (权重共享):** RNN uses the SAME weight matrices $W_x$, $W_h$ at EVERY time step
- **Unrolling/Unfolding (展开):** conceptually "unrolling" the RNN loop into a chain of copies, one per time step

### 💡 Key Points

- 💡 RNN core equation: $h_t = f(W_x \cdot x_t + W_h \cdot h_{t-1})$ where $f$ = tanh
- 💡 Weight sharing means: regardless of sequence length, parameter count stays FIXED
- 💡 Same weights enable **generalization** to sequence lengths not seen during training

### ⚠️ Traps

- ⚠️ Weights $W_x$ and $W_h$ are shared — NOT different at each time step
- ⚠️ $f$ is typically **tanh** (not sigmoid, not ReLU) for vanilla RNN hidden state

---

## Backpropagation Through Time (BPTT)

### 📖 Definition

- **Backpropagation (反向传播):** algorithm for computing gradients by applying chain rule layer by layer
- **BPTT (Backpropagation Through Time, 时序反向传播):** extension of backprop for RNNs — gradients flow backward through ALL time steps
- **Gradient Descent (梯度下降):** weight update rule: $W = W - \alpha \cdot \frac{\partial L}{\partial W}$

### 💡 Key Points

- 💡 BPTT steps: (1) Unroll RNN across time, (2) Forward pass — compute outputs & losses, (3) Backward pass — gradients flow back through time
- 💡 Because weights are **shared**, gradient = **SUM** of contributions from all time steps: $\frac{\partial L}{\partial W} = \sum_t \frac{\partial L_t}{\partial W}$
- 💡 Runtime and memory are both $O(\tau)$ where $\tau$ = sequence length

### ⚠️ Traps

- ⚠️ BPTT requires **multiplying gradients through many time steps** — this is where vanishing/exploding gradients originate
- ⚠️ Chain rule in BPTT: each step multiplies by $\frac{\partial h_t}{\partial h_{t-1}}$ which involves $W_h$ and $\tanh'$

---

## Vanishing Gradient Problem

### 📖 Definition

- **Vanishing Gradient (梯度消失):** gradients become extremely small as they propagate backward through many time steps, causing early layers to receive almost no weight updates
- **Exploding Gradient (梯度爆炸):** gradients become extremely large — rarer but destructive
- **Gradient Clipping (梯度裁剪):** technique to cap gradients at a maximum value to prevent explosion

### 💡 Key Points

- 💡 Root cause: tanh derivative is in (0, 1] — multiplying many values < 1 exponentially shrinks the product
- 💡 Example: $0.5^{100} \approx 10^{-30}$ — gradient essentially becomes zero
- 💡 Consequence: RNN **cannot learn long-term dependencies** — only learns short-range patterns

### ⚠️ Traps

- ⚠️ Vanishing gradient is a **mathematical certainty** for long sequences with tanh — NOT just "possible"
- ⚠️ sigmoid makes it WORSE (max derivative = 0.25 vs tanh max = 1)
- ⚠️ 5 solutions: (1) Gated architectures (LSTM/GRU), (2) Gradient clipping, (3) ReLU activation, (4) Layer/Batch normalization, (5) Shorter sequences

---

## Long Short-Term Memory (LSTM)

### 📖 Definition

- **LSTM (Long Short-Term Memory, 长短期记忆网络):** special RNN variant with 3 gates + cell state, designed to learn long-term dependencies
- **Cell State (细胞状态):** $C_t$ — the "highway" for information to flow across time steps with minimal modification
- **Forget Gate (遗忘门):** $f_t$ — decides what old information to DISCARD from cell state (0 = forget, 1 = keep)
- **Input Gate (输入门):** $i_t$ — decides what NEW information to WRITE into cell state
- **Candidate Values (候选值):** $\tilde{C}_t$ — the actual new content proposed for writing
- **Output Gate (输出门):** $o_t$ — decides what information to OUTPUT from cell state as hidden state $h_t$

### 💡 Key Points

- 💡 LSTM core innovation: cell state update uses **addition** (not matrix multiplication) → gradients don't vanish
- 💡 Cell state formula: $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$ — only element-wise multiply + add
- 💡 When $f_t \approx 1$, information passes through unchanged for many time steps ("gradient highway")
- 💡 Introduced by **Hochreiter & Schmidhuber (1997)**
- 💡 All 3 gates use **sigmoid** (output 0–1), candidate uses **tanh** (output -1 to 1)

### ⚠️ Traps

- ⚠️ LSTM has TWO states: cell state $C_t$ (long-term) AND hidden state $h_t$ (short-term output)
- ⚠️ Gates use **sigmoid** (not tanh) — because gates need 0-to-1 range for "how much to allow"
- ⚠️ $\odot$ means element-wise (Hadamard) product — NOT matrix multiplication
- ⚠️ LSTM solves vanishing gradient through **additive** cell state update, NOT by removing multiplication entirely

### 📊 Compare

| Feature          | Vanilla RNN           | LSTM                          |
| ---------------- | --------------------- | ----------------------------- |
| Gates            | None                  | 3 (Forget, Input, Output)     |
| States           | $h_t$ only            | $C_t$ (cell) + $h_t$ (hidden) |
| Long-term Memory | ❌ Vanishing gradient | ✅ Cell state highway         |
| Selective Forget | ❌ Cannot control     | ✅ Forget gate                |
| Selective Write  | ❌ Cannot control     | ✅ Input gate                 |
| Parameters       | Fewer                 | ~4× more (4 weight matrices)  |
| Gradient Path    | Multiplicative chain  | Additive shortcut             |

---

## LSTM vs GRU

### 📖 Definition

- **GRU (Gated Recurrent Unit, 门控循环单元):** simplified LSTM variant with 2 gates (update + reset) and only 1 state ($h_t$)
- **Update Gate (更新门):** controls how much of past state to keep (combines LSTM's forget + input gates)
- **Reset Gate (重置门):** controls how much of past state to use when computing new candidate

### 📊 Compare

| Feature        | LSTM                      | GRU               |
| -------------- | ------------------------- | ----------------- |
| Gates          | 3 (forget, input, output) | 2 (update, reset) |
| States         | 2 ($C_t$ and $h_t$)       | 1 ($h_t$ only)    |
| Parameters     | More                      | Fewer (~25% less) |
| Training Speed | Slower                    | Faster            |
| Long Sequence  | Slightly better           | Slightly worse    |

---

## Loss Functions

### 📖 Definition

- **Loss Function (损失函数):** method to quantify the error between model output and target — also called cost function or error function
- **MSE (Mean Squared Error, 均方误差):** average of squared differences — penalizes large errors more
- **MAE (Mean Absolute Error, 平均绝对误差):** average of absolute differences — robust to outliers
- **MBE (Mean Bias Error, 平均偏差误差):** average of raw differences (can be negative) — shows directional bias
- **Cross Entropy (交叉熵):** loss for classification — measures difference between predicted and true probability distributions
- **Binary Cross Entropy (二元交叉熵):** CE for 2-class problems (labels 0/1)
- **Categorical Cross Entropy (分类交叉熵):** CE for multi-class with one-hot encoded labels
- **Sparse Categorical Cross Entropy (稀疏分类交叉熵):** CE for multi-class with integer labels
- **Hinge Loss (合页损失):** loss for maximum-margin classifiers (SVM) — requires labels -1/+1

### 💡 Key Points

- 💡 MSE is default for regression (e.g., temperature prediction in Lab4)
- 💡 Cross Entropy is default for classification (e.g., next word prediction)
- 💡 MAE is more robust to outliers than MSE (no squaring)
- 💡 MBE can show positive/negative bias but positives cancel negatives → less accurate

### ⚠️ Traps

- ⚠️ Hinge Loss requires labels **-1 and +1**, NOT 0 and 1!
- ⚠️ MSE penalizes large errors **quadratically** — one big outlier can dominate
- ⚠️ Cross Entropy outputs are **probabilities** (after softmax), Hinge Loss uses **raw scores**
- ⚠️ Categorical CE = one-hot labels, Sparse Categorical CE = integer labels — same math, different format

### 📊 Compare

| Loss Function | Task           | Formula Essence       | Key Property           |
| ------------- | -------------- | --------------------- | ---------------------- | --- | ------------------ |
| MSE           | Regression     | $(y - \hat{y})^2$     | Sensitive to outliers  |
| MAE           | Regression     | $                     | y - \hat{y}            | $   | Robust to outliers |
| Cross Entropy | Classification | $-y\log(\hat{y})$     | For probability output |
| Hinge Loss    | Classification | $\max(0, 1-y\hat{y})$ | For SVM, labels ±1     |
