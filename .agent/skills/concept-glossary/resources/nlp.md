# Natural Language Processing (自然语言处理)

> This file grows automatically as new notes are written. Entries are alphabetical.

---

## Corpus (语料库)

- **Definition:** A collection of text documents used as input for NLP analysis
- **Example:** All tweets from Twitter in 2024, all Wikipedia articles, a dataset of news articles
- **Analogy:** A corpus is like a library — the entire collection of books available for study
- **Hierarchy:** Corpus → Document → Paragraph → Sentence → Token
- **Appears In:** NLP Week 2 — Text Preprocessing

---

## Lemmatization (词元化)

- **Definition:** A dictionary-based method that converts words to their canonical dictionary form (lemma)
- **How:** Uses vocabulary (dictionary) and morphological analysis (word structure and grammar relations)
- **Output:** Always a valid dictionary word
- **Examples:** am/are/is → be, better → good, running → run
- **Requires:** POS information ("meeting" as noun → "meeting", as verb → "meet")
- **Tools:** WordNet Lemmatizer (NLTK), spaCy Lemmatizer, TextBlob, Stanford CoreNLP
- **vs Stemming:** More accurate but slower; uses context; always produces real words
- **Appears In:** NLP Week 2 — Normalization

---

## Named Entity Recognition — NER (命名实体识别)

- **Definition:** Identifies and classifies proper nouns into predefined categories
- **Categories:** PERSON, LOCATION/GPE, ORGANIZATION, DATE, MONEY, etc.
- **Depends on:** POS tagging (needs to know a word is a noun first)
- **Applications:** Information extraction, search indexing, sentiment analysis, knowledge graphs
- **Pitfall:** Must run BEFORE lowercasing — "Apple" (company) vs "apple" (fruit)
- **Appears In:** NLP Week 2 — POS Tagging & NER

---

## POS Tagging (词性标注)

- **Definition:** Assigning grammatical categories (noun, verb, adjective, etc.) to each word
- **Tag Set:** Penn Treebank — NN (noun), VB (verb), JJ (adjective), RB (adverb), etc.
- **Purpose:** Syntactic/semantic analysis, disambiguation, foundation for NER
- **Example:** "book" can be VERB ("book a flight") or NOUN ("read a book")
- **Tool:** `nltk.pos_tag()`, `nltk.help.upenn_tagset()` to view all tags
- **Appears In:** NLP Week 2 — POS Tagging & NER

---

## Regular Expression — Regex (正则表达式)

- **Definition:** A formal mini-language for describing text patterns using metacharacters
- **Key Metacharacters:** `.` (any char), `*` (0+), `+` (1+), `?` (0 or 1), `[]` (set), `^` (start/negation), `$` (end)
- **Character Classes:** `\s` (whitespace), `\w` (word char), `\d` (digit); capitalize to negate (`\D`, `\W`, `\S`)
- **Python Functions:** `re.match()` (start only), `re.search()` (anywhere), `re.findall()` (all matches), `re.sub()` (replace), `re.compile()` (pre-compile)
- **Pitfall:** `re.match` ≠ `re.search`; always use raw strings `r''`; `^` has dual meaning inside/outside `[]`
- **Applications:** Text cleaning, tokenization, information retrieval, pattern extraction
- **Appears In:** NLP Week 2 — Regular Expressions

---

## Stemming (词干提取)

- **Definition:** A crude, rule-based method that chops off word suffixes to approximate the root
- **Output:** May NOT be a real word (e.g., "studying" → "studi")
- **Algorithms (NLTK):** Porter Stemmer (moderate), Snowball Stemmer (improved), Lancaster Stemmer (aggressive)
- **Applications:** Text classification, clustering, information retrieval
- **vs Lemmatization:** Faster but less accurate; no context needed; may produce non-words
- **Pitfall:** Over-stemming — "university" and "universe" both → "univers"
- **Note:** SpaCy does NOT provide built-in stemming (only lemmatization)
- **Appears In:** NLP Week 2 — Normalization

---

## Stop Words (停用词)

- **Definition:** High-frequency words with little semantic content ("the", "is", "at", "which", "on")
- **Why Remove:** Reduce feature space dimensionality without losing useful information
- **Tools:** `nltk.corpus.stopwords`, spaCy built-in lists
- **Pitfall:** Removing negation words ("not", "no", "never") reverses sentiment — "not good" → "good"
- **Appears In:** NLP Week 2 — Noise Entities Removal

