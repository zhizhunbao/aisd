# CST8507 NLP Quiz 5 — RNN与语言模型 (RNN & Language Models)

Topic: RNN, LSTM, Gradient, N-gram Language Models, Learning Rate, Training Data

---

## Question 1 (1 point)

In the context of Recurrent Neural Networks (RNNs), the gradient refers to the rate of change of the loss function with respect to the network's parameters (weights and biases). During the training process, these gradients are computed using backpropagation to adjust the model's parameters in order to minimize the loss and improve the model's performance.

Options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> This is the standard definition of gradients in RNN training. **Why True**: The gradient $\frac{\partial L}{\partial \theta}$ represents the rate of change of the loss function with respect to parameters. In RNNs, gradients are computed via BPTT (Backpropagation Through Time), then used with gradient descent to update parameters and minimize loss.
>
> > 这是 RNN 训练中梯度的标准定义。**为什么是 True**：梯度 $\frac{\partial L}{\partial \theta}$ 表示损失函数对参数的变化率，通过时序反向传播（BPTT）计算梯度，然后用梯度下降法更新参数以最小化损失。
>
> - **$\frac{\partial L}{\partial \theta}$**: Partial derivative of loss w.r.t. parameters (gradient) / 损失函数对参数的偏导数（梯度）
> - **BPTT**: Backpropagation Through Time — the specialized backpropagation algorithm for RNNs / 时序反向传播，RNN 专用的反向传播算法
>
> **Key**: Gradient = $\frac{\partial L}{\partial \theta}$, computed via BPTT in RNNs, used to minimize loss by adjusting weights and biases.

---

## Question 2 (1 point)

"Stateful computation" in the context of Recurrent Neural Networks (RNNs) refers to maintaining internal memory states across multiple inputs.

Options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> The core feature of RNNs is "stateful computation" — transferring information between time steps through hidden state $h_t$. **Why True**: At each time step, the RNN receives the current input and previous hidden state: $h_t = f(W_h h_{t-1} + W_x x_t + b)$. This mechanism enables RNNs to maintain memory across multiple inputs.
>
> > RNN 的核心特征就是"有状态计算"——通过隐藏状态 $h_t$ 在时间步之间传递信息。**为什么是 True**：RNN 在每个时间步接收当前输入和上一步的隐藏状态 $h_t = f(W_h h_{t-1} + W_x x_t + b)$，使其能跨多个输入维持记忆。
>
> - **$h_t$**: Hidden state — carries historical information across time steps / 隐藏状态，携带历史信息
>
> **Key**: Stateful computation = RNN maintains hidden state $h_t$ across time steps, carrying information from previous inputs.

---

## Question 3 (1 point)

Publicly available datasets, such as news articles, social media posts, and web pages, are commonly used as sources of data for training NLP models, as they provide a diverse range of language usage and context.

Options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> NLP model training relies on large-scale, diverse text datasets. **Why True**: News, social media, and web data cover various genres, topics, and expressions, providing rich linguistic diversity and contextual information essential for robust model training.
>
> > NLP 模型训练依赖大规模多样化文本数据集。**为什么是 True**：新闻、社交媒体、网页等公开数据涵盖了各种文体、话题和表达方式，为模型提供了丰富的语言多样性和上下文信息。
>
> **Key**: Public datasets (news, social media, web) provide diverse language patterns essential for training robust NLP models.

---

## Question 4 (1 point)

Suppose we have the following sentence:

"Sunny days make people feel **\_\_\_\_**."

Let's assume we have a corpus, and we count the occurrences:

- Count("feel"): 100 occurrences
- Count("feel happy"): 40 occurrences
- Count("happy"): 30 occurrences

The conditional probability P("happy" | "feel") is:

Options:

A) 0.2

B) 0.4

C) 0

D) 0.3

