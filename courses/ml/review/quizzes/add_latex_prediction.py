import json, re

path = r"c:\Users\40270\Desktop\workspace\aisd\courses\ml\review\quizzes\prediction_quiz.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

def add_latex(s):
    if not s:
        return s

    # Formulas - wrap known patterns in $...$
    # F1 formula
    s = re.sub(r'(?<!\$)F1 = 2pr / \(p \+ r\)(?!\$)', r'$F_1 = \\frac{2 \\cdot P \\cdot R}{P + R}$', s)
    s = re.sub(r'(?<!\$)F1 = 2 × p × r / \(p \+ r\)(?!\$)', r'$F_1 = \\frac{2 \\cdot P \\cdot R}{P + R}$', s)
    s = re.sub(r'(?<!\$)F1 = 2 × 0\.5 × 0\.8 / \(0\.5 \+ 0\.8\) = 0\.8 / 1\.3 ≈ 0\.615 ≈ 0\.62(?!\$)',
               r'$F_1 = \\frac{2 \\times 0.5 \\times 0.8}{0.5 + 0.8} = \\frac{0.8}{1.3} \\approx 0.615 \\approx 0.62$', s)
    s = re.sub(r'(?<!\$)2×0\.667×0\.8/\(0\.667\+0\.8\) ≈ 0\.727(?!\$)',
               r'$\\frac{2 \\times 0.667 \\times 0.8}{0.667 + 0.8} \\approx 0.727$', s)

    # Precision, Recall, FPR, Accuracy formulas
    s = re.sub(r'Precision = 40/60 = 0\.667', r'$\\text{Precision} = \\frac{40}{60} = 0.667$', s)
    s = re.sub(r'Recall = 40/50 = 0\.8', r'$\\text{Recall} = \\frac{40}{50} = 0.8$', s)
    s = re.sub(r'Accuracy = 970/1000 = 97%', r'$\\text{Accuracy} = \\frac{970}{1000} = 97\\%$', s)
    s = re.sub(r'FPR = 20/950 ≈ 0\.021 \(2\.1%\)', r'$\\text{FPR} = \\frac{20}{950} \\approx 0.021$ (2.1%)', s)
    s = re.sub(r'FPR = 20/950 ≈ 0\.021（2\.1%）', r'$\\text{FPR} = \\frac{20}{950} \\approx 0.021$（2.1%）', s)

    # FPR/TPR formulas in explanation
    s = re.sub(r'FPR = FP / \(FP \+ TN\)', r'$\\text{FPR} = \\frac{FP}{FP+TN}$', s)
    s = re.sub(r'TPR = TP / \(TP \+ FN\)', r'$\\text{TPR} = \\frac{TP}{TP+FN}$', s)
    s = re.sub(r'(?<!\$)Recall(正类)? = 0/10 = 0%', r'$\\text{Recall} = 0/10 = 0\\%$', s)

    # Support/Confidence formulas
    s = re.sub(r'Confidence\(\{X\}→\{Y\}\) = Support\(\{X ∪ Y\}\) / Support\(\{X\}\)',
               r'$\\text{Confidence}(\\{X\\} \\to \\{Y\\}) = \\frac{\\text{Support}(\\{X \\cup Y\\})}{\\text{Support}(\\{X\\})}$', s)
    s = re.sub(r'Support（支持度）= σ\(Itemset\) / \|T\|',
               r'$\\text{Support} = \\frac{\\sigma(\\text{Itemset})}{|T|}$', s)
    s = re.sub(r'σ\(X ∪ Y\) / σ\(X\)', r'$\\frac{\\sigma(X \\cup Y)}{\\sigma(X)}$', s)
    s = re.sub(r'σ\(\{Milk,Diaper,Beer\}\) / σ\(\{Milk,Diaper\}\) = 2/3',
               r'$\\frac{\\sigma(\\{\\text{Milk,Diaper,Beer}\\})}{\\sigma(\\{\\text{Milk,Diaper}\\})} = \\frac{2}{3}$', s)
    s = re.sub(r'Support = 2/5 = 0\.4, Confidence = 2/4 = 0\.5',
               r'$\\text{Support} = \\frac{2}{5} = 0.4$, $\\text{Confidence} = \\frac{2}{4} = 0.5$', s)
    s = re.sub(r'Support = 2/5 = 0\.4(?!,)', r'$\\text{Support} = \\frac{2}{5} = 0.4$', s)
    s = re.sub(r'σ\(X∪Y\)/\|T\|', r'$\\sigma(X \\cup Y) / |T|$', s)
    s = re.sub(r'σ\(X∪Y\)/σ\(X\)', r'$\\sigma(X \\cup Y) / \\sigma(X)$', s)
    s = re.sub(r'= 3/5 = 0\.6', r'$= \\frac{3}{5} = 0.6$', s)

    # AdaBoost alpha formula
    s = re.sub(r'α = ½ × ln\(\(1 − ε\) / ε\)', r'$\\alpha = \\frac{1}{2} \\ln\\frac{1-\\varepsilon}{\\varepsilon}$', s)
    s = re.sub(r'α = ½ × ln\(\(1−ε\)/ε\)', r'$\\alpha = \\frac{1}{2} \\ln\\frac{1-\\varepsilon}{\\varepsilon}$', s)
    s = re.sub(r'α₁ = ½ × ln\(0\.7/0\.3\) = ½ × ln\(2\.333\) ≈ 0\.424',
               r'$\\alpha_1 = \\frac{1}{2} \\ln\\frac{0.7}{0.3} = \\frac{1}{2} \\ln 2.333 \\approx 0.424$', s)
    s = re.sub(r'α = ½ × ln\(\(1−0\.3\)/0\.3\) = ½ × ln\(2\.333\) ≈ 0\.424',
               r'$\\alpha = \\frac{1}{2} \\ln\\frac{0.7}{0.3} = \\frac{1}{2} \\ln 2.333 \\approx 0.424$', s)

    # Bootstrap probability
    s = re.sub(r'1 − \(1 − 1/n\)\^n', r'$1 - (1-\\frac{1}{n})^n$', s)
    s = re.sub(r'\(1−1/n\)\^n → 1/e ≈ 0\.368', r'$(1-\\frac{1}{n})^n \\to \\frac{1}{e} \\approx 0.368$', s)

    # Association rule count
    s = re.sub(r'(?<!\$)2\^k − 2(?!\$)', r'$2^k - 2$', s)
    s = re.sub(r'(?<!\$)2\^k(?!\s*−)(?!\$)', r'$2^k$', s)
    s = re.sub(r'(?<!\$)2\^D − 1(?!\$)', r'$2^D - 1$', s)

    # OCSVM decision function
    s = re.sub(r'f\(x\) = w·φ\(x\) - ρ', r'$f(x) = \\mathbf{w} \\cdot \\varphi(x) - \\rho$', s)
    s = re.sub(r'f\(x\) ≥ 0', r'$f(x) \\geq 0$', s)
    s = re.sub(r'f\(x\) < 0', r'$f(x) < 0$', s)

    # LOF formula
    s = re.sub(r'relative_density\(x,k\) = \(邻居的平均密度\) / \(x的密度\)',
               r'$\\text{relative\\_density}(x,k) = \\frac{\\text{avg density of neighbors}}{\\text{density of } x}$', s)

    # Weight update formulas
    s = re.sub(r'×e\^\(-α\)≈0\.655', r'$\\times e^{-\\alpha} \\approx 0.655$', s)
    s = re.sub(r'×e\^\(\+α\)≈1\.528', r'$\\times e^{+\\alpha} \\approx 1.528$', s)
    s = re.sub(r'e\^\(-0\.424\) ≈ 0\.655', r'$e^{-0.424} \\approx 0.655$', s)
    s = re.sub(r'e\^\(\+0\.424\) ≈ 1\.528', r'$e^{+0.424} \\approx 1.528$', s)

    # Anti-monotone property
    s = re.sub(r'∀X ⊆ Y: s\(X\) ≥ s\(Y\)', r'$\\forall X \\subseteq Y: s(X) \\geq s(Y)$', s)

    # AUC values
    s = re.sub(r'AUC = 0\.5', r'$\\text{AUC} = 0.5$', s)
    s = re.sub(r'AUC = 1\.0', r'$\\text{AUC} = 1.0$', s)
    s = re.sub(r'AUC = 0\.0', r'$\\text{AUC} = 0.0$', s)

    # Error rate threshold
    s = re.sub(r'ε = 0\.5 时 α = 0', r'$\\varepsilon = 0.5$ 时 $\\alpha = 0$', s)

    # Clean up double-dollar artifacts
    s = s.replace('$$', '$')

    return s

