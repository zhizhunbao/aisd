"""
Convert plain-text math formulas in quiz JSON files to LaTeX $...$ notation.
Handles: IDF, TF, cosine, attention formulas, subscripts, superscripts, etc.
"""
import json
import re
import glob
import os

# ===== Replacement rules =====
# Each rule: (regex_pattern, replacement)
# Applied in ORDER — put more specific patterns first.

LATEX_RULES = [
    # ---- Block formulas (display math) ----
    # Attention formula
    (r'Attention\(Q,\s*K,\s*V\)\s*=\s*softmax\(QK\^T\s*/\s*√d_k\)\s*×\s*V',
     r'$$\\text{Attention}(Q,K,V) = \\text{softmax}\\!\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right) V$$'),
    (r'Attention\(Q,K,V\)\s*=\s*softmax\(QK<sup>T</sup>\s*/\s*√d_k\)\s*×\s*V',
     r'$$\\text{Attention}(Q,K,V) = \\text{softmax}\\!\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right) V$$'),

    # ---- Inline math patterns ----

    # h_t = f(W_h·h_{t-1} + W_x·x_t + b)
    (r'h_t\s*=\s*f\(W_h·h_\{t-1\}\s*\+\s*W_x·x_t\s*\+\s*b\)',
     r'$h_t = f(W_h \\cdot h_{t-1} + W_x \\cdot x_t + b)$'),

    # ∂L/∂θ
    (r'∂L/∂θ', r'$\\partial L / \\partial \\theta$'),

    # IDF(t) = log(N / df(t))  or  IDF = log(N/df)
    (r'IDF\(t\)\s*=\s*log\(N\s*/\s*df\(t\)\)',  r'$\\text{IDF}(t) = \\log\\!\\left(\\frac{N}{\\text{df}(t)}\\right)$'),
    (r'IDF\s*=\s*log\(N/df\)',                    r'$\\text{IDF} = \\log(N/\\text{df})$'),
    (r'IDF\s*=\s*log\(N/N\)\s*=\s*log\(1\)\s*=\s*0',  r'$\\text{IDF} = \\log(N/N) = \\log(1) = 0$'),

    # TF-IDF = TF × IDF
    (r'TF-IDF\s*=\s*TF\s*×\s*IDF',  r'$\\text{TF-IDF} = \\text{TF} \\times \\text{IDF}$'),

    # IDF = log₂(N/df) = log₂(2/1) = 1.0
    (r'IDF\(([^)]+)\)\s*=\s*log₂\(([^)]+)\)\s*=\s*([0-9.]+)',
     r'$\\text{IDF}(\\text{\\1}) = \\log_2(\\2) = \\3$'),
    (r'IDF\s*=\s*log₂\(([^)]+)\)\s*=\s*([0-9.]+)',
     r'$\\text{IDF} = \\log_2(\\1) = \\2$'),
    (r'log₂\(([^)]+)\)',  r'$\\log_2(\\1)$'),

    # TF(word, doc) = count / total = val
    (r'TF\(([^,]+),\s*([^)]+)\)\s*=\s*count\s*/\s*total\s*=\s*(\S+)\s*≈\s*(\S+)',
     r'$\\text{TF}(\\text{\\1}, \\text{\\2}) = \\frac{\\text{count}}{\\text{total}} = \\3 \\approx \\4$'),
    (r'TF\(([^,]+),\s*([^)]+)\)\s*=\s*(\S+)',
     r'$\\text{TF}(\\text{\\1}, \\text{\\2}) = \\3$'),

    # TF-IDF(word, doc) = value
    (r'TF-IDF\(([^,]+),\s*([^)]+)\)\s*=\s*(\S+)\s*×\s*(\S+)\s*=\s*(\S+)',
     r'$\\text{TF-IDF}(\\text{\\1}, \\text{\\2}) = \\3 \\times \\4 = \\5$'),

    # cos(θ) = ... / ...
    (r'cos\(θ\)\s*=\s*(\S+)\s*/\s*\(([^)]+)\)\s*≈\s*(\S+)',
     r'$\\cos(\\theta) = \\frac{\\1}{\\2} \\approx \\3$'),

    # Cosine = dot(A,B)/(|A|×|B|)
    (r'Cosine\s*=\s*dot\(A,B\)/\(\|A\|×\|B\|\)',
     r'$\\text{Cosine} = \\frac{A \\cdot B}{\\|A\\| \\times \\|B\\|}$'),

    # cos(D1, D2) = (D1 · D2) / (‖D1‖ × ‖D2‖)
    (r'cos\(D1,\s*D2\)\s*=\s*\(D1\s*·\s*D2\)\s*/\s*\(‖D1‖\s*×\s*‖D2‖\)',
     r'$\\cos(D_1, D_2) = \\frac{D_1 \\cdot D_2}{\\|D_1\\| \\times \\|D_2\\|}$'),

    # P(w|context) patterns
    (r"P\('([^']+)'\s*\|\s*'([^']+)'\)",   r"$P(\\text{'\\1'} \\mid \\text{'\\2'})$"),
    (r"P\('([^']+)'\|'([^']+)'\)",          r"$P(\\text{'\\1'} \\mid \\text{'\\2'})$"),

    # P(w₃|w₁w₂) = Count(w₁w₂w₃) / Count(w₁w₂)
    (r'P\(w₃\|w₁w₂\)\s*=\s*Count\(w₁w₂w₃\)\s*/\s*Count\(w₁w₂\)',
     r'$P(w_3 \\mid w_1 w_2) = \\frac{\\text{Count}(w_1 w_2 w_3)}{\\text{Count}(w_1 w_2)}$'),

    # σ_max notations
    (r'σ_max\s*<\s*1',  r'$\\sigma_{\\max} < 1$'),
    (r'σ_max\s*>\s*1',  r'$\\sigma_{\\max} > 1$'),
    (r'\(σ_max\)\^\(T-1\)\s*=\s*([0-9.]+)\^([0-9]+)\s*≈\s*([0-9.E×⁻⁺\-]+)',
     r'$(\\sigma_{\\max})^{T-1} = \\1^{\\2} \\approx \\3$'),

    # 0.9^99 ≈ 2.66×10⁻⁵
    (r'0\.9\^99\s*≈\s*2\.66×10⁻⁵',  r'$0.9^{99} \\approx 2.66 \\times 10^{-5}$'),
    (r'0\.9\^99\s*≈\s*0\.0000266',   r'$0.9^{99} \\approx 0.0000266$'),

    # gradient ∝ (σ_max)^(T-1)
    (r'gradient\s*∝\s*\(σ_max\)\^\(T-1\)',
     r'gradient $\\propto (\\sigma_{\\max})^{T-1}$'),

    # QK^T / √d_k
    (r'QK\^T\s*/\s*√d_k',     r'$QK^T / \\sqrt{d_k}$'),
    (r'QK<sup>T</sup>\s*/\s*√d_k',  r'$QK^T / \\sqrt{d_k}$'),
    (r'Q·K<sup>T</sup>',       r'$Q \\cdot K^T$'),

    # √d_k standalone (but not inside other patterns)
    (r'(?<!\$)√d_k(?!\$)',     r'$\\sqrt{d_k}$'),
    (r'(?<!\$)√2(?!\$)',       r'$\\sqrt{2}$'),

    # softmax standalone formula mentions
    (r'softmax\(\[([0-9,.]+)\]\)\s*≈\s*\[([0-9,.]+)\]',
     lambda m: f'$\\text{{softmax}}([{m.group(1)}]) \\approx [{m.group(2)}]$'),

    # output = sublayer(x) + x
    (r'output\s*=\s*sublayer\(x\)\s*\+\s*x',
     r'$\\text{output} = \\text{sublayer}(x) + x$'),
    (r'output\s*=\s*x\s*\+\s*Sublayer\(x\)',
     r'$\\text{output} = x + \\text{Sublayer}(x)$'),

    # W_Q, W_K, W_V with subscript notation
    (r'W<sub>Q</sub>',   r'$W_Q$'),
    (r'W<sub>K</sub>',   r'$W_K$'),
    (r'W<sub>V</sub>',   r'$W_V$'),

    # L_MLM + L_NSP
    (r'L<sub>MLM</sub>',  r'$L_{\\text{MLM}}$'),
    (r'L<sub>NSP</sub>',  r'$L_{\\text{NSP}}$'),

    # d² → 2dr
    (r'd²\s*→\s*2dr',  r'$d^2 \\to 2dr$'),
    (r'd²参数→2dr参数', r'$d^2$ 参数 $\\to 2dr$ 参数'),
    # standalone d² (be careful)
    (r'(?<![a-zA-Z0-9])d²(?![a-zA-Z0-9])',  r'$d^2$'),

    # ΔW = A(d×r) × B(r×d)
    (r'ΔW\s*=\s*A\(d×r\)\s*×\s*B\(r×d\)',
     r'$\\Delta W = A_{d \\times r} \\times B_{r \\times d}$'),

    # A(d×r) and B(r×d) standalone
    (r'A\(d×r\)',  r'$A_{d \\times r}$'),
    (r'B\(r×d\)',  r'$B_{r \\times d}$'),

    # r ≪ d
    (r'r\s*≪\s*d',  r'$r \\ll d$'),

    # FP32=×4, FP16=×2, INT8=×1, INT4=×0.5
    (r'FP32=×4,\s*FP16=×2,\s*INT8=×1,\s*INT4=×0\.5',
     r'FP32 $= \\times 4$, FP16 $= \\times 2$, INT8 $= \\times 1$, INT4 $= \\times 0.5$'),

    # N × bytes = GB form:  7B × 4 bytes = 28 GB
    (r'(\d+)B\s*×\s*(\d+)\s*bytes?\s*=\s*<strong>(\S+\s*GB)</strong>',
     r'$\\1\\text{B} \\times \\2\\text{ bytes} = \\textbf{\\3}$'),

    # Precision/Recall/F1 formulas
    (r'F1\s*=\s*2\s*×\s*P\s*×\s*R\s*/\s*\(P\s*\+\s*R\)',
     r'$F_1 = \\frac{2 \\cdot P \\cdot R}{P + R}$'),

    # freq ∝ 1/rank^α
    (r'freq\s*∝\s*1/rank\^α',  r'$\\text{freq} \\propto 1/\\text{rank}^\\alpha$'),

    # R² > 0.95
    (r'R²\s*>\s*0\.95',  r'$R^2 > 0.95$'),

    # O(n²) standalone
    (r"O\(n²\)",  r"$O(n^2)$"),
    (r"O\(n\)",   r"$O(n)$"),

    # MRR = 1/rank
    (r'MRR\s*=\s*1/rank',  r'$\\text{MRR} = 1/\\text{rank}$'),
    (r'MRR\s*=\s*1/rank_of_first_relevant',
     r'$\\text{MRR} = 1/\\text{rank of first relevant}$'),

    # Precision@k = val
    (r'Precision@(\d+)\s*=\s*(\d+)/(\d+)',
     r'$\\text{Precision@\\1} = \\frac{\\2}{\\3}$'),
    (r'Recall@(\d+)\s*=\s*(\d+)/(\d+)',
     r'$\\text{Recall@\\1} = \\frac{\\2}{\\3}$'),

]


