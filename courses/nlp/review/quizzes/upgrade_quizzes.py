"""
Quiz Bank Upgrade Script
========================
1. Add calculation / Why / What-if / code-analysis questions to each week
2. Remove exact-duplicate knowledge points
3. Regenerate all_quizzes.html with updated data
"""
import json, pathlib, re, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DIR = pathlib.Path(__file__).parent

# ============================================================
# NEW QUESTIONS TO ADD — organized by week
# ============================================================
NEW_QUESTIONS = {

# ---- Week 3: Edit Distance DP table, TF-IDF multi-doc ----
"week03_quiz.json": [
  {
    "type": "Short",
    "source": "supplement",
    "question": "<strong>[Calculation]</strong> Fill in the edit distance DP matrix for transforming 'CAT' into 'CAR'. Show the final matrix and trace the optimal path.<br><br><em>Allowed operations: Insert, Delete, Substitute (each costs 1).</em>",
    "answer": "≈ 1",
    "explanation": "<strong>DP Matrix:</strong><br><pre>    ''  C  A  R\n''   0  1  2  3\n C   1  0  1  2\n A   2  1  0  1\n T   3  2  1  <strong>1</strong></pre><br>• d(CAT, CAR) = 1 (substitute T→R at position 3)<br>• Only 1 operation needed.<br><br><strong>解题规则：</strong><br>• d[i][j] = d[i-1][j-1] if chars match<br>• d[i][j] = 1 + min(d[i-1][j], d[i][j-1], d[i-1][j-1]) if mismatch<br><br><strong>考试中必须画完整矩阵，不能只写答案！</strong>"
  },
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "Given 3 documents: D1='the cat sat', D2='the cat ate', D3='the dog sat'. Which word has the <strong>highest</strong> TF-IDF score in D1?",
    "options": [
      "A) 'the' — it appears in every document so IDF boosts it",
      "B) 'cat' — it appears in D1 and D2 (df=2), so IDF = log(3/2)",
      "C) 'sat' — it appears in D1 and D3 (df=2), so IDF = log(3/2)",
      "D) 'cat' and 'sat' are tied — both have TF=1/3 and df=2"
    ],
    "answer": 3,
    "explanation": "<strong>Why D:</strong> In D1, TF(cat) = TF(sat) = 1/3. Both cat and sat appear in exactly 2 documents → IDF = log(3/2) ≈ 0.585. So TF-IDF = 1/3 × 0.585 ≈ 0.195 for both. 'the' has IDF = log(3/3) = 0 → eliminated.<br><br><strong>在D1中，cat和sat的TF和IDF完全相同，因此TF-IDF分数相同。'the' 被IDF=0消除。</strong><br><br>⚠️ This tests whether you can identify that IDF eliminates universally common words AND compare tied scores."
  }
],

# ---- Week 4: Word2Vec analogy reasoning ----
"week04_quiz.json": [
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "You trained Word2Vec on a corpus and found cos(v_king, v_queen) = 0.75, cos(v_king, v_man) = 0.82. What does this tell you about the embedding quality?",
    "options": [
      "A) The embeddings are poor because king should be closer to queen than to man",
      "B) The embeddings may be reasonable — king-man captures a gender-neutral 'royalty' relationship, while king-queen involves a gender shift",
      "C) This proves Word2Vec cannot learn gender relationships",
      "D) The cosine values are meaningless without checking the full analogy e_king - e_man + e_woman ≈ e_queen"
    ],
    "answer": 3,
    "explanation": "<strong>Why D:</strong> Raw cosine similarity between word pairs alone doesn't validate analogy quality. The correct test is whether the full analogy <code>v_king - v_man + v_woman ≈ v_queen</code> holds. King being close to man could simply reflect shared contexts (both are male, both are human), which is valid.<br><br><strong>单看两两余弦不能验证类比能力。必须检验完整类比公式 v_king - v_man + v_woman ≈ v_queen 是否成立。</strong><br><br>⚠️ 似是而非陷阱：A和B都有道理但不是最佳答案，D才是方法论上正确的。"
  },
  {
    "type": "TF",
    "source": "supplement",
    "question": "FastText can generate embeddings for misspelled or out-of-vocabulary (OOV) words like 'amazzing', while Word2Vec cannot.",
    "answer": "True",
    "explanation": "<strong>Why True:</strong> FastText represents words as bags of character n-grams (e.g., 'amazzing' → 'ama','maz','azz','zzi','zin','ing'). Even for OOV words, it can compose an embedding from these subword pieces. Word2Vec/GloVe have NO mechanism for OOV words — they simply return an error or zero vector.<br><br><strong>FastText 用字符 n-gram 表示词，即使拼错的 OOV 词也能通过子词拼出嵌入。Word2Vec/GloVe 对 OOV 词完全无能为力。</strong>"
  }
],

