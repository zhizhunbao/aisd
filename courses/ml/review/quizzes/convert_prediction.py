import json, re

md_path = r"c:\Users\40270\Desktop\workspace\aisd\courses\ml\review\期末预测题_解析.md"
out_path = r"c:\Users\40270\Desktop\workspace\aisd\courses\ml\review\quizzes\prediction_quiz.json"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

results = []

# --- PART 1: TF Q1-Q10 ---
tf_pattern = re.compile(
    r"### Q(\d+)\.\s+(.*?)\n\n\*\*(TRUE|FALSE)\*\*.*?\n\n\*\*解析\*\*：(.*?)\n\n>",
    re.DOTALL
)
for m in tf_pattern.finditer(text):
    qnum = int(m.group(1))
    if qnum > 10:
        break
    question = m.group(2).strip()
    answer = "True" if m.group(3) == "TRUE" else "False"
    explanation_zh = m.group(4).strip()
    # Build English explanation from Chinese (simplified)
    results.append({
        "question": question,
        "type": "TF",
        "answer": answer,
        "explanation": explanation_zh,
        "explanation_zh": explanation_zh,
        "source": "predicted"
    })

# --- PART 2: MCQ Q11-Q30 ---
mcq_blocks = re.split(r"### Q(\d+)\.", text)
i = 1
while i < len(mcq_blocks):
    qnum = int(mcq_blocks[i])
    body = mcq_blocks[i+1]
    i += 2
    if qnum < 11 or qnum > 30:
        continue
    
    lines = body.strip().split("\n")
    question = lines[0].strip()
    
    options = []
    opt_pattern = re.compile(r"^[a-d]\)\s+(.*)")
    for line in lines:
        om = opt_pattern.match(line.strip())
        if om:
            options.append(om.group(1).strip())
    
    ans_match = re.search(r"\*\*✅ 答案: ([a-d])\)\*\*", body)
    if ans_match:
        answer_idx = ord(ans_match.group(1)) - ord('a')
    else:
        answer_idx = 0
    
    expl_match = re.search(r"\*\*解析\*\*：(.*?)(?:\n\n---|\n\n>|\Z)", body, re.DOTALL)
    explanation_zh = expl_match.group(1).strip() if expl_match else ""
    
    results.append({
        "question": question,
        "type": "MCQ",
        "options": options,
        "answer": answer_idx,
        "explanation": explanation_zh,
        "explanation_zh": explanation_zh,
        "source": "predicted"
    })

# --- PART 3: Written Q31-Q34 ---
written_questions = [
    {
        "question": "Confusion Matrix Calculations:\n(a) Calculate Precision, Recall, and F1-measure.\n(b) Calculate Accuracy. Is it reliable here? Explain.\n(c) Calculate FPR and explain its meaning.",
        "type": "Short",
        "answer": "(a) Precision = 40/60 = 0.667, Recall = 40/50 = 0.8, F1 = 2×0.667×0.8/(0.667+0.8) ≈ 0.727\n(b) Accuracy = 970/1000 = 97%. NOT reliable — data is imbalanced (YES=50, NO=950).\n(c) FPR = 20/950 ≈ 0.021 (2.1%). 2.1% of healthy people are falsely diagnosed.",
        "explanation": "在不平衡数据中，accuracy 具有误导性。F1 (0.727) 比 accuracy (97%) 更真实地反映模型性能。",
        "explanation_zh": "在不平衡数据中，accuracy 具有误导性。F1 (0.727) 比 accuracy (97%) 更真实地反映模型性能。FPR 在医疗检测中表示健康患者的误诊率。",
        "source": "predicted",
        "points": 18
    },
    {
        "question": "Association Rule Mining Calculations:\n(a) Find all frequent 1-itemsets and 2-itemsets (min support count = 2).\n(b) Using the Apriori principle, which 3-itemset candidates can be pruned? Find the frequent 3-itemsets.\n(c) Calculate the support and confidence of {A} → {B, C}.",
        "type": "Short",
        "answer": "(a) Freq 1-itemsets: {A}=4, {B}=4, {C}=4, {D}=2. Freq 2-itemsets: {A,B}=3, {A,C}=3, {B,C}=3, {B,D}=2, {C,D}=2. {A,D}=1 pruned.\n(b) {A,B,D} and {A,C,D} pruned (contain {A,D} which is infrequent). Freq 3-itemsets: {A,B,C}=2, {B,C,D}=2.\n(c) Support = 2/5 = 0.4, Confidence = 2/4 = 0.5.",
        "explanation": "Apriori 原则：非频繁项集的超集也非频繁。{A,D} 非频繁所以包含它的3-项集被剪枝。",
        "explanation_zh": "Apriori 原则：非频繁项集的超集也非频繁。{A,D} 非频繁所以包含它的3-项集被剪枝。Support = σ(X∪Y)/|T|，Confidence = σ(X∪Y)/σ(X)。",
        "source": "predicted",
        "points": 18
    },
    {
        "question": "Bagging vs Boosting Comparison + Calculation:\n(a) Compare Bagging and Boosting in: sampling method, training order, voting mechanism.\n(b) In AdaBoost, ε = 0.3. Calculate α.\n(c) Three classifiers predict +1, -1, +1. What is the ensemble prediction by majority voting?",
        "type": "Short",
        "answer": "(a) Bagging: bootstrap (with replacement), parallel, simple majority vote. Boosting: weighted sampling, sequential, weighted vote.\n(b) α = ½ × ln((1−0.3)/0.3) = ½ × ln(2.333) ≈ 0.424.\n(c) +1 gets 2 votes, -1 gets 1 → Ensemble = +1.",
        "explanation": "Bagging 降低 Variance（并行独立学习），Boosting 降低 Bias（顺序专注错误）。",
        "explanation_zh": "Bagging 降低 Variance（并行独立学习），Boosting 降低 Bias（顺序专注错误）。α = ½ × ln((1−ε)/ε)，ε 越小 α 越大。",
        "source": "predicted",
        "points": 18
    },
    {
        "question": "Outlier Detection Concepts + Calculation:\n(a) List and briefly describe three different outlier detection methods.\n(b) In OCSVM, explain f(x) ≥ 0 vs f(x) < 0 and what ν controls.\n(c) Explain reconstruction-based outlier detection with an example.",
        "type": "Short",
        "answer": "(a) Statistical (probability distribution), Proximity-based (k-NN distance), Density-based (LOF relative density).\n(b) f(x) ≥ 0 → Normal. f(x) < 0 → Outlier. ν = upper bound on fraction of outliers.\n(c) Compress → Reconstruct → High reconstruction error = Outlier. Methods: PCA, Auto-encoder.",
        "explanation": "三种检测方法各适用于不同场景。OCSVM 使用 ν 控制边界松紧。基于重建的方法假设正常数据具有低维模式。",
        "explanation_zh": "三种检测方法各适用于不同场景。OCSVM 使用 ν 控制边界松紧。基于重建的方法假设正常数据具有低维模式。",
        "source": "predicted",
        "points": 18
    }
]
results.extend(written_questions)

