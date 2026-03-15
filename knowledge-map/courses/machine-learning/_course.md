# 机器学习 Machine Learning

> 名词总表 · 来源：ESL · ISLR · PML1 · PRML · scikit-learn

---

### 统计学习基础 Statistical Learning Foundations

| 名词 | 英文 |
|------|------|
| 监督学习 | Supervised Learning |
| 无监督学习 | Unsupervised Learning |
| 半监督学习 | Semi-Supervised Learning |
| 自监督学习 | Self-Supervised Learning |
| 偏差 | Bias |
| 方差 | Variance |
| 偏差-方差权衡 | Bias-Variance Tradeoff |
| 过拟合 | Overfitting |
| 欠拟合 | Underfitting |
| 泛化误差 | Generalization Error |
| 训练误差 | Training Error |
| 测试误差 | Test Error |
| 不可约误差 | Irreducible Error |
| 维度灾难 | Curse of Dimensionality |
| 没有免费午餐定理 | No Free Lunch Theorem |
| 奥卡姆剃刀 | Occam's Razor |
| 参数模型 | Parametric Model |
| 非参数模型 | Nonparametric Model |
| 生成式模型 | Generative Model |
| 判别式模型 | Discriminative Model |
| i.i.d. 假设 | i.i.d. Assumption |
| 损失函数 | [Loss Function](../deep-learning/loss_functions/) |
| 经验风险最小化 | Empirical Risk Minimization (ERM) |
| 结构风险最小化 | Structural Risk Minimization (SRM) |
| VC 维 | VC Dimension |

---

### 线性回归 Linear Regression

| 名词 | 英文 |
|------|------|
| 最小二乘法 | Ordinary Least Squares (OLS) |
| 正规方程 | Normal Equation |
| R² 决定系数 | Coefficient of Determination R² |
| 调整 R² | Adjusted R² |
| 残差 | Residual |
| 残差平方和 | Residual Sum of Squares (RSS) |
| 总平方和 | Total Sum of Squares (TSS) |
| 多重共线性 | Multicollinearity |
| 方差膨胀因子 | Variance Inflation Factor (VIF) |
| 异方差性 | Heteroscedasticity |
| 加权最小二乘 | Weighted Least Squares (WLS) |
| 广义线性模型 | Generalized Linear Models (GLM) |
| 连接函数 | Link Function |
| 指数族分布 | Exponential Family |
| [梯度下降](../deep-learning/optimizers/) | Gradient Descent |

---

### 逻辑回归 Logistic Regression

| 名词 | 英文 |
|------|------|
| Sigmoid 函数 | Sigmoid Function |
| 对数几率 | Logit / Log-Odds |
| 几率 | Odds |
| 几率比 | Odds Ratio |
| 最大似然估计 | Maximum Likelihood Estimation (MLE) |
| 决策边界 | Decision Boundary |
| [交叉熵损失](../deep-learning/loss_functions/) | Cross-Entropy Loss |
| IRLS | Iteratively Reweighted Least Squares |
| Softmax 回归 | Multinomial Logistic Regression |
| Probit 回归 | Probit Regression |

---

### 正则化与模型选择 Regularization & Model Selection

| 名词 | 英文 |
|------|------|
| 正则化 | Regularization |
| L1 正则化 | Lasso (L1 Regularization) |
| L2 正则化 | Ridge (L2 Regularization) |
| 弹性网 | Elastic Net |
| 正则化路径 | Regularization Path |
| 收缩 | Shrinkage |
| 稀疏性 | Sparsity |
| 特征选择 | Feature Selection |
| 前向选择 | Forward Selection |
| 后向消除 | Backward Elimination |
| AIC | Akaike Information Criterion |
| BIC | Bayesian Information Criterion |
| Cp 统计量 | Mallows' Cp |
| 交叉验证 | Cross-Validation (K-Fold / LOOCV) |
| 信息准则 | Information Criteria |

---

### 判别分析 Discriminant Analysis

| 名词 | 英文 |
|------|------|
| 线性判别分析 | LDA (Linear Discriminant Analysis) |
| 二次判别分析 | QDA (Quadratic Discriminant Analysis) |
| Fisher 判别 | Fisher's Linear Discriminant |
| 类间散布矩阵 | Between-Class Scatter Matrix |
| 类内散布矩阵 | Within-Class Scatter Matrix |
| 投影方向 | Projection Direction |