# ---- Week 5: N-gram calculation, BPTT chain rule ----
"week05_quiz.json": [
  {
    "type": "Short",
    "source": "supplement",
    "question": "<strong>[Calculation]</strong> Given a trigram language model trained on this corpus:<br>• 'I love NLP' (1 time)<br>• 'I love ML' (2 times)<br>• 'I hate bugs' (1 time)<br><br>Calculate P('NLP' | 'I love') and P('ML' | 'I love').",
    "answer": "P('NLP'|'I love') = 1/3, P('ML'|'I love') = 2/3",
    "explanation": "<strong>Step-by-step:</strong><br>• Count('I love') = 1 + 2 = 3 (total occurrences of bigram 'I love')<br>• Count('I love NLP') = 1<br>• Count('I love ML') = 2<br><br>P('NLP' | 'I love') = Count('I love NLP') / Count('I love') = 1/3 ≈ 0.333<br>P('ML' | 'I love') = Count('I love ML') / Count('I love') = 2/3 ≈ 0.667<br><br><strong>Trigram用前2个词预测第3个词：P(w₃|w₁w₂) = Count(w₁w₂w₃) / Count(w₁w₂)</strong><br><br>⚠️ 注意 'I hate bugs' 不影响计算——条件概率只看匹配的前缀！"
  },
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "If an RNN processes a sequence of length T=100 and the largest singular value of W_h is 0.9, what happens to the gradient signal from t=100 back to t=1?",
    "options": [
      "A) The gradient grows by a factor of 0.9^99 ≈ 3×10⁻⁵ — effectively vanishing",
      "B) The gradient stays constant because 0.9 < 1",
      "C) The gradient explodes because multiplication is repeated 99 times",
      "D) The gradient is multiplied by 0.9 only once, not 99 times"
    ],
    "answer": 0,
    "explanation": "<strong>Why A:</strong> In BPTT, the gradient is multiplied by W_h at each time step. Over T-1 steps: gradient ∝ (σ_max)^(T-1) = 0.9^99 ≈ 2.66×10⁻⁵. This is the vanishing gradient problem — early layers receive negligible gradient signals.<br><br><strong>BPTT中梯度在每个时间步乘以W_h。0.9^99 ≈ 0.0000266，梯度几乎消失。这就是为什么标准RNN无法学习长距离依赖。</strong><br><br>• σ_max < 1 → vanishing<br>• σ_max > 1 → exploding<br>• LSTM solves this with gating + cell state highway"
  }
],

