NLP Quiz – Final Answers
Question 1

Given the words "intention" and "execution", what is the minimum number of operations required to transform "intention" into "execution"?

Answer: 5

Reason: This is the classic Levenshtein (edit) distance example.

Question 2

In a Bag of Words representation, the order of words in a document is crucial, and each word is treated as dependent on its surrounding words.

Answer: False

Reason: Bag of Words ignores word order and context.

Question 3

The inverse document frequency (IDF) of a word is calculated by dividing the total number of documents by the number of documents containing the word.

Answer: True

Reason: IDF is proportional to 
𝑁
𝑑
𝑓
df
N
	​

 (often with log).

Question 4

If the cosine similarity between the word vectors for Word A and Word B is close to 1, it means that Word A and Word B are considered highly similar in meaning.

Answer: True

Reason: Cosine similarity close to 1 means the vectors point in the same direction.

Question 5

One of the disadvantages of using TF-IDF is:

Answer: It does not consider the context and semantic relationships between words

Reason: TF-IDF is a bag-of-words statistical model, not semantic.

Question 6

TF values:

𝑇
𝐹
𝑑
1
=
25
127
,
𝑇
𝐹
𝑑
2
=
3
250
,
𝑇
𝐹
𝑑
3
=
20
650
,
𝑇
𝐹
𝑑
9
=
15
125
,
𝑇
𝐹
𝑑
1000
=
20
800
TF
d1
	​

=
127
25
	​

,TF
d2
	​

=
250
3
	​

,TF
d3
	​

=
650
20
	​

,TF
d9
	​

=
125
15
	​

,TF
d1000
	​

=
800
20
	​


Proposed order:
[d2, d1000, d3, d1, d9]

Answer: False

Correct ascending order by TF (and TF-IDF):

[
𝑑
2
,
𝑑
1000
,
𝑑
3
,
𝑑
9
,
𝑑
1
]
[d2,d1000,d3,d9,d1]
Question 7

w1 = (0.2, 0.2, 0.3, 0.7)
w2 = (0.3, 0.4, 0.8, 0.5)

cos
⁡
(
𝜃
)
=
𝑤
1
⋅
𝑤
2
∣
∣
𝑤
1
∣
∣
⋅
∣
∣
𝑤
2
∣
∣
=
0.73
0.8124
×
1.0677
≈
0.8421
cos(θ)=
∣∣w1∣∣⋅∣∣w2∣∣
w1⋅w2
	​

=
0.8124×1.0677
0.73
	​

≈0.8421

Answer: 0.8421

Question 8
cv = CountVectorizer(ngram_range=(1,2)).fit(
    ["I love NLP", "He love NLP", "good man"]
)
cv.transform(["love"]).toarray()


Claimed output:

array([[0, 0, 1, 0, 0, 0, 0]], dtype=int64)


Answer: False

Reason: The vocabulary includes multiple unigrams and bigrams, so the vector is longer and not a single 1.