---

## Tokenization (分词)

- **Definition:** Converting raw text into a sequence of meaningful units (tokens) that a model can process
- **Types:** Word-level, sub-word (BPE, WordPiece), character-level
- **Always First:** Tokenization is always the first step in any NLP pipeline
- **Tools:** NLTK `word_tokenize()`, spaCy tokenizer, Hugging Face tokenizers
- **Pitfall:** Simple `text.split(" ")` fails for contractions ("don't"), multi-word entities ("New York"), non-space languages
- **Appears In:** NLP Week 2 — Tokenization

---

## Word Embedding (词嵌入)

- **Definition:** Representation of words as dense, low-dimensional vectors of real numbers that capture semantic relationships
- **Formal:** A mapping f: V → R^d where V = vocabulary, d = embedding dimension (typically 50-300)
- **Key Property:** Semantically similar words have similar vectors (small cosine distance)
- **Famous Example:** vector('king') - vector('man') + vector('woman') ≈ vector('queen')
- **Foundation:** Distributional hypothesis — "A word is characterized by the company it keeps" (Firth, 1957)
- **vs OHE:** Dense (300-dim, all non-zero) vs sparse (50,000-dim, one non-zero)
- **Methods:** Word2Vec (CBOW/Skip-gram), GloVe, FastText
- **Limitation:** Static — same word gets same vector regardless of context (→ BERT fixes this)
- **Appears In:** NLP Week 4 — Word Embedding

---

## Word2Vec (Word2Vec)

- **Definition:** Neural network-based word embedding method using self-supervised learning from large text corpora
- **Two Architectures:** CBOW (context→center word, faster) and Skip-gram (center word→context, better for rare words)
- **Training:** Self-supervised — no human labels needed; predicts words from their context
- **SGNS:** Skip-gram with Negative Sampling — replaces expensive softmax with binary classification using k negative samples
- **Pretrained:** Google News model — 3M words, 300-dim vectors, trained on 100B words
- **Tool:** `gensim.models.Word2Vec(text, vector_size=300, window=5, sg=1, negative=5)`
- **Key Parameters:** `sg`=1 for Skip-gram/0 for CBOW; `window`=context size; `negative`=num negative samples
- **Appears In:** NLP Week 4 — Word2Vec Architectures

---

## GloVe — Global Vectors (全局向量)

- **Definition:** Word embedding method combining count-based and prediction-based approaches by factorizing a word-word co-occurrence matrix
- **Core Idea:** Learn vectors such that dot product w_i · w_j = log(P(co-occurrence of i and j))
- **vs Word2Vec:** Uses global co-occurrence statistics (matrix factorization) vs local context windows (prediction)
- **Pretrained:** Stanford — Wikipedia+Gigaword (6B tokens), Common Crawl (840B tokens), Twitter (27B tokens)
- **Inventor:** Pennington, Socher, Manning — Stanford, 2014
- **Appears In:** NLP Week 4 — GloVe

---

## FastText (FastText)

- **Definition:** Word embedding method extending Word2Vec by representing words as bags of character n-grams (length 3-6)
- **Key Innovation:** word vector = sum of character n-gram vectors + whole-word vector
- **OOV Solution:** Even unseen words get vectors because they share character n-grams with known words
- **Morphology:** Captures word structure — "unhappiness" shares n-grams with "happy", "unhappy", "happiness"
- **Trade-off:** Larger model size (stores all n-gram vectors) but handles OOV, typos, and morphological variants
- **Inventor:** Facebook (Bojanowski et al.), 2016
- **Appears In:** NLP Week 4 — FastText

---

## Distributional Hypothesis (分布假说)

- **Definition:** Words that occur in similar contexts have similar meanings
- **Quote:** "You shall know a word by the company it keeps" — J.R. Firth, 1957
- **Foundation:** The theoretical basis for ALL word embedding methods (Word2Vec, GloVe, FastText)
- **Implication:** We can learn word meanings from raw text without human annotation (self-supervision)
- **Appears In:** NLP Week 4 — Key Terms

---

## WordNet (词网)