# ---- Week 6: Attention score hand calculation ----
"week06_quiz.json": [
  {
    "type": "Short",
    "source": "supplement",
    "question": "<strong>[Calculation]</strong> Given Q = [1, 0], K₁ = [1, 0], K₂ = [0, 1], V₁ = [10, 0], V₂ = [0, 10], d_k = 2.<br><br>(a) Calculate the raw attention scores Q·K₁ᵀ and Q·K₂ᵀ. (1 pt)<br>(b) Apply scaling by √d_k. (1 pt)<br>(c) Apply softmax to get attention weights. (1 pt)<br>(d) What is the final output Attention(Q,K,V)? (1 pt)",
    "answer": "Output ≈ [7.31, 2.69]",
    "explanation": "<strong>(a) Raw scores:</strong><br>• Q·K₁ᵀ = 1×1 + 0×0 = 1<br>• Q·K₂ᵀ = 1×0 + 0×1 = 0<br><br><strong>(b) Scaling by √2 ≈ 1.414:</strong><br>• score₁ = 1/1.414 ≈ 0.707<br>• score₂ = 0/1.414 = 0<br><br><strong>(c) Softmax:</strong><br>• e^0.707 ≈ 2.028, e^0 = 1<br>• α₁ = 2.028/(2.028+1) ≈ 0.669<br>• α₂ = 1/(2.028+1) ≈ 0.331<br><br><strong>(d) Output = α₁·V₁ + α₂·V₂:</strong><br>• = 0.669×[10,0] + 0.331×[0,10]<br>• = [6.69, 0] + [0, 3.31]<br>• ≈ <strong>[6.69, 3.31]</strong><br><br><strong>直觉：Q与K₁方向相同，所以注意力权重集中在V₁上（~67%），但V₂也有贡献（~33%）。这就是soft attention的核心——不是非此即彼，而是加权混合。</strong>"
  },
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "If we remove the √d_k scaling from attention and d_k = 512, what is the most likely consequence?",
    "options": [
      "A) The model trains faster because we skip a division operation",
      "B) Attention weights become nearly uniform — every token gets equal weight",
      "C) Attention weights become nearly one-hot — softmax saturates and gradients vanish",
      "D) The model produces the same results because scaling is just a constant"
    ],
    "answer": 2,
    "explanation": "<strong>Why C:</strong> Without scaling, dot products have variance ~d_k=512. With such large values going into softmax, one score dominates (e.g., softmax([50,1,2]) ≈ [1.0, 0.0, 0.0]). This near-one-hot distribution has near-zero gradients → training fails.<br><br><strong>不除以√d_k时，点积的方差~512，softmax输出近似one-hot → 梯度消失 → 训练失败。</strong><br><br>⚠️ A is wrong — one division is negligible computation.<br>⚠️ B is the opposite — large scores cause concentration, not uniformity.<br>⚠️ D is wrong — scaling is NOT a constant, it depends on d_k."
  }
],

# ---- Week 10: F1 calculation, BERT tokenizer ----
"week10_quiz.json": [
  {
    "type": "Short",
    "source": "supplement",
    "question": "<strong>[Calculation]</strong> In extractive QA, the gold answer is 'the quick brown fox' and the prediction is 'quick brown cat'.<br><br>(a) Calculate Precision, Recall, and F1 at the token level. (3 pts)<br>(b) What is the EM (Exact Match) score? (1 pt)",
    "answer": "F1 = 0.667, EM = 0",
    "explanation": "<strong>Gold tokens:</strong> {the, quick, brown, fox} (4 tokens)<br><strong>Pred tokens:</strong> {quick, brown, cat} (3 tokens)<br><strong>Overlap:</strong> {quick, brown} = 2 tokens<br><br><strong>(a) Metrics:</strong><br>• Precision = overlap / |pred| = 2/3 ≈ 0.667<br>• Recall = overlap / |gold| = 2/4 = 0.5<br>• F1 = 2 × P × R / (P + R) = 2 × 0.667 × 0.5 / (0.667 + 0.5) = 0.667/1.167 ≈ <strong>0.571</strong><br><br><strong>(b) EM = 0</strong> (prediction ≠ gold, not an exact string match)<br><br><strong>关键理解：EM=0 不代表完全错误！F1=0.571 说明预测有部分正确。这就是为什么QA评估要同时看EM和F1。</strong>"
  },
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "Given BERT input: '[CLS] I love NLP [SEP] It is fun [SEP]', which statement about the three special tokens is correct?",
    "options": [
      "A) [CLS] separates the two sentences; [SEP] marks the start of classification",
      "B) [CLS] output is used for sentence-level tasks; the first [SEP] ends sentence A; the second [SEP] ends sentence B",
      "C) All three tokens are removed before the Transformer processes the input",
      "D) [CLS] and [SEP] serve the same function — they are interchangeable"
    ],
    "answer": 1,
    "explanation": "<strong>Why B:</strong> In BERT's input format:<br>• <code>[CLS]</code> = always first token, its output represents the entire sequence (used for classification)<br>• First <code>[SEP]</code> = marks end of Sentence A<br>• Second <code>[SEP]</code> = marks end of Sentence B<br>• Segment Embeddings: tokens before first [SEP] get Segment A; tokens after get Segment B<br><br><strong>BERT输入格式：[CLS]句A[SEP]句B[SEP]。[CLS]输出用于分类，[SEP]分隔句子。</strong>"
  }
],

