# W9: Imbalance Class Problem (类不平衡问题)

## 1. Definitions (定义)

### Core Concepts (核心概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Class Imbalance Problem (类不平衡问题) | 分类数据集中各类别的样本量差异悬殊，导致传统评估指标失效的情况。 | 99%健康数据，1%罕见病数据 |
| Confusion Matrix (混淆矩阵) | 一个2x2的矩阵，展示分类模型在正类和负类预测上的绝对数量（真阳/真阴/假阳/假阴）。 | TP=10, FN=0, FP=500, TN=490 |
| Precision (精确率) | 模型预测为正类的样本中，真实为正类的比例，用来衡量模型"不误杀"的能力。 | 预测诈骗的电话里，多少是真的诈骗 |
| Recall / TPR (召回率/真正侧率) | 真实正类样本中，被模型正确找出的比例，用来衡量模型"不漏找"的能力。 | 所有的病患里，找出了多少人 |
| FPR (假正侧率) | 真实负类样本中，被错误预测为正类的比例。由于误报而付出的代价。 | 所有健康人里，多少人被误诊有病 |
| F-measure / F1-score (F1分值) | Precision 和 Recall 的调和平均数，在两者之间取得平衡的单项指标。 | F=0.67 (避免极端高Recall低Precision) |
| ROC Curve (受试者工作特征曲线) | 以 FPR 为横坐标，TPR 为纵坐标，展示分类器在所有可能判定阈值下性能表现的全局评估曲线。 | 寻找诊断系统的最佳灵敏度旋钮 |
| AUC (ROC曲线下面积) | ROC曲线下的积分面积(0.5到1.0之间)，用于整体量化并客观比较两个分类器的性能。 | AUC=0.9 的分类器强于 AUC=0.7 |

### Sampling & Anomaly Detection (采样与异常检测)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Undersampling (欠采样) | 随机删除绝大部份多数类记录，强行让正负样本数量均衡的方法。 | 扔掉9000条正常交易，保留1000条正常和欺诈1:1 |
| Oversampling (过采样) | 简单粗暴地复制少数类记录，强行让正负样本数量均衡的方法（易致过拟合）。 | 复制欺诈交易9次以赶超正常记录 |
| SMOTE (少数类合成过采样技术) | 不仅是复制，而是通过在相近的少数类样本间进行线性连线插值，凭空合成全新的虚拟样本。 | 在两张病变图特征见插值出一张新特征图 |
| Anomaly Detection (异常检测) | 放弃分类器思想，通过寻找偏高概率模型、距离或密度的点来识别偏离常规数据特征的过程。 | 从日常记录中找出千分之一血压极高的病人 |
| LOF (局部离群因子) | 一种密度法，如果一个点自身的局部邻域密度比其周围所有邻居的密度都要低得多，则被判定为孤立离群点。 | 真空地带的孤立天体 |
| Reconstruction Error (重构误差) | 数据经过PCA/Autoencoder降维压缩后再还原回原空间时，原始数据和还原后数据的差异度（异类难以完美还原）。 | 喂给正常照片训练的编码器一张猫图，还原时失真大 |
| One-Class SVM / OCSVM (单类支持向量机) | 将无监督数据通过高斯核投射到高维只占据一角，并用分离超平面隔离它们与原点的无监督防御边界技术。 | 画一个包裹所有好人的紧圈，圈外全当坏人 |

## 2. Comparisons (对比)

### Evaluation Metrics (评价指标对比)

| Dimension (维度) | Accuracy (准确率) | Precision / Recall / F-measure | ROC & AUC | Example (示例) |
|-----------|---|---|---|---------|
| Focus (关注点) | 整体所有类别的判断正确率 | 专门聚焦在正类/少数类上的表现 | 全局视野下的所有阈值的博弈表现 | 评价模型抓小偷的能力 |
| Impact of Imbalance (不平衡影响) | 极易被误导 (瞎蒙多数也有99%高分) | 公平 (关注小众是否真正被查出) | 客观 (曲线不受少数类样本量的骗) | 1个小偷+99个好人 |
| Threshold (阈值依赖) | 强依赖固定阈值（如0.5） | 强依赖固定阈值 | 展示各阈值连贯画卷，不依赖单一阈值 | 雷达敏感度调高调低 |

### Sampling Methods (重采样方法对比)

