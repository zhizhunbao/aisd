"""
Convert plain-text math expressions in quiz JSON to LaTeX $...$ notation for KaTeX rendering.

Targets:
  - question, question_zh, answer, answer_zh
  - explanation, explanation_zh
  - options[], options_zh[]

Patterns converted:
  1.  P(X|Y), P(X,Y|Z), P(xᵢ|C) → $P(X|Y)$ etc.
  2.  K(xᵢ, xⱼ) = φ(xᵢ)·φ(xⱼ) → LaTeX
  3.  Dimension expressions: 32×32×6, 224×224×3
  4.  Fraction-like: 3.2 / 4.8 = 0.667
  5.  w·x + b = 0
  6.  ∂hₜ/∂hₜ₋₁
  7.  O(n·K·I·d)
  8.  Subscript/superscript Unicode → LaTeX: xᵢ → x_i, hₜ → h_t etc.
"""

import json
import re
import glob
import os

def convert_math(text):
    """Convert plain-text math expressions to LaTeX $...$ notation."""
    if not text:
        return text
    
    # Skip if already has $ delimiters
    # (we still process to catch remaining patterns)
    
    # ===== Pattern 1: Probability expressions =====
    # P(X|Y), P(X,Y|Z), P(xᵢ|C), P(F), P(E|F) etc.
    # Match P(...) patterns that aren't already in $...$
    def latex_prob(m):
        full = m.group(0)
        # Convert Unicode subscripts inside
        full = full.replace('ᵢ', '_i').replace('ⱼ', '_j').replace('ₜ', '_t').replace('₋', '-')
        return f'${full}$'
    
    # P(...) with various contents - but NOT inside existing $ or HTML tags
    text = re.sub(r'(?<!\$)P\([^)]{1,30}\)(?!\$)', latex_prob, text)
    
    # ===== Pattern 2: Kernel function K(xᵢ, xⱼ) = φ(xᵢ)·φ(xⱼ) =====
    text = re.sub(
        r'K\(xᵢ,\s*xⱼ\)\s*=\s*φ\(xᵢ\)·φ\(xⱼ\)',
        r'$K(x_i, x_j) = \\varphi(x_i) \\cdot \\varphi(x_j)$',
        text
    )
    # φ(x) standalone
    text = re.sub(r'(?<!\$)φ\(x\)(?!\$)', r'$\\varphi(x)$', text)
    
    # ===== Pattern 3: Dimension expressions like 32×32×6, 16×16×6 =====
    # Convert dimensions in context: "32 × 32 × 6" or "32×32×6"
    def latex_dims(m):
        return f'${m.group(0).replace("×", " \\times ")}$'
    
    # Match NxNxN patterns (2 or 3 dimensions), with optional spaces around ×
    text = re.sub(r'(?<!\$)\d+\s*×\s*\d+(?:\s*×\s*\d+)?(?!\$)', latex_dims, text)
    
    # ===== Pattern 4: w·x + b = 0 type expressions =====
    text = re.sub(
        r'(?<!\$)w·x\s*\+\s*b\s*=\s*0(?!\$)',
        r'$\\mathbf{w} \\cdot \\mathbf{x} + b = 0$',
        text
    )
    text = re.sub(
        r'𝐰·𝐱\s*\+\s*b',
        r'$\\mathbf{w} \\cdot \\mathbf{x} + b$',
        text
    )
    
    # ===== Pattern 5: ∂hₜ/∂hₜ₋₁ =====
    text = re.sub(
        r'∂hₜ/∂hₜ₋₁',
        r'$\\frac{\\partial h_t}{\\partial h_{t-1}}$',
        text
    )
    
    # ===== Pattern 6: O(n·K·I·d) complexity =====
    text = re.sub(
        r'O\(n·K·I·d\)',
        r'$O(n \\cdot K \\cdot I \\cdot d)$',
        text
    )
    
    # ===== Pattern 7: Wₓ, Wᵧ, Wₕ weight matrices =====
    text = re.sub(r'(?<!\$)Wₓ(?!\$)', r'$W_x$', text)
    text = re.sub(r'(?<!\$)Wᵧ(?!\$)', r'$W_y$', text)
    text = re.sub(r'(?<!\$)Wₕ(?!\$)', r'$W_h$', text)
    
    # ===== Pattern 8: hₜ, xₜ etc. =====
    text = re.sub(r'(?<!\$)hₜ₋₁(?!\$)', r'$h_{t-1}$', text)
    text = re.sub(r'(?<!\$)hₜ(?!\$)', r'$h_t$', text)
    text = re.sub(r'(?<!\$)xₜ(?!\$)', r'$x_t$', text)
    
    # ===== Pattern 9: xᵢ standalone =====
    text = re.sub(r'(?<!\$)xᵢ(?!\$)', r'$x_i$', text)
    
    # ===== Pattern 10: Mathematical operations with · =====
    # count(xᵢ,C) + 1 / (count(C) + |V|)  - Laplace formula
    text = re.sub(
        r'P\(xᵢ\|C\)\s*=\s*\(count\(xᵢ,C\)\s*\+\s*1\)\s*/\s*\(count\(C\)\s*\+\s*\|V\|\)',
        r'$P(x_i|C) = \\frac{\\text{count}(x_i, C) + 1}{\\text{count}(C) + |V|}$',
        text
    )
    # Simpler Laplace: P(xᵢ|C) = (count(xᵢ,C) + 1) / (count(C) + |V|)
    
    # ===== Pattern 11: C-1 in context =====
    text = re.sub(r'(?<!\$)C-1(?!\$)', r'$C-1$', text)
    
    # ===== Pattern 12: Fraction expressions like 3.2 / 4.8 = 0.667 ≈ 67% =====
    # These are better as inline math
    text = re.sub(
        r'(\d+\.?\d*)\s*/\s*(\d+\.?\d*)\s*=\s*(\d+\.?\d*)',
        lambda m: f'${m.group(1)} / {m.group(2)} = {m.group(3)}$',
        text
    )
    
    # ===== Pattern 13: ≥, ≤, < comparisons in math context =====
    # MinPts - keep as is since it's a named parameter
    
    # ===== Pattern 14: |1-2|=1 distance calculations =====
    text = re.sub(
        r'\|(\d+)-(\d+)\|=(\d+)',
        lambda m: f'$|{m.group(1)}-{m.group(2)}|={m.group(3)}$',
        text
    )
    
    # ===== Pattern 15: dist({...}, ...) =====
    text = re.sub(
        r'dist\(\{([^}]+)\},\s*(\d+)\)\s*=\s*max\(([^)]+)\)\s*=\s*(\d+)',
        lambda m: f'$\\text{{dist}}(\\{{{m.group(1)}\\}}, {m.group(2)}) = \\max({m.group(3)}) = {m.group(4)}$',
        text
    )
    
    # ===== Clean up: fix nested $$ from double-matching =====
    # Collapse adjacent $$ into single $ (but preserve intentional display math)
    # Pattern: $content$$ or $$content$ → $content$
    while '$$' in text and not re.search(r'^\$\$', text, re.MULTILINE):
        text = text.replace('$$', '$')
    
    return text