- **Definition:** A hand-crafted lexical database organizing English words into synonym sets (synsets) connected by semantic relationships
- **Key Relations:** Synset (synonym set), Hypernym (IS-A general), Hyponym (IS-A specific), Meronym (PART-OF), Holonym (WHOLE-OF), Antonym (opposite), Troponym (manner-of for verbs), Entailment (verb implies verb)
- **Limitations:** Manual curation (expensive, incomplete, static), not computational, domain-specific, English-only
- **vs Embeddings:** Labels relationships but doesn't provide numerical vectors; embeddings learn relationships as vector directions
- **Appears In:** NLP Week 4 — WordNet

---

## BPTT — Backpropagation Through Time (时序反向传播)

- **Definition:** The training algorithm for RNNs — extends standard backpropagation by unrolling the RNN across all timesteps and computing gradients through the entire sequence
- **Problem:** Gradients are multiplied by Wₕ at each timestep. If |Wₕ| < 1, gradients vanish exponentially (vanishing gradient). If |Wₕ| > 1, gradients explode (exploding gradient)
- **Impact:** Vanishing gradients prevent learning long-range dependencies; the model forgets early words
- **Solutions:** Gradient clipping (for exploding), LSTM cell state highway (for vanishing)
- **Appears In:** NLP Week 5 — RNN Training & Vanishing Gradient

---

## Language Model — LM (语言模型)

- **Definition:** A probability distribution over sequences of words that predicts the next word given previous context: P(wₜ | w₁, ..., wₜ₋₁)
- **Goal:** Learn patterns in text and predict the next word (or sequence of words) based on prior context
- **Types:** N-gram (count-based), Fixed-window NN, RNN, LSTM, Transformer
- **Applications:** Autocomplete, machine translation, speech recognition, text generation, chatbots (GPT, Claude, Gemini)
- **Evaluation:** Perplexity (PPL) — lower is better
- **Appears In:** NLP Week 5 — Language Modeling

---

## LSTM — Long Short-Term Memory (长短时记忆网络)

- **Definition:** An RNN variant (Hochreiter & Schmidhuber, 1997) that uses three gates and a cell state to solve the vanishing gradient problem
- **Components:** Cell state (long-term memory conveyor belt), Hidden state (short-term output)
- **Three Gates:** Forget gate (what to erase), Input gate (what to write), Output gate (what to read)
- **Key Insight:** Cell state flows through time with only pointwise operations (multiply + add), enabling gradient flow without exponential decay
- **Keras:** `LSTM(units, input_shape=(timesteps, features))`
- **vs RNN:** ~4x parameters but handles long-range dependencies; solves vanishing gradient
- **Limitation:** Still struggles with very long sequences (1000+ tokens); replaced by Transformers
- **Appears In:** NLP Week 5 — LSTM, NLP Week 6 — Bi-LSTM

---

## N-gram (N元语法)

- **Definition:** A contiguous sequence of N items from text; as a language model, predicts next word using only the previous N-1 words (Markov assumption)
- **Formula:** P(wₜ | wₜ₋ₙ₊₁...wₜ₋₁) = Count(wₜ₋ₙ₊₁...wₜ) / Count(wₜ₋ₙ₊₁...wₜ₋₁)
- **Types:** Unigram (N=1, no context), Bigram (N=2), Trigram (N=3), 4-gram, 5-gram
- **Limitations:** Data sparsity (many n-grams never observed → zero probability), fixed context window, no word similarity
- **Solutions for sparsity:** Add-k smoothing, backoff, interpolation
- **vs Neural LMs:** Cannot capture semantic similarity; treats each word as independent symbol
- **Appears In:** NLP Week 5 — N-gram Language Modeling

---

## Perplexity — PPL (困惑度)

- **Definition:** Standard evaluation metric for language models; measures how "confused" a model is when predicting the next word
- **Formula:** PPL = exp(-(1/T) Σ log P(wₜ | w₁...wₜ₋₁)) — inverse probability of test set, normalized by word count
- **Interpretation:** PPL = k means the model is "as confused as choosing uniformly among k words at each step"
- **Lower is better:** Low PPL → model predicts well; High PPL → text is unexpected
- **Appears In:** NLP Week 5 — Evaluating Language Models

---

## RNN — Recurrent Neural Network (循环神经网络)