| Dimension (维度) | Undersampling (欠采样) | Oversampling (过采样) | SMOTE (合成过采样) | Example (示例) |
|-----------|---|---|---|---------|
| Operation (操作) | 剪除大多数样本 | 简单复制少数样本 | 人工合成新特质少数样本 | 解决 1:100 数据失衡 |
| Danger (风险/缺点) | 信息丢失 (可能扔掉重要特征) | 过拟合死记硬背 (完全没泛化力) | k个邻居若找不到将无法插值 | 模型遇到新变形样本的盲区 |
| Effectiveness (效果) | 降低训练运算量，但易抛弃规律 | 训练集高分但测试极易翻车 | 增加了真实的决策泛化边界分布 | 在边界更精细地训练 |

### Anomaly Detection Strategies (异常检测策略对比)

| Strategy (检测流派) | Core Logic (核心判定逻辑) | Benefit/Drawback (优缺点) | Example (示例) |
|-----------|---|---|---------|
| Statistical (统计法) | 违背了先验概率分布(如偏离高斯钟形曲线老远) | 强依赖分布假设是否正确 | Grubbs' Test |
| Proximity (邻近日法) | 计算自己离周围k个最近邻居的距离特别遥远 | 计算量大(O(N²)) | 距离最近邻 1000米外 |
| Density (密度LOF) | 周围区域空旷程度远超隔壁邻居所在区域的空挤 | 能应对密度不均匀的不同集群簇 | 贫民窟(密)旁边的独栋(疏) |
| Reconstruction (重构法) | 原本只能压缩"人"脸，丢入"猫"脸会导致极高还原误差 | 非线性降维(Autoencoder)抓潜特质强 | PCA降维复原前后的差异 |
| OCSVM (单类SVM) | 超平面不区分两类，只努力把所有正常数据推离中心原点 | 核函数威力无穷，对未知异常鲁棒极高 | 未知入侵病毒检测 |

## 3. Formulas (公式)

### Confusion Matrix Formulas (混淆矩阵评估公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$ | 所有判断对的 / 总体样本 | 连小偷带好人全测准的占比 |
| $Precision = \frac{TP}{TP + FP}$ | 预测真正且属实的 / 所有被预测为真的 | 被抓的人里多少真有罪 |
| $Recall(TPR) = \frac{TP}{TP + FN}$ | 预测真正且属实的 / 所有客观属实的 | 所有罪犯多少被落网了 |
| $FPR = \frac{FP}{FP + TN}$ | 预测出错的假正类 / 所有客观存在的负类 | 好人被冤枉的几率 |
| $F_1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}$ | 调和平均值，任何一个接近0都会拉低总体 | P=1 但 R=0.1，F1=0.18 |

### Anomaly Detection Formulas (异常检测计算)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $density(x, k) = \frac{1}{dist(x, k)}$ | 局部密度：到第k个邻居绝对距离的倒数 | 距离越大，密度越小 |
| $RelativeDensity = \frac{\sum density(y_i, k) / k}{density(x, k)}$ | 相对密度LOF：邻居平均密度 除以 x自己的密度 | LOF ≫ 1 代表x是孤立异常点 |
| $Reconstruction\_Error(x) = \|x - \hat{x}\|$ | 重构误差：原始向量 $x$ 与降维再展开后的 $\hat{x}$ 的范数差 | 误差极大表明模型未见过此物 |

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------|
| _No practical content this week._ | _(Weekly lab materials do not explicitly focus on imbalanced class coding experiments)_ | _N/A_ |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------|
| Using Accuracy for rare class | 考题问："1000个良品1个次品，机器全判良品，准确率99.9%代表机器很好"？错！Accuracy 被多数人绑架，彻底遮蔽了抓次品的失败。应该用 Recall / F1。 | 回答应指责全答No的模型是个废柴 |
| ROC diagonal line | 考题问："ROC曲线下面积(AUC)最差是0吗？" 错！对角线的瞎蒙 AUC是 0.5。若 AUC<0.5，说明分类器在反向做恶，你只要反向预测就能超过0.5。 | AUC=1才是上帝视觉。|
| Single Point ROC comparison | 考题问："如果两条 ROC 曲线交叉了，A在左下比B好，B在右上比A好，怎么选模型？" 答：没有绝对的好，取决于你能忍受的 FPR (冤枉人的代价)。但客观对比可求两曲线的 AUC。 | 宁可抓错不放过的安检选右上角能力强的模型 |
| SMOTE vs Oversampling | 考题问："SMOTE是否就是复制一堆极少类防止过拟合？" 错！SMOTE 不是纯复制，它是通过在少数类和近邻特征做连线差分乘以随机数，合成"从未见过的新实例"。| 不产生一模一样的猫，而是产生合成猫图 |
| OCSVM mechanism | 考题问："OCSVM 是把少数异常类与多数正常类之间切一刀？" 错！OCSVM 训练时【并没有】异常类的标签！它是通过将高维所有的好数据强塞并与（原点）切割切出边界防护墙。 | 纯无监督防御隔离 |
