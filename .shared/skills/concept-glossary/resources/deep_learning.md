# Deep Learning (深度学习)

> This file grows automatically as new notes are written. Entries are alphabetical.

---

### Backpropagation Through Time, BPTT (时间反向传播)

**Tags:** `#rnn` `#gradient` `#training` `#ml-week4`

**📌 One-line Definition:**
> BPTT is the backpropagation algorithm applied to unrolled RNNs, where gradients are computed across all time steps and summed to update the shared weights.
>> BPTT是应用于展开RNN的反向传播算法，梯度在所有时间步上计算并求和以更新共享权重。

**💡 Intuition (直觉理解):**
> **The telephone game backward:** The error message at the end needs to travel back through every person (time step). Each person might distort it (multiply by < 1 or > 1), causing the message to vanish or explode.
>> **反向传话游戏：** 最后的错误消息需要通过每个人（时间步）传回。每个人可能扭曲它（乘以<1或>1），导致消息消失或爆炸。

**🔗 Related Concepts:**
→ see: Vanishing Gradient Problem (the main issue BPTT faces)
→ see: LSTM (addresses BPTT's limitations)

**📚 Appears In:**
- ML Week 4 §8 (Backpropagation and BPTT)

---

### Feed Forward Network, FFN (前馈网络)

**Tags:** `#architecture` `#basic` `#ml-week4`

**📌 One-line Definition:**
> A neural network where connections between nodes do NOT form a cycle. Information moves only forward: input → hidden → output, with no memory of previous inputs.
>> 一种神经网络，节点之间的连接不形成循环。信息只向前移动：输入 → 隐藏层 → 输出，没有对先前输入的记忆。

**💡 Intuition (直觉理解):**
> **Goldfish memory:** Each input is processed independently. If you feed the same input twice, you get the exact same output — the network has no "memory" of what it saw before.
>> **金鱼记忆：** 每个输入都独立处理。如果你两次输入相同的数据，你会得到完全相同的输出 — 网络对之前看到的没有"记忆"。

**⚖️ Compare:**
| Feature | FFN | RNN |
|---|---|---|
| Memory | None | Hidden state stores past |
| Input | Fixed-size | Sequential, variable |
| Use case | Image classification | Text, speech, time series |

**📚 Appears In:**
- ML Week 4 §1 (Review of FFN)

---

### Long Short-Term Memory, LSTM (长短期记忆)

**Tags:** `#rnn` `#architecture` `#sequence` `#ml-week4`

**📌 One-line Definition:**
> LSTM is a gated RNN architecture with a cell state that acts as a "gradient highway," enabling learning of long-term dependencies without vanishing gradients.
>> LSTM是一种门控RNN架构，具有作为"梯度高速公路"的细胞状态，能够在不发生梯度消失的情况下学习长期依赖。

**📐 Key Components:**

$$\begin{aligned}
f_t &= \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) & \text{(Forget gate)} \\
i_t &= \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) & \text{(Input gate)} \\
\tilde{C}_t &= \tanh(W_C \cdot [h_{t-1}, x_t] + b_C) & \text{(Candidate)} \\
C_t &= f_t \odot C_{t-1} + i_t \odot \tilde{C}_t & \text{(Cell state)} \\
o_t &= \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) & \text{(Output gate)} \\
h_t &= o_t \odot \tanh(C_t) & \text{(Hidden state)}
\end{aligned}$$

**💡 Intuition (直觉理解):**
> **The notebook analogy:** Cell state = a notebook. Forget gate = eraser (decide what to erase). Input gate + candidate = pencil (decide what to write). Output gate = what to read aloud from the notebook.
>> **笔记本类比：** 细胞状态 = 笔记本。遗忘门 = 橡皮擦（决定擦除什么）。输入门 + 候选值 = 铅笔（决定写什么）。输出门 = 从笔记本大声读出什么。

**⚖️ Compare:**
| Feature | LSTM | GRU |
|---|---|---|
| Gates | 3 (forget, input, output) | 2 (reset, update) |
| States | 2 (C_t and h_t) | 1 (h_t only) |
| Parameters | More | Fewer |

**🔗 Related Concepts:**
→ see: Vanishing Gradient Problem (what LSTM solves)
→ see: RNN (the base architecture)
→ see: GRU (simpler alternative)

**📚 Appears In:**
- ML Week 4 §10 (LSTM)

---

### Recurrent Neural Network, RNN (循环神经网络)

**Tags:** `#architecture` `#sequence` `#ml-week4`

**📌 One-line Definition:**
> RNN is a neural network where the hidden state at time t depends on both the current input x_t and the previous hidden state h_{t-1}, enabling processing of sequential data with memory.
>> RNN是一种神经网络，其中时间t的隐藏状态同时依赖于当前输入x_t和先前隐藏状态h_{t-1}，从而能够带记忆地处理序列数据。

**📐 Core Formula:**

$$h_t = f(W_x \cdot x_t + W_h \cdot h_{t-1})$$

- $h_t$ = hidden state at time $t$
- $x_t$ = input at time $t$
- $W_x$, $W_h$ = weight matrices (shared across all time steps)
- $f$ = activation function (typically tanh)

**💡 Intuition (直觉理解):**
> **The note-passing analogy:** Imagine students in a row. Each student gets a note from the previous student (h_{t-1}) and sees something new (x_t). They write a new note combining both and pass it forward. The final note contains info from everyone.
>> **传纸条类比：** 想象一排学生。每个学生从前一个学生那里收到一张纸条（h_{t-1}），并看到新东西（x_t）。他们写一张结合两者的新纸条并传递。最后的纸条包含所有人的信息。

**🔗 Related Concepts:**
→ see: FFN (non-recurrent baseline)
→ see: LSTM (addresses RNN's limitations)
→ see: BPTT (how RNN is trained)

**📚 Appears In:**
- ML Week 4 §5 (Recurrent Neural Networks)

---

### Vanishing Gradient Problem (梯度消失问题)

**Tags:** `#gradient` `#training` `#rnn` `#ml-week4`

**📌 One-line Definition:**
> The vanishing gradient problem occurs when gradients become exponentially small during backpropagation through many layers or time steps, preventing the network from learning long-range dependencies.
>> 梯度消失问题发生在反向传播通过许多层或时间步时梯度变得指数级小，阻止网络学习长程依赖。

**💡 Intuition (直觉理解):**
> **The fading echo:** Imagine shouting in a canyon. Each bounce loses energy. After 100 bounces, the echo is inaudible. Vanishing gradients are similar — the "error signal" fades as it travels back through time.
>> **衰减回声：** 想象在峡谷中喊叫。每次反弹都会失去能量。100次反弹后，回声听不见了。梯度消失类似 — "错误信号"在通过时间向后传播时衰减。

**⚙️ Cause:**
> When using tanh/sigmoid, derivatives are in (0,1). Multiplying many values < 1 → product → 0. Example: 0.5^100 ≈ 10^-30.
>> 使用tanh/sigmoid时，导数在(0,1)之间。乘以许多<1的值 → 乘积 → 0。例如：0.5^100 ≈ 10^-30。

**⚙️ Solutions:**
1. **LSTM/GRU** — gate-controlled information flow
2. **Gradient Clipping** — cap gradient magnitude
3. **Layer/Batch Normalization** — keep activations in stable range
4. **ReLU** (partial) — derivative = 1 for positive inputs

**🔗 Related Concepts:**
→ see: LSTM (solves this problem)
→ see: BPTT (where this problem occurs)

**📚 Appears In:**
- ML Week 4 §9 (Vanishing Gradient Problem)

---
