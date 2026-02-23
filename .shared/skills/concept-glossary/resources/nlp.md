# Natural Language Processing (自然语言处理)

> This file grows automatically as new notes are written. Entries are alphabetical.

---

## Ambiguity (歧义)

- **Definition:** The property of language where a word, phrase, or sentence can have multiple valid interpretations.
- **Types:** Lexical (word-level: "bank"), syntactic/attachment ("saw the man with the telescope"), coreference (pronoun resolution: "she" = who?).
- **Why it matters:** The #1 challenge in NLP — requires contextual understanding to resolve.
- **Appears In:** NLP Week 1

## Common Knowledge (常识知识)

- **Definition:** The set of facts about the world that most humans are aware of but are not explicitly stated in text.
- **Example:** "man bit dog" is newsworthy; "dog bit man" is not — understood via world knowledge.
- **Why it matters:** NLP systems have no built-in world knowledge; even LLMs struggle with common sense reasoning.
- **Appears In:** NLP Week 1

## NLG — Natural Language Generation (自然语言生成)

- **Definition:** The ability of a machine to produce human-readable text or speech from structured data or meaning.
- **Tasks:** Text summarization, machine translation, dialogue generation, report writing.
- **Relationship:** NLP = NLU + NLG. NLG is the "mouth" of NLP.
- **Appears In:** NLP Week 1

## NLU — Natural Language Understanding (自然语言理解)

- **Definition:** The ability of a machine to read and comprehend text or speech, extracting structured meaning.
- **Tasks:** Sentiment analysis, named entity recognition, intent detection, text classification.
- **Relationship:** NLP = NLU + NLG. NLU is the "ear" of NLP.
- **Appears In:** NLP Week 1

## Sparsity (稀疏性)

- **Definition:** The phenomenon where most words in a language appear very rarely (Zipf's law).
- **Zipf's Law:** Word frequency follows a power law — the k-th most frequent word appears ~N/k times. >1/3 of words occur only once.
- **Impact:** Creates the out-of-vocabulary (OOV) problem for NLP models.
- **Appears In:** NLP Week 1

## Turing Test (图灵测试)

- **Definition:** A test where a machine must be indistinguishable from a human in conversation.
- **Relevance to NLP:** Establishes language understanding as the benchmark for AI intelligence.
- **Caveat:** Passing ≠ true understanding (Chinese Room argument, Searle 1980).
- **Appears In:** NLP Week 1

## Variation (变异性)

- **Definition:** The phenomenon where the same meaning can be expressed in many different ways.
- **Types:** Lexical, syntactic, regional/geographic, social, stylistic, generational, cross-lingual.
- **Example:** "She gave the book to Tom" vs "She gave Tom the book" (dative alternation).
- **Appears In:** NLP Week 1
