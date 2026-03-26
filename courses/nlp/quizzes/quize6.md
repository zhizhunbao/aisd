# Attention / Transformer Quiz Answers

## Question 1

**Statement:** BiLSTM is capable of capturing contextual information exclusively from upcoming time steps.
**Answer:** False
**Reason:** BiLSTM uses both past and future context, not only upcoming time steps.

## Question 2

**Statement:** The Encoder-Decoder Framework is primarily used for image classification tasks.
**Answer:** False
**Reason:** Encoder-Decoder is mainly used for sequence-to-sequence tasks such as machine translation, summarization, and text generation.

## Question 3

**Statement:** The primary motivation behind using multi-head self-attention is to capture different types of relationships and dependencies in the input data by allowing the model to attend to different positions at different semantic levels.
**Answer:** True
**Reason:** Different attention heads can learn different relationships and focus on different parts of the input.

## Question 4

**Statement:** The Transformer in NLP is a novel architecture that aims to solve sequence-to-sequence tasks while handling long-range dependencies.
**Answer:** True
**Reason:** Transformer was designed for sequence-to-sequence problems and is very effective at modeling long-range dependencies.

## Question 5

**Statement:** In transformer, residual connections let each layer subtract refinements to the input rather than replace it. This preserves information across depth, prevents vanishing gradients, and makes it possible to train Transformers with dozens or hundreds of layers.
**Answer:** True
**Reason:** Residual connections preserve information and improve gradient flow, which makes deep Transformer training possible.

## Question 6

**Statement:** Positional encoding is a type of regularization technique that stabilizes the training process.
**Answer:** False
**Reason:** Positional encoding provides sequence order information, not regularization.

## Question 7

**Question:** In the context of the Transformer model's attention mechanism, what does the term "scaled" refer to in the scaled dot-product attention?
**Answer:** Scaling the dot product of the query and key vectors by the square root of the dimensionality.
**Reason:** The dot product is divided by sqrt(d_k) to keep values from becoming too large before softmax.

## Question 8

**Question:** Which of the following deep learning architectures commonly uses the attention mechanism?
**Answer:** Transformer-based models
**Reason:** Transformers are built around the attention mechanism.

## Question 9

**Statement:** Attention mechanisms enhance model interpretability by emphasizing the most relevant parts of the input sequences.
**Answer:** True
**Reason:** Attention weights can highlight which input parts the model focuses on.

## Question 10

**Statement:** When implementing self-attention in deep learning models, the purpose of the masking mechanism is to mask out gradients during backpropagation and speed up training.
**Answer:** False
**Reason:** Masking is used to hide padding tokens or future tokens, not to mask gradients.
