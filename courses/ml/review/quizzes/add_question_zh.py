import json

path = r"c:\Users\40270\Desktop\workspace\aisd\courses\ml\review\quizzes\prediction_quiz.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Map: English question (start) -> Chinese translation
zh_map = {
    # PART 1 TF Q1-Q10
    "In imbalanced class problems, accuracy is always a reliable metric": "在不平衡类别问题中，准确率始终是评估分类器性能的可靠指标。",
    "Oversampling the minority class works by randomly duplicating": "对少数类进行过采样是通过随机复制少数类实例来平衡数据集。",
    "SMOTE generates synthetic minority class instances by duplicating": "SMOTE通过复制现有少数类实例并添加少量随机噪声来生成合成少数类实例。",
    "A randomly guessing model has an Area Under the ROC Curve": "随机猜测模型的ROC曲线下面积（AUC）为0.5。",
    "In Bagging, each bootstrap sample is created by sampling": "在Bagging中，每个自助样本是通过从原始训练集中进行无放回抽样创建的。",
    "In AdaBoost, correctly classified instances have their weights increased": "在AdaBoost中，正确分类的实例在下一轮中权重增加，以便模型专注于简单样本。",
    "Random Forest combines Bagging with random feature selection": "随机森林将Bagging与每个分裂点的随机特征选择相结合，以创建多样化的决策树。",
    "The confidence of an association rule {X}": "关联规则{X}→{Y}的置信度计算为{X∪Y}的支持度除以总交易数。",
    "According to the Apriori principle, if an itemset is infrequent": "根据Apriori原则，如果一个项集是非频繁的，那么它的所有超集也一定是非频繁的。",
    "In association rule mining, rules generated from the same frequent itemset": "在关联规则挖掘中，从同一频繁项集生成的规则始终具有相同的支持度和相同的置信度。",

    # PART 2 MCQ Q11-Q30
    "In a confusion matrix, False Positive (FP) refers to": "在混淆矩阵中，假阳性（FP）指的是：",
    "The F1-measure is defined as": "F1值的定义为：",
    "In the ROC curve, the x-axis and y-axis represent": "在ROC曲线中，x轴和y轴分别表示：",
    "Which of the following correctly describes the SMOTE technique": "以下哪项正确描述了SMOTE技术？",
    "In the Local Outlier Factor (LOF) method": "在局部异常因子（LOF）方法中，如果点x的相对密度远大于1，这表明：",
    "One-Class SVM (OCSVM) is designed to": "一类SVM（OCSVM）被设计用于：",
    "What are the two necessary conditions for ensemble methods": "集成方法优于单个基分类器的两个必要条件是什么？",
    "In Bagging, when n is sufficiently large": "在Bagging中，当n足够大时，特定训练实例被包含在单个自助样本中的概率约为：",
    "Which of the following best describes the key difference between Bagging and Boosting": "以下哪项最好地描述了Bagging和Boosting之间的关键区别？",
    "In AdaBoost, the importance (alpha) of a base classifier": "在AdaBoost中，基分类器的重要度（alpha）计算为：",
    "What happens if an intermediate round of AdaBoost produces an error rate greater than 50%": "如果AdaBoost的中间轮次产生大于50%的错误率，会发生什么？",
    "What distinguishes Random Forest from standard Bagging": "随机森林与标准Bagging的区别是什么？",
    "Ensemble methods work best with what type of base classifiers": "集成方法与什么类型的基分类器效果最好？",
    "Given a transaction database of 5 transactions": "给定包含5个交易的交易数据库，如果项集{Beer, Diaper}出现在3个交易中，{Beer, Diaper}的支持度是多少？",
    "Given the rule {Milk, Diaper}": "给定规则{Milk, Diaper}→{Beer}，其中σ({Milk, Diaper, Beer})=2，σ({Milk, Diaper})=3，|T|=5，该规则的置信度为：",
    "The Apriori principle states that": "Apriori原则表明：",
    "In the Apriori algorithm, candidate pruning works by": "在Apriori算法中，候选剪枝的工作方式是：",
    "What is the anti-monotone property of support": "支持度的反单调属性是什么？",
    "If |L| = k (a frequent itemset of size k)": "如果|L|=k（大小为k的频繁项集），可以生成多少条候选关联规则（排除平凡规则）？",
    "Given Precision = 0.5 and Recall = 0.8": "给定Precision=0.5和Recall=0.8，F1值是多少？",

    # PART 3 Written Q31-Q34
    "Confusion Matrix Calculations": "混淆矩阵计算：\n(a) 计算Precision、Recall和F1值。\n(b) 计算Accuracy。在此是否可靠？解释原因。\n(c) 计算FPR并解释其含义。",
    "Association Rule Mining Calculations": "关联规则挖掘计算：\n(a) 找出所有频繁1-项集和2-项集（最小支持度计数=2）。\n(b) 使用Apriori原则，哪些3-项集候选可以被剪枝？找出频繁3-项集。\n(c) 计算规则{A}→{B,C}的支持度和置信度。",
    "Bagging vs Boosting Comparison": "Bagging与Boosting比较+计算：\n(a) 从采样方法、训练顺序、投票机制三方面比较Bagging和Boosting。\n(b) 在AdaBoost中，ε=0.3，计算α。\n(c) 三个分类器分别预测+1, -1, +1，多数投票的集成预测是什么？",
    "Outlier Detection Concepts": "异常检测概念+计算：\n(a) 列出并简要描述三种不同的异常检测方法。\n(b) 在OCSVM中，解释f(x)≥0与f(x)<0以及ν控制什么。\n(c) 用一个例子解释基于重建的异常检测。",

    # PART 4-1 Supplement TF Q35-Q49
    "Ensemble methods such as Bagging and Boosting have good explainability": "Bagging和Boosting等集成方法具有良好的可解释性，因为我们可以向最终用户解释多数投票过程。",
    "In Boosting (AdaBoost), all training samples are treated equally": "在Boosting（AdaBoost）中，所有训练样本在整个训练过程中被同等对待。",
    "In Bagging, every training instance is guaranteed": "在Bagging中，每个训练实例都保证被包含在每个自助样本中。",
    "In AdaBoost, if an intermediate round produces an error rate greater than 50%, the algorithm terminates": "在AdaBoost中，如果中间轮次产生大于50%的错误率，算法立即终止。",
    "In Random Forest, the base classifiers (decision trees) are pruned": "在随机森林中，基分类器（决策树）经过剪枝以降低模型复杂度。",
    "Association rules represent causal relationships": "关联规则表示项目之间的因果关系（例如，购买啤酒导致购买尿布）。",
    "In association rule mining, the purchase quantity": "在关联规则挖掘中，每个商品的购买数量和顾客身份是分析中的重要因素。",
    "The brute-force approach is feasible": "暴力法适用于在包含数千个商品的大型数据集中寻找频繁项集。",
    "In AdaBoost, the final prediction uses simple majority voting where all classifiers have equal": "在AdaBoost中，最终预测使用简单多数投票，所有分类器具有相同的影响力。",
    "In association rule mining, the two-step approach first generates rules": "在关联规则挖掘中，两步法首先生成规则，然后找到频繁项集。",
    "Ensemble methods are most effective when combined with stable classifiers": "集成方法与稳定分类器（如k近邻kNN）结合时最有效。",
    "Bagging primarily reduces the bias": "Bagging主要降低模型的偏差，而Boosting主要降低方差。",
    "In the Apriori algorithm, candidate k-itemsets are generated by merging": "在Apriori算法中，候选k-项集通过合并两个前(k-2)个项相同的频繁(k-1)-项集来生成。",
    "In a confusion matrix, high accuracy necessarily implies": "在混淆矩阵中，高准确率必然意味着模型对少数类具有高召回率。",
    "The Apriori algorithm uses the anti-monotone property": "Apriori算法利用支持度的反单调属性在计算候选项集的支持度之前进行剪枝。",

    # PART 4-2 Supplement Written Q50-Q53
    "A student argues": "一个学生争辩说：\"像Bagging这样的集成方法是可解释的，因为我们可以告诉用户10个不同的分类器投了票，我们取了多数。\"这个说法正确吗？解释原因。",
    "AdaBoost Weight Update Process": "AdaBoost权重更新过程：\n(a) 10个样本，初始权重1/10，ε₁=0.3，计算α₁。\n(b) 描述正确分类和错误分类样本的权重变化。\n(c) 在第2轮中，样本8（第1轮中被错误分类）被选中的可能性更大还是更小？为什么？",
    "Association Rule Mining Applications": "关联规则挖掘应用：\n(a) 除了市场篮分析，给出两个现实世界的应用。\n(b) 关联规则如何用于两种对立的商品摆放策略？\n(c) 为什么关联规则需要定期更新？",
}