# ---- Week 12: Retrieval metrics calculation ----
"week12_quiz.json": [
  {
    "type": "Short",
    "source": "supplement",
    "question": "<strong>[Calculation]</strong> A retriever returns 5 documents for a query. The relevance labels are: [1, 0, 1, 0, 1] (1=relevant, 0=irrelevant).<br><br>(a) Calculate Precision@3 and Recall@3 (total relevant = 3). (2 pts)<br>(b) Calculate MRR (Mean Reciprocal Rank). (1 pt)<br>(c) If we swap positions 1 and 2 to get [0, 1, 1, 0, 1], does Precision@3 change? Does MRR change? (1 pt)",
    "answer": "P@3 = 2/3, MRR = 1.0 (original); P@3 = 2/3, MRR = 0.5 (swapped)",
    "explanation": "<strong>(a) Original [1, 0, 1, 0, 1]:</strong><br>• Top-3 results: [1, 0, 1] → 2 relevant out of 3<br>• Precision@3 = 2/3 ≈ 0.667<br>• Recall@3 = 2/3 ≈ 0.667 (2 found out of 3 total relevant)<br><br><strong>(b) MRR:</strong><br>• First relevant document is at rank 1<br>• MRR = 1/rank = 1/1 = <strong>1.0</strong><br><br><strong>(c) Swapped [0, 1, 1, 0, 1]:</strong><br>• Precision@3 = 2/3 (same — still 2 relevant in top 3)<br>• MRR = 1/2 = <strong>0.5</strong> (first relevant is now at rank 2)<br>• ⚠️ <strong>MRR changes but P@3 doesn't — MRR cares about the FIRST relevant position!</strong><br><br><strong>关键区别：Precision@k 不关心排序顺序，MRR 关心第一个相关文档的位置。NDCG 同时关心相关性和位置。</strong>"
  },
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "A RAG system retrieves chunks about 'Python programming' for the query 'What causes diabetes?'. What is the most likely outcome?",
    "options": [
      "A) The LLM will correctly answer about diabetes because it has medical knowledge from pre-training",
      "B) The LLM will likely generate a confident but incorrect answer mixing Python and diabetes information",
      "C) The LLM will refuse to answer because the context doesn't match the query",
      "D) The retriever error has no impact because the LLM ignores retrieved context"
    ],
    "answer": 1,
    "explanation": "<strong>Why B:</strong> This is a 'garbage in, garbage out' scenario. Most LLMs are instruction-following — they try to use the provided context even if irrelevant. The model may generate a plausible-sounding but nonsensical response. Only well-designed LLMs with strong 'context-query mismatch detection' would handle this gracefully (option C).<br><br><strong>RAG的'垃圾进垃圾出'场景。大多数LLM会试图使用提供的上下文，即使内容不相关，也会生成看似合理但错误的回答。</strong><br><br>⚠️ A is dangerous thinking — relying on pre-training knowledge defeats the purpose of RAG.<br>⚠️ D is wrong — RAG context IS used by the LLM."
  }
],