> **Answer**: B
> **Explanation**:
> Conditional probability formula: $P(w_2|w_1) = \frac{Count(w_1, w_2)}{Count(w_1)}$. **Why 0.4**:
>
> - $P(\text{"happy"} | \text{"feel"}) = \frac{Count(\text{"feel happy"})}{Count(\text{"feel"})} = \frac{40}{100} = 0.4$
> - **Note**: Count("happy") = 30 is a **distractor** — conditional probability only uses the co-occurrence count divided by the conditioning word count.
>
> > 条件概率公式：$P(w_2|w_1) = \frac{Count(w_1, w_2)}{Count(w_1)}$。**为什么是 0.4**：
> >
> > - $P(\text{"happy"} | \text{"feel"}) = \frac{40}{100} = 0.4$
> > - **注意**：Count("happy") = 30 是**干扰信息**，条件概率只用共现次数除以条件词总次数。
>
> - **$P(w_2|w_1) = \frac{Count(w_1 w_2)}{Count(w_1)}$**: N-gram conditional probability (Bigram model) / N-gram 条件概率（Bigram 模型）
>
> **Key**: $P(\text{happy}|\text{feel}) = \frac{Count(\text{feel happy})}{Count(\text{feel})} = \frac{40}{100} = 0.4$. Count("happy") alone is a distractor.

---

## Question 5 (1 point)

What is a significant advantage of Recurrent Neural Networks (RNNs) over traditional feedforward neural networks (FFNs) that makes them particularly suited for natural language processing tasks?

Options:

A) RNNs maintain an internal state that allows them to model sequential dependencies, which is crucial for tasks like language modeling and machine translation.

B) RNNs can process fixed-length input sequences, making them ideal for tasks with static input sizes.

C) RNNs only process input in a single forward pass, making them more efficient than FFNs for sequential tasks.

D) RNNs are faster to train than FFNs because they do not require backpropagation.

> **Answer**: A
> **Explanation**:
> The core advantage of RNNs over FFNs is the ability to process sequential data and model temporal dependencies. **Why A**: RNNs pass information between time steps via hidden state $h_t$, capturing sequential dependencies crucial for language modeling and machine translation.
>
> > RNN 相比 FFN 的核心优势在于能处理序列数据并建模时序依赖关系。**为什么是 A**：RNN 通过隐藏状态 $h_t$ 在时间步之间传递信息，捕捉序列中的依赖关系，对语言建模和机器翻译至关重要。
>
> - **B**: RNNs can handle **variable-length** sequences — that's precisely their advantage, not "fixed-length."
> - **C**: RNNs compute at every time step and use BPTT for backpropagation — not "a single forward pass."
> - **D**: RNNs require backpropagation (BPTT) and are typically slower than FFNs due to sequential unrolling.
>
> > - **B 错**：RNN 能处理**变长**序列，这恰恰是它的优势，不限于固定长度。
> > - **C 错**：RNN 在每个时间步都进行计算，并通过 BPTT 反向传播，不是"单次前向传播"。
> > - **D 错**：RNN 需要反向传播（BPTT），且由于序列展开通常比 FFN 更慢。
>
> **Key**: RNN advantage over FFN: internal state $h_t$ models sequential dependencies — essential for language tasks.

---

## Question 6 (1 point)

Which of the following best explains why LSTMs are able to handle long-term dependencies better than standard RNNs?

Options:

A) Because LSTMs use more hidden layers, which automatically prevent vanishing gradients.

B) Because LSTMs replace the recurrent connection with a fully connected feedforward network.

C) Because LSTMs use gating mechanisms that regulate information flow and help preserve gradients over long sequences.

D) Because LSTMs remove backpropagation and instead rely only on forward propagation.