# Also add options_zh for MCQ questions
options_zh_map = {
    "In a confusion matrix, False Positive (FP) refers to": [
        "模型正确预测了一个正类实例。",
        "模型错误地将一个负类实例预测为正类。",
        "模型错误地将一个正类实例预测为负类。",
        "模型正确预测了一个负类实例。"
    ],
    "The F1-measure is defined as": [
        "(Precision + Recall) / 2",
        "2 × Precision × Recall / (Precision + Recall)",
        "Precision × Recall",
        "(TP + TN) / (TP + FP + FN + TN)"
    ],
    "In the ROC curve, the x-axis and y-axis represent": [
        "x = 精确率, y = 召回率",
        "x = FPR（假阳性率）, y = TPR（真阳性率）",
        "x = 召回率, y = 精确率",
        "x = TPR, y = FPR"
    ],
    "Which of the following correctly describes the SMOTE technique": [
        "它通过移除多数类实例来平衡数据集。",
        "它随机复制少数类实例。",
        "它通过沿少数类最近邻之间的线段生成合成少数类实例。",
        "它使用PCA来降低少数类的维度。"
    ],
    "In the Local Outlier Factor (LOF) method": [
        "x是一个密度高的正常点。",
        "x被非常密集的邻居包围，因此是正常的。",
        "x是一个强异常值，因为其密度远低于邻居。",
        "x是一个密集簇的中心。"
    ],
    "One-Class SVM (OCSVM) is designed to": [
        "将数据精确分为两个平衡的类别。",
        "学习正常数据点周围的边界，并将边界外的点识别为异常值。",
        "使用多个超平面进行多分类。",
        "基于密度对数据进行聚类。"
    ],
    "What are the two necessary conditions for ensemble methods": [
        "基分类器必须复杂且在完整数据集上训练。",
        "基分类器必须彼此独立，且每个都必须优于随机猜测。",
        "基分类器必须使用相同的算法并在相同的数据上训练。",
        "基分类器必须具有零训练误差和高方差。"
    ],
    "In Bagging, when n is sufficiently large": [
        "0.5",
        "0.368",
        "0.632",
        "1.0"
    ],
    "Which of the following best describes the key difference between Bagging and Boosting": [
        "Bagging使用加权投票，而Boosting使用简单多数投票。",
        "Bagging并行独立训练基分类器，而Boosting顺序训练，专注于之前错误分类的实例。",
        "Bagging只适用于决策树，而Boosting适用于任何分类器。",
        "Bagging增加偏差，而Boosting增加方差。"
    ],
    "In AdaBoost, the importance (alpha) of a base classifier": [
        "α = ln(1/ε)",
        "α = ½ × ln((1 − ε) / ε)",
        "α = ε / (1 − ε)",
        "α = 1 − ε"
    ],
    "What happens if an intermediate round of AdaBoost produces an error rate greater than 50%": [
        "算法立即终止。",
        "权重回退至1/n并重复重采样过程。",
        "分类器被分配负权重。",
        "训练数据被随机打乱。"
    ],
    "What distinguishes Random Forest from standard Bagging": [
        "随机森林不使用自助采样。",
        "随机森林在自助采样基础上，还在每次分裂时随机选择特征子集。",
        "随机森林使用剪枝决策树，而Bagging使用未剪枝树。",
        "随机森林使用加权投票，而Bagging使用多数投票。"
    ],
    "Ensemble methods work best with what type of base classifiers": [
        "对训练数据变化不敏感的非常稳定的分类器。",
        "对训练集微小扰动敏感的不稳定分类器。",
        "具有非常高偏差的简单模型。",
        "预训练的深度学习模型。"
    ],
    "Given a transaction database of 5 transactions": [
        "3",
        "0.6",
        "0.4",
        "5/3"
    ],
    "Given the rule {Milk, Diaper}": [
        "2/5 = 0.4",
        "3/5 = 0.6",
        "2/3 ≈ 0.67",
        "3/2 = 1.5"
    ],
    "The Apriori principle states that": [
        "如果一个项集是频繁的，那么它的所有超集也一定是频繁的。",
        "如果一个项集是频繁的，那么它的所有子集也一定是频繁的。",
        "如果一个项集是非频繁的，那么它的所有子集也一定是非频繁的。",
        "支持度和置信度始终正相关。"
    ],
    "In the Apriori algorithm, candidate pruning works by": [
        "移除支持度计数低于阈值的候选。",
        "移除包含任何非频繁(k-1)-子集的候选k-项集。",
        "移除包含稀有项的所有项集。",
        "基于置信度值移除候选。"
    ],
    "What is the anti-monotone property of support": [
        "项集的支持度随着项的添加总是增加。",
        "项集的支持度永远不会超过其任何子集的支持度。",
        "支持度始终等于置信度。",
        "项集的支持度与其大小无关。"
    ],
    "If |L| = k (a frequent itemset of size k)": [
        "k",
        "2^k",
        "2^k − 2",
        "k! − 2"
    ],
    "Given Precision = 0.5 and Recall = 0.8": [
        "0.65",
        "0.625",
        "大约0.62",
        "0.80"
    ],
}

matched = 0
for q in data:
    question = q.get("question", "")
    if "question_zh" in q and q["question_zh"]:
        continue  # already has zh

    for key, zh in zh_map.items():
        if question.startswith(key) or key in question:
            q["question_zh"] = zh
            matched += 1
            break

    # Add options_zh for MCQ
    if q.get("type") == "MCQ" and "options_zh" not in q:
        for key, opts_zh in options_zh_map.items():
            if question.startswith(key) or key in question:
                q["options_zh"] = opts_zh
                break

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = len(data)
has_zh = sum(1 for q in data if q.get("question_zh"))
has_opts_zh = sum(1 for q in data if q.get("options_zh"))
print(f"Done! {matched} questions got question_zh (total: {has_zh}/{total})")
print(f"MCQ with options_zh: {has_opts_zh}")