# Add formula fields for Short questions
def add_formula_field(q):
    if q["type"] == "Short":
        qtext = q.get("question", "")
        if "Confusion Matrix" in qtext or "Precision" in qtext:
            q["formula"] = "$\\text{Precision} = \\frac{TP}{TP+FP}$ &nbsp;&nbsp; $\\text{Recall} = \\frac{TP}{TP+FN}$ &nbsp;&nbsp; $F_1 = \\frac{2 \\cdot P \\cdot R}{P + R}$ &nbsp;&nbsp; $\\text{FPR} = \\frac{FP}{FP+TN}$ &nbsp;&nbsp; $\\text{Acc} = \\frac{TP+TN}{TP+FP+FN+TN}$"
        elif "Association Rule Mining Calc" in qtext:
            q["formula"] = "$\\text{Support} = \\frac{\\sigma(X \\cup Y)}{|T|}$ &nbsp;&nbsp; $\\text{Confidence} = \\frac{\\sigma(X \\cup Y)}{\\sigma(X)}$"
        elif "Bagging vs Boosting" in qtext:
            q["formula"] = "$\\alpha = \\frac{1}{2} \\ln \\frac{1-\\varepsilon}{\\varepsilon}$"
        elif "AdaBoost Weight" in qtext:
            q["formula"] = "$\\alpha = \\frac{1}{2} \\ln \\frac{1-\\varepsilon}{\\varepsilon}$ &nbsp;&nbsp; Correct: $w \\times e^{-\\alpha}$ &nbsp;&nbsp; Misclassified: $w \\times e^{+\\alpha}$"
        elif "Outlier" in qtext:
            q["formula"] = "$\\text{LOF}(x) = \\frac{\\text{avg density of neighbors}}{\\text{density of } x}$ &nbsp;&nbsp; OCSVM: $f(x) \\geq 0 \\to \\text{Normal}$, $f(x) < 0 \\to \\text{Outlier}$"

for q in data:
    for field in ["explanation", "explanation_zh", "answer", "answer_zh"]:
        if field in q and isinstance(q[field], str):
            q[field] = add_latex(q[field])
    # Also add question_zh
    add_formula_field(q)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Done! LaTeX added to {len(data)} questions.")