---

### 朴素贝叶斯 Naive Bayes

| 名词 | 英文 |
|------|------|
| 贝叶斯定理 | Bayes' Theorem |
| 条件独立假设 | Conditional Independence |
| 先验概率 | Prior Probability |
| 后验概率 | Posterior Probability |
| 似然函数 | Likelihood Function |
| 拉普拉斯平滑 | Laplace Smoothing |
| 高斯朴素贝叶斯 | Gaussian NB |
| 多项式朴素贝叶斯 | Multinomial NB |
| 伯努利朴素贝叶斯 | Bernoulli NB |

---

### K-近邻 K-Nearest Neighbors

| 名词 | 英文 |
|------|------|
| K 值 | K Value |
| 欧氏距离 | Euclidean Distance |
| 曼哈顿距离 | Manhattan Distance |
| Minkowski 距离 | Minkowski Distance |
| 余弦相似度 | Cosine Similarity |
| 惰性学习 | Lazy Learning |
| KD-Tree | KD-Tree |
| Ball Tree | Ball Tree |
| 距离加权 | Distance Weighting |

---

### 决策树 Decision Tree

| 名词 | 英文 |
|------|------|
| Gini 不纯度 | Gini Impurity |
| 信息熵 | Entropy |
| 信息增益 | Information Gain |
| 增益率 | Gain Ratio |
| CART 算法 | CART Algorithm |
| ID3 算法 | ID3 Algorithm |
| C4.5 算法 | C4.5 Algorithm |
| 递归二分法 | Recursive Binary Splitting |
| 预剪枝 | Pre-Pruning |
| 后剪枝 | Post-Pruning |
| 代价复杂度剪枝 | Cost-Complexity Pruning (CCP) |
| 特征重要性 | Feature Importance (MDI) |
| 置换重要性 | Permutation Importance |
| 回归树 | Regression Tree |
| 分类树 | Classification Tree |
| 代理分割 | Surrogate Split |

---

### 支持向量机 SVM

| 名词 | 英文 |
|------|------|
| 超平面 | Hyperplane |
| 间隔 | Margin |
| 最大间隔 | Maximum Margin |
| 支持向量 | Support Vectors |
| 硬间隔 | Hard Margin |
| 软间隔 | Soft Margin |
| 松弛变量 | Slack Variables |
| C 参数 | Regularization Parameter C |
| 核技巧 | Kernel Trick |
| 线性核 | Linear Kernel |
| 多项式核 | Polynomial Kernel |
| RBF 核 | Radial Basis Function Kernel |
| Sigmoid 核 | Sigmoid Kernel |
| Mercer 条件 | Mercer's Condition |
| 核矩阵 | Kernel Matrix (Gram Matrix) |
| 对偶问题 | Dual Problem |
| 拉格朗日乘子 | Lagrange Multipliers |
| KKT 条件 | KKT Conditions |
| SMO 算法 | SMO Algorithm |
| [铰链损失](../deep-learning/loss_functions/) | Hinge Loss |
| 支持向量回归 | SVR (Support Vector Regression) |
| ε-不敏感损失 | ε-Insensitive Loss |

---

### 集成方法 Ensemble Methods

| 名词 | 英文 |
|------|------|
| Bagging | Bootstrap Aggregating |
| Bootstrap 采样 | Bootstrap Sampling |
| 随机森林 | Random Forest |
| 特征随机子集 | Feature Subsampling / Max Features |
| 袋外误差 | Out-of-Bag Error (OOB) |
| Boosting | Boosting |
| AdaBoost | Adaptive Boosting |
| 梯度提升 | Gradient Boosting (GBDT) |
| 前向加法模型 | Forward Stagewise Additive Model |
| 残差拟合 | Residual Fitting |
| 学习率 / 收缩 | Learning Rate / Shrinkage |
| 子采样 | Subsampling (Stochastic GB) |
| XGBoost | Extreme Gradient Boosting |
| LightGBM | Light Gradient Boosting Machine |
| CatBoost | CatBoost |
| Stacking | Stacked Generalization |
| Voting | Majority / Soft Voting |
| Blending | Blending |
| 弱学习器 | Weak Learner |
| 强学习器 | Strong Learner |

---

### 聚类 Clustering

