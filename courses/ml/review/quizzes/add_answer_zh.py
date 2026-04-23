"""Add answer_zh to all Short-type questions."""
import json, os

# answer_zh translations keyed by (filename, question_index)
ANSWER_ZH = {
    # midterm Q30: CNN Dimension
    ("midterm_quiz.json", 30):
        "(a) 32 × 32 × 6 — 'Same' 填充保持空间维度不变，6个滤波器 → 深度 = 6。\n"
        "(b) 16 × 16 × 6 — 输出 = 输入/步长 = 32/2 = 16。池化不改变深度。\n"
        "(c) 153,700 — 展平 = 16×16×6 = 1,536。权重 = 1,536×100 = 153,600。+ 100个偏置 = 153,700。",

    # midterm Q31: RNN Architecture
    ("midterm_quiz.json", 31):
        "(a) 任务A：多对多（60个序列 → 5个序列）。任务B：多对一（词序列 → 单个标签）。\n"
        "(b) 任务A：MSE（回归任务）。任务B：二元交叉熵（二分类）。",

    # midterm Q32: Bayesian Network
    ("midterm_quiz.json", 32):
        "(a) DAG：F → E，F → C，E → M，C → M（F在顶部、M在底部的菱形结构）。\n"
        "(b) P(F, E, C, M) = P(F) · P(E|F) · P(C|F) · P(M|E, C)",

    # midterm Q33: Hierarchical Clustering
    ("midterm_quiz.json", 33):
        "(a) |1-2|=1, |1-5|=4, |1-9|=8, |2-5|=3, |2-9|=7, |5-9|=4。\n"
        "(b) 点1和点2首先合并（距离为1，最小）。\n"
        "(c) MAX链接：dist({1,2},5) = max(4,3) = 4；dist({1,2},9) = max(8,7) = 8。下一步：{1,2}↔5 或 5↔9（都是4）。",

    # week09 Q11: Confusion Matrix
    ("week09_quiz.json", 11):
        "(a) Precision = 40/60 = 0.667，Recall = 40/50 = 0.8，F1 = 2×0.667×0.8/(0.667+0.8) ≈ 0.727\n"
        "(b) Accuracy = 970/1000 = 97%。不可靠——数据不平衡（YES=50, NO=950）。即使预测全部为NO也有95%准确率。\n"
        "(c) FPR = 20/950 ≈ 0.021（2.1%）。含义：2.1%的健康人被误诊。",

    # week09 Q13: Outlier Detection
    ("week09_quiz.json", 13):
        "(a) 统计方法（概率分布）、基于邻近度的方法（k-NN距离）、基于密度的方法（LOF相对密度）。\n"
        "(b) f(x) ≥ 0 → 正常（边界内）。f(x) < 0 → 异常值。ν = 异常值比例的上限（ν=0.05 → 约5%异常值）。\n"
        "(c) 将数据压缩到低维 → 重建回来 → 高重建误差 = 异常值。方法：PCA、自编码器。",

    # week10 Q18: Bagging vs Boosting
    ("week10_quiz.json", 18):
        "(a) Bagging：Bootstrap（有放回），并行，简单多数投票（等权）。Boosting：权重采样，顺序，加权投票。\n"
        "(b) α = ½ × ln(0.7/0.3) = ½ × ln(2.333) ≈ ½ × 0.847 ≈ 0.424。\n"
        "(c) +1得2票，-1得1票 → 集成预测 = +1。",

    # week10 Q19: AdaBoost Weight Update
    ("week10_quiz.json", 19):
        "(a) α₁ = ½ × ln(0.7/0.3) ≈ 0.424。\n"
        "(b) 正确分类（1-7）：w × e^(−α) ≈ w × 0.655（降至约65.5%）。误分类（8-10）：w × e^(+α) ≈ w × 1.528（升至约152.8%）。权重归一化使总和=1。\n"
        "(c) 样本8被选中的可能性更大——其权重增加，在\"轮盘赌\"上的份额更大。",

    # week10 Q20: Ensemble Explainability
    ("week10_quiz.json", 20):
        "不正确。解释多数投票 ≠ 可解释性。用户想知道每个分类器为什么做出其决定，而不仅仅是10个投了票。"
        "即使在数百个特征和数百万数据点的情况下，单个分类器也难以解释，更不用说10个。集成方法不可解释——这是其主要局限性。",

    # week11 Q15: Association Rule Mining
    ("week11_quiz.json", 15):
        "(a) F1：{A}=4, {B}=4, {C}=4, {D}=2（全部≥2）。F2：{A,B}=3, {A,C}=3, {B,C}=3, {B,D}=2, {C,D}=2（全部≥2）。{A,D}=1 ❌。\n"
        "(b) 被剪枝：{A,B,D}和{A,C,D}（包含非频繁的{A,D}）。剩余：{A,B,C}=2✅，{B,C,D}=2✅。\n"
        "(c) Support({A}→{B,C}) = σ({A,B,C})/|T| = 2/5 = 0.4。Confidence = σ({A,B,C})/σ({A}) = 2/4 = 0.5。",

    # week11 Q16: Applications
    ("week11_quiz.json", 16):
        "应用：(1) 保险欺诈检测——发现欺诈索赔中的重复组合。(2) 推荐系统——\"买了X的顾客也买了Y\"。\n"
        "摆放策略：策略1（近距离）——将相关商品放在一起方便购买。策略2（远距离）——将它们分开放置，让顾客浏览途中购买更多商品。\n"
        "需要更新的原因：消费模式随季节变化（如感恩节火鸡）。上个月的规则下个月可能不适用。",
}

def main():
    quiz_dir = os.path.dirname(os.path.abspath(__file__))
    total = 0
    for (fname, qidx), zh in ANSWER_ZH.items():
        filepath = os.path.join(quiz_dir, fname)
        with open(filepath, 'r', encoding='utf-8') as f:
            qs = json.load(f)
        qs[qidx]['answer_zh'] = zh
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(qs, f, ensure_ascii=False, indent=2)
        total += 1
        print(f"  [OK] {fname} Q{qidx}")
    print(f"\nDone! {total} answer_zh added.")

if __name__ == '__main__':
    main()
