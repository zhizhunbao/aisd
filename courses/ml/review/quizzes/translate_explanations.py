"""
Replace explanation_zh with full Chinese translations of the English explanation.
Also update index.html: show options_zh, remove hint display.
"""
import json, re, os

# Strip HTML tags for readability in translations
def strip_html(s):
    return re.sub(r'<[^>]+>', '', s)

# Full Chinese translations keyed by file, indexed by question order
TRANSLATIONS = {
    "midterm_quiz.json": [
        # Q1-Q10 (TF)
        "<strong>特征选择</strong>从现有特征中挑选子集（不创建新特征）。<strong>特征提取</strong>（如PCA、LDA）通过变换/组合原始特征来创建新的合成特征。它们是根本不同的方法。",
        "<strong>等宽</strong>分箱将范围划分为等宽的区间。<strong>等频（等深）</strong>分箱划分数据使每个箱包含大致相同数量的数据点。",
        "SVM<strong>最大化</strong>间隔（到最近点——支持向量的距离），而不是最小化。",
        "核技巧使用核函数 K(xᵢ, xⱼ) = φ(xᵢ)·φ(xⱼ) 在高维空间中计算点积，而无需显式计算 φ(x)。",
        "在CNN中，滤波器权重通过反向传播<strong>在训练过程中学习</strong>。像Sobel这样的预定义滤波器用于传统图像处理，而不是学习型卷积。",
        "BPTT确实展开RNN并应用反向传播。然而，RNN在所有时间步上<strong>共享权重</strong>；梯度在所有时间步上<strong>累积</strong>，然后用于一次权重更新。",
        "条件独立意味着 P(X,Y|Z) = P(X|Z)·P(Y|Z)。这与边际独立不同。两个边际独立的变量在条件化后可能变得依赖（\"解释消除\"效应）。",
        "如果某个特征不相关，其条件概率 P(xᵢ|C) 对所有类别大致相同，因此贡献相等并有效抵消。",
        "不同的算法（K-Means、DBSCAN、层次聚类）有不同的假设（形状、密度、连通性），通常会产生不同的聚类结果。",
        "<strong>MIN（单链接）</strong>使用<strong>最近</strong>点之间的距离。<strong>MAX（完全链接）</strong>使用最远点之间的距离。",
        # Q11-Q20 (MCQ)
        "将连续变量转换为离散类别（箱）称为<strong>分箱</strong>（也称为离散化）。",
        "总方差 = 3.2 + 1.1 + 0.4 + 0.1 = 4.8。比例 = 3.2 / 4.8 = 0.667 ≈ <strong>67%</strong>。",
        "PCA按解释的方差排序；LDA按判别力排序。(a) 错误：LDA是有监督的；(c) 仅限LDA；(d) LDA最多产生 C-1 个成分。",
        "硬间隔SVM找到具有<strong>最大间隔</strong>的超平面——到任一类别最近数据点的最大垂直距离。",
        "SVM内存效率高（仅存储支持向量），在高维空间中有效。不适用于超大数据集，不可解释，需要调参（C、kernel、γ）。",
        "决策边界由 w·x + b = 0 定义。超平面上的任何点都满足此方程。",
        "对于 224×224×3 的图像，全连接层每个神经元需要 150,528 个权重。这就是CNN使用局部连接和权重共享的原因。",
        "'Same' 填充保持空间维度不变 → 32×32。10个滤波器 → 深度 = 10。输出：<strong>32×32×10</strong>。",
        "浅层学习简单的低级特征（边缘、纹理）。深层将这些组合成越来越复杂/抽象的表示。",
        "权重共享意味着在每个时间步使用相同的 Wₓ、Wₕ，因此网络可以处理任意长度的序列，并在不受位置影响的情况下识别模式。",
        # Q21-Q30 (MCQ continued)
        "在BPTT过程中，梯度涉及 ∂hₜ/∂hₜ₋₁ 的重复乘法。如果这些值 < 1，乘积指数级缩小 → 梯度消失。",
        "隐藏状态组合了：当前输入 xₜ（乘以 Wₓ）、前一个隐藏状态 hₜ₋₁（乘以 Wᵧ），通过非线性激活函数 f。",
        "贝叶斯定理：<strong>后验 = (似然 × 先验) / 证据</strong> = P(X|Y)·P(Y) / P(X)。",
        "拉普拉斯平滑：P(xᵢ|C) = (count(xᵢ,C) + 1) / (count(C) + |V|)，其中 |V| 是不同值的数量。",
        "朴素贝叶斯假设<strong>条件独立</strong>。高度相关/冗余的特征违反此假设并降低性能（重复计算证据）。",
        "NB将所有条件概率相乘。如果任何 P(xᵢ|C) = 0，整个乘积变为0。这就是拉普拉斯平滑解决的零频率问题。",
        "在基于原型的聚类（如K-Means）中，每个簇由质心（原型）表示，每个点属于质心最近的簇。",
        "在 O(n·K·I·d) 中：n = 点数，K = 簇数，I = 迭代次数，d = 维度（属性）数量。",
        "层次聚类构建树状图——可以在任何层级切割。K-Means需要预先指定K。",
        "DBSCAN：<strong>核心点</strong>在ε范围内有 ≥ MinPts 个邻居；<strong>边界点</strong> < MinPts 但可从核心点到达；<strong>噪声</strong>两者都不是。",
        # Q31-Q34 (Short)
        "'Same' 填充保持空间维度不变。池化不改变深度。全连接层参数 = 输入维度 × 输出维度 + 偏置。",
        "回归任务使用MSE；分类任务使用交叉熵。序列→序列 = 多对多；序列→标签 = 多对一。",
        "使用链式法则 + DAG条件独立性：F是根节点 → P(F)；E仅依赖F → P(E|F)；C仅依赖F → P(C|F)；M依赖E和C → P(M|E,C)。",
        "MAX（完全链接）使用两个簇之间最远点的距离。先合并最近的一对，然后使用MAX规则更新距离矩阵。",
    ],
    "week09_quiz.json": [
        "在不平衡数据集中，<strong>准确率具有误导性</strong>。例如，10个正样本和990个负样本，预测全部为负类可获得99%准确率但检测不到任何正样本。应使用<strong>精确率、召回率、F1值</strong>。",
        "过采样通过<strong>复制</strong>少数类实例来工作。简单但有过拟合风险。改进版本 = SMOTE。",
        "SMOTE不使用\"复制+噪声\"。它通过在少数类实例与其<strong>k近邻</strong>之间的线段上进行<strong>插值</strong>来生成合成实例。",
        "随机猜测模型沿ROC曲线的对角线，AUC = 0.5。完美模型的AUC = 1.0。",
        "<strong>FP（假阳性）</strong>：实际为负类但被预测为正类。<br>TP = 正确预测的正类，FP = 误报（I型错误），FN = 漏检（II型错误），TN = 正确预测的负类。",
        "F1 = 2pr / (p + r) 是精确率和召回率的<strong>调和平均</strong>。(a) 是算术平均；(d) 是准确率公式。",
        "ROC曲线：x轴 = <strong>FPR</strong> = FP/(FP+TN)，y轴 = <strong>TPR</strong> = TP/(TP+FN) = 召回率。好的模型接近左上角。",
        "SMOTE通过沿连接少数类最近邻的<strong>线段进行插值</strong>来生成合成实例。(a) = 欠采样，(b) = 简单过采样。",
        "LOF：relative_density(x,k) = (邻居的平均密度) / (x的密度)。值 ≫ 1 表示x的密度远低于其邻居 → <strong>强异常值</strong>。值 ≈ 1 → 正常。",
        "OCSVM仅使用正常数据学习边界。f(x) ≥ 0 → 正常，f(x) < 0 → 异常值。<strong>ν参数</strong>控制异常值比例的上限。",
        "F1 = 2 × 0.5 × 0.8 / (0.5 + 0.8) = 0.8 / 1.3 ≈ <strong>0.615 ≈ 0.62</strong>。",
        "在不平衡数据中，准确率具有误导性。F1（0.727）比准确率（97%）更真实地反映模型性能。FPR在医学检测中代表健康患者的误诊率。",
        "在不平衡数据中，即使准确率为99%，少数类召回率也可能为<strong>0%</strong>（预测全部为多数类）。",
        "三种检测方法各适用于不同场景。OCSVM使用ν控制边界松紧。基于重建的方法假设正常数据具有低维模式。",
    ],
    "week10_quiz.json": [
        "Bagging使用<strong>有放回</strong>抽样。大约63.2%的原始数据被包含在每个自助样本中。",
        "在AdaBoost中，<strong>误分类</strong>实例的权重增加，正确分类的权重降低。下一轮专注于难样本。",
        "随机森林 = <strong>Bagging + 随机特征子集</strong>。(1) 自助抽样 (2) 每个节点随机选择p个特征子集。两种随机性确保树的多样性。",
        "集成方法优于单个分类器的条件：① 基分类器相互<strong>独立</strong> ② 每个分类器的错误率<strong>小于0.5</strong>（优于随机猜测）。",
        "P(被包含) = 1 − (1−1/n)^n → 1 − 1/e ≈ 1 − 0.368 = <strong>0.632</strong>（约63.2%）。",
        "<strong>Bagging</strong>：并行独立学习 → 降低方差。<strong>Boosting</strong>：顺序学习，专注前一轮的错误 → 降低偏差。",
        "α = ½ × ln((1−ε)/ε)。更低的ε（更准确）→ 更大的α → 更大的投票权重。当ε = 0.5时，α = 0。",
        "错误率 > 50% 意味着比随机猜测还差 → 权重<strong>重置为1/n</strong>并重复重采样。它<strong>不会终止</strong>！",
        "随机森林 = Bagging + 每次分裂时的<strong>随机特征子集</strong>选择。双重随机性降低了树之间的相关性。",
        "集成方法与<strong>不稳定</strong>分类器（如未剪枝决策树、ANN）配合效果最好。稳定分类器（如kNN）收效甚微。",
        "集成方法<strong>不可解释</strong>！解释投票过程 ≠ 可解释性。用户想知道\"<strong>为什么</strong>\"做出某个决定，而不是\"10个医生投票了\"。",
        "在Bagging中样本被同等对待。但在Boosting中，权重<strong>每轮更新</strong>——误分类的增加，正确分类的减少。",
        "有放回抽样意味着特定实例可能被遗漏。当n足够大时，每个自助样本仅包含约<strong>63.2%</strong>的原始数据。",
        "当错误率 > 50% 时，算法<strong>不会终止</strong>。相反，权重<strong>重置为1/n</strong>并重复重采样。",
        "随机森林使用<strong>未剪枝</strong>的决策树。教授说过：\"基分类器是未剪枝的……我们不做任何后剪枝。\"",
        "AdaBoost使用<strong>加权多数投票</strong>。α更大的分类器有更大的投票权重。简单多数投票用于Bagging，不是AdaBoost。",
        "集成方法与<strong>不稳定</strong>分类器（如未剪枝决策树、ANN）配合最有效。稳定分类器（kNN）即使数据变化也几乎不变，因此集成收效甚微。",
        "恰恰<strong>相反</strong>！<strong>Bagging</strong>降低方差。<strong>Boosting</strong>降低偏差。",
        "Bagging减少方差（并行、独立）。Boosting减少偏差（顺序、专注错误）。必须会算α公式。多数投票 = 计票。",
        "AdaBoost核心：误分类权重上升(e^(+α))，正确分类权重下降(e^(-α))。教授用\"轮盘赌\"类比来解释加权抽样。",
        "解释多数投票 ≠ 可解释性。用户想知道每个分类器为什么做出其决定，而不仅仅是10个投票了。即使单个分类器在数百个特征和数百万数据点下也难以解释，更不用说10个。集成方法不可解释——这是其主要局限性。",
    ],
    "week11_quiz.json": [
        "该表述描述的是<strong>支持度</strong>的定义，而非置信度。<strong>置信度</strong> = σ(X∪Y) / σ(X)（除以X的计数，而非总交易数）。",
        "这是Apriori原理的<strong>逆否命题</strong>：非频繁项集 → 所有超集也非频繁。基于支持度的<strong>反单调性</strong>——随着项集增大，支持度只会保持不变或下降。",
        "来自同一频繁项集的规则具有<strong>相同的支持度</strong>（相同的并集频率），但<strong>不同的置信度</strong>（不同的分母）。",
        "支持度 = σ(项集) / |T| = 3/5 = <strong>0.6</strong>。选项(a)给出的是支持度计数（绝对计数），而非支持度（比率）。",
        "置信度 = σ(X∪Y)/σ(X) = σ({M,D,B})/σ({M,D}) = 2/3 ≈ <strong>0.67</strong>。支持度 = 2/5 = 0.4。",
        "频繁项集的所有<strong>子集</strong>也是频繁的。逆否命题：非频繁项集的所有超集都是非频繁的。(a) 方向反了——超集不一定频繁。(c) 子集方向错误。",
        "候选剪枝：如果候选k-项集的任何(k-1)-子集是<strong>非频繁</strong>的，则移除该候选。(a) 描述的是支持度计数步骤；(d) 描述的是规则生成步骤。",
        "反单调性：随着项集增大，支持度只会保持不变或下降。∀X⊆Y: s(X) ≥ s(Y)。这是Apriori剪枝的数学基础。",
        "候选关联规则数 = <strong>2^k − 2</strong>。从总子集数2^k中减去两条平凡规则：∅→L 和 L→∅。",
        "关联规则<strong>不</strong>代表因果关系——它们表示<strong>共现/相关性</strong>。教授多次强调：\"它只是显示相关性。不是因果关系。\"",
        "关联规则挖掘<strong>不考虑数量或顾客身份</strong>。教授说过：\"我们没有价格……数量……关于顾客的什么都没有。\"仅关注商品是否存在（是/否）。",
        "D个商品的可能项集数 = 2^D − 1。即使6个商品也会产生602条规则。教授说过：\"这种暴力搜索没有意义。\"",
        "顺序<strong>反了</strong>！正确的是：第1步 = <strong>频繁项集生成（支持度）</strong> → 第2步 = <strong>规则生成（置信度）</strong>。",
        "候选生成规则：合并两个前<strong>(k-2)个项相同</strong>的频繁(k-1)-项集。例如 {A,B,C} + {A,B,D} → {A,B,C,D}。",
        "Apriori的核心：利用反单调性在<strong>计算支持度之前</strong>剪枝候选。如果(k-1)-子集非频繁 → 直接移除候选，无需计算支持度。",
        "Apriori剪枝：{A,D}非频繁 → 超集{A,B,D}和{A,C,D}直接剪掉，无需计算支持度。支持度和置信度的分母不同！",
        "两种相反的摆放策略是教授强调的：近距离（便利）vs 远距离（增加浏览/购买）。关联规则不是静态的——随着模式变化需要定期更新。",
    ],
}

def process_file(filepath, translations):
    fname = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        quizzes = json.load(f)

    if len(quizzes) != len(translations):
        print(f"  [ERROR] {fname}: {len(quizzes)} questions but {len(translations)} translations!")
        return 0

    changes = 0
    for i, q in enumerate(quizzes):
        q['explanation_zh'] = translations[i]
        changes += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, ensure_ascii=False, indent=2)

    print(f"  [OK] {fname}: {changes} explanation_zh updated")
    return changes

def main():
    quiz_dir = os.path.dirname(os.path.abspath(__file__))
    total = 0
    for fname, translations in TRANSLATIONS.items():
        filepath = os.path.join(quiz_dir, fname)
        if not os.path.exists(filepath):
            print(f"  [SKIP] {fname} not found")
            continue
        total += process_file(filepath, translations)
    print(f"\nDone! Total updated: {total}")

if __name__ == '__main__':
    main()