> **Answer**: C
> **Explanation**:
> LSTMs solve the standard RNN's vanishing gradient problem through three gating mechanisms. **Why C**:
>
> - **Forget Gate**: Decides which old information to discard
> - **Input Gate**: Decides which new information to store
> - **Output Gate**: Decides which information to output
> - These gates allow gradients to flow along the cell state over long distances, preventing vanishing gradients.
>
> > LSTM 通过三个门控机制解决了标准 RNN 的梯度消失问题。**为什么是 C**：
> >
> > - **遗忘门（Forget Gate）**：决定丢弃哪些旧信息
> > - **输入门（Input Gate）**：决定存储哪些新信息
> > - **输出门（Output Gate）**：决定输出哪些信息
> > - 这些门控机制允许梯度沿细胞状态长距离传播，避免梯度消失。
>
> - **A**: More layers don't automatically prevent vanishing gradients — the key is the gating mechanism.
> - **B**: LSTMs are still recurrent architectures — they don't replace recurrence with feedforward networks.
> - **D**: LSTMs still require backpropagation for training.
>
> > - **A 错**：层数多不能自动防止梯度消失，关键是门控机制。
> > - **B 错**：LSTM 仍然是循环结构，没有替换为前馈网络。
> > - **D 错**：LSTM 仍需反向传播来训练。
>
> **Key**: LSTM gates (forget, input, output) regulate information flow, preserving gradients across long sequences — solving vanishing gradient.

---

## Question 7 (1 point)

The core idea of an n-gram language model is to predict the next word by understanding the semantic meaning of entire sentences and applying deep reasoning.

Options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> N-gram models are shallow, statistics-based methods without deep semantic understanding. **Why False**: N-gram models only rely on the frequency of the previous $n-1$ words to predict the next word ($P(w_n|w_1,...,w_{n-1})$). They don't understand sentence meaning or perform "deep reasoning."
>
> > N-gram 模型是基于统计的浅层方法，不具备深层语义理解能力。**为什么是 False**：N-gram 模型只依赖前 $n-1$ 个词的出现频率来预测下一个词，不理解句子含义，也不进行"深层推理"。
>
> - **$P(w_n|w_{n-N+1},...,w_{n-1})$**: N-gram conditional probability — only looks at the previous N-1 words / N-gram 条件概率 — 只看前 N-1 个词
> - N-gram limitations / N-gram 局限：no semantic understanding (无语义理解), fixed window size (固定窗口), sparsity (稀疏性)
>
> **Key**: N-gram = statistical frequency-based prediction from previous N-1 words. No semantic understanding or deep reasoning.

---

## Question 8 (1 point)

When the learning rate is set too low, the training process will become much faster, and the model will reach the optimal solution quickly because small weight updates allow for faster progress.

Options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> Too low a learning rate causes training to become **slower**, not faster — the opposite of what the statement claims. **Why False**: A very small learning rate means each parameter update is tiny ($\theta = \theta - \alpha \cdot \nabla L$), requiring many more iterations to converge, and potentially getting stuck in local optima.
>
> > 学习率过低会导致训练**变慢**而非变快，与题干所述相反。**为什么是 False**：过小的学习率意味着每次参数更新幅度极小，需要更多迭代才能收敛，甚至可能卡在局部最优。
>
> - **Too low learning rate / 学习率过低**: Extremely slow convergence, may get stuck in local optima / 收敛极慢，可能陷入局部最优
> - **Too high learning rate / 学习率过高**: Oscillation/divergence, may skip the optimal solution / 振荡不收敛，可能跳过最优解
> - **$\alpha$**: Learning rate — controls the step size of parameter updates / 学习率，控制参数更新步长
>
> **Key**: Low learning rate → slow convergence (not faster). Too high → oscillation/divergence. Need balanced $\alpha$.

---

## Summary of Answers / 答案汇总

| Question | Answer | Topic / 主题                                          |
| -------- | ------ | ----------------------------------------------------- |
| Q1       | True   | RNN gradient & backpropagation / RNN梯度与反向传播    |
| Q2       | True   | RNN stateful computation / RNN有状态计算              |
| Q3       | True   | NLP training data sources / NLP训练数据来源           |
| Q4       | 0.4    | Conditional probability (bigram) / 条件概率（二元组） |
| Q5       | A      | RNN vs FFN advantage / RNN相比FFN的优势               |
| Q6       | C      | LSTM gating mechanisms / LSTM门控机制                 |
| Q7       | False  | N-gram limitations / N-gram局限性                     |
| Q8       | False  | Learning rate effects / 学习率影响                    |