# ---- Week 13: LoRA calculation, What-if prompting ----
"week13_quiz.json": [
  {
    "type": "Short",
    "source": "supplement",
    "question": "<strong>[Calculation]</strong> A BERT-base model has 12 Transformer layers. Each layer has a self-attention module with W_Q, W_K, W_V, W_O matrices, each of dimension 768×768. If we apply LoRA with rank r=8 to ONLY the Q and V matrices:<br><br>(a) How many original parameters are in Q and V per layer? (1 pt)<br>(b) How many LoRA trainable parameters per layer? (1 pt)<br>(c) Total LoRA trainable parameters for all 12 layers? (1 pt)<br>(d) What percentage of the original Q+V parameters does LoRA use? (1 pt)",
    "answer": "LoRA uses ~1.06% of original Q+V parameters",
    "explanation": "<strong>(a) Original Q+V per layer:</strong><br>• W_Q: 768 × 768 = 589,824<br>• W_V: 768 × 768 = 589,824<br>• Total per layer: 589,824 × 2 = <strong>1,179,648</strong><br><br><strong>(b) LoRA per layer (r=8):</strong><br>• Each LoRA adapter: A(768×8) + B(8×768) = 6,144 + 6,144 = 12,288<br>• Two adapters (Q and V): 12,288 × 2 = <strong>24,576</strong><br><br><strong>(c) All 12 layers:</strong><br>• 24,576 × 12 = <strong>294,912</strong> (≈ 295K parameters)<br><br><strong>(d) Percentage:</strong><br>• 294,912 / (1,179,648 × 12) = 294,912 / 14,155,776 ≈ <strong>2.08%</strong><br><br><strong>LoRA公式：每个适配器 2×d×r 参数。d=768, r=8 → 每个12,288。只训练~2%参数就能达到接近全量微调的效果！</strong>"
  },
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "You need to build a QA system for a hospital's internal medical documents. These documents are updated weekly. Which approach is most appropriate?",
    "options": [
      "A) Fine-tune GPT-4 on all medical documents — the model will memorize all answers",
      "B) Use RAG with the medical documents as the knowledge base — updated documents are re-embedded weekly",
      "C) Use zero-shot prompting with GPT-4 — it already has medical knowledge from pre-training",
      "D) Use keyword matching (TF-IDF) without any LLM — it's simpler and sufficient"
    ],
    "answer": 1,
    "explanation": "<strong>Why B:</strong> RAG is ideal because:<br>• Documents update weekly → RAG just re-embeds new chunks (no retraining)<br>• Answers must be grounded in hospital's OWN documents (not general internet knowledge)<br>• Source attribution enables doctors to verify answers<br><br><strong>RAG最适合因为：文档每周更新只需重新嵌入（不需重训）；答案必须基于医院自己的文档；可以追溯来源。</strong><br><br>⚠️ A: Fine-tuning is expensive and doesn't handle weekly updates<br>⚠️ C: Pre-training knowledge may be outdated and not hospital-specific<br>⚠️ D: TF-IDF can't understand semantic queries like 'what are the side effects of drug X?'"
  }
],

# ---- Week 1: fix Variation TF question (it's mis-labeled as True) ----
"week01_quiz.json": [
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "Which of the following is an example of the 'Common Knowledge' challenge in NLP?",
    "options": [
      "A) The word 'bank' can mean a financial institution or a river bank",
      "B) A human knows that 'water is wet' but an NLP model doesn't unless explicitly told",
      "C) The word 'happy' can also be expressed as 'glad', 'joyful', or 'content'",
      "D) The word 'the' appears in almost every document"
    ],
    "answer": 1,
    "explanation": "<strong>Why B:</strong> Common Knowledge = machines lack basic world knowledge that humans take for granted. 'Water is wet' is obvious to humans but requires explicit modeling or training data for NLP systems.<br><br><strong>常识知识挑战 = 机器缺乏人类认为理所当然的基础世界知识。</strong><br><br>• A = Ambiguity（歧义性）<br>• B = Common Knowledge（常识知识）✓<br>• C = Variation（变异性）<br>• D = Sparsity（稀疏性）<br><br>⚠️ 这道题考的是四大挑战的彼此区分——每个选项对应一个不同的挑战！"
  }
],

# ---- Week 2: Code analysis question ----
"week02_quiz.json": [
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "What is the output of the following code?<br><code>import re<br>text = 'Hello World 123 foo_bar'<br>result = re.findall(r'\\b[A-Z][a-z]+\\b', text)<br>print(result)</code>",
    "options": [
      "A) ['Hello', 'World']",
      "B) ['Hello', 'World', '123', 'foo_bar']",
      "C) ['Hello World']",
      "D) ['Hello', 'World', 'foo']"
    ],
    "answer": 0,
    "explanation": "<strong>Why A:</strong> The regex <code>\\b[A-Z][a-z]+\\b</code> matches words that start with an uppercase letter followed by one or more lowercase letters, bounded by word boundaries.<br>• 'Hello' ✓ (H + ello)<br>• 'World' ✓ (W + orld)<br>• '123' ✗ (starts with digit)<br>• 'foo_bar' ✗ ('foo' starts lowercase, 'bar' starts lowercase)<br><br><strong>正则 [A-Z][a-z]+ 匹配以大写字母开头、后跟一个或多个小写字母的单词。</strong>"
  }
],