def apply_rules(text):
    """Apply all LaTeX conversion rules to a string."""
    for pattern, replacement in LATEX_RULES:
        if callable(replacement):
            text = re.sub(pattern, replacement, text)
        else:
            text = re.sub(pattern, replacement, text)
    return text


def process_json_file(filepath):
    """Process a single JSON quiz file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changed = False
    for item in data:
        for field in ['question', 'explanation', 'answer']:
            if field in item and isinstance(item[field], str):
                original = item[field]
                converted = apply_rules(original)
                if converted != original:
                    item[field] = converted
                    changed = True
        # Handle options
        if 'options' in item:
            new_opts = []
            for opt in item['options']:
                converted = apply_rules(opt)
                if converted != opt:
                    changed = True
                new_opts.append(converted)
            item['options'] = new_opts

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ Updated: {os.path.basename(filepath)}")
    else:
        print(f"  ⏭️  No changes: {os.path.basename(filepath)}")

    return changed


def main():
    quiz_dir = os.path.dirname(os.path.abspath(__file__))
    json_files = sorted(glob.glob(os.path.join(quiz_dir, '*.json')))

    print(f"Found {len(json_files)} JSON files.\n")

    updated_count = 0
    for f in json_files:
        if process_json_file(f):
            updated_count += 1

    print(f"\n{'='*40}")
    print(f"Done! Updated {updated_count}/{len(json_files)} files.")


if __name__ == '__main__':
    main()
