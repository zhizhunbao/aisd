#!/usr/bin/env python3
"""Convert MV_Final_Practice_Exam.txt to final_review_quiz.json"""
import json, re, os

src = os.path.join(os.path.dirname(__file__), '..', '..', 'quizzes', 'MV_Final_Practice_Exam.txt')
with open(src, 'r', encoding='utf-8') as f:
    text = f.read()

quizzes = []

# ===== PART A: MCQ (Q1-Q30) =====
mcq_pattern = re.compile(
    r'(\d+)\.\s+(.*?)\n\s*a\.\s+(.*?)\n\s*b\.\s+(.*?)\n\s*c\.\s+(.*?)\n\s*d\.\s+(.*?)\n\s*Answer:\s*([abcd])\)?\s*(.*?)\n(.*?)(?=\n\d+\.|PART|\Z)',
    re.DOTALL
)

for m in mcq_pattern.finditer(text):
    qnum = int(m.group(1))
    if qnum > 56: break  # skip calculation questions
    question = m.group(2).strip()
    opts = [f"A) {m.group(3).strip()}", f"B) {m.group(4).strip()}", f"C) {m.group(5).strip()}", f"D) {m.group(6).strip()}"]
    ans_letter = m.group(7).strip().lower()
    ans_idx = {'a':0,'b':1,'c':2,'d':3}[ans_letter]
    explanation = (m.group(8).strip() + ' ' + m.group(9).strip()).strip()
    # Clean explanation
    explanation = re.sub(r'\n+', ' ', explanation).strip()
    explanation = re.sub(r'\s+', ' ', explanation)
    
    source = "teacher"
    if '🎤 Professor' in explanation or '⭐ Professor' in explanation:
        source = "teacher"
    
    q = {
        "question": question,
        "type": "MCQ",
        "options": opts,
        "answer": ans_idx,
        "explanation": explanation,
        "source": source
    }
    quizzes.append(q)

# ===== PART B: Fill/Short (Q31-Q45) =====
fill_pattern = re.compile(
    r'(\d+)\.\s+(.*?)\n\s*Answer:\s*(.*?)\n(.*?)(?=\n\d+\.|PART|\Z)',
    re.DOTALL
)

for m in fill_pattern.finditer(text):
    qnum = int(m.group(1))
    if qnum < 31 or qnum > 45: continue
    question = m.group(2).strip()
    answer = m.group(3).strip()
    explanation = m.group(4).strip()
    explanation = re.sub(r'\n+', ' ', explanation).strip()
    explanation = re.sub(r'\s+', ' ', explanation)
    
    # Determine if fill or short
    if '________' in question or 'Name ' in question:
        qtype = "Fill"
        ans_obj = [answer]
    else:
        qtype = "Short"
        ans_obj = answer
    
    q = {
        "question": question,
        "type": qtype,
        "answer": ans_obj,
        "explanation": explanation,
        "source": "teacher"
    }
    if qtype == "Short":
        q["points"] = 1
    quizzes.append(q)

# ===== PART C: Calculation (Q57-Q61) =====
calc_questions = [
    {
        "question": "Given input 64×64, 32 filters of size 3×3, stride=2, padding=1. Find output dimensions.\n给定输入64×64，32个3×3滤波器，步长=2，填充=1。求输出维度。",
        "type": "Short",
        "answer": "Output = (64−3+2×1)/2+1 = 63/2+1 = 32. Answer: 32×32×32",
        "explanation": "Formula: Output = (Input − Filter + 2×Padding) / Stride + 1 = (64−3+2)/2+1 = 32. Depth = 32 filters.",
        "source": "teacher", "points": 2
    },
    {
        "question": "Given input 28×28, 64 filters of size 5×5, stride=1, padding=0. Find output dimensions.\n给定输入28×28，64个5×5滤波器，步长=1，填充=0。求输出维度。",
        "type": "Short",
        "answer": "Output = (28−5+0)/1+1 = 24. Answer: 24×24×64",
        "explanation": "Formula: (28−5+0)/1+1 = 24. Depth = 64 filters.",
        "source": "teacher", "points": 2
    },
    {
        "question": "After a 24×24×64 feature map, apply Max Pooling with 2×2 kernel, stride=2. Find output.\n在24×24×64特征图上应用2×2最大池化，步长=2。求输出。",
        "type": "Short",
        "answer": "Pooling Output = 24/2 = 12. Answer: 12×12×64 (depth unchanged)",
        "explanation": "Max Pooling reduces spatial dimensions: 24/2 = 12. Depth stays the same = 64.",
        "source": "teacher", "points": 1
    },
    {
        "question": "Convolution: Matrix A (4×4) with Kernel K (2×2), stride=1, no padding.\nA=[[2,0,1,3],[1,5,8,2],[4,3,6,7],[0,9,2,4]], K=[[1,0],[0,-1]]. Compute result.\n卷积：4×4矩阵A与2×2卷积核K，步长=1，无填充。计算结果。",
        "type": "Short",
        "answer": "Output 3×3: [[-3,-8,-1],[-2,-1,1],[-5,1,2]]",
        "explanation": "Output size=(4−2)/1+1=3×3. (0,0):2×1+0×0+1×0+5×(-1)=-3. (0,1):0×1+1×0+5×0+8×(-1)=-8. ... Full matrix: [[-3,-8,-1],[-2,-1,1],[-5,1,2]].",
        "source": "teacher", "points": 3
    },
    {
        "question": "Calculate IoU: Predicted box (x1=2,y1=1,x2=6,y2=5), Ground truth (x1=3,y1=2,x2=7,y2=6).\n计算IoU：预测框(2,1,6,5)，真实框(3,2,7,6)。",
        "type": "Short",
        "answer": "Pred Area=16, GT Area=16, Overlap=(6-3)×(5-2)=9, Union=16+16-9=23. IoU=9/23≈0.391. Not acceptable (<0.5).",
        "explanation": "Overlap: x_left=max(2,3)=3, x_right=min(6,7)=6, y_top=max(1,2)=2, y_bottom=min(5,6)=5. Overlap=3×3=9. Union=23. IoU≈0.391 < 0.5 threshold.",
        "source": "teacher", "points": 2
    }
]
quizzes.extend(calc_questions)

# Write output
out_path = os.path.join(os.path.dirname(__file__), 'final_review_quiz.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(quizzes, f, ensure_ascii=False, indent=2)

print(f"Generated {len(quizzes)} questions -> {out_path}")