# --- PART 4-1: Supplement TF Q35-Q49 ---
supp_tf_pattern = re.compile(
    r"\*\*Q(\d+)\.\s+(.*?)\*\*\n\n\*\*(TRUE|FALSE)\*\*.*?\n\n\*\*解析\*\*：(.*?)\n\n>",
    re.DOTALL
)
for m in supp_tf_pattern.finditer(text):
    qnum = int(m.group(1))
    if qnum < 35 or qnum > 49:
        continue
    question = m.group(2).strip()
    answer = "True" if m.group(3) == "TRUE" else "False"
    explanation_zh = m.group(4).strip()
    results.append({
        "question": question,
        "type": "TF",
        "answer": answer,
        "explanation": explanation_zh,
        "explanation_zh": explanation_zh,
        "source": "predicted-supplement"
    })

# --- PART 4-2: Supplement Written Q50, Q51, Q53 ---
supp_written = [
    {
        "question": "A student argues: 'Ensemble methods like Bagging are explainable because we can tell the user that 10 different classifiers voted and we took the majority.' Is this correct? Explain why.",
        "type": "Short",
        "answer": "Incorrect. Explaining the majority voting process ≠ explainability. Users want to know WHY each classifier made its decision, not just that 10 classifiers voted. With hundreds of features and millions of data points, even a single classifier is hard to explain.",
        "explanation": "教授核心论点：解释多数投票过程本身不等于透明性。用户想要的是每个分类器为什么做出那样决定的具体解释。集成方法不具有可解释性是其主要局限。",
        "explanation_zh": "教授核心论点：解释多数投票过程本身不等于透明性。用户想要的是每个分类器为什么做出那样决定的具体解释。集成方法不具有可解释性是其主要局限。",
        "source": "predicted-supplement",
        "points": 12
    },
    {
        "question": "AdaBoost Weight Update Process:\n(a) 10 samples, initial weight 1/10, ε₁ = 0.3. Calculate α₁.\n(b) Describe weight changes for correctly and misclassified samples.\n(c) In round 2, is sample 8 (misclassified in round 1) more or less likely to be selected? Why?",
        "type": "Short",
        "answer": "(a) α₁ = ½ × ln(0.7/0.3) = ½ × ln(2.333) ≈ 0.424.\n(b) Correct samples: weight DOWN (×e^(-α)≈0.655). Misclassified: weight UP (×e^(+α)≈1.528). Sum normalized to 1.\n(c) More likely — its weight increased, so larger area on the 'roulette wheel'.",
        "explanation": "AdaBoost 中错误分类的样本权重增加，正确分类的权重减少。教授用轮盘赌比喻：权重越高占面积越大，被选中概率越高。",
        "explanation_zh": "AdaBoost 中错误分类的样本权重增加，正确分类的权重减少。教授用轮盘赌比喻：权重越高占面积越大，被选中概率越高。",
        "source": "predicted-supplement",
        "points": 12
    },
    {
        "question": "Association Rule Mining Applications:\n(a) Besides market basket analysis, give two real-world applications.\n(b) How can association rules be used for two opposing product placement strategies?\n(c) Why do association rules need periodic updates?",
        "type": "Short",
        "answer": "(a) Insurance fraud detection (finding recurring fraud patterns), Recommendation systems ('customers who bought X also bought Y').\n(b) Strategy 1: Close placement for convenience. Strategy 2: Far placement to encourage browsing and impulse buying.\n(c) Consumer patterns change with seasons/time. E.g., Thanksgiving increases turkey purchases. Rules must be updated with new transaction data.",
        "explanation": "关联规则不是静态的，消费模式随季节和时间变化。教授举了感恩节火鸡的例子说明规则需要定期更新。",
        "explanation_zh": "关联规则不是静态的，消费模式随季节和时间变化。教授举了感恩节火鸡的例子说明规则需要定期更新。",
        "source": "predicted-supplement",
        "points": 12
    }
]
results.extend(supp_written)

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Done! {len(results)} questions written to {out_path}")
for t in ["TF", "MCQ", "Short"]:
    count = sum(1 for q in results if q["type"] == t)
    print(f"  {t}: {count}")
