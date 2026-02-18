# RNN & NLP Quiz – Full Version (Questions 1–8)

---

## Question 1 (1 point)

**Statement:**
In the context of Recurrent Neural Networks (RNNs), the gradient refers to the rate of change of the loss function with respect to the network's parameters (weights and biases). During the training process, these gradients are computed using backpropagation to adjust the model’s parameters in order to minimize the loss and improve the model's performance.

**Options:**

- True
- False

**Correct Answer:** True

---

## Question 2 (1 point)

**Statement:**
"Stateful computation" in the context of Recurrent Neural Networks (RNNs) refers to maintaining internal memory states across multiple inputs.

**Options:**

- True
- False

**Correct Answer:** True

---

## Question 3 (1 point)

**Statement:**
Publicly available datasets, such as news articles, social media posts, and web pages, are commonly used as sources of data for training NLP models, as they provide a diverse range of language usage and context.

**Options:**

- True
- False

**Correct Answer:** True

---

## Question 4 (1 point)

**Problem:**
Suppose we have the following sentence:

"Sunny days make people feel ________."

Let's assume we have a corpus, and we count the occurrences of the words "feel" and "feel happy" in that corpus.

- Count("feel"): 100 occurrences
- Count("feel happy"): 40 occurrences
- Count("happy"): 30 occurrences

The conditional probability P("happy" | "feel") is:

**Options:**

- 0.2
- 0.4
- 0
- 0.3

**Correct Answer:** 0.4

---

## Question 5 (1 point)

**Question:**
What is a significant advantage of Recurrent Neural Networks (RNNs) over traditional feedforward neural networks (FFNs) that makes them particularly suited for natural language processing tasks?

**Options:**

A) RNNs maintain an internal state that allows them to model sequential dependencies, which is crucial for tasks like language modeling and machine translation.

B) RNNs can process fixed-length input sequences, making them ideal for tasks with static input sizes.

C) RNNs only process input in a single forward pass, making them more efficient than FFNs for sequential tasks.

D) RNNs are faster to train than FFNs because they do not require backpropagation.

**Correct Answer:** A

---

## Question 6 (1 point)

**Question:**
Which of the following best explains why LSTMs are able to handle long-term dependencies better than standard RNNs?

**Options:**

A) Because LSTMs use more hidden layers, which automatically prevent vanishing gradients.

B) Because LSTMs replace the recurrent connection with a fully connected feedforward network.

C) Because LSTMs use gating mechanisms that regulate information flow and help preserve gradients over long sequences.

D) Because LSTMs remove backpropagation and instead rely only on forward propagation.

**Correct Answer:** C

---

## Question 7 (1 point)

**Statement:**
The core idea of an n-gram language model is to predict the next word by understanding the semantic meaning of entire sentences and applying deep reasoning.

**Options:**

- True
- False

**Correct Answer:** False

---

## Question 8 (1 point)

**Statement:**
When the learning rate is set too low, the training process will become much faster, and the model will reach the optimal solution quickly because small weight updates allow for faster progress.

**Options:**

- True
- False

**Correct Answer:** False

---

# Summary of Answers

| Question | Answer |
| -------- | ------ |
| Q1       | True   |
| Q2       | True   |
| Q3       | True   |
| Q4       | 0.4    |
| Q5       | A      |
| Q6       | C      |
| Q7       | False  |
| Q8       | False  |
