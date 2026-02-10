# CST8507 NLP Quiz — Word Embedding Summary

Student: Peng Wang
Topic: TF-IDF, Word Embeddings, Word2Vec, GloVe, Self-Supervised Learning

---

## Question 1 (1 point)

While TF-IDF is useful for some applications (like search engines), its high-dimensional nature can make it difficult to use efficiently for tasks like deep learning-based NLP.

Options:

- [X] True
- [ ] False

Answer: True

Explanation:
TF-IDF produces high-dimensional sparse vectors. Deep learning models typically work better with dense and low-dimensional embeddings.

---

## Question 2 (1 point)

Which of the following equations should hold for an effective word embedding?

Options:

- [ ] e_boy − e_brother ≈ e_sister − e_girl
- [X] e_boy − e_girl ≈ e_brother − e_sister
- [ ] e_boy − e_girl ≈ e_sister − e_brother

Answer: e_boy − e_girl ≈ e_brother − e_sister

Explanation:
Effective word embeddings preserve semantic relationships as vector differences. The gender relationship should be consistent in vector space.

---

## Question 3 (1 point)

The self-supervision method in neural language modeling avoids the need for hand-labeled supervision signals by using surrounding words as implicit training data for classifiers.

Options:

- [X] True
- [ ] False

Answer: True

Explanation:
Self-supervised learning uses the data itself to generate labels, such as predicting missing or next words from context.

---

## Question 4 (1 point)

One advantage of GloVe over other word embedding methods is that it is global in the sense that it considers the entire corpus to learn relationships between words, and local in the sense that it considers the co-occurrence of words within a limited context window.

Options:

- [X] True
- [ ] False

Answer: True

Explanation:
GloVe combines global corpus statistics with local context co-occurrence information.

---

## Question 5 (1 point)

Suppose you learn a word embedding for a vocabulary of 1000 words. Should the embedding vectors be 1000 dimensional to capture the full range of variation and meaning in those words?

Options:

- [ ] True
- [X] False

Answer: False

Explanation:
Embeddings are low-dimensional dense representations. The embedding dimension does not need to equal vocabulary size.

---

## Question 6 (1 point)

What is the default dimensionality of word embeddings in the Gensim Word2Vec method?

Options:

- [ ] 4000
- [ ] 120
- [X] 100
- [ ] 10

Answer: 100

Explanation:
The default embedding size in Gensim Word2Vec is vector_size = 100.

---

## Question 7 (1 point)

Word2Vec consists of two main techniques: CBOW (Continuous Bag of Words) and Skip-gram.

Options:

- [X] True
- [ ] False

Answer: True

Explanation:
Word2Vec includes two training methods: CBOW and Skip-gram.

---

## Question 8 (1 point)

Is the goal of the Skip-Gram model to determine the central word based on its surrounding context words?

Options:

- [ ] True
- [X] False

Answer: False

Explanation:
Skip-gram predicts surrounding words from the central word. CBOW predicts the central word from context.

---

## Question 9 (1 point)

Most modern NLP algorithms do not use embeddings as the representation of word meaning.

Options:

- [ ] True
- [X] False

Answer: False

Explanation:
Modern NLP models rely heavily on embeddings (Word2Vec, GloVe, BERT, GPT, etc.).

---

## Quick Review Notes

- TF-IDF → sparse, high-dimensional
- Embeddings → dense, low-dimensional
- Self-supervised learning uses data as labels
- GloVe = global statistics + local context
- Word2Vec = CBOW + Skip-gram
- CBOW: context → word
- Skip-gram: word → context
- Modern NLP uses embeddings