| 名词 | 英文 |
|------|------|
| 质心 | Centroid |
| K-Means | K-Means |
| K-Means++ | K-Means++ Initialization |
| WCSS | Within-Cluster Sum of Squares |
| Lloyd 算法 | Lloyd's Algorithm |
| 肘部法则 | Elbow Method |
| 轮廓系数 | Silhouette Coefficient |
| DBSCAN | DBSCAN |
| 核心点 | Core Point |
| 边界点 | Border Point |
| 噪声点 | Noise Point |
| ε 邻域 | ε-Neighborhood |
| MinPts | Minimum Points |
| 密度可达 | Density-Reachable |
| 密度相连 | Density-Connected |
| OPTICS | OPTICS |
| 层次聚类 | Hierarchical Clustering |
| 凝聚聚类 | Agglomerative Clustering |
| 分裂聚类 | Divisive Clustering |
| 谱聚类 | Spectral Clustering |
| 拉普拉斯矩阵 | Laplacian Matrix |
| 高斯混合模型 | Gaussian Mixture Model (GMM) |
| EM 算法 | Expectation-Maximization (EM) |
| E 步 | E-Step (Expectation) |
| M 步 | M-Step (Maximization) |
| 先验混合权重 | Mixing Coefficients |

---

### 异常检测 Anomaly Detection

| 名词 | 英文 |
|------|------|
| 局部离群因子 | LOF (Local Outlier Factor) |
| k-距离 | k-Distance |
| 可达距离 | Reachability Distance |
| 局部可达密度 | Local Reachability Density |
| LOF 得分 | LOF Score |
| 隔离森林 | Isolation Forest |
| 隔离树 | Isolation Tree (iTree) |
| 路径长度 | Path Length |
| 异常分数 | Anomaly Score |
| One-Class SVM | One-Class SVM |
| 马氏距离 | Mahalanobis Distance |

---

### 降维 Dimensionality Reduction

| 名词 | 英文 |
|------|------|
| 主成分分析 | PCA (Principal Component Analysis) |
| 协方差矩阵 | Covariance Matrix |
| 特征值分解 | Eigendecomposition |
| 奇异值分解 | SVD (Singular Value Decomposition) |
| 方差解释比 | Explained Variance Ratio |
| 白化 | Whitening |
| 核 PCA | Kernel PCA |
| 线性判别分析 | LDA (as dimensionality reduction) |
| t-SNE | t-Distributed Stochastic Neighbor Embedding |
| 困惑度 | Perplexity |
| UMAP | Uniform Manifold Approximation and Projection |
| 流形学习 | Manifold Learning |
| Isomap | Isometric Mapping |
| LLE | Locally Linear Embedding |
| MDS | Multidimensional Scaling |
| 因子分析 | Factor Analysis |
| 独立成分分析 | ICA (Independent Component Analysis) |

---

### 模型评估与度量 Model Evaluation & Metrics

| 名词 | 英文 |
|------|------|
| 准确率 | Accuracy |
| 精确率 | Precision |
| 召回率 | Recall |
| F1 分数 | F1 Score |
| 混淆矩阵 | Confusion Matrix |
| ROC 曲线 | ROC Curve |
| AUC | Area Under the Curve |
| PR 曲线 | Precision-Recall Curve |
| 对数损失 | Log Loss |
| 均方误差 | MSE (Mean Squared Error) |
| 均方根误差 | RMSE (Root MSE) |
| 平均绝对误差 | MAE (Mean Absolute Error) |
| R² 分数 | R² Score |
| 交叉验证 | Cross-Validation |
| K 折交叉验证 | K-Fold CV |
| 留一法 | LOOCV (Leave-One-Out CV) |
| 分层抽样 | Stratified Sampling |
| 自助法 | Bootstrap |
| 学习曲线 | Learning Curve |
| 验证曲线 | Validation Curve |
| 校准曲线 | Calibration Curve |
| Brier 分数 | Brier Score |

---

### 特征工程 Feature Engineering

| 名词 | 英文 |
|------|------|
| 特征缩放 | Feature Scaling |
| 标准化 | Standardization (Z-Score) |
| 归一化 | Normalization (Min-Max) |
| 独热编码 | One-Hot Encoding |
| 标签编码 | Label Encoding |
| 目标编码 | Target Encoding |
| 分箱 | Binning / Discretization |
| 多项式特征 | Polynomial Features |
| 特征交叉 | Feature Crossing |
| 缺失值处理 | Missing Value Imputation |
| 异常值处理 | Outlier Treatment |
| 特征选择 | Feature Selection |
| 过滤法 | Filter Methods |
| 包裹法 | Wrapper Methods |
| 嵌入法 | Embedded Methods |