- **Definition:** A neural network that processes sequences by maintaining a hidden state hₜ = σ(Wₕhₜ₋₁ + Wₑeₜ + b) updated at each timestep
- **Key Feature:** Parameter sharing — same weights Wₕ, Wₑ at every timestep; can handle variable-length input
- **Training:** BPTT (Backpropagation Through Time); loss = average negative log probability of correct words
- **Solves:** Variable length, order preservation, long-range deps (in theory), parameter sharing
- **Limitation:** Vanishing/exploding gradients make learning long-range dependencies difficult in practice
- **vs Fixed-window NN:** Handles any length, shares parameters, maintains full history (in theory)
- **Appears In:** NLP Week 5 — RNN

---

## Attention Mechanism (注意力机制)

- **Definition:** A mechanism that computes a weighted average of encoder hidden states at each decoder step, allowing the decoder to focus on relevant input positions
- **How:** 1) Compute attention scores via dot product between decoder state and each encoder state. 2) Apply softmax to get attention distribution. 3) Compute context vector = weighted sum of encoder states. 4) Concatenate with decoder state for prediction
- **Why:** Solves the information bottleneck in vanilla Seq2Seq — no need to compress entire source into one fixed vector
- **Key Benefit:** Enables direct connection from any encoder position to any decoder position; attention weights are interpretable as alignment
- **Complexity:** O(m×n) where m=output length, n=input length
- **Appears In:** NLP Week 6 — Attention Mechanism

---

## Bi-LSTM — Bidirectional LSTM (双向长短时记忆网络)

- **Definition:** Runs two separate LSTMs on the input sequence — one forward (left→right), one backward (right→left) — and concatenates their hidden states
- **Output:** h_t = [h_forward_t ; h_backward_t], doubling the hidden state dimension
- **Why:** Captures both left and right context — "terribly" in "the movie was terribly exciting" needs right context to know it means "very" (positive)
- **Keras:** `Bidirectional(LSTM(n))` — automatically creates forward+backward copies
- **Limitation:** Requires the ENTIRE sequence upfront; CANNOT be used for text generation (only understanding tasks like classification, NER, tagging)
- **Appears In:** NLP Week 6 — Bi-LSTM

---

## Conditional Language Model (条件语言模型)

- **Definition:** A language model where predictions are conditioned on an additional input — P(y₁...yₜ | x₁...xₛ) instead of just P(y₁...yₜ)
- **Use:** In machine translation, the decoder is a conditional LM conditioned on the encoder's output (source sentence encoding)
- **Unifies:** Translation, summarization, dialogue — all are "conditional text generation"
- **Appears In:** NLP Week 6 — Seq2Seq / Machine Translation

---

## Encoder-Decoder (编码器-解码器)

- **Definition:** Architecture where an encoder reads the entire input sequence into a fixed-length context vector, and a decoder generates the output sequence from that vector
- **Encoder:** RNN/LSTM that processes input left-to-right, producing hidden states; final state = context vector
- **Decoder:** RNN/LSTM initialized with context vector; generates output autoregressively (previous output → next input)
- **Bottleneck:** The single context vector must capture ALL source information — degrades for long sequences
- **Solution:** Add attention mechanism → decoder accesses all encoder states, not just the final one
- **Appears In:** NLP Week 6 — Seq2Seq

---

## Seq2Seq — Sequence-to-Sequence (序列到序列)

- **Definition:** A model architecture that transforms one sequence into another sequence, handling variable input/output lengths
- **Implementation:** Encoder-Decoder with LSTM/GRU cells
- **Applications:** Machine translation, text summarization, dialogue systems, question answering
- **Training:** Teacher forcing — feed ground truth previous word to decoder; loss = mean negative log prob of target words
- **Testing:** Autoregressive — feed decoder's own previous prediction as next input
- **Pitfall:** Exposure bias — training uses ground truth but testing uses predictions; errors accumulate
- **Appears In:** NLP Week 6 — Seq2Seq

---

## Transformer (Transformer)

- **Definition:** A novel architecture (Vaswani et al., 2017) that replaces recurrence entirely with self-attention, enabling parallel computation
- **Paper:** "Attention Is All You Need" — https://arxiv.org/abs/1706.03762
- **Key Innovation:** Self-attention — every position attends to every other position simultaneously; no sequential dependency
- **Advantage over RNN:** Fully parallelizable; handles long-range dependencies in O(1) steps instead of O(n)
- **Components:** Multi-head self-attention, positional encoding, feed-forward networks, layer normalization
- **Impact:** Foundation for GPT, BERT, and all modern LLMs
- **Appears In:** NLP Week 6 — Transformer Introduction