def process_quiz_file(filepath):
    """Process a single quiz JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changed = False
    for q in data:
        fields = ['question', 'question_zh', 'answer', 'answer_zh', 
                  'explanation', 'explanation_zh']
        for field in fields:
            if field in q and isinstance(q[field], str):
                original = q[field]
                q[field] = convert_math(original)
                if q[field] != original:
                    changed = True
        
        # Process options arrays
        for opt_field in ['options', 'options_zh']:
            if opt_field in q and isinstance(q[opt_field], list):
                for i, opt in enumerate(q[opt_field]):
                    if isinstance(opt, str):
                        original = opt
                        q[opt_field][i] = convert_math(opt)
                        if q[opt_field][i] != original:
                            changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] Updated: {os.path.basename(filepath)}")
    else:
        print(f"[--] No changes: {os.path.basename(filepath)}")
    
    return changed


def main():
    quiz_dir = os.path.dirname(os.path.abspath(__file__))
    json_files = glob.glob(os.path.join(quiz_dir, '*_quiz.json'))
    
    print(f"Found {len(json_files)} quiz files\n")
    
    total_changed = 0
    for f in sorted(json_files):
        if process_quiz_file(f):
            total_changed += 1
    
    print(f"\n{'='*40}")
    print(f"Done! {total_changed}/{len(json_files)} files updated.")
    print("Refresh the browser to see LaTeX-rendered math formulas.")


if __name__ == '__main__':
    main()
