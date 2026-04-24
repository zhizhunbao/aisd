"""Generate MV Review Hub index.html based on PJ template - excluding Week 11"""
import re

# Read PJ template
with open(r'c:\Users\40270\Desktop\workspace\aisd\courses\pj\review\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Title changes
html = html.replace('GenAI Review Hub — Quizzes + Storylines', 'CST8508 Machine Vision — Review Hub')
html = html.replace('GenAI Evaluation — Review Hub', 'CST8508 Machine Vision — Review Hub')
html = html.replace('刷题 + 故事线阅读 · W1-W12 · 手机随时复习', '刷题 + 故事线 + Slides · W1-W10 · 手机随时复习')

# 2. Hero map
old_hero = """const heroMap = {
    quiz:       ['GenAI Evaluation — All Quizzes (' + totalQ + ' Questions)', '全部测验合集 · W1-W12 + Final Prediction · 手机随时刷题'],
    story:      ['GenAI Evaluation — Storylines 📖', '故事线阅读 · 因果链路 · 手机随时看'],
    slides:     ['GenAI Evaluation — Slides 📊', '课件笔记 · 原始 Slide 结构化阅读'],
    cheatsheet: ['GenAI Evaluation — Cheat Sheets 📄', '速查表 · 定义/对比/公式/陷阱 · 考前速览'],
  };"""
new_hero = """const heroMap = {
    quiz:       ['CST8508 Machine Vision — All Quizzes (' + totalQ + ' Questions)', '全部测验合集 · W1-W10 · 手机随时刷题'],
    story:      ['CST8508 Machine Vision — Storylines 📖', '故事线阅读 · 因果链路 · 手机随时看'],
    slides:     ['CST8508 Machine Vision — Slides 📊', '课件笔记 · 原始 Slide 结构化阅读'],
    cheatsheet: ['CST8508 Machine Vision — Cheat Sheets 📄', '速查表 · 定义/对比/公式/陷阱 · 考前速览'],
  };"""
html = html.replace(old_hero, new_hero)

# 3. Replace STORYLINES
old_storylines = """const STORYLINES = [
  { id: 'w1', label: 'W1 评估基础', file: '../notes/Week1_storyline.md' },
  { id: 'w2', label: 'W2 框架工具', file: '../notes/Week2_storyline.md' },
  { id: 'w3', label: 'W3 特征工程', file: '../notes/Week3_storyline.md' },
  { id: 'w4', label: 'W4 算法/分布式', file: '../notes/Week4_storyline.md' },
  { id: 'w6', label: 'W6 部署压缩', file: '../notes/Week6_storyline.md' },
  { id: 'w7', label: 'W7 MLOps', file: '../notes/Week7_storyline.md' },
  { id: 'w9', label: 'W9 基础设施', file: '../notes/Week9_storyline.md' },
  { id: 'w11', label: 'W11 RAG/Prompt', file: '../notes/Week11_storyline.md' },
  { id: 'w12', label: 'W12 微调/LoRA', file: '../notes/Week12_storyline.md' },
];"""
new_storylines = """const STORYLINES = [
  { id: 'w1',  label: 'W1 MV 概述',        file: '../notes/week1_intro_storyline.md' },
  { id: 'w2',  label: 'W2 图像处理',       file: '../notes/week2_image_processing_storyline.md' },
  { id: 'w3',  label: 'W3 特征检测',       file: '../notes/week3_feature_detection_storyline.md' },
  { id: 'w4',  label: 'W4 CNN 入门',       file: '../notes/week4_cnn_intro_storyline.md' },
  { id: 'w5',  label: 'W5 深度学习',       file: '../notes/week5_deep_learning_storyline.md' },
  { id: 'w7',  label: 'W7 PyTorch',        file: '../notes/week7_pytorch_storyline.md' },
  { id: 'w8',  label: 'W8 目标检测',       file: '../notes/week8_object_detection_storyline.md' },
  { id: 'w9',  label: 'W9 目标跟踪',       file: '../notes/Week9 - Object Tracking_storyline.md' },
  { id: 'w10', label: 'W10 传感器融合',    file: '../notes/week10_sensor_fusion_storyline.md' },
  { id: 'mid', label: '期中复习',          file: '../notes/midterm_test_storyline.md' },
];"""
html = html.replace(old_storylines, new_storylines)

# 4. Replace SLIDES
old_slides = """const SLIDES = [
  { id: 'w1',  label: 'W1 评估基础', file: '../notes/Week1_slides.md' },
  { id: 'w2',  label: 'W2 框架工具', file: '../notes/Week2_slides.md' },
  { id: 'w3',  label: 'W3 特征工程', file: '../notes/Week3_slides.md' },
  { id: 'w4',  label: 'W4 算法/分布式', file: '../notes/Week4_slides.md' },
  { id: 'w6',  label: 'W6 部署压缩', file: '../notes/Week6_slides.md' },
  { id: 'w7',  label: 'W7 MLOps', file: '../notes/Week7_slides.md' },
  { id: 'w9',  label: 'W9 基础设施', file: '../notes/Week9_slides.md' },
  { id: 'w11', label: 'W11 RAG/Prompt', file: '../notes/Week11_slides.md' },
  { id: 'w12', label: 'W12 微调/LoRA', file: '../notes/Week12_slides.md' },
];"""
new_slides = """const SLIDES = [
  { id: 'w1',  label: 'W1 MV 概述',        file: '../notes/week1_intro_slides.md' },
  { id: 'w2',  label: 'W2 图像处理',       file: '../notes/week2_image_processing_slides.md' },
  { id: 'w3',  label: 'W3 特征检测',       file: '../notes/week3_feature_detection_slides.md' },
  { id: 'w4',  label: 'W4 CNN 入门',       file: '../notes/week4_cnn_intro_slides.md' },
  { id: 'w5',  label: 'W5 深度学习',       file: '../notes/week5_deep_learning_slides.md' },
  { id: 'w7',  label: 'W7 PyTorch',        file: '../notes/week7_pytorch_slides.md' },
  { id: 'w8',  label: 'W8 目标检测',       file: '../notes/week8_object_detection_slides.md' },
  { id: 'w9',  label: 'W9 目标跟踪',       file: '../notes/Week9 - Object Tracking_slides.md' },
  { id: 'w10', label: 'W10 传感器融合',    file: '../notes/week10_sensor_fusion_slides.md' },
  { id: 'mid', label: '期中复习',          file: '../notes/midterm_test_slides.md' },
];"""
html = html.replace(old_slides, new_slides)

# 5. Replace CHEATSHEETS - MV has no cheat sheets yet, leave empty but functional
old_cs = """const CHEATSHEETS = [
  { id: 'w1',   label: 'W1 评估基础', file: 'cheat_sheet_w1.md' },
  { id: 'w2',   label: 'W2 框架工具', file: 'cheat_sheet_w2.md' },
  { id: 'w3',   label: 'W3 特征工程', file: 'cheat_sheet_w3.md' },
  { id: 'w4',   label: 'W4 算法/分布式', file: 'cheat_sheet_w4.md' },
  { id: 'w6',   label: 'W6 部署压缩', file: 'cheat_sheet_w6.md' },
  { id: 'w7w9', label: 'W7/W9 MLOps', file: 'cheat_sheet_w7w9.md' },
  { id: 'w11',  label: 'W11 RAG/Prompt', file: 'cheat_sheet_w11.md' },
  { id: 'w12',  label: 'W12 微调/LoRA', file: 'cheat_sheet_w12.md' },
];"""
new_cs = """const CHEATSHEETS = [
  // MV course cheat sheets - add as they are created
];"""
html = html.replace(old_cs, new_cs)

# 6. Replace QUIZ_FILES
old_quiz = """const QUIZ_FILES = [
  { id: 'w1',    title: 'Week 1 — GenAI Evaluation Fundamentals',       subtitle: 'LLM-as-Judge, BLEU, METEOR, BERTScore, Bias Types',                     file: 'quizzes/week01_quiz.json' },
  { id: 'w2',    title: 'Week 2 — Evaluation Frameworks & Observability', subtitle: 'RAGAS, DeepEval, OpenTelemetry, Faithfulness, G-Eval',                  file: 'quizzes/week02_quiz.json' },
  { id: 'w3',    title: 'Week 3 — Feature Engineering & Data Quality',    subtitle: 'Missing Data, One-Hot, SHAP, Data Leakage, Imbalanced Data',           file: 'quizzes/week03_quiz.json' },
  { id: 'w4',    title: 'Week 4 — Algorithm Selection & Distributed',     subtitle: 'Parallelism, NAS, HPO, Gradient Boosting, DDP/FSDP',                    file: 'quizzes/week04_quiz.json' },
  { id: 'w6',    title: 'Week 6 — Deployment & Model Compression',        subtitle: 'Quantization, Pruning, Knowledge Distillation, Scaling',                file: 'quizzes/week06_quiz.json' },
  { id: 'w7',    title: 'Week 7 — MLOps & Infrastructure',                subtitle: 'Docker, Kubernetes, Airflow, Feature Store, DAG',                       file: 'quizzes/week07_quiz.json' },
  { id: 'w11',   title: 'Week 11 — Advanced RAG & Prompt Optimization',   subtitle: 'Chunking, Hybrid Retrieval, OPRO, Self-Consistency, Reflexion',         file: 'quizzes/week11_quiz.json' },
  { id: 'w12',   title: 'Week 12 — Fine-Tuning & LoRA',                   subtitle: 'LoRA, Full Fine-Tuning, Catastrophic Forgetting, LlamaFactory',         file: 'quizzes/week12_quiz.json' },
  { id: 'final', title: 'Final Exam — Predicted Short Answer',            subtitle: 'Comprehensive short-answer questions covering all weeks',               file: 'quizzes/final_short_answer.json' },
];"""
new_quiz = """const QUIZ_FILES = [
  { id: 'w1',   title: 'Week 1 — Introduction to Machine Vision',   subtitle: 'MV vs CV, Pixels, RGB/HSV, CCD/CMOS, Image Formats',         file: 'quizzes/week01_quiz.json' },
  { id: 'w2',   title: 'Week 2 — Image Processing Fundamentals',    subtitle: 'Filtering, Canny Edge, Morphology, Thresholding, Histogram',  file: 'quizzes/week02_quiz.json' },
  { id: 'lab5', title: 'Lab 5 — CNN Cats vs Dogs',                  subtitle: 'PyTorch CNN, DataLoader, Dropout, CrossEntropy, Transforms',  file: 'quizzes/lab5_quiz.json' },
  { id: 'a1',   title: 'Assignment 1 — mmpretrain',                 subtitle: 'OpenMMLab, ResNet, MobileNet V2, Config-Driven Training',     file: 'quizzes/assignment1_quiz.json' },
];"""
html = html.replace(old_quiz, new_quiz)

# Write output
with open(r'c:\Users\40270\Desktop\workspace\aisd\courses\mv\review\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[OK] MV Review Hub generated successfully!")
print(f"   Output: courses/mv/review/index.html ({len(html)} bytes)")