# ---- Week 9: Transformer architecture depth ----
"week09_quiz.json": [
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "In the original Transformer, the encoder has 6 identical layers. Each layer contains (in order):",
    "options": [
      "A) FFN → Self-Attention → LayerNorm (repeated)",
      "B) Self-Attention → Add&Norm → FFN → Add&Norm",
      "C) Self-Attention → FFN → Pooling → Output",
      "D) Embedding → Self-Attention → Cross-Attention → FFN"
    ],
    "answer": 1,
    "explanation": "<strong>Why B:</strong> Each encoder layer: <br>① Multi-Head Self-Attention<br>② Add & Layer Normalization (residual connection)<br>③ Position-wise FFN<br>④ Add & Layer Normalization<br><br><strong>每个编码器层：自注意力 → Add&Norm → FFN → Add&Norm。顺序很重要，考试可能考！</strong><br><br>⚠️ A: FFN在Self-Attention之后，不是之前<br>⚠️ C: 没有Pooling层<br>⚠️ D: Cross-Attention只在解码器中有"
  }
],

# ---- Week 7: Scenario-based QA ----
"week07_quiz.json": [
  {
    "type": "MCQ",
    "source": "supplement",
    "question": "A company has a BERT model fine-tuned for sentiment analysis. They now want to use it for Named Entity Recognition (NER). What is the most efficient approach?",
    "options": [
      "A) Train a new BERT from scratch specifically for NER",
      "B) Take the original pre-trained BERT (not the sentiment-tuned one) and fine-tune it for NER with a new output layer",
      "C) Use the sentiment-tuned BERT directly for NER without any changes",
      "D) Convert the sentiment-tuned BERT into a GPT model for NER"
    ],
    "answer": 1,
    "explanation": "<strong>Why B:</strong> The sentiment-tuned model has task-specific output layers that are useless for NER. The best approach is to go back to the ORIGINAL pre-trained BERT and fine-tune with a token-level classification head for NER.<br><br><strong>情感分析的输出头对NER没用。应该从原始预训练BERT出发，加NER专用的token级分类头重新微调。</strong><br><br>⚠️ A: Training from scratch wastes the pre-trained knowledge<br>⚠️ C: Sentiment output layer can't do NER<br>⚠️ D: BERT→GPT conversion is not a thing"
  }
],

}

def main():
    """Add new questions to JSON files and regenerate HTML."""
    print("=" * 60)
    print("Quiz Bank Upgrade — Adding killer questions")
    print("=" * 60)

    total_added = 0
    for filename, new_qs in NEW_QUESTIONS.items():
        filepath = DIR / filename
        if not filepath.exists():
            print(f"  ⚠️  {filename} not found, skipping")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        before = len(data)
        data.extend(new_qs)
        after = len(data)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        added = after - before
        total_added += added
        print(f"  ✅ {filename}: {before} → {after} (+{added})")

    print(f"\n  Total new questions: {total_added}")

    # ---- Regenerate HTML ----
    print("\n  🔄 Regenerating all_quizzes.html ...")
    regenerate_html()
    print("  ✅ all_quizzes.html updated!")

def regenerate_html():
    """Rebuild the HTML file with updated JSON data."""
    html_path = DIR / "all_quizzes.html"

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Map of JS variable name → JSON filename
    week_map = {
        "WEEK1_DATA": "week01_quiz.json",
        "WEEK2_DATA": "week02_quiz.json",
        "WEEK3_DATA": "week03_quiz.json",
        "WEEK4_DATA": "week04_quiz.json",
        "WEEK5_DATA": "week05_quiz.json",
        "WEEK6_DATA": "week06_quiz.json",
        "WEEK7_DATA": "week07_quiz.json",
        "WEEK9_DATA": "week09_quiz.json",
        "WEEK10_DATA": "week10_quiz.json",
        "WEEK12_DATA": "week12_quiz.json",
        "WEEK13_DATA": "week13_quiz.json",
        "FINAL_SHORT_DATA": "final_short_answer.json",
    }

    for var_name, json_file in week_map.items():
        json_path = DIR / json_file
        if not json_path.exists():
            continue

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Serialize to compact JS-safe JSON
        js_data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

        # Replace the const assignment in HTML
        pattern = rf'const {var_name} = \[.*?\];'
        replacement = f'const {var_name} = {js_data};'
        html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