---

### 超参数调优 Hyperparameter Tuning

| 名词 | 英文 |
|------|------|
| 网格搜索 | Grid Search |
| 随机搜索 | Random Search |
| 贝叶斯优化 | Bayesian Optimization |
| Hyperband | Hyperband |
| 早停 | Early Stopping |
| 学习率调度 | Learning Rate Scheduling |

---

### 贝叶斯方法 Bayesian Methods

| 名词 | 英文 |
|------|------|
| 贝叶斯推断 | Bayesian Inference |
| 先验分布 | Prior Distribution |
| 后验分布 | Posterior Distribution |
| 共轭先验 | Conjugate Prior |
| MAP 估计 | Maximum A Posteriori (MAP) |
| 贝叶斯线性回归 | Bayesian Linear Regression |
| 高斯过程 | Gaussian Process (GP) |
| 高斯过程回归 | GP Regression (Kriging) |
| 采集函数 | Acquisition Function |
| MCMC | Markov Chain Monte Carlo |
| 变分推断 | Variational Inference |
| 证据下界 | ELBO (Evidence Lower Bound) |

---

### 概率图模型 Probabilistic Graphical Models

| 名词 | 英文 |
|------|------|
| 有向图模型 | Directed Graphical Models (Bayesian Networks) |
| 无向图模型 | Undirected Graphical Models (MRFs) |
| 条件随机场 | CRF (Conditional Random Fields) |
| 隐马尔可夫模型 | HMM (Hidden Markov Model) |
| Viterbi 算法 | Viterbi Algorithm |
| 前向-后向算法 | Forward-Backward Algorithm |
| 信念传播 | Belief Propagation |
| 团 | Clique |
| 因子图 | Factor Graph |

---

### 核方法 Kernel Methods

| 名词 | 英文 |
|------|------|
| 核函数 | Kernel Function |
| 正定核 | Positive Definite Kernel |
| 再生核希尔伯特空间 | RKHS (Reproducing Kernel Hilbert Space) |
| 表示定理 | Representer Theorem |
| 核岭回归 | Kernel Ridge Regression |
| 核 PCA | Kernel PCA |
| [核 SVM](svm/) | Kernel SVM |
| 核密度估计 | KDE (Kernel Density Estimation) |
| 带宽 | Bandwidth |

---

### 采样与重抽样 Sampling & Resampling

| 名词 | 英文 |
|------|------|
| 自助法 | Bootstrap |
| 置换检验 | Permutation Test |
| 交叉验证 | Cross-Validation |
| 过采样 | Oversampling |
| 欠采样 | Undersampling |
| SMOTE | Synthetic Minority Oversampling |
| 类别不平衡 | Class Imbalance |
| 代价敏感学习 | Cost-Sensitive Learning |

---

### 模型可解释性 Model Interpretability

| 名词 | 英文 |
|------|------|
| SHAP 值 | SHAP (SHapley Additive exPlanations) |
| LIME | Local Interpretable Model-Agnostic Explanations |
| 部分依赖图 | PDP (Partial Dependence Plot) |
| 个体条件期望 | ICE (Individual Conditional Expectation) |
| 置换重要性 | Permutation Importance |
| 特征重要性 | Feature Importance (MDI) |
| Shapley 值 | Shapley Value |
| 全局可解释性 | Global Interpretability |
| 局部可解释性 | Local Interpretability |
| 模型无关方法 | Model-Agnostic Methods |

---

### Scikit-Learn 框架 Scikit-Learn Framework

| 名词 | 英文 |
|------|------|
| Estimator API | Estimator API |
| fit / predict / transform | Core Methods |
| Pipeline | Pipeline |
| ColumnTransformer | ColumnTransformer |
| GridSearchCV | Grid Search Cross-Validation |
| RandomizedSearchCV | Randomized Search CV |
| StandardScaler | StandardScaler |
| MinMaxScaler | MinMaxScaler |
| train_test_split | Train/Test Split |
| make_pipeline | make_pipeline |
| 自定义估计器 | Custom Estimator |
