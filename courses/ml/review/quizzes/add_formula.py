"""Add formula field to Short answer questions in all quiz JSON files."""
import json, os, glob

FORMULAS = {
    # midterm
    "CNN Dimension Calculation": "Conv Output: $O = \\frac{I - F + 2P}{S} + 1$ &nbsp;&nbsp; Same Padding: $O = I$ &nbsp;&nbsp; Pool: $O = \\frac{I}{S}$ &nbsp;&nbsp; FC Params: $= n_{in} \\times n_{out} + n_{out}$",
    "RNN Architecture": "$h_t = f(W_x \\cdot x_t + W_h \\cdot h_{t-1} + b)$ &nbsp;&nbsp; MSE: $L = \\frac{1}{n}\\sum(y - \\hat{y})^2$ &nbsp;&nbsp; BCE: $L = -[y\\log\\hat{y} + (1-y)\\log(1-\\hat{y})]$",
    "Bayesian Network": "$P(X_1, \\ldots, X_n) = \\prod_{i=1}^{n} P(X_i \\mid \\text{Parents}(X_i))$",
    "Hierarchical Clustering with MAX": "MIN: $d = \\min_{x \\in C_i, y \\in C_j} d(x,y)$ &nbsp;&nbsp; MAX: $d = \\max_{x \\in C_i, y \\in C_j} d(x,y)$ &nbsp;&nbsp; Group Average: $d = \\frac{1}{|C_i||C_j|}\\sum d(x,y)$",
    # week09
    "confusion matrix": "$\\text{Precision} = \\frac{TP}{TP+FP}$ &nbsp;&nbsp; $\\text{Recall} = \\frac{TP}{TP+FN}$ &nbsp;&nbsp; $F_1 = \\frac{2 \\cdot P \\cdot R}{P + R}$ &nbsp;&nbsp; $\\text{FPR} = \\frac{FP}{FP+TN}$ &nbsp;&nbsp; $\\text{Acc} = \\frac{TP+TN}{TP+FP+FN+TN}$",
    "Outlier Detection": "$\\text{LOF}(x) = \\frac{\\text{avg density of neighbors}}{\\text{density of } x}$ &nbsp;&nbsp; OCSVM: $f(x) \\geq 0 \\rightarrow \\text{Normal}$, $f(x) < 0 \\rightarrow \\text{Outlier}$",
    # week10
    "Compare Bagging and Boosting": "$\\alpha = \\frac{1}{2} \\ln\\frac{1 - \\varepsilon}{\\varepsilon}$ &nbsp;&nbsp; Correct: $w \\times e^{-\\alpha}$ &nbsp;&nbsp; Misclassified: $w \\times e^{+\\alpha}$ &nbsp;&nbsp; $P(\\text{included}) \\approx 1 - \\frac{1}{e} \\approx 0.632$",
    "AdaBoost Weight Update": "$\\alpha = \\frac{1}{2} \\ln\\frac{1 - \\varepsilon}{\\varepsilon}$ &nbsp;&nbsp; Correct: $w' = w \\cdot e^{-\\alpha}$ &nbsp;&nbsp; Misclassified: $w' = w \\cdot e^{+\\alpha}$ &nbsp;&nbsp; Normalize: $\\sum w_i = 1$",
    "student argues": None,  # no formula needed
    # week11
    "Association Rule Mining: Given transactions": "$\\text{Support} = \\frac{\\sigma(X \\cup Y)}{|T|}$ &nbsp;&nbsp; $\\text{Confidence} = \\frac{\\sigma(X \\cup Y)}{\\sigma(X)}$ &nbsp;&nbsp; Anti-monotone: $X \\subseteq Y \\Rightarrow s(X) \\geq s(Y)$ &nbsp;&nbsp; Rules: $2^k - 2$",
    "Besides market basket": None,
}

def match_formula(question):
    q_lower = question.lower()
    for key, formula in FORMULAS.items():
        if key.lower() in q_lower:
            return formula
    return None

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changed = False
    for q in data:
        if q.get('type') != 'Short':
            continue
        if 'formula' in q:
            continue  # already has formula
        
        formula = match_formula(q['question'])
        if formula:
            q['formula'] = formula
            changed = True
            print(f"  + Added formula to: {q['question'][:60]}...")
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] {os.path.basename(filepath)}")
    else:
        print(f"[--] {os.path.basename(filepath)}")
    return changed

def main():
    quiz_dir = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(quiz_dir, '*_quiz.json')))
    print(f"Found {len(files)} files\n")
    for f in files:
        process_file(f)

if __name__ == '__main__':
    main()